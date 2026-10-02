---
title: Close or confirm the four open substrate cells
status: draft
issue: 576
created: 2026-10-01
updated: 2026-10-02
---

Tracking issue: [#576](https://github.com/qte77/ai-agents-research/issues/576). Follows plan 0009
([plan](2026-09-27-0009-focus-shared-memory-context.md), #509), whose
[reference architecture](../sdlc-lcm/agent-substrate-reference-architecture.md#what-stays-open) leaves four
cells where no scored row reaches `partial`: **context·Distributed, context·Reproducible, skills·Shared,
skills·Distributed**.

## Current status

- **Shipped:** nothing yet. This plan is a `draft`: no research lane runs until the owner approves it.
- **Why calibration comes first:** the four cells rest mostly on `no data` and `n/a`, not on a measured
  `no`. Context has only 4 scored rows, and skills·Shared is `no data` on six git-hosted skill repos. Part
  of the gap may be definitional (row C0), so research lanes run on the cells that calibration cannot
  close.
- **Next, in order:** Phase A rows (agent only) → Phase B (one owner sitting: C0, T1) → Phase C (R1, Y2, Z).
- **Arc done-when:** each of the four cells ends in exactly one state:
  - *filled*: a first-party-scored row at `partial` or better;
  - *confirmed open*: the named tools were checked and none documents the property (list them);
  - *re-scored*: under the calibrated rubric (C0).

  "All four reach `yes`" is not the goal.
- **The loop, per row:** branch `<type>/<slug>` → write → `make check_docs check_status` → lychee (offline,
  plus online for new URLs) → PR → `/workspaces/temp/ai-agents-research-triage/merge_gated.py <PR>` →
  strike the row in the same PR, and close issues by hand (the gated squash drops `Closes #N`).
- **Owner gates:** C0 (rubric calibration, default below) and T1 (census module, default yes).
- **Access:** nothing new. The existing `gh` credential and polyfetch cover every row.
- **Commands:** prefix `gh`/`git` network calls with `env -u GH_TOKEN -u GITHUB_TOKEN`; polyfetch for
  blocked pages: `uv run --directory /workspaces/qte77/polyfetch-scrape polyfetch fetch --show-body <url>`.
- **Watch-outs:** briefs follow the guardrails in
  [`adding-research-source`](../../.claude/skills/adding-research-source/SKILL.md): evidence levels, verbatim
  quotes, a "strongest claims" list, and site-wide checks for absence claims. Do not re-paste them here.
  Plan 0009's learnings are in [AGENT_LEARNINGS.md](../../AGENT_LEARNINGS.md).

## Decision C0: calibrate the rubric for static artifacts (owner gate)

The [rubric](../sdlc-lcm/agent-substrate-rubric.md) defines Shared as "several agents, users or sessions read and
write the same store or artifact, with defined concurrency" (`partial`: shared read-only, or sharing via
manual export). It defines Distributed as "runs, syncs or scales across machines or services" (`partial`:
sync via a third-party drive). Both are written for running systems. Static artifacts in git (skill repos,
CLAUDE.md) fit them awkwardly:

- six skill repos score Shared `no data`, although git's pull-request flow is a defined way for several users
  to write the same artifact;
- the CC context row scores Distributed `no` because auto memory is machine-local, while git-tracked
  CLAUDE.md does sync across machines. One row mixes the two.

**Default:** static artifacts in git are scored on how they are governed and synced (repo, PR or merge flow,
pinning), not on runtime concurrency. Git hosting with a documented contribution flow is `partial` on Shared
and Distributed; papers stay `n/a`. Mixed rows are split. The owner may override with "keep the runtime
reading; the cells stay open as genuine gaps". Either way, record the decision in the rubric's "How to score"
section.

## Source map

- **Open cells:** [reference architecture § What stays open](../sdlc-lcm/agent-substrate-reference-architecture.md#what-stays-open).
- **Rows behind the open cells** (current main):
  - context: `docs/cc-native/context-memory/CC-memory-system-analysis.md` lines 176 (arXiv 2608.11095),
    222 (context-engineering-intro), 272 (TrackPoint), 430 (CC CLAUDE.md + auto memory);
  - skills: `docs/cc-community/CC-community-skills-landscape.md` lines 479, 485, 508 (coleam00 skills,
    excalidraw skill, cloudflare security-audit skill);
    `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` line 52 (runtypelabs/skills);
    `docs/non-cc/frameworks/agent-skill-evolution-research-landscape.md` lines 37, 62, 89, 108 (WikiSkill,
    AutoTailor, SkillLift, Skill2Env).
- **Census:** a local scratch file, `/workspaces/temp/research-0009/y-census.tsv` (61 rows, not in the repo).
  To regenerate it, `git grep -n "scored 2026-" -- docs` and grep for the six-column header
  (`| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |`); then exclude the
  reference-architecture page, whose composed row parses as a tool row. T1 would make this a tested module.
- **Lead backlog:** `/workspaces/temp/ai-agents-research-triage/rowB/ranked.tsv` (local). The leads kept
  below are the only ones that target an open cell. The rest of the P2 "context" leads (HEADROOM, Lynkr,
  pxpipe, context trimming) are about context *size*, which fills none of these cells.
- **Owner leads (2026-10-02), for rows M1–M3.** Existence checked 2026-10-02; content not yet verified.
  - First-party (Anthropic GitHub):
    - `github.com/anthropics/claude-code/tree/main/mods/agents-md` (contains `.claude-plugin`, `README.md`, `hooks`, `tests`);
    - `github.com/anthropics/claude-plugins-official/tree/main/plugins/code-modernization`.
  - Issue `github.com/anthropics/claude-code/issues/91870`, "Mods - make Claude 10x more extensible" (open, filed 2026-09-03 by `poteat`; whether that is an Anthropic account is unverified).
  - `claude.dev/blog/getting-started-with-claude-code-mods`: the fetch returned an empty body on 2026-10-02. Retry; if it stays empty, mark it unverified.
  - Third-party, leads only: any claim they make must trace to a first-party source.
    - `dev.to/valyuai/claude-code-now-supports-agentsmd-natively-heres-how-it-actually-works-5nl`
    - `www.explainx.ai/blog/claude-code-agents-md-support-2026`
    - `www.mindstudio.ai/blog/claude-code-mods-agents-md`
  - For row M3: `huggingface.co/spaces/AdithyaSK/multi-harness-rl` resolves to `FineEnvs/multi-harness-rl` (cite the canonical id). Per its own Space card: "The ultimate guide to multi-harness RL", "Train open models with RL inside real agent harnesses"; tags openenv, harbor, grpo, trl; created 2026-08-31.
  - Existing coverage: the CLAUDE.md/AGENTS.md dual-format read in `CC-memory-system-analysis.md` (its context rubric row); `code-modernization` as a name only in `CC-official-plugins-landscape.md` (Dev workflow list); mods: none.

## Remaining work

| # | Item | Gate | Done-when |
|---|---|---|---|
| U1 | Score CC cloud sessions on the rubric (long-running; plan 0009 gaps 7–8 named it, no row exists) | agent (Phase A) | A dated rubric row in `docs/cc-native/ci-remote/CC-cloud-sessions-analysis.md`, first-party only |
| U2 | Score CC scheduled tasks on the rubric (same gap) | agent (Phase A) | A dated rubric row in `docs/cc-native/ci-remote/CC-web-scheduled-tasks-analysis.md`, first-party only |
| A1 | Are ACE-FCA phase artifacts git-tracked or diffable? (`CC-memory-system-analysis.md` lists it as open) | agent (Phase A) | A cited answer, or "confirmed open" naming what was checked |
| L1 | Context·Shared/Distributed leads: Hyperspell, Redis Iris (backlog P2; existence and claims unverified) | agent (Phase A) | Each scored first-party, or dropped with the reason |
| L2 | Context·Reproducible lead: ReContext (backlog P2; may not be a context-layer tool at all, so check fit first) | agent (Phase A) | Scored, or dropped with the reason |
| L3 | Skills·Shared/Distributed leads: ctx, ACM (backlog P2). Search targets, *unverified*: org-level skill provisioning in agent products, and skill registries | agent (Phase A) | Each lead scored or dropped; each search target reported as found (first-party URL) or not found, with the pages checked |
| M1 | Claude Code mods and native AGENTS.md support (owner leads above). AGENTS.md is a cross-agent instruction file, so it bears on context·Shared. The `mods/agents-md` directory suggests the support ships as a mod: verify, don't assume | agent (Phase A) | First-party description of how CC reads AGENTS.md and what a mod is; extends `CC-memory-system-analysis.md` and a plugins-ecosystem doc (new page only if mods warrant one); the context row re-checked; mods rubric-scored |
| M2 | `code-modernization` official plugin (owner lead above) | agent (Phase A) | The `CC-official-plugins-landscape.md` entry extended from its own README and LICENSE, rubric-scored |
| M3 | Multi-harness RL guide (FineEnvs Space, owner lead above). Harness subject, next to the self-improving-harness entries (RRSI and the RSI analysis); it fills no open cell, so it runs after L1–L3 | agent (Phase A) | Placed in the harness docs from the Space's own content and any linked code (license from the LICENSE file), rubric-scored, or dropped with the reason |
| C0 | Rubric calibration for static artifacts (decision above) | owner (Phase B) | Decision recorded in the rubric's "How to score" section |
| T1 | Commit the census as `.github/scripts/lib/doc_census.py` with tests and a make target, so the Y matrix can be regenerated | owner (Phase B), default yes | Module plus RED-first tests merged; on current main it finds all scored rows (61 at plan time) and reproduces every cell of the reference architecture's evidence matrix |
| R1 | Re-score the 12 context and skills rows under C0 (split mixed rows) | agent (Phase C, after C0) | Rows updated with evidence |
| Y2 | Update the reference architecture: matrix, "What stays open", and the arc done-when state for each cell | agent (Phase C, last) | Each of the four cells is marked filled, confirmed open, or re-scored |
| Z | Close-out: changelog, release, close #576 | agent | Release published, #576 closed |
