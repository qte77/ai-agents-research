---
title: Feynman Research Agent Analysis
source: https://github.com/Companion-Inc/feynman
purpose: Analysis of Feynman as an open-source terminal-based AI research agent with multi-agent investigation workflows.
created: 2026-04-09
updated: 2026-11-26
validated_links_on: 2026-09-30
status: assess
---

**Details:** Open-source (MIT), active development by [Companion AI][feynman-site]

## What It Is

Feynman is an **open-source terminal-based AI research agent** that automates
literature review, experiment replication, and scientific investigation through
multi-agent coordination. Named after the physicist's approach to understanding
through investigation.

**Key distinction**: Unlike DeerFlow (general-purpose super agent harness) or
Goose (a coding agent native to the Model Context Protocol, MCP), Feynman is purpose-built for **scientific
research workflows** — paper search, peer review simulation, and experiment
replication on local or cloud GPUs.

## Core Architecture

```text
User → CLI commands → Dispatcher → Sub-agents (4 bundled)
                                 → Paper search (alphaXiv plus other indexes)
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
| `/recipe` | Ranked ML training recipes |
| `/summarize` | Summarisation |
| `/autoresearch` | Autonomous research loops |

## Adoption Decision

| Dimension | Assessment |
|-----------|------------|
| **Use case** | Scientific research, literature review, experiment replication |
| **Runtime** | Pi agent runtime, Node.js >=22.22.0 for npm installs (package.json engines, feynman 0.5.74, checked 2026-11-26) |
| **GPU support** | Local, Modal, RunPod (optional, each only if its CLI is set up) for experiment replication |
| **Maturity** | Active (about 10.2K stars, 1.1K forks, last push 2026-11-25; checked 2026-11-26) |
| **License** | MIT |

**Strengths**: Only agent in this survey with dedicated experiment replication
(`/replicate` with GPU backend dispatch). Source verification with inline
citations. Session-based recall for research continuity.

**Risks**: Niche scope — research-only, not general-purpose coding. Pi runtime
dependency (not widely adopted). The README lists many paper indexes (alphaXiv, Semantic Scholar, OpenAlex, arXiv, PubMed and others), so coverage is not limited to alphaXiv (checked 2026-11-26).

## Cross-References

- [deerflow-analysis.md](../orchestrators/deerflow-analysis.md) — general-purpose super agent (LangGraph)
- [CC-community-skills-landscape.md](../../cc-community/CC-community-skills-landscape.md) — agent-skills `/review` for code (different domain)
- [openresearch-analysis.md](openresearch-analysis.md) — local-first, git-native research workspace from the team that started alphaXiv (the paper search Feynman uses); a separate product that does not document which service backs its paper commands

## Sources

| Source | Content |
|---|---|
| [Feynman repo][feynman] | Open-source research agent |
| [Feynman docs][feynman-docs] | Installation and workflow documentation |

[feynman]: https://github.com/Companion-Inc/feynman
[feynman-site]: https://feynman.is
[feynman-docs]: https://feynman.is/docs
