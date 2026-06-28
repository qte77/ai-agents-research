---
title: Goal Tracking & Attribution Landscape
purpose: How an agentic coding fleet ties work back to stated goals — the top-down goal→spec→build→learning cascade and the bottom-up attribution of every feature, PR, and agent run to the goal that motivated it — with the qte77 estate as the worked reference and the commercial OKR/PM tooling baseline it diverges from.
category: landscape
created: 2026-06-28
updated: 2026-06-28
validated_links: 2026-06-28
---

**Status**: Assess

## What It Is

A map of how an agentic coding fleet connects day-to-day work back to stated goals: the **top-down** `goal → spec → build → learning` cascade, and the **bottom-up attribution** that traces every feature, PR, and agent run to the goal that motivated it. Where the [agentic-engineering-disciplines landscape][disciplines] frames *goals, specs, builds, and learnings compound instead of drift* as a credo, this doc is the **goals anchor** of that credo made concrete: what a machine-writable goal store looks like, how runs are attributed to goals, and how the loop closes.

**Status Assess** because the estate implementations are early (v0.x schemas, some stores still empty) and the mature commercial OKR/PM tooling does not yet fill the agent-native gap — see the baseline contrast below.

## The agentic attribution loop

The qte77 estate's `docs/architecture.md` ([qte77/qte77][qte77]) states the loop in one line: **"goals feed specs, specs feed builds, builds emit learnings, learnings flow back into the next goals."** Read top-down it is goal decomposition; read bottom-up it is attribution — every spec traces to a goal, every build to a spec, every learning to a build.

```text
              top-down decomposition  →
   Goals ───→ Specs ───→ Builds ───→ Learnings
     ↑                                    │
     └──  ←  bottom-up attribution + reflect  ──┘
```

Two control points recur (the estate credo): **agents drive** the decomposition and tracing machinery; **humans approve and steer** the goals themselves — *"agents propose, humans decide."*

## Estate worked examples

The substance of this landscape is four first-party implementations at different points on the loop. (Files are named in backticks; links point at the public repo roots.)

### qte77/qte77 — the goal store and OKR home

[qte77/qte77][qte77] is the meta-orchestration repo:

- `goals.json` — a minimal machine-writable OKR schema (v0.1.0). It currently holds `goals: []`; the human→agent handoff boundary is explicit (humans set goals, orchestrators read them), and the array stays empty until a cockpit/dashboard consumer pressure-tests the schema.
- `docs/cto-handbook-mapping.md` — the OKR home: it maps the [Startup CTO Handbook][cto-map]'s "OKRs / measuring success" chapter onto `goals.json`, under the same *"agents propose, humans decide"* boundary.
- `docs/architecture.md` — states the `goals → specs → builds → learnings` loop above.

### liminal-flux-gh-acc — a self-operating account with per-run attribution

[liminal-flux-gh-acc][liminal] is an 8-agent-role self-operating GitHub account. Its `docs/living-github-account.md` documents four mechanisms that close the loop with cost-gated tracing:

1. **Inbound goals** — `repository_dispatch` events land in a `state/goals.json` registry.
2. **Idle discovery** — when the work queue is empty, a heartbeat generates a new goal, so the account never sits idle.
3. **Per-run tracing** — every agent run appends to `state/performance-log.jsonl` with `goal_id`, `task_id`, `agent`, `model`, `tokens_in`/`tokens_out`, `cost_usd`, and `outcome`: the bottom-up attribution record.
4. **Reflector loop** — a daily pass over a 7-day window of the performance log opens improvement Issues and updates `agent-memory.md`, feeding learnings back into the next goals.

Cost gates bound the autonomy: a ~$5/day hard stop, a `>2×` spend-spike notification, and a `>30%` failure rate routed to a `human-required` label. This is the [agentic-sdlc-patterns][sdlc-patterns] ADLC **Observe → Correct** phase — flagged there as a gap — instantiated.

### research-ralphy — research → PRD attribution

[research-ralphy][research-ralphy]'s `config/prd-generation-prompt.md` chains a research finding → a top-3-to-5 selection → `docs/PRD.md` → `generate_prd_json.py` → a `prd.json` of stories carrying acceptance criteria and target files. Every story is traceable back to the discovery that motivated it.

### ralph-loop template — story-level status tracking

The [ralph-loop-cc-tdd-wt-vibe-kanban-template][ralph-loop]'s `ralph/README.md` defines the `prd.json` story record: `id`, `depends_on`, `acceptance`, `files`, `status` (pending → in_progress → passed/failed), and `wave`. Durable state lives in `prd.json` + `progress.txt` + `LEARNINGS.md` + git commits — no database; the repo *is* the attribution ledger.

## Traditional baseline (brief contrast)

The mature commercial tools target this space, but from the human-ceremony side:

