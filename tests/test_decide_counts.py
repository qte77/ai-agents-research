"""Unit tests for lib/decide_counts.py — the weekly paper run's decide() share,
read from the committed triage reports (plan 0014 row 13-A7, part 2).
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import decide_counts as dc  # noqa: E402

REPORT = (
    "## ArXiv AI Agents: Relevant Papers\n\n"
    "- Relevant (LLM YES): 67\n"
    "- LLM call failures: 0 / 100 (0 %)\n"
    "- Decided via decide(): 88 / 100 (the rest fell back to the chat call)\n"
)


def _run(date, decided, total=100):
    return dc.RunCounts(date=date, decided=decided, total=total)


class ParseReportTests(unittest.TestCase):
    def test_reads_decided_and_total(self):
        self.assertEqual(dc.parse_report(REPORT), (88, 100))

    def test_report_from_before_decide_returns_none(self):
        # Reports older than plan 0012 P2 have no decide() line; they are not data points.
        self.assertIsNone(dc.parse_report("- LLM call failures: 0 / 100 (0 %)\n"))

    def test_zero_total_returns_none(self):
        self.assertIsNone(dc.parse_report("- Decided via decide(): 0 / 0\n"))


class CollectTests(unittest.TestCase):
    def test_collects_dated_runs_in_date_order_and_skips_reports_without_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            (d / "2026-11-24-papers.md").write_text(REPORT.replace("88 / 100", "80 / 90"))
            (d / "2026-11-17-papers.md").write_text(REPORT)
            (d / "2026-10-06-papers.md").write_text("- LLM call failures: 0 / 100\n")
            runs = dc.collect(sorted(d.glob("*-papers.md")))
        self.assertEqual(runs, [_run("2026-11-17", 88), _run("2026-11-24", 80, 90)])


class DriftTests(unittest.TestCase):
    def test_no_flag_before_enough_runs(self):
        # Reason: row 13-A7 says flag only after 4–6 weeks of data; five runs are not enough.
        runs = [_run(f"2026-12-0{i}", d) for i, d in enumerate([90, 90, 60, 60, 60], start=1)]
        self.assertEqual(dc.drift(runs), "")

    def test_flags_sustained_fall_in_decided_share(self):
        runs = [_run(f"2026-12-0{i}", d) for i, d in enumerate([90, 88, 89, 70, 72, 71], start=1)]
        message = dc.drift(runs)
        self.assertIn("decided share", message)
        self.assertIn("0.89", message)
        self.assertIn("0.71", message)

    def test_one_bad_week_is_not_sustained(self):
        runs = [_run(f"2026-12-0{i}", d) for i, d in enumerate([90, 88, 89, 89, 50, 90], start=1)]
        self.assertEqual(dc.drift(runs), "")

    def test_small_fall_is_not_flagged(self):
        runs = [_run(f"2026-12-0{i}", d) for i, d in enumerate([90, 88, 89, 84, 83, 85], start=1)]
        self.assertEqual(dc.drift(runs), "")


class TableTests(unittest.TestCase):
    def test_markdown_table_lists_each_run_with_its_share(self):
        table = dc.table([_run("2026-11-17", 88)])
        self.assertIn("| 2026-11-17 | 88 | 12 | 100 | 0.88 |", table)


if __name__ == "__main__":
    unittest.main()
