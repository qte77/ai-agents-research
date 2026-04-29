---
title: Devstral Analysis
source: https://mistral.ai/news/devstral, https://huggingface.co/mistralai/Devstral-Small-2-24B-Instruct-2512, https://huggingface.co/mistralai/Devstral-Small-2507, https://huggingface.co/mistralai/Devstral-Small-2505
purpose: Analysis of Devstral as an open-source agentic coding LLM — SWE-Bench performance, OpenHands scaffold lineage, local deployability, cost profile, and integration with Claude Code as an alternative model backend.
created: 2026-04-26
updated: 2026-04-26
validated_links: 2026-04-26
---

**Status**: Assess (open-source, active, agentic-first design)

## What It Is

Devstral is an open-source LLM family by Mistral AI built specifically for **agentic software-engineering tasks** — exploring codebases, editing multiple files, and powering coding agents. Released under **Apache 2.0** in collaboration with [All Hands AI][all-hands] (the team behind [OpenHands][openhands], the de-facto open-source SWE-Bench reference scaffold).

Three releases to date, all 24B parameters:

| Release | Date | Context | SWE-Bench Verified | Base model |
|---|---|---|---|---|
| Devstral Small 1.0 (2505) | 2025-05-21 | 128k | 46.8% | Mistral-Small-3.1 |
| Devstral Small 1.1 (2507) | 2025-07 | 128k | 53.6% | Mistral-Small-3.1 |
| **Devstral Small 2 (2512)** | 2025-12 | **256k** | **68.0%** | Mistral-Small-3.1-24B-Base-2503 |

A larger **Devstral 2 (123B)** scores **72.2%** SWE-Bench Verified, approaching closed frontier models ([Devstral Small 2 model card][devstral-2-card]).

## Why It Matters

**Open SOTA for agentic coding.** No other open-source 24B model approaches Devstral's SWE-Bench numbers. The closest comparison points:

| Model | SWE-Bench Verified | License |
|---|---|---|
| Claude Sonnet 4.5 | 77.2% | Closed |
| Gemini 3 Pro | 76.2% | Closed |
| **Devstral 2 (123B)** | 72.2% | Apache 2.0 |
| **Devstral Small 2 (24B)** | 68.0% | Apache 2.0 |
| Devstral Small 1.1 (24B) | 53.6% | Apache 2.0 |
| Devstral Small 1.0 (24B) | 46.8% | Apache 2.0 |
| Deepseek-V3-0324 (671B) | <53.6% under OpenHands | MIT |
| Qwen3 232B-A22B | <53.6% under OpenHands | Apache 2.0 |

Devstral 1.0 already beat Deepseek-V3 (671B) and Qwen3 (232B) **under the same OpenHands scaffold**, despite being ~25× smaller — agentic-first training matters more than parameter count for SWE-Bench ([Mistral news][devstral-news]).

## Architecture

Devstral 2 (2512) was distilled from `Mistral-Small-3.1-24B-Base-2503`, with key additions versus 2507 ([Devstral Small 2 model card][devstral-2-card]):

- **Vision** — image analysis enabled (predecessors were text-only)
- **Scalable softmax attention** — temperature scaling per [arXiv:2501.19399][softmax-paper], same approach as Ministral 3, rope-scaling Llama 4-style
- **Better generalization** — across diverse prompts and coding environments
- **256k context** — doubled from 128k, supports `--max-model-len 262144` in vLLM
- **FP8 quantization** — float8_e4m3 format ships natively

Recommended sampling: `temperature=0.15`. System prompt loaded from the model repo (`CHAT_SYSTEM_PROMPT.txt`) and formatted with current/yesterday dates per inference call.

## Local Deployability

Designed for **on-device use** — runs on single RTX 4090 GPU or Apple Silicon Mac with 32GB RAM ([Mistral news][devstral-news]). This is the primary differentiator versus Claude/GPT/Gemini for privacy-sensitive enterprise repos and air-gapped environments.

Distribution channels:

| Channel | Use case |
|---|---|
| [Hugging Face][devstral-2-card] | Direct download, vLLM/Transformers serving |
| [Ollama][ollama-devstral] | Local inference, simplest path |
| [LM Studio][lmstudio-devstral] | macOS/Windows GUI |
| Mistral API | Hosted inference, $0.10/M in, $0.30/M out |
| Kaggle, Unsloth, Bartowski | Community quantizations (GGUF, etc.) |

## Pricing

API pricing on Mistral La Plateforme ([Mistral news][devstral-news]):

| Model | Input | Output |
|---|---|---|
| `devstral-small-2505` | $0.10 / M tokens | $0.30 / M tokens |
| Claude Sonnet 4.6 | $3 / M | $15 / M |
| Claude Opus 4.7 | $15 / M | $75 / M |

