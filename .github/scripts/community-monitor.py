#!/usr/bin/env python3
"""Monitor community sources for Claude Code features, tips, and tricks.

Fetches content from community sources (awesome-claude-code,
awesome-claude-code-plugins) and identifies entries not yet covered
by existing community docs. claudelog.com is not polled: its changelog text
duplicates cc-changelog-monitor and its truncated lines made noisy reports.
Pure parsing lives in lib/community_sources.py.

Usage:
    python community-monitor.py --community-docs-dir PATH [--state-file PATH]

Exit codes:
    0 = no new uncovered content
    1 = new content found (workflow should open a PR)
    2 = fatal error (bad input, or no source returned any entries) — distinct from 1 so the workflow fails loudly
        instead of treating an error as "new content"
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.community_sources import extract_markdown_entries
from lib.monitor_utils import fatal, fetch_text, run_monitor

SOURCES: list[dict[str, str]] = [
    {
        "name": "awesome-claude-code",
        "url": "https://raw.githubusercontent.com/hesreallyhim/awesome-claude-code/main/README.md",
        "type": "markdown",
        "description": "Curated resource list (skills, workflows, tooling, hooks, commands)",
    },
    {
        "name": "awesome-claude-code-plugins",
        "url": "https://raw.githubusercontent.com/ccplugins/awesome-claude-code-plugins/main/README.md",
        "type": "markdown",
        "description": "Installable plugin registry with marketplace format",
    },
]

def fetch_and_extract_source(source: dict[str, str]) -> list[dict[str, str]]:
    """Fetch a markdown source and extract its entries."""
    content = fetch_text(source["url"])
    return extract_markdown_entries(content)


def main() -> None:
    """Entry point for the community monitor script."""
    parser = argparse.ArgumentParser(
        description="Monitor community sources for CC features and tips."
    )
    parser.add_argument("--community-docs-dir", required=True, type=Path,
                        help="Path to docs/cc-community/ directory")
    parser.add_argument("--state-file", type=Path,
                        default=Path(".github/state/community-monitor-state.json"),
                        help="Path to state file tracking previously seen entries")
    args = parser.parse_args()

    if not args.community_docs_dir.exists():
        fatal(f"ERROR: Community docs dir does not exist: {args.community_docs_dir}")

    run_monitor(
        sources=SOURCES,
        fetch_fn=fetch_and_extract_source,
        docs_dir=args.community_docs_dir,
        state_file=args.state_file,
        report_title="Community Monitor Report",
        script_name="community-monitor.py",
    )


if __name__ == "__main__":
    main()
