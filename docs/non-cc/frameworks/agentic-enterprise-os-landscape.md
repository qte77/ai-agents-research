---
title: Agentic Enterprise OS Landscape
purpose: Survey of the "agentic enterprise OS" pattern (the operating-environment layer for AI agents) across enterprise platforms, open-source workspaces and the qte77 estate, with registry and pricing views.
platform_scope: [salesforce-agentforce, microsoft-copilot-studio, servicenow, sap-joule, databricks-genie, glean, lyzr, claude-code]
created: 2026-06-28
updated: 2026-11-27
validated_links_on: 2026-11-18
status: assess
---

**Details:**. Also runs on or integrates with: `self-hosted-oss`.

## What It Is

"Agentic enterprise OS" is the convergent idea of an **operating environment for agents** — a place where agents are deployed, governed, given tools and context, and run continuously, the way an OS hosts processes. It is a useful synthesis label, **not an established analyst category**: Gartner's formal 2026 term is *"AI agent development platforms"* (the 2026 Hype Cycle for Agentic AI places the category at the Peak of Inflated Expectations), and **no major enterprise vendor self-describes as an "agent OS"** — each uses its own framing ("digital labor", "AI control tower", "AI-first development environment"). "Agent OS" is mostly positioning language used by infrastructure-layer startups against the incumbents.

This doc maps the pattern across three tiers and contrasts the human-governed enterprise platforms with the agent-native goal-attribution loop in [goal-tracking-attribution-landscape][goal-attr].

## Tier 1 — Enterprise vendor platforms

