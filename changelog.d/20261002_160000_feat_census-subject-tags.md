### Changed

- Every scored rubric row in `docs/` (75 rows in 25 docs) now carries a `subject:` tag, so `make census` regenerates the reference architecture's evidence matrix from the corpus (plan 0010, T1 part 2).
- `.github/scripts/lib/doc_census.py`: a table takes its nearest `subject:` tag, so two tables under one heading can have different subjects. An inline row ends where the next list item starts, and the first score per property wins.

### Fixed

- `docs/cc-native/plugins-ecosystem/CC-official-plugins-landscape.md`: Code Modernization's Reproducible score goes `yes` → `partial`. The proof step is deterministic, but the analysis and rewrite run as agents with no pinned model (the rubric's "pinned code but unpinned model" case).
