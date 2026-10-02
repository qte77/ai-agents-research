---
title: AIDE² — Weco AI's Recursive Self-Improvement Experiment
source: https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement
purpose: Analysis of Weco AI's AIDE² experiment and its arXiv technical report, where an outer-loop agent rewrote the inner-loop AIDE research-agent's code across 100 iterations. Also covers RRSI and ROFT as comparison points in the self-improving-harness family, plus two further harness-subject entries, FineEnvs multi-harness RL training and the agentic meta-reasoning paper.
created: 2026-09-24
updated: 2026-10-02
validated_links: 2026-10-02
status: assess
---

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

## FineEnvs: Training a Small Model Across Agent Harnesses (added 2026-10-02)

[The multi-harness RL guide][fineenvs-space] is a Hugging Face Space (`sdk: docker`, canonical id
`FineEnvs/multi-harness-rl`; the `AdithyaSK/...` URL in earlier notes redirects here) published by the
same maintainer as [github.com/adithya-s-k/FineEnvs][fineenvs-repo], which its own README names as the
companion repo ("Source lives in FineEnvs under `content/articles/multi-harness-rl/`"). The GitHub repo
is **Apache-2.0** (confirmed via `gh api repos/adithya-s-k/FineEnvs`: 278 stars, 37 forks, created
2026-05-01, pushed 2026-10-02). The Space's own `LICENSE` file is separate and reads "Copyright (c) 2024
Thibaud Frere" under **CC BY 4.0** — inherited from the [research-article-template][template] scaffold
the article is built on; the README itself attributes "the source code and technical implementation" to
that template, so this CC BY 4.0 grant most plausibly covers the article's prose/template boilerplate,
not the Apache-2.0 training code in the companion repo. This split is stated here rather than resolved,
since neither page says explicitly which license governs FineEnvs' own added article text.

The Space card tags `openenv`, `harbor`, `grpo`, `trl`; the article chapters (`why-multi-harness.mdx`,
`training.mdx`), fetched directly, confirm each is load-bearing rather than decorative. On **OpenEnv**
(verbatim): "We built this on OpenEnv ..., around a capture proxy that sits between the harness and the
model. Every call the agent makes passes through the proxy, which records the prompt and completion
tokens as the model saw and produced them, with their log probabilities." On **Harbor** (verbatim): "the
Harbor integration serves Harbor's containerized tasks as OpenEnv environments, so the harness and the
sandbox become settings you choose per rollout." On the training recipe (verbatim): "Async GRPO
[@shao2024deepseekmath] in TRL for 1,000 steps," run across the harnesses **OpenCode, Claude Code, Codex
and Mini-SWE-Agent**, "each GRPO group of eight rollouts uses one of the four harnesses."

The reported experiment trained [LFM2.5-2.6B][lfm-model] on 1,000 SmolDataEnvs tasks, once in OpenCode
alone and once across the four harnesses, on "Two H100s per run on the Hugging Face cluster, and one
E2B sandbox per rollout." The headline result (verbatim, `conclusions.mdx`): "LFM2.5-2.6B went from
42.2% to 54.2% pass@1, with gains under all four harnesses," and the multi-harness model "used 31% fewer
tool calls on held-out tasks that both it and the base model solved, with savings under every harness,"
while the OpenCode-only run scored best only inside OpenCode (58% vs. 50% for multi-harness). The
authors' own hedge (verbatim): "These are small experiments on one task family, with one seed per setup
and unequal data and compute exposure. They support the gains over the base model, but do not establish
a general ranking of harness mixes." A separate verbatim reproducibility caveat: "The reported LFM runs
used Harbor for both policies and E2B sandboxes. The current tutorial uses Daytona and includes native
OpenCode as a separate comparison, so it is not an exact replay of those historical runs."

This is a different kind of harness-level intervention from RRSI, ROFT and AIDE² above: instead of
evolving the harness's own code or a model's weights, it trains one model to work across several
*unmodified* harnesses, using harness diversity itself — not a search or rewrite loop — as the training
signal.

**Rubric** (scored 2026-10-02, [article][fineenvs-space] + [repo][fineenvs-repo]): Shared: partial (the
Space's documented review mode lets allow-listed reviewers — the `REVIEWERS` list — comment on and
suggest edits to the article, one JSON thread file each, with only the owner able to accept or reject; a
defined but gated multi-writer flow; the companion repo's `CONTRIBUTING.md` also documents a PR flow
("open a PR adding a new numbered project folder"), which is rubric rule 6's cited contribution flow);
Distributed: partial ("Two H100s per run on the Hugging Face cluster" plus a per-rollout E2B/Daytona
sandbox, and `REPRODUCE.md` documents HF Jobs and Slurm instructions — multi-machine by design, though
the published Space itself runs as one Docker container); Reproducible: partial (models and the training
recipe are named and version-linked — LFM2.5-2.6B, Async GRPO in TRL — and a `REPRODUCE.md` exists, but
the authors state the current tutorial "is not an exact replay" of the reported runs, training draws on
async/stale weights, and each run used "one seed"); Adaptable: yes (harness, sandbox and trainer are each
a per-rollout setting, per the Harbor-integration quote above, and the guide itself demonstrates swapping
all three — E2B vs. Daytona sandboxes, OpenCode-only vs. four-harness training); Versionable: yes
(training code is in a git repo, and the derived dataset is published and versioned on the Hub as
[SmolDataEnvs-multiharness-sft][sft-dataset]); Traceable: yes (the capture proxy records "the prompt and
completion tokens as the model saw and produced them, with their log probabilities," and a published
`reward-group-audit.json` (linked in-text as `/data/reward-group-audit.json`, served by the running
Space) is reported, verbatim, to have "found no formula mismatches and no bonus on wrong answers").

## Agentic Meta-Reasoning: An Inference-Time Harness Controller (added 2026-10-02)

[arXiv 2609.38147][meta-reasoning], "Thinking Before Thinking: Scaling Agentic Inference Through
Meta-Reasoning" (Dahal, Bakhtin, Cohen, Chen, Wu, Fergus, Yih, Synnaeve, Salakhutdinov, Arora, Weston,
Goyal; submitted 2026-09-29), is a **paper-only** entry: the abstract page lists no code repository, no
project page, and no author affiliation (checked 2026-10-02 — the page's only metadata field beyond
authors and abstract is `Subjects: Artificial Intelligence (cs.AI)`; no `Comments:` field is present).
No affiliation is stated anywhere on the page, so none is given here.

