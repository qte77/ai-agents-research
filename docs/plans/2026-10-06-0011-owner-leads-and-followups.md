---
title: Owner leads (2026-10-06) and post-0010 follow-ups
status: approved
created: 2026-10-06
updated: 2026-10-06
---

Collects the owner's 2026-10-06 leads (repos, papers, one keyword) and the open follow-ups from
2026-10-03 to 2026-10-05: Fable's review of #587/#589, the rxiv relevance filter (#594), link rot (#598) and the
release of the pending changelog fragments. Plans 0009 and 0010 are closed; this is the only open arc.

## Current status

- **Approved 2026-10-06** (owner: "proceed" on #600). O1 decided by default the same day: gap-driven
  scoring (overridable). Coverage of every lead was checked on 2026-10-06 with a calibrated
  `git grep` over `docs/` (archive excluded); the result is in the table's *Coverage* column.
- **Next, in order:** Phase A agent rows (F1 → N1–N5 → E1 → K1 → P1 → L1) → Phase B (owner: O1, O2) → Z.
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
| rxiv relevance filter | consumer `.github/workflows/rxiv-paper-eval.yaml` (`relevance_prompt`, `model`); upstream `qte77/gha-rxiv-paper-eval` v0.5.0; model-eval harness `.github/workflows/llm-model-eval.yaml` |

## Remaining work

| Row | Item | Coverage | Gate | Done when |
|---|---|---|---|---|
| ~~F1~~ | ~~Apply Fable's review: Claude Science provenance/export facts (artifacts, multiple-computers, changelog pages) and platform timeline; MacDiarmid priming step; Nguyen "coding agents" framing; interpretability-index row 20 (2511.18397 vs 2024 sycophancy paper); "worst reported"; AIDDA↔autoresearch inference; Pro auto-review default; hub rows (`harness`, `long-running`) and cross-links (bwrap quirks, system-1 ↔ Brier, EvilGenie ↔ benchmarks); move Claude Science beside OpenScience~~ | n/a | agent | Done 2026-10-06 (PR: plan-0011-f1). system-1 → Brier back-link left to lane B (that file is fenced to it); all other items applied, re-read at source 2026-10-06 |
| N1 | diagram-design | none | agent | Entry with licence/stars from `gh api`, `platform_scope`, visualization hub row |
| N2 | operator-memory | none | agent | Entry placed per skill tree; rubric row only if O1 says it could change a cell (context·Reproducible is open) |
| N3 | pg-jev | none | agent | Licence read from `LICENSE`; added to system-1 + Jev ecosystem lists |
| N4 | tailnet-preview | none | agent | Added with an agent tie-in from its README, or dropped with the reason in this row |
| N5 | Papers 2609.37226, 2609.33439, 2610.00906, 2610.01509 | none | agent | Each added at its use-case home from the abstract page (verbatim quotes only); Raven paper cited in `raven-analysis.md` |
| E1 | Existing-coverage refresh: FineEnvs cited papers; Haystack beyond one line; SkillSpector stale hedge | partial | agent | Cited papers listed or added; Haystack entry reflects current README; line 185 corrected |
| K1 | Keyword sweep "self-evolving ontology" beyond EvoOntology | EvoOntology only | agent | Sources found are added or listed as rejected with reasons |
| P1 | rxiv relevance precision (#594): tighten prompt and/or model, test via `llm-model-eval.yaml` against the #527 labels, rerun W38 | n/a | agent | Spot-checked rerun accepts only agent-relevant papers; #593/#599 regenerated or closed; #594 closed |
| L1 | Link rot #598 (`tuleap.com/comparisons/` 503) | n/a | agent | Rechecked; repointed if persistent, else left to auto-close |
| ~~O1~~ | ~~Scoring policy for new tools~~ | n/a | owner | Decided by default 2026-10-06: **gap-driven** — score only when a tool could change a reference-architecture cell (owner may override) |
| O2 | `qte77/gha-issue-triage` `self-triage.yml` has no LLM secret | n/a | owner | Owner adds a secret there; default: leave until then |
| Z | Release: collect the pending `changelog.d/` fragments (#587, #589, #590–#592) plus this arc's | n/a | agent | `bump-my-version` run, release PR merged, tag + GitHub Release published |

**Deferred (not rows):** #588 held leads (Originator, Serova, C3) — waiting on first-party evidence;
plan 0001 (#452) — unchanged; upstream `gha-rxiv-paper-eval` leftovers (dispatch and example workflows still on
GitHub Models; issues #76, #79, #80) — tracked there; AlphaEvolve-family coverage gap (Fable, 2026-10-04) —
candidate for the next arc.
