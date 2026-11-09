### Fixed

- `docs/cc-native/configuration/CC-env-vars-reference.md`: configuration precedence was wrong —
  environment variables aren't a settings level, `--settings` is the only command-line level, and a
  settings `env` block overrides the same variable exported in the shell in most sessions; listed the
  variables project/local files can't set. `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` no longer claims a
  documented ~95 % default.
- `docs/cc-native/examples/settings.json`: eight `Bash(git:<sub>:*)` rules matched nothing (`:*` works
  only at the end of a pattern) — including the `git push` deny and `git commit` ask; rewritten as
  `Bash(git push *)` etc., read-only git allows dropped (built-in read-only set).
- `docs/cc-native/configuration/CC-bash-mode-analysis.md`, `docs/cc-native/sandboxing/CC-permissions-bypass-analysis.md`:
  stopped recommending `Bash(git *:*)` / `Bash(git *)` / `Bash(make *)`; the permissions docs say to put
  the `*` after the subcommand (a leading `*` also matches injected options such as `git -c`).
- `docs/cc-native/configuration/CC-tools-inventory.md`: "Precedence unclear" answered for
  `respectGitignore`; the `fastMode` `.claude.json` cell and the VS Code key marked unverified.
- `CC-remote-control-analysis.md`, `CC-model-provider-configuration.md`: `.claude/settings.local.json`
  isn't automatically gitignored when created by hand; three dead settings-page anchors repointed.
- `docs/cc-native/sessions/CC-print-mode-gotchas.md` (observation, 2026-10-29): strip
  `GH_TOKEN`/`GITHUB_TOKEN` per `gh`/git network call, not for the whole `claude -p` process — the
  Codespaces commit signer needs `GITHUB_TOKEN`.
