---
title: CC Models & Free-Tier Provider Reference
source: https://platform.claude.com/docs/en/about-claude/models/overview
purpose: Descriptive reference for CC's primary agentic model (Claude Fable 5, superseded by Claude Fable 5.2), the 5.x lifecycle and the current per-model pricing table — the model facts behind CC-model-provider-configuration.md, which owns provider facts.
created: 2026-06-14
updated: 2026-11-23
validated_links: 2026-11-12
status: reference
---

**Details:** Reference (descriptive). For *how to configure* CC against these models/providers (env vars, endpoints, gateways), see [CC-model-provider-configuration.md](CC-model-provider-configuration.md), which also owns the free-tier and OSS provider facts.

## Claude Fable 5 (CC's primary agentic model)

Claude Fable 5 (`claude-fable-5`) — Anthropic's most capable widely released model, built for complex, long-running agentic work — is selectable in CC via `/model` or `ANTHROPIC_MODEL=claude-fable-5`. Generally available on the Claude API and major clouds since 2026-06-09 ([source][fable5-intro]).

**Claude Fable 5.2** (`claude-fable-5-2`) has since superseded it as Anthropic's current flagship, listed first under "Latest models" on the models overview page — "now the default Fable model," per the CC changelog, selectable via `/model` or `ANTHROPIC_MODEL=claude-fable-5-2` as of **CC v2.1.321+** ([source][changelog]). The models page recommends it "for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still fall short" ([source][models-overview]). **Claude Mythos 5.2** ships alongside it but — like Mythos 5 and 5.1 before it — stays limited-availability, gated behind Anthropic's verification programs such as the Cyber Verification Program ([source][models-overview]); Fable 5.1 and 5.2 are both generally available, not limited. The announcement says Fable and Mythos are the same underlying model: Fable carries cybersecurity and biology safeguards that let it ship to all users, and organizations pursuing cybersecurity or biomedical research can apply for Mythos through the Life Sciences and Cyber Verification Programs ([source][fable52-intro], read 2026-11-23). The same post says Fable 5.2's safeguards "will block most cybersecurity-related tasks" and that blocked queries get a response from Opus 4.8 (cyber) or Opus 5 (biology).

Anthropic's announcement ([source][fable52-intro], 2026-11-09) claims (vendor benchmark claims, not independently verified here) that Fable 5.2 and Mythos 5.2 are "a step above Opus 5.5 in almost all the capabilities we evaluated." Figures stated directly in the post's text (not read off its comparison table, whose column alignment this doc does not reproduce): a RoboDojo Sim score of 64.9% at Max effort (vs. 27.6% for Fable 5.1 and 29.8% for GPT-6 Astra), a BenchCAD 2.1 score of 83.5 at Max effort (vs. 65.3 for Opus 5.5 and 44.4 for Fable 5.1), and — for Mythos 5.2 — "10.2% more vulnerabilities than Claude Opus 5.5 and 14.4% more than Claude Mythos 5.1" on its internal CVE-rediscovery benchmark. The post's own table also lines Fable 5.2 up against GPT-6 Astra and Gemini 4 Carbon on a wider benchmark set; read it directly for that full matrix.

**Hardware these models run on (dated note, 2026-11-13).** Anthropic's S-1/A, filed with the SEC on 2026-11-10, says it trains and serves Claude "natively across four major chip families (AWS Trainium, Google TPUs, NVIDIA GPUs, and AMD GPUs)" and treats that capacity as "a single, fungible pool from multiple strategic partners" ([source][s1a]). The filing also says: "By leveraging Claude, our engineering teams can now bring new chip platforms into production more quickly." It contrasts "intense engineering effort over many months" in the past with "a fraction of the time it once took" now, but gives no figure for the new duration. A chart shared on X on 2026-11-11 puts a number on it for Mythos on AMD hardware. That number isn't in the filing's text, and this note hasn't traced the chart to an Anthropic source, so it doesn't repeat it. AMD's 2026-07-22 release covers deploying up to 2 GW of Instinct MI450 Series GPUs in Helios racks, with the first gigawatt starting in the first half of 2027. The release says the deal "builds on Anthropic's existing use of AMD Instinct™ MI355X GPUs" and that the teams "will use Claude to optimize workloads for AMD Instinct GPUs and accelerate ROCm software development" ([source][amd-release]). Neither source mentions CUDA.

