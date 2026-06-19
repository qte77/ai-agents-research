#!/usr/bin/env python3
"""Render the EyeRest-restyled knowledge graph into the committed ui/graph.html.

Local/interactive step (graphify stays key-free, no LLM in CI): build the graph
with the /graphify skill (or `make graph-build`), render it with `make graph-html`,
then run this — or just `make graph-page` — to write the branded ui/graph.html
that the gh-pages workflow deploys. Commit ui/graph.html to publish.

Stdlib only; reuses the unit-tested restyle_graph from the src/ module.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pages_build import filter_graph_data, restyle_graph  # noqa: E402

SRC = Path("graphify-out/graph.html")
DST = Path("ui/graph.html")

if not SRC.exists():
    sys.exit(f"{SRC} not found — run `make graph-html` (or build the graph) first")

# Prune tooling/code nodes, then apply the EyeRest brand.
html = restyle_graph(filter_graph_data(SRC.read_text(encoding="utf-8")))
DST.parent.mkdir(parents=True, exist_ok=True)
DST.write_text(html, encoding="utf-8")
print(f"Wrote branded {DST} ({DST.stat().st_size:,} bytes) — commit it to publish")
