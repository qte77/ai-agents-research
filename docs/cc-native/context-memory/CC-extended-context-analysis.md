---
title: CC Extended Context Window (1M) Analysis
source: https://code.claude.com/docs/en/model-config#extended-context
purpose: Analysis of 1M token extended context window for cost planning and headless CC workflow usage.
created: 2026-03-07
updated: 2026-06-19
validated_links: 2026-06-19
---

**Status**: Beta (features, pricing, and availability may change)

## What It Is

Opus 4.6 and Sonnet 4.6 support a 1 million token context window, up from
the standard 200K. This enables long sessions with large codebases without
hitting context limits or triggering auto-compaction.

## Availability

| Account Type | 1M Access | Billing |
| ------------ | --------- | ------- |
| API / pay-as-you-go | Full access | Long-context pricing above 200K |
| Pro, Max, Teams, Enterprise | Requires [extra usage](https://support.claude.com/en/articles/12429409-manage-extra-usage-for-paid-claude-plans) enabled | Tokens above 200K billed as extra usage |

## Pricing Model

Selecting a 1M model does **not** immediately change billing. The session
uses standard rates until context exceeds 200K tokens. Beyond 200K:

- Requests charged at
  [long-context pricing](https://platform.claude.com/docs/en/about-claude/pricing#long-context-pricing)
- Dedicated
  [rate limits](https://platform.claude.com/docs/en/api/rate-limits#long-context-rate-limits)
  apply
- For subscribers, billed as extra usage (not subscription)

### Interaction with Fast Mode

Fast mode pricing splits at the same 200K boundary — see pricing table in
[CC-fast-mode-analysis.md](../configuration/CC-fast-mode-analysis.md#pricing). The 1M window
extends the upper-tier pricing zone from 200K to 1M tokens. Fast mode is
compatible with the full 1M context (confirmed v2.1.50).

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

Removes 1M model variants from the model picker entirely. Set in
`settings.json` env section or shell environment.

## Relevance by Workflow

| Workflow | Fit | Rationale |
| -------- | --- | --------- |
| Interactive development | Strong | Large codebase exploration without compaction; avoids context rot mid-session |
| Autonomous development loop (`claude -p`) | Weak | Each iteration starts fresh with clean context; rarely approaches 200K. Extra cost unjustified. |
| Headless teams mode | Weak | Each teammate has its own context window; same fresh-start pattern as solo mode |
| CC baseline collection | Neutral | Longer runs may benefit, but cost scales with context; only if evaluation requires deep multi-file analysis in a single pass |
| Code review sessions | Medium | Multi-file reviews with large diffs can benefit from sustained context |

### Decision Rule

**Use 1M context for interactive sessions exploring large codebases or
reviewing large diffs. Avoid for autonomous/headless invocations where
fresh context per iteration is the design pattern.**

### Cost Awareness

The 200K threshold is the key cost boundary. Monitor context usage via
`/cost` or the status line (`context_window.used/remaining_percentage`).
For headless autonomous runs, `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` prevents
accidental long-context charges.

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

## References

- [CC Model Configuration — Extended context](https://code.claude.com/docs/en/model-config#extended-context)
- [CC Costs](https://code.claude.com/docs/en/costs)
- [Long-context pricing](https://platform.claude.com/docs/en/about-claude/pricing#long-context-pricing)
- [Long-context rate limits](https://platform.claude.com/docs/en/api/rate-limits#long-context-rate-limits)
- [CC-fast-mode-analysis.md](../configuration/CC-fast-mode-analysis.md) — fast mode pricing tiers
- [CC-model-provider-configuration.md](../configuration/CC-model-provider-configuration.md) — model env vars
- [Long-Context Isn't the Answer][hlyr-long-ctx] — hlyr.dev, Kyle, 2026-03-23
- [Context-Efficient Backpressure][hlyr-backpressure] — hlyr.dev, Dex, 2025-12-09

[hlyr-long-ctx]: https://www.hlyr.dev/blog/long-context-isnt-the-answer
[hlyr-backpressure]: https://www.hlyr.dev/blog/context-efficient-backpressure
[cc-ralph]: ../agents-skills/CC-ralph-enhancement-research.md
[cc-mem-ace]: CC-memory-system-analysis.md#context-engineering-workflow-ace-fca
