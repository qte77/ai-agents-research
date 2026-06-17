"""Unit tests for the pure site-build module (src/pages_build.py).

Only the module is tested — the scripts/*.py entry points are thin IO wrappers
around these functions and are not unit-tested. Stdlib `unittest`, no deps.

Run: python3 -m unittest discover -s tests
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pages_build  # noqa: E402

# A minimal stand-in for the graphify-generated graph.html head, carrying every
# hardcoded color the restyle must neutralize (dark bg, navy sidebar, borders,
# the steel-blue accent / blue node category, and the body text gray).
SAMPLE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>graphify - graphify-out/graph.html</title>
<script src="https://unpkg.com/vis-network@9.1.6/standalone/umd/vis-network.min.js"
        integrity="sha384-deadbeef"
        crossorigin="anonymous"></script>
<style>
  body { background: #0f0f1a; color: #e0e0e0; }
  #sidebar { background: #1a1a2e; border-left: 1px solid #2a2a4e; }
  #search { border: 1px solid #3a3a5e; }
  #search:focus { border-color: #4E79A7; }
  .legend-cb:checked { background: #4e79a7; border-color: #4E79A7; }
</style>
</head>
<body><div id="sidebar"></div></body>
</html>
"""


class RestyleGraphTests(unittest.TestCase):
    def setUp(self):
        self.out = pages_build.restyle_graph(SAMPLE)

    def test_blue_accent_removed(self):
        # Zero-blue is the brand's defining constraint — no steel blue survives,
        # in either letter case.
        self.assertNotIn("#4E79A7", self.out)
        self.assertNotIn("#4e79a7", self.out)

    def test_graphify_default_dark_bg_replaced_with_eyerest(self):
        self.assertNotIn("#0f0f1a", self.out)
        self.assertIn("#1c1a14", self.out)  # EyeRest dark-bg

    def test_amber_primary_present(self):
        self.assertIn("#c8a858", self.out)  # EyeRest dark-primary

    def test_favicon_injected(self):
        self.assertIn('rel="icon"', self.out)
        self.assertIn("favicon.svg", self.out)

    def test_brand_fonts_injected(self):
        self.assertIn("@font-face", self.out)
        self.assertIn("Inter", self.out)
        self.assertIn("font-family", self.out)

    def test_title_replaced(self):
        self.assertIn(
            "<title>ai-agents-research — knowledge graph</title>", self.out
        )
        self.assertNotIn("graphify - graphify-out", self.out)

    def test_vis_network_vendored(self):
        # The graph must render offline / without the unpkg CDN.
        self.assertNotIn("unpkg.com", self.out)
        self.assertIn('src="vendor/vis-network.min.js"', self.out)

    def test_idempotent(self):
        # Republishing a refreshed graph must not double-inject head content.
        self.assertEqual(pages_build.restyle_graph(self.out), self.out)


class IsWoff2Tests(unittest.TestCase):
    def test_accepts_woff2_signature(self):
        self.assertTrue(pages_build.is_woff2(b"wOF2\x00\x01\x00\x00rest"))

    def test_rejects_non_woff2(self):
        self.assertFalse(pages_build.is_woff2(b"<!DOCTYPE html>"))
        self.assertFalse(pages_build.is_woff2(b"wOFF"))  # woff1, not woff2
        self.assertFalse(pages_build.is_woff2(b""))


if __name__ == "__main__":
    unittest.main()
