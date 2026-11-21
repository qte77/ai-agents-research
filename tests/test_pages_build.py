"""Unit tests for the pure site-build module (scripts/pages_build.py).

Only the module is tested — the scripts/*.py entry points are thin IO wrappers
around these functions and are not unit-tested. Stdlib `unittest`, no deps.

Run: python3 -m unittest discover -s tests
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import pages_build  # noqa: E402

PYPROJECT = """[project]
name = "x"

[tool.bumpversion]
current_version = "0.12.0"
parse = "(?P<major>\\\\d+)"
"""


class ReadVersionTests(unittest.TestCase):
    def test_reads_bumpversion_current_version(self):
        self.assertEqual(pages_build.read_version(PYPROJECT), "0.12.0")

    def test_none_when_missing(self):
        self.assertIsNone(pages_build.read_version('[project]\nname = "x"\n'))


class SiteInfoTests(unittest.TestCase):
    def setUp(self):
        self.info = pages_build.site_info(
            version="0.12.0",
            commit="a" * 40, commit_date="2026-09-30T14:18:14+00:00",
            repo_url="https://github.com/qte77/ai-agents-research",
        )

    def test_site_fields(self):
        self.assertEqual(self.info["version"], "0.12.0")
        self.assertEqual(self.info["site"], {
            "commit": "a" * 40, "short": "aaaaaaa", "date": "2026-09-30",
            "url": "https://github.com/qte77/ai-agents-research/commit/" + "a" * 40,
        })

    def test_no_graph_artifact_key(self):
        # The separate concept-graph page is gone (plan 0015 G1); build.json describes the deploy only.
        self.assertEqual(set(self.info), {"version", "site"})


class IsWoff2Tests(unittest.TestCase):
    def test_accepts_woff2_signature(self):
        self.assertTrue(pages_build.is_woff2(b"wOF2\x00\x01\x00\x00rest"))

    def test_rejects_non_woff2(self):
        self.assertFalse(pages_build.is_woff2(b"<!DOCTYPE html>"))
        self.assertFalse(pages_build.is_woff2(b"wOFF"))  # woff1, not woff2
        self.assertFalse(pages_build.is_woff2(b""))


if __name__ == "__main__":
    unittest.main()
