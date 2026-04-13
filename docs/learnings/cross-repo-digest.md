---
title: Cross-Repo Pattern Digest
description: Recurring operational patterns identified across multiple qte77 repos — GitHub API, CC sandbox, CI tooling, release management.
created: 2026-03-27
updated: 2026-03-27
---

## Cross-Repo Pattern Digest

Patterns that recur across two or more repos. Each entry is distilled from AGENT_LEARNINGS.md files. Full entries live in the source repos; this is the canonical cross-cutting reference.

---

## GitHub API & CLI

### `gh pr edit` Broken — Use GraphQL

- **Context**: Editing PR title or body via GitHub CLI
- **Problem**: `gh pr edit` exits with GraphQL error about Projects (classic) deprecation even for unrelated edits.
- **Solution**: Use GraphQL mutation directly via `gh api graphql -f query="mutation { updatePullRequest(...) }"`.
- **Example**: `PR_ID=$(gh pr view NUM --json id --jq '.id')` then GraphQL `updatePullRequest` mutation.
- **References**: AGENT_LEARNINGS.md (Agents-eval, ralph-template)

### PR Squash Merge Requires Both Title and Message

- **Context**: Merging PRs via GitHub API (`gh api repos/.../pulls/NUM/merge`)
- **Problem**: `commit_title` alone drops all branch commit messages from the squash body.
- **Solution**: Pass both `commit_title` (`PR <title> (#NUM)`) and `commit_message` (branch commit log).
- **Example**: `-f commit_message="$(git log origin/main..HEAD --format='* %s')"`
- **References**: AGENT_LEARNINGS.md (Agents-eval), ralph/docs/LEARNINGS.md

### GitHub API Enum Values Use Spaces Not Underscores

- **Context**: GitHub REST API enum parameters (e.g., `dismissed_reason` for code scanning)
- **Problem**: `-f dismissed_reason=false_positive` returns HTTP 422.
- **Solution**: Use space-separated values: `-f "dismissed_reason=false positive"`.
- **References**: AGENT_LEARNINGS.md (Agents-eval)

---

## Git Operations

### `-X ours` Does Not Delete Files Added by Theirs

- **Context**: `git merge -X ours` or `git rebase -X ours` strategy option
- **Problem**: The strategy option keeps *our* content for conflicts but does not delete files that only exist in theirs.
- **Solution**: After merge, manually delete unexpected files or use `git checkout --ours -- <path>` per-file.
- **References**: AGENT_LEARNINGS.md (Agents-eval), ralph/docs/LEARNINGS.md section 4

### Dependabot Rebase Fails with GPG Signing Mismatch

- **Context**: Rebasing dependabot PRs when GPG signing is required on main
- **Problem**: `git rebase` fails — dependabot commit author doesn't match GPG signing identity.
- **Solution**: Close the PR, create a fresh branch from main, apply the change manually, open new PR.
- **References**: AGENT_LEARNINGS.md (Agents-eval, gha-github-mirror-action)

---

## Claude Code Sandbox

### CC Sandbox Blocks `.claude/skills/` Writes

- **Context**: Any git or Bash operation touching `.claude/skills/` paths in CC sessions
- **Problem**: `.claude/skills/` is write-denied in the Bash sandbox. Git reset/stash/pull fail with "Read-only file system".
- **Solution**: Use Edit/Write tools for skill file changes; run git from a non-sandboxed terminal.
- **References**: AGENT_LEARNINGS.md (Agents-eval), MEMORY.md

### `claude -p` Inherits Sandbox — `.git` Read-Only

- **Context**: Running `claude -p` (headless/print mode) from within a CC session
- **Problem**: `.git` is read-only in inherited sandbox; `git commit` fails inside subprocesses.
- **Solution**: Run Ralph and `claude -p` from an independent terminal outside the CC sandbox.
- **References**: AGENT_LEARNINGS.md (Agents-eval), MEMORY.md

### CC Teams Artifacts Ephemeral in Print Mode

- **Context**: Running `claude -p` and expecting `~/.claude/teams/` artifacts afterward
- **Problem**: `~/.claude/teams/` and `~/.claude/tasks/` are empty after `claude -p` completes.
- **Solution**: Parse `raw_stream.jsonl` for `TeamCreate`/`Task`/`TodoWrite` events instead of filesystem artifacts.
- **References**: AGENT_LEARNINGS.md (Agents-eval), ADR-008

### CC OTel Exports Metrics/Logs Only — No Trace Spans

