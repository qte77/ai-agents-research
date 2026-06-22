---
title: LLM Routers & Gateways Landscape
source: https://openrouter.ai/
purpose: Provider-agnostic model routers, hosted aggregators, self-hostable gateways, and model-fusion/ensemble routing tools — a reference catalog verified 2026-06-16.
created: 2026-06-16
updated: 2026-06-22
validated_links: 2026-06-16
---

**Status**: Reference (informational catalog)

## What It Is

A survey of provider-agnostic LLM routers, API gateways, and model aggregators — tools that sit between an AI client and one or more inference backends to add routing, failover, cost control, and observability. Unlike Claude Code-specific proxies (see [CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md)), the tools here are general-purpose: they serve any SDK, agent framework, or coding-agent harness that speaks OpenAI-compatible or Anthropic-compatible APIs. Several entries — OpenRouter and LiteLLM in particular — also appear in the CC-routing doc as Claude Code integration targets; those cross-references are noted inline. Entries are organized into three groups: open/self-hostable gateways, hosted aggregators, and model-fusion/ensemble routing.

---

## Open / Self-Hostable Gateways

| Tool | License | Pricing | Models / Providers | Differentiator |
|---|---|---|---|---|
| [LiteLLM](https://github.com/BerriAI/litellm) | MIT (enterprise dir: separate) | Free self-hosted; enterprise custom | 100+ providers incl. OpenAI, Anthropic, Gemini, Azure, Bedrock, Vertex, Cohere, vLLM, HuggingFace | Python SDK + proxy server; 50.5 k stars; v1.89.0 (2026-06-14); cost tracking, load balancing, guardrails, MCP gateway support; also appears in CC-routing doc |
| [Portkey](https://portkey.ai/) | MIT (OSS gateway); managed: proprietary | Free self-hosted / managed from $49/month | 1,600+ LLMs across 200+ providers | TypeScript gateway (12.1 k stars); dedicated Claude Code Gateway product page; Anthropic/Bedrock/Vertex backends; RBAC, guardrails, semantic caching |
| [Bifrost](https://www.getmaxim.ai/bifrost/) | Apache 2.0 | Free self-hosted; enterprise hosted (no public price) | 23+ providers, 1,000+ models (OpenAI, Anthropic, Bedrock, Vertex, Azure, Cerebras, Mistral, Groq, Ollama) | Go implementation; claims 50× lower P99 latency vs LiteLLM; 5.8 k stars; v1.4.9 (2026-06-15); adaptive load balancer, provider fallback, semantic caching, MCP gateway |
| [Helicone AI Gateway](https://www.helicone.ai/) | Apache-2.0 | Hobby free (10 k req/month); Pro $79/month; Team $799/month; Enterprise on-prem | 100+ models incl. OpenAI, Anthropic, Azure, Gemini, DeepSeek, Groq, OpenRouter | TypeScript (91.2%); 5.8 k stars; v2025.08.21-1; observability-first — request logging, cost tracking, agent tracing, prompt management; SOC-2/HIPAA on Team+ |
| [Arch Gateway (archgw)](https://github.com/katanemo/archgw) | Apache 2.0 | OSS free; free hosted tier (dev); production: self-hosted or contact Katanemo | OpenAI, Anthropic, Azure, DigitalOcean, Vercel AI Gateway, OpenRouter, Kimi Code, Astraflow | Rust 70%; 6.6 k stars; v0.4.25; 4B-param orchestrator model for intent-based routing; zero-code OTel tracing with Agentic Signals; built on Envoy |
| [Apache APISIX AI Gateway](https://apisix.apache.org/ai-gateway/) | Apache 2.0 | Free open source (self-hosted) | OpenAI, Anthropic, DeepSeek, Mistral, Gemini (5+ named providers) | Lua (81.5%); 16.7 k stars; v3.16.0 (2026-04-08); traditional API gateway + AI layer; multi-LLM load balancing with dynamic weights, token-level rate limiting, RAG integration |
| [AISIX](https://api7.ai/ai-gateway) | Apache 2.0 | OSS free; managed cloud free to start (no credit card) | 100+ providers incl. OpenAI, Anthropic, Gemini, DeepSeek, Bedrock, Azure, Vertex, Mistral, Groq, Cohere, Qwen | Rust; 57 stars; v0.1.0 (2026-03-30); from Apache APISIX team; sub-ms overhead; weighted load balancing, token-level rate limiting (RPM/RPD/TPM/TPD) with Redis sync, PII redaction, OTel/ClickHouse observability |
| [LLM Gateway (llmgateway.io)](https://llmgateway.io/) | AGPLv3 (core); enterprise dir: commercial | Freemium hosted (BYOK free); enterprise custom | 400+ models across 40+ providers (OpenAI, Anthropic, Google, Groq, Mistral) | TypeScript (95.1%); 1.3 k stars; v1.3.0 (2025-12-18); real-time cost/latency analytics, LLM guardrails (prompt-injection, PII), model cost calculator |
| [Lightport](https://github.com/glama-ai/lightport) | MIT | Free / self-hosted via `pnpx lightport` | 77 providers (OpenAI, Anthropic, Azure, Gemini, Vertex, Bedrock, Cohere, Mistral, Groq, DeepSeek, Ollama) | TypeScript; 11 stars; v2.3.0 (2026-05-26); deliberately minimal — no retries, caching, or rate limiting; pure OpenAI-compat translation layer for 77 providers |
| [RouteLLM](https://github.com/lm-sys/RouteLLM) | Apache 2.0 | Free OSS; users supply own API keys | Any LiteLLM-supported endpoint (OpenAI, Anthropic, Gemini, Bedrock, Together AI, Ollama) | Python; ~5 k stars; 0.2.0 (2024-07-08 PyPI); academic project from lm-sys team; pre-trained routers (matrix factorization, BERT, causal LLM) route per-query to strong vs. weak model; claims 85% cost reduction; uses LiteLLM as multi-provider backend |
| [Kong AI Gateway](https://konghq.com/products/kong-ai-gateway) | Apache 2.0 (OSS core); enterprise: commercial | OSS free; enterprise: contact sales | OpenAI, Anthropic, Azure AI, GCP Gemini, Bedrock, Databricks, Mistral, HuggingFace (8+ named) | Lua (89.2%); 43.6 k stars (github.com/Kong/kong); v3.9.2 (2026-06-04); AI features embedded in Kong Gateway; semantic caching/routing, PII sanitization, MCP traffic governance, A2A observability |
| [RelayPlane](https://relayplane.com/) | MIT (core npm) | Free trial 7 days; Starter / Pro / Max tiers (price not public) | 11 providers: Anthropic, OpenAI, Gemini, xAI, OpenRouter, DeepSeek, Groq, Mistral, Together, Fireworks, Perplexity | TypeScript (92.3%); 180 stars; v1.9.39 (2026-06-16 npm); local Node.js proxy, no Docker; multi-credential round-robin, quota-aware failover, cheap-model offload (`rp:best`/`rp:cheap` via OpenRouter); explicit CC settings.json hook support |

---

## Hosted Aggregators

| Tool | License | Pricing | Models / Providers | Differentiator |
|---|---|---|---|---|
| [OpenRouter](https://openrouter.ai/) | Proprietary platform; SDKs Apache-2.0/MIT | Pay-as-you-go credits; 20+ free models; no subscription | 400+ models from 60+ providers (Anthropic, OpenAI, Google, Meta, Amazon, and more) | 100T tokens/month; automatic provider failover; OpenAI-SDK-compatible; MCP server at openrouter.ai/docs/_mcp/server; CC integration via `ANTHROPIC_BASE_URL`; also appears in CC-routing doc |
| [Requesty](https://requesty.ai/) | Proprietary (SDKs: MIT/Apache-2.0) | Free (200 req/day free models); PAYG 5% markup; $10 free credits on signup; Enterprise custom | 400+ models across 30+ providers (Anthropic, OpenAI, Google, Mistral) | Hosted SaaS; automatic failover, prompt caching (up to 90% token cost reduction claimed), per-request cost/latency dashboards, RBAC; CC integration via `ANTHROPIC_BASE_URL=https://router.requesty.ai`; EU residency endpoint |
| [Martian](https://docs.withmartian.com/) | Proprietary (research tools ARES/K-Steering: MIT) | Free (2,500 req); usage-based ($20/5 k req); enterprise SLA/VPC | 200+ models (OpenAI, Anthropic, Google) | Hosted SaaS; per-request ML routing for cost-quality trade-off; Airlock compliance layer; CC integration via `ANTHROPIC_BASE_URL=https://api.withmartian.com/v1`; ~$1.3B valuation (Apr 2026) |
| [Vercel AI Gateway](https://vercel.com/docs/ai-gateway) | Proprietary hosted | No token markup (pass-through); BYOK option; Vercel AI Gateway Credits | 200+ models (Anthropic, OpenAI, xAI, Google, DeepSeek, Alibaba, NVIDIA, and more) | Hosted SaaS; single API key for all providers; zero markup; automatic fallbacks/retries, load balancing, spend monitoring, web search capability; CC integration via `ANTHROPIC_BASE_URL=https://ai-gateway.vercel.sh` |
| [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) | Proprietary hosted | Available on all Cloudflare plans; unified billing option | 24 providers: Bedrock, Anthropic, Azure OpenAI, Cerebras, Cohere, DeepSeek, Google AI Studio, Vertex, Groq, Mistral, OpenAI, OpenRouter, Perplexity, Workers AI, and others | Hosted SaaS; adds observability, semantic/response caching, rate limiting, sequential model fallback (Universal endpoint); changelog updated 2026-06-12; no CC-specific integration documented |
| [Portkey](https://portkey.ai/) | MIT (OSS); managed: proprietary | Managed from $49/month (see OSS row above for self-hosted) | (same as OSS row) | Also offered as managed SaaS with dedicated Claude Code Gateway product (portkey.ai/for/claude-code); Palo Alto Networks acquisition mentioned on homepage (unverified via press release) |
| [Z.AI](https://docs.z.ai/scenario-example/develop-tools/claude) | MIT (SDK + GLM model weights); platform: not disclosed | Pay-per-token: GLM-5.1 $1.00–$1.40/M input, $3.20–$4.40/M output; free tiers for GLM-4.7-Flash and GLM-4.5-Flash; Coding Plans: Lite $30/quarter, Pro $90/quarter, Max $240/quarter | GLM model family: 15+ models across text, vision, image, video, audio (GLM-5.1, GLM-5, GLM-4.7, GLM-4.5, CogView-4, CogVideoX-3, GLM-ASR-2512) | Zhipu AI's international platform; Anthropic-compatible endpoint at `api.z.ai/api/anthropic`; CC model slots map Opus/Sonnet/Haiku → GLM-4.7/GLM-4.7/GLM-4.5-Air; sponsors musistudio/claude-code-router (35 k stars) |
| [Eden AI](https://www.edenai.co/) | Proprietary SaaS; peripheral repos: MIT | 5.5% fee on provider cost (self-serve); Advanced: custom/volume | 500+ models from 50+ providers: LLM, OCR, vision, audio, translation, moderation | Hosted SaaS; unified billing across all providers; EU-region endpoint; edenai-skill (MIT, github.com/edenai/edenai-skill) integrates as a CC tool-belt skill giving CC access to 500+ models |
| [Mammouth](https://mammouth.ai/) | Proprietary (closed SaaS) | Starter €12/month; Standard €24/month; Expert €72/month (incl. $2–$10 API credits); PAYG also available | 20+ models: Claude, GPT, Gemini, Mistral, Llama, Grok, DeepSeek, Kimi, Perplexity; image/video generators | OpenAI-compatible API at `api.mammouth.ai/v1/chat/completions`; subscription model aimed at end-users wanting a single plan for multiple frontier LLMs; no CC-specific integration |
| [TrueFoundry AI Gateway](https://www.truefoundry.com/ai-gateway) | Proprietary (SaaS) | Free Developer (50 k req/month, 3 users); Pro $499/month; Pro Plus $2,999/month; Enterprise custom | 1,600+ models: OpenAI, Anthropic Claude, Google Gemini, Groq, Mistral, 250+ additional LLMs, self-hosted open models | sub-3ms internal latency; latency-based/weighted load balancing, model fallback, RBAC, token budgeting; claims 30% cost reduction; no CC or MCP integration mentioned |
| [AIMLAPI](https://aimlapi.com/) | Proprietary (no OSS repo found) | Pay-as-you-go per token/image/video-second/audio-minute; ≥1 free model (NVIDIA Nemotron 3 Nano Omni) | 500+ models from 15+ providers: OpenAI, Anthropic, Google, xAI, Alibaba, NVIDIA, DeepSeek, Meta, ByteDance | OpenAI-compatible REST API; covers chat, image, video, audio, embeddings; no automatic routing/fallback — users select models explicitly; no CC integration found |
| [ZenMux](https://zenmux.ai/) | Proprietary (closed SaaS, Cloudflare infra) | Credit-based top-up (PAYG); free tier on Product Hunt launch | 200+ models across 12+ providers: OpenAI, Anthropic, Google, DeepSeek, xAI, Meta, Moonshot, Minimax, Qwen, Baidu, Volcengine, Kuaishou | "LLM Insurance" — passive/active compensation for latency or quality failures; smart routing; exposes OpenAI-, Anthropic-, and Vertex AI-compatible endpoints; explicitly markets against OpenRouter |
| [ClawRouters](https://www.clawrouters.com/) | Not disclosed (no confirmed OSS repo) | Freemium: Free BYOK ($0); Starter $29/month (10M tokens); Pro $99/month (20M tokens + 500 k Opus) | 50+ models: OpenAI, Anthropic, Google, DeepSeek, Kimi, Qwen, GLM | ~10 ms routing latency; OpenAI-compatible drop-in; auto-failover; SOC 2; 99.9% uptime SLA; BYOK free tier; no CC-specific integration |
| [ShareAI](https://shareai.now/) | Proprietary (no OSS repo found) | Pay-per-token; 70% of revenue to GPU providers; no confirmed free tier | 150+ open-source models (Llama4 Maverick, Llama4 Scout, GPT OSS 120B) via decentralized global GPU provider grid | Decentralized inference network; BYOI (bring your own hardware) with elastic network spillover; covers OCR, STT, translation, image generation, document parsing; no CC integration |
| [Inworld Router](https://inworld.ai/router) | Proprietary (closed SaaS) | Free during Research Preview; zero markup on provider rates; first-party open models up to 50% below third-party rates | 116 models listed on models page (marketing: 220+); OpenAI, Anthropic, Google, xAI, Mistral, DeepSeek, Meta, Alibaba, MiniMax, Kimi, NVIDIA, Nous Research | CEL-expression conditional routing on user metadata; A/B testing; automatic multi-provider failover; TTS in single API call; voice pipeline routing on acoustic signals; <5 ms overhead; Anthropic SDK drop-in via `base_url=https://api.inworld.ai/v1` |
| [Not Diamond](https://www.notdiamond.ai/) | Apache-2.0 (Python SDK); hosted platform: proprietary | Free early-access (apply); Enterprise: contact sales; small fixed fee per million tokens | 13 providers: OpenAI, Anthropic, Google, Mistral, xAI, Replicate, TogetherAI, Perplexity, Cohere, Minimax, DeepSeek, Qwen, Inception | Per-request ML model prediction (not static rules); privacy-preserving routing; SOC-2 + ISO 27001; custom router training from usage data; OpenRouter integration via `/models` API filter; Python SDK v1.7.0 (2026-05-22) |
| [Zuplo AI Gateway](https://zuplo.com/ai-gateway) | Proprietary (hosted SaaS) | Free (1,000 req/month, ≤3 users); Enterprise from $1,000/month annual | Anthropic, OpenAI, Google Gemini, Mistral (4 confirmed providers) | Explicit CC integration docs at zuplo.com/docs/ai-gateway/integrations/claude-code; semantic caching, prompt-injection protection, PII/secret masking, hierarchical dollar budgets per team/org/app; Galileo/Comet Opik observability |

---

## Model-Fusion / Ensemble Routing

| Tool | License | Pricing | Models / Providers | Differentiator |
|---|---|---|---|---|
| [OpenRouter Fusion](https://openrouter.ai/blog/announcements/fusion-beats-frontier/) | Proprietary (OpenRouter hosted feature) | Sum of all panel model completions; Quality (default) and Budget presets; custom panels supported | Any models on OpenRouter; benchmark panels include Claude Opus 4.8, Fable 5, GPT-5.5, Gemini 3 Flash, Gemini 3.1 Pro, Kimi K2.6, DeepSeek V4 Pro | Dispatches prompt to parallel panel of models + judge synthesizer; single synthesized response; benchmark on DRACO deep-research tasks shows fused panels outperform single frontier models; accessed via `openrouter/fusion` slug or `{"plugins":[{"id":"fusion"}]}` |

---

## When to Use What

**Need maximum model breadth with a single API key?** OpenRouter (400+ models, CC-native via `ANTHROPIC_BASE_URL`) or LiteLLM (100+ providers, self-hosted, MIT). **Need Claude Code integration out of the box?** Requesty, Martian, Portkey, Vercel AI Gateway, Zuplo, and RelayPlane all document explicit CC `ANTHROPIC_BASE_URL` patterns. **Prioritizing performance and low overhead?** Bifrost (Go, Apache 2.0, claims 50× faster P99 than LiteLLM), AISIX (Rust, sub-ms overhead), or Arch Gateway (Rust/Envoy, intent-based routing). **Need observability and cost attribution?** Helicone (Apache 2.0, OSS, strong tracing), Kong AI Gateway (43.6 k stars, MCP + A2A governance), or ClawRouters / Requesty for per-developer spend dashboards. **Running fully local / air-gapped?** LiteLLM, Apache APISIX, RouteLLM, Lightport, or RelayPlane (no Docker required). **Want ensemble/fusion quality beyond any single model?** OpenRouter Fusion dispatches to a judge-synthesized panel at the cost of all constituent completions.

---

## Sources

Facts compiled from each tool's first-party page (1p-verified 2026-06-16). No third-party claims were introduced; omissions reflect data not present in first-party content at access date.

| Source | Content |
|---|---|
| [openrouter.ai](https://openrouter.ai/) | OpenRouter platform, model/provider counts |
| [openrouter.ai/blog/announcements/fusion-beats-frontier/](https://openrouter.ai/blog/announcements/fusion-beats-frontier/) | OpenRouter Fusion benchmark and billing model |
| [github.com/BerriAI/litellm](https://github.com/BerriAI/litellm) | LiteLLM release, license, star count |
| [portkey.ai/for/claude-code](https://portkey.ai/for/claude-code) | Portkey Claude Code Gateway product |
| [docs.requesty.ai/integrations/claude-code](https://docs.requesty.ai/integrations/claude-code) | Requesty CC integration |
| [docs.withmartian.com/integrations/claude-code](https://docs.withmartian.com/integrations/claude-code) | Martian CC integration, pricing |
| [vercel.com/docs/ai-gateway](https://vercel.com/docs/ai-gateway) | Vercel AI Gateway docs |
| [developers.cloudflare.com/ai-gateway/](https://developers.cloudflare.com/ai-gateway/) | Cloudflare AI Gateway docs |
| [helicone.ai](https://www.helicone.ai/) | Helicone pricing, GitHub stats |
| [notdiamond.ai](https://www.notdiamond.ai/) | Not Diamond routing, pricing |
| [docs.z.ai/scenario-example/develop-tools/claude](https://docs.z.ai/scenario-example/develop-tools/claude) | Z.AI CC integration, model/pricing |
| [edenai.co](https://www.edenai.co/) | Eden AI pricing, model breadth |
| [mammouth.ai](https://mammouth.ai/) | Mammouth subscription plans |
| [konghq.com/products/kong-ai-gateway](https://konghq.com/products/kong-ai-gateway) | Kong AI Gateway features |
| [truefoundry.com/ai-gateway](https://www.truefoundry.com/ai-gateway) | TrueFoundry pricing, features |
| [github.com/katanemo/archgw](https://github.com/katanemo/archgw) | Arch Gateway license, stars, features |
| [aimlapi.com](https://aimlapi.com/) | AIMLAPI model breadth, pricing |
| [getmaxim.ai/bifrost/](https://www.getmaxim.ai/bifrost/) | Bifrost (catB) features |
| [apisix.apache.org/ai-gateway/](https://apisix.apache.org/ai-gateway/) | Apache APISIX AI Gateway |
| [api7.ai/ai-gateway](https://api7.ai/ai-gateway) | AISIX features, release |
| [llmgateway.io](https://llmgateway.io/) | LLM Gateway features, release |
| [relayplane.com](https://relayplane.com/) | RelayPlane CC integration, pricing |
| [zenmux.ai](https://zenmux.ai/) | ZenMux LLM Insurance, model count |
| [clawrouters.com](https://www.clawrouters.com/) | ClawRouters pricing, SOC 2 |
| [shareai.now](https://shareai.now/) | ShareAI decentralized network |
| [inworld.ai/router](https://inworld.ai/router) | Inworld Router CEL routing |
| [zuplo.com/ai-gateway](https://zuplo.com/ai-gateway) | Zuplo pricing, CC integration docs |
| [github.com/glama-ai/lightport](https://github.com/glama-ai/lightport) | Lightport license, providers |
| [github.com/lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM) | RouteLLM paper/OSS router |

Cross-ref: [CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md) — OpenRouter and LiteLLM appear there as Claude Code integration targets, and the five hosted CC-integrated gateways here (Portkey, Martian, Vercel AI Gateway, Zuplo, RelayPlane) are back-ported there with their Claude Code `ANTHROPIC_BASE_URL` config. This landscape stays the authoritative catalog (license/pricing/breadth); the CC doc holds only the CC-specific setup.
