### Fixed

- `.github/scripts/lib/status_incidents.py`, `.github/workflows/cc-status-monitor.yaml`: the status monitor read `status.anthropic.com`, which has answered the weekly run with HTTP 403 since 2026-08-24, and the step swallowed the error, so 12 runs went green without collecting anything. It now reads `status.claude.com` (same Statuspage API) and fails the run on any collector error.
