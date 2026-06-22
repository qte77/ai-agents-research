### Added

- `docs/cc-native/configuration/CC-model-provider-configuration.md`: **5 hosted CC-integrated gateways** (Portkey, Martian, Vercel AI Gateway, Zuplo, RelayPlane) back-ported as a compact CC-config table — each `ANTHROPIC_BASE_URL` / auth pattern verified against the gateway's own Claude Code docs (2026-06-22). Defers to `llm-routers-gateways-landscape.md` for the full catalog (router-architecture consolidation, DRY). Partial #304.
- `docs/non-cc/aider-analysis.md`: expanded the **repo-map** mechanism — symbol extraction, PageRank-style graph ranking over the dependency graph, `--map-tokens` (default 1,000), and dynamic auto-sizing (first-party `aider.chat/docs/repomap.html`). Partial #304.

### Changed

- `docs/non-cc/llm-routers-gateways-landscape.md`: bottom cross-ref now records that the five CC-integrated gateways are back-ported into the CC config doc, with the landscape kept as the single authoritative catalog (license/pricing/breadth).
