#!/usr/bin/env python3
"""Build the deterministic structural doc graph (plan 0009 row G, option B; #504).

Pure graph logic lives in ``lib/doc_graph.py``; this entry point reads the corpus
from ``--root`` and writes the JSON. ``docs/archive/`` is skipped.

Usage:
    python build-doc-graph.py [--root .] [--out ui/doc-graph.json]

Exit codes:
    0 = graph written
    2 = fatal error (no docs/ under --root)
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.doc_graph import build_graph, load_corpus, to_json  # noqa: E402


def main() -> None:
    """Entry point: build the graph from the corpus and write it as JSON."""
    parser = argparse.ArgumentParser(description="Build the structural doc graph JSON.")
    parser.add_argument("--root", type=Path, default=Path("."),
                        help="Repo root containing docs/ (default: .)")
    parser.add_argument("--out", type=Path, default=Path("ui/doc-graph.json"),
                        help="Output JSON path (default: ui/doc-graph.json)")
    args = parser.parse_args()

    if not (args.root / "docs").is_dir():
        print(f"ERROR: no docs/ under {args.root}", file=sys.stderr)
        sys.exit(2)

    graph = build_graph(load_corpus(args.root))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(to_json(graph), encoding="utf-8")
    docs = sum(1 for n in graph["nodes"] if n["type"] == "doc")
    print(f"Wrote {args.out}: {docs} docs, {len(graph['nodes']) - docs} domains, {len(graph['edges'])} edges")


if __name__ == "__main__":
    main()