All are proprietary SaaS; all govern **human-directed** agents (instructions, topics, guardrails); all interoperate via **MCP + A2A** and **none has adopted AG-UI** (see [ag-ui-protocol-landscape][ag-ui]); and — the load-bearing gap — **none exposes a machine-writable goal schema, autonomous goal generation, or per-run cost+outcome attribution**. Cost is billed per action or per consumption, not attributed to a goal. A per-*agent* cost view does exist: Agent 365 breaks Copilot Credits down by user, group, agent and service ([overview][agent365-overview]), but not by run or outcome. Registries are compared in [Agent registries compared](#agent-registries-compared); Microsoft 365 Copilot and Agentforce 360 are compared side by side in [Microsoft 365 Copilot vs Salesforce Agentforce 360](#microsoft-365-copilot-vs-salesforce-agentforce-360).

| Platform | Vendor framing | Commercial model | Notable |
|---|---|---|---|
| **[Salesforce Agentforce 360][agentforce]** | "digital labor" platform | proprietary; Flex Credits (20 credits/standard action × $500/100k credits ≈ $0.10/action, multiplier unchanged between the 2026-08-18 and 2026-11-03 rate cards) + per-conversation (not combinable with Flex Credits in the same org) + per-user editions | Agentforce Builder (Canvas/Script views) / Agent Script (Apache-2.0 authoring toolchain, runtime excluded) / Voice on the Einstein/Atlas engine; the [LLM Open Connector spec][einstein] (Apache-2.0) is the only other OSS-adjacent piece; whether Agentforce Agents have *direct* Agent-to-Agent Protocol (A2A) support is unsettled across Salesforce's own documentation (an architecture recipe and MuleSoft's own A2A-bridge guide say no, Salesforce's own interoperability guide says yes) — MuleSoft Agent Fabric's Agent Governance layer is at least the documented MCP+A2A path either way, no Agent-User Interaction Protocol (AG-UI); see [salesforce-agentforce-analysis.md][sf-agentforce-analysis] for the full first-party fact-check (pricing, Claude-on-Bedrock trust boundary, EU Operating Zone, data-masking scope, the A2A contradiction) |
| **[Microsoft Copilot Studio][copilot-studio]** (+ Agent 365) | "platform for building and managing agents" | proprietary; in M365 Copilot (add-on, $30.00/user/month paid yearly on the en-us pricing page, 2026-11-20) or Azure pay-as-you-go credits | declarative + autonomous (event-triggered) agents; Agent 365 is the governance control plane; A2A GA for the standard harness (April 2026), preview for the Microsoft Copilot harness (formerly the GitHub Copilot harness; the rename appears on both the [licensing FAQ][managed-runtime-licensing-faq] and Copilot Studio's [what's new][copilot-studio-whats-new] page, checked 2026-11-26) — a same-named "Copilot harness", documented separately from Microsoft Foundry's own "Copilot harness" and "managed runtime" (whether they share an implementation is not stated on either page) — see the caveat below; legacy Bot Framework (MIT) being archived |
| **[ServiceNow Otto][servicenow]** | "the AI control tower" | proprietary, cloud-only; bundled into Foundation/Advanced/Prime tiers (Apr 2026) | AI Agent Studio / Orchestrator / Control Tower + Action Fabric (MCP); vendor-neutral ("open to Claude, Copilot, or homegrown agents") |
| **[SAP Joule Studio 2.0][sap-joule]** | "AI-first development environment" | proprietary; free design-time through 2026 (promotional), production terms TBD | NL goal → PRD + code + tests + multi-agent orchestration *at design time*; part of the SAP Business AI Platform ("the Autonomous Enterprise", Sapphire 2026) |
| **[Databricks Genie][genie]** | "agentic data coworker" | proprietary managed; OSS lakehouse base (Spark / Delta / Iceberg) | Genie Ontology semantic graph as the persistent context "kernel"; Genie Agents as reusable autonomous workflows |
| **[Glean Independent Agents][glean]** | "AI coworkers" | not stated in the announcement | Distinct per-agent identity + persistent memory; proactive/event-triggered action (parallel to Copilot Studio's autonomous agents) across Slack/Jira/Teams — still admin-configured, not autonomous goal origination; first instance is the OnCall Assistant (beta) |
| **[Lyzr Agent Studio][lyzr-docs]** (+ Lyzr ADK, [Opencontroller][lyzr-opencontroller] (marketing page, no docs)) | enterprise agent builder with a governance control plane | proprietary; deploys as SaaS, on-premise in your VPC, or hybrid; Build tier $0, governance and workflow tiers custom, fixed-scope proof of concept $20,000; "No token billing: you pay your model provider directly" ([pricing][lyzr-pricing]) | no-code studio plus a Python SDK (`pip install lyzr-adk`); model-agnostic, Claude listed in the [ADK model table][lyzr-adk]; MCP client, with only its Cognis memory exposed as an MCP server ([MCP docs][lyzr-mcp]); A2A both ways, calling LangGraph/CrewAI/Semantic Kernel agents as sub-agents ([A2A docs][lyzr-a2a]) |

**Lyzr caveat** (added 2026-11-14): unlike the rest of the tier it also runs on-premise or hybrid, so "proprietary SaaS" above reads as "proprietary" for Lyzr. Its Model Context Protocol (MCP) and A2A support are documented first-party; its AG-UI posture was not checked. Compliance certifications and adoption figures on its site are vendor claims, not verified here. The public `LyzrCore` GitHub repos are small side projects; the most-starred, `lyzr-automata`, has no LICENSE file and is not the platform.

**Glean caveat**: added from the announcement blog post alone (2026-06-30). Its MCP support is confirmed first-party (`developers.glean.com/mcp`, IDE/host integrations for Claude Code, Cursor, Codex, and other MCP hosts); its A2A and AG-UI posture were not checked, so this row does not extend the "all interoperate via MCP + A2A, none has adopted AG-UI" line above to Glean — read that line as covering the original five.

**Microsoft Foundry "managed runtime" caveat (2026-11-12)**: Microsoft Foundry uses "managed
runtime" for two further, Copilot-Studio-unrelated things, each verified first-party against
Microsoft's own Learn pages:

- **Foundry Copilot harness** (public preview) — "an optional managed runtime for prompt agents.
  Foundry operates the harness and its execution environment" [foundry-copilot-harness]
  (2026-11-04). It is a same-named "Copilot harness," documented separately from the Copilot
  Studio one in the table above — whether they share an implementation is not stated on either
  page.
- **Foundry hosted agents** — "containerized agentic AI applications that run on Agent Service,"
  bring-your-own framework (Agent Framework, LangGraph, Semantic Kernel) [foundry-hosted-agents]
  (2026-11-09). The Learn concept page states no preview or GA status for this feature at all;
  only the separate marketing product page calls hosted agents "a managed runtime for running
  agent code in Azure" and "a session-isolated managed runtime with autoscaling and zero idle
  cost" [foundry-agent-service] — **GA status is unverified**, confirmed only as marketing-page
  wording, not repeated on the Learn concept page checked.

Full three-way harness disambiguation (Copilot Studio's renamed harness, Foundry's Copilot harness,
and Foundry hosted agents) is in
[microsoft-365-copilot-analysis.md § Three things called "harness"][m365-copilot-harness].

**Read carefully.** SAP Joule's "NL goal → PRD + code + tests" is *design-time code generation*, not runtime goal attribution. ServiceNow's "AI Control Tower" is a human-facing governance/observability dashboard, not a machine-readable attribution store. These are governance and authoring surfaces layered over human-set objectives — strong on identity, audit, and control; silent on autonomous goal origination.

## Microsoft 365 Copilot vs Salesforce Agentforce 360

Tier 1 has a Copilot Studio row and an Agentforce row; this section widens the Microsoft side to Microsoft 365
Copilot and sets it against Agentforce 360. Each cell points into [the Microsoft analysis][ms-analysis] ("MS") or
[the Salesforce analysis][sf-agentforce-analysis] ("SF"), which carry the evidence levels; this table does not
restate them.

| Dimension | Microsoft 365 Copilot | Salesforce Agentforce 360 |
|---|---|---|
| Target user and surfaces | Employees in Microsoft 365 apps, Copilot Chat and Cowork ([MS stack][ms-stack], [Cowork][ms-cowork]); customer-facing use is not compared here | Service, sales, Slack, Voice and role products ([SF surfaces][sf-surfaces]) |
| Agent builders | Agent Builder (low-code), Agents Toolkit (pro-code), Copilot Studio, Foundry ([MS declarative][ms-da], [MS stack][ms-stack]) | Agentforce Builder (Canvas/Script); Agent Script toolchain is Apache-2.0, runtime excluded ([SF products][sf-products], [SF Agent Script][sf-script]) |
| Runtime / harness | Three things called "harness" ([MS harness][m365-copilot-harness]); Managed Runtime is preview on Learn, while the Ignite post of 2026-11-17 announced GA ([MS Managed Runtime][ms-managed-runtime]); billing differs by harness ([MS stack][ms-stack]) | Atlas-based reasoning in Salesforce's trust boundary ([SF Claude][sf-claude]); Headless 360 exposes capabilities as API, MCP or CLI ([SF products][sf-products]) |
| Models incl. Claude | Anthropic models selectable, but excluded from the EU Data Boundary ([MS residency][ms-residency]) | Claude via Amazon Bedrock inside the Salesforce trust boundary ([SF Claude][sf-claude]) |
| MCP / A2A | A bring-your-own MCP registry is preview and needs the Agent 365 licence ([MS governance][m365-agent365]); Copilot Studio A2A status is in the Tier 1 row; Work IQ is reached over A2A, MCP or REST ([MS grounding][ms-grounding]) | MCP via the registry and MuleSoft Agent Fabric; direct A2A on agents is contradicted in Salesforce's own docs ([SF registry][sf-agentforce-registry], [SF status][sf-status]) |
| Data grounding | Microsoft Graph, SharePoint, connectors, Work IQ ([MS grounding][ms-grounding]) | Salesforce data and Data 360, metered per usage type ([SF pricing][sf-pricing]) |
| Governance and registry | See [Agent registries compared](#agent-registries-compared) | See [Agent registries compared](#agent-registries-compared) |
| Identity | Not compared in the analysis as a whole; Foundry hosted agents each get their own Entra identity ([MS Foundry][ms-stack]), Managed Runtime uses Entra ID ([MS Managed Runtime][ms-managed-runtime]) | Agent-user and permission-set detail not read; SSO/IdP federation for agent identity not found ([SF licences][sf-licences]) |
| Licence model | Per-user add-on, plus Copilot Credits for unlicensed or autonomous use ([MS licences][ms-licences]) | Flex Credits, per-conversation (not combinable in one org), per-user editions ([SF pricing][sf-pricing]) |
| Release status | Mixed GA and preview ([MS timeline][ms-timeline]) | Platform GA; many components pilot or beta ([SF status][sf-status]) |

### Worked pricing example (illustrative; re-check before budgeting)

Sources and what is confirmed:

- **Microsoft credit rate (confirmed from Learn raw text, 2026-11-20):** an agent action is 5 Copilot Credits, premium
  reasoning-model tokens 10 credits per 1,000 tokens ([billing rates][cs-billing-rates], ms.date 2026-11-24; rates re-checked 2026-11-26). The page covers the standard harness only, and its no-charge M365 Copilot inclusion does not apply to agents on the Microsoft Copilot harness.
  Employee-facing use by a Microsoft 365 Copilot-licensed user costs no credits only if the agent runs under that
  user's own identity (footnote 1), and computer-using agents are not included (footnote 4).
- **Microsoft credit price:** "PayGo is priced at $0.01 per Copilot Credit", quoted in the analysis's
  [Cowork section][ms-cowork] from Microsoft's GA blog (2026-06-16); the Managed Runtime FAQ gives the same
  rate ([MS Managed Runtime][ms-managed-runtime], accessed 2026-11-10). Applying it to Copilot Studio is an assumption.
- **Microsoft prices as shown (confirmed from the rendered en-us pages, 2026-11-20):** the
  [enterprise page][m365-pricing-ent] lists Microsoft 365 Copilot as an add-on at "$30.00 user/month, paid yearly",
  needing a qualifying Microsoft 365 plan, and notes that "Prices shown are for marketing purposes only and may not
  reflect the actual list price due to currency, country, and regional variant factors". The
  [Copilot Studio page][m365-pricing-cs] lists "capacity packs of 25,000 Copilot Credits each, priced at $200.00
  /pack/month" (that disclaimer was read on the enterprise page only). Both pages show "$" with no currency code and,
  from the fetching machine, "This product is not available in your market". The pack price is not used in the math
  below, which uses the PayGo rate.
- **Salesforce ([pricing page][agentforce-pricing], raw text read 2026-11-20, consistent with the
  analysis's 2026-11-12 read):** "$500 per 100k Credits" and a "$5 USD/User/Month (Requires Flex Credits)" Agentforce User License (metered agent usage for employees). The 20-credit action figure comes from the
  [rate card PDF][sf-rate-card] ("Updated as of November 3, 2026": Standard/Custom Action 20, sandbox 16), not from
  the pricing page.

Assumptions (invented): 100,000 agent actions per month, 500 employees, one Copilot Studio "agent action" and one
Flex "standard action" treated as comparable (they are not defined identically).

| Line | Microsoft (credits at $0.01) | Salesforce (Flex at $500 per 100,000) |
|---|---|---|
| Credits for 100,000 actions | 100,000 x 5 = 500,000 | 100,000 x 20 = 2,000,000 |
| Monthly credit cost | 500,000 x $0.01 = $5,000 | 2,000,000 / 100,000 x $500 = $10,000 |
| Employee user licence | Scenario 1, users not Copilot-licensed or agent autonomous: credits as above. Scenario 2, licensed users under their own identity: no credits; the seat is $30.00/user/month, paid yearly (as shown on the en-us page; see the disclaimer above) | 500 x $5 = $2,500 on top, as the licence requires Flex Credits ("$500" carries no currency code; the licence is quoted as "$5 USD", raw text 2026-11-20) |

Not captured: base suites (the qualifying Microsoft 365 plan the add-on needs) and other seats, Agent 365, Max Edition and add-ons, overage and enforcement rules, reasoning-token
charges, prompt/LLM rows and Data 360 on the rate card, discounts, commitments, other currencies, and the fair-use
limits. Salesforce's page says to contact sales for detailed pricing. Treat every figure as a snapshot, as both
analyses' Pricing sections ask.

## Tier 2 — Open-source self-operating workspaces & runtimes

The OSS layer gives you the runtime instead of a managed platform. Each has a dedicated analysis or is covered in the frameworks landscape; they are gathered here for the pattern:

- **[AutoAgent][autoagent]** (HKUDS, MIT; stale: 9.8k stars, last push 2025-10-16, `gh api` 2026-11-22) — explicitly an "autonomous Agent Operating System": a self-managing file system, an LLM-powered actionable engine, and self-play customization that generates its own tools and agents at runtime inside a Docker sandbox. The closest literal "agent OS" in this corpus.
- **[Odysseus][odysseus]** (AGPL-3.0) — self-hosted all-in-one AI workspace (chat, agents, deep research, email, calendar, notes) in one Docker Compose deploy with MCP integration — the breadth-over-depth "operating environment" model.
- **[Goose][goose]** (AAIF / Linux Foundation, Apache-2.0) — MCP co-creator and reference implementation; extensions *are* MCP servers and ACP handles agent-to-agent/IDE messaging — the protocol-native runtime an agent OS is built on.
- **multica** (in [agent-frameworks-infrastructure-landscape §1][frameworks]; source-available, modified Apache-2.0 — not OSI) — turns coding-agent CLIs into managed teammates: issues route to an agent or squad, a local daemon executes with autopilot (cron/webhook) scheduling.
- **[Octop][octop]** (TencentCloud, MIT) — self-hosted multi-user, multi-agent assistant: one admin account serves a household or small team, each user's "experts" (agents) isolated per database row inside a single Python process (no queue, no separate worker); an **AgentTeams (Beta)** coordinator schedules multiple experts on multi-step work, and outbound ACP delegates coding tasks to Claude Code, OpenCode, CodeBuddy, and Codex.

## Tier 3 — Estate worked examples (the self-operating pattern, built from primitives)

The qte77 estate assembles the self-operating environment from primitives rather than buying a platform:

- **[polyforge-orchestrator][polyforge]** — orchestrates parallel coding agents across a polyrepo from one devcontainer/workspace; it bridges the VS Code multi-root lifecycle gap by replaying each sibling repo's `onCreateCommand`/`postCreateCommand` hooks and generating a `workspace.code-workspace` with per-repo terminal tasks.
- **[office-forge-orchestrator][office-forge]** — the same pattern applied to office/business workflows, in three layers: `.claude/skills` (deterministic invoice/contract/report workflows) + `mcp/` (a business-API MCP catalog) + `config/` (project and credential definitions).
- **[liminal-flux-gh-acc][liminal]** ("Lim Sid") — a self-evolving, agent-operated GitHub account where agents **plan, code, review, reflect, supervise, and evolve** their own infrastructure (six action roles) across an **8-phase autonomy progression** (Phase 0–7; Phase 0 is deployment-ready, no live infra running yet). Humans set goals and handle security escalations. Its per-run attribution and cost gates are detailed in [goal-tracking-attribution-landscape][goal-attr].

## Company brain (adjacent synthesis label)

"Company brain" is a fresh (mid-2026; YC-Summer-2026-RFS- and essayist-coined) umbrella for a
**shared, permissioned, continuously-updated operational memory/context layer** over an organization's
data and decisions that both humans and agents query and act through: ingest → consolidate (typed
entities, contradictions auto-resolved, provenance + temporal tags) → retrieve (semantic + entity +
graph, permissioned at query time) → act (agents read/act/write outcomes back). It is **not a distinct
technology** but a *synthesis* of layers this repo already tracks — agent-memory infrastructure
([agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) §4),
knowledge-graph/GraphRAG + informal ontology
([semantic-layers-data-catalog-landscape.md](../infrastructure/semantic-layers-data-catalog-landscape.md)) — plus
retrieval-time permissioning and a write-back loop, applied org-wide.

Two of the four canonical sources are vendor marketing (a LinkedIn "context graph" pitch; a
Vectorize build-guide plugging its own ecosystem); the more substantive are an early OSS prototype
([caelstewart/company-brain](https://github.com/caelstewart/company-brain) — a temporal-KG engine on
Postgres+pgvector with an MCP server, ~alpha) and a concept note in
[hornof/llm-wiki](https://github.com/hornof/llm-wiki) (Karpathy-pattern KB). Treated here as an
**adjacent framing** of the same goal-attribution gap the enterprise platforms leave — not a separate
category. A standalone doc is deferred until the term accrues non-vendor traction.

## Agent registries compared

A registry answers "which agents and tools exist, who owns them, which version is live, and how is one
retired". Read 2026-11-20 at each source; Microsoft and Salesforce detail stays in their analyses.

| Registry | What it registers | Version and ownership | Retirement | Status (as read) |
|---|---|---|---|---|
| **[A2A Agent Card][a2a-spec]** | One agent, self-described at `/.well-known/agent-card.json`; the spec lists curated registries as one discovery route but defines no registry API; an AI Catalog at `/.well-known/ai-catalog.json` is merged to `dev-1.1`, unreleased ([ag-ui § A2A][ag-ui-a2a]) | Card has a free-form `version`; optional `provider`; cards may be JWS-signed | None for agents; the spec's deprecation rules cover protocol names only | Spec site 1.0.0; GitHub release v1.0.1 ([ag-ui § A2A][ag-ui-a2a]) |
| **[Official MCP Registry][mcp-registry]** | Metadata (`server.json`) for publicly reachable MCP servers; namespace proven by a GitHub, DNS or HTTP challenge; no private servers | Version string unique per publication and immutable; ranges rejected ([versioning][mcp-registry-versioning]) | `mcp-publisher status --status deleted` hides a server; it can be restored, never permanently removed ([FAQ][mcp-registry-faq]) | Preview: "Breaking changes or data resets may occur before general availability" |
| **[AWS Agent Registry][aws-agent-registry-ga]** (AgentCore) | Agents (A2A cards), MCP servers, skills and custom records; auto-detects agents on AgentCore runtime and gateways | Record `name` + `recordVersion` unique; publisher, curator and admin roles; tags for cost allocation and access control ([concepts][aws-registry-concepts]) | Curators approve or reject records and deprecate them to remove them from discovery ([curating][aws-registry-curating]) | GA, posted 2026-08-31, five regions at launch; 10 regions in the [AgentCore region table][aws-agentcore-regions] (read 2026-11-20) |
| **[Google Cloud Agent Registry][gcp-agent-registry]** | Agents, MCP servers and tools, endpoints and skills in a governance project, optionally across a folder or organization; automatic registration from supported runtimes or manual; Agent Gateway checks it before routing | Not compared here | Not stated on the two pages read | GA 2026-06-18 per the [Agent Platform release notes][gcp-agent-platform-relnotes] (the overview pages carry no label); standalone skills Preview, cross-cloud registration Limited Preview |
| **Microsoft Agent 365** | Agents built across Microsoft's tools plus synced third-party agents | Registry shows owner, usage and risk per agent; ownerless agents can be reassigned ([overview][agent365-overview]) | Approve, block, delete ([M365 analysis][m365-agent365]) | GA, commercial segment, per user |
| **Salesforce Agentforce Registry / MuleSoft Agent Fabric** | MCP servers (allowlist with sync states) and agents | Not stated in the analysis | Not stated in the analysis | No GA label on the first-party pages ([Agentforce analysis][sf-agentforce-registry]) |

**Reading the table.** Of the rows read, only AWS and Microsoft document ownership, approval and
retirement together (Google and Salesforce state less on the pages read); the two open formats stop at self-description (A2A) or public metadata
(MCP Registry). Claude Code has no org-level agent registry: fleets get policy through managed settings
and see agents only through telemetry ([CC-managed-settings-fleet-analysis.md][cc-fleet]). Per-cloud
depth: [aws-agent-stack-analysis.md][aws-stack] and [google-cloud-agent-stack-analysis.md][gcp-stack].

## Enterprise data APIs for agents

How an agent reaches the data each vendor holds: who it signs in as, what plan that needs, whether it can
run without a person present, what the terms say about automation or AI, and whether the vendor runs an
MCP server. Read 2026-11-26 and 2026-11-27 at each vendor's own pages; quotes are verbatim, and a cell
that could not be read says **unverified**. "Unattended" means an app identity (service account,
service principal, client credentials) rather than a signed-in person. This is not legal advice; the
terms pages are the authority. Vendor depth: [M365 Copilot][ms-graph-copilot],
[Salesforce][sf-agentforce-analysis], [Databricks Genie][genie], [AWS][aws-stack], [Google Cloud][gcp-stack].

| Vendor | Auth model | Licence or plan | Unattended access | Terms on automation or AI | Official MCP server |
|---|---|---|---|---|---|
| Microsoft Graph and Copilot APIs | Both: delegated ("an app acting on behalf of a signed-in user") and app-only ("an app acting with its own identity") ([auth][eda-ms-auth]) | Copilot Chat and Retrieval APIs: "available at no extra cost to users with a Microsoft 365 Copilot add-on license" ([chat][eda-ms-chat], [retrieval][eda-ms-retrieval]); Graph base licence unverified | Graph: yes, app-only. Copilot Chat, Retrieval and Search: delegated only ([endpoint table][ms-graph-copilot]) | API Terms (October 2025): you may not "Scrape, build databases or otherwise create copies of any data accessed or obtained using the Microsoft APIs" ([terms][eda-ms-terms]); the Copilot APIs have their own preview terms ([summary][ms-graph-copilot]) | Work IQ MCP, user-bound ([analysis][ms-analysis]); Microsoft's Graph MCP page marks its Enterprise server as deprecated ([page][eda-ms-mcp]) |
| Google Workspace | User OAuth 2.0 client ID; service accounts alone cannot reach user data "customarily accessed using Google Workspace APIs" ([auth][eda-gw-auth]) | Edition needed for the APIs: unverified | Yes, by domain-wide delegation: the service account names a user to impersonate and "cannot access data that the impersonated user themselves cannot access" ([service accounts][eda-g-sa]) | User Data Policy: "Limit your use of data to providing or improving user-facing features"; restricted scopes need an annual security assessment unless the app serves only your own domain ([policy][eda-g-udp]); no generative-AI clause seen | Yes, remote servers per app, e.g. Gmail `https://gmailmcp.googleapis.com/mcp/v1`; the OAuth client needs "Use this client for an AI-powered agent" ([MCP][eda-gw-mcp]) |
| Salesforce | OAuth 2.0 through external client apps; new connected apps can no longer be created since Spring '26 ([OAuth][eda-sf-oauth]) | Client credentials flow: "Available in: All Editions" ([flow][eda-sf-cc]); the "API Enabled" permission and per-edition API access: unverified | Yes: the client credentials flow runs as a named integration user and "eliminates the need for explicit user interaction" ([flow][eda-sf-cc]) | Unverified | Local `salesforcecli/mcp` reaches end of life on 2026-11-02 ([repo][eda-sf-mcp]); a hosted or Agentforce MCP server: unverified |
| Databricks | Both: OAuth U2M ("Attended authentication scenario") and a service principal with OAuth M2M ("Unattended, automated, and CI/CD workflows") ([auth][eda-dbx-auth]) | Plan tier: unverified | Yes: an OAuth secret for the service principal; tokens last one hour ([M2M][eda-dbx-m2m]) | Acceptable Use Policy bars interacting "through automated means", naming computer-use agents and robotic process automation, unless through a Databricks validated integration, and bars using "outputs of Databricks AI services to create or improve AI systems" ([AUP][eda-dbx-aup]) | Yes, managed: "The Genie One MCP is generally available"; `system.ai.dbsql` is Beta; some server URLs need a workspace admin to enable Managed MCP Servers ([MCPs][eda-dbx-mcp]) |
| AWS | IAM for AWS services; AgentCore Gateway outbound auth: caller IAM credentials, OAuth client credentials ("Machine-to-machine"), OAuth authorization code ("User-delegated access"), token exchange or API key ([Gateway][eda-aws-gw]) | Unverified | Yes: the client credentials grant acts "on the application's behalf, rather than on behalf of the user" ([Gateway][eda-aws-gw]) | Unverified (Service Terms not re-read) | `awslabs/mcp`: "The Agent Toolkit for AWS is the successor to the MCP servers, plugins, and skills available on AWS Labs" ([repo][eda-aws-labs]) |
| Google Cloud (BigQuery, Cloud Storage) | User credentials, service-account impersonation or attached service accounts; client libraries use Application Default Credentials ([auth][eda-bq-auth]) | Unverified | Yes: service accounts ([auth][eda-bq-auth]) | Service Terms §18: "Google will not use Customer Data to train or fine-tune any AI/ML models without Customer's prior permission or instruction." ([terms][eda-gcp-terms]) | Yes: `https://bigquery.googleapis.com/mcp` and `https://storage.googleapis.com/storage/mcp` ([MCP][eda-gcp-mcp]) |
| Atlassian (Jira, Confluence) | Jira Cloud REST v3: Forge scopes, Connect JWT, OAuth 2.0 (3LO), and "For personal scripts, bots, and ad-hoc execution of the REST APIs use basic authentication" ([Jira][eda-jira-auth]); Confluence: unverified | Unverified | API-token basic auth for scripts and bots ([Jira][eda-jira-auth]); "API token-based traffic is not affected" by the 65,000-point hourly app quota ([rate limits][eda-atl-rate]) | Developer Terms §6(d), written for Marketplace developers: no calls "that are not driven by a request from an end user or the Marketplace App itself" ([terms][eda-atl-terms]) | Yes: Rovo MCP server `https://mcp.atlassian.com/v2/mcp`, OAuth 2.1 or API token ([MCP][eda-atl-mcp]) |
| Slack | Bot tokens (`xoxb-`) are "not tied to a user's identity"; user tokens (`xoxp-`) ([tokens][eda-slack-tokens]) | Unverified | Yes: bot tokens ([tokens][eda-slack-tokens]) | API Terms (effective 2025-10-10), for apps offered outside your organisation: you may not "(A) use API Data to train a large language model" or "(B) bulk export Slack message and file data except where expressly allowed by an additional agreement" ([terms][eda-slack-terms]) | Yes: `https://mcp.slack.com/mcp`; "Only directory-published apps or internal apps may use MCP"; user tokens through OAuth ([MCP][eda-slack-mcp]) |
| ServiceNow | Inbound REST takes OAuth, ID token, mTLS and Basic by default; admins can deny Basic ([community post][eda-sn-auth]) | Unverified (product docs and legal pages not readable here) | Yes: for autonomous agents an admin signs in once "as a dedicated ServiceNow integration user account" ([FAQ][eda-sn-faq]) | Unverified | Yes: "MCP Server Console", "ServiceNow's native implementation of an MCP server", OAuth 2.0 authorization code ([FAQ][eda-sn-faq], [Action Fabric][eda-sn-fabric]). All ServiceNow cells come from community articles on servicenow.com, not product docs |
| Snowflake | SQL API: OAuth, key-pair authentication or workload identity federation; "The JWT is valid for at most one hour after the token is issued." ([SQL API][eda-snow-auth]) | Edition and cost: unverified | Key-pair and workload identity need no interactive sign-in (our reading of [SQL API][eda-snow-auth]) | AI Terms (updated 2026-10-27) §3.2: Snowflake will not use Customer Data or Usage Data "to train, re-train or fine-tune any Model that Snowflake makes available for use by other parties" (Snowflake AI Terms, see Sources) | Yes, Snowflake-managed: "Snowflake OAuth by default, with optional External OAuth."; "Tool results leave Snowflake." ([MCP][eda-snow-mcp]) |
| Box | Both: "Apps that people sign in to are User apps, which always use OAuth 2.0."; "Apps that run on their own are Server apps, which use either Client Credentials Grant (CCG) or JWT." ([auth][eda-box-auth]) | Free Developer plan: "Full Box API access", "10K API calls per month" (Box pricing page, see Sources) | Yes: CCG: "No one logs in, so it suits code that runs unattended."; JWT apps can act for a user through the `as-user` header once an admin enables it ([auth][eda-box-auth], [as-user][eda-box-asuser]) | ToS (effective 2026-08-17) §10(d): you must not "use any automated process or service (such as a bot, a spider, or periodic caching of information stored by Box) to access or use the Services" (Box ToS, see Sources); whether API apps fall under it is not stated. AI AUP: "Customers are responsible for the configuration, instruction and testing of their own customized agents" (Box AI AUP, see Sources) | Yes: hosted `https://mcp.box.com` ([MCP][eda-box-mcp]) |
| Notion | Internal connection (one static token), personal access token (acts as its creator) or OAuth ([authorization][eda-notion-auth], [tokens][eda-notion-pat]) | Internal connections need a workspace owner; who may create a personal access token varies by plan ([tokens][eda-notion-pat]); plan for API use: unverified | Yes, by internal connection, but each page "must be manually shared with the connection" ([authorization][eda-notion-auth]) | Unverified (developer terms pages not reachable) | Yes: hosted `https://mcp.notion.com/mcp` over OAuth ([MCP][eda-notion-mcp]); the self-hosted `makenotion/notion-mcp-server` is "no longer actively maintained or supported" ([repo][eda-notion-gh]) |
| SAP | Unverified (api.sap.com and help.sap.com need JavaScript the fetcher could not render) | Unverified | Unverified | Unverified (API policy page returned HTTP 403) | Product servers only: LeanIX MCP Server ([repo][eda-sap-leanix]) and an Integration Suite MCP Gateway sample ([repo][eda-sap-imcp]); no general business-data server found in the SAP and SAP-samples GitHub orgs |
| Workday | REST and integration system user: unverified; Workday says its "REST, SOAP, GraphQL, and RaaS catalog remains the standard for system-to-system integrations" ([agent tools][eda-wd-tools]) | Unverified | Agents get "a unique identity (Agent System User) for authentication, authorization and auditing" ([system of record][eda-wd-asor]) | Unverified | Early: "Agent-Ready Tools are available in Early Availability for MCP-based agent stacks." ([blog][eda-wd-blog]); the tools "Scope every action to the user's identity" ([agent tools][eda-wd-tools]) |
| OpenCloud | OIDC; app tokens for clients that cannot use OIDC ([auth-app][eda-oc-app], read 2026-11-26) | Community Edition "can be run yourself free of charge"; Basic, Professional and Premium by quote ([plans][eda-oc-subs]); Apache-2.0 ([repo][eda-oc-gh]) | No app-only grant found: app tokens belong to a user ([auth-app][eda-oc-app]) | Unverified | `opencloud-eu/opencloud-mcp` (Apache-2.0), in "Lab status", acts "always as the signed-in user" ([repo][eda-oc-mcp]) |
| Nextcloud | User-bound: Login Flow v2, an app password "for WebDAV clients and scripts", OAuth2 for "only confidential clients" ([Login Flow][eda-nc-lf], [WebDAV][eda-nc-dav], [OAuth2][eda-nc-oauth]) | Server AGPL-3.0 ([repo][eda-nc-gh]); Community vs Enterprise terms: unverified | No app-only grant found; app passwords belong to a user ([WebDAV][eda-nc-dav]) | Unverified | Inside the Context Agent app: "Context Agent exposes an MCP server that can be used by other large language models or applications", authenticated with an app password ([Context Agent][eda-nc-ca]) |

Reading the table (our synthesis, not a vendor statement):

- **Hosted MCP servers mostly act as a signed-in user.** Workday, OpenCloud, Slack, Nextcloud and the
  Work IQ server say so outright; ServiceNow's answer for agents with no user present is a dedicated
  integration user signed in once. An unattended agent otherwise goes through the REST API with an app
  identity, where the vendor offers one (Google, Databricks, Salesforce, Box, AWS, Microsoft Graph).
- **Training clauses point two ways.** Slack bars the *app provider* from training a large language
  model on API data; Google Cloud, Snowflake and Box bind *themselves* not to train on customer data
  without consent.
- **Automation clauses exist but rarely name agents.** Box §10(d), the Databricks AUP and Atlassian
  §6(d) restrict automated access; none of the pages read says how that applies to an agent using the
  vendor's own API credentials. Check the vendor's terms before building on it.

## Synthesis

Three tiers, one axis — **who sets and owns the goals**:

- **Enterprise platforms** instrument and govern agents that execute *human-authored* objectives. Strong on governance, identity, and audit; silent on autonomous goal origination and per-run attribution.
- **OSS runtimes** hand you the operating environment but leave the goal/attribution model to you.
- **The estate pattern** wires the missing loop — machine-writable goals, per-run `cost_usd` + `outcome` tracing, cost gates — on top of OSS primitives.

The enterprise "agent OS" is real as a **governance-and-authoring layer**; it is not (yet) an **autonomous goal-attribution system**. That gap is the research thread this corpus tracks in [goal-tracking-attribution-landscape][goal-attr].

## Cross-References

- [goal-tracking-attribution-landscape.md][goal-attr] — the agent-native goal/attribution loop these platforms do not close
- [databricks-genie-analysis.md][genie] · [autoagent-analysis.md][autoagent] · [odysseus-analysis.md][odysseus] · [goose-analysis.md][goose] · [octop-analysis.md][octop] — per-tool deep dives
- [agent-frameworks-infrastructure-landscape.md][frameworks] — multica + the broader orchestration catalog
- [ag-ui-protocol-landscape.md][ag-ui] — the AG-UI protocol none of these enterprise platforms adopt

## Not included

Entries removed under the [pruning rule](../../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (alive, adopted or proven; checked 2026-11-22).

| Name | Reason | Date | Link |
|---|---|---|---|
| HugAgentOS (ZJU-REAL) | (criterion 3) 635 stars, last push 2026-11-20 (`gh api` 2026-11-22); no paper (arXiv search for the name returns nothing), no named independent users and no measured benefit in the README | 2026-11-22 | [ZJU-REAL/HugAgentOS](https://github.com/ZJU-REAL/HugAgentOS) |

## Sources

| Source | Content |
|---|---|
| [M365 Copilot pricing][m365-pricing-ent], [Copilot Studio pricing][m365-pricing-cs], [billing rates][cs-billing-rates], [Agentforce pricing][agentforce-pricing], [Flex Credits rate card][sf-rate-card] | Rates for the worked example; Learn billing rates, the rate card and the Salesforce pricing page confirmed from raw text 2026-11-20; Microsoft pricing pages from the rendered en-us pages (headless browser) 2026-11-20 |
| [Salesforce Agentforce (news)][agentforce] | Agentforce 360 "digital labor" platform; per-action/Flex-Credit billing |
| [salesforce/einstein-platform][einstein] | LLM Open Connector spec (Apache-2.0) — the OSS-adjacent connector piece |
| [Microsoft Copilot Studio overview][copilot-studio] | "Platform for building and managing agents"; declarative + autonomous agents |
| [ServiceNow Otto (newsroom)][servicenow] | "AI control tower"; AI Agent Studio/Orchestrator + Action Fabric (MCP) |
| [SAP Joule Studio (news)][sap-joule] | "AI-first development environment"; design-time NL→PRD→code→tests |
| [Databricks Genie analysis][genie] | Agentic data coworker; Genie Ontology context graph |
| [Glean — "Introducing independent agents"][glean] | AI coworker agents; independent identity, memory, proactive action |
| [Lyzr docs][lyzr-docs], [ADK overview][lyzr-adk], [MCP][lyzr-mcp], [A2A][lyzr-a2a], [pricing][lyzr-pricing] | Lyzr deployment modes, SDK and models, MCP/A2A support, tiers |
| [Lyzr Opencontroller page][lyzr-opencontroller] | Marketing page (checked 2026-11-18): pitches a single control plane over all of an org's agents; no docs or repo link on it, so treat the capability as a vendor claim |
| Gartner — 2026 Hype Cycle for Agentic AI (gartner.com; bot-blocked, not link-checked) | First-party anchor for the formal category "AI agent development platforms" |
| [A2A specification][a2a-spec] | Agent Card, discovery (§ 8.2), signing (§ 8.4); latest released version 1.0.0 (read 2026-11-20) |
| [MCP Registry: about][mcp-registry], [versioning][mcp-registry-versioning], [FAQ][mcp-registry-faq] | Preview status, public-only metadata, immutable versions, `deleted` status (read 2026-11-20) |
| [AWS Agent Registry GA][aws-agent-registry-ga], [concepts][aws-registry-concepts], [curating][aws-registry-curating] | GA 2026-08-31, record types and versions, roles, deprecation (read 2026-11-20) |
| [Google Cloud Agent Registry overview][gcp-agent-registry], [Agent Platform page][gcp-agent-registry-govern] | Governance project, management boundary, automatic vs manual registration, Agent Gateway (read 2026-11-20); GA date from the [release notes][gcp-agent-platform-relnotes] |
| [Microsoft Agent 365 overview][agent365-overview] | Registry per-agent owner, usage and risk; Copilot Credits by user, group, agent and service (read 2026-11-20) |
| [Use the Microsoft Copilot harness with prompt agents][foundry-copilot-harness] | Foundry's own "Copilot harness" — a different thing from Copilot Studio's harness |
| [Hosted agents in Foundry Agent Service][foundry-hosted-agents] | Foundry hosted agents — containerized, bring-your-own-framework; no stated preview/GA status |
| [Microsoft Foundry Agent Service (product page)][foundry-agent-service] | Marketing-page-only "managed runtime" wording for hosted agents |
| [AutoAgent][autoagent] · [Odysseus][odysseus] · [Goose][goose] · [multica][frameworks] · [Octop][octop] | OSS self-operating workspaces / runtimes (in-corpus analyses) |
| [polyforge-orchestrator][polyforge] · [office-forge-orchestrator][office-forge] · [liminal-flux-gh-acc][liminal] | qte77 estate self-operating orchestrators (public repos) |
| Enterprise data APIs ([section](#enterprise-data-apis-for-agents)): Microsoft [auth][eda-ms-auth], [Chat API][eda-ms-chat], [Retrieval API][eda-ms-retrieval], [API Terms][eda-ms-terms], [Graph MCP][eda-ms-mcp]; Google [Workspace auth][eda-gw-auth], [service accounts][eda-g-sa], [User Data Policy][eda-g-udp], [Workspace MCP][eda-gw-mcp], [BigQuery auth][eda-bq-auth], [Cloud Service Terms][eda-gcp-terms], [Cloud MCP][eda-gcp-mcp]; Salesforce [OAuth][eda-sf-oauth], [client credentials][eda-sf-cc], [CLI MCP][eda-sf-mcp]; Databricks [auth][eda-dbx-auth], [M2M][eda-dbx-m2m], [AUP][eda-dbx-aup], [MCPs][eda-dbx-mcp]; AWS [Gateway outbound auth][eda-aws-gw], [awslabs/mcp][eda-aws-labs] | Read 2026-11-27 (Workspace, Microsoft, Salesforce, Databricks, AWS, Google Cloud) |
| Atlassian [Jira auth][eda-jira-auth], [rate limits][eda-atl-rate], [Developer Terms][eda-atl-terms], [Rovo MCP][eda-atl-mcp]; Slack [tokens][eda-slack-tokens], [API Terms][eda-slack-terms], [MCP][eda-slack-mcp]; ServiceNow community articles: [REST auth][eda-sn-auth], [MCP FAQ][eda-sn-faq], [Action Fabric][eda-sn-fabric]; Snowflake [SQL API auth][eda-snow-auth], [MCP][eda-snow-mcp]; Snowflake AI Terms `https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/ai-terms/` | Read 2026-11-27; ServiceNow product docs and legal pages could not be read, so its cells rest on community articles |
| Box [auth][eda-box-auth], [as-user][eda-box-asuser], [MCP][eda-box-mcp]; Box pricing `https://www.box.com/pricing`, ToS `https://www.box.com/legal/termsofservice` and AI AUP `https://www.box.com/legal/boxaiacceptableusepolicy`; Notion [authorization][eda-notion-auth], [tokens][eda-notion-pat], [MCP][eda-notion-mcp], [repo][eda-notion-gh]; SAP [LeanIX plugins][eda-sap-leanix], [MCP Gateway sample][eda-sap-imcp]; Workday [agent tools][eda-wd-tools], [system of record][eda-wd-asor], [blog][eda-wd-blog]; OpenCloud [auth-app][eda-oc-app], [plans][eda-oc-subs], [repo][eda-oc-gh], [MCP][eda-oc-mcp]; Nextcloud [Login Flow][eda-nc-lf], [WebDAV][eda-nc-dav], [OAuth2][eda-nc-oauth], [Context Agent][eda-nc-ca], [repo][eda-nc-gh] | Read 2026-11-27 (OpenCloud auth-app 2026-11-26); SAP, Workday and Notion terms pages not readable. The Box and Snowflake pages in code format return 403 to the link checker (bot-blocked), so they are not linked; they were read with a browser-impersonating fetch |

[ms-analysis]: ../agents/microsoft-365-copilot-analysis.md
[ms-stack]: ../agents/microsoft-365-copilot-analysis.md#microsoft-agent-stack-2026-11-18
[ms-cowork]: ../agents/microsoft-365-copilot-analysis.md#microsoft-copilot-cowork-ga-june-2026
[ms-da]: ../agents/microsoft-365-copilot-analysis.md#declarative-agents
[ms-residency]: ../agents/microsoft-365-copilot-analysis.md#residency-anthropic-excluded-from-the-eu-data-boundary-claude-on-foundry-has-no-eu-data-zone-either
[ms-grounding]: ../agents/microsoft-365-copilot-analysis.md#grounding-layers
[ms-licences]: ../agents/microsoft-365-copilot-analysis.md#licences-2026-11-18
[ms-timeline]: ../agents/microsoft-365-copilot-analysis.md#timeline
[ms-managed-runtime]: ../agents/microsoft-365-copilot-analysis.md#microsoft-copilot-managed-runtime-preview
[sf-surfaces]: ../agents/salesforce-agentforce-analysis.md#naming-lineage-agentexchange-role-products-and-agent-surfaces
[sf-products]: ../agents/salesforce-agentforce-analysis.md#products-and-timeline-what-agentforce-360-comprises
[sf-script]: ../agents/salesforce-agentforce-analysis.md#agent-script-and-agentforce-dx
[sf-claude]: ../agents/salesforce-agentforce-analysis.md#claude-inside-salesforces-trust-boundary-via-amazon-bedrock
[sf-status]: ../agents/salesforce-agentforce-analysis.md#announced-vs-shipped
[sf-pricing]: ../agents/salesforce-agentforce-analysis.md#pricing-flex-credits-rate-card-as-of-2026-11-03
[sf-licences]: ../agents/salesforce-agentforce-analysis.md#licences-and-roles-for-agentforce-agents
[m365-pricing-ent]: https://www.microsoft.com/en-us/microsoft-365-copilot/pricing/enterprise
[m365-pricing-cs]: https://www.microsoft.com/en-us/microsoft-365-copilot/pricing/copilot-studio
[cs-billing-rates]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management
[agentforce-pricing]: https://www.salesforce.com/agentforce/pricing/
[sf-rate-card]: https://www.salesforce.com/en-us/wp-content/uploads/sites/4/assets/pdf/agentforce/Flex-Credits-Rate-Card-11.3.2026.pdf
[agentforce]: https://www.salesforce.com/news/stories/agentforce-operations-announcement/
[sf-agentforce-analysis]: ../agents/salesforce-agentforce-analysis.md
[einstein]: https://github.com/salesforce/einstein-platform
[copilot-studio]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-what-is-copilot-studio
[copilot-studio-whats-new]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/whats-new
[servicenow]: https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-Otto-creates-the-unified-AI-experience-for-the-enterprise/default.aspx
[sap-joule]: https://news.sap.com/2026/05/new-joule-studio-enterprise-scale-agentic-development/
[glean]: https://www.glean.com/blog/introducing-independent-agents
[lyzr-docs]: https://docs.lyzr.ai/
[lyzr-adk]: https://docs.lyzr.ai/enterprise/adk/overview
[lyzr-mcp]: https://docs.lyzr.ai/enterprise/agent-studio/tools/MCP
[lyzr-a2a]: https://docs.lyzr.ai/enterprise/integrations/a2a-protocol
[lyzr-pricing]: https://www.lyzr.ai/pricing/
[lyzr-opencontroller]: https://www.lyzr.ai/opencontroller/
[octop]: ../agents/octop-analysis.md
[polyforge]: https://github.com/qte77/polyforge-orchestrator
[office-forge]: https://github.com/qte77/office-forge-orchestrator
[liminal]: https://github.com/qte77/liminal-flux-gh-acc
[goal-attr]: ../../sdlc-lcm/goal-tracking-attribution-landscape.md
[genie]: ../agents/databricks-genie-analysis.md
[autoagent]: autoagent-analysis.md
[odysseus]: ../agents/odysseus-analysis.md
[goose]: ../agents/goose-analysis.md
[frameworks]: agent-frameworks-infrastructure-landscape.md
[ag-ui]: ../protocols/ag-ui-protocol-landscape.md
[managed-runtime-licensing-faq]: https://learn.microsoft.com/en-us/microsoft-365/admin/manage/apps/licensing-faq?view=o365-worldwide
[foundry-copilot-harness]: https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/use-tools-skills-copilot-harness
[foundry-hosted-agents]: https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents
[foundry-agent-service]: https://azure.microsoft.com/en-us/products/ai-foundry/agent-service
[m365-copilot-harness]: ../agents/microsoft-365-copilot-analysis.md#three-things-called-harness
[a2a-spec]: https://a2a-protocol.org/latest/specification/
[mcp-registry]: https://modelcontextprotocol.io/registry/about
[mcp-registry-versioning]: https://modelcontextprotocol.io/registry/versioning
[mcp-registry-faq]: https://modelcontextprotocol.io/registry/faq
[aws-agent-registry-ga]: https://aws.amazon.com/about-aws/whats-new/2026/08/aws-agent-registry-generally-available
[aws-registry-concepts]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-concepts.html
[aws-registry-curating]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-curating.html
[gcp-agent-registry]: https://docs.cloud.google.com/agent-registry/overview
[aws-agentcore-regions]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html
[gcp-agent-platform-relnotes]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes
[gcp-agent-registry-govern]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/agent-registry
[agent365-overview]: https://learn.microsoft.com/en-us/microsoft-agent-365/overview
[m365-agent365]: ../agents/microsoft-365-copilot-analysis.md#governance-agent-365-covers-agents-not-sharepoint-skills
[sf-agentforce-registry]: ../agents/salesforce-agentforce-analysis.md#agentforce-registry-and-mulesoft-agent-fabric
[ag-ui-a2a]: ../protocols/ag-ui-protocol-landscape.md#a2a-agent-to-agent-protocol
[aws-stack]: ../agents/aws-agent-stack-analysis.md
[gcp-stack]: ../agents/google-cloud-agent-stack-analysis.md
[cc-fleet]: ../../cc-native/configuration/CC-managed-settings-fleet-analysis.md
[ms-graph-copilot]: ../agents/microsoft-365-copilot-analysis.md#microsoft-graph-copilot-apis-learn-read-2026-11-26
[eda-ms-auth]: https://learn.microsoft.com/en-us/graph/auth/auth-concepts
[eda-ms-chat]: https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/api/ai-services/chat/overview
[eda-ms-retrieval]: https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/api/ai-services/retrieval/overview
[eda-ms-terms]: https://learn.microsoft.com/en-us/legal/microsoft-apis/terms-of-use
[eda-ms-mcp]: https://learn.microsoft.com/en-us/graph/mcp-server/overview
[eda-gw-auth]: https://developers.google.com/workspace/guides/auth-overview
[eda-g-sa]: https://developers.google.com/identity/protocols/oauth2/service-account
[eda-g-udp]: https://developers.google.com/terms/api-services-user-data-policy
[eda-gw-mcp]: https://developers.google.com/workspace/guides/configure-mcp-servers
[eda-sf-oauth]: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_oauth_and_connected_apps.htm
[eda-sf-cc]: https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_client_credentials_flow.htm
[eda-sf-mcp]: https://github.com/salesforcecli/mcp
[eda-dbx-auth]: https://docs.databricks.com/aws/en/dev-tools/auth/
[eda-dbx-m2m]: https://docs.databricks.com/aws/en/dev-tools/auth/oauth-m2m
[eda-dbx-aup]: https://www.databricks.com/legal/acceptable-use-policy
[eda-dbx-mcp]: https://docs.databricks.com/aws/en/agents/mcp-tools/built-in-mcp-services
[eda-aws-gw]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-outbound-auth.html
[eda-aws-labs]: https://github.com/awslabs/mcp
[eda-bq-auth]: https://docs.cloud.google.com/bigquery/docs/authentication
[eda-gcp-terms]: https://cloud.google.com/terms/service-terms
[eda-gcp-mcp]: https://docs.cloud.google.com/mcp/supported-products
[eda-jira-auth]: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
[eda-atl-rate]: https://developer.atlassian.com/cloud/confluence/rate-limiting/
[eda-atl-terms]: https://developer.atlassian.com/platform/marketplace/atlassian-developer-terms/
[eda-atl-mcp]: https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/
[eda-slack-tokens]: https://docs.slack.dev/authentication/tokens
[eda-slack-terms]: https://slack.com/terms-of-service/api
[eda-slack-mcp]: https://docs.slack.dev/ai/slack-mcp-server/
[eda-sn-auth]: https://www.servicenow.com/community/platform-privacy-security-blog/eliminating-basic-auth-across-all-inbound-surfaces-rest-apis/ba-p/3552359
[eda-sn-faq]: https://www.servicenow.com/community/servicenow-otto-articles/mcp-server-console-faq/ta-p/3550125
[eda-sn-fabric]: https://www.servicenow.com/community/servicenow-otto-articles/action-fabric-mcp-server-mcp-client-and-a2a-explained/ta-p/3557794
[eda-snow-auth]: https://docs.snowflake.com/en/developer-guide/sql-api/authenticating
[eda-snow-mcp]: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp
[eda-box-auth]: https://developer.box.com/guides/authentication/
[eda-box-asuser]: https://developer.box.com/guides/authentication/jwt/as-user/
[eda-box-mcp]: https://developer.box.com/guides/box-mcp/
[eda-notion-auth]: https://developers.notion.com/guides/get-started/authorization
[eda-notion-pat]: https://developers.notion.com/guides/connections-and-tokens/personal-access-tokens
[eda-notion-mcp]: https://developers.notion.com/docs/mcp
[eda-notion-gh]: https://github.com/makenotion/notion-mcp-server
[eda-sap-leanix]: https://github.com/SAP/leanix-ai-plugins
[eda-sap-imcp]: https://github.com/SAP-samples/integration-mcp-gateway
[eda-wd-tools]: https://www.workday.com/en-us/ai-platform/agent-tools-mcp.html
[eda-wd-asor]: https://www.workday.com/en-us/ai-platform/agent-system-of-record.html
[eda-wd-blog]: https://blog.workday.com/en-us/workday-agentic-era-paths-build.html
[eda-oc-app]: https://github.com/opencloud-eu/docs/blob/main/docs/_static/env-vars/auth-app_readme.md
[eda-oc-subs]: https://opencloud.eu/en/subscription-support
[eda-oc-gh]: https://github.com/opencloud-eu/opencloud
[eda-oc-mcp]: https://github.com/opencloud-eu/opencloud-mcp
[eda-nc-lf]: https://docs.nextcloud.com/server/latest/developer_manual/client_apis/LoginFlow/index.html
[eda-nc-dav]: https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/basic.html
[eda-nc-oauth]: https://docs.nextcloud.com/server/latest/admin_manual/configuration_server/oauth2.html
[eda-nc-ca]: https://docs.nextcloud.com/server/latest/admin_manual/ai/app_context_agent.html
[eda-nc-gh]: https://github.com/nextcloud/server
