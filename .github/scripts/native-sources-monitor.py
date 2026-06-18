#!/usr/bin/env python3
"""Monitor native/Anthropic sources for Claude Code updates.

Polls Anthropic Blog, GitHub Issues (enhancement), and GitHub Discussions
(feature-request) for new entries not yet covered by existing native docs.
Pure HTML/JSON parsing lives in lib/native_sources.py.

Usage:
    python native-sources-monitor.py --native-docs-dir PATH [--state-file PATH]

Exit codes:
    0 = no new uncovered content
    1 = new content found (workflow should open a PR)
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor_utils import fetch_text, run_monitor
from lib.native_sources import (
    discussion_page,
    extract_blog_entries,
    extract_discussions,
    extract_issues,
    feature_category_id,
)

CC_REPO_OWNER = "anthropics"
CC_REPO_NAME = "claude-code"
MAX_PAGES = 3

SOURCES: list[dict[str, str]] = [
    {
        "name": "anthropic-blog",
        "url": "https://www.anthropic.com/news",
        "type": "html",
        "auth": "none",
        "description": "Anthropic Blog — announcements and product updates",
    },
    {
        "name": "cc-issues-enhancement",
        "url": (
            f"https://api.github.com/repos/{CC_REPO_OWNER}/{CC_REPO_NAME}"
            "/issues?labels=enhancement&state=open&per_page=100"
        ),
        "type": "github_rest",
        "auth": "github_token",
        "description": "CC GitHub Issues labeled 'enhancement'",
    },
    {
        "name": "cc-discussions-feature-request",
        "type": "github_graphql",
        "auth": "github_token",
        "description": "CC GitHub Discussions in feature-request category",
    },
]


def github_headers(token: str) -> dict[str, str]:
    """Build GitHub API request headers."""
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def fetch_github_rest_pages(url: str, token: str) -> list[list[dict]]:
    """Fetch paginated GitHub REST API results (up to MAX_PAGES)."""
    pages: list[list[dict]] = []
    current_url: str | None = url
    for _ in range(MAX_PAGES):
        if current_url is None:
            break
        req = urllib.request.Request(current_url, headers=github_headers(token))
        with urllib.request.urlopen(req, timeout=30) as resp:
            pages.append(json.loads(resp.read().decode("utf-8")))
            next_match = re.search(r'<([^>]+)>;\s*rel="next"', resp.headers.get("Link", ""))
            current_url = next_match.group(1) if next_match else None
    return pages


def graphql_request(query: str, variables: dict, token: str) -> dict | None:
    """Execute a GitHub GraphQL request (None on network failure)."""
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    headers = github_headers(token)
    headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        "https://api.github.com/graphql", data=payload, headers=headers, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"WARNING: GraphQL request failed: {e}", file=sys.stderr)
        return None


def resolve_discussion_category_id(token: str) -> str | None:
    """Resolve the 'Feature Requests' discussion category ID via GraphQL."""
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        discussionCategories(first: 25) {
          nodes { id name }
        }
      }
    }
    """
    data = graphql_request(query, {"owner": CC_REPO_OWNER, "name": CC_REPO_NAME}, token)
    return feature_category_id(data)


def fetch_discussions_graphql(token: str, category_id: str | None) -> list[dict]:
    """Fetch discussions via GraphQL with cursor pagination (up to MAX_PAGES)."""
    all_nodes: list[dict] = []
    cursor: str | None = None
    query = """
    query($owner: String!, $name: String!, $categoryId: ID, $after: String) {
      repository(owner: $owner, name: $name) {
        discussions(first: 100, categoryId: $categoryId, after: $after) {
          pageInfo { hasNextPage endCursor }
          nodes { title url body createdAt category { name } }
        }
      }
    }
    """
    for _ in range(MAX_PAGES):
        variables: dict = {"owner": CC_REPO_OWNER, "name": CC_REPO_NAME, "after": cursor}
        if category_id:
            variables["categoryId"] = category_id
        nodes, page_info = discussion_page(graphql_request(query, variables, token))
        all_nodes.extend(nodes)
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")
    return all_nodes


def fetch_and_extract(source: dict[str, str]) -> list[dict[str, str]]:
    """Fetch a source and extract entries based on its type and auth.

    Skips github-token sources (returning []) when no token is set.
    """
    source_type = source["type"]
    token = os.environ.get("GITHUB_TOKEN", "")
    if source["auth"] == "github_token" and not token:
        print(f"WARNING: Skipping {source['name']} — GITHUB_TOKEN not set", file=sys.stderr)
        return []

    if source_type == "html":
        return extract_blog_entries(fetch_text(source["url"]))
    if source_type == "github_rest":
        return extract_issues(fetch_github_rest_pages(source["url"], token))
    if source_type == "github_graphql":
        category_id = resolve_discussion_category_id(token)
        return extract_discussions(fetch_discussions_graphql(token, category_id))

    print(f"WARNING: Unknown source type '{source_type}'", file=sys.stderr)
    return []


def main() -> None:
    """Entry point for the native sources monitor script."""
    parser = argparse.ArgumentParser(
        description="Monitor native/Anthropic sources for CC updates."
    )
    parser.add_argument("--native-docs-dir", required=True, type=Path,
                        help="Path to docs/cc-native/ directory")
    parser.add_argument("--state-file", type=Path,
                        default=Path(".github/state/native-monitor-state.json"),
                        help="Path to state file tracking previously seen entries")
    args = parser.parse_args()

    if not args.native_docs_dir.exists():
        sys.exit(f"ERROR: Native docs dir does not exist: {args.native_docs_dir}")

    run_monitor(
        sources=SOURCES,
        fetch_fn=fetch_and_extract,
        docs_dir=args.native_docs_dir,
        state_file=args.state_file,
        report_title="Native Sources Monitor Report",
        script_name="native-sources-monitor.py",
    )


if __name__ == "__main__":
    main()
