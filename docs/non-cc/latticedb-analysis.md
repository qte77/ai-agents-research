---
title: LatticeDB Analysis
source: https://github.com/jeffhajewski/latticedb
purpose: Analysis of LatticeDB, an embedded single-file graph, vector, and full-text database written in Zig.
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

[LatticeDB][repo] is an embedded, single-file property-graph database combining graph traversal, HNSW vector search, and BM25 full-text search behind one Cypher-like query language (`MATCH`/`WHERE`/`RETURN`, a vector-distance operator `<=>`, a text-match operator `@@`). It is written in Zig with no external dependencies, uses a single-writer embedded model (one owning process, WAL-backed durability), and targets local, relationship-heavy workloads such as Graph RAG and agent memory — its own README frames these as example workloads built on the graph/vector/text substrate, not the definition of the engine.

Stars: 685 · License: MIT · Language: Zig · Latest release: **v0.15.0** (2026-08-29, via GitHub Releases) · 4 contributors · homepage [latticedb.org][site] (all accessed 2026-09-24). Bindings: CLI, Python (`pip install latticedb`), TypeScript/Node (`npm install @hajewski/latticedb`), Go (cgo), Java (JDK 21+, JNI). Note: the in-repo release-notes index still lists 0.11.1 as its newest entry as of 2026-09-24 — docs lag the tagged releases by several versions.

## Performance (Self-Reported)

Benchmarked by the project on Apple M1, single-threaded, reproducible via `zig build benchmark`/`vector-benchmark`/`graph-benchmark`:

- Node lookup: 0.13 μs (7.9M ops/sec).
- 10-NN vector search at 1M vectors (128-dim, HNSW): 0.83 ms mean latency, 100% recall@10.
- Depth-limited graph traversal (10K nodes/50K edges, depth 50): 500 μs vs. SQLite's 1.4 s recursive CTE — a **2,819x** speedup on this specific same-machine, same-harness comparison.

Cross-vendor comparisons in the README (vs. Neo4j, Kuzu, FAISS, Weaviate, Qdrant, Milvus, pgvector, Pinecone, sqlite-vec) are drawn from those projects' own third-party benchmark posts rather than measured head-to-head — the README itself flags this as "order-of-magnitude orientation," not a controlled result, and this analysis carries that caveat forward rather than repeating the headline multiples as apples-to-apples.

## Known Gaps

| Issue | Detail |
|---|---|
| Bus factor | 4 contributors total (per GitHub API, accessed 2026-09-24) |
| Incomplete Cypher | No `OPTIONAL MATCH` or `CALL` procedures yet, per the README's own "When to Use Something Else" section |
| Single-writer, single-machine | No clustering, sharding, or multi-node replicas — the README recommends Neo4j, PostgreSQL, or Dgraph instead when that's a requirement |

## Adoption Decision

**Assess.** MIT-licensed, ~9 months old (created 2025-12), with credible self-reported latency numbers for the embedded-single-writer niche it targets (comparable in spirit to the now-archived Kuzu). Worth a pilot for local-first agent-memory or RAG use cases where a single embedded process is acceptable; the low bus factor (4 contributors) and young ecosystem are the main risks to track before depending on it in production.

## Sources

| Source | Content |
|---|---|
| [LatticeDB GitHub repo][repo] (README) | Architecture, query language, feature list, benchmark tables, license (accessed 2026-09-24) |
| [GitHub API — repo metadata][gh-api] | Stars, license, language, created/pushed dates (accessed 2026-09-24) |
| [GitHub API — latest release][gh-release] | v0.15.0, published 2026-08-29 |
| [GitHub API — contributors][gh-contrib] | 4 contributors (accessed 2026-09-24) |

[repo]: https://github.com/jeffhajewski/latticedb
[site]: https://latticedb.org
[gh-api]: https://api.github.com/repos/jeffhajewski/latticedb
[gh-release]: https://github.com/jeffhajewski/latticedb/releases/latest
[gh-contrib]: https://github.com/jeffhajewski/latticedb/graphs/contributors
