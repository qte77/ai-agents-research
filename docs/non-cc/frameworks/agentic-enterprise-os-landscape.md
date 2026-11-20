---
title: Agentic Enterprise OS Landscape
purpose: Survey of the "agentic enterprise OS" pattern — the operating-environment layer for AI agents — across enterprise vendor platforms (Agentforce 360, Microsoft Copilot Studio, ServiceNow Otto, SAP Joule, Databricks Genie, Glean Independent Agents), open-source self-operating workspaces (AutoAgent, Odysseus, Goose, multica, HugAgentOS, Octop), and the qte77 estate's self-operating orchestrators; framed honestly against Gartner's "AI agent development platforms" category and the agent-native goal-attribution gap each enterprise platform leaves; includes a comparison of agent registries (A2A, MCP Registry, AWS, Google, Agent 365, Agentforce) and a Microsoft 365 Copilot vs Agentforce 360 comparison with an illustrative pricing example.
category: landscape
platform_scope: [salesforce-agentforce, microsoft-copilot-studio, servicenow, sap-joule, databricks-genie, glean, lyzr, self-hosted-oss, claude-code]
created: 2026-06-28
updated: 2026-11-20
validated_links: 2026-11-18
status: assess
---

## What It Is

"Agentic enterprise OS" is the convergent idea of an **operating environment for agents** — a place where agents are deployed, governed, given tools and context, and run continuously, the way an OS hosts processes. It is a useful synthesis label, **not an established analyst category**: Gartner's formal 2026 term is *"AI agent development platforms"* (the 2026 Hype Cycle for Agentic AI places the category at the Peak of Inflated Expectations), and **no major enterprise vendor self-describes as an "agent OS"** — each uses its own framing ("digital labor", "AI control tower", "AI-first development environment"). "Agent OS" is mostly positioning language used by infrastructure-layer startups against the incumbents.

This doc maps the pattern across three tiers and contrasts the human-governed enterprise platforms with the agent-native goal-attribution loop in [goal-tracking-attribution-landscape][goal-attr].

## Tier 1 — Enterprise vendor platforms

