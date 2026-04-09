---
title: Feynman Research Agent Analysis
source: https://github.com/getcompanion-ai/feynman
purpose: Analysis of Feynman as an open-source terminal-based AI research agent with multi-agent investigation workflows.
created: 2026-04-09
updated: 2026-04-09
validated_links: 2026-04-09
---

**Status**: Open-source (MIT), active development by [Companion AI][feynman-site]

## What It Is

Feynman is an **open-source terminal-based AI research agent** that automates
literature review, experiment replication, and scientific investigation through
multi-agent coordination. Named after the physicist's approach to understanding
through investigation.

**Key distinction**: Unlike DeerFlow (general-purpose super agent harness) or
Goose (MCP-native coding agent), Feynman is purpose-built for **scientific
research workflows** — paper search, peer review simulation, and experiment
replication on local or cloud GPUs.

## Core Architecture

```
User → CLI commands → Dispatcher → Sub-agents (4 bundled)
                                 → AlphaXiv (paper search)
                                 → GPU backends (Modal, RunPod)
                                 → Session recall
```

### Sub-Agent System

| Agent | Role |
|-------|------|
| **Researcher** | Evidence gathering across papers, web, repos |
| **Reviewer** | Severity-graded critique generation |
| **Writer** | Structured artifact drafting |
| **Verifier** | Citation and URL validation |

### Workflow Commands

| Command | Purpose |
|---------|---------|
| `/deepresearch` | Multi-source investigation |
| `/lit` | Literature review synthesis |
| `/audit` | Paper-vs-codebase verification |
| `/replicate` | Experiment reproduction (local/cloud GPU) |
| `/review` | Simulated peer review with severity grades |
| `/compare` | Cross-paper comparison |
| `/draft` | Structured writing |
| `/watch` | Monitoring mode |
| `/autoresearch` | Autonomous research loops |

## Adoption Decision

| Dimension | Assessment |
|-----------|------------|
| **Use case** | Scientific research, literature review, experiment replication |
| **Runtime** | Pi agent runtime, Node.js 20.19.0+ |
| **GPU support** | Local, Modal, RunPod for experiment replication |
| **Maturity** | Active (3.8K stars, 451 forks) |
| **License** | MIT |

**Strengths**: Only agent in this survey with dedicated experiment replication
(`/replicate` with GPU backend dispatch). Source verification with inline
citations. Session-based recall for research continuity.

**Risks**: Niche scope — research-only, not general-purpose coding. Pi runtime
dependency (not widely adopted). AlphaXiv integration may limit paper coverage.

## Cross-References

- [deerflow-analysis.md](deerflow-analysis.md) — general-purpose super agent (LangGraph)
- [CC-community-skills-landscape.md](../cc-community/CC-community-skills-landscape.md) — agent-skills `/review` for code (different domain)

## Sources

| Source | Content |
|---|---|
| [Feynman repo][feynman] | Open-source research agent |
| [Feynman docs][feynman-docs] | Installation and workflow documentation |

[feynman]: https://github.com/getcompanion-ai/feynman
[feynman-site]: https://feynman.is
[feynman-docs]: https://feynman.is/docs
