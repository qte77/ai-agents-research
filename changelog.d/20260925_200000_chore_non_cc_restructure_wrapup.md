### Changed

- `CONTRIBUTING.md`, `docs/architecture.md`: directory trees list the 9 `docs/non-cc/<section>/` subdirs.
- `.claude/skills/adding-research-source/SKILL.md`: new non-cc docs go into the `docs/non-cc/<section>/` subdir that matches their README section.

### Removed

- `scripts/restructure_links.py`, `tests/test_restructure_links.py`, `docs/non-cc/.restructure-map.tsv`: one-off #309 Phase 1 move tooling, removed after all 9 moves (#489–#497). Recoverable from commit `7179e0a`.
