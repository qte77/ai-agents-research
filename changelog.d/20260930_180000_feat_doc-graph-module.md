### Added

- `.github/scripts/lib/doc_graph.py` + `tests/test_doc_graph.py`: deterministic structural doc graph (plan 0009 row G, option B; #504), built test-first. Doc nodes with bucket, status (via `doc_status`) and title; external-domain nodes; aggregated `link` / `hub` / `cites` edges with line numbers; code fences ignored; `docs/archive/` excluded; byte-identical JSON regardless of input order.
- `.github/scripts/build-doc-graph.py` and `make graph-data`: write the graph to `ui/doc-graph.json` (no LLM, stdlib only).
