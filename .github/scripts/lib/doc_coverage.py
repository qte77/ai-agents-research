"""Coverage checks over the doc graph (plan 0015 X1, X3).

Every content doc must be (1) linked from its folder's README index, the nearest
``README.md`` above it inside ``docs/``, and (2) linked from at least one other
doc or repo-root markdown file. Every ``#fragment`` in a doc-to-doc link must
match a heading slug (or explicit anchor) in its target (3). Built on ``doc_graph.build_graph``; pure logic, so
the entry point (``check-doc-coverage.py``) only reads files and sets the exit code.

Not content docs: README indexes themselves, ``docs/`` root files that have no
folder index, and ``docs/cc-native/examples/`` (example rule files, not analyses).
"""
from __future__ import annotations

import posixpath
import re

from .doc_graph import build_graph, extract_links, resolve

_EXEMPT_PREFIXES = ("docs/cc-native/examples/",)
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
