#!/usr/bin/env python3
"""Publish graphify-out/graph.html to the gh-pages branch as index.html.

Idempotent: updates the existing gh-pages branch (creates it if missing). Uses
the GitHub API only — it never touches the local git tree, so it is safe to run
with uncommitted work on main. Requires the `gh` CLI authenticated for the repo.

Run from the repo root, or via `make graph-publish`.
"""
import base64
import json
import os
import subprocess
import sys
from pathlib import Path

REPO = os.environ.get("GRAPHIFY_PAGES_REPO", "qte77/ai-agents-research")
HTML = Path("graphify-out/graph.html")

if not HTML.exists():
    sys.exit("graphify-out/graph.html not found — run `make graph-html` (or build) first")

# Invalid GH_TOKEN/GITHUB_TOKEN env vars can shadow the stored gh credential.
env = dict(os.environ)
env.pop("GH_TOKEN", None)
env.pop("GITHUB_TOKEN", None)


def gh(method, path, body=None):
    cmd = ["gh", "api", "--method", method, path]
    inp = json.dumps(body) if body is not None else None
    if body is not None:
        cmd += ["--input", "-"]
    r = subprocess.run(cmd, input=inp, capture_output=True, text=True, env=env)
    if r.returncode != 0:
        sys.exit(f"gh api {method} {path} failed:\n{r.stderr}\n{r.stdout}")
    return json.loads(r.stdout) if r.stdout.strip() else {}


# Current gh-pages head (used as the commit parent), if the branch exists.
parent = None
probe = subprocess.run(
    ["gh", "api", f"repos/{REPO}/git/ref/heads/gh-pages"],
    capture_output=True, text=True, env=env,
)
if probe.returncode == 0 and probe.stdout.strip():
    parent = json.loads(probe.stdout)["object"]["sha"]

index_blob = gh("POST", f"repos/{REPO}/git/blobs",
                {"content": base64.b64encode(HTML.read_bytes()).decode(), "encoding": "base64"})
nojekyll_blob = gh("POST", f"repos/{REPO}/git/blobs", {"content": "", "encoding": "utf-8"})
tree = gh("POST", f"repos/{REPO}/git/trees", {"tree": [
    {"path": "index.html", "mode": "100644", "type": "blob", "sha": index_blob["sha"]},
    {"path": ".nojekyll", "mode": "100644", "type": "blob", "sha": nojekyll_blob["sha"]},
]})
commit = gh("POST", f"repos/{REPO}/git/commits", {
    "message": "Refresh graphify knowledge graph (GitHub Pages)\n\nCo-Authored-By: Claude <noreply@anthropic.com>",
    "tree": tree["sha"],
    "parents": [parent] if parent else [],
})
if parent:
    gh("PATCH", f"repos/{REPO}/git/refs/heads/gh-pages", {"sha": commit["sha"]})
else:
    gh("POST", f"repos/{REPO}/git/refs", {"ref": "refs/heads/gh-pages", "sha": commit["sha"]})

print(f"Published graph.html ({HTML.stat().st_size:,} bytes) to gh-pages @ {commit['sha'][:12]}")
print("Live: https://qte77.github.io/ai-agents-research/")
