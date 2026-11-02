### Fixed

- `.github/scripts/learnings-aggregator.py`: change detection now hashes the upstream
  `AGENT_LEARNINGS.md` instead of the rendered mirror, whose `updated:` date changed every run, so
  the weekly job no longer opens a date-only PR. The first run after this lands rewrites the state
  file once.
