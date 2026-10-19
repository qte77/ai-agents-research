### Added

- `docs/cc-native/sessions/CC-goal-analysis.md`: "Using `/goal` With Plan Files" — the plan file
  as the cross-session north star and `/goal` as the per-session driver. Covers how to write the
  condition (name the file, scope to agent-gated rows, make the evidence visible, use the agent-level
  done-when, bound it), failure modes (compaction, permission mode, subagent lanes, mid-run plan
  edits, headless runs), and a command Stop hook as the deterministic alternative (exit 2 /
  `decision: "block"`, `stop_hook_active`, 8-continuation cap). Labelled as a design pattern, not tested.
