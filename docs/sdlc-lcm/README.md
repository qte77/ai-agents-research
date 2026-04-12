---
title: SDLC & LCM Research
purpose: Research overview for Software Development Lifecycle (SDLC) and Lifecycle Management (LCM) applied to AI coding agent ecosystems.
created: 2026-03-24
---

## SDLC & LCM Research

Lifecycle management specs for the qte77 coding agent ecosystem.

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
| [multi-agent-onboarding-outlook.md](multi-agent-onboarding-outlook.md) | Multi-agent support: CC, Kiro, Cursor, Gemini CLI, AGENTS.md convergence |

## Framework Grounding

Specs build on NIST AI RMF, ISO 42001 A.6, ISO 23894, and OWASP MAESTRO. See sdlc-spec.md cross-framework summary table.

## Target Repo

Implementation code (state machines, gates, config) will live in a dedicated
`sdlc-lcm-manager` repo (future), consumed as a git submodule by downstream repos.
