"""Pure changelog-vs-docs comparison logic for changelog-compare.py.

No file IO / argparse / sys.exit here (the entry script reads files and handles
exit codes), so the parsing, coverage, and report logic is unit-testable.
"""
from __future__ import annotations

import re

# Reason: xml.etree.ElementTree.fromstring parses a first-party GitHub feed
# (releases.atom) fetched over HTTPS in CI, not arbitrary/untrusted input;
# stdlib is the repo convention (CONTRIBUTING.md) and no external entities
# are resolved here (no DTD/XXE surface in an Atom release feed).
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

from .monitor_utils import DEFAULT_NOISE, extract_keywords

_NOISE_ONLY = re.compile(
    r"^[-\s]*bug fixes and reliability improvements\.?\s*$", re.IGNORECASE
)
_COVERAGE_THRESHOLD = 0.4
_VERSION_SECTION = re.compile(r"^##\s+\[?(\d+\.\d+\.\d+)\]?", re.MULTILINE)
_ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
_RELEASE_ID_VERSION = re.compile(r"/v(\d+\.\d+\.\d+)$")


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


def parse_releases_feed(xml_text: str) -> list[dict[str, str]]:
    """Parse a GitHub releases Atom feed into ``[{version, updated, id}]``.

    Trigger/timestamp/dedup source only (issue #410) — CHANGELOG.md remains the
    sole content source. Returned newest-first by version, mirroring
    ``parse_changelog_versions``. Entries whose ``<id>`` doesn't end in a
    parseable ``vX.Y.Z`` (e.g. a non-release tag) are skipped rather than
    failing the whole parse. Malformed XML or empty/whitespace-only input
    returns ``[]``.
    """
    if not xml_text or not xml_text.strip():
        return []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    entries: list[dict[str, str]] = []
    for entry in root.findall("atom:entry", _ATOM_NS):
        entry_id = (entry.findtext("atom:id", default="", namespaces=_ATOM_NS) or "").strip()
        m = _RELEASE_ID_VERSION.search(entry_id)
        if not m:
            continue
        updated = (entry.findtext("atom:updated", default="", namespaces=_ATOM_NS) or "").strip()
        entries.append({"version": m.group(1), "updated": updated, "id": entry_id})
    entries.sort(key=lambda e: version_tuple(e["version"]), reverse=True)
    return entries


def unseen_releases(
    feed_entries: list[dict[str, str]],
    seen_ids: set[str],
    scan_cutoff_version: str,
) -> list[dict[str, str]]:
    """Feed entries the monitor hasn't already processed (issue #410 trigger).

    An entry is excluded — treated as already seen — when either its ``id``
    is already in ``seen_ids`` (the persisted dedup ledger) or its version is
    at or below ``scan_cutoff_version`` (the scan-doc's already-scanned range
    end). The cutoff check alone covers two cases the ledger can't:

    - **Bootstrap**: an empty ``seen_ids`` (first run, or a reset ledger)
      would otherwise make every entry in the feed's rolling window look
      "unseen" and re-report the changelog's entire existing history.
    - **Window rollout**: an id that has rolled out of the feed's ~31-entry
      window is never in ``feed_entries`` to begin with, so it can't be
      resurfaced by this function — but if the ledger was ever reset, the
      cutoff (not the ledger) is what keeps an in-window entry at or below
      it from being re-reported.

    Empty ``feed_entries`` returns ``[]`` — the caller falls back to
    CHANGELOG.md-cutoff-only comparison when there's no feed data.
    """
    cutoff = version_tuple(scan_cutoff_version)
    return [
        e for e in feed_entries
        if e["id"] not in seen_ids and version_tuple(e["version"]) > cutoff
    ]


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
    results: list[VersionCoverage],
    last_scanned: str,
    updated_by_version: dict[str, str] | None = None,
) -> tuple[str, bool]:
    """Render the markdown report; returns ``(report_text, has_uncovered)``.

    ``updated_by_version`` (optional) maps a version string to its releases.atom
    ``<updated>`` timestamp (issue #410) — when a version has a known date, the
    version heading is annotated with it; CHANGELOG.md has no dates of its own.
    """
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
        updated = (updated_by_version or {}).get(r.version)
        heading = f"#### v{r.version}"
        if updated:
            heading += f" — released {updated.split('T')[0]}"
        lines += [heading, ""]
        for feat, docs in r.covered:
            lines.append(f"- **[covered]** {feat}")
            lines.append(f"  - Covered by: {', '.join(f'`{d}`' for d in docs[:3])}")
        for feat in r.uncovered:
            lines.append(f"- **[UNCOVERED]** {feat}")
        lines.append("")

    lines += ["---", "_Generated by `.github/scripts/changelog-compare.py`_"]
    return "\n".join(lines).rstrip("\n"), any(r.uncovered for r in results)
