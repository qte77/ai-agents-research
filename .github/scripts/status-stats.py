#!/usr/bin/env python3
"""Generate statistical analysis of Claude platform outages from a JSONL archive.

Reads the outage archive and prints a markdown report (frequency, duration,
severity, component, and time-of-day analysis). The pure report logic lives in
lib/status_report.py; this entry point only loads the archive and prints.

Usage:
    python status-stats.py --archive triage/status-monitor/outages.jsonl > triage/status-monitor/outage-stats.md
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor_utils import fatal, load_jsonl
from lib.status_report import generate_report


def main() -> None:
    """Entry point for the status stats generator."""
    parser = argparse.ArgumentParser(
        description="Generate outage statistics from JSONL archive."
    )
    parser.add_argument(
        "--archive", type=Path, default=Path("triage/status-monitor/outages.jsonl"),
        help="Path to the JSONL archive file (default: triage/status-monitor/outages.jsonl)",
    )
    args = parser.parse_args()

    if not args.archive.exists():
        fatal(f"ERROR: Archive not found: {args.archive}")
    print(generate_report(load_jsonl(args.archive)))


if __name__ == "__main__":
    main()
