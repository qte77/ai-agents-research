---
title: Context Caching Patterns — FACT and Beyond
description: Analysis of FACT (Fast Augmented Context Tools) as a caching-over-RAG pattern for deterministic, low-latency context retrieval in Claude Code workflows.
category: research
status: research
created: 2026-03-26
validated_links: 2026-03-26
---

**Status**: Research (informational)

## Summary

FACT (Fast Augmented Context Tools) introduces a retrieval pattern that replaces vector search with prompt caching + deterministic tool calls via MCP. The approach delivers 93% cost reduction over traditional RAG with sub-100ms latency. While the implementation is specific to Arcade.dev, the architectural pattern is applicable to any MCP-based CC workflow.

## FACT Architecture

### Core Mechanism

Traditional RAG: Query → Embed → Vector search → Retrieve chunks → Inject context
FACT: Query → Check cache → (hit: return cached) / (miss: Execute tool → Cache result → Return)

Three components:

1. **Prompt caching**: Leverages Claude's native caching to store and reuse responses. Static tokens cached inside the model; no external vector DB needed.
2. **Tool-based retrieval**: Structured MCP tool calls (SQL queries, API calls, custom functions) fetch exact, live data instead of probabilistic similarity matches.
3. **Intelligent routing**: Automatically decides what to cache vs. what to fetch live based on data volatility.

### Three-Tier Content Management

| Tier | Content Type | TTL | Strategy |
|------|-------------|-----|----------|
| Static | Documentation, schemas, rules | Hours/days | Long-term cache, rarely invalidate |
| Semi-dynamic | Configuration, metadata | Minutes/hours | Medium-term cache, periodic refresh |
| Dynamic | Live data, API responses | Seconds/minutes | Short-term cache or always-fetch |

### Performance Benchmarks (Claimed, 2026-03-26)

| Metric | FACT | Target | Traditional RAG |
|--------|------|--------|----------------|
| Cache hit latency | 23ms avg | <=25ms | N/A (no cache tier) |
| Cache miss latency | 95ms avg | <=100ms | 2-5 seconds |
| Cache hit rate | 87.3% | >=80% | N/A |
| Cost per 10K queries | $50/month | — | $450/month |
| Cost reduction | 93% | >=85% | Baseline |
| Error rate | <0.1% | <=0.5% | Variable |

**Note**: These are author-claimed benchmarks (retrieved 2026-03-26), not independently verified. The cost comparison assumes a specific RAG stack (embedding + vector DB + lookup).

## FACT vs RAG

| Aspect | RAG | FACT |
|--------|-----|------|
| Retrieval | Embeddings → Vector search | Prompt cache → Tool calls |
| Data freshness | Periodic re-indexing | Live on-demand execution |
| Accuracy | Probabilistic (similarity) | Exact (SQL/API) |
| Cost model | Embedding + lookup per query | Cache hits = near-zero cost |
| Infrastructure | Vector DB + embedding pipeline | MCP tools + cache layer |
| Failure mode | Stale/wrong chunks retrieved | Tool execution failure (deterministic error) |

## Applicability to CC Workflows

### Directly Applicable Patterns

1. **Static context caching**: CLAUDE.md, AGENTS.md, architecture docs are static-tier content. CC already caches these implicitly via conversation context, but explicit tiered caching could reduce re-reading on long sessions.

2. **Tool-over-search for live data**: Instead of embedding project state and searching it, use MCP tools that query git, file systems, or APIs directly. This aligns with CC's existing tool model (Bash, Read, Grep are already deterministic tools).

3. **TTL-based invalidation**: The three-tier model (static/semi-dynamic/dynamic) maps to CC's context management:
   - Static: rules, skills (always-loaded, rarely change)
   - Semi-dynamic: project state, task lists (change per session)
   - Dynamic: git status, test results (change per minute)

### Not Directly Applicable

- **Arcade.dev dependency**: FACT's tool execution layer is hosted on Arcade.dev. The pattern is portable; the implementation is not.
- **Vector search replacement**: CC doesn't use RAG internally — it uses direct file reads and tool calls. FACT's anti-RAG argument is solved differently in CC.

## Key Insight: Deterministic Tools Beat Probabilistic Search

The core principle — *prefer exact tool execution over probabilistic similarity search* — is already the foundation of CC's architecture. CC uses `Read`, `Grep`, `Glob` (exact tools) rather than embedding-based code search. FACT validates this design choice with cost and latency data.

**Where FACT adds value**: The explicit caching tier with TTL-based invalidation is not natively present in CC. CC re-reads files on every reference. A caching layer for slow-changing context (architecture docs, dependency graphs, project rules) could reduce token consumption on long sessions.

## Cross-References

- [CC-extended-context-analysis.md](CC-extended-context-analysis.md) — context window management strategies
- [CC-memory-system-analysis.md](CC-memory-system-analysis.md) — CC's native memory system
- [CC-community-tooling-landscape.md](../../community/CC-community-tooling-landscape.md) — RTK and Pilot Shell context optimization approaches

## Sources

<!-- markdownlint-disable MD013 -->

| Source | Content |
|---|---|
| [FACT repository][fact] | Caching-over-RAG pattern, benchmarks, architecture |

<!-- markdownlint-enable MD013 -->

[fact]: https://github.com/ruvnet/FACT
