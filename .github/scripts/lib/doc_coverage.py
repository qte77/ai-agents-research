"""Coverage checks over the doc graph (plan 0015 X1).

Every content doc must be (1) linked from its folder's README index, the nearest
``README.md`` above it inside ``docs/``, and (2) linked from at least one other
doc or repo-root markdown file. Built on ``doc_graph.build_graph``; pure logic, so
the entry point (``check-doc-coverage.py``) only reads files and sets the exit code.

Not content docs: README indexes themselves, ``docs/`` root files that have no
folder index, and ``docs/cc-native/examples/`` (example rule files, not analyses).
"""
from __future__ import annotations

import posixpath

from .doc_graph import build_graph, extract_links, resolve

_EXEMPT_PREFIXES = ("docs/cc-native/examples/",)


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
