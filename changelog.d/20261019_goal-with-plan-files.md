### Added

- `docs/cc-native/sessions/CC-goal-analysis.md`: "Pairing `/goal` With a Persistent Task List".
  A durable task list (plan file, backlog, issue queue) holds the work across sessions, and `/goal`
  drives one session through it. Covers how to write the condition (name the file, scope to items
  Claude can finish, make the evidence visible, pick a reachable end state, bound it), failure modes
  (compaction, permission mode, subagents, mid-run list edits, headless runs), and a command Stop
  hook as the deterministic alternative (exit 2 / `decision: "block"`, `stop_hook_active`,
  8-continuation cap). Labelled as a design pattern, not tested.
