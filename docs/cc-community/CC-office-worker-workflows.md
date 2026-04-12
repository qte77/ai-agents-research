---
title: Office Worker Workflows & Multi-Agent Orchestration
description: End-to-end office workflow patterns (invoices, documents, email, financial reporting) and multi-agent orchestrators (Vibe Kanban, Conductor, tmux tools) for parallel business task execution.
created: 2026-03-26
updated: 2026-03-26
validated_links: 2026-03-26
---

**Status**: Research (2026-03-26)

## Summary

Claude can handle typical office workflows — invoice processing, document generation, email triage, financial reporting — through a combination of document skills, business MCP servers, and multi-agent orchestration. This doc maps the end-to-end patterns and the orchestration tools that enable parallel execution across business functions.

## Office Workflow Patterns

### Invoice & Receipt Processing

```
Receipt images/PDFs → Claude OCR → Excel spreadsheet → Accounting API (Xero/QB)
```

- **Input**: Scanned receipts, invoice PDFs, mixed formats
- **Processing**: Claude for Excel extracts amounts/dates/vendor names, populates spreadsheets with formulas
- **Validation**: Flags duplicate invoice numbers, inconsistent payment terms, budget overruns
- **Output**: Tax-ready organized records pushed to accounting system
- **Tools**: Built-in `xlsx`/`pdf` skills + [Xero MCP](../cc-native/plugins-ecosystem/CC-business-api-integrations.md#xero-official-xeroapi) or [QuickBooks MCP](../cc-native/plugins-ecosystem/CC-business-api-integrations.md#quickbooks)
- **Reference**: [Cowork invoice processing](https://support.claude.com/en/articles/13345190-get-started-with-cowork)

### Document Renaming & Organization

```
Chaotic folder → Content-aware analysis → YYYY-MM-DD taxonomy → Organized archive
```

- **Pattern**: Claude reads document content (not just filenames), classifies by type, applies consistent naming
- **Example**: 247 chaotic invoice files → tax-ready order with date-based naming
- **Tools**: CC CLI file operations or Cowork drag-and-drop
- **Scheduling**: [Cowork scheduled tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-cowork) — set weekly/monthly cleanup cadence

### Email Triage

```
Gmail/Outlook (read) → Categorize → Draft responses → Flag priorities
```

- **Read**: M365 connector (Outlook) or Gmail connector for thread analysis
- **Write gap**: Built-in connectors are read-only. For send/draft, use [Google Workspace MCP](../cc-native/plugins-ecosystem/CC-business-api-integrations.md#google-workspace-mcp-community-most-complete) (write-capable)
- **Pattern**: Categorize by urgency, draft responses for review, identify newsletters for unsubscription

### Financial Reporting

```
QuickBooks/Xero MCP → P&L + Balance Sheet → Excel modeling → PowerPoint deck
```

- **Data pull**: Accounting MCP server retrieves financial data
- **Analysis**: Claude for Excel performs variance analysis, reconciliation
- **Presentation**: Claude for PowerPoint generates brand-consistent deck with shared Excel context (Mar 2026+)
- **Tools**: [Business API integrations](../cc-native/plugins-ecosystem/CC-business-api-integrations.md) + [Excel/PowerPoint add-ins](../cc-native/plugins-ecosystem/CC-connectors-overview.md#claude-for-excel-add-in)

### Offer & Contract Generation

```
Template (docx) → Client data (CRM) → Populated document → PDF export
```

- **Template**: `docx` skill with tracked changes for legal review
- **Data**: HubSpot or Salesforce MCP for client details
- **Output**: `pdf` skill for final export
- **Tools**: [Document skills](../cc-native/plugins-ecosystem/CC-office-document-skills.md) + [CRM integrations](../cc-native/plugins-ecosystem/CC-business-api-integrations.md#crm)

## Multi-Agent Orchestration for Office Tasks

The `/rename invoices`, `/rename offers`, `/rename mails` pattern — dedicated agents per business function running in parallel.

### Orchestrator Landscape

| Tool | Type | Agents Supported | Key Capability | URL |
|------|------|-----------------|----------------|-----|
| **Vibe Kanban** | Web platform | CC + Cursor, Gemini, Copilot, Aider, Amp, OpenCode, ChatGPT, Windsurf | Plan→Prompt→Review with kanban board, git worktrees, QA browser | [vibekanban.com](https://www.vibekanban.com/) |
| **CC Agent Teams** | Native | CC only | Shift+Tab lead agent + parallel teammates in tmux panes | [code.claude.com](https://code.claude.com/docs/en/agent-teams) |
| **Conductor** | macOS app | CC, Codex | Isolated workspaces per agent, review before merge. Used by Linear, Vercel, Stripe | [conductor.build](https://conductor.build) |
| **claude-tmux** | OSS TUI | CC | Manage multiple CC sessions in tmux with git worktree and PR support | [nielsgroen/claude-tmux](https://github.com/nielsgroen/claude-tmux) |
| **claude-session-driver** | OSS | CC | Launch, control, monitor CC sessions as workers. Fan-out, pipeline, supervise patterns | [obra/claude-session-driver](https://github.com/obra/claude-session-driver) |
| **Tmux-Orchestrator** | OSS | CC | 24/7 autonomous agents with self-scheduled check-ins, multi-project coordination | [Jedward23/Tmux-Orchestrator](https://github.com/Jedward23/Tmux-Orchestrator) |
| **claude-conductor** | OSS | CC | Multi-agent via `claude -p` in tmux with MCP server integration (filesystem, Slack, Atlassian) | [lancejames221b/claude-conductor](https://github.com/lancejames221b/claude-conductor) |

### Vibe Kanban (30K+ Users, 100K+ PRs)

Most agent-agnostic option. 9 coding agents supported. Key differentiators:

- **Plan→Prompt→Review** workflow with built-in issue tracker
- **Git worktree automation**: Isolated environments per agent/task
- **Built-in QA browser**: Test outputs within the platform
- **Code review interface**: Comment on agent-generated changes
- Install: `npx vibe-kanban`

**Business workflow fit**: The Plan→Prompt→Review cycle and parallel agent dispatch pattern applies directly to office task parallelism. Currently dev-focused, but the architecture (kanban board → agent dispatch → human review) is the exact pattern needed for dedicated business function sessions.

### Business Task Session Pattern

```
tmux session 1: /rename invoices    → CC + pdf skill + Xero MCP
tmux session 2: /rename offers      → CC + docx skill + CRM MCP
tmux session 3: /rename mails       → CC + Gmail MCP (read) + Google Workspace MCP (write)
tmux session 4: /financial-report   → CC + xlsx skill + QuickBooks MCP + pptx skill
```

Each session gets its own Claude Code instance with task-specific MCP servers configured. Sessions survive disconnect (tmux persistence), giving business task continuity across the workday.

**Implementation options**:

- **Simplest**: CC Agent Teams (native, zero setup)
- **Most flexible**: claude-session-driver (fan-out pattern, programmatic control)
- **Most visual**: Vibe Kanban (kanban board, agent-agnostic)
- **Most persistent**: Tmux-Orchestrator (24/7, self-scheduling)

## Non-CC Outlook (Future)

CC-first for high ROI MVP, but these extend the pattern:

- **Vibe Kanban**: Already agent-agnostic — swap CC for Cursor/Gemini/Copilot per task
- **n8n**: Open-source workflow automation with MCP server support
- **Zapier / Make**: Low-code automation with Claude API integration
- **Microsoft Copilot**: Native M365 integration (competing approach for Excel/PowerPoint)
- **Google Gemini**: Workspace integration

## Cross-References

- [CC-office-document-skills.md](../cc-native/plugins-ecosystem/CC-office-document-skills.md) — Document skills ecosystem (4 layers)
- [CC-business-api-integrations.md](../cc-native/plugins-ecosystem/CC-business-api-integrations.md) — Business MCP servers (payments, accounting, CRM, ERP)
- [CC-connectors-overview.md](../cc-native/plugins-ecosystem/CC-connectors-overview.md) — Built-in connectors and Office add-ins
- [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) — RTK, Pilot Shell, ruflo
- [CC-community-skills-landscape.md](CC-community-skills-landscape.md) — Skill libraries and organizational frameworks

## Sources

| Source | Content |
|---|---|
| [Vibe Kanban][vk] | Agent-agnostic project management |
| [Conductor][conductor] | Multi-agent orchestration platform |
| [claude-tmux][tmux] | Tmux-based parallel CC sessions |
| [claude-session-driver][driver] | Session lifecycle management |
| [Tmux-Orchestrator][orch] | Tmux orchestration for CC |
| [claude-conductor][cc-conductor] | Multi-agent conductor |
| [CC agent teams docs][teams] | Official agent teams documentation |
| [Cowork getting started][cowork] | Cowork onboarding guide |
| [Cowork scheduled tasks][cowork-sched] | Recurring task scheduling |

[vk]: https://www.vibekanban.com/
[conductor]: https://conductor.build
[tmux]: https://github.com/nielsgroen/claude-tmux
[driver]: https://github.com/obra/claude-session-driver
[orch]: https://github.com/Jedward23/Tmux-Orchestrator
[cc-conductor]: https://github.com/lancejames221b/claude-conductor
[teams]: https://code.claude.com/docs/en/agent-teams
[cowork]: https://support.claude.com/en/articles/13345190-get-started-with-cowork
[cowork-sched]: https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-cowork
