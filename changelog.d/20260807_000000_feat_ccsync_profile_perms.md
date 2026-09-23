### Added

- `scripts/cc-multi-account.sh`: `ccsync <profile>` / `ccsync --all` (and `./cc-multi-account.sh sync <profile>`) re-applies the shared `~/.claude/settings.json` to per-account profiles, keeping per-profile UI keys (`CC_PROFILE_KEEP`), backing up to `settings.json.bak`, reporting dropped keys, and never touching `.credentials.json`.

### Fixed

- `scripts/cc-multi-account.sh`: profile directories are now `chmod 700` — a default umask left them 755, so other local users could read `history.jsonl` and `projects/` transcripts.
