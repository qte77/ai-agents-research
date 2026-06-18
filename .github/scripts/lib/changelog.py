"""Pure changelog-vs-docs comparison logic for changelog-compare.py.

No file IO / argparse / sys.exit here (the entry script reads files and handles
exit codes), so the parsing, coverage, and report logic is unit-testable.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .monitor_utils import DEFAULT_NOISE, extract_keywords

_NOISE_ONLY = re.compile(
    r"^[-\s]*bug fixes and reliability improvements\.?\s*$", re.IGNORECASE
)
_COVERAGE_THRESHOLD = 0.4
_VERSION_SECTION = re.compile(r"^##\s+\[?(\d+\.\d+\.\d+)\]?", re.MULTILINE)


def version_tuple(v: str) -> tuple[int, ...]:
    """Convert a version string like '2.1.71' to a comparable tuple."""
    return tuple(int(x) for x in v.split("."))


def extract_scanned_version(scan_doc_text: str) -> str | None:
    """End of the version range in the scan-doc frontmatter purpose field, or None.

    Looks for ``purpose: ... vX.Y.Z–A.B.C ...`` (en-dash or hyphen) and returns
    the end version (``A.B.C``).
    """
    fm = re.search(r"^---\s*\n(.*?)\n---", scan_doc_text, re.DOTALL | re.MULTILINE)
    if not fm:
        return None
    m = re.search(r"purpose:.*?v(\d+\.\d+\.\d+)[–\-](\d+\.\d+\.\d+)", fm.group(1))
    return m.group(2) if m else None


def bump_scanned_version(scan_doc_text: str, new_end_version: str) -> str | None:
    """Return scan-doc text with the range end bumped, or None if nothing changed."""
    updated = re.sub(
        r"(purpose:.*?v\d+\.\d+\.\d+[–\-])\d+\.\d+\.\d+",
        rf"\g<1>{new_end_version}",
        scan_doc_text,
        count=1,
    )
    return updated if updated != scan_doc_text else None


def parse_changelog_versions(text: str) -> list[tuple[str, list[str]]]:
    """Parse CHANGELOG text into ``[(version, feature_lines)]``, newest first.

    Section headers look like ``## 2.1.72`` or ``## [2.1.72]``. Feature lines are
    the non-empty, non-heading lines within each section.
    """
    matches = list(_VERSION_SECTION.finditer(text))
    versions: list[tuple[str, list[str]]] = []
    for match, nxt in zip(matches, matches[1:] + [None]):
        section = text[match.end():(nxt.start() if nxt else len(text))]
        feature_lines = [
            line.strip()
            for line in section.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        versions.append((match.group(1), feature_lines))
    versions.sort(key=lambda t: version_tuple(t[0]), reverse=True)
    return versions


def collect_doc_keyword_index(docs_dir: Path) -> dict[str, frozenset[str]]:
    """Map each ``*.md`` doc's relative path to its keyword set (filename + H2/H3).

    Pre-computing keywords once here avoids rebuilding them per feature line in
    find_covering_docs.
    """
    heading_re = re.compile(r"^#{2,3}\s+(.*)")
    index: dict[str, frozenset[str]] = {}
    for md in sorted(docs_dir.rglob("*.md")):
        rel = str(md.relative_to(docs_dir.parent))
        kw = set(extract_keywords(md.name))
        for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
            m = heading_re.match(line)
            if m:
                kw.update(extract_keywords(m.group(1).strip()))
        index[rel] = frozenset(kw)
    return index


def find_covering_docs(
    feature_line: str, keyword_index: dict[str, frozenset[str]]
) -> list[str]:
    """Doc paths whose keywords overlap the feature's keywords past the threshold.

    Pure "Bug fixes and reliability improvements" lines and keyword-empty lines
    return ``[]`` (the caller then marks them uncovered).
    """
    if _NOISE_ONLY.match(feature_line.strip("- ")):
        return []
    feature_kw = extract_keywords(feature_line) - DEFAULT_NOISE
    if not feature_kw:
        return []
    return [
        path for path, doc_kw in keyword_index.items()
        if len(feature_kw & doc_kw) / len(feature_kw) > _COVERAGE_THRESHOLD
    ]


@dataclass
class VersionCoverage:
    """Coverage breakdown for one changelog version."""
    version: str
    covered: list[tuple[str, list[str]]]  # (feature_line, covering_doc_paths)
    uncovered: list[str]                   # feature_lines with no covering doc


def classify_versions(
    new_versions: list[tuple[str, list[str]]],
    keyword_index: dict[str, frozenset[str]],
) -> list[VersionCoverage]:
    """Split each version's feature lines into covered / uncovered."""
    results: list[VersionCoverage] = []
    for version, feature_lines in new_versions:
        covered: list[tuple[str, list[str]]] = []
        uncovered: list[str] = []
        for feat in feature_lines:
            docs = find_covering_docs(feat, keyword_index)
            if docs:
                covered.append((feat, docs))
            else:
                uncovered.append(feat)
        results.append(VersionCoverage(version, covered, uncovered))
    return results


def render_changelog_report(
    results: list[VersionCoverage], last_scanned: str
) -> tuple[str, bool]:
    """Render the markdown report; returns ``(report_text, has_uncovered)``."""
    lines: list[str] = [
        "## Changelog Monitor Report", "",
        f"Last scanned version: **{last_scanned}**",
        f"New versions detected: **{len(results)}**", "",
    ]
    if not results:
        lines.append("No new versions found beyond the scanned range. Nothing to review.")
        return "\n".join(lines).rstrip("\n"), False

    lines += ["### New Versions Summary", "",
              "| Version | Features | Covered | Uncovered |",
              "|---------|----------|---------|-----------|"]
    for r in results:
        lines.append(
            f"| {r.version} | {len(r.covered) + len(r.uncovered)} "
            f"| {len(r.covered)} | {len(r.uncovered)} |"
        )
    lines.append("")

    lines += ["### Feature Coverage Details", ""]
    for r in results:
        lines += [f"#### v{r.version}", ""]
        for feat, docs in r.covered:
            lines.append(f"- **[covered]** {feat}")
            lines.append(f"  - Covered by: {', '.join(f'`{d}`' for d in docs[:3])}")
        for feat in r.uncovered:
            lines.append(f"- **[UNCOVERED]** {feat}")
        lines.append("")

    lines += ["---", "_Generated by `.github/scripts/changelog-compare.py`_"]
    return "\n".join(lines).rstrip("\n"), any(r.uncovered for r in results)
