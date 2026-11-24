---
title: CC Model & Provider Configuration
source: https://code.claude.com/docs/en/env-vars
purpose: Reference for configuring Claude Code with alternative models, endpoints, API keys, third-party providers, local models and LLM gateway proxies.
created: 2026-03-07
updated: 2026-11-23
validated_links_on: 2026-11-09
status: reference
---

**Details:** actionable configuration guide

## Model Selection

| Variable | Purpose | Example |
| -------- | ------- | ------- |
| `ANTHROPIC_MODEL` | Primary model override | `claude-sonnet-4-6` |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Override Haiku-class model | Custom model ID |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Override Sonnet-class model | Custom model ID |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Override Opus-class model | Custom model ID |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for subagents/teammates | Custom model ID |
| `CLAUDE_CODE_EFFORT_LEVEL` | Reasoning effort on effort-capable models (see [Effort Levels](#effort-levels)) | `low`, `medium`, `high`, `xhigh`, `max` |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` | Disable adaptive reasoning | `1` |

All variables can also be set in `settings.json` under the `env` key. ([source][cc-settings])

### Effort Levels

`CLAUDE_CODE_EFFORT_LEVEL` (above), the `/effort` command, the effort slider in `/model`, the `--effort` flag, the `modelSettings` and `effortLevel` settings, and per-skill/subagent `effort` frontmatter all select an **adaptive-reasoning effort level**. Which levels exist, and which one is the default, depend on the model ([source][cc-effort], checked 2026-11-19):

| Model | Levels | Default |
|---|---|---|
| Fable 5.2 | `low`, `medium`, `high`, `xhigh`, `max` | `medium` |
| Other Fable models (Fable 5, Fable 5.1) | `low`, `medium`, `high`, `xhigh`, `max` | `high` |
| Opus 5.5, Sonnet 5.5, Haiku 5.5 | `low`, `medium`, `high`, `xhigh`, `max` | `medium` |
| Opus 5, Sonnet 5, Opus 4.8 | `low`, `medium`, `high`, `xhigh`, `max` | `high` |
| Opus 4.7 | `low`, `medium`, `high`, `xhigh`, `max` | `xhigh` |
| Opus 4.6, Sonnet 4.6 | `low`, `medium`, `high`, `max` (no `xhigh`) | `high` |

The page states the defaults as one rule: Fable 5.2, Opus 5.5, Sonnet 5.5 and Haiku 5.5 default to `medium`, Opus 4.7 to `xhigh`, and every other model in its effort table to `high`. Models missing from that table do not support effort. An organization that sets a default effort for its organization default model overrides the model default for that model. Setting an unsupported level falls back to the highest supported level at or below it (e.g. `xhigh` runs as `high` on Opus 4.6). The page names no other plan-specific default. The docs note that Opus 5.5 at `medium` matches or exceeds Opus 5 at `high` on Anthropic's coding and knowledge-work evaluations (vendor claim), and that the scale is calibrated per model, so the same level name is not the same setting across models.

**Precedence & persistence** ([source][cc-effort]):

- Resolution order, first that applies: `CLAUDE_CODE_EFFORT_LEVEL` > a level picked in the session (`/effort`, the `/model` slider) > `--effort` > settings (`modelSettings` per model, or `effortLevel`) > the model default. Skill and subagent `effort` frontmatter overrides the session level while it runs, unless `CLAUDE_CODE_EFFORT_LEVEL` is set; `maxEffortLevel` and Enterprise per-role effort caps still limit it.
- `low`/`medium`/`high`/`xhigh` picked interactively are **saved per model** under `modelSettings` (press `s` in the slider to apply to the session only, v2.1.257+); a level set with `/effort` in a `-p` run is session-only. `max` is **session-only** unless set through `CLAUDE_CODE_EFFORT_LEVEL`; neither `max` nor `ultracode` is accepted in `effortLevel` or `modelSettings`.
- Opus 5.5 and later models ignore a top-level `effortLevel` in the *user* settings file (the older, pre-per-model form) and start at their own default until you pick a level for them; a top-level `effortLevel` in project, local or managed settings still applies to every model.
- `/effort auto` clears the saved level for the active model. `CLAUDE_CODE_EFFORT_LEVEL=auto` (or `unset`) is different: Claude Code then sends **no** effort level, so the API's own default applies.
- A subagent or teammate without its own `effort` runs at the session's level only when it is on the main conversation's model; on another model, set `effort` in its definition.

**Related, but not effort levels**:

- **`ultracode`** — a Claude Code setting, not an effort level: with it on, Claude orchestrates dynamic workflows for substantive tasks at whatever level the session runs at (from v2.1.284; earlier builds forced `xhigh`). `--effort ultracode` turns it on *and* sets `xhigh`; it is not accepted by `effortLevel` or `CLAUDE_CODE_EFFORT_LEVEL`, and it needs a model that supports `xhigh`. See [CC-dynamic-workflows-analysis.md](../agents-skills/CC-dynamic-workflows-analysis.md#ultracode-effort-setting).
- **`ultrathink`** — include it anywhere in a prompt for one-off deeper reasoning on that turn; Claude Code adds an in-context instruction but the **effort level sent to the API is unchanged**. Phrases like "think", "think hard", and "think more" are *not* recognized keywords ([source][cc-ultrathink]).

**Verified 2026-11-19** against the model-config page. Effort availability and defaults are model-generation-specific and shift with each model release; for gateway or provider model IDs that Claude Code does not recognize, the `xhigh_effort` and `max_effort` capability values in `ANTHROPIC_DEFAULT_*_MODEL_SUPPORTED_CAPABILITIES` turn those levels on ([source][cc-effort]). Lowering effort is one of the documented cost levers; see [CC-session-cost-analysis.md § Documented cost levers](../sessions/CC-session-cost-analysis.md#documented-cost-levers).

### Fable Models

Claude **Fable 5.2** (`claude-fable-5-2`) has superseded **Fable 5** (`claude-fable-5`) as the newest Fable model (see CC-models-reference.md); either is selectable in CC via `/model` or `ANTHROPIC_MODEL`. For its model card (context, pricing, tokenizer/refusal caveats, CC plan access) see [CC-models-reference.md](CC-models-reference.md); free-tier and OSS provider facts are in [Free-tier and OSS inference providers](#free-tier-and-oss-inference-providers) below.

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

Or in `.claude/settings.local.json` (project-level; this file holds a key, so make sure git ignores it — Claude Code adds it to your global git excludes only once it has written the file itself; a file you create by hand needs a `.gitignore` entry, [source](https://code.claude.com/docs/en/settings#keep-personal-settings-out-of-a-repository)):

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

AWS's agent stack (AgentCore, Bedrock Agents, Amazon Quick; roles, identity, licences) is covered in
[aws-agent-stack-analysis.md](../../non-cc/agents/aws-agent-stack-analysis.md). Six cloud agent stacks are compared in
[cloud-agent-platforms-landscape.md](../../non-cc/infrastructure/cloud-agent-platforms-landscape.md).

### Google Vertex AI

```bash
export CLAUDE_CODE_USE_VERTEX=true
# For LLM gateways: export CLAUDE_CODE_SKIP_VERTEX_AUTH=true
```

([source][cc-settings])

Google Cloud's agent stack (Agent Platform, formerly Vertex AI; roles, identity, licences) is covered in
[google-cloud-agent-stack-analysis.md](../../non-cc/agents/google-cloud-agent-stack-analysis.md).

### Microsoft Azure Foundry

```bash
export CLAUDE_CODE_USE_FOUNDRY=true
export ANTHROPIC_FOUNDRY_BASE_URL="https://my-resource.services.ai.azure.com/anthropic"
# Or: export ANTHROPIC_FOUNDRY_RESOURCE="my-resource"
# Optional: export ANTHROPIC_FOUNDRY_API_KEY="<api-key>"
# For LLM gateways: export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=true
```

([source][cc-settings])

Foundry as Microsoft's agent platform (agent types, tools, Claude model hosting and billing) is covered in [microsoft-365-copilot-analysis.md § Foundry as an agent platform](../../non-cc/agents/microsoft-365-copilot-analysis.md#foundry-as-an-agent-platform); Foundry roles, identity and licences in [§ Roles, identity and licences](../../non-cc/agents/microsoft-365-copilot-analysis.md#roles-identity-and-licences).

### Infomaniak AI (Swiss-hosted, OpenAI-Compatible)

Infomaniak (Swiss host) runs an **OpenAI-compatible** inference API serving open-source models. Read 2026-11-23 from the vendor's [models page][infomaniak-models], [prices page][infomaniak-prices] and [AI Services page][infomaniak-ai]; data-location and privacy statements below are **vendor claims**, not independently verified. Because it speaks OpenAI Chat Completions rather than the Anthropic Messages API, **using it from CC needs a translation proxy** (LiteLLM or claude-code-proxy; see the LLM Gateway / Proxy section below); OpenAI-native agents such as OpenCode and n8n point at it directly. The same generic route for Codex CLI is limited by the Responses-API requirement noted in [codex-cli-analysis.md § Providers](../../non-cc/coding-agents/codex-cli-analysis.md#providers).

```bash
# product_id is per-organization: GET https://api.infomaniak.com/1/ai (Authorization: Bearer $API_TOKEN)
# v2 (current) OpenAI-compatible base URL (per models.dev and a third-party blog; not checked in Infomaniak's developer docs):
https://api.infomaniak.com/2/ai/${PRODUCT_ID}/openai/v1
```

The v2 base URL form is also listed by the third-party catalog [models.dev][infomaniak-modelsdev] (read 2026-11-23, via the `@ai-sdk/openai-compatible` package).

**Models (vendor models page, 2026-11-23).** All chat models list function calling. Max input tokens as the page states them:

| Model id | Max input | Notes (vendor wording, condensed) |
| --- | --- | --- |
| `moonshotai/Kimi-K2.6` | 256K | Beta; image-text input; pitched for coding and agent workflows |
| `Qwen/Qwen3.5-397B-A17B-FP8` | 200K | Beta; image-text input; the page's "most powerful" |
| `Qwen/Qwen3.8-27B-FP8` | 100K | Beta; image-text input; thinking mode on by default |
| `mistralai/Mistral-Small-4-119B-2603` | 256K | Image-text input |
| `swiss-ai/Apertus-v1.5-70B` | 100K | Beta; image-audio-text input; vendor stresses open weights and training-data transparency |
| `google/gemma-4-31B-it` | 100K | Text input |
| `mistralai/Ministral-3-14B-Instruct-2512` | 100K | Image-text input; small and cheap |

The page also lists re-rankers (`BAAI/bge-reranker-v2-m3`, `Qwen/Qwen3-Reranker-0.6B`), embeddings (`Qwen/Qwen3-Embedding-8B`, Bge Multilingual Gemma2, All MiniLM L12 v2), Whisper V3 transcription and image generation. The catalog moves: the older `qwen3` / `llama3` / `mistral3` / `gemma3n` ids in this doc's earlier recipe no longer match this list, and models.dev (10 models at the same read) lacked Qwen3.8-27B, so check the vendor page before pinning an id.

**Pricing (vendor prices page, 2026-11-23, CHF per 1M tokens, excluding VAT, input / output).** Gemma 4 31B 0.20 / 0.40; Ministral 3 14B 0.30 / 0.40; Kimi K2.6 0.60 / 3.00; Mistral Small 4 0.20 / 0.75; Qwen3.5 397B 0.80 / 3.60; Apertus 70B 0.70 / 2.50; Qwen3.8 27B 0.40 / 3.00. Billing is per token, invoiced monthly; Whisper V3 is CHF 0.006 per minute. The vendor offers 1M free credits; the page does not state an expiry, and the prices page says a valid payment card is required. Earlier versions of this doc listed Llama-family models and an Infomaniak build of TranslateGemma-27B; the 2026-11-23 models page lists neither. models.dev (third party) lists different USD prices for some of the same models, so treat vendor CHF prices as the reference.

**Data location (vendor claims).** The page says infrastructure is in Switzerland, that queries are not stored or used for training, and that the service complies with the Swiss FADP and GDPR (Federal Act on Data Protection; General Data Protection Regulation).

- **OpenCode** ([source][infomaniak-opencode], blog dated 2026-04-01): register a provider in `~/.config/opencode/opencode.json` using the `@ai-sdk/openai-compatible` package with `baseURL` set to the v2 endpoint; the recipe's model ids predate the current list. It wires `API_TOKEN` (created with the `ai-tools` scope at manager.infomaniak.com) and `PRODUCT_ID` as environment variables.
- **n8n** ([source][infomaniak-n8n]): no native node; use the built-in OpenAI node with a custom base URL (`.../1/ai/{product_id}/openai`) and the API token as the key. The credential test fails but inference works; early threads predated function-calling support.

### Free-tier and OSS inference providers

Snapshot of providers with free or trial tiers, for routing CC (via proxy) or sibling agents (OpenCode, n8n, PydanticAI) to non-Anthropic models. Moved here from `CC-models-reference.md` on 2026-11-23 (Infomaniak is in its own section above). The columns are the **February 2026 snapshot**; four rows were re-checked at source on 2026-11-23 and are marked. Free-tier terms and model ids change often, so confirm on each provider's site before relying on a row.

| Provider | Free Tier | Example Model (API ID) | Context | Output | Tools | Notes / Limit |
| --- | --- | --- | --- | --- | --- | --- |
| **gemini** | Free tier (Feb 2026 snapshot; unconfirmed 2026-11-23) | `gemini-2.0-flash` | 1M | 8K | Yes | 15 RPM, ~1.5K RPD (Feb 2026). **Re-check 2026-11-23:** the [rate-limits page][rl-gemini] gives no free-tier numbers for this model; read current limits in AI Studio |
| **github** | Truly free | `gpt-4.1-mini` | 1M | 32K | Yes | 15 RPM, ~150 RPD |
| **cerebras** | Free trial (2026-11-23) | `gpt-oss-120b` | 128K | 8K | Yes | 5 RPM, 1M TPD on the free trial ([rate-limits page][rl-cerebras], 2026-11-23; was 30 RPM in Feb 2026); $5 credits after adding a verified payment method, expiring 30 days after grant |
| **groq** | Free plan (Feb 2026 snapshot; unconfirmed 2026-11-23) | `llama-3.3-70b-versatile` | 131K | 32K | Yes | 30 RPM, 1K RPD (Feb 2026). **Re-check 2026-11-23:** the [limits page][rl-groq] showed no free-plan table; not confirmed |
| **mistral** | Truly free | `open-mistral-nemo` | 128K | 4K | Yes | 1 RPS, 1B tokens/mo |
| **openrouter** | Truly free | `qwen/qwen3-next-80b-a3b-instruct:free` | 262K | 8K | Yes | 20 RPM, 50 RPD. **Re-check 2026-11-23:** [limits page][rl-openrouter] confirms 20 RPM / 50 RPD under 10 purchased credits, 1000 RPD from 10 credits |
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

Rows without a re-check note were not re-verified on 2026-11-23 and are carried over as the February 2026 snapshot (unverified since).

> **OpenAI-compatible tool calling**: some providers reject strict tool-definition schemas: `groq`, `cerebras`, `fireworks`, `together`, `sambanova`. With PydanticAI, set `OpenAIModelProfile(openai_supports_strict_tool_definition=False)` for these.

(`restack`, which appears on some provider lists, is a workflow-orchestration platform, not an inference provider; it proxies to others.)

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

#### Strata

[Strata][strata] runs `Qwen3.8-Flash-Next` locally (NVIDIA/AMD GPU, 12GB+ VRAM, Windows/Linux,
one-click installer) and documents the exact CC env var for its Anthropic-compatible endpoint
verbatim in its own README: "Apps that use Anthropic's API: `http://127.0.0.1:8080/v1/messages`
(Claude Code: `ANTHROPIC_BASE_URL=http://127.0.0.1:8080`)" ([source][strata]).

```bash
# After the Strata installer starts the engine on 127.0.0.1:8080
ANTHROPIC_BASE_URL=http://127.0.0.1:8080 \
claude
```

- Also exposes an OpenAI-compatible endpoint at `/v1` for non-Anthropic clients, and `/v1/responses` for Codex CLI and other OpenAI Responses API clients.
- Ships a separate Model Context Protocol (MCP) server (`tools/strata_mcp.py`, stdlib-only Python) that lets an agent **manage** Strata itself — install, start, stop, check VRAM/logs, recommend a model size for the host's hardware — via `claude mcp add strata -- python3 /path/to/Strata/tools/strata_mcp.py`. This is setup/ops tooling, not an inference-serving MCP tool; the Anthropic-compatible HTTP endpoint above is what Claude Code actually talks to for inference.
- MIT, 21,540 stars, 2,037 forks (`gh api`, 2026-10-11); created 2026-09-24 — 17 days old at time of writing, so no independent track record yet.

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
- **CC story**: wraps `claude` via OAuth account; supports multi-account switching, per-credential circuit breakers, quota management. Note this is *gateway-level* multi-account (quota harvesting for downstream clients) — for running N interactive CC sessions on N subscription accounts, see [CC-multi-account-switching-landscape.md](../../cc-community/CC-multi-account-switching-landscape.md)
- **Also routes**: Gemini CLI (status 2026-11-18: [no longer served for free, AI Pro, AI Ultra users](../../non-cc/coding-agents/gemini-cli-analysis.md), so its free-tier quota harvesting no longer applies to those accounts; routing claims are the project's own), Codex, Grok Build, Antigravity — plus OpenAI-compatible upstream relay (e.g. OpenRouter)
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

#### Hosted CC-Integrated Gateways (Portkey · Martian · Vercel · Zuplo)

Four more hosted gateways document explicit Claude Code support — set `ANTHROPIC_BASE_URL` (plus the gateway's auth token) and CC routes through them. To avoid duplicating the catalog, provider breadth, licensing, and pricing for these (and ~30 more routers/gateways) live in [llm-routers-gateways-landscape.md](../../non-cc/infrastructure/llm-routers-gateways-landscape.md); the **CC-specific config** is below (each verified against the gateway's own CC docs, 2026-06-22):

| Gateway | CC config | First-party CC doc |
|---|---|---|
| **Portkey** | `ANTHROPIC_BASE_URL=https://api.portkey.ai` + `ANTHROPIC_AUTH_TOKEN=<portkey-key>` + `ANTHROPIC_CUSTOM_HEADERS` carrying `x-portkey-api-key` and `x-portkey-provider: @<provider-slug>` — one unified endpoint fronting Anthropic/Bedrock/Vertex backends; OSS gateway is also self-hostable | [portkey.ai/docs][portkey-cc] |
| **Martian** | `ANTHROPIC_BASE_URL=https://api.withmartian.com/v1`; key via `apiKeyHelper: echo $MARTIAN_API_KEY` — per-request ML cost-quality routing | [docs.withmartian.com][martian-cc] |
| **Vercel AI Gateway** | `ANTHROPIC_BASE_URL=https://ai-gateway.vercel.sh` — Anthropic Messages API, zero token markup, BYOK option | [vercel.com/docs][vercel-gw] |
| **Zuplo AI Gateway** | `ANTHROPIC_BASE_URL=<your-app-gateway-url>` + `ANTHROPIC_AUTH_TOKEN=<app-key>` — per-app URL after provider/team/app setup; serves Anthropic `/v1/messages` | [zuplo.com/docs][zuplo-cc] |

All four satisfy the [Gateway Requirements](#gateway-requirements) below (Anthropic `/v1/messages` + forwarded `anthropic-beta` / `anthropic-version` headers).

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

#### Claude apps gateway

Anthropic's own self-hosted gateway runs Claude Code through Amazon Bedrock, Claude Platform on AWS, Google Cloud or Microsoft Foundry "with SSO sign-in, per-group model access, and OTLP telemetry" ([overview][cc-apps-gateway]). Budget rules in its `gateway.yaml` ([configuration reference][cc-apps-gateway-config], checked 2026-11-15):

- **Pooled budgets.** For a developer in several groups with pooled budgets, "each request counts against the first budget whose spend is below its limit, and is refused when every budget is used up."
- **Order.** `admin.pooled_conflict_rule` is `default_order` (the default) or `priority_list`; with `priority_list`, `admin.pooled_priority_order` names up to 50 groups whose budgets are tried first. Both need v2.1.319 or later.
- **Spend in `/usage`.** Once the gateway runs 2.1.319 or later, developers behind it who have no spend limit see their spend for today, this week and this month in `/usage` ([changelog][cc-changelog]).

Auto mode behind a gateway depends on `CLAUDE_CODE_AUTO_MODE_SERVER`; see [CC-env-vars-reference.md § Session Guards & Runtime](CC-env-vars-reference.md#session-guards--runtime).

### Changes in v2.1.321–325

Changelog entries unless marked; see [CC-env-vars-reference](CC-env-vars-reference.md#v21321325-additions) for the variables.

- **Unrecognized model IDs assume a 1M window (v2.1.323).** The window assumed for an ID Claude Code does not recognize moved from 200K to 1M; `/autocompact` compacts earlier and `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` keeps 200K. On other vendors' smaller-window models a full session can fail every turn until `/clear`, so set the variable before it fills. From v2.1.325 `CLAUDE_CODE_MAX_CONTEXT_TOKENS` also sets the window for unrecognized IDs starting with `claude-` (a gateway's `claude-sonnet-latest`).
- **Fable 5.1 picks move to `fable` (v2.1.321).** Saved Fable 5.1 model picks move to the `fable` alias: at once on Pro and Max, on Team and Enterprise once the organization allows it; `/model claude-fable-5-1` switches back.
- **Fast mode on Vertex (v2.1.322).** Fable 5.2 only, region `global`, `us` or `eu`; see [CC-fast-mode-analysis](CC-fast-mode-analysis.md) (documented on the fast-mode page).
- **Claude apps gateway (v2.1.321).** `policy_mode: layered` now adds managed MCP servers over every matching policy, `match: {}` included, so a gateway already on it serves more after the upgrade; Bedrock, Vertex and Foundry upstreams ignore the gateway environment's `ANTHROPIC_*_BASE_URL` variables, so set `base_url` on the upstream. v2.1.323: `/v1/models` states `max_input_tokens` for models whose window is certain on every upstream.
- **Proxy handling (v2.1.323, v2.1.325).** Organization settings and policy requests ignore a proxy set only by `ALL_PROXY`; plugin downloads use a CONNECT tunnel when `ALL_PROXY` is the only proxy.
- **Cost accounting (v2.1.325).** `/cost`, `--max-budget-usd` and the cost and token metrics now count a mod's `$.model.complete` and `$.model.classify` calls.

## Output & Context Tuning

| Variable | Purpose | Default |
| -------- | ------- | ------- |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max output tokens | 32,000 (max 64,000) |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | Token limit for file reads | Default |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | `1` removes `[1m]` variants and holds models that default to the 1M window to 200K; since v2.1.323 it also keeps 200K for an unrecognized model ID (see [extended context analysis](../context-memory/CC-extended-context-analysis.md)) | unset |

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
| **Swiss-hosted data (vendor claim), OSS models** | Infomaniak AI (+ proxy for CC; native in OpenCode) | Medium (OpenAI→Anthropic proxy) |
| **Free or trial inference tiers** | [Free-tier provider table](#free-tier-and-oss-inference-providers) (+ proxy for CC) | Medium (OpenAI→Anthropic proxy) |
| **Free-tier quota harvesting (no API key)** | CLIProxyAPI | Medium (OAuth setup + local server) |
| **Multi-tool gateway + token compression** | 9Router | Medium (local server + config) |
| **Hot-swap multiple local models** | llama-swap | Medium (config + backends) |
| **580+ models via OpenRouter / direct providers** | Claudish | Low (install + env var) |
| **Hosted SaaS router, per-developer analytics** | Requesty | Low (env vars only) |

## Cross-References

- [CC-models-reference.md](CC-models-reference.md) — model card, 5.x lifecycle and pricing (model facts; this doc owns provider facts)
- [CC-cli-reference.md](CC-cli-reference.md) — canonical flag definitions (`--model`, `--effort`, `--fallback-model`, `--betas`)
- [CC-env-vars-reference.md](CC-env-vars-reference.md) — env var reference for `ANTHROPIC_MODEL`, `CLAUDE_CODE_EFFORT_LEVEL`, etc.
- [llm-routers-gateways-landscape.md](../../non-cc/infrastructure/llm-routers-gateways-landscape.md) — authoritative provider-agnostic router/gateway catalog (license, pricing, model breadth) for the gateways above and ~30 more; this doc holds only their CC-specific config

## References

- [CC Settings — Environment Variables][cc-settings]
- [CC Model Configuration — Effort Levels][cc-effort]
- [CC Model Configuration — ultrathink][cc-ultrathink]
- [Anthropic — Pricing][models-pricing]
- [OpenRouter — Claude Code Integration][openrouter]
- [Ollama — Claude Code with Anthropic API Compatibility][ollama-claude]
- [llama.cpp — Anthropic Messages API][llamacpp-anthropic]
- [Strata — README (local Qwen3.8-Flash-Next engine, Anthropic/OpenAI-compatible endpoints)][strata]
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
- [Local setup guide][local-setup]
- [Infomaniak — AI Services][infomaniak-ai], [Open-Source AI Models][infomaniak-models] and [Prices][infomaniak-prices] (read 2026-11-23)
- [models.dev — Infomaniak provider][infomaniak-modelsdev] (third-party catalog)
- Rate-limit pages re-checked 2026-11-23: [Gemini API][rl-gemini], [Cerebras][rl-cerebras], [Groq][rl-groq], [OpenRouter][rl-openrouter]
- [OpenCode + Infomaniak AI Tools setup (janikvonrotz)][infomaniak-opencode]
- [n8n community — add Infomaniak AI language model][infomaniak-n8n]

[cc-settings]: https://code.claude.com/docs/en/env-vars
[cc-effort]: https://code.claude.com/docs/en/model-config#adjust-effort-level
[cc-ultrathink]: https://code.claude.com/docs/en/model-config#use-ultrathink-for-one-off-deep-reasoning
[openrouter]: https://openrouter.ai/docs/cookbook/coding-agents/claude-code-integration
[ollama-claude]: https://ollama.com/blog/claude
[llamacpp-anthropic]: https://huggingface.co/blog/ggml-org/anthropic-messages-api-in-llamacpp
[strata]: https://github.com/Niko1221/Strata
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
[infomaniak-ai]: https://www.infomaniak.com/en/hosting/ai-services
[infomaniak-models]: https://www.infomaniak.com/en/hosting/ai-services/open-source-models
[infomaniak-prices]: https://www.infomaniak.com/en/hosting/ai-services/prices
[infomaniak-modelsdev]: https://models.dev/providers/infomaniak/
[rl-gemini]: https://aistudio.google.com/docs/rate-limits
[rl-cerebras]: https://inference-docs.cerebras.ai/support/rate-limits
[rl-groq]: https://console.groq.com/docs/rate-limits
[rl-openrouter]: https://openrouter.ai/docs/api-reference/limits
[infomaniak-opencode]: https://janikvonrotz.ch/2026/04/01/setup-opencode-with-infomaniak-ai-tools/
[infomaniak-n8n]: https://community.n8n.io/t/add-new-language-model-informaniak-ai/73182
[portkey-cc]: https://portkey.ai/docs/integrations/libraries/claude-code
[martian-cc]: https://docs.withmartian.com/integrations/claude-code
[vercel-gw]: https://vercel.com/docs/ai-gateway
[zuplo-cc]: https://zuplo.com/docs/ai-gateway/integrations/claude-code
[cc-apps-gateway]: https://code.claude.com/docs/en/claude-apps-gateway
[cc-apps-gateway-config]: https://code.claude.com/docs/en/claude-apps-gateway-config
[cc-changelog]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
