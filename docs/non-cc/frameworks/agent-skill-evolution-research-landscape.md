---
title: Agent Skill Evolution Research Landscape
purpose: Survey of research (papers and reference repos) on constructing, evolving and transferring agent skills and tool sets, distinct from the packaging landscapes in cc-community and cc-native.
created: 2026-09-30
updated: 2026-11-27
validated_links_on: 2026-11-12
status: assess
---

## What It Is

Three 2026 research efforts on the *mechanics* of agent skills — how a skill is authored, tested,
evolved, or compiled — rather than how it is packaged or distributed (see
[CC-community-skills-landscape.md](../../cc-community/CC-community-skills-landscape.md) and
[CC-skills-adoption-analysis.md](../../cc-native/agents-skills/CC-skills-adoption-analysis.md) for the
distribution side). SkillLift and Skill2Env were scored 2026-09-30 against the [agent substrate
rubric][rubric]; Adaptive Skill Granularity (added 2026-11-12) is a batch-triage addition, not
rubric-scored. None ships a Claude Code integration; they are general agent-harness research
(SkillLift's benchmarks, WildClawBench and SkillsBench, run on OpenClaw and OpenHands harnesses, not
CC). Three paper-only entries were removed 2026-11-22 (see Not included).

## SkillLift

**Paper**: [arXiv:2609.15396][skilllift-paper] — "SkillLift: Learning Dense Rubrics from Sparse Oracles
for Efficient Skill Evolution" (Kang, Wen; affiliation not stated on the abstract page — not confirmed
as Fudan University despite the plan's lead description). **Repo**: [WalteR-MittY-pro/SkillLift][skilllift]
— MIT, 5★, last push 2026-10-28 (checked 2026-11-22). The paper states "Codes are available at" the repo, confirming the
pairing.

Rubric-guided self-evolution: rather than spending a full agent rollout (an "oracle call") to judge
every candidate skill, SkillLift first learns a *rubric* — binary criteria with signed weights — that
reproduces the oracle's preference *order* over skills ("ranking is a smoother supervision target than
absolute outcome regression"), then scores new candidates with one LLM call at zero oracle cost. A
bilevel loop alternates: an inner loop refines skills under the frozen rubric (never degrading a
candidate — refinement only continues while the rubric score is non-decreasing); an outer loop spends
K+1 oracle rollouts to re-align the rubric via Kendall's τ. Every skill revision applies as a validated
unified diff through a `bounded-edits` engine, "no uncontrolled rewrites." Evaluated on 147 tasks across
WildClawBench and SkillsBench, three backbones (GPT-5.4, GLM-5.1, DeepSeek-V4-Pro): the authors report
winning "all six model × benchmark combinations," +8.8–24.2pp over the one-shot skill ceiling, at
40–70% less token cost than SkillOpt/CoEvoSkills baselines — self-reported by the repo's own
`scripts/plot_readme_figures.py`, not independently replicated.

