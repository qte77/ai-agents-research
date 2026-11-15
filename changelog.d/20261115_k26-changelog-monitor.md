### Fixed

- Changelog monitor coverage tagging (plan 0014 K26): a feature line now counts as covered when every backticked setting, variable or flag it names (an assignment like `VAR=1` matches `VAR`) appears backticked in one doc's body. Before, only filenames and H2/H3 headings were indexed, so documented settings stayed UNCOVERED. Since v2.1.71 this moves 93 → 1,448 of 7,940 changelog lines to covered. Tests pin the rule and guard that the scan doc still yields a cutoff.
- `CC-changelog-feature-scan.md`: the frontmatter range is now labelled as the monitor's comparison cutoff, not documentation coverage.

### Added

- 2.1.317–2.1.319 features: `CLAUDE_CODE_AUTO_MODE_SERVER`, `CLAUDE_CODE_DISABLE_FEATURE_FLAGS`, `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`, `CLAUDE_CODE_DISABLE_MCP_TASK_BACKGROUND`, `CLAUDE_CODE_DISABLE_MCP_TASKS` in `CC-env-vars-reference.md`; `permissions.denyInsteadOfPrompting` in `CC-permissions-bypass-analysis.md`; Claude apps gateway pooled-budget rules and `/usage` spend in `CC-model-provider-configuration.md`.
