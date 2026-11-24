---
title: Agentic Workflow Frameworks — Landscape
purpose: The workflows-vs-agents distinction (Anthropic's 5 patterns), agentic-workflow frameworks, durable-execution engines and production anti-patterns, beyond Claude Code's own workflow tool.
created: 2026-06-27
updated: 2026-11-18
validated_links: 2026-11-18
status: research
---

## What It Is

The external agentic-**workflow** framework landscape plus the workflows-vs-agents distinction. It complements Claude Code's own [Workflow tool](../../cc-native/agents-skills/CC-dynamic-workflows-analysis.md) and the broader [agent-frameworks catalog](agent-frameworks-infrastructure-landscape.md) (which lists the orchestration frameworks). What this doc adds: the **pattern vocabulary**, the **durable-execution** layer, and an **anti-pattern taxonomy**.

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

### Checkpoint and resume matrix

Added 2026-11-18, each row from the vendor's docs fetched that day. Resume flags per harness are in [CC-agentic-harness-patterns-analysis.md § Cross-Harness Matrix](../../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#cross-harness-matrix-checked-2026-11-15); this table adds only what is saved, what bounds it and what is not restored. The two families differ in kind: a harness resumes a **transcript** (the model re-reads history), an engine resumes **code** (steps replay from a journal).

| System | Unit saved | Bound / not restored |
|---|---|---|
| Claude Code | Local JSONL transcript per session ([sessions][cc-sessions]); restores history, model, agent, permission mode (terminal), active goal (counters reset), unexpired session-scoped schedules | A tool running when the process died is not rerun. Background Bash and monitors are not restored. Model Context Protocol (MCP), plugin, `--add-dir` and settings flags must be passed again. 30-day default retention. Resuming one session in two terminals makes both write to one transcript, and messages can be missing on a later resume |
| Codex CLI | Session rollout files; `--ephemeral` skips persisting ([commands][codex-cmds]) | The page read does not state what is restored or where files live (unverified) |
| Gemini CLI | Conversation, tool inputs and outputs, token usage stats, auto-saved per project under `~/.gemini/tmp/<hash>/chats/` ([sessions][gem-sessions]) | 30-day default cleanup; `maxSessionTurns` default unlimited. The page notes Gemini CLI was replaced by Antigravity CLI for unpaid and Google One users from 2026-06-18 |
| OpenCode | A local database path is documented (`opencode debug paths db`, `OPENCODE_DB`) ([CLI][oc-cli]) | Resume behaviour unverified: the CLI page documents no resume flags, and the harness matrix records sessions living in a shared background server |
| Temporal | Event history ([workflow execution][temporal-we]); worker replays it, so workflow code must be deterministic | An activity heartbeat can carry a progress payload that the next attempt reads ([activity failures][temporal-af]) |
| DBOS | Workflow inputs and step outputs in Postgres, as a library ([architecture][dbos-arch]) | Steps must be idempotent; non-determinism belongs inside steps |
| Restate | Journal held by a Restate server in front of stateless services ([durable execution][restate-de]) | Idempotency keys dedupe requests; retries use backoff |
| Inngest | Memoized step results keyed by step ID ([execution][inngest-ex]) | Code outside `step.run()` can run again on replay; a step that had not saved before a crash likely reruns |

Reading it: harness resume gives continuity of **context**, not of **side effects**; an interrupted action is dropped or must be re-asked. Engines give exactly-once-per-step semantics only if steps are idempotent and replayed code is deterministic, which LLM calls are not, so they belong inside recorded steps. Hybrid use (an engine wrapping `claude -p` calls) is an inference from these two properties, not something either vendor documents.

### Watchdog and liveness design

The mechanisms below are each documented; the composition is this corpus's synthesis, not a vendor recipe.

| Failure | Signal that catches it | Documented building block |
|---|---|---|
| Hung or crashed worker | No heartbeat within a window | Temporal Heartbeat Timeout fails the attempt and retries per policy ([activity failures][temporal-af]) |
| Runaway loop or spend | Hard cap | Claude Code `-p` `--max-turns` (no limit by default) and `--max-budget-usd` (client-side estimate; can overshoot, subagent spend counts) ([CLI][cc-cli]); Gemini `maxSessionTurns` |
| Waiting on a prompt nobody sees | Run state, not exit code | Cloud scheduled-task runs (formerly routines) stop for ask rules and repeated auto-mode blocks ([routines](../../cc-native/ci-remote/CC-web-scheduled-tasks-analysis.md#permission-posture-in-unattended-runs)) |
| Green but idle or wrong | Output check, not status | The scheduled-tasks docs say a green run status does not mean the task succeeded ([CC-goal-analysis.md](../../cc-native/sessions/CC-goal-analysis.md) quotes it); see also the green-run entries in [AGENT_LEARNINGS.md](../../../AGENT_LEARNINGS.md); the watchdog must be independent of the component it watches ([silent-failure taxonomy](../../sdlc-lcm/agent-silent-failure-taxonomy-analysis.md#the-5-pillar-defense-framework)) |

Design rules that follow: put the liveness check outside the agent process; make the monitor fail on any outcome it did not expect (the corpus's third occurrence of a green no-op); pair every cap with a defined stop state that a person or a resume can pick up. Keep-alive for the host itself is a separate layer: [CC-session-keepalive-analysis.md](../../cc-native/sessions/CC-session-keepalive-analysis.md).

### Long-run failure evidence

Four October 2026 preprints, abstract pages read 2026-11-18; all single-source and unreviewed, so they are leads on mechanism, not settled rates.

- [AgentTime][arx-agenttime]: 222 tasks, duration-following. Reports Fable 5.1 in Claude Code missing requested runtimes by a typical 2.9x against 1.2x for GPT-6 Astra in Codex, and 14 of 158 reviewed Astra runs sleeping after apparently finishing. Matching a duration is not proof of work, which is the green-but-idle case in benchmark form.
- [Loud Failures, Quiet Failures][arx-quiet]: across 1,920 fault-injected trials, agents flagged a problem in 91.3% of explicit-error cases but 58.8% when a tool returned a plausible wrong value; a "check each result" prompt did not help. Supports detection outside the agent.
- [Sentry][arx-sentry]: a layer beside the agent that detects failure, retrieves matching lessons from an external playbook and keeps a lesson only after verified recovery; the authors report gains over runtime-intervention baselines (vendor-of-the-paper numbers, not reproduced here).
- [Transect][arx-transect]: observability tooling for 13-million-token evaluation runs; relevant as a trace-review aid, with no resume or liveness mechanism.

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

- [CC-dynamic-workflows-analysis.md](../../cc-native/agents-skills/CC-dynamic-workflows-analysis.md) — Claude Code's own Workflow tool (these patterns in a deterministic JS script)
- [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) — §1 orchestration frameworks, §8 output validation / guardrails
- [agentic-engineering-disciplines-landscape.md](../../sdlc-lcm/agentic-engineering-disciplines-landscape.md) — flow / loop engineering as disciplines

## Sources

| Source | Content |
|---|---|
| [Anthropic — Building Effective Agents][anthropic-bea] | Workflows-vs-agents; the 5 composable patterns |
| [Temporal][temporal] · [Inngest][inngest] · [Restate][restate] | Durable-execution engines |
| [Temporal workflow execution][temporal-we] · [activity failures][temporal-af] · [DBOS architecture][dbos-arch] · [Restate durable execution][restate-de] · [Inngest execution][inngest-ex] | Engine recovery and heartbeat semantics (2026-11-18) |
| [CC sessions][cc-sessions] · [CC CLI][cc-cli] · [Codex commands][codex-cmds] · [Gemini sessions][gem-sessions] · [OpenCode CLI][oc-cli] | Harness resume and caps (2026-11-18) |
| [AgentTime][arx-agenttime] · [Loud/Quiet Failures][arx-quiet] · [Sentry][arx-sentry] · [Transect][arx-transect] | Long-run failure preprints (abstract pages, 2026-11-18) |
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
[temporal-we]: https://docs.temporal.io/workflow-execution
[temporal-af]: https://docs.temporal.io/encyclopedia/detecting-activity-failures
[dbos-arch]: https://docs.dbos.dev/architecture
[restate-de]: https://docs.restate.dev/concepts/durable_execution
[inngest-ex]: https://www.inngest.com/docs/learn/how-functions-are-executed
[cc-sessions]: https://code.claude.com/docs/en/sessions
[cc-cli]: https://code.claude.com/docs/en/cli-reference
[codex-cmds]: https://learn.chatgpt.com/docs/developer-commands?surface=cli
[gem-sessions]: https://geminicli.com/docs/cli/session-management/
[oc-cli]: https://opencode.ai/docs/cli/
[arx-agenttime]: https://arxiv.org/abs/2610.09944
[arx-quiet]: https://arxiv.org/abs/2610.10062
[arx-sentry]: https://arxiv.org/abs/2610.02994
[arx-transect]: https://arxiv.org/abs/2610.08364
