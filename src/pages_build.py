"""Pure helpers for building the branded GitHub Pages site.

Stdlib only, no side effects on import — so it is unit-testable. The
`scripts/*.py` entry points (graphify-publish-pages.py, fetch-web-fonts.py) are
thin IO wrappers that import from here; all testable logic lives in this module.

Brand source of truth: qte77/qte77/brand/DESIGN.md (EyeRest — zero-blue, warm
umber/parchment). Tokens are transcribed by value here, same as the sibling
repos analyze-stock-kpi/ui/style.css and paperverse/ui/src/theme.css.
"""
from __future__ import annotations

import re

# -- Fonts -------------------------------------------------------------------
# Self-hosted Inter + JetBrains Mono (latin woff2), fetched on demand into
# ui/assets/fonts/ by scripts/fetch-web-fonts.py. Pinned to the Fontsource major
# (not @latest) for reproducibility; jsDelivr resolves the range server-side.
# The woff2 magic-byte check (is_woff2) is the integrity guard at download time.
_FONT_CDN = "https://cdn.jsdelivr.net/npm"
FONT_FILES = {
    "Inter-Regular.woff2": f"{_FONT_CDN}/@fontsource/inter@5/files/inter-latin-400-normal.woff2",
    "Inter-Bold.woff2": f"{_FONT_CDN}/@fontsource/inter@5/files/inter-latin-700-normal.woff2",
    "JetBrainsMono-Regular.woff2": f"{_FONT_CDN}/@fontsource/jetbrains-mono@5/files/jetbrains-mono-latin-400-normal.woff2",
}


def is_woff2(data: bytes) -> bool:
    """True iff ``data`` begins with the woff2 signature (``wOF2``).

    Cheap integrity guard so a redirect/error page (or a tampered CDN response)
    is never written out as a font file.
    """
    return data[:4] == b"wOF2"


# -- Graph restyle -----------------------------------------------------------
# The graphify export hardcodes a dark-navy theme with a steel-blue accent that
# is also the blue node category. Remap every occurrence to EyeRest dark tokens
# in one pass — this neutralizes both the chrome and the blue node color.
_HEX_REMAP = {
    "#0f0f1a": "#1c1a14",  # page bg            -> dark-bg
    "#1a1a2e": "#242018",  # sidebar surface    -> dark-surface
    "#2a2a4e": "#383428",  # border             -> dark-border
    "#3a3a5e": "#383428",  # border (lighter)   -> dark-border
    "#4E79A7": "#c8a858",  # steel-blue accent  -> dark-primary (amber)
    "#4e79a7": "#c8a858",  # same, lowercase
    "#e0e0e0": "#d8d0b8",  # body text          -> dark-text
}

_GRAPH_TITLE = "ai-agents-research — knowledge graph"

# Repoint the graphify export's vis-network <script> from the unpkg CDN to the
# vendored copy (ui/vendor/vis-network.min.js), so the published graph renders
# offline / without a CDN round-trip and isn't gated on an SRI match. The opening
# tag spans several lines (src/integrity/crossorigin) but contains no '>' until
# it closes, so [^>]* spans the newlines.
_VIS_CDN_RE = re.compile(
    r'<script\s+src="https://unpkg\.com/vis-network[^>]*>\s*</script>',
    re.IGNORECASE,
)
_VIS_LOCAL = '<script src="vendor/vis-network.min.js"></script>'

# Injected once before </head>: favicon + self-hosted brand fonts. font-family
# falls back to system-ui if the woff2 files are absent, so the graph still
# renders unbranded rather than broken.
_BRAND_HEAD = (
    '<link rel="icon" type="image/svg+xml" href="favicon.svg">\n'
    "<style>\n"
    "/* EyeRest brand fonts (qte77 DESIGN.md); woff2 fetched on demand, "
    "system-ui fallback if absent. */\n"
    "@font-face{font-family:'Inter';font-style:normal;font-weight:400;"
    "font-display:swap;src:url('assets/fonts/Inter-Regular.woff2') format('woff2');}\n"
    "@font-face{font-family:'Inter';font-style:normal;font-weight:600 700;"
    "font-display:swap;src:url('assets/fonts/Inter-Bold.woff2') format('woff2');}\n"
    "@font-face{font-family:'JetBrains Mono';font-style:normal;font-weight:400;"
    "font-display:swap;src:url('assets/fonts/JetBrainsMono-Regular.woff2') format('woff2');}\n"
    "body{font-family:'Inter',system-ui,-apple-system,'Segoe UI',sans-serif;}\n"
    "</style>\n"
)


def restyle_graph(html: str) -> str:
    """Return ``html`` rebranded to EyeRest: zero-blue palette, brand fonts,
    favicon, and project title. Idempotent — safe to re-run on already-styled
    output (each republish refreshes a regenerated graph).
    """
    for old, new in _HEX_REMAP.items():
        html = html.replace(old, new)
    html = _VIS_CDN_RE.sub(_VIS_LOCAL, html, count=1)
    html = re.sub(
        r"<title>.*?</title>",
        f"<title>{_GRAPH_TITLE}</title>",
        html,
        count=1,
        flags=re.DOTALL,
    )
    if _BRAND_HEAD not in html:
        html = html.replace("</head>", _BRAND_HEAD + "</head>", 1)
    return html
