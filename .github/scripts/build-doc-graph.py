#!/usr/bin/env python3
"""Build the doc graph JSON the Pages site loads (plan 0009 row G; plan 0015 G2).

Pure graph logic lives in ``lib/doc_graph.py``; this entry point reads the corpus
from ``--root`` and writes its slim site projection (docs with their topic hubs,
one edge per linked pair). ``docs/archive/`` is skipped.

Usage:
    python build-doc-graph.py [--root .] [--out ui/doc-graph.json]

Exit codes:
    0 = graph written
    2 = fatal error (no docs/ under --root)
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.doc_coverage import hub_filing  # noqa: E402
from lib.doc_graph import build_graph, load_corpus, site_graph, to_json  # noqa: E402


def main() -> None:
    """Entry point: build the site graph from the corpus and write it as JSON."""
    parser = argparse.ArgumentParser(description="Build the doc graph JSON for the Pages site.")
    parser.add_argument("--root", type=Path, default=Path("."),
                        help="Repo root containing docs/ (default: .)")
    parser.add_argument("--out", type=Path, default=Path("ui/doc-graph.json"),
                        help="Output JSON path (default: ui/doc-graph.json)")
    args = parser.parse_args()

    if not (args.root / "docs").is_dir():
        print(f"ERROR: no docs/ under {args.root}", file=sys.stderr)
        sys.exit(2)

    docs = load_corpus(args.root)
    graph = site_graph(build_graph(docs), hub_filing(docs))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(to_json(graph), encoding="utf-8")
    # Reason: same count as the page's checkboxes, which leave the hubs themselves to their own boxes.
    counts = Counter(n["filing"] for n in graph["nodes"]
                     if not n["hubs"] and (n["bucket"] != "_topics" or n["id"] == "docs/_topics/README.md"))
    print(f"Wrote {args.out}: {len(graph['nodes'])} docs ({counts['unfiled']} unfiled, "
          f"{counts['exempt']} exempt, {counts['not-hub-content']} not hub content), "
          f"{len(graph['edges'])} linked pairs")


if __name__ == "__main__":
    main()
