"""Unit tests for lib/decision_eval.py (decision-model calibration on the G1 gold sets).

Run: python3 -m unittest discover -s tests
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import decision_eval as de  # noqa: E402


class RocAucTests(unittest.TestCase):
    def test_perfect_separation_is_one(self):
        self.assertEqual(de.roc_auc([0.1, 0.2, 0.8, 0.9], [False, False, True, True]), 1.0)

    def test_inverted_separation_is_zero(self):
        self.assertEqual(de.roc_auc([0.9, 0.8, 0.2, 0.1], [False, False, True, True]), 0.0)

    def test_ties_count_half(self):
        # Every positive ties every negative: AUC = 0.5.
        self.assertEqual(de.roc_auc([0.5, 0.5, 0.5, 0.5], [False, True, False, True]), 0.5)

    def test_partial_overlap(self):
        # Positives 0.6, 0.9; negatives 0.3, 0.7 -> pairs won: (0.6>0.3), (0.9>0.3), (0.9>0.7) = 3 of 4.
        self.assertEqual(de.roc_auc([0.3, 0.7, 0.6, 0.9], [False, False, True, True]), 0.75)

    def test_single_class_is_undefined(self):
        self.assertIsNone(de.roc_auc([0.2, 0.9], [True, True]))


class BrierTests(unittest.TestCase):
    def test_perfect_is_zero(self):
        self.assertEqual(de.brier([1.0, 0.0], [True, False]), 0.0)

    def test_coin_flip_is_quarter(self):
        self.assertEqual(de.brier([0.5, 0.5], [True, False]), 0.25)


class BootstrapTests(unittest.TestCase):
    def test_same_seed_same_interval_and_bounds_ordered(self):
        probs = [0.1, 0.4, 0.35, 0.8, 0.7, 0.9, 0.2, 0.65]
        labels = [False, False, True, True, True, True, False, False]
        a = de.bootstrap_ci(de.roc_auc, probs, labels, n=200, seed=7)
        b = de.bootstrap_ci(de.roc_auc, probs, labels, n=200, seed=7)
        self.assertEqual(a, b)
        low, high = a
        self.assertLessEqual(low, high)
        self.assertGreaterEqual(low, 0.0)
        self.assertLessEqual(high, 1.0)

    def test_undefined_resamples_are_skipped(self):
        # One negative among many positives: many resamples have one class; must not crash.
        probs = [0.9] * 9 + [0.1]
        labels = [True] * 9 + [False]
        low, high = de.bootstrap_ci(de.roc_auc, probs, labels, n=100, seed=1)
        self.assertEqual((low, high), (1.0, 1.0))


class SweepTests(unittest.TestCase):
    PROBS = [0.95, 0.9, 0.6, 0.4, 0.1, 0.05]
    LABELS = [True, False, True, True, False, False]

    def test_counts_per_threshold(self):
        row = de.sweep(self.PROBS, self.LABELS, [0.85])[0]
        # act-true: 0.95 (T), 0.9 (F) -> 1 false accept; act-false (<=0.15): 0.1, 0.05 (both F) -> 0 false rejects.
        self.assertEqual(row["hi"], 0.85)
        self.assertEqual(row["acted"], 4)
        self.assertEqual(row["review"], 2)
        self.assertEqual(row["false_accepts"], 1)
        self.assertEqual(row["false_rejects"], 0)
        self.assertAlmostEqual(row["coverage"], 4 / 6)
        self.assertAlmostEqual(row["error_rate"], 1 / 4)

    def test_recommend_picks_smallest_hi_meeting_the_rule(self):
        rows = de.sweep(self.PROBS, self.LABELS, [0.5, 0.85, 0.92])
        # 0.5: everything acts, 0.4 (T) is a false reject and 0.9 (F) a false accept -> 2/6.
        # 0.85: 1/4. 0.92: act-true 0.95 (T); act-false (<=0.08) 0.05 (F) -> 0/2.
        best = de.recommend_hi(rows, max_error_rate=0.05)
        self.assertEqual(best["hi"], 0.92)

    def test_recommend_returns_none_when_no_threshold_qualifies(self):
        rows = de.sweep(self.PROBS, self.LABELS, [0.5])
        self.assertIsNone(de.recommend_hi(rows, max_error_rate=0.05))


class GoldAndStateTests(unittest.TestCase):
    def test_load_gold_joins_items_and_labels_by_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            items = Path(tmp, "x.items.jsonl")
            labels = Path(tmp, "x.labels.jsonl")
            items.write_text(
                json.dumps({"id": "a", "title": "T", "text": "B", "context": "C", "source": "u"}) + "\n"
            )
            labels.write_text(json.dumps({"id": "a", "label": True, "confidence": "high"}) + "\n")
            gold = de.load_gold(items, labels)
        self.assertEqual(gold, [{"id": "a", "title": "T", "text": "B", "context": "C", "label": True}])

    def test_issue_state_uses_the_labellers_inputs(self):
        state = de.issue_state({"title": "Fix typo", "text": "pip instal", "context": "A toolkit."})
        for part in ("A toolkit.", "Fix typo", "pip instal"):
            self.assertIn(part, state)

    def test_paper_question_is_agent_strict_without_the_token_instruction(self):
        q = de.PAPER_QUESTION["instructions"]
        self.assertIn("When unsure, answer NO.", q)
        self.assertIn(de.GOLD_PAPER_TOPIC, q)
        self.assertNotIn("single token", q)
        self.assertEqual(de.PAPER_QUESTION["type"], "predicate")


class TransientTests(unittest.TestCase):
    def test_rate_limit_and_server_errors_are_transient(self):
        for error in ("HTTP 429 Too Many Requests", "HTTP 503: unavailable", "request timed out"):
            self.assertTrue(de.is_transient(error), error)

    def test_auth_and_shape_errors_are_not(self):
        for error in ("HTTP 401 Unauthorized", "missing CF_WORKERS_AI_TOKEN", None):
            self.assertFalse(de.is_transient(error), error)


if __name__ == "__main__":
    unittest.main()


class CompareToBaselineTests(unittest.TestCase):
    BASE = {
        "papers/clef:clef": {"auc": 0.970, "brier": 0.061, "recommended_hi": 0.75},
        "issues/clef:clef": {"auc": None, "brier": 0.009, "recommended_hi": 0.50},
    }

    def test_no_findings_within_tolerance(self):
        current = {
            "papers/clef:clef": {"auc": 0.950, "brier": 0.070, "recommended_hi": 0.75},
            "issues/clef:clef": {"auc": None, "brier": 0.010, "recommended_hi": 0.50},
        }
        self.assertEqual(de.compare_to_baseline(current, self.BASE), [])

    def test_auc_drop_above_tolerance_is_flagged(self):
        current = {"papers/clef:clef": {"auc": 0.930, "brier": 0.061, "recommended_hi": 0.75}}
        findings = de.compare_to_baseline(current, self.BASE)
        self.assertEqual(len(findings), 1)
        self.assertIn("papers/clef:clef", findings[0])
        self.assertIn("0.970", findings[0])
        self.assertIn("0.930", findings[0])

    def test_hi_move_of_a_step_and_more_is_flagged(self):
        current = {"papers/clef:clef": {"auc": 0.970, "brier": 0.061, "recommended_hi": 0.85}}
        findings = de.compare_to_baseline(current, self.BASE)
        self.assertEqual(len(findings), 1)
        self.assertIn("hi", findings[0])

    def test_hi_lost_is_flagged(self):
        current = {"issues/clef:clef": {"auc": None, "brier": 0.2, "recommended_hi": None}}
        findings = de.compare_to_baseline(current, self.BASE)
        self.assertEqual(len(findings), 1)
        self.assertIn("no hi meets the rule", findings[0])

    def test_brier_alone_is_never_flagged(self):
        current = {"papers/clef:clef": {"auc": 0.970, "brier": 0.300, "recommended_hi": 0.75}}
        self.assertEqual(de.compare_to_baseline(current, self.BASE), [])

    def test_keys_missing_on_either_side_are_skipped(self):
        current = {"papers/jev:jev-1.13.0": {"auc": 0.5, "brier": 0.3, "recommended_hi": None}}
        self.assertEqual(de.compare_to_baseline(current, self.BASE), [])


class BaselineFileTests(unittest.TestCase):
    def test_committed_baseline_has_the_metric_keys(self):
        path = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "data" / "gold" / "baseline.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertIn("papers/clef:clef", data["metrics"])
        for entry in data["metrics"].values():
            self.assertTrue({"auc", "brier", "recommended_hi"} <= set(entry))
