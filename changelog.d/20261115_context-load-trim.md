### Changed

- `.claude/settings.json`: drop the project-level `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (60). Project settings override user settings, so it was overriding the owner's user-scope value (50).
- `AGENTS.md`: link `CONTRIBUTING.md` and `AGENT_LEARNINGS.md` instead of `@`-importing them; the imports loaded about 7.4k tokens into every request in this repo.
