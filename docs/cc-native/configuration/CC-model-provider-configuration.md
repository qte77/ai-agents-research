---
title: CC Model & Provider Configuration
source: https://code.claude.com/docs/en/settings#environment-variables, https://openrouter.ai/docs/cookbook/coding-agents/claude-code-integration, https://ollama.com/blog/claude, https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models, https://www.infomaniak.com/en/hosting/ai-services/open-source-models
purpose: Reference for configuring CC with alternative models, endpoints, API keys, third-party providers (OpenRouter, Bedrock, Vertex, Foundry, Infomaniak), local models (Ollama, llama.cpp, LM Studio), and LLM gateway proxies.
created: 2026-03-07
updated: 2026-07-05
validated_links: 2026-07-05
---

**Status**: Reference (actionable configuration guide)

## Model Selection

| Variable | Purpose | Example |
| -------- | ------- | ------- |
| `ANTHROPIC_MODEL` | Primary model override | `claude-sonnet-4-6` |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Override Haiku-class model | Custom model ID |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Override Sonnet-class model | Custom model ID |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Override Opus-class model | Custom model ID |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for subagents/teammates | Custom model ID |
| `CLAUDE_CODE_EFFORT_LEVEL` | Reasoning effort (Fable 5, Opus 4.8/4.7/4.6, Sonnet 4.6) | `low`, `medium`, `high`, `xhigh`, `max` |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` | Disable adaptive reasoning | `1` |

All variables can also be set in `settings.json` under the `env` key. ([source][cc-settings])

### Effort Levels

`CLAUDE_CODE_EFFORT_LEVEL` (above), the `/effort` command, the `--effort` flag, and per-skill/subagent `effort` frontmatter all select an **adaptive-reasoning effort level**. The levels available depend on the model ([source][cc-effort]):

| Level | Models | Notes |
|---|---|---|
| `low` | all effort-capable | Short, scoped, latency-sensitive work |
| `medium` | all effort-capable | Cost-sensitive work trading some intelligence |
| `high` | all effort-capable | Balance — **default** on Fable 5, Opus 4.8, Opus 4.6, Sonnet 4.6 |
| `xhigh` | Fable 5, Opus 4.8, Opus 4.7 | Deeper reasoning, higher spend — **default** on Opus 4.7 |
| `max` | all effort-capable | Deepest reasoning, no token cap; can overthink |

Opus 4.6 and Sonnet 4.6 support `low`/`medium`/`high`/`max` (no `xhigh`). Setting an unsupported level falls back to the highest the model supports (e.g. `xhigh` runs as `high` on Opus 4.6).

**Precedence & persistence** ([source][cc-effort]):

- Precedence: `CLAUDE_CODE_EFFORT_LEVEL` > configured level (`effortLevel` / `/effort`) > model default. Skill/subagent `effort` frontmatter overrides the session level while active (but not the env var).
- `low`/`medium`/`high`/`xhigh` **persist** across sessions; `max` is **session-only** (except via `CLAUDE_CODE_EFFORT_LEVEL`). `effortLevel` in `settings.json` accepts only `low`/`medium`/`high`/`xhigh` — `max` and `ultracode` are not accepted there.
- `/effort auto` (or `CLAUDE_CODE_EFFORT_LEVEL=auto`) resets to the model default.

**Related, but not effort levels**:

- **`ultracode`** — a session setting that sends `xhigh` *and* auto-orchestrates dynamic workflows; not part of `effortLevel`/`--effort`/`CLAUDE_CODE_EFFORT_LEVEL`. See [CC-dynamic-workflows-analysis.md](../agents-skills/CC-dynamic-workflows-analysis.md#ultracode-effort-setting).
- **`ultrathink`** — include it anywhere in a prompt for one-off deeper reasoning on that turn; Claude Code adds an in-context instruction but the **effort level sent to the API is unchanged**. Phrases like "think", "think hard", and "think more" are *not* recognized keywords ([source][cc-ultrathink]).

**Verified 2026-06-11.** Effort availability and defaults are model-generation-specific and shift over time; `xhigh` is gated on the `xhigh_effort` capability (CC v2.1.111+), and `xhigh`-capable models require recent CC builds (Opus 4.8 → v2.1.154+, Fable 5 → v2.1.170+) ([source][cc-effort]).

### Newest Model (Fable 5)

Claude **Fable 5** (`claude-fable-5`) is the newest model, selectable in CC via `/model` or `ANTHROPIC_MODEL=claude-fable-5`. For its model card (context, pricing, tokenizer/refusal caveats, CC plan access) and a free-tier/OSS provider snapshot, see [CC-models-reference.md](CC-models-reference.md).

## API Key & Endpoint

| Variable | Purpose | Example |
| -------- | ------- | ------- |
| `ANTHROPIC_API_KEY` | API key (sent as `X-Api-Key` header) | `sk-ant-...` |
| `ANTHROPIC_AUTH_TOKEN` | Custom `Authorization` header value (auto-prefixed with `Bearer`) | OpenRouter key |
| `ANTHROPIC_BASE_URL` | Override API endpoint | `https://openrouter.ai/api` |
| `ANTHROPIC_CUSTOM_HEADERS` | Extra headers (newline-separated `Name: Value`) | Custom routing headers |

