"""Shared utilities for CC monitor scripts.

Provides keyword extraction, doc scanning, coverage checking,
state management, and HTTP fetching used by changelog-compare,
community-monitor, and native-sources-monitor.
"""

import hashlib
import json
import re
import sys
import urllib.request
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import NoReturn

# Noise words that match too broadly across docs.
# Changelog verbs (added, fixed, improved, removed, renamed) are included so
# "Bug fixes and reliability improvements" lines don't generate spurious matches.
DEFAULT_NOISE: set[str] = {
    "claude", "code", "with", "that", "this", "from", "have",
    "been", "will", "your", "more", "tool", "tools", "https",
    "github", "added", "fixed", "improved", "removed", "renamed",
    "support", "feature",
}


def fatal(message: str, code: int = 2) -> NoReturn:
    """Print an error to stderr and exit with ``code`` (default 2)."""
    print(message, file=sys.stderr)
    sys.exit(code)


def strip_html_noise(html: str) -> str:
    """Remove <script>/<style> blocks from HTML.

    Tolerant of case and whitespace/junk in tags (e.g. ``</script >``) so the
    regex can't be trivially defeated (CodeQL py/bad-tag-filter).
    """
    clean = re.sub(r"<script[^>]*>.*?</script[^>]*>", "", html, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r"<style[^>]*>.*?</style[^>]*>", "", clean, flags=re.DOTALL | re.IGNORECASE)
    return clean


def parse_iso(s: str) -> datetime | None:
    """Parse an ISO-8601 timestamp (tolerating a trailing ``Z``); None on failure."""
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def load_jsonl(path: Path) -> list[dict]:
    """Load a JSONL file into a list of dicts, skipping blank lines.

    Returns ``[]`` when the file does not exist.
    """
    if not path.exists():
        return []
    records: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    return records


def extract_keywords(text: str, min_len: int = 4) -> set[str]:
    """Extract lowercase alphanumeric tokens of at least ``min_len`` chars."""
    return {w.lower() for w in re.findall(r"[A-Za-z0-9_/-]{%d,}" % min_len, text)}


def build_doc_keywords(docs_dir: Path) -> set[str]:
    """Build a keyword set from all markdown files under ``docs_dir``."""
    keywords: set[str] = set()
    for md_file in sorted(docs_dir.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8", errors="replace")
        keywords.update(extract_keywords(text))
    return keywords


def is_covered(
    entry: dict[str, str],
    doc_keywords: set[str],
    threshold: float = 0.4,
    noise: set[str] | None = None,
) -> bool:
    """Check if an entry's key terms appear in existing docs.

    Returns True when overlap exceeds ``threshold`` fraction of entry keywords
    (after removing noise words).
    """
    if noise is None:
        noise = DEFAULT_NOISE

    entry_text = f"{entry.get('name', '')} {entry.get('description', '')}"
    entry_words = extract_keywords(entry_text) - noise

    if not entry_words:
        return True  # No meaningful keywords to match

    overlap = entry_words & doc_keywords
    return len(overlap) / len(entry_words) > threshold


def entry_fingerprint(entry: dict[str, str]) -> str:
    """Generate a stable 16-char hex fingerprint for an entry."""
    key = f"{entry.get('name', '')}|{entry.get('url', '')}".lower()
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def load_state(state_file: Path) -> dict[str, list[str]]:
    """Load previously seen entry fingerprints per source."""
    if state_file.exists():
        text = state_file.read_text(encoding="utf-8")
        if text.strip():
            return json.loads(text)
    return {}


def save_state(state_file: Path, state: dict[str, list[str]]) -> None:
    """Save seen entry fingerprints."""
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def build_report(
    source_results: list[dict],
    report_title: str,
    script_name: str,
) -> tuple[str, bool]:
    """Build a markdown report of uncovered content.

    Args:
        source_results: List of per-source result dicts.
        report_title: H2 heading for the report.
        script_name: Script filename shown in the footer.

    Returns:
        (report_text, has_new_content).
    """
    lines: list[str] = [
        f"## {report_title}",
        "",
        f"Sources checked: **{len(source_results)}**",
        "",
    ]

    total_new = 0
    for result in source_results:
        total_new += len(result["new_entries"])
        lines += _render_source_section(result)

    lines += [
        "---",
        f"Total new uncovered entries: **{total_new}**",
        "",
        f"_Generated by `.github/scripts/{script_name}`_",
    ]

    return "\n".join(lines).rstrip("\n"), total_new > 0


def _render_source_section(result: dict) -> list[str]:
    """Render one source's markdown section (header, counts, optional table)."""
    new_entries = result["new_entries"]
    lines = [
        f"### {result['name']}",
        "",
        f"- Source: {result['description']}",
        f"- Entries fetched: {result['total']}",
        f"- New uncovered: {len(new_entries)}",
        "",
    ]
    if new_entries:
        lines.append("| Entry | Section | Description |")
        lines.append("|-------|---------|-------------|")
        for entry in new_entries[:30]:
            name_col = _clean_table_cell(entry.get("name", ""), 60)
            heading = _clean_table_cell(entry.get("heading", ""), 40)
            desc = _clean_table_cell(entry.get("description", ""), 80)
            lines.append(f"| {name_col} | {heading} | {desc} |")
        lines.append("")
        if len(new_entries) > 30:
            lines.append(f"_... and {len(new_entries) - 30} more entries._")
            lines.append("")
    return lines


def _clean_table_cell(text: str, max_len: int) -> str:
    """Sanitize a string for use inside a markdown table cell.

    Strips URLs (to avoid MD034 bare-URL noise when truncation breaks links),
    flattens newlines and pipes, collapses whitespace, and clips length.
    """
    text = re.sub(r"https?://\S+", "", text)
    text = text.replace("\n", " ").replace("|", "\\|")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_len]


