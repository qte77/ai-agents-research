---
title: CC Advisor Tool Analysis
purpose: First-party analysis of Anthropic's advisor tool — a server-executed API beta that lets an executor model consult a stronger advisor model mid-request — and its Claude Code /advisor surface.
created: 2026-10-26
updated: 2026-10-26
validated_links: 2026-10-26
status: beta
---

**Details:** Anthropic API feature, beta; behavior, pricing, and availability may change.

## What It Is

The advisor tool is a beta Anthropic API feature (beta header `advisor-tool-2026-03-01`, tool `type: "advisor_20260301"`, `name: "advisor"`) that lets a faster **executor model** pause mid-generation and consult a stronger **advisor model**, inside a single `/v1/messages` request. The advisor receives the executor's full transcript — system prompt, tool definitions, prior turns and tool results, and the text produced so far in the current turn — runs under its own Anthropic-supplied system prompt, and "runs without tools and without context management." Its thinking blocks are dropped before the result returns; "only the advice text reaches the executor" ([advisor-tool-api]). Claude Code exposes the same mechanism as the `/advisor` slash command, layered on top of this API tool ([advisor-cc]).

The advisor "fits long, multi-step tasks where most turns are routine but plan quality determines the outcome" — large refactors, debugging sessions where an error keeps recurring, and tasks that benefit from an independent check before being declared done ([advisor-cc]).

## API mechanics

### How a call happens

1. The executor emits a `server_tool_use` block (`name: "advisor"`, empty `input`) — the executor decides timing, the server supplies the advisor's context.
2. Anthropic runs a separate advisor inference server-side against the full transcript.
3. The advice returns as an `advisor_tool_result` block; the executor continues generating.

All of this happens inside one `/v1/messages` request, with no extra round trip — the exception is a turn that pauses mid-call, resumed with a follow-up request. Sub-inference does not stream: "the advisor sub-inference does not stream" — the executor's SSE stream pauses (idle `ping` keepalives roughly every 30s) and the full `advisor_tool_result` arrives in one `content_block_start` event ([advisor-tool-api]).

### Tool parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `type` | string | required | Must be `"advisor_20260301"` |
| `name` | string | required | Must be `"advisor"` |
| `model` | string | required | Advisor model ID; billed at that model's rates |
| `max_uses` | integer | unlimited | Per-request cap on advisor calls — "not a per-conversation cap" |
| `max_tokens` | integer | advisor's output cap | Caps advisor output (thinking + text) per call; minimum 1024 |
| `caching` | object \| null | off (`null`) | `{"type": "ephemeral", "ttl": "5m" \| "1h"}` — advisor-side transcript caching |

There is no conversation-level cap built into the tool: "the advisor tool has no built-in conversation-level cap. To limit advisor calls across a conversation, count them client-side" ([advisor-tool-api]).

### Pairing summary

"The advisor must be Claude Sonnet 4.6 or a more capable model, and it must be at least as capable as the executor" — models of equal capability (e.g. Opus 4.7 and Opus 4.8) can advise each other. An invalid pair returns `400 invalid_request_error` naming the unsupported combination ([advisor-tool-api]). The published compatibility table has 14 executor rows; Claude Haiku 4.5 appears only in the executor column and never in any advisor column — it can call the advisor but the table never lists it as one, consistent with the Sonnet-4.6-or-above floor. Seven newer executors (Sonnet 5.5, Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Fable 5, Mythos 5) "pair only with advisors that return the encrypted form, so on those executors the advice text isn't readable in the response" — their accepted advisors return `advisor_redacted_result` (`encrypted_content`) rather than the plaintext `advisor_result` (`text`) that e.g. `claude-opus-4-8` returns.

### Errors

A failed call returns `advisor_tool_result_error` with one of seven `error_code` values (`max_uses_exceeded`, `too_many_requests`, `overloaded`, `prompt_too_long`, `execution_time_exceeded`, `model_not_found`, `unavailable`). "The executor receives the error and continues without further advice. The request itself does not fail" ([advisor-tool-api]).

