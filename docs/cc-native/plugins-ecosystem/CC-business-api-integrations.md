---
title: Business API & MCP Server Integrations
description: Landscape of business-oriented MCP servers for Claude Code — payments, accounting, CRM, ERP, legal/IP, and universal hubs. First-party and official sources prioritized.
created: 2026-03-26
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Research (2026-03-26)

## Summary

20+ business MCP servers are available for Claude Code, covering payments, accounting, CRM, ERP, productivity, and legal/IP domains. Three are official first-party servers (Stripe, HubSpot, Oracle NetSuite); one is from the vendor's official GitHub org (Xero). Composio provides a universal hub covering 1,000+ apps.

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

**Source**: [developers.hubspot.com/mcp](https://developers.hubspot.com/mcp) (2026-07-23)

- Setup: `hs mcp setup` (gated on Developer Platform v2025.2)
- Full read/write access to CRM objects (contacts, companies, deals, tickets) and engagements (calls, emails, meetings, notes, tasks); read-only limited to organizational context and marketing content
- Auth: OAuth 2.0 (OAuth 2.1 support planned)

### Salesforce

**Source**: [Composio Salesforce](https://composio.dev/toolkits/salesforce/framework/claude-code) (2026-03-26)

- Full CRUD: contacts, opportunities, campaigns, accounts
- Enterprise, Unlimited, and Developer editions
- Salesforce's own native [Hosted MCP Servers][sf-ga] reached General Availability 2026-04-29 (piloted spring 2025, beta Oct 2025), available to every Enterprise Edition org and above
- Auth: OAuth 2.0

## ERP

### Oracle NetSuite (Official)

**Source**: [netsuite.com AI Connector](https://www.netsuite.com/portal/products/artificial-intelligence-ai/mcp-server.shtml) | [Oracle Developer Blog](https://blogs.oracle.com/developers/talking-to-your-erp-netsuite-meets-claude-via-mcp) | [Oracle NetSuite Help][netsuite-tools] (2026-07-23)

- MCP Standard Tools SuiteApp: 14 tools, all `ns_`-prefixed (`ns_createRecord`, `ns_getRecord`, `ns_getRecordTypeMetadata`, `ns_updateRecord`, `ns_getAccountingBooks`, `ns_getAccountingContexts`, `ns_getNexusIds`, `ns_getSubsidiaries`, `ns_listAllReports`, `ns_runReport`, `ns_listSavedSearches`, `ns_runSavedSearch`, `ns_runCustomSuiteQL`, `ns_getSuiteQLMetadata`) — supersedes the deprecated MCP Sample Tools SuiteApp (discontinued for new installs Sept 2025)
- Bring-your-own-AI model (Claude, ChatGPT, or custom LLM)
- Auth: OAuth 2.0 + PKCE
- Launched August 2025 (2025-08-12)

**SAP**: No dedicated MCP server as of 2026-03-26.

## Productivity / Google Workspace

### Google Workspace MCP (Community, Most Complete)

**Source**: [taylorwilsdon/google_workspace_mcp](https://github.com/taylorwilsdon/google_workspace_mcp) (2026-07-23)

- 12 services: Gmail, Drive, Calendar, Docs, Sheets, Slides, Forms, Chat, Apps Script, Tasks, Contacts, Search
- Remote OAuth 2.1 multi-user support
- 1-click Claude installation
- Can be hosted centrally for an organization

### Google Workspace MCP (Commercial)

**Source**: [workspacemcp.com](https://workspacemcp.com) (2026-07-23)

- 12 services, 100+ tools, full CLI for Claude Code/Codex
- Install via `uvx workspace-mcp`; Claude Desktop uses a `.mcpb` bundle (Anthropic renamed the Desktop Extensions format from `.dxt` to `.mcpb`)

**Note**: These are distinct from the built-in Google connectors in claude.ai (which are read-only). These MCP servers provide **read-write** access.

## Legal / Intellectual Property

### USPTO Patent MCP Server

**Source**: [riemannzeta/patent_mcp_server](https://github.com/riemannzeta/patent_mcp_server) | [PyPI](https://pypi.org/project/patent-mcp-server/) (v1.0.0, released 2026-06-10; checked 2026-07-23)

- 61 tools across 9 USPTO data sources — only 36 tools are currently active; 25 are unavailable due to API shutdowns
- Patent Public Search, Prosecution History, PTAB Proceedings, Office Actions (Office Action/Enriched Citation APIs decommissioned early 2026)
- Patent Litigation (74,000+ district court cases, now bulk-download only — the live API was never on the Open Data Portal), Citation Analysis, Patent Family Data (PatentsView API shut down 2026-03-20)
- Auth: `USPTO_API_KEY` env var

### Patent Connector (patent.dev)

**Source**: [patent.dev](https://patent.dev/patent-connector-mcp-server-for-ai-powered-patent-research/) (open beta, 2026-03-26)

- Claude Desktop and ChatGPT Desktop integration
- USPTO and EPO patent databases
- Natural language patent search

## Universal Hubs

### Composio (1,000+ Apps)

**Source**: [composio.dev](https://composio.dev) | [composio.dev/toolkits][composio-toolkits] (2026-07-23)

- **Rube** universal MCP server: 1,047 toolkits/integrations (site copy: "1,000+ apps") including Salesforce, Slack, Notion, QuickBooks, Xero, Google Workspace, Microsoft (Outlook, Teams), GitHub, Figma
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
| CRM | HubSpot official (read/write) or Composio Salesforce (CRUD) | Depends on vendor |
| ERP | NetSuite official | Only ERP with native MCP |
| Multi-app | Composio Rube | 1,000+ apps, single setup |
| Legal/IP | USPTO patent_mcp_server | 61 tools, 9 data sources (36 active) |

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
| [Composio][composio] / [toolkits][composio-toolkits] | Universal 1,000+ app hub |
| [NetSuite MCP][netsuite] / [tools list][netsuite-tools] | Official Oracle NetSuite MCP |
| [USPTO patent MCP][patent] | Patent search, 61 tools (36 active) |
| [Salesforce Hosted MCP GA][sf-ga] | Salesforce's own hosted MCP server, GA April 2026 |

[stripe]: https://mcp.stripe.com
[xero]: https://github.com/XeroAPI/xero-mcp-server
[qb]: https://github.com/laf-rge/quickbooks-mcp
[hubspot]: https://developers.hubspot.com/mcp
[composio]: https://composio.dev
[composio-toolkits]: https://composio.dev/toolkits
[netsuite]: https://www.netsuite.com/portal/products/artificial-intelligence-ai/mcp-server.shtml
[netsuite-tools]: https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/article_0902023508.html
[patent]: https://github.com/riemannzeta/patent_mcp_server
[sf-ga]: https://developer.salesforce.com/blogs/2026/04/salesforce-hosted-mcp-servers-are-now-generally-available
