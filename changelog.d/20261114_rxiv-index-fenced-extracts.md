### Fixed

- `.github/scripts/build-rxiv-index.py`: recover paper summaries, methods and findings that the triage action dropped into `_raw` since 2026 W26 (the extraction model wraps its JSON in a ```json fence, which the action's strict parser rejects). The cumulative index now shows summaries for 1,162 of 1,919 papers (was 53). Replies cut off at the token limit or with invalid JSON stay empty.
