---
title: CC Prompt Caching Behavior — Server-Side Mechanism and Session Economics
purpose: How Anthropic's server-side prompt caching works in CC sessions — what's cached, matching, TTL, hit rates, and cost impact.
created: 2026-03-27
updated: 2026-11-25
validated_links_on: 2026-11-09
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
3. If a matching hash exists from a prior request within the TTL → **cache hit** — 0.025x input price on Claude Fable 5.2/Mythos 5.2 and Fable 5.1/Mythos 5.1, 0.05x on Claude Opus 5.5/Sonnet 5.5, and the standard 0.1x on every other model ([pricing docs][pricing], accessed 2026-10-26)
4. If no match → **cache miss** → full processing + cache write (1.25x input price for 5m)

### 20-block lookback window

The server checks at most 20 block positions backward from the breakpoint. If the prior cache entry is beyond 20 blocks back, it's a miss even if the prefix is identical. Parallel tool calls don't exhaust the window: "On the Claude API, a run of consecutive `tool_use` blocks counts as one position, and so does a run of consecutive `tool_result` blocks, so a turn with many parallel tool calls doesn't push the previous request's entry out of the window on its own."

Source: [prompt caching docs][caching], "How automatic prefix checking works" section (accessed 2026-10-26)

### Minimum cacheable prefix

The cacheable prefix is model-dependent (re-verified against the [caching docs][caching], 2026-10-15; Fable 5.2 and Mythos 5.2 added to the 512-token row after re-reading the page on 2026-11-23). On the Claude API, Claude Platform on AWS, Google Cloud, and Microsoft Foundry:

| Minimum tokens | Models |
|---|---|
| 512 | Fable 5.2, Mythos 5.2, Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5, Opus 5, Sonnet 5.5, Haiku 5.5 |
| 1,024 | Opus 4.8, Sonnet 5, Sonnet 4.6, Sonnet 4.5 (deprecated) |
| 2,048 | Opus 4.7, Mythos Preview |
| 4,096 | Opus 4.6, Opus 4.5, Haiku 4.5 |

A prefix shorter than the minimum silently skips caching: no error, just `cache_creation_input_tokens: 0`. The [caching docs][caching] state "these minimums apply on every platform where each model is available," but that sentence's scope is the four platforms named in its own lead-in (Claude API, Claude Platform on AWS, Google Cloud, Microsoft Foundry) — it does not cover Bedrock, which the same docs point elsewhere for: [AWS's own Bedrock documentation][bedrock-caching] (sentence verified 2026-10-15).

**Corrected 2026-10-15**: this doc previously claimed Bedrock uses a different (1,024-token) minimum for Fable 5 / Mythos 5. [AWS's Bedrock prompt-caching docs][bedrock-caching] (its "Supported models, Regions, and explicit caching limits" table) list Claude Fable 5.1, Mythos 5.1, Fable 5, and Mythos 5 — along with Opus 5.5/5, Sonnet 5.5, and Haiku 5.5 — at a 512-token minimum per cache checkpoint on Bedrock too, the same figure as the other platforms. (Bedrock's 1,024-token minimum applies to Opus 4.8 and Sonnet 5/4.6/4.5/3.7/3.5v2, not to Fable/Mythos.) Removed the stale claim on that basis.

Source: [prompt caching docs][caching], "Cache limitations" section; [AWS Bedrock prompt-caching docs][bedrock-caching], "Supported models, Regions, and explicit caching limits" table (accessed 2026-10-15)

### Breakpoints, TTL lifetime, and other platform facts

From the [prompt caching docs][caching] (raw page text, accessed 2026-10-26):

