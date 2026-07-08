---
title: Plans — Design & Decision Docs
purpose: Convention for docs/plans/ — durable plan/design docs (the saved output of plan-mode work). GitHub Issues remain the authoritative backlog/roadmap; each plan doc links its tracking issue.
created: 2026-06-14
updated: 2026-07-08
---

**Status**: Reference (convention)

`docs/plans/` holds **plan / design / decision docs** — the durable output of a plan-mode (or design) session for a non-trivial effort. It is **not** a task list or a roadmap.

## What goes where

| Need | Home |
|---|---|
| Backlog / roadmap / "what to do next" | **GitHub Issues** — the single source of truth ([#191](https://github.com/qte77/ai-agents-research/issues/191) retired the static `docs/TODO.md` to stop CHANGELOG/issue duplication) |
| Detailed plan / design for a specific effort | **`docs/plans/`** (here) — one doc per effort, linked from its tracking issue |
| What has already landed | `CHANGELOG.md` `[Unreleased]` |
| Escalations / blockers needing a human decision | `AGENT_REQUESTS.md` |

## Convention

- **One doc per effort**, named `YYYY-MM-DD-<slug>.md`.
- **Link the tracking issue both ways**: the plan doc names its issue in frontmatter (`issue:`) and body; the issue links back to the plan doc.
- **Plans are not the backlog.** A plan doc explains *how* a tracked task will be done; the issue tracks *whether/when*. Don't list untracked tasks here — open an issue.
- Frontmatter: `title / status / issue / created / updated`. `status` ∈ `draft` | `approved` | `done` | `superseded`.

## Index

| Plan | Status | Issue(s) |
|---|---|---|
| [2026-06-14-planning-workflow-and-open-task-triage.md](2026-06-14-planning-workflow-and-open-task-triage.md) | done | #242, #243 |
| [2026-07-05-status-frontmatter-migration.md](2026-07-05-status-frontmatter-migration.md) | approved | #348 |
| [2026-07-08-new-sources-batch.md](2026-07-08-new-sources-batch.md) | done | #374 |
| [2026-07-08-source-expansion-wave2.md](2026-07-08-source-expansion-wave2.md) | done | #374 |
| [2026-07-08-graphify-rebuild-354.md](2026-07-08-graphify-rebuild-354.md) | approved | #354 |
