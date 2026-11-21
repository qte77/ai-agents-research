#!/usr/bin/env python3
"""Check content-doc frontmatter against the CONTRIBUTING §1–§2 schema (plan 0015 F2).

Pure logic lives in ``lib/doc_frontmatter.py``. Lenient by default: violations are
printed and the exit code is 0. ``--strict`` exits 1 on any violation; ``make
check_frontmatter`` (and CI) runs strict since the plan 0015 F3 migration.

Usage:
    python check-doc-frontmatter.py [--root .] [--strict]

Exit codes:
    0 = no violations, or lenient mode
    1 = violations in strict mode
    2 = fatal error (no docs/ under --root)
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.doc_frontmatter import check_doc, in_scope  # noqa: E402


def main() -> None:
    """Entry point: check every in-scope doc and exit accordingly."""
    parser = argparse.ArgumentParser(description="Check content-doc frontmatter against the schema.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Repo root containing docs/ (default: .)")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any violation")
    args = parser.parse_args()

    docs_dir = args.root / "docs"
    if not docs_dir.is_dir():
        print(f"ERROR: no docs/ under {args.root}", file=sys.stderr)
        sys.exit(2)

    kinds: Counter = Counter()
    docs_with_problems = 0
    for path in sorted(docs_dir.rglob("*.md")):
        rel = path.relative_to(args.root).as_posix()
        if not in_scope(rel):
            continue
        problems = check_doc(path.read_text(encoding="utf-8"))
        docs_with_problems += bool(problems)
        for p in problems:
            print(f"{rel}: {p}")
            kinds[p.split(":")[0]] += 1

    summary = ", ".join(f"{n} × {k}" for k, n in kinds.most_common())
    mode = "strict" if args.strict else "lenient"
    print(f"doc-frontmatter ({mode}): {docs_with_problems} doc(s) with violations" + (f" — {summary}" if summary else ""))
    if args.strict and docs_with_problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
