---
title: Rowboat AI Coworker Analysis
source: https://github.com/rowboatlabs/rowboat
purpose: Analysis of Rowboat as a local-first AI coworker building long-lived knowledge graphs from communications.
created: 2026-04-09
updated: 2026-11-26
validated_links_on: 2026-06-22
status: assess
---

**Details:** Open-source (Apache-2.0), active development by [Rowboat Labs][rowboat-site]. Also runs on or integrates with: `desktop`, `ollama`, `mcp-generic`.

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

```text
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
| **Communication** | Gmail, Google Calendar, Google Drive |
| **Meeting notes** | Fireflies (unverified: the current README does not mention it; it describes a built-in meeting note taker) |
| **Web search** | Exa |
| **Tools library** | Composio |
| **MCP servers** | Twitter/X, Slack, Linear/Jira, GitHub, ElevenLabs |
| **Voice input** | Deepgram API |
| **Voice output** | ElevenLabs API |

### Model Flexibility

Works with local models (Ollama, LM Studio) or hosted APIs. Model-swappable
without data migration — knowledge graph is model-independent Markdown.

Despite the GitHub topic tags `claude-code` and `claude-cowork`, there is no
Claude-specific integration surface — model access is via Model Context Protocol (MCP) and bring-your-own
API key, fully model-agnostic. The tags are discovery/categorization only.

## Adoption Decision

| Dimension | Assessment |
|-----------|------------|
| **Use case** | Knowledge work: meeting prep, people tracking, artifact generation |
| **Storage** | Obsidian-compatible Markdown vault |
| **Privacy** | Local-first, all data on disk |
| **Platforms** | Mac, Windows, Linux desktop apps; web (spaces.rowboatlabs.com) and iPhone app (checked 2026-11-26) |
| **Maturity** | Active (about 18K stars, 1.8K forks, checked 2026-11-26) |
| **License** | Apache-2.0 |
| **Stack** | TypeScript (98.0% of bytes, checked 2026-11-26) |

**Strengths**: Largest community in the knowledge-work agent space (about 18K stars, checked 2026-11-26).
Obsidian compatibility means no vendor lock-in. MCP support for extensibility.
Local model support (Ollama) for fully offline operation.

**Risks**: Not a coding agent — different use case than most entries in this
survey. Desktop-app centred distribution (the README now documents a headless `rowboat-server` in `apps/x` and an open-source Harbor Spaces server in `apps/harbor`). Integration
depth with each service may vary.

## Cross-References

- [karpathy-llm-kb-analysis.md](../knowledge-management/karpathy-llm-kb-analysis.md) — markdown-first knowledge management (different approach)
- [openviking-analysis.md](../context-memory/openviking-analysis.md) — filesystem-based context DB (structural similarity)

## Sources

| Source | Content |
|---|---|
| [Rowboat repo][rowboat] | Open-source AI coworker (about 18K stars, checked 2026-11-26) |
| [Rowboat Labs][rowboat-site] | Company site and downloads |

[rowboat]: https://github.com/rowboatlabs/rowboat
[rowboat-site]: https://www.rowboatlabs.com
