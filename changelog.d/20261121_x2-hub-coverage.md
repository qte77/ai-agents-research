### Added

- `make check_coverage` now also fails on duplicate topic-hub rows (same doc and section) and on more unhubbed docs than the `MAX_UNHUBBED` ratchet (71, only ever lowered); the D6 hub exemptions are in CONTRIBUTING § Index maintenance, duplicate rows in `memory.md`, `harness.md` and `plugins.md` are merged, and `data.md` points to the knowledge-graph, memory and RAG hubs instead of repeating their rows (plan 0015 X2)
