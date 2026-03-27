---
title: CC Prompt Caching Behavior — Server-Side Mechanism and Session Economics
purpose: How Anthropic's server-side prompt caching works in CC sessions — what's cached, matching, TTL, hit rates, and cost impact.
created: 2026-03-27
updated: 2026-03-27
validated_links: 2026-03-27
---

**Status**: Adopt

## What It Is

Anthropic's [prompt caching][caching] is a server-side optimization that caches the **input prefix** of API requests. In CC sessions, this means the entire conversation history (system prompt, prior messages, tool results) is cached and reused across turns. CC uses 5-minute ephemeral cache exclusively.

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
3. If a matching hash exists from a prior request within the TTL → **cache hit** (0.1x input price)
4. If no match → **cache miss** → full processing + cache write (1.25x input price for 5m)

### 20-block lookback window

The server checks at most 20 block positions backward from the breakpoint. If the prior cache entry is beyond 20 blocks back, it's a miss even if the prefix is identical.

Source: [prompt caching docs][caching], "How cache lookback works" section

## CC-Specific Caching Behavior

### 5-minute cache only

CC uses `{"type": "ephemeral"}` (default 5-minute TTL) exclusively. The 1-hour tier (`{"type": "ephemeral", "ttl": "1h"}`) is never used.

**Evidence**: Session `9f7de296`, CC 2.1.83, Codespaces, 2026-03-27 — 281 turns:
- `ephemeral_5m_input_tokens`: 1,732,355 (all cache writes)
- `ephemeral_1h_input_tokens`: 0

### TTL refresh on hit

Each cache hit resets the 5-minute timer at no additional cost. From the [caching docs][caching]: *"The cache is refreshed for no additional cost each time the cached content is used."*

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

<!-- markdownlint-disable MD013 -->

| Metric | Value |
|---|---|
| Overall hit rate | 96.3% |
| Total cache read | 45.7M tokens |
| Total cache create | 1.7M tokens |
| Actual session cost | $35.52 |
| Hypothetical cost without caching (all at base input) | $242.49 |
| **Savings** | **$206.97 (85%)** |

<!-- markdownlint-enable MD013 -->

Pricing: input $5/MTok, output $25/MTok, 5m cache write $6.25/MTok (1.25x), cache read $0.50/MTok (0.1x). Source: [pricing docs][pricing], accessed 2026-03-27.

## Why Hit Rates Are So High in CC

In a CC session, the input to each API call is:

```text
[tools] + [system prompt] + [message 1] + [response 1] + [tool_use 1] + [tool_result 1] + ... + [new user message]
```

Everything except the new user message is identical to the prior call's prefix. Since tool results and assistant responses are part of the cached prefix, only the delta (new message + its tool results) triggers cache writes. The growing prefix stays cached.

## Slug (CC-Internal)

"Slug" is **not an Anthropic API concept**. It does not appear in the [API docs][api], [prompt caching docs][caching], or any platform documentation.

Slug is a CC-internal auto-generated session display name (e.g., `stateful-dreaming-donut`) carried on every message in session JSONL files. See [CC-session-lifecycle-analysis.md](../ci-execution/CC-session-lifecycle-analysis.md) for slug behavior and `/rename` bugs.

## Cross-References

- [CC-session-cost-analysis.md](../ci-execution/CC-session-cost-analysis.md) — JSONL cache fields, jq cost recipes
- [CC-extended-context-analysis.md](CC-extended-context-analysis.md) — Context window management
- [CC-session-lifecycle-analysis.md](../ci-execution/CC-session-lifecycle-analysis.md) — Session naming, slug, `/rename`

## Sources

<!-- markdownlint-disable MD013 -->

| Source | Content |
|---|---|
| [Prompt caching docs][caching] | What's cached, prefix matching, breakpoints, TTL, pricing multipliers |
| [Pricing docs][pricing] | Per-model cache write/read rates (accessed 2026-03-27) |
| [API messages docs][api] | Usage object fields (`cache_read_input_tokens`, `cache_creation_input_tokens`) |
| CC 2.1.83, session `9f7de296`, Codespaces, 2026-03-27 | Cache warmup curve, 5m-only behavior, 96.3% hit rate |

<!-- markdownlint-enable MD013 -->

[caching]: https://platform.claude.com/docs/en/docs/build-with-claude/prompt-caching
[pricing]: https://platform.claude.com/docs/en/docs/about-claude/pricing
[api]: https://platform.claude.com/docs/en/docs/api/messages
