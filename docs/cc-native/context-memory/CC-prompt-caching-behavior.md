---
title: CC Prompt Caching Behavior — Server-Side Mechanism and Session Economics
purpose: How Anthropic's server-side prompt caching works in CC sessions — what's cached, matching, TTL, hit rates, and cost impact.
created: 2026-03-27
updated: 2026-10-26
validated_links: 2026-10-26
status: adopt
---

## What It Is

Anthropic's [prompt caching][caching] is a server-side optimization that caches the **input prefix** of API requests. In CC sessions, this means the entire conversation history (system prompt, prior messages, tool results) is cached and reused across turns. CC requests either a 5-minute or 1-hour TTL per request, chosen by request type and by how you're billed — see [TTL varies by request bucket and billing method](#ttl-varies-by-request-bucket-and-billing-method) below.

## What Gets Cached

The cache covers the full input prefix of each API request, not just the user prompt.

### Cacheable content

| Content | Location in request | Cacheable? |
|---|---|---|
| Tool definitions | `tools` array | Yes |
| System prompt (CLAUDE.md, rules, skills) | `system` messages | Yes |
| User messages | `messages.content` (user turns) | Yes |
| Assistant responses | `messages.content` (assistant turns) | Yes |
| `tool_use` blocks | `messages.content` (assistant turns) | Yes |
| `tool_result` blocks | `messages.content` (user turns) | Yes |
| Images and documents | `messages.content` (user turns) | Yes |
| Thinking blocks | Cached as part of prior assistant turns | Yes (indirectly) |

### Not cached

- **Output generation** — responses are always computed fresh. From the [caching docs][caching]: *"Prompt caching has no effect on output token generation."*
- Thinking blocks cannot have `cache_control` directly
- Empty text blocks, sub-content blocks like citations

Source: [prompt caching docs][caching], "What can be cached" section

## Cache Matching Mechanism

**Exact prefix matching** via cumulative hash — not semantic similarity.

From the [caching docs][caching]:

> *"Cache hits require 100% identical prompt segments, including all text and images up to and including the block marked with cache control."*

### How it works in CC sessions

1. CC places `cache_control: {"type": "ephemeral"}` on the request
2. The server hashes the prefix up to the breakpoint
3. If a matching hash exists from a prior request within the TTL → **cache hit** — 0.025x input price on Claude Fable 5.1/Mythos 5.1, 0.05x on Claude Opus 5.5/Sonnet 5.5, and the standard 0.1x on every other model ([pricing docs][pricing], accessed 2026-10-26)
4. If no match → **cache miss** → full processing + cache write (1.25x input price for 5m)

### 20-block lookback window

The server checks at most 20 block positions backward from the breakpoint. If the prior cache entry is beyond 20 blocks back, it's a miss even if the prefix is identical. The [prompt caching docs][caching] additionally describe a run of consecutive `tool_use` blocks, and separately a run of consecutive `tool_result` blocks, as each counting toward that limit as a single position — so a turn with many parallel tool calls would not by itself push the previous request's cache entry outside the window. *(This additional detail reflects a model-mediated extraction of the page made in this session, not raw page text read directly — re-confirm the exact mechanism before treating it as settled.)*

Source: [prompt caching docs][caching], "How cache lookback works" section

### Minimum cacheable prefix

The cacheable prefix is model-dependent (re-verified against the [caching docs][caching], 2026-10-15). On the Claude API, Claude Platform on AWS, Google Cloud, and Microsoft Foundry:

| Minimum tokens | Models |
|---|---|
| 512 | Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5, Opus 5, Sonnet 5.5, Haiku 5.5 |
| 1,024 | Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5 (deprecated) |
| 2,048 | Opus 4.7, Mythos Preview |
| 4,096 | Opus 4.6, Opus 4.5, Haiku 4.5 |

A prefix shorter than the minimum silently skips caching: no error, just `cache_creation_input_tokens: 0`. The [caching docs][caching] state "these minimums apply on every platform where each model is available," but that sentence's scope is the four platforms named in its own lead-in (Claude API, Claude Platform on AWS, Google Cloud, Microsoft Foundry) — it does not cover Bedrock, which the same docs point elsewhere for: [AWS's own Bedrock documentation][bedrock-caching]. (A 2026-10-26 check via model-mediated extraction of the page — not raw text — did not surface a change to this sentence; treat that check as a lead, not a re-confirmation at the same standard as the other re-verified facts in this doc.)