| Property | Value |
| -------- | ----- |
| Model ID | `claude-fable-5` |
| Context / max output | 1M tokens (default) / 128K tokens ([source][models-overview]) |
| Pricing | $10 / MTok input, $50 / MTok output — see the full current per-model table below ([source][models-pricing]) |
| Thinking | Adaptive only, always on (`thinking: disabled` unsupported); tune depth with `CLAUDE_CODE_EFFORT_LEVEL` / effort `low`–`xhigh`/`max` ([source][fable5-intro]) |

CC-relevant caveats ([source][fable5-intro]):

- **New tokenizer** (introduced with Opus 4.7, shared with Opus 4.8): the same text is roughly 1×–1.35× the tokens of pre-4.7 models (varies by content) — re-baseline cost and `CLAUDE_CODE_MAX_OUTPUT_TOKENS` expectations. Token counts are roughly unchanged when moving between Opus 4.7/4.8 and Fable 5. The [pricing page][models-pricing] independently describes this same newer tokenizer (Claude 4.7 and later models, and Claude Mythos Preview) as producing "approximately 30% more tokens for the same text" than the tokenizer used by Claude Sonnet 4.6 and earlier models — a second, corroborating source for the same effect.
- **`refusal` stop reason**: safety classifiers may decline a request as a successful HTTP 200 (not an error); plan for refusal handling and fallback to another model.
- **30-day data retention required** — not available to zero-data-retention orgs.
- **CC plan access** (per the in-product `/model` notice, 2026-06): included in Claude plan limits through 2026-06-22; from 2026-06-22 it continues via usage credits.

## Claude 5.x lifecycle, defaults and Fable 5.2 breaking changes

Documented on the per-model overview pages, the Fable 5.2 migration guide and the model-deprecations page, all read 2026-11-23 ([Fable 5.2][fable52-overview], [Opus 5.5][opus55-overview], [Sonnet 5.5][sonnet55-overview], [migration guide][fable52-migration], [deprecations][deprecations]). All three models list a 1M-token context window, 128K max output and a Jun 2026 knowledge cutoff.

| Model | Released | Retirement | Default effort | Thinking | Batch output (beta) |
| --- | --- | --- | --- | --- | --- |
| Claude Fable 5.2 (`claude-fable-5-2`) | 2026-11-09 | not sooner than 2027-11-09 | high | adaptive, always on | not listed on its page |
| Claude Opus 5.5 (`claude-opus-5-5`) | 2026-09-22 | not sooner than 2027-09-22 | medium | adaptive, always on | 300K tokens |
| Claude Sonnet 5.5 (`claude-sonnet-5-5`) | 2026-09-28 | not sooner than 2027-09-28 | high | adaptive; lowest setting `between_tools` (no up-front thinking), usable at high effort or below | 300K tokens |

