---
title: Block Goose Analysis
source: https://github.com/block/goose
purpose: Analysis of Goose as MCP co-creator, reference implementation, and AAIF founding project — architectural comparison with CC's MCP integration.
created: 2026-04-05
updated: 2026-04-05
validated_links: 2026-04-05
---

**Status**: Assess (open-source, active, architecturally significant)

## What It Is

Goose is an open-source (Apache-2.0) coding agent by Block (Square). 36K+ stars, Rust 58% / TypeScript 34%, 126 releases. Desktop app + CLI. LLM-agnostic with multi-model routing.

**Key distinction**: Goose co-developed MCP with Anthropic — Block's internal extension friction led to the collaboration that produced the protocol. Goose is the **reference MCP implementation**, not merely an adopter. It is an AAIF founding project alongside MCP and AGENTS.md ([source][aaif]).

## MCP Co-Origin

Before MCP had a name, Block's internal Goose agent had a Python extension system that required custom integration per tool. Block contacted Anthropic about this friction and discovered Anthropic was already building what became MCP. They co-developed the protocol, with Goose as the proving ground ([source][arcade-origin]).

This means Goose's architecture **is** MCP architecture — extensions are MCP servers, tools are MCP tool calls, the agent loop speaks MCP natively. 3,000+ MCP servers available. Goose is also the reference client for MCP Apps (interactive UI rendered in conversation) ([source][mcp-apps]).

## Architecture

```text
User → Interface (desktop/CLI)
         → Agent (interactive loop)
           → Provider (any LLM via configurable backends)
           → Extensions (= MCP servers, built-in + external)
             → Tools (MCP tool calls)
```

### Six-Step Agent Loop

1. **Human request** → agent
2. **Provider chat** → sends request + available tools to LLM
3. **Model extension call** → LLM returns tool call (JSON)
4. **Goose executes** → runs tool, gathers results
5. **Context revision** → summarizes/deletes outdated content for token efficiency
6. **Model response** → final output or loop back to step 2

Errors are sent back to the model as tool responses — the LLM self-corrects rather than breaking execution ([source][arch]).

### ACP (Agent Client Protocol)

Goose implements ACP bidirectionally:

- **As server**: `goose acp` over stdio — enables IDE integration (JetBrains, Zed)
- **As client**: delegates to external ACP agents, passing extensions as MCP servers

This is comparable to CC's WebSocket IDE protocol but uses a different standard ([source][arch]).

## Comparison with CC

| Aspect | Claude Code | Goose |
|--------|------------|-------|
| MCP role | Consumer (MCP bridge since v2.1.46) | Co-creator and reference implementation |
| LLM | Anthropic-only (Opus/Sonnet/Haiku) | Any provider (multi-model routing) |
| Extensions | Plugins + MCP servers (separate systems) | Extensions = MCP servers (unified) |
| IDE protocol | WebSocket JSON-RPC 2.0 (proprietary) | ACP (open standard) |
| License | Proprietary | Apache-2.0 |
| Context management | Prompt caching + compaction | Context revision (summarize + delete) |
| MCP Apps | Not supported | Reference client |
| Language | TypeScript (Bun) | Rust + TypeScript |

## Relevance to qte77

- **MCP research**: Goose is the canonical example of ground-up MCP-native design — compare with CC's bolt-on MCP bridge for protocol design insights
- **Plugin architecture**: Goose's "extension = MCP server" unification is what CC's plugin system may converge toward
- **ACP**: emerging protocol for agent-to-agent and agent-to-IDE communication — track alongside CC's WebSocket protocol

## Sources

| Source | Content |
|---|---|
| [block/goose][repo] | Repository, architecture docs |
| [Goose Architecture][arch] | Agent loop, extensions, MCP integration |
| [Arcade: Goose shaped MCP][arcade-origin] | MCP co-development history |
| [AAIF announcement][aaif] | Linux Foundation founding with MCP + Goose + AGENTS.md |
| [MCP Apps blog][mcp-apps] | Goose as reference MCP Apps client |

[repo]: https://github.com/block/goose
[arch]: https://block.github.io/goose/
[arcade-origin]: https://www.arcade.dev/blog/goose-the-open-source-agent-that-shaped-mcp
[aaif]: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
[mcp-apps]: https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/
