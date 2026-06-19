#!/usr/bin/env python3
"""Compare CC CHANGELOG.md against the scanned version range in CC-changelog-feature-scan.md.

Identifies versions newer than the last scanned version and checks whether
existing docs cover those features. Pure parsing/coverage/report logic lives in
lib/changelog.py; this entry point handles file IO and exit codes.

Usage:
    python changelog-compare.py --changelog PATH --scan-doc PATH --docs-dir PATH [--update-scan-doc]

Exit codes:
    0 = no new uncovered features
    1 = new features found (workflow should open a PR)
    2 = fatal error (bad input / parse failure) — distinct from 1 so the workflow
        fails loudly instead of treating an error as "new features"
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.changelog import (
    bump_scanned_version,
    classify_versions,
    collect_doc_keyword_index,
    extract_scanned_version,
    parse_changelog_versions,
    render_changelog_report,
    version_tuple,
)
from lib.monitor_utils import fatal


def main() -> None:
    """Entry point for the changelog comparison script."""
    parser = argparse.ArgumentParser(
        description="Compare CC CHANGELOG.md against scanned version range."
    )
    parser.add_argument("--changelog", required=True, type=Path,
                        help="Path to fetched CHANGELOG.md")
    parser.add_argument("--scan-doc", required=True, type=Path,
                        help="Path to CC-changelog-feature-scan.md (frontmatter version range)")
    parser.add_argument("--docs-dir", required=True, type=Path,
                        help="Path to docs/ directory to search for coverage")
    parser.add_argument("--update-scan-doc", action="store_true",
                        help="Bump the scan doc frontmatter to the newest changelog version")
    args = parser.parse_args()

    for p in (args.changelog, args.scan_doc, args.docs_dir):
        if not p.exists():
            fatal(f"ERROR: Path does not exist: {p}")

    scan_text = args.scan_doc.read_text(encoding="utf-8")
    last_scanned = extract_scanned_version(scan_text)
    if last_scanned is None:
        fatal(f"ERROR: Could not parse scanned version range from {args.scan_doc}")
    print(f"Last scanned version: {last_scanned}", file=sys.stderr)

    all_versions = parse_changelog_versions(args.changelog.read_text(encoding="utf-8"))
    if not all_versions:
        fatal(f"ERROR: No version sections found in {args.changelog}")
    cutoff = version_tuple(last_scanned)
    new_versions = [(v, feats) for v, feats in all_versions if version_tuple(v) > cutoff]
    print(f"New versions found: {len(new_versions)}", file=sys.stderr)

    keyword_index = collect_doc_keyword_index(args.docs_dir)
    print(f"Docs indexed: {len(keyword_index)}", file=sys.stderr)

    results = classify_versions(new_versions, keyword_index)
    report, has_uncovered = render_changelog_report(results, last_scanned)

    if args.update_scan_doc and new_versions:
        newest = new_versions[0][0]  # already sorted descending
        updated = bump_scanned_version(scan_text, newest)
        if updated is not None:
            args.scan_doc.write_text(updated, encoding="utf-8")
            print(f"Updated scan doc version range end to {newest}", file=sys.stderr)
        else:
            print(f"WARNING: Could not update version in {args.scan_doc}", file=sys.stderr)

    print(report)
    sys.exit(1 if has_uncovered else 0)


if __name__ == "__main__":
    main()
