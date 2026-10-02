#!/usr/bin/env python3
"""Census of agent-substrate rubric rows and the evidence matrix they imply (plan 0010 row T1).

Pure census logic lives in ``lib/doc_census.py``; this entry point reads ``docs/`` under
``--root``, prints the 8 x 6 matrix (best score per subject and property) and the number of
rows that declare no ``subject:``, and optionally writes the full census as TSV.

Usage:
    python build-doc-census.py [--root .] [--tsv census.tsv]

Exit codes:
    0 = census built
    2 = fatal error (no docs/ under --root)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.doc_census import census_tsv, load_corpus, matrix_markdown  # noqa: E402


def main() -> None:
    """Entry point: print the evidence matrix; write the census TSV if asked."""
    parser = argparse.ArgumentParser(description="Census of rubric rows and the evidence matrix.")
    parser.add_argument("--root", type=Path, default=Path("."),
                        help="Repo root containing docs/ (default: .)")
    parser.add_argument("--tsv", type=Path, help="Also write the full census to this TSV path")
    args = parser.parse_args()

    docs = args.root / "docs"
    if not docs.is_dir():
        print(f"ERROR: no docs/ under {args.root}", file=sys.stderr)
        sys.exit(2)

    rows = load_corpus(docs)
    if args.tsv:
        args.tsv.write_text(census_tsv(rows), encoding="utf-8")
    unassigned = sum(1 for r in rows if r.subject is None)
    print(matrix_markdown(rows))
    print(f"{len(rows)} scored rows; {unassigned} without a subject: tag (not in the matrix)")


if __name__ == "__main__":
    main()
