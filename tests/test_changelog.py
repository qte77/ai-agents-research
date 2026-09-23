"""Unit tests for lib/changelog.py (pure changelog-vs-docs comparison logic)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import changelog as cl  # noqa: E402

IDX = {"docs/sandbox.md": frozenset({"sandboxing", "controls", "bash"})}

# Verified shape (WebFetch of https://github.com/anthropics/claude-code/releases.atom,
# 2026-09-23; corroborated by issue #410's own quoted <id>/<updated> excerpt). Entries
# below are deliberately out of document order to prove the function sorts, and include
# one entry whose <id> doesn't end in a parseable version to prove it's skipped.
FEED_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-US">
  <entry>
    <id>tag:github.com,2008:Repository/937253475/v2.1.278</id>
    <updated>2026-09-19T03:10:40Z</updated>
    <title>v2.1.278</title>
  </entry>
  <entry>
    <id>tag:github.com,2008:Repository/937253475/v2.1.280</id>
    <updated>2026-09-22T16:38:14Z</updated>
    <title>v2.1.280</title>
  </entry>
  <entry>
    <id>tag:github.com,2008:Repository/937253475/not-a-release</id>
    <updated>2026-01-01T00:00:00Z</updated>
    <title>legacy tag</title>
  </entry>
</feed>
"""


class VersionTupleTests(unittest.TestCase):
    def test_compares(self):
        self.assertTrue(cl.version_tuple("2.1.80") > cl.version_tuple("2.1.71"))


class ScannedVersionTests(unittest.TestCase):
    def test_extracts_range_end(self):
        self.assertEqual(
            cl.extract_scanned_version("---\npurpose: scan (v2.1.0-2.1.71) here\n---\n"),
            "2.1.71",
        )

    def test_none_without_frontmatter_or_range(self):
        self.assertIsNone(cl.extract_scanned_version("no frontmatter"))
        self.assertIsNone(cl.extract_scanned_version("---\npurpose: no range\n---\n"))

    def test_bump(self):
        out = cl.bump_scanned_version("---\npurpose: (v2.1.0-2.1.71)\n---\n", "2.1.85")
        self.assertIn("v2.1.0-2.1.85", out)
        self.assertIsNone(cl.bump_scanned_version("no version", "2.1.85"))


class ParseChangelogTests(unittest.TestCase):
    def test_sections_newest_first_and_feature_lines(self):
        text = "# CL\n\n## 2.1.71\n- Old\n\n## 2.1.80\n- Feature A\n- Feature B\n"
        versions = cl.parse_changelog_versions(text)
        self.assertEqual([v for v, _ in versions], ["2.1.80", "2.1.71"])
        self.assertEqual(versions[0][1], ["- Feature A", "- Feature B"])


class ParseReleasesFeedTests(unittest.TestCase):
    def test_extracts_version_id_and_updated(self):
        entries = cl.parse_releases_feed(FEED_XML)
        newest = entries[0]
        self.assertEqual(newest["version"], "2.1.280")
        self.assertEqual(newest["updated"], "2026-09-22T16:38:14Z")
        self.assertEqual(
            newest["id"], "tag:github.com,2008:Repository/937253475/v2.1.280"
        )

    def test_orders_newest_first_regardless_of_document_order(self):
        entries = cl.parse_releases_feed(FEED_XML)
        self.assertEqual([e["version"] for e in entries], ["2.1.280", "2.1.278"])

    def test_skips_entry_without_parseable_version_id(self):
        entries = cl.parse_releases_feed(FEED_XML)
        self.assertEqual(len(entries), 2)
        self.assertNotIn("not-a-release", [e["version"] for e in entries])

    def test_malformed_xml_returns_empty(self):
        self.assertEqual(cl.parse_releases_feed("<feed><entry><id>oops"), [])

    def test_empty_and_whitespace_return_empty(self):
        self.assertEqual(cl.parse_releases_feed(""), [])
        self.assertEqual(cl.parse_releases_feed("   \n\t  "), [])


class FindCoveringDocsTests(unittest.TestCase):
    def test_covered_uncovered_and_noise(self):
        self.assertEqual(
            cl.find_covering_docs("New sandboxing controls for the bash tool", IDX),
            ["docs/sandbox.md"],
        )
        self.assertEqual(cl.find_covering_docs("Totally unrelated xyzzy widget", IDX), [])
        self.assertEqual(cl.find_covering_docs("- Bug fixes and reliability improvements", IDX), [])


class ReportTests(unittest.TestCase):
    def test_covered(self):
        results = cl.classify_versions(
            [("2.1.80", ["- New sandboxing controls for the bash tool"])], IDX
        )
        report, has_unc = cl.render_changelog_report(results, "2.1.71")
        self.assertIn("## Changelog Monitor Report", report)
        self.assertIn("Last scanned version: **2.1.71**", report)
        self.assertIn("- **[covered]** - New sandboxing controls for the bash tool", report)
        self.assertFalse(has_unc)

    def test_uncovered(self):
        results = cl.classify_versions([("2.2.0", ["- novel xyzzy thing"])], IDX)
        report, has_unc = cl.render_changelog_report(results, "2.1.71")
        self.assertIn("- **[UNCOVERED]** - novel xyzzy thing", report)
        self.assertTrue(has_unc)

    def test_empty(self):
        report, has_unc = cl.render_changelog_report([], "2.1.71")
        self.assertIn("No new versions found", report)
        self.assertFalse(has_unc)

    def test_adds_release_date_when_known(self):
        results = cl.classify_versions([("2.2.0", ["- novel xyzzy thing"])], IDX)
        report, _ = cl.render_changelog_report(
            results, "2.1.71", updated_by_version={"2.2.0": "2026-09-22T16:38:14Z"}
        )
        self.assertIn("#### v2.2.0 — released 2026-09-22", report)

    def test_omits_release_date_when_unknown(self):
        results = cl.classify_versions([("2.2.0", ["- novel xyzzy thing"])], IDX)
        report, _ = cl.render_changelog_report(results, "2.1.71")
        self.assertIn("#### v2.2.0", report)
        self.assertNotIn("released", report)


if __name__ == "__main__":
    unittest.main()
