"""Deterministic structural graph of the docs corpus (plan 0009 row G; plan 0015 G2).

Nodes are docs (with bucket, status and title); edges are the links between them,
aggregated per (source, target, kind) with the line numbers and section fragments
they occur on (the coverage checks use these). ``site_graph`` projects this onto the
slim shape the Pages site loads: docs with their hubs, one edge per linked pair.
External links produce no node or edge. No LLM and no network: the same corpus always yields
byte-identical JSON, which is what makes the graph reproducible and traceable.

Link *validity* is not checked here — lychee already does that in CI. A link whose
target is outside the corpus (repo-root files, the archive) simply produces no edge.

Pure logic except ``load_corpus``, the only function that touches the filesystem.
"""
from __future__ import annotations

import json
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit

from .doc_status import extract_frontmatter, frontmatter_status

_FENCE = re.compile(r"^\s*(```|~~~)")
_INLINE_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
_REF_DEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?\s*$")
_TITLE_KEY = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
_H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
_SUBDIR_SECTIONS = ("cc-native", "non-cc")
_HUB_BUCKET = "_topics"
_HUB_INDEX = "docs/_topics/README.md"
_ARCHIVE = "docs/archive/"
_DOC_TYPES = ("analysis", "landscape", "reference", "spec", "runbook")
_PLATFORMS = re.compile(r"^platform_scope:\s*\[(.*)\]\s*$", re.MULTILINE)
_DATE_KEYS = {k: re.compile(rf"^{k}:\s*(\d{{4}}-\d{{2}}-\d{{2}})\s*$", re.MULTILINE)
              for k in ("created", "updated")}
_PURPOSE = re.compile(r"^purpose:\s*(.+?)\s*$", re.MULTILINE)
_CC_BUCKETS = ("cc-native", "cc-community")


def bucket_of(path: str) -> str:
    """Corpus bucket of a repo-relative doc path (``non-cc/frameworks``, ``_topics``, ...)."""
    parts = path.split("/")
    if len(parts) <= 2:
        return "docs"
    if parts[1] in _SUBDIR_SECTIONS and len(parts) > 3:
        return f"{parts[1]}/{parts[2]}"
    return parts[1]


def doc_status(text: str) -> str | None:
    """Doc status from frontmatter ``status:`` (body badges are rejected by check_status)."""
    return frontmatter_status(text)


def doc_title(text: str, path: str) -> str:
    """Frontmatter ``title:``, else the first H1, else the file stem."""
    fm = extract_frontmatter(text)
    m = _TITLE_KEY.search(fm) if fm else None
    if m:
        return m.group(1).strip().strip("\"'")
    m = _H1.search(text)
    return m.group(1) if m else posixpath.splitext(posixpath.basename(path))[0]


def doc_type(path: str) -> str:
    """Doc type from the filename suffix (``-analysis``, ``-landscape``, ...), else ``other``."""
    stem = posixpath.splitext(posixpath.basename(path))[0]
    suffix = stem.rsplit("-", 1)[-1] if "-" in stem else ""
    return suffix if suffix in _DOC_TYPES else "other"


def doc_platforms(text: str, path: str) -> list[str]:
    """``platform_scope`` slugs; Claude Code docs without one get ``claude-code`` from their folder."""
    fm = extract_frontmatter(text)
    m = _PLATFORMS.search(fm) if fm else None
    if m:
        return [v.strip() for v in m.group(1).split(",") if v.strip()]
    return ["claude-code"] if bucket_of(path).split("/")[0] in _CC_BUCKETS else []


def doc_dates(text: str) -> dict[str, str | None]:
    """Frontmatter ``created`` and ``updated`` as ISO date strings, ``None`` when absent or malformed."""
    fm = extract_frontmatter(text) or ""
    return {k: (m.group(1) if (m := rx.search(fm)) else None) for k, rx in _DATE_KEYS.items()}


def doc_purpose(text: str) -> str | None:
    """Frontmatter ``purpose:`` one-liner (surrounding quotes dropped), else ``None``."""
    fm = extract_frontmatter(text)
    m = _PURPOSE.search(fm) if fm else None
    return m.group(1).strip("\"'") if m else None


