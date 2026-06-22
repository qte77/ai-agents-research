### Added

- `docs/cc-community/CC-research-agents-landscape.md` + `CC-memory-tooling-landscape.md`: **`## Sources` tables** — added the CONTRIBUTING-mandated Sources section to both landscape docs. `CC-research-agents` converted ~45 inline body links to reference-style + a Sources table; `CC-memory-tooling` wraps its existing reference definitions in a Sources table.

### Changed

- `CONTRIBUTING.md`: **rxiv dispatch serialization note** in Auto-generated content — never fire two same-day `rxiv-paper-eval` dispatches concurrently (the date-stamped `chore/rxiv-paper-triage-<date>` branch collides; the second push is rejected). Cross-refs upstream `gha-rxiv-paper-eval#71`.
