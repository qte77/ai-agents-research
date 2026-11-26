"""The EyeRest brand-kit CSS is an unedited copy and owns every colour token (plan 0017 N59)."""
import hashlib
import re
import unittest
from pathlib import Path

UI = Path(__file__).resolve().parents[1] / "ui"

# Source: qte77/qte77 brand/ui-kit/eyerest.css at commit
# 9cbdfa6453f2b8aa323c543afccaf0f1d9bd5945 (kit 0.5.0). Update both together.
EYEREST_SHA256 = "157e7cacdf718b9a244c37873850ccfc98b38a7819f6991794abf534dc51a744"

KIT_COLOUR_PROPS = ("bg", "surface", "border", "text", "text-muted", "primary", "primary-on", "link")


class BrandKitTests(unittest.TestCase):
    def test_kit_copy_is_unedited(self):
        raw = (UI / "eyerest.css").read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), EYEREST_SHA256)

    def test_kit_version_header(self):
        text = (UI / "eyerest.css").read_text(encoding="utf-8")
        self.assertRegex(text, r"kit version: 0\.5\.0")

    def test_style_css_defines_no_colour_tokens(self):
        css = (UI / "style.css").read_text(encoding="utf-8")
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
        defined = {d.lower() for d in re.findall(r"(--[a-z0-9-]+)\s*:", css, flags=re.I)}
        banned = {f"--{p}" for p in KIT_COLOUR_PROPS}
        self.assertEqual(defined & banned, set())
        self.assertEqual({d for d in defined if d.startswith(("--data-", "--cat-"))}, set())

    def test_pages_link_kit_before_style(self):
        for page in ("doc-graph.html", "index.html"):
            html = (UI / page).read_text(encoding="utf-8")
            kit = html.find('href="eyerest.css"')
            style = html.find('href="style.css"')
            self.assertGreaterEqual(kit, 0, page)
            self.assertGreater(style, kit, page)


if __name__ == "__main__":
    unittest.main()