## Billing & usage accounting

Top-level `usage` fields reflect executor tokens only. Advisor tokens appear separately in the `usage.iterations[]` array, tagged `"type": "advisor_message"` (vs. `"type": "message"` for executor iterations), each billed at the advisor model's own rates. Advisor output is "typically 400 to 700 text tokens, or 1,400 to 1,800 tokens total including thinking" ([advisor-tool-api]).

Caching the advisor's own transcript (the tool's `caching` param) "breaks even at roughly three advisor calls" — the cache write costs more than it saves below that, and pays off from there via non-zero `cache_read_input_tokens` on the second and later `advisor_message` iterations. Keep the setting constant across a conversation to avoid cache misses.

Priority Tier is per-model: "a Priority Tier commitment on the executor model does not extend to the advisor" — advisor calls run at Priority Tier only if the organization separately holds a commitment on the advisor model. Batch processing is supported, with `usage.iterations` reported per batch item ([advisor-tool-api]).

## Claude Code surface

Claude Code exposes the API tool as `/advisor`:

- `/advisor [model]` — picker with no argument, or set directly (e.g. `/advisor opus`); saved to the `advisorModel` setting and persists across sessions.
- `/advisor off` — turns it off.
- `--advisor <model>` flag — single-session override; Claude Code "doesn't list `--advisor` in `claude --help`."
- `advisorModel` setting — persistent default in the settings file.

`/advisor` works non-interactively (`-p`), in the Agent SDK, the desktop app, and over Remote Control only on **Claude Code v2.1.260+**. Other version gates: **Fable 5.1 requires v2.1.257+**; **Sonnet 5.5 as advisor for an Opus 4.7/4.8 main model requires v2.1.287+**; **Haiku 5.5 as main model or advisor requires v2.1.293+** ([advisor-cc]).

Setting `CLAUDE_CODE_DISABLE_ADVISOR_TOOL=1` disables the advisor entirely: `/advisor` becomes unavailable, any configured `advisorModel` is ignored, and `--advisor` is accepted but has no effect. Claude Code turns the advisor on through a feature flag it fetches from Anthropic; a session with flag-fetching disabled (e.g. `DISABLE_TELEMETRY`) keeps the advisor off regardless of configuration. Subagents inherit the configured advisor and apply the same pairing check against their own model.

**Caching interaction**: toggling `/advisor` mid-session does not invalidate the main model's prompt cache (unlike switching models) — the cached prefix stays intact, and the advisor's returned guidance is cached as part of the transcript on later turns. The advisor model's own read of the conversation is never cached: "each advisor call processes the full transcript anew, with no reuse between calls" ([advisor-cc]). "There is no setting to cap or force advisor calls" from Claude Code either — ask for more or fewer consultations in the prompt itself.

**Fable billing & billing split**: on plans where Fable usage bills to usage credits, selecting Fable as the advisor needs a one-time consent (given via `/model fable`). Before that consent, Claude Code doesn't apply Fable as the advisor and points you to `/model fable` instead — via `/advisor fable`, a notification (interactive sessions), or an exit-at-launch message (`claude --advisor fable`, except a background session, which starts without the advisor instead of exiting). With API billing, advisor tokens bill at the advisor model's own rates; on subscription plans, advisor usage counts toward the plan's usage limits, except a Fable advisor still bills to usage credits.

**What you see during a session**: the transcript shows an `Advising` line with the advisor model name while the call is in progress. On completion it reports one of three outcomes: `Reviewed` (press `Ctrl+O` to read the guidance), `Advisor declined to advise on this request` (reason via `Ctrl+O` if given), or `Advisor unavailable (<error_code>)`. Claude generally follows the advisor's guidance but surfaces a conflict rather than following it unconditionally when its own evidence — a failed step, contradicting file contents — disagrees with a specific claim.

