"""Unit tests for lib/doc_census.py — the rubric-row census behind the reference architecture (plan 0010 T1)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import doc_census as dc  # noqa: E402

HEADER = "| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |\n|---|---|---|---|---|---|\n"

TABLE_DOC = (
    "## Tool A\n\nScored 2026-10-02 · subject: skills\n\n"
    + HEADER
    + "| yes [s][s] (why) | partial (why) | no data (why) | yes (why) | no [s][s] (why) | n/a (why) |\n"
    "\nAfter.\n"
)

INLINE_DOC = (
    "## Tool B\n\n- [B](https://x) does things. **Rubric** (scored 2026-09-30, subject: harness, [README](https://x)): "
    "Shared: partial (a; b); Distributed: no data (c); Reproducible: no (d); Adaptable: yes (e); "
    "Versionable: yes (f); Traceable: partial (g).\n"
)


class ParseTests(unittest.TestCase):
    def test_table_row_scores_subject_and_date(self):
        rows = dc.parse_rows("docs/a.md", TABLE_DOC)
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r.scores, {"Shared": "yes", "Distributed": "partial", "Reproducible": "no data",
                                    "Adaptable": "yes", "Versionable": "no", "Traceable": "n/a"})
        self.assertEqual((r.subject, r.scored, r.form, r.line), ("skills", "2026-10-02", "table", 7))

    def test_inline_row_scores_subject_and_date(self):
        rows = dc.parse_rows("docs/b.md", INLINE_DOC)
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r.scores["Shared"], "partial")
        self.assertEqual(r.scores["Distributed"], "no data")
        self.assertEqual(r.scores["Reproducible"], "no")
        self.assertEqual((r.subject, r.scored, r.form), ("harness", "2026-09-30", "inline"))

    def test_row_without_subject_is_unassigned_not_guessed(self):
        doc = "## Tool C\n\nScored 2026-10-02.\n\n" + HEADER + "| yes | yes | yes | yes | yes | yes |\n"
        self.assertIsNone(dc.parse_rows("docs/c.md", doc)[0].subject)

    def test_indented_table_inside_a_list_item(self):
        doc = "## Tool D\n\n- item\n\n  " + HEADER.replace("\n|", "\n  |") + "  | yes | no | no | no | no | no |\n"
        rows = dc.parse_rows("docs/d.md", doc)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].scores["Shared"], "yes")

    def test_leading_tool_column_names_the_row(self):
        doc = ("## Rubric\n\nScored 2026-09-30 · subject: long-running\n\n"
               "| Tool | Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |\n"
               "|---|---|---|---|---|---|---|\n"
               "| triagebot | no data | yes | partial | yes | partial | yes |\n")
        rows = dc.parse_rows("docs/e.md", doc)
        self.assertEqual(len(rows), 1)
        self.assertEqual((rows[0].heading, rows[0].scores["Distributed"], rows[0].subject),
                         ("triagebot", "yes", "long-running"))

    def test_heading_is_recorded(self):
        self.assertEqual(dc.parse_rows("docs/a.md", TABLE_DOC)[0].heading, "Tool A")

    def test_meta_pages_are_excluded(self):
        self.assertEqual(dc.parse_rows("docs/sdlc-lcm/agent-substrate-rubric.md", TABLE_DOC), [])
        self.assertEqual(dc.parse_rows("docs/sdlc-lcm/agent-substrate-reference-architecture.md", TABLE_DOC), [])


class MatrixTests(unittest.TestCase):
    def _row(self, subject, shared, tool="t"):
        return dc.Row(path="docs/x.md", line=1, form="table", heading=tool, subject=subject,
                      scored="2026-10-02", scores={p: "no data" for p in dc.PROPERTIES} | {"Shared": shared})

    def test_rank_order(self):
        self.assertEqual(sorted(["n/a", "no", "yes", "no data", "partial"], key=dc.rank, reverse=True),
                         ["yes", "partial", "no", "no data", "n/a"])

    def test_best_per_cell_picks_highest_rank(self):
        best = dc.best_per_cell([self._row("skills", "no", "low"), self._row("skills", "partial", "high")])
        token, row = best[("skills", "Shared")]
        self.assertEqual((token, row.heading), ("partial", "high"))

    def test_unassigned_rows_do_not_enter_the_matrix(self):
        self.assertEqual(dc.best_per_cell([self._row(None, "yes")]), {})

    def test_cell_label_distinguishes_open_kinds(self):
        self.assertEqual(dc.cell_label(None), "open (no row)")
        self.assertEqual(dc.cell_label(("no data", None)), "open (best: no data)")
        self.assertEqual(dc.cell_label(("no", None)), "open (best: no)")
        self.assertEqual(dc.cell_label(("partial", None)), "partial")


if __name__ == "__main__":
    unittest.main()
