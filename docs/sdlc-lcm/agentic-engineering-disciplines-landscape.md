---
title: Agentic Engineering Disciplines & Methodologies Landscape
purpose: Credo-framed synthesis of the "-engineering" disciplines (prompt → spec) and "-driven development" methodologies (TDD → EDD → SDD) that make an agentic coding fleet compound instead of drift — with first-party coiners, a five-layer stack, and qte77's open-agentic-coding-harness as the reference implementation.
category: landscape
created: 2026-06-23
updated: 2026-09-30
validated_links: 2026-09-30
status: assess
---

## What It Is

A map of the **disciplines** and **methodologies** of agentic coding, organized by the qte77 credo: a polyrepo agent fleet where *goals, specs, builds, and learnings compound instead of drift; agents drive, humans approve and steer.* Each discipline below is an instrument for that goal.

Two sibling vocabularies have crystallized in 2024–2026 — the **"-engineering"** disciplines (the *skills*: how to think about the environment around the model) and the **"-driven development"** methodologies (the *processes*: how to work) — and they compose into one five-layer stack. This doc is a **synthesis**; deeper per-tool coverage is cross-linked, not duplicated. It builds on the harness *patterns* in [CC-agentic-harness-patterns-analysis.md][harness-patterns] and the execution mechanics in [CC-dynamic-workflows-analysis.md][workflows]. The same shift surfaces in industry framing — Warp's Zach Lloyd reframes it as moving from *product engineers* to *factory engineers* (you build the system that builds the product), the practitioner mirror of *Agent = Model + Harness*.

## The five-layer stack

The same two control points recur at every layer: **"agents drive"** = the automatic/deterministic machinery; **"humans approve and steer"** = the review gates that catch drift.

| Layer | What it answers | Disciplines | Covered in |
|---|---|---|---|
| **1. Disciplines** (think) | how to think | prompt → context → harness → loop → graph → flow → spec **engineering** | §1 below |
| **2. Methodology** (work) | how to work | TDD → BDD → EDD → SDD (+ DDD / ATDD / RDD) | §2 below |
| **3. Execution** (run) | how it runs | workflows, harness, the agentic loop | [CC-dynamic-workflows][workflows], [agent-frameworks §1/§3][frameworks] |
| **4. Feedback** (stay honest) | observe + verify | OTel tracing; hooks / EDD verify gates | [CC-dynamic-workflows §Observability][workflows], [CC-agent-observability][observability], eval landscapes |
| **5. Compound** (persist) | memory + learnings | CLAUDE.md, auto-memory, CRLA | [CC-memory-system][memory], `docs/learnings/` |

**Through-line:** Discipline → Methodology → Execution → Feedback → Compound. **EDD is the keystone** — simultaneously a Layer-2 methodology (evals-as-spec), a Layer-4 feedback mechanism (verify non-deterministic output), and the engine of Layer-5 compounding. The repo's own [agentic-sdlc-patterns.md][sdlc-patterns] ADLC (Build → Evaluate → Observe → Correct) is this loop.

**Org-adoption lens:** Pydantic's [Applied GenAI Maturity Model][pydantic-maturity] (Jun 2026) grades an organization across five dimensions — visibility, evaluation, cost governance, access/identity, and audit/incident-response — mapping onto Layers 4–5 above; it is a diagnostic for *which* layer's gaps currently bite, not a scoreboard to race.

## §1. The "-engineering" ladder

Each rung scaffolds the next; together they describe the environment built *around* the model ("the model doesn't change — the harness does").

