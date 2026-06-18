#!/usr/bin/env python3
"""Monitor community sources for Claude Code features, tips, and tricks.

Fetches content from community sources (claudelog.com, awesome-claude-code,
awesome-claude-code-plugins, Reddit, X) and identifies entries not yet covered
by existing community docs. Pure parsing lives in lib/community_sources.py.

Usage:
    python community-monitor.py --community-docs-dir PATH [--state-file PATH]

Exit codes:
    0 = no new uncovered content
    1 = new content found (workflow should open a PR)
    2 = fatal error (bad input) — distinct from 1 so the workflow fails loudly
        instead of treating an error as "new content"
"""

import argparse
import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.community_sources import extract_html_entries, extract_markdown_entries
from lib.monitor_utils import fatal, fetch_text, run_monitor

SOURCES: list[dict[str, str]] = [
    {
        "name": "claudelog",
        "url": "https://claudelog.com/claude-code-changelog/",
        "type": "html",
        "description": "Third-party CC changelog aggregator with community annotations",
    },
    {
        "name": "awesome-claude-code",
        "url": "https://raw.githubusercontent.com/hesreallyhim/awesome-claude-code/main/README.md",
        "type": "markdown",
        "description": "Curated resource list (skills, workflows, tooling, hooks, commands)",
    },
    {
        "name": "awesome-claude-code-plugins",
        "url": "https://raw.githubusercontent.com/ccplugins/awesome-claude-code-plugins/main/README.md",
        "type": "markdown",
        "description": "Installable plugin registry with marketplace format",
    },
    {
        "name": "reddit-claudeai",
        "url": "https://oauth.reddit.com/r/ClaudeAI/search.json?q=claude+code&sort=new&limit=100&restrict_sr=1",
        "type": "reddit",
        "auth": "reddit",
        "description": "r/ClaudeAI posts mentioning Claude Code",
    },
    {
        "name": "x-claudecode",
        "url": "https://api.x.com/2/tweets/search/recent?query=%23ClaudeCode&max_results=100&tweet.fields=text,created_at",
        "type": "x",
        "auth": "x_bearer",
        "description": "X/Twitter posts with #ClaudeCode hashtag",
    },
]

_USER_AGENT = "cc-community-monitor/1.0"


def _require_env(source_name: str, *names: str) -> list[str] | None:
    """Return the env values for ``names``, or None (with a WARNING) if any is unset."""
    values = [os.environ.get(n, "") for n in names]
    if all(values):
        return values
    print(f"WARNING: Skipping {source_name} — {'/'.join(names)} not set", file=sys.stderr)
    return None


def _reddit_access_token(client_id: str, client_secret: str) -> str:
    """Obtain a Reddit OAuth2 client_credentials access token."""
    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    data = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
    req = urllib.request.Request(
        "https://www.reddit.com/api/v1/access_token", data=data,
        headers={"Authorization": f"Basic {credentials}", "User-Agent": _USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))["access_token"]


def _fetch_reddit_search(url: str, token: str) -> list[dict[str, str]]:
    """Fetch + extract Reddit search results given an access token."""
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {token}", "User-Agent": _USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return [
        {
            "name": post.get("title", ""),
            "url": f"https://reddit.com{post.get('permalink', '')}",
            "description": (post.get("selftext") or "")[:200],
            "heading": "r/ClaudeAI",
        }
        for child in data.get("data", {}).get("children", [])
        for post in [child.get("data", {})]
    ]


def fetch_reddit(url: str, client_id: str, client_secret: str) -> list[dict[str, str]]:
    """Fetch Reddit search results via OAuth2 client_credentials grant."""
    return _fetch_reddit_search(url, _reddit_access_token(client_id, client_secret))


def fetch_x_tweets(url: str, bearer_token: str) -> list[dict[str, str]]:
    """Fetch recent tweets from X API v2."""
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {bearer_token}", "User-Agent": _USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return [
        {
            "name": tweet.get("text", "")[:80],
            "url": f"https://x.com/i/status/{tweet['id']}" if tweet.get("id") else "",
            "description": tweet.get("text", "")[:200],
            "heading": "#ClaudeCode",
        }
        for tweet in data.get("data", [])
    ]


def fetch_and_extract_source(source: dict[str, str]) -> list[dict[str, str]]:
    """Fetch and extract entries from a source, handling auth requirements.

    Skips with a WARNING (returning []) when required credentials are unset.
    """
    auth = source.get("auth", "none")
    if auth == "reddit":
        creds = _require_env(source["name"], "REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET")
        return fetch_reddit(source["url"], *creds) if creds else []
    if auth == "x_bearer":
        creds = _require_env(source["name"], "X_BEARER_TOKEN")
        return fetch_x_tweets(source["url"], creds[0]) if creds else []

    content = fetch_text(source["url"])
    if source["type"] == "markdown":
        return extract_markdown_entries(content)
    return extract_html_entries(content)


def main() -> None:
    """Entry point for the community monitor script."""
    parser = argparse.ArgumentParser(
        description="Monitor community sources for CC features and tips."
    )
    parser.add_argument("--community-docs-dir", required=True, type=Path,
                        help="Path to docs/cc-community/ directory")
    parser.add_argument("--state-file", type=Path,
                        default=Path(".github/state/community-monitor-state.json"),
                        help="Path to state file tracking previously seen entries")
    args = parser.parse_args()

    if not args.community_docs_dir.exists():
        fatal(f"ERROR: Community docs dir does not exist: {args.community_docs_dir}")

    run_monitor(
        sources=SOURCES,
        fetch_fn=fetch_and_extract_source,
        docs_dir=args.community_docs_dir,
        state_file=args.state_file,
        report_title="Community Monitor Report",
        script_name="community-monitor.py",
    )


if __name__ == "__main__":
    main()
