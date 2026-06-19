"""Unit tests for lib/changelog.py (pure changelog-vs-docs comparison logic)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import changelog as cl  # noqa: E402

IDX = {"docs/sandbox.md": frozenset({"sandboxing", "controls", "bash"})}


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


if __name__ == "__main__":
    unittest.main()
