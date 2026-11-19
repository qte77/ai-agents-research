---
title: CC Fast Mode Analysis
source: https://code.claude.com/docs/en/fast-mode
purpose: Analysis of Claude Code Fast Mode and the underlying API `speed` parameter for potential adoption within CC-based workflows.
created: 2026-02-17
updated: 2026-11-19
validated_links: 2026-11-08
status: available
---

**Details:** (2026-11-17 update: the [CC page][cc-fast] now also lists Fable 5.2, from v2.1.321.) Available on Opus 5.5, research preview on Opus 5 and Opus 4.8 — the API and Claude Code pages now both state this per model; Opus 4.8 fast mode is deprecated (2026-10-30) and will be removed 2026-11-30 (both pages read 2026-11-08)

## What Fast Mode Is

A faster inference configuration for Claude Opus and, per the [CC page][cc-fast] read 2026-11-17, Fable 5.2 (v2.1.321+) — **same model, same quality, up to 2.5x higher output tokens per second** ([CC][cc-fast], [API][api-fast]). The gain is in output tokens per second, not time to first token ([API][api-fast]). Not a different model or reduced reasoning — an infrastructure-level latency optimization at higher per-token cost.

Supported models (2026-11-08):

| Model | API status | Access |
|---|---|---|
| Fable 5.2 | Listed on the CC page (read 2026-11-17); API-page status not re-read | Claude Code v2.1.321 or later; with `/fast` it persists only if turned on while using Fable 5.2; `"fastMode": true` alone has no effect on it until `/fast` is run on Fable 5.2 ([CC][cc-fast]) |
| Opus 5.5 | Generally available | No beta header, no access request; default fast rate limit in the Start, Build and Scale tiers, not Evaluation ([API][api-fast]) |
| Opus 5, Opus 4.8 | Research preview | `fast-mode-2026-02-01` beta header (else `400`) plus provisioned access (the API page names account manager or waitlist for Opus 5); Opus 4.8 fast mode deprecated 2026-10-30, removal 2026-11-30 ([API][api-fast], [CC][cc-fast]) |
| Opus 4.7 | Removed | Deprecated 2026-06-25, removed 2026-07-24; switching to it turns fast mode off ([CC][cc-fast]) |
| Opus 4.6 | Not supported | With the beta header, a `speed: "fast"` request succeeds but runs at standard speed (`usage.speed` = `"standard"`); on Google Cloud (Anthropic managed) it returns `400` ([API][api-fast]) |

Not available on Sonnet or Haiku ([CC][cc-fast]). Supported on the Anthropic API: Fable 5.2, Opus 5.5, Opus 5 and Opus 4.8 ([CC][cc-fast], 2026-11-17).

**Claude Code default fast-mode model:** Opus 5.5 from v2.1.280; Opus 5 on v2.1.219–v2.1.279 ([CC][cc-fast]). Earlier releases defaulted to Opus 4.8 (v2.1.154–v2.1.218 per the page as read 2026-10-26; that range is no longer listed).

### Pricing

| Model | Fast input (MTok) | Fast output (MTok) | Standard input / output |
|---|---|---|---|
| Fable 5.2 | $16 | $80 | not re-read |
| Opus 5.5 | $8 | $40 | $4 / $20 |
| Opus 5, Opus 4.8 | $10 | $50 | $5 / $25 |

Fast prices from [the fast-mode page][api-fast] and [CC page][cc-fast]; standard prices from the [pricing page][pricing] (2026-10-26) — fast mode is exactly **2x** standard on every supported model. Flat across the full context window, including requests over 200k input tokens ([API][api-fast]). Prompt-caching and data-residency multipliers stack on top of fast pricing ([API][api-fast]); see [CC-models-reference.md](CC-models-reference.md) for the full price table.

### Effort Level Interaction

