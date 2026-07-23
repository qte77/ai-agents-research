---
title: Code Correctness Is Linearly Decodable from LLM Hidden States Before Generation
purpose: Third-party interpretability study on pre-generation code-correctness probing and its relevance to coding-agent repair heuristics
source: https://arxiv.org/abs/2606.14530
created: 2026-07-23
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Assess

## What It Is

Single-author (Carlo Di Cicco) empirical interpretability study probing
Qwen3-4B-Instruct-2507's hidden states. It shows that the correctness of a
model's first-attempt code is linearly decodable from the hidden state at the
prompt's final token — before any code tokens are generated. arXiv:2606.14530,
currently v3 (submitted 2026-07-16; cs.LG, no institutional affiliation listed
on the abstract page). v1 (2026-06-12) carried the title "...Pre-Generation
Probing and Repair Geometry"; v2 followed 2026-07-10. The "Repair Geometry"
claim was dropped from the title by v3, consistent with the paper's own
finding below that this secondary analysis doesn't hold up under covariate
control.

## Probing Method

- Model: Qwen3-4B-Instruct-2507 — **not** a Claude/Anthropic model.
- Benchmark: 444 LiveCodeBench tasks (easy/medium/hard tiers).
- Technique: linear probing (logistic-regression decoder) on the hidden state
  at the prompt's final token, plus residualization to separate the
  correctness signal from a prompt-length confound, with nested
  cross-validation to guard against leakage.

## Results

- Held-out AUC **0.881** (±0.008) raw.
- **0.842** (±0.010) after residualizing out prompt length.
- vs. **0.657** (±0.014) for a prompt-length-only baseline.
- The correctness signal is present pre-generation and is not merely a proxy
  for prompt length. (An earlier pass surfaced a possible v1 figure of 0.931;
  it could not be corroborated against primary text and is omitted here — the
  0.881/0.842/0.657 triple above is the one confirmed against both the arXiv
  abstract and the repo README.)

## Repair-Geometry Analysis (Secondary, Weaker)

236 repair attempts (failing attempt to its repair) were analyzed for a
directional shift in hidden-state space. A statistically detectable shift
exists, but it is confounded by repair-context covariates and does not hold
up as evidence of standalone "repair comprehension" once controlled — the
paper is explicit that this analysis is underpowered/inconclusive for a
strong repair-geometry claim.

## Repair Implications

Pre-generation correctness probing is directly applicable to coding-agent
repair-trigger design: if a linear probe on hidden states can flag
likely-incorrect code before any tokens are generated, a harness could use it
as a cheap pre-check for deciding when to trigger self-repair or
re-generation — without first executing or evaluating the generated code. The
repair-geometry finding is weaker and, per the authors, not yet actionable.

## Corpus Relevance

This is third-party academic research on a non-Anthropic model, placed in
`model-internals/` because the directory is the corpus home for model-level
interpretability research generally. Its two existing docs,
[CC-emotion-vectors-interpretability.md](CC-emotion-vectors-interpretability.md)
and
[CC-first-party-interpretability-index.md](CC-first-party-interpretability-index.md),
are both Anthropic first-party — this doc is not. Its relevance to Claude
Code is operational rather than provenance-based: the probing technique
generalizes to any coding agent's repair-trigger heuristics, regardless of
which model produced the hidden states.

Paper license: CC BY 4.0. Companion code/data repo
([CarloDiCicco/ReasoningLab][repo]): Apache-2.0, verified against the repo's
own `LICENSE` file (not just a badge).

## Sources

| Source | Content |
|---|---|
| [arXiv:2606.14530 (v3)][arxiv] | Abstract, AUC figures, version history |
| [ReasoningLab repo][repo] | Code, data, reproduction scripts; license |

[arxiv]: https://arxiv.org/abs/2606.14530
[repo]: https://github.com/CarloDiCicco/ReasoningLab
