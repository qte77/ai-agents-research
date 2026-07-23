### Added

- `docs/cc-community/CC-multi-account-switching-landscape.md`: multi-account/profile switching for CC — native `CLAUDE_CONFIG_DIR` mechanism (first-party-verified: documented only in the debug-your-config guide; per-platform credential isolation — Linux/Windows per-dir, macOS Keychain carries over), tool table (claude-swap, claude-code-profiles, claude-multiprofile, claude-multisession), disambiguation vs CC Switch (provider mgmt) and CLIProxyAPI (gateway quota harvesting).
- `docs/plans/2026-07-23-corpus-update-new-sources.md`: durable plan for the 2026-07-23 corpus-update + new-sources arc (backlog drain #374, fresh mining, stale-fact refresh cohort).

### Changed

- `docs/cc-native/configuration/CC-env-vars-reference.md`: added `CLAUDE_CONFIG_DIR` (verified zero-coverage gap; noted its absence from the official env-vars list as of 2026-07-23) + cross-ref to the new landscape.
- `docs/cc-native/configuration/CC-model-provider-configuration.md`: CLIProxyAPI entry now disambiguates gateway-level multi-account from native CLI multi-account sessions.
- `.claude/skills/adding-research-source/scripts/batch-sources.workflow.js`: tolerate args delivered as a JSON-encoded string (harness stringification made the workflow no-op).
