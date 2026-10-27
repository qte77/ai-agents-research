---
title: CC Session Cost Analysis from Transcript JSONL
purpose: Extract per-session cost and token usage from CC transcript files using jq.
created: 2026-03-27
updated: 2026-10-26
validated_links: 2026-10-26
status: adopt
---

## What It Is

Every CC session writes a JSONL transcript to `~/.claude/projects/<project-key>/<session-id>.jsonl`. These files contain per-turn token usage, model info, and timing data -- sufficient to reconstruct session cost without any external API or OTel infrastructure.

The transcript path is also available in the [statusline JSON][statusline] as `transcript_path`.

## Transcript Location

```text
~/.claude/projects/<project-key>/
  <session-id>.jsonl              # Main session transcript
  <session-id>/subagents/         # Subagent/teammate transcripts
    agent-<hash>.jsonl
```

The `<project-key>` is derived from the working directory path with `/` replaced by `-` (e.g., `-workspaces-Agents-eval`).

Transcript retention is controlled by `cleanupPeriodDays` (default: 30 days, minimum: 1). Setting `0` now fails with a validation error rather than disabling persistence; use `CLAUDE_CODE_SKIP_PROMPT_HISTORY` to fully disable transcript writes ([settings docs][settings]).

## Message Types

Each line is a JSON object with a `type` field:

| Type | Contains |
|---|---|
| `human` | User messages |
| `assistant` | Model responses with `.message.usage` (cost data lives here) |
| `system` | Internal events (`subtype: "turn_duration"` has `durationMs`) |

## Usage Object Structure

From `assistant` messages at `.message.usage` (observed CC 2.1.83, 2026-03-27):

```json
{
  "input_tokens": 1,
  "output_tokens": 199,
  "cache_creation_input_tokens": 126,
  "cache_read_input_tokens": 76860,
  "cache_creation": {
    "ephemeral_1h_input_tokens": 126,
    "ephemeral_5m_input_tokens": 0
  },
  "service_tier": "standard",
  "server_tool_use": {
    "web_search_requests": 0,
    "web_fetch_requests": 0
  },
  "speed": "standard",
  "inference_geo": ""
}
```

Additional fields on assistant messages: `.message.model` (e.g., `claude-opus-4-6`), `.message.stop_reason` (`end_turn`, `tool_use`).

These fields match the [OTel `api_request` event attributes][monitoring] (`input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_creation_tokens`, `cost_usd`, `model`).

## Price Modifiers Exposed by the Usage Object

The `speed` and `inference_geo` fields shown above aren't just telemetry — each corresponds to a real pricing multiplier on the [pricing page][pricing] (accessed 2026-10-26). For the base per-model rate table these modifiers multiply, see [CC-models-reference.md § Model Pricing][models-reference-pricing] (not duplicated here).