- **300K batch output** needs the `output-300k-2026-03-24` beta header on the Message Batches API; the Opus 5.5 and Sonnet 5.5 pages both state it.
- **Cache minimum**: 512 tokens on Opus 5.5 and Sonnet 5.5 (their pages), and on Fable 5.2 and Mythos 5.2 per the [caching docs][caching-docs] (see [CC-prompt-caching-behavior.md](../context-memory/CC-prompt-caching-behavior.md#minimum-cacheable-prefix)).
- **Fable 5.2 pricing re-read**: the overview page matches the [pricing table below](#model-pricing-current-lineup). Batch is $4 / $20 and fast mode (up to 2.5x token generation speed, per the announcement) is $16 / $80 per MTok (what's-new page, 2026-11-23). Opus 5.5 and Sonnet 5.5 rows also match their pages.
- **Data retention**: Fable 5.2 and Mythos 5.2 require 30-day retention and are not available under zero data retention unless Anthropic expressly authorizes it; on the Claude API a request from an org or workspace without 30-day retention returns a 400. Priority Tier is not supported on either.
- **Rate limits**: Fable 5.2 has its own limit, separate from the one Fable 5.1 and Fable 5 share; Mythos 5.2 shares one combined limit with Mythos 5.1 and Mythos 5.

**Breaking changes from Fable 5.1 (documented, migration guide).** Four can break code:

1. **Prefix check.** Each request is checked: if `system`, `tools` or earlier messages changed since a thinking block was produced and that block is sent back, the API returns a 400 ("The block is bound to a different conversation"). Retrying unchanged does not help. Claude Code, claude.ai, Managed Agents and the Agent SDK manage history themselves, so nothing changes for them. The `thinking-binding-controls-2026-08-01` beta header with `thinking.block_binding.prefix_mismatch_behavior: "drop_block"` drops the affected blocks instead; the guide calls that a stopgap because dropped blocks can raise output tokens. For the cache angle see [CC-prompt-caching-behavior.md](../context-memory/CC-prompt-caching-behavior.md#api-level-invalidation-platform-docs).
2. **Thinking blocks are model- and account-bound.** On the Claude API and Google-managed Claude Models on Google Cloud, Fable 5.2 and Mythos 5.2 read many earlier models' blocks (including Opus 5.5, Sonnet 5.5, Haiku 5.5, Fable 5.1), but no other model reads theirs; the API drops unreadable blocks (request succeeds, dropped blocks not billed), so a router or refusal fallback to another model continues without that reasoning. Blocks also work only in the account that produced them or a linked account.
3. **`computer_20251124` returns a 400** on every platform except Amazon Bedrock; use the `computer_toolset_20260801` toolset.
4. **Advisor pairing**: see [CC-advisor-tool-analysis.md](CC-advisor-tool-analysis.md#pairing-summary).

Settings unchanged from Fable 5.1 per the guide: thinking cannot be disabled (`disabled` and manual `budget_tokens` return 400), assistant prefill returns 400, `temperature`, `top_p` and `top_k` should be omitted, and forced `tool_choice` (`any` or `tool`) returns 400 (relative to Fable 5 this one is breaking). Behavior notes from the same guide (Anthropic's own testing): prompt lines asking for less thinking do not stop thinking at medium effort and above, and at xhigh or max in an agentic coding product the model was seen starting subagents to review its own work. Permitted refusal-fallback targets for Fable 5.2 are Opus 4.8 and Opus 5.

**Deprecations (deprecations page, 2026-11-23).** `claude-sonnet-4-5-20250929` (and the undated `claude-sonnet-4-5`) retires 2026-11-30, with `claude-sonnet-5-5` as the recommended replacement. `claude-mythos-preview` is listed as deprecated since 2026-06-09 with its retirement date "to be announced"; it has no announced end-of-life date on that page.

## Model Pricing (current lineup)

Per-model USD pricing from the [pricing page][models-pricing] (accessed 2026-10-26), all rates per million tokens (MTok):

| Model | Input | 5m cache write | 1h cache write | Cache hit | Output |
| --- | --- | --- | --- | --- | --- |
| Claude Fable 5.2 | $8 | $10 | $16 | $0.20 (0.025x) | $40 |
| Claude Mythos 5.2 (limited availability) | $8 | $10 | $16 | $0.20 (0.025x) | $40 |
| Claude Fable 5.1 | $10 | $12.50 | $20 | $0.25 (0.025x) | $50 |
| Claude Mythos 5.1 (limited availability) | $10 | $12.50 | $20 | $0.25 (0.025x) | $50 |
| Claude Fable 5 | $10 | $12.50 | $20 | $1 (0.1x) | $50 |
| Claude Mythos 5 (limited availability) | $10 | $12.50 | $20 | $1 (0.1x) | $50 |
| Claude Opus 5.5 | $4 | $5 | $8 | $0.20 (0.05x) | $20 |
| Claude Opus 5 | $5 | $6.25 | $10 | $0.50 (0.1x) | $25 |
| Claude Opus 4.8 | $5 | $6.25 | $10 | $0.50 (0.1x) | $25 |
| Claude Opus 4.7 | $5 | $6.25 | $10 | $0.50 (0.1x) | $25 |
| Claude Opus 4.6 | $5 | $6.25 | $10 | $0.50 (0.1x) | $25 |
| Claude Opus 4.5 | $5 | $6.25 | $10 | $0.50 (0.1x) | $25 |
| Claude Sonnet 5.5 | $2 | $2.50 | $4 | $0.10 (0.05x) | $10 |
| Claude Sonnet 5 | $2 | $2.50 | $4 | $0.20 (0.1x) | $10 |
| Claude Sonnet 4.6 | $3 | $3.75 | $6 | $0.30 (0.1x) | $15 |
| Claude Sonnet 4.5 | $3 | $3.75 | $6 | $0.30 (0.1x) | $15 |
| Claude Haiku 5.5 (≤100,000-token prompts) | $0.10 | $0.125 | $0.20 | $0.01 (0.1x) | $0.50 |
| Claude Haiku 5.5 (>100,000-token prompts) | $0.50 | $0.625 | $1 | $0.05 (0.1x) | $2.50 |
| Claude Haiku 4.5 | $1 | $1.25 | $2 | $0.10 (0.1x) | $5 |

Cache-hit multiplier is 0.025x base input on Fable 5.2/Mythos 5.2/Fable 5.1/Mythos 5.1, 0.05x on Opus 5.5/Sonnet 5.5, and the standard 0.1x on every other model above.

**Claude Sonnet 5's $2/$10 per-MTok input/output price is now the standard rate, not introductory pricing.** Per the pricing page's footnote, this rate was "announced at launch as introductory pricing through August 31, 2026, is now the standard price. The previously scheduled increase to $3/$15 per million input/output tokens on September 1, 2026 will not occur."

## Free-Tier & OSS Provider Reference

Moved 2026-11-23: provider facts (endpoints, auth, free tiers, which models each provider serves) now live in one place, [CC-model-provider-configuration.md § Free-tier and OSS inference providers](CC-model-provider-configuration.md#free-tier-and-oss-inference-providers) and the provider sections around it. This doc keeps model facts only: IDs, pricing, lifecycle.

## Cross-References

- [CC-model-provider-configuration.md](CC-model-provider-configuration.md) — how to point CC at these models and at other providers (env vars, endpoints, free tiers, gateways, decision matrix)

## References

- [Anthropic — Introducing Claude Fable 5 & Mythos 5][fable5-intro]
- [Anthropic — Introducing Claude Fable 5.2 & Mythos 5.2][fable52-intro]
- [Anthropic — Models Overview][models-overview]
- [Anthropic — Claude Fable 5.2 overview][fable52-overview], [Opus 5.5 overview][opus55-overview], [Sonnet 5.5 overview][sonnet55-overview], [Fable 5.2 migration guide][fable52-migration] and [Model deprecations][deprecations] (read 2026-11-23)
- [Anthropic — Pricing][models-pricing]
- [Claude Code CHANGELOG.md][changelog] — `v2.1.321` adds `claude-fable-5-2` as the default Fable model
- [Anthropic PBC — Form S-1/A (SEC EDGAR, filed 2026-11-10)][s1a] — multi-chip compute approach, fungible compute pool
- [AMD — AMD and Anthropic strategic partnership (2026-07-22)][amd-release] — MI450 Series deployment, existing MI355X use

[fable5-intro]: https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5
[fable52-intro]: https://www.anthropic.com/claude-fable-and-mythos-5-2
[models-overview]: https://platform.claude.com/docs/en/about-claude/models/overview
[fable52-overview]: https://platform.claude.com/docs/en/models/fable-5-2/overview
[opus55-overview]: https://platform.claude.com/docs/en/models/opus-5-5/overview
[sonnet55-overview]: https://platform.claude.com/docs/en/models/sonnet-5-5/overview
[fable52-migration]: https://platform.claude.com/docs/en/models/fable-5-2/migration-guide
[deprecations]: https://platform.claude.com/docs/en/about-claude/model-deprecations
[caching-docs]: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[models-pricing]: https://platform.claude.com/docs/en/about-claude/pricing
[changelog]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
[s1a]: https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/anthropicpbc-sx1ax2.htm
[amd-release]: https://newsroom.amd.com/news/amd-anthropic-strategic-partnership/
