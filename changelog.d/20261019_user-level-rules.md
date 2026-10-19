### Removed

- `.claude/rules/context-management.md`, `compound-learning.md`, `core-principles.md`: the shared
  estate rules now load once, at user level, from `~/.claude/rules/` symlinked to the
  claude-code-plugins rules SoT (plan 0001). Repo sessions on this machine loaded them up to four
  times, in three versions of core-principles.

### Changed

- `AGENTS.md`: the Rules line says where the shared rules come from, and that cloud, GHA and
  other-machine sessions don't get them.
- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: the context-management link points
  at the plugins SoT.
