---
title: LatticeDB Analysis
source: https://github.com/jeffhajewski/latticedb
purpose: Analysis of LatticeDB, an embedded single-file graph, vector, and full-text database written in Zig.
created: 2026-09-24
updated: 2026-11-26
validated_links_on: 2026-09-24
status: assess
---

## What It Is

[LatticeDB][repo] is an embedded, single-file property-graph database combining graph traversal, HNSW vector search, and BM25 full-text search behind one Cypher-like query language (`MATCH`/`WHERE`/`RETURN`, a vector-distance operator `<=>`, a text-match operator `@@`). It is written in Zig with no external dependencies, uses a single-writer embedded model (one owning process, WAL-backed durability), and targets local, relationship-heavy workloads such as Graph RAG and agent memory — its own README frames these as example workloads built on the graph/vector/text substrate, not the definition of the engine.

Stars: 764 · License: MIT · Language: Zig · Latest release: **v0.18.1** (2026-11-18, via GitHub Releases) · 5 contributors · homepage [latticedb.org][site] (all checked 2026-11-26). Bindings: CLI, Python (`pip install latticedb`), TypeScript/Node (`npm install @hajewski/latticedb`), Go (cgo), Java (JDK 21+, JNI).

## Performance (Self-Reported)

Benchmarked by the project on Apple M5 (README, v0.17.0, medians of five runs, checked 2026-11-26; the project says `zig build capi-benchmark` reproduces the tables):

- Property read by node id: 0.22 μs p50 (C API, open read transaction).
- 10-NN vector search at 1M vectors, default 100 MB cache: 1.34 ms p50, 3.1 ms p99, recall@10 95.6%; with a 2 GB cache 0.21 ms p50, 0.46 ms p99.
- Graph traversal vs. SQLite: level for 1-3 hops and about 2x faster for `*1..5` paths (600 μs vs. 1,361 μs in the repo's competitive-analysis page); SQLite inserts rows several times faster (332K nodes/s vs. 1.84M rows/s). The earlier M1 figures (including a 2,819x traversal speedup) are no longer in the README.

The README's cross-vendor comparison section cited in the earlier version of this analysis is no longer present (unverified), so no cross-vendor multiples are repeated here.

## Known Gaps

| Issue | Detail |
|---|---|
| Bus factor | 5 contributors total (per GitHub API, checked 2026-11-26) |
| Incomplete Cypher | `OPTIONAL MATCH`, `UNION`, `CASE` and `CALL { }` subqueries are implemented; quantified path patterns, `LOAD CSV`, user-defined procedures, temporal/spatial types and schema statements are not, per the README (checked 2026-11-26) |
| Single-writer, single-machine | No clustering, sharding, or multi-node replicas — the README recommends Neo4j, PostgreSQL, or Dgraph instead when that's a requirement |

## Adoption Decision

**Assess.** MIT-licensed, ~11 months old (created 2025-12-20), with credible self-reported latency numbers for the embedded-single-writer niche it targets — comparable in spirit to Kuzu, whose own [GitHub repo](https://github.com/kuzudb/kuzu) is archived (last push 2025-10-10, checked 2026-11-26). Worth a pilot for local-first agent-memory or Retrieval-Augmented Generation (RAG) use cases where a single embedded process is acceptable; the low bus factor (5 contributors) and young ecosystem are the main risks to track before depending on it in production.

## Sources

| Source | Content |
|---|---|
| [LatticeDB GitHub repo][repo] (README) | Architecture, query language, feature list, benchmark tables, license (checked 2026-11-26) |
| [jeffhajewski/latticedb][repo] (repo metadata, releases, contributors) | Stars, license, language, created/pushed dates, v0.18.1 release date, 5-contributor count (checked 2026-11-26 via GitHub API) |

[repo]: https://github.com/jeffhajewski/latticedb
[site]: https://latticedb.org
