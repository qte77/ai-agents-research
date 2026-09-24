#!/usr/bin/env python3
"""Compare CC CHANGELOG.md against the scanned version range in CC-changelog-feature-scan.md.

Identifies versions newer than the last scanned version and checks whether
existing docs cover those features. Pure parsing/coverage/report logic lives in
lib/changelog.py; this entry point handles file IO and exit codes.

Optionally reads a fetched releases.atom (issue #410) to drive the "which
versions are new" decision: when the feed parses to at least one entry,
lib.changelog.select_new_versions decides which CHANGELOG.md versions to
report — a version the feed covers is gated by its per-id dedup ledger
(persisted in the shared monitor state file) with the scan-doc cutoff as a
bootstrap / window-rollout safety net; a version the feed doesn't cover at
all (upstream feed/changelog skew) falls back to the plain cutoff instead of
being silently dropped — CHANGELOG.md is the full-history backstop. When the
feed is absent, empty, or unparseable, every version falls back to the
cutoff — the pre-#410 behaviour. Either way CHANGELOG.md remains the sole
content source, and the ledger (via lib.changelog.ledger_ids, which excludes
any feed entry whose version CHANGELOG.md doesn't have yet) is written only
after a full, successful comparison run (never on a fatal/early exit).

Usage:
    python changelog-compare.py --changelog PATH --scan-doc PATH --docs-dir PATH
        [--update-scan-doc] [--releases-feed PATH] [--state-file PATH]

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
    ledger_ids,
    parse_changelog_versions,
    parse_releases_feed,
    render_changelog_report,
    select_new_versions,
)
from lib.monitor_utils import fatal, load_state, save_state

# Key under which this script's feed-id ledger lives in the shared monitor
# state file (alongside native-sources-monitor.py's per-source keys).
_RELEASES_FEED_STATE_KEY = "cc-changelog-releases"


def _load_releases_feed(releases_feed: Path | None) -> list[dict[str, str]]:
    """Fetch+parse the optional releases.atom path.

    Returns ``[]`` (with a stderr warning) when the path wasn't given, doesn't
    exist, or parses to no entries — the caller then falls back to a pure
    scan-doc-cutoff comparison for every version.
    """
    if releases_feed is None:
        return []
    if not releases_feed.exists():
        print(
            f"WARNING: releases feed not found at {releases_feed} "
            "— falling back to scan-doc-cutoff-only trigger",
            file=sys.stderr,
        )
        return []
    feed_entries = parse_releases_feed(releases_feed.read_text(encoding="utf-8"))
    if not feed_entries:
        print(
            "WARNING: releases feed parsed to no entries "
            "— falling back to scan-doc-cutoff-only trigger",
            file=sys.stderr,
        )
    return feed_entries


def _load_ledger_state(
    feed_entries: list[dict[str, str]], state_file: Path
) -> tuple[dict[str, list[str]], set[str]]:
    """Load the shared monitor state — only when there's a feed to dedup against."""
    if not feed_entries:
        return {}, set()
    state = load_state(state_file)
    seen_ids = set(state.get(_RELEASES_FEED_STATE_KEY, []))
    return state, seen_ids


def _log_trigger_summary(
    feed_entries: list[dict[str, str]], new_versions: list[tuple[str, list[str]]]
) -> None:
    """Report which trigger path decided ``new_versions`` (feed ledger vs. cutoff-only)."""
    if feed_entries:
        print(
            f"Releases feed: {len(feed_entries)} entries — {len(new_versions)} new "
            "versions (feed ledger, cutoff fallback for feed-uncovered versions)",
            file=sys.stderr,
        )
    else:
        print(f"New versions found (cutoff-only): {len(new_versions)}", file=sys.stderr)


def _maybe_bump_scan_doc(
    scan_doc: Path,
    scan_text: str,
    new_versions: list[tuple[str, list[str]]],
    update_scan_doc: bool,
) -> None:
    """Bump the scan-doc frontmatter to the newest reported version, if asked."""
    if not (update_scan_doc and new_versions):
        return
    newest = new_versions[0][0]  # already sorted descending
    updated = bump_scanned_version(scan_text, newest)
    if updated is not None:
        scan_doc.write_text(updated, encoding="utf-8")
        print(f"Updated scan doc version range end to {newest}", file=sys.stderr)
    else:
        print(f"WARNING: Could not update version in {scan_doc}", file=sys.stderr)


def _persist_ledger(
    feed_entries: list[dict[str, str]],
    all_versions: list[tuple[str, list[str]]],
    state: dict[str, list[str]],
    state_file: Path,
) -> None:
    """Persist the feed-id ledger — call only after a full, successful run.

    ``ledger_ids`` excludes any feed entry whose version CHANGELOG.md doesn't
    have yet (upstream skew) so a not-yet-published version is never marked
    "seen" prematurely.
    """
    if not feed_entries:
        return
    changelog_versions = {v for v, _ in all_versions}
    state[_RELEASES_FEED_STATE_KEY] = ledger_ids(feed_entries, changelog_versions)
    save_state(state_file, state)


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
    parser.add_argument("--releases-feed", type=Path, default=None,
                        help="Path to fetched releases.atom (optional; when it parses to "
                             "at least one entry, its id ledger drives the new-versions "
                             "trigger for feed-covered versions (cutoff fallback for any "
                             "version the feed doesn't cover) and its timestamps annotate "
                             "the report; falls back to the scan-doc cutoff alone when "
                             "absent/empty/unparseable. CHANGELOG.md always stays the "
                             "content source)")
    parser.add_argument("--state-file", type=Path,
                        default=Path(".github/state/native-monitor-state.json"),
                        help="Path to the shared monitor state file "
                             "(only used when --releases-feed is given)")
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

    # select_new_versions reduces to a pure cutoff comparison when
    # feed_entries is empty (pre-#410 behaviour) and otherwise gates
    # feed-covered versions by the ledger while falling back to the cutoff
    # for versions the feed doesn't cover at all (skew safety net).
    feed_entries = _load_releases_feed(args.releases_feed)
    updated_by_version = {e["version"]: e["updated"] for e in feed_entries}
    state, seen_ids = _load_ledger_state(feed_entries, args.state_file)
    new_versions = select_new_versions(all_versions, feed_entries, seen_ids, last_scanned)
    _log_trigger_summary(feed_entries, new_versions)

    keyword_index = collect_doc_keyword_index(args.docs_dir)
    print(f"Docs indexed: {len(keyword_index)}", file=sys.stderr)

    results = classify_versions(new_versions, keyword_index)
    report, has_uncovered = render_changelog_report(
        results, last_scanned, updated_by_version=updated_by_version or None
    )

    _maybe_bump_scan_doc(args.scan_doc, scan_text, new_versions, args.update_scan_doc)

    # Persist the ledger only once the comparison has fully succeeded (never
    # on a fatal/early exit above) — "update the ledger only after a
    # successful comparison run" per #410.
    _persist_ledger(feed_entries, all_versions, state, args.state_file)

    print(report)
    sys.exit(1 if has_uncovered else 0)


if __name__ == "__main__":
    main()
