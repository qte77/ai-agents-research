---
title: FM-Bench — Long-Horizon Competitive-Agent Benchmark
purpose: A football-club-management benchmark that tests LLM agents on long-horizon decision-making with cumulative consequences, in both isolated and competitive multi-agent settings.
source: https://arxiv.org/abs/2608.18423
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

An arXiv paper, "FM-Bench: A Benchmark for Long-Horizon Management with Competing
Agents" (arXiv:2608.18423, v1 submitted 2026-08-19, revised as v2 2026-08-20, cs.AI;
authors Tianyou Wang, Chongyang Gao, Kezhen Chen, Dong Chen, Yinghao He, Donghan Li,
Wangcheng Xu, Hongjiu Zhang, Chi Li). FM-Bench has an LLM agent run a football club for
**20 in-game years** through **26 tools** and roughly **340–400 decision stops**,
testing whether a model can sustain effective decision-making across a horizon long
enough for early decisions to have cumulative, compounding consequences — a dimension
most single-episode agent benchmarks don't exercise.

## What It Measures

Within the simulation, the agent must:

- Draft a squad within a fixed budget.
- Trade and negotiate player contracts.
- Invest in facilities and youth development (long-horizon payoff, not immediate).
- Configure lineups and tactics.
- Answer to a simulated board for results and spending — an accountability signal
  distinct from raw task completion.

The benchmark runs models in two modes: **isolated** (one agent per club, no direct
competition) and **arena** (multiple agent-run clubs competing in the same league),
making it one of the few agent benchmarks that measures long-horizon management and
competitive multi-agent dynamics in the same harness.

## Results (paper-claimed)

15 frontier models were compared. The paper's headline finding is that **"neither
scale, price, nor vendor predicts the order"** of model performance on this benchmark —
model ranking did not track the usual proxies for capability. Stronger performers were
instead distinguished by behavioral patterns: the timing of long-term investment (youth
development, facilities) and cash-management discipline, rather than by raw compute or
list price.

## Corpus Relevance

FM-Bench adds a **long-horizon, cumulative-consequence, competitive-multi-agent**
dimension that is a genuine gap in this corpus's existing benchmark coverage — see
[agent-evaluation-metrics-landscape.md](agent-evaluation-metrics-landscape.md) (task
completion / reasoning / tool-use / safety metrics) and
[mas-benchmarking-best-practices.md](mas-benchmarking-best-practices.md) (production MAS
benchmarking practices), neither of which yet has an entry for a benchmark whose horizon
is measured in hundreds of sequential decisions with compounding state rather than a
single task episode. Flagged here for the main session as a candidate addition to
either of those landscape docs; not added to them in this batch since neither is a
target of this batch.

## Sources

| Source | Content |
|---|---|
| [arXiv:2608.18423 abstract][paper-abs] | Title, authors, abstract, v1/v2 submission dates, subject categories |

[paper-abs]: https://arxiv.org/abs/2608.18423
