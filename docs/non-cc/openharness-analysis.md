---
title: OpenHarness Analysis
source: https://github.com/HKUDS/OpenHarness
purpose: Analysis of HKUDS OpenHarness — an open-source Python agent harness framework (10 subsystems) compatible with Claude Code conventions but provider-agnostic.
created: 2026-06-27
updated: 2026-06-27
validated_links: 2026-06-27
---

**Status**: Assess

## What It Is

OpenHarness (HKUDS) is an **open-source Python agent harness framework** — infrastructure plumbing between LLMs and tools. It implements **10 core subsystems** and is **compatible with Claude Code conventions** (markdown skills, plugin architecture, CLAUDE.md, hooks, MCP), but is an independent, multi-provider harness rather than a CC plugin — which is why it lives here rather than in the cc-community tooling docs.

**Repo**: [HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) | **Stars**: 14.2K | **License**: MIT | **Version**: 0.1.0 (2026-04-01)

## Core Subsystems

| Subsystem | Purpose | CC Equivalent |
|-----------|---------|---------------|
| **Engine** | Streaming tool-call loop with retry | CC agent loop |
| **Tools** | 43+ integrated tools (file I/O, shell, web, MCP) | CC built-in tools |
| **Skills** | On-demand markdown knowledge loading | `.claude/skills/` |
| **Plugins** | Extensions for commands, hooks, agents | `.claude-plugin/` |
| **Permissions** | Multi-level safety with path rules | `settings.json` permissions |
| **Hooks** | PreToolUse/PostToolUse lifecycle events | CC hooks system |
| **Commands** | 54 built-in directives (/commit, /plan, etc.) | CC slash commands |
| **Memory** | Persistent cross-session knowledge | CC memory system |
| **Coordinator** | Subagent spawning and team management | CC agent teams |
| **UI** | React (Ink) TUI + backend protocol | CC terminal UI |

## Multi-Provider Support

- **Anthropic format** (default): Claude, Moonshot/Kimi, Vertex, Bedrock
- **OpenAI format** (`--api-format openai`): OpenAI, DeepSeek, DashScope, GitHub Models, Groq, Ollama

## Adoption Considerations

**Strengths**: Most complete open harness (10 subsystems, 43 tools, 114 tests, 6 E2E suites). CC-convention compatible — skills, plugins, CLAUDE.md, hooks all work. Multi-provider. MIT licensed.

**Risks**: Early stage (v0.1.0). Not a CC replacement — lacks CC's model quality, context-window management, and Anthropic infrastructure. Python-only (CC is TypeScript/Node).

## Cross-References

- [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) — orchestration frameworks catalog (LangGraph, CrewAI, PydanticAI, …)
- [harnessx-analysis.md](harnessx-analysis.md) — harness-evolution research (adjacent)
- [agentic-engineering-disciplines-landscape.md](../sdlc-lcm/agentic-engineering-disciplines-landscape.md) — harness engineering ("the model doesn't change — the harness does")

## Sources

| Source | Content |
|---|---|
| [HKUDS/OpenHarness](https://github.com/HKUDS/OpenHarness) | Open-source Python agent harness framework (10 subsystems, 43 tools; MIT) |
