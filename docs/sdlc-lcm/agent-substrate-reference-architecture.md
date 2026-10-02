---
title: Agent Substrate Reference Architecture — a Shared, Versioned, Traceable Memory and Context Layer
purpose: Synthesis of the plan 0009 rubric rows into one store-first reference architecture for shared, versioned, traceable agent memory and context, with each cell linked to its scored row and the layers mapped to qte77 estate repos.
created: 2026-09-30
updated: 2026-10-02
validated_links: 2026-09-30
status: reference
---

**Details:** synthesis — adds no new facts, re-scores nothing

## What It Is

The [plan 0009][plan] arc scored 61 tools, papers and systems across 21 corpus docs against the
[agent substrate rubric][rubric] (a census of every dated rubric row, taken 2026-09-30). This page
reads those rows as one architecture: which properties the field already delivers, which component
delivers each, and what no scored row delivers yet. Every cell below links the doc section that holds
the original score; nothing is re-scored here. [Plan 0010][plan-0010] (2026-10-02) extended the census to
75 rows in 28 docs. Every row now declares its subject with a `subject:` tag (rubric rule 4), and
`make census` regenerates the matrix below from the corpus.

Reading rule for the tables: a cell is `open` when no row of that subject reaches `partial`; otherwise it
shows the best score found and one row at that score. The linked section lists the rest.

## The argument: store first, model as client

**Reproducible is the discriminating property.** Nine of the 75 rows score `yes` on it, in three shapes:

