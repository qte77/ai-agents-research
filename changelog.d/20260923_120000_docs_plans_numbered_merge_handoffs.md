### Added

- `docs/plans/2026-09-23-0008-backlog-triage-prs-issues.md`: read-only triage of all open PRs, branches and issues (29 PRs, 10 issues) with a single remaining-work table (gate + done-when per row).
- `docs/plans/2026-06-11-0001-plugin-rules-codeburn-merge.md`: the untracked 2026-06-11 plugin-rules/CodeBurn handoff promoted to a plan, with a 2026-09-23 status check (not shipped yet).

### Changed

- `docs/plans/`: files renamed to `YYYY-MM-DD-NNNN-<slug>.md` (0001–0008, creation order); convention and index updated in `docs/plans/README.md`, inbound links repointed (`AGENT_LEARNINGS.md`, `.github/scripts/lib/doc_status.py`).

### Removed

- `docs/handoffs/`: the three handoffs were merged into their plans (0003 status migration, 0005 source expansion, 0006 graphify rebuild) — plans now carry their own onboarding. Dropped the `.claude/handoffs/` `.gitignore` entry.
