---
title: Agentic Workflow Frameworks — Landscape
purpose: The workflows-vs-agents distinction (Anthropic's 5 patterns), the agentic-workflow framework landscape, durable-execution engines, and production anti-patterns — beyond Claude Code's own workflow tool.
category: landscape
created: 2026-06-27
updated: 2026-06-27
validated_links: 2026-06-27
---

**Status**: Research (informational)

## What It Is

The external agentic-**workflow** framework landscape plus the workflows-vs-agents distinction. It complements Claude Code's own [Workflow tool](../cc-native/agents-skills/CC-dynamic-workflows-analysis.md) and the broader [agent-frameworks catalog](agent-frameworks-infrastructure-landscape.md) (which lists the orchestration frameworks). What this doc adds: the **pattern vocabulary**, the **durable-execution** layer, and an **anti-pattern taxonomy**.

## Workflows vs agents (Anthropic's 5 patterns)

Per [Anthropic — Building Effective Agents][anthropic-bea]: **workflows** orchestrate LLMs + tools through *predefined code paths*; **agents** let the LLM direct its own process. The guiding rule — "find the simplest solution, and add complexity only when it demonstrably improves outcomes." The five composable workflow patterns:

1. **Prompt chaining** — a fixed sequence of steps (each output feeds the next), with optional gates between.
2. **Routing** — classify the input, dispatch to a specialized follow-up.
3. **Parallelization** — *sectioning* (independent subtasks at once) or *voting* (same task N times, aggregate).
4. **Orchestrator–workers** — a lead LLM decomposes + delegates to workers dynamically, then synthesizes.
5. **Evaluator–optimizer** — one LLM generates, another critiques, in a loop until a bar is met.

Claude Code's own Workflow tool implements these in a deterministic JS script — see the cross-ref.

## Framework landscape

The orchestration frameworks themselves are catalogued in [agent-frameworks-infrastructure-landscape.md §1](agent-frameworks-infrastructure-landscape.md) (LangGraph, CrewAI, AutoGen, …); this table adds the axis that matters for *workflows* — **deterministic-DAG vs agentic** control flow, and whether execution is **durable** (survives a crash/restart). Stars via `gh api`, 2026-06-27.

| Framework | Stars | Control flow | Durable? |
|---|---|---|---|
| [LangGraph][langgraph] | 35.9K | graph (DAG + agentic) | checkpointers |
| [CrewAI][crewai] | 54.5K | roles + flows | app-level only |
| [Langflow][langflow] | 150.1K | visual DAG builder | no |
| [Mastra][mastra] | 25.5K | TS workflows + agents | suspend/resume |
| [Burr][burr] | 2.5K | explicit state-machine DAG | persisters |
| [Conductor (OSS)][conductor] | 32.0K | server-orchestrated DAG | yes (server-side) |

LangGraph/CrewAI detail lives in the catalog — cross-referenced, not duplicated.

## Durable execution (the layer the catalog omits)

When a workflow must survive process crashes, provider timeouts, or human-in-the-loop pauses lasting hours, **durable-execution engines** persist each step so a fresh process resumes from the last checkpoint. The pattern mainstreamed across AWS / Cloudflare / Vercel in late 2025.

| Engine | Stars | Model |
|---|---|---|
| [Temporal][temporal] | 21.3K (MIT) | workflows-as-code; deterministic replay from an event history |
| [Inngest][inngest] | 5.5K | event-driven durable functions with built-in flow control |
| [Restate][restate] | 4.1K | durable execution + virtual objects; low-latency |

The core primitive is idempotency on a stable **`(workflow_id, step_id)`** key — so a replayed step is a no-op, not a duplicated side-effect.

## Anti-patterns (severity-tiered)

| Tier | Anti-pattern | Why it bites |
|---|---|---|
| **S0** | Hidden state across steps | non-reproducible runs; can't replay/debug |
| **S0** | Over-broad tool grants | one bad step → wide blast radius |
| **S0** | Unbounded loops | runaway cost; no termination |
| **S1** | Races on shared state | lost updates, nondeterminism |
| **S1** | Missing idempotency | retries duplicate side-effects |
| **S1** | Naive retry (no backoff/cap) | thundering-herd; infinite retry |
| **S2** | Synchronous blocking | one slow step stalls the pipeline |
| **S2** | Orchestrator bottleneck | a single lead serializes everything |

**Best-practices checklist:** bound every loop; make each side-effecting step idempotent on a stable key; scope tools per step; keep state explicit (no hidden globals); backoff + retry caps; parallelize independent sections; checkpoint long / HITL workflows on a durable engine.

**Real-world signal:** the "framework graveyard" of abandoned 2023–24 agent frameworks, and production write-ups (e.g. Replit's Agent 3), point the same way — *fewer, simpler, durable* patterns beat elaborate orchestration.

## Cross-References

- [CC-dynamic-workflows-analysis.md](../cc-native/agents-skills/CC-dynamic-workflows-analysis.md) — Claude Code's own Workflow tool (these patterns in a deterministic JS script)
- [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) — §1 orchestration frameworks, §8 output validation / guardrails
- [agentic-engineering-disciplines-landscape.md](../sdlc-lcm/agentic-engineering-disciplines-landscape.md) — flow / loop engineering as disciplines

## Sources

| Source | Content |
|---|---|
| [Anthropic — Building Effective Agents][anthropic-bea] | Workflows-vs-agents; the 5 composable patterns |
| [Temporal][temporal] · [Inngest][inngest] · [Restate][restate] | Durable-execution engines |
| [LangGraph][langgraph] · [CrewAI][crewai] · [Langflow][langflow] · [Mastra][mastra] · [Burr][burr] · [Conductor (OSS)][conductor] | Workflow / orchestration frameworks (stars via `gh api`, 2026-06-27) |

[anthropic-bea]: https://www.anthropic.com/research/building-effective-agents
[temporal]: https://github.com/temporalio/temporal
[inngest]: https://github.com/inngest/inngest
[restate]: https://github.com/restatedev/restate
[langgraph]: https://github.com/langchain-ai/langgraph
[crewai]: https://github.com/crewAIInc/crewAI
[langflow]: https://github.com/langflow-ai/langflow
[mastra]: https://github.com/mastra-ai/mastra
[burr]: https://github.com/DAGWorks-Inc/burr
[conductor]: https://github.com/conductor-oss/conductor
