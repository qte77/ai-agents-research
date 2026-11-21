#!/usr/bin/env python3
"""Write build.json (version, last-modified date, commit links) for the Pages site.

Run by the gh-pages deploy; thin IO wrapper around the unit-tested
pages_build.site_info / read_version.

Usage:
    python scripts/build-site-info.py [--out ui/build.json]
"""
import argparse
import json
import subprocess
from pathlib import Path

from pages_build import read_version, site_info

REPO_URL = "https://github.com/qte77/ai-agents-research"


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()


def _last_commit() -> tuple[str | None, str | None]:
    """``(sha, ISO date)`` of HEAD."""
    out = _git("log", "-1", "--format=%H %cI")
    return tuple(out.split(" ", 1)) if out else (None, None)


def main() -> None:
    parser = argparse.ArgumentParser(description="Write build.json for the Pages site.")
    parser.add_argument("--out", type=Path, default=Path("ui/build.json"))
    args = parser.parse_args()

    commit, commit_date = _last_commit()
    info = site_info(read_version(Path("pyproject.toml").read_text(encoding="utf-8")),
                     commit, commit_date, REPO_URL)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(info, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}: v{info['version']} @ {info['site']['short']}")


if __name__ == "__main__":
    main()
