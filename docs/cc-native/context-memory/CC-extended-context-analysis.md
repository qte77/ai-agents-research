---
title: CC Extended Context Window (1M) Analysis
source: https://code.claude.com/docs/en/model-config#extended-context
purpose: Analysis of 1M token extended context window for cost planning and headless CC workflow usage.
created: 2026-03-07
updated: 2026-11-23
validated_links: 2026-11-18
status: assess
---

**Details:** Beta; features, pricing, and availability may change

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

### Context failure modes

[Drew Breunig's "How Long Contexts Fail"][breunig-ctx] (2025-06-22, practitioner blog) names four ways a large context goes wrong. The labels are his; the evidence behind each is a mix of papers and benchmarks he cites, so treat the taxonomy as a vocabulary, not a measurement.

| Failure mode | What happens |
|---|---|
| Poisoning | An early error or hallucination enters the context and keeps being referenced |
| Distraction | The context grows so long that the model over-focuses on it and neglects what it learned in training |
| Confusion | Irrelevant content, such as unused tool definitions, degrades the answer |
| Clash | New information contradicts what is already in context |

Two of the primary papers behind it (abstract pages read 2026-11-23):

- **Tool count** — [Less is More (arXiv 2411.15399)][arxiv-less-is-more] (Paramanayakam et al., submitted 2024-11-23, accepted at DATE 2025) proposes selecting a subset of tools per query rather than passing all of them. In its worked example (read in the HTML version, not the abstract), a 4-bit quantized Llama 3.1 8B on an edge board picked the wrong tool when given 46 tools at a 16K context, and succeeded with 19. This is one model and one query on a benchmark's tool set: an illustration that tool-list size alone can break selection, not a general threshold. The abstract's headline numbers are different (execution time down by up to 70%, power by up to 40%).
- **Multi-turn drift** — [LLMs Get Lost In Multi-Turn Conversation (arXiv 2505.06120)][arxiv-lost-multiturn] (Laban et al., submitted 2025-05-09) reports that every top open- and closed-weight model tested did worse when a task was spread across turns than when given in one prompt, an average drop of 39% across six generation tasks. The authors split it into a small loss of aptitude and a larger rise in unreliability: once a model takes a wrong turn, it gets lost and does not recover.

Read with care: both papers are not Claude Code studies. They are background for, not proof of, trimming unused tool sets and starting a fresh session after a wrong turn (see Mitigation below). A [Splunk blog][splunk-ctx] (Pratik Bhavsar, 2026-08-11, read 2026-11-23; a vendor post promoting its agent-observability product) cites the same post and both papers and adds a context-size-tier strategy table and token thresholds; those are vendor guidance, not adopted here.

### Mitigation

The primary mitigation is [frequent intentional compaction][cc-mem-ace]: distilling progress into a structured artifact before the dumb zone is reached, then starting a fresh session from the artifact. This is preferable to relying on a 1M window to avoid compaction altogether. Cross-ref: [fresh-context-per-iteration in CC-ralph-enhancement-research.md][cc-ralph]; [Context Engineering Workflow (ACE-FCA) in CC-memory-system-analysis.md][cc-mem-ace].

## Unrecognized model IDs (v2.1.323, v2.1.325)

Changelog entries: from v2.1.323 the context window assumed for a model ID Claude Code does not recognize is 1M instead of 200K; `/autocompact` compacts earlier and `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` keeps 200K, which matters on other vendors' smaller-window models that can fail every turn once full. From v2.1.325 `CLAUDE_CODE_MAX_CONTEXT_TOKENS` also sets the window for unrecognized IDs starting with `claude-`, such as a gateway's `claude-sonnet-latest` ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)).

## Setting the auto-compact window (`/autocompact`)

Documented on the [commands page][cc-commands] (`/autocompact`, requires v2.1.221 or later) and in [Model Configuration: auto-compact window][cc-autocompact] (read 2026-11-18). The auto-compact window is how full the context may get before Claude Code compacts; `/compact` is the manual trigger and `/context` shows usage.

| Where | Scope | Notes |
|---|---|---|
| `/autocompact [auto\|<tokens>]` | Current model, this and later sessions | Saved under the model in `modelSettings` in user settings (per model since v2.1.288; before that one top-level `autoCompactWindow`). `auto` returns to the window tuned for the model. No argument opens a dialog showing the current window. A higher-priority scope such as managed settings wins for the session; the command says so |
| `autoCompactWindow` setting | Every model | A per-model value saved by `/autocompact` takes precedence in the same file |
| `--autocompact <value>` | One launch | Overrides saved settings without changing them; not preempted by managed settings (unlike the command) |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | Scripts, cloud | Wins over the command, flag and setting; `/autocompact` then reports the override without saving. Bare number is tokens; `k`/`M` suffixes need v2.1.304+ |
| subagent frontmatter `autoCompactWindow` | One subagent | Lowers the window for that subagent, 100K to 1M, v2.1.296+ ([sub-agents page][cc-subagents]); the changelog says it also lowers a window set by the env var and never raises it |

Accepted values for command and flag: 100K to 1M tokens as `200000`, `500k`, `1M`, or a bare 100-1000 meaning thousands (`200` is 200,000; but the env var reads `200` as 200 tokens). The window is capped at the model's context window.

Defaults when unset: models with a native 1M window (Fable, Sonnet 5+, Haiku 5.5, Opus 4.7+) compact at about 967K tokens; Sonnet 4.6 and Opus 4.6 without extended context at 200K; `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` holds native-1M models to 200K (the window setting cannot lift that hold).

