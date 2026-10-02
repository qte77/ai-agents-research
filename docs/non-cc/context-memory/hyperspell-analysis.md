---
title: Hyperspell Analysis
source: https://hyperspell.com
purpose: Analysis of Hyperspell, a hosted company-data memory/context platform for AI agents, scored against the plan-0009/0010 agent-substrate rubric — checked as a lead for the context·Shared and context·Distributed open cells (plan 0010, row L1).
created: 2026-10-02
updated: 2026-10-02
validated_links: 2026-10-02
status: assess
---

## What It Is

Hyperspell is a hosted platform, described on its own site as the "memory layer for your business": it
connects company data sources (Slack, email, drive, CRM, and more) and "surfaces it as a filesystem any
agent can read" ([hyperspell.com][hyperspell-home], fetched 2026-10-02). The company (YC F25; founder Conor
Brennan-Burke) frames the problem as agents lacking "sufficient context and memory to be truly useful"
([Every.io profile][every-profile]).

**Context or memory?** Despite the "context" framing in places, Hyperspell's own description —
"continuously synthesizes your data into one bespoke model of the company that is always up-to-date" and
improves "with every query and every conversation" ([hyperspell.com][hyperspell-home]) — matches this
corpus's **memory** taxonomy (persistent, evolving state across sessions, built from ingested sources), the
same shape as [Mitosis Cortex][cortex] (hosted per-team knowledge-graph memory) and [Core][core] (personal
AI OS indexing many sources) in this corpus, not the **context** taxonomy (what enters the context window
per turn). Placed here as memory; **this does not fill the context·Shared or context·Distributed open
cells** (plan 0010, row L1) — see [Redis Iris's Context Retriever][redis-iris] for a lead that does bear on
those cells.

## Facts

- Ingests from Gmail, Slack, Notion, and other permissioned data sources; builds a "context graph" queried
  via a universal API/SDK ([hyperspell.com][hyperspell-home]).
- Client libraries are published under the `hyperspell` GitHub org: [`node-sdk`][node-sdk] (MIT, 4★/1 fork,
  pushed 2026-09-27, `gh api` 2026-10-02), a Python SDK (MIT, 3★/0 forks per repo listing, `gh api`
  2026-10-02), and a Go SDK, plus an `hyperspell-mcp` MCP server, an `hyperspell-openclaw` plugin, and an
  `hyperspell-n8n-node` community node.
- **No LICENSE file for the core platform**: the hosted service itself is closed, with no self-hosting path
  documented. Only the thin client SDKs (REST wrappers) are open-source (MIT) — the same pattern this
  corpus already notes for Mitosis Cortex (closed engine, MIT client-side integrations) and Runtype (closed
  platform, Apache-2.0 CLI only).
- YC F25 batch; raised ~$2.0M from Y Combinator and The Autopilot Fund ([startup profile sources][yc-funding]).
- No first-party documentation of multi-agent concurrent access, cross-machine sync, or self-hosting was
  found on the fetched pages.

## Rubric

Scored 2026-10-02, evidence from [hyperspell.com][hyperspell-home] unless noted. Subject: **Memory** (see
placement note above).

`subject: memory`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no data [hyperspell.com][hyperspell-home] (describes a per-company knowledge model multiple agents can query, but no concurrency/locking semantics are documented — the rubric's own trap: "a hosted SaaS alone is not 'shared' if each user gets an isolated silo," and nothing here rules that reading) | no data [hyperspell.com][hyperspell-home] (a hosted SaaS with no self-hosting path or deployment architecture disclosed) | no data [hyperspell.com][hyperspell-home] (describes continuous, query-reinforced synthesis — an unpinned, evolving process — with no pinned model/version or rebuild path stated) | no data [hyperspell.com][hyperspell-home] (no schema/plugin/extension mechanism documented beyond "connect your tools") | no data [hyperspell.com][hyperspell-home] (no snapshot/diff/rollback of the context graph documented) | no data [hyperspell.com][hyperspell-home] (no citation or audit-trail mechanism documented for what the agent reads) |

**Strongest claim check**: nothing here is scored above `no data` — the fetched marketing page makes
architecture claims ("bespoke model of the company", "continuous learning") but documents no mechanism for
any of the six properties, so none is asserted.

## Sources

| Source | Content |
|---|---|
| [hyperspell.com][hyperspell-home] | Product description, architecture framing (fetched 2026-10-02) |
| [Every.io — "AI Agents are the Future"][every-profile] | Founder/company background |
| [hyperspell/node-sdk][node-sdk] | Client SDK license and repo metadata (`gh api`, 2026-10-02) |
| [Plan 0010, row L1][plan] | Lead source and open-cell framing |

[hyperspell-home]: https://hyperspell.com
[every-profile]: https://www.every.io/blog-post/ai-agents-are-the-future-conor-brennan-burke-is-building-the-infrastructure-that-enables-them-to-run
[yc-funding]: https://www.ycombinator.com/companies/hyperspell
[node-sdk]: https://github.com/hyperspell/node-sdk
[cortex]: mitosis-cortex-analysis.md
[core]: ../../cc-community/CC-memory-tooling-landscape.md#core-redplanethq
[redis-iris]: redis-iris-analysis.md#context-retriever
[plan]: ../../plans/2026-10-01-0010-open-substrate-cells.md
