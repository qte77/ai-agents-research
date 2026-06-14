---
title: CC Models & Free-Tier Provider Reference
source: https://platform.claude.com/docs/en/about-claude/models/overview, https://platform.claude.com/docs/en/about-claude/pricing
purpose: Descriptive reference for the newest Claude model (Fable 5) and a snapshot of free-tier / OSS inference providers — the model/provider facts behind CC-model-provider-configuration.md.
created: 2026-06-14
updated: 2026-06-14
validated_links: 2026-06-14
---

**Status**: Reference (descriptive). For *how to configure* CC against these models/providers (env vars, endpoints, gateways), see [CC-model-provider-configuration.md](CC-model-provider-configuration.md).

## Claude Fable 5 (newest model)

Claude Fable 5 (`claude-fable-5`) — Anthropic's most capable widely released model, built for complex, long-running agentic work — is selectable in CC via `/model` or `ANTHROPIC_MODEL=claude-fable-5`. Generally available on the Claude API and major clouds since 2026-06-09 ([source][fable5-intro]).

| Property | Value |
| -------- | ----- |
| Model ID | `claude-fable-5` |
| Context / max output | 1M tokens (default) / 128K tokens ([source][models-overview]) |
| Pricing | $10 / $50 per MTok (input / output) — above Opus-tier's $5 / $25 ([source][models-pricing]) |
| Thinking | Adaptive only, always on (`thinking: disabled` unsupported); tune depth with `CLAUDE_CODE_EFFORT_LEVEL` / effort `low`–`xhigh`/`max` ([source][fable5-intro]) |

CC-relevant caveats ([source][fable5-intro]):

- **New tokenizer** (the one introduced with Opus 4.7): the same text is ~30% more tokens than on pre-4.7 models — re-baseline cost and `CLAUDE_CODE_MAX_OUTPUT_TOKENS` expectations.
- **`refusal` stop reason**: safety classifiers may decline a request as a successful HTTP 200 (not an error); plan for refusal handling and fallback to another model.
- **30-day data retention required** — not available to zero-data-retention orgs.
- **CC plan access** (per the in-product `/model` notice, 2026-06): included in Claude plan limits until 2026-06-22, after which it continues via usage credits.

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
- [Anthropic — Models Overview][models-overview]
- [Anthropic — Pricing][models-pricing]

[fable5-intro]: https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5
[models-overview]: https://platform.claude.com/docs/en/about-claude/models/overview
[models-pricing]: https://platform.claude.com/docs/en/about-claude/pricing
