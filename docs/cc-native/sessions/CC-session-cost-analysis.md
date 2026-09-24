---
title: CC Session Cost Analysis from Transcript JSONL
purpose: Extract per-session cost and token usage from CC transcript files using jq.
created: 2026-03-27
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Adopt

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

Pricing from the [official pricing page][pricing] (accessed 2026-03-27):

| Token type | Opus 4.6 | Sonnet 4.6 | Haiku 4.5 |
|---|---|---|---|
| Base input | $5/MTok | $3/MTok | $1/MTok |
| 5m cache write | $6.25/MTok (1.25x) | $3.75/MTok | $1.25/MTok |
| 1h cache write | $10/MTok (2x) | $6/MTok | $2/MTok |
| Cache read (hit) | $0.50/MTok (0.1x) | $0.30/MTok | $0.10/MTok |
| Output | $25/MTok | $15/MTok | $5/MTok |

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

## Relationship to Statusline

The [statusline][statusline] receives pre-aggregated cost/usage JSON via stdin on each turn, including `cost.total_cost_usd` (session total) and `context_window.*` (current usage). The transcript JSONL is the raw per-turn source. Use statusline for live monitoring; use transcripts for post-hoc analysis.

## Shared plan usage across Claude products

**One limit, three surfaces.** Per the help center: "Note that your usage of all different Claude product surfaces (claude.ai, Claude Code, Claude Desktop) counts towards the same usage limit." Plan size varies: "Different subscription plans (Pro, Max, Team, etc.) have different usage allowances, with paid plans offering higher limits" — but the article gives no concrete figures ([usage-limits][usage-limits]).

**Reset and display.** "Your plan's included usage limit will reset every five hours once you reach it." Usage is tracked via "Usage dashboard: View real-time consumption in Settings > Usage." For paid plans (Pro, Max 5x, Max 20x) with usage credits enabled, "Usage credits apply to both Claude conversations and Claude Code terminal usage. Your combined usage across both interfaces counts toward your limits." ([usage-credits][usage-credits])

**Metering by sign-in method.** ["Models, usage, and limits in Claude Code"][cc-usage-metering] states "How you signed in determines how usage is metered" — but its table names only two flows, not a general subscription-vs-Enterprise split: "Claude Enterprise seat (via `/login`)" gets "A pool of usage included in your organization's plan, reset on a rolling window," while "API key (Console, Bedrock, Vertex, or Microsoft Foundry)" gets "Pay-as-you-go, billed per token to that cloud or Console account. No hard stop; the account is charged for what it uses." The article does not describe a separate row for a personal Pro/Max/Team subscriber signed in via `/login` — that case falls under the shared five-hour plan limit described above ([usage-limits][usage-limits], [usage-credits][usage-credits]) instead of either of this table's two rows.

**Owner observation** (claude.ai Settings > Usage, observed 2026-09-23): the usage page splits usage per product — Claude Code / Chats / Cowork / Other. None of the three help-center articles cited above documents this per-product split; [usage-limits][usage-limits] states only that the three surfaces share one limit, not how the dashboard breaks it out.

**UNVERIFIED**: weekly usage limits and per-plan usage amounts (e.g., token or message counts for Pro/Max/Team). None of the three articles cited above state either.

### Local tools vs plan usage

