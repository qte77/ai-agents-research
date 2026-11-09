#!/usr/bin/env python3
"""Monitor the Microsoft Learn pages cited by the Microsoft 365 Copilot doc.

Checks whether each watched page's `ms.date` meta value or stored verbatim
quote has drifted since the last run, and whether an entry's optional `due`
date (YYYY-MM-DD, a dated event the doc predicts) has passed. The watch list (url + quote) lives in
the state file itself; pure extraction/diff/report logic lives in
lib/m365_drift.py.

Usage:
    python m365-drift-monitor.py [--state-file PATH]

Exit codes:
    0 = no drift, no fetch failures
    1 = drift found, a due date passed, and/or a page could not be checked
"""
import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.m365_drift import (
    build_new_state,
    diff_entries,
    extract_ms_date,
    quote_present,
    render_report,
)
from lib.monitor_utils import fetch_text, load_state, save_state

DEFAULT_STATE_FILE = Path(".github/state/m365-drift-state.json")


def observe(url: str, quote: str) -> dict:
    """Fetch one watched page and build its observation dict.

    On fetch failure, ``ms_date``/``quote_found`` are None and ``error`` is
    set — diff_entries reports this as "could not check", not as drift.
    """
    try:
        raw_html = fetch_text(url)
    except Exception as e:  # noqa: BLE001 — any network/HTTP failure is "could not check"
        print(f"WARNING: Failed to fetch {url}: {e}", file=sys.stderr)
        return {"url": url, "quote": quote, "ms_date": None, "quote_found": None, "error": str(e)}

    return {
        "url": url,
        "quote": quote,
        "ms_date": extract_ms_date(raw_html),
        "quote_found": quote_present(raw_html, quote),
        "error": None,
    }


def main() -> None:
    """Entry point for the M365 drift monitor script."""
    parser = argparse.ArgumentParser(
        description="Check the M365 Copilot doc's cited Microsoft Learn pages for drift."
    )
    parser.add_argument("--state-file", type=Path, default=DEFAULT_STATE_FILE,
                        help="Path to the JSON state file (watch list + last-seen ms.date)")
    args = parser.parse_args()

    prev_state = load_state(args.state_file)
    if not prev_state:
        sys.exit(f"ERROR: No watch-list entries in {args.state_file}")

    observations = [observe(url, entry["quote"]) for url, entry in prev_state.items()]

    today = datetime.now(UTC).date()
    diffs = diff_entries(prev_state, observations, today=today)
    print(render_report(diffs))

    save_state(args.state_file, build_new_state(prev_state, observations))
    print(f"State saved to {args.state_file}", file=sys.stderr)

    sys.exit(1 if diffs else 0)


if __name__ == "__main__":
    main()