def extract_links(text: str) -> list[tuple[str, int]]:
    """``(target, line)`` for every inline and reference-style link outside code fences."""
    links: list[tuple[str, int]] = []
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        targets = _INLINE_LINK.findall(line)
        ref = _REF_DEF.match(line)
        if ref:
            targets.append(ref.group(1))
        links.extend((t, lineno) for t in targets if not t.startswith("#"))
    return links


def resolve(source: str, target: str) -> tuple[str, str | None] | None:
    """Resolve a relative ``.md`` link from ``source`` to ``(path, fragment)``; anything else is ``None``."""
    parts = urlsplit(target)
    if parts.scheme or not parts.path.endswith(".md") or parts.path.startswith("/"):
        return None
    path = posixpath.normpath(posixpath.join(posixpath.dirname(source), parts.path))
    return path, parts.fragment or None


def _doc_node(path: str, text: str) -> dict:
    return {"id": path, "type": "doc", "bucket": bucket_of(path), "status": doc_status(text),
            "title": doc_title(text, path), "doc_type": doc_type(path),
            "platforms": doc_platforms(text, path), "purpose": doc_purpose(text), **doc_dates(text)}


def _add_link(edges: dict, docs: dict, source: str, target: str, line: int) -> None:
    """Record one link from ``source`` on its aggregated edge, if it lands in the corpus."""
    resolved = resolve(source, target)
    if resolved is None or resolved[0] not in docs:
        return
    target_id, fragment = resolved
    kind = "hub" if bucket_of(source) == _HUB_BUCKET else "link"
    agg = edges.setdefault((source, target_id, kind), {"lines": [], "fragments": set()})
    agg["lines"].append(line)
    if fragment:
        agg["fragments"].add(fragment)


def build_graph(docs: dict[str, str]) -> dict:
    """Build the graph dict (``nodes``, ``edges``) from ``{repo-relative path: text}``."""
    nodes = {path: _doc_node(path, docs[path]) for path in docs}
    edges: dict[tuple[str, str, str], dict] = {}
    for source in sorted(docs):
        for target, line in extract_links(docs[source]):
            _add_link(edges, docs, source, target, line)
    return {
        "nodes": [nodes[k] for k in sorted(nodes)],
        "edges": [
            {"source": s, "target": t, "kind": k,
             "lines": sorted(v["lines"]), "fragments": sorted(v["fragments"])}
            for (s, t, k), v in sorted(edges.items())
        ],
    }


def site_graph(graph: dict, filing: dict[str, str] | None = None) -> dict:
    """Slim projection for the Pages site: each doc's title, bucket, hubs and facets (status,
    doc type, platforms, purpose, created, updated), one edge per linked pair.

    A doc's hubs are the topic hubs (``_topics/*`` except the hub index) with a row
    linking to it, counted once even when several rows point at its sections.
    ``filing`` (``doc_coverage.hub_filing``, passed in to keep this module free of the
    coverage rules) adds each doc's hub state so the site splits "no hub" the way
    ``check_coverage`` does.
    """
    hubs: dict[str, set] = {}
    pairs = set()
    for e in graph["edges"]:
        if e["source"] == e["target"]:
            continue
        if e["kind"] == "hub" and e["source"] != _HUB_INDEX:
            hubs.setdefault(e["target"], set()).add(e["source"])
        pairs.add(tuple(sorted((e["source"], e["target"]))))
    nodes = [{"id": n["id"], "title": n["title"], "bucket": n["bucket"],
              "hubs": sorted(hubs.get(n["id"], ())), "status": n["status"],
              "doc_type": n["doc_type"], "platforms": n["platforms"], "purpose": n["purpose"],
              "created": n["created"], "updated": n["updated"]} for n in graph["nodes"]]
    for n in nodes if filing else ():
        n["filing"] = filing[n["id"]]
    return {"nodes": nodes, "edges": [list(p) for p in sorted(pairs)]}


def to_json(graph: dict) -> str:
    """Deterministic JSON serialization (sorted keys, trailing newline)."""
    return json.dumps(graph, sort_keys=True, indent=1, ensure_ascii=False) + "\n"


def load_corpus(root: Path) -> dict[str, str]:
    """Read every ``docs/**/*.md`` under ``root`` except the archive, keyed by repo-relative path."""
    root = Path(root)
    corpus = {}
    for path in sorted((root / "docs").rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        if not rel.startswith(_ARCHIVE):
            corpus[rel] = path.read_text(encoding="utf-8")
    return corpus
