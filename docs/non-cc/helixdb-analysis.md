---
title: HelixDB Analysis
source: https://github.com/HelixDB/helix-db
purpose: Analysis of HelixDB, a Rust graph-vector database positioned for knowledge graphs and AI-agent memory.
platform_scope: [claude-code, codex, opencode, cursor]
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

[HelixDB][repo] is a graph-vector database "for knowledge graphs and AI memory," built from scratch in Rust. It primarily uses a graph-plus-vector data model but also supports key-value, document, and relational data. Its vendor positioning is to replace a stack of separate application/relational/vector/graph databases with one platform — a claim worth verifying against a real workload rather than taking at face value.

Stars: 6,087 · License: Apache-2.0 · Language: Rust · Latest release: **v3.3.0** (2026-09-20) · 32 contributors · homepage [helix-db.com][site] (all accessed 2026-09-24, via GitHub API + latest-release lookup).

## How It Works

- **Query model**: queries are authored with DSL builders (Rust, TypeScript, Python, or Go), compile to a JSON AST, and are sent directly to a running instance over `POST /v2/query` — no build or deploy step. Current SDK releases: Rust crate `helix-db` 3.0.0, TypeScript `@helix-db/helix-db` 3.1.0, Python `helix-db` (PyPI) 0.3.4, Go `github.com/helixdb/helix-db/sdks/go` v0.3.1 (from the README's own SDK table).
- **Versioning is layered and easy to conflate**: "HelixDB v3" is the current product/SDK generation, the CLI is independently versioned as "3.x," and `POST /v2/query`'s `v2` refers only to the wire-protocol path — the README calls this out explicitly to avoid confusion.
- **`helix chef`**: an interactive, one-shot bootstrapper that installs HelixDB query skills and a docs MCP server, scaffolds a project, starts a local instance, seeds example data, and can hand off to a coding agent to build a working app end-to-end from a one-line description. It detects agent platforms in this order: Claude Code → OpenAI Codex → OpenCode → Cursor Agent.
- **HelixDB Cloud**: the commercial layer — an object-storage-backed managed deployment with full ACID transactions, a single writer with auto-scaling reader nodes, and high availability (3+ gateways and DB nodes), authenticated via a WorkOS session from the CLI.

## Adoption Decision

**Assess.** Apache-2.0 licensing, 6k+ stars, and an active release cadence (v3.3.0 shipped days before this review) make HelixDB worth evaluating for AI-agent memory or knowledge-graph backends, especially given first-class multi-language SDKs and the `helix chef` agent-handoff flow. Caveats: it is a young (created Nov 2024), single-vendor, YC-backed project with a hosted-Cloud upsell — check the commercial-vs-self-hosted feature split before depending on it for production memory, and no independent (non-vendor) benchmarks were found as of 2026-09-24.

## Sources

| Source | Content |
|---|---|
| [HelixDB GitHub repo][repo] (README) | Architecture, query model, SDK versions, `helix chef`, Cloud features (accessed 2026-09-24) |
| [GitHub API — repo metadata][gh-api] | Stars, license, language, created/pushed dates (accessed 2026-09-24) |
| [GitHub API — latest release][gh-release] | v3.3.0, published 2026-09-20 |

[repo]: https://github.com/HelixDB/helix-db
[site]: https://helix-db.com
[gh-api]: https://api.github.com/repos/HelixDB/helix-db
[gh-release]: https://github.com/HelixDB/helix-db/releases/latest