Per the abstract (verbatim): it introduces "agentic meta-reasoning, an inference-time harness that makes
[control] choices an explicit and structured reasoning process. Workers carry out the task-level
computation, while a controller consolidates what the run has established, explores next options,
assesses what each option is worth under the remaining budget, and dispatches the chosen work with
context drawn from persistent memory. Between decisions the controller carries only a compact account of
the run rather than replaying its full history."

Reported results (verbatim, self-reported — no independent reproduction found): "On ProgramBench, which
tests long-horizon agentic capability through program reconstruction, meta-reasoning achieves 71.5% with
GPT-5.5 against 58.0% for Codex; with Opus 4.8 it achieves 67.2% against 65.5% for Claude Code. On the
other benchmarks, spanning abstract reasoning, multi-domain long-horizon reasoning, and proof generation,
it gains between 3.6 and 4.2 points over direct control, averaged across three frontier models." The
abstract hedges its own result: "its overhead can hurt at small budgets."

This bears on two subjects in the arc: it is a harness (an inference-time control loop evaluated against
"production coding agents and research harnesses," including Claude Code and Codex, as baselines), and
its "compact account of the run" plus "context drawn from persistent memory" is a context-management
design — a compaction/resumption strategy for long-running agent work. It does not join RRSI/ROFT's
"evolve the loop" family: the controller is a runtime component the paper describes running *within* an
agent session, not a search process that edits or retrains the harness itself.

**Rubric** (scored 2026-10-02, [arXiv abstract][meta-reasoning]; paper only, no code found. Shared and
Distributed are `n/a` because a single-session controller makes them meaningless (rubric rule 5);
properties that would need a shipped artifact are `no data`): Shared: n/a (a single-run controller directing workers within one session, not a
multi-agent shared store); Distributed: n/a (an inference-time technique over one model session; no
deployed multi-machine service is described); Reproducible: no data (no code, model/version pins, or seeds
are published); Adaptable: no data (no extension points are documented; paper only); Versionable: no data (no published artifact to version); Traceable: no data (the
abstract's "artifact-graph analysis" of run reuse gestures at lineage, but nothing on the abstract page
confirms it as an exposed, citable trace rather than an internal post-hoc analysis the authors ran for
the paper).

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
| [FineEnvs multi-harness-rl Space][fineenvs-space] | Space metadata (`sdk: docker`, tags), README (companion-repo pointer, review-mode mechanism), `LICENSE` file (CC BY 4.0, copyright Thibaud Frere) — accessed 2026-10-02 |
| `app/src/content/chapters/why-multi-harness.mdx`, `training.mdx`, `conclusions.mdx` (fetched raw from the Space) | Verbatim method description (OpenEnv capture proxy, Harbor integration, GRPO/TRL recipe), experiment setup, reported results and authors' own hedges — accessed 2026-10-02 |
| [adithya-s-k/FineEnvs repo][fineenvs-repo] | Companion training code; `gh api` confirms license (Apache-2.0), 278 stars, 37 forks, created 2026-05-01, pushed 2026-10-02 — accessed 2026-10-02 |
| [arXiv 2609.38147 abstract page][meta-reasoning] | Title, full author list (12), submission date (2026-09-29), full abstract verbatim, subject (cs.AI), confirmation of no code link/project page/affiliation field — accessed 2026-10-02 |

[blog]: https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement
[paper]: https://arxiv.org/abs/2609.26457
[aideml]: https://github.com/WecoAI/aideml
[harnessx]: harnessx-analysis.md
[moss]: ../agents/moss-self-evolving-agent-analysis.md
[rrsi-repo]: https://github.com/google-research/rrsi
[rrsi-paper]: https://arxiv.org/abs/2609.24972
[roft-paper]: https://arxiv.org/abs/2609.35741
[fineenvs-space]: https://huggingface.co/spaces/FineEnvs/multi-harness-rl
[fineenvs-repo]: https://github.com/adithya-s-k/FineEnvs
[template]: https://huggingface.co/spaces/tfrere/research-article-template
[lfm-model]: https://huggingface.co/LiquidAI/LFM2.5-2.6B
[sft-dataset]: https://huggingface.co/datasets/FineEnvs/SmolDataEnvs-multiharness-sft
[meta-reasoning]: https://arxiv.org/abs/2609.38147