How it relates to the other knobs: `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` is a percentage of the window and can only lower the trigger; `DISABLE_AUTO_COMPACT=1` (or the `autoCompactEnabled` setting, both on the settings reference) turns automatic compaction off and wins over any window; `idleCompaction` is a separate idle-time trigger. Details in [CC-env-vars-reference.md](../configuration/CC-env-vars-reference.md#context--token-control).

### How the window and the percentage combine

They are two settings, and they stack rather than override each other. The window (set by `/autocompact`, `--autocompact`, `autoCompactWindow` or `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, in tokens) is how full the context may get; the [env-vars page][cc-env-vars] defines `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` as "the percentage (1-100) of the auto-compact window at which auto-compaction triggers", which "can't raise the threshold" (read 2026-11-23). So the trigger is roughly window × percentage: with `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=50`, a 400K window compacts near 200K and a 1M window near 500K. The model-config page adds that the status line's `used_percentage` is measured against the full context window, so while a window is set it does not show when compaction will run. Owner observation (2026-11-23, CC v2.1.330, one sample): with the percentage at 50, the "compact earlier" prompt said a 400K window would summarize a 205K conversation on the next message, which fits the stacked reading; the prompt itself shows the window, not the effective trigger.

### When `/autocompact` first appeared

The [commands page][cc-commands] gives v2.1.221 as the minimum version. The CC CHANGELOG (read 2026-11-23, through v2.1.330) has no "added `/autocompact`" entry; its oldest mention is v2.1.234 (dialogs that open mid-turn), so the command shipped between v2.1.221 and v2.1.234 (inferred, not stated). Later entries: v2.1.280 footer hint, v2.1.285 `/autocompact 200k` advice for gateways that stop at 200K, v2.1.288 per-model saving, v2.1.296 subagent `autoCompactWindow`, v2.1.304 `k`/`M` suffixes on the env var, v2.1.323 unknown model IDs assumed 1M, v2.1.326 slider, v2.1.329 a fix for the percentage variable staying in effect after removal from settings. The usage prompt that suggests compacting earlier (offering, for example, a 400K window) is not in the changelog through v2.1.330 (owner observation, 2026-11-23).

**Related guidance.** Anthropic's [session-management article][cc-session-mgmt] (Thariq Shihipar, 2026-04-15) does not cover the window settings; it advises a new session per task, rewinding instead of correcting after a failed attempt, compacting proactively with a note on what comes next rather than letting auto-compaction fire mid-task, and subagents for steps with large intermediate output. A community guide ([bogdanmatasaru/claude-code-guide][community-autocompact], not affiliated with Anthropic, last verified against CC v2.1.226 on 2026-08-10) describes the same settings; the first-party pages above are the authority.

## References

- [CC Model Configuration — Extended context](https://code.claude.com/docs/en/model-config#extended-context)
- [CC Commands: `/autocompact`][cc-commands]
- [CC Model Configuration: auto-compact window][cc-autocompact]
- [CC Environment variables][cc-env-vars] — `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` definition (read 2026-11-23)
- [Using Claude Code: session management and 1M context][cc-session-mgmt] — Anthropic article, 2026-04-15
- [Auto-compact guide][community-autocompact] — community guide, not affiliated with Anthropic (verified against v2.1.226)
- [CC Costs](https://code.claude.com/docs/en/costs)
- [Long-context pricing][pricing-long-context]
- [Rate limits](https://platform.claude.com/docs/en/api/rate-limits)
- [CC-fast-mode-analysis.md](../configuration/CC-fast-mode-analysis.md) — fast mode pricing tiers
- [CC-model-provider-configuration.md](../configuration/CC-model-provider-configuration.md) — model env vars
- [Long-Context Isn't the Answer][hlyr-long-ctx] — hlyr.dev, Kyle, 2026-03-23
- [Context-Efficient Backpressure][hlyr-backpressure] — hlyr.dev, Dex, 2025-12-09
- [How Long Contexts Fail][breunig-ctx] — dbreunig.com, Drew Breunig, 2025-06-22 (practitioner taxonomy)
- [Less is More (arXiv 2411.15399)][arxiv-less-is-more] — tool-count example, paper
- [LLMs Get Lost In Multi-Turn Conversation (arXiv 2505.06120)][arxiv-lost-multiturn] — multi-turn degradation, paper
- [Context Engineering for AI Agents in Production][splunk-ctx] — Splunk, 2026-08-11, vendor blog (pointer only)

[cc-commands]: https://code.claude.com/docs/en/commands
[cc-subagents]: https://code.claude.com/docs/en/sub-agents#subagent-auto-compact-window
[cc-autocompact]: https://code.claude.com/docs/en/model-config#set-the-auto-compact-window
[cc-model-config]: https://code.claude.com/docs/en/model-config#extended-context
[pricing-long-context]: https://platform.claude.com/docs/en/about-claude/pricing#long-context-pricing
[hlyr-long-ctx]: https://www.hlyr.dev/blog/long-context-isnt-the-answer
[hlyr-backpressure]: https://www.hlyr.dev/blog/context-efficient-backpressure
[cc-ralph]: ../agents-skills/CC-ralph-enhancement-research.md
[cc-mem-ace]: CC-memory-system-analysis.md#context-engineering-workflow-ace-fca
[breunig-ctx]: https://www.dbreunig.com/2025/06/22/how-contexts-fail-and-how-to-fix-them.html
[arxiv-less-is-more]: https://arxiv.org/abs/2411.15399
[arxiv-lost-multiturn]: https://arxiv.org/abs/2505.06120
[splunk-ctx]: https://www.splunk.com/en_us/blog/artificial-intelligence/context-engineering-production-agents.html
[cc-env-vars]: https://code.claude.com/docs/en/env-vars
[cc-session-mgmt]: https://claude.com/resources/articles/using-claude-code-session-management-and-1m-context
[community-autocompact]: https://bogdanmatasaru.github.io/claude-code-guide/guides/auto-compact
