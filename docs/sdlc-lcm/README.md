---
title: SDLC & LCM Research
purpose: Research overview for Software Development Lifecycle (SDLC) and Lifecycle Management (LCM) applied to AI coding agent ecosystems.
created: 2026-03-24
---

## SDLC & LCM Research

Lifecycle management specs for the qte77 coding agent ecosystem.

> **Legacy note:** RAPID is legacy — the `RAPID-spec-forge` repo was archived 2026-04-26 and superseded by [qte77/qte77](https://github.com/qte77/qte77). RAPID references below are retained for historical SDLC/LCM-pattern context.

## Two Tracks

| Track | Scope | Applies To | Key Question |
|-------|-------|------------|--------------|
| **SDLC** | Dev process phases (plan, build, test, release, deploy, maintain) | All repos via Ralph + Polyforge | "What dev phase is this repo/feature in?" |
| **LCM** | Product lifecycle phases (incubation, active, maintenance, deprecated, retired) | Products/projects via RAPID | "What lifecycle stage is this product in?" |

## Documents

| Document | Content |
|----------|---------|
| [sdlc-spec.md](sdlc-spec.md) | SDLC phase definitions with entry/exit gates, mapped to NIST AI RMF + ISO 42001 |
| [lcm-spec.md](lcm-spec.md) | Product lifecycle phase definitions with SLA expectations and allowed changes |
| [lcm-release-runbook.md](lcm-release-runbook.md) | Release management checklist bridging SDLC release phase to LCM transitions |
| [oss-alm-landscape.md](oss-alm-landscape.md) | OSS ALM tool comparison (Tuleap, OpenProject, Redmine, GitLab) |
| [agentic-sdlc-patterns.md](agentic-sdlc-patterns.md) | Emerging patterns: ADLC, Agentic SDLC, Spec-Driven Development |
| [agentic-engineering-disciplines-landscape.md](agentic-engineering-disciplines-landscape.md) | Synthesis: "-engineering" disciplines (prompt→spec) + "-driven-dev" methodologies (TDD→EDD→SDD) in a five-layer credo stack |
| [goal-tracking-attribution-landscape.md](goal-tracking-attribution-landscape.md) | Top-down goals → bottom-up attribution: the goal→spec→build→learning loop, qte77-estate worked examples, and the commercial OKR/PM baseline |
| [multi-agent-onboarding-outlook.md](multi-agent-onboarding-outlook.md) | Multi-agent support: CC, Kiro, Cursor, Gemini CLI, AGENTS.md convergence |
| [mas-design-principles.md](mas-design-principles.md) | MAS design principles from 12-Factor Agents, Anthropic harnesses, PydanticAI |
| [mas-benchmarking-best-practices.md](mas-benchmarking-best-practices.md) | Production best practices for MAS development and benchmarking |
| [mas-security-framework.md](mas-security-framework.md) | OWASP MAESTRO v1.0 threat modeling (7-layer) for multi-agent systems |
| [ai-security-governance-analysis.md](ai-security-governance-analysis.md) | NIST AI RMF, EU AI Act, OWASP LLM Top 10, ISO 42001 frameworks |
| [agent-evaluation-metrics-landscape.md](agent-evaluation-metrics-landscape.md) | Agent evaluation metrics survey (task completion, reasoning, safety) |
| [evaluation-data-resources-landscape.md](evaluation-data-resources-landscape.md) | Eval frameworks, agentic benchmarks, datasets (companion to the metrics survey) |

## Framework Grounding

Specs build on NIST AI RMF, ISO 42001 A.6, ISO 23894, and OWASP MAESTRO. See sdlc-spec.md cross-framework summary table.

## Target Repo

Implementation code (state machines, gates, config) will live in a dedicated
`sdlc-lcm-manager` repo (future), consumed as a git submodule by downstream repos.
