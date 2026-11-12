### Fixed

- `.github/scripts/community-monitor.py`, `.github/scripts/lib/monitor_utils.py`: a source whose
  credentials are unset (Reddit, X) is now listed as skipped, with the missing variables, in the
  report and the triage PR, instead of showing as a source that returned nothing. The workflow
  writes the report to the run summary and adds a warning annotation per skipped source (#726).