`subject: skills`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no data [README][skilllift] (single evaluation pipeline per run; no multi-agent shared-rubric-store semantics documented) | no [README][skilllift] (Docker containers run locally per benchmark task; no cluster/remote deployment claim) | yes [README][skilllift] (env-driven model endpoints in `.env`, algorithm-knob YAML profiles selected by `--param-profile`, pinned Python 3.11+/Docker requirements, and figures regenerated from checked-in `RESULTS` data, not screenshots) | yes [README][skilllift] (bounded-edits diff engine constrains how skills change; new baselines register as CLI methods alongside `skilllift`) | yes [README][skilllift] (git-hosted with `CITATION.cff`; every skill revision is a validated unified diff, an inherently versioned edit) | yes [README][skilllift] ("fully auditable per-round records"; the rubric's own criteria are the traceable evaluation surface for why a candidate was accepted or rejected) |

`scored 2026-09-30`

## NVlabs Skill2Env

**Repo**: [NVlabs/Skill2Env][skill2env] — Apache-2.0 (project-owned source; third-party material in
`SkillHub/` keeps its own upstream licenses), last push 2026-11-14 (checked 2026-11-22). Subtitle: "Reinforcing Agents with Collective Skills". Turns [Agent Skills][agentskills-org] into RL-ready terminal tasks in the
[Harbor][harbor] framework: a planner/creator pipeline (Codex agents in Docker containers) generates
task instructions, a containerized environment, deterministic tests (`test.sh` + a grading `rubric.md`),
and a reference solution per skill, retaining only tasks with `retained_tasks >= 1`. This converts a
*procedural* skill (a `SKILL.md` an agent follows) into a *benchmark task* (an environment an agent is
scored against) — the inverse direction from SkillLift, which evolves skills from
task performance. Requires a Codex CLI login and Docker; `--resume` makes batch generation over
`SkillHub/skills/` restartable.

`subject: skills`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no data [README][skill2env] (single-operator CLI tool; no multi-user task-generation store documented) | no [README][skill2env] (Docker containers on one host; `--max-parallel-workers` scales locally, not across machines) | partial [README][skill2env] (`--codex-version` pins the Codex CLI in the generator image and `--model`/`--reasoning-effort` are explicit flags, but task generation still depends on an LLM-driven planner/creator with no seed/determinism guarantee across runs) | yes [README][skill2env] (`--input-root` accepts one Skill, a family, or the whole hub; the README says it turns Agent Skills into tasks; "any Agent Skill" is unverified) | yes [README][skill2env] (Apache-2.0 git repo; `--resume` persists partial-batch state across runs; a `_corpus_manifest.json` tracks retained tasks) | partial [README][skill2env] (`SkillHub/skillhub_source_licenses.csv` traces each source skill's license/origin; individual generated tasks carry no lineage back to the LLM decisions that produced them) |

`scored 2026-09-30`

## Adaptive Skill Granularity (added 2026-11-12)

**Paper**: [arXiv:2610.31461][adaptive-skill] — "Adaptive Skill Granularity for Coding Agents: Runtime
Routing and Macro-to-Micro Recovery" (Zhang, Jiang, Wang, Zhou; submitted 2026-10-22). **Repo**:
[Jayceon-3/Adaptive-Skill-Agent][adaptive-skill-repo], which the paper's HTML version names as its code
(2 stars, last push 2026-06-28, no licence file; checked 2026-11-22). An earlier version of this entry
(2026-11-12) left the repo uncited because the abstract page doesn't name it.

Argues that prior skill-evolution work studies skills *before*
execution — retrieval, composition, synthesis — and that for coding agents the *runtime* choice matters
just as much: a task can be solved with primitive tool calls, a macro skill, or a hybrid that falls back
from macro to primitives on mismatch. The authors frame granularity as an action-abstraction policy
driven by task structure, execution state, and macro-skill failures, pairing a feature-based granularity
controller with a finite-state recovery executor. In a deterministic coding-agent evaluation using
verifier-defined success/cost/process metrics, fixed macro execution was efficient when it applied but
brittle on mismatch, while runtime routing plus explicit macro-to-micro recovery improved robustness —
self-reported, no independent replication found.

`subject: skills`

Not rubric-scored: a batch-triage addition; score if promoted to a dedicated analysis.

## Cross-References

- [docs/_topics/skills.md](../../_topics/skills.md) — topic hub pointer
- [CC-community-skills-landscape.md](../../cc-community/CC-community-skills-landscape.md) — distribution-side skill libraries (coleam00, cloudflare, superpowers, …)
- [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) — `runtypelabs/skills`, the adjacent distribution-side entry for this research batch; also ACM (§1), a general agentic-configuration-governance paper that names "skills" as one of several configuration-item types it covers but gives it no distinct treatment (checked and found not to fill the skills·Shared/Distributed open cells, plan 0010 row L3)
- [weco-aide-recursive-self-improvement-analysis.md § Meta-levels](../reference/weco-aide-recursive-self-improvement-analysis.md#meta-levels-what-is-being-optimized-added-2026-11-27) — the wider ladder this research sits on: prompt and program optimizers, automated agent design, self-referential agents

## Not included

Entries removed under the [pruning rule](../../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (alive, adopted or proven; checked 2026-11-22).

| Name | Reason | Date | Link |
|---|---|---|---|
| WikiSkill ("Compiling Agent Experience into Persistent Knowledge for Skill Evolution") | Criterion 1: paper only, no code link on the abstract page (arXiv:2608.27454); results self-reported | 2026-11-22 | <https://arxiv.org/abs/2608.27454> |
| AutoTailor ("Automatic, User-Aligned Capability Selection and Adaptation for Web Agents") | Criterion 1: paper only, no code link on the abstract page (arXiv:2609.13548); single-benchmark self-reported results | 2026-11-22 | <https://arxiv.org/abs/2609.13548> |
| Skill++ ("Towards Lifelong Agents via Routing-Aware Skill Refinement") | Criterion 1: paper only, no code link on the abstract page (arXiv:2611.00544); self-reported results | 2026-11-22 | <https://arxiv.org/abs/2611.00544> |

## Sources

| Source | Content |
|---|---|
| [SkillLift (arXiv:2609.15396)][skilllift-paper] | Abstract, method summary; confirms the GitHub pairing |
| [WalteR-MittY-pro/SkillLift][skilllift] | README (fetched via GitHub contents API, 2026-09-30), MIT license, repo metadata |
| [NVlabs/Skill2Env][skill2env] | README (fetched via GitHub contents API, 2026-09-30), Apache-2.0 license, repo metadata |
| [Adaptive Skill Granularity (arXiv:2610.31461)][adaptive-skill] | Abstract and method summary (2026-11-12); the HTML version names the code repo (checked 2026-11-22) |
| [Jayceon-3/Adaptive-Skill-Agent][adaptive-skill-repo] | Repo metadata (2026-11-22) |
| [Plan 0009][plan] | Lead list and rubric scope for this batch |

[rubric]: ../../sdlc-lcm/agent-substrate-rubric.md
[plan]: ../../plans/2026-09-27-0009-focus-shared-memory-context.md
[skilllift-paper]: https://arxiv.org/abs/2609.15396
[skilllift]: https://github.com/WalteR-MittY-pro/SkillLift
[skill2env]: https://github.com/NVlabs/Skill2Env
[agentskills-org]: https://agentskills.io
[harbor]: https://harborframework.com
[adaptive-skill]: https://arxiv.org/abs/2610.31461
[adaptive-skill-repo]: https://github.com/Jayceon-3/Adaptive-Skill-Agent
