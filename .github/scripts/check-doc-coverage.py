#!/usr/bin/env python3
"""Check doc coverage: README index, inbound links (plan 0015 X1) and section anchors (X3).

Pure logic lives in ``lib/doc_coverage.py``; this entry point reads ``docs/`` (minus
the archive) and the repo-root markdown files, prints each violation and sets the
exit code.

Usage:
    python check-doc-coverage.py [--root .]

Exit codes:
    0 = no violations
    1 = one or more violations
    2 = fatal error (no docs/ under --root)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.doc_coverage import check_anchors, check_coverage  # noqa: E402
from lib.doc_graph import load_corpus  # noqa: E402


def main() -> None:
    """Entry point: run the coverage checks and exit accordingly."""
    parser = argparse.ArgumentParser(description="Check README-index, inbound-link and anchor coverage of docs/.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Repo root containing docs/ (default: .)")
    args = parser.parse_args()

    if not (args.root / "docs").is_dir():
        print(f"ERROR: no docs/ under {args.root}", file=sys.stderr)
        sys.exit(2)

    root_files = {p.name: p.read_text(encoding="utf-8") for p in sorted(args.root.glob("*.md"))}
    docs = load_corpus(args.root)
    problems = check_coverage(docs, root_files) + check_anchors(docs)
    for line in problems:
        print(line)
    if problems:
        print(f"doc-coverage: {len(problems)} violation(s)", file=sys.stderr)
        sys.exit(1)
    print("doc-coverage: OK")


if __name__ == "__main__":
    main()
