---
title: CC Fast Mode Analysis
source: https://code.claude.com/docs/en/fast-mode
purpose: Analysis of Claude Code Fast Mode for potential adoption within CC-based workflows.
created: 2026-02-17
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Research preview (pricing and availability may change)

## What Fast Mode Is

A high-speed API configuration — **same model, same quality, 2.5x faster output tokens** ([source][cc-fast]). Currently supports Opus 4.8 and Opus 4.7, not Opus 4.6: Opus 4.8 is the fast-mode default as of CC v2.1.154+ (v2.1.142–2.1.153 defaulted to Opus 4.7). Opus 4.7 fast mode is deprecated as of 2026-06-25 and scheduled for removal 2026-07-24, after which it returns an error with no fallback ([source][cc-fast]). Toggle with `/fast` — fast mode is not supported in the VS Code extension, CLI only ([source][cc-fast]). Not a different model or reduced reasoning — purely an infrastructure-level latency optimization at higher per-token cost.

### Pricing

| Mode | Input (MTok) | Output (MTok) |
| ---- | ------------ | ------------- |
| Fast mode Opus 4.8 | $10 | $50 |
| Fast mode Opus 4.7 (deprecated, removed 2026-07-24) | $30 | $150 |
| Standard (non-fast-mode) | Lower | Lower |

([source][cc-fast])

Compatible with the 1M token extended context window ([source][cc-fast]). Pricing is flat across the full 1M context window for both fast-mode-supported models (Opus 4.8, Opus 4.7) — no context-size split.

### Effort Level Interaction

Default effort is **high** across Opus 4.6, Fable 5, Sonnet 5, Opus 4.8, and Sonnet 4.6, and **xhigh** on Opus 4.7 — no model defaults to medium effort, and there is no Max/Team-subscriber-specific default ([source][cc-model]). The "ultrathink" keyword still exists — it triggers deeper reasoning for one turn without changing the session effort setting. This interacts with fast mode:

| Combination | Effect |
| ----------- | ------ |
| Fast mode + default (high) effort | Balanced speed/quality for the fast-mode model default |
| Fast mode + `ultrathink` | Maximum quality, highest cost and latency |
| Fast mode + low effort | Maximum speed on simple tasks |

After `/usage-credits`, `/fast` remains available.

### Configuration

```json
{ "fastMode": true }
```

Or toggle per-session: `/fast` (persists across sessions). No dedicated `--fast` CLI flag exists; enable non-interactively via `claude -p --settings '{"fastMode": true}'` ([source][cc-cli]).

### Key Mechanics

- Enabling mid-conversation pays full uncached input price for entire context (enable at session start for cost efficiency) ([source][cc-fast])
- Separate rate limits from standard (non-fast-mode) usage; auto-fallback to standard on limit hit ([source][cc-fast])
- Available via usage credits only — not included in subscription rate limits ([source][cc-fast])
- Not available on Bedrock, Google Cloud's Agent Platform (formerly Vertex AI), Microsoft Foundry (formerly Azure Foundry), or Claude Platform on AWS ([source][cc-model])
- Teams/Enterprise: admin must explicitly enable ([source][cc-fast])

### Fast Mode vs Effort Level

| Setting | Effect |
| ------- | ------ |
| Fast mode | Same quality, lower latency, higher cost |
| Lower effort | Less thinking, faster, potentially lower quality on complex tasks |

Combinable: fast mode + lower effort for maximum speed on simple tasks.

## Applicability

| Workflow | Fit | Rationale |
| -------- | --- | --------- |
| Interactive development (debugging, iteration) | Strong | Latency reduction directly improves developer flow |
| Autonomous headless loop (`claude -p`) | Weak | Developer not waiting; cost matters more than speed |
| Parallel autonomous tasks | Weak | Same as above; multiple concurrent agents multiply the cost further |
| Batch/background generation tasks | Weak | No interactive waiting; cost efficiency preferred |
| Time-boxed collection runs | Neutral | Faster turnaround but 2x+ cost; only worth it under time pressure |

### Decision Rule

**Enable fast mode for interactive sessions where latency breaks flow. Disable for autonomous/headless invocations (`claude -p`) where cost efficiency matters.**

### Potential Integration

If adopted, fast mode could be passed through Makefile recipes:

```makefile
# Example (NOT implemented — YAGNI until measured need)
FAST_MODE ?= false
autonomous_run:
    $(if $(filter true,$(FAST_MODE)),--fast)
```

**Recommendation**: Do not integrate yet. Fast mode is a research preview with unstable pricing. Headless CC usage (`claude -p`) is autonomous — the 2.5x speed gain doesn't justify 2x+ cost increase when no human is waiting. Revisit if:

1. Pricing stabilizes and drops
2. The autonomous loop becomes interactive (unlikely by design)
3. Time-boxed runs need faster turnaround

## References

- [CC Fast Mode docs][cc-fast]
- [CC Model Configuration][cc-model]
- [CC Cost Management][cc-costs]
- [CC CLI Reference][cc-cli]

[cc-fast]: https://code.claude.com/docs/en/fast-mode
[cc-model]: https://code.claude.com/docs/en/model-config
[cc-costs]: https://code.claude.com/docs/en/costs
[cc-cli]: https://code.claude.com/docs/en/cli-reference