- **`speed: "fast"`** — [Fast mode][fast-mode] premium pricing, available for Claude Opus 5.5, Claude Opus 5, and Claude Opus 4.8 (research preview for the latter two): Opus 5.5 is $8/MTok input, $40/MTok output; Opus 5 and Opus 4.8 are $10/MTok input, $50/MTok output. Fast mode pricing "is not available with the Batch API" and applies across the full context window, including requests over 200k input tokens. It stacks with prompt-caching and data-residency multipliers ("apply on top of fast mode pricing").
- **`inference_geo: "us"`** — a 1.1x multiplier on all token pricing categories (input, output, cache writes, cache reads) for Claude 4.6 and later models. "Earlier models do not support the `inference_geo` parameter and always use standard pricing; requests that include the parameter on these models return a 400 error." `inference_geo: "global"` (the default) uses standard pricing.
- **Cloud regional endpoints** — Bedrock and Claude Models on Google Cloud (Google managed) regional/multi-region endpoints for Claude Sonnet 4.5+, Haiku 4.5+, and Opus 4.5+ models "include a 10 percent premium over global endpoints." On Claude in Microsoft Foundry, the Azure "US Data Zone Standard" deployment type applies the same 1.1x multiplier as `inference_geo: "us"` rather than this separate 10% figure.
- **Long-context pricing** — Claude 4.6+ models (except Haiku 5.5) and Claude Mythos Preview bill the full 1M-token context window at standard per-token rates (a 900k-token request costs the same per token as a 9k-token one). Claude Haiku 5.5 is the exception: it is priced by prompt length, with a request whose prompt (including cache reads and cache writes) exceeds 100,000 tokens billed at the higher per-request tier shown in [CC-models-reference.md][models-reference-pricing]; each request is priced on its own.
- **Stacking rules** — per the pricing page: prompt-caching multipliers "stack with other pricing modifiers, including the Batch API discount and data residency"; "Batch API and prompt caching discounts can be combined"; fast-mode pricing stacks with both caching and data-residency multipliers. The Batch API discount and cloud-platform (CCU) pricing do **not** apply to Claude Managed Agents sessions (see below).
- **Tool-use overhead tokens** — every request with `tools` present adds a per-model tool-use system-prompt token count (listed on the pricing page, not duplicated here) on top of normal input/output tokens, plus tokens for the `tools` parameter itself and any `tool_use`/`tool_result` blocks. Specific server tools carry their own usage-based charges:
  - **Web search**: $10 USD per 1,000 searches, plus standard token costs for search-generated content; each search counts once regardless of result count; an errored search is not billed.
  - **Web fetch**: no additional charge beyond standard token costs for the fetched content.
  - **Code execution**: free of the per-hour charge when used alongside `web_search_20260209`+ or `web_fetch_20260209`+ in the same request. Otherwise it is billed by execution time with a 5-minute minimum per execution; each organization gets 1,550 free container-hours/month, and usage beyond that is $0.05 USD per container-hour. If files are attached to the request, execution time is billed even when the tool isn't called, because files are preloaded onto the container.
- **Claude Managed Agents** — billed on tokens (standard per-model rates, with prompt-caching and `inference_geo` multipliers applying identically) plus a session-runtime SKU of **$0.08 USD per session-hour**, metered to the millisecond and accruing only while session status is `running` (not `idle`, `rescheduling`, or `terminated`). Session runtime "replaces the code execution container-hour billing model" for these sessions — no separate container-hour charge on top of it.

## Cost Extraction Recipes

### Single session summary

```bash
jq -s '[.[] | select(.type == "assistant" and .message.usage)] |
  {
    turns: length,
    model: (map(.message.model) | unique),
    input_tokens: [.[].message.usage.input_tokens // 0] | add,
    output_tokens: [.[].message.usage.output_tokens // 0] | add,
    cache_create: [.[].message.usage.cache_creation_input_tokens // 0] | add,
    cache_read: [.[].message.usage.cache_read_input_tokens // 0] | add
  }' ~/.claude/projects/<project>/<session-id>.jsonl
```

### Cost estimate (Opus 4.6 pricing)

The worked jq recipe below uses Opus 4.6's per-model rates ($5/MTok input, $6.25/MTok 5m cache write, $10/MTok 1h cache write, $0.50/MTok cache read, $25/MTok output), captured from the [official pricing page][pricing] on 2026-03-27, as an illustrative example. For the current rate on any model — including the newer Fable/Mythos 5.x, Opus 5.x, and Sonnet/Haiku 5.x lines — substitute the matching row from [CC-models-reference.md § Model Pricing][models-reference-pricing] rather than this one example (not duplicated here).

**Note**: The transcript `cache_creation` sub-object distinguishes `ephemeral_5m_input_tokens` from `ephemeral_1h_input_tokens`, enabling precise cost calculation per cache tier.

