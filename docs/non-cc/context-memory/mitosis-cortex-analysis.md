---
title: Mitosis Cortex Analysis
source: https://mitosislabs.ai/developers
purpose: Analysis of Cortex, Mitosis Labs' hosted knowledge-graph memory system for AI agents, scored against the plan-0009 agent-substrate rubric.
created: 2026-09-30
updated: 2026-09-30
validated_links: 2026-09-30
---

**Status**: Assess

## What It Is

Cortex is a hosted memory product from **Mitosis Labs** (GitHub org [`OperatingSystem-1`][org], self-described as
"Autonomous AI agents that persist, reproduce, and evolve" — org profile, 2026-09-30). Per its own developer docs,
Cortex builds "one graph per team, built once at ingest" from connected sources — Google Workspace, WhatsApp,
GitHub, Notion, Obsidian — and exposes it through four surfaces: an MCP server, a REST API, a TypeScript SDK, and a
CLI ([Mitosis developer docs][mitosis-docs], fetched 2026-09-30). Cortex itself is a **closed, hosted service**: the
docs give no license, no self-hosting path, and no public source repository for the memory engine. The
`OperatingSystem-1` org does publish MIT-licensed **client-side** integrations that connect an agent to a user's
Cortex — `mitosis-agent-plugin` (MCP server + seven memory skills) and `mitosis-memory-skills` — analyzed for the
skills/plugins subject (S5), not here; `openclaw-operator` and `mcp-git-coord` go to the harness subject (S6).

## Architecture

Quoting the developer docs directly (fetched 2026-09-30, not paraphrased):

- **Ingest-time extraction, no LLM at query time**: "Embedding and extraction are paid once per item, no matter how
  many agents read it later. There is no LLM at query time. A query runs vector kNN, full-text and a one-hop graph
  expansion, fused with reciprocal rank fusion. You get evidence; your agent does the reasoning."
- **Typed, cited graph**: "Knowledge graph memory: one graph per team, built once at ingest", "Cited answers: every
  result carries the source it came from", "Typed entities: normalization collapses different spellings into one
  node."
- **Per-team isolation**: "Isolation per team: each memory has its own namespace and database" / "Each office is
  its own namespace, database and pods. Data does not flow between cortexes."
- **Evolving schema**: a "derivation ladder," "re-enrichment on rule change," and a "consolidation cycle" are named
  as the mechanism for re-deriving graph structure when extraction rules change, without a full re-ingest.
- **Answer-quality signal**: "source-gap signals that tell you when the answer is missing rather than merely poor."

## Accuracy Claims — Unverified, and the Benchmark Site Has Moved

Plan 0009's lead cited a third-party "Agentic Memory Index" at `x402oracle.com` showing Mitosis Cortex at 91.7%
accuracy and 0.0% fabricated (as of 2026-09-29). As of 2026-09-30, `x402oracle.com` **301-redirects** to
`verginglabs.com`, a site that self-describes as an "independent" benchmark lab: "Compare independent test results
to see where each memory system works well and where it fails... No provider pays for placement, ordering, or
scores" ([Verging Labs][verginglabs], fetched 2026-09-30). That self-description is the site's own marketing copy,
not verified evidence of independence — no team, affiliation, or "about" page was found to corroborate it.

The live page currently shows **Mitosis Cortex ranked 6th** with an Agentic Memory Index of **92.0 (86.6–95.4 CI)**
and a **0.0% fabrication rate** in its failure-mode breakdown (`data-v-fabrication="0.00"`), at a stated cost of
$270.05 per 1,000 questions ([Verging Labs][verginglabs], fetched 2026-09-30). The 0.0% fabrication figure matches
the plan's lead; the 92.0 overall index is close to, but not identical to, the plan's cited 91.7% — plausibly
day-to-day drift on a re-run benchmark, but this cannot be confirmed because the original `x402oracle.com` page is
no longer reachable at that URL. **Neither figure appears anywhere on Mitosis's own site.** This is a different
benchmark from [LongMemEval and LoCoMo][cc-mem-benchmarks] (the corpus's other memory-accuracy anchors) and is not
comparable to vendor self-reports scored against those datasets.

## Rubric

Scored 2026-09-30, evidence from the developer docs unless noted.

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| yes [docs][mitosis-docs] | partial [docs][mitosis-docs] | no [docs][mitosis-docs] | partial [docs][mitosis-docs] | no data | yes [docs][mitosis-docs] |

- **Shared — yes**: one graph per team, read by multiple agents/surfaces (MCP, REST, SDK, CLI) without repeat
  ingest cost ("paid once per item, no matter how many agents read it later").
- **Distributed — partial**: hosted, multi-tenant infrastructure ("its own namespace, database and pods" per
  office), but the docs don't state whether a single tenant's Cortex runs or syncs across multiple machines, only
  that tenants are isolated from each other.
- **Reproducible — no**: ingest relies on LLM-driven embedding/extraction with no pinned model or version stated;
  per the rubric's own trap ("LLM extraction with no fixed model/version is `no`"), and there's no self-hosted
  rebuild path since the engine is closed.
- **Adaptable — partial**: "re-enrichment on rule change" and a "derivation ladder" imply the extraction schema can
  change without a full rewrite, but no plugin/extension mechanism or schema-versioning detail is documented.
- **Versionable — no data**: no mention of snapshots, diffs, rollback, or git-backed state in the docs reviewed.
- **Traceable — yes**: "every result carries the source it came from," plus explicit source-gap signaling when
  evidence is missing.

## Sources

| Source | Content |
|---|---|
| [OperatingSystem-1 org profile][org] | Org name, description, blog URL (via `gh api`, 2026-09-30) |
| [Mitosis developer docs][mitosis-docs] | Architecture, ingest/query model, isolation model, adaptability mechanism (fetched via polyfetch `--show-body`, 2026-09-30) |
| [Mitosis Labs homepage][mitosis-home] | Product framing (data sources connected, "living knowledge graph") |
| [Verging Labs][verginglabs] | Third-party "Agentic Memory Index" benchmark listing Mitosis Cortex (fetched via polyfetch `--show-body`, 2026-09-30) |
| [CC-memory-tooling-landscape.md § Benchmarks][cc-mem-benchmarks] | LongMemEval/LoCoMo comparison anchors (not the same benchmark as Verging Labs) |
| [Plan 0009][plan] | Original lead, 91.7%/0.0% claim, x402oracle.com URL (2026-09-29) |

[org]: https://github.com/OperatingSystem-1
[mitosis-docs]: https://mitosislabs.ai/developers
[mitosis-home]: https://mitosislabs.ai/
[verginglabs]: https://verginglabs.com/
[cc-mem-benchmarks]: ../../cc-community/CC-memory-tooling-landscape.md#benchmarks
[plan]: ../../plans/2026-09-27-0009-focus-shared-memory-context.md
