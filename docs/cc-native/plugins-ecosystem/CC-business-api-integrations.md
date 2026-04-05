---
title: Business API & MCP Server Integrations
description: Landscape of business-oriented MCP servers for Claude Code — payments, accounting, CRM, ERP, legal/IP, and universal hubs. First-party and official sources prioritized.
created: 2026-03-26
updated: 2026-03-26
validated_links: 2026-03-26
---

**Status**: Research (2026-03-26)

## Summary

20+ business MCP servers are available for Claude Code, covering payments, accounting, CRM, ERP, productivity, and legal/IP domains. Three are official first-party servers (Stripe, HubSpot, Oracle NetSuite); one is from the vendor's official GitHub org (Xero). Composio provides a universal hub covering 850+ apps.

## Payments

### Stripe (Official)

**Source**: Official hosted MCP server | **URL**: `https://mcp.stripe.com` (2026-03-26)

```bash
claude mcp add --transport http stripe https://mcp.stripe.com
```

- Create customers, manage subscriptions, issue refunds
- Generate invoices, confirm payment intents
- Query transaction history, balance, payouts
- Configuration storable in `.mcp.json` (team-shareable via version control)

## Accounting

### Xero (Official XeroAPI)

**Source**: [XeroAPI/xero-mcp-server](https://github.com/XeroAPI/xero-mcp-server) | [Glama listing](https://glama.ai/mcp/servers/XeroAPI/xero-mcp-server) (2026-03-26)

- Retrieve contacts, manage connections, update invoices, monitor quotes
- PDF invoice parsing to Xero bill creation fields
- Conversational accounting queries ("Will I have enough cash to pay vendors next week?")
- Auth: OAuth 2.0

### QuickBooks

**Source**: [laf-rge/quickbooks-mcp](https://github.com/laf-rge/quickbooks-mcp) (community, 2026-03-26)

- Query, create, edit QuickBooks Online data
- Pull P&L, Balance Sheet, Trial Balance by month/department/class
- All write operations default to draft/preview mode before committing
- Auth: OAuth 2.0

**Intuit + Anthropic Partnership** (Feb 2026): TurboTax, Credit Karma, QuickBooks, and Mailchimp will be surfaced inside Anthropic products via MCP. Rolling out spring 2026. ([Intuit investor announcement](https://investors.intuit.com/news-events/press-releases/detail/1305/intuit-and-anthropic-partner-to-bring-trusted-financial-intelligence-and-custom-ai-agents-to-consumers-and-businesses))

### FreshBooks

**Source**: [roboulos/freshbooks-mcp](https://github.com/roboulos/freshbooks-mcp) (community, 2026-03-26)

- Invoicing and time tracking automation
- Auth: OAuth 2.0

### Accountable

No public MCP server found (2026-03-26). Accountable is a German freelancer accounting app — potential gap for European freelancer use cases.

## CRM

### HubSpot (Official)

**Source**: [developers.hubspot.com/mcp](https://developers.hubspot.com/mcp) (2026-03-26)

- Setup: `hs mcp setup` (HubSpot CLI v7.60.0+)
- Currently **read-only**: summaries, trends, associations, pipeline snapshots
- Auth: OAuth 2.0 (OAuth 2.1 support planned)

### Salesforce

**Source**: [Composio Salesforce](https://composio.dev/toolkits/salesforce/framework/claude-code) (2026-03-26)

- Full CRUD: contacts, opportunities, campaigns, accounts
- Enterprise, Unlimited, and Developer editions
- Salesforce's own native hosted MCP server still in beta (2026-03-26)
- Auth: OAuth 2.0

## ERP

### Oracle NetSuite (Official)

**Source**: [netsuite.com AI Connector](https://www.netsuite.com/portal/products/artificial-intelligence-ai/mcp-server.shtml) | [Oracle Developer Blog](https://blogs.oracle.com/developers/talking-to-your-erp-netsuite-meets-claude-via-mcp) (2026-03-26)

- MCP Standard Tools SuiteApp: 9 tools (`runSuiteQL`, `getCustomer`, `updateRecord`, etc.)
- Bring-your-own-AI model (Claude, ChatGPT, or custom LLM)
- Auth: OAuth 2.0 + PKCE
- Launched August 2025

**SAP**: No dedicated MCP server as of 2026-03-26.

## Productivity / Google Workspace

### Google Workspace MCP (Community, Most Complete)

**Source**: [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) (2026-03-26)

- 12 services: Gmail, Calendar, Drive, Docs, Sheets, Slides, Forms, Tasks, Contacts, Chat
- Remote OAuth 2.1 multi-user support
- 1-click Claude installation
- Can be hosted centrally for an organization

### Google Workspace MCP (Commercial)

**Source**: [workspacemcp.com](https://workspacemcp.com) (2026-03-26)

- 12 services, 100+ tools, full CLI for Claude Code/Codex
- Install via `.dxt` file (no JSON editing)

**Note**: These are distinct from the built-in Google connectors in claude.ai (which are read-only). These MCP servers provide **read-write** access.

## Legal / Intellectual Property

### USPTO Patent MCP Server

**Source**: [riemannzeta/patent_mcp_server](https://github.com/riemannzeta/patent_mcp_server) | [PyPI](https://pypi.org/project/patent-mcp-server/) (2026-03-26)

- 51 tools across 6 USPTO data sources
- Patent Public Search, Prosecution History, PTAB Proceedings, Office Actions
- Patent Litigation (74,000+ district court cases), Citation Analysis, Patent Family Data
- Auth: `USPTO_API_KEY` env var

### Patent Connector (patent.dev)

**Source**: [patent.dev](https://patent.dev/patent-connector-mcp-server-for-ai-powered-patent-research/) (open beta, 2026-03-26)

- Claude Desktop and ChatGPT Desktop integration
- USPTO and EPO patent databases
- Natural language patent search

## Universal Hubs

### Composio (850+ Apps)

**Source**: [composio.dev](https://composio.dev) (2026-03-26)

- **Rube** universal MCP server: 850+ SaaS apps including Salesforce, Slack, Notion, QuickBooks, Xero, Google Workspace, Microsoft (Outlook, Teams), GitHub, Figma
- Just-in-time tool loading (keeps LLM context window clean)
- Pre-built workflow skills for 78 SaaS apps

```bash
claude mcp add --transport http composio "<YOUR_MCP_URL>" --headers "X-API-Key:YOUR_COMPOSIO_KEY"
```

### Coupler.io

**Source**: [coupler.io/mcp](https://www.coupler.io/mcp/quickbooks) (2026-03-26)

- Hub integrating QuickBooks, Xero, Stripe, Salesforce, HubSpot, Google Sheets, Microsoft Excel
- Conversational financial analysis across multiple data sources

## Adoption Decision

| Need | Best Option | Why |
|------|-------------|-----|
| Payments/billing | Stripe official MCP | First-party, hosted, zero-setup |
| Accounting (global) | Xero official MCP | First-party XeroAPI, full CRUD |
| Accounting (US) | QuickBooks community MCP | Draft-mode writes, P&L/BS reports |
| CRM | HubSpot official (read) or Composio Salesforce (CRUD) | Depends on vendor |
| ERP | NetSuite official | Only ERP with native MCP |
| Multi-app | Composio Rube | 850+ apps, single setup |
| Legal/IP | USPTO patent_mcp_server | 51 tools, 6 data sources |

## Cross-References

- [CC-connectors-overview.md](CC-connectors-overview.md) — Built-in connectors (Google, M365, GitHub, Slack)
- [CC-office-document-skills.md](CC-office-document-skills.md) — Document generation skills that consume data from these APIs
- [CC-office-worker-workflows.md](../../cc-community/CC-office-worker-workflows.md) — End-to-end workflows combining APIs + document skills

## Sources

| Source | Content |
|---|---|
| [Stripe MCP][stripe] | Official Stripe MCP server |
| [Xero MCP][xero] | Official Xero API MCP server |
| [QuickBooks MCP][qb] | Community QuickBooks integration |
| [HubSpot MCP][hubspot] | Official HubSpot developer MCP |
| [Composio][composio] | Universal 850+ app hub |
| [NetSuite MCP][netsuite] | Official Oracle NetSuite MCP |
| [USPTO patent MCP][patent] | Patent search, 51 tools |

[stripe]: https://mcp.stripe.com
[xero]: https://github.com/XeroAPI/xero-mcp-server
[qb]: https://github.com/laf-rge/quickbooks-mcp
[hubspot]: https://developers.hubspot.com/mcp
[composio]: https://composio.dev
[netsuite]: https://www.netsuite.com/portal/products/artificial-intelligence-ai/mcp-server.shtml
[patent]: https://github.com/riemannzeta/patent_mcp_server
