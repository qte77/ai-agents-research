---
title: AIDE² — Weco AI's Recursive Self-Improvement Experiment
source: https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement
purpose: Analysis of Weco AI's AIDE² experiment and its arXiv technical report, where an outer-loop agent rewrote the inner-loop AIDE research-agent's code across 100 iterations. Also covers RRSI and ROFT as comparison points in the self-improving-harness family.
created: 2026-09-24
updated: 2026-09-30
validated_links: 2026-09-30
---

**Status**: Assess

## What It Is

AIDE is Weco AI's autonomous research agent that optimizes code against
evaluation metrics; the blog post states it "previously took first place in
OpenAI's MLE-Bench" (a machine-learning-engineering agent benchmark, not a
head-to-head competition event). For this experiment the team built
**AIDE0**, a simplified version stripped
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

The blog post and the arXiv abstract report reward-hacking numbers that
look like the same claim at a glance but are **not** — different task
families, cited separately below rather than merged, per this repo's
citation rules.

- **MLE-Bench deltas (blog, verbatim)**: paired by task vs. AIDE0 —
  "+0.053 (p = 0.0024) for AIDE47, +0.042 (p = 0.0041) for AIDE85." No
  numeric deltas for ALE-Bench or WeatherBench 2 were given in the fetched
  text beyond naming them as held-out generalization benchmarks.
- **Reward-hacking rate, KernelBench (blog, verbatim)**: "AIDE0 reward
  hacks on 63% of the test cases. The discovered agents hack much less
  often, 42% for AIDE47 and 34% for AIDE85."
- **Reward-hacking rate, a separate held-out task family (arXiv abstract,
  verbatim)**: "the discovered agents also exhibit reduced reward hacking,
  a property the loop never explicitly optimized for: the rate falls from
  55% to 32% during the run, 7 percentage points below the human-engineered
  agent." This is explicitly a **different, held-out task family** from the
  blog's KernelBench-specific 63%→34%/42% figures — the two are not the
  same measurement and are not blended here.
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
2026-09-22) arXiv technical report, with no independent reproduction found;
its two first-party sources report similarly-worded but distinct
reward-hacking figures for different task families, easy to conflate if
not read carefully. It belongs alongside this corpus's other "results
without a released harness" entries (HarnessX) and its self-evolving-harness
entries (MOSS, Raven) as a comparison point, without itself being adoptable.

## RRSI: Regularized Recursive Self-Improvement of Agent Harnesses (added 2026-09-30)

[RRSI][rrsi-repo] (Google Research, **Apache-2.0**, LICENSE file confirmed, 977 stars/80 forks, pushed
2026-09-23, created 2026-09-16) is the code-available counterpart AIDE² lacks: a released harness-search
framework accompanying [arXiv 2609.24972][rrsi-paper]. Where AIDE² has an outer loop rewrite an inner
agent's own source, RRSI evolves the harness *around* a frozen policy model (Claude Opus 4.8 on Vertex
AI, pinned in `domains/coding/rrsi.json`) across three instances (a terminal agent, a document-work
agent, an engineering-design agent), regularizing the search so it does not overfit the evolve set: an
annealed edit budget, a critic that screens for suite-specific logic before evaluation, a noise-adjusted
floor, and a cost rule requiring added inference tokens to be paid for by measured gain. Two mechanisms
make it directly relevant to this arc's harness gaps rather than just a sibling self-improvement paper:

- **Versionable (fills gap 9, Harness · Versionable).** "Candidates in git worktrees. Every candidate
  harness is drafted, screened and evaluated in its own worktree on a branch off `evolve/<domain>`;
  accepting one fast-forwards the branch, so the incumbent is always a commit" (README, verbatim). The
  harness-pattern, dynamic-workflow and Ralph docs this arc scored in row C never described versioning
  the harness's own state — RRSI's git-worktree-per-candidate design is first-party evidence that a
  harness search process can be made git-native.
- **Traceable.** "Evidence you can audit. The edit history records, per edit, the component, the
  hypothesis, the measured score and cost change and the verdict; the prompts the proposer, analyst and
  critic receive are plain files" (README, verbatim) — a per-edit lineage record, not just aggregate
  benchmark numbers.

