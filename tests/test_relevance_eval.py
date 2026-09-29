"""Unit tests for lib/relevance_eval.py — pure functions backing the one-off
Cloudflare Workers AI relevance-filter model-comparison eval
(.github/scripts/eval-relevance-models.py).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import relevance_eval as rl  # noqa: E402

CSV_HEADER = "Published,ISOWeek,Updated,ID,Version,Title,Categories,Authors,Abstract\n"
CSV_ROWS = (
    "2026-07-24T00:00:00Z,30,2026-07-24T00:00:00Z,2607.001,1,'Paper A',cs.AI;cs.LG,Auth A,Abstract A\n"
    "2026-07-24T00:00:00Z,30,2026-07-24T00:00:00Z,2607.002,1,Paper B,cs.CV,Auth B,Abstract B\n"
    "2026-07-24T00:00:00Z,30,2026-07-24T00:00:00Z,2607.003,1,Paper C,cs.RO,Auth C,Abstract C\n"
)


class ParseVerdictTests(unittest.TestCase):
    def test_yes_and_no(self):
        self.assertEqual(rl.parse_verdict("YES"), "YES")
        self.assertEqual(rl.parse_verdict("no, not relevant"), "NO")

    def test_empty_and_none_are_unparseable(self):
        self.assertEqual(rl.parse_verdict(""), "UNPARSEABLE")
        self.assertEqual(rl.parse_verdict(None), "UNPARSEABLE")
        self.assertEqual(rl.parse_verdict("   "), "UNPARSEABLE")

    def test_closed_think_block_stripped_before_yes_check(self):
        raw = "<think>reasoning about the topic</think>\nYES"
        self.assertEqual(rl.parse_verdict(raw, strip_think=True), "YES")
        # Strict (no stripping) mirrors production exactly: the leading
        # "<think" text defeats startswith("YES") -> NO, not UNPARSEABLE.
        self.assertEqual(rl.parse_verdict(raw, strip_think=False), "NO")

    def test_unclosed_think_block_is_unparseable_under_relaxed(self):
        # max_tokens cut the model off mid-reasoning: no closed </think>, so
        # no answer was actually emitted -- that's a distinct failure mode
        # from a genuine NO, not a NO itself.
        raw = "<think>still reasoning when the token budget ran out"
        self.assertEqual(rl.parse_verdict(raw, strip_think=True), "UNPARSEABLE")


class BuildLabelledSetTests(unittest.TestCase):
    def test_caps_labels_and_normalizes_category_and_title(self):
        csv_text = CSV_HEADER + CSV_ROWS
        rows = rl.build_labelled_set(csv_text, {"2607.001"}, cap=2)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["label"], "YES")
        self.assertEqual(rows[1]["label"], "NO")
        # Primary category only (before the first ';').
        self.assertEqual(rows[0]["category"], "cs.AI")
        # Quoted title has the wrapping single-quotes stripped.
        self.assertEqual(rows[0]["title"], "Paper A")


class ComputeMetricsTests(unittest.TestCase):
    def test_agreement_false_accept_reject_and_unparseable(self):
        records = [
            {"pred": "YES", "label": "YES", "latency": 1.0},
            {"pred": "NO", "label": "NO", "latency": 2.0},
            {"pred": "YES", "label": "NO", "latency": 1.5},   # false accept
            {"pred": "NO", "label": "YES", "latency": 0.5},   # false reject
            {"pred": "UNPARSEABLE", "label": "YES", "latency": 3.0},
            {"pred": "UNPARSEABLE", "label": "NO", "latency": None},  # failed call: no latency
        ]
        m = rl.compute_metrics(records)
        self.assertEqual(m["n"], 6)
        self.assertEqual(m["unparseable"], 2)
        self.assertEqual(m["false_accept"], 1)
        self.assertEqual(m["false_reject"], 1)
        # Denominator is total calls n (unparseable counts against
        # agreement, not excluded from it): 2 agreements / 6 = 33.3%.
        self.assertEqual(m["agreement_pct"], 33.3)
        # A failed call's None latency is excluded from mean/p95 rather than
        # dragging them toward zero.
        self.assertEqual(m["mean_latency_s"], round((1.0 + 2.0 + 1.5 + 0.5 + 3.0) / 5, 3))
        # Invariant: every record is exactly one of agree/FA/FR/unparseable.
        agree = sum(1 for r in records if r["pred"] == r["label"])
        self.assertEqual(agree + m["false_accept"] + m["false_reject"] + m["unparseable"], m["n"])


if __name__ == "__main__":
    unittest.main()
