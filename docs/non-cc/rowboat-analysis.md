---
title: Rowboat AI Coworker Analysis
source: https://github.com/rowboatlabs/rowboat
purpose: Analysis of Rowboat as a local-first AI coworker building long-lived knowledge graphs from communications.
created: 2026-04-09
updated: 2026-04-09
validated_links: 2026-04-09
---

**Status**: Open-source (Apache-2.0), active development by [Rowboat Labs][rowboat-site]

## What It Is

Rowboat is a **local-first AI coworker** that connects to communications (Gmail,
Google Calendar, meeting notes) and automatically builds a long-lived knowledge
graph. It produces actionable artifacts — PDF decks, email drafts, meeting
briefs — from the accumulated context. All data stored as plain Markdown in an
Obsidian-compatible vault.

**Key distinction**: Unlike coding agents (CC, Goose, DeerFlow) or research
agents (Feynman), Rowboat targets **knowledge work** — tracking people,
companies, topics across communications and producing business artifacts.

## Core Architecture

```
Communication Sources (Gmail, Calendar, Meetings)
  → Ingestion & Entity Extraction
    → Knowledge Graph (Markdown + backlinks)
      → Artifact Generation (PDFs, emails, briefs)
```

### Storage Model

- **Format**: Plain Markdown files with backlinks (Obsidian-compatible)
- **Philosophy**: No proprietary formats, no cloud lock-in
- **Transparency**: Knowledge graph doubles as human-readable "working memory"

### Integrations

| Category | Services |
|----------|----------|
| **Communication** | Gmail, Google Calendar |
| **Meeting notes** | Fireflies |
| **Web search** | Exa |
| **Tools library** | Composio |
| **MCP servers** | Twitter/X, Slack, Linear, GitHub, ElevenLabs |
| **Voice input** | Deepgram API |
| **Voice output** | ElevenLabs API |

### Model Flexibility

Works with local models (Ollama, LM Studio) or hosted APIs. Model-swappable
without data migration — knowledge graph is model-independent Markdown.

## Adoption Decision

| Dimension | Assessment |
|-----------|------------|
| **Use case** | Knowledge work: meeting prep, people tracking, artifact generation |
| **Storage** | Obsidian-compatible Markdown vault |
| **Privacy** | Local-first, all data on disk |
| **Platforms** | Mac, Windows, Linux desktop apps |
| **Maturity** | Active (11.1K stars, 1K forks) |
| **License** | Apache-2.0 |
| **Stack** | TypeScript (96.7%) |

**Strengths**: Largest community in the knowledge-work agent space (11.1K stars).
Obsidian compatibility means no vendor lock-in. MCP support for extensibility.
Local model support (Ollama) for fully offline operation.

**Risks**: Not a coding agent — different use case than most entries in this
survey. Desktop-app distribution (no headless/CI mode documented). Integration
depth with each service may vary.

## Cross-References

- [karpathy-llm-kb-analysis.md](karpathy-llm-kb-analysis.md) — markdown-first knowledge management (different approach)
- [openviking-analysis.md](openviking-analysis.md) — filesystem-based context DB (structural similarity)

## Sources

| Source | Content |
|---|---|
| [Rowboat repo][rowboat] | Open-source AI coworker (11.1K stars) |
| [Rowboat Labs][rowboat-site] | Company site and downloads |

[rowboat]: https://github.com/rowboatlabs/rowboat
[rowboat-site]: https://www.rowboatlabs.com
