"""Pure helpers for building the branded GitHub Pages site.

Stdlib only, no side effects on import — so it is unit-testable. The
`scripts/*.py` entry points (build-site-info.py, fetch-web-fonts.py) are
thin IO wrappers that import from here; all testable logic lives in this module.

Brand source of truth: qte77/qte77/brand/DESIGN.md (EyeRest — zero-blue, warm
umber/parchment). Tokens are transcribed by value here, same as the sibling
repos analyze-stock-kpi/ui/style.css and paperverse/ui/src/theme.css.
"""
from __future__ import annotations

import tomllib

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


# -- Build metadata ------------------------------------------------------------
# The Pages deploy writes build.json (scripts/build-site-info.py); ui/build-info.js
# shows version, last-modified date and commit link on each page.


def read_version(pyproject_text: str) -> str | None:
    """Release version from ``[tool.bumpversion] current_version``, or ``None``."""
    data = tomllib.loads(pyproject_text)
    return data.get("tool", {}).get("bumpversion", {}).get("current_version")


def _commit(sha: str | None, date: str | None, repo_url: str) -> dict | None:
    if not sha:
        return None
    return {"commit": sha, "short": sha[:7], "date": (date or "")[:10],
            "url": f"{repo_url}/commit/{sha}"}


def site_info(version: str | None, commit: str, commit_date: str, repo_url: str) -> dict:
    """Metadata for build.json: release version and the deploy commit."""
    return {"version": version, "site": _commit(commit, commit_date, repo_url)}
