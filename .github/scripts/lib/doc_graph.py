"""Deterministic structural graph of the docs corpus (plan 0009 row G, option B; #504).

Nodes are docs (with bucket, status and title) and the external domains they cite;
edges are the links between them, aggregated per (source, target, kind) with the
line numbers they occur on. No LLM and no network: the same corpus always yields
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

from .doc_status import extract_frontmatter, frontmatter_status, preamble_badge

_FENCE = re.compile(r"^\s*(```|~~~)")
_INLINE_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
_REF_DEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?\s*$")
_TITLE_KEY = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
_H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
_BADGE_CUT = re.compile(r"\s+(?:\(|—|–|-\s)|[;,]")
_SUBDIR_SECTIONS = ("cc-native", "non-cc")
_HUB_BUCKET = "_topics"
_ARCHIVE = "docs/archive/"


def bucket_of(path: str) -> str:
    """Corpus bucket of a repo-relative doc path (``non-cc/frameworks``, ``_topics``, ...)."""
    parts = path.split("/")
    if len(parts) <= 2:
        return "docs"
    if parts[1] in _SUBDIR_SECTIONS and len(parts) > 3:
        return f"{parts[1]}/{parts[2]}"
    return parts[1]


def _normalize_badge(badge: str) -> str:
    """``Research Preview — beta`` -> ``research-preview`` (the badge's leading token)."""
    head = _BADGE_CUT.split(badge, maxsplit=1)[0]
    return "-".join(head.strip().lower().split())


def doc_status(text: str) -> str | None:
    """Doc status: frontmatter ``status:`` if present, else the normalized preamble badge."""
    status = frontmatter_status(text)
    if status is not None:
        return status
    badge = preamble_badge(text)
    return _normalize_badge(badge) if badge else None


def doc_title(text: str, path: str) -> str:
    """Frontmatter ``title:``, else the first H1, else the file stem."""
    fm = extract_frontmatter(text)
    m = _TITLE_KEY.search(fm) if fm else None
    if m:
        return m.group(1).strip().strip("\"'")
    m = _H1.search(text)
    return m.group(1) if m else posixpath.splitext(posixpath.basename(path))[0]


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


def resolve(source: str, target: str) -> tuple[str, str, str | None] | None:
    """Classify a link from ``source``: ``("doc", path, fragment)``, ``("domain", host, None)`` or ``None``."""
    parts = urlsplit(target)
    if parts.scheme in ("http", "https"):
        host = (parts.hostname or "").removeprefix("www.")
        return ("domain", host, None) if host else None
    if parts.scheme or not parts.path.endswith(".md") or parts.path.startswith("/"):
        return None
    path = posixpath.normpath(posixpath.join(posixpath.dirname(source), parts.path))
    return ("doc", path, parts.fragment or None)


def _doc_node(path: str, text: str) -> dict:
    return {"id": path, "type": "doc", "bucket": bucket_of(path),
            "status": doc_status(text), "title": doc_title(text, path)}


def _edge_for(source: str, resolved: tuple[str, str, str | None], docs: dict) -> tuple | None:
    """``(target_id, kind, fragment)`` for a resolved link, or ``None`` if it leaves the corpus."""
    kind, target, fragment = resolved
    if kind == "domain":
        return f"domain:{target}", "cites", None
    if target not in docs:
        return None
    return target, "hub" if bucket_of(source) == _HUB_BUCKET else "link", fragment


def _add_link(nodes: dict, edges: dict, docs: dict, source: str, target: str, line: int) -> None:
    """Record one link from ``source``: a domain node if needed, and the aggregated edge."""
    resolved = resolve(source, target)
    edge = _edge_for(source, resolved, docs) if resolved else None
    if edge is None:
        return
    target_id, kind, fragment = edge
    if kind == "cites":
        nodes.setdefault(target_id, {"id": target_id, "type": "domain", "title": resolved[1]})
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
            _add_link(nodes, edges, docs, source, target, line)
    return {
        "nodes": [nodes[k] for k in sorted(nodes)],
        "edges": [
            {"source": s, "target": t, "kind": k,
             "lines": sorted(v["lines"]), "fragments": sorted(v["fragments"])}
            for (s, t, k), v in sorted(edges.items())
        ],
    }


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
