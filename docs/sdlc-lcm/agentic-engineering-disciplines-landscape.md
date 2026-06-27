---
title: Agentic Engineering Disciplines & Methodologies Landscape
purpose: Credo-framed synthesis of the "-engineering" disciplines (prompt → spec) and "-driven development" methodologies (TDD → EDD → SDD) that make an agentic coding fleet compound instead of drift — with first-party coiners, a five-layer stack, and qte77's open-agentic-coding-harness as the reference implementation.
category: landscape
created: 2026-06-23
updated: 2026-06-27
validated_links: 2026-06-27
---

**Status**: Assess

## What It Is

A map of the **disciplines** and **methodologies** of agentic coding, organized by the qte77 credo: a polyrepo agent fleet where *goals, specs, builds, and learnings compound instead of drift; agents drive, humans approve and steer.* Each discipline below is an instrument for that goal.

Two sibling vocabularies have crystallized in 2024–2026 — the **"-engineering"** disciplines (the *skills*: how to think about the environment around the model) and the **"-driven development"** methodologies (the *processes*: how to work) — and they compose into one five-layer stack. This doc is a **synthesis**; deeper per-tool coverage is cross-linked, not duplicated. It builds on the harness *patterns* in [CC-agentic-harness-patterns-analysis.md][harness-patterns] and the execution mechanics in [CC-dynamic-workflows-analysis.md][workflows]. The same shift surfaces in industry framing — Warp's Zach Lloyd reframes it as moving from *product engineers* to *factory engineers* (you build the system that builds the product), the practitioner mirror of *Agent = Model + Harness*.

## The five-layer stack

The same two control points recur at every layer: **"agents drive"** = the automatic/deterministic machinery; **"humans approve and steer"** = the review gates that catch drift.

| Layer | What it answers | Disciplines | Covered in |
|---|---|---|---|
| **1. Disciplines** (think) | how to think | prompt → context → harness → loop → flow → spec **engineering** | §1 below |
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
| **Flow engineering** | a structured multi-stage pipeline (reflect → generate → test → fix → validate) | **Itamar Friedman** / CodiumAI, [AlphaCodium][alphacodium] (arXiv 2401.08500, Jan 2024; +2.3× pass@5) | Established in code-gen |
| **Spec engineering / SDD** | machine-readable specs as the agent's source of truth | GitHub Spec-Kit (Sep 2025), Kiro (2025); [Fowler on SDD tools][fowler-sdd] | Emerging→mainstream |

**Nesting:** Spec → **Harness** {Instructions, State, Verification, Scope, Session-Lifecycle} → {Context → Prompt} + {Loop → Flow}. Context engineering runs *inside* the harness each turn; loop engineering *schedules above* the model turn but *below* the harness definition; flow engineering is a per-task workflow inside a loop tick; spec engineering is the *pre-harness* authoring step.

> This repo's **ACE-FCA** context rules (40–60% utilization, compaction triggers, subagent isolation) are an independent convergent implementation of Anthropic's context-engineering framework (`compress` = compaction, `isolate` = subagents) — now citable against a [first-party source][anthropic-ce].

NEW vs current repo coverage: the Anthropic context-engineering and OpenAI harness-engineering first-party anchors, **Flow Engineering** (no current coverage), and the **spec-engineering** landscape (see §3).

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
| [bmadcode/BMAD-METHOD][bmad] | 49,513 | NOASSERTION | multi-agent planning (Analyst/PM/Architect) → context-engineered dev |
| buildermethods/agent-os | 4,936 | MIT | MCP context-injection layer; pairs with any SDD framework |
| kirodotdev/Kiro | 3,912 | Proprietary | requirements→design→tasks "waves"; full IDE — see [kiro-analysis.md][kiro-doc] |
| Tessl (tile) | 41 | MIT | "spec-as-source" (spec is the maintained artifact); main framework closed-beta |

A full standalone comparison (`spec-driven-frameworks-landscape.md`) is a natural follow-up; this table is the synthesis-level entry.

## Reference implementation: open-agentic-coding-harness

qte77's sibling project [open-agentic-coding-harness][oach] implements the whole stack — `ralph-loop` (Layers 2–3: TDD + loop), `claude-code-plugins` (Layer 1: harness), `cc-recursive-team-mode` (Layer 3: teams), `coding-agent-eval` (Layer 4: deterministic EDD), and `LEARNINGS.md` refeeding (Layer 5: compound) — under "faithful adoption + measurability" ("you can't trust a harness you can't measure"). Per cross-repo routing, deep product analysis stays in that repo; here it is cited as the reference implementation of the disciplines above.

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
[frameworks]: ../non-cc/agent-frameworks-infrastructure-landscape.md
[observability]: ../cc-community/CC-agent-observability-methods-analysis.md
[memory]: ../cc-native/context-memory/CC-memory-system-analysis.md
[eval-data]: ../cc-community/CC-evaluation-data-resources-landscape.md
[sdlc-patterns]: agentic-sdlc-patterns.md
[ralph]: ../cc-native/agents-skills/CC-ralph-enhancement-research.md
[kiro-doc]: ../non-cc/kiro-analysis.md
