---
title: Ralph Template Learnings
description: Ralph-specific patterns from qte77/ralph-loop-cc-tdd-wt-vibe-kanban-template — shell scripting, prd.json, self-evolving loop, git strategy.
created: 2026-03-27
updated: 2026-03-27
source: https://github.com/qte77/ralph-loop-cc-tdd-wt-vibe-kanban-template
---

## Ralph Template Learnings

Patterns from [qte77/ralph-loop-cc-tdd-wt-vibe-kanban-template](https://github.com/qte77/ralph-loop-cc-tdd-wt-vibe-kanban-template) and its instances. Cross-repo patterns are in [../cross-repo-digest.md](../cross-repo-digest.md).

This file is a write-back target for Ralph's `compound_writeback()`.

---

## Shell Scripting

### Makefile `$(or)` Does Not Override `?=` Defaults

- **Context**: Makefile variable defaults with `?=` and `$(or $(VAR),fallback)` pattern
- **Problem**: `VAR ?= default` sets VAR at parse time; `$(or $(VAR),fallback)` always sees VAR as truthy — fallback never triggers.
- **Solution**: Use `?=` directly as the default mechanism. Use `ifdef`/`ifndef` guards when conditional override is needed.
- **References**: `Makefile` (cc_run_solo, cc_run_teams recipes)

### Repeated Dispatch Chains Inflate File Complexity

- **Context**: Multiple methods in a module dispatching on the same enum/string value
- **Problem**: Each `if/elif/else` chain over the same enum adds ~3 CC complexity points; 4 methods = 12 points from one pattern.
- **Solution**: Replace with a registry dict. Dispatch becomes a single lookup validated once at entry point.
- **References**: `ralph/scripts/` dispatch patterns

---

## Git Strategy

### `-X ours` Does Not Delete Files Added by Theirs

- **Context**: `git merge -X ours` or rebase with ours strategy
- **Problem**: Strategy keeps our content for conflicts but does not delete files that only exist on the other branch.
- **Solution**: After merge, manually delete unexpected files or cherry-pick specific paths.
- **References**: ralph/docs/LEARNINGS.md section 4 (authoritative)

### PR Squash Merge via GitHub API Requires Both Title and Message

- **Context**: Merging a Ralph branch PR via GitHub API
- **Problem**: `commit_title` alone drops all branch commit messages from squash body.
- **Solution**: Pass both `commit_title` and `commit_message`; title format: `PR <title> (#NUM)`.
- **References**: ralph/docs/LEARNINGS.md section 4

---

## Self-Evolving Loop

### Coverage Before Audit Ordering

- **Context**: Sprint includes both adding test coverage and deleting low-value tests
- **Problem**: Deleting implementation-detail tests first creates a coverage gap.
- **Solution**: Order coverage improvements before test pruning. Express as `depends:` in story breakdown.
- **References**: AGENT_LEARNINGS.md (Agents-eval) Sprint 6 Features 14-15

---

## BATS Testing

### BATS Tests Need Git Identity in CI

- **Context**: BATS tests creating temporary git repos and running `git commit`
- **Problem**: CI runners lack `user.name`/`user.email`; `git commit` fails.
- **Solution**: Add `git config --global user.name "test"` and `user.email "test@test"` in BATS `setup()`.
- **References**: `tests/unit/test_*.bats`
