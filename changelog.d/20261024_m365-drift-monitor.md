### Added

- `.github/workflows/m365-drift-monitor.yaml` + `.github/scripts/m365-drift-monitor.py` +
  `.github/scripts/lib/m365_drift.py`: weekly monitor that checks the Microsoft Learn pages cited
  by the Microsoft 365 Copilot doc for an `ms.date` change or a vanished stored quote, upserting a
  single `m365-drift` tracking issue for a human to triage (#705). Watch list + last-seen state in
  `.github/state/m365-drift-state.json`; refreshed state commits via the shared `create-triage-pr`
  action, same as the other state-backed monitors.
