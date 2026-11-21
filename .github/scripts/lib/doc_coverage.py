"""Coverage checks over the doc graph (plan 0015 X1, X3).

Every content doc must be (1) linked from its folder's README index, the nearest
``README.md`` above it inside ``docs/``, and (2) linked from at least one other
doc or repo-root markdown file. Every ``#fragment`` in a doc-to-doc link must
match a heading slug (or explicit anchor) in its target (3). Hub coverage (X2, owner
decision D6): every content doc outside the D6 exemptions is linked from at least one
topic hub, and no hub has two rows for the same doc and section. Built on ``doc_graph.build_graph``; pure logic, so
the entry point (``check-doc-coverage.py``) only reads files and sets the exit code.

Not content docs: README indexes themselves, ``docs/`` root files that have no
folder index, and ``docs/cc-native/examples/`` (example rule files, not analyses).
"""
from __future__ import annotations

import posixpath
import re

from .doc_frontmatter import in_scope
from .doc_graph import build_graph, extract_links, resolve

_EXEMPT_PREFIXES = ("docs/cc-native/examples/",)
_HUB_DIR = "docs/_topics/"
_HUB_INDEX = "docs/_topics/README.md"
# D6: not expected in a hub (their folder README is the index).
_PROFILE_DIRS = tuple(f"docs/non-cc/{d}/" for d in ("coding-agents", "agents", "orchestrators", "reference"))
_NOT_HUB_CONTENT = (_HUB_DIR, "docs/plans/", "docs/archive/", "docs/research/")
_FENCE = re.compile(r"^\s*(```|~~~)")
_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
_HTML_ANCHOR = re.compile(r"<a\s+(?:name|id)=\"([^\"]+)\"")
_MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_EMPHASIS_UNDERSCORE = re.compile(r"(?<!\w)_+|_+(?!\w)")


def index_of(path: str, docs: dict) -> str | None:
    """The nearest ``README.md`` above ``path`` inside ``docs/``, or ``None``."""
    folder = posixpath.dirname(path)
    while folder.startswith("docs/"):
        readme = f"{folder}/README.md"
        if readme in docs and readme != path:
            return readme
        folder = posixpath.dirname(folder)
    return None


def inbound(docs: dict, extra: dict | None = None) -> dict[str, set]:
    """``{doc: {linking sources}}`` from other docs and from ``extra`` (repo-root files)."""
    links: dict[str, set] = {}
    for e in build_graph(docs)["edges"]:
        if e["source"] != e["target"]:
            links.setdefault(e["target"], set()).add(e["source"])
    for source, text in (extra or {}).items():
        for target, _ in extract_links(text):
            resolved = resolve(source, target)
            if resolved and resolved[0] in docs:
                links.setdefault(resolved[0], set()).add(source)
    return links


def is_content(path: str) -> bool:
    """True for docs the checks cover: not a README index, not an example file."""
    return posixpath.basename(path) != "README.md" and not path.startswith(_EXEMPT_PREFIXES)


def check_coverage(docs: dict, extra: dict | None = None) -> list[str]:
    """Violations, one line each, sorted: a doc missing from its index, or with no inbound link."""
    links = inbound(docs, extra)
    problems = []
    for path in sorted(p for p in docs if is_content(p)):
        sources = links.get(path, set())
        index = index_of(path, docs)
        if index and index not in sources:
            problems.append(f"{path}: not linked from its index {index}")
        if not sources:
            problems.append(f"{path}: no inbound link from any other doc")
    return sorted(problems)


def slugify(heading: str) -> str:
    """GitHub's heading anchor: rendered text, lowercased, punctuation dropped, spaces to hyphens."""
    text = _MD_LINK.sub(r"\1", heading)
    text = re.sub(r"<[^>]+>", "", text).replace("`", "")
    # Reason: emphasis underscores vanish when rendered; underscores inside a word (my_var) stay.
    text = _EMPHASIS_UNDERSCORE.sub("", text)
    text = re.sub(r"[^\w\- ]", "", text.lower())
    return text.replace(" ", "-")


def heading_slugs(text: str) -> set[str]:
    """Every anchor a rendered doc offers: heading slugs (duplicates get ``-1``, ``-2``) and ``<a id>``s."""
    slugs: set[str] = set()
    seen: dict[str, int] = {}
    in_fence = False
    for line in text.splitlines():
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        slugs.update(_HTML_ANCHOR.findall(line))
        m = _HEADING.match(line)
        if m:
            slug = slugify(m.group(1))
            count = seen.get(slug, 0)
            seen[slug] = count + 1
            slugs.add(slug if count == 0 else f"{slug}-{count}")
    return slugs


def check_anchors(docs: dict) -> list[str]:
    """Violations, sorted: a doc-to-doc link whose ``#fragment`` matches no anchor in its target."""
    anchors: dict[str, set] = {}
    problems = set()
    for source in docs:
        for link, line in extract_links(docs[source]):
            resolved = resolve(source, link)
            if not resolved or resolved[0] not in docs or not resolved[1]:
                continue
            target, fragment = resolved
            if target not in anchors:
                anchors[target] = {a.lower() for a in heading_slugs(docs[target])}
            if fragment.lower() not in anchors[target]:
                problems.add(f"{source}:{line}: #{fragment} not found in {target}")
    return sorted(problems)


def hub_exempt(path: str) -> bool:
    """D6 exemptions: docs/ root files, single-product profiles, framework analyses, specs and runbooks.

    Landscapes are never exempt.
    """
    name = posixpath.basename(path)
    if name.endswith("-landscape.md"):
        return False
    if path.count("/") == 1:
        return True
    if path.startswith(_PROFILE_DIRS):
        return True
    if path.startswith("docs/non-cc/frameworks/") and name.endswith("-analysis.md"):
        return True
    return name.endswith(("-spec.md", "-runbook.md"))