**Corrected 2026-10-15**: this doc previously claimed Bedrock uses a different (1,024-token) minimum for Fable 5 / Mythos 5. [AWS's Bedrock prompt-caching docs][bedrock-caching] (its "Supported models, Regions, and explicit caching limits" table) list Claude Fable 5.1, Mythos 5.1, Fable 5, and Mythos 5 — along with Opus 5.5/5, Sonnet 5.5, and Haiku 5.5 — at a 512-token minimum per cache checkpoint on Bedrock too, the same figure as the other platforms. (Bedrock's 1,024-token minimum applies to Opus 4.8 and Sonnet 5/4.6/4.5/3.7/3.5v2, not to Fable/Mythos.) Removed the stale claim on that basis.

Source: [prompt caching docs][caching], "Cache limitations" section; [AWS Bedrock prompt-caching docs][bedrock-caching], "Supported models, Regions, and explicit caching limits" table (accessed 2026-10-15)

### Breakpoints, TTL lifetime, and other platform facts

Re-verified against the [prompt caching docs][caching] (accessed 2026-10-26). The first group below was read directly from fetched page text. The second group was obtained only via a model-mediated extraction of the page (direct network fetch was unavailable in this session) and is paraphrased rather than quoted for that reason — re-confirm against raw text before quoting it directly.

**Read directly from page text:**

