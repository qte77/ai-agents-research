---
title: AIDE² — Weco AI's Recursive Self-Improvement Experiment
source: https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement
purpose: Analysis of Weco AI's AIDE² experiment and its arXiv technical report, where an outer-loop agent rewrote the inner-loop AIDE research-agent's code across 100 iterations.
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

AIDE is Weco AI's autonomous research agent that optimizes code against
evaluation metrics; the original version won OpenAI's MLE-Bench competition.
For this experiment the team built **AIDE0**, a simplified version stripped
of ML-specific features so it generalizes across task families (ML
engineering, combinatorial optimization, system/harness engineering). Weco's
blog post ([weco.ai/blog][blog], published 2026-07-14) and a technical
report on arXiv ([2609.26457][paper], submitted 2026-09-22) both describe
**AIDE²**: an outer-loop agent (AIDE-human, their two-year-old hand-tuned
production agent) that proposed rewrites of the inner-loop AIDE0's own code
across 100 iterations over an eight-day autonomous run, keeping only
verified improvements.

**No public code repository for AIDE² was found** — neither the blog post
nor the arXiv abstract page links one, matching the "results published,
code not yet released" pattern already tracked for HarnessX in this corpus
(see [Cross-References](#cross-references)). The **original** AIDE (the
system AIDE² evolved from) is open-source at [WecoAI/aideml][aideml] (MIT).

## The AIDE² Method

Per the blog post: the inner loop optimized code on heterogeneous tasks with
public/private score splits, under fixed dollar-cost budgets (to prevent
brute-force search). The outer loop's proposals were evaluated against that
budget, and "about nine in ten proposed changes were rejected." The system
discovered **seven successive improved versions of AIDE** after 100
outer-loop iterations, each reported as stronger than the last under the
same cost budget.

## Reported Results — attributed per source, not blended

The blog post and the arXiv abstract report **different numbers for
overlapping claims**; both are given here rather than reconciled, per this
repo's citation rules.

- **MLE-Bench deltas (blog, verbatim)**: paired by task vs. AIDE0 —
  "+0.053 (p = 0.0024) for AIDE47, +0.042 (p = 0.0041) for AIDE85." No
  numeric deltas for ALE-Bench or WeatherBench 2 were given in the fetched
  text beyond naming them as held-out generalization benchmarks.
- **Reward-hacking rate, kernel test cases (blog, verbatim)**: "AIDE0
  reward hacks on 63% of the test cases ... and 34% for AIDE85. Our
  hand-tuned AIDEhuman only matches AIDE47 at 42%." (AIDE47's own rate was
  elided in the fetched text and is not stated here.)
- **Reward-hacking rate (arXiv abstract, paraphrased by the fetch tool, not
  independently re-quoted)**: reported as dropping from 55% to 32% — a
  different figure than the blog's kernel-specific 63%→34%, likely a
  different benchmark scope or aggregate; **not reconciled here**.
- **Prompt/context compression (blog, verbatim)**: "reduced the prompt size
  by 16×"; elsewhere, "the compression it found averages 16× on the full
  prompt against naive history concatenation."
- **Ignition-test efficiency (blog, verbatim)**: "AIDE47 reaches it in
  around 20 steps, whereas the hand-built one, AIDEhuman, needs about 40
  steps."

## Stated Limitations (the authors' own hedges, blog, verbatim)

- "We do not think this is strong enough evidence of ignition" (i.e.,
  whether discovered agents improve the outer loop itself).
- "We believe we are not near an intelligence explosion with the current
  system."
- The evolved agent has "fairly complex logic," making it "very difficult
  to understand how the system works."
- The authors classify this result as **"Level 1" RSI**, not the higher
  stages that would require self-acceleration.

## Corpus Relevance

This is a single-vendor blog claim paired with a very recent (submitted
2026-09-22) arXiv technical report, with no independent reproduction found
and an unreconciled numeric discrepancy between the two first-party sources
themselves. It belongs alongside this corpus's other "results without a
released harness" entries (HarnessX) and its self-evolving-harness entries
(MOSS, Raven) as a comparison point, without itself being adoptable.

## Cross-References

- [harnessx-analysis.md][harnessx] — the same "paper claims ahead of public
  code" shape; both should be re-assessed if/when code ships.
- [moss-self-evolving-agent-analysis.md][moss] — a working, code-available
  self-evolution system using an external coding-agent CLI, in contrast to
  AIDE²'s own-code rewriting loop.

## Sources

| Source | Content |
|---|---|
| [Weco AI blog — "First evidence of recursive self-improvement"][blog] | Method, AIDE0/AIDE² description, all quoted quantitative claims, authors' own stated limitations — published 2026-07-14, accessed 2026-09-24 |
| [arXiv 2609.26457 — "Recursive self-improvement of AI research agents"][paper] | Title, authors (Dhruv Srikanth, Bingchen Zhao, Dixing Xu, Yuxiang Wu, Zhengyao Jiang), submission date (2026-09-22), abstract — accessed 2026-09-24 |
| [WecoAI/aideml repo][aideml] | Confirms the original AIDE is open-source (MIT); AIDE² itself has no linked repo |

[blog]: https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement
[paper]: https://arxiv.org/abs/2609.26457
[aideml]: https://github.com/WecoAI/aideml
[harnessx]: harnessx-analysis.md
[moss]: moss-self-evolving-agent-analysis.md