def unhubbed(docs: dict) -> list[str]:
    """Content docs outside the D6 exemptions that no topic hub links to, sorted."""
    hubbed = {e["target"] for e in build_graph(docs)["edges"]
              if e["kind"] == "hub" and e["source"] != _HUB_INDEX}
    return sorted(p for p in docs
                  if is_content(p) and not p.startswith(_NOT_HUB_CONTENT)
                  and not hub_exempt(p) and p not in hubbed)


def check_hub_duplicates(docs: dict) -> list[str]:
    """Hub table rows (lines starting with ``|``) whose first link repeats an earlier row's doc and section; sorted."""
    problems = []
    for hub in sorted(p for p in docs if p.startswith(_HUB_DIR) and p != _HUB_INDEX):
        first_seen: dict[tuple, int] = {}
        rows: dict[int, str] = {}
        lines = docs[hub].splitlines()
        for link, line in extract_links(docs[hub]):
            if line in rows or not lines[line - 1].lstrip().startswith("|"):
                continue  # Reason: a row's first link is its target; later links and prose pointers are asides.
            rows[line] = link
            resolved = resolve(hub, link)
            if not resolved or resolved[0] not in docs:
                continue
            key = (resolved[0], resolved[1] or "")
            if key in first_seen:
                target = resolved[0] + (f"#{resolved[1]}" if resolved[1] else "")
                problems.append(f"{hub}:{line}: duplicate row for {target} (first at line {first_seen[key]}); merge them")
            else:
                first_seen[key] = line
    return sorted(problems)


GLOSSARY = "docs/glossary.md"
# Reason: per-repo learnings are mirrors overwritten by learnings-aggregator.py; fix upstream, not here.
_MIRRORS = ("docs/learnings/per-repo/",)
_ABBR = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*$")
_INLINE_CODE = re.compile(r"`[^`\n]*`")
_REF_DEF = re.compile(r"^\s*\[[^\]]+\]:\s")
_FRONTMATTER = re.compile(r"\A---[ \t]*\n.*?\n---[ \t]*\n", re.DOTALL)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_LINK_TARGET = re.compile(r"\]\([^)]*\)")
_URL = re.compile(r"<?https?://[^\s>)]+>?")
_GLOSSARY_LINK = re.compile(r"\]\((?!https?:)[^)\s]*glossary\.md|^\s*\[[^\]]+\]:\s*(?!https?:)\S*glossary\.md", re.MULTILINE)
_FENCE_RUN = re.compile(r"^\s*(`{3,}|~{3,})")


def parse_glossary(text: str) -> dict[str, str]:
    """Abbreviation → expansion from the glossary tables (plan 0015 C2, owner decision D7).

    A row's Expansion is either the expansion of a one-abbreviation Term, or
    ``ABBR = expansion`` pairs separated by ``;`` when the Term lists several names.
    Rows whose Expansion is ``—`` define no abbreviation.
    """
    out = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[1] in ("", "—", "Expansion") or set(cells[1]) <= set("-"):
            continue
        term, expansion = cells[0], cells[1]
        if "=" in expansion:
            for pair in expansion.split(";"):
                abbr, _, full = (s.strip() for s in pair.partition("="))
                if _ABBR.match(abbr):
                    out[abbr] = full
        elif _ABBR.match(term):
            out[term] = expansion
    return out


def _prose(text: str, ref_defs: bool = False) -> str:
    """Body text outside frontmatter, fenced code, inline code and HTML comments.

    Reference-link definitions are dropped unless ``ref_defs`` is set.
    """
    kept, fence = [], None
    for line in _COMMENT.sub("", _FRONTMATTER.sub("", text, count=1)).splitlines():
        m = _FENCE_RUN.match(line)
        if m and fence is None:
            fence = m.group(1)
        elif m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
            # Reason: only a run of the opening character, at least as long, closes a block.
            fence = None
        elif fence is None and (ref_defs or not _REF_DEF.match(line)):
            kept.append(_INLINE_CODE.sub("", line))
    return "\n".join(kept)


def check_abbreviations(docs: dict, glossary: dict[str, str]) -> list[str]:
    """Content docs that use a glossary abbreviation without expanding it (C2; fails check_coverage).

    Scope is the frontmatter schema's (no READMEs, hubs, plans, examples, archive or
    ``docs/research/``) minus the per-repo learnings mirrors.

    A doc passes if the expansion appears anywhere in its body text (any case; a hyphen and a
    space count as the same, as does a line break; URLs and link targets don't count) or it
    links the glossary with a relative inline or reference-style link.
    Plurals and hyphen compounds ("MCPs", "MCP-based") count as uses.
    """
    def norm(s: str) -> str:
        return " ".join(s.lower().replace("-", " ").split())

    out = []
    for path in sorted(docs):
        if path == GLOSSARY or not in_scope(path) or path.startswith(_MIRRORS):
            continue
        if _GLOSSARY_LINK.search(_prose(docs[path], ref_defs=True)):
            continue
        prose = _prose(docs[path])
        prose = _URL.sub("", _LINK_TARGET.sub("]", prose))
        lower = norm(prose)
        missing = [a for a in sorted(glossary)
                   if re.search(rf"(?<![\w-]){re.escape(a)}(?=s?\b)", prose) and norm(glossary[a]) not in lower]
        if missing:
            out.append(f"{path}: {', '.join(missing)} not expanded")
    return out
