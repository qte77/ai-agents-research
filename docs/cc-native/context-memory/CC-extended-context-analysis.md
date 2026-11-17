---
title: CC Extended Context Window (1M) Analysis
source: https://code.claude.com/docs/en/model-config#extended-context
purpose: Analysis of 1M token extended context window for cost planning and headless CC workflow usage.
created: 2026-03-07
updated: 2026-11-17
validated_links: 2026-11-15
status: beta
---

**Details:** features, pricing, and availability may change

## What It Is

A 1 million token context window, up from the standard 200K, for long sessions
with large codebases. Per the [model configuration docs][cc-model-config]
(checked 2026-11-15), Fable models, Sonnet 5 and later, Haiku 5.5, Opus 4.6 and
later, and Sonnet 4.6 support it. Fable models, Sonnet 5 and later, Haiku 5.5
and Opus 4.7 and later run with the 1M window **by default**; Opus 4.6 and
Sonnet 4.6 reach it only through the `[1m]` suffix.

**Corrected 2026-11-15:** earlier versions of this doc described a
long-context premium above 200K tokens and a 200K billing boundary. That no
longer matches the pricing page; see [Pricing Model](#pricing-model).

## Availability

| Account type | 1M access and billing (per [model configuration docs][cc-model-config], 2026-11-15) |
| ------------ | --------- |
| API / pay-as-you-go | Full access at standard per-token prices (Haiku 5.5: higher prices on prompts over 100K tokens) |
| Max, Ultra, Team, Enterprise | Opus 4.6 with 1M is included in the subscription; Sonnet 4.6 with 1M needs usage credits on every plan |
| Pro | Opus 4.6 and Sonnet 4.6 with 1M need usage credits |

Claude Code checks these plan requirements only when it connects to the
Anthropic API directly: with `ANTHROPIC_BASE_URL` pointing at an LLM gateway
while a claude.ai login stays the active credential, it doesn't check usage
credits and the gateway decides. The docs give no per-plan rule for the models
that run at 1M by default (Fable, Sonnet 5+, Haiku 5.5, Opus 4.7+); separately,
Fable usage itself can bill to usage credits depending on plan and seat tier.
Checked 2026-11-15 by two fetches whose text for this section came from a
summary of the page rather than verbatim — re-check before quoting.

## Pricing Model

There is no long-context premium on current models. The
[pricing page][pricing-long-context] (checked 2026-11-15): "Claude 4.6 and later
models (except Claude Haiku 5.5) and Claude Mythos Preview include the full 1M
token context window at standard pricing. (A 900k-token request is billed at the
same per-token rate as a 9k-token request.)" Prompt-caching and batch discounts
apply across the whole window. Haiku 5.5 is the exception: a request whose prompt
is over 100,000 tokens, cache reads and writes included, pays higher prices.

The [rate-limits page](https://platform.claude.com/docs/en/api/rate-limits) no
longer has a separate long-context rate-limit section (checked 2026-11-15).

What still grows with context is the per-request cost: every request re-sends the
whole prefix, mostly as cache reads (see
[CC-prompt-caching-behavior.md](CC-prompt-caching-behavior.md)).

### Interaction with Fast Mode

Per the [pricing page][pricing-long-context] (checked 2026-11-15): "Fast mode
pricing applies across the full context window, including requests over 200k
input tokens." Fast-mode prices per model are in
[CC-fast-mode-analysis.md](../configuration/CC-fast-mode-analysis.md#pricing).

## Configuration

### Enable

The 1M option appears in `/model` picker if the account supports it. Use
the `[1m]` suffix with model aliases or full model names:

```bash
# Alias
/model sonnet[1m]

# Full model name
/model claude-sonnet-4-6[1m]
```

The `sonnet[1m]` alias is a top-level model alias in CC.

### Disable

```bash
CLAUDE_CODE_DISABLE_1M_CONTEXT=1
```

Removes the `[1m]` variants from the model picker; models that default to 1M
are then treated as 200K and compact at that boundary. Set in the
`settings.json` env section or the shell environment.

## Relevance by Workflow

| Workflow | Fit | Rationale |
| -------- | --- | --------- |
| Interactive development | Strong | Large codebase exploration without compaction; avoids context rot mid-session |
| Autonomous development loop (`claude -p`) | Weak | Each iteration starts fresh with clean context; rarely approaches 200K. A larger window only lets per-request cost and drift grow. |
| Headless teams mode | Weak | Each teammate has its own context window; same fresh-start pattern as solo mode |
| CC baseline collection | Neutral | Longer runs may benefit, but cost scales with context; only if evaluation requires deep multi-file analysis in a single pass |
| Code review sessions | Medium | Multi-file reviews with large diffs can benefit from sustained context |

### Decision Rule

**Use 1M context for interactive sessions exploring large codebases or
reviewing large diffs. Avoid for autonomous/headless invocations where
fresh context per iteration is the design pattern.**

### Cost Awareness

There is no 200K price step on current models, so the cost driver is how much
context each request carries, not which window is selected. Monitor it via
`/cost` or the status line (`context_window.used/remaining_percentage`). On a
subscription, Sonnet 4.6 at 1M (and both 4.6 models on Pro) draws on usage
credits. For headless runs, `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` keeps sessions at
200K and compacts them there.

Idle sessions: since v2.1.299 Claude Code compacts a 200K+ token conversation left idle for about 54 minutes, before its one-hour prompt cache expires (`idleCompaction`, default on). See [CC-prompt-caching-behavior.md § Idle compaction](CC-prompt-caching-behavior.md#idle-compaction-before-the-cache-expires).

## Context Quality Degradation

A larger context window does not raise a model's **instruction budget** — the count of instructions it reliably follows before adherence drops. The instruction budget is set by model size and instruction-tuning; window-extension techniques such as YaRN extend the position space but do not increase how many directives the model tracks simultaneously ([source][hlyr-long-ctx]).

### Smart Zone vs Dumb Zone

HumanLayer distinguishes two operating regions based on their empirical practice ([source][hlyr-backpressure]):

| Region | Token range | Behavior |
|---|---|---|
| Smart Zone | 0 – ~75k tokens | Peak adherence; retrieval fidelity high |
| Dumb Zone | Beyond ~75k tokens | Positional interpolation loses fidelity; "lost in the middle" effects increase |

The ~75k smart-zone figure is comparable to this repo's 40–60% utilization target (for a 200K standard window). HumanLayer's empirical practice sets a context warning/reset around ~100k tokens regardless of the model's stated maximum window.

> **Framing note**: HumanLayer reports observing instruction-adherence degradation when defaulting to very large context windows. This is a practitioner observation, not an Anthropic-confirmed specification.

### Observable Degradation Signals

- Model ignores instructions given early in the session
- Coherence drops between consecutive turns
- Repetition of already-completed steps increases

### Mitigation

The primary mitigation is [frequent intentional compaction][cc-mem-ace]: distilling progress into a structured artifact before the dumb zone is reached, then starting a fresh session from the artifact. This is preferable to relying on a 1M window to avoid compaction altogether. Cross-ref: [fresh-context-per-iteration in CC-ralph-enhancement-research.md][cc-ralph]; [Context Engineering Workflow (ACE-FCA) in CC-memory-system-analysis.md][cc-mem-ace].

## Unrecognized model IDs (v2.1.323, v2.1.325)

Changelog entries: from v2.1.323 the context window assumed for a model ID Claude Code does not recognize is 1M instead of 200K; `/autocompact` compacts earlier and `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` keeps 200K, which matters on other vendors' smaller-window models that can fail every turn once full. From v2.1.325 `CLAUDE_CODE_MAX_CONTEXT_TOKENS` also sets the window for unrecognized IDs starting with `claude-`, such as a gateway's `claude-sonnet-latest` ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).

## References

- [CC Model Configuration — Extended context](https://code.claude.com/docs/en/model-config#extended-context)
- [CC Costs](https://code.claude.com/docs/en/costs)
- [Long-context pricing][pricing-long-context]
- [Rate limits](https://platform.claude.com/docs/en/api/rate-limits)
- [CC-fast-mode-analysis.md](../configuration/CC-fast-mode-analysis.md) — fast mode pricing tiers
- [CC-model-provider-configuration.md](../configuration/CC-model-provider-configuration.md) — model env vars
- [Long-Context Isn't the Answer][hlyr-long-ctx] — hlyr.dev, Kyle, 2026-03-23
- [Context-Efficient Backpressure][hlyr-backpressure] — hlyr.dev, Dex, 2025-12-09

[cc-model-config]: https://code.claude.com/docs/en/model-config#extended-context
[pricing-long-context]: https://platform.claude.com/docs/en/about-claude/pricing#long-context-pricing
[hlyr-long-ctx]: https://www.hlyr.dev/blog/long-context-isnt-the-answer
[hlyr-backpressure]: https://www.hlyr.dev/blog/context-efficient-backpressure
[cc-ralph]: ../agents-skills/CC-ralph-enhancement-research.md
[cc-mem-ace]: CC-memory-system-analysis.md#context-engineering-workflow-ace-fca