## Provider Configuration

### Anthropic API (default)

No extra config needed. Set `ANTHROPIC_API_KEY` or use `/login`. ([source][cc-settings])

### OpenRouter

Routes requests through OpenRouter for provider failover, budget controls, and usage analytics. OpenRouter implements an "Anthropic Skin" compatible with the Messages API — no local proxy needed. ([source][openrouter])

```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="<openrouter-api-key>"
export ANTHROPIC_API_KEY=""  # must be explicitly empty
```

Or in `.claude/settings.local.json` (project-level, git-ignored):

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
    "ANTHROPIC_AUTH_TOKEN": "<openrouter-api-key>",
    "ANTHROPIC_API_KEY": ""
  }
}
```

**Key caveats** ([source][openrouter]):

- CC compatibility guaranteed only with Anthropic first-party provider on OpenRouter
- Run `/logout` first to clear existing Anthropic credentials
- Standard `.env` files are NOT read by CC — use shell profile or `settings.local.json`
- Prompts not logged unless explicitly enabled in OpenRouter account settings

**Benefits**: Provider failover during Anthropic outages, centralized team budget controls, real-time cost monitoring via Activity Dashboard. ([source][openrouter])

**Fast Mode via OpenRouter** (CC v2.1.96+): CC's built-in `/fast` command sends `speed: "fast"` in the request (up to 2.5× faster output on Opus 4.7, premium pricing). OpenRouter supports this parameter and auto-routes such requests to the Anthropic 1P provider while injecting the required beta header. To enable: ([source][openrouter])

```bash
export CLAUDE_CODE_SKIP_FAST_MODE_ORG_CHECK=1
```

### AWS Bedrock

```bash
export CLAUDE_CODE_USE_BEDROCK=true
# Optional: export AWS_BEARER_TOKEN_BEDROCK="<api-key>"
# For LLM gateways: export CLAUDE_CODE_SKIP_BEDROCK_AUTH=true
```

([source][cc-settings])

### Google Vertex AI

```bash
export CLAUDE_CODE_USE_VERTEX=true
# For LLM gateways: export CLAUDE_CODE_SKIP_VERTEX_AUTH=true
```

([source][cc-settings])

### Microsoft Azure Foundry

```bash
export CLAUDE_CODE_USE_FOUNDRY=true
export ANTHROPIC_FOUNDRY_BASE_URL="https://my-resource.services.ai.azure.com/anthropic"
# Or: export ANTHROPIC_FOUNDRY_RESOURCE="my-resource"
# Optional: export ANTHROPIC_FOUNDRY_API_KEY="<api-key>"
# For LLM gateways: export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=true
```

([source][cc-settings])

### Infomaniak AI (EU-Sovereign, OpenAI-Compatible)

Infomaniak (Swiss host) runs an **OpenAI-compatible** inference API serving open-source models — Llama, Mistral, Qwen, Gemma, plus Infomaniak's own vLLM build of Google's [TranslateGemma-27B][infomaniak-translategemma] — with end-to-end processing in Switzerland and 1M free credits for a one-month trial ([source][infomaniak-ai]). Because it speaks OpenAI Chat Completions rather than the Anthropic Messages API, **using it from CC needs a translation proxy** (LiteLLM or claude-code-proxy — see the LLM Gateway / Proxy section below); OpenAI-native agents such as OpenCode and n8n point at it directly.

```bash
# product_id is per-organization: GET https://api.infomaniak.com/1/ai (Authorization: Bearer $API_TOKEN)
# v2 (current) OpenAI-compatible base URL:
https://api.infomaniak.com/2/ai/${PRODUCT_ID}/openai/v1
```

- **OpenCode** ([source][infomaniak-opencode]): register a provider in `~/.config/opencode/opencode.json` using the `@ai-sdk/openai-compatible` package with `baseURL` set to the v2 endpoint and model ids `qwen3` / `llama3` / `mistral3` / `gemma3n` (e.g. default `infomaniak/qwen3`). The recipe wires `API_TOKEN` (created with the `ai-tools` scope at manager.infomaniak.com) and `PRODUCT_ID` as environment variables.
- **n8n** ([source][infomaniak-n8n]): no native node — use the built-in OpenAI node with a custom base URL (`.../1/ai/{product_id}/openai`) and the API token as the key. The credential test fails but inference works; early threads predated function-calling support.

### Local Models

Claude Code works with any backend that speaks the Anthropic Messages API format. Several local inference engines now support this natively.

#### Ollama (Recommended for Local)

Ollama v0.14+ implements the Anthropic Messages API natively — no proxy needed ([source][ollama-claude]).

```bash
# Pull a model
ollama pull qwen3-coder

