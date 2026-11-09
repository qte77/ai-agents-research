### Added

- `.github/workflows/plan-reconcile-monitor.yaml`: weekly `make reconcile` (Monday 14:00 UTC) that
  opens or updates a single `plan-drift` issue while any row of the newest plan disagrees with the
  live state of the PRs/issues it cites, and closes it once every row agrees. A failed `gh`
  preflight fails the job instead of filing an issue. Documented in `docs/architecture.md`,
  `AGENT_LEARNINGS.md` and plan 0012.
