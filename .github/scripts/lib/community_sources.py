"""Pure content extractors for community-monitor.py (markdown + HTML).

No HTTP / os.environ / sys.exit here (the entry script does the fetching), so the
parsing is unit-testable.
"""
from __future__ import annotations

import re

from .monitor_utils import strip_html_noise

# Hoisted out of the per-line loop (was rebuilt every iteration).
_FEATURE_KEYWORDS = frozenset({
    "added", "new", "feature", "support", "improved", "fix",
    "hook", "plugin", "skill", "agent", "team", "command",
    "tool", "mode", "config", "memory", "context", "remote",
})
_HEADING_RE = re.compile(r"^(#{1,4})\s+(.*)")
_LINK_ITEM_RE = re.compile(r"^\s*[-*]\s+\[([^\]]+)\]\(([^)]+)\)\s*[-–—:]?\s*(.*)")
_BOLD_ITEM_RE = re.compile(r"^\s*[-*]\s+\*\*([^*]+)\*\*\s*[-–—:]?\s*(.*)")
_VERSION_RE = re.compile(r"^v?(\d+\.\d+\.\d+)")


def _markdown_item(line: str, heading: str) -> dict[str, str] | None:
    """Parse one markdown list line into an entry (link item or bold item), else None."""
    link = _LINK_ITEM_RE.match(line)
    if link:
        return {"heading": heading, "name": link.group(1).strip(),
                "url": link.group(2).strip(), "description": link.group(3).strip()}
    bold = _BOLD_ITEM_RE.match(line)
    if bold:
        return {"heading": heading, "name": bold.group(1).strip(),
                "url": "", "description": bold.group(2).strip()}
    return None


def extract_markdown_entries(text: str) -> list[dict[str, str]]:
    """Extract list entries (link + bold items) grouped under their headings."""
    entries: list[dict[str, str]] = []
    current_heading = ""
    for line in text.splitlines():
        h = _HEADING_RE.match(line)
        if h:
            current_heading = h.group(2).strip()
            continue
        entry = _markdown_item(line, current_heading)
        if entry:
            entries.append(entry)
    return entries


def extract_html_entries(text: str) -> list[dict[str, str]]:
    """Extract feature-like lines from HTML (claudelog), grouped under version headings."""
    clean = strip_html_noise(text)
    clean = re.sub(r"<[^>]+>", "\n", clean)
    clean = re.sub(r"\n{3,}", "\n\n", clean)

    entries: list[dict[str, str]] = []
    current_heading = ""
    for raw in clean.splitlines():
        line = raw.strip()
        if not line or len(line) < 10:
            continue
        if _VERSION_RE.match(line):
            current_heading = line
            continue
        if len(line) > 20 and set(line.lower().split()) & _FEATURE_KEYWORDS:
            entries.append({"heading": current_heading, "name": line[:80],
                            "url": "", "description": line})
    return entries
