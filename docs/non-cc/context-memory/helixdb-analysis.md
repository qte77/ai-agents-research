---
title: HelixDB Analysis
source: https://github.com/HelixDB/helix-db
purpose: Analysis of HelixDB, a Rust graph-vector database positioned for knowledge graphs and AI-agent memory.
platform_scope: [claude-code, codex, opencode, cursor]
created: 2026-09-24
updated: 2026-11-26
validated_links_on: 2026-09-24
status: assess
---

## What It Is

[HelixDB][repo] is, per its README (checked 2026-11-26), "an open-source (Apache 2.0) graph database with native vector search and BM25 full-text search, built in Rust on object storage". The README FAQ frames use as memory and retrieval for AI applications (agent memory, GraphRAG/hybrid RAG, knowledge graphs) and answers that a separate vector database is not needed next to it (vectors are properties on nodes and edges). Key-value, document and relational support, and replacing a whole stack of separate databases, are not stated in the README (unverified), so evaluate the consolidation claim against a real workload rather than taking it at face value.

Stars: 6,315 · License: Apache-2.0 · Language: Rust · Latest release: **v3.7.0** (2026-11-11) · 37 non-anonymous contributors · homepage [helix-db.com][site] (all checked 2026-11-26, via GitHub API + latest-release lookup).

## How It Works

- **Query model**: queries are authored with DSL builders (Rust, TypeScript, Python, or Go), compile to a JSON AST, and are sent directly to a running instance over `POST /v2/query` — no build or deploy step. Current SDK releases: Rust crate `helix-db` 3.0.0, TypeScript `@helix-db/helix-db` 4.0.0, Python `helix-db` (PyPI) 0.4.0, Go `github.com/helixdb/helix-db/sdks/go` v0.3.1 (from the README's own SDK table).
- **Versioning is layered and easy to conflate**: "HelixDB v3" is the current product/SDK generation, the CLI is independently versioned as "3.x," and `POST /v2/query`'s `v2` refers only to the wire-protocol path — the README calls this out explicitly to avoid confusion.
- **`helix chef`**: an interactive, one-shot bootstrapper that installs HelixDB query skills and a docs Model Context Protocol (MCP) server, scaffolds a project, starts a local instance, seeds example data, and can hand off to a coding agent to build a working app end-to-end from a one-line description. It detects agent platforms in this order: Claude Code → OpenAI Codex → OpenCode → Cursor Agent.
- **HelixDB Cloud**: the commercial layer — an object-storage-backed managed deployment with full ACID transactions, a single writer with auto-scaling reader nodes, and high availability ("3+ gateways and DB nodes" is unverified); per [helix-db.com][site], MCP and CLI access use WorkOS sign-in or scoped service credentials, Database MCP is Cloud-only, plans start at $5/month for 200K reads and 100K writes (checked 2026-11-26), and SSO/SAML, role-based access, audit logs and AWS PrivateLink are listed as roadmap.

## Adoption Decision

**Assess.** Apache-2.0 licensing, 6k+ stars, and an active release cadence (v3.3.0 to v3.7.0, 2026-09-20 to 2026-11-11, five releases in about two months) make HelixDB worth evaluating for AI-agent memory or knowledge-graph backends, especially given first-class multi-language SDKs and the `helix chef` agent-handoff flow. Caveats: it is a young (created Nov 2024), single-vendor, YC-backed project with a hosted-Cloud upsell — check the commercial-vs-self-hosted feature split before depending on it for production memory. The README itself publishes no performance-benchmark figures; independent benchmarks were not sought in this pass and should be run before a capacity-sensitive deployment.

## Sources

| Source | Content |
|---|---|
| [HelixDB GitHub repo][repo] (README) | Architecture, query model, SDK versions, `helix chef`, Cloud features (checked 2026-11-26) |
| [helix-db.com][site] | Cloud plans, pricing, WorkOS sign-in, Database MCP, roadmap (checked 2026-11-26) |
| [HelixDB/helix-db][repo] (repo metadata + releases) | Stars, license, language, created/pushed dates, v3.7.0 release date (checked 2026-11-26 via GitHub API) |

[repo]: https://github.com/HelixDB/helix-db
[site]: https://helix-db.com
