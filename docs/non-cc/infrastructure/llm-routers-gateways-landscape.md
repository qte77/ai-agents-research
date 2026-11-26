---
title: LLM Routers & Gateways Landscape
source: https://openrouter.ai/
purpose: Provider-agnostic model routers, hosted aggregators, self-hostable gateways, and model-fusion/ensemble routing tools — a reference catalog verified 2026-06-16.
created: 2026-06-16
updated: 2026-11-26
validated_links_on: 2026-11-18
status: reference
---

**Details:** informational catalog

## What It Is

A survey of provider-agnostic LLM routers, API gateways, and model aggregators — tools that sit between an AI client and one or more inference backends to add routing, failover, cost control, and observability. Unlike Claude Code-specific proxies (see [CC-model-provider-configuration.md](../../cc-native/configuration/CC-model-provider-configuration.md)), the tools here are general-purpose: they serve any SDK, agent framework, or coding-agent harness that speaks OpenAI-compatible or Anthropic-compatible APIs. Several entries — OpenRouter and LiteLLM in particular — also appear in the CC-routing doc as Claude Code integration targets; those cross-references are noted inline. Entries are organized into three groups: open/self-hostable gateways, hosted aggregators, and model-fusion/ensemble routing.

---

## Open / Self-Hostable Gateways

