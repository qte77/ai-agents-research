"""Weekly decide() share of the paper relevance run (plan 0014 row 13-A7, part 2).

Each weekly triage report in ``triage/rxiv/`` carries the eval summary line
"Decided via decide(): N / M", so the committed reports are already the per-run
store; this module reads them and flags a sustained fall in the decided share.
No I/O beyond reading the given report files.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_DECIDED_RE = re.compile(r"Decided via decide\(\):\s*(\d+)\s*/\s*(\d+)")
_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

# Reason: row 13-A7 asks for 4–6 weeks of data before flagging; a 3-run
# baseline plus 3 recent runs is the smallest series that says "sustained".
RECENT_RUNS = 3
MIN_RUNS = 2 * RECENT_RUNS
MAX_DROP = 0.10


@dataclass(frozen=True)
class RunCounts:
    date: str
    decided: int
    total: int

    @property
    def share(self) -> float:
        return self.decided / self.total


def parse_report(text: str) -> tuple[int, int] | None:
    """Return (decided, total) from a triage report, or None if it has no decide() line."""
    m = _DECIDED_RE.search(text)
    if not m or int(m.group(2)) == 0:
        return None
    return int(m.group(1)), int(m.group(2))


def collect(paths: list[Path]) -> list[RunCounts]:
    """Read dated reports (``YYYY-MM-DD-papers.md``) into runs, oldest first."""
    runs = []
    for path in paths:
        counts = parse_report(path.read_text())
        date = _DATE_RE.match(path.name)
        if counts and date:
            runs.append(RunCounts(date.group(1), *counts))
    return sorted(runs, key=lambda r: r.date)


def drift(runs: list[RunCounts]) -> str:
    """Markdown note when each of the last 3 runs' decided share is more than
    MAX_DROP below the mean of the earlier runs; empty string otherwise."""
    if len(runs) < MIN_RUNS:
        return ""
    earlier, recent = runs[:-RECENT_RUNS], runs[-RECENT_RUNS:]
    baseline = sum(r.share for r in earlier) / len(earlier)
    if not all(r.share < baseline - MAX_DROP for r in recent):
        return ""
    recent_mean = sum(r.share for r in recent) / len(recent)
    return (
        f"- Paper run decided share fell: {recent_mean:.2f} over the last {RECENT_RUNS} runs "
        f"(from {recent[0].date}) vs {baseline:.2f} before; more papers are falling back to the chat call.\n"
    )


def table(runs: list[RunCounts]) -> str:
    """Markdown table of each run's counts."""
    rows = [
        "| Run | Decided | Fell back | Total | Decided share |",
        "|---|---|---|---|---|",
    ]
    rows += [f"| {r.date} | {r.decided} | {r.total - r.decided} | {r.total} | {r.share:.2f} |" for r in runs]
    return "\n".join(rows) + "\n"
