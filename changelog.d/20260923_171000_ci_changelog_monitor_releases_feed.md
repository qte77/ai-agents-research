### Changed

- `.github/scripts/lib/changelog.py`, `.github/scripts/changelog-compare.py`, `.github/workflows/cc-changelog-monitor.yaml`: the changelog monitor now also fetches `claude-code`'s `releases.atom` to annotate each detected version with its release date and to maintain an id-based dedup ledger in `.github/state/native-monitor-state.json` (key `cc-changelog-releases`); `CHANGELOG.md` remains the sole content source and the scanned-version-range cutoff remains the sole trigger (#410).
