---
title: CC Dynamic Workflows, Ultracode & deep-research
source: https://code.claude.com/docs/en/workflows
purpose: Document Claude Code's dynamic workflow orchestration tool, the ultracode effort setting, and the bundled /deep-research workflow, with first-party sourcing.
created: 2026-06-11
updated: 2026-06-11
validated_links: 2026-06-11
---

**Status**: Trial (GA since CC v2.1.154; paid plans + API/Bedrock/Vertex/Foundry)

## What It Is

A **dynamic workflow** is a JavaScript script that orchestrates [subagents][cc-subagents] at scale — "Claude writes the script for the task you describe, and a runtime executes it in the background while your session stays responsive" ([workflows][cc-workflows]). The loop, branching, and intermediate results live in the script, so only the final answer returns to Claude's context. Built for codebase-wide audits, large (500-file) migrations, and cross-checked research.

Surfaced as the feature-gated `WorkflowTool` (`WORKFLOW_SCRIPTS` flag) in [CC-tools-inventory.md](../configuration/CC-tools-inventory.md); this doc is the first-party-documented analysis of that tool.

**Availability**: CC **v2.1.154+**, all paid plans, plus Anthropic API, Bedrock, Vertex AI, and Foundry. On Pro, enable via the *Dynamic workflows* row in `/config` ([workflows][cc-workflows]).

## When to Use vs Subagents / Skills / Agent Teams

The dividing line is **who holds the plan** ([workflows][cc-workflows]):

| | Subagents | Skills | Agent teams | Workflows |
|---|---|---|---|---|
| What it is | A worker Claude spawns | Instructions Claude follows | A lead agent supervising peers | A script the runtime executes |
| Who decides next | Claude, turn by turn | Claude, per prompt | The lead agent | The script |
| Intermediate results | Context window | Context window | Shared task list | Script variables |
| Scale | A few per turn | Same | A handful of peers | Dozens–hundreds per run |
| Interruption | Restarts turn | Restarts turn | Teammates keep running | Resumable in session |

Moving the plan into code also lets a workflow apply a repeatable **quality pattern** — e.g. independent agents adversarially reviewing each other's findings before they are reported.

## The Workflow Tool & Script API

Invoke a saved workflow as `Workflow({ scriptPath, args })`, or have Claude author one for a task. The runtime provides these script primitives ([workflows][cc-workflows]):

- `agent()` — spawn a subagent (optionally structured-output / model / worktree)
- `parallel()` — barrier: run thunks concurrently, await all
- `pipeline()` — run items through stages with no barrier between stages
- `phase()`, `log()` — progress grouping and narration
- `budget` — the run's token target
- `meta` export — name / description / phases (required script header)

**Saving & args**: `/workflows` → `s` saves a run's script to `.claude/workflows/` (project, shared) or `~/.claude/workflows/` (personal); project beats personal on a name clash. Saved workflows run as `/<name>`. Input is passed via the `args` parameter and read inside the script as the `args` global (structured data, not a string).

**Execution model**: the runtime runs the script in an isolated environment; intermediate results stay in script variables; the script is written to a file under `~/.claude/projects/` (readable/editable). Runs are **resumable within the same session** (completed agents return cached results); exiting CC restarts a running workflow fresh next session.

**Limits** ([workflows][cc-workflows]): no mid-run user input (only agent permission prompts pause it); no direct filesystem/shell from the script itself (agents do that); **up to 16 concurrent agents**; **1,000 agents total per run**. Spawned subagents always run in `acceptEdits` and inherit the tool allowlist regardless of session mode.

## Ultracode (effort setting)

`ultracode` is "a Claude Code setting rather than a model effort level: it sends `xhigh` to the model and additionally has Claude orchestrate dynamic workflows for substantive tasks" ([model config — effort][cc-effort]). Set with `/effort ultracode`; **session-only** (resets on a new session — `/effort high` to drop back). With it on, "a single request can turn into several workflows in a row: one to understand the code, one to make the change, and one to verify it" ([workflows][cc-workflows]).

It is **not** part of `effortLevel` in settings.json, the `--effort` flag, or `CLAUDE_CODE_EFFORT_LEVEL`; it can be passed as `"ultracode": true` via `--settings` or an Agent SDK control request ([model config — effort][cc-effort]). Requires a model that supports `xhigh` (Fable 5, Opus 4.8/4.7).

**Keyword trigger** (single task, without changing session effort): include `ultracode` in a prompt — or just ask "use a workflow". Before v2.1.160 the literal keyword was `workflow`. Disable via *Ultracode keyword trigger* in `/config`. Distinct from `ultrathink` (one-off deeper reasoning — no workflow, no effort change).

## Bundled Workflow: /deep-research

The one built-in workflow Claude Code ships ([bundled workflows][cc-bundled]):

> `/deep-research <question>` — Fans out web searches on a question across several angles, fetches and cross-checks the sources it finds, votes on each claim, and returns a cited report with claims that didn't survive cross-checking filtered out. Requires the [WebSearch tool][cc-tools-ref] to be available.

