### Added

- `ui/doc-graph.html`: live structural doc graph page (plan 0009 row G slice 2; #504) rendering the deterministic `doc-graph.json` with the vendored vis-network, in EyeRest tokens. Docs are dots, topic hubs diamonds, cited domains squares (toggle, hidden by default), with search, a details panel and a GitHub link per doc. Linked from the landing page and the README.

### Changed

- `.github/workflows/gh-pages.yaml`: the deploy now builds `doc-graph.json` from `docs/` (stdlib, no LLM) and also runs on changes to `docs/**` and the graph builder. The JSON is gitignored and never committed.