All are proprietary SaaS; all govern **human-directed** agents (instructions, topics, guardrails); all interoperate via **MCP + A2A** and **none has adopted AG-UI** (see [ag-ui-protocol-landscape][ag-ui]); and — the load-bearing gap — **none exposes a machine-writable goal schema, autonomous goal generation, or per-run cost+outcome attribution**. Cost is billed per action or per consumption, not attributed to a goal. A per-*agent* cost view does exist: Agent 365 breaks Copilot Credits down by user, group, agent and service ([overview][agent365-overview]), but not by run or outcome. Registries are compared in [Agent registries compared](#agent-registries-compared); Microsoft 365 Copilot and Agentforce 360 are compared side by side in [Microsoft 365 Copilot vs Salesforce Agentforce 360](#microsoft-365-copilot-vs-salesforce-agentforce-360).

| Platform | Vendor framing | Commercial model | Notable |
|---|---|---|---|
| **[Salesforce Agentforce 360][agentforce]** | "digital labor" platform | proprietary; Flex Credits (20 credits/standard action × $500/100k credits ≈ $0.10/action, multiplier unchanged between the 2026-08-18 and 2026-11-03 rate cards) + per-conversation (not combinable with Flex Credits in the same org) + per-user editions | Agentforce Builder (Canvas/Script views) / Agent Script (Apache-2.0 authoring toolchain, runtime excluded) / Voice on the Einstein/Atlas engine; the [LLM Open Connector spec][einstein] (Apache-2.0) is the only other OSS-adjacent piece; whether Agentforce Agents have *direct* A2A support is unsettled across Salesforce's own documentation (an architecture recipe and MuleSoft's own A2A-bridge guide say no, Salesforce's own interoperability guide says yes) — MuleSoft Agent Fabric's Agent Governance layer is at least the documented MCP+A2A path either way, no AG-UI; see [salesforce-agentforce-analysis.md][sf-agentforce-analysis] for the full first-party fact-check (pricing, Claude-on-Bedrock trust boundary, EU Operating Zone, data-masking scope, the A2A contradiction) |
| **[Microsoft Copilot Studio][copilot-studio]** (+ Agent 365) | "platform for building and managing agents" | proprietary; in M365 Copilot ($30/user/mo) or Azure pay-as-you-go credits | declarative + autonomous (event-triggered) agents; Agent 365 is the governance control plane; A2A GA for the standard harness (April 2026), preview for the GitHub Copilot harness, now itself being renamed the Microsoft Copilot harness per Microsoft's own billing documentation ([licensing FAQ][managed-runtime-licensing-faq]) — Copilot Studio's own [what's new][copilot-studio-whats-new] page still calls it the GitHub Copilot harness throughout, as of its 2026-11-04 content date — a same-named "Copilot harness", documented separately from Microsoft Foundry's own "Copilot harness" and "managed runtime" (whether they share an implementation is not stated on either page) — see the caveat below; legacy Bot Framework (MIT) being archived |
| **[ServiceNow Otto][servicenow]** | "the AI control tower" | proprietary, cloud-only; bundled into Foundation/Advanced/Prime tiers (Apr 2026) | AI Agent Studio / Orchestrator / Control Tower + Action Fabric (MCP); vendor-neutral ("open to Claude, Copilot, or homegrown agents") |
| **[SAP Joule Studio 2.0][sap-joule]** | "AI-first development environment" | proprietary; free design-time through 2026 (promotional), production terms TBD | NL goal → PRD + code + tests + multi-agent orchestration *at design time*; part of the SAP Business AI Platform ("the Autonomous Enterprise", Sapphire 2026) |
| **[Databricks Genie][genie]** | "agentic data coworker" | proprietary managed; OSS lakehouse base (Spark / Delta / Iceberg) | Genie Ontology semantic graph as the persistent context "kernel"; Genie Agents as reusable autonomous workflows |
| **[Glean Independent Agents][glean]** | "AI coworkers" | not stated in the announcement | Distinct per-agent identity + persistent memory; proactive/event-triggered action (parallel to Copilot Studio's autonomous agents) across Slack/Jira/Teams — still admin-configured, not autonomous goal origination; first instance is the OnCall Assistant (beta) |
| **[Lyzr Agent Studio][lyzr-docs]** (+ Lyzr ADK, [Opencontroller][lyzr-opencontroller] (marketing page, no docs)) | enterprise agent builder with a governance control plane | proprietary; deploys as SaaS, on-premise in your VPC, or hybrid; Build tier $0, governance and workflow tiers custom, fixed-scope proof of concept $20,000; "No token billing: you pay your model provider directly" ([pricing][lyzr-pricing]) | no-code studio plus a Python SDK (`pip install lyzr-adk`); model-agnostic, Claude listed in the [ADK model table][lyzr-adk]; MCP client, with only its Cognis memory exposed as an MCP server ([MCP docs][lyzr-mcp]); A2A both ways, calling LangGraph/CrewAI/Semantic Kernel agents as sub-agents ([A2A docs][lyzr-a2a]) |

**Lyzr caveat** (added 2026-11-14): unlike the rest of the tier it also runs on-premise or hybrid, so "proprietary SaaS" above reads as "proprietary" for Lyzr. Its MCP and A2A support are documented first-party; its AG-UI posture was not checked. Compliance certifications and adoption figures on its site are vendor claims, not verified here. The public `LyzrCore` GitHub repos are small side projects; the most-starred, `lyzr-automata`, has no LICENSE file and is not the platform.

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
  reasoning-model tokens 10 credits per 1,000 tokens ([billing rates][cs-billing-rates], ms.date 2026-10-30).
  Employee-facing use by a Microsoft 365 Copilot-licensed user costs no credits only if the agent runs under that
  user's own identity (footnote 1), and computer-using agents are not included (footnote 4).
- **Microsoft credit price:** "PayGo is priced at $0.01 per Copilot Credit", quoted in the analysis's
  [Cowork section][ms-cowork] from Microsoft's GA blog (2026-06-16); the Managed Runtime FAQ gives the same
  rate ([MS Managed Runtime][ms-managed-runtime], accessed 2026-11-10). Applying it to Copilot Studio is an assumption.
- **Not confirmed:** a WebFetch summary of Microsoft's pricing pages ([enterprise][m365-pricing-ent],
  [Copilot Studio][m365-pricing-cs]) showed a $30.00 seat and a $200-per-pack, 25,000-credit pack. These were not
  confirmed from raw text on 2026-11-20 (the pages refuse non-browser fetchers), no currency was seen, and they are not
  used in the math below.
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
| Employee user licence | Scenario 1, users not Copilot-licensed or agent autonomous: credits as above. Scenario 2, licensed users under their own identity: no credits; seat price unconfirmed | 500 x $5 = $2,500 on top, as the licence requires Flex Credits (both "$", currency not stated on the fetched summary) |

Not captured: base suites and seats, Agent 365, Max Edition and add-ons, overage and enforcement rules, reasoning-token
charges, prompt/LLM rows and Data 360 on the rate card, discounts, commitments, other currencies, and the fair-use
limits. Salesforce's page says to contact sales for detailed pricing. Treat every figure as a snapshot, as both
analyses' Pricing sections ask.

## Tier 2 — Open-source self-operating workspaces & runtimes

The OSS layer gives you the runtime instead of a managed platform. Most already have a dedicated analysis (HugAgentOS does not yet); they are gathered here for the pattern:

- **[AutoAgent][autoagent]** (HKUDS, MIT) — explicitly an "autonomous Agent Operating System": a self-managing file system, an LLM-powered actionable engine, and self-play customization that generates its own tools and agents at runtime inside a Docker sandbox. The closest literal "agent OS" in this corpus.
- **[Odysseus][odysseus]** (AGPL-3.0) — self-hosted all-in-one AI workspace (chat, agents, deep research, email, calendar, notes) in one Docker Compose deploy with MCP integration — the breadth-over-depth "operating environment" model.
- **[Goose][goose]** (AAIF / Linux Foundation, Apache-2.0) — MCP co-creator and reference implementation; extensions *are* MCP servers and ACP handles agent-to-agent/IDE messaging — the protocol-native runtime an agent OS is built on.
- **multica** (in [agent-frameworks-infrastructure-landscape §1][frameworks]; source-available, modified Apache-2.0 — not OSI) — turns coding-agent CLIs into managed teammates: issues route to an agent or squad, a local daemon executes with autopilot (cron/webhook) scheduling.
- **[HugAgentOS][hugagentos]** (ZJU-REAL; source-available: Apache-2.0 + Additional Terms — no competing multi-tenant SaaS offering, "Powered by" UI attribution required without a commercial white-label license; not OSI) — self-hosted "AgentOS" combining agentic chat, private RAG knowledge bases, sub-agents, sandboxed code execution, long-term memory, and automation; treats **domain ontology as a control plane** for agent reasoning, decisions, and tool execution — governed concepts/relations/rules/action-contracts, with versioned ontology proposals and audit logs for traceable evolution.
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

## Sources

| Source | Content |
|---|---|
| [M365 Copilot pricing][m365-pricing-ent], [Copilot Studio pricing][m365-pricing-cs], [billing rates][cs-billing-rates], [Agentforce pricing][agentforce-pricing], [Flex Credits rate card][sf-rate-card] | Rates for the worked example; Learn billing rates, the rate card and the Salesforce pricing page confirmed from raw text 2026-11-20; Microsoft pricing pages via WebFetch summary only |
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
| [AutoAgent][autoagent] · [Odysseus][odysseus] · [Goose][goose] · [multica][frameworks] · [HugAgentOS][hugagentos] · [Octop][octop] | OSS self-operating workspaces / runtimes (in-corpus analyses + HugAgentOS repo) |
| [polyforge-orchestrator][polyforge] · [office-forge-orchestrator][office-forge] · [liminal-flux-gh-acc][liminal] | qte77 estate self-operating orchestrators (public repos) |

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
[hugagentos]: https://github.com/ZJU-REAL/HugAgentOS
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