# Run Claude Code against Ollama
ANTHROPIC_AUTH_TOKEN=ollama \
ANTHROPIC_BASE_URL=http://localhost:11434 \
ANTHROPIC_API_KEY="" \
claude --model qwen3-coder
```

**Supported features**: Messages, streaming, system prompts, tool calling, extended thinking, vision ([source][ollama-claude]).

**Requirements** ([source][ollama-claude]):

- Ollama v0.14.0+
- Model with at least 32K context window (64K+ recommended for agentic use)
- 32GB+ RAM recommended for usable coding experience (Apple Silicon unified memory or PC RAM)

**Recommended models** (as of March 2026): `qwen3-coder`, `gpt-oss:20b`, `glm-4.7:cloud`, `minimax-m2.1:cloud` ([source][ollama-claude])

#### llama.cpp

llama.cpp server supports the Anthropic Messages API directly. It converts Anthropic format to OpenAI internally, reusing the existing inference pipeline ([source][llamacpp-anthropic]).

```bash
# Start llama.cpp server with a model
llama-server -hf unsloth/Qwen3-Next-80B-A3B-Instruct-GGUF:Q4_K_M

# Run Claude Code
ANTHROPIC_BASE_URL=http://127.0.0.1:8080 \
ANTHROPIC_API_KEY="" \
claude
```

#### LM Studio & Other OpenAI-Compatible Servers

Servers that only speak OpenAI's Chat Completions format (not Anthropic's Messages API) need a translation proxy. Options:

- **claude-code-proxy** ([source][cc-proxy]) — lightweight Python (FastAPI) proxy converting Anthropic → OpenAI format
- **Olla** ([source][olla]) — multi-backend proxy with load balancing across Ollama, LM Studio, and vLLM
- **LiteLLM** ([source][litellm]) — full-featured proxy with auth, rate limiting, audit logging

```bash
# Example with claude-code-proxy
ANTHROPIC_BASE_URL=http://localhost:8082 \
ANTHROPIC_API_KEY="any-value" \
claude
```

#### Tips for Local Models

| Tip | Detail |
|---|---|
| **KV cache invalidation** | CC prepends an attribution header that invalidates KV cache. Set `CLAUDE_CODE_ATTRIBUTION_HEADER=0` to prevent this ([source][local-setup]) |
| **Login bypass** | If CC prompts for login, add `"hasCompletedOnboarding": true` and `"primaryApiKey": "sk-dummy-key"` to `~/.claude.json` ([source][local-setup]) |
| **Non-essential traffic** | Set `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` to reduce calls to Anthropic servers ([source][cc-settings]) |
| **Cost savings** | Local models are free; third-party cloud options like DeepSeek V3.2 are ~$0.28/$0.42 per million tokens vs Opus 4.8 $5/$25 (Fable 5 $10/$50) ([source][models-pricing]) |

### LLM Gateway / Proxy Configuration

For enterprise or multi-provider setups, an LLM gateway sits between CC and the provider, translating API formats and adding features like auth, rate limiting, and audit logging.

#### LiteLLM

Full-featured proxy supporting 100+ providers. Recommended for team environments. Latest: v1.89.0 (2026-06-14, MIT) ([source][litellm]).

```bash
# Start LiteLLM proxy
litellm --model gpt-4o

