---
title: Agent Substrate Rubric — Shared, Versionable, Traceable Memory, Context and Harness
purpose: One scoring rubric (6 properties × 8 subjects) for judging agent memory, ontology, graphs/RAG, context, skills, plugins, harness and long-running offloaded tasks.
created: 2026-09-29
updated: 2026-10-02
validated_links: 2026-09-30
status: reference
---

**Details:** method

## What It Is

The single rubric that the plan 0009 research batches ([#509][plan-issue]) score against. Landscapes and
analyses link here instead of restating the definitions. A doc adds a short **Rubric** table for the tool
it covers. It does not copy this page.

The rubric asks one question of every tool: can a team **share** it, **run** it across machines,
**rebuild** its state, **change** it without a rewrite, **version** it, and **trace** what it did?

## Properties

Each property is scored `yes` / `partial` / `no`. Every score carries one evidence link, a first-party
page (docs, LICENSE, source file, paper) or an observation with version and date. With no evidence, the
score is `no data` (not `no`).

| Property | `yes` means | Typical evidence | `partial` / common traps |
|---|---|---|---|
| **Shared** | Several agents, users or sessions read and write the same store or artifact, with defined concurrency | Docs on multi-user or multi-agent access, locking or merge semantics | `partial`: shared read-only, or sharing via manual export. A hosted SaaS alone is not "shared" if each user gets an isolated silo |
| **Distributed** | Runs, syncs or scales across machines or services, not only one local process | Deployment docs (cluster, remote server, sync protocol), replication | `partial`: remote API with a single node, or sync via a third-party drive |
| **Reproducible** | The same inputs rebuild the same state: pinned versions or models, deterministic pipelines, rebuild from source | Pinned model or version IDs, lockfiles, rebuild commands, seeds | `partial`: pinned code but unpinned model. LLM extraction with no fixed model/version is `no` |
| **Adaptable** | Schema, ontology, behavior or backends change without a rewrite | Config, plugin or extension points, schema evolution, swappable providers | `partial`: forks or code edits are needed for common changes |
| **Versionable** | State lives in git or supports snapshots, diffs and rollback | Git-backed storage, snapshot/branch/rollback APIs, migration history | `partial`: export/import only, or versioned code but unversioned state |
| **Traceable** | Outputs cite their sources; writes have an audit trail or lineage | Citations in answers, audit logs, lineage, OTel/trace export | `partial`: logs exist but don't link output to input. Self-reported accuracy is not traceability |

## Subjects

The eight subjects of the arc. The `_topics` hubs index existing coverage for each.

| Subject | Covers | Hub |
|---|---|---|
| Memory | Persistent agent memory: stores, extraction, consolidation, recall | [memory.md](../_topics/memory.md) |
| Ontology | Schemas, semantic layers, formal ontologies, knowledge formats | [knowledge-graphs.md](../_topics/knowledge-graphs.md) |
| Graphs/RAG/hybrid | Knowledge graphs, vector/full-text/graph retrieval, indexing pipelines | [knowledge-graphs.md](../_topics/knowledge-graphs.md), [rag.md](../_topics/rag.md) |
| Context | What enters the context window: repo context, compression, retrieval-for-context | [context.md](../_topics/context.md), [code-tooling.md](../_topics/code-tooling.md) |
| Skills | Packaged agent capabilities (SKILL.md and equivalents), their distribution and optimization | [skills.md](../_topics/skills.md) |
| Plugins | Extension packaging: plugins, MCP servers, marketplaces | [plugins.md](../_topics/plugins.md) |
| Harness | The loop around the model: orchestration, tools, sandboxes, self-improving harnesses | [harness.md](../_topics/harness.md) |
| Long-running | Hands-off, offloaded, multi-hour or scheduled agent work: durability, resume, remote execution | [long-running.md](../_topics/long-running.md) |

## How to score

1. Score from first-party sources only. Marketing copy counts as a claim, not evidence; a vendor's social
   posts count as external claims unless its docs state the same.
2. Put the table in the tool's own section, in this form:

   | Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
   |---|---|---|---|---|---|
   | yes [src] | partial [src] | no data | yes [src] | no [src] | partial [src] |

3. Score the tool as shipped (default or documented configuration), not as it could be extended.
4. Date the scoring (`scored YYYY-MM-DD`). Re-score on a major version change.
5. Where the subject makes a property meaningless (for example "distributed" for a research paper), write
   `n/a` with a one-line reason.
6. **Static artifacts in git** (skill repos, instruction files such as CLAUDE.md or AGENTS.md, plugin and
   ontology files) are scored on how they are governed and synced, not on runtime concurrency. A git repo
   with a documented contribution flow is `partial` on Shared (git merge is the defined concurrency) and
   `partial` on Distributed (git remotes sync across machines, comparable to the third-party-drive example
   above). `yes` needs more than git, such as a native multi-writer store. When one row mixes a git-hosted
   artifact with a runtime store (for example CLAUDE.md with machine-local auto memory), split it into two
   rows. For a vendor's instruction-file mechanism (CLAUDE.md, AGENTS.md), which lives inside the user's
   repo rather than being a repo itself, the vendor's own documentation of team sharing through source
   control is the cited flow. Decided 2026-10-02 ([plan 0010, C0 and R1][plan-0010]); the owner may override.

## Sources

| Source | Content |
|---|---|
| [Plan 0009][plan] | Arc scope, subjects and remaining-work rows that use this rubric |
| [#509][plan-issue] | Tracking issue for the arc |
| [Plan 0010][plan-0010] | Decision C0: scoring static artifacts in git (rule 6) |
| [`docs/_topics/`](../_topics/README.md) | Existing subject hubs |
| [agent-substrate-reference-architecture.md](agent-substrate-reference-architecture.md) | Synthesis of every scored row into one reference architecture (evidence matrix, composed rubric row, open cells) |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | First-party citation rules the evidence column follows |

[plan]: ../plans/2026-09-27-0009-focus-shared-memory-context.md
[plan-issue]: https://github.com/qte77/ai-agents-research/issues/509
[plan-0010]: ../plans/2026-10-01-0010-open-substrate-cells.md#decision-c0-calibrate-the-rubric-for-static-artifacts-owner-gate
