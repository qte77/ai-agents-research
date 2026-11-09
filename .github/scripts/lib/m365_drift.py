"""Pure drift-detection logic for m365-drift-monitor.py.

Checks whether the Microsoft Learn pages cited by the Microsoft 365 Copilot doc
still carry their last-known `ms.date` meta value and still contain their
stored verbatim quote. No HTTP / os.environ / sys.exit here (the entry script
does the fetching), so the extraction/diff/report logic is unit-testable.
"""
from __future__ import annotations

import html as html_lib
import re
from datetime import date

from .monitor_utils import strip_html_noise

_META_TAG_RE = re.compile(r"<meta\b[^>]*>", re.IGNORECASE)
_NAME_MS_DATE_RE = re.compile(r"""name\s*=\s*["']ms\.date["']""", re.IGNORECASE)
_CONTENT_RE = re.compile(r"""content\s*=\s*["']([^"']*)["']""", re.IGNORECASE)

# Typographic punctuation a rendered page may use in place of ASCII
# equivalents (curly quotes, en/em dashes) — folded before matching so a
# verbatim ASCII quote still matches rendered page text.
_TYPOGRAPHIC_EQUIVALENTS = {
    "’": "'", "‘": "'",
    "“": '"', "”": '"',
    "–": "-", "—": "-",
}


def extract_ms_date(raw_html: str) -> str | None:
    """Extract the `ms.date` meta tag's `content` value (None if absent).

    Attribute-order-agnostic: matches `<meta name="ms.date" content="...">`
    and `<meta content="..." name="ms.date">` alike, single- or double-quoted.
    """
    for tag in _META_TAG_RE.finditer(raw_html):
        attrs = tag.group(0)
        if _NAME_MS_DATE_RE.search(attrs):
            match = _CONTENT_RE.search(attrs)
            if match:
                return match.group(1)
    return None


def _normalize_text(text: str) -> str:
    """Collapse whitespace and fold typographic punctuation to ASCII equivalents."""
    for typo, ascii_eq in _TYPOGRAPHIC_EQUIVALENTS.items():
        text = text.replace(typo, ascii_eq)
    return re.sub(r"\s+", " ", text).strip()


def _visible_text(raw_html: str) -> str:
    """Strip tags/scripts/styles from raw HTML and decode entities into plain text."""
    no_noise = strip_html_noise(raw_html)
    text = re.sub(r"<[^>]+>", " ", no_noise)
    return html_lib.unescape(text)


def quote_present(raw_html: str, quote: str) -> bool:
    """Whitespace-normalised, case-sensitive check that `quote` is still in the page text."""
    page_text = _normalize_text(_visible_text(raw_html))
    needle = _normalize_text(quote)
    return needle in page_text


def _due_passed(due: str | None, today: date | None) -> bool:
    """True when an entry's ``due`` date (YYYY-MM-DD) is today or earlier."""
    if not due or today is None:
        return False
    return date.fromisoformat(due) <= today


def diff_entries(
    prev_state: dict[str, dict], observations: list[dict], today: date | None = None
) -> list[dict]:
    """Compare freshly fetched observations against the previously stored state.

    ``prev_state`` maps url -> {"quote": str, "ms_date": str | None, "due"?: "YYYY-MM-DD"}.
    Each observation is {"url", "quote", "ms_date", "quote_found", "error"}
    (``ms_date``/``quote_found`` are None and ``error`` is set on fetch failure).
    ``today`` enables the ``due`` check; without it no entry is ever due.

    Returns one record per URL that changed, could not be checked, or whose ``due``
    date has passed — other entries are omitted. Each record:
        {"url", "old_date", "new_date", "quote_found", "fetch_failed", "error",
         "due", "due_passed"}
    """
    diffs: list[dict] = []
    for obs in observations:
        url = obs["url"]
        prev = prev_state.get(url, {})
        old_date = prev.get("ms_date")
        due = prev.get("due")
        # Reason: a page can keep its ms.date and quote after a dated event passes
        # (the 2026-10-31 retirement went unflagged), so the date itself must alert (#705).
        due_passed = _due_passed(due, today)

        if obs.get("error"):
            diffs.append({
                "url": url,
                "old_date": old_date,
                "new_date": None,
                "quote_found": None,
                "fetch_failed": True,
                "error": obs["error"],
                "due": due,
                "due_passed": due_passed,
            })
            continue

        new_date = obs.get("ms_date")
        quote_found = obs.get("quote_found")
        if new_date != old_date or not quote_found or due_passed:
            diffs.append({
                "url": url,
                "old_date": old_date,
                "new_date": new_date,
                "quote_found": quote_found,
                "fetch_failed": False,
                "error": None,
                "due": due,
                "due_passed": due_passed,
            })
    return diffs


def build_new_state(prev_state: dict[str, dict], observations: list[dict]) -> dict[str, dict]:
    """Next state: each entry's fields carried over, ``ms_date`` updated from a successful fetch.

    Extra fields such as ``due`` are kept; on fetch failure the previous ``ms_date`` stays.
    """
    new_state: dict[str, dict] = {}
    for obs in observations:
        entry = dict(prev_state.get(obs["url"], {}))
        entry["quote"] = obs["quote"]
        if obs["error"] is None:
            entry["ms_date"] = obs["ms_date"]
        else:
            entry.setdefault("ms_date", None)
        new_state[obs["url"]] = entry
    return new_state


def render_report(diffs: list[dict]) -> str:
    """Render a markdown drift report listing changed/unverifiable URLs.

    Returns "" when ``diffs`` is empty (nothing changed).
    """
    if not diffs:
        return ""

    lines = ["## M365 doc drift report", ""]
    for d in diffs:
        lines.append(f"### {d['url']}")
        if d["fetch_failed"]:
            lines.append(f"- Could not check: {d['error']}")
        else:
            old = d["old_date"] or "(none)"
            new = d["new_date"] or "(none)"
            lines.append(f"- `ms.date`: {old} → {new}")
            lines.append(f"- Quote still present: {'yes' if d['quote_found'] else 'no'}")
        if d.get("due_passed"):
            lines.append(
                f"- Due date {d['due']} has passed: check whether the dated event happened, "
                "update the doc, then move or remove `due` in the state file"
            )
        lines.append("")

    lines.append("_Generated by `.github/scripts/m365-drift-monitor.py`_")
    return "\n".join(lines).rstrip("\n")
