---
title: GoClaw Multi-Tenant Agent Gateway Analysis
source: https://github.com/nextlevelbuilder/goclaw
purpose: Analysis of GoClaw as a multi-tenant AI agent platform with 8-stage execution pipeline and multi-channel messaging.
platform_scope: [telegram, discord, slack, zalo, feishu, whatsapp]
created: 2026-04-09
updated: 2026-04-09
validated_links: 2026-04-09
---

**Status**: Open-source (CC BY-NC 4.0), active development

## What It Is

GoClaw is a **multi-tenant AI agent platform** built in Go — a single binary
(~25 MB) that unifies 20+ LLM providers, 7 messaging channels, and 30+ built-in
tools with strict security boundaries between users. Self-described as *"OpenClaw
rebuilt in Go — with multi-tenant isolation, 5-layer security, and native
concurrency."*

**Key distinction**: Unlike single-user coding agents (CC, Goose) or research
agents (Feynman), GoClaw is a **deployment platform** for agent teams at scale
across messaging channels.

## Core Architecture

### 8-Stage Execution Pipeline

```
Context → History → Prompt → Think → Act → Observe → Memory → Summarize
```

All stages execute on every request; stages are pluggable.

### 3-Tier Memory System

| Tier | Purpose |
|------|---------|
| **Working** | Active conversation context |
| **Episodic** | Session summaries and key events |
| **Semantic** | Knowledge graphs with progressive loading |

### Provider Support (20+)

Anthropic (native HTTP + prompt caching), OpenAI, OpenRouter, Groq, DeepSeek,
Gemini, and OpenAI-compatible endpoints.

### Messaging Channels (7)

Telegram, Discord, Slack, Zalo OA/Personal, Feishu/Lark, WhatsApp.

### Built-in Tools (30+)

Filesystem, shell execution, browser automation, web search, memory/knowledge
graph access, media generation, skill management, team orchestration, scheduling.

## Deployment

- **Docker**: `docker compose pull && docker compose up -d`
- **Source**: `make build && ./goclaw onboard`
- **Desktop (Lite)**: macOS/Windows installers

## Adoption Decision

| Dimension | Assessment |
|-----------|------------|
| **Use case** | Multi-tenant agent deployment across messaging channels |
| **Language** | Go (single binary, ~25 MB) |
| **Multi-tenancy** | 5-layer security isolation |
| **Maturity** | Active (2.4K stars) |
| **License** | CC BY-NC 4.0 (non-commercial) |

**Strengths**: Single-binary deployment. Broadest messaging channel support in
this survey. Native Go concurrency for multi-tenant workloads. 8-stage pipeline
provides clear execution model. Anthropic prompt caching support.

**Risks**: CC BY-NC 4.0 license prohibits commercial use without separate
agreement. Successor to OpenClaw — migration path unclear. Smaller community
than alternatives (2.4K stars vs Hermes 43K).

## Cross-References

- [hermes-agent-analysis.md](hermes-agent-analysis.md) — also multi-platform agent with messaging channels
- [deerflow-analysis.md](deerflow-analysis.md) — general-purpose agent harness (different deployment model)

## Sources

| Source | Content |
|---|---|
| [GoClaw repo][goclaw] | Multi-tenant agent platform (2.4K stars) |
| [GoClaw docs][goclaw-docs] | Platform documentation |

[goclaw]: https://github.com/nextlevelbuilder/goclaw
[goclaw-docs]: https://docs.goclaw.sh
