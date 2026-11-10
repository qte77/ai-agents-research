#!/usr/bin/env python3
"""Compare a plan's remaining-work rows with the live state of the PRs/issues they cite.

Run at the start of a session, before reporting what is open or blocked: a row whose PR was
merged weeks ago still reads "blocked" until someone checks. Queries GitHub through the `gh`
CLI (it must be authenticated); pure parsing/assessment logic lives in lib/plan_reconcile.py.

Usage:
    python plan-reconcile.py [--plan PATH] [--repo OWNER/REPO]

Exit codes:
    0 = every row agrees with live state
    1 = at least one row is flagged (or a reference could not be checked)
"""
import argparse
import json
import subprocess  # nosec B404
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.plan_reconcile import assess, extract_refs, remaining_rows, unchecked_open_rows

PLANS_DIR = Path("docs/plans")
DEFAULT_REPO = "qte77/ai-agents-research"


def newest_plan() -> Path:
    """The plan with the highest date-and-sequence filename (YYYY-MM-DD-NNNN-slug.md)."""
    plans = sorted(PLANS_DIR.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]-*.md"))
    if not plans:
        sys.exit(f"ERROR: no plans in {PLANS_DIR}")
    return plans[-1]


def ref_state(repo: str, number: int) -> str | None:
    """"merged" | "closed" | "open" for a PR or issue, or None if gh can't read it."""
    # Reason: fixed argv, no shell, gh resolved from PATH; repo/number come from the plan file.
    result = subprocess.run(  # nosec B603 B607
        ["gh", "api", f"repos/{repo}/issues/{number}"],
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        return None
    data = json.loads(result.stdout)
    if data.get("pull_request", {}).get("merged_at"):
        return "merged"
    return data.get("state")


def main() -> None:
    """Entry point: print one line per remaining-work row and exit 1 if any row is flagged."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--plan", type=Path, default=None, help="Plan file (default: newest in docs/plans)")
    parser.add_argument("--repo", default=DEFAULT_REPO, help="Repo for bare #N references")
    args = parser.parse_args()

    plan = args.plan or newest_plan()
    rows = remaining_rows(plan.read_text(encoding="utf-8"))
    if not rows:
        sys.exit(f"ERROR: no '## Remaining work' table in {plan}")

    refs = {ref for row in rows for ref in extract_refs(row.text, args.repo)}
    states = {ref: ref_state(*ref) for ref in sorted(refs)}

    print(f"Plan: {plan} ({len(rows)} rows, {len(refs)} references)")
    flagged = 0
    for row in rows:
        flag = assess(row, states, args.repo)
        if not flag:
            continue
        flagged += 1
        cited = ", ".join(f"{r}#{n}={states[(r, n)]}" for r, n in extract_refs(row.text, args.repo))
        status = "struck" if row.struck else "open"
        print(f"- {row.row_id} ({status}): {flag} [{cited}]")
    if not flagged:
        print("All rows agree with live state.")
    unchecked = unchecked_open_rows(rows, args.repo)
    if unchecked:
        # Reason: informational only — these rows cite no PR/issue, so check them by hand.
        print(f"Open rows with no PR/issue to check (verify by hand): {', '.join(unchecked)}")
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()
