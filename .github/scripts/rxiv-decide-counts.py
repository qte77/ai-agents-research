#!/usr/bin/env python3
"""Append the weekly paper run's decide() counts to the monthly decision-model
eval output (plan 0014 row 13-A7, part 2).

Reads every ``triage/rxiv/*-papers.md`` report, appends a per-run table to the
summary file and, when the decided share has fallen for three runs in a row,
a drift note to the drift file (which feeds the ``decision-drift`` issue).
"""
from __future__ import annotations

import argparse
from pathlib import Path

from lib import decide_counts as dc


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reports-dir", type=Path, default=Path("triage/rxiv"))
    parser.add_argument("--summary", type=Path, required=True, help="markdown file to append the table to")
    parser.add_argument("--drift", type=Path, required=True, help="markdown file to append a drift note to")
    args = parser.parse_args()

    runs = dc.collect(sorted(args.reports_dir.glob("*-papers.md")))
    with args.summary.open("a") as f:
        f.write("\n## Weekly paper runs: decide() share\n\n")
        f.write(dc.table(runs) if runs else "No triage report carries a decide() line yet.\n")
    note = dc.drift(runs)
    if note:
        with args.drift.open("a") as f:
            f.write(note)
    print(f"{len(runs)} paper runs with decide() counts; drift: {'yes' if note else 'no'}")


if __name__ == "__main__":
    main()
