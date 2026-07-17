"""Pure validation logic for doc frontmatter ``status:`` tokens (#348).

No file IO / argparse / sys.exit here (the entry script ``check-doc-status.py``
reads files and handles exit codes), so the parsing and validation logic is
unit-testable.

Two checks, gated by ``strict``:

* **lenient** (default) — if a doc declares a frontmatter ``status:``, its value
  must be in the controlled vocabulary. A missing ``status:`` is allowed (the
  corpus is mid-migration; badge-less READMEs/specs never get one).
* **strict** — additionally, no doc may keep a body ``**Status**:`` *badge*. The
  badge is the doc-level line in the preamble (before the first heading); a
  ``**Status**:`` line under a later section describes something else and is left
  alone (see ``agent-observability-methods-analysis.md``).
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# Normalized leading token of the legacy body `**Status**:` badge (kebab-case).
# Analysis/reference/research docs use the maturity set; plan docs (docs/plans/)
# add draft|approved|superseded|done. Keep in sync with CONTRIBUTING.md
# "Frontmatter status" and docs/plans/2026-07-05-status-frontmatter-migration.md.
DOC_STATUS_VOCAB = frozenset({
    "adopt", "trial", "assess", "hold",
    "research", "reference", "research-preview", "beta",
    "generally-available", "stable", "public-preview", "available",
    "verified", "proprietary", "source-available", "open-source",
    "active-development", "completed", "done", "archived",
})
PLAN_STATUS_VOCAB = frozenset({"draft", "approved", "superseded"})
VOCAB = DOC_STATUS_VOCAB | PLAN_STATUS_VOCAB

_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
_STATUS_KEY = re.compile(r"^status:\s*(.+?)\s*$", re.MULTILINE)
_BADGE = re.compile(r"^\*\*Status\*\*:\s*(.+?)\s*$")
_HEADING = re.compile(r"^#{1,6}\s")


def extract_frontmatter(text: str) -> str | None:
    """Return the YAML frontmatter block (between the leading ``---`` fences)."""
    m = _FRONTMATTER.match(text)
    return m.group(1) if m else None


def frontmatter_status(text: str) -> str | None:
    """Return the ``status:`` value from the doc's frontmatter, or ``None``."""
    fm = extract_frontmatter(text)
    if fm is None:
        return None
    m = _STATUS_KEY.search(fm)
    return m.group(1).strip() if m else None


def preamble_badge(text: str) -> str | None:
    """Return the doc-level ``**Status**:`` badge value, or ``None``.

    Only the *preamble* — the region between the frontmatter close and the first
    body heading — is inspected. A ``**Status**:`` line under a later section is
    not the doc's own badge (e.g. one describing an upstream project's status).
    """
    fm = _FRONTMATTER.match(text)
    body = text[fm.end():] if fm else text
    for line in body.splitlines():
        if _HEADING.match(line):
            return None
        m = _BADGE.match(line)
        if m:
            return m.group(1).strip()
    return None


@dataclass(frozen=True)
class Violation:
    """A single doc-status problem, keyed by repo-relative path."""
    path: str
    kind: str    # "invalid-token" | "residual-badge"
    detail: str


def check_doc(path: str, text: str, *, strict: bool = False) -> list[Violation]:
    """Return the status violations for one doc's text (empty if clean)."""
    out: list[Violation] = []
    status = frontmatter_status(text)
    if status is not None and status not in VOCAB:
        out.append(Violation(path, "invalid-token",
                             f"frontmatter status: {status!r} not in vocabulary"))
    if strict:
        badge = preamble_badge(text)
        if badge is not None:
            out.append(Violation(path, "residual-badge",
                                 f"body **Status**: {badge!r} — move to frontmatter status:"))
    return out


def render_report(violations: list[Violation]) -> str:
    """Human-readable summary of violations (one per line), or an all-clear."""
    if not violations:
        return "doc-status: OK"
    lines = [f"doc-status: {len(violations)} violation(s)"]
    for v in violations:
        lines.append(f"  {v.path}: [{v.kind}] {v.detail}")
    return "\n".join(lines)
