---
title: Owner leads (2026-10-06) and post-0010 follow-ups
status: done
created: 2026-10-06
updated: 2026-10-09
---

Collects the owner's 2026-10-06 leads (repos, papers, one keyword) and the open follow-ups from
2026-10-03 to 2026-10-05: Fable's review of #587/#589, the rxiv relevance filter (#594), link rot (#598) and the
release of the pending changelog fragments. Plans 0009 and 0010 are closed; this is the only open arc.

## Current status

- **Approved 2026-10-06** (owner: "proceed" on #600). O1 decided by default the same day: gap-driven
  scoring (overridable). Coverage of every lead was checked on 2026-10-06 with a calibrated
  `git grep` over `docs/` (archive excluded); the result is in the table's *Coverage* column.
- **Arc closed 2026-10-09.** Every row shipped or deferred; see the table and the deferred list. Also shipped as owner leads outside the table: Firecrawl Universal Scrape (#631) and a practitioner Jev cascade (#632).
- **Arc done-when:** every row is shipped (PR number), dropped (reason), or deferred (gate + reason).
- **The loop, per row:** branch `<type>/<slug>` → write → `make check_docs check_status` → lychee on changed
  files → PR → `/workspaces/temp/ai-agents-research-triage/merge_gated.py <PR>` → strike the row in the same PR;
  close issues by hand (the gated squash drops `Closes #N`).
- **Owner gates:** O2 (`gha-issue-triage` secret). O1 is decided (default applied, overridable).
- **Access:** nothing new. The existing `gh` credential and polyfetch cover every row; Cloudflare Workers AI
  (`secrets.CF_WORKERS_AI_TOKEN`, `vars.LLM_BASE_URL`) already serves P1.
- **Commands:** prefix `gh`/`git` network calls with `env -u GH_TOKEN -u GITHUB_TOKEN`; polyfetch for blocked
  pages: `uv run --directory /workspaces/qte77/polyfetch-scrape polyfetch fetch --show-body <url>`.
- **Watch-outs:** follow [`adding-research-source`](../../.claude/skills/adding-research-source/SKILL.md)
  (evidence levels, verbatim quotes, strongest-claims list, site-wide checks for absence claims). Rubric rows only
  under O1's policy. Never fire two `rxiv-paper-eval` dispatches on one day concurrently (CONTRIBUTING).

## Source map

| Lead | Where it lives or would go |
|---|---|
| [diagram-design](https://github.com/cathrynlavery/diagram-design) (MIT, 43.6k★, multi-platform skill) | `cc-community/` (CC integration surface) with `platform_scope`; row in `_topics/visualization.md` |
| [operator-memory](https://github.com/aerovato/operator-memory) (BSD-3-Clause, 358★, "self-improving context engine for coding agents") | `cc-community/CC-memory-tooling-landscape.md` or `non-cc/context-memory/` — placement per the skill's tree |
| [pg-jev](https://github.com/realZachi/pg-jev) (976★, licence NOASSERTION → read `LICENSE`) | `non-cc/reference/system-1-decision-models-landscape.md` + `non-cc/infrastructure/jev-analysis.md` ecosystem list |
| [tailnet-preview](https://github.com/elsheppo/tailnet-preview) (MIT, 1★) | Only if the README ties it to agents (e.g. previewing agent-built apps); else drop |
| arXiv [2609.37226](https://arxiv.org/abs/2609.37226) CorpusMap ("Follow the Entities") | agentic search / graphs-rag — `_topics/rag.md` hub decides the doc |
| arXiv [2609.33439](https://arxiv.org/abs/2609.33439) Raven paper (EverMind AI) | extend `non-cc/orchestrators/raven-analysis.md` (repo already covered; paper not cited) |
| arXiv [2610.00906](https://arxiv.org/abs/2610.00906) ActiveSaddler (curriculum for harness optimization) | next to FineEnvs / AIDE² in `non-cc/reference/weco-aide-recursive-self-improvement-analysis.md`, or `_topics/harness.md` |
| arXiv [2610.01509](https://arxiv.org/abs/2610.01509) Sharpening Tax in Post-Training | harness topic (pre-trained LLM + light harness vs post-trained) — same placement call as 2610.00906 |
| arXiv 2609.39551 RankEvolve | already added (#589, `research-agents-landscape.md` §1) |
| FineEnvs [multi-harness-rl](https://huggingface.co/spaces/FineEnvs/multi-harness-rl) | covered (`weco-aide-…-analysis.md` § FineEnvs, #578); the papers it cites are not |
| [Utopia](https://github.com/deeplethe/utopia), [open-ontologies](https://github.com/fabio-rovai/open-ontologies), EvoOntology | covered + scored (`non-cc/infrastructure/semantic-layers-data-catalog-landscape.md`) |
| [Haystack](https://github.com/deepset-ai/haystack) | one line only (`agent-frameworks-infrastructure-landscape.md:114`); now pitched as "context-engineered" |
| [learn-harness-engineering](https://github.com/walkinglabs/learn-harness-engineering) | covered (`agentic-engineering-disciplines-landscape.md`, frameworks landscape) |
| [jevgrep](https://github.com/dzhng/jevgrep) | covered (`CC-code-tooling-landscape.md § jevgrep`) |
| [SkillSpector](https://github.com/NVIDIA/SkillSpector) | covered (`agentic-ai-vulnerability-landscape.md`); `agent-code-analysis-landscape.md:185` still calls it "secondary source" — stale |
| Fable review findings (2026-10-04) | `CC-claude-science-analysis.md:30–42`, `ai-security-governance-analysis.md` (reward-hacking subsection), `agent-evaluation-metrics-landscape.md` (Brier metric), `research-agents-landscape.md` (AIDDA line, Claude Science placement), `cc-native/model-internals/CC-first-party-interpretability-index.md:20` |
| arXiv [2610.02525](https://arxiv.org/abs/2610.02525) MIRA, "Learning What to Investigate Next: Meta-Reasoning for Long-Horizon Research Agents" (2026-10-01, no code link) | extend the meta-reasoning section of `non-cc/reference/weco-aide-recursive-self-improvement-analysis.md` (plan 0010 M4) |
| [TencentCloud/Octop](https://github.com/TencentCloud/Octop) (MIT, 7.4k★, v1.0.2b6, "A smarter, self-hosted AI assistant — multi-user, multi-agent.") | not covered (the plan 0007 hit is "Octopus"); placement per the skill's tree — likely `non-cc/agents/` or `non-cc/orchestrators/` |
| Jev and similar system-1 models, by use case: model routing; guardrails (block, grant); tool-call gating; reranking (query, probability); LLM output evals and scores; confidence gate (act, confirm, HITL) | `non-cc/reference/system-1-decision-models-landscape.md` (alternatives) and `non-cc/infrastructure/jev-analysis.md` (Jev); routing, guardrails, gating, judging and confidence have scattered mentions, reranking and HITL escalation have none; Brier metric in `sdlc-lcm/agent-evaluation-metrics-landscape.md` |
| rxiv weekly selection | `rxiv-paper-eval.yaml` passes `max_papers: 50` ("Capped to first 50" of ~2,200, feed order); upstream v0.5.0 offers `max_llm_calls` (rank by topic-keyword overlap, send top N) |
| rxiv relevance filter | consumer `.github/workflows/rxiv-paper-eval.yaml` (`relevance_prompt`, `model`); upstream `qte77/gha-rxiv-paper-eval` v0.5.0; model-eval harness `.github/workflows/llm-model-eval.yaml` |

## Remaining work

| Row | Item | Coverage | Gate | Done when |
|---|---|---|---|---|
| ~~F1~~ | ~~Apply Fable's review: Claude Science provenance/export facts (artifacts, multiple-computers, changelog pages) and platform timeline; MacDiarmid priming step; Nguyen "coding agents" framing; interpretability-index row 20 (2511.18397 vs 2024 sycophancy paper); "worst reported"; AIDDA↔autoresearch inference; Pro auto-review default; hub rows (`harness`, `long-running`) and cross-links (bwrap quirks, system-1 ↔ Brier, EvilGenie ↔ benchmarks); move Claude Science beside OpenScience~~ | n/a | agent | Done 2026-10-06 (#601). system-1 → Brier back-link left to lane B (that file is fenced to it); all other items applied, re-read at source 2026-10-06 |
| ~~N1~~ | ~~diagram-design~~ | none | agent | Done 2026-10-06 (#605): `CC-community-skills-landscape.md`, visualization hub row; 44 type references vs the tagline's 42; not scored (no skills cell can move) |
| ~~N2~~ | ~~operator-memory~~ | none | agent | Done 2026-10-06 (#605): `CC-memory-tooling-landscape.md`, memory hub row; not scored (Brain content written by an unpinned agent, so context·Reproducible does not move) |
| ~~N3~~ | ~~pg-jev~~ | none | agent | Done 2026-10-06 (#603): PostgreSQL License (detector reads NOASSERTION); system-1 + Jev ecosystem lists |
| ~~N4~~ | ~~tailnet-preview~~ | none | agent | Done 2026-10-06 (#603): added to `CC-remote-access-landscape.md` § DIY; its README ties the skill to Codex, not Claude Code |
| ~~N5~~ | ~~Papers 2609.37226, 2609.33439, 2610.00906, 2610.01509~~ | none | agent | Done 2026-10-06 (#602): CorpusMap → `karpathy-llm-kb-analysis.md`; Raven paper → `raven-analysis.md`; ActiveSaddler + Sharpening Tax → `weco-aide-…-analysis.md`; hub rows |
| ~~E1~~ | ~~Existing-coverage refresh: FineEnvs cited papers; Haystack beyond one line; SkillSpector stale hedge~~ | partial | agent | Done 2026-10-06: FineEnvs cited papers (#602; 20 arXiv IDs, one already in the corpus); Haystack refreshed and SkillSpector hedge fixed (#603) |
| ~~K1~~ | ~~Keyword sweep "self-evolving ontology" beyond EvoOntology~~ | EvoOntology only | agent | Done 2026-10-06 (#602): OaK, SciToolAgent-Evo, Evo-DKD added (all paper-only); four rejects stated in the doc |
| ~~P1~~ | ~~rxiv relevance precision (#594): tighten prompt and/or model, test via `llm-model-eval.yaml` against the #527 labels, rerun W38~~ | n/a | agent | Done 2026-10-06 (#604): agent-strict prompt (70B, W22–30: 83.6% vs 46.0% agreement, 16 vs 135 false accepts); #593/#599 closed; W40 rerun accepted 6/50, all agent papers (#606); #594 closed |
| ~~L1~~ | ~~Link rot #598 (`tuleap.com/comparisons/` 503)~~ | n/a | agent | Done 2026-10-06, no change: the link passes again (lychee); #598 auto-closes on the next scheduled run |
| ~~O1~~ | ~~Scoring policy for new tools~~ | n/a | owner | Decided by default 2026-10-06: **gap-driven** — score only when a tool could change a reference-architecture cell (owner may override) |
| ~~N6~~ | ~~arXiv 2610.02525 MIRA~~ | none | agent | Done 2026-10-09 (#623): MIRA section in `weco-aide-…-analysis.md`; no code found; not scored |
| ~~N7~~ | ~~TencentCloud/Octop~~ | none | agent | Done 2026-10-09 (#623): new `non-cc/agents/octop-analysis.md` (MIT, v1.0.2b6), Tier 2 of the enterprise-OS landscape; not scored |
| ~~J1~~ | ~~Use-case map for Jev and similar models: model routing, guardrails (block/grant), tool-call gating, reranking (query, probability), LLM output evals/scores, confidence gate (act/confirm/HITL)~~ | partial | agent | Done 2026-10-09 (#625): § Use cases in `system-1-decision-models-landscape.md`; gaps stated: no system-1 model documents LLM routing or query-document reranking; Jev documents an act/confirm/escalate confidence gate |
| ~~S1~~ | ~~rxiv selection: replace `max_papers: 50` (first 50 in feed order) with `max_papers: 0` + `max_llm_calls: <cap>` (keyword-ranked)~~ | n/a | agent | Done 2026-10-06 (#614): `max_papers: 0` + `max_llm_calls: 100`; ranked selection confirmed in the run log; #615 dedups repeated feed rows |
| ~~B1~~ | ~~Backfill missing arXiv weeks after S1: W26–W29, W33–W39 (11), then rerun W31 and W40 on the ranked selection. W32 is absent from the feed (`gha-rxiv-feed-action` has no `32.csv`) — not backfillable. Serial: run → review titles → merge triage PR → next (each PR rebuilds the full index)~~ | partial (W31, W40 done on first-50) | agent | Done 2026-10-09: W26–W29 (#616–#619), W33 (#620), W34 (#621), W35 (#624), W36 (#627), W37 (#628), W38 (#629), W39 (#630); reruns W31 (#633, 77 accepted vs 7 on first-50) and W40 (#634, 84 vs 6). State lists W21–W40 except W32; index 909 papers. Fixes found on the way: #610 (week-keyed branch), #615 (repeated feed rows) |
| ~~O3~~ | ~~Backfill parameters~~ | n/a | owner | Decided 2026-10-06 by the owner: cap 100 per week; serial per-week PRs. W11–W20 not decided → deferred (below) |
| ~~Z~~ | ~~Release: collect the pending `changelog.d/` fragments (#587, #589, #590–#592) plus this arc's~~ | n/a | agent | Done 2026-10-06: v0.15.0 released (#608, tag + GitHub Release) |

**Deferred (not rows):** O2 — `qte77/gha-issue-triage` `self-triage.yml` needs an LLM secret (owner gate; until then it posts "GitHub Models retired" comments in that repo); backfill of arXiv W11–W20 (owner decision; the feed has them, the pipeline started at W21; about 2 hours of serial runs); JevSpawn (arXiv 2610.00437) surfaced in the W40 triage — a candidate for the system-1 use-case map, not yet researched; #588 held leads (Originator, Serova, C3) — waiting on first-party evidence;
plan 0001 (#452) — unchanged; upstream `gha-rxiv-paper-eval` leftovers (dispatch and example workflows still on
GitHub Models; issues #76, #79, #80) — tracked there; AlphaEvolve-family coverage gap (Fable, 2026-10-04) —
candidate for the next arc.
