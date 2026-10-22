### Added

- `docs/non-cc/coding-agents/goal-loops-landscape.md`: goal loops across coding agents — `/goal` in
  Codex, Antigravity, Kiro, Copilot CLI and Cursor, VS Code Advanced Autopilot, and Stop-style hooks
  in Codex, Copilot CLI, Antigravity, Devin, Cursor and Amp. Compares who judges completion (a
  separate model in Claude Code and VS Code; the agent itself in Codex, Antigravity and Kiro; not
  stated for Cursor and Copilot) and the bounds. Every cell fetched first-party and re-checked by an
  adversarial pass, 2026-10-22.
- `docs/cc-native/sessions/CC-goal-analysis.md`: "Offloading and Batch Runs" — `claude -p` starts in
  Manual mode from v2.1.302, so an unattended goal needs a permission mode; exit codes don't separate
  met/impossible/bounded; one goal per process for batches; cloud sessions and routines don't mention
  `/goal`; Anthropic's explore → spec → `/goal` guidance.

### Changed

- `docs/non-cc/README.md`, `docs/_topics/long-running.md`: index rows for the new landscape.