**Workflow vs harness**: `/deep-research` is the **only** bundled workflow Claude Code currently ships, and it is a *workflow* — not a skill. "Harness" describes its *pattern* (fan-out → cross-check → vote → synthesize), not its mechanism; the mechanism is a dynamic workflow. A project may also define a same-named custom `deep-research` **skill** that labels itself a "harness" and mirrors the behavior, but the first-party artifact is the bundled workflow.

## Managing Runs (`/workflows`)

Runs execute in the background, so the session stays responsive. Run `/workflows` to **list running and completed runs** and open a progress view showing each phase with its agent count, token total, and elapsed time; a one-line summary also appears in the task panel below the input box ([watch the run][cc-watch]).

Progress-view controls ([watch the run][cc-watch]):

| Key | Action |
|---|---|
| `↑` / `↓` | Select a phase or agent |
| `Enter` / `→` | Drill into a phase, then an agent (its prompt, recent tool calls, result) |
| `Esc` | Back out one level |
| `j` / `k` | Scroll within the agent detail |
| `p` | Pause or resume the run |
| `x` | Stop the selected agent, or the whole workflow |
| `r` | Restart the selected running agent |
| `s` | Save the run's script as a `/<name>` command |

**Resume** is **same-session only**: a paused or stopped run resumes with completed agents returning cached results and the rest running live (select it and press `p`, or ask Claude to relaunch). Exiting Claude Code restarts a running workflow fresh in the next session ([manage runs][cc-manage]).

## Disabling

Workflows run in the CLI, Desktop, IDE extensions, headless (`claude -p`), and the [Agent SDK][cc-agent-sdk]. Disable via *Dynamic workflows* off in `/config`, `"disableWorkflows": true` in settings, or `CLAUDE_CODE_DISABLE_WORKFLOWS=1`. When disabled, bundled workflow commands are unavailable, the `ultracode` keyword stops triggering, and `ultracode` is removed from the `/effort` menu ([workflows][cc-workflows]).

## Relevance to this repo

- **Doc audits at scale** — a workflow could fan the `enforcing-doc-hierarchy` audit across all of `docs/` in one resumable run instead of turn-by-turn (Fork-Join ≈ `parallel()`, Context-Isolated Subagents ≈ `agent()` — see [CC-agentic-harness-patterns-analysis.md](CC-agentic-harness-patterns-analysis.md)).
- **Cross-checked research** — `/deep-research` is the canonical fan-out → verify → synthesize pattern this research catalog depends on.
- **Cost discipline** — a run can spend meaningfully more tokens than a conversation; the docs advise scoping to one directory / narrow question first and watching `/workflows` token totals.

## Cross-References

- [CC-tools-inventory.md](../configuration/CC-tools-inventory.md) — `WorkflowTool` / `WORKFLOW_SCRIPTS` feature gate (leak-derived name)
- [CC-agentic-harness-patterns-analysis.md](CC-agentic-harness-patterns-analysis.md) — harness patterns that map to `parallel()` / `agent()`
- [CC-agent-teams-orchestration.md](CC-agent-teams-orchestration.md) — the agent-teams alternative (a lead agent holds the plan)
- [CC-plans-as-skill-rule-templates.md](CC-plans-as-skill-rule-templates.md) — UltraPlan (cloud planning), a separate "ultra" feature
- [CC-skills-adoption-analysis.md](CC-skills-adoption-analysis.md) — skills, the lighter alternative

## Sources

| Source | Content |
|---|---|
| [Dynamic workflows][cc-workflows] | Workflow tool, script API, ultracode triggers, limits, disabling |
| [Bundled workflows][cc-bundled] | The `/deep-research` table + walkthrough |
| [Watch the run][cc-watch] | `/workflows` progress view + key controls |
| [Manage runs][cc-manage] | Resume / pause / stop after launch |
| [Model configuration — effort][cc-effort] | ultracode effort setting definition and constraints |
| [Subagents][cc-subagents] | The worker primitive workflows orchestrate |
| [Run agents in parallel][cc-agents] | Subagents vs skills vs teams vs workflows |
| [Agent SDK overview][cc-agent-sdk] | Workflows on the SDK surface |
| [Tools reference — WebSearch][cc-tools-ref] | `/deep-research` dependency |

[cc-workflows]: https://code.claude.com/docs/en/workflows
[cc-bundled]: https://code.claude.com/docs/en/workflows#bundled-workflows
[cc-watch]: https://code.claude.com/docs/en/workflows#watch-the-run
[cc-manage]: https://code.claude.com/docs/en/workflows#manage-runs
[cc-effort]: https://code.claude.com/docs/en/model-config#adjust-effort-level
[cc-subagents]: https://code.claude.com/docs/en/sub-agents
[cc-agents]: https://code.claude.com/docs/en/agents
[cc-agent-sdk]: https://code.claude.com/docs/en/agent-sdk/overview
[cc-tools-ref]: https://code.claude.com/docs/en/tools-reference#websearch-tool-behavior
