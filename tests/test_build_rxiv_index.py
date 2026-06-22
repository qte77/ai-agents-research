"""Regression tests for build-rxiv-index render() — MD012 (no consecutive blank lines).

The script filename is hyphenated (not a valid module name), so it is loaded via
importlib rather than imported. Run: python3 -m unittest discover -s tests
"""
import importlib.util
import unittest
from pathlib import Path

_SCRIPT = (
    Path(__file__).resolve().parents[1] / ".github" / "scripts" / "build-rxiv-index.py"
)
_spec = importlib.util.spec_from_file_location("build_rxiv_index", _SCRIPT)
build_rxiv_index = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_rxiv_index)


def _record(extracted, title="Some Paper", doi="2601.00001"):
    return {
        "title": title,
        "doi": doi,
        "extracted": extracted,
        "server": "arxiv",
        "year": 2026,
        "week": 22,
    }


class RenderBlankLineTests(unittest.TestCase):
    def test_no_double_blank_after_empty_extracted(self):
        # A paper with no summary/methods/findings followed by another record must
        # not leave two blank lines between their headings (markdownlint MD012). #274.
        recs = [
            _record({}, title="Empty", doi="2601.00001"),
            _record({"summary": "x"}, title="Full", doi="2601.00002"),
        ]
        out = build_rxiv_index.render(recs, 1)
        self.assertNotIn("\n\n\n", out)

    def test_content_preserved(self):
        # The fix must not drop real content or headings.
        out = build_rxiv_index.render([_record({"summary": "abc"})], 1)
        self.assertIn("- summary: abc", out)
        self.assertIn("### [Some Paper](https://arxiv.org/abs/2601.00001)", out)


if __name__ == "__main__":
    unittest.main()
