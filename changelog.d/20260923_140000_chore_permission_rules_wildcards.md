### Fixed

- `.claude/settings.json`: removed the six `Bash(git -C * <subcommand> *)` allow rules. A `*` before the subcommand also matches injected git options such as `-c core.fsmonitor=<script>`, so these auto-approved arbitrary command execution. Read-only git needs no allow rule: Claude Code's built-in read-only command set covers it.
