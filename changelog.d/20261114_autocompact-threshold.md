### Changed

- `.claude/settings.json`: set `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` to 60, so long research and PR/CI sessions compact earlier with room left for reasoning and recovery.

### Fixed

- `docs/cc-native/examples/statusline.sh`: check that `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` is numeric and pass it to awk with `-v`, instead of interpolating the env var into the awk program.
