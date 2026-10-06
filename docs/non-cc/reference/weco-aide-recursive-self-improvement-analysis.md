---
title: AIDE² — Weco AI's Recursive Self-Improvement Experiment
source: https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement
purpose: Analysis of Weco AI's AIDE² experiment and its arXiv technical report, where an outer-loop agent rewrote the inner-loop AIDE research-agent's code across 100 iterations. Also covers RRSI and ROFT as comparison points in the self-improving-harness family, plus further harness-subject entries, FineEnvs multi-harness RL training, the agentic meta-reasoning paper, ActiveSaddler's curriculum-driven harness optimization, and the Sharpening Tax critique of RL post-training for agentic coverage.
created: 2026-09-24
updated: 2026-10-06
validated_links: 2026-10-06
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

**Rubric** (subject: harness, scored 2026-09-30, [README][rrsi-repo]): Shared: n/a (a single research harness's own
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

**Rubric** (subject: harness, scored 2026-09-30, [arXiv abstract][roft-paper]): Shared: n/a (a single-agent training
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

**Rubric** (subject: harness, scored 2026-10-02, [article][fineenvs-space] + [repo][fineenvs-repo]): Shared: partial (the
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

### Papers the article cites (added 2026-10-06)

The Space's `app/src/content/bibliography.bib` (fetched raw, 2026-10-06) lists **35 entries** (20 of them
carrying an arXiv `eprint`); the article's six chapters (`basics.mdx`, `introduction.mdx`, `openenv.mdx`,
`why-multi-harness.mdx`, `training.mdx`, `conclusions.mdx`, all fetched raw) cite most of these by `@key`
in the running text. The load-bearing ones — the article's own sibling multi-harness-training literature
and the benchmarks/algorithms its method depends on — are, one line each on what the article uses each
for:

- [Zhang et al., "Stop Comparing LLM Agents Without Disclosing the Harness"][fe-zhang] (arXiv:2605.23950) — the
  harness-disclosure position paper `basics.mdx` opens with to define what a harness is.
- [He et al., "Agent Lightning v1.0"][fe-he] (arXiv:2608.17528) — cited for the training-engine-owns-the-loop
  vs. agent-owns-the-loop distinction, and for its own reported SWE-bench Verified gain (41.8%→56.4%).
- [Yu et al., "OpenForgeRL"][fe-yu] (arXiv:2607.21557) — the closest sibling work; `basics.mdx` calls it
  "the strongest multi-harness results published so far."
- [KwaiKAT Team, "KAT-Coder-V2.5 Technical Report"][fe-kwaikat] (arXiv:2607.05471) — `why-multi-harness.mdx`
  quotes it verbatim for the central claim that a model trained on one harness "learns not 'how to solve
  the task' but 'how to solve the task under that particular harness's interface conventions.'"
- [Peng et al., "Orchard"][fe-peng] (arXiv:2605.15040) — cited for measuring cross-harness skill transfer.
- [Poolside, "Laguna M.1/XS.2 Technical Report"][fe-poolside] (arXiv:2605.27605) — cited for training data
  that deliberately includes trajectories from external harnesses to encourage generalization.
- [Xu et al., "Polar"][fe-xu] (arXiv:2605.24220) — "Agentic RL on Any Harness at Scale"; its converter code is
  vendored into the article's own Harbor-to-OpenEnv bridge.
- [Shao et al., "DeepSeekMath" (GRPO)][fe-shao] (arXiv:2402.03300) — the training algorithm used ("Async GRPO
  ... in TRL for 1,000 steps," already quoted verbatim above in this doc's FineEnvs section).
- [Kwon et al., "Efficient Memory Management... (vLLM)"][fe-kwon] (arXiv:2309.06180) — the inference server
  used to serve rollouts.
- [Jiménez et al., "SWE-bench"][fe-jimenez] (arXiv:2310.06770) and [Merrill et al., "Terminal-Bench"][fe-merrill]
  (arXiv:2601.11868) — the two benchmark families Harbor's own integration is built against.
- [Deng et al., "SWE-Bench Pro"][fe-deng] (arXiv:2509.16941) — cited in `training.mdx` for a per-harness
  model score ("Claude Opus 4.5 scores 45.9% on SWE-bench Pro"), not as a Harbor-evaluated benchmark.
- Model technical reports cited for how each names/handles harnesses in its own benchmark reporting:
  [Kimi K2][fe-kimik2] (arXiv:2507.20534), [Kimi K3][fe-kimik3] (arXiv:2607.24653),
  [Qwen3-Coder-Next][fe-qwen] (arXiv:2603.00729) and [DeepSeek-V3.2][fe-deepseekv32] (arXiv:2512.02556).

**Already in the corpus:** `git grep` across `docs/` for all 20 arXiv IDs in the bibliography (the
cited-in-text subset above plus the remainder, including arXiv:2504.00698 / Cohere Command A, which is in
the bibliography but not confirmed cited in the six chapters' running text) found exactly one hit:
arXiv:2402.03300 (DeepSeekMath/GRPO) also appears in
[kv-cache-serving-landscape.md](../infrastructure/kv-cache-serving-landscape.md) (checked 2026-10-06). The
other 19 IDs are not cited elsewhere in this corpus — this is the first time any of them is named here.
Not rubric-scored: these are citations *within* an already-covered article, not new standalone systems,
and none bears on the open Context·Reproducible cell in
[agent-substrate-reference-architecture.md](../../sdlc-lcm/agent-substrate-reference-architecture.md).

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

**Rubric** (subject: harness, scored 2026-10-02, [arXiv abstract][meta-reasoning]; paper only, no code found. Shared and
Distributed are `n/a` because a single-session controller makes them meaningless (rubric rule 5);
properties that would need a shipped artifact are `no data`): Shared: n/a (a single-run controller directing workers within one session, not a
multi-agent shared store); Distributed: n/a (an inference-time technique over one model session; no
deployed multi-machine service is described); Reproducible: no data (no code, model/version pins, or seeds
are published); Adaptable: no data (no extension points are documented; paper only); Versionable: no data (no published artifact to version); Traceable: no data (the
abstract's "artifact-graph analysis" of run reuse gestures at lineage, but nothing on the abstract page
confirms it as an exposed, citable trace rather than an internal post-hoc analysis the authors ran for
the paper).

## ActiveSaddler: Automated Curriculum Learning for Harness Optimization (added 2026-10-06)

[ActiveSaddler][activesaddler] ("ActiveSaddler: Automated Curriculum Learning for Agent Harness
Optimization," Park, Kim, Zhang, Han, Gao, Park, Yao, Fu, Nallipogu, Lin, Rühle; arXiv 2610.00906,
submitted 2026-10-01; project page [autosaddler-projectpage.github.io/activesaddler][activesaddler-page])
targets the training-scenario side of harness optimization rather than the harness-edit side RRSI and
AIDE² cover. Per the abstract (verbatim): "existing methods primarily optimize how the harness is updated
while largely fixing which training scenarios generate the feedback that drives those updates... we
formulate this missing dimension of harness optimization as an automated curriculum learning problem."
ActiveSaddler "models the evolving curriculum as a non-stationary bandit with dynamically instantiated
optimization targets," abstracting recurring failures into reusable "failure-pattern arms" and balancing
revisiting known weaknesses against exploring new ones as the harness itself changes under optimization.

Reported result (verbatim, self-reported, no independent reproduction found): "Experiments on GAIA2 and
Terminal-Bench 2.0 show that ActiveSaddler consistently discovers stronger harnesses, improving test
Pass@1 by 4.4 and 7.5 percentage points over the same harness optimizer using a scenario order fixed
before optimization, respectively." The comparison is against "the same harness optimizer" with a fixed
curriculum — i.e., the reported gain is attributable to the curriculum layer alone, holding the
underlying optimizer constant. The project page links a real code repository,
[microsoft/AutoSaddler][autosaddler-repo] (branch `feat/activesaddler`) — confirmed via `gh api`
(2026-10-06): **MIT license**, 237 stars, 18 forks, created 2026-05-11, pushed 2026-10-04. This is
code-available, unlike AIDE² and ROFT above.

This sits alongside RRSI, ROFT and AIDE² in the "evolve the loop around a frozen model" family, but at a
different layer again: RRSI edits the harness's prompts/tools/control-flow, ROFT fine-tunes weights on
self-generated retrospectives, and ActiveSaddler instead adapts *which training scenarios* drive whichever
harness-optimization loop sits underneath it — a curriculum wrapper, not a competing harness-edit method.
Not rubric-scored here: per the arc's gap-driven policy, this doesn't touch the open Context·Reproducible
cell in
[agent-substrate-reference-architecture.md](../../sdlc-lcm/agent-substrate-reference-architecture.md), and
Harness already has scored rows elsewhere in the corpus.

## Sharpening Tax: A Caution on Post-Training for Agentic Coverage (added 2026-10-06)

[Sharpening Tax in Post-Training][sharpening-tax] (Oh, Zeng, Qi, Zhmoginov, Lei, He, Phan, Kang,
Mirhoseini, Li; arXiv 2610.01509, submitted 2026-10-01) is not a harness-optimization method but a
caution relevant to the same "where should capability live" question RRSI and ROFT raise from the
harness/training-time sides respectively. Full abstract (verbatim): "An emerging hypothesis about
reinforcement learning (RL) post-training of large language models (LLMs) is that it merely sharpens
existing behaviors of a base model, improving single-shot accuracy at the cost of solution coverage.
Although this trade-off has been observed in math and coding tasks, it need not extend to agentic tasks,
where multi-turn tool use and interaction may require capabilities newly acquired during post-training.
Our surprising finding is that pre-trained LLMs, equipped with a light inference harness, can serve as
capable agents. Despite far lower accuracy (pass@1), they often surpass their post-trained counterparts in
solution coverage (pass@K) given a sufficient test-time budget. We further analyze the underlying
mechanism and show that post-training pushes tasks toward two extremes, always solved or never solved, and
thereby improves sampling efficiency and consistency at the cost of solution coverage. To measure this
cost, we propose Sharpening Tax, a diagnostic metric that quantifies the loss in test-time scalability
after post-training. Across 14 base/post-trained model pairs from four families and three agentic
benchmarks (42 cases in total), the tax is prevalent in most settings, can be estimated from a few
rollouts, and correlates well with other metrics. Finally, we present posterior-tempered group sampling
(PTGS), a simple plug-and-play Bayesian sampler that adapts the sampling temperature per prompt to its
estimated difficulty. Applied during RL training in two agentic environments, PTGS pays a smaller tax than
the fixed-temperature baseline, solving more tasks under repeated sampling while also improving
single-shot accuracy." No code repository or project page was found on the abstract page (checked
2026-10-06), matching the "results published, code not yet released" pattern this corpus already tracks
for HarnessX, AIDE² and ROFT above.

Why this belongs in this doc rather than being a harness-search entry of its own: Sharpening Tax is
first-party evidence that *RL* post-training can cost agentic solution coverage even while raising
single-shot accuracy — relevant context for reading any "we fine-tuned/post-trained the model and it got
better" claim in this family. ROFT (above) is explicitly RL-free ("no RL, no external instruction
signal"), so whether ROFT's retrospection-based SFT pays the same tax is **not tested by this paper** and
is not claimed here. The two papers' mitigations also sit at different layers, not a harness-vs-model
substitution: PTGS is itself "applied during RL training" (a training-time sampler, per the abstract),
while the base finding — a frozen, non-post-trained model plus "a light inference harness" can match or
beat its post-trained counterpart given enough test-time budget — is the inference-side comparison point
worth reading alongside RRSI/ROFT's harness-time and training-time interventions. Not rubric-scored: this
is a diagnostic finding and a training-time sampling technique, not a shipped harness or memory/context
system, and it does not touch the open Context·Reproducible cell in
[agent-substrate-reference-architecture.md](../../sdlc-lcm/agent-substrate-reference-architecture.md).

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
| `app/src/content/bibliography.bib` (fetched raw from the FineEnvs Space) | Full 28-entry BibTeX bibliography resolving the article's `@key` citations to titles/authors/arXiv IDs — accessed 2026-10-06 |
| `app/src/content/chapters/basics.mdx`, `introduction.mdx`, `openenv.mdx` (fetched raw from the Space) | In-text `@key` citation usage confirming which bibliography entries the article actually cites — accessed 2026-10-06 |
| [arXiv 2610.00906 abstract page][activesaddler] | Title, full author list (11), submission date (2026-10-01), full abstract verbatim, Comments field (project website + code URL), confirmation of GAIA2/Terminal-Bench 2.0 Pass@1 deltas — accessed 2026-10-06 |
| [ActiveSaddler project page][activesaddler-page] | Confirms a linked GitHub repo (microsoft/AutoSaddler, branch `feat/activesaddler`) — accessed 2026-10-06 |
| `gh api repos/microsoft/AutoSaddler`, 2026-10-06 | License (MIT), stars (237), forks (18), created/pushed dates |
| [arXiv 2610.01509 abstract page][sharpening-tax] | Title, full author list (10), submission date (2026-10-01), full abstract verbatim, Sharpening Tax and PTGS definitions verbatim, confirmation of no code/project link — accessed 2026-10-06 |

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
[activesaddler]: https://arxiv.org/abs/2610.00906
[activesaddler-page]: https://autosaddler-projectpage.github.io/activesaddler/
[autosaddler-repo]: https://github.com/microsoft/AutoSaddler/tree/feat/activesaddler
[sharpening-tax]: https://arxiv.org/abs/2610.01509
[fe-zhang]: https://arxiv.org/abs/2605.23950
[fe-he]: https://arxiv.org/abs/2608.17528
[fe-yu]: https://arxiv.org/abs/2607.21557
[fe-peng]: https://arxiv.org/abs/2605.15040
[fe-poolside]: https://arxiv.org/abs/2605.27605
[fe-xu]: https://arxiv.org/abs/2605.24220
[fe-shao]: https://arxiv.org/abs/2402.03300
[fe-kwon]: https://arxiv.org/abs/2309.06180
[fe-jimenez]: https://arxiv.org/abs/2310.06770
[fe-merrill]: https://arxiv.org/abs/2601.11868
[fe-kwaikat]: https://arxiv.org/abs/2607.05471
[fe-deng]: https://arxiv.org/abs/2509.16941
[fe-kimik2]: https://arxiv.org/abs/2507.20534
[fe-kimik3]: https://arxiv.org/abs/2607.24653
[fe-qwen]: https://arxiv.org/abs/2603.00729
[fe-deepseekv32]: https://arxiv.org/abs/2512.02556
