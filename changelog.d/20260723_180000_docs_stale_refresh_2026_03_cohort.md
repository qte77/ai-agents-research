### Added

- `.claude/workflows/refresh-docs.js`: generalized, args-driven stale-fact refresh workflow (read-only checker per doc + adversarial verifier per correction set); documented in `docs/architecture.md` §Automated Monitors.

### Changed

- Stale-fact refresh of the 27-doc `validated_links: 2026-03-*` cohort (first `refresh-docs` run, ~50 agents): ~110 adversarially-verified corrections applied across 24 docs (3 clean) — version gates, feature renames, count/roster drift, dead-URL replacements — spanning cc-community (2), agents-skills (1), ci-remote (6), configuration (3), plugins-ecosystem (7), sandboxing (3), sessions (2), non-cc (1); all touched docs bumped to `updated`/`validated_links: 2026-07-23`.
- `lychee.toml`: exact-URL exclude for the bot-blocking (403) Salesforce MCP-GA blog cite (page verified live via WebFetch 2026-07-23; owner-approved).

### Fixed

- `docs/non-cc/kiro-analysis.md`: de-linked the usage.ai AWS-May-2026 source (dead — redirect loop as of 2026-07-23; retained as plain-text provenance).
