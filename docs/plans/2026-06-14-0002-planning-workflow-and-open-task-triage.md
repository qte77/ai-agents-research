---
title: Planning Workflow + Open-Task Triage
status: done
issue: "#242, #243"
created: 2026-06-14
updated: 2026-06-14
---

**Status**: Done — establishes the `docs/plans/` convention and triages the session's untracked open tasks into GitHub Issues.

## Context

A 2026-06-14 working session (research integration + archive sweep + doc splits + PR-backlog cleanup) produced several deferred items and raised the question of where to durably record plans. Recon found the repo had **already** made **GitHub Issues the authoritative backlog/roadmap** ([#191](https://github.com/qte77/ai-agents-research/issues/191), 2026-05-26 — which deleted the static `docs/TODO.md` to stop CHANGELOG/issue duplication). There was no `docs/plans/`, no roadmap doc, and no "plans" slot in the doc hierarchy.

## Decision

- `docs/plans/` = home for **plan/design docs** (this is the first). It is **not** a task list.
- **GitHub Issues stay the authoritative backlog/roadmap.** Untracked deferrals become tracker issues.
- Plan docs ↔ issues cross-link. See [README.md](README.md) for the convention.
- Registered `docs/plans/` in [docs/architecture.md](../architecture.md) (hierarchy + "Planning & Roadmap"), `CONTRIBUTING.md`, and `README.md` so it isn't mistaken for `docs/todo/`-style staging.

## Open tasks triaged → issues

| Task | Issue |
|---|---|
| Langtrace URL relocated (404) — update the entry in `CC-agent-observability-methods-analysis.md` + drop the `lychee.toml` exclude added in #237 | [#242](https://github.com/qte77/ai-agents-research/issues/242) |
| Re-apply un-merged PR #206 content (CodeBurn optimize-rules → `CC-usage-tooling-landscape.md`; GitHub-App provenance → `CC-github-actions-analysis.md`; HuggingScience `llms-full.txt` example → `CC-llms-txt-analysis.md`; `BASH_MAX_OUTPUT_LENGTH` → `.claude/settings.json`) | [#243](https://github.com/qte77/ai-agents-research/issues/243) |

Already tracked (no new issue needed): #232, #217, #191, #189, #188, #185.

## Verification

- `make check_docs` and `make check_links` pass.
- `docs/plans/` registered in `docs/architecture.md` / `CONTRIBUTING.md` / `README.md`.
- #242 and #243 open and cross-linked to this doc.
