### Changed

- `.claude/settings.json`: allow the read-only `make check_status`, `make check_actions`, `make help`, `make census` and `shellcheck *`, alongside the existing exact make-target rules, so sessions without a local settings file (cloud, CI, other machines) don't prompt for them.