- **Up to 4 cache breakpoints**: "You can define up to 4 cache breakpoints (using `cache_control` parameters) in your prompt." Automatic caching takes one of them: "When used together, the automatic cache breakpoint uses one of the 4 available breakpoint slots."; with 4 explicit breakpoints already set "the API returns a 400 error (no slots left for automatic caching)."
- **TTL ordering**: "Cache entries with longer TTL must appear before shorter TTLs (that is, a 1-hour cache entry must appear before any 5-minute cache entries)."
- **Rate limits**: listed as a reason to use the 1-hour cache — "cache hits are not deducted against your rate limit" (a property of cache hits in general, not only the 1-hour tier).
- **Lifetime is measured from request start, not response end**: the TTL clock starts "from the start of the request that writes or reads the cache entry, not from the end of its response," so time spent generating a long response eats into the window available for a follow-up request to hit the cache.
- **ZDR-eligible**: "Prompt caching (both automatic and explicit) is ZDR eligible. Anthropic does not store the raw text of your prompts or Claude's responses."
- **No manual clear**: "Currently, there's no way to manually clear the cache. Cached prefixes automatically expire after a minimum of 5 minutes of inactivity."
- **Caching + Batches API is best-effort**: "it is possible to use prompt caching with your Batches API requests. However, because asynchronous batch requests can be processed concurrently and in any order, cache hits are provided on a best-effort basis." See also [CC-session-cost-analysis.md § Message Batches API](../sessions/CC-session-cost-analysis.md#message-batches-api) for the batch-pricing side of this.

Source: [prompt caching docs][caching], "Combining with block-level caching", "Mixing different TTLs", "When to use the 1-hour cache", "Data retention" and FAQ sections (accessed 2026-10-26)

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

### Idle compaction (before the cache expires)

The other side of the TTL: a session you step away from loses its cache, and the next message would reprocess the whole prefix at full input price. Since v2.1.299 Claude Code compacts such a session first. The [changelog][cc-changelog] entry: "a 200K+ token conversation left idle for about 54 minutes is compacted before its one-hour prompt cache expires, so your next message doesn't reprocess it all." The terminal then shows a notice such as "Compacted while idle, before the prompt cache expired · turn off with "idleCompaction": false in settings.json" (owner observation, 2026-11-09).

- **Setting:** `idleCompaction` in any settings file, default `true`. Per the [settings reference][settings-ref]: "Idle compaction compacts a long conversation that you've stepped away from. Your next message then sends a summary instead of the whole conversation." The key "requires Claude Code v2.1.290 or later. On an earlier version, which ignores this key, turn off `autoCompactEnabled` to stop idle compaction."
- **Threshold:** `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS` changes the 200K-token minimum (changelog, 2.1.299).
- **Idle time, two wordings:** the [changelog][cc-changelog] (2.1.299, read 2026-11-09) says "about 54 minutes"; the [settings reference][settings-ref] (read 2026-11-25) lists the condition "about an hour has passed since the last request, and your computer stays awake until then". Both say "about", neither gives an exact trigger; the two are consistent with a check shortly before the one-hour lifetime ends (inference, not documented). The settings reference also requires the conversation to be on the one-hour TTL, auto-compaction to be on, and an interactive terminal, the VS Code chat panel, or the desktop Code tab running on your machine or over SSH.
- **Resume and compaction:** the [sessions page][cc-sessions] (read 2026-11-25) says a resumed session restores the history up to the last compaction. It describes no compaction step on resume; that resuming doesn't compact is our reading of the page, not a stated rule. Compaction on a resumed old session is something you trigger or auto-compact triggers, and the [Claude Code caching page][cc-caching] says `/compact` "costs the most" there because the summarization request reprocesses the history uncached.
- **Needs a running session:** idle compaction runs inside the Claude Code process of the open session. When the host is stopped (a container or dev container, a VM, a desktop app, a CI runner, a serverless function scaled to zero), nothing runs, so it cannot fire; the cache then expires unseen and the next request pays a full rewrite. The settings reference's "your computer stays awake" condition points the same way (documented condition; the consequence for stopped hosts is our inference).
- **Where it runs:** terminal from 2.1.299; `/config` gained an "Idle compaction" toggle in 2.1.302; 2.1.314 added it to VS Code and Claude Desktop's Code tab (there, "the summary is used on your next message if the prompt cache has expired") and extended it to "subscribers with telemetry turned off, and on Bedrock, Vertex, Foundry and LLM gateways once the one-hour prompt cache is on"; 2.1.318 "Fixed idle compaction replacing a conversation with a reply that was not a summary."
- **Trade-off:** the next turn is cheaper (a summary instead of a full cache rebuild of 200K+ tokens), but it continues from a summary, so detail from the conversation can be lost exactly as with `/compact`. Turn it off for sessions where you need the full transcript after a break, and see [CC-extended-context-analysis.md](CC-extended-context-analysis.md) for compaction in general.

### One week of sessions on one machine (2026-11-07 to 2026-11-14)

A measurement of the owner's own transcripts, to size what idle gaps cost in practice. Scope: every
transcript under `~/.claude/projects/` on one Codespace, CC 2.1.319 to 2.1.325, Claude subscription.
Method: one row per API request (deduplicated on message ID and request ID), reading the `usage`
fields described in [CC-session-cost-analysis.md](../sessions/CC-session-cost-analysis.md). An
"idle rewrite" is a request that follows a gap of more than one hour in the same transcript and
writes more than 20,000 tokens to the cache.

| Metric | Main conversations (51 transcripts) | Including subagent transcripts (453) |
|---|---|---|
| Requests | 14,026 | 25,059 |
| Cache reads | 4,718M tokens (98.6% of input tokens) | 6,289M tokens |
| Cache writes | 65.4M tokens, all at the one-hour TTL | 114.0M tokens |
| Mean cache read per request | 336k tokens | 251k tokens |
| Idle rewrites | 109, totalling 34.1M tokens (52% of cache writes) | 113, totalling 34.5M tokens (30%) |
| Size of an idle rewrite | median 237k, largest 920k tokens; 87 of 109 were 100k tokens or more | — |

Read it as one user's working pattern, not a benchmark:

- Uncached input was negligible (about 0.03M tokens). Nearly every input token was a cache read or a
  cache write, so cost tracks the size of the context carried on each request.
- A cache write is billed at a higher multiple of base input than a cache read ([pricing docs][pricing]),
  so idle rewrites weigh more in cost than their token share suggests.
- Most idle rewrites were full-context rebuilds (100k tokens or more), not just the base context. Idle
  compaction above did not prevent them; this measurement does not show why (a conversation under its
  200K-token minimum, a resumed session, or another cause).
- Levers, from this doc and [CC-extended-context-analysis.md](CC-extended-context-analysis.md): `/clear`
  or `/compact` before stepping away from a long session, start a new session after a long break rather
  than resuming a large one, and run fewer long-lived sessions in parallel.

**Reproduce it.** [`scripts/cc_cache_usage.py`](../../../scripts/cc_cache_usage.py) (stdlib, unit-tested)
applies this method to one session: `python3 scripts/cc_cache_usage.py <transcript.jsonl> [gap_min]
[ttl_min]`, where the transcript is a `<session-id>.jsonl` under `~/.claude/projects/<project>/`. It
prints the input split (cache reads, cache writes by 5-minute and 1-hour lifetime, uncached), output
tokens, the turns after an idle gap longer than `gap_min` (default 60) with their cache write and read,
the share of writes after gaps, a hit/miss prediction (a miss when the gap since the previous response
exceeds the cache lifetime, which defaults to 5 or 60 minutes from the session's write buckets) checked
against the outcome, and the compaction markers. A turn counts as a miss when it writes again part of
what the previous turn had cached, that is, when it reads less than the previous turn read and wrote;
a turn that reads the whole cached prefix and writes a large new suffix is a hit. The rule follows the
rebuilt-token ledger of [cachemiss][cachemiss] (source read, not run, 2026-11-25). On the session in the
second data point below it counts 14 misses in 1,826 turns, where the earlier rule "writes more than
it reads" counted 11. The script dedupes on message ID only (keeping the last streamed chunk) and skips
subagent sidechains, so its counts can differ slightly from the week's table, which also deduped on
request ID. Run it on your own transcripts before relying on these shares.

### Second data point: one long session (2026-11-22 to 2026-11-25)

A second own measurement, read from one session's transcript with the method above (main thread only, one
machine, n=1; not a benchmark). Observed on 2026-11-25:

| Metric | Value |
|---|---|
| Main-thread responses | 1,706 |
| Input tokens served as cache reads | 99.2% (472M tokens) |
| Cache writes | 0.8% (3.7M tokens), all at the one-hour lifetime |
| Writes after idle gaps over 60 minutes | 33% of writes: 4 gaps of 2 to 17 hours rewrote 110K to 435K tokens each |
| Compactions | 5, all `trigger: "auto"` at 469K to 492K tokens, down to 15K to 27K tokens |

- Idle compaction did not fire before those gaps. The cause is **unverified**; the likely one is that the Claude
  Code process was not running while its host was stopped (see [Stopped host](#stopped-host-options)).
- Subagent turns are sidechains with their own cache and do not warm the main thread's ([CC caching docs][cc-caching],
  "Subagents and the cache").
- Both measurements (one machine each, so n=1 apiece) show the same pattern (a very high read share, with a large part of the writes coming from
  rebuilds after long gaps). They differ in the share (52% of writes in the week, 33% here), so read the share as
  workload-dependent.

### Cost levers and their evidence

Three levers follow from the mechanics above: keep the context smaller, keep the prompt start stable, and do not
idle past the cache lifetime. Each is stated at its own evidence level; none of the studies below measures Claude
Code itself.

| Lever | Evidence | Level |
|---|---|---|
| Keep the context smaller | Across agentic coding runs, "input tokens rather than output tokens" drive the overall cost, and runs on the same task "can differ by up to 30x in total tokens" ([arXiv 2604.22750][p-spend], v3 2026-10-02, preprint). Replacing old tool observations with placeholders "halves cost relative to the raw agent" and matches LLM summarization's solve rate on SWE-agent ([arXiv 2508.21433][p-complexity], preprint, 2025-08-29; the abstract does not mention caching, so the saving is not shown net of cache effects). Cost differences between harnesses "from under 10% to 3 to 4 times" depending on the model ([arXiv 2610.04433][p-harness-tokens], preprint, 2026-10-03). | Papers (preprints) |
| Smaller context also helps quality | Performance "grows increasingly unreliable as input length grows" across 18 models ([Chroma, Context Rot][chroma-rot], 2025-07-14, practitioner report with code); performance "significantly degrades" for information in the middle of long inputs ([arXiv 2307.03172][p-lost-middle], 2023, older models). Anthropic reports context editing +29% and +39% with the memory tool on "an internal evaluation set for agentic search", and an 84% token cut in a 100-turn web-search eval, with no eval size or baseline given ([Anthropic, context management][anth-context-mgmt], 2025-09-29). | Paper, practitioner, vendor claim (internal eval) |
| Keep the prompt start stable | A hit needs 100% identical prompt segments up to the breakpoint, in the order tools, system, messages ([prompt caching docs][caching], read 2026-11-25). Across three providers, caching cut API cost 41-80% and time to first token 13-31% on long agentic tasks ([arXiv 2601.06007][p-dontbreak], abstract, 2026-01; which caching placement works best is not taken from the abstract and is **unverified** here). Manus calls the KV-cache hit rate "the single most important metric" for a production agent, cites an input-to-output ratio of "around 100:1" and 0.30 against 3 USD/MTok cached against uncached on Claude Sonnet (as of its 2025 post), and advises against a second-precise timestamp at the start of the system prompt and for append-only context ([Manus][manus-ctx], practitioner). | Vendor doc, paper (preprint), practitioner |
| Do not idle past the cache lifetime | The lifetime is measured from the start of the request that wrote or read the entry ([prompt caching docs][caching], read 2026-11-25); in Claude Code the main conversation gets one hour only on a subscription within plan usage, five minutes otherwise ([above](#ttl-varies-by-request-bucket-and-billing-method)). The two own measurements in this doc show rebuilds after long gaps at 52% (week) and 33% (one session) of cache writes. No independent measurement of cold-cache cost after idle gaps was found. | Vendor doc, own measurement (n=1 each) |

What is not shown: no study found compares compaction with an append-only, cache-preserving history on total
cost, so "smaller is cheaper" is not shown net of the cache rebuild a compaction causes (the Claude Code caching
page says compaction invalidates the conversation layer, then the next turn rebuilds the cache for only the shorter
history). For cross-vendor caching rules (OpenAI, Gemini) and serving-engine internals, see
[kv-cache-serving-landscape.md](../../non-cc/infrastructure/kv-cache-serving-landscape.md).

### Stopped host options

When the host is stopped, nothing sends requests and the in-session idle compaction cannot run
([Idle compaction](#idle-compaction-before-the-cache-expires)). Options, none of which is Claude Code behaviour
documented as a feature:

- **Compact before the stop (untested):** a stop hook or a watchdog on the host could run a headless
  `claude -p --resume <session-id> "/compact"` while the cache is still warm, on a graceful stop signal or after
  about 50 minutes of transcript idleness. It works only if the stop leaves time for one request, and a
  [`SessionEnd` hook][cc-sessions] receives the transcript path. Whether a slash command works in `-p` mode was not checked.
- **Raise the host's idle limit above the cache lifetime:** keeping the host alive past one hour lets idle
  compaction run (documented condition: the computer stays awake).
- **Accept one cold rewrite:** after a long stop the next request reprocesses the prefix once; with a very large
  context, resume into a new session instead of the old one ([sessions][cc-sessions]).
- **A keep-alive ping from outside the session does not help** unless it sends a byte-identical prefix to the one
  Claude Code sends (our inference from the exact-match rule, not a documented statement).

### Predicting a hit or a miss

A request hits when its prefix is byte-identical to the last request's, on the same model and speed, in the same
workspace, and within the lifetime of that request's start ([caching docs][caching], [CC caching docs][cc-caching],
read 2026-11-25). This predicts hit or miss only, not the saving. In Claude Code, `/usage` shows a
"Prompt cache (main)" line with the hit ratio, misses and whether the cache is warm, plus a likely cause such as
"tool definitions changed" (v2.1.260 or later). For code that builds its own requests, the API's
[cache diagnostics][cache-diag] (documented stable on the Claude API; the SDKs expose it under their `beta` namespace, read 2026-11-25)
compare consecutive requests via `diagnostics.previous_message_id` and report the first divergence (`model_changed`,
`system_changed`, `tools_changed`, `messages_changed`); it needs the previous response's `id`, the same workspace, and
closely spaced requests.

### Claims checked (2026-11-25)

| Claim | Status | Source |
|---|---|---|
| Auto-compact has no time-based trigger | Wrong: `idleCompaction` (default `true`) compacts a long idle session before its cache expires | [settings reference][settings-ref] |
| Idle compaction fires after exactly 54 minutes | Conflict: changelog "about 54 minutes", settings reference "about an hour"; both recorded above | [changelog][cc-changelog], [settings reference][settings-ref] |
| Claude Code compacts on resume or restart | Not found (inference from the docs): a resumed session restores history to its last compaction, and no compaction step on resume is described; compacting an old session costs the most | [sessions][cc-sessions], [CC caching docs][cc-caching] |
| A cache can be exported, rebuilt or hosted locally | Not possible for a closed model: caches are isolated per organization (and per workspace on the Claude API); no export is documented | [caching docs][caching] |
| A subagent or another session shares the main thread's cache | Fresh subagent: no (own prompt and tools). Fork: yes, it inherits the parent's prompt, tools and history, so its first request reads the parent's cache. Parallel sessions in one directory can read each other's cache | [CC caching docs][cc-caching] |
| Prompt-caching cost cut of 41-80% | From the abstract, across three providers; one study | [arXiv 2601.06007][p-dontbreak] |
| "Agents spend 76.1% of the token budget on reads" (SWE-Pruner) | Unverified (search snippet only); not used | [arXiv 2601.16746](https://arxiv.org/abs/2601.16746) |

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

**Invalidates** (abridged — see source for the full mechanism per item): switching models (`/model`), including the `opusplan` setting's Opus↔Sonnet toggle between plan mode and execution; changing effort level mid-session (except on Opus 5.5/Sonnet 5.5/Haiku 5.5/Fable 5.1 with an API key or Claude subscription); turning on fast mode for the first time in a conversation; connecting or removing a Model Context Protocol (MCP) server, or enabling/disabling a plugin that provides one, when MCP tool search isn't deferring tool definitions; denying a whole tool when tool search is unavailable or disabled; compacting the conversation (`/compact`); accumulating enough images/PDFs to evict a batch; and upgrading the CC binary.

**Keeps the cache**: editing files in the repo; editing CLAUDE.md mid-session (the edit also doesn't apply until `/clear`, `/compact`, or a restart); changing permission mode; changing output style; invoking skills and commands; `/recap`; `/rewind`; and spawning a subagent — the subagent starts its own fresh cache (its first request can't read the parent's), and the parent's prefix is left untouched by the call and its result.

Source: [CC prompt-caching docs][cc-caching], "Actions that invalidate the cache" / "Actions that keep the cache" sections

### API-level invalidation (platform docs)

The list above is CC's own framing. The [prompt caching docs][caching] document invalidation one level down, at the Messages API. The cache follows the hierarchy `tools` → `system` → `messages`, and "Changes at each level invalidate that level and all subsequent levels." Their "What invalidates the cache" table (✘ = invalidated):

| What changes | Tools | System | Messages |
|---|---|---|---|
| Tool definitions (names, descriptions, parameters) | ✘ | ✘ | ✘ |
| Web search toggle, citations toggle (both modify the system prompt) | ✓ | ✘ | ✘ |
| Speed setting (`speed: "fast"` ↔ standard) | ✓ | ✘ | ✘ |
| `tool_choice`; adding/removing images | ✓ | ✓ | ✘ |
| Thinking parameters (mode, `budget_tokens` in extended mode) | model-specific | model-specific | ✘ |
| Effort setting (`output_config.effort`) | model-specific | model-specific | ✘ |
| Non-tool results passed to requests with thinking | ✓ | ✓ | ✓ on Opus 4.5+, Sonnet 4.6+, Haiku 5.5 (thinking blocks preserved); ✘ on earlier Opus/Sonnet and Haiku through 4.5 |
| Dropped thinking blocks (blocks the receiving model cannot read; readable blocks passed back unchanged keep the cache; Fable 5.2 binding rules in [CC-models-reference.md](../configuration/CC-models-reference.md#claude-5x-lifecycle-defaults-and-fable-52-breaking-changes)) | ✓ | ✓ | ✘ from the dropped block onward |

Two exceptions in the table's own text bear on CC: "Setting effort explicitly to the model's default is equivalent to omitting it and does not invalidate," and "On models that support per-message effort, an effort change carried in a `role: "system"` message inside `messages` leaves the cached prefix intact." Likewise, on Fable 5.2, Mythos 5.2, Fable 5.1, Mythos 5.1, Fable 5, Mythos 5, Opus 5.5, Opus 4.8, Opus 5, Sonnet 5.5 and Haiku 5.5 a new system instruction can be appended as a `{"role": "system"}` message without invalidating the system or message caches (not on Sonnet 5), and the `inline-tools-2026-09-15` beta lets a tool be added mid-conversation without editing `tools`.

**Effort: the two statements reconcile.** The API table says a top-level `output_config.effort` change "always invalidates message blocks", with the per-message exception above. The CC list says CC's mid-session effort changes keep the cache on Opus 5.5/Sonnet 5.5/Haiku 5.5/Fable 5.1 with an API key or Claude subscription ([CC prompt-caching docs][cc-caching]). CC uses exactly that exception: "On Opus 5.5, Sonnet 5.5, Haiku 5.5, and Fable 5.1, a beta header pairs with `output_config.effort` on `role: "system"` entries, either a system message or an entry with empty content" ([CC gateway guide][cc-gateway], "Beta header and body field pairs", accessed 2026-11-08). The [effort docs][effort] name that beta `mid-conversation-output-config-2026-07-01` and list per-message effort on Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Sonnet 5.5 and Haiku 5.5 on the Claude API (fewer models on other platforms), so CC's list is a subset. Where CC doesn't send the per-message field — Bedrock, Google Cloud's Agent Platform, a Claude apps gateway, `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`, or a HIPAA configuration — an effort change invalidates as on other models ([CC prompt-caching docs][cc-caching], [CC gateway guide][cc-gateway]).

Source: [prompt caching docs][caching], "What invalidates the cache" section and the notes after it (raw page text, accessed 2026-10-26); [CC gateway guide][cc-gateway] and [effort docs][effort] (accessed 2026-11-08)

### Preserved thinking (documented, 2026-11-23)

[Preserved thinking][pthink] covers which earlier-turn thinking blocks Claude can still use when a request sends them back. Documented scope: Fable 5.2, Mythos 5.2, Fable 5.1, Mythos 5.1, Opus 5.5, Sonnet 5.5 and Haiku 5.5 (Messages API, Managed Agents). On these models, usable blocks stay in context and are billed as input.

| Binding | Rule (documented) |
|---|---|
| Prior content | A block is tied to `system`, `tools` and every earlier message; a change fails the prefix check and the request can get a 400 (rules: [CC-models-reference.md](../configuration/CC-models-reference.md#claude-5x-lifecycle-defaults-and-fable-52-breaking-changes)) |
| Model | A model reads only some other models' blocks; the page has a switch matrix (for example Fable 5.2 blocks are read only by Fable 5.2 and Mythos 5.2) |
| Account | Fable 5.2, Mythos 5.2, Sonnet 5.5 and Haiku 5.5 blocks work only in the producing account or a linked one. "Account" means the organization on the Claude API, Platform on AWS, Google Cloud (Anthropic managed) and Foundry; the AWS account on Bedrock; the project on Google Cloud (Google managed) |

**Unusable block.** A block the new model or account cannot read never causes an error: the API drops it for that request, does not bill it, and Claude answers without that reasoning. The dropped entry is listed in `input_transformations` (reasons `model_binding_mismatch`, `organization_binding_mismatch`) when the `anthropic-beta: thinking-binding-controls-2026-08-01` header is sent. The history is not changed, so the block is readable again on the original model or account. A prefix-check failure is separate: `prefix_mismatch_behavior` chooses between a 400 and dropping the failing blocks (`"drop_block"`, which needs that beta header and adaptive thinking); with the setting unset, behaviour varies by model (some let the blocks through), and Message Batches items never get the 400.

**Cost of dropping.** The docs say Claude can spend more output tokens re-deriving reasoning it cannot read, and that dropping invalidates the prompt cache from the first dropped block onward. This is the "Dropped thinking blocks" row in the [invalidation table](#api-level-invalidation-platform-docs) above.

**In Claude Code (owner observation, CC v2.1.330).** After signing in to a different organization, CC showed a notice that Claude cannot use thinking from another organization. The text said the earlier thinking was written under the other org and is not deleted, that resuming signed in to that org makes it usable again, and that the next responses may be slower and use more tokens because Claude rereads the session and writes new thinking. It linked the preserved-thinking page. This is a single observation, not in the CC changelog through 2.1.330; it matches the documented account-bound drop, and the cost it names matches the cache effect above. Whether it applies to every affected model or sign-in path is unverified.

Source: [Preserved thinking][pthink] and [Fix a thinking block bound to a different conversation][pthink-fix] (read 2026-11-23)

## Cache Scope

In CC, the cache is effectively scoped to one machine and directory — the system prompt embeds auto-memory paths, and the conversation opens with an announcement of the working directory, platform, shell, and OS version. Two sessions in different directories therefore build different prefixes and miss each other's cache. Sessions run in **parallel** in the *same* directory build matching prefixes and read each other's cache; **sequential** sessions in the same directory share the prefix only when the git status snapshot taken at startup matches, since each conversation also carries the branch and recent commits from that snapshot.

The underlying API cache is broader than CC's own scoping. Requoted 2026-10-26 from the FAQ "How does prompt caching handle privacy and data separation?" (the earlier quote here was no longer verbatim): "On the Claude API, Claude Platform on AWS, and Microsoft Foundry, caches are isolated by workspace within an organization. On Bedrock and Claude Models on Google Cloud (Google managed), caches are isolated by organization. In every case, caches are never shared across organizations, even for identical prompts." The "(Google managed)" qualifier implies a split within "Google Cloud": the Google-managed surface gets organization-level isolation (grouped with Bedrock), while **Claude Models on Google Cloud (Anthropic managed) is not named in either list** — it most plausibly falls under the first (workspace-level) group by the same logic as Claude Platform on AWS, but the docs don't say so explicitly, so treat that specific inference as unverified. (code.claude.com elsewhere calls this same Google product "Google Cloud's Agent Platform" — same product, different doc family's naming.)

Source: [CC prompt-caching docs][cc-caching], "Cache scope" section; [prompt caching docs][caching], FAQ "How does prompt caching handle privacy and data separation?" section (accessed 2026-10-26)

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

**Fable 5.2 prefix check (documented, 2026-11-23).** On Fable 5.2 and Mythos 5.2 the API also runs a [prefix check](../configuration/CC-models-reference.md#claude-5x-lifecycle-defaults-and-fable-52-breaking-changes): changing `system`, `tools` or earlier messages and then sending thinking blocks back returns a 400 rather than a silent cache miss. The [migration guide][fable52-migration] says an append-only history, which this section's invalidation rules already favor, also keeps the prompt cache warm. The guide points to compaction on demand (beta) and mid-conversation tool and system changes as ways to keep history append-only. Claude Code manages history itself, so this affects only code that builds its own `messages` array.

## Sources

| Source | Content |
|---|---|
| [Fable 5.2 migration guide][fable52-migration] | Prefix check, append-only history and cache note (read 2026-11-23) |
| [Preserved thinking][pthink], [fix-bound page][pthink-fix] | Supported models, model/account binding, unusable-block drop, cost of dropping, `input_transformations` (read 2026-11-23) |
| [Prompt caching docs][caching] | What's cached, prefix matching, breakpoints, TTL, minimum cacheable prefix per model, cache isolation, lifetime start, manual clear, ZDR, Batches interaction, API-level invalidation table — raw page text, re-verified 2026-10-26 |
| [CC LLM gateway guide][cc-gateway] | Per-turn effort via `output_config.effort` on `role: "system"` entries (accessed 2026-11-08) |
| [Effort docs][effort] | Per-message effort beta, header, supported models (accessed 2026-11-08) |
| [Pricing docs][pricing] | Per-model cache write/read rates, including the 0.025x/0.05x/0.1x cache-hit multiplier tiers (accessed 2026-10-26) |
| [API messages docs][api] | Usage object fields (`cache_read_input_tokens`, `cache_creation_input_tokens`) |
| [CC prompt-caching docs][cc-caching] | CC-specific TTL buckets, choose-the-TTL precedence, disable vars, cache scope, actions that invalidate/keep the cache (accessed 2026-10-15) |
| [CC env vars reference][cc-env-vars] | `CLAUDE_CODE_PROMPT_CACHE_TTL`, `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`, `FORCE_PROMPT_CACHING_5M`, `ENABLE_PROMPT_CACHING_1H`, `DISABLE_PROMPT_CACHING*` (accessed 2026-10-15) |
| [CC changelog][cc-changelog] | Idle compaction: 2.1.299 (terminal, `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS`), 2.1.302 (`/config` row), 2.1.314 (VS Code, Desktop, gateways), 2.1.318 (fix) (read 2026-11-09) |
| [Settings reference][settings-ref] | `idleCompaction` description, default `true`, v2.1.290+ (read 2026-11-09); conditions list with "about an hour" idle time and the one-hour-TTL requirement (read 2026-11-25) |
| [Cache diagnostics][cache-diag] | `diagnostics.previous_message_id`, `cache_miss_reason` types, stable status, same-workspace limit (read 2026-11-25) |
| [cachemiss][cachemiss] | Rebuilt-token rule for a cache miss (tokens the previous call had cached that this call writes again); MIT, source read 2026-11-25, not run |
| [Claude Code caching docs][cc-caching] | Prefix layers, subagent and fork cache sharing, `/usage` "Prompt cache (main)" line, cache scope (read 2026-11-25) |
| [arXiv 2604.22750][p-spend], [2508.21433][p-complexity], [2610.04433][p-harness-tokens], [2601.06007][p-dontbreak], [2307.03172][p-lost-middle] | Cost-lever papers, abstracts read 2026-11-25 (preprints; 2307.03172 peer-reviewed in 2023) |
| [Chroma, Context Rot][chroma-rot], [Manus][manus-ctx], [Anthropic, context management][anth-context-mgmt] | Practitioner and vendor sources for the context-size and prompt-stability levers (read 2026-11-25) |
| [Sessions][cc-sessions] | What a resumed session restores: history up to the last compaction, no compaction on resume (read 2026-11-25) |
| CC 2.1.83, session `9f7de296`, Codespaces, 2026-03-27 | Cache warmup curve, 96.3% hit rate — predates the TTL-bucket model (CC v2.1.242+) described above |
| [AWS Bedrock prompt-caching docs][bedrock-caching] | Per-model minimum cacheable prefix on Bedrock specifically (Fable/Mythos 5.x = 512 tokens, same as other platforms) (accessed 2026-10-15) |

[caching]: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[fable52-migration]: https://platform.claude.com/docs/en/models/fable-5-2/migration-guide
[pthink]: https://platform.claude.com/docs/en/build-with-claude/preserved-thinking
[pthink-fix]: https://platform.claude.com/docs/en/build-with-claude/preserved-thinking/fix-bound-to-a-different-conversation
[pricing]: https://platform.claude.com/docs/en/about-claude/pricing
[api]: https://platform.claude.com/docs/en/api/messages
[cc-caching]: https://code.claude.com/docs/en/prompt-caching
[cc-env-vars]: https://code.claude.com/docs/en/env-vars
[settings-ref]: https://code.claude.com/docs/en/settings-reference#idlecompaction
[cc-sessions]: https://code.claude.com/docs/en/sessions
[bedrock-caching]: https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html
[cc-gateway]: https://code.claude.com/docs/en/llm-gateway-protocol
[effort]: https://platform.claude.com/docs/en/build-with-claude/effort
[cc-changelog]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
[cache-diag]: https://platform.claude.com/docs/en/build-with-claude/cache-diagnostics
[cachemiss]: https://github.com/CedricConday/cachemiss
[p-spend]: https://arxiv.org/abs/2604.22750
[p-complexity]: https://arxiv.org/abs/2508.21433
[p-harness-tokens]: https://arxiv.org/abs/2610.04433
[p-dontbreak]: https://arxiv.org/abs/2601.06007
[p-lost-middle]: https://arxiv.org/abs/2307.03172
[chroma-rot]: https://www.trychroma.com/research/context-rot
[manus-ctx]: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
[anth-context-mgmt]: https://www.claude.com/blog/context-management
