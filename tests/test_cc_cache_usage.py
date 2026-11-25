"""Unit tests for scripts/cc_cache_usage.py (prompt-cache usage of one Claude Code transcript).

Stdlib `unittest`, no deps. Run: python3 -m unittest discover -s tests
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import cc_cache_usage as cu  # noqa: E402


def resp(msg_id, ts, read=0, write=0, w1h=0, uncached=0, out=0, sidechain=False):
    usage = {"cache_read_input_tokens": read, "cache_creation_input_tokens": write,
             "input_tokens": uncached, "output_tokens": out,
             "cache_creation": {"ephemeral_1h_input_tokens": w1h, "ephemeral_5m_input_tokens": write - w1h}}
    return json.dumps({"type": "assistant", "isSidechain": sidechain, "timestamp": ts,
                       "message": {"id": msg_id, "usage": usage}})


def boundary(ts, pre, post, trigger="auto"):
    return json.dumps({"type": "system", "subtype": "compact_boundary", "timestamp": ts,
                       "compactMetadata": {"trigger": trigger, "preTokens": pre, "postTokens": post}})


class SummarizeTests(unittest.TestCase):
    def test_counts_each_response_once_and_skips_subagents(self):
        lines = [
            resp("a", "2026-11-25T10:00:00Z", read=100, write=10, w1h=10, out=5),
            resp("a", "2026-11-25T10:00:01Z", read=100, write=10, w1h=10, out=5),  # streamed repeat
            resp("s", "2026-11-25T10:00:02Z", read=999, sidechain=True),  # subagent: own cache
            "not json",
            resp("b", "2026-11-25T10:05:00Z", read=200, out=7),
        ]
        s = cu.summarize(lines)
        self.assertEqual(s["responses"], 2)
        self.assertEqual(s["read"], 300)
        self.assertEqual(s["write"], 10)
        self.assertEqual(s["write_1h"], 10)
        self.assertEqual(s["output"], 12)

    def test_gap_turns_and_predicted_hit(self):
        lines = [
            resp("a", "2026-11-25T10:00:00Z", read=50),
            resp("b", "2026-11-25T10:30:00Z", read=60),  # 30 min: inside the lifetime
            resp("c", "2026-11-25T12:00:00Z", write=400),  # 90 min: past it
        ]
        s = cu.summarize(lines, gap_min=60, ttl_min=60)
        self.assertEqual([g["gap_min"] for g in s["gaps"]], [90])
        self.assertEqual(s["gaps"][0]["write"], 400)
        self.assertEqual(s["gap_write"], 400)
        # prediction: miss after a gap longer than the lifetime, hit otherwise
        self.assertEqual(s["predicted"], {"hit": 1, "miss": 1})
        self.assertEqual(s["prediction_correct"], 2)

    def test_a_large_new_tool_result_is_not_a_miss(self):
        # Reason: turn b reads everything turn a cached and writes only its new suffix; a rule of
        # "writes > reads" would call it a miss. Turn c reads less than b held: the prefix was rebuilt.
        lines = [
            resp("a", "2026-11-25T10:00:00Z", read=1000, write=200),
            resp("b", "2026-11-25T10:01:00Z", read=1200, write=5000),
            resp("c", "2026-11-25T10:02:00Z", read=0, write=6300),
        ]
        s = cu.summarize(lines, ttl_min=60)
        self.assertEqual(s["actual"], {"hit": 1, "miss": 1})
        self.assertEqual(s["rebuilt"], 6200)

    def test_compactions(self):
        lines = [boundary("2026-11-25T13:32:57Z", 490310, 25638)]
        s = cu.summarize(lines)
        self.assertEqual(s["compactions"], [{"time": "2026-11-25T13:32:57Z", "trigger": "auto",
                                             "pre": 490310, "post": 25638}])


class RobustnessTests(unittest.TestCase):
    def test_skips_non_objects_and_missing_fields(self):
        lines = ["[1]", '"x"', "null", json.dumps({"type": "assistant", "message": {"id": "z"}}),
                 resp("a", "2026-11-25T10:00:00Z", read=5)]
        s = cu.summarize(lines)
        self.assertEqual(s["responses"], 2)  # the timestamp-less response counts, without gap logic
        self.assertEqual(s["read"], 5)

    def test_idless_messages_are_not_merged(self):
        line = json.dumps({"type": "assistant", "timestamp": "2026-11-25T10:00:00Z",
                           "message": {"usage": {"cache_read_input_tokens": 3}}})
        self.assertEqual(cu.summarize([line, line])["responses"], 2)

    def test_keeps_last_chunk_of_a_streamed_message(self):
        lines = [resp("a", "2026-11-25T10:00:00Z", read=100, out=1),
                 resp("a", "2026-11-25T10:00:05Z", read=100, out=40)]
        self.assertEqual(cu.summarize(lines)["output"], 40)

    def test_sidechain_compactions_are_skipped(self):
        d = json.loads(boundary("2026-11-25T13:32:57Z", 10, 5))
        d["isSidechain"] = True
        self.assertEqual(cu.summarize([json.dumps(d)])["compactions"], [])

    def test_lifetime_defaults_from_the_write_buckets(self):
        lines = [resp("a", "2026-11-25T10:00:00Z", write=100, w1h=0),  # 5-minute writes
                 resp("b", "2026-11-25T10:10:00Z", write=100, w1h=0)]
        s = cu.summarize(lines)
        self.assertEqual(s["ttl_min"], 5)
        self.assertEqual(s["predicted"], {"hit": 0, "miss": 1})


if __name__ == "__main__":
    unittest.main()
