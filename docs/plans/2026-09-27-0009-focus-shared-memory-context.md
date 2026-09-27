---
title: Focus arc — shared, versionable, traceable memory, context, skills and harness
status: draft
issue: 509, 504
created: 2026-09-27
updated: 2026-09-27
---

**Status**: Reference (plan)

Tracking issue: [#509](https://github.com/qte77/ai-agents-research/issues/509). This arc refocuses the corpus on
**shared, distributed, reproducible, adaptable, versionable and traceable** memory, ontology,
graphs/RAG/hybrid, context, skills, plugins, harness, and long-running hands-off offloaded tasks.

## Current status

- **Shipped:** nothing yet. This plan and #509 were opened 2026-09-27. The previous arc
  ([plan 0008](2026-09-23-0008-backlog-triage-prs-issues.md)) left one open row, the graph rebuild (#504);
  it is folded into row G below.
- **Next, in order (START HERE):** rows R → C → B, then the S rows one subject at a time, then Y, G, Z.
- **The loop, per row:** new branch `<type>/<slug>` → write → `make check_docs check_status` (+ `test` if
  code) → lychee (offline for relative links, online for new URLs) → PR → gated admin squash
  (`/workspaces/temp/ai-agents-research-triage/merge_gated.py <PR>`) → strike the row in the same PR.
- **Owner gates:** the graph-system decision (row G) has a default, below. Nothing else is gated.
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
| R | Rubric doc (6 properties × 8 subjects, evidence rules), placed in `sdlc-lcm/` | agent | Merged; linked from `docs/_topics/README.md` |
| C | Coverage map: score the existing docs in the source map against the rubric; add hubs for context, skills, plugins, harness and long-running tasks | agent | Gap list in this plan; 5 new hubs merged, anchors verified |
| B | Re-rank the backlog (screenshot topics + rxiv index) against the 8 subjects | agent | Ranked list in this plan; off-focus items marked dropped with a reason |
| S1 | Research batch: memory (incl. Mitosis Labs, benchmark anchors) | agent | One PR, first-party verified, rubric-scored |
| S2 | Research batch: ontology | agent | Same as S1 |
| S3 | Research batch: graphs/RAG/hybrid (incl. GraphRAG, LightRAG, Cognee for row G) | agent | Same as S1 |
| S4 | Research batch: context | agent | Same as S1 |
| S5 | Research batch: skills + plugins | agent | Same as S1 |
| S6 | Research batch: harness + long-running hands-off offloaded tasks | agent | Same as S1 |
| Y | Synthesis: reference architecture for a shared, versioned, traceable memory/context layer, mapped to estate repos | agent | Merged in `sdlc-lcm/`; cites the S-row docs, adds no new facts |
| G | Graph system: default C (deterministic graph module + optional graphify overlay); closes #504 | owner decision → agent | Module + tests merged; `ui/graph.html` rebuilt in CI; #504 closed |
| Z | Close-out: README/UserStory focus statements, CHANGELOG, release | agent | Release published; #509 closed |
