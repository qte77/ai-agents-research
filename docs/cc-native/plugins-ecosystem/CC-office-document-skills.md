---
title: Office Document Skills & MCP Servers
description: Ecosystem analysis of document generation/manipulation capabilities — Anthropic official skills, knowledge-work plugins, community skills, and MCP servers for docx, xlsx, pptx, and pdf.
created: 2026-03-26
updated: 2026-03-26
validated_links: 2026-03-26
---

**Status**: Research (2026-03-26)

## Summary

Four layers of document handling are available for Claude workflows: Anthropic's built-in document skills (docx/xlsx/pptx/pdf), Anthropic's knowledge-work plugins (11 business domain plugins), community CC skills (OOXML editing, batch processing), and standalone MCP servers for direct file manipulation. Together they cover the full office document lifecycle.

## Layer 1: Anthropic Built-in Document Skills

**Source**: [anthropics/skills](https://github.com/anthropics/skills) (source-available, 2026-03-26)

These are the production skills powering Claude.ai, Cowork, and the Skills API. Documented in detail in [CC-cowork-skills-api-workflows.md](CC-cowork-skills-api-workflows.md#anthropic-document-skill-capabilities-2026-03-26).

| Skill | Create | Edit | Read | Key Capabilities |
|-------|--------|------|------|-----------------|
| `docx` | Yes | Yes | Yes | Tracked changes, redlining, comments, OOXML, templates |
| `xlsx` | Yes | Yes | Yes | Formulas, data validation, conditional formatting, pivots |
| `pptx` | Yes | Yes | Yes | Template-aware generation (slide masters), OOXML, thumbnails |
| `pdf` | Yes | Limited | Yes | Form filling, merging, extraction. No full content editing |

**Access**: Skills API (`/v1/skills`), Cowork, Claude.ai. Max 8 skills per request. Models: Sonnet 4.6, Opus 4.6.

## Layer 2: Anthropic Knowledge-Work Plugins

**Source**: [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (2026-03-26)

11 official open-source plugins for business domain workflows:

| Plugin | Domain | Office-Relevant Capabilities |
|--------|--------|------------------------------|
| **Finance** | Accounting, reporting | Journal entries, reconciliation, financial statements, variance analysis |
| **HR** | People ops | Offer letters, onboarding docs, performance reviews, compensation analysis |
| **Sales** | CRM, pipeline | Proposals, battlecards, pipeline reports |
| **Operations** | Process management | SOPs, process documentation, workflow templates |
| **Productivity** | Communication | Aggregates Slack, Notion, GitHub context |
| **Design** | Creative | Design briefs, asset specifications |
| **Engineering** | Development | Technical specs, architecture docs |
| **Enterprise Search** | Knowledge | Cross-platform document search |
| **Plugin Create** | Meta | Build custom plugins |
| **Plugin Customize** | Meta | Extend existing plugins |
| **Investment Banking** | Finance (specialized) | Financial modeling, deal documentation |

**Key insight**: These plugins combine document skills with domain expertise — the Finance plugin doesn't just create spreadsheets, it knows accounting conventions (journal entry format, P&L structure, reconciliation workflows).

## Layer 3: Community CC Skills

### claude-office-skills (tfriedel)

**Repo**: [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) (2026-03-26)

CC-native SKILL.md files for office document workflows. Mirrors the Anthropic skills pattern with added capabilities:

- OOXML editing (direct XML manipulation for precise formatting)
- Tracked changes and redlining
- Batch processing (multiple documents in sequence)
- Database-driven report generation
- CI/CD pipeline integration (automated document generation in builds)
- Python/JS validation scripts

### jezweb/claude-skills

Pure-JS library approach (`docx`, SheetJS, `pdf-lib`, `pptxgenjs`) for invoices, reports, spreadsheets. Works in Node.js, browsers, and Cloudflare Workers — relevant for serverless document generation.

## Layer 4: MCP Servers for Document Operations

Standalone MCP servers enabling Claude Code (or any MCP client) to manipulate documents programmatically:

| Server | Formats | Key Capability | URL |
|--------|---------|---------------|-----|
| **Office-Word-MCP-Server** | DOCX | Word document creation/editing | [GongRzhe/Office-Word-MCP-Server](https://github.com/GongRzhe/Office-Word-MCP-Server) |
| **docx-mcp** | DOCX + PDF conversion | Word + PDF format conversion | [hongkongkiwi/docx-mcp](https://github.com/hongkongkiwi/docx-mcp) |
| **excel-mcp-server** | XLSX | Read/write with formulas | [negokaz/excel-mcp-server](https://github.com/negokaz/excel-mcp-server) |
| **excel-to-pdf-mcp** | XLSX/Numbers → PDF | LibreOffice-based conversion | [kmexnx/excel-to-pdf-mcp](https://github.com/kmexnx/excel-to-pdf-mcp) |
| **document-edit-mcp** | PDF + Word + Excel | Multi-format CRUD | [alejandroBallesterosC/document-edit-mcp](https://github.com/alejandroBallesterosC/document-edit-mcp) |
| **mcp-server-doccreator** | PDF, DOCX, PPTX, XLSX | Multi-format generation | [Git-Fg/mcp-server-doccreator](https://github.com/Git-Fg/mcp-server-doccreator) |

**When to use MCP servers vs built-in skills**: MCP servers give fine-grained programmatic control (specific API calls for cell operations, page manipulation). Built-in skills provide higher-level natural language interaction ("create an invoice spreadsheet"). Use MCP servers for automation pipelines; use skills for interactive work.

## Adoption Decision

| Use Case | Best Option |
|----------|-------------|
| Interactive document creation in Cowork | Built-in skills (`docx`, `xlsx`, `pptx`, `pdf`) |
| Domain-specific business documents | Knowledge-work plugins (Finance, HR, Sales) |
| CC CLI automation / batch processing | MCP servers + community skills |
| Serverless / CI document generation | jezweb/claude-skills (pure JS, no dependencies) |
| Complex OOXML manipulation | tfriedel/claude-office-skills |

## Cross-References

- [CC-cowork-skills-api-workflows.md](CC-cowork-skills-api-workflows.md) — Skills API endpoints, skill type details, capability table
- [CC-connectors-overview.md](CC-connectors-overview.md) — Claude for Excel/PowerPoint add-ins, M365 connector
- [CC-business-api-integrations.md](CC-business-api-integrations.md) — Business APIs (accounting, CRM, payments) that feed into document workflows
- [CC-office-worker-workflows.md](../../cc-community/CC-office-worker-workflows.md) — End-to-end workflow patterns combining these capabilities

## Sources

<!-- markdownlint-disable MD013 -->

| Source | Content |
|---|---|
| [Anthropic skills][skills] | Official built-in document skills |
| [Knowledge-work plugins][kw] | 11 business domain plugins |
| [claude-office-skills][office] | Community OOXML editing skills |
| [Office-Word-MCP-Server][word] | Word document MCP server |
| [excel-mcp-server][excel] | Excel MCP server |
| [document-edit-mcp][docedit] | Document editing MCP server |
| [mcp-server-doccreator][doccreator] | Multi-format document generator |

<!-- markdownlint-enable MD013 -->

[skills]: https://github.com/anthropics/skills
[kw]: https://github.com/anthropics/knowledge-work-plugins
[office]: https://github.com/tfriedel/claude-office-skills
[word]: https://github.com/GongRzhe/Office-Word-MCP-Server
[excel]: https://github.com/negokaz/excel-mcp-server
[docedit]: https://github.com/alejandroBallesterosC/document-edit-mcp
[doccreator]: https://github.com/Git-Fg/mcp-server-doccreator