```bash
# Opus 4.6 cost estimate (uses 1h cache write rate as conservative default)
jq -s '[.[] | select(.type == "assistant" and .message.usage)] |
  ([.[].message.usage.input_tokens // 0] | add) as $in |
  ([.[].message.usage.output_tokens // 0] | add) as $out |
  ([.[].message.usage.cache_read_input_tokens // 0] | add) as $cr |
  ([.[].message.usage.cache_creation_input_tokens // 0] | add) as $cc |
  {
    input_usd: ($in / 1e6 * 5),
    output_usd: ($out / 1e6 * 25),
    cache_read_usd: ($cr / 1e6 * 0.50),
    cache_create_usd: ($cc / 1e6 * 10),
    total_usd: ($in/1e6*5 + $out/1e6*25 + $cr/1e6*0.50 + $cc/1e6*10)
  }' <transcript.jsonl>
```

**Verify pricing**: The [official pricing page][pricing] is the authoritative source. Prices change across model generations (e.g., Opus 4.0/4.1 was $15/$75, Opus 4.5/4.6 is $5/$25).

### Precise cost with cache tier breakdown

```bash
# Split 5m vs 1h cache writes for accurate costing (Opus 4.6)
jq -s '[.[] | select(.type == "assistant" and .message.usage)] |
  ([.[].message.usage.input_tokens // 0] | add) as $in |
  ([.[].message.usage.output_tokens // 0] | add) as $out |
  ([.[].message.usage.cache_read_input_tokens // 0] | add) as $cr |
  ([.[].message.usage.cache_creation.ephemeral_5m_input_tokens // 0] | add) as $cc5 |
  ([.[].message.usage.cache_creation.ephemeral_1h_input_tokens // 0] | add) as $cc1h |
  {
    input_usd: ($in / 1e6 * 5),
    output_usd: ($out / 1e6 * 25),
    cache_read_usd: ($cr / 1e6 * 0.50),
    cache_5m_write_usd: ($cc5 / 1e6 * 6.25),
    cache_1h_write_usd: ($cc1h / 1e6 * 10),
    total_usd: ($in/1e6*5 + $out/1e6*25 + $cr/1e6*0.50 + $cc5/1e6*6.25 + $cc1h/1e6*10)
  }' <transcript.jsonl>
```

### All sessions ranked by cache read (dominant cost driver)

```bash
for f in ~/.claude/projects/<project>/*.jsonl; do
  jq -s --arg s "$(basename "$f" .jsonl)" \
    '[.[] | select(.type == "assistant" and .message.usage)] |
    {session: $s, turns: length,
     out: [.[].message.usage.output_tokens // 0] | add,
     cache_read: [.[].message.usage.cache_read_input_tokens // 0] | add,
     branch: (last | .gitBranch // ""),
     time: (last | .timestamp // "")}' "$f" 2>/dev/null
done | jq -s 'sort_by(.cache_read) | reverse | .[:10]'
```

### Session wall-clock duration

```bash
jq -s '[.[] | select(.type == "system" and .subtype == "turn_duration")] |
  {
    turns: length,
    total_duration_min: ([.[].durationMs] | add / 60000),
    avg_turn_ms: ([.[].durationMs] | add / length)
  }' <transcript.jsonl>
```

## CLI `-p --output-format json` Result Fields