Default effort is model-specific (`medium` on the newest models, `xhigh` on Opus 4.7, `high` on the rest; no subscriber-plan-specific default). The per-model table lives in [CC-model-provider-configuration.md § Effort Levels](CC-model-provider-configuration.md#effort-levels) ([source][cc-model], checked 2026-11-19). The "ultrathink" keyword still exists — it triggers deeper reasoning for one turn without changing the session effort setting. This interacts with fast mode:

| Combination | Effect |
| ----------- | ------ |
| Fast mode + the model's default effort | Balanced speed/quality for the fast-mode model default |
| Fast mode + `ultrathink` | Maximum quality, highest cost and latency |
| Fast mode + low effort | Maximum speed on simple tasks |

After `/usage-credits`, `/fast` remains available.

### Configuration

**API:** set `speed: "fast"` on the request; the response `usage.speed` reports `"fast"` or `"standard"` ([API][api-fast]).

**Claude Code:**

```json
{ "fastMode": true }
```

- `/fast` in the CLI (persists across sessions by default); the VS Code extension has a **Toggle fast mode** command when the selected model supports it ([CC][cc-fast])
- No dedicated `--fast` flag; non-interactively, `claude -p --settings '{"fastMode": true}'` — the `-p` form requires v2.1.205+ ([CC][cc-fast], [CLI][cc-cli])
- Cloud sessions: `/fast on`, session-only, requires v2.1.271+ in the session's environment ([CC][cc-fast])
- `fastModePerSessionOptIn: true` makes every session start with fast mode off; deployable org-wide via server-managed settings ([CC][cc-fast])
- `CLAUDE_CODE_DISABLE_FAST_MODE=1` disables it; behind LLM gateways the client-side availability check goes direct to `api.anthropic.com` — `CLAUDE_CODE_SKIP_FAST_MODE_NETWORK_ERRORS=1` / `CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1` work around a failed or misread check ([CC][cc-fast])

### Key Mechanics

- **Mid-conversation cost:** the first enable in a conversation pays the full fast-mode uncached input price for the whole context; fast and standard speed keep separate caches, so every later switch re-reads uncached ([CC][cc-fast]). API: "Requests at different speeds do not share cached prefixes." ([API][api-fast])
- **Rate limits:** a dedicated fast-mode limit separate from standard Opus ([API][api-fast]); in Claude Code all supported Opus models share one fast pool ([CC][cc-fast]).
  - **API:** over the limit returns `429` with `retry-after`; no automatic fallback — the SDK retries `429` up to 2 times by default, and falling back means retrying without `speed` ([API][api-fast]). Limit status is in `anthropic-fast-{input,output}-tokens-{limit,remaining,reset}` headers.
  - **Claude Code:** falls back to standard speed automatically, the `↯` icon greys during cooldown, then re-enables ([CC][cc-fast]).
- **Billing:** subscription plans (Pro/Max/Ultra/Team/Enterprise; Ultra is the renamed Max 20x plan per [feature availability][cc-features]) pay from usage credits only, even with plan usage left; Console organizations pay per token with the rest of their API usage ([CC][cc-fast]).
- **Enablement:** Team/Enterprise need an Owner to enable it; Console organizations need access provisioned — without it every fast request is rejected with a 429 that Claude Code treats as a rate limit ([CC][cc-fast]).
- **Not combinable** with the Batch API or a Priority Tier commitment ([API][api-fast]).
- ZDR eligible, excluding Covered Models ([API][api-fast] page metadata).

### Platform availability (read 2026-11-08; CC layer re-read 2026-11-17)

- **API layer** ([API][api-fast]): `speed: "fast"` on Opus 5.5 works on the Claude API, Claude Models on Google Cloud (Anthropic managed) and Microsoft Foundry (hosted on Azure); the Opus 5 / 4.8 preview and Managed Agents fast mode are Claude API only.
- **Claude Code layer** ([CC][cc-fast], [feature availability][cc-features]): Anthropic Console or claude.ai subscription only — as re-read 2026-11-17, available through the Console API, subscriptions with usage credits and (with conditions) Google Cloud's Agent Platform; "not available on Amazon Bedrock, Microsoft Foundry, or Claude Platform on AWS". The 2026-11-08 reading also listed Agent Platform as unavailable; see the Vertex section below.
- **Why the API and CC layers differ (Agent Platform part superseded, see below):** "Google Cloud's Agent Platform" is the Google-managed offering (`CLAUDE_CODE_USE_VERTEX`, `aiplatform.googleapis.com`), a different product from Claude Models on Google Cloud (Anthropic managed) (`claude.googleapis.com`), for which Claude Code documents no integration ([Google Cloud overview][gcp-overview]). Microsoft Foundry is the same product on both pages: the API supports fast mode there for Opus 5.5, but Claude Code's Foundry integration doesn't offer it. A client limitation, not a disagreement about the API.

### Fast mode on Vertex (v2.1.322, supersedes the 2026-11-08 reading above)

The CHANGELOG (2.1.322) says: "Added fast mode on Vertex in the global, us and eu regions, falling back to standard speed if Vertex refuses it". The [fast-mode page](https://code.claude.com/docs/en/fast-mode) (read 2026-11-17) documents it under "Use fast mode on Agent Platform": Fable 5.2 only, Claude Code v2.1.322 or later, the Fable 5.2 region must be `global`, `us` or `eu` (otherwise `/fast` reports `Fast mode needs Vertex region global, us or eu`), and `"fastMode": true` in settings has no effect there. A 403 or 404 from the provider pauses fast mode with a retry message (v2.1.323). The 2026-11-08 "not available on ... Google Cloud's Agent Platform" quote predates this; the live page now lists only Amazon Bedrock, Microsoft Foundry and Claude Platform on AWS as unavailable. The region variable is `VERTEX_REGION_CLAUDE_FABLE_5_2` (added v2.1.321 per the env-vars page; see [CC-env-vars-reference](CC-env-vars-reference.md)).

### Fast Mode vs Effort Level

| Setting | Effect |
| ------- | ------ |
| Fast mode | Same quality, lower latency, higher cost |
| Lower effort | Less thinking, faster, potentially lower quality on complex tasks |

Combinable: fast mode + lower effort for maximum speed on simple tasks.

## Applicability

| Workflow | Fit | Rationale |
| -------- | --- | --------- |
| Interactive development (debugging, iteration) | Strong | Latency reduction directly improves developer flow |
| Autonomous headless loop (`claude -p`) | Weak | Developer not waiting; cost matters more than speed |
| Parallel autonomous tasks | Weak | Same as above; multiple concurrent agents multiply the cost further |
| Batch/background generation tasks | Weak | No interactive waiting; fast mode can't be used with the Batch API anyway |
| Time-boxed collection runs | Neutral | Faster turnaround but 2x cost; only worth it under time pressure |

### Decision Rule

**Enable fast mode for interactive sessions where latency breaks flow. Disable for autonomous/headless invocations (`claude -p`) where cost efficiency matters.**

### Potential Integration

If adopted, fast mode could be passed through Makefile recipes:

```makefile
# Example (NOT implemented — YAGNI until measured need)
FAST_MODE ?= false
autonomous_run:
    $(if $(filter true,$(FAST_MODE)),--settings '{"fastMode": true}')
```

**Recommendation**: Do not integrate yet. Headless CC usage (`claude -p`) is autonomous — the up-to-2.5x speed gain doesn't justify a 2x cost when no human is waiting. Revisit if:

1. Pricing drops relative to standard
2. The autonomous loop becomes interactive (unlikely by design)
3. Time-boxed runs need faster turnaround

## Sources

| Source | Content |
|---|---|
| [CC Fast Mode docs][cc-fast] | Claude Code toggles, defaults, version gates, billing, rate-limit fallback, platform list |
| [API Fast mode docs][api-fast] | `speed` parameter, model status, beta header, rate-limit headers, platforms, Batch/Priority Tier exclusions |
| [CC feature availability][cc-features] | Per-provider feature matrix (fast mode ✗ on Bedrock, Foundry; Agent Platform per the 2026-11-08 read, now superseded by the fast-mode page); Ultra plan name |
| [Claude Models on Google Cloud overview][gcp-overview] | Anthropic-managed vs Google-managed offerings |
| [Claude API pricing][pricing] | Standard Opus rates for the 2x comparison |
| [CC Model Configuration][cc-model] | Effort defaults |
| [CC Cost Management][cc-costs] | Usage-credit billing context |
| [CC CLI Reference][cc-cli] | `--settings` flag |
| [CC CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) / [fast-mode page](https://code.claude.com/docs/en/fast-mode) | Vertex fast mode, v2.1.322–323 (accessed 2026-11-17) |

[cc-fast]: https://code.claude.com/docs/en/fast-mode
[api-fast]: https://platform.claude.com/docs/en/build-with-claude/fast-mode
[pricing]: https://platform.claude.com/docs/en/about-claude/pricing
[cc-features]: https://code.claude.com/docs/en/feature-availability
[gcp-overview]: https://platform.claude.com/docs/en/build-with-claude/claude-models-on-google-cloud/overview
[cc-model]: https://code.claude.com/docs/en/model-config
[cc-costs]: https://code.claude.com/docs/en/costs
[cc-cli]: https://code.claude.com/docs/en/cli-reference
