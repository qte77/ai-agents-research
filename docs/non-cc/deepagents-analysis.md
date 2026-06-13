---
title: deepagents Analysis
source: https://github.com/langchain-ai/deepagents
purpose: Architecture analysis of deepagents — LangChain's batteries-included harness for long-horizon agents with planning, sub-agent delegation, and a virtual filesystem, built on LangGraph.
created: 2026-06-13
updated: 2026-06-13
validated_links: 2026-06-13
---

**Status**: Assess

## What It Is

`deepagents` is LangChain's opinionated, production-ready harness for building long-horizon "deep" agents — agents that plan, delegate work to sub-agents, manage files, and maintain context across extended task runs, all on a LangGraph runtime ([repo][repo]).

- **License**: MIT
- **Package**: `deepagents` ([PyPI][pypi])
- **Version**: 0.6.10
- **Stars**: 24.6k

## Key Concepts

| Pillar | What it provides |
|---|---|
| **LangGraph foundation** | Underlying graph runtime — streaming, persistence, and checkpointing |
| **Sub-agent delegation** | Spawn isolated sub-agents with their own context windows for parallel or sequential work |
| **Virtual filesystem** | Read / write / edit across pluggable backends (local, sandboxed, or remote) |
| **Planning (todo list)** | Built-in task decomposition: the agent maintains and works through a dynamic todo list |
| **Context management** | Thread summarisation and tool-output archiving to handle long conversations |
| **Shell access** | Execute commands in a sandboxed environment |
| **Persistent memory** | Cross-session recall via pluggable memory backends |
| **Human-in-the-loop** | Review and approve tool calls before execution |
| **Skills** | Loadable, reusable agent behaviours |
| **LangSmith integration** | Built-in tracing and evaluation for production deployment |

The public entry point is `create_deep_agent`, which returns a compiled LangGraph agent (the `model` argument is optional and defaults to a Claude model):

```python
from deepagents import create_deep_agent

agent = create_deep_agent(
    tools=[my_custom_tool],
    system_prompt="You are a research assistant.",
)
result = agent.invoke({"messages": "Research LangGraph and write a summary"})
```

## Positioning

| Dimension | deepagents | Plain LangGraph | AutoAgent ([analysis][autoagent]) | simpleagents ([analysis][simpleagents]) |
|---|---|---|---|---|
| Abstraction level | High — opinionated defaults | Low — graph primitives only | High — zero-code NL interface | SDK / infrastructure layer |
| Sub-agent delegation | Yes (built-in) | Manual wiring | Yes (workflow editor) | Planned (issue #25) |
| Virtual filesystem | Yes (pluggable backends) | No | Self-managing FS | No |
| Planning | Todo-list tool | No | Self-play customisation | No |
| Language | Python | Python | Python | Rust + polyglot bindings |
| Model agnostic | Yes (any tool-calling LLM) | Yes | Via LiteLLM | Yes (OpenAI, Anthropic, OpenRouter) |
| Production runtime | LangGraph + LangSmith | LangGraph | Docker sandbox | gRPC workers |

### What deepagents adds over plain LangGraph

LangGraph provides the graph execution primitive. `deepagents` layers opinionated defaults on top: a tuned system prompt for long-horizon work, a planning tool, a virtual filesystem, sub-agent spawning, context summarisation, shell execution, and memory — so teams do not need to wire each capability individually.

### Where it sits in the ecosystem

Among agent frameworks that target long-horizon tasks, deepagents is the closest to a "production harness with batteries included." It is narrower than AutoAgent (which is NL-driven and self-modifying) but deeper than plain LangGraph (which is a runtime only). The simpleagents framework targets a different niche (Rust-first SDK with polyglot bindings) and does not overlap in philosophy.

## Sources

[repo]: https://github.com/langchain-ai/deepagents
[pypi]: https://pypi.org/project/deepagents/
[autoagent]: autoagent-analysis.md
[simpleagents]: simpleagents-analysis.md