| Discipline | One-line | Coiner / first-party anchor | Status |
|---|---|---|---|
| **Prompt engineering** | crafting the literal input text | GPT-3 era (Brown et al. 2020); Learn Prompting (Schulhoff) | Established, now "table stakes" |
| **Context engineering** | filling the context window with the right tokens each step | **Tobi Lütke** (X, Jun 2025), amplified by Karpathy; **Anthropic** canonical 4-component framework ([Effective Context Engineering][anthropic-ce], Sep 2025); LangChain *write/select/compress/isolate* | Emerging→established |
| **Harness engineering** | the full runtime environment (Instructions/State/Verification/Scope/Session-Lifecycle) | WalkingLabs ([learn-harness-engineering][walkinglabs], MIT); **OpenAI** independently ([Harness Engineering][openai-harness], Feb 2026, from the Codex effort); **Pydantic** ([The Harness Thesis][pydantic-thesis] + [What Makes a Good Harness][pydantic-good-harness], Jun 2026 — axioms: *disclosure* = just-in-time context/tools, *steering* = catch agent drift early) | Established in practice |
| **Loop engineering** | the outer autonomous cycle (schedule/spawn/persist across many ticks) | no single coiner; [ReAct][react] = inner loop; Ralph loop (Geoffrey Huntley, 2025) and [loop-engineering][loop-eng] (Cobus Greyling, 2026 — 7 production patterns, `loop-audit`/`loop-init`/`loop-cost` CLIs, Claude Code/Grok/Codex starter kits) = concrete outer-loop references | Emerging / buzzword |
| **Graph engineering** | wiring already-loop-shaped specialized agents (planner/implementer/reviewer/tester) into a topology — each node is still a loop; edges carry state, routing, and the gate the handoff must pass | **Hamel Husain** (X, `x.com/HamelHusain/article/2078346425621237935` — not fetchable, HTTP 402; verified via [Turing Post][turingpost-graph], "Loop Engineering Is Dead. Enter Graph Engineering.", published within hours of Peter Steinberger's question on 2026-07-18, `x.com/steipete/status/2078277297791189132`) | Emerging / contested naming — [Turing Post][turingpost-graph] found no confirmed Microsoft/Stanford/Anthropic adoption of a "graph engineering" discipline |
| **Flow engineering** | a structured multi-stage pipeline (reflect → generate → test → fix → validate) | **Itamar Friedman** / CodiumAI, [AlphaCodium][alphacodium] (arXiv 2401.08500, Jan 2024; +2.3× pass@5) | Established in code-gen |
| **Spec engineering / SDD** | machine-readable specs as the agent's source of truth | GitHub Spec-Kit (Sep 2025), Kiro (2025); [Fowler on SDD tools][fowler-sdd] | Emerging→mainstream |

**Nesting:** Spec → **Harness** {Instructions, State, Verification, Scope, Session-Lifecycle} → {Context → Prompt} + {Loop → Graph} + {Loop → Flow}. Context engineering runs *inside* the harness each turn; loop engineering *schedules above* the model turn but *below* the harness definition; graph engineering wires multiple already-built loop-nodes into a topology, sitting beside flow engineering rather than beneath it; flow engineering is a per-task workflow inside a loop tick; spec engineering is the *pre-harness* authoring step.

> This repo's **ACE-FCA** context rules (40–60% utilization, compaction triggers, subagent isolation) are an independent convergent implementation of Anthropic's context-engineering framework (`compress` = compaction, `isolate` = subagents) — now citable against a [first-party source][anthropic-ce].

NEW vs current repo coverage: the Anthropic context-engineering and OpenAI harness-engineering first-party anchors, **Flow Engineering** (no current coverage), and the **spec-engineering** landscape (see §3).

**Quantified evidence for the thesis:** [The Harness Effect][harness-effect] (Sayed Ali et al., 32 authors, Jul 2026) shows the orchestration layer — not model choice — dominates agentic cost/quality: holding six foundation models constant (Claude Sonnet 4.6, Gemini 3.1, Gemini Flash 3.5, Qwen 3.6, GLM 5.1, Palmyra X6), a purpose-built "Writer Agent Harness" cut blended cost per task 41% ($0.21→$0.12), with the efficiency gain model-invariant (every model 33–61% cheaper) while quality gains correlated almost perfectly with each model's baseline strength (r=0.99) — direct quantitative support for *Agent = Model + Harness*.

**2026 harness-evolution research cluster:** three Aug–Sep 2026 arXiv papers extend the harness-as-evolvable-artifact line from [HarnessX][harnessx] (composable scaffolding evolved from execution traces) into concrete benchmarking and optimization. **HarnessDev** ([arXiv:2609.01437][harnessdev], Wu et al., Sep 2026) benchmarks whether LLMs can build and iteratively evolve their own execution harness (2,207 instances, 6 LLMs, 4 domains) — generated harnesses beat human-engineered references for writing and ML-experimentation tasks but lag for coding/research, and evolution gains transfer poorly across models. **AutoDesign** ([arXiv:2608.13560][autodesign-paper], [repo][autodesign-repo], Luo et al., Aug 2026, 227★, MIT + third-party-notices addendum) frames design as a long-horizon agentic process and runs "Meta-Harness Optimization" — a meta-harness optimizer that recursively improves a task-specific *DesignHarness* from failure feedback — for +12.4% on academic paper-to-poster generation (78.32 on PosterBench). **RobustSGPO** ([arXiv:2609.09646][robustsgpo], Zhao et al., Sep 2026) controls the search space of semantic-gradient prompt optimization for harness evolution, lifting an AgentX brainstorming workflow's completion rate 60%→80% across 120 tasks. Full harness-as-primitive analysis: [harnessx-analysis.md][harnessx].

**Design lens — graph engineering names the wiring, not new model behavior:** André Lindenberg's *From Loops to Graphs* (LinkedIn, 2026-07-25; `linkedin.com/pulse/from-loops-graphs-andré-lindenberg-m8jae`) reads the term above against the software factories already shipping — StrongDM, OpenAI's Symphony, Stripe's Minions, Ramp's Inspect, WorkOS's Project Horizon — as graphs that were "always there": intake, builder, review, test and incident-feedback nodes wired by edges, each edge only as trustworthy as the gate sitting on it. "A graph's throughput is set by its narrowest verified edge, not by its widest generating node." Deeper coverage of the same human-gate convergence (spec and merge as the two gates that hold, Dex Horthy's `wsff.md` dissent on why lights-off factories degrade) already lives in [software-factory-landscape.md §(c)][software-factory] — this entry is the ladder-rung framing, not a restatement.

**Harness engineering's Verification axiom — three 2026 data points on its cost (design lens, Lindenberg's *Artificial Engineering*):** Dan Shapiro's zero-indexed five-levels framework ([*The Five Levels*][shapiro-five-levels], 2026-01-23) names Level 3 as the rung most teams get stuck on — "Your life is diffs," his own words for the agent generating while a human reviews every line — and Level 4 ("Then you leave for 12 hours, and check to see if the tests pass") as the one the Verification axiom actually describes — machine verification standing in for unread diffs. The jump is not free: METR's randomized controlled trial (16 experienced open-source developers, 246 real tasks, [metr.org][metr-rct], 2025-07-10) found developers *estimated* AI had made them 20% faster after the fact, while the clock measured them 19% *slower*. [Faros AI][faros-whiplash]'s own published telemetry (22,000 developers, two years, 4,000 teams — fetched 2026-09-30) independently shows the same shape at the fleet level: +242.7% incidents per PR and +54% bugs per developer accompany high AI adoption (Faros measures adoption intensity, not Shapiro's levels directly). Lindenberg reads that fleet-level telemetry as the shadow of teams staying parked on Level-3 review load instead of building a Level-4 verifier (Lindenberg, *The Most Expensive Rung on the Ladder*, LinkedIn, 2026-08-08, `linkedin.com/pulse/most-expensive-rung-ladder-andré-lindenberg-l2oqe`; *The Half We Don't Budget For*, LinkedIn, 2026-08-01, `linkedin.com/pulse/half-we-dont-budget-andré-lindenberg-pinxe`).

  **Specula** ([arXiv:2607.25333][specula-arxiv], Cheng et al., 9 authors, Jul–Aug 2026 v2 — already cited for its security-bug-finding angle in [agent-code-analysis-landscape.md][acal], not restated here) is a concrete Level-4 verifier for concurrent/distributed system code: coding agents write TLA+ specs, instrument the real code to collect execution traces, and pair trace-conformance checking with invariant checking so neither an overfit model nor an under-specified one passes alone. Verified directly from the paper: 48 OSS projects (36 distributed, 12 concurrent; 7 languages; 2K–95K LoC), 249 bugs found (207 new, 42 previously known), 89 reported to maintainers of which 68 are confirmed and 24 fixed; cost per system check $19–$168 (median $57; 1.43–9.86 hours); on a five-system subset (Autobahn, CometBFT, libspdm, MongoDB, sofa-jraft) scored against its own SysMoBench-derived quality metric, specification quality holds at 93% overall with Claude Sonnet-4.6 but falls to 47% with Haiku-4.5 — the verifier's own reliability is model-dependent. The companion benchmark [SysMoBench][sysmobench-arxiv] (Cheng et al., arXiv:2509.23130, Sep 2025 – Jan 2026 v3) independently scores AI-generated TLA+ models against syntax/runtime/conformance/invariant metrics across eleven real system artifacts; its own write-up ([SIGOPS blog][sysmobench-writeup], fetched 2026-09-30) confirms the newsletter's aggregate — "even the latest leading LLMs average around 46% on conformance and 41% on invariant" — with three named failure modes: a ZooKeeper vote-storage model that unions old and new votes where the real system's map overwrites the previous one, a ZooKeeper leader-election model that fuses two sequential steps into one guarded atomic action, and a model that reproduces the Raft paper's own appendix rather than Etcd's actual implementation.

  **Bend 2** ([bendlang/bend][bend-repo], Apache-2.0, 23,165★/713 forks — `gh api`, 2026-09-30) is a harder Level-4 bet: its own README poses "how can you trust AI code, without reading it?" and answers that its compiler "guarantees" a declared `LAWS.bend` rule always holds "by demanding mathematical proof whenever your code is edited" (README fetched via `gh api repos/bendlang/bend/readme`, 2026-09-30) — Lindenberg's framing reads that as rejecting sampling-based verification (tests, review) in favor of a categorical gate. Its Hacker News launch thread ([item 49746163][bend-hn], 616 points/327 comments as re-verified 2026-09-30) carries the sharpest objection in public — "the issue is I'll have to vibecode all the laws and the laws could be wrong" (user garrisonj) — because the laws are still written by someone, so Bend hardens what was specified without closing the completeness gap. Martin Kleppmann's cost anchor for this style of verification ([kleppmann.com][kleppmann-sel4], 2025-12-08) is the seL4 microkernel: as of 2009, 8,700 lines of C required 20 person-years and 200,000 lines of Isabelle proof — 23 lines of proof for every line of implementation (Lindenberg, *Laws Instead of Diffs*, LinkedIn, 2026-09-19, `linkedin.com/pulse/laws-instead-diffs-andré-lindenberg-wxlmf`).

## §2. The "-driven development" ladder

The trajectory is *bounding the unboundable* — from deterministic asserts toward probabilistic-output verification.

```text
TDD (2002)            BDD (2006)               EDD (2023–)              SDD (2024–)
deterministic tests → behavioral specs    →   eval suites          +  specs as source of truth
Red-Green-Refactor    Given-When-Then          LLM-judge + human       Spec→Plan→Tasks→Implement
```

| Methodology | Originator | Agentic relevance |
|---|---|---|
| **TDD** | Kent Beck (2002) | R-G-R = a deterministic stop-condition per agent task (Ralph loop already does this). Farley: "TDD is **design**, not testing." |
| **BDD** | Dan North ([Introducing BDD][bdd], 2006) | Given-When-Then = LLM-readable executable specs ≈ ideal agent task boundaries (Given=setup, When=action, Then=assert) |
| **EDD** | **provenance uncertain** — no single coiner; Hamel Husain ([Your AI Product Needs Evals][husain-evals], 2024), LangChain/Dosu (2024) | evals = the regression suite for non-deterministic output. **Husain cautions against strict "eval-first"** — discover failures, *then* write evaluators |
| **SDD** | category, 2024–25 (Spec-Kit, Kiro, OpenSpec) | spec → plan → tasks → implement *is* the core agentic loop; human review shifts from code to spec. Complements EDD: SDD = *what*, EDD = *how to verify* |
| siblings | ATDD (Uncle Bob/Farley "executable specifications"), DDD (Eric Evans 2003 — "a trained model is a bounded context"), README-driven (Preston-Werner 2010), contract/schema-driven, prompt-driven (vibe coding, Karpathy 2025; synthesized end-to-end in the Kaggle/Google [*New SDLC With Vibe Coding*][kaggle-sdlc] whitepaper — Osmani/Saboo/Kartakis — which frames the vibe-coding→agentic-engineering arc as *Agent = Model + Harness*) | — |

**Dave Farley** (Continuous Delivery Ltd; *Continuous Delivery* 2010, *Modern Software Engineering* 2021; courses at `courses.cd.training`) is the throughline authority: TDD as a *design* tool (the *Driven* is load-bearing) with three mindsets (developer/tester/architect); BDD as *outside-in* acceptance testing ("Executable Specifications"); and CD/MSE as **empirical, small-step, fast-feedback** engineering — the same discipline a compounding agent fleet needs. *(davefarley.net carried an expired TLS cert at the 2026-06-23 access; cited from secondary sources.)*

NEW vs current repo coverage: **BDD, ATDD, EDD-as-methodology, Dave Farley, DDD+LLM, README-driven, contract-driven** — none are currently covered. The eval *tools* (DeepEval/RAGAs/TruLens) are in [CC-evaluation-data-resources-landscape.md][eval-data]; EDD is the *methodology* that gives them purpose.

## §3. Spec-driven frameworks (the 2025–26 inflection)

By 2026 every major coding tool shipped an SDD flavor. Stars verified via `gh api`, 2026-06-23:

| Framework | Stars | License | Workflow / note |
|---|---|---|---|
| [github/spec-kit][spec-kit] | 114,808 | MIT | Spec → Plan → Tasks → Implement; 30+ agent integrations, 70+ extensions ("intent is the source of truth") |
| [Fission-AI/OpenSpec][openspec] | 56,043 | MIT | Proposal → Apply → Archive; no MCP/keys required |
| [bmadcode/BMAD-METHOD][bmad] | 49,513 | MIT | multi-agent planning (Analyst/PM/Architect) → context-engineered dev |
| buildermethods/agent-os | 4,936 | MIT | MCP context-injection layer; pairs with any SDD framework |
| kirodotdev/Kiro | 3,912 | Proprietary | requirements→design→tasks "waves"; full IDE — see [kiro-analysis.md][kiro-doc] |
| Tessl (tile) | 41 | MIT | "spec-as-source" (spec is the maintained artifact); main framework closed-beta |

A full standalone comparison (`spec-driven-frameworks-landscape.md`) is a natural follow-up; this table is the synthesis-level entry.

**Adjacent 2026 developments:** Anthropic's own [The AI-Native SDLC Playbook][anthropic-sdlc] (Aug 2026) operationalizes SDD as a committed artifact chain — "the intent, the spec, the plan, the diff and the review findings are the audit trail" — across six loop stages (Plan/Design/Build/Test/Deploy/Maintain), with a control-band breach in production writing the next `intent.md` to restart the loop. `CLAUDE.md` carries institutional knowledge across sessions; **Skills** encode organizational policy as advisory, reusable constraints; **Hooks** are the deterministic enforcement layer (blocking unsafe edits, gating approvals); **Evals** form the regression suite triggered on config/prompt changes. A human always accepts the spec before build starts, consulting a technical lead for anything the org classes as higher-risk; humans also approve the implementation plan and hold exclusive PR-merge and deploy authorization. In an adjacent domain, [SMART][smart] (Kushnir, Noorbakhsh, Sreedhar et al., Sep 2026) pushes design-docs-as-source past code review into ML systems tooling: an ML performance-modeling repo holds "almost no code," only a DAG of natural-language design docs, and coding sub-agents regenerate the implementation from the docs on each version update — validated against hand-audited reference models including DeepSeek-V3.

## Reference implementation: open-agentic-coding-harness

qte77's sibling project [open-agentic-coding-harness][oach] implements the whole stack — `ralph-loop` (Layers 2–3: TDD + loop), `claude-code-plugins` (Layer 1: harness), `cc-recursive-team-mode` (Layer 3: teams), `coding-harness-eval` (Layer 4: deterministic EDD), and `LEARNINGS.md` refeeding (Layer 5: compound) — under "faithful adoption + measurability" ("you can't trust a harness you can't measure"). Per cross-repo routing, deep product analysis stays in that repo; here it is cited as the reference implementation of the disciplines above.

## Cross-References

- [CC-dynamic-workflows-analysis.md][workflows] — execution + observability + verify surfaces (Layers 3–4)
- [CC-agentic-harness-patterns-analysis.md][harness-patterns] — the 12 harness patterns (Layer 1/3)
- [agent-frameworks-infrastructure-landscape.md][frameworks] — orchestration frameworks, RAG, §8 output validation
- [agentic-sdlc-patterns.md][sdlc-patterns] — the ADLC this stack instantiates
- [CC-ralph-enhancement-research.md][ralph] — the Ralph loop in this repo's tooling
- [Startup CTO Handbook → qte77 mapping][cto-map] — the traditional human-team engineering-leadership baseline these agentic disciplines diverge from

## Sources

| Source | Content |
|---|---|
| [Anthropic — Effective Context Engineering][anthropic-ce] | Canonical 4-component context-engineering framework |
| [Anthropic — Building Effective Agents][anthropic-bea] | Workflows-vs-agents; 5 patterns |
| [OpenAI — Harness Engineering][openai-harness] | Convergent harness definition; Codex throughput evidence |
| [Pydantic — The Harness Thesis][pydantic-thesis] · [What Makes a Good Harness][pydantic-good-harness] | Harness > model; *disclosure* + *steering* operational axioms |
| [Pydantic — Applied GenAI Maturity Model][pydantic-maturity] | 5-dimension org-adoption maturity diagnostic |
| [The Harness Effect (arXiv 2607.06906)][harness-effect] | Orchestration-layer cost/token economics; quantitative *Agent = Model + Harness* evidence |
| [HarnessX analysis][harnessx] | Composable, trace-evolved harness foundry — the repo's existing harness-evolution coverage |
| [HarnessDev (arXiv 2609.01437)][harnessdev] | Benchmark: can LLMs build and evolve their own harness? |
| [AutoDesign (arXiv 2608.13560)][autodesign-paper] · [repo][autodesign-repo] | Meta-harness optimization for long-horizon agentic design |
| [RobustSGPO (arXiv 2609.09646)][robustsgpo] | Search-space control for agent harness evolution |
| [Anthropic — The AI-Native SDLC Playbook][anthropic-sdlc] | intent.md→spec.md→plan.md artifact chain; CLAUDE.md/Skills/Hooks/Evals loop |
| [SMART (arXiv 2609.05364)][smart] | Design-docs-as-source ML performance tool; docs-only repo regenerated by coding sub-agents |
| André Lindenberg — *From Loops to Graphs* (LinkedIn, 2026-07-25; `linkedin.com/pulse/from-loops-graphs-andré-lindenberg-m8jae`) | Design lens: graph engineering as the wiring already present in shipped software factories (LinkedIn — not link-checked) |
| Hamel Husain — "Loop Engineering Is Dead. Enter Graph Engineering." (X, 2026-07-18; `x.com/HamelHusain/article/2078346425621237935`) | Coining post for "graph engineering" (X returns HTTP 402 — not fetchable/link-checked; existence and content verified via Turing Post) |
| [Turing Post — Is Graph Engineering Real?][turingpost-graph] | Independent verification of Hamel Husain's coining post + debunks Microsoft/Stanford/Anthropic misattribution |
| André Lindenberg — *The Most Expensive Rung on the Ladder* (LinkedIn, 2026-08-08; `linkedin.com/pulse/most-expensive-rung-ladder-andré-lindenberg-l2oqe`) | Design lens: Level-3 review-cost trap vs. Level-4 verifier build-out (LinkedIn — not link-checked) |
| [Dan Shapiro — The Five Levels][shapiro-five-levels] | Zero-indexed six-level AI-dev framework; Level 3 "your life is diffs" / Level 4 spec-manager |
| [METR — Measuring the Impact of Early-2025 AI][metr-rct] | RCT: 16 developers, 246 tasks; developers estimated 20% faster, measured 19% slower |
| [Faros AI — The Acceleration Whiplash][faros-whiplash] | Telemetry: 22K developers/4K teams/2yr; +242.7% incidents per PR, +54% bugs/developer (fetched 2026-09-30) |
| André Lindenberg — *The Half We Don't Budget For* (LinkedIn, 2026-08-01; `linkedin.com/pulse/half-we-dont-budget-andré-lindenberg-pinxe`) | Design lens: verification-budget asymmetry; Specula as a closing move (LinkedIn — not link-checked) |
| [Specula (arXiv:2607.25333)][specula-arxiv] | TLA+ trace+invariant verifier; 48 projects, 249 bugs (207 new), 68 confirmed/24 fixed, $19–168/median $57 |
| [SysMoBench (arXiv:2509.23130)][sysmobench-arxiv] | Companion benchmark: AI-generated TLA+ model-code conformance, per-system/per-model scores |
| [SysMoBench SIGOPS write-up][sysmobench-writeup] | Confirms ~46%/41% conformance/invariant aggregate + 3 named LLM modeling failure modes |
| André Lindenberg — *Laws Instead of Diffs* (LinkedIn, 2026-09-19; `linkedin.com/pulse/laws-instead-diffs-andré-lindenberg-wxlmf`) | Design lens: proof-gated compiler as a harder Level-4 bet (LinkedIn — not link-checked) |
| [bendlang/bend][bend-repo] | Apache-2.0, 23,165★ (`gh api`, 2026-09-30); proof-gated language, HN launch |
| [Bend Hacker News thread][bend-hn] | 616 points/327 comments (2026-09-30); "vibecode all the laws" skepticism quoted |
| [Martin Kleppmann — AI and formal verification][kleppmann-sel4] | seL4: 8,700 LOC / 20 person-years / 200,000 Isabelle lines (2025-12-08) |
| [AlphaCodium (arXiv 2401.08500)][alphacodium] | Flow engineering; Itamar Friedman / CodiumAI |
| [ReAct (arXiv 2210.11610)][react] | Inner-loop foundation |
| [WalkingLabs learn-harness-engineering][walkinglabs] | 5-subsystem harness model (MIT) |
| [Dan North — Introducing BDD][bdd] | BDD origin / Given-When-Then |
| [Hamel Husain — Your AI Product Needs Evals][husain-evals] | EDD primary practitioner reference |
| [Martin Fowler — SDD tools][fowler-sdd] | Spec-driven development survey |
| [Kaggle/Google — The New SDLC With Vibe Coding][kaggle-sdlc] | Vibe-coding→agentic-engineering synthesis; *Agent = Model + Harness* (Osmani, Saboo, Kartakis) |
| [cobusgreyling/loop-engineering][loop-eng] | Concrete loop-engineering reference — production patterns, readiness/scaffold/cost CLIs, CC/Grok/Codex starter kits |
| [GitHub Spec-Kit][spec-kit] · [OpenSpec][openspec] · [BMAD-METHOD][bmad] · [Kiro specs][kiro] | SDD frameworks |
| [qte77/open-agentic-coding-harness][oach] | Reference implementation (sibling repo) |
| Tobi Lütke / Karpathy (X, Jun 2025); Dave Farley (davefarley.net / courses.cd.training); Geoffrey Huntley Ralph loop (2025) | Attributions cited in prose (no stable/linkable URL) |
| Zach Lloyd / Warp — *We are now factory engineers, not product engineers* (LinkedIn memo, 2026) | Industry framing of the "-engineering" shift: build the system that builds the product (LinkedIn — not link-checked) |
| *Talking AI* podcast — agentic development & the future of engineering (Hatchworks, 2026) | Practitioner perspective on the agentic-engineering shift (LinkedIn — not link-checked) |
| [Lenny's Newsletter — AI][lennys] | Practitioner essays on agentic adoption & AI-first product/eng workflows (e.g. "Not all AI agents are created equal") — perspective layer, not a technical reference |
| [Startup CTO Handbook (Goldberg)][cto-handbook] · [qte77 mapping][cto-map] | Traditional engineering-leadership baseline — contrast to the agentic disciplines |

[anthropic-ce]: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
[anthropic-bea]: https://www.anthropic.com/research/building-effective-agents
[openai-harness]: https://openai.com/index/harness-engineering/
[pydantic-thesis]: https://pydantic.dev/articles/the-harness-thesis
[pydantic-good-harness]: https://pydantic.dev/articles/what-makes-a-good-harness
[pydantic-maturity]: https://pydantic.dev/articles/applied-generative-ai-maturity-model
[alphacodium]: https://arxiv.org/abs/2401.08500
[react]: https://arxiv.org/abs/2210.11610
[walkinglabs]: https://github.com/walkinglabs/learn-harness-engineering
[cto-handbook]: https://github.com/ZachGoldberg/Startup-CTO-Handbook
[lennys]: https://www.lennysnewsletter.com/t/ai
[cto-map]: https://github.com/qte77/qte77/blob/main/docs/cto-handbook-mapping.md
[bdd]: https://dannorth.net/blog/introducing-bdd/
[husain-evals]: https://hamel.dev/blog/posts/evals/
[fowler-sdd]: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
[kaggle-sdlc]: https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding
[loop-eng]: https://github.com/cobusgreyling/loop-engineering
[spec-kit]: https://github.com/github/spec-kit
[openspec]: https://github.com/Fission-AI/OpenSpec
[bmad]: https://github.com/bmadcode/BMAD-METHOD
[kiro]: https://kiro.dev/docs/specs/
[oach]: https://qte77.github.io/open-agentic-coding-harness/
[workflows]: ../cc-native/agents-skills/CC-dynamic-workflows-analysis.md
[harness-patterns]: ../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md
[frameworks]: ../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md
[observability]: ../non-cc/protocols/agent-observability-methods-analysis.md
[memory]: ../cc-native/context-memory/CC-memory-system-analysis.md
[eval-data]: evaluation-data-resources-landscape.md
[sdlc-patterns]: agentic-sdlc-patterns.md
[ralph]: ../cc-native/agents-skills/CC-ralph-enhancement-research.md
[kiro-doc]: ../non-cc/coding-agents/kiro-analysis.md
[harness-effect]: https://arxiv.org/abs/2607.06906
[harnessx]: ../non-cc/reference/harnessx-analysis.md
[harnessdev]: https://arxiv.org/abs/2609.01437
[autodesign-paper]: https://arxiv.org/abs/2608.13560
[autodesign-repo]: https://github.com/Yaxin9Luo/AutoDesign
[robustsgpo]: https://arxiv.org/abs/2609.09646
[anthropic-sdlc]: https://claude.com/blog/the-ai-native-sdlc-playbook
[smart]: https://arxiv.org/abs/2609.05364
[turingpost-graph]: https://www.turingpost.com/p/is-graph-engineering-real-why-everyone-is-talking-about-it
[shapiro-five-levels]: https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/
[metr-rct]: https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/
[faros-whiplash]: https://www.faros.ai/research/ai-acceleration-whiplash
[specula-arxiv]: https://arxiv.org/abs/2607.25333
[sysmobench-arxiv]: https://arxiv.org/abs/2509.23130
[sysmobench-writeup]: https://www.sigops.org/2026/can-llms-model-real-world-systems-in-tla/
[bend-repo]: https://github.com/bendlang/bend
[bend-hn]: https://news.ycombinator.com/item?id=49746163
[kleppmann-sel4]: https://martin.kleppmann.com/2025/12/08/ai-formal-verification.html
[acal]: agent-code-analysis-landscape.md
[software-factory]: software-factory-landscape.md