# Point Claude Code at it
export ANTHROPIC_BASE_URL="http://0.0.0.0:4000"
export ANTHROPIC_AUTH_TOKEN="$LITELLM_MASTER_KEY"
claude --model gpt-4o
```

Supports: `claude --model gpt-4o`, `claude --model gemini-3.0-flash-exp`, `claude --model azure-gpt-4`, etc.

#### Bifrost (Maxim AI)

Open-source Go-based gateway supporting 1000+ models across 23+ providers (5,814 stars, Apache-2.0, enterprise v1.4.9). Intercepts Anthropic-format requests, converts to target provider format, and translates responses back transparently. Also acts as an MCP gateway (`claude mcp add --transport http bifrost http://localhost:8080/mcp`) that aggregates upstream MCP servers behind a single endpoint ([source][bifrost]).

#### Claude Code Router (CCR)

A local, **task-aware** router — not a passive translator. It intercepts CC's outbound requests and picks a provider/model **per request** by task type, token count, or custom rules, with no cloud hop for the routing logic ([source][cc-router]).

```bash
npm install -g @musistudio/claude-code-router
ccr start    # local router on :3456
ccr code     # launches CC with ANTHROPIC_BASE_URL=http://localhost:3456
```

- **Routing scenarios**: `default`, `background`, `think`, `longContext` (auto-switches past a token threshold, default ~60K), `webSearch`, `image` (beta)
- **Providers / transformers**: OpenRouter, DeepSeek, Gemini, Ollama, Volcengine, SiliconFlow, ModelScope, DashScope, AIHubmix; plus custom JS routing functions
- **Maturity**: very popular (35K stars, MIT, v2.0.0) but a large open-issue backlog (~800+) — pin a known-good version

Unlike the passive proxies above (LiteLLM/Bifrost translate API formats), CCR decides *which* model handles each request. CCR is also the community routing layer noted in [CC-vlm-screen-sharing-landscape.md](../../cc-community/CC-vlm-screen-sharing-landscape.md).

#### CLIProxyAPI

Wraps Claude Code (and Gemini CLI, ChatGPT Codex, Grok Build) as an OpenAI/Anthropic-compatible API endpoint, harvesting free-tier quota from existing authenticated CLI sessions — no API-key billing ([source][cliproxyapi]).

```bash
# Point any Anthropic-SDK client at the local proxy
export ANTHROPIC_BASE_URL=http://localhost:<PORT>
export ANTHROPIC_AUTH_TOKEN=<cliproxy-key>
```

- **Stars / version**: 37.6K stars, v7.2.7 (MIT, Go)
- **CC story**: wraps `claude` via OAuth account; supports multi-account switching, per-credential circuit breakers, quota management
- **Also routes**: Gemini CLI, Codex, Grok Build, Antigravity — plus OpenAI-compatible upstream relay (e.g. OpenRouter)
- **Companion GUI**: [EasyCLI][easycli] (Rust/Tauri desktop app)

#### 9Router

Multi-tool AI gateway with built-in RTK token compression (~20–40% savings), routing CC, Codex, Cursor, Cline, and Copilot to 40+ providers with auto-fallback ([source][9router]).

```bash
# Claude Code config in ~/.claude/config.json
# "anthropic_api_base": "http://localhost:20128/v1"
# "anthropic_api_key": "<9router-key>"
```

- **Stars / version**: 17.6K stars, v0.4.80 (MIT, JavaScript)
- **Providers**: OpenRouter, DeepSeek, Groq, xAI, Mistral, Kiro AI, OpenCode Free, Vertex AI, custom OpenAI-compatible endpoints, plus subscription proxies (CC, Codex, Copilot, Cursor)
- **Pricing**: free/open-source; no billing layer — users pay providers directly (free tiers available; cheap fallback from $0.20/1M tokens)

#### llama-swap

Hot-swaps local models on demand across llama.cpp, vLLM, tabbyAPI, and other backends — a zero-overhead router for multi-model local inference ([source][llama-swap]).

```bash
# ANTHROPIC_BASE_URL=http://localhost:<port>  (Anthropic-compatible endpoint)
# or OPENAI_BASE_URL for OpenAI-compatible path
```

