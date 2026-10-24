"""Unit tests for lib/m365_drift.py (pure drift extraction/diff/report logic).

Run: python3 -m unittest discover -s tests
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import m365_drift as md  # noqa: E402


class ExtractMsDateTests(unittest.TestCase):
    def test_extracts_iso_date_from_meta_tag(self):
        html = '<head><meta name="ms.date" content="2026-09-25T00:00:00Z" /></head>'
        self.assertEqual(md.extract_ms_date(html), "2026-09-25T00:00:00Z")

    def test_attribute_order_agnostic(self):
        html = '<meta content="2026-10-22T00:00:00Z" name="ms.date">'
        self.assertEqual(md.extract_ms_date(html), "2026-10-22T00:00:00Z")

    def test_single_quoted_attributes(self):
        html = "<meta name='ms.date' content='2026-07-31T00:00:00Z'>"
        self.assertEqual(md.extract_ms_date(html), "2026-07-31T00:00:00Z")

    def test_none_when_tag_absent(self):
        self.assertIsNone(md.extract_ms_date("<head><meta name=\"other\" content=\"x\"></head>"))

    def test_ignores_unrelated_meta_tags(self):
        html = '<meta name="description" content="x"><meta name="ms.date" content="2026-01-01T00:00:00Z">'
        self.assertEqual(md.extract_ms_date(html), "2026-01-01T00:00:00Z")


class QuotePresentTests(unittest.TestCase):
    def test_finds_plain_quote(self):
        html = "<p>You don't need to configure a model to use Copilot in SharePoint.</p>"
        self.assertTrue(md.quote_present(html, "You don't need to configure a model to use Copilot in SharePoint"))

    def test_missing_quote_returns_false(self):
        html = "<p>Something completely different.</p>"
        self.assertFalse(md.quote_present(html, "You don't need to configure a model"))

    def test_whitespace_normalised_across_line_breaks(self):
        html = "<p>You don't need\n  to configure   a model</p>"
        self.assertTrue(md.quote_present(html, "You don't need to configure a model"))

    def test_strips_inline_tags_between_words(self):
        html = "<p>You don't need to <b>configure</b> a model</p>"
        self.assertTrue(md.quote_present(html, "You don't need to configure a model"))

    def test_typographic_apostrophe_normalised(self):
        html = "<p>You don’t need to configure a model</p>"
        self.assertTrue(md.quote_present(html, "You don't need to configure a model"))

    def test_case_sensitive(self):
        html = "<p>you don't need to configure a model</p>"
        self.assertFalse(md.quote_present(html, "You don't need to configure a model"))

    def test_ignores_script_and_style_blocks(self):
        html = "<style>.x{content:'You dont need'}</style><p>You don't need to configure a model</p>"
        self.assertTrue(md.quote_present(html, "You don't need to configure a model"))


class DiffEntriesTests(unittest.TestCase):
    def _prev(self, ms_date="2026-09-25T00:00:00Z", quote="Q"):
        return {"https://x": {"quote": quote, "ms_date": ms_date}}

    def test_no_change(self):
        prev = self._prev()
        obs = [{"url": "https://x", "quote": "Q", "ms_date": "2026-09-25T00:00:00Z",
                "quote_found": True, "error": None}]
        self.assertEqual(md.diff_entries(prev, obs), [])

    def test_date_changed(self):
        prev = self._prev()
        obs = [{"url": "https://x", "quote": "Q", "ms_date": "2026-10-22T00:00:00Z",
                "quote_found": True, "error": None}]
        diffs = md.diff_entries(prev, obs)
        self.assertEqual(len(diffs), 1)
        d = diffs[0]
        self.assertEqual(d["url"], "https://x")
        self.assertEqual(d["old_date"], "2026-09-25T00:00:00Z")
        self.assertEqual(d["new_date"], "2026-10-22T00:00:00Z")
        self.assertTrue(d["quote_found"])
        self.assertFalse(d["fetch_failed"])

    def test_quote_missing(self):
        prev = self._prev()
        obs = [{"url": "https://x", "quote": "Q", "ms_date": "2026-09-25T00:00:00Z",
                "quote_found": False, "error": None}]
        diffs = md.diff_entries(prev, obs)
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0]["old_date"], diffs[0]["new_date"])
        self.assertFalse(diffs[0]["quote_found"])
        self.assertFalse(diffs[0]["fetch_failed"])

    def test_fetch_failed_reported_separately_not_as_drift(self):
        prev = self._prev()
        obs = [{"url": "https://x", "quote": "Q", "ms_date": None,
                "quote_found": None, "error": "HTTP 503"}]
        diffs = md.diff_entries(prev, obs)
        self.assertEqual(len(diffs), 1)
        d = diffs[0]
        self.assertTrue(d["fetch_failed"])
        self.assertEqual(d["error"], "HTTP 503")
        self.assertEqual(d["old_date"], "2026-09-25T00:00:00Z")
        self.assertIsNone(d["new_date"])

    def test_multiple_entries_only_changed_ones_returned(self):
        prev = {
            "https://a": {"quote": "QA", "ms_date": "2026-01-01T00:00:00Z"},
            "https://b": {"quote": "QB", "ms_date": "2026-01-01T00:00:00Z"},
        }
        obs = [
            {"url": "https://a", "quote": "QA", "ms_date": "2026-01-01T00:00:00Z",
             "quote_found": True, "error": None},
            {"url": "https://b", "quote": "QB", "ms_date": "2026-02-02T00:00:00Z",
             "quote_found": True, "error": None},
        ]
        diffs = md.diff_entries(prev, obs)
        self.assertEqual([d["url"] for d in diffs], ["https://b"])


class RenderReportTests(unittest.TestCase):
    def test_empty_when_nothing_changed(self):
        self.assertEqual(md.render_report([]), "")

    def test_renders_date_change_and_quote_status(self):
        diffs = [{
            "url": "https://x", "old_date": "2026-09-25T00:00:00Z",
            "new_date": "2026-10-22T00:00:00Z", "quote_found": True,
            "fetch_failed": False, "error": None,
        }]
        report = md.render_report(diffs)
        self.assertIn("https://x", report)
        self.assertIn("2026-09-25T00:00:00Z", report)
        self.assertIn("2026-10-22T00:00:00Z", report)
        self.assertIn("Quote still present: yes", report)

    def test_renders_quote_missing_as_no(self):
        diffs = [{
            "url": "https://x", "old_date": "d", "new_date": "d", "quote_found": False,
            "fetch_failed": False, "error": None,
        }]
        self.assertIn("Quote still present: no", md.render_report(diffs))

    def test_renders_fetch_failure_as_could_not_check_not_drift(self):
        diffs = [{
            "url": "https://x", "old_date": "d", "new_date": None, "quote_found": None,
            "fetch_failed": True, "error": "HTTP 503",
        }]
        report = md.render_report(diffs)
        self.assertIn("Could not check", report)
        self.assertIn("HTTP 503", report)
        self.assertNotIn("Quote still present", report)


if __name__ == "__main__":
    unittest.main()
