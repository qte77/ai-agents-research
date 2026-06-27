---
title: CC Output Verification Methods
purpose: How to verify/validate Claude Code's own agentic outputs — across dynamic workflows, agent teams, subagents, plan mode, and memory — using hooks, structured-output schemas, and headless asserts.
category: analysis
created: 2026-06-27
updated: 2026-06-27
validated_links: 2026-06-27
---

**Status**: Adopt

## What It Is

The repo has evaluation *landscapes* (metrics, tools) but no guide on verifying Claude Code's **own mechanism outputs**. This doc maps each CC agentic mechanism to its verification surface. Three through-lines:

- **Hooks are the deterministic backbone** — they run regardless of what the model decides.
- **Structured output schema-validates the final result** — a programmatic pass/fail signal.
- **There is no first-party eval runner** — verification is DIY (headless pipe + your own asserts, optionally an adversarial re-check).

All mechanism facts below are first-party verified against the CC hooks / agent-teams / CLI / Agent-SDK / memory docs (2026-06-27).

## Verify matrix (mechanism → surface)

| Mechanism | Primary verification surface | Note |
|---|---|---|
| **Dynamic workflow** | Script-level adversarial-verify stage; `/deep-research` per-claim voting | The workflow script can spawn skeptic subagents per finding |
| **Agent team** | `TaskCompleted` / `TeammateIdle` hooks (block incomplete work); a reviewer teammate | Team hooks gated behind `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` |
| **Subagent** | Structured-output schema (`--json-schema` / SDK `outputFormat`) + `SubagentStop` hook | `SubagentStop` exit 2 keeps the subagent working |
| **Plan** | Human approval at the plan-mode UI gate (**not** a hook) | Programmatic gating → intercept `Stop` + parse the transcript |
| **Memory** | `/memory` audit; `PreToolUse` hook for must-always rules | `CLAUDE.md` loads as a *user message* — context, not enforced |

## Hooks: the deterministic backbone

Block-capable hook events feed your stderr back to the model and stop the action on **exit 2**:

