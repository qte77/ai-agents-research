---
title: ByteDance DeerFlow Analysis
source: https://github.com/bytedance/deer-flow
purpose: Analysis of DeerFlow as an open-source super agent harness for research, coding, and content creation.
created: 2026-03-25
updated: 2026-03-25
---

**Status**: Open-source (Apache 2.0), active development by ByteDance

## What It Is

DeerFlow is an **open-source super agent harness** built on LangGraph/LangChain
that orchestrates sub-agents, memory, and sandboxed execution for tasks ranging
from minutes to hours. Tagline: "researches, codes, and creates."

**Key distinction**: Unlike CC (model-native agent) or Air (agent orchestrator),
DeerFlow is a batteries-included runtime — pre-built research/coding skills with
an extensible tool/skill system.

## Core Architecture

```
User → Primary Agent → Sub-agents (spawned dynamically)
                     → Skills (Markdown-based, modular)
                     → Tools (web search, file ops, bash, MCP)
                     → Sandbox (local / Docker / K8s)
                     → Memory (persistent context)
```

**Components:**

- **Skills**: Markdown-defined capability units (research, report generation,
  slide creation). Custom skills follow same format.
- **Tools**: Web search, file operations, bash execution, MCP server integration
  for custom tools.
- **Sandboxing**: Local, Docker, or Kubernetes-provisioned execution isolation.
- **Memory**: Persistent context engineering across conversations.
- **Sub-agents**: Dynamic spawning for task decomposition.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12+, LangChain, LangGraph |
| Frontend | Node.js 22+ |
| Models | OpenAI, Claude, DeepSeek, OpenRouter-compatible |
| Deployment | Local, Docker, Kubernetes |

## Adoption Decision

**Skip for Agents-eval** — LangGraph dependency is a full framework commitment.
Agents-eval uses PydanticAI for agent orchestration. DeerFlow's value is in its
pre-built research skills, which overlap with the existing MAS pipeline.

**Monitor for**: Skill format as a portable capability standard (Markdown-based
skills are a pattern also seen in CC). MCP tool integration may offer reusable
tool definitions.

## Comparison

| Dimension | DeerFlow | CC (Claude Code) | Air (JetBrains) |
|---|---|---|---|
| Type | Agent harness | Model-native agent | Agent orchestrator |
| Framework | LangGraph/LangChain | Anthropic-native | Proprietary |
| Skills | Markdown-based | Markdown SKILL.md | N/A (delegates) |
| Sandboxing | Docker/K8s/local | Filesystem + network | Worktrees/Docker |
| Multi-agent | Sub-agent spawning | Agent teams | Multi-agent parallel |
| MCP support | Yes (tools) | Yes (servers) | Planned (ACP) |
| Open source | Yes (Apache 2.0) | Yes (consumer license) | No |

## Action Items

- [ ] Track skill format evolution — compare with CC SKILL.md for convergence
- [ ] Monitor MCP tool registry for reusable tool definitions
