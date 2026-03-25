---
title: Agentic SDLC Patterns
purpose: Emerging lifecycle patterns for AI agent-driven development.
created: 2026-03-24
sources:
  - https://www.epam.com/insights/ai/blogs/agentic-development-lifecycle-explained
  - https://techcommunity.microsoft.com/blog/appsonazureblog/an-ai-led-sdlc-building-an-end-to-end-agentic-software-development-lifecycle-wit/4491896
  - https://www.amplifypartners.com/blog-posts/the-agent-first-developer-toolchain-how-ai-will-radically-transform-the-sdlc
  - https://www.pwc.com/m1/en/publications/2026/docs/future-of-solutions-dev-and-delivery-in-the-rise-of-gen-ai.pdf
  - https://about.gitlab.com/blog/agentic-sdlc-gitlab-and-tcs-deliver-intelligent-orchestration-across-the-enterprise/
  - https://www.cio.com/article/4134741/how-agentic-ai-will-reshape-engineering-workflows-in-2026.html
---

# Agentic SDLC Patterns

Lifecycle patterns designed for AI agent-driven development, not traditional
human-driven SDLC.

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

```
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
