---
title: Claude Connectors — MCP-Based Integrations
purpose: Analysis of Claude's connector ecosystem, capabilities, limitations, and platform availability.
created: 2026-03-19
updated: 2026-11-26
validated_links_on: 2026-11-25
status: assess
---

## Claude Connectors Overview

Connectors extend Claude via [MCP (Model Context Protocol)][mcp] — an open standard by Anthropic for AI-to-external-service interaction. They provide tool access (search, read, act) and UI rendering (charts, maps, forms via MCP Apps).

CC version requirements: >=2.1.46 (MCP bridge), >=2.1.63 (opt-out env var), 2.1.71 (OAuth fixes).

## Prebuilt Connectors

| Connector | Read | Write | Plan | Status (unverified) |
|-----------|------|-------|------|--------|
| Google Drive | Docs, Sheets, Slides, PDF, Office, OpenDocument, PNG/JPEG (about 10 MB export cap on Google files) | Creates new files | Pro+ (unverified) | Beta |
| Gmail | Search & read threads | No (can't send/draft) | Pro+ | Beta |
| Google Calendar | Schedule, attendees, conflicts | No (can't create/modify/delete) | Pro+ | Beta |
| GitHub | File names, file contents, branch content | No | All plans | GA |
| Slack | Searches channels, direct messages, files (Claude app must be installed in Slack first) | No (search only; inferred, writes not stated) | Team/Enterprise | Beta |
| Microsoft 365 | SharePoint, OneDrive, Outlook, Teams | Yes (OneDrive/SharePoint files, Outlook mail, drafts and calendar events, Teams messages; admin-controlled) | All plans (work/school accounts need Entra Global Administrator consent; Team/Enterprise: work/school only) | GA |

**Key pattern**: Gmail, Google Calendar and GitHub are **read-only** — Claude can search and answer questions but cannot create, modify, or delete content there. Drive can create new files, and Microsoft 365 has write actions.

## Custom Connector Types

| Type | Hosting | Distribution | Use case |
|------|---------|-------------|----------|
| Remote MCP servers | Cloud | URL | Custom APIs, cloud tools |
| MCP Apps | Cloud | URL | Interactive UI (charts, maps, forms) |
| MCP Bundles (MCPB) | Local | Desktop package | Desktop tools with dependencies |
| Self-serve local MCP | Local | npm/PyPI (plugins) | Developer tools, CLI integrations |

## Platform Availability

| Platform | Remote MCP | Local MCP | MCP Apps | Plugins | claude.ai Connectors |
|----------|-----------|-----------|----------|---------|---------------------|
| Claude.ai | Yes | No | Yes | No | Native |
| Claude Desktop | Yes | Yes | Yes | Yes | Yes |
| Claude Mobile | Yes | No | No | No | Yes |
| Claude Code | Yes | Yes (plugins) | No | Yes | Yes (since v2.1.46) |
| Claude Cowork | Yes | Yes | Yes | Yes | Yes |

### Claude Code MCP Bridge (v2.1.46+)

Since [v2.1.46 (Feb 18, 2026)][cc-changelog], Claude Code automatically surfaces MCP servers configured in claude.ai — including Gmail, Google Drive, and Google Calendar connectors.

**Setup** ([source][cc-mcp-docs]):

1. **Configure in claude.ai**: Go to [claude.ai/settings/connectors](https://claude.ai/settings/connectors) and add Google connectors. Authenticate with your Google account. (Team/Enterprise: admin must enable first.)
2. **Connectors auto-appear in CC**: Start Claude Code and run `/mcp` — claude.ai servers show up with indicators marking their origin. No extra CLI setup needed.
3. **Use naturally**: Ask Claude directly — "search my Gmail for emails about the deploy failure", "what meetings do I have tomorrow", "find the architecture doc in Drive". Gmail, Calendar and GitHub are read-only; Claude searches and answers there but cannot send, create, or modify anything.

**Opt out**: `ENABLE_CLAUDEAI_MCP_SERVERS=false claude` (added in [v2.1.63, Feb 28, 2026][cc-changelog])

**v2.1.71 fixes** (March 7, 2026):

- Fixed startup UI freeze when many connectors refresh OAuth tokens simultaneously
- Fixed connectors failing to reconnect after OAuth token refresh
- Fixed startup notification noise for unauthenticated org connectors
- Removed notification spam for every org-configured connector

## Google Connectors Detail

### Google Drive

- **Supported**: Google Docs, Sheets and Slides, PDF, Word/Excel/PowerPoint, OpenDocument and PNG/JPEG files; can create new files in Drive (checked 2026-11-26)
- **Not supported**: comments and suggested edits
- **Size cap**: about 10 MB applies to Google's export of Docs/Sheets/Slides for files picked into a chat or project; over the cap Claude gets only the name and details. Picked files convert to Markdown (Docs, no images), CSV (Sheets, all tabs) and plain text (Slides)
- **Access**: Permission-mirrored — only docs the user can view
- **Setup**: + then "Add from Google Drive" in chat; in a private project, knowledge section → "Add files" → Google Drive
- **Workaround**: Convert `.docx` to Google Docs via File → Save as Google Docs
- **Reconnect**: on the connector's page under claude.ai/customize/connectors/yours (Reconnect, Disconnect, Remove)

### Gmail

- **Can do**: Search emails, analyze threads, provide citations linking to source
- **Cannot do**: Create, send, or modify emails; view embedded images
- **Access**: Mirrors existing Gmail permissions (specific OAuth scopes undocumented; unverified)

### Google Calendar

- **Can do**: Query schedule, meeting details, attendees, conflict detection, pattern analysis; citations link to original events
- **Cannot do**: Create, modify, or delete events; send invitations
- **Access**: Only calendars accessible to the authenticated user

### Common Google Connector Properties

- **Auth**: Direct Google account authentication (no API keys)
- **Admin**: Team/Enterprise requires Owner or Primary Owner to enable integrations
- **Data handling**: Retrieved data stored on Anthropic servers with security protections; retention tied to chat (delete chat = delete data); models not trained on integration data (unverified)
- **Access pattern**: Data retrieved only on explicit user request, minimal information fetched

## Applicability to Coding Agent Workflows

| Aspect | Fit | Rationale |
|--------|-----|-----------|
| Code execution | No | Connectors are for data access, not compute |
| Research input | Yes | Drive/Gmail feed docs and threads into CC context via MCP bridge |
| Task automation | Low | Gmail, Calendar and GitHub are read-only; Drive and Microsoft 365 can write |
| CI/CD integration | No | Use GitHub Actions or Claude Code directly |
| Multi-repo orchestration | No | Connectors don't provide repo-level operations |
| Enterprise admin | Yes | Connectors + plugins provisioning via admin controls |

**Bottom line**: Since v2.1.46, all claude.ai connectors work in Claude Code via the MCP bridge. Gmail, Calendar, GitHub and Slack connectors are read-only (search/answer only; Slack write capability is not stated, search-only is inferred); Drive can create new files and Microsoft 365 has the broadest write actions (OneDrive/SharePoint files, mail, calendar events, Teams messages), admin-controlled for work/school accounts.

## Discovery

- Full docs index: `https://claude.com/docs/llms.txt`
- Connectors Directory: third-party integrations across Claude products; see [§ Public Connectors Directory](#public-connectors-directory)

### Public Connectors Directory

Observed 2026-11-25 on the [public directory page][dir] (a JavaScript-rendered page, read with a headless browser; a plain fetch returns nothing). Evidence level: observed on the vendor's page; the counts move, so treat them as a snapshot.

- **Counts (2026-11-25)**: "Show all 1224" connectors and "Show all 544" plugins. A fetch of the same page on 2026-11-24 showed 1,218 and 542. Only the first screen of cards (34 distinct connector links) was read in full; the other connectors sit behind the "Show all" links and were not enumerated.
- **Layout**: sections for Top connectors, Top plugins, Trending connectors (9) and New connectors (7), then a filter bar.
- **Filters**: 17 categories (Commerce & shopping, Communication, Consumer health, Creative, Data & analytics, Developer tools, Education, Financial services, Health & life sciences, Legal, Media & entertainment, Nonprofit, Other, Productivity, Sales & marketing, Travel, Healthcare); three types (Web, Desktop extension, Interactive); five sorts (Recommended, Most popular, Trending, Newest, A-Z).
- **"Anthropic verified" badge**: every card and detail page read on 2026-11-25 (34 listed connectors, and 12 detail pages: the ten in the table below plus Firecrawl and Checkatrade) carries the checkmark with the tooltip "Anthropic verified". Anthropic's own [verification page][verif] defines the labels: a Verified connector had its tools tested for quality and compatibility and met the Software Directory Policy at review time; Anthropic says this is not a security audit or a guarantee, and the developer can change the tools afterwards. The other label is Community (screened, not reviewed in depth). New submissions are listed as Community by default, and Anthropic's automated assessment may escalate popular ones to Verified review; there is no separate application ([submission guide][submit]). No Community card was visible in the portion read, so the share of Verified entries across all 1,224 is unknown.
- **Surfaces**: the detail pages do not state which Claude surfaces (web, desktop, Claude Code) a connector supports; only the Type filter hints at it. Claude Code reaches claude.ai connectors through the [MCP bridge](#claude-code-mcp-bridge-v2146).

Each entry's detail page shows its categories, maker, whether sign-in is required, the month added, the remote MCP URL and the tool list. Selected entries, each read at its own directory page on 2026-11-25 (all show the Anthropic verified badge). "Added" is the month the page shows; seven of the ten show November 2025, which may mark when the current listing began rather than when the connector first shipped:

| Entry | What it connects | Added | Sign-in |
|---|---|---|---|
| [Canva][c-canva] | Search, create, import and export designs | Nov 2025 | Required |
| [Box][c-box] | Search, Q&A and metadata extraction over Box files | Nov 2025 | Required |
| [monday.com][c-monday] | Boards, items and workflows; also CRM use | Nov 2025 | Required |
| [Notion][c-notion] | Search and edit pages and databases; skills and memory in Notion | Nov 2025 | Required |
| [Asana][c-asana] | Tasks, projects, portfolios and goals | Nov 2025 | Required |
| [Atlassian MCP][c-atlassian] | Jira, Confluence, Loom, Bitbucket under existing permissions; admin controls delete tools | Nov 2025 | Required |
| [Figma][c-figma] | Design context to code; diagrams in FigJam | Nov 2025 | Required |
| [Shopify][c-shopify] | Store building, products, orders, inventory, analytics | Apr 2026 | Not required |
| [ElevenLabs][c-elevenlabs] | Create and manage ElevenAgents voice agents | Jul 2026 | Required |
| [Zoho CRM][c-zohocrm] | Leads, deals, contacts; regional MCP URLs | Sep 2026 | Required |

- **Business and CRM entries**: monday.com and Zoho CRM are not covered in [CC-business-api-integrations.md](CC-business-api-integrations.md) (its [CRM section](CC-business-api-integrations.md#crm) covers HubSpot and Salesforce); that doc owns the business-API comparison and this table does not repeat it.
- **Entries in other docs**: Firecrawl's directory connector (Verified, added July 2026, read 2026-11-25) is analysed in [CC-web-scraping-plugins-analysis.md § Hosted Connector Route](CC-web-scraping-plugins-analysis.md#hosted-connector-route-chatgpt-and-claude); Checkatrade's (Verified, added July 2026, sign-in not required, read 2026-11-25) in [evaluation-data-resources-landscape.md](../../sdlc-lcm/evaluation-data-resources-landscape.md#3-datasets). Submission requirements are in [agent-identity-auth-landscape.md](../../sdlc-lcm/agent-identity-auth-landscape.md#2-authorize-the-agent-on-behalf-of-a-human-delegated-scoped-auditable).

## References

- [Connectors overview][overview]
- [Google Drive connector][drive]
- [Gmail connector][gmail]
- [Google Calendar connector][calendar]
- [GitHub connector][github]
- [Slack connector][slack]
- [Microsoft 365 connector][ms365]
- [CC MCP docs][cc-mcp-docs]
- [MCP specification][mcp]
- [Connectors directory][dir], [connector verification][verif], [submission guide][submit]
- [Cowork plugins & enterprise analysis](CC-cowork-plugins-enterprise-analysis.md)

[overview]: https://claude.com/docs/connectors/overview
[drive]: https://claude.com/docs/connectors/google/drive
[gmail]: https://claude.com/docs/connectors/google/gmail
[calendar]: https://claude.com/docs/connectors/google/calendar
[github]: https://claude.com/docs/connectors/github/index
[slack]: https://claude.com/docs/connectors/slack/index
[ms365]: https://claude.com/docs/connectors/microsoft/365
[mcp]: https://modelcontextprotocol.io
[dir]: https://claude.com/marketplace/connectors-plugins
[verif]: https://claude.com/docs/connectors/verification
[submit]: https://claude.com/docs/connectors/building/submission
[c-canva]: https://claude.com/marketplace/connectors/canva
[c-box]: https://claude.com/marketplace/connectors/box
[c-monday]: https://claude.com/marketplace/connectors/monday
[c-notion]: https://claude.com/marketplace/connectors/notion
[c-asana]: https://claude.com/marketplace/connectors/asana
[c-atlassian]: https://claude.com/marketplace/connectors/atlassian
[c-figma]: https://claude.com/marketplace/connectors/figma
[c-shopify]: https://claude.com/marketplace/connectors/shopify
[c-elevenlabs]: https://claude.com/marketplace/connectors/elevenlabs
[c-zohocrm]: https://claude.com/marketplace/connectors/zohocrm
[cc-changelog]: https://code.claude.com/docs/en/changelog
[cc-mcp-docs]: https://code.claude.com/docs/en/mcp
