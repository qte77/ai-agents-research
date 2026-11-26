---
title: Redis Iris Analysis
source: https://redis.io/docs/latest/develop/ai/context-engine/
purpose: Analysis of Redis Iris, Redis's AI context-engine suite (Agent Memory and Context Retriever services), scored against the agent-substrate rubric as a lead for the Shared and Distributed cells.
created: 2026-10-02
updated: 2026-11-26
validated_links_on: 2026-10-02
status: assess
---

## What It Is

Redis Iris is "a suite of managed and self-managed services that give your customers accurate, consistent experiences with your AI agents by providing memories, approved answers, governed access to business data, and turn-by-turn tracing" ([Redis Iris context-engine docs][redis-iris-docs], checked 2026-11-26; deployment options are documented per service, with Python and JavaScript SDKs and REST APIs). The landing page now lists seven services: **Agent Memory**, **Agent Playbooks** (approved answers returned by semantic match, no model call), **Context Gateway** (one MCP endpoint for MCP-server tools and Context Surfaces generated from a data model; it replaces the earlier **Context Retriever**, whose docs URL now returns 404), **Intent Router**, **Lens** (beta, per-turn tracing), **Agent Mesh** (beta, resumable response streams) and **Data Integration**. **LangCache** (semantic response caching) is no longer listed on the landing page; the earlier analysis did not score it, as it is neither a memory nor a context-retrieval mechanism. Data Integration (Redis Data
Integration / RDI, a change-data-capture pipeline syncing relational sources into Redis in near real time).

**Context or memory — split, per plan 0010's instruction.** Agent Memory (session + long-term recall) is
this corpus's **memory** taxonomy; it is scored below for completeness but does not bear on the open
cells. **Context Retriever** — "turns your business data into structured tools that AI agents can safely
and reliably use" at runtime — matches this corpus's **context** subject ("what enters the context window...
retrieval-for-context"), the same bucket as [opensrc][opensrc] (fetches dependency source into agent
context). It is scored separately below and is the component relevant to plan 0010's L1 lead.

## Agent Memory

A two-tier store: **session memory** (current conversation state, TTL-based expiration) and **long-term
memory** (facts/preferences extracted from past sessions, text + vector embeddings), available via Python
and JavaScript SDKs and a REST API. Promotion from session to long-term memory is automatic and
asynchronous ([Agent Memory docs][redis-iris-docs]). The underlying open-source implementation is
[`redis/agent-memory-server`][agent-memory-server] — **Apache License 2.0** (Redis, Inc., 2025; verified
by reading the LICENSE file directly, not just the GitHub license badge, which mis-detects this file as
"Other/NOASSERTION" because the license text is prefixed with a non-standard copyright line), 326★/66
forks, pushed 2026-11-17 (`gh api`, checked 2026-11-26). Its README now states the Agent Memory Server is deprecated and not the supported production path: the supported product is Redis Agent Memory in Redis Iris, and the `V0/` folder holding the original server is marked "Deprecated. Preserved for study."

### Rubric (Agent Memory — Memory subject)

Scored 2026-10-02, evidence from the docs/README unless noted.

`subject: memory`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no data [docs][redis-iris-docs] (per-agent session/long-term stores; no multi-agent concurrent-read/write semantics documented) | no data [docs][redis-iris-docs] (deployable on Redis Cloud or self-managed, but no cross-machine sync/clustering is documented specifically for Agent Memory) | no data [docs][redis-iris-docs] (long-term memory extraction is described but no pinned model/version is named) | partial [docs][redis-iris-docs] (two-tier model with configurable TTL and a documented direct-write API for bulk import, but no plugin/schema-extension point beyond that) | no data [docs][redis-iris-docs] (no snapshot/diff/rollback of memory state documented) | no data [docs][redis-iris-docs] (no citation or audit-trail mechanism documented for what a recalled memory is based on) |

## Context Retriever

"Context Retriever turns your raw business data into structured tools that agents can reliably act on...
You define your data model once, specifying the entities that matter... and the fields agents need.
Context Retriever automatically generates the tools agents use to query and work with that data. Agents
never access your database directly" ([Redis Iris docs][redis-iris-docs], quoted verbatim from the 2026-10-02 version; that Context Retriever page is now renamed Context Gateway / Context Surface and its old URL returns 404). Agents authenticate with an agent key; the current Context Gateway concepts page says access is granted at the Gateway level and an agent can call every tool the Gateway exposes, including tools that modify data (read-only and destructive annotations describe behavior but do not restrict access). The earlier "access tags automatically filter" wording was not found on the current pages (unverified). Freshness is supplied by the sibling Data Integration (RDI) service, which
streams live changes from relational databases into Redis "within seconds" (landing page, checked 2026-11-26); the earlier source-database list (Oracle, MySQL, PostgreSQL, SQL Server, MariaDB, AWS Aurora) is unverified.

### Rubric (Context Retriever — Context subject)

Scored 2026-10-02, evidence from [Redis Iris docs][redis-iris-docs] unless noted.

`subject: context`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| **partial** [docs][redis-iris-docs] ("Business context is captured once and shared across all agents" — but the current Gateway docs say any agent with Gateway access can call every tool including data-modifying ones, so the earlier "read-only per generated tool, access-tag filtering" rationale is unverified and this cell should be re-scored against Context Gateway; matches the rubric's own "shared read-only" `partial` example) | **partial** [docs][redis-iris-docs] (Data Integration/RDI documents a real-time change-data-capture sync "across machines or services" — source relational databases to Redis Cloud, "within seconds" — which is the specific sync protocol the rubric's `yes` bar names as typical evidence; scored `partial` rather than `yes` because this is a one-directional freshness pipeline into the store, not documented clustering/scaling of the Context Retriever service itself) | no data [docs][redis-iris-docs] (tool generation is schema-driven, which reads as deterministic, but the docs never state this explicitly or document pinning/versioning of the generation step) | yes [docs][redis-iris-docs] ("Tools are generated from your data model, not hand-coded per agent"; "Define once, reuse everywhere") | no data [docs][redis-iris-docs] (no snapshot/diff/rollback of the data model documented) | no data [docs][redis-iris-docs] (access-tag filtering is governance, not output citation or an audit trail linking a tool call back to its data) |

**This is the first row in the corpus to score `partial` on context·Distributed and context·Shared** — both
previously fully open per [the reference architecture's "What stays open"][open-cells] (no row reached
`partial`). Flagged here for [plan 0010 row Y2][plan] to fold into that page; this document does not edit
the reference architecture itself.

## Sources

| Source | Content |
|---|---|
| [Redis Iris context-engine docs][redis-iris-docs] | Service descriptions, architecture, Context Retriever/Agent Memory/Data Integration quotes (fetched 2026-10-02) |
| [`redis/agent-memory-server`][agent-memory-server] | OSS Agent Memory implementation, LICENSE file (read directly), repo metadata (`gh api`, 2026-10-02) |
| [Plan 0010, row L1][plan] | Lead source and open-cell framing |
| [agent-substrate-reference-architecture.md § What stays open][open-cells] | Prior state of the context·Shared/Distributed cells this row bears on |

[redis-iris-docs]: https://redis.io/docs/latest/develop/ai/context-engine/
[agent-memory-server]: https://github.com/redis/agent-memory-server
[opensrc]: opensrc-analysis.md
[open-cells]: ../../sdlc-lcm/agent-substrate-reference-architecture.md#what-stays-open
[plan]: ../../plans/2026-10-01-0010-open-substrate-cells.md