**Rubric** (scored 2026-09-30, [README][rrsi-repo]): Shared: n/a (a single research harness's own
evolution loop, not a multi-agent shared store); Distributed: no data (the search runs against
benchmark harnesses; no multi-machine sync is documented); Reproducible: partial (the policy, proposer,
analyst and critic models are pinned by name in `rrsi.json`, and accepted edits are commits, but the
proposer's LLM-driven edit proposals are not seeded/deterministic run-to-run); Adaptable: yes ("prompts,
control flow, configuration, context management, tools, skills, memory and sub-agents may all be
modified" — an explicitly open edit space, with a `Domain` adapter per target agent); Versionable: yes
(git worktrees + branch fast-forward, as above); Traceable: yes (per-edit audit record, as above).

## ROFT: Retrospection-Only Fine-Tuning (added 2026-09-30)

[ROFT][roft-paper] ("Shockingly Simple Self-retrospection Improves Agentic Models Without RL," Light et
al., submitted 2026-09-28, **CC BY 4.0**) is a training-time method rather than a harness-search system:
an agent attempts a task, observes feedback, writes a retrospective explanation of what happened, and is
then fine-tuned by ordinary next-token prediction on those retrospectives only — no RL, no external
instruction signal. The authors report solve rates of "49.2% and 26.8% ... after 20 updates" on held-out
software-engineering benchmarks (self-reported, not independently reproduced) and that the method can
bootstrap learning even from a set of entirely-failed initial attempts. **No code repository URL is
given anywhere on the abstract page** (checked 2026-09-30), matching the "results published, code not
yet released" pattern this corpus already tracks for [HarnessX][harnessx] and AIDE² above.

ROFT and RRSI both sit in the "evolve the loop around a frozen model" family this doc catalogs, but at
different layers: RRSI restructures the harness's prompts/tools/control-flow and versions the result in
git; ROFT changes the *model's weights* via fine-tuning on self-generated text and versions nothing —
there is no artifact analogous to RRSI's per-edit commit history. No corpus entry yet exists for
ModularRSI or Skill Self-Play (both named in this arc's backlog research); nothing is claimed about them
here.

**Rubric** (scored 2026-09-30, [arXiv abstract][roft-paper]): Shared: n/a (a single-agent training
method); Distributed: n/a (a training procedure, not a deployed system); Reproducible: no (no code,
weights, or seed information found — the paper reports results, not a rebuild path); Adaptable: no data
(the abstract does not describe extension points beyond the method itself); Versionable: no (fine-tuned
weights are not described as snapshotted, diffable, or rolled back); Traceable: no data (no audit-trail
or lineage mechanism is described for the retrospective explanations themselves).

## Cross-References

- [harnessx-analysis.md][harnessx] — the same "paper claims ahead of public
  code" shape; both should be re-assessed if/when code ships.
- [moss-self-evolving-agent-analysis.md][moss] — a working, code-available
  self-evolution system using an external coding-agent CLI, in contrast to
  AIDE²'s own-code rewriting loop.
- [orcareplay-analysis.md](orcareplay-analysis.md) — a different kind of "record the run" tool: OrcaReplay
  replays a trace for human debugging and model comparison; it does not evolve the harness the way RRSI
  does.

## Sources

| Source | Content |
|---|---|
| [Weco AI blog — "First evidence of recursive self-improvement"][blog] | Method, AIDE0/AIDE² description, all quoted quantitative claims, authors' own stated limitations — published 2026-07-14, accessed 2026-09-24 |
| [arXiv 2609.26457 — "Recursive self-improvement of AI research agents"][paper] | Title, authors (Dhruv Srikanth, Bingchen Zhao, Dixing Xu, Yuxiang Wu, Zhengyao Jiang), submission date (2026-09-22), abstract — accessed 2026-09-24 |
| [WecoAI/aideml repo][aideml] | Confirms the original AIDE is open-source (MIT); AIDE² itself has no linked repo |
| [google-research/rrsi README][rrsi-repo] | RRSI method, architecture, git-worktree/audit-log mechanisms, pinned-model config — accessed 2026-09-30 |
| `gh api repos/google-research/rrsi`, 2026-09-30 | License (Apache-2.0), stars (977), forks (80), created/pushed dates |
| [arXiv 2609.24972 — RRSI paper][rrsi-paper] | Title, submission date (2026-09-21 per the repo's own update note) — accessed 2026-09-30 |
| [arXiv 2609.35741 — ROFT abstract page][roft-paper] | Title, authors, submission date (2026-09-28), license (CC BY 4.0), method summary, reported solve-rate figures, confirmation that no code URL is given — accessed 2026-09-30 |

[blog]: https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement
[paper]: https://arxiv.org/abs/2609.26457
[aideml]: https://github.com/WecoAI/aideml
[harnessx]: harnessx-analysis.md
[moss]: ../agents/moss-self-evolving-agent-analysis.md
[rrsi-repo]: https://github.com/google-research/rrsi
[rrsi-paper]: https://arxiv.org/abs/2609.24972
[roft-paper]: https://arxiv.org/abs/2609.35741
