---
title: Office Worker Workflows & Multi-Agent Orchestration
description: End-to-end office workflow patterns (invoices, documents, email, financial reporting) and multi-agent orchestrators (Vibe Kanban, Conductor, tmux tools) for parallel business task execution.
created: 2026-03-26
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Research (2026-03-26)

## Summary

Claude can handle typical office workflows — invoice processing, document generation, email triage, financial reporting — through a combination of document skills, business MCP servers, and multi-agent orchestration. This doc maps the end-to-end patterns and the orchestration tools that enable parallel execution across business functions.

## Office Workflow Patterns

### Invoice & Receipt Processing

```text
Receipt images/PDFs → Claude OCR → Excel spreadsheet → Accounting API (Xero/QB)
```

- **Input**: Scanned receipts, invoice PDFs, mixed formats
- **Processing**: Claude for Excel extracts amounts/dates/vendor names, populates spreadsheets with formulas
- **Validation**: Flags duplicate invoice numbers, inconsistent payment terms, budget overruns
- **Output**: Tax-ready organized records pushed to accounting system
- **Tools**: Built-in `xlsx`/`pdf` skills + [Xero MCP](../cc-native/plugins-ecosystem/CC-business-api-integrations.md#xero-official-xeroapi) or [QuickBooks MCP](../cc-native/plugins-ecosystem/CC-business-api-integrations.md#quickbooks)
- **Reference**: [Cowork invoice processing](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)

### Document Renaming & Organization

```text
Chaotic folder → Content-aware analysis → YYYY-MM-DD taxonomy → Organized archive
```

- **Pattern**: Claude reads document content (not just filenames), classifies by type, applies consistent naming
- **Example**: 247 chaotic invoice files → tax-ready order with date-based naming
- **Tools**: CC CLI file operations or Cowork drag-and-drop
- **Scheduling**: [Cowork scheduled tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork) — set hourly/daily/weekly cleanup cadence (no monthly option)

### Email Triage

```text
Gmail/Outlook (read) → Categorize → Draft responses → Flag priorities
```

- **Read**: M365 connector (Outlook) or Gmail connector for thread analysis
- **Write status**: Built-in connectors have partial write support, not read-only. The [Gmail/Google Workspace connector](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors) creates drafts but cannot send emails. The [Microsoft 365 connector](https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector) has optional write tools (send email, manage drafts/calendar events, update mailbox settings, create/update OneDrive/SharePoint files) — a mid-2026 rollout, off by default and admin-enabled. For full send capability today, use [Google Workspace MCP](../cc-native/plugins-ecosystem/CC-business-api-integrations.md#google-workspace-mcp-community-most-complete) (write-capable)
- **Pattern**: Categorize by urgency, draft responses for review, identify newsletters for unsubscription

### Financial Reporting

```text
QuickBooks/Xero MCP → P&L + Balance Sheet → Excel modeling → PowerPoint deck
```

- **Data pull**: Accounting MCP server retrieves financial data
- **Analysis**: Claude for Excel performs variance analysis, reconciliation
- **Presentation**: Claude for PowerPoint generates brand-consistent deck with shared Excel context (Mar 2026+)
- **Tools**: [Business API integrations](../cc-native/plugins-ecosystem/CC-business-api-integrations.md) + [Excel/PowerPoint add-ins](../cc-native/plugins-ecosystem/CC-connectors-overview.md#claude-for-excel-add-in)

### Offer & Contract Generation

```text
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
| **Vibe Kanban** | Local (was web) | CC, Codex, Gemini CLI, GitHub Copilot, Amp, Cursor, OpenCode, Droid, CCR, Qwen Code (10+) | Plan→Prompt→Review, kanban board, git worktrees, QA browser. **Sunsetting** — Bloop shut down 2026-04-10; Apache-2.0, local-only | [vibekanban.com](https://www.vibekanban.com/) |
| **CC Agent Teams** | Native | CC only | CC v2.1.179+ (experimental, opt-in via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) — parallel teammates, in-process display by default (tmux/iTerm2 split panes opt-in via `teammateMode`) | [code.claude.com](https://code.claude.com/docs/en/agent-teams) |
| **Conductor** | macOS app | CC, Codex | Isolated workspaces per agent, review before merge. Used by Linear, Vercel, Stripe | [conductor.build](https://conductor.build) |
| **claude-tmux** | OSS TUI | CC | Manage multiple CC sessions in tmux with git worktree and PR support | [nielsgroen/claude-tmux](https://github.com/nielsgroen/claude-tmux) |
| **claude-session-driver** | OSS | CC | Launch, control, monitor CC sessions as workers. Fan-out, pipeline, supervise patterns | [obra/claude-session-driver](https://github.com/obra/claude-session-driver) |
| **Tmux-Orchestrator** | OSS | CC | 24/7 autonomous agents with self-scheduled check-ins, multi-project coordination | [Jedward23/Tmux-Orchestrator](https://github.com/Jedward23/Tmux-Orchestrator) |
| **claude-conductor** | OSS | CC | Multi-agent via `claude -p` in tmux with MCP server integration (filesystem, Slack, Atlassian) | [lancejames221b/claude-conductor](https://github.com/lancejames221b/claude-conductor) |

*Naming note: several agent-management surfaces adopt cockpit / "command center" / "HUD" framing — see the [Agent Control-Surface Naming landscape](../non-cc/ag-ui-protocol-landscape.md#agent-control-surface-naming-2026) for the verified taxonomy and the live-generative-UI gap.*

### Vibe Kanban (Sunsetting — Apache-2.0, ~27k stars)

**Status update (2026-06-20):** Bloop AI announced its shutdown on **2026-04-10** (in the [v0.1.42 release notes][vk-releases], which link to the project's shutdown post). The repo stays at [`BloopAI/vibe-kanban`][vk-repo] under **Apache-2.0** (not archived); a community edition is under discussion but not yet an established fork. Last release: v0.1.44 (2026-04-24). Hosted remote services were discontinued ~30 days post-announcement → **use as a local self-hosted tool only**. Earlier "30K+ users / 100K+ PRs" figures are unverifiable; GitHub shows ~27 k stars and ~2,400 PRs.

Still the most agent-agnostic option (10+ agents). Differentiators (Rust + React/Axum):

- **Plan→Prompt→Review** workflow with built-in issue tracker
- **Git worktree automation**: isolated environment per agent/task/attempt
- **"Attempts"**: multiple independent agent runs per task in separate worktrees, with **manual** human selection of the best (functionally Best-of-N, but not automated)
- **MCP client + server**: connects to external MCP servers and exposes itself as one
- **Built-in QA browser** + code-review interface
- Install: `npx vibe-kanban`

**Business workflow fit**: the kanban-board → agent-dispatch → human-review architecture still maps cleanly to office-task parallelism, but factor in the sunsetting status before adopting.

### Business Task Session Pattern

```text
tmux session 1: /rename invoices    → CC + pdf skill + Xero MCP
tmux session 2: /rename offers      → CC + docx skill + CRM MCP
tmux session 3: /rename mails       → CC + Gmail MCP (read) + Google Workspace MCP (write)
tmux session 4: /financial-report   → CC + xlsx skill + QuickBooks MCP + pptx skill
```

Each session gets its own Claude Code instance with task-specific MCP servers configured. Sessions survive disconnect (tmux persistence), giving business task continuity across the workday.

**Implementation options**:

- **Simplest**: CC Agent Teams (native, zero setup)
- **Most flexible**: claude-session-driver (fan-out pattern, programmatic control)
- **Most visual**: Vibe Kanban (kanban board, agent-agnostic) — note: sunsetting, local-only
- **Most persistent**: Tmux-Orchestrator (24/7, self-scheduling)

## Non-CC Outlook (Future)

CC-first for high ROI MVP, but these extend the pattern:

- **Vibe Kanban**: Already agent-agnostic — swap CC for Cursor/Gemini/Copilot per task (now community/local-only after Bloop's 2026-04-10 shutdown)
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
| [BloopAI/vibe-kanban repo][vk-repo] | Apache-2.0 repo (~27k stars, Rust+React, MCP client/server, "Attempts") |
| [Vibe Kanban releases][vk-releases] | v0.1.42 shutdown announcement (2026-04-10); v0.1.44 last release |
| [Conductor][conductor] | Multi-agent orchestration platform |
| [claude-tmux][tmux] | Tmux-based parallel CC sessions |
| [claude-session-driver][driver] | Session lifecycle management |
| [Tmux-Orchestrator][orch] | Tmux orchestration for CC |
| [claude-conductor][cc-conductor] | Multi-agent conductor |
| [CC agent teams docs][teams] | Official agent teams documentation |
| [Cowork getting started][cowork] | Cowork onboarding guide |
| [Cowork scheduled tasks][cowork-sched] | Recurring task scheduling |
| [Google Workspace connectors][gw-connectors] | Gmail/Calendar/Drive connector setup (drafts only, no send) |
| [Microsoft 365 connector][m365] | M365 connector setup (optional write tools, admin opt-in) |

[vk]: https://www.vibekanban.com/
[vk-repo]: https://github.com/BloopAI/vibe-kanban
[vk-releases]: https://github.com/BloopAI/vibe-kanban/releases
[conductor]: https://conductor.build
[tmux]: https://github.com/nielsgroen/claude-tmux
[driver]: https://github.com/obra/claude-session-driver
[orch]: https://github.com/Jedward23/Tmux-Orchestrator
[cc-conductor]: https://github.com/lancejames221b/claude-conductor
[teams]: https://code.claude.com/docs/en/agent-teams
[cowork]: https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
[cowork-sched]: https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork
[gw-connectors]: https://support.claude.com/en/articles/10166901-use-google-workspace-connectors
[m365]: https://support.claude.com/en/articles/12542951-set-up-the-microsoft-365-connector
