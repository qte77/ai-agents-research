### Changed

- `Makefile`: `lint` now runs `check_docs` + `check_actions` before the network-dependent `check_links`, so a transient lychee failure can no longer mask markdownlint/actionlint locally (root cause of a markdownlint error reaching CI in #366).
- `docs/architecture.md`: corrected the automated-monitor count (three → four), added root `scripts/`/`tests/`/`ui/`/`changelog.d/` to the directory tree, and documented `link-rot-monitor` as a fifth (health, not content) scheduled workflow.

### Fixed

- `docs/non-cc/cocoindex-analysis.md`: removed a duplicate `**Status**` line inside the Adoption Decision section.
- `docs/non-cc/fastcontext-analysis.md`: finalized the #362 note — analysis kept (arXiv paper is authoritative; upstream Microsoft repo removed).
