---
title: Redis Iris Analysis
source: https://redis.io/docs/latest/develop/ai/context-engine/
purpose: Analysis of Redis Iris, Redis's AI context-engine suite, split into its Agent Memory and Context Retriever services and scored against the plan-0009/0010 agent-substrate rubric — checked as a lead for the context·Shared and context·Distributed open cells (plan 0010, row L1).
created: 2026-10-02
updated: 2026-10-02
validated_links: 2026-10-02
status: assess
---

## What It Is

Redis Iris is "a suite of managed and self-managed services for agent memory, semantic caching, and
governed data access" ([Redis Iris context-engine docs][redis-iris-docs], fetched 2026-10-02). It bundles
four services, all available "fully managed on Redis Cloud... or self-managed on your own infrastructure,
via REST API": **LangCache** (semantic response caching — not scored here, it is neither a memory nor a
context-retrieval mechanism), **Agent Memory**, **Context Retriever**, and **Data Integration** (Redis Data
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
and TypeScript SDKs and a REST API. Promotion from session to long-term memory is automatic and
asynchronous ([Agent Memory docs][redis-iris-docs]). The underlying open-source implementation is
[`redis/agent-memory-server`][agent-memory-server] — **Apache License 2.0** (Redis, Inc., 2025; verified
by reading the LICENSE file directly, not just the GitHub license badge, which mis-detects this file as
"Other/NOASSERTION" because the license text is prefixed with a non-standard copyright line), 321★/63
forks, pushed 2026-09-18 (`gh api`, 2026-10-02). Its README states it "is part of Redis Iris"; a `V0/`
folder inside the repo holds "the original Redis Agent Memory Server... kept as an open research artifact,
not as the supported production distribution."

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
never access your database directly" ([Redis Iris docs][redis-iris-docs], quoted verbatim). Access is
per-agent-keyed with tag-based filtering: "Each agent requires a key, and access tags automatically filter
what data each agent can see." Freshness is supplied by the sibling Data Integration (RDI) service, which
performs an "initial sync" then "captures changes in real time," so that "updates from your primary
database appear in Redis within seconds" across source databases (Oracle, MySQL, PostgreSQL, SQL Server,
MariaDB, AWS Aurora) and the Redis store.

### Rubric (Context Retriever — Context subject)

Scored 2026-10-02, evidence from [Redis Iris docs][redis-iris-docs] unless noted.

`subject: context`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| **partial** [docs][redis-iris-docs] ("Business context is captured once and shared across all agents" — but access is read-only per generated tool, with per-agent keys and access-tag filtering rather than documented write concurrency; matches the rubric's own "shared read-only" `partial` example) | **partial** [docs][redis-iris-docs] (Data Integration/RDI documents a real-time change-data-capture sync "across machines or services" — source relational databases to Redis Cloud, "within seconds" — which is the specific sync protocol the rubric's `yes` bar names as typical evidence; scored `partial` rather than `yes` because this is a one-directional freshness pipeline into the store, not documented clustering/scaling of the Context Retriever service itself) | no data [docs][redis-iris-docs] (tool generation is schema-driven, which reads as deterministic, but the docs never state this explicitly or document pinning/versioning of the generation step) | yes [docs][redis-iris-docs] ("Tools are generated from your data model, not hand-coded per agent"; "Define once, reuse everywhere") | no data [docs][redis-iris-docs] (no snapshot/diff/rollback of the data model documented) | no data [docs][redis-iris-docs] (access-tag filtering is governance, not output citation or an audit trail linking a tool call back to its data) |

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