- **Stars / version**: 4,571 stars, v226 (MIT, Go)
- **CC story**: exposes both `/v1/messages` (Anthropic) and `/v1/chat/completions` (OpenAI) — point CC at it via `ANTHROPIC_BASE_URL`. Routing is model-name-based: the `model` field in the request selects which backend process to hot-load.
- **Backends**: llama.cpp, vLLM, tabbyAPI, stable-diffusion.cpp, whisper.cpp, ik-llama-server, and any OpenAI/Anthropic-compatible server; OpenRouter supported as a remote peer.
- **No CC-specific docs** found as of 2026-06-16 — integration inferred from Anthropic endpoint support.

#### Claudish

580+ models via OpenRouter and direct provider integrations behind an `ANTHROPIC_BASE_URL` intercept; auto-detects well-known model names ([source][claudish]).

```bash
# Install via Homebrew, npm, or Bun; then:
export ANTHROPIC_BASE_URL=http://127.0.0.1:<PORT>
```

- **Stars / version**: 912 stars, v7.5.0 (MIT, TypeScript)
- **Providers**: OpenRouter (580+ models), Google Gemini, OpenAI, MiniMax, Kimi, GLM, Z.AI, OllamaCloud, Vertex AI, Ollama, LM Studio, vLLM, MLX
- **Routing**: `provider@model[:concurrency]` notation; auto-detection for well-known model names (e.g. `gemini-2.0-flash` routes to Google automatically)

#### Requesty

Hosted LLM router (SaaS) with 300–400+ models across 30+ providers, dedicated Claude Code integration, and optional analytics tagging by git branch/repo/developer ([source][requesty]).

```bash
export ANTHROPIC_BASE_URL=https://router.requesty.ai
export ANTHROPIC_AUTH_TOKEN=<requesty-api-key>
# EU residency: export ANTHROPIC_BASE_URL=https://router.eu.requesty.ai
```

- **Pricing**: pay-per-token at provider rates; $10 free credits for new accounts; enterprise volume discounts. No open-source core.
- **Analytics**: optional wrapper tags sessions with git metadata for per-developer cost attribution.

#### Hosted CC-Integrated Gateways (Portkey · Martian · Vercel · Zuplo · RelayPlane)

Five more hosted gateways document explicit Claude Code support — set `ANTHROPIC_BASE_URL` (plus the gateway's auth token) and CC routes through them. To avoid duplicating the catalog, provider breadth, licensing, and pricing for these (and ~30 more routers/gateways) live in [llm-routers-gateways-landscape.md](../../non-cc/llm-routers-gateways-landscape.md); the **CC-specific config** is below (each verified against the gateway's own CC docs, 2026-06-22):

| Gateway | CC config | First-party CC doc |
|---|---|---|
| **Portkey** | `ANTHROPIC_BASE_URL=https://api.portkey.ai` + `ANTHROPIC_AUTH_TOKEN=<portkey-key>` + `ANTHROPIC_CUSTOM_HEADERS` carrying `x-portkey-api-key` and `x-portkey-provider: @<provider-slug>` — one unified endpoint fronting Anthropic/Bedrock/Vertex backends; OSS gateway is also self-hostable | [portkey.ai/docs][portkey-cc] |
| **Martian** | `ANTHROPIC_BASE_URL=https://api.withmartian.com/v1`; key via `apiKeyHelper: echo $MARTIAN_API_KEY` — per-request ML cost-quality routing | [docs.withmartian.com][martian-cc] |
| **Vercel AI Gateway** | `ANTHROPIC_BASE_URL=https://ai-gateway.vercel.sh` — Anthropic Messages API, zero token markup, BYOK option | [vercel.com/docs][vercel-gw] |
| **Zuplo AI Gateway** | `ANTHROPIC_BASE_URL=<your-app-gateway-url>` + `ANTHROPIC_AUTH_TOKEN=<app-key>` — per-app URL after provider/team/app setup; serves Anthropic `/v1/messages` | [zuplo.com/docs][zuplo-cc] |
| **RelayPlane** | local Node.js proxy (no Docker) wired via a `settings.json` hook; `rp:best` / `rp:cheap` model offload through OpenRouter | [relayplane.com][relayplane] |