Devstral Small is ~30× cheaper than Sonnet input, ~50× cheaper output. Devstral 2 (123B) pricing not publicly listed at the time of writing.

## Mistral Vibe CLI

Released alongside Devstral 2: a **CLI agent harness** distributed via `uv tool install mistral-vibe` or `pip install mistral-vibe` ([Devstral Small 2 model card][devstral-2-card]). Direct competitor to Claude Code, Codex CLI, Aider — Mistral's own first-party scaffold for Devstral.

```bash
uv tool install mistral-vibe
vibe   # creates ~/.vibe/config.toml on first run
```

Not analyzed in depth here — separate investigation if/when adoption grows.

## Integration with Claude Code

The Devstral 2 model card explicitly lists **Claude Code** among supported agentic frameworks ([Devstral Small 2 model card][devstral-2-card]):

> Mistral Vibe CLI, Cline, Kilo Code, **Claude Code**, OpenHands, SWE Agent

This means Devstral can run as the underlying model when Claude Code is configured via custom API endpoints (e.g. through provider routers like OpenRouter, or local vLLM/Ollama exposing OpenAI-compatible APIs). The CC harness — slash commands, hooks, skills, tool dispatch — works on top, with Devstral providing inference. Practical use case: cost-sensitive or privacy-sensitive workflows where Claude Code's UX is preferred but Anthropic API consumption is undesirable.

Cross-ref: [CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md) for CC's model routing options.

## Adoption Considerations

**Strengths**:

- Highest open-source SWE-Bench numbers (68.0% / 72.2%)
- Apache 2.0 — commercial-friendly, no attribution
- Single-GPU local deployment (RTX 4090 / Mac 32GB)
- 30–50× cheaper than Claude API at the small-model tier
- Multi-harness — runs under Mistral Vibe, OpenHands, SWE Agent, Cline, Kilo Code, **Claude Code**
- 256k context (Devstral 2) and vision

**Risks / Limits**:

- Still 5–9 pts behind Claude Sonnet 4.5 / Gemini 3 Pro on SWE-Bench
- Optimized for OpenHands-style scaffolds — may underperform on harnesses with different tool semantics
- Trained against vibe-coding-style traces — reasoning depth on novel/research code less benchmarked
- Mistral La Plateforme region/SLA differs from major US clouds
- Larger Devstral 2 (123B) requires multi-GPU serving

**Roadmap**: Mistral Small 4 (2603, March 2026, 119B, 256k) is a hybrid model unifying Instruct + Reasoning + Devstral capabilities into a single line ([Mistral Small 4 card][mistral-small-4]) — Devstral capabilities are now being absorbed into the unified Mistral model line, and standalone Devstral releases may slow.

## Cross-References

- [docs/cc-community/CC-community-tooling-landscape.md](../cc-community/CC-community-tooling-landscape.md) — OpenHarness (HKUDS, the open-source agent harness analyzed in this repo, is a CC-convention-compatible peer to OpenHands)
- [docs/cc-native/configuration/CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md) — CC's model routing for non-Anthropic backends
- [docs/non-cc/goose-analysis.md](goose-analysis.md) — Block Goose, MCP-native open-source agent (different positioning: Goose is a harness, Devstral is a model)

## Sources

| Source | Content |
|---|---|
| [Mistral Devstral announcement][devstral-news] | Initial release, OpenHands collaboration, pricing, SWE-Bench 1.0 numbers |
| [Devstral Small 2 model card][devstral-2-card] | 2512 release: 68.0% SWE-Bench, vision, scalable softmax, supported frameworks |
| [Devstral Small 1.1 model card][devstral-2507] | 2507 release: 53.6% SWE-Bench |
| [Devstral Small 1.0 model card][devstral-2505] | 2505 release: 46.8% SWE-Bench |
| [Mistral Small 4 model card][mistral-small-4] | Hybrid model absorbing Devstral capabilities (Mar 2026) |
| [Scalable-Softmax paper][softmax-paper] | Attention temperature scaling used in Devstral 2 |
| [OpenHands][openhands] | All Hands AI's open-source SWE-Bench reference scaffold |

[devstral-news]: https://mistral.ai/news/devstral
[devstral-2-card]: https://huggingface.co/mistralai/Devstral-Small-2-24B-Instruct-2512
[devstral-2507]: https://huggingface.co/mistralai/Devstral-Small-2507
[devstral-2505]: https://huggingface.co/mistralai/Devstral-Small-2505
[mistral-small-4]: https://huggingface.co/mistralai/Mistral-Small-4-119B-2603
[softmax-paper]: https://arxiv.org/abs/2501.19399
[openhands]: https://github.com/All-Hands-AI/OpenHands
[all-hands]: https://www.all-hands.dev/
[ollama-devstral]: https://ollama.com/library/devstral-small-2
[lmstudio-devstral]: https://lmstudio.ai/models/devstral-2
