---
title: Architecture - ai-agents-research
description: Document hierarchy, conventions, and downstream consumer relationships for the ai-agents-research repository
category: technical
created: 2026-03-22
updated: 2026-05-25
---

## Architecture: ai-agents-research

## Overview

This is a research-only repository — no code, only structured markdown documents. The "architecture" is the document hierarchy, naming conventions, and the three automated monitors that keep it current.

## Document Hierarchy

```text
ai-agents-research/
├── docs/
│   ├── cc-native/             # Anthropic-native CC features
│   │   ├── agents-skills/     # Agent spawning, skills, orchestration patterns
│   │   ├── ci-remote/         # GHA, cloud sessions, remote access, web auth
│   │   ├── configuration/     # Hooks, fast mode, model/provider config, CLI ref
│   │   ├── context-memory/    # Extended context, memory system, llms.txt
│   │   ├── examples/          # Worked examples and reference workflows
│   │   ├── model-internals/   # Model-level interpretability research
│   │   ├── plugins-ecosystem/ # Official plugins, community plugins, cowork API
│   │   ├── sandboxing/        # Sandbox internals (bwrap, platforms, permissions)
│   │   └── sessions/          # Session lifecycle, artifacts, schemas
│   ├── cc-community/          # Community skills, tooling, CLAUDE.md patterns
│   ├── non-cc/                # Non-CC coding agents (JetBrains Air, DeerFlow, Goose, ...)
│   ├── sdlc-lcm/              # SDLC + product lifecycle management specs
│   ├── learnings/             # Cross-repo compound learnings hub (CRLA write-back target)
│   │   └── per-repo/          # Per-repo pattern distillations
│   ├── research/              # Auto-generated cumulative agentic-AI paper index (rxiv eval)
│   └── archive/               # Retired Agents-eval era docs
├── triage/                    # Auto-generated monitor outputs (at repo root)
│   ├── cc-changelog/          # CC changelog + native-sources triage
│   ├── community/             # Community-sources triage
│   ├── status-monitor/        # CC status page incident archive + stats
│   └── rxiv/                  # ArXiv paper eval triage (filtered by RXIV_TOPIC)
└── .github/
    ├── workflows/             # 4 monitor cron jobs + lint workflow
    ├── actions/               # Composite actions (create-triage-pr)
    ├── scripts/               # Monitor scripts + shared lib/monitor_utils.py
    └── state/                 # Per-monitor fingerprint files (committed)
```

## Analysis Format Convention

Every research document follows this four-section structure:

1. **What it is** — Brief description of the feature or agent
2. **How it works** — Mechanism, internals, observed behavior
3. **Adoption decision** — Adopt / Defer / Skip with rationale
4. **Action items** — Concrete next steps for downstream repos

This format ensures each doc is directly actionable, not just descriptive.

## Frontmatter Conventions

All documents carry YAML frontmatter:

```yaml
---
title: <Descriptive title>
description: <One-line summary>
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Optional fields: `category`, `version`, `tags`, `source`.

## Automated Monitors

Four GitHub Actions cron workflows maintain currency by polling external sources and opening triage PRs when new content is found:

| Monitor | Source | Output | Schedule |
|---|---|---|---|
| CC status monitor | Anthropic status page | `triage/status-monitor/` | Monday 09:00 UTC |
| CC changelog + native sources | CC release notes + GH issues/discussions + Anthropic blog | `triage/cc-changelog/` | Monday 09:00 UTC |
| Community monitor | Community forums, GitHub | `triage/community/` | Monday 10:00 UTC |
| ArXiv paper eval | `qte77/gha-rxiv-feed-action` CSVs → LLM relevance filter | `triage/rxiv/` | Tuesday 09:00 UTC |

Each monitor commits its state-fingerprint file in `.github/state/` alongside the triage PR for content-stable dedup across runs. The rxiv eval skips PR creation when the assembled report fingerprint matches the prior emission for the same `(server, year, week)` key.

## Lint Gate

Three lint jobs run on every PR touching docs, workflows, or actions:

| Job | Tool | Scope |
|---|---|---|
| Markdown lint | `markdownlint-cli2` | `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `docs/**/*.md` |
| Link check | `lychee` | repo-wide (configured via `lychee.toml`) |
| Action lint | `actionlint` (+ `shellcheck` on the runner) | `.github/workflows/**`, `.github/actions/**` |

The rxiv triage job additionally runs `markdownlint-cli2` against the assembled would-be PR content (with the action's H1 prepend simulated) and fails the job before opening a triage PR if the output is md-dirty.

## Downstream Consumers

Research from this repository feeds directly into implementation repos:

| Downstream Repo | Consumes From | Key Docs |
|---|---|---|
| [cc-recursive-team-mode](https://github.com/qte77/cc-recursive-team-mode) | `docs/cc-native/agents-skills/`, `docs/cc-native/session-analysis/` | `CC-recursive-spawning-patterns.md`, session artifact schema docs |
| [coding-agent-eval](https://github.com/qte77/coding-agent-eval) | `docs/cc-native/comparisons/`, `docs/cc-native/features/`, `docs/non-cc/` | Agent feature matrices, invocation method analyses |
| [multi-tasking-quality-benchmark](https://github.com/qte77/multi-tasking-quality-benchmark) | `docs/cc-native/meta/` | Quality metric methodology docs |
| [ralph-loop-cc-tdd-wt-vibe-kanban-template](https://github.com/qte77/ralph-loop-cc-tdd-wt-vibe-kanban-template) | `docs/learnings/` | Cross-repo compound learning aggregation (CRLA) — Ralph reads this as `COMPOUND_LEARNINGS_PATH` |

## Reference Flow

```text
External sources (CC changelog, status page, community)
        ↓ (automated monitors)
triage/  (raw triage outputs, human-reviewed)
        ↓ (researcher promotes findings)
docs/cc-native/ or docs/non-cc/ or docs/cc-community/  (structured analyses)
        ↓ (downstream repos consume)
cc-recursive-team-mode / coding-agent-eval / multi-tasking-quality-benchmark
```

Human review is required at the triage → docs promotion step. Monitors surface content; researchers make adoption decisions.
