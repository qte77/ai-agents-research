---
title: Plugin-source aar's rules + merge CodeBurn optimize disciplines
status: draft
issue: none
created: 2026-06-11
updated: 2026-09-23
---

**Status**: Reference (plan)

Two coupled enhancements, first captured as a local session handoff on 2026-06-11 (merged here
2026-09-23): (1) make `ai-agents-research` (aar) consume its rules from `claude-code-plugins` instead of
its own `.claude/rules/`; (2) merge CodeBurn's [`optimize`][codeburn] disciplines into the best-fit
plugin(s). **No tracking issue exists yet** — open one before executing (plans are not the backlog).

## Current status (verified 2026-09-23)

- **Not shipped.** `claude-code-plugins/.claude/rules/` has compound-learning, context-management,
  core-principles, plugin-versioning, skill-authoring — **no `read-discipline.md`**; the
  `workspace-setup` plugin symlinks only three of those. aar's `.claude/settings.json` does not enable
  `workspace-setup`.
- **Next, in order:** confirm scope with the owner (OPEN below) → PR 1 (claude-code-plugins) → PR 2 (aar).
- **Owner gates:** scope choice; merges (signed-commit ruleset → owner `gh pr merge --admin --squash --delete-branch`).
- **Re-verify before executing:** the rule-drift facts below are from 2026-06-11 and have likely moved.

## Source map

- Plugins (source of truth): `/workspaces/qte77/claude-code-plugins`.
- Consumer: `/workspaces/qte77/ai-agents-research` (`.claude/rules/`).
- CodeBurn optimize source: [getagentseal/codeburn#optimize][codeburn].

### How the plugin rules work (verified 2026-06-11)

- **SoT = `claude-code-plugins/.claude/rules/`** (real files).
- `workspace-setup/rules/` and `workspace-sandbox/rules/` are **symlinks** →
  `../../../.claude/rules/<name>.md`, so both plugins' rule layers stay identical.
- `make sync` (`sync_rules`) is a **no-op** (symlinks auto-reflect SoT); `make check_sync` verifies.
  Adding a rule = add the SoT file + symlink it into both plugins.
- `workspace-setup` deploys `rules/*.md → .claude/rules/` via a SessionStart hook
  (**copy-if-not-exists**) and ships a **read-once PreToolUse hook** — CodeBurn's "re-read files"
  pattern, already implemented.
- The two plugins differ ONLY in settings (base vs sandbox), setup script and metadata
  (`plugin.json`, `README.md`, `hooks/hooks.json`).

### Rule drift, aar vs plugin SoT (as of 2026-06-11 — re-check)

- `context-management.md`: identical.
- `core-principles.md`: differ — plugin more current (AHA + Clarity); aar uniquely names
  "Prevent Incoherence" + "Resolve Ambiguity".
- `compound-learning.md`: differ — plugin canonical (plugin-promotion model incl. `make sync` +
  version bump); aar's is stale.
- `read-discipline.md`: unique to aar; already reframed for a docs corpus + cites CodeBurn `#optimize`.
  **This is the artifact to migrate.**

## Decisions made

- **CodeBurn is mostly diagnostic.** Only read:edit + re-read + lean-instruction-files translate to
  agent rules; the rest (unused MCP, ghost skills, session cost) is CodeBurn the tool's job, not
  always-loaded rules.
- **read-discipline → `workspace-setup` + `workspace-sandbox`** (SoT + symlinks), backed by the
  existing read-once hook.
- **docs-governance earns ONE pattern:** "keep context-loaded instruction files lean" → a line in
  `enforcing-doc-hierarchy`.
- **`BASH_MAX_OUTPUT_LENGTH`** default → `workspace-setup/settings/settings-base.json` (optional).
- **aar adopts the plugin's canonical core-principles + compound-learning.** Optional: fold aar's
  "Prevent Incoherence"/"Resolve Ambiguity" into SoT core-principles.

## OPEN — confirm with the owner before implementing

- **Scope:** (a) minimal = read-discipline only; (b) + docs-governance "lean files" line;
  (c) + `BASH_MAX_OUTPUT_LENGTH` settings default; (d) + a cc-meta "audit-setup-waste" skill mirroring
  `codeburn optimize`. **Default: (a).**
- Whether to include the optional core-principles enhancement. **Default: no.**

## Implementation

### PR 1 — claude-code-plugins

1. Add `read-discipline.md` to SoT `.claude/rules/` (content from aar's `.claude/rules/read-discipline.md`).
2. Symlink into both plugins:
   `ln -s ../../../.claude/rules/read-discipline.md plugins/workspace-setup/rules/read-discipline.md`
   (same for `workspace-sandbox`).
3. `make check_sync` + `make lint_md` (or `make validate`).
4. **Bump `version`** in both plugins' `.claude-plugin/plugin.json` AND root
   `.claude-plugin/marketplace.json` — entries must match (SoT `plugin-versioning.md` rule).
5. Update `workspace-setup/README.md` deployed-rules list.
6. (if scoped) docs-governance `enforcing-doc-hierarchy` line and its version bump; settings-base
   BASH default and its version bump.
7. Open the PR.

### PR 2 — ai-agents-research

1. Add `workspace-setup` to `.claude/settings.json` `enabledPlugins`.
2. Remove the local `.claude/rules/` copies the plugin will own, so the SessionStart hook deploys the
   canonical versions (copy-if-not-exists won't overwrite).
3. Verify on a fresh session that the hook deploys the rules + the read-once hook.

## Remaining work

| # | Item | Gate | Done-when |
|---|---|---|---|
| 1 | Open a tracking issue; confirm scope (default a) | owner | Issue exists, scope recorded in it |
| 2 | PR 1 — read-discipline into plugin SoT + symlinks + version bumps | agent | PR open, `make check_sync` + `make validate` green |
| 3 | PR 2 — enable `workspace-setup` in aar, drop superseded local rules | agent | Fresh session deploys the rules + read-once hook |
| 4 | Merge both PRs | owner | Merged |

## Gotchas

- aar `main` requires signed commits; the sandbox can't sign → owner `gh pr merge --admin --squash --delete-branch`
  (rebase merges disabled). Check whether `claude-code-plugins` has the same ruleset before pushing (unverified).
- Prefix gh/git with `env -u GH_TOKEN -u GITHUB_TOKEN` (invalid env tokens shadow the stored credential).
- Plugin version must match between `plugin.json` and `marketplace.json` or CI fails.
- Never edit a plugin `rules/*.md` directly — they are symlinks; edit the SoT `.claude/rules/`.
- Lint: aar uses `make lint` (markdownlint-cli2 + lychee); the plugins repo uses `make lint_md` / `make validate`.

## Sources

| Source | Content |
|---|---|
| [CodeBurn optimize][codeburn] | Token-waste patterns the disciplines come from |
| Local session handoff, 2026-06-11 | Original notes (merged here, local copy removed) |
| Repo inspection, 2026-09-23 | Current-status check of both repos |

[codeburn]: https://github.com/getagentseal/codeburn#optimize
