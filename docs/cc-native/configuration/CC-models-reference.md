---
title: CC Models & Free-Tier Provider Reference
source: https://platform.claude.com/docs/en/about-claude/models/overview, https://platform.claude.com/docs/en/about-claude/pricing
purpose: Descriptive reference for CC's primary agentic model (Claude Fable 5, superseded by Claude Fable 5.2), the current per-model pricing table, and a snapshot of free-tier / OSS inference providers — the model/provider facts behind CC-model-provider-configuration.md.
created: 2026-06-14
updated: 2026-11-13
validated_links: 2026-11-12
status: reference
---

**Details:** Reference (descriptive). For *how to configure* CC against these models/providers (env vars, endpoints, gateways), see [CC-model-provider-configuration.md](CC-model-provider-configuration.md).

## Claude Fable 5 (CC's primary agentic model)

Claude Fable 5 (`claude-fable-5`) — Anthropic's most capable widely released model, built for complex, long-running agentic work — is selectable in CC via `/model` or `ANTHROPIC_MODEL=claude-fable-5`. Generally available on the Claude API and major clouds since 2026-06-09 ([source][fable5-intro]).

**Claude Fable 5.2** (`claude-fable-5-2`) has since superseded it as Anthropic's current flagship, listed first under "Latest models" on the models overview page — "now the default Fable model," per the CC changelog, selectable via `/model` or `ANTHROPIC_MODEL=claude-fable-5-2` as of **CC v2.1.321+** ([source][changelog]). The models page recommends it "for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5.5 at higher effort still fall short" ([source][models-overview]). **Claude Mythos 5.2** ships alongside it but — like Mythos 5 and 5.1 before it — stays limited-availability, gated behind Anthropic's verification programs such as the Cyber Verification Program ([source][models-pricing]); Fable 5.1 and 5.2 are both generally available, not limited.

Anthropic's announcement ([source][fable52-intro], 2026-11-09) frames Fable 5.2 as "a step above Opus 5.5 in almost all the capabilities we evaluated." Figures stated directly in the post's text (not read off its comparison table, whose column alignment this doc does not reproduce): a RoboDojo Sim score of 64.9% at Max effort (vs. 27.6% for Fable 5.1 and 29.8% for GPT-6 Astra), a BenchCAD 2.1 score of 83.5 at Max effort (vs. 65.3 for Opus 5.5 and 44.4 for Fable 5.1), and — for Mythos 5.2 — "10.2% more vulnerabilities than Claude Opus 5.5 and 14.4% more than Claude Mythos 5.1" on its internal CVE-rediscovery benchmark. The post's own table also lines Fable 5.2 up against GPT-6 Astra and Gemini 4 Carbon on a wider benchmark set; read it directly for that full matrix.

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

Snapshot of inference providers with free or trial tiers — useful when routing CC (via proxy) or sibling agents (OpenCode, n8n, PydanticAI) to non-Anthropic models. Free-tier terms and model ids change frequently: **the rows below are a February 2026 snapshot** (except Infomaniak, verified June 2026); confirm current offerings on each provider's site before relying on them.

| Provider | Free Tier | Example Model (API ID) | Context | Output | Tools | Notes / Limit |
| --- | --- | --- | --- | --- | --- | --- |
| **infomaniak** | 1M credits, 1-mo trial | OSS via OpenAI API: `qwen3`, `mistral3`, `gemma3`, `llama3` | model-dependent | — | Yes | EU/Swiss-hosted; OpenAI-compatible (proxy for CC) |
| **gemini** | Truly free | `gemini-2.0-flash` | 1M | 8K | Yes | 15 RPM, ~1.5K RPD |
| **github** | Truly free | `gpt-4.1-mini` | 1M | 32K | Yes | 15 RPM, ~150 RPD |
| **cerebras** | Truly free | `gpt-oss-120b` | 128K | 8K | Yes | 30 RPM, 1M TPD |
| **groq** | Truly free | `llama-3.3-70b-versatile` | 131K | 32K | Yes | 30 RPM, 1K RPD |
| **mistral** | Truly free | `open-mistral-nemo` | 128K | 4K | Yes | 1 RPS, 1B tokens/mo |
| **openrouter** | Truly free | `qwen/qwen3-next-80b-a3b-instruct:free` | 262K | 8K | Yes | 20 RPM, 50 RPD |
| **cohere** | Truly free | `command-a-03-2025` | 256K | 8K | Yes | 20 RPM, 1K calls/mo |
| **deepseek** | 5M free tokens | `deepseek-chat` | 128K | 8K | Yes | Spend-limited |
| **grok** | $25 trial credit | `grok-3-mini` | 131K | 32K | Yes | Spend-limited |
| **sambanova** | $5 trial + limited free | `Meta-Llama-3.3-70B-Instruct` | 128K | 8K | Yes | Free: 40 RPD |
| **nebius** | $1 trial credit | `meta-llama/Meta-Llama-3.1-70B-Instruct` | 128K | 8K | Yes | $1 credit |
| **fireworks** | $1 trial credit | `accounts/fireworks/models/llama-v3p3-70b-instruct` | 131K | 8K | Yes | $1 credit |
| **together** | No free tier | `meta-llama/Llama-3.3-70B-Instruct-Turbo` | 128K | 8K | Yes | $5 min purchase |
| **perplexity** | No free API tier | `sonar` | 127K | 4K | Limited | Credits required |
| **huggingface** | ~$0.10/mo | `meta-llama/Meta-Llama-3.3-70B-Instruct` | 128K | 8K | Yes | ~10 calls on free |
| **ollama** | Always free (local) | `llama3.3:70b` | 128K | 8K | Yes | Hardware-bound (local) |

> **OpenAI-compatible tool calling**: some providers reject strict tool-definition schemas — `groq`, `cerebras`, `fireworks`, `together`, `sambanova`. With PydanticAI, set `OpenAIModelProfile(openai_supports_strict_tool_definition=False)` for these.

(`restack`, which appears on some provider lists, is a workflow-orchestration platform — not an inference provider; it proxies to others.)

## Cross-References

- [CC-model-provider-configuration.md](CC-model-provider-configuration.md) — how to point CC at these models/providers (env vars, endpoints, gateways, decision matrix)

## References

- [Anthropic — Introducing Claude Fable 5 & Mythos 5][fable5-intro]
- [Anthropic — Introducing Claude Fable 5.2 & Mythos 5.2][fable52-intro]
- [Anthropic — Models Overview][models-overview]
- [Anthropic — Pricing][models-pricing]
- [Claude Code CHANGELOG.md][changelog] — `v2.1.321` adds `claude-fable-5-2` as the default Fable model
- [Anthropic PBC — Form S-1/A (SEC EDGAR, filed 2026-11-10)][s1a] — multi-chip compute approach, fungible compute pool
- [AMD — AMD and Anthropic strategic partnership (2026-07-22)][amd-release] — MI450 Series deployment, existing MI355X use

[fable5-intro]: https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5
[fable52-intro]: https://www.anthropic.com/news/claude-fable-and-mythos-5-2
[models-overview]: https://platform.claude.com/docs/en/about-claude/models/overview
[models-pricing]: https://platform.claude.com/docs/en/about-claude/pricing
[changelog]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
[s1a]: https://www.sec.gov/Archives/edgar/data/2130357/000162828026072484/anthropicpbc-sx1ax2.htm
[amd-release]: https://newsroom.amd.com/news/amd-anthropic-strategic-partnership/
