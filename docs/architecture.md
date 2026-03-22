---
title: Architecture - coding-agents-research
description: Document hierarchy, conventions, and downstream consumer relationships for the coding-agents-research repository
category: technical
created: 2026-03-22
updated: 2026-03-22
---

# Architecture: coding-agents-research

## Overview

This is a research-only repository — no code, only structured markdown documents. The "architecture" is the document hierarchy, naming conventions, and the three automated monitors that keep it current.

## Document Hierarchy

```
coding-agents-research/
├── docs/
│   ├── cc-native/          # Anthropic-native CC features
│   │   ├── agents-skills/  # Agent spawning, skills, orchestration patterns
│   │   ├── architecture/   # CC internals and system design analyses
│   │   ├── changelog-triage/ # Per-release feature breakdowns
│   │   ├── ci-execution/   # Sandboxing, CI runners, remote execution
│   │   ├── comparisons/    # Cross-agent and cross-feature comparisons
│   │   ├── configuration/  # Hooks, fast mode, model/provider config
│   │   ├── features/       # Discrete feature analyses
│   │   ├── meta/           # Research methodology, scope, coverage tracking
│   │   ├── plugins-ecosystem/ # Official plugins, community plugins, cowork API
│   │   ├── context-memory/ # Extended context, memory system, llms.txt
│   │   └── session-analysis/ # Session artifacts, trace schemas, OTEL
│   ├── non-cc/             # Non-CC coding agents
│   │   ├── air/            # JetBrains AI Assistant / Air analysis
│   │   └── devteam/        # agent-era/devteam analysis
│   └── community/          # Community resources
│                           # Skills, plugins, tooling, CLAUDE.md patterns
├── triage/                 # Auto-generated monitor outputs (at repo root)
│   ├── outage-archive/     # CC status page incident archive
│   ├── changelog-triage/   # CC changelog triage outputs
│   └── community-triage/   # Community content triage outputs
└── .github/
    └── workflows/          # 3 automated monitor cron jobs
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

Three GitHub Actions cron workflows maintain currency by polling external sources and opening triage PRs when new content is found:

| Monitor | Source | Output |
|---|---|---|
| CC status monitor | Anthropic status page | `triage/outage-archive/` |
| CC changelog monitor | CC release notes / changelog | `triage/changelog-triage/` |
| Community monitor | Community forums, GitHub | `triage/community-triage/` |

See [`.github/README.md`](../.github/README.md) for monitor configuration details.

## Downstream Consumers

Research from this repository feeds directly into implementation repos:

| Downstream Repo | Consumes From | Key Docs |
|---|---|---|
| [cc-recursive-team-mode](https://github.com/qte77/cc-recursive-team-mode) | `docs/cc-native/agents-skills/`, `docs/cc-native/session-analysis/` | `CC-recursive-spawning-patterns.md`, session artifact schema docs |
| [coding-agent-eval](https://github.com/qte77/coding-agent-eval) | `docs/cc-native/comparisons/`, `docs/cc-native/features/`, `docs/non-cc/` | Agent feature matrices, invocation method analyses |
| [multi-tasking-quality-benchmark](https://github.com/qte77/multi-tasking-quality-benchmark) | `docs/cc-native/meta/` | Quality metric methodology docs |

## Reference Flow

```
External sources (CC changelog, status page, community)
        ↓ (automated monitors)
triage/  (raw triage outputs, human-reviewed)
        ↓ (researcher promotes findings)
docs/cc-native/ or docs/non-cc/ or docs/community/  (structured analyses)
        ↓ (downstream repos consume)
cc-recursive-team-mode / coding-agent-eval / multi-tasking-quality-benchmark
```

Human review is required at the triage → docs promotion step. Monitors surface content; researchers make adoption decisions.
