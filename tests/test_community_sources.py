"""Unit tests for lib/community_sources.py (pure markdown extractor)."""
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


if __name__ == "__main__":
    unittest.main()
