#!/usr/bin/env python3
"""Write build.json (version, last-modified date, commit links) for the Pages site.

Run by the gh-pages deploy (needs full git history for the graph's own commit);
thin IO wrapper around the unit-tested pages_build.site_info / read_version.
With --graph, it also re-applies the idempotent restyle_graph to the *deployed* copy
of graph.html so it loads build-info.js. The committed ui/graph.html is left
untouched, so its git history still dates the real graph rebuild.

Usage:
    python scripts/build-site-info.py [--out ui/build.json] [--graph _site/graph.html]
"""
import argparse
import json
import subprocess
from pathlib import Path

from pages_build import read_version, restyle_graph, site_info

REPO_URL = "https://github.com/qte77/ai-agents-research"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()


def _last_commit(path: str | None = None) -> tuple[str | None, str | None]:
    """``(sha, ISO date)`` of HEAD, or of the last commit touching ``path``."""
    out = _git("log", "-1", "--format=%H %cI", *(["--", path] if path else []))
    return tuple(out.split(" ", 1)) if out else (None, None)


def main() -> None:
    parser = argparse.ArgumentParser(description="Write build.json for the Pages site.")
    parser.add_argument("--out", type=Path, default=Path("ui/build.json"))
    parser.add_argument("--graph", type=Path, help="Deployed graph.html to tag with build-info.js")
    args = parser.parse_args()

    if args.graph and args.graph.exists():
        args.graph.write_text(restyle_graph(args.graph.read_text(encoding="utf-8")), encoding="utf-8")

    commit, commit_date = _last_commit()
    graph_commit, graph_date = _last_commit("ui/graph.html")
    info = site_info(read_version(Path("pyproject.toml").read_text(encoding="utf-8")),
                     commit, commit_date, graph_commit, graph_date, REPO_URL)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(info, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}: v{info['version']} @ {info['site']['short']}")


if __name__ == "__main__":
    main()
