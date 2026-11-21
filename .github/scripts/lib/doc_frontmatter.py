"""Frontmatter schema check for content docs (CONTRIBUTING §1–§2; plan 0015 F2, owner decision D5).

Regex parsing only (no YAML dependency), like ``doc_status.py``; no file IO here, so
the entry point ``check-doc-frontmatter.py`` owns reading files and exit codes.
"""
from __future__ import annotations

import re

from .doc_status import DOC_STATUS_VOCAB, extract_frontmatter

REQUIRED = ("title", "purpose", "created", "updated", "validated_links", "status")
OPTIONAL = frozenset({"source", "platform_scope", "test_run"})
REMOVED = frozenset({"sources", "description", "release", "version", "license", "authority", "category"})
DATE_KEYS = ("created", "updated", "validated_links")
LIFECYCLE = DOC_STATUS_VOCAB

# Not content docs: indexes, hubs, plans (own schema), example files, the archive, generated output.
_OUT_OF_SCOPE = ("docs/_topics/", "docs/plans/", "docs/cc-native/examples/", "docs/archive/", "docs/research/")
_TOP_KEY = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$")
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_ONE_URL = re.compile(r"^https?://\S+$")


def in_scope(path: str) -> bool:
    """True for content docs the schema applies to."""
    return path.startswith("docs/") and not path.endswith("/README.md") and not path.startswith(_OUT_OF_SCOPE)


def _keys(frontmatter: str) -> dict[str, str]:
    """Top-level ``key: value`` pairs; indented or list lines belong to the key above."""
    out = {}
    for line in frontmatter.splitlines():
        m = _TOP_KEY.match(line)
        if m:
            out[m.group(1)] = m.group(2).strip("\"'")
    return out


def check_doc(text: str) -> list[str]:
    """Schema violations for one doc, in a stable order."""
    fm = extract_frontmatter(text)
    if fm is None:
        return ["no frontmatter"]
    keys = _keys(fm)
    problems = [f"missing required key: {k}" for k in REQUIRED if k not in keys]
    for k in DATE_KEYS:
        if k in keys and not _ISO_DATE.match(keys[k]):
            problems.append(f"{k} is not an ISO date (YYYY-MM-DD): {keys[k]}")
    for k in sorted(set(keys) - set(REQUIRED) - OPTIONAL):
        problems.append(f"key not allowed (see CONTRIBUTING §1): {k}" if k in REMOVED else f"unknown key: {k}")
    if "source" in keys and not _ONE_URL.match(keys["source"]):
        problems.append(f"source must be one URL (others go in the Sources section): {keys['source']}")
    status = keys.get("status")
    if status is not None and status not in LIFECYCLE:
        problems.append(f"status not in the lifecycle vocabulary (CONTRIBUTING §2): {status}")
    return problems
