"""Frontmatter schema check for content docs (plan 0015 F2, owner decision D5).

The rules come from ``docs/schema/frontmatter.schema.json`` (via ``frontmatter_schema``).
Regex parsing only (no YAML dependency), like ``doc_status.py``; the entry point
``check-doc-frontmatter.py`` owns reading docs and exit codes.
"""
from __future__ import annotations

import re

from .doc_status import DOC_STATUS_VOCAB, extract_frontmatter
from .frontmatter_schema import PROPERTIES, SCHEMA, SCHEMA_PATH  # noqa: F401  (SCHEMA_PATH re-exported)

REQUIRED = tuple(SCHEMA["required"])
OPTIONAL = frozenset(PROPERTIES) - frozenset(REQUIRED)
REMOVED = frozenset(SCHEMA["x-removed"])
DATE_KEYS = tuple(k for k, v in PROPERTIES.items() if v.get("format") == "date")
LIFECYCLE = DOC_STATUS_VOCAB
PLATFORMS = frozenset(PROPERTIES["platform_scope"]["items"]["enum"])
PURPOSE_MAX = PROPERTIES["purpose"]["maxLength"]  # one line; detail belongs in the body

# Not content docs: indexes, hubs, plans (own schema), example files, the archive, generated output.
_OUT_OF_SCOPE = ("docs/_topics/", "docs/plans/", "docs/cc-native/examples/", "docs/archive/", "docs/research/")
_TOP_KEY = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$")
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_ONE_URL = re.compile(PROPERTIES["source"]["pattern"])
_INLINE_LIST = re.compile(r"^\[(.*)\]$")
_BLOCK_SCALAR = re.compile(r"^[>|][+-]?\d?[+-]?$")  # YAML folded/literal markers: >, |-, >+, |2 ...
_CONTINUED = re.compile(r"^purpose:.*\n[ \t]+\S", re.M)  # an indented line right after purpose:


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
    if keys.get("title") == "":
        problems.append("title must not be empty")
    for k in DATE_KEYS:
        if k in keys and not _ISO_DATE.match(keys[k]):
            problems.append(f"{k} is not an ISO date (YYYY-MM-DD): {keys[k]}")
    for k in sorted(set(keys) - set(REQUIRED) - OPTIONAL):
        problems.append(f"key not allowed (see docs/schema/frontmatter.schema.json): {k}" if k in REMOVED else f"unknown key: {k}")
    if "source" in keys and not _ONE_URL.match(keys["source"]):
        problems.append(f"source must be one URL (others go in the Sources section): {keys['source']}")
    purpose = keys.get("purpose")
    if purpose is not None:
        if not purpose or _BLOCK_SCALAR.match(purpose) or _CONTINUED.search(fm):
            problems.append("purpose must be one non-empty line")
        elif len(purpose) > PURPOSE_MAX:
            problems.append(f"purpose over {PURPOSE_MAX} characters; keep it to one line (detail goes in the body)")
    if "platform_scope" in keys:
        m = _INLINE_LIST.match(keys["platform_scope"])
        if not m:
            problems.append("platform_scope must be an inline list, e.g. [claude-code, codex]")
        else:
            for slug in sorted({v.strip() for v in m.group(1).split(",") if v.strip()} - PLATFORMS):
                problems.append(f"platform_scope value not in the harness list (docs/schema/frontmatter.schema.json): {slug}")
    status = keys.get("status")
    if status is not None and status not in LIFECYCLE:
        problems.append(f"status not in the lifecycle vocabulary (CONTRIBUTING §2): {status}")
    return problems