| Tool | Layer | Goal model |
|---|---|---|
| [Jira Align][jira-align] (Atlassian) | enterprise portfolio | strategic themes / OKRs cascade to stories; SAFe PI-planning ceremonies |
| [WorkBoard][workboard] (acquired Quantive / ex-Gtmhub, 2025) | strategy execution | OKR cascade + executive business reviews; human check-in cadence |
| [Tability][tability] (independent) | lightweight OKR | weekly check-in rituals, manual UI |
| [Productboard][productboard] | product discovery | customer feedback → prioritized features → roadmap; human insight votes |
| [LinearB][linearb] | engineering metrics | DORA / cycle-time from Jira + Git; assumes a human author per PR |

**The 2026 wrinkle — and the gap it leaves.** These tools now ship MCP servers (Atlassian's [Rovo MCP Server][atlassian-mcp] is GA; Jira, Productboard, and Linear all expose MCP endpoints), so an agent *can* read and write their work items. But MCP bolts agent **access** onto a human-authored, UI-first goal model — it does not make the goal store machine-native. None expose what the estate pattern needs: a machine-writable goal schema that agents author, a per-run `cost_usd` + `outcome` attribution row, autonomous idle-discovery goal generation, or a spend-based kill switch. As with the [OSS ALM landscape][oss-alm], the verdict is **none fit the agent-native need** — they instrument human goal-setting, not autonomous goal attribution.

## Connections

- [agentic-engineering-disciplines-landscape.md][disciplines] — this doc is the **goals** anchor of the credo's compound loop (its Layer 5, *Compound*).
- [agentic-sdlc-patterns.md][sdlc-patterns] — the reflector loop + cost gates instantiate the ADLC **Observe → Correct** phase the patterns doc flags as a gap.
- [Startup CTO Handbook → qte77 mapping][cto-map] — the traditional human-OKR baseline the estate maps its `goals.json` onto.
- [agentic-enterprise-os-landscape.md][enterprise-os] — the operating-environment layer around liminal-flux's self-operating account (six action roles across an 8-phase progression); the enterprise platforms surveyed there govern human-set goals but do not close this attribution loop.

### The substrate thread

Goal attribution is the top of a substrate stack this corpus tracks end-to-end: **file/graph/vector memory** ([agent-frameworks §4][frameworks]) persists agent state → **knowledge graphs / GraphRAG + graph visualization** ([agent-frameworks §7][frameworks]) structure it → **formal ontologies & semantic layers** ([semantic-layers-data-catalog][semantic]) formalize and govern its meaning → the **goal graph** here attributes work back to it → **enterprise agent-OS platforms** ([agentic-enterprise-os][enterprise-os]) operate the whole stack (and reveal the attribution gap). Each rung is one expression of the same *compound, don't drift* credo.

## Sources

| Source | Content |
|---|---|
| [qte77/qte77][qte77] | `goals.json` OKR schema, `docs/cto-handbook-mapping.md` (OKR home), `docs/architecture.md` (the goals→specs→builds→learnings loop) |
| [liminal-flux-gh-acc][liminal] | `docs/living-github-account.md` — inbound goals, idle discovery, `performance-log.jsonl` per-run tracing, reflector loop, cost gates |
| [research-ralphy][research-ralphy] | `config/prd-generation-prompt.md` — research-finding → PRD → `prd.json` story attribution |
| [ralph-loop-cc-tdd-wt-vibe-kanban-template][ralph-loop] | `ralph/README.md` — `prd.json` story record (id/depends_on/acceptance/files/status/wave) |
| [Jira Align][jira-align] | Enterprise portfolio: strategy→execution, OKR hub, SAFe |
| [WorkBoard][workboard] | Enterprise strategy execution / OKR (absorbed Quantive, ex-Gtmhub, 2025) |
| [Tability][tability] | Lightweight independent OKR / goal check-ins |
| [Productboard][productboard] | Product discovery: feedback → prioritized features → roadmap |
| [LinearB][linearb] | Engineering delivery metrics (DORA, cycle time) over Jira + Git |
| [Atlassian Rovo MCP Server][atlassian-mcp] | First-party evidence of the 2026 MCP-access layer over a human-authored goal model |
| [Startup CTO Handbook → qte77 mapping][cto-map] | Traditional human-OKR baseline mapped onto `goals.json` |

[qte77]: https://github.com/qte77/qte77
[liminal]: https://github.com/qte77/liminal-flux-gh-acc
[research-ralphy]: https://github.com/qte77/research-ralphy
[ralph-loop]: https://github.com/qte77/ralph-loop-cc-tdd-wt-vibe-kanban-template
[cto-map]: https://github.com/qte77/qte77/blob/main/docs/cto-handbook-mapping.md
[jira-align]: https://www.atlassian.com/software/jira/align
[workboard]: https://www.workboard.com/
[tability]: https://www.tability.io/
[productboard]: https://www.productboard.com/
[linearb]: https://linearb.io/
[atlassian-mcp]: https://www.atlassian.com/platform/remote-mcp-server
[disciplines]: agentic-engineering-disciplines-landscape.md
[sdlc-patterns]: agentic-sdlc-patterns.md
[oss-alm]: oss-alm-landscape.md
[enterprise-os]: ../non-cc/agentic-enterprise-os-landscape.md
[frameworks]: ../non-cc/agent-frameworks-infrastructure-landscape.md
[semantic]: ../non-cc/semantic-layers-data-catalog-landscape.md