- **Up to 4 cache breakpoints**: "You can define up to 4 cache breakpoints (using `cache_control` parameters) in your prompt."
- **Lifetime is measured from request start, not response end**: the TTL clock starts "from the start of the request that writes or reads the cache entry, not from the end of its response," so time spent generating a long response eats into the window available for a follow-up request to hit the cache.
- **ZDR-eligible**: "Prompt caching (both automatic and explicit) is ZDR eligible. Anthropic does not store the raw text of your prompts or Claude's responses."
- **No manual clear**: "Currently, there's no way to manually clear the cache. Cached prefixes automatically expire after a minimum of 5 minutes of inactivity."
- **Caching + Batches API is best-effort**: "it is possible to use prompt caching with your Batches API requests. However, because asynchronous batch requests can be processed concurrently and in any order, cache hits are provided on a best-effort basis." See also [CC-session-cost-analysis.md § Message Batches API](../sessions/CC-session-cost-analysis.md#message-batches-api) for the batch-pricing side of this.

**Extraction-only — re-confirm before quoting:**

- Automatic caching is reported to use one of the 4 available breakpoint slots when combined with explicit breakpoints, leaving at most 3 slots for explicit ones.
- Mixing TTLs is reported to require an ordering: a 1-hour cache entry must appear before any 5-minute cache entries in the same request.
- The docs reportedly give improved rate-limit utilization — because cache hits aren't deducted against the rate limit — as a reason to use the 1-hour cache; the sentence appears to describe cache hits generally, not something unique to the 1-hour tier.

Source: [prompt caching docs][caching], "How many cache breakpoints can I use?", "When does the cache lifetime start?", "Can I manually clear the cache?", "Can I use prompt caching with the Batches API?", and "Data retention" FAQ/body sections, read directly (accessed 2026-10-26); automatic-caching slot usage, TTL ordering, and the rate-limit sentence via model-mediated extraction, not raw text (accessed 2026-10-26)

## CC-Specific Caching Behavior

### TTL varies by request bucket and billing method

**Corrected 2026-10-15** — this doc previously claimed CC uses the 5-minute ephemeral cache exclusively and never the 1-hour tier. That matched the session analyzed below (CC 2.1.83, 2026-03-27) but is not CC's current behavior. Per the [CC prompt-caching docs][cc-caching] (choosing a TTL yourself requires CC v2.1.242+), CC decides the TTL per request and buckets every request into one of two groups:

- **Main conversation**: interactive turns, non-interactive `-p` runs, Agent SDK turns, and the helpers CC runs inline with them.
- **Everything else**: subagents, workflows, in-process teammates, forks, compaction, and session titles.

Unless you choose a TTL yourself, CC requests the **one-hour TTL only on a Claude subscription within your plan's included usage** — and only for the main conversation, plus a small set of server-controlled helper requests. Once a session draws on usage credits, CC drops the main conversation to the five-minute TTL (which bills cache writes at the lower rate).

| Request bucket | Claude subscription, within plan usage | Usage credits, API key, or cloud provider |
|---|---|---|
| Main conversation | One hour | Five minutes |
| Everything else | Five minutes (server-controlled helper requests get one hour) | Five minutes |

Source: [CC prompt-caching docs][cc-caching], "Which TTL each request gets" section

#### Choose the TTL yourself

Each control takes `5m` or `1h` only; CC ignores any other value. Both settings and both env vars require **CC v2.1.242+**:

| Bucket | Setting | Env var |
|---|---|---|
| Main conversation | [`promptCacheTtl`][settings-ref] | `CLAUDE_CODE_PROMPT_CACHE_TTL` |
| Everything else | [`subagentPromptCacheTtl`][settings-ref] | `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` (also settable per-subagent via its `experimental.cacheTtl` frontmatter field, CC v2.1.248+) |

Precedence when more than one control applies (highest first):

1. `FORCE_PROMPT_CACHING_5M=1` — forces 5m for **both** buckets, overriding every control below
2. The bucket's env var (`CLAUDE_CODE_PROMPT_CACHE_TTL` / `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`)
3. The bucket's setting (`promptCacheTtl` / `subagentPromptCacheTtl`)
4. A subagent's `experimental.cacheTtl` frontmatter field (CC v2.1.248+; CC ignores a `1h` value there while the subscription is drawing on usage credits)
5. `ENABLE_PROMPT_CACHING_1H=1` — requests 1h for **both** buckets
6. The bucket's default from the table above

To confirm which TTL a run actually used: `claude -p "hello" --output-format json` and read `usage.cache_creation` — 1-hour cache writes are reported under `ephemeral_1h_input_tokens`, 5-minute writes under `ephemeral_5m_input_tokens`.

Source: [CC prompt-caching docs][cc-caching], "Choose the TTL yourself" section; [CC env vars reference][cc-env-vars] (`CLAUDE_CODE_PROMPT_CACHE_TTL`, `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`, `FORCE_PROMPT_CACHING_5M`, `ENABLE_PROMPT_CACHING_1H`)

#### Disable prompt caching

| Variable | Effect |
|---|---|
| `DISABLE_PROMPT_CACHING` | Disable for all models (takes precedence over the per-model variables below) |
| `DISABLE_PROMPT_CACHING_HAIKU` | Disable for the default Haiku model, wherever it runs (CC v2.1.283+ to also cover the main conversation when Haiku is the main model) |
| `DISABLE_PROMPT_CACHING_SONNET` | Disable for the default Sonnet model |
| `DISABLE_PROMPT_CACHING_OPUS` | Disable for the default Opus model |
| `DISABLE_PROMPT_CACHING_FABLE` | Disable for Fable models |

Source: [CC prompt-caching docs][cc-caching], "Disable prompt caching" section

### Evidence from one session predating the TTL-bucket model

Session `9f7de296`, CC 2.1.83, Codespaces, 2026-03-27 — 281 turns, all cache writes landed in `ephemeral_5m_input_tokens` (1,732,355 tokens), none in `ephemeral_1h_input_tokens`:

- `ephemeral_5m_input_tokens`: 1,732,355 (all cache writes)
- `ephemeral_1h_input_tokens`: 0

CC 2.1.83 predates the v2.1.242 TTL-selection controls above, so this observation reflects the 5-minute-only behavior of that era, not necessarily today's default — which can request the one-hour TTL automatically on a Claude subscription within plan usage (see the table above). The warmup curve and cost figures below are from this same session and carry the same caveat.

### TTL refresh on hit

Each cache hit resets the active TTL's timer at no additional cost, whichever TTL is in effect. From the [caching docs][caching]: *"The cache is refreshed for no additional cost each time the cached content is used."* The CC-specific docs state the same for its longer TTL: *"Each request that hits the cache resets the timer, so the cache stays warm as long as you keep working."*

This means active sessions keep the cache warm indefinitely — each turn resets the clock.

### Cache warmup curve

Observed in session `9f7de296` (CC 2.1.83, 281 turns):

| Turn | Cache read | Cache create | Hit % |
|---|---|---|---|
| 1 | 0 | 30,043 | 0% |
| 2 | 6,981 | 23,329 | 23% |
| 5 | 34,650 | 137 | 99.6% |
| 50 | 74,964 | 1,458 | 98.1% |
| 100 | 161,921 | 63 | 100% |
| 200 | 224,258 | 168 | 99.9% |
| 281 | 253,289 | 1,496 | 99.4% |

Cache warms in ~5 turns. After turn 5, hit rate is consistently 98%+. Small cache writes on later turns are from new content added to the prefix (tool results, new messages).

### Session cost impact

Same session (281 turns, Opus 4.6):

| Metric | Value |
|---|---|
| Overall hit rate | 96.3% |
| Total cache read | 45.7M tokens |
| Total cache create | 1.7M tokens |
| Actual session cost | $35.52 |
| Hypothetical cost without caching (all at base input) | $242.49 |
| **Savings** | **$206.97 (85%)** |

Pricing: input $5/MTok, output $25/MTok, 5m cache write $6.25/MTok (1.25x), cache read $0.50/MTok (0.1x). Source: [pricing docs][pricing], accessed 2026-03-27.

## Why Hit Rates Are So High in CC

In a CC session, the input to each API call is:

```text
[tools] + [system prompt] + [message 1] + [response 1] + [tool_use 1] + [tool_result 1] + ... + [new user message]
```

Everything except the new user message is identical to the prior call's prefix. Since tool results and assistant responses are part of the cached prefix, only the delta (new message + its tool results) triggers cache writes. The growing prefix stays cached.

This is a simplification: several mid-session actions invalidate part or all of the cache even without a new message. See the next section for what actually breaks it.

## Actions That Invalidate vs. Keep the Cache

Per the [CC prompt-caching docs][cc-caching], each of these actions costs one slower/pricier turn while the prefix rebuilds:

**Invalidates** (abridged — see source for the full mechanism per item): switching models (`/model`), including the `opusplan` setting's Opus↔Sonnet toggle between plan mode and execution; changing effort level mid-session (except on Opus 5.5/Sonnet 5.5/Haiku 5.5/Fable 5.1 with an API key or Claude subscription); turning on fast mode for the first time in a conversation; connecting or removing an MCP server, or enabling/disabling a plugin that provides one, when MCP tool search isn't deferring tool definitions; denying a whole tool when tool search is unavailable or disabled; compacting the conversation (`/compact`); accumulating enough images/PDFs to evict a batch; and upgrading the CC binary.

**Keeps the cache**: editing files in the repo; editing CLAUDE.md mid-session (the edit also doesn't apply until `/clear`, `/compact`, or a restart); changing permission mode; changing output style; invoking skills and commands; `/recap`; `/rewind`; and spawning a subagent — the subagent starts its own fresh cache (its first request can't read the parent's), and the parent's prefix is left untouched by the call and its result.

Source: [CC prompt-caching docs][cc-caching], "Actions that invalidate the cache" / "Actions that keep the cache" sections

### API-level invalidation (platform docs)

The list above is CC's own framing. The underlying [prompt caching docs][caching] also document cache invalidation one level down, at the Messages API, in a "What invalidates the cache" table. **Sourcing note**: direct network fetch of this page was unavailable in this session; the table's content below was obtained via a model-mediated extraction (WebFetch) rather than read as raw page text, so it is paraphrased rather than quoted and should be re-confirmed against raw text before being cited as a direct quote:

- **Tool definitions**: modifying tool definitions (names, descriptions, parameters) is reported to invalidate the entire cache.
- **Web search toggle**: enabling/disabling web search modifies the system prompt.
- **Citations toggle**: enabling/disabling citations modifies the system prompt.
- **Speed setting**: switching between `speed: "fast"` and standard speed is reported to invalidate system and message caches.
- **Tool choice**: changes to the `tool_choice` parameter are reported to affect only message blocks.
- **Images**: adding/removing images anywhere in the prompt is reported to affect message blocks.
- **Thinking parameters**: the thinking configuration (mode, and `budget_tokens` in extended mode) is rendered into the prompt, so changing it is reported to always invalidate message blocks, and can also invalidate tool/system caches on models that render the configuration ahead of them.
- **Effort setting**: changing `output_config.effort` is reported to always invalidate message blocks, with the same model-specific effect on tool/system caches as thinking parameters; setting it explicitly to the model's default reportedly does not invalidate; on models that support per-message effort, an effort change carried in a per-message `role: "system"` entry reportedly leaves the cached prefix intact.
- **Non-tool results passed to requests with thinking**: on Opus 4.5+, Sonnet 4.6+, and Haiku 5.5, thinking blocks are reportedly preserved by default so the cache stays valid; on earlier Opus/Sonnet models and Haiku through 4.5, previously-cached thinking blocks (and anything cached after them) are reportedly stripped.
- **Dropped thinking blocks**: on Fable 5.1, Mythos 5.1, Opus 5.5, Sonnet 5.5, or Haiku 5.5, if the API drops a thinking block that isn't preserved on that request, the cached prefix is reported to change from that block's position onward on that request; blocks the receiving model can read and pass back unchanged reportedly keep the cache intact.

**Conflict — recorded, not resolved:** the effort-setting row above is reported to state that changing `output_config.effort` always invalidates message blocks ([prompt caching docs][caching], "What invalidates the cache" section — extraction-only, see sourcing note above, accessed 2026-10-26). The CC-specific list in the parent section instead states that CC's own effort-level changes mid-session do **not** invalidate "on Opus 5.5/Sonnet 5.5/Haiku 5.5/Fable 5.1 with an API key or Claude subscription" ([CC prompt-caching docs][cc-caching], "Actions that invalidate the cache" section, accessed 2026-10-15 — this claim predates this session and is unaffected by the sourcing note above). Both are first-party Anthropic sources, from different doc families (platform.claude.com vs. code.claude.com) and different access dates. This doc keeps both claims rather than picking one or resolving the discrepancy.

Source: [prompt caching docs][caching], "What invalidates the cache" section — content obtained via model-mediated extraction, not raw text (accessed 2026-10-26); treat as a lead to re-confirm, not a settled quote

## Cache Scope

In CC, the cache is effectively scoped to one machine and directory — the system prompt embeds auto-memory paths, and the conversation opens with an announcement of the working directory, platform, shell, and OS version. Two sessions in different directories therefore build different prefixes and miss each other's cache. Sessions run in **parallel** in the *same* directory build matching prefixes and read each other's cache; **sequential** sessions in the same directory share the prefix only when the git status snapshot taken at startup matches, since each conversation also carries the branch and recent commits from that snapshot.

The underlying API cache is broader than CC's own scoping. The sentence this doc previously quoted here is no longer verbatim against the current prompt caching docs. Requoted 2026-10-26 from the FAQ "How does prompt caching handle privacy and data separation?" (read directly from fetched page text, not a model-mediated extraction): "On the Claude API, Claude Platform on AWS, and Microsoft Foundry, caches are isolated by workspace within an organization. On Bedrock and Claude Models on Google Cloud (Google managed), caches are isolated by organization. In every case, caches are never shared across organizations, even for identical prompts." The "(Google managed)" qualifier implies a split within "Google Cloud": the Google-managed surface gets organization-level isolation (grouped with Bedrock), while **Claude Models on Google Cloud (Anthropic managed) is not named in either list** — it most plausibly falls under the first (workspace-level) group by the same logic as Claude Platform on AWS, but the docs don't say so explicitly, so treat that specific inference as unverified. (code.claude.com elsewhere calls this same Google product "Google Cloud's Agent Platform" — same product, different doc family's naming.)

Source: [CC prompt-caching docs][cc-caching], "Cache scope" section; [prompt caching docs][caching], FAQ "How does prompt caching handle privacy and data separation?" section (read directly, accessed 2026-10-26)

## Slug (CC-Internal)

"Slug" is **not an Anthropic API concept**. It does not appear in the [API docs][api], [prompt caching docs][caching], or any platform documentation.

Slug is a CC-internal auto-generated session display name (e.g., `stateful-dreaming-donut`) carried on every message in session JSONL files. See [CC-session-lifecycle-analysis.md](../sessions/CC-session-lifecycle-analysis.md) for slug behavior and `/rename` bugs.

## Cross-References

- [CC-session-cost-analysis.md](../sessions/CC-session-cost-analysis.md) — JSONL cache fields, jq cost recipes
- [CC-extended-context-analysis.md](CC-extended-context-analysis.md) — Context window management
- [CC-session-lifecycle-analysis.md](../sessions/CC-session-lifecycle-analysis.md) — Session naming, slug, `/rename`

## Related

This doc is the **CC client / session-economics** view of Anthropic prompt caching. For the
cross-vendor prompt-caching comparison (OpenAI, Gemini) and the underlying serving-engine KV-cache
internals (PagedAttention, RadixAttention, quantization, offload/disaggregation), see
[kv-cache-serving-landscape.md](../../non-cc/infrastructure/kv-cache-serving-landscape.md). For the KV-cache
invalidation gotcha on self-hosted backends (`CLAUDE_CODE_ATTRIBUTION_HEADER=0`), see
[CC-model-provider-configuration.md](../configuration/CC-model-provider-configuration.md).

## Sources

| Source | Content |
|---|---|
| [Prompt caching docs][caching] | What's cached, prefix matching, breakpoints, TTL, minimum cacheable prefix per model, cache isolation, lifetime start, manual clear, ZDR, Batches interaction — read directly from fetched page text (re-verified 2026-10-26); the "What invalidates the cache" table and a few other items noted inline were obtained via model-mediated extraction only, not raw text, and are flagged as such in the body |
| [Pricing docs][pricing] | Per-model cache write/read rates, including the 0.025x/0.05x/0.1x cache-hit multiplier tiers (accessed 2026-10-26) |
| [API messages docs][api] | Usage object fields (`cache_read_input_tokens`, `cache_creation_input_tokens`) |
| [CC prompt-caching docs][cc-caching] | CC-specific TTL buckets, choose-the-TTL precedence, disable vars, cache scope, actions that invalidate/keep the cache (accessed 2026-10-15) |
| [CC env vars reference][cc-env-vars] | `CLAUDE_CODE_PROMPT_CACHE_TTL`, `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`, `FORCE_PROMPT_CACHING_5M`, `ENABLE_PROMPT_CACHING_1H`, `DISABLE_PROMPT_CACHING*` (accessed 2026-10-15) |
| CC 2.1.83, session `9f7de296`, Codespaces, 2026-03-27 | Cache warmup curve, 96.3% hit rate — predates the TTL-bucket model (CC v2.1.242+) described above |
| [AWS Bedrock prompt-caching docs][bedrock-caching] | Per-model minimum cacheable prefix on Bedrock specifically (Fable/Mythos 5.x = 512 tokens, same as other platforms) (accessed 2026-10-15) |

[caching]: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[pricing]: https://platform.claude.com/docs/en/about-claude/pricing
[api]: https://platform.claude.com/docs/en/api/messages
[cc-caching]: https://code.claude.com/docs/en/prompt-caching
[cc-env-vars]: https://code.claude.com/docs/en/env-vars
[settings-ref]: https://code.claude.com/docs/en/settings-reference
[bedrock-caching]: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
