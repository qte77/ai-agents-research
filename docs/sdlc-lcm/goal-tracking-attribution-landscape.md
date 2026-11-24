---
title: Goal Tracking & Attribution Landscape
purpose: How an agentic coding fleet ties work to stated goals (top-down cascade, bottom-up attribution), with the qte77 estate as worked reference and the commercial OKR/PM tooling baseline it diverges from.
created: 2026-06-28
updated: 2026-11-23
validated_links: 2026-06-28
status: assess
---

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

The mature commercial tools target this space, but from the human-ceremony side (Tability has since added agent features, see its row):

| Tool | Layer | Goal model |
|---|---|---|
| [Jira Align][jira-align] (Atlassian) | enterprise portfolio | strategic themes / OKRs cascade to stories; SAFe PI-planning ceremonies |
| [WorkBoard][workboard] (acquired Quantive / ex-Gtmhub, 2025) | strategy execution | OKR cascade + executive business reviews; human check-in cadence |
| [Tability][tability] (independent) | lightweight OKR | check-in rhythm; on 2026-11-22 also agent check-ins that run on a schedule and an [MCP server][tability-mcp] that reads and updates goals, plans and tasks from Claude or ChatGPT |
| [Productboard][productboard] | product discovery | customer feedback → prioritized features → roadmap; human insight votes |
| [LinearB][linearb] | engineering metrics | DORA / cycle-time from Jira + Git; assumes a human author per PR |

**The 2026 wrinkle — and the gap it leaves.** These tools now ship Model Context Protocol (MCP) servers (Atlassian publishes a [Rovo MCP Server][atlassian-mcp], though the pages fetched on 2026-11-18 did not state its release stage, so the earlier "GA" label is dropped; Linear documents a [remote MCP server][linear-mcp] that finds, creates and updates issues, projects and comments, read-write by default; Jira and Productboard endpoints were not re-checked), so an agent *can* read and write their work items. But MCP bolts agent **access** onto a human-authored, UI-first goal model — it does not make the goal store machine-native. None expose what the estate pattern needs: a machine-writable goal schema that agents author, a per-run `cost_usd` + `outcome` attribution row, autonomous idle-discovery goal generation, or a spend-based kill switch. As with the [OSS ALM landscape][oss-alm], the verdict is **none fit the agent-native need** — they instrument human goal-setting, not autonomous goal attribution.

## Plan state as the goal predicate (2026-11 refresh)

A session-level goal needs a predicate that reads plan state, and Claude Code's `/goal` judge sees only the conversation, so the state must be printed there; see [CC-goal-analysis.md](../cc-native/sessions/CC-goal-analysis.md) and the cross-vendor [goal-loops-landscape.md](../non-cc/coding-agents/goal-loops-landscape.md).

Applied to the stores above (our synthesis, not vendor guidance): a predicate such as "every story in `prd.json` has `status` passed, shown by a command whose output is printed" ties the stop condition to the attribution ledger; a plan-row table with a done-when column works the same way. The ledger is the check; the goal only restates it.

**Strategy-level planning (above goals and specs): coverage gap.** A corpus search on 2026-11-18 found strategy only as the human OKR baseline above and the estate's `goals.json`; no doc covers agent-authored strategy or roadmap planning, and vendor docs were not searched for it in this pass. Treat it as unaudited, not as absent.

## Core vs context: classifying work (Moore)

Geoffrey Moore's core/context analysis (book *Dealing with Darwin*; Moore's Stanford talk is dated 2005-04-06) is a way to decide where scarce attention goes, and it can double as a classifier for the work this doc attributes to goals. Evidence level: Moore's framing is documented (his [Stanford talk page][moore-talk], which states the framework is used "to discuss how to overcome inertia in strategy and structure", and [Zone to Win page][moore-ztw]); the quadrant layout is confirmed by Moore's own 2×2 in his 2021-08-06 LinkedIn post (`linkedin.com/pulse/core-context-future-work-geoffrey-moore`; not a live link) and a [PDMA review][moore-pdma] of the book. The action labels (Deploy, Invent, Manage, Offload) come from an uploader's [slide deck][moore-slides], read as slide text only (the SlideShare copy was bot-blocked); Moore's own prose uses "extract resources" and "outsource" instead.