- **`Stop`** — fires when the main turn ends; exit 2 prevents stopping and forces another turn (the re-verify gate). A JSON `additionalContext` path can feed context back *without* framing it as an error.
- **`SubagentStop`** — fires when a subagent finishes; exit 2 keeps it running with your feedback (verify a subagent's result before it returns).
- **`TaskCreated` / `TaskCompleted` / `TeammateIdle`** — agent-team gates (experimental flag): exit 2 rolls back a task creation, blocks a premature "complete", or keeps an idle teammate working. *(The `team_name` payload field is deprecated as of v2.1.178 — it now carries a session-derived name.)*

**Exit 2 is not uniform** — assert this precisely:

| Hook class | Exit 2 |
|---|---|
| Blocking (`Stop`, `SubagentStop`, `PreToolUse`, `TaskCompleted`, `TeammateIdle`, `TaskCreated`) | Blocks the action + stderr → model |
| `PostToolUse` | Does **not** block; stderr → model |
| Info-only (`SessionStart`, `Notification`, `CwdChanged`, …) | Does **not** block; stderr → **user only** |
| `PostToolUseFailure`, `StopFailure`, `WorktreeRemove` | Exit code + output **ignored** |

Cross-ref: [CC-hooks-system-analysis.md](../configuration/CC-hooks-system-analysis.md) for the full event table; [CC-ralph-enhancement-research.md](CC-ralph-enhancement-research.md) for the Stop-hook re-verify pattern; [CC-agent-teams-orchestration.md](CC-agent-teams-orchestration.md) for the team gates.

## Structured output: schema-validate the result

Headless schema validation is the **`--json-schema`** flag — *not* `--output-format json` (which only serializes turn messages; the two are unrelated):

```bash
claude -p --json-schema '{"type":"object","properties":{...}}' "query"   # validated final output, print mode
```

SDK equivalents: TS `outputFormat: { type: "json_schema", schema: {...} }`; Python `output_format={"type":"json_schema","schema":{...}}`.

**The programmatic fail signal** is the result-message **`subtype`**: `success` vs **`error_max_structured_output_retries`** (no schema-valid output after the retry limit). Check `msg.subtype` directly — this is your deterministic "the agent's output is invalid" assertion.

Cross-ref: [CC-cli-reference.md](../configuration/CC-cli-reference.md) (`--json-schema`, print-mode only).

## Plan mode

The verification point is the **interactive approval gate** when Claude presents the plan (auto / accept-edits / review manually / keep planning). There is **no `ExitPlanMode` hook event** — plan approval is a TUI interaction, not a lifecycle hook. To gate plan *content* programmatically, intercept `Stop` (the planning turn's end) and parse the transcript; there is no dedicated plan-approval hook. Entry points: `/plan` prefix and `--permission-mode plan`.

## Memory

`CLAUDE.md` is delivered as a **user message after the system prompt** — Claude reads and tries to follow it, but "there's no guarantee of strict compliance." So:

- **Must-always rules** → a **`PreToolUse` hook** (blocks the action regardless of what the model decides), *not* a CLAUDE.md line.
- System-prompt-level injection → `--append-system-prompt` per invocation (does **not** persist — script-oriented).
- Audit what's loaded with `/memory`.

## No first-party eval runner → DIY

There is **no built-in general eval runner** and no native promptfoo / DeepEval / Inspect integration (skill-creator's "run evals" is skill-specific). The documented pattern is DIY:

1. Pipe `claude -p` headless output into your own assertion scripts.
2. Use `--json-schema` (or SDK `outputFormat`) for a schema-validatable result + the `error_max_structured_output_retries` fail signal.
3. Add an **adversarial review step** — spawn a second session to critique the first's output (per CC best practices).

**Deterministic asserts and hooks beat LLM-judge** wherever the property is checkable. Report gaps via `/feedback`.

## Cross-References

- [CC-dynamic-workflows-analysis.md](CC-dynamic-workflows-analysis.md) — workflow-script verify stages + `/deep-research` claim voting
- [CC-agent-teams-orchestration.md](CC-agent-teams-orchestration.md) — `TaskCompleted` / `TeammateIdle` quality gates
- [CC-hooks-system-analysis.md](../configuration/CC-hooks-system-analysis.md) — hook events + exit-code semantics
- [agent-evaluation-metrics-landscape.md](../../sdlc-lcm/agent-evaluation-metrics-landscape.md) · [evaluation-data-resources-landscape.md](../../sdlc-lcm/evaluation-data-resources-landscape.md) — the metrics/tooling layer this CC-mechanism guide sits above

## Sources

| Source | Content |
|---|---|
| [CC hooks reference][cc-hooks] | Hook events; non-uniform `exit 2` semantics |
| [CC agent teams][cc-teams] | `TaskCreated`/`TaskCompleted`/`TeammateIdle` gates; experimental flag |
| [CC CLI reference][cc-cli] | `--json-schema` (print-mode validated output) |
| [Agent SDK — structured outputs][cc-sdk-struct] | `outputFormat` + `error_max_structured_output_retries` subtype |
| [CC memory][cc-memory] | CLAUDE.md as user message; `PreToolUse` for enforcement |
| [CC best practices][cc-bp] | Adversarial-review step (DIY verification) |
| CC mechanism facts, claude-code-guide verification, 2026-06-27 | First-party confirmation (no URL) |

[cc-hooks]: https://code.claude.com/docs/en/hooks
[cc-teams]: https://code.claude.com/docs/en/agent-teams
[cc-cli]: https://code.claude.com/docs/en/cli-reference
[cc-sdk-struct]: https://code.claude.com/docs/en/agent-sdk/structured-outputs
[cc-memory]: https://code.claude.com/docs/en/memory
[cc-bp]: https://code.claude.com/docs/en/best-practices
