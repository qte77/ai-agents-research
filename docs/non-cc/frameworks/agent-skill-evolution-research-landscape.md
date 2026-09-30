---
title: Agent Skill Evolution Research Landscape
purpose: Survey research (papers and reference repos) on constructing, evolving, and transferring agent skills and tool sets — as distinct from the packaging/distribution landscapes in cc-community and cc-native.
created: 2026-09-30
updated: 2026-09-30
validated_links: 2026-09-30
status: assess
---

## What It Is

Four 2026 research efforts on the *mechanics* of agent skills — how a skill is authored, tested,
evolved, or compiled — rather than how it is packaged or distributed (see
[CC-community-skills-landscape.md](../../cc-community/CC-community-skills-landscape.md) and
[CC-skills-adoption-analysis.md](../../cc-native/agents-skills/CC-skills-adoption-analysis.md) for the
distribution side). Scored 2026-09-30 against the [agent substrate rubric][rubric]. None of the four
ships a Claude Code integration; they are general agent-harness research (WildClawBench/SkillsBench run
on OpenClaw and OpenHands harnesses, not CC).

## WikiSkill

**Paper**: [arXiv:2608.27454][wikiskill] — "WikiSkill: Compiling Agent Experience into Persistent
Knowledge for Skill Evolution" (Tang, Rashtchian, Ferng, Tomkins, Juan, Vu; submitted 2026-08-27). No
public code repository is linked from the abstract page.

A framework that "co-evolves agent skills with a persistent knowledge base (wiki)," distinguishing raw
execution experience, accumulated knowledge, and executable skills — where prior skill-evolution methods
leave "insights that guide skill development... scattered across optimization histories," WikiSkill
consolidates them into a wiki that "subsequent skill updates can build on." The authors report it
"consistently outperforms state-of-the-art skill-evolution methods," that evolved skills "transfer
effectively across models and model families," and that smaller models with evolved skills can
"outperform substantially larger models without them" — all self-reported, no independent replication
found.

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| n/a [paper][wikiskill] (research method, not a shipped multi-user system) | n/a [paper][wikiskill] (no deployment artifact to run across machines) | no data [paper][wikiskill] (no code repository linked from the abstract page, so rebuildability can't be checked either way) | yes [paper][wikiskill] (the wiki is explicitly designed to accumulate and be built on by later skill updates) | no data [paper][wikiskill] (no stated mechanism for snapshotting or rolling back the wiki's state) | partial [paper][wikiskill] (the wiki records *why* a skill changed — provenance for the update, not a citation trail for a given output) |

`scored 2026-09-30`

## AutoTailor

**Paper**: [arXiv:2609.13548][autotailor] — "AutoTailor: Automatic, User-Aligned Capability Selection
and Adaptation for Web Agents" (Cao, Szekeres, Faisal; affiliation not stated on the abstract page — not
confirmed as Microsoft Research despite the plan's lead description). No public code repository linked.

A meta-agentic framework that constructs and maintains a compact set of trajectory-derived MCP APIs in
two phases: **offline**, converting web trajectories into parameterized automation programs, quality-
filtering them, and keeping only broadly useful ones via a "Usage Likelihood Filter"; **online**,
"Dynamic Reselection monitors task outcomes and API usage, identifies recurring coverage gaps, adds
relevant candidates, and prunes persistently unused capabilities." On 106 WebArena Postmill tasks, the
authors report reducing 1,283 unrefined APIs to 87 (offline) then 33 (online), reaching "90.6%
correctness, compared with 87.5% for ReAct alone," with 57.8% lower token cost and 29.4% lower latency —
self-reported, single-benchmark.

This is a **tool-set curation** method — it produces MCP APIs, not `SKILL.md` procedures — so it is as
relevant to the Plugins subject as to Skills; see
[docs/_topics/plugins.md](../../_topics/plugins.md).

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| n/a [paper][autotailor] (research method, not a shipped multi-user system) | n/a [paper][autotailor] (single-agent evaluation harness, no deployment claim) | no [paper][autotailor] (no code repository linked; the offline/online pipeline depends on an unpinned LLM for trajectory-to-API conversion) | yes [paper][autotailor] (Dynamic Reselection adds/prunes APIs at runtime without a rewrite of the agent) | no data [paper][autotailor] (no stated versioning of the evolving 1,283→87→33 API set) | no data [paper][autotailor] (no audit trail linking a kept/pruned API back to the trajectories that justified it) |

`scored 2026-09-30`

## SkillLift