**The model (per the slide deck).** *Core* is the work that creates differentiation that wins customers; *context* is all other work. A second axis separates *mission-critical* work (a shortfall creates serious and immediate risk) from non-mission-critical. Crossing the two gives four quadrants, each paired with one action:

| | Mission-critical | Not mission-critical |
|---|---|---|
| **Core** | **Deploy** differentiation at scale | **Invent** the next differentiated offering (Moore calls this quadrant "enabling core") |
| **Context** | **Manage** at scale, and extract resources to repurpose for core (five levers: centralize, standardize, modularize, optimize, outsource) | **Offload** it, to fund the next innovation |

The deck also makes two dynamic points: core becomes context over time as it commoditizes, and resources get stuck "clinging to context", where mission-critical context work absorbs the people and money that core invention needs. That is the inertia point of the Stanford talk. (We could not watch the talk; only its one-line description was read.)

**The AI angle (one practitioner's claim).** A single-author [Medium essay][moore-ai] (2025-05-22, opinion, not research) argues the model needs an agent layer: its "Context Offloading (with Human-in-the-Loop)" has people supervise and validate agent output, while core stays human-led and agent-augmented, and the boundary stays fluid. Its sharpest point for us is that context work is where agents plausibly absorb effort, which maps onto the deck's Offload action and Moore's "extract resources"; whether that happens at a given team is an open empirical question, not something these sources show.

**How-to: classifying work items (this corpus's synthesis, not Moore's).** Keep two fields per item, `class: core|context` and `critical: yes|no`, set when the item is created or triaged, and reviewed when the goal set changes (the [attribution loop](#the-agentic-attribution-loop) already ties each item to a goal, so the goal is the natural place to decide core vs context once).

| Item | Where the label lives | Tally and review |
|---|---|---|
| Goal / milestone | On the goal record (e.g. an OKR entry in the [goal store](#qte77qte77--the-goal-store-and-okr-home)); children inherit it | Review quarterly: is this still core, or did it commoditize? |
| Issue / task / feature | Label pair or project field; default to the parent goal's class | Count open items per quadrant; a large Manage share is the "clinging to context" signal |
| Pull request | Inherit from the linked issue; no separate label | Merged PRs per quadrant per period |
| Agent run | Inherit from the attributed goal in the run log | Cost and run counts per quadrant; Offload/Manage items are the first candidates for full agent execution |
| Time spent | Sum item time (or run cost) by quadrant | Compare share spent on Invent/Deploy vs Manage/Offload against intent |

The classification is a judgment call per team; two reviewers can disagree, so record who set the label and when.

**Adjacent and orthogonal concepts** (all well known; each differs from core/context as noted):

- *Zone to Win* (Moore, [author page][moore-ztw]): adjacent, from the same author. Four zones (Performance, Productivity, Incubation, Transformation), each with its own operating model and metrics; it organizes by operating mode where core/context classifies by differentiation.
- *Wardley mapping* ([Learn Wardley Mapping][wardley]): adjacent. Places capabilities on an evolution axis (Genesis, Custom, Product, Commodity), which models the movement of core toward context as it commoditizes (our reading) more explicitly than a single slide does.
- *Jobs to be done* ([HBR, Christensen et al., 2016][jtbd]): orthogonal. Classifies work by the customer need it serves, not by whether it differentiates; useful to decide what is core (our reading), not a substitute for the classification.
- *Build vs buy / outsourcing*: the action layer of the context quadrants (Moore's own "outsource" lever is one instance); it is a decision, not a classification, so no separate source is cited.

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
| [Tability MCP server][tability-mcp] | Vendor page: read and update goals, plans and tasks from an MCP client (checked 2026-11-22) |
| [Productboard][productboard] | Product discovery: feedback → prioritized features → roadmap |
| [LinearB][linearb] | Engineering delivery metrics (DORA, cycle time) over Jira + Git |
| [Atlassian Rovo MCP Server][atlassian-mcp] | First-party evidence of the 2026 MCP-access layer over a human-authored goal model |
| [Linear MCP docs][linear-mcp] | Remote MCP server for issues, projects, comments; read-write default (checked 2026-11-18) |
| [Startup CTO Handbook → qte77 mapping][cto-map] | Traditional human-OKR baseline mapped onto `goals.json` |
| [Moore, Core and Context (Stanford)][moore-talk] | Talk page (dated 2005-04-06): one-line description of the core/context framework applied to inertia (video not watched; checked 2026-11-23) |
| `linkedin.com/pulse/core-context-future-work-geoffrey-moore` | Moore, "Core, Context and the Future of Work" (2021-08-06): his own core/context 2×2 incl. "enabling core" (not link-checked) |
| [PDMA review of Dealing with Darwin][moore-pdma] | Book review: outsourcing as an exhaust vent after centralize/standardize/modularize/optimize |
| [Moore, Dealing with Darwin slides][moore-slides] | Uploader's slide deck (secondary, slide text only): core/context quadrants, five levers (checked 2026-11-23) |
| [Moore, Zone to Win][moore-ztw] | Author's book page: four zones of enterprise work (checked 2026-11-23) |
| [Traveso, core vs context in the age of AI][moore-ai] | Single-author Medium essay (2025-05-22): agent layer on Moore's model; opinion |
| [Learn Wardley Mapping][wardley] | Wardley map components and the four evolution stages |
| [HBR, Know Your Customers' "Jobs to Be Done"][jtbd] | Christensen et al., 2016: jobs-to-be-done framing |

[qte77]: https://github.com/qte77/qte77
[liminal]: https://github.com/qte77/liminal-flux-gh-acc
[research-ralphy]: https://github.com/qte77/research-ralphy
[ralph-loop]: https://github.com/qte77/ralph-loop-cc-tdd-wt-vibe-kanban-template
[cto-map]: https://github.com/qte77/qte77/blob/main/docs/cto-handbook-mapping.md
[jira-align]: https://www.atlassian.com/software/jira-align
[workboard]: https://www.workboard.com/
[tability]: https://www.tability.io/
[tability-mcp]: https://www.tability.io/ai/mcp-server
[productboard]: https://www.productboard.com/
[linearb]: https://linearb.io/
[atlassian-mcp]: https://www.atlassian.com/platform/remote-mcp-server
[linear-mcp]: https://linear.app/docs/mcp
[disciplines]: agentic-engineering-disciplines-landscape.md
[sdlc-patterns]: agentic-sdlc-patterns.md
[oss-alm]: oss-alm-landscape.md
[enterprise-os]: ../non-cc/frameworks/agentic-enterprise-os-landscape.md
[frameworks]: ../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md
[semantic]: ../non-cc/infrastructure/semantic-layers-data-catalog-landscape.md
[moore-talk]: https://stvp.stanford.edu/av/core-and-context
[moore-slides]: https://www.slideserve.com/ellema/dealing-with-darwin-by-geoffrey-moore
[moore-ztw]: https://geoffreyamoore.com/book/zone-to-win/
[moore-ai]: https://medium.com/@ivantraveso/redrawing-the-business-core-vs-context-line-in-the-age-of-ai-an-updated-model-d56ed3f165b8
[wardley]: https://learnwardleymapping.com/introduction/
[jtbd]: https://hbr.org/2016/09/know-your-customers-jobs-to-be-done
[moore-pdma]: https://pdma.org/page/review_dealing_w_dar
