---
title: AgentCanvas — Pydantic AI Execution Trace Visualizer
source: https://github.com/vstorm-co/agentcanvas
purpose: Evaluate AgentCanvas as an observability/debugging tool for Pydantic AI agents via Logfire traces.
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
---

**Status**: Assess

## What It Is

[AgentCanvas][repo] is a Python CLI and library that transforms Pydantic AI
agent execution traces stored in [Logfire][logfire] into self-contained,
interactive HTML diagrams. The tool is authored by Vstorm, described as a
production agentic AI consultancy. It is MIT-licensed and published on PyPI as
`agentcanvas` (latest release: 0.1.1, June 12, 2026, accessed 2026-06-16).

The project sits in the **observability/debugging** category rather than in the
agent UI or generative-UI protocol space. It is not an implementation of AG-UI
or A2UI. Its closest neighbors are trace-inspection tools; the [AG-UI protocol
landscape][ag-ui-landscape] notes that Pydantic AI has adopted AG-UI as a
framework integration, but AgentCanvas itself is a separate, standalone
visualization layer built on top of Pydantic AI's OpenTelemetry output.

## How It Works

AgentCanvas follows a four-stage pipeline (all facts from the GitHub README,
accessed 2026-06-16):

1. **Collect** — Pydantic AI emits OpenTelemetry GenAI spans to Logfire during
   a run. The `LOGFIRE_READ_TOKEN` environment variable is required.
2. **Query** — The `logfire_client` module calls Logfire's query API to fetch
   the raw spans for a given trace ID (or the latest trace).
3. **Parse** — The `parser` module reconstructs the execution tree recursively,
   capturing model calls, tool invocations, nested sub-agents, token counts
   (input/output/reasoning), and per-step costs via `genai-prices`.
4. **Render** — The `render` module produces a single offline-capable HTML file
   (`agent_flow.html` by default) with an interactive pan/zoom/drag canvas.

Key features (from the README, accessed 2026-06-16):

- Recursive rendering of nested agents and sub-agents
- Full multi-turn conversation transcripts with reasoning summaries
- Exact cost calculation per model call and in aggregate
- Deep inspector: provider details, finish reasons, available tools
- Guided tours (auto and manual step modes) for client demonstrations
- Single-file HTML output — no server required after generation

**Language**: Python 98.7% (with Makefile 1.3%), requires Python 3.12+.
**Core dependencies**: Pydantic AI, Logfire, OpenTelemetry, genai-prices.
**Repository stats** (accessed 2026-06-16): 26 stars, 2 forks, MIT license.

## Adoption Decision

**Assess** — the tool is genuinely useful for any team running Pydantic AI
agents in production with Logfire, but it carries two hard constraints that
limit its scope:

- **Logfire lock-in**: the pipeline requires Pydantic AI telemetry piped
  through Logfire specifically. Teams using a different OpenTelemetry backend
  (Jaeger, Honeycomb, Grafana Tempo) cannot use AgentCanvas without adapting
  the `logfire_client` module.
- **Pydantic AI lock-in**: the span schema is specific to Pydantic AI's GenAI
  OTel instrumentation. LangGraph, CrewAI, or custom agent traces are not
  supported.

Within those constraints the tool is well-scoped: fully typed, uses ruff and
mypy, MIT-licensed, and installable in one `pip install agentcanvas` step. At
v0.1.1 it is early-stage (26 stars), so API stability is not guaranteed.

For research contexts in this repo, AgentCanvas is worth tracking as a
reference implementation of OTel-driven agent visualization. It does not
replace a protocol-level frontend (see [AG-UI landscape][ag-ui-landscape]) but
complements it by providing post-hoc trace inspection rather than live
streaming.

## Action Items

- Watch the repository for v0.2+ to assess whether Logfire dependency is
  relaxed to a generic OTel collector.
- Evaluate whether the `parser` module's recursive span-tree logic is
  reusable for other OTel-instrumented agent frameworks.
- Note the `genai-prices` dependency — verify it covers models in active use
  before adopting for cost reporting.

## Sources

| Source | Content |
|---|---|
| [vstorm-co/agentcanvas (GitHub)][repo] | Repository description, stars, forks, license, release version, topics |
| [README.md (GitHub)][readme] | Features, installation, architecture, dependencies, CLI/library usage, environment variables |

[repo]: https://github.com/vstorm-co/agentcanvas
[readme]: https://github.com/vstorm-co/agentcanvas/blob/main/README.md
[logfire]: https://logfire.pydantic.dev
[ag-ui-landscape]: ag-ui-protocol-landscape.md