`/stats` (the owner's `stats='claude /stats'` alias) computes entirely from local transcript `.jsonl` files under `~/.claude/projects/` — no separate output file (see [CC-binary-architecture.md § `/stats` and `/usage` Data Flow][binary-arch]). CodeBurn (`burn='npx codeburn'`) reads the same local transcripts for its dashboard, `optimize`, and `export` commands. Both are therefore blind to Chats and Cowork usage and undercount total plan usage relative to the shared limit described above — see [CC-usage-tooling-landscape.md][usage-tooling] for the full CodeBurn/ccusage comparison.

CodeBurn's dollar figures default to API list-price equivalents, not a live billing figure: "The dollar figure is what your tokens would have cost at API rates. It is not an invoice. The card labels it API-equivalent, not a live provider window." Matching that figure to an actual subscription is opt-in — confirmed directly against CodeBurn v0.9.25's CLI help (`npx codeburn plan --help`, `npx codeburn export --help`): `codeburn plan set <plan-id>` (e.g. `claude-max`) "Show[s] or configure[s] a subscription plan for overage tracking," and `codeburn export --billing <mode>` "Filter[s] by billing mode (metered|subscription)."

CodeBurn's separate `codeburn quota` subcommand is the exception to the transcript-only blind spot: per its `--help`, it reports "Live provider capacity: quota windows for each signed-in coding tool on this machine" by querying the provider directly rather than reading local transcripts — but it still does not appear to break that figure out per product the way the Settings > Usage page above does.

## Relationship to OTel

The [CC OTel integration][monitoring] exports `claude_code.cost.usage` (USD metric) and `claude_code.token.usage` (by type: input/output/cacheRead/cacheCreation) as time-series metrics. It also exports `api_request` events with per-call cost. Transcripts provide the same data without OTel infrastructure. Use transcripts for local analysis; use OTel for centralized dashboards across teams.

**Note**: CC now has a "Traces (beta)" feature exporting distributed trace spans (`claude_code.interaction`, `claude_code.llm_request`, `claude_code.tool`, etc.), enabled via `CLAUDE_CODE_ENABLE_TELEMETRY=1` + `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` + `OTEL_TRACES_EXPORTER` (CC v2.1.216+, [monitoring docs][monitoring]). Upstream issues [#9584][gh-9584] and [#2090][gh-2090], which had requested this capability, are now closed. See also [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md) (OTel section).

## Sources

| Source | Content |
|---|---|
| [CC statusline docs][statusline] | Statusline JSON schema (full field list) |
| [CC monitoring docs][monitoring] | OTel metrics, events, cost tracking |
| [Anthropic pricing][pricing] | Official per-model token pricing |
| [CC settings docs][settings] | `cleanupPeriodDays` transcript retention |
| CC 2.1.83 transcript inspection, Codespaces, 2026-03-27 | JSONL structure, usage object fields |
| [How do usage and length limits work?][usage-limits] | Shared usage limit across claude.ai/Claude Code/Claude Desktop; per-plan allowances vary (no figures given) |
| [Manage usage credits for paid Claude plans][usage-credits] | Five-hour reset timing; Settings > Usage dashboard location; usage credits cover both chat and Claude Code |
| [Models, usage, and limits in Claude Code][cc-usage-metering] | Sign-in-based metering table: Enterprise seat pool vs API key pay-per-token |
| claude.ai Settings > Usage, observed 2026-09-23 | Per-product usage split (Claude Code / Chats / Cowork / Other); undocumented in the help-center articles above |
| CodeBurn v0.9.25 CLI (`--help`, `plan --help`, `export --help`, `quota --help`), 2026-09-24 | `plan`/`export --billing`/`quota` subcommand behavior |

[statusline]: https://code.claude.com/docs/en/statusline
[monitoring]: https://code.claude.com/docs/en/monitoring-usage
[pricing]: https://platform.claude.com/docs/en/docs/about-claude/pricing
[settings]: https://code.claude.com/docs/en/settings
[gh-9584]: https://github.com/anthropics/claude-code/issues/9584
[gh-2090]: https://github.com/anthropics/claude-code/issues/2090
[usage-limits]: https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work
[usage-credits]: https://support.claude.com/en/articles/12429409-manage-usage-credits-for-paid-claude-plans
[cc-usage-metering]: https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code
[binary-arch]: ../configuration/CC-binary-architecture.md#stats-and-usage-data-flow
[usage-tooling]: ../../cc-community/CC-usage-tooling-landscape.md
