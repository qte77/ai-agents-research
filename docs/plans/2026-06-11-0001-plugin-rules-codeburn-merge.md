---
title: Plugin-source aar's rules + merge CodeBurn optimize disciplines
status: approved
issue: "#452"
created: 2026-06-11
updated: 2026-10-19
---

Two coupled enhancements, first captured as a local session handoff on 2026-06-11 (merged here
2026-09-23): (1) make `ai-agents-research` (aar) consume its rules from `claude-code-plugins` instead of
its own `.claude/rules/`; (2) merge CodeBurn's [`optimize`][codeburn] disciplines into the best-fit
plugin(s). Tracking issue: [#452][issue] (open since 2026-09-23).

## Current status (verified 2026-10-19)

- **Approved 2026-10-19** by the owner ("do it now") with the defaults below: scope (a), no
  core-principles change.
- **PR 1 open:** [claude-code-plugins#251][pr1], CI green, awaiting owner merge (plain `--squash`).
- **PR 2 (aar)** waits on PR 1's merge (its done-when needs the published plugin) and on the owner
  decision in row 5.
- **Owner gates:** row 5 decision; both merges.
- Facts below re-verified 2026-10-19 against `claude-code-plugins` origin/main (`ec8c050`) and aar `main`.

## Source map

- Plugins (source of truth): `/workspaces/qte77/claude-code-plugins`.
- Consumer: `/workspaces/qte77/ai-agents-research` (`.claude/rules/`, `.claude/settings.json`).
- CodeBurn optimize source: [getagentseal/codeburn#optimize][codeburn].
- **Template commit:** `claude-code-plugins` `ec8c050` (#250) added the `unattended-execution` rule
  the same way PR 1 adds `read-discipline` — mirror the files it touched.

### How the plugin rules work (verified 2026-10-19)

- **SoT = `claude-code-plugins/.claude/rules/`** — 7 files: ci-status-checks, compound-learning,
  context-management, core-principles, plugin-versioning, skill-authoring, unattended-execution.
- `plugins/workspace-setup/rules/` and `plugins/workspace-sandbox/rules/` each hold 5 **symlinks** →
  `../../../.claude/rules/<name>.md` (ci-status-checks, compound-learning, context-management,
  core-principles, unattended-execution). plugin-versioning and skill-authoring stay repo-local.
- `make sync_rules` is a no-op; `make check_sync` hardcodes one `test -L` line per rule symlink and
  also curls the qte77 README/CONTRIBUTING canon (needs network; unrelated to rules).
- `workspace-setup` SessionStart hook (`hooks/scripts/setup-workspace.sh`) deploys
  `rules/*.md → .claude/rules/` **copy-if-not-exists**, plus `statusline.sh`, `settings-base.json`
  (if `.claude/settings.json` is missing) and governance files (if missing). It also ships the
  **read-once** PreToolUse (`Read`) + PostCompact hooks — CodeBurn's "re-read files" pattern.
- Versions on origin/main: workspace-setup **1.6.0**, workspace-sandbox **1.4.0**
  (`plugin.json` and `marketplace.json` match, per the repo's `plugin-versioning.md`).

### Rule drift, aar vs plugin SoT (verified 2026-10-19)

- `context-management.md`: identical.
- `core-principles.md`: differs — SoT restructured (AHA, Clarity, "Consistency and coherence");
  aar keeps the old format plus "Prevent Incoherence" + "Resolve Ambiguity".
- `compound-learning.md`: differs — SoT promotes to a plugin's `rules/` via PR (version bump,
  cross-repo PR); aar's promotes to local `.claude/rules/`.
- `read-discipline.md`: unique to aar. Its two repo-relative links and "this repo" wording don't
  carry over, so PR 1 ships a **generalized** version (same four disciplines, CodeBurn link kept).

## Decisions made

- **CodeBurn is mostly diagnostic.** Only read:edit + re-read + lean-instruction-files translate to
  agent rules; the rest (unused MCP, ghost skills, session cost) is CodeBurn the tool's job, not
  always-loaded rules.
- **read-discipline → `workspace-setup` + `workspace-sandbox`** (SoT + symlinks), backed by the
  existing read-once hook.
- **Scope (a) only** (owner, 2026-10-19). Options (b) docs-governance "lean files" line,
  (c) `BASH_MAX_OUTPUT_LENGTH` settings default (aar already sets `15000` locally), and
  (d) an "audit-setup-waste" skill are not pursued.
- **aar adopts the plugin's canonical core-principles + compound-learning**; no SoT
  core-principles change.

## Implementation

### PR 1 — claude-code-plugins (mirror `ec8c050`)

1. Add generalized `read-discipline.md` to SoT `.claude/rules/`.
2. Symlink it into `plugins/workspace-setup/rules/` and `plugins/workspace-sandbox/rules/`.
3. Add two `test -L` lines to `check_sync` in the Makefile.
4. Bump both plugins' `plugin.json` and the matching `marketplace.json` entries (from 1.6.0 / 1.4.0).
5. Update the deployed-rules line in **both** plugin READMEs; add a CHANGELOG `[Unreleased]` entry.
6. `make check_sync` + `make validate` + `make lint_md`; open the PR.

### PR 2 — ai-agents-research

1. Add `"workspace-setup@qte77-claude-code-plugins": true` to `.claude/settings.json` `enabledPlugins`
   (the canonical marketplace name; aar's stale `qte77-claude-code-utils` alias is fixed in #688).
2. Apply the row 5 decision for `.claude/rules/`, removing the local copies the plugin now owns
   (copy-if-not-exists won't overwrite them).
3. Verify on a fresh session that the hook deploys the rules + the read-once hook.

## Remaining work

| # | Item | Gate | Done-when |
|---|---|---|---|
| ~~1~~ | ~~Open a tracking issue; confirm scope (default a)~~ | owner | Done: #452 (2026-09-23); scope (a) confirmed 2026-10-19 |
| ~~2~~ | ~~PR 1 — read-discipline into plugin SoT + symlinks + version bumps~~ | agent | Done 2026-10-19: [claude-code-plugins#251][pr1] open, workspace-setup 1.7.0 / workspace-sandbox 1.5.0, all three make targets + CI green |
| 3 | Merge PR 1 | owner | Merged |
| 4 | PR 2 — enable `workspace-setup` in aar, drop superseded local rules | agent | Fresh session deploys the rules + read-once hook |
| 5 | Decide how aar tracks plugin-deployed rules: enabling `workspace-setup` adds `ci-status-checks.md` + `unattended-execution.md` as untracked files, and deleted local rules come back untracked. **Default:** gitignore the plugin-owned rule files by name (committed copies never refresh under copy-if-not-exists, so they would drift again) | owner | Choice recorded in #452 |
| 6 | Merge PR 2 | owner | Merged |

## Gotchas

- aar `main` requires signed commits; the sandbox can't sign → owner `gh pr merge --admin --squash --delete-branch`.
- `claude-code-plugins` `main` also requires signatures but has **no bypass actors**; GitHub's squash
  commit is verified, so a plain `gh pr merge --squash` works (no `--admin`). Required check: CodeFactor.
- Prefix gh/git with `env -u GH_TOKEN -u GITHUB_TOKEN` (invalid env tokens shadow the stored credential).
- Plugin version must match between `plugin.json` and `marketplace.json` or CI fails.
- Never edit a plugin `rules/*.md` directly — they are symlinks; edit the SoT `.claude/rules/`.
- Lint: aar uses `make lint` (markdownlint-cli2 + lychee); the plugins repo uses `make lint_md` / `make validate`.
- Out of scope: `/workspaces/.claude/rules/` and `/workspaces/qte77/.claude/rules/` hold older copies of
  core-principles and compound-learning that also load into aar sessions.

## Sources

| Source | Content |
|---|---|
| [CodeBurn optimize][codeburn] | Token-waste patterns the disciplines come from |
| [#452][issue] | Tracking issue |
| Local session handoff, 2026-06-11 | Original notes (merged here, local copy removed) |
| Repo inspection, 2026-09-23 and 2026-10-19 | Current-status checks of both repos (`claude-code-plugins` origin/main `ec8c050`, rulesets API) |

[codeburn]: https://github.com/getagentseal/codeburn#optimize
[issue]: https://github.com/qte77/ai-agents-research/issues/452
[pr1]: https://github.com/qte77/claude-code-plugins/pull/251
