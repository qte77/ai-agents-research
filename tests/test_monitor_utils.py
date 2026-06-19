"""Unit tests for the shared monitor lib (.github/scripts/lib/monitor_utils.py).

Tests the module's pure logic only (the hyphenated entry scripts are thin IO
wrappers and are not imported here). Stdlib `unittest`, no deps.

Run: python3 -m unittest discover -s tests
"""
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts" / "lib"))

import monitor_utils as mu  # noqa: E402


class ExtractKeywordsTests(unittest.TestCase):
    def test_lowercases_and_filters_short(self):
        kw = mu.extract_keywords("Hello Foo subagent x ab")
        self.assertIn("hello", kw)
        self.assertIn("subagent", kw)
        self.assertNotIn("foo", kw)  # 3 chars < min_len 4
        self.assertNotIn("ab", kw)

    def test_keeps_slash_hyphen_tokens(self):
        self.assertIn("a/b-c", mu.extract_keywords("token a/b-c here"))


class IsCoveredTests(unittest.TestCase):
    def test_covered_when_overlap_exceeds_threshold(self):
        docs = {"subagent", "orchestration", "spawning"}
        entry = {"name": "Subagent orchestration", "description": "spawning"}
        self.assertTrue(mu.is_covered(entry, docs))

    def test_uncovered_when_below_threshold(self):
        docs = {"unrelated", "words"}
        entry = {"name": "Subagent orchestration spawning", "description": ""}
        self.assertFalse(mu.is_covered(entry, docs))

    def test_empty_keywords_treated_as_covered(self):
        # Only noise words -> no meaningful keywords -> covered (skip).
        self.assertTrue(mu.is_covered({"name": "claude code", "description": ""}, set()))


class EntryFingerprintTests(unittest.TestCase):
    def test_stable_and_16_hex(self):
        fp = mu.entry_fingerprint({"name": "X", "url": "http://a"})
        self.assertEqual(len(fp), 16)
        self.assertEqual(fp, mu.entry_fingerprint({"name": "x", "url": "HTTP://A"}))  # case-insensitive

    def test_distinct_entries_differ(self):
        self.assertNotEqual(
            mu.entry_fingerprint({"name": "A", "url": "u"}),
            mu.entry_fingerprint({"name": "B", "url": "u"}),
        )


class CleanTableCellTests(unittest.TestCase):
    def test_strips_url_escapes_pipe_collapses_ws_and_truncates(self):
        out = mu._clean_table_cell("see https://x.com/y  a|b\nc   d", 6)
        self.assertNotIn("http", out)
        self.assertNotIn("\n", out)
        self.assertEqual(out, "see a\\")  # pipe escaped, ws collapsed, clipped to 6


class StripHtmlNoiseTests(unittest.TestCase):
    def test_strips_script_style_case_and_whitespace_insensitive(self):
        html = "<script>a</script >B<STYLE x>c</STYLE>D<script\n>e</script\t bar>F"
        self.assertEqual(mu.strip_html_noise(html), "BDF")


class LoadJsonlTests(unittest.TestCase):
    def test_reads_skipping_blank_lines(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.jsonl"
            p.write_text('{"a": 1}\n\n  \n{"a": 2}\n', encoding="utf-8")
            self.assertEqual(mu.load_jsonl(p), [{"a": 1}, {"a": 2}])

    def test_missing_file_returns_empty(self):
        self.assertEqual(mu.load_jsonl(Path("/nonexistent/x.jsonl")), [])


class ParseIsoTests(unittest.TestCase):
    def test_parses_trailing_z_as_utc(self):
        self.assertEqual(
            mu.parse_iso("2026-06-18T12:00:00Z"),
            datetime(2026, 6, 18, 12, 0, tzinfo=timezone.utc),
        )

    def test_empty_and_invalid_return_none(self):
        self.assertIsNone(mu.parse_iso(""))
        self.assertIsNone(mu.parse_iso("not-a-date"))


class FatalTests(unittest.TestCase):
    def test_exits_with_code(self):
        with self.assertRaises(SystemExit) as cm:
            mu.fatal("boom", code=2)
        self.assertEqual(cm.exception.code, 2)


class ProcessSourceTests(unittest.TestCase):
    def test_filters_seen_and_covered(self):
        source = {"name": "s", "description": "d"}
        entries = [
            {"name": "Fresh subagent topic", "url": "u1", "description": ""},  # new
            {"name": "Already seen", "url": "u2", "description": ""},          # seen
            {"name": "covered thing", "url": "u3", "description": ""},         # covered
        ]
        seen = {mu.entry_fingerprint(entries[1])}
        doc_keywords = {"covered", "thing"}
        result, fingerprints = mu._process_source(
            source, lambda _s: entries, seen, doc_keywords
        )
        self.assertEqual(result["total"], 3)
        self.assertEqual([e["name"] for e in result["new_entries"]], ["Fresh subagent topic"])
        self.assertEqual(len(fingerprints), 3)


class BuildReportTests(unittest.TestCase):
    def _result(self, new_entries):
        return {"name": "Src", "description": "desc", "total": len(new_entries), "new_entries": new_entries}

    def test_has_new_and_renders_table(self):
        results = [self._result([{"name": "E1", "heading": "H", "description": "about subagents"}])]
        report, has_new = mu.build_report(results, "My Report", "x.py")
        self.assertTrue(has_new)
        self.assertIn("## My Report", report)
        self.assertIn("### Src", report)
        self.assertIn("| E1 | H | about subagents |", report)
        self.assertIn("Total new uncovered entries: **1**", report)
        self.assertIn("_Generated by `.github/scripts/x.py`_", report)

    def test_no_new_content(self):
        _, has_new = mu.build_report([self._result([])], "T", "x.py")
        self.assertFalse(has_new)

    def test_truncates_over_30(self):
        entries = [{"name": f"E{i}", "heading": "", "description": ""} for i in range(35)]
        report, _ = mu.build_report([self._result(entries)], "T", "x.py")
        self.assertIn("_... and 5 more entries._", report)


if __name__ == "__main__":
    unittest.main()
