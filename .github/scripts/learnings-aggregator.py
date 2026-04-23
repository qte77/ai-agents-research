"""Aggregate AGENT_LEARNINGS.md files from qte77 repos.

Fetches AGENT_LEARNINGS.md from each mapped qte77 repo, writes raw content
to docs/learnings/per-repo/<stem>.md with frontmatter. Skips unchanged
files via SHA-256 fingerprint stored in .github/state/.

Exits 1 when any file updated (triggers PR creation in workflow).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

# Add sibling lib to path for shared utilities
sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor_utils import fetch_text  # noqa: E402

# Key = GitHub repo name, value = target filename stem in docs/learnings/per-repo/.
# Preserves curated filenames for existing files (agents-eval, ralph-template, so101-biolab).
REPO_FILENAME_MAP: dict[str, str] = {
    "Agents-eval": "agents-eval",
    "ralph-loop-cc-tdd-wt-vibe-kanban-template": "ralph-template",
    "so101-biolab-automation": "so101-biolab",
    "cc-voice-plugin-prototype": "cc-voice-plugin-prototype",
    "learnings-ralphy": "learnings-ralphy",
    "claude-code-plugins": "claude-code-plugins",
    "research-ralphy": "research-ralphy",
}


def fetch_learnings(owner: str, repo: str) -> str | None:
    """Fetch raw AGENT_LEARNINGS.md from owner/repo main branch."""
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/AGENT_LEARNINGS.md"
    try:
        return fetch_text(url)
    except Exception as exc:
        print(f"  fetch failed: {exc}", file=sys.stderr)
        return None


def render_file(owner: str, repo: str, content: str) -> str:
    """Wrap upstream content with frontmatter + source attribution."""
    today = date.today().isoformat()
    source_url = f"https://github.com/{owner}/{repo}/blob/main/AGENT_LEARNINGS.md"
    frontmatter = (
        "---\n"
        f'title: "{repo} AGENT_LEARNINGS"\n'
        f"description: Mirror of AGENT_LEARNINGS.md from {owner}/{repo}.\n"
        f"updated: {today}\n"
        f"source: {source_url}\n"
        "---\n\n"
        "> Auto-aggregated by `.github/scripts/learnings-aggregator.py`.\n"
        f"> Source: [{owner}/{repo}/AGENT_LEARNINGS.md]({source_url}).\n"
        "> Manual edits will be overwritten on the next run.\n\n"
    )
    return frontmatter + content


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="qte77")
    parser.add_argument("--target-dir", default="docs/learnings/per-repo")
    parser.add_argument(
        "--state-file",
        default=".github/state/learnings-aggregator-state.json",
    )
    args = parser.parse_args()

    target_dir = Path(args.target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    state_file = Path(args.state_file)

    state: dict[str, str] = {}
    if state_file.exists():
        state = json.loads(state_file.read_text(encoding="utf-8"))

    updated: list[str] = []

    for repo, stem in REPO_FILENAME_MAP.items():
        print(f"Fetching {args.owner}/{repo}", file=sys.stderr)
        content = fetch_learnings(args.owner, repo)
        if content is None:
            print("  SKIP: no AGENT_LEARNINGS.md", file=sys.stderr)
            continue

        rendered = render_file(args.owner, repo, content)
        fingerprint = hashlib.sha256(rendered.encode("utf-8")).hexdigest()[:16]

        if state.get(repo) == fingerprint:
            print("  SKIP: unchanged", file=sys.stderr)
            continue

        target = target_dir / f"{stem}.md"
        target.write_text(rendered, encoding="utf-8")
        state[repo] = fingerprint
        updated.append(f"{repo} -> {target}")
        print(f"  UPDATED: {target}", file=sys.stderr)

    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(
        json.dumps(state, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if updated:
        print(f"\nUpdated {len(updated)} file(s):")
        for line in updated:
            print(f"  - {line}")
        return 1

    print("No changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
