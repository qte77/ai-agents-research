"""Unit tests for lib/plan_reconcile.py (plan remaining-work rows vs live PR/issue state).

Run: python3 -m unittest discover -s tests
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import plan_reconcile as pr  # noqa: E402

PLAN = """---
title: x
---

## Current status

Mentions #999 here, which is not a table row.

## Remaining work

| Row | Item | Gate | Done when |
|---|---|---|---|
| ~~T0~~ | ~~Tracking issue~~ | agent | Shipped: #652 |
| D0 | `decide` action, PR qte77/.github#45 | owner | merged |
| C1 | consumer PRs analyze-stock-kpi#512, vlm-toolkit#20 | owner | live check |
| K0 | create keys; rerun fixed (#703) | owner | secrets set |
| Q1 | no references at all | agent | done |

**Loop (not rows):** #741 is a weekly bot PR.

## Sources

| Source | Content |
|---|---|
| #123 | not a work row |
"""


class ExtractRefsTests(unittest.TestCase):
    def test_bare_number_uses_default_repo(self):
        self.assertEqual(pr.extract_refs("see #652", "qte77/aar"), [("qte77/aar", 652)])

    def test_owner_repo_ref(self):
        self.assertEqual(pr.extract_refs("PR qte77/.github#45", "qte77/aar"), [("qte77/.github", 45)])

    def test_bare_repo_name_defaults_to_default_owner(self):
        self.assertEqual(
            pr.extract_refs("analyze-stock-kpi#512 and vlm-toolkit#20", "qte77/aar"),
            [("qte77/analyze-stock-kpi", 512), ("qte77/vlm-toolkit", 20)],
        )

    def test_refs_in_code_spans_are_context_not_deciders(self):
        self.assertEqual(pr.extract_refs("history `#703`, tracker `o/r#652`; waits on #12", "o/r"),
                         [("o/r", 12)])

    def test_ignores_non_numeric_anchors_and_duplicates(self):
        self.assertEqual(
            pr.extract_refs("[a](#settings-precedence) #12 and again #12", "o/r"),
            [("o/r", 12)],
        )


class RemainingRowsTests(unittest.TestCase):
    def test_only_rows_of_the_remaining_work_table(self):
        rows = pr.remaining_rows(PLAN)
        self.assertEqual([r.row_id for r in rows], ["T0", "D0", "C1", "K0", "Q1"])

    def test_struck_rows_detected(self):
        rows = {r.row_id: r for r in pr.remaining_rows(PLAN)}
        self.assertTrue(rows["T0"].struck)
        self.assertFalse(rows["D0"].struck)

    def test_missing_section_returns_empty(self):
        self.assertEqual(pr.remaining_rows("## Other\n\n| a | b |\n"), [])


class AssessTests(unittest.TestCase):
    def _row(self, row_id):
        return {r.row_id: r for r in pr.remaining_rows(PLAN)}[row_id]

    def test_open_row_whose_refs_are_all_done_is_flagged(self):
        flag = pr.assess(self._row("D0"), {("qte77/.github", 45): "merged"}, "qte77/aar")
        self.assertIn("all referenced", flag)

    def test_open_row_with_an_open_ref_is_not_flagged(self):
        states = {("qte77/analyze-stock-kpi", 512): "merged", ("qte77/vlm-toolkit", 20): "open"}
        self.assertEqual(pr.assess(self._row("C1"), states, "qte77/aar"), "")

    def test_struck_row_with_an_open_ref_is_flagged(self):
        flag = pr.assess(self._row("T0"), {("qte77/aar", 652): "open"}, "qte77/aar")
        self.assertIn("struck", flag)

    def test_row_without_refs_is_not_flagged(self):
        self.assertEqual(pr.assess(self._row("Q1"), {}, "qte77/aar"), "")

    def test_unknown_state_is_reported_not_guessed(self):
        flag = pr.assess(self._row("D0"), {("qte77/.github", 45): None}, "qte77/aar")
        self.assertIn("could not check", flag)


class UncheckedOpenRowsTests(unittest.TestCase):
    def test_open_rows_without_checkable_refs_are_listed(self):
        rows = pr.remaining_rows(PLAN)
        # Q1 has no reference; T0 is struck; D0/C1/K0 each cite at least one checkable ref.
        self.assertEqual(pr.unchecked_open_rows(rows, "qte77/ai-agents-research"), ["Q1"])

    def test_refs_only_in_code_spans_count_as_unchecked(self):
        rows = [pr.Row(row_id="H1", struck=False, text="| H1 | after `qte77/.github#47` | agent | x |")]
        self.assertEqual(pr.unchecked_open_rows(rows, "qte77/ai-agents-research"), ["H1"])


if __name__ == "__main__":
    unittest.main()