**Paper**: [arXiv:2609.15396][skilllift-paper] — "SkillLift: Learning Dense Rubrics from Sparse Oracles
for Efficient Skill Evolution" (Kang, Wen; affiliation not stated on the abstract page — not confirmed
as Fudan University despite the plan's lead description). **Repo**: [WalteR-MittY-pro/SkillLift][skilllift]
— MIT, 4★, pushed 2026-09-08. The paper states "Codes are available at" the repo, confirming the
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

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no data [README][skilllift] (single evaluation pipeline per run; no multi-agent shared-rubric-store semantics documented) | no [README][skilllift] (Docker containers run locally per benchmark task; no cluster/remote deployment claim) | yes [README][skilllift] (env-driven model endpoints in `.env`, algorithm-knob YAML profiles selected by `--param-profile`, pinned Python 3.11+/Docker requirements, and figures regenerated from checked-in `RESULTS` data, not screenshots) | yes [README][skilllift] (bounded-edits diff engine constrains how skills change; new baselines register as CLI methods alongside `skilllift`) | yes [README][skilllift] (git-hosted with `CITATION.cff`; every skill revision is a validated unified diff, an inherently versioned edit) | yes [README][skilllift] ("fully auditable per-round records"; the rubric's own criteria are the traceable evaluation surface for why a candidate was accepted or rejected) |

`scored 2026-09-30`

## NVlabs Skill2Env

**Repo**: [NVlabs/Skill2Env][skill2env] — Apache-2.0 (project-owned source; third-party material in
`SkillHub/` keeps its own upstream licenses), pushed 2026-09-21. Tagline: "Democratizing Collective
Intelligence." Turns any [Agent Skill][agentskills-org] into RL-ready terminal tasks in the
[Harbor][harbor] framework: a planner/creator pipeline (Codex agents in Docker containers) generates
task instructions, a containerized environment, deterministic tests (`test.sh` + a grading `rubric.md`),
and a reference solution per skill, retaining only tasks with `retained_tasks >= 1`. This converts a
*procedural* skill (a `SKILL.md` an agent follows) into a *benchmark task* (an environment an agent is
scored against) — the inverse direction from SkillLift/WikiSkill/AutoTailor, which evolve skills from
task performance. Requires a Codex CLI login and Docker; `--resume` makes batch generation over
`SkillHub/skills/` restartable.

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no data [README][skill2env] (single-operator CLI tool; no multi-user task-generation store documented) | no [README][skill2env] (Docker containers on one host; `--max-parallel-workers` scales locally, not across machines) | partial [README][skill2env] (`--codex-version` pins the Codex CLI in the generator image and `--model`/`--reasoning-effort` are explicit flags, but task generation still depends on an LLM-driven planner/creator with no seed/determinism guarantee across runs) | yes [README][skill2env] (`--input-root` accepts one Skill, a family, or the whole hub; works on "any Agent Skill" per the tagline) | yes [README][skill2env] (Apache-2.0 git repo; `--resume` persists partial-batch state across runs; a `_corpus_manifest.json` tracks retained tasks) | partial [README][skill2env] (`SkillHub/skillhub_source_licenses.csv` traces each source skill's license/origin; individual generated tasks carry no lineage back to the LLM decisions that produced them) |

`scored 2026-09-30`

## Cross-References

- [docs/_topics/skills.md](../../_topics/skills.md) — topic hub pointer
- [docs/_topics/plugins.md](../../_topics/plugins.md) — AutoTailor's MCP tool-set angle
- [CC-community-skills-landscape.md](../../cc-community/CC-community-skills-landscape.md) — distribution-side skill libraries (coleam00, cloudflare, superpowers, …)
- [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) — `runtypelabs/skills`, the adjacent distribution-side entry for this research batch

## Sources

| Source | Content |
|---|---|
| [WikiSkill (arXiv:2608.27454)][wikiskill] | Abstract, method summary, self-reported results |
| [AutoTailor (arXiv:2609.13548)][autotailor] | Abstract, WebArena Postmill results |
| [SkillLift (arXiv:2609.15396)][skilllift-paper] | Abstract, method summary; confirms the GitHub pairing |
| [WalteR-MittY-pro/SkillLift][skilllift] | README (fetched via GitHub contents API, 2026-09-30), MIT license, repo metadata |
| [NVlabs/Skill2Env][skill2env] | README (fetched via GitHub contents API, 2026-09-30), Apache-2.0 license, repo metadata |
| [Plan 0009][plan] | Lead list and rubric scope for this batch |

[rubric]: ../../sdlc-lcm/agent-substrate-rubric.md
[plan]: ../../plans/2026-09-27-0009-focus-shared-memory-context.md
[wikiskill]: https://arxiv.org/abs/2608.27454
[autotailor]: https://arxiv.org/abs/2609.13548
[skilllift-paper]: https://arxiv.org/abs/2609.15396
[skilllift]: https://github.com/WalteR-MittY-pro/SkillLift
[skill2env]: https://github.com/NVlabs/Skill2Env
[agentskills-org]: https://agentskills.io
[harbor]: https://harborframework.com
