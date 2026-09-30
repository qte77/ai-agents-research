### Added

- `ui/doc-graph.html`: live structural doc graph page (plan 0009 row G slice 2; #504) rendering the deterministic `doc-graph.json` with the vendored vis-network, in EyeRest tokens. Docs are dots, topic hubs diamonds, cited domains squares (toggle, hidden by default), with search, a details panel and a GitHub link per doc. Linked from the landing page and the README.

- `ui/build-info.js`, `scripts/build-site-info.py`, `pages_build.read_version` / `site_info` (test-first): every page shows the release version, last-modified date and commit link from a deploy-time `build.json`. The knowledge graph shows its own last-rebuild commit and date, not the deploy's. The deploy injects the tag into the published copy only, so `ui/graph.html`'s history still dates the real rebuild.

### Changed

- `.github/workflows/gh-pages.yaml`: the deploy now builds `doc-graph.json` from `docs/` (stdlib, no LLM) and also runs on changes to `docs/**` and the graph builder. The JSON is gitignored and never committed.
