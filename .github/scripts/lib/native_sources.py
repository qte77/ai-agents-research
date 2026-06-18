"""Pure extractors + GraphQL-response navigation for native-sources-monitor.py.

No HTTP / os.environ / sys.exit here (the entry script does the fetching), so the
HTML/JSON parsing is unit-testable.
"""
from __future__ import annotations

import re

from .monitor_utils import strip_html_noise


def extract_blog_entries(html: str) -> list[dict[str, str]]:
    """Extract Anthropic /news blog links from HTML (deduped by URL, single pass)."""
    clean = strip_html_noise(html)
    seen: set[str] = set()
    entries: list[dict[str, str]] = []
    for match in re.finditer(r'<a[^>]+href="(/news/[^"]+)"[^>]*>(.*?)</a>', clean, re.DOTALL):
        title = re.sub(r"<[^>]+>", "", match.group(2)).strip()
        url = f"https://www.anthropic.com{match.group(1)}"
        if not title or len(title) < 5 or url in seen:
            continue
        seen.add(url)
        entries.append({"name": title, "url": url, "description": title, "heading": "Anthropic Blog"})
    return entries


def extract_issues(json_pages: list[list[dict]]) -> list[dict[str, str]]:
    """Extract entries from GitHub REST Issues API response pages (skipping PRs)."""
    return [
        {
            "name": issue.get("title", ""),
            "url": issue.get("html_url", ""),
            "description": (issue.get("body") or "")[:200],
            "heading": "GitHub Issues (enhancement)",
        }
        for page in json_pages
        for issue in page
        if "pull_request" not in issue
    ]


def extract_discussions(nodes: list[dict]) -> list[dict[str, str]]:
    """Extract entries from GitHub GraphQL Discussions response nodes."""
    return [
        {
            "name": node.get("title", ""),
            "url": node.get("url", ""),
            "description": (node.get("body") or "")[:200],
            "heading": f"GitHub Discussions ({node.get('category', {}).get('name', 'feature-request')})",
        }
        for node in nodes
    ]


def feature_category_id(graphql_data: dict | None) -> str | None:
    """Pick the 'feature' discussion category id from a categories GraphQL response."""
    if graphql_data is None:
        return None
    categories = (
        graphql_data.get("data", {}).get("repository", {})
        .get("discussionCategories", {}).get("nodes", [])
    )
    for cat in categories:
        if "feature" in cat.get("name", "").lower():
            return cat["id"]
    return None


def discussion_page(graphql_data: dict | None) -> tuple[list[dict], dict]:
    """Extract ``(nodes, pageInfo)`` from a discussions GraphQL response."""
    if graphql_data is None:
        return [], {}
    discussions = (
        graphql_data.get("data", {}).get("repository", {}).get("discussions", {})
    )
    return discussions.get("nodes", []), discussions.get("pageInfo", {})
