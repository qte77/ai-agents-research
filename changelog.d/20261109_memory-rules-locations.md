### Changed

- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: rules in parent folders load in practice
  but are undocumented (observed CC 2.1.303); symlinked rules outside the working directory are
  documented as external imports needing approval, with an observed headless exception for
  `~/.claude/rules/`; project settings files are read from the working directory (local file: git
  root). Plan 0001 row 6 done.