def _process_source(
    source: dict[str, str],
    fetch_fn: Callable[[dict[str, str]], list[dict[str, str]]],
    seen: set[str],
    doc_keywords: set[str],
) -> tuple[dict, list[str]]:
    """Fetch + filter one source.

    Returns ``(result_dict, fingerprints_of_all_fetched)``. Pure except for the
    injected ``fetch_fn`` (whose exceptions propagate to the caller).
    """
    entries = fetch_fn(source)
    new_entries = [
        e for e in entries
        if entry_fingerprint(e) not in seen and not is_covered(e, doc_keywords)
    ]
    result = {
        "name": source["name"],
        "description": source["description"],
        "total": len(entries),
        "new_entries": new_entries,
    }
    return result, [entry_fingerprint(e) for e in entries]


def run_monitor(
    sources: list[dict[str, str]],
    fetch_fn: Callable[[dict[str, str]], list[dict[str, str]]],
    docs_dir: Path,
    state_file: Path,
    report_title: str,
    script_name: str,
) -> None:
    """Shared monitor loop: fetch sources, filter, report, exit.

    Args:
        sources: Source definitions to poll.
        fetch_fn: Callable that fetches and extracts entries for a source.
        docs_dir: Directory of existing docs for coverage checking.
        state_file: Path to JSON state file.
        report_title: H2 heading for the report.
        script_name: Script filename for the report footer.
    """
    doc_keywords = build_doc_keywords(docs_dir)
    print(f"Doc keywords indexed: {len(doc_keywords)}", file=sys.stderr)

    state = load_state(state_file)
    source_results: list[dict] = []

    for source in sources:
        name = source["name"]
        print(f"Fetching {name}...", file=sys.stderr)

        try:
            result, fingerprints = _process_source(
                source, fetch_fn, set(state.get(name, [])), doc_keywords
            )
        except Exception as e:
            print(f"WARNING: Failed to fetch {name}: {e}", file=sys.stderr)
            source_results.append({
                "name": name,
                "description": source["description"],
                "total": 0,
                "new_entries": [],
            })
            continue

        print(f"  Extracted {result['total']} entries", file=sys.stderr)
        print(f"  New uncovered: {len(result['new_entries'])}", file=sys.stderr)
        state[name] = fingerprints
        source_results.append(result)

    save_state(state_file, state)
    print(f"State saved to {state_file}", file=sys.stderr)

    report, has_new = build_report(source_results, report_title, script_name)
    print(report)

    sys.exit(1 if has_new else 0)


def fetch_text(
    url: str,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
) -> str:
    """Fetch text content from a URL.

    Args:
        url: Target URL.
        headers: Optional HTTP headers (merged with default User-Agent).
        timeout: Request timeout in seconds.

    Returns:
        Response body as string.
    """
    default_headers = {"User-Agent": "cc-monitor/1.0"}
    if headers:
        default_headers.update(headers)
    req = urllib.request.Request(url, headers=default_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")
