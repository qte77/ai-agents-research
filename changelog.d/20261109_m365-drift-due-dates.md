### Added

- `.github/scripts/lib/m365_drift.py`, `.github/scripts/m365-drift-monitor.py`: a watched entry may carry
  an optional `due` date (YYYY-MM-DD); the weekly M365 drift monitor now flags it once that date has
  passed, even when the page's `ms.date` and quote are unchanged (the 2026-10-31 retirement went
  unflagged). The state file keeps extra fields across runs (`build_new_state`). Tests in
  `tests/test_m365_drift.py` (8 new). Closes the remaining #705 items.

### Changed

- `.github/state/m365-drift-state.json`: `due` dates on the 2026-11-12 and 2026-12-01 entries; new
  watched quotes for the 2026-11-01 PowerShell retirement and the structured-document-generation GA
  roadmap feed.
- `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: the 2026-10-31, 2026-11-01 and October GA
  timeline rows marked passed, with what the pages said on 2026-11-09 (none confirms the event).
