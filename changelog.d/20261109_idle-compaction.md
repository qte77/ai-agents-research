### Added

- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: idle compaction — Claude Code compacts
  a 200K+ token session left idle for about 54 minutes before its one-hour prompt cache expires
  (`idleCompaction`, default on, v2.1.290+ setting; feature history 2.1.299–2.1.318 from the
  changelog). New env var row `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS` in `CC-env-vars-reference.md`;
  cross-link from `CC-extended-context-analysis.md`.
