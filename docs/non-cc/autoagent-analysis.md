---
title: AutoAgent Analysis (HKUDS)
source: https://github.com/HKUDS/AutoAgent
purpose: Analysis of AutoAgent as a zero-code LLM agent framework with self-developing capabilities.
category: analysis
status: research
created: 2026-04-06
updated: 2026-04-06
validated_links: 2026-04-06
---

**Status**: Open-source (MIT), active development by HKU Data Science Lab

## What It Is

AutoAgent is a **fully-automated, zero-code LLM agent framework** from the University of Hong Kong (HKUDS lab). Users create and deploy agents through natural language alone -- no programming required. It operates as an autonomous Agent Operating System with self-developing capabilities: the system can generate its own tools, agents, and workflows at runtime.

**Stars**: 8,925 | **License**: MIT | **Paper**: [arxiv:2502.05957](https://arxiv.org/abs/2502.05957)

**Key distinction**: Unlike LangChain or AutoGen (which require programming), AutoAgent targets the 99.97% of the population without coding skills. Unlike CC (which requires CLI proficiency), AutoAgent accepts plain natural language task descriptions.

## Cross-References in This Repository

| Topic | Existing Analysis | File |
|-------|------------------|------|
| Paper citation | Further reading (arxiv 2502.05957) | `docs/todo/research/further_reading.md:797` |
| HKUDS OpenHarness | Community tooling landscape | `docs/cc-community/CC-community-tooling-landscape.md:147-179` |
| HKUDS CLI-Anything | CLI analysis | `docs/cc-native/agents-skills/CC-cli-anything-analysis.md` |
| HKUDS AI-Researcher | Further reading (NeurIPS 2025 Spotlight) | `docs/todo/research/further_reading.md:732` |
| Agent frameworks | 30+ frameworks landscape | `docs/todo/landscape/agent_frameworks.md` |
| Zero-code agents | Convergence research | `docs/todo/research/research_integration_analysis.md` |

## Three Operational Modes

### User Mode (Deep Research Agents)

Ready-to-use multi-agent system for information retrieval and report generation. Claims to match Deep Research performance using Claude 3.5 Sonnet instead of o3. Launch: `auto deep-research`.

### Agent Editor Mode

Natural-language-driven single-agent creation: describe the desired agent -> automated profiling -> tool code generation -> task specification -> deployed agent. Supports tool creation.

### Workflow Editor Mode

Multi-agent workflow generation through natural language. Handles workflow profiling and agent coordination. Does not support tool creation (workflow-level orchestration only). Launch: `auto main`.

## Core Architecture

Four components forming an autonomous Agent Operating System:

1. **Agentic System Utilities** -- foundational services
2. **LLM-powered Actionable Engine** -- inference backbone
3. **Self-Managing File System** -- autonomous resource management
4. **Self-Play Agent Customization** -- iterative self-refinement for single and multi-agent systems

**Self-modification**: Docker sandbox allows AutoAgent to update its own codebase, adding new tools/agents/workflows to a cloned mirror repository during runtime.

## Model Support

Uses [LiteLLM](https://github.com/BerriAI/litellm) abstraction layer (100+ models):

| Provider | Default Model |
|----------|--------------|
| Anthropic | `claude-3-5-sonnet-20241022` (default) |
| OpenAI | `gpt-4o` |
| DeepSeek | `deepseek/deepseek-chat` |
| Google Gemini | `gemini/gemini-2.0-flash` |
| Groq | `groq/deepseek-r1-distill-llama-70b` |
| HuggingFace | `huggingface/meta-llama/Llama-3.3-70B-Instruct` |
| OpenRouter | `openrouter/deepseek/deepseek-r1` |

## Benchmarks

| Benchmark | Result |
|-----------|--------|
| [GAIA](https://gaia-benchmark-leaderboard.hf.space/) | Surpasses existing SOTA on generalist multi-agent tasks |
| MultiHopRAG | Superior performance vs alternative LLM-based RAG solutions |
| SWE-bench | Planned |
| WebArena | Planned |

## Comparison

| Dimension | AutoAgent | CC (Claude Code) | OpenHarness (HKUDS) |
|-----------|-----------|------------------|---------------------|
| Target user | Non-programmers | Developers (CLI) | Developers (CLI) |
| Agent creation | Natural language | CLAUDE.md + skills | Config + CLI |
| Self-modification | Yes (Docker sandbox) | No | No |
| Tool creation | Runtime code generation | MCP servers | 43+ built-in tools |
| Multi-agent | Workflow Editor mode | Agent teams | Coordinator subsystem |
| MCP support | No (own tool system) | Yes | Yes |
| Model default | Claude 3.5 Sonnet | Claude (native) | Configurable |
| Sandboxing | Docker (mandatory) | Filesystem + network | Filesystem |

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Core | Python (pip-installable) |
| Sandbox | Docker (mandatory) |
| Models | LiteLLM abstraction |
| CLI | `auto main`, `auto deep-research` |
| Tool management | `tool_docs.csv`, runtime code generation |

## Sources

- [GitHub: HKUDS/AutoAgent](https://github.com/HKUDS/AutoAgent)
- [Paper: AutoAgent (arxiv:2502.05957)](https://arxiv.org/abs/2502.05957)
- [Project page: AutoAgent-ai.github.io](https://AutoAgent-ai.github.io)
- [GAIA Benchmark Leaderboard](https://gaia-benchmark-leaderboard.hf.space/)

## Action Items

- [ ] Track SWE-bench and WebArena results when published
- [ ] Compare self-modification approach with CC's static skills model
- [ ] Monitor HKUDS lab output -- also behind OpenHarness, CLI-Anything, AI-Researcher
- [ ] Evaluate zero-code paradigm as onboarding path for non-developer users
