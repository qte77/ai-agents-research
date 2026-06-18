"""Pure helpers for building the branded GitHub Pages site.

Stdlib only, no side effects on import — so it is unit-testable. The
`scripts/*.py` entry points (graphify-publish-pages.py, fetch-web-fonts.py) are
thin IO wrappers that import from here; all testable logic lives in this module.

Brand source of truth: qte77/qte77/brand/DESIGN.md (EyeRest — zero-blue, warm
umber/parchment). Tokens are transcribed by value here, same as the sibling
repos analyze-stock-kpi/ui/style.css and paperverse/ui/src/theme.css.
"""
from __future__ import annotations

import json
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


# -- Graph node pruning -------------------------------------------------------
# The published graph maps the docs/research corpus, not build tooling. Drop
# nodes whose source_file is under these dirs (and any edge/hyperedge that would
# then dangle). Keeps .github/workflows + .github/actions (architecture).
_EXCLUDED_DIRS = ("scripts/", "tests/", "ui/", "src/", ".github/scripts/")
_GRAPH_ARRAYS = ("RAW_NODES", "RAW_EDGES", "hyperedges")


def _excluded(source_file) -> bool:
    return str(source_file or "").startswith(_EXCLUDED_DIRS)


def filter_graph_data(html: str) -> str:
    """Prune tooling/code nodes (and their now-dangling edges) from the inline
    graph data, so the published graph maps the research corpus.

    All-or-nothing: if the inline arrays can't be located and parsed, return the
    HTML unchanged rather than risk emitting edges that reference missing nodes.
    Idempotent — re-running on already-pruned output is a no-op.
    """
    found = {}
    for var in _GRAPH_ARRAYS:
        m = re.search(rf"{var} = (\[.*?\]);", html, re.DOTALL)
        if not m:
            return html
        try:
            found[var] = (m.group(0), json.loads(m.group(1)))
        except ValueError:
            return html

    nodes = [n for n in found["RAW_NODES"][1] if not _excluded(n.get("source_file"))]
    kept = {n["id"] for n in nodes}
    edges = [
        e for e in found["RAW_EDGES"][1]
        if e.get("from") in kept and e.get("to") in kept
    ]
    hyper = []
    for h in found["hyperedges"][1]:
        if _excluded(h.get("source_file")):
            continue
        members = [nid for nid in h.get("nodes", []) if nid in kept]
        if len(members) >= 2:  # a hyperedge needs at least two members to mean anything
            hyper.append({**h, "nodes": members})

    out = html
    for var, data in (("RAW_NODES", nodes), ("RAW_EDGES", edges), ("hyperedges", hyper)):
        out = out.replace(
            found[var][0], f"{var} = {json.dumps(data, ensure_ascii=False)};", 1
        )
    return out