| Tool | License | Pricing | Models / Providers | Differentiator |
|---|---|---|---|---|
| [LiteLLM](https://github.com/BerriAI/litellm) | MIT (enterprise dir: separate) | Free self-hosted; enterprise custom | 100+ providers incl. OpenAI, Anthropic, Gemini, Azure, Bedrock, Vertex, Cohere, vLLM, HuggingFace | Python SDK + proxy server; 63.9 k stars; v1.111.0 (2026-11-25) (checked 2026-11-26); cost tracking, load balancing, guardrails, Model Context Protocol (MCP) gateway support; [Customer Portal][litellm-portal] (announced 2026-11-13, not yet confirmed in a release): spend tracking and budgets per customer org, team and member, a budget webhook, usage APIs to show costs in your own product; OSS caps each level at 5, per-model key budgets need Enterprise; [agent evaluations][litellm-agent-eval] (blog 2026-11-16, preview): `litellm.agent_eval()` runs your own typed tasks against harness-and-model targets (tool loop, Claude Code, Codex) in fresh workspaces and reports pass rate, cost and duration; the page says published PyPI releases do not include it yet (on `main`, release version not stated), so it is not shipped as of 2026-11-18; also appears in CC-routing doc; [Lens][litellm-lens] (early access; repo [BerriAI/lens][lens-repo], MIT, with no `enterprise/` directory in the repo; 63 stars for the Lens repo; v0.4.0 on 2026-11-23): a self-hosted trace and investigation service (one container plus ClickHouse) that Claude Code and Codex plugins can send session traces to, and a [Lens CLI][litellm-lens-cli] in private preview (no public install yet) whose `lens run` runs one task set across harness × model configurations (Claude Code, Codex, OpenCode, Pi, Deep Agents and others) and reports pass rate, estimated cost, cost per pass and P50 latency. The launch post's run uses 24 synthetic legal-QA sample tasks: a demo, not a benchmark |
| [Portkey](https://portkey.ai/) | MIT (OSS gateway); managed: proprietary | Free self-hosted / managed from $49/month | 1,600+ LLMs across 200+ providers | TypeScript gateway (13.4 k stars, Portkey-AI/gateway, checked 2026-11-26); dedicated Claude Code Gateway product page; Anthropic/Bedrock/Vertex backends; RBAC, guardrails, semantic caching |
| [Bifrost](https://www.getmaxim.ai/bifrost/) | Apache 2.0 | Free self-hosted; enterprise hosted (no public price) | 23+ providers, 1,000+ models (OpenAI, Anthropic, Bedrock, Vertex, Azure, Cerebras, Mistral, Groq, Ollama) | Go implementation; claims 50× lower P99 latency vs LiteLLM; 10.0 k stars (checked 2026-11-26); core release version unverified (the repo's latest GitHub release tag is a Helm chart); adaptive load balancer, provider fallback, semantic caching, MCP gateway |
| [Helicone AI Gateway](https://www.helicone.ai/) | Apache-2.0 | Hobby free (10 k req/month); Pro $79/month; Team $799/month; Enterprise on-prem | 100+ models incl. OpenAI, Anthropic, Azure, Gemini, DeepSeek, Groq, OpenRouter | TypeScript (91.2%); 6.3 k stars (checked 2026-11-26); v2025.08.21-1; observability-first — request logging, cost tracking, agent tracing, prompt management; SOC-2/HIPAA on Team+ |
| [Arch Gateway (archgw)](https://github.com/katanemo/archgw) | Apache 2.0 | OSS free; free hosted tier (dev); production: self-hosted or contact Katanemo | OpenAI, Anthropic, Azure, DigitalOcean, Vercel AI Gateway, OpenRouter, Kimi Code, Astraflow | Rust 70%; 7.1 k stars (repo now `katanemo/plano`); v0.4.39 (2026-10-24); 4B-param orchestrator model for intent-based routing; zero-code OTel tracing with Agentic Signals; built on Envoy |
| [Apache APISIX AI Gateway](https://apisix.apache.org/ai-gateway/) | Apache 2.0 | Free open source (self-hosted) | OpenAI, Anthropic, DeepSeek, Mistral, Gemini (5+ named providers) | Lua (81.5%); 17.4 k stars; v3.21.0 (2026-11-19) (checked 2026-11-26); traditional API gateway + AI layer; multi-LLM load balancing with dynamic weights, token-level rate limiting, Retrieval-Augmented Generation (RAG) integration |
| [AISIX](https://api7.ai/ai-gateway) | Apache 2.0 | OSS free; managed cloud free to start (no credit card) | 100+ providers incl. OpenAI, Anthropic, Gemini, DeepSeek, Bedrock, Azure, Vertex, Mistral, Groq, Cohere, Qwen | Rust; 236 stars; v1.12.0 (2026-11-26) (checked 2026-11-26); from Apache APISIX team; sub-ms overhead; weighted load balancing, token-level rate limiting (RPM/RPD/TPM/TPD) with Redis sync, PII redaction, OTel/ClickHouse observability |
| [LLM Gateway (llmgateway.io)](https://llmgateway.io/) | AGPLv3 (core); enterprise dir: commercial | Freemium hosted (BYOK free); enterprise custom | 400+ models across 40+ providers (OpenAI, Anthropic, Google, Groq, Mistral) | TypeScript (95.1%); 1.76 k stars; v1.27.0 (2026-11-23) (checked 2026-11-26); real-time cost/latency analytics, LLM guardrails (prompt-injection, PII), model cost calculator |
| [RouteLLM](https://github.com/lm-sys/RouteLLM) | Apache 2.0 | Free OSS; users supply own API keys | Any LiteLLM-supported endpoint (OpenAI, Anthropic, Gemini, Bedrock, Together AI, Ollama) | Stale but widely adopted academic router from the lm-sys team (5.7 k stars); last push 2024-08-10, PyPI 0.2.0 2024-07-08 (`gh api` 2026-11-22) |
| [Kong AI Gateway](https://konghq.com/products/kong-ai-gateway) | Apache 2.0 (OSS core); enterprise: commercial | OSS free; enterprise: contact sales | OpenAI, Anthropic, Azure AI, GCP Gemini, Bedrock, Databricks, Mistral, HuggingFace (8+ named) | Lua (89.2%); 44.4 k stars (github.com/Kong/kong); v3.9.5 (2026-11-19) (checked 2026-11-26); AI features embedded in Kong Gateway; semantic caching/routing, PII sanitization, MCP traffic governance, Agent-to-Agent Protocol (A2A) observability |

---

## Hosted Aggregators

| Tool | License | Pricing | Models / Providers | Differentiator |
|---|---|---|---|---|
| [OpenRouter](https://openrouter.ai/) | Proprietary platform; SDKs Apache-2.0/MIT | Pay-as-you-go credits; `:free` model variants (the earlier "20+ free models" count is unverified); no subscription | hundreds of models from many providers (Anthropic, OpenAI, Google, Meta, Amazon, and more); the earlier "400+ models from 60+ providers" count is unverified | a State of AI study over 100 trillion tokens (period not stated; the earlier "/month" is unverified); automatic provider failover; OpenAI-SDK-compatible; MCP server at openrouter.ai/docs/_mcp/server; CC integration via `ANTHROPIC_BASE_URL`; also appears in CC-routing doc |
| [Requesty](https://requesty.ai/) | Proprietary (SDKs: MIT/Apache-2.0) | Free (200 req/day free models); PAYG 5% markup; $10 free credits on signup; Enterprise custom | 400+ models across 30+ providers (Anthropic, OpenAI, Google, Mistral) | Hosted SaaS; automatic failover, prompt caching (up to 90% token cost reduction claimed), per-request cost/latency dashboards, RBAC; CC integration via `ANTHROPIC_BASE_URL=https://router.requesty.ai`; EU residency endpoint |
| [Martian](https://docs.withmartian.com/) | Proprietary (research tools ARES/K-Steering: MIT) | Free (2,500 req); usage-based ($20/5 k req); enterprise SLA/VPC | 200+ models (OpenAI, Anthropic, Google) | Hosted SaaS; per-request ML routing for cost-quality trade-off; Airlock compliance layer; CC integration via `ANTHROPIC_BASE_URL=https://api.withmartian.com/v1`; ~$1.3B valuation (Apr 2026) |
| [Vercel AI Gateway](https://vercel.com/docs/ai-gateway) | Proprietary hosted | No token markup (pass-through); BYOK option; Vercel AI Gateway Credits | 200+ models (Anthropic, OpenAI, xAI, Google, DeepSeek, Alibaba, NVIDIA, and more) | Hosted SaaS; single API key for all providers; zero markup; automatic fallbacks/retries, load balancing, spend monitoring, web search capability; CC integration via `ANTHROPIC_BASE_URL=https://ai-gateway.vercel.sh` |
| [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) | Proprietary hosted | Available on all Cloudflare plans; unified billing option | 24 providers: Bedrock, Anthropic, Azure OpenAI, Cerebras, Cohere, DeepSeek, Google AI Studio, Vertex, Groq, Mistral, OpenAI, OpenRouter, Perplexity, Workers AI, and others | Hosted SaaS; adds observability, semantic/response caching, rate limiting, sequential model fallback (Universal endpoint); changelog updated 2026-06-12; no CC-specific integration documented |
| [Portkey](https://portkey.ai/) | MIT (OSS); managed: proprietary | Managed from $49/month (see OSS row above for self-hosted) | (same as OSS row) | Also offered as managed SaaS with dedicated Claude Code Gateway product (portkey.ai/for/claude-code); Palo Alto Networks acquisition mentioned on homepage (unverified via press release) |
| [Z.AI](https://docs.z.ai/scenario-example/develop-tools/claude) | MIT (SDK + GLM model weights); platform: not disclosed | Pay-per-token: GLM-5.1 $1.00–$1.40/M input, $3.20–$4.40/M output; free tiers for GLM-4.7-Flash and GLM-4.5-Flash; Coding Plans: Lite $30/quarter, Pro $90/quarter, Max $240/quarter | GLM model family: 15+ models across text, vision, image, video, audio (GLM-5.1, GLM-5, GLM-4.7, GLM-4.5, CogView-4, CogVideoX-3, GLM-ASR-2512) | Zhipu AI's international platform; Anthropic-compatible endpoint at `api.z.ai/api/anthropic`; CC model slots: the [devpack page](https://docs.z.ai/devpack/tool/claude) defaults Opus/Sonnet/Haiku to GLM-5.3-Flash (its manual example uses glm-5.4 for Opus/Sonnet and glm-5.3-flash for Haiku); sponsors musistudio/claude-code-router (38.4 k stars, checked 2026-11-26) |
| [Eden AI](https://www.edenai.co/) | Proprietary SaaS; peripheral repos: MIT | 5.5% fee on provider cost (self-serve); Advanced: custom/volume | 500+ models from 50+ providers: LLM, OCR, vision, audio, translation, moderation | Hosted SaaS; unified billing across all providers; EU-region endpoint; edenai-skill (MIT, github.com/edenai/edenai-skill) integrates as a CC tool-belt skill giving CC access to 500+ models |
| [Mammouth](https://mammouth.ai/) | Proprietary (closed SaaS) | Starter €12/month; Standard €24/month; Expert €72/month (incl. $2–$10 API credits); PAYG also available | 20+ models: Claude, GPT, Gemini, Mistral, Llama, Grok, DeepSeek, Kimi, Perplexity; image/video generators | OpenAI-compatible API at `api.mammouth.ai/v1/chat/completions`; subscription model aimed at end-users wanting a single plan for multiple frontier LLMs; no CC-specific integration |
| [TrueFoundry AI Gateway](https://www.truefoundry.com/ai-gateway) | Proprietary (SaaS) | Free Developer (50 k req/month, 3 users); Pro $499/month; Pro Plus $2,999/month; Enterprise custom | 1,600+ models: OpenAI, Anthropic Claude, Google Gemini, Groq, Mistral, 250+ additional LLMs, self-hosted open models | sub-3ms internal latency; latency-based/weighted load balancing, model fallback, RBAC, token budgeting; claims 30% cost reduction; no CC or MCP integration mentioned |
| [AIMLAPI](https://aimlapi.com/) | Proprietary (no OSS repo found) | Pay-as-you-go per token/image/video-second/audio-minute; ≥1 free model (NVIDIA Nemotron 3 Nano Omni) | 500+ models from 15+ providers: OpenAI, Anthropic, Google, xAI, Alibaba, NVIDIA, DeepSeek, Meta, ByteDance | OpenAI-compatible REST API; covers chat, image, video, audio, embeddings; no automatic routing/fallback — users select models explicitly; no CC integration found |
| [ZenMux](https://zenmux.ai/) | Proprietary (closed SaaS, Cloudflare infra) | Credit-based top-up (PAYG); free tier on Product Hunt launch | 200+ models across 12+ providers: OpenAI, Anthropic, Google, DeepSeek, xAI, Meta, Moonshot, Minimax, Qwen, Baidu, Volcengine, Kuaishou | "LLM Insurance" — passive/active compensation for latency or quality failures; smart routing; exposes OpenAI-, Anthropic-, and Vertex AI-compatible endpoints; explicitly markets against OpenRouter |
| [Inworld Router](https://inworld.ai/router) | Proprietary (closed SaaS) | Free during Research Preview; zero markup on provider rates; first-party open models up to 50% below third-party rates | 116 models listed on models page (marketing: 220+); OpenAI, Anthropic, Google, xAI, Mistral, DeepSeek, Meta, Alibaba, MiniMax, Kimi, NVIDIA, Nous Research | CEL-expression conditional routing on user metadata; A/B testing; automatic multi-provider failover; TTS in single API call; voice pipeline routing on acoustic signals; <5 ms overhead; Anthropic SDK drop-in via `base_url=https://api.inworld.ai/v1` |
| [Not Diamond](https://www.notdiamond.ai/) | Apache-2.0 (Python SDK); hosted platform: proprietary | Free early-access (apply); Enterprise: contact sales; small fixed fee per million tokens | 13 providers: OpenAI, Anthropic, Google, Mistral, xAI, Replicate, TogetherAI, Perplexity, Cohere, Minimax, DeepSeek, Qwen, Inception | Per-request ML model prediction (not static rules); privacy-preserving routing; SOC-2 + ISO 27001; custom router training from usage data; OpenRouter integration via `/models` API filter; Python SDK v1.7.0 (2026-05-22) |
| [Zuplo AI Gateway](https://zuplo.com/ai-gateway) | Proprietary (hosted SaaS) | Free (1,000 req/month, ≤3 users); Enterprise from $1,000/month annual | Anthropic, OpenAI, Google Gemini, Mistral (4 confirmed providers) | Explicit CC integration docs at zuplo.com/docs/ai-gateway/integrations/claude-code; semantic caching, prompt-injection protection, PII/secret masking, hierarchical dollar budgets per team/org/app; Galileo/Comet Opik observability |

---

## Model-Fusion / Ensemble Routing

| Tool | License | Pricing | Models / Providers | Differentiator |
|---|---|---|---|---|
| [OpenRouter Fusion](https://openrouter.ai/blog/announcements/fusion-beats-frontier/) | Proprietary (OpenRouter hosted feature) | Billing not stated on the cited blog (earlier "sum of all panel completions" unverified); presets not defined there; custom panels supported | Any models on OpenRouter; benchmark panels include Claude Opus 4.8, Fable 5, GPT-5.5, Gemini 3 Flash, Gemini 3.1 Pro, Kimi K2.6, DeepSeek V4 Pro | Dispatches prompt to parallel panel of models + judge synthesizer; single synthesized response; benchmark on DRACO deep-research tasks shows fused panels outperform single frontier models; accessed via `openrouter/fusion` slug or `{"plugins":[{"id":"fusion"}]}` |

---

## When to Use What

**Need maximum model breadth with a single API key?** OpenRouter (400+ models, CC-native via `ANTHROPIC_BASE_URL`) or LiteLLM (100+ providers, self-hosted, MIT). **Need Claude Code integration out of the box?** Requesty, Martian, Portkey, Vercel AI Gateway, and Zuplo all document explicit CC `ANTHROPIC_BASE_URL` patterns. **Prioritizing performance and low overhead?** Bifrost (Go, Apache 2.0, claims 50× faster P99 than LiteLLM), AISIX (Rust, sub-ms overhead), or Arch Gateway (Rust/Envoy, intent-based routing). **Need observability and cost attribution?** Helicone (Apache 2.0, OSS, strong tracing), Kong AI Gateway (44.4 k stars, MCP + A2A governance), or Requesty for per-developer spend dashboards. **Running fully local / air-gapped?** LiteLLM, Apache APISIX, or RouteLLM. **Want ensemble/fusion quality beyond any single model?** OpenRouter Fusion dispatches to a judge-synthesized panel at the cost of all constituent completions. **Which coding harness accepts a custom base URL?** See [Model access and billing](../coding-agents/coding-agents-comparison-landscape.md#model-access-and-billing), which compares 15 harnesses from their own docs.

---

## Not included

Entries removed under the [pruning rule](../../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (checked 2026-11-22).

| Name | Reason | Date | Link |
|---|---|---|---|
| Lightport | Criterion 3: 25 stars, no GitHub releases; the only named user is its own maker Glama (README) (`gh api` 2026-11-22) | 2026-11-22 | <https://github.com/glama-ai/lightport> |
| RelayPlane | Criterion 3: 211 stars (`RelayPlane/proxy`); names no customers; its savings figures are notional list-price examples, not measured results (product page, 2026-11-22) | 2026-11-22 | <https://relayplane.com/> |
| ClawRouters | Criterion 3: no repo, no named customers; "5,000+ integrations", 70-90% savings and SOC 2 claims are unsourced on its own page (2026-11-22) | 2026-11-22 | <https://www.clawrouters.com/> |
| ShareAI | Criterion 3: no repo; its only adoption evidence is an unattributed "Companies using ShareAI" logo list of small startups, with no case studies, usage figures or measured benefit (product page, 2026-11-22) | 2026-11-22 | <https://shareai.now/> |
| Pandora's AI Model Routing Box | Criterion 1: paper only, no code link on the arXiv abstract page (v2, 2026-08-21) | 2026-11-22 | <https://arxiv.org/abs/2608.20316> |

## Sources

Facts compiled from each tool's first-party page (1p-verified 2026-06-16). No third-party claims were introduced; omissions reflect data not present in first-party content at access date.

| Source | Content |
|---|---|
| [openrouter.ai](https://openrouter.ai/) | OpenRouter platform, model/provider counts |
| [openrouter.ai/blog/announcements/fusion-beats-frontier/](https://openrouter.ai/blog/announcements/fusion-beats-frontier/) | OpenRouter Fusion benchmark and billing model |
| [github.com/BerriAI/litellm](https://github.com/BerriAI/litellm) | LiteLLM release, license, star count |
| [LiteLLM Agent evaluations blog][litellm-agent-eval] | `litellm.agent_eval` API shape and its preview status (2026-11-16) |
| [LiteLLM Lens docs][litellm-lens] · [Lens CLI docs][litellm-lens-cli] · [Lens CLI blog][litellm-lens-blog] · [BerriAI/lens][lens-repo] | Lens status (early access), data paths, CLI scope (private preview) and metrics; repo licence and release from `gh api` (2026-11-23) |
| [LiteLLM Customer Portal blog][litellm-portal] | Customer Portal announcement (2026-11-13), OSS vs Enterprise limits |
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
| [zenmux.ai](https://zenmux.ai/) | ZenMux LLM Insurance, model count |
| [inworld.ai/router](https://inworld.ai/router) | Inworld Router CEL routing |
| [zuplo.com/ai-gateway](https://zuplo.com/ai-gateway) | Zuplo pricing, CC integration docs |
| [github.com/lm-sys/RouteLLM](https://github.com/lm-sys/RouteLLM) | RouteLLM paper/OSS router |

Cross-ref: [CC-model-provider-configuration.md](../../cc-native/configuration/CC-model-provider-configuration.md) — OpenRouter and LiteLLM appear there as Claude Code integration targets, and the hosted CC-integrated gateways here (Portkey, Martian, Vercel AI Gateway, Zuplo) are back-ported there with their Claude Code `ANTHROPIC_BASE_URL` config. This landscape stays the authoritative catalog (license/pricing/breadth); the CC doc holds only the CC-specific setup.

[litellm-portal]: https://docs.litellm.ai/blog/customer-portal
[litellm-agent-eval]: https://docs.litellm.ai/blog/agent-evaluations
[litellm-lens]: https://docs.litellm.ai/docs/proxy/lens
[litellm-lens-cli]: https://docs.litellm.ai/docs/proxy/lens/cli
[litellm-lens-blog]: https://docs.litellm.ai/blog/lens-cli
[lens-repo]: https://github.com/BerriAI/lens
