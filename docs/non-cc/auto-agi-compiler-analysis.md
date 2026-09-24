---
title: AUTO — Compiling Agent Behavior to Deterministic WASM
purpose: Assess RightNow AI's AUTO compiler and its self-published "Auto — The AGI Compiler" paper
source: https://github.com/RightNow-AI/auto
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

[AUTO][repo] ("the agi compiler") is a research prototype from RightNow AI
that records LLM agent execution traces, identifies which decision spans
behave deterministically across replays, and compiles the deterministic
spans into small, capability-confined WebAssembly binaries (`.cbin`
artifacts, described as having zero external imports and measured resource
bounds) that run without the frontier model in the loop. Spans that are not
proven deterministic still fall back to the frontier model. The project
frames itself as treating "frontier models as interpreters" and building a
compiler on top of them, with three layers: capturing agent traces,
compiling deterministic portions into small specialist models, and emitting
the sandboxed WASM artifacts. It is written in Rust and Apache-2.0 licensed.

## The Paper's Claims (Self-Reported, Not Independently Reviewed)

The repo's own homepage links "Auto: The AGI Compiler"
([arXiv:2607.04542][paper], Jaber Jaber and Osama Jaber, submitted
2026-07-05). Its abstract-level claims, fetched from the arXiv listing page
today and reported here **as the authors' own figures on their own
AUTO-BENCH benchmark suite** — not independently re-run or peer-reviewed:

- 87.1% of 560 recorded agent execution spans exhibited deterministic
  behavior across replays (some task families reaching 100%).
- A 6.4x reduction in marginal cost (from 59 to 2 micro-dollars per item) on
  distribution-shifted benchmark streams, with 96.9% output parity on
  witnessed inputs and zero errors reported.
- The paper's own stated failure mode: loose determinism guards caused
  **silent mislabeling in 48.9% of compiled outputs** in their evaluation,
  and unfaithful "deopts" (fallback paths) prevented successful
  recompilation in some cases — the authors present this as evidence that
  calibration and reference fidelity are the load-bearing risk, not that the
  approach is safe by default.

## Repo Activity

Created 2026-07-05, last pushed 2026-07-07 — two days later — with no
further pushes recorded as of 2026-09-24 (today). 128 stars, 13 forks, 0 open
issues. Treat as dormant since its initial publication rather than under
active development.

## Sources

| Source | Content |
|---|---|
| [RightNow-AI/auto repo][repo] | README, architecture description, license (first-party) |
| [arXiv:2607.04542][paper] | Paper abstract and self-reported benchmark figures |
| GitHub API repo metadata, 2026-09-24 | Stars(128)/forks(13)/issues(0), Apache-2.0, dates (created/pushed) |

[repo]: https://github.com/RightNow-AI/auto
[paper]: https://arxiv.org/abs/2607.04542
