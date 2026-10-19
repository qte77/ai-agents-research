---
title: One copy per rule — user-level rules from the claude-code-plugins SoT + CodeBurn read discipline
status: approved
issue: "#452"
created: 2026-06-11
updated: 2026-10-19
---

First captured as a local session handoff on 2026-06-11 (merged here 2026-09-23). The original goal was
(1) to source aar's rules from `claude-code-plugins` instead of its own `.claude/rules/`, and (2) to
merge CodeBurn's [`optimize`][codeburn] disciplines into the best-fit plugin. **Redesigned 2026-10-19
by the owner:** every shared rule loads **once, at user level**, from `~/.claude/rules/` symlinked into
the versioned `claude-code-plugins/.claude/rules/` SoT. Repos keep only rules specific to themselves.
Tracking issue: [#452][issue].

## Current status (2026-10-19)

- **Done (phase 1, not yet merged):**
  - `~/.claude/rules/` (= `/workspaces/.claude-files/rules/`) holds symlinks to the SoT for
    context-management, compound-learning, core-principles and unattended-execution.
  - The duplicate copies in `/workspaces/.claude/rules/` and `/workspaces/qte77/.claude/rules/` are
    deleted.
  - [#689][pr689] removes aar's three copies.
  - A fresh session (CC 2.1.303) loads each rule once: the 4 SoT symlinks, plus external-input,
    claim-verification, documentation-hierarchy and read-discipline from their current homes.
- **Open PRs:** [claude-code-plugins#251][pr1] (adds read-discipline, external-input,
  claim-verification to the SoT) · [#688][pr688] (canonical marketplace key) · [#689][pr689] · this
  plan's PR.
- **Next, in order:** owner merges → row 4 (phase 2) → row 6 (corpus update). Row 5 waits on a
  gha-issue-triage change.
- **Backup** of every rules folder, CLAUDE.md/AGENTS.md and settings file before the change:
  `/workspaces/temp/claude-config-backup-2026-10-19/` (none of these folders are in git).

## Source map

- Rules SoT: `/workspaces/qte77/claude-code-plugins/.claude/rules/` (local clone; user-level rules follow
  **whatever that clone has checked out** — do branch work there only in worktrees).
- User rules: `~/.claude/rules` → `/workspaces/.claude-files/rules/` (per-file symlinks; don't link
  the folder — ci-status-checks, plugin-versioning and skill-authoring must not load everywhere).
- Stays in place: `/workspaces/qte77/.claude/rules/documentation-hierarchy.md` (qte77-only scope,
  owner 2026-10-19).
- aar: `.claude/rules/read-discipline.md` (until row 4), `AGENTS.md:16` (Rules line),
  `CLAUDE.md` → symlink to `AGENTS.md`.
- Issue triage reads `README.md` + `CLAUDE.md` from the checkout: `qte77/gha-issue-triage`
  `src/relevance.py` `_load_repo_context()`.
- CodeBurn optimize source: [getagentseal/codeburn#optimize][codeburn].

### Verified behaviour (CC 2.1.303, Codespaces, 2026-10-19)

- **Observed, not documented:** `.claude/rules/` in parent folders (`/workspaces`, `/workspaces/qte77`)
  load into repo sessions. The [memory docs][cc-mem] name only the project's and `~/.claude/rules/`.
- **Observed:** a symlink in `~/.claude/rules/` pointing outside the working directory loads with no
  approval prompt in a headless run.
- **Documented** ([settings][cc-settings]): `.claude/settings.json` is read from the session's primary
  working directory; parent-folder settings files are not used in repo sessions.
- **Documented** ([memory][cc-mem]): CC v2.1.277+ reads `AGENTS.md` natively, but "only when you have
  no `CLAUDE.md` in your working directory or above it", and then loads every `AGENTS.md` in the
  working directory and above.

## Decisions made

- **CodeBurn is mostly diagnostic.** Only read:edit + re-read + lean-instruction-files translate to
  agent rules. Scope (a) only (owner, 2026-10-19): read-discipline.
- **One home per shared rule: `~/.claude/rules/` as symlinks into the plugins SoT** (owner,
  2026-10-19). This replaces the original PR 2 (enable `workspace-setup` in aar), which would have put
  per-repo copies back.
- **Consequence:** cloud sessions, GHA runs and other machines don't get user-level rules.
- **Shared rules follow the plugin SoT text** (core-principles, compound-learning).
- **documentation-hierarchy stays in `/workspaces/qte77/.claude/rules/`** (qte77-only scope).
- **external-input and claim-verification** go into the SoT unchanged (SoT-only; no plugin deploys them).
- **AGENTS.md-only:** approved, but gated on row 5.

## Remaining work

| # | Item | Gate | Done-when |
|---|---|---|---|
| ~~1~~ | ~~Open a tracking issue; confirm scope (default a)~~ | owner | Done: #452 (2026-09-23); scope (a) confirmed 2026-10-19 |
| ~~2~~ | ~~PR 1 — read-discipline (+ external-input, claim-verification) into the plugin SoT~~ | agent | Done 2026-10-19: [claude-code-plugins#251][pr1]; `make check_sync`/`validate`/`lint_md` green |
| 3 | Merge claude-code-plugins#251 (plain `--squash`), #688, #689 and this plan's PR (`--admin`) | owner | Merged |
| 4 | Phase 2: `git pull --ff-only` the plugins clone, symlink read-discipline, external-input and claim-verification into `~/.claude/rules/`, delete `/workspaces/.claude/rules/{external-input,claim-verification}.md`, then a PR in aar that deletes `.claude/rules/read-discipline.md` and repoints its links (`AGENT_LEARNINGS.md:66` and the `/workspaces/.claude/rules/` path in its first entry) | agent | Fresh headless session lists each rule exactly once |
| 5 | AGENTS.md-only: make gha-issue-triage `_load_repo_context()` fall back to `AGENTS.md`; then delete `/workspaces/AGENTS.md` + `/workspaces/qte77/AGENTS.md` (check no repo under `/workspaces` relies on them) and aar's `CLAUDE.md` symlink. **Default:** gha-issue-triage PR first | agent (owner merges) | Fresh session loads aar's AGENTS.md once; triage still gets repo context |
| 6 | Corpus: add the verified behaviour above to `CC-memory-system-analysis.md` (parent rules observed, AGENTS.md native read, settings precedence — fixes `CC-tools-inventory.md:240` "Precedence unclear") | agent | Doc PR merged, lint + lychee green |
| 7 | Parent settings files `/workspaces/.claude/settings*.json` and `/workspaces/qte77/.claude/settings*.json` are used only when CC starts in those folders. **Default:** keep | owner | Keep/delete recorded in #452 |

## Gotchas

- aar `main` requires signed commits; the sandbox can't sign → owner `gh pr merge --admin --squash --delete-branch`.
- `claude-code-plugins` `main` also requires signatures but has **no bypass actors**; GitHub's squash
  commit is verified, so a plain `gh pr merge --squash` works (no `--admin`). Required check: CodeFactor.
- Prefix gh/git with `env -u GH_TOKEN -u GITHUB_TOKEN` (invalid env tokens shadow the stored credential).
- Plugin version must match between `plugin.json` and `marketplace.json` or CI fails.
- Never edit a plugin `rules/*.md` directly — they are symlinks; edit the SoT `.claude/rules/`.
- Lint: aar uses `make lint` (markdownlint-cli2 + lychee); the plugins repo uses `make lint_md` / `make validate`.

## Sources

| Source | Content |
|---|---|
| [CodeBurn optimize][codeburn] | Token-waste patterns the disciplines come from |
| [CC memory docs][cc-mem] | Rules locations, symlinks, AGENTS.md native read (v2.1.277+) |
| [CC settings docs][cc-settings] | Settings scopes and precedence |
| [#452][issue] | Tracking issue |
| Local session handoff, 2026-06-11 | Original notes (merged here, local copy removed) |
| CC 2.1.303, Codespaces, 2026-10-19 | Headless probe + loaded-rules listing (observations above) |

[codeburn]: https://github.com/getagentseal/codeburn#optimize
[cc-mem]: https://code.claude.com/docs/en/memory
[cc-settings]: https://code.claude.com/docs/en/settings
[issue]: https://github.com/qte77/ai-agents-research/issues/452
[pr1]: https://github.com/qte77/claude-code-plugins/pull/251
[pr688]: https://github.com/qte77/ai-agents-research/pull/688
[pr689]: https://github.com/qte77/ai-agents-research/pull/689
