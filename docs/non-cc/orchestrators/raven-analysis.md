---
title: Raven — Self-Evolving Multi-Agent Orchestration Harness
source: https://github.com/EverMind-AI/Raven
purpose: Analysis of Raven, EverMind's "harness of harnesses" — a multi-agent orchestrator with a benchmark-gated self-evolution loop and pluggable third-party coding-agent backends.
platform_scope: [claude-code, github-copilot, qwen-code]
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

Raven ([EverMind-AI/Raven][repo]) describes itself as "The Harness of
Harnesses—a trusted, persistent, self-evolving multi-agent ecosystem for
all-domain collaboration" (per repo description, accessed 2026-09-24). It
runs as a Host Agent that coordinates specialized sub-agents through unified
surfaces — delegating tasks, managing execution, and integrating results
across domains — rather than being a single coding agent itself.

## Architecture

Per the README, five components make up the system:

- **Agent Orchestration** — coordinates multiple agents, manages task
  dependencies and parallel execution, and converts multi-step collaboration
  into reusable workflows.
- **Evolver** — a separate tool, not a runtime component of the agents
  themselves, that "drives harness self-evolution by diagnosing failures,
  testing candidate improvements" against benchmarks and keeping the ones
  that hold up. This is benchmark-gated offline evolution of the harness
  configuration, not in-session learning.
- **EverOS Memory** — cross-session context and "reusable skills for future
  tasks." EverOS is itself a separate EverMind-AI project, already catalogued
  in this corpus as a Markdown-native, local-first memory layer (see
  [Cross-References](#cross-references)); Raven consumes it rather than
  reimplementing memory.
- **SkillForge** — retrieves specialized expertise from local libraries and a
  catalog the README states contains "114,190 skills" (per README, accessed
  2026-09-24 — an unverified vendor count, not independently audited).
- **Proactivity** — combines event monitoring and scheduled execution for
  anticipatory task initiation.

## Built-In Agents and Third-Party Backends

Four specialized agents ship ready for orchestration: **Raven-Research**
(autonomous deep research with structured reports), **Raven-Code** (agentic
software development and debugging), **Raven-Design** (visual design and
presentation creation), and **Raven-Oncall** (unattended workflow automation
spanning hours or overnight).

Separately, the README states Raven connects to 13 external agents via ACP,
CLI, or OpenAI-compatible APIs, including Claude Code, GitHub Copilot, and
Qwen Code. Claude Code is one of several pluggable third-party backends here,
not an exclusive integration surface — the same pattern documented for MOSS's
`CodingAgentRunner` interface (see [Cross-References](#cross-references)) —
which is why this doc sits in `non-cc/` rather than `cc-community/`.

## Installation

The README documents four install paths: a shell installer for
Linux/macOS/WSL2, a PowerShell installer for Windows, a pre-configured Docker
Compose stack, and an editable source install from a repository checkout.
The WebUI launches with `raven web`.

## License and Maturity

Apache-2.0 (per `gh api repos/EverMind-AI/Raven`). Created 2026-05-21, latest
release `v0.2.0` (published 2026-09-23), most recent push 2026-09-24 —
4,058 stars, 93 forks, 87 open issues (all via `gh api`, accessed
2026-09-24). This is a fast-moving, ~4-month-old project; the star/fork
counts indicate visibility but no independent evidence of production
adoption was found beyond the repo's own activity.

## Corpus Relevance

Raven pairs two patterns already tracked in this corpus — benchmark-gated
harness self-evolution (as in MOSS) and pluggable multi-vendor coding-agent
backends — inside a broader multi-agent orchestration product that also
folds in memory (EverOS) and a large skill catalog (SkillForge). Its
self-evolution claims rest entirely on the vendor's own README; no
third-party benchmark reproduction was found.

## Cross-References

- [agent-frameworks-infrastructure-landscape.md — EverOS][everos] — the
  memory-layer component Raven's "EverOS Memory" consumes, already
  catalogued in this corpus independently of Raven.
- [moss-self-evolving-agent-analysis.md][moss] — the same benchmark-gated,
  offline harness-self-evolution pattern (MOSS's evolution module vs.
  Raven's Evolver), and the same "Claude Code as one of several pluggable
  coding-agent backends" shape.

## Sources

| Source | Content |
|---|---|
| [EverMind-AI/Raven repo][repo] | README — architecture, components, install methods, built-in agents, third-party integrations, license |
| GitHub API `repos/EverMind-AI/Raven`, accessed 2026-09-24 | Stars, forks, open issues, license, created/pushed timestamps, latest release tag |

[repo]: https://github.com/EverMind-AI/Raven
[everos]: ../agent-frameworks-infrastructure-landscape.md
[moss]: ../agents/moss-self-evolving-agent-analysis.md
