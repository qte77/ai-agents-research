### Changed

- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: the effort-vs-cache "two statements"
  are reconciled — Claude Code's gateway guide documents that CC sends per-turn effort as
  `output_config.effort` on `role: "system"` entries (the API's per-message-effort exception, beta
  `mid-conversation-output-config-2026-07-01`).
- `docs/cc-native/configuration/CC-fast-mode-analysis.md`: platform lists reconciled (Google Cloud's
  Agent Platform is the Google-managed product, not the Anthropic-managed one; Foundry fast mode is
  API-only, not in Claude Code); Opus 4.8 fast mode deprecated 2026-10-30, removal 2026-11-30; both
  pages now label Opus 5.5 available; Ultra plan name; status `available`.
- `docs/cc-native/configuration/CC-advisor-tool-analysis.md`: platform "conflict" resolved (Claude Code
  disables the advisor on Claude Platform on AWS; the API page dropped its not-available sentence);
  compatibility table is 12 entries / 14 models; Haiku 5.5 is an accepted advisor; Haiku 4.5's
  executor-only role is stated in the Claude Code docs.
