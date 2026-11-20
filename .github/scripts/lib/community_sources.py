"""Pure content extractors for community-monitor.py (markdown).

No HTTP / os.environ / sys.exit here (the entry script does the fetching), so the
parsing is unit-testable.
"""
from __future__ import annotations

import re

_HEADING_RE = re.compile(r"^(#{1,4})\s+(.*)")
_LINK_ITEM_RE = re.compile(r"^\s*[-*]\s+\[([^\]]+)\]\(([^)]+)\)\s*[-–—:]?\s*(.*)")
_BOLD_ITEM_RE = re.compile(r"^\s*[-*]\s+\*\*([^*]+)\*\*\s*[-–—:]?\s*(.*)")


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
