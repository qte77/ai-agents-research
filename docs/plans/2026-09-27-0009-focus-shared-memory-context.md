---
title: Focus arc — shared, versionable, traceable memory, context, skills and harness
status: draft
issue: 509, 504, 515, 516, 517, 527
created: 2026-09-27
updated: 2026-09-29
---

**Status**: Reference (plan)

Tracking issue: [#509](https://github.com/qte77/ai-agents-research/issues/509). This arc refocuses the corpus on
**shared, distributed, reproducible, adaptable, versionable and traceable** memory, ontology,
graphs/RAG/hybrid, context, skills, plugins, harness, and long-running hands-off offloaded tasks.

## Current status

- **Shipped:** this plan and #509 (opened 2026-09-27). The previous arc
  ([plan 0008](2026-09-23-0008-backlog-triage-prs-issues.md)) left one open row, the graph rebuild (#504);
  it is folded into row G below.
  - Row I (2026-09-28): the second screenshot batch is ingested (see Source map). Leads only; nothing
    is committed yet.
  - Jev: another session filed #515–#517. My duplicates #518–#520 are closed.
  - Row R (#526) and row B (this PR) shipped. #527 tracks the paper-eval and issue-triage workflows,
    dead since GitHub Models was retired on 2026-07-30.
- **Next, in order (START HERE, 2026-09-29):** R and B are done.
  1. **Row C:** score the existing docs against the [rubric](../sdlc-lcm/agent-substrate-rubric.md) and add
     4 hubs (skills, plugins, harness, long-running) plus context.
  2. **S1 → S6:** one subject per PR, working from the P1 table in "Ranked backlog". Research each lead
     first-party; delegate the fetching to subagents (at most about 3 large landscapes per brief, results
     written to disk). J1–J3 go with S6/S3.
  3. **Then:** Y, G, Z.

  S1 can start in parallel with C; it only needs the rubric.
- **Side track (not a plan row):** #527. The paper-eval and issue-triage workflows have been dead since
  GitHub Models was retired on 2026-07-30.
  - The owner chose OpenAI-compatible providers (OpenRouter, Cerebras, Cloudflare Workers AI), Anthropic
    native, and a Jev classifier backend. The specs are posted on qte77/gha-rxiv-paper-eval#81 and
    qte77/gha-issue-triage#110.
  - The fix happens in those repos, in their own sessions.
  - Owner gate: add the chosen provider secret here, then bump the pins.
  - Meanwhile no new rxiv papers arrive, which does not block the S rows.
- **The loop, per row:** new branch `<type>/<slug>` → write → `make check_docs check_status` (+ `test` if
  code) → lychee (offline for relative links, online for new URLs) → PR → gated admin squash
  (`/workspaces/temp/ai-agents-research-triage/merge_gated.py <PR>`) → strike the row in the same PR.
- **Owner gates:**
  - The graph-system decision (row G) has a default, below.
  - The provider secret for #527 (off-plan).

  Nothing else is gated.
- **Commands:** prefix `gh`/`git` network calls with `env -u GH_TOKEN -u GITHUB_TOKEN`. When WebFetch
  paraphrases or fails, use polyfetch: `uv run --directory /workspaces/qte77/polyfetch-scrape polyfetch fetch --show-body <url>`.
- **Watch-outs:**
  - First-party only. Mark vendor benchmark numbers as self-reported.
  - Read the license from the LICENSE file and counts from the live README.
  - Never commit owner screenshots; they are leads only and stay in `/workspaces/temp/`.
  - Subagent sweeps are advisory: confirm "no coverage" with `git grep` before creating a doc.
  - Subagents: at most about 3 large landscapes per brief; write results to disk, don't echo them.

## Scope: the rubric (row R builds it)

Six properties × eight subjects. Each cell is scored `yes` / `partial` / `no` with a first-party evidence link.

| Property | Evidence that counts |
|---|---|
| Shared | Several agents, users or sessions read and write the same store |
| Distributed | Runs or syncs across machines or services, not only one local process |
| Reproducible | The same inputs rebuild the same state (pinned models or versions, deterministic pipelines) |
| Adaptable | Schema, ontology or behavior changes without a rewrite (config, plugins, schema evolution) |
| Versionable | State lives in git or supports snapshots, diffs and rollback |
| Traceable | Outputs cite their sources; audit trail or lineage for every write |

Subjects: memory · ontology · graphs/RAG/hybrid · context · skills · plugins · harness · long-running
hands-off offloaded tasks.

## Source map (existing coverage to start from)

- Hubs: [`docs/_topics/`](../_topics/README.md) (memory, knowledge-graphs, rag, code-tooling, visualization).
- Memory and context: `cc-native/context-memory/CC-memory-system-analysis.md`,
  `cc-community/CC-memory-tooling-landscape.md`, `non-cc/context-memory/` (mex, OpenViking, HelixDB,
  LatticeDB, CocoIndex, on-device semantic search), `non-cc/frameworks/agent-frameworks-infrastructure-landscape.md`
  §4 (memory) and §7 (RAG).
- Ontology: `non-cc/infrastructure/semantic-layers-data-catalog-landscape.md` § Formal Ontologies,
  `non-cc/knowledge-management/open-knowledge-format-analysis.md`, `non-cc/agents/databricks-genie-analysis.md`.
- Skills and plugins: `cc-native/agents-skills/CC-skills-adoption-analysis.md`,
  `cc-community/CC-community-skills-landscape.md`, `cc-community/CC-community-plugins-landscape.md`,
  `cc-native/plugins-ecosystem/`.
- Harness and long-running tasks: `cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md`,
  `CC-dynamic-workflows-analysis.md`, `CC-ralph-enhancement-research.md`, `cc-native/ci-remote/`
  (cloud sessions, scheduled tasks), `cc-native/sessions/CC-session-keepalive-analysis.md`, and the
  owner's unattended-execution rule (`/workspaces/.claude/rules/unattended-execution.md`).
- Backlog leads: `/workspaces/temp/ai-agents-research-triage/placement/merged.json` (682 topics; the
  medium- and low-priority ones not yet researched) and `docs/research/rxiv-agentic-papers.md`.
- First queued lead: **Mitosis Labs** (`mitosislabs.ai`, GitHub `OperatingSystem-1`). It offers the
  Cortex memory system and, per its site, fuses vector, full-text and knowledge-graph search. Its org has
  `mitosis-agent-plugin` (MIT, MCP server + 7 memory skills), `mitosis-memory-skills` and `mcp-git-coord`.
  Its accuracy claims (91.7%, 0.0% fabricated) and the "Agentic Memory Index" (hosted on `x402oracle.com`)
  are self-reported and unverified. Benchmark anchors: LongMemEval (arXiv 2410.10813), LoCoMo (arXiv 2402.17753).

### Screenshot batch 2 (row I, 2026-09-28)

- **Input:** 87 new screenshots, 2026-09-21 to 2026-09-28, in `/workspaces/temp/screenshots/`.
- **Method:** 5 extraction agents (about 3 min each) tagged scope and focus subjects and pulled URLs.
- **Results:** `/workspaces/temp/ai-agents-research-triage/batch2/out-*.tsv`, deduped into
  `batch2/merged.json`, each lead flagged `in_old_triage` / `in_corpus`.
- **Scope:** 61 Y, 14 M, 12 N.
- **Leads by subject.** Unmarked leads have no corpus hit by name. "partial" = mentioned once, no own
  entry. All are unverified until researched first-party.
  - **Memory:** aru-labs/lossless-memory, tigerless-labs/agent-memory, JITMEM (Salesforce paper),
    volotat/mini-AGI, WeKnora, Mitosis Labs (queued above).
  - **Ontology:** aws/context-ontology-accelerator (already in the batch-1 triage); an unnamed
    "semantic model / enterprise context layer" post.
  - **Graphs/RAG:** run-llama/liteparse, WeKnora, RuVector (partial), BrainAPI (BSL-1.1).
  - **Skills and plugins:**
    - Skills: SkillLift (paper + repo), NVlabs/Skill2Env, microsoft/SkillOpt (partial), a "coding agents
      are strong prompt optimizers" paper.
    - Plugins: Xpert plugins.
  - **Harness:**
    - Repos and tools: trycua/cua, NVIDIA/OpenShell, BitMiracle-AI/Dormice (E2B), tigerless-labs/autoharness
      (partial), yetone/magpie, vllm-project/semantic-router (partial), google/ax (Agent Substrate),
      Contrastive-LM/CLM.
    - Papers and courses: ModularRSI and RRSI (self-improving harness papers), "Learn Harness Engineering".
    - Jev ecosystem (abide, laya, Jev-as-a-Judge, UFA): see #515–#517.
  - **Long-running:** RIVER (Salesforce/CMU, terminal agents), PrimeScientist, Self-Organizing Agent Teams,
    EvolveTrade, an agent-server comparison paper (arXiv 2609.21081: Agno AgentOS, LangGraph Agent
    Server), Kitaru/Opik on Modal.
  - **Already covered:** Raven/EverOS (`raven-analysis.md`), Shepherd (`shepherd-analysis.md`),
    CopilotKit/AG-UI, E2B, Modal. These only need a refresh if a lead adds a new fact.

### Screenshot batch 3 (row I2, 2026-09-29)

- **Input:** 20 new screenshots, 2026-09-28 18:22 to 2026-09-29 18:27.
- **Method:** 2 extraction agents. Results in `batch3/out-*.tsv`, deduped into `batch3/merged.json`.
- **Scope:** 10 Y, 6 M, 4 N.
- **New leads.** Repo existence and license are from GitHub metadata, 2026-09-29; everything else is
  unverified.
  - **Harness:**
    - google-research/rrsi (Apache-2.0): upgrades batch 2's RRSI paper lead with a repo.
    - Orchestrator.inc ("AO", agent IDE / meta harness).
    - A Critical-State RL paper (Salesforce, arXiv 2609.24985).
  - **Plugins/MCP:** the Hex-Rays IDA MCP server (IDA Nexus, Code Mode); jtaoufik/tiger (MIT,
    git-native API client with an MCP server).
  - **Context/code search:** dzhng/jevgrep (MIT; added to #517); Sonar Vortex.
  - **Repeats from batch 2:** OpenMuse / CopilotKit.
  - **Off-focus (M):** Pydantic AI realtime, Netflix GenRec, Anthropic for Startups posts.

### Owner-requested leads (2026-09-29, for the next research run)

Licenses and descriptions come from GitHub repo metadata (2026-09-29); confirm each license against its
LICENSE file during research.

| Lead | Row | Existing coverage | What to research |
|---|---|---|---|
| `x.com/typesafeai` (not linked: X returns 403 to lychee) | J1 (#515) | none | Jev use cases; X blocks bots, so use polyfetch. Treat every use case there as an **external, unconfirmed** claim, not as TypeSafe's own. Cite it as confirmed only if docs.typesafe.ai states it; otherwise label it unconfirmed or drop it (owner rule, 2026-09-29) |
| [aaif.io](https://aaif.io/) | S5 | only as Goose's foundation (`non-cc/agents/goose-analysis.md`) | The Agentic AI Foundation itself: governance, hosted projects, relevance to skills/plugins standards |
| [github.com/OperatingSystem-1](https://github.com/OperatingSystem-1) | S1, S5, S6 | none (Mitosis Labs, queued above) | S1: Cortex memory. S5: `mitosis-agent-plugin`, `mitosis-memory-skills`. S6: `openclaw-operator`, `mcp-git-coord` |
| [github.com/coleam00](https://github.com/coleam00) (Cole Medin) | S4, S5, S6 | none | S6: `Archon` ("open-source harness builder for AI coding", MIT). S4: `context-engineering-intro` (MIT). S5: `excalidraw-diagram-skill` (no license on GitHub) |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | J1, S6 | none | Hybrid deterministic + LLM code review (Apache-2.0). Goes with the "no review agent" gap (#515) and `code-review-products-landscape.md` |
| [github.com/tysoncung](https://github.com/tysoncung) | S5 (low) | none | Personal account; `notion-agent-hub` (MIT) and `awesome-vibe-coding` (CC0) are the only agent-related repos. Low priority unless the owner names a specific repo |
| [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | S5 | none | Coding-agent skill for multi-phase security audits with "independently verified, machine-readable findings" (MIT); scores high on traceable |
| [HarnessRouter/harnessrouter](https://github.com/HarnessRouter/harnessrouter) | S6 (refresh) | `cc-community/CC-harnessrouter-analysis.md` (updated 2026-09-24) | Refresh stars and release only; score on the rubric |
| [jaredpalmer/kev](https://github.com/jaredpalmer/kev) | J3 (#517) | none | "Jev-like family of decision models" on Qwen, self-trainable (Apache-2.0); open-weights alternative to Jev next to Laya |
| probably, laya, jev-ultrafast | J3 (#517) | none | Already in #517; owner re-confirmed 2026-09-29 |
| [driceroland/Search](https://github.com/driceroland/Search) | S6 (check relevance) | none | Described as "a small, fast WebKit browser for macOS" (MIT); no agent angle in the description. Include only if its README shows agent use |
| [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | S6 | none | "The open-source app everyone uses to manage agents at work" (MIT); agent management and long-running orchestration |
| [alphasignal.ai](https://alphasignal.ai/) and its article [What belongs in AGENTS.md, design docs and tests](https://alphasignal.ai/news/what-belongs-in-agents-md-design-docs-and-tests) | S4 | none | AlphaSignal is a news digest, so use it as a lead source, not as a citation. The article (Akruti Acharya, 2026-09-29) summarizes arXiv 2608.11095 ("Why Does CLAUDE.md Keep Growing?"). Cite the paper; the article's own framing ("instruction file as a best-effort cache") is secondary. Target: `cc-native/context-memory/CC-repo-guidance-probe-refine-analysis.md` or `CC-memory-system-analysis.md` |
| [Sumanth077/Hands-On-AI-Engineering `ai_agents/`](https://github.com/Sumanth077/Hands-On-AI-Engineering/tree/main/ai_agents) | S1, S3, S6 | none (seen twice in batch-2/3 screenshots) | Example collection, not a product: 45 agent projects; no license on GitHub, so cite as examples only. Focus-relevant: `research_assistant_with_memory` (S1), `agentic_rag_system` (S3), `self_evolving_code_review_agent` and `multi_agent_coding_assistant` (S6). Score only these on the rubric; mention them in the matching landscapes, no new page |
| [github.com/runtypelabs](https://github.com/runtypelabs) | S5, S6 | Runtype bullet in `agent-frameworks-infrastructure-landscape.md` | S5: `skills` (official agent skills). S6: `hermes-runtype-otel` (OTel export of agent turns), `persona`. Extend the existing entry; no new page |

### Ranked backlog (row B, 2026-09-29)

- **Method:** a subagent merged 280 open batch-1 topics, 75 batch-2 leads, 16 batch-3 leads and the
  owner-requested leads. It deduplicated them by entity and ranked them against the 8 subjects. It
  fetched nothing from the web; coverage is a `git grep` check only.
- **Result:** 320 leads — 42 P1, 66 P2, 39 P3, 173 DROP (58 already covered with nothing new, the rest
  off-focus).
- **Full list** (P2/P3/DROP with reasons): `/workspaces/temp/ai-agents-research-triage/rowB/ranked.tsv`
  and `summary.md`. These are local working files, not in the repo.
- **P1 checks:** every P1 GitHub repo was checked to exist on 2026-09-29. Licenses are from GitHub
  metadata. arXiv ids marked "derived" in the TSV came from a stated id, not a visible link; confirm
  them when researching.
- **Owner qualifiers kept:** tysoncung is P3 (low); driceroland/Search is P2 (only if its README shows
  agent use).

| Row | Lead | First-party URL |
|---|---|---|
| S1 | OperatingSystem-1 / Mitosis Labs: Cortex memory | <https://github.com/OperatingSystem-1> |
| S1 | AgentiCow (ruvnet; copy-on-write branching for agent vector memory) | <https://github.com/ruvnet/agenticow> |
| S1 | Beads / bd (gastownhall; dependency-aware task graph tracker for agents, Dolt-backed per n | <https://github.com/gastownhall/beads> |
| S1 | WMT: Weighted Memory Tree (arXiv 2608.20631) | <https://arxiv.org/abs/2608.20631v1> |
| S1 | lossless-memory (aru-labs; lossless long-term memory, never summarizes) | <https://github.com/aru-labs/lossless-memory> |
| S1 | JITMEM: Just-in-Time Memory (Salesforce AI Research, arXiv 2609.27334) | <https://arxiv.org/abs/2609.27334> |
| S1 | agent-memory (tigerless-labs; long-term memory runtime for Claude Code/Codex) | <https://github.com/tigerless-labs/agent-memory> |
| S2 | Ontology Atlas (wlsdks; markdown-graph, MCP-native, local-first ontology workbench) | <https://github.com/wlsdks/ontology-atlas> |
| S2 | open-ontologies (Rust MCP server for RDF/OWL/SHACL, Oxigraph) | <https://github.com/fabio-rovai/open-ontologies> |
| S2 | EvoOntology (ruc-datalab; MCP-exposed self-evolving ontology layer, arXiv 2609.15779) | <https://github.com/ruc-datalab/EvoOntology> |
| S2 | AWS context-ontology-accelerator (governed ontology KGs via MCP/SPARQL) | <https://github.com/aws/context-ontology-accelerator> |
| S3 | SSTorytime (markburgess; Semantic Spacetime Postgres graph via MCP) | <https://github.com/markburgess/SSTorytime> |
| S3 | Omnigraph (ModernRelay; git-branching multi-agent graph DB) | <https://github.com/ModernRelay/omnigraph> |
| S3 | Semantica (graph-native accountable decision infrastructure) | <https://github.com/semantica-agi/semantica> |
| S4 | coleam00/context-engineering-intro | <https://github.com/coleam00/context-engineering-intro> |
| S5 | Agentic AI Foundation (aaif.io) + Goose donation | <https://aaif.io/> |
| S5 | OperatingSystem-1: mitosis-agent-plugin + mitosis-memory-skills | <https://github.com/OperatingSystem-1> |
| S5 | coleam00/excalidraw-diagram-skill | <https://github.com/coleam00/excalidraw-diagram-skill> |
| S5 | coleam00/skills repo + drive-screen skill | <https://github.com/coleam00/skills> |
| S5 | cloudflare/security-audit-skill | <https://github.com/cloudflare/security-audit-skill> |
| S5 | runtypelabs/skills (official agent skills) | <https://github.com/runtypelabs> |
| S5 | WikiSkill (arXiv 2608.27454; persistent wiki skill evolution) | <https://arxiv.org/abs/2608.27454> |
| S5 | AutoTailor (MSR; auto-constructs compact MCP tool set, arXiv 2609.13548) | <https://arxiv.org/abs/2609.13548> |
| S5 | SkillLift (Fudan; learned rubrics for skill self-evolution, arXiv 2609.15396) | <https://github.com/WalteR-MittY-pro/SkillLift> |
| S5 | NVlabs Skill2Env (collective agent skills to RL environments) | <https://github.com/NVlabs/Skill2Env> |
| S6 | OperatingSystem-1: openclaw-operator + mcp-git-coord | <https://github.com/OperatingSystem-1> |
| S6 | coleam00/Archon (open-source harness builder for AI coding) | <https://github.com/coleam00/Archon> |
| S6 | HarnessRouter (refresh stars + release only) | <https://github.com/HarnessRouter/harnessrouter> |
| S6 | paperclipai/paperclip (multi-agent orchestration app) | <https://github.com/paperclipai/paperclip> |
| S6 | runtypelabs: hermes-runtype-otel + persona | <https://github.com/runtypelabs> |
| S6 | Google AX / Agent Substrate (agentexecutor.io) + Celesto critique | <https://github.com/google/ax> |
| S6 | NVIDIA OpenShell (safe runtime for agent fleets) | <https://github.com/NVIDIA/OpenShell> |
| S6 | OrcaReplay (record/replay/fork debugging of coding-agent runs) | <https://github.com/Continuum-AI-Corp/OrcaReplay> |
| S6 | RRSI (Google; regularized recursive self-improvement of agent harnesses) | <https://github.com/google-research/rrsi> |
| J1 | TypeSafe / Jev (system-one classifier; pre-CI code-change gate; x.com/typesafeai use cases | <https://docs.typesafe.ai/> |
| J1 | alibaba/open-code-review (hybrid deterministic + LLM code review) | <https://github.com/alibaba/open-code-review> |
| J3 | jaredpalmer/kev (Jev-like decision models on Qwen, self-trainable) | <https://github.com/jaredpalmer/kev> |
| J3 | probably (Jev ecosystem) | <https://github.com/southpolesteve/probably> |
| J3 | laya (non-autoregressive System 1 decision engine) | <https://github.com/NandhaKishorM/laya> |
| J3 | jev-ultrafast (browser-use fast browser agent) | <https://github.com/browser-use/jev-ultrafast> |
| J3 | abide (coldteadotai; catches AGENTS.md rule violations) | <https://github.com/coldteadotai/abide> |
| J3 | jevgrep (dzhng; small decision model for code-context search) | <https://github.com/dzhng/jevgrep> |
| S4 | Paper: "Why Does CLAUDE.md Keep Growing? Catastrophic Remembering in Agentic Coding" (owner-requested 2026-09-29, via AlphaSignal) | <https://arxiv.org/abs/2608.11095> |

## Graph system decision (row G)

The current graph (`ui/graph.html`, last full rebuild #404: 785 nodes) comes from graphify. Graphify
extracts concepts using the session model, so a uniform rebuild of about 248 docs takes roughly 60–80
subagents. Its output is not deterministic. That conflicts with this arc's own "reproducible" and
"traceable" criteria.

| Option | Reproducible | Cost per rebuild | Notes |
|---|---|---|---|
| A. Keep graphify, full rebuild (#504 as written) | no (LLM extraction) | high | Concept-level graph; partial updates make it lopsided (AGENT_LEARNINGS) |
| B. Deterministic structural graph | yes | about zero, runs in CI | Nodes = docs, sections, hubs, source domains; edges = actual links (file:line), bucket, status. Stdlib module, TDD |
| C. B as the base + graphify concept overlay on demand | base yes, overlay no | low base, occasional overlay cost | Overlay kept as a separate, clearly labelled layer |
| D. Adopt an external GraphRAG system (e.g. Microsoft GraphRAG, LightRAG, Cognee) | varies | API keys or infrastructure | These are research subjects of this arc; judge them in S3 before adopting any |

**Default: C.** Build B as a tested module that regenerates on every push. Keep graphify only as an
optional concept overlay. Re-scope #504 to "build B, then overlay". Revisit D after S3 scores those
systems on the rubric.

## Remaining work

| # | Item | Gate | Done-when |
|---|---|---|---|
| ~~I~~ | ~~Ingest screenshot batch 2 (87 images)~~ | agent | Done 2026-09-28 (this PR): extracted + deduped to `batch2/merged.json`; leads listed in the Source map; feeds row B |
| ~~I2~~ | ~~Ingest screenshot batch 3 (20 images)~~ | agent | Done 2026-09-29 (this PR): `batch3/merged.json`; leads in the Source map; feeds row B; jevgrep added to #517 |
| J1 | #515: Jev (TypeSafe) analysis page: system-one classifier as a pre-CI code-change gate (feelings pilot results); fills the `agentic-sdlc-patterns.md` "no review agent" gap | agent | Page merged (status Trial), gap row repointed, #515 closed |
| J2 | #516: extend §8 Output Validation with BAML feelings (`.feels`/`.fill`) and probability-returning classifiers | agent | §8 extended, #516 closed |
| J3 | #517: Jev ecosystem scout batch (abide, jev-ultrafast, laya, probably), scored on the rubric | agent | Entries merged (extend existing pages first), #517 closed |
| ~~R~~ | ~~Rubric doc (6 properties × 8 subjects, evidence rules), placed in `sdlc-lcm/`~~ | agent | Done 2026-09-29 (this PR): `docs/sdlc-lcm/agent-substrate-rubric.md`, indexed in `sdlc-lcm/README.md` and linked from `docs/_topics/README.md` |
| C | Coverage map: score the existing docs in the source map against the rubric; add hubs for context, skills, plugins, harness and long-running tasks | agent | Gap list in this plan; 5 new hubs merged, anchors verified |
| ~~B~~ | ~~Re-rank the backlog (screenshot topics + rxiv index) against the 8 subjects~~ | agent | Done 2026-09-29 (this PR): 320 leads → 42 P1 (table in "Ranked backlog"), full list in `rowB/ranked.tsv`. The rxiv index was not re-ranked: the paper-eval workflow has produced nothing since 2026-07-28 (#527) |
| S1 | Research batch: memory (incl. Mitosis Labs / OperatingSystem-1, benchmark anchors) | agent | One PR, first-party verified, rubric-scored |
| S2 | Research batch: ontology | agent | Same as S1 |
| S3 | Research batch: graphs/RAG/hybrid (incl. GraphRAG, LightRAG, Cognee for row G) | agent | Same as S1 |
| S4 | Research batch: context | agent | Same as S1 |
| S5 | Research batch: skills + plugins (incl. AAIF, runtypelabs `skills`, Mitosis plugin/skills; see Owner-requested leads) | agent | Same as S1 |
| S6 | Research batch: harness + long-running hands-off offloaded tasks (incl. `hermes-runtype-otel`, `openclaw-operator`, `mcp-git-coord`) | agent | Same as S1 |
| Y | Synthesis: reference architecture for a shared, versioned, traceable memory/context layer, mapped to estate repos | agent | Merged in `sdlc-lcm/`; cites the S-row docs, adds no new facts |
| G | Graph system: default C (deterministic graph module + optional graphify overlay); closes #504 | owner decision → agent | Module + tests merged; `ui/graph.html` rebuilt in CI; #504 closed |
| Z | Close-out: README/UserStory focus statements, CHANGELOG, release | agent | Release published; #509 closed |
