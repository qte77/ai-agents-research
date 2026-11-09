### Added

- `make reconcile` (`.github/scripts/plan-reconcile.py`, `.github/scripts/lib/plan_reconcile.py`,
  `tests/test_plan_reconcile.py`, 13 tests): reads the newest plan's remaining-work table, looks up
  every cited PR/issue in any repo through `gh`, and flags open rows whose PRs are all merged/closed,
  struck rows with an open reference, and references it could not check. References in backticks are
  treated as context. Documented in `CONTRIBUTING.md`; plan 0012's "How to run it" now starts with it.
- `AGENT_LEARNINGS.md`: the stale-gate recurrence (D0/C1 merged 2026-10-24, read as blocked until
  2026-11-09) and the update-branch-before-merge pattern.

### Changed

- `docs/plans/2026-10-10-0012-decision-models-estate.md`: cross-repo references made explicit
  (C1, P2, Q1), history references marked as context; R10 struck (qte77/qte77 commits verified since
  2026-11-02).
