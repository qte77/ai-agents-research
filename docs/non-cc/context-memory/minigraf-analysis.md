---
title: Minigraf Analysis
source: https://github.com/project-minigraf/minigraf
purpose: Analysis of Minigraf, an embedded bi-temporal Datalog graph database pitched as agent memory.
created: 2026-10-11
updated: 2026-10-11
validated_links: 2026-10-11
status: assess
---

## What It Is

[Minigraf][repo] is a single-file embedded graph database — "the SQLite of bi-temporal graph
databases," per its own tagline — queried with **Datalog** and supporting **bi-temporal time
travel** (separate transaction-time and valid-time dimensions on every fact). The core is Rust
(crates.io, current v2.0.5, MSRV 1.89), with published bindings for Python (PyPI), Node.js (npm),
browser/WASM (`@minigraf/browser`, IndexedDB-backed via `wasm-pack`), WASI (`@minigraf/wasi`), and
native mobile (Android `.aar` + iOS `.xcframework` via [Mozilla's uniffi-rs][uniffi]). `cargo test`
runs 1,250 tests; CI, Clippy, and Codecov badges are green per the README (not independently re-run
by this review).

## How It Works

- **Datalog over SQL-like querying.** The README's stated rationale: recursive multi-hop traversal is
  native to Datalog (`(rule [(reachable ?a ?b) [?a :friend ?b]] [(reachable ?a ?b) [?a :friend ?m]
  (reachable ?m ?b)])`), the grammar is small enough to fit a system prompt — framed explicitly as
  "LLM-friendly" — and facts are literally Entity-Attribute-Value edges.
- **Bi-temporal queries.** Every fact carries transaction time (when it was recorded) and valid time
  (when it was true), so a query can ask `:as-of <tx>` to reconstruct exactly what was known or true
  at a past point, including corrections (`retract` + `transact` pairs) without losing the original
  record.
- **Prepared statements and windowed aggregates.** Parse-and-plan-once `$slot`-bound prepared queries,
  plus `sum/count/min/max/avg/rank/row-number :over (partition-by … :order-by …)` window functions in
  `:find` clauses.
- **Platform tiers.** Tier 1 (fully tested, released with every core release): Rust (crates.io) and
  Python (PyPI). Tier 2 (built/smoke-tested, best-effort, experimental): browser WASM, WASI, Node.js,
  Java/JVM (Maven Central), Android, iOS/macOS, and C/FFI.
- **Performance (self-reported, `docs/BENCHMARKS.md`):** at 1M facts, point query 4.3–4.5s, open time
  1.31s, peak heap 1.05GB. A 4,080-byte max fact size applies to file-backed databases only.

### For AI Agents

The README's own framing: store what an agent believes, retract and correct without losing history,
and replay past states to audit a past decision. It positions Minigraf as a companion to vector
stores rather than a replacement — "the vector store answers 'what is similar?'; Minigraf answers
'what are the relationships, who recorded them, and what did we believe at time T?'" — i.e. the
GraphRAG pattern already covered for [HelixDB][helixdb] and [LatticeDB][latticedb] in this directory.

## License, stars, dates

Dual-licensed **MIT OR Apache-2.0** — confirmed by opening and reading both license files directly,
not just their directory listing: `LICENSE-MIT` begins "MIT License / Copyright (c) 2023-2026 Aditya
Mukhopadhyay"; `LICENSE-APACHE` is the unmodified Apache License, Version 2.0 text. GitHub's own
repo-level `license` API field can report only one value for a dual-licensed repo and shows
`apache-2.0`. 186 stars, 13 forks, 45 open issues (`gh api repos/project-minigraf/minigraf`,
2026-10-11). Created 2023-07-02, last pushed 2026-10-11 (same day) — over three years of continuous
history, not a flash project. The README itself states this is "a solo-maintained project with a
long-term vision."

## The cited third-party agent-memory demo is the maintainer's own example

The README's "For AI Agents" evidence points to a "working implementation of temporal reasoning with
Minigraf" at `github.com/adityamukho/temporal_reasoning`, described as "an AI agent that uses
Minigraf's bi-temporal model to store, correct, and audit beliefs" — framed as if it were independent
third-party validation of the agent-memory use case. Two pieces of first-party evidence, read
directly rather than inferred from the name alone, indicate this is the project's own maintainer,
not an independent adopter:

1. Minigraf's own `LICENSE-MIT` file names the copyright holder as "Aditya Mukhopadhyay" — the same
   name as the GitHub user `adityamukho` credited for the demo.
2. The README's own "For Python / Node.js / Java / C" section states the Java/JVM package ships as
   `io.github.adityamukho:minigraf-jvm` on Maven Central (the platform-support table two sections
   earlier gives a different group ID, `io.github.project-minigraf:minigraf-jvm`, for the same
   package — an inconsistency in the README itself; `project-minigraf` is the project's own GitHub
   org namespace, while `adityamukho` is the maintainer's personal GitHub handle, so this is not a
   third party's namespace either way).

Both point the same way: the demo the README cites as evidence for the agent-memory use case is very
likely the maintainer demonstrating their own project, not independent corroboration. This review did
not open the `temporal_reasoning` repository itself to check its commit history or contributors.

## Adoption Decision

**Assess.** Minigraf is a mature (3+ years), dual-licensed, multi-platform (Rust/Python/Node/
WASM/mobile) embedded graph database with a real test suite and an active release cadence, and its
Datalog-plus-bi-temporal model is a genuinely distinctive combination (its own comparison table shows
no competitor — XTDB, Cozo, Neo4j, SQLite — matching single-file + bi-temporal + embedded + graph-
native + Rust together). Its positioning as agent memory is vendor-documented, not independently
demonstrated: there is no MCP server or memory-specific API beyond the general Datalog interface, and
the one example cited for the agent-memory use case is the maintainer's own project (see above), not
a third-party adopter. Worth evaluating as a general embedded graph/temporal store; treat the
"for AI agents" framing as a positioning claim pending an independent adopter.

## Sources

| Source | Content |
|---|---|
| [project-minigraf/minigraf][repo] (README) | Product description, Datalog/bi-temporal model, platform tiers, agent-memory framing, demo citation (accessed 2026-10-11) |
| [project-minigraf/minigraf][repo] (repo metadata) | Stars/forks/issues, created/pushed dates (accessed 2026-10-11 via GitHub API) |
| `LICENSE-MIT` and `LICENSE-APACHE` files, decoded via GitHub API, 2026-10-11 | Dual MIT/Apache-2.0 text; MIT copyright holder "Aditya Mukhopadhyay" |

[repo]: https://github.com/project-minigraf/minigraf
[uniffi]: https://github.com/mozilla/uniffi-rs
[helixdb]: helixdb-analysis.md
[latticedb]: latticedb-analysis.md
