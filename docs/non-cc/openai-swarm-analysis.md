---
title: OpenAI Swarm Analysis
source: https://github.com/openai/swarm
purpose: Analysis of OpenAI Swarm as a deprecated educational multi-agent orchestration framework superseded by the OpenAI Agents SDK.
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
---

**Status**: Hold

## What It Is

[Swarm][repo] is an **educational, experimental** multi-agent orchestration
framework managed by the OpenAI Solution team. Its own README describes it as
"exploring ergonomic, lightweight multi-agent orchestration" — the word
*educational* is intentional: the project was never positioned for production.

The repository is now explicitly deprecated. The README states that "Swarm is
now replaced by the [OpenAI Agents SDK][agents-sdk], which is a
production-ready evolution of Swarm." Current users are directed to migrate.

## How It Works

Swarm operates **statelessly via the Chat Completions API** (not the Assistants
API) and runs almost entirely client-side. Its two core abstractions are:

- **Agents** — Python objects that bundle a system prompt (instructions) and a
  list of callable tools. Each agent encapsulates a slice of capability.
- **Handoffs** — an agent can transfer execution mid-conversation to another
  agent by returning a special `Agent` object. This is the primary composition
  mechanism: a triage agent routes to a specialist agent, which may route
  further.

Supporting primitives include **context variables** (a shared dict threaded
through every agent call for stateful bookkeeping) and **function calling**
(plain Python functions are introspected to auto-generate JSON schemas).

Because the orchestration loop runs client-side and statelessly, Swarm is easy
to trace and debug but unsuitable for long-running or production workloads.

| Attribute | Value (fetched 2026-06-16) |
|---|---|
| Language | Python (100%) |
| License | MIT |
| Stars | 21.6k |
| Forks | 2.3k |
| Commits | 29 total |
| Published releases | None |
| Status | Deprecated — educational only |

## Adoption Decision

**Hold.** Swarm is deprecated upstream and replaced by the [OpenAI Agents
SDK][agents-sdk], which the Agents SDK docs call "a production-ready upgrade of
our previous experimentation for agents, Swarm." There is no reason to adopt
Swarm in new work.

The **handoffs** pattern Swarm pioneered is worth understanding conceptually —
it maps cleanly onto the agent-routing primitives in frameworks catalogued in
the [Agent Frameworks & Infrastructure Landscape][landscape]. The **client-side
stateless loop** design is a useful reference for minimal harness construction,
but the implementation itself should not be used.

For OpenAI-ecosystem multi-agent work, use the OpenAI Agents SDK directly:
it preserves the handoffs model, adds guardrails, tracing, sessions, MCP
server integration, and realtime voice support (`pip install openai-agents`).

## Action Items

- Do not use Swarm in any new evaluation or integration work.
- If existing experiment notebooks reference Swarm, note the migration path:
  replace `swarm.Swarm` with the Agents SDK agent loop; handoff semantics
  carry over almost unchanged.
- Re-evaluate the OpenAI Agents SDK entry in [agent-frameworks-infrastructure-landscape.md][landscape]
  if deeper integration with OpenAI tooling is needed.

## Sources

| Source | Content |
|---|---|
| [openai/swarm GitHub][repo] | Deprecation notice, description, stars, forks, license, architecture |
| [OpenAI Agents SDK docs][agents-sdk] | Explicit supersession statement, SDK features |

[repo]: https://github.com/openai/swarm
[agents-sdk]: https://openai.github.io/openai-agents-python/
[landscape]: agent-frameworks-infrastructure-landscape.md
