#!/usr/bin/env python3
"""Validate doc frontmatter ``status:`` tokens across docs/ (#348).

Pure parsing/validation lives in ``lib/doc_status.py``; this entry point walks
the docs tree, reads files, and maps violations to an exit code. ``docs/archive/``
is skipped (archived docs are frozen).

Usage:
    python check-doc-status.py [--docs-dir docs] [--strict]

Exit codes:
    0 = no violations
    1 = one or more violations (invalid token; or, with --strict, a residual body badge)
    2 = fatal error (docs dir missing)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.doc_status import check_doc, render_report  # noqa: E402


def main() -> None:
    """Entry point: validate every docs/ markdown file and exit accordingly."""
    parser = argparse.ArgumentParser(description="Validate doc status: frontmatter tokens.")
    parser.add_argument("--docs-dir", type=Path, default=Path("docs"),
                        help="Docs directory to scan (default: docs)")
    parser.add_argument("--strict", action="store_true",
                        help="Also forbid residual body **Status**: badges")
    args = parser.parse_args()

    if not args.docs_dir.is_dir():
        print(f"ERROR: docs dir not found: {args.docs_dir}", file=sys.stderr)
        sys.exit(2)

    violations = []
    for md in sorted(args.docs_dir.rglob("*.md")):
        if "archive" in md.relative_to(args.docs_dir).parts:
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        violations.extend(check_doc(str(md), text, strict=args.strict))

    print(render_report(violations))
    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
