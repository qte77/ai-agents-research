### Fixed

- `CONTRIBUTING.md`: corrected the Directory Structure tree to match reality — added `docs/archive/`, `docs/learnings/`, `docs/cc-native/model-internals/`, root `changelog.d/`, `scripts/`, `ui/`, and `.github/state/`; removed the retired `docs/todo/`. Fixed 3 stale `docs/todo/` prose references to `docs/archive/` (including the incorrect "`docs/todo/` is in `lychee.toml` `exclude_path`" claim — it is `docs/archive/`).

### Changed

- `Makefile`: hoisted the markdown-lint file list into a single `DOC_LINT_GLOB` variable shared by `check_docs` + `autofix`, and widened it to also lint the root governance docs (`CLAUDE.md`, `AGENTS.md`, `AGENT_LEARNINGS.md`, `AGENT_REQUESTS.md`).
- `docs/architecture.md`: updated the lint-scope row to match the widened glob, and documented the `uv tool install graphifyy` key-free graphify install path (previously only the side-loaded `GRAPHIFY=` path was noted).
- `README.md`: added an inbound link to `docs/UserStory.md` (a current requirements doc that was previously unlinked/undiscoverable).