**Common model pairings** (a curated subset of the API's compatibility table, per the Claude Code docs): Sonnet main + Opus advisor (escalate planning, ambiguous failures, and completion checks); Sonnet main + Fable advisor (needs Fable access); Haiku main + Opus advisor (lowest-cost main with strong planning, costing more than Haiku alone but less than switching the main model up); Opus main + Opus advisor (independent check for high-stakes work); Fable main + Fable advisor (the ceiling pairing — Claude Code doesn't apply an Opus or Sonnet advisor to a Fable main model); Sonnet main + Sonnet advisor (a cheap check for routine oversights).

**Compare with related features**: the advisor runs at decision points Claude itself chooses, mid-task. `opusplan` instead runs the stronger model only during plan mode (subject to the account's `availableModels` allowlist), then switches to Sonnet for execution. A subagent with its own `model` set runs the stronger model for the entire delegated subtask. `/model` switches the main model outright, from the next request onward. See [CC-model-provider-configuration.md](CC-model-provider-configuration.md) for `opusplan` and subagent model selection.

## Platform availability (unresolved conflict)

The two first-party pages disagree on **Claude Platform on AWS** (both accessed 2026-10-26):

- **API docs** ([advisor-tool-api]): "The advisor tool is available in beta on the Claude API, on Claude Platform on AWS, and on Claude Models on Google Cloud (Anthropic managed). It is not currently available on Amazon Bedrock, Claude Models on Google Cloud (Google managed), or Microsoft Foundry."
- **Claude Code docs** ([advisor-cc]): "The advisor tool is experimental and requires the Anthropic API. It is not available on Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, or Microsoft Foundry."

The API page lists Claude Platform on AWS as supported; the Claude Code page lists it as unsupported. Both agree Amazon Bedrock and Microsoft Foundry are unsupported. Left unresolved here — re-check once one page updates.

## Gotchas

- **Claude Managed Agents has a separate advisor config**, not the tool-definition form above: set `"advisor": {"type": "enabled", "model": ...}` in the agent's `multiagent` block; it takes no `max_uses`/`max_tokens`/`caching`, and advice arrives as session event-stream thread events rather than `advisor_tool_result` blocks. Don't conflate the two surfaces.
- **No conversation-level cap exists anywhere in the API** — `max_uses` is per-request only; client-side counting is the one lever for a conversation-level budget.
- **LLM gateways**: through `ANTHROPIC_BASE_URL`, advisor availability depends on whether the gateway forwards the request intact to the Anthropic API.
- **Encrypted advice is silent**: on the seven newer executors that only pair with redacted-result advisors, the advice still steers the executor — it is simply unreadable, whether inspecting the API response directly or reading a Claude Code transcript with `Ctrl+O`.
- **Haiku 4.5 asymmetry**: it can trigger the advisor as an executor but never appears as anyone's advisor in the compatibility table — a consequence of, not a separately stated exception to, the Sonnet-4.6-floor rule.

## Sources

| Source | Content |
|---|---|
| [Advisor tool — Claude API docs][advisor-tool-api] | Tool schema, pairing table, billing/usage accounting, streaming, caching, platform availability (accessed 2026-10-26) |
| [Escalate hard decisions with the advisor tool — Claude Code docs][advisor-cc] | `/advisor` command, `advisorModel` setting, `--advisor` flag, version gates, disable env var, cache interaction (accessed 2026-10-26) |

Cross-ref: [CC-tools-inventory.md](CC-tools-inventory.md), [CC-cli-reference.md](CC-cli-reference.md), [CC-env-vars-reference.md](CC-env-vars-reference.md), [CC-model-provider-configuration.md](CC-model-provider-configuration.md) (opusplan/subagent comparison), [CC-community-reimplementations-landscape.md](../../cc-community/CC-community-reimplementations-landscape.md) (leaked `advisor-tool` beta header)

[advisor-tool-api]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool
[advisor-cc]: https://code.claude.com/docs/en/advisor
