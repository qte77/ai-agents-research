---
title: Agentic Workflow Frameworks — Landscape
purpose: The workflows-vs-agents distinction (Anthropic's 5 patterns), agentic-workflow frameworks, durable-execution engines and production anti-patterns, beyond Claude Code's own workflow tool.
created: 2026-06-27
updated: 2026-11-27
validated_links_on: 2026-11-25
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

| Framework | Stars (2026-11-26) | Control flow | Durable? |
|---|---|---|---|
| [LangGraph][langgraph] | 45.5K | graph (DAG + agentic) | checkpointers |
| [CrewAI][crewai] | 61.3K | roles + flows | app-level only |
| [Langflow][langflow] | 157.0K | visual DAG builder | no |
| [Mastra][mastra] | 29.8K | TS workflows + agents | suspend/resume |
| [Burr][burr] | 2.6K | explicit state-machine DAG | persisters |
| [Conductor (OSS)][conductor] | 32.5K | server-orchestrated DAG | yes (server-side) |
| [Prefect][prefect] | 24.2K (2026-11-25) | Python flows; data/workflow orchestrator | not assessed |
| [Dagster][dagster] | 16.5K (2026-11-25) | asset-based pipelines; data orchestrator | not assessed |
| [Apache Airflow][airflow] | 47.7K (2026-11-25) | Python-defined DAGs; scheduler | not assessed |

LangGraph/CrewAI detail lives in the catalog — cross-referenced, not duplicated. The last three rows are data/workflow orchestrators that predate LLM agents; their durability was not assessed here, and the section below covers only their AI surfaces.

### Data orchestrators with an AI surface (2026-11-25)

All three are Apache-2.0 (repo LICENSE as reported by the GitHub API); stars, versions and dates were read on 2026-11-25. Evidence level is "documented" unless noted. For the Model Context Protocol (MCP) see [glossary](../../glossary.md); HITL below means a human approval pause.

| Engine | Latest release | AI / agent surface |
|---|---|---|
| Prefect | 3.9.5 (2026-11-24) | **FastMCP** ([PrefectHQ/fastmcp][fastmcp], Apache-2.0, 28.7K stars, v4.2.6) is a Prefect-org library for building MCP servers and clients. **prefect-mcp-server** ([repo][pf-mcp], MIT, 56 stars) gives MCP clients read-only tools over flows, runs, deployments and logs; its README calls it experimental and subject to drastic change. **Marvin** (v3.3.0, 6.2K stars) is built on Pydantic AI, see [agent-frameworks catalog § Structured output](agent-frameworks-infrastructure-landscape.md#structured-output--schema-enforcement). ControlFlow is archived (last release v0.12.1, 2025-02-06) |
| Dagster | 1.13.31 (2026-11-19) | **Dagster+ MCP server**: docs call it beta and Dagster+-only (plan tiers not stated); it can launch runs, materialize assets, fetch logs and Insights metrics. The [dagster-io/skills][dg-skills] plugin (Apache-2.0, 219 stars) bundles that MCP server with Dagster agent skills; its README lists Claude Code, Cursor, OpenAI Codex, GitHub Copilot, OpenCode and Pi. Integrations: `dagster-openai` is labelled Dagster-supported; `dagster-anthropic` (an `AnthropicResource`) is labelled community-maintained |
| Apache Airflow | 3.4.0 (2026-11-06) | **common-ai provider** 1.2.0 (2026-11-23, Apache-2.0, needs Airflow >= 2.11): `@task.llm`, tool-using agents as tasks, batch operator, HITL approval (on Airflow 3.3+ a parked task holds no worker slot; on 3.1 and 3.2 it stays running and polls); built on pydantic-ai. PyPI classifies it Production/Stable, but its stability page marks some features experimental (for example `decision_policy`). `anthropic` provider 1.2.1 (needs Airflow >= 3.0: batch operator, batch sensor, Managed Agents session operator); `openai` provider 2.2.0 (embedding, Responses and Batch operators). **No official Apache Airflow MCP server found** (see caveat). `astronomer/airflow-ai-sdk` (525 stars, v0.1.8) is **archived** (last push 2026-07-01) |

Caveat on the Airflow MCP absence: searched the `apache` GitHub org's repository names for "mcp" (11 other-project servers, none for Airflow), the `apache/airflow` providers directory, and GitHub search for "airflow mcp server". The community servers found there (for example `yangkyeongmo/mcp-server-apache-airflow`, 183 stars; `astronomer/astro-airflow-mcp`, 13 stars, archived) are not Apache projects. The airflow.apache.org nav and PyPI were not exhaustively searched (PyPI search page failed to load), so this is "none found", not "none exists".

## Durable execution (the layer the catalog omits)

When a workflow must survive process crashes, provider timeouts, or human-in-the-loop pauses lasting hours, **durable-execution engines** persist each step so a fresh process resumes from the last checkpoint. The pattern mainstreamed across AWS / Cloudflare / Vercel in late 2025.

| Engine | Stars (2026-11-26) | Model |
|---|---|---|
| [Temporal][temporal] | 24.6K (MIT) | workflows-as-code; deterministic replay from an event history |
| [Inngest][inngest] | 6.1K | event-driven durable functions with built-in flow control |
| [Restate][restate] | 4.7K | durable execution + virtual objects; low-latency |

The core primitive is idempotency on a stable **`(workflow_id, step_id)`** key — so a replayed step is a no-op, not a duplicated side-effect.

### Checkpoint and resume matrix

Added 2026-11-18, each row from the vendor's docs fetched that day; the rows from GitHub Copilot CLI to Windsurf were added and the Codex CLI, Gemini CLI and OpenCode rows re-checked on 2026-11-27, again from the vendors' own pages (and, for the two open-source harnesses, source at a named release tag). "Not documented on the pages read" means exactly that, not that the feature is absent. Resume flags per harness are in [CC-agentic-harness-patterns-analysis.md § Cross-Harness Matrix](../../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#cross-harness-matrix-checked-2026-11-15); this table adds only what is saved, what bounds it and what is not restored. The two families differ in kind: a harness resumes a **transcript** (the model re-reads history), an engine resumes **code** (steps replay from a journal).

| System | Unit saved | Bound / not restored |
|---|---|---|
| Claude Code | Local JSONL transcript per session ([sessions][cc-sessions]); restores history, model, agent, permission mode (terminal), active goal (counters reset), unexpired session-scoped schedules | A tool running when the process died is not rerun. Background Bash and monitors are not restored. Model Context Protocol (MCP), plugin, `--add-dir` and settings flags must be passed again. 30-day default retention. Resuming one session in two terminals makes both write to one transcript, and messages can be missing on a later resume |
| Codex CLI | Session rollout files, JSONL, `rollout-<timestamp>-<id>.jsonl` under `sessions/` and `archived_sessions/` of the Codex home (source at tag `rust-v0.172.0`, [recorder.rs][cx-rec], [lib.rs][cx-lib]); `codex resume`, `codex fork`, `codex archive` and `codex delete` act on saved sessions, `codex exec resume --last` for non-interactive runs; `--ephemeral` skips persisting ([commands][codex-cmds]; harness: [codex-cli-analysis.md](../coding-agents/codex-cli-analysis.md)) | What a resume restores (tool state, approvals, files) is not documented on the command page read, and no file rewind is documented there. Fork keeps the original transcript. Archive hides a session from the picker without deleting it; delete is permanent. No retention period is documented on the page read |
| Gemini CLI | Conversation, tool inputs and outputs, token usage stats, auto-saved per project under `~/.gemini/tmp/<hash>/chats/`; `gemini --resume` (latest, by index or by ID) or `/resume`, plus named chat checkpoints with `/resume save <tag>` ([sessions][gem-sessions]; harness: [gemini-cli-analysis.md](../coding-agents/gemini-cli-analysis.md)) | Resume restores prior context per the page. 30-day default cleanup (`sessionRetention.maxAge`, `maxCount` unlimited by default, 1-day `minRetention`); `maxSessionTurns` default unlimited. The page notes Gemini CLI was replaced by Antigravity CLI for unpaid and Google One users from 2026-06-18. A separate Rewind page exists in the docs navigation and was not read |
| OpenCode | Sessions live in a local database (`opencode debug paths db`, `OPENCODE_DB`) owned by a shared background server by default ([CLI][oc-cli]). `/sessions` returns to a session; `/undo` and `/redo` revert and restore the last message and the work after it ([TUI][oc-tui]); at tag `v1.19.6` the docs source lists `--continue`, `--session` and `--fork` and `opencode session list/delete` ([cli.mdx][oc-src]; harness: [opencode-analysis.md](../coding-agents/opencode-analysis.md)) | The live [Commands page][oc-cmds-live] (OpenCode v2) documents `opencode run --continue` and `--session`, `opencode session list` and `opencode session delete`; `--fork` is verified only at that v1 tag. At the same tag `session/revert.ts` restores file patches through a snapshot, so `/undo` covers files as well as messages (source reading). No retention period documented on the pages read; the CLI page says uninstalling never removes session data |
| GitHub Copilot CLI | A per-session subdirectory under `~/.copilot/session-state/`, plus a session store file (`~/.copilot/session-store.db`); `copilot --continue`, `--resume [ID]`, `/resume` ([session data][cop-chron]; harness: [github-copilot-cli-analysis.md](../agents/github-copilot-cli-analysis.md)) | Resume loads the full conversation history and restores the session's approvals and denials for commands, tools, URLs and file paths (directory approvals, policy-granted approvals and approvals granted automatically by the safety review are not). `/rewind` rolls back to an earlier turn, conversation only or with files, tracked per turn without Git, and cannot be undone. A session open when the process died can be offered for restore at the next start, opt-in via `COPILOT_ENABLE_INTERRUPTED_SESSION_RESTORE=1`; a mid-turn session then resumes its work ([reference][cop-ref]). No automatic expiry documented on the pages read; `/session prune --older-than DAYS` and `delete` are manual |
| VS Code Copilot Chat | A session groups workspace, code changes and one or more chats, each with its own history; archived or done sessions are filtered out of the active list and restored before a follow-up ([manage sessions][vsc-sess]; harness: [vscode-copilot-chat-analysis.md](../coding-agents/vscode-copilot-chat-analysis.md)) | Restore Checkpoint restores affected workspace files and removes later turns; Undo on pending edits reverts files without rewinding the conversation. Checkpoints do not reverse completed terminal commands, network requests or external services, and Undo does not track terminal-made changes ([review edits][vsc-ckpt]). `/fork` copies the conversation. The page marks the Local harness deprecated (removal February 2027) and cloud sessions experimental. Where chat history is stored and its retention are not documented on the pages read |
| Cursor | CLI: `agent ls`, `agent resume`, `agent --continue`, `agent --resume=<id>` ([CLI][cur-cli]); IDE agent sessions with checkpoints ([agent][cur-agent]; harness: [cursor-analysis.md](../coding-agents/cursor-analysis.md)) | Checkpoints snapshot modified files before significant changes, are stored locally apart from Git, and restoring reverts files only, not the messages. What a CLI resume restores, where chats are stored and retention are not documented on the pages read |
| Cline | Each task is saved locally with its full conversation and a dedicated storage directory; resumable from the History view across sessions ([tasks][cline-task]; harness: [cline-analysis.md](../coding-agents/cline-analysis.md)) | Resuming loads the conversation and checks file states against checkpoints. Checkpoints use a shadow Git repository committed after each tool use, on by default, and restore offers Files, Task only, or Files and Task ([checkpoints][cline-ck]); the page warns of storage use on very large repositories. Favourited tasks are protected from deletion; a retention period is not documented on the pages read |
| Aider | Chat transcript appended to `.aider.chat.history.md` and input history to `.aider.input.history` by default; `--restore-chat-history` reloads previous messages, default off ([options][aider-opt]; harness: [aider-analysis.md](../coding-agents/aider-analysis.md)) | No session list or resume command is documented on the pages read. Aider's file recovery is Git: `/undo` reverts the last commit if aider made it ([commands][aider-cmd]). What a restored history contains beyond messages is not documented on the pages read; no retention policy is documented |
| Amp | A thread (prompts, replies, every tool call, files changed) with a URL, usable from any device (so stored by Amp, implied by the page rather than stated): `amp threads continue T-…`; a long thread can be handed off by asking the agent to start a fresh thread with the context that matters ([threads][amp-th]; harness: [amp-analysis.md](../coding-agents/amp-analysis.md)) | Threads running in an orb continue there; a thread started in the CLI stays open on the web. Threads archived in the last 72 hours sit behind the sidebar's archive button; every archived thread stays in Activity under the Archived status and its URL keeps working. A file rewind is not documented on the page read, and a retention period is not stated in the text read |
| Windsurf (Devin Desktop) | The Cascade agent kept conversations with named checkpoints and reverts ([Cascade legacy][ws-cas]; harness: [windsurf-analysis.md](../coding-agents/windsurf-analysis.md)) | The page calls Cascade the legacy agent: Devin Desktop starts no new Cascade conversations and no longer opens old ones. Reverts are stated to be irreversible. Devin Local, the replacement, was not read, so its resume behaviour is not documented here |
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
| [Codex recorder][cx-rec] · [Codex lib][cx-lib] · [OpenCode TUI][oc-tui] · [OpenCode cli.mdx][oc-src] · [Copilot CLI session data][cop-chron] · [Copilot CLI reference][cop-ref] · [VS Code sessions][vsc-sess] · [VS Code review edits][vsc-ckpt] · [Cursor CLI][cur-cli] · [Cursor agent][cur-agent] · [Cline tasks][cline-task] · [Cline checkpoints][cline-ck] · [Aider options][aider-opt] · [Aider commands][aider-cmd] · [Amp threads][amp-th] · [Windsurf Cascade (legacy)][ws-cas] | Session and resume rows added or re-checked (2026-11-27) |
| [AgentTime][arx-agenttime] · [Loud/Quiet Failures][arx-quiet] · [Sentry][arx-sentry] · [Transect][arx-transect] | Long-run failure preprints (abstract pages, 2026-11-18) |
| [Prefect][prefect] · [Dagster][dagster] · [Airflow][airflow] · [FastMCP][fastmcp] · [prefect-mcp-server][pf-mcp] · [dagster-io/skills][dg-skills] · [Airflow common-ai][af-ai] · [Airflow anthropic][af-anth] · [Airflow openai][af-oai] · [Dagster+ MCP][dg-mcp] · [Dagster anthropic][dg-anth] · [Dagster openai][dg-oai] | Data-orchestrator AI surfaces (`gh api`, PyPI, vendor docs, 2026-11-25) |
| [LangGraph][langgraph] · [CrewAI][crewai] · [Langflow][langflow] · [Mastra][mastra] · [Burr][burr] · [Conductor (OSS)][conductor] | Workflow / orchestration frameworks (stars via `gh api`, 2026-11-26) |

[anthropic-bea]: https://www.anthropic.com/research/building-effective-agents
[temporal]: https://github.com/temporalio/temporal
[inngest]: https://github.com/inngest/inngest
[restate]: https://github.com/restatedev/restate
[langgraph]: https://github.com/langchain-ai/langgraph
[crewai]: https://github.com/crewAIInc/crewAI
[langflow]: https://github.com/langflow-ai/langflow
[mastra]: https://github.com/mastra-ai/mastra
[burr]: https://github.com/apache/burr
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
[oc-tui]: https://opencode.ai/docs/cli/tui/
[oc-src]: https://github.com/anomalyco/opencode/blob/v1.19.6/packages/web/src/content/docs/cli.mdx
[cx-rec]: https://github.com/openai/codex/blob/rust-v0.172.0/codex-rs/rollout/src/recorder.rs
[cx-lib]: https://github.com/openai/codex/blob/rust-v0.172.0/codex-rs/rollout/src/lib.rs
[cop-chron]: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/chronicle
[cop-ref]: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
[vsc-sess]: https://code.visualstudio.com/docs/agents/run/sessions/manage-sessions
[vsc-ckpt]: https://code.visualstudio.com/docs/agents/run/review-code-edits
[cur-cli]: https://cursor.com/docs/cli/overview
[cur-agent]: https://cursor.com/docs/agent/overview
[cline-task]: https://docs.cline.bot/core-workflows/task-management
[cline-ck]: https://docs.cline.bot/core-workflows/checkpoints
[aider-opt]: https://aider.chat/docs/config/options.html
[aider-cmd]: https://aider.chat/docs/usage/commands.html
[amp-th]: https://ampcode.com/docs/threads
[ws-cas]: https://docs.devin.ai/desktop/cascade
[arx-agenttime]: https://arxiv.org/abs/2610.09944
[arx-quiet]: https://arxiv.org/abs/2610.10062
[arx-sentry]: https://arxiv.org/abs/2610.02994
[arx-transect]: https://arxiv.org/abs/2610.08364
[prefect]: https://github.com/PrefectHQ/prefect
[dagster]: https://github.com/dagster-io/dagster
[airflow]: https://github.com/apache/airflow
[fastmcp]: https://github.com/PrefectHQ/fastmcp
[pf-mcp]: https://github.com/PrefectHQ/prefect-mcp-server
[dg-skills]: https://github.com/dagster-io/skills
[af-ai]: https://airflow.apache.org/docs/apache-airflow-providers-common-ai/stable/index.html
[af-anth]: https://airflow.apache.org/docs/apache-airflow-providers-anthropic/stable/index.html
[af-oai]: https://airflow.apache.org/docs/apache-airflow-providers-openai/stable/index.html
[dg-mcp]: https://dagster.io/docs/getting-started/ai-tools/dagster-mcp
[dg-anth]: https://dagster.io/docs/integrations/libraries/anthropic
[dg-oai]: https://dagster.io/docs/integrations/libraries/openai
[oc-cmds-live]: https://opencode.ai/docs/cli/commands/