1. **No LLM in the write path.** [agent-memory][memtool] ("files are the truth; every index is a
   rebuildable cache"), [AgentiCow][fw4] (copy-on-write reads), [Beads][fw4] (Dolt is commit-addressed),
   [lossless-memory][fw4] (indexes rebuild from raw logs) and [open-ontologies][ont] (Lean-checked
   certificates, pinned Oxigraph).
2. **LLM output recorded, then replayed.** [OrcaReplay][orca] ("Reproduce the run byte-for-byte with no
   model called").
3. **Model pinned by checksum or ID.** [Laya][laya] (checkpoints pinnable by revision and SHA-256, though
   unpinned by default; one deterministic forward pass, no generation step), [kev][kev] (SHA-256-checksummed release weights, a frozen eval suite) and
   [SkillLift][skilllift] (endpoint-configured models, pinned runtime requirements, checked-in results).

Everywhere an unpinned LLM writes into the store, the score stops at `partial` or `no`: [Omnigraph][fw7p],
[Semantica][fw7p], [Cognee][fw4], [LightRAG][fw7g], [HydraDB][fw4], [LlamaParse][fw7], the [AWS
context-ontology-accelerator][ont], [EvoOntology][ont] (its evolution runs on several unpinned LLM
backbones), [Archon and AX][fw1] and the [RRSI][rrsi] proposer are `partial`;
[GraphRAG][fw7g], [WeKnora][fw7p] and [BrainAPI][fw7p] are `no`; [Paperclip][fw1] is `no data`. This is
also why the plan's [graph-system decision][plan-g] kept a deterministic base graph and treats LLM
extraction as an overlay.

The consequence is a store-first design: keep state in a store that is itself a version-control system
(Dolt in Beads, Lance in Omnigraph, git in the ontology and skills rows, a bitemporal ledger in
[Utopia][ont]), and make the model a **client** of that store — it proposes writes, it does not own the
state. **Versionable** and **Traceable** then come from the store, not from the model: [Beads][fw4] is the
only row with `yes` on all six properties, and it is a tracker whose data layer branches, merges and
carries an audit trail. The [software-factory landscape][sf-c] adds the design lens (rUv's "fluid
software" post): the faster software changes, the more a recorded, replayable history matters. That lens
is stated there; this page does not restate it.

## Evidence matrix

Best score per subject and property, one exemplar row each, derived from the census.

| Subject | Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|---|
| Memory | yes — [Beads][fw4] | yes — [Beads][fw4] | yes — [Beads][fw4] | yes — [Beads][fw4] | yes — [Beads][fw4] | yes — [Beads][fw4] |
| Ontology | yes — [AWS context-ontology-accelerator][ont] | yes — [AWS context-ontology-accelerator][ont] | yes — [open-ontologies][ont] | yes — [AWS context-ontology-accelerator][ont] | yes — [open-ontologies][ont] | yes — [AWS context-ontology-accelerator][ont] |
| Graphs/RAG/hybrid | yes — [Omnigraph][fw7p] | yes — [Omnigraph][fw7p] | partial — [Omnigraph][fw7p] | yes — [Omnigraph][fw7p] | yes — [Omnigraph][fw7p] | yes — [Omnigraph][fw7p] |
| Context | partial — [Redis Iris Context Retriever][redis-ctx]; [CLAUDE.md][ccmem] under rule 6 | partial — [Redis Iris Context Retriever][redis-ctx]; [CLAUDE.md][ccmem] under rule 6 | open (best: no data) | yes — [CLAUDE.md][ccmem] | yes — [context-engineering-intro][cei] | partial — [CLAUDE.md][ccmem] |
| Skills | yes — [org skill provisioning][orgskills] | yes — [org skill provisioning][orgskills] | yes — [SkillLift][skilllift] | yes — [SkillLift][skilllift] | yes — [SkillLift][skilllift] | yes — [SkillLift][skilllift] |
| Plugins | yes — [OpenAI plugins][oaiplug] | partial — [OpenAI plugins][oaiplug] | partial — [OpenAI plugins][oaiplug] | yes — [OpenAI plugins][oaiplug] | yes — [OpenAI plugins][oaiplug] | yes — [Code Modernization][codemod] |
| Harness | yes — [OpenShell][openshell] | yes — [OpenShell][openshell] | yes — [Laya][laya] (decision-model rows; harness loops reach partial) | yes — [OpenShell][openshell] | yes — [Paperclip][fw1] | yes — [OpenShell][openshell] |
| Long-running | partial — [OpenResearch][openresearch] | yes — [OpenResearch][openresearch] | yes — [OrcaReplay][orca] (local replay; Distributed is no) | yes — [OrcaReplay][orca] | yes — [OrcaReplay][orca] | yes — [OrcaReplay][orca] |

Two cells need their caveat read with them. Harness·Reproducible is `yes` only through the decision-model
rows (Laya, kev); the harness loops themselves — [Archon, AX][fw1], [RRSI][rrsi], [OpenShell][openshell]
— top out at `partial`. Long-running·Reproducible is `yes` through OrcaReplay's local replay; the two rows
that run off-box ([OpenResearch][openresearch], [triagebot-action][sf-rubric]) are `partial`.

## Layers

**Store.** One canonical store that is a version-control system for its own data, read and written by
every agent and session: Dolt under [Beads][fw4] (branch, merge, `bd dolt push`/`pull`), Lance under
[Omnigraph][fw7p] ("branchable, time-travelable"), git under [Ontology Atlas][ont] ("Your disk is the
database; Git is the history") and under every git-hosted skills row, and a plain-file truth with a
rebuildable index under [agent-memory][memtool] and [lossless-memory][fw4]. Derived indexes are
disposable; the store is not.

**Write path: propose → gate → commit.** Agents draft; something deterministic or human accepts; only
accepted changes land in the store. [RRSI][rrsi] drafts each candidate in its own git worktree and
fast-forwards the branch on acceptance, so "the incumbent is always a commit"; [EvoOntology][ont]
publishes a Candidate only when paired evaluation beats its Parent; [Utopia][ont] and the [AWS
accelerator][ont] route agent writes through a review queue; [human-review][hr] and [Ontology Atlas][ont]
put a human diff review in front of the commit; [agent-memory][memtool] lets an unattended pass add or
update but never delete without confirmation. [mex][mex] (an Inbox draft a human publishes into git;
described in the corpus but not rubric-scored) is the same shape.

**Share.** Concurrency is defined by the store's own semantics, not by the agent: branch-and-merge
([Omnigraph][fw7p] runs "hundreds of agents" on isolated branches; [AgentiCow][fw4] branches one shared
base memory; [Beads][fw4] avoids collisions with hash IDs), an elected single writer per cell
([HydraDB][fw4]), workspace RBAC ([WeKnora][fw7p], the [AWS accelerator][ont]), or explicit intent
registration before writing ([mcp-git-coord][fw1]).

**Trace.** Every write carries lineage and every output cites what it read: PROV-O provenance and a live
mutation registry in [Semantica][fw7p], actor/audit tracking on every mutation in [Omnigraph][fw7p], a
per-edit record of hypothesis, score and verdict in [RRSI][rrsi], a byte-for-byte run trace in
[OrcaReplay][orca], one OpenTelemetry trace per turn in [hermes-runtype-otel][fw1], an `llm-audit.jsonl`
in [Ontology Atlas][ont], and `bd show <id>` "task details and audit trail" in [Beads][fw4].

**Human gates at spec and merge.** The [software-factory convergence][sf-conv] finds four independent
agentic factories placing human gates at the same two points — the spec before the build and the merge
after it — and notes that this repo's own unattended-execution discipline (agent-only phase, one owner
sitting for the gates, then activation) has the same shape. The write path above is that gate applied to
memory: agents propose, humans (or a deterministic check) decide.

## Rubric row for the composed architecture

This row is a **composition, not an observed system**: nobody has run these components together, and each
cell inherits the score of the component named. Composed 2026-09-30 from rows scored on that date.

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| yes via Beads — multi-agent store, hash IDs ([frameworks §4][fw4]); branch-and-merge via Omnigraph ([§7][fw7p]) | yes via Beads — `bd dolt push`/`pull` across machines ([§4][fw4]); object-store graph via Omnigraph ([§7][fw7p]) | yes via Beads — commit-addressed Dolt store ([§4][fw4]); LLM-facing loop replayed via OrcaReplay ([rubric][orca]) | yes via Beads — typed links, per-agent setup ([§4][fw4]); swappable graph and vector backends via Semantica ([§7][fw7p]) | yes via Beads — Dolt branch/diff/merge ([§4][fw4]); plan/apply/rollback via open-ontologies ([ontology][ont]) | yes via Beads — per-item audit trail ([§4][fw4]); PROV-O lineage via Semantica ([§7][fw7p]) |

Beads alone supplies every `yes`; the second component in each cell shows the same property delivered by
a different store type (graph, ontology) so the design does not depend on one tracker. The gate layer
(RRSI, EvoOntology, human-review) adds no score of its own — it is what keeps the LLM out of the write
path so the store's Reproducible holds. The composition does not close the cells listed next: its
`yes` scores are Beads' own, as a memory store, and no component here makes context or skills shared or
distributed.

## What stays open

`make census` confirms these gaps; each is stated with the best score the rows reach.

- **Plan 0010 outcome for the four cells plan 0009 left open** (2026-10-02):
  - *Context·Shared* and *Context·Distributed*: **filled by new evidence** at `partial`. [Redis Iris's
    Context Retriever][redis-ctx] shares business context "across all agents" and syncs it from source
    databases "within seconds". Rubric rule 6 also lifts [CLAUDE.md][ccmem] and AGENTS.md to `partial`
    on both.
  - *Skills·Shared* and *Skills·Distributed*: **filled by new evidence** at `yes`. [Organization-level
    skill provisioning][orgskills] lets owners and members share skills across a Claude organization,
    and those skills load in Claude Code.
  - *Context·Reproducible*: **confirmed open**. All six context rows are `no data`: CLAUDE.md,
    AGENTS.md, Redis Iris's Context Retriever, context-engineering-intro, the CLAUDE.md-growth paper and
    TrackPoint. Of the
    plan's leads for this cell, ReContext was dropped as a training-free inference method rather than a
    context layer.

  No cell was closed by calibration alone. Rule 6 additionally lifted CLAUDE.md, AGENTS.md and
  runtypelabs/skills to `partial`.
- **Partial ceiling (no `yes` anywhere).** Graphs·Reproducible: extraction or embedding runs an unpinned
  LLM (GraphRAG, LightRAG, Cognee, Omnigraph, Semantica, WeKnora, BrainAPI), or no pinned rebuild is
  documented (HydraDB, SSTorytime; LlamaParse pins only opt-in) ([§7][fw7p], [plan row G][plan-g]).
  Plugins·Reproducible: pinning is opt-in in [CC][ccplug] (`sha`/`sha256`) and undermined in [OpenAI's
  system][oaiplug] (placeholder integrity hashes, daily server-side rescans); [Code
  Modernization][codemod]'s proof step is deterministic but its agent steps run on an unpinned model.
  Plugins·Distributed, Context·Traceable and Long-running·Shared: `partial` at best.
- **Qualified `yes`.** Long-running·Reproducible holds only on one box ([OrcaReplay][orca]);
  Harness·Reproducible only for decision models, not loops (matrix caveat above).
- **Narrower claim still open.** Whether the [ACE-FCA phase artifacts][acefca] are git-tracked or
  diffable has no first-party source (re-checked 2026-10-02, [ccmem][ccmem]).

## Estate mapping

A repo is named here only if it is in the owner's repo list and a corpus doc already describes it; the
doc is cited. Repos without a corpus analysis are not scored. This repo is the one worked example
described from source.

| Layer | Estate repo | What it supplies | Corpus doc |
|---|---|---|---|
| Store | `ai-agents-research` (this repo) | `docs/` as the canonical store, `docs/plans/` as durable plan state, `changelog.d/` fragments as the change record — all in git; `.github/scripts/lib/doc_graph.py` builds the structural doc graph with no LLM (docs, hubs, cited domains; edges carry line numbers), the deterministic base of plan row G | [architecture.md][arch-kg], [plan][plan-g] |
| Store | `qte77` | `goals.json`, a machine-writable goal schema humans set and orchestrators read | [goal-tracking][goal-estate] |
| Store | `ralph-loop-cc-tdd-wt-vibe-kanban-template` | `prd.json` + `progress.txt` + `LEARNINGS.md` + commits — "the repo *is* the attribution ledger" | [goal-tracking][goal-estate] |
| Store | `learnings-ralphy` | Markdown learnings as git-versioned memory with a promotion path (inline → `AGENT_LEARNINGS.md` → rules → skills) | [frameworks §4][fw4] |
| Write path | `research-ralphy` | research finding → `PRD.md` → `prd.json` stories with acceptance criteria | [goal-tracking][goal-estate] |
| Write path | `learnings-ralphy` | weekly synthesize → PRD → TDD → write-back PR across the estate | [frameworks §4][fw4] |
| Share | `polyforge-orchestrator`, `office-forge-orchestrator` | parallel coding agents across a polyrepo from one workspace; the same pattern for office workflows | [enterprise OS landscape][eos] |
| Share | `liminal-flux-gh-acc` | agents plan, code, review, reflect, supervise and evolve one GitHub account (six action roles) | [enterprise OS landscape][eos] |
| Share | `cc-recursive-team-mode` | recursive Claude Code teams (the disciplines stack's teams layer) | [disciplines landscape][disc-ref] |
| Trace | `liminal-flux-gh-acc` | `state/performance-log.jsonl` with `goal_id`, `model`, tokens, `cost_usd`, `outcome` per run | [goal-tracking][goal-estate] |
| Trace | `coding-harness-eval` | deterministic evaluation of harnesses (the stack's EDD layer) | [disciplines landscape][disc-ref] |
| Trace | `ai-agents-research` | doc-graph edges with line numbers; `build.json` version, date and commit on every published page | [architecture.md][arch-kg] |
| Gates | `qte77`, `liminal-flux-gh-acc` | "agents propose, humans decide"; cost gates and a `human-required` label | [goal-tracking][goal-estate] |
| Gates | `ai-agents-research` | CI gates before merge: markdown lint and lychee; `make check_status` (frontmatter `status:` is the only status); plan rows carry a gate column | [architecture.md lint gate][arch-lint], [frontmatter conventions][arch-fm] |
| Gates | `claude-code-plugins` | the harness layer (Layer 1) of the disciplines stack | [disciplines landscape][disc-ref] |

Against the matrix, the estate's store and gate layers are git and CI — Versionable and Traceable by
construction, Reproducible where no LLM writes (the doc graph, the status check). Its open cells are the
corpus's own: shared, distributed context and skills.

## Cross-References

- [agent-substrate-rubric.md](agent-substrate-rubric.md) — the properties, subjects and evidence rules every cell follows
- [Plan 0009][plan] — arc scope, [coverage gaps][plan-gaps], [graph-system decision][plan-g]
- [goal-tracking-attribution-landscape.md § The substrate thread][goal-thread] — the same stack read from the goals end
- [software-factory-landscape.md][sf-c] — human gates at spec and merge; the fluid-software design lens
- [`docs/_topics/`][topics] — per-subject hubs indexing every scored row

## Sources

| Source | Content |
|---|---|
| [agent-substrate-rubric.md][rubric] | Properties, subjects, scoring rules |
| [Plan 0009][plan] | Coverage gaps (row C), graph-system decision (row G), row Y done-when |
| [agent-frameworks-infrastructure-landscape.md][fw1] | 22 rows: harness (§1–2), memory (§4), graphs/RAG (§7) |
| [semantic-layers-data-catalog-landscape.md][ont] | 5 ontology rows |
| [system-1-decision-models-landscape.md][laya] | 7 decision-model rows |
| [CC-memory-system-analysis.md][ccmem] | 4 context rows; ACE-FCA workflow and review gates |
| [agent-skill-evolution-research-landscape.md][skilllift] | 4 skills rows |
| [CC-community-skills-landscape.md][skl-cole] | 3 skills rows |
| [CC-community-tooling-landscape.md][hr] | human-review row |
| [CC-memory-tooling-landscape.md][memtool] | agent-memory row |
| [CC-plugin-packaging-research.md][ccplug] | CC plugin packaging row |
| [openai-apps-plugins-analysis.md][oaiplug] | OpenAI plugins row |
| [agent-plugins-standard-analysis.md][mitplug] | Mitosis Memory plugin row |
| [goose-analysis.md][aaif] | AAIF row |
| [CC-harnessrouter-analysis.md][hrouter] | HarnessRouter row |
| [nvidia-openshell-analysis.md][openshell] | OpenShell row |
| [code-review-products-landscape.md][ocr] | open-code-review row |
| [jev-analysis.md][jev] | Jev row |
| [weco-aide-recursive-self-improvement-analysis.md][rrsi] | RRSI and ROFT rows |
| [mitosis-cortex-analysis.md][cortex] | Mitosis Cortex row |
| [openresearch-analysis.md][openresearch] | OpenResearch row |
| [orcareplay-analysis.md][orca] | OrcaReplay row |
| [software-factory-landscape.md][sf-rubric] | triagebot-action row; convergence finding; design lens |
| [mex-analysis.md][mex] | Write-path example (not rubric-scored) |
| [goal-tracking-attribution-landscape.md][goal-estate] | Estate worked examples |
| [agentic-enterprise-os-landscape.md][eos] | Estate orchestrators |
| [agentic-engineering-disciplines-landscape.md][disc-ref] | Estate layer map |
| [architecture.md][arch-kg] | This repo's doc graph, monitors and lint gate |

[rubric]: agent-substrate-rubric.md
[plan]: ../plans/2026-09-27-0009-focus-shared-memory-context.md
[plan-gaps]: ../plans/2026-09-27-0009-focus-shared-memory-context.md#coverage-gaps-row-c-2026-09-30
[plan-g]: ../plans/2026-09-27-0009-focus-shared-memory-context.md#graph-system-decision-row-g
[topics]: ../_topics/README.md
[fw1]: ../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#1-multi-agent-orchestration-frameworks
[fw4]: ../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#4-agent-memory-infrastructure
[fw7]: ../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#7-rag--retrieval-infrastructure
[fw7g]: ../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#graphrag-family
[fw7p]: ../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#agent-native-graph--hybrid-rag-platforms
[ont]: ../non-cc/infrastructure/semantic-layers-data-catalog-landscape.md#agent-native-ontology-tools-2026-mcp-wave
[laya]: ../non-cc/reference/system-1-decision-models-landscape.md#laya-nandhakishorm
[kev]: ../non-cc/reference/system-1-decision-models-landscape.md#kev-jaredpalmer
[ccmem]: ../cc-native/context-memory/CC-memory-system-analysis.md#scored-on-the-agent-substrate-rubric
[redis-ctx]: ../non-cc/context-memory/redis-iris-analysis.md#context-retriever
[orgskills]: ../cc-native/agents-skills/CC-skills-adoption-analysis.md#organization-level-skill-provisioning-claude-team-and-enterprise
[codemod]: ../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md#code-modernization
[plan-0010]: ../plans/2026-10-01-0010-open-substrate-cells.md
[cei]: ../cc-native/context-memory/CC-memory-system-analysis.md#practitioner-template-context-engineering-intro
[acefca]: ../cc-native/context-memory/CC-memory-system-analysis.md#context-engineering-workflow-ace-fca
[skilllift]: ../non-cc/frameworks/agent-skill-evolution-research-landscape.md#skilllift
[skl-cole]: ../cc-community/CC-community-skills-landscape.md#coleam00-cole-medin-skills-and-excalidraw-diagram-skill
[hr]: ../cc-community/CC-community-tooling-landscape.md#human-review-petergyang
[memtool]: ../cc-community/CC-memory-tooling-landscape.md#agent-memory-tigerless-labs
[ccplug]: ../cc-native/plugins-ecosystem/CC-plugin-packaging-research.md#5-version-pinning-for-reproducible-installs
[oaiplug]: ../non-cc/protocols/openai-apps-plugins-analysis.md#rubric
[mitplug]: ../non-cc/protocols/agent-plugins-standard-analysis.md#concrete-implementation-mitosis-memory-mitosis-agent-plugin
[aaif]: ../non-cc/agents/goose-analysis.md#agentic-ai-foundation-aaif-governance-and-hosted-projects
[hrouter]: ../cc-community/CC-harnessrouter-analysis.md#rubric
[openshell]: ../non-cc/infrastructure/nvidia-openshell-analysis.md#rubric
[ocr]: ../non-cc/infrastructure/code-review-products-landscape.md#hybrid-deterministic--llm-review
[jev]: ../non-cc/infrastructure/jev-analysis.md#rubric
[rrsi]: ../non-cc/reference/weco-aide-recursive-self-improvement-analysis.md#rrsi-regularized-recursive-self-improvement-of-agent-harnesses-added-2026-09-30
[cortex]: ../non-cc/context-memory/mitosis-cortex-analysis.md#rubric
[openresearch]: ../non-cc/agents/openresearch-analysis.md#rubric
[orca]: ../non-cc/reference/orcareplay-analysis.md#rubric
[sf-rubric]: software-factory-landscape.md#rubric
[sf-conv]: software-factory-landscape.md#the-convergence--and-why-it-matters
[sf-c]: software-factory-landscape.md#c-agentic-software-factory--the-focus
[mex]: ../non-cc/context-memory/mex-analysis.md#key-differentiator-human-approval-boundary
[goal-estate]: goal-tracking-attribution-landscape.md#estate-worked-examples
[goal-thread]: goal-tracking-attribution-landscape.md#the-substrate-thread
[eos]: ../non-cc/frameworks/agentic-enterprise-os-landscape.md#tier-3--estate-worked-examples-the-self-operating-pattern-built-from-primitives
[disc-ref]: agentic-engineering-disciplines-landscape.md#reference-implementation-open-agentic-coding-harness
[arch-kg]: ../architecture.md#knowledge-graph-graphify
[arch-lint]: ../architecture.md#lint-gate
[arch-fm]: ../architecture.md#frontmatter-conventions
