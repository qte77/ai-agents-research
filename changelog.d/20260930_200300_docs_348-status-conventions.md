### Changed

- `CONTRIBUTING.md` §1–§2: doc status lives only in frontmatter `status:`. §2 "Status Badge" is replaced by "Frontmatter status", which points to `VOCAB` in `.github/scripts/lib/doc_status.py` as the one list of tokens. Extra detail goes on a `**Details:**` line (#348).
- `Makefile` `check_status`: now runs `--strict`, so CI (`lint.yaml`) fails on any body `**Status**:` badge.
- `docs/architecture.md` "Frontmatter Conventions": now points to CONTRIBUTING §1–§2 instead of keeping its own copy, which had drifted (`description:` vs `purpose:`).
- `.claude/skills/adding-research-source`: writes `status:` in frontmatter instead of a badge.
- `docs/plans/2026-07-05-0003-status-frontmatter-migration.md`: marked done.