A different data source from the transcript JSONL above: `claude -p "<prompt>" --output-format json` prints a single JSON result object to stdout when the run finishes. Per the [TypeScript Agent SDK reference][ts-sdk-ref] (`SDKResultMessage`, which the CLI's own result object matches) and the [cost-tracking docs][cost-tracking], the documented fields include:

| Field | Type | Notes |
|---|---|---|
| `session_id` | string | |
| `duration_ms` | number | Wall-clock duration of the run |
| `duration_api_ms` | number | Time spent in API calls specifically |
| `num_turns` | number | Agentic turn count |
| `total_cost_usd` | number | Cumulative **client-side estimate**, not a billing figure |
| `usage` | object | Main-agent-loop usage only — excludes subagent/auxiliary calls |
| `modelUsage` | object, `{ [modelName]: ModelUsage }` | Per-model totals **including** subagent and auxiliary-call (e.g. compaction, workflow-agent) usage — prefer this over `usage` for whole-tree token/cost accounting |
| `result` | string | Final response text (success subtype only) |
| `is_error` | boolean | |
| `permission_denials` | array | |

`usage` and `modelUsage` both nest `cache_creation_input_tokens` and `cache_read_input_tokens` alongside `input_tokens`/`output_tokens`, matching the transcript fields documented above.

### jq recipe over `-p` JSON (documented fields only)

```bash
claude -p "your prompt" --output-format json | jq '{
  session_id: .session_id,
  num_turns: .num_turns,
  duration_ms: .duration_ms,
  duration_api_ms: .duration_api_ms,
  total_cost_usd: .total_cost_usd,
  usage: {
    input_tokens: .usage.input_tokens,
    output_tokens: .usage.output_tokens,
    cache_creation_input_tokens: .usage.cache_creation_input_tokens,
    cache_read_input_tokens: .usage.cache_read_input_tokens
  },
  by_model: .modelUsage
}'
```

`--continue`/`--resume` report the **whole conversation's** totals on `total_cost_usd` and `modelUsage` — earlier runs' spend included, since CC v2.1.277 (before that, a session resumed through the SDK or `claude -p` started its totals at zero per call). `usage` is per-turn in streaming-input mode; read the latest result rather than summing across results. Both figures remain client-side estimates that can drift from the actual bill; for authoritative billing, use the Usage and Cost API or the Claude Console Usage page.

Source: [TypeScript Agent SDK reference][ts-sdk-ref], `SDKResultMessage` type; [cost-tracking docs][cost-tracking]; [headless docs][headless]

## Relationship to Statusline

The [statusline][statusline] receives pre-aggregated cost/usage JSON via stdin on each turn, including `cost.total_cost_usd` (session total) and `context_window.*` (current usage). The transcript JSONL is the raw per-turn source. Use statusline for live monitoring; use transcripts for post-hoc analysis.

## Shared plan usage across Claude products

**One limit, three surfaces.** Per the help center: "Note that your usage of all different Claude product surfaces (claude.ai, Claude Code, Claude Desktop) counts towards the same usage limit." Plan size varies: "Different subscription plans (Pro, Max, Team, etc.) have different usage allowances, with paid plans offering higher limits" — but the article gives no concrete figures ([usage-limits][usage-limits]).

**Reset and display.** "Your plan's included usage limit will reset every five hours once you reach it." Usage is tracked via "Usage dashboard: View real-time consumption in Settings > Usage." For paid plans (Pro, Max 5x, Max 20x) with usage credits enabled, "Usage credits apply to both Claude conversations and Claude Code terminal usage. Your combined usage across both interfaces counts toward your limits." ([usage-credits][usage-credits])

**Metering by sign-in method.** ["Models, usage, and limits in Claude Code"][cc-usage-metering] states "How you signed in determines how usage is metered" — but its table names only two flows, not a general subscription-vs-Enterprise split: "Claude Enterprise seat (via `/login`)" gets "A pool of usage included in your organization's plan, reset on a rolling window," while "API key (Console, Bedrock, Vertex, or Microsoft Foundry)" gets "Pay-as-you-go, billed per token to that cloud or Console account. No hard stop; the account is charged for what it uses." The article does not describe a separate row for a personal Pro/Max/Team subscriber signed in via `/login` — that case falls under the shared five-hour plan limit described above ([usage-limits][usage-limits], [usage-credits][usage-credits]) instead of either of this table's two rows.

**Owner observation** (claude.ai Settings > Usage, observed 2026-09-23): the usage page splits usage per product — Claude Code / Chats / Cowork / Other. None of the three help-center articles cited above documents this per-product split; [usage-limits][usage-limits] states only that the three surfaces share one limit, not how the dashboard breaks it out.

**Fable models: a sub-cap, not a separate pool.** Per [Claude Fable models on your plan][fable-plan] (help center, modified 2026-09-02):

- **Max, and premium Team / seat-based Enterprise seats:** "You can use up to 50% of your weekly usage limits on Fable models at no extra cost. They draw from your plan's regular weekly usage limits and use them faster than other Claude models."
  - So Fable usage fills both the Fable bar and the general weekly pool. Switching to Fable does not preserve the general pool.
  - Past the 50% Fable cap: "keep using Fable models with usage credits, or switch to another Claude model."
- **Pro, and standard Team / seat-based Enterprise seats:** Fable "aren't included in your plan's usage limits" and run on pay-as-you-go usage credits.
- **Usage-based Enterprise and the API:** billed at standard API rates.
- **History:** the earlier "up to 50% at no extra cost" promotion for Fable 5 ended 2026-07-19. Fable 5 and 5.1 now "work the same way on your plan."
- **CC version gates:** Fable 5 needs CC v2.1.170+, Fable 5.1 needs v2.1.255+.

**Limit resets (redeemable).** Separate from the automatic five-hour and weekly refills, "Limit resets are given occasionally to eligible plans, and set your usage limits back to full when you choose to use one." Per [What is a limit reset?][limit-reset] (help center, modified 2026-09-22):

- "Depending on the limit reset shown, either your five-hour session limit or your weekly usage limit go back to full right away. Your weekly limits still reset on their usual day and time."
- It can be used before a limit is reached and "can't [be] undo[ne]." An expiry, if any, is shown in Settings > Usage. It "doesn't refund extra usage you've already been billed for or change your usage credit balance," and it is lost on downgrade or cancellation before use.
- To redeem it, go to Settings > Usage on the web or in Claude Desktop → "Reset for free" in the **Resets** section; the same button appears on the limit-reached message. The button "isn't currently available on Claude Mobile or in Claude Code in your terminal or IDE," but because limits are shared, a reset also refills Claude Code.
- The article does not name which plans are "eligible." The Claude Code CHANGELOG (through 2.1.283, checked 2026-09-27) has no entry for redeeming a reset. Related CC behavior is limited to resuming automatically when a limit resets: sessions (CC v2.1.234+, toggle in `/config`: "Continue automatically at usage limit") and dynamic workflows (CC v2.1.271+).

**Owner observation** (claude.ai Settings > Usage, German UI, observed 2026-09-27): the Resets section reads, in translation, "A reset refills your 5-hour and weekly limits when you use it. Your week keeps its usual reset day. You currently have no resets." This conflicts with the article, which says a given reset refills *either* the five-hour *or* the weekly limit. Treat the article as authoritative until Anthropic reconciles the two.

**UNVERIFIED**: per-plan usage amounts (e.g., token or message counts for Pro/Max/Team) and the weekly limit's size. None of the articles cited above state either; [limit-reset][limit-reset] confirms that a weekly usage limit exists.

**General usage-limit best practices (claude.ai, not CC-specific).** Per [Usage limit best practices][usage-best-practices] (help center, accessed 2026-10-15), the factors it lists as affecting limits are message length, file-attachment size, conversation length, tool use (e.g. Research and web search), model choice, effort level, artifacts, and multi-step tasks. Its prompt-level tips — plan ahead ("Planning helps reduce the number of back-and-forth messages needed"), be specific, batch related requests into one message, review before sending, and reuse context already in the conversation instead of repeating it — are written for claude.ai chat generally, not Claude Code specifically. "Caching" in that article refers to **claude.ai Projects** ("Content in projects is cached and counts less against your limits when reused," expiring after inactivity) — a different mechanism from CC's own prompt caching (see [CC-prompt-caching-behavior.md](../context-memory/CC-prompt-caching-behavior.md)). The article has no Claude-Code-specific section; it links to "Models, usage, and limits in Claude Code" (already cited above as [cc-usage-metering][cc-usage-metering]) by title only.

**Claude Code wrap-up allowance.** Per [What is the Claude Code wrap-up allowance?][wrap-up-allowance] (help center, accessed 2026-10-15): if a response is already in progress when a session hits its five-hour limit, CC may keep working briefly past the limit to reach a reasonable stopping point, shown as "Usage limit reached · wrapping up." It applies only to a response already running — a *new* message sent after the limit doesn't qualify.

Frequency, verbatim:

- **Pro**: *"Up to once per weekly usage period, whether or not the full allowance is used that time."*
- **Max and Team (Premium seats)**: *"When you reach a five-hour usage limit, within your weekly limit."*

It counts toward the weekly limit without increasing it, and the response ends when it completes, the allowance runs out, or it's interrupted; if usage credits are enabled, the included allowance is used first and the response then continues on credits at standard rates, subject to any spend limit.

What it is not, verbatim (from separate sentences, not a single stitched quote): *"The Wrap-Up Allowance is not a credit, promotional credit, or usage credit."* *"It has no cash value and is not transferable."* *"It can't be exchanged or refunded."* *"It can't be requested, saved, or carried over to a later response or usage period."* Anthropic may change, pause, or discontinue it at any time without notice.

Eligibility requires all of: Pro, Max, or a Team plan with a Premium seat, in good standing; **CC v2.1.277 or later**, signed in with a Claude account (not an API key, a third-party cloud provider, or claude.ai chats); an unpublished minimum account/organization age; and inclusion in a gradual rollout.

### Local tools vs plan usage

`/stats` (the owner's `stats='claude /stats'` alias) computes entirely from local transcript `.jsonl` files under `~/.claude/projects/` — no separate output file (see [CC-binary-architecture.md § `/stats` and `/usage` Data Flow][binary-arch]). CodeBurn (`burn='npx codeburn'`) reads the same local transcripts for its dashboard, `optimize`, and `export` commands. Both are therefore blind to Chats and Cowork usage and undercount total plan usage relative to the shared limit described above — see [CC-usage-tooling-landscape.md][usage-tooling] for the full CodeBurn/ccusage comparison.

CodeBurn's dollar figures default to API list-price equivalents, not a live billing figure: "The dollar figure is what your tokens would have cost at API rates. It is not an invoice. The card labels it API-equivalent, not a live provider window." Matching that figure to an actual subscription is opt-in — confirmed directly against CodeBurn v0.9.25's CLI help (`npx codeburn plan --help`, `npx codeburn export --help`): `codeburn plan set <plan-id>` (e.g. `claude-max`) "Show[s] or configure[s] a subscription plan for overage tracking," and `codeburn export --billing <mode>` "Filter[s] by billing mode (metered|subscription)."

CodeBurn's separate `codeburn quota` subcommand is the exception to the transcript-only blind spot: per its `--help`, it reports "Live provider capacity: quota windows for each signed-in coding tool on this machine" by querying the provider directly rather than reading local transcripts — but it still does not appear to break that figure out per product the way the Settings > Usage page above does.

## Relationship to OTel

The [CC OTel integration][monitoring] exports `claude_code.cost.usage` (USD metric) and `claude_code.token.usage` (by type: input/output/cacheRead/cacheCreation) as time-series metrics. It also exports `api_request` events with per-call cost. Transcripts provide the same data without OTel infrastructure. Use transcripts for local analysis; use OTel for centralized dashboards across teams.

**Note**: CC now has a "Traces (beta)" feature exporting distributed trace spans (`claude_code.interaction`, `claude_code.llm_request`, `claude_code.tool`, etc.), enabled via `CLAUDE_CODE_ENABLE_TELEMETRY=1` + `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` + `OTEL_TRACES_EXPORTER` (CC v2.1.216+, [monitoring docs][monitoring]). Upstream issues [#9584][gh-9584] and [#2090][gh-2090], which had requested this capability, are now closed. See also [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md) (OTel section).

## Message Batches API

The Message Batches API runs large request volumes asynchronously. This section is deliberately bounded to the billing/limits facts that bear on cost accounting; see the [batch processing docs][batch] for the full guide. For ZDR eligibility specifically, Batches is **not** ZDR-eligible per [CC-web-auth-setup-analysis.md § Adjacent Platform Building Blocks for Agents][web-auth-batch] (not edited by this pass; that doc's claim stands as-is).

- **Discount**: "All usage is charged at 50 percent of the standard API prices" — both input and output tokens.
- **Size limit**: a batch is "limited to either 100,000 Message requests or 256 MB in size, whichever is reached first."
- **24-hour expiry**: results become available once every request has completed or after 24 hours, whichever comes first; "batches expire if processing does not complete within 24 hours."
- **Result retention**: "Batch results are available for 29 days after creation. After that, you can still view the Batch, but its results will no longer be available for download."
- **Billing by result type**: `errored`, `canceled`, and `expired` requests are each documented as "You will not be billed for these requests." Only `succeeded` requests are billed.
- **Result ordering**: "Batch results can be returned in any order, and may not match the ordering of requests when the batch was created." Match results to requests via `custom_id`, never position.
- **Unsupported batch parameters** (return a validation error): `stream: true`, `speed` (Fast mode), `fallbacks` (server-side fallback), and `max_tokens: 0` (cache pre-warming) — per the batch processing docs' own parameter table.
- **Caching + batches**: cache hits are best-effort because batch requests process "concurrently and in any order" — "Users typically experience cache hit rates ranging from 30 percent to 98 percent, depending on their traffic patterns." The docs' tip: write a shared prefix to the 1-hour cache with one request first, then submit the rest, since batches commonly take longer than the 5-minute cache's lifetime.
- **Rate limits**: "Usage of the Batches API does not affect rate limits in the Messages API" — Batches has its own, separate HTTP-request and in-flight-request limits instead.
- **`output-300k-2026-03-24` beta**: raises the batch `max_tokens` cap to 300,000, "available on the Message Batches API only, not the synchronous Messages API." Supported models: Claude Opus 5.5, Opus 5, Opus 4.8, Opus 4.7, Opus 4.6, Sonnet 5.5, Sonnet 5, Sonnet 4.6, and Haiku 5.5. Supported platforms: the Claude API (first-party) and Claude Platform on AWS; "not currently available on Amazon Bedrock, Claude Models on Google Cloud (Google managed), or Microsoft Foundry."

## Sources

| Source | Content |
|---|---|
| [CC statusline docs][statusline] | Statusline JSON schema (full field list) |
| [CC monitoring docs][monitoring] | OTel metrics, events, cost tracking |
| [Anthropic pricing][pricing] | Official per-model token pricing; fast mode, data-residency, long-context, tool-use, and Managed Agents pricing modifiers (accessed 2026-10-26) |
| [Anthropic batch processing][batch] | Message Batches API discount, limits, unsupported parameters, caching interaction, rate limits, `output-300k-2026-03-24` beta (accessed 2026-10-26) |
| [CC settings docs][settings] | `cleanupPeriodDays` transcript retention |
| CC 2.1.83 transcript inspection, Codespaces, 2026-03-27 | JSONL structure, usage object fields |
| [How do usage and length limits work?][usage-limits] | Shared usage limit across claude.ai/Claude Code/Claude Desktop; per-plan allowances vary (no figures given) |
| [Manage usage credits for paid Claude plans][usage-credits] | Five-hour reset timing; Settings > Usage dashboard location; usage credits cover both chat and Claude Code |
| [Models, usage, and limits in Claude Code][cc-usage-metering] | Sign-in-based metering table: Enterprise seat pool vs API key pay-per-token |
| [Claude Fable models on your plan][fable-plan] | Fable 50% weekly sub-cap drawing from the regular weekly limits (Max/premium); usage credits on Pro/standard; CC version gates |
| [What is a limit reset?][limit-reset] | Redeemable limit resets: which limit they refill, expiry, "Reset for free" flow, no button in CC terminal/IDE |
| [Claude Code CHANGELOG][cc-changelog] (through 2.1.283, checked 2026-09-27) | No reset-redemption entry; auto-continue at limit reset (2.1.234, 2.1.271) |
| claude.ai Settings > Usage (German UI), observed 2026-09-27 | Resets section text (conflicts with the help-center article on which limits a reset refills) |
| claude.ai Settings > Usage, observed 2026-09-23 | Per-product usage split (Claude Code / Chats / Cowork / Other); undocumented in the help-center articles above |
| CodeBurn v0.9.25 CLI (`--help`, `plan --help`, `export --help`, `quota --help`), 2026-09-24 | `plan`/`export --billing`/`quota` subcommand behavior |
| [Usage limit best practices][usage-best-practices] | General claude.ai usage-limit factors and prompt-level best practices; not CC-specific (accessed 2026-10-15) |
| [Claude Code wrap-up allowance][wrap-up-allowance] | Wrap-up allowance mechanics, frequency by plan, eligibility (CC v2.1.277+), what it is and isn't (accessed 2026-10-15) |
| [TypeScript Agent SDK reference][ts-sdk-ref] | `SDKResultMessage` field names and types (`total_cost_usd`, `usage`, `modelUsage`, `duration_api_ms`, `num_turns`, …) (accessed 2026-10-15) |
| [Track cost and usage][cost-tracking] | `usage` vs `modelUsage` vs `total_cost_usd` scope, subagent accounting, cross-call accumulation since CC v2.1.277 (accessed 2026-10-15) |
| [Headless / Agent SDK docs][headless] | `-p --output-format json` usage, `--continue`/`--resume` cost reporting (accessed 2026-10-15) |

[statusline]: https://code.claude.com/docs/en/statusline
[monitoring]: https://code.claude.com/docs/en/monitoring-usage
[pricing]: https://platform.claude.com/docs/en/about-claude/pricing
[settings]: https://code.claude.com/docs/en/settings
[gh-9584]: https://github.com/anthropics/claude-code/issues/9584
[gh-2090]: https://github.com/anthropics/claude-code/issues/2090
[usage-limits]: https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work
[usage-credits]: https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans
[cc-usage-metering]: https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code
[limit-reset]: https://support.claude.com/en/articles/17007452-what-is-a-limit-reset
[fable-plan]: https://support.claude.com/en/articles/15424964-claude-fable-models-on-your-plan
[cc-changelog]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
[binary-arch]: ../configuration/CC-binary-architecture.md#stats-and-usage-data-flow
[usage-tooling]: ../../cc-community/CC-usage-tooling-landscape.md
[usage-best-practices]: https://support.claude.com/en/articles/9797557-usage-limit-best-practices
[wrap-up-allowance]: https://support.claude.com/en/articles/17040437-claude-code-wrap-up-allowance
[ts-sdk-ref]: https://code.claude.com/docs/en/agent-sdk/typescript#sdkresultmessage
[cost-tracking]: https://code.claude.com/docs/en/agent-sdk/cost-tracking
[headless]: https://code.claude.com/docs/en/headless
[batch]: https://platform.claude.com/docs/en/build-with-claude/batch-processing
[fast-mode]: https://platform.claude.com/docs/en/build-with-claude/fast-mode
[models-reference-pricing]: ../configuration/CC-models-reference.md#model-pricing-current-lineup
[web-auth-batch]: ../ci-remote/CC-web-auth-setup-analysis.md#adjacent-platform-building-blocks-for-agents
