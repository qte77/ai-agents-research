---
title: Agentic SDLC Patterns
purpose: Emerging lifecycle patterns for AI agent-driven development.
created: 2026-03-24
updated: 2026-09-24
validated_links: 2026-09-24
sources:
  - https://www.epam.com/insights/ai/blogs/agentic-development-lifecycle-explained
  - https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896
  - https://www.amplifypartners.com/blog-posts/the-agent-first-developer-toolchain-how-ai-will-radically-transform-the-sdlc
  - https://www.pwc.com/m1/en/publications/2026/docs/future-of-solutions-dev-and-delivery-in-the-rise-of-gen-ai.pdf
  - https://about.gitlab.com/blog/agentic-sdlc-gitlab-and-tcs-deliver-intelligent-orchestration-across-the-enterprise/
  - https://www.cio.com/article/4134741/how-agentic-ai-will-reshape-engineering-workflows-in-2026.html
---

## Agentic SDLC Patterns

Lifecycle patterns designed for AI agent-driven development, not traditional
human-driven SDLC.

> **Legacy note:** RAPID is legacy — the `RAPID-spec-forge` repo was archived 2026-04-26 and superseded by [qte77/qte77](https://github.com/qte77/qte77). RAPID references below are retained for historical SDLC/LCM-pattern context.

## 1. ADLC (Agentic Development Lifecycle)

**Source:** EPAM

A lifecycle for systems where LLMs are core product behavior, not just assistants.

| Dimension | Traditional SDLC | ADLC |
|-----------|-----------------|------|
| Behavior | Fully specified at build time | Emergent, non-deterministic |
| Testing | Pass/fail against spec | Observation and correction loops |
| Failure mode | Bug (deviation from spec) | Drift (behavior changes without code change) |
| Lifecycle focus | Build -> Ship | Build -> Observe -> Correct -> Repeat |

**Phases:** Define -> Build -> Evaluate -> Deploy -> Observe -> Correct

**qte77 mapping:** Ralph = Build+Evaluate, RAPID = Define+Evaluate.
Gap: no formal Observe+Correct phases (post-deployment feedback loop).

## 2. Agentic SDLC (Microsoft/GitLab/PwC)

Specialized agents per SDLC phase, orchestrated in parallel.

```text
Orchestrator
  +-- Requirements Agent    (Ralph: RAPID BRD->PRD->FRD)
  +-- Coding Agent          (Ralph: TDD loop)
  +-- Review Agent          (gap: no formal review agent)
  +-- Deploy Agent          (gap: manual CI/CD)
  +-- Monitor Agent         (gap: no monitoring agent)
```

**Measured impact (early 2026):** ~55% faster task completion, 38.7% of AI
review comments lead to code fixes (Atlassian RovoDev).

## 3. Spec-Driven Development (SDD)

"Version control for your thinking" — specs are the primary artifact.

- Specs version-controlled alongside code
- Agents consume specs, produce code
- Spec changes trigger agent re-execution (like code changes trigger CI)
- Human review shifts from code to specs

**qte77 mapping:** RAPID pipeline + Ralph prd.json already spec-driven.
Gap: no automated spec-change -> agent-trigger pipeline.

**SpecShip** (`aws-samples/sample-specship`, MIT, 252 stars, created 2026-07-10,
`gh api` 2026-09-24) is AWS Samples' own instance of the SDD pattern: a five-stage
pipeline (brownfield recon -> plan, with market research -> TDD build -> adversarial
validation -> ship with PR + changelog) packaged as a "Kiro Power" -- a reusable skill
package for the Kiro agent-orchestration platform. Its quality gate is the "human
review shifts from code to specs" idea made concrete: the builder agent cannot judge
its own code, so seven independent validator subagents (code review, security, browser
QA, design, alignment, load testing) run in parallel with typed verdicts before a
milestone is accepted, on top of failing-tests-first TDD. Installed via a single
`./install.sh` that auto-detects dependencies (superpowers, gstack, Playwright MCP) and
copies steering files to `~/.kiro/steering/`; runs guided (pauses for plan approval) or
autonomous (end-to-end).

## 4. Agent-First Developer Toolchain (Amplify Partners)

Traditional SDLC artifacts reimagined as coordination layers for agents.

| Traditional | Agent-First | qte77 Status |
|------------|-------------|-------------|
| IDE | Agent workspace | Claude Code |
| VCS branches | Agent task boundaries | Polyforge, Ralph worktrees |
| CI/CD | Continuous validation | Gap: manual `make validate` |
| Code review | Agent review + human oversight | Gap: no review agent |

## Synthesis

| Pattern | Have | Gap |
|---------|------|-----|
| ADLC Observe+Correct | -- | Post-deployment feedback loop |
| Parallel agents | Ralph (build), RAPID (req) | Review, Monitor agents |
| SDD spec-as-trigger | RAPID, prd.json | Automated trigger pipeline |
| Agent-first toolchain | CC, worktrees, Polyforge | Agent-triggered CI/CD |

**sdlc-lcm-manager priorities:**

1. Codify Observe+Correct as formal phases (extend maintain)
2. Gate predicates agents can evaluate programmatically
3. Phase inference from repo artifacts (SDD alignment)

## Sources

| Source | Content |
|---|---|
| [SpecShip][specship] (`aws-samples/sample-specship`) | Kiro Power SDD workflow; 252★, MIT, `gh api` 2026-09-24 |

[specship]: https://github.com/aws-samples/sample-specship
