"""Unit tests for lib/community_sources.py (pure markdown + HTML extractors)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import community_sources as cs  # noqa: E402


class MarkdownTests(unittest.TestCase):
    def test_link_and_bold_items_under_heading(self):
        md = (
            "## Tools\n"
            "- [Ruff](https://ruff.rs) - fast linter\n"
            "- **Black** - formatter\n"
            "not a list line\n"
        )
        entries = cs.extract_markdown_entries(md)
        self.assertEqual(entries, [
            {"heading": "Tools", "name": "Ruff", "url": "https://ruff.rs", "description": "fast linter"},
            {"heading": "Tools", "name": "Black", "url": "", "description": "formatter"},
        ])


class HtmlTests(unittest.TestCase):
    def test_strips_script_tracks_version_heading_and_matches_features(self):
        html = (
            "<script>junk</script>"
            "<p>v2.1.80 release notes</p>"
            "<p>Added new plugin support for hooks and skills</p>"
            "<p>tiny</p>"
            "<p>just prose without any matching terms at all here</p>"
        )
        entries = cs.extract_html_entries(html)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["heading"], "v2.1.80 release notes")
        self.assertEqual(entries[0]["description"], "Added new plugin support for hooks and skills")
        self.assertNotIn("junk", entries[0]["description"])


if __name__ == "__main__":
    unittest.main()
