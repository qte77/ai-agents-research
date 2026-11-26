---
title: Code Correctness Is Linearly Decodable from LLM Hidden States Before Generation
purpose: Third-party interpretability study on pre-generation code-correctness probing and its relevance to coding-agent repair heuristics
source: https://arxiv.org/abs/2606.14530
created: 2026-07-23
updated: 2026-11-26
validated_links_on: 2026-07-23
status: assess
---

## What It Is

Single-author (Carlo Di Cicco) empirical interpretability study probing
Qwen3-4B-Instruct-2507's hidden states. It shows that the correctness of a
model's first-attempt code is linearly decodable from the hidden state at the
prompt's final token — before any code tokens are generated. arXiv:2606.14530,
currently v3 (submitted 2026-07-16; cs.LG, no institutional affiliation listed
on the abstract page). v1 (2026-06-12) carried the title "...Pre-Generation
Probing and Repair Geometry"; v2 followed 2026-07-10. The "Repair Geometry"
claim was dropped from the title by v3, whose abstract says the
repair-geometry question could not be tested because successful repairs
after a failed first attempt were too rare (the covariate-control finding
below belongs to v1; the v2 title is unverified).

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
  for prompt length. (The superseded v1 abstract reported 0.931 / 0.911 /
  0.754 for the same three quantities; the 0.881/0.842/0.657 triple above is
  the current v3 one, confirmed against the arXiv abstract page and the repo
  README.)

## Repair-Geometry Analysis (v1 only; no finding in v3)

The v1 abstract (2026-06-12) analyzed 236 cleaned repair cases (failing
attempt to its repair) and reported a statistically detectable contrastive
direction that did not survive residualization against repair-context
covariates, read as a correlate of repair success rather than an isolated
repair-comprehension feature. The current v3 abstract makes no repair-geometry
finding: it says the question could not be tested because successful repairs
were too rare. Specific task counts for that data starvation (reported
secondhand) are not on the abstract page (unverified).

## Repair Implications

Pre-generation correctness probing is directly applicable to coding-agent
repair-trigger design: if a linear probe on hidden states can flag
likely-incorrect code before any tokens are generated, a harness could use it
as a cheap pre-check for deciding when to trigger self-repair or
re-generation — without first executing or evaluating the generated code. The
current version makes no repair-geometry finding, so nothing there is actionable.

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