All five satisfy the [Gateway Requirements](#gateway-requirements) below (Anthropic `/v1/messages` + forwarded `anthropic-beta` / `anthropic-version` headers).

#### Direct CC-Compatible Endpoints

Some providers expose Anthropic-compatible endpoints natively (no proxy needed):

```bash
# Example: Z.AI
export ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
export ANTHROPIC_AUTH_TOKEN=YOUR_API_KEY
claude
```

#### Gateway Requirements

For a gateway to work with CC, it must ([source][cc-settings]):

- Expose at least one of: Anthropic Messages (`/v1/messages`), Bedrock InvokeModel (`/invoke`), or Vertex rawPredict (`:rawPredict`)
- Forward required headers: `anthropic-beta`, `anthropic-version`

When routing through gateways, additionally set ([source][cc-settings]):

- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` — disable Anthropic-specific `anthropic-beta` headers
- `CLAUDE_CODE_SKIP_*_AUTH=true` — skip native provider auth (Bedrock/Vertex/Foundry)

## Output & Context Tuning

| Variable | Purpose | Default |
| -------- | ------- | ------- |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max output tokens | 32,000 (max 64,000) |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | Token limit for file reads | Default |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | Disable 1M context window (see [extended context analysis](../context-memory/CC-extended-context-analysis.md)) | `1` to disable |

([source][cc-settings])

## Applicability

| Aspect | Fit | Rationale |
| ------ | --- | --------- |
| Model override (`ANTHROPIC_MODEL`) | Strong | Direct env var control per run; useful in any project to select model per task |
| Subagent model (`CLAUDE_CODE_SUBAGENT_MODEL`) | Strong | Control cost by routing teammates/subagents to cheaper models |
| OpenRouter for failover | Strong | Provider failover during Anthropic outages + centralized budget controls |
| Ollama / local models | Moderate | Free, private, no API dependency; limited by local hardware and model quality |
| LLM gateway (LiteLLM/Bifrost) | Moderate | Team auth, rate limiting, multi-provider routing; adds infrastructure |
| Bedrock/Vertex/Foundry | Conditional | Relevant when a project runs on cloud infrastructure |
| Effort level tuning | Strong | `CLAUDE_CODE_EFFORT_LEVEL=medium` for routine tasks saves tokens |

### Decision Rule

**Model and effort variables are immediately useful** for optimizing autonomous CC runs (cost vs quality trade-offs). OpenRouter is recommended for provider failover and team budget controls. Local models (Ollama) are useful for privacy-sensitive work, offline development, or eliminating API costs — but quality and context window are limited by hardware. LLM gateways (LiteLLM) add value for team environments needing auth and audit logging. Cloud providers (Bedrock/Vertex/Foundry) are relevant once a project runs on cloud infrastructure.

### Provider Decision Matrix

| Need | Best Option | Setup Effort |
|---|---|---|
| **Default (best quality)** | Anthropic API direct | None |
| **Failover / budget** | OpenRouter | Low (env vars) |
| **Free / private / offline** | Ollama + local model | Medium (install + model download) |
| **Multi-provider / team** | LiteLLM proxy | Medium (proxy setup) |
| **Enterprise cloud** | Bedrock / Vertex / Foundry | High (cloud config) |
| **Non-Anthropic models in CC** | LiteLLM or claude-code-proxy | Medium (proxy) |
| **Per-task local routing / cost control** | Claude Code Router (CCR) | Medium (npm + `ccr start`) |
| **EU / Swiss data sovereignty, OSS models** | Infomaniak AI (+ proxy for CC; native in OpenCode) | Medium (OpenAI→Anthropic proxy) |
| **Free-tier quota harvesting (no API key)** | CLIProxyAPI | Medium (OAuth setup + local server) |
| **Multi-tool gateway + token compression** | 9Router | Medium (local server + config) |
| **Hot-swap multiple local models** | llama-swap | Medium (config + backends) |
| **580+ models via OpenRouter / direct providers** | Claudish | Low (install + env var) |
| **Hosted SaaS router, per-developer analytics** | Requesty | Low (env vars only) |

## Cross-References

- [CC-models-reference.md](CC-models-reference.md) — Fable 5 model card + free-tier/OSS provider reference table
- [CC-cli-reference.md](CC-cli-reference.md) — canonical flag definitions (`--model`, `--effort`, `--fallback-model`, `--betas`)
- [CC-env-vars-reference.md](CC-env-vars-reference.md) — env var reference for `ANTHROPIC_MODEL`, `CLAUDE_CODE_EFFORT_LEVEL`, etc.
- [llm-routers-gateways-landscape.md](../../non-cc/llm-routers-gateways-landscape.md) — authoritative provider-agnostic router/gateway catalog (license, pricing, model breadth) for the gateways above and ~30 more; this doc holds only their CC-specific config

## References

- [CC Settings — Environment Variables][cc-settings]
- [CC Model Configuration — Effort Levels][cc-effort]
- [CC Model Configuration — ultrathink][cc-ultrathink]
- [Anthropic — Pricing][models-pricing]
- [OpenRouter — Claude Code Integration][openrouter]
- [Ollama — Claude Code with Anthropic API Compatibility][ollama-claude]
- [llama.cpp — Anthropic Messages API][llamacpp-anthropic]
- [LiteLLM — Claude Code with Non-Anthropic Models][litellm]
- [claude-code-proxy (GitHub)][cc-proxy]
- [Olla — Multi-Backend Proxy][olla]
- [Bifrost — Open-Source AI Gateway][bifrost]
- [Claude Code Router (CCR)][cc-router]
- [CLIProxyAPI][cliproxyapi]
- [9Router][9router]
- [llama-swap][llama-swap]
- [Claudish (MadAppGang)][claudish]
- [Requesty — Claude Code Integration][requesty]
- [Portkey — Claude Code integration][portkey-cc]
- [Martian — Claude Code integration][martian-cc]
- [Vercel AI Gateway docs][vercel-gw]
- [Zuplo AI Gateway — Claude Code integration][zuplo-cc]
- [RelayPlane][relayplane]
- [Local setup guide][local-setup]
- [Infomaniak — Open-Source AI Models][infomaniak-ai]
- [Infomaniak — vLLM TranslateGemma-27B (Hugging Face)][infomaniak-translategemma]
- [OpenCode + Infomaniak AI Tools setup (janikvonrotz)][infomaniak-opencode]
- [n8n community — add Infomaniak AI language model][infomaniak-n8n]

[cc-settings]: https://code.claude.com/docs/en/settings#environment-variables
[cc-effort]: https://code.claude.com/docs/en/model-config#adjust-effort-level
[cc-ultrathink]: https://code.claude.com/docs/en/model-config#use-ultrathink-for-one-off-deep-reasoning
[openrouter]: https://openrouter.ai/docs/cookbook/coding-agents/claude-code-integration
[ollama-claude]: https://ollama.com/blog/claude
[llamacpp-anthropic]: https://huggingface.co/blog/ggml-org/anthropic-messages-api-in-llamacpp
[litellm]: https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models
[cc-proxy]: https://github.com/fuergaosi233/claude-code-proxy
[olla]: https://thushan.github.io/olla/integrations/frontend/claude-code/
[bifrost]: https://www.getmaxim.ai/articles/running-non-anthropic-models-in-claude-code-via-an-enterprise-ai-gateway/
[cc-router]: https://github.com/musistudio/claude-code-router
[cliproxyapi]: https://github.com/router-for-me/CLIProxyAPI
[easycli]: https://github.com/router-for-me/EasyCLI
[9router]: https://github.com/decolua/9router
[llama-swap]: https://github.com/mostlygeek/llama-swap
[claudish]: https://github.com/MadAppGang/claudish
[requesty]: https://docs.requesty.ai/integrations/claude-code
[local-setup]: https://medium.com/@luongnv89/run-claude-code-on-local-cloud-models-in-5-minutes-ollama-openrouter-llama-cpp-6dfeaee03cda
[models-pricing]: https://platform.claude.com/docs/en/about-claude/pricing
[infomaniak-ai]: https://www.infomaniak.com/en/hosting/ai-services/open-source-models
[infomaniak-translategemma]: https://huggingface.co/Infomaniak-AI/vllm-translategemma-27b-it
[infomaniak-opencode]: https://janikvonrotz.ch/2026/04/01/setup-opencode-with-infomaniak-ai-tools/
[infomaniak-n8n]: https://community.n8n.io/t/add-new-language-model-informaniak-ai/73182
[portkey-cc]: https://portkey.ai/docs/integrations/libraries/claude-code
[martian-cc]: https://docs.withmartian.com/integrations/claude-code
[vercel-gw]: https://vercel.com/docs/ai-gateway
[zuplo-cc]: https://zuplo.com/docs/ai-gateway/integrations/claude-code
[relayplane]: https://relayplane.com/
