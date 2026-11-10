"""Pure logic for plan-reconcile.py: compare a plan's remaining-work rows with live PR/issue state.

A plan row stays "open" in text long after the PR it waits on is merged unless someone checks
(plan 0012's D0 and C1 read as blocked for two weeks after both merged). This module finds the
PR/issue references in each row of the plan's single remaining-work table and flags rows whose
text disagrees with the live state. No subprocess / network here: the entry script fetches states.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# owner/repo#N, repo#N (default owner) or #N (default repo). `#` must be followed by digits only,
# so markdown anchors like `#settings-precedence` don't match.
_REF_RE = re.compile(
    r"(?<![\w/.-])(?:(?P<owner>[A-Za-z0-9-]+)/)?(?P<repo>[A-Za-z0-9._-]+)?#(?P<num>\d+)\b"
)
# A reference written as inline code is context (history, a tracker that stays open), not a
# row decider — the convention lets a plan cite it without tripping the check.
_CODE_SPAN_RE = re.compile(r"`[^`]*`")
_SECTION_RE = re.compile(r"^##\s+Remaining work\s*$", re.MULTILINE)
_NEXT_H2_RE = re.compile(r"^##\s+", re.MULTILINE)

DONE_STATES = {"merged", "closed"}


@dataclass(frozen=True)
class Row:
    row_id: str
    struck: bool
    text: str


def extract_refs(text: str, default_repo: str) -> list[tuple[str, int]]:
    """Return the PR/issue references in ``text`` as (owner/repo, number), first-seen order.

    References inside inline code (backticks) are skipped: they are context, not deciders.
    """
    default_owner = default_repo.split("/", 1)[0]
    refs: list[tuple[str, int]] = []
    for m in _REF_RE.finditer(_CODE_SPAN_RE.sub(" ", text)):
        owner, repo, num = m.group("owner"), m.group("repo"), int(m.group("num"))
        if repo is None:
            full = default_repo
        else:
            full = f"{owner or default_owner}/{repo}"
        ref = (full, num)
        if ref not in refs:
            refs.append(ref)
    return refs


def remaining_rows(plan_text: str) -> list[Row]:
    """Rows of the table under the plan's `## Remaining work` heading (header/separator skipped)."""
    start = _SECTION_RE.search(plan_text)
    if not start:
        return []
    rest = plan_text[start.end():]
    nxt = _NEXT_H2_RE.search(rest)
    section = rest[: nxt.start()] if nxt else rest

    rows: list[Row] = []
    in_table = False
    for line in section.splitlines():
        if not line.startswith("|"):
            if in_table:
                break  # the section's single table ended
            continue
        in_table = True
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        first = cells[0] if cells else ""
        if not first or set(first) <= {"-", ":", " "} or first.lower() == "row":
            continue  # separator or header
        struck = first.startswith("~~") and first.endswith("~~")
        rows.append(Row(row_id=first.strip("~").strip(), struck=struck, text=line))
    return rows


def assess(row: Row, states: dict[tuple[str, int], str | None], default_repo: str) -> str:
    """Return a short flag when the row's text disagrees with live state, else "".

    ``states`` maps (repo, number) -> "open" | "closed" | "merged" | None (could not check).
    - open row, every referenced PR/issue merged or closed -> may be stale (check, then strike)
    - struck row, a referenced PR/issue still open -> struck too early, or the ref is follow-up
    """
    refs = extract_refs(row.text, default_repo)
    if not refs:
        return ""
    unknown = [r for r in refs if states.get(r) is None]
    if unknown:
        names = ", ".join(f"{repo}#{num}" for repo, num in unknown)
        return f"could not check {names}"
    found = [states[r] for r in refs]
    if not row.struck and all(s in DONE_STATES for s in found):
        return "open, but all referenced PRs/issues are merged or closed: check, then strike"
    if row.struck and any(s == "open" for s in found):
        names = ", ".join(f"{repo}#{num}" for (repo, num) in refs if states[(repo, num)] == "open")
        return f"struck, but {names} is still open"
    return ""


def unchecked_open_rows(rows: list[Row], default_repo: str) -> list[str]:
    """IDs of open rows that cite no checkable PR/issue, so the check can't tell if they're stale.

    Plan 0012's D2 named its repo but no PR number and read "next" for two weeks after it merged.
    """
    return [r.row_id for r in rows if not r.struck and not extract_refs(r.text, default_repo)]