- **Context**: Configuring `OTEL_*` env vars in `.claude/settings.json` for CC observability
- **Problem**: CC OTel exports only metrics and logs — no distributed trace spans despite documentation suggesting otherwise.
- **Solution**: Use artifact collection (`CCTraceAdapter` / `raw_stream.jsonl`) for trace-level analysis; OTel for cost/token dashboards only.
- **References**: AGENT_LEARNINGS.md (Agents-eval), upstream issues #9584 and #2090

---

## CI / GitHub Actions

### CodeQL `actions` Language for Bash/GHA Repos

- **Context**: CodeQL workflow in repos with only bash scripts and GHA YAML (no JS/Python)
- **Problem**: `languages: javascript-typescript` triggers "detected GitHub Actions, but not JS/TS" error.
- **Solution**: Use `languages: actions`; remove the `autobuild` step (not needed for actions analysis).
- **References**: AGENT_LEARNINGS.md (Agents-eval, gha-github-mirror-action)

### BATS Tests Need Git Identity in CI

- **Context**: BATS tests creating temporary git repos and running `git commit`
- **Problem**: CI runners lack `user.name`/`user.email` git config; `git commit` fails.
- **Solution**: Add `git config --global user.name "test"` and `user.email "test@test"` in BATS `setup()`.
- **Also**: Use `$BATS_TEST_NUMBER` not `$$` for unique temp dir names.
- **References**: AGENT_LEARNINGS.md (Agents-eval, gha-github-mirror-action)

### PAT Scrubbing in Shell Scripts (Defense in Depth)

- **Context**: Shell scripts handling PATs and running `git push` with authenticated URLs
- **Problem**: `::add-mask::` only works inside GitHub Actions; PATs leak elsewhere.
- **Solution**: Wrap script body in `_main()`, pipe all output through `sed "s|$PAT|***|g"`. Use `PIPESTATUS[0]` to preserve exit code.
- **References**: AGENT_LEARNINGS.md (Agents-eval, gha-github-mirror-action)

---

## Release & Versioning

### First Release Bootstrap for `bump-my-version` Repos

- **Context**: New repo with `pyproject.toml` version already at target (e.g., `0.1.0`)
- **Problem**: `bump-my-version` always increments — no "tag current version" mode.
- **Solution**: Create first release manually via GitHub API (tag + release + floating major tag), then let bump-my-version handle subsequent releases.
- **References**: AGENT_LEARNINGS.md (Agents-eval, gha-github-mirror-action)

### Plugin/Package Version Must Be Synced Across Manifest Files

- **Context**: Multi-manifest systems (CC plugins: `plugin.json` + `marketplace.json`)
- **Problem**: Bumping version in one manifest but not the other causes CI validation failures.
- **Solution**: Grep for old version string across all manifest files and update all occurrences atomically.
- **References**: AGENT_LEARNINGS.md (Agents-eval, claude-code-plugins)

---

## Python / uv Toolchain

### `uv exclude-newer` Silently Blocks Dependency Resolution

- **Context**: Upgrading a dependency with `uv lock --upgrade-package` when `pyproject.toml` has `[tool.uv] exclude-newer`
- **Problem**: Package exists on PyPI but uv resolves to an older version with no error — package was uploaded after the cutoff date.
- **Solution**: Check and update `exclude-newer` date before debugging cache, index, or version constraints.
- **References**: AGENT_LEARNINGS.md (Agents-eval)

---

## Shell Scripting

### Shell Keyword Collision in `jq` Arguments (SC1010)

- **Context**: Bash scripts calling `jq` with `--argjson` using shell keywords as variable names
- **Problem**: `--argjson done "$var"` triggers ShellCheck SC1010 because `done` is a shell keyword.
- **Solution**: Avoid shell keywords (`done`, `then`, `fi`, `do`, `esac`) as jq variable names; use descriptive names.
- **References**: AGENT_LEARNINGS.md (Agents-eval), ralph/scripts/ralph.sh

### Pipe-into-While Loses Variable Assignments (Bash Subshell)

- **Context**: Bash `while read` loops processing multi-line variables
- **Problem**: `echo "$var" | while read -r line; do found=true; done` — pipe creates subshell; `found` never propagates.
- **Solution**: Use here-string: `while read -r line; do ...; done <<< "$var"` to keep loop in current shell.
- **References**: AGENT_LEARNINGS.md (Agents-eval), ralph/scripts/lib/snapshot.sh (ShellCheck SC2031)
