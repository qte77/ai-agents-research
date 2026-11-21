#!/usr/bin/env python3
"""Check doc coverage: README index, inbound links (plan 0015 X1), section anchors (X3) and topic hubs (X2).

Also reports, without failing, glossary abbreviations a doc uses but never expands (C2).

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
from lib.doc_coverage import (  # noqa: E402
    GLOSSARY, check_abbreviations, check_anchors, check_coverage, check_hub_duplicates, parse_glossary, unhubbed,
)
from lib.doc_graph import load_corpus  # noqa: E402


def main() -> None:
    """Entry point: run the coverage checks and exit accordingly."""
    parser = argparse.ArgumentParser(description="Check README-index, inbound-link and anchor coverage of docs/.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Repo root containing docs/ (default: .)")
    parser.add_argument("--max-unhubbed", type=int, default=None,
                        help="Ratchet: fail if more content docs than this are in no topic hub (plan 0015 X2)")
    args = parser.parse_args()

    if not (args.root / "docs").is_dir():
        print(f"ERROR: no docs/ under {args.root}", file=sys.stderr)
        sys.exit(2)

    root_files = {p.name: p.read_text(encoding="utf-8") for p in sorted(args.root.glob("*.md"))}
    docs = load_corpus(args.root)
    problems = check_coverage(docs, root_files) + check_anchors(docs) + check_hub_duplicates(docs)
    missing = unhubbed(docs)
    if args.max_unhubbed is not None and len(missing) > args.max_unhubbed:
        problems += [f"{p}: in no topic hub" for p in missing]
        problems.append(f"{len(missing)} docs in no topic hub, above the ratchet of {args.max_unhubbed}: add hub rows")
    elif args.max_unhubbed is not None and len(missing) < args.max_unhubbed:
        print(f"note: {len(missing)} docs in no topic hub; lower MAX_UNHUBBED in the Makefile to {len(missing)}")
    # Reason: report-only until the abbreviation backfill (plan 0015 C2); never sets the exit code.
    unexpanded = check_abbreviations(docs, parse_glossary(docs.get(GLOSSARY, "")))
    for line in unexpanded:
        print(f"report: {line}")
    if unexpanded:
        print(f"note: {len(unexpanded)} docs use a glossary abbreviation without expanding it (report-only)")
    for line in problems:
        print(line)
    if problems:
        print(f"doc-coverage: {len(problems)} violation(s)", file=sys.stderr)
        sys.exit(1)
    print("doc-coverage: OK")


if __name__ == "__main__":
    main()
