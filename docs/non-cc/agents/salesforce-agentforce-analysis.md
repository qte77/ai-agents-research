---
title: Salesforce Agentforce 360 Analysis — Claude on Bedrock, Agentforce Registry, Agent Script, Pricing
purpose: First-party fact-check of Salesforce Agentforce 360 (platform scope, Claude via Amazon Bedrock inside the Salesforce trust boundary, Agentforce Registry / MuleSoft Agent Fabric, Agent Script / Agentforce DX, Flex Credits pricing, EU Operating Zone, data-masking behavior for agents) against Salesforce's own documentation, press releases, and rate card.
created: 2026-11-12
updated: 2026-11-12
validated_links: 2026-11-12
status: assess
---

**Details:** Salesforce ships Agentforce 360 as a family of separately versioned pieces — the
Agentforce 360 Platform, the new Agentforce Builder (Canvas/Script views), Agent Script, Data 360,
Headless 360, the Agentforce Registry, and the MuleSoft-branded Agent Fabric — plus "Claudeforce," a
2026-08-26 partnership layer that is Anthropic-branded but not a Salesforce product name of its own.
No single version string or GA date applies to "Agentforce 360" as a whole; each piece below carries
its own first-party date and status.

## TL;DR

- **Agentforce 360 reached general availability 2025-10-13**: "Agentforce 360 is available globally
  today, with continued innovation arriving in pilot and beta over the coming months"
  [sf-360-ga]. Individual components (Agentforce Builder, Agent Script, Agentforce Vibes, Data 360)
  carry no separate GA/beta label on that same page — only the platform as a whole does.
- **The "masking disabled for agents" claim is correct and not actually in conflict with anything.**
  Salesforce's own help article states plainly: "pattern-based and field-based data masking for
  large language models (LLMs) is disabled for agents" [masking-agents]. A 2025-06-10 Salesforce
  blog post explains the scope: masking stays on for out-of-the-box features (Service Replies, Field
  Summaries) and for prompt templates run *directly* through Prompt Builder or Flow — it turns off
  only when that same template is invoked *through an agent action* [masking-blog] [masking-agents].
  This holds even when the model is Claude running inside the Salesforce trust boundary: "Data
  masking remains disabled for agents in this case, but the data stays within the Salesforce trust
  boundary" [masking-agents]. See [Data Masking](#data-masking-and-the-einstein-trust-layer-for-agents).
- **Claude sits inside Salesforce's own trust boundary via Amazon Bedrock**, a posture Salesforce's
  own press release frames as a first: "Anthropic is the first LLM provider fully integrated within
  the Salesforce trust boundary, with all of Claude's traffic contained in the Salesforce virtual
  private cloud" [sf-anthropic-1014] — a "first" claim attributed to that 2025-10-14 announcement,
  not independently verified against competing vendors here. See
  [Claude inside the trust boundary](#claude-inside-salesforces-trust-boundary-via-amazon-bedrock).
- **The developer-docs model catalog is far richer than a single "AWS-Hosted" toggle.** The same
  page that describes a simple "Salesforce Default vs. AWS-Hosted" admin choice ("The AWS-Hosted
  option uses Anthropic Claude Sonnet 4 on Amazon Bedrock" [dev-models]) also lists at least seven
  individually selectable Claude variants under "Salesforce Trust Boundary" (Haiku 4.5, Haiku 5.5,
  Sonnet 4.5, Sonnet 4.6, Sonnet 5, Sonnet 5.5, Opus 5.5) [dev-models] — the one-line summary and the
  full table on the *same page*, read the same day, don't agree with each other. Treat the
  single-model framing as probably stale, not as the current admin-UI truth. Not resolved further in
  this pass — see [Unverified](#what-this-pass-did-not-settle).
- **Salesforce's own documentation disagrees with itself on whether Agentforce agents have direct
  A2A support.** An architect.salesforce.com recipe states, as its premise, "In the absence of
  direct A2A support on Agentforce Agents" [agentic-patterns], and MuleSoft's own A2A-bridge
  documentation agrees: "Salesforce Agentforce agents and Microsoft Copilot Studio agents, aren't
  A2A-compliant on their own" [a2a-bridge]. But Salesforce's own Agentforce interoperability guide
  contradicts both: "Agentforce A2A Outbound is the native way for Agentforce agents to collaborate
  directly with a third party agent," and "A2A Inbound allows external third-party agents to
  natively call upon the specialized skills and data of an Agentforce agent" [interop-guide]. None of
  the three pages carries a date or a GA/preview/beta label. **Presented here as an open
  contradiction inside Salesforce's own documentation, not resolved in this pass** — see
  [Unverified](#what-this-pass-did-not-settle).
- **The Flex Credits Rate Card cited here is the 2026-11-03 version** ("Updated as of November 3,
  2026" [rate-card]), which supersedes the 2026-08-18 version an earlier draft of this doc cited
  [rate-card-aug]; the multipliers common to both are unchanged, but November adds new rows (IT/HR
  Employee Agent Resolutions, a Sales category, a Slack Workspace section) — see
  [Pricing](#pricing-flex-credits-rate-card-as-of-2026-11-03). Salesforce republishes this PDF at the
  same URL pattern periodically; re-check the current file before quoting any multiplier in a budget.
- **The Hyperforce EU Operating Zone's own pages do not name Agentforce** anywhere this pass checked
  — not a stated exclusion, just a documented silence (see
  [EU Operating Zone](#eu-operating-zone-hyperforce)), the same "absence, not refutation" shape the
  companion Microsoft 365 Copilot analysis uses for SharePoint Skills and Agent 365.

## Scope

First-party research pass on **2026-11-12**: Salesforce's own press releases, developer docs
(`developer.salesforce.com`), Salesforce Help (`help.salesforce.com`), the architecture
reference site (`architect.salesforce.com`), the `salesforce/agentscript` GitHub repository, and the
2026-08-18 Flex Credits Rate Card PDF. `developer.salesforce.com` and `help.salesforce.com` serve a
JS-rendered shell to a plain fetch; pages under those hosts were rendered with
[polyfetch-scrape][polyfetch]'s Patchright tier and the extracted text greped for the relevant
passage. Covers: Agentforce 360 and its component products; Claude's placement inside the Salesforce
trust boundary via Amazon Bedrock and the Claudeforce partnership; the Agentforce Registry (MCP
server registration, risk scoring) and the separately-branded MuleSoft Agent Fabric; Agent Script and
Agentforce DX as the pro-code developer surface; the Flex Credits rate card; the Hyperforce EU
Operating Zone; data-masking behavior for agent actions; and the Agent Development Lifecycle best
practices.

**Explicitly out of scope / not independently re-verified here:** Koa (the CRM reasoning model),
long-horizon agents/"Hunter", Agent Optimizer, Superagent, AI Skills, third-party orchestration, and
other Dreamforce 2026 announcements named only in prior secondary research notes — none of these are
claimed as fact below; see [Unverified](#what-this-pass-did-not-settle). Cross-vendor comparison
(Microsoft 365 Copilot, ServiceNow, SAP Joule, Databricks Genie) is covered at the survey level in
[agentic-enterprise-os-landscape.md](../frameworks/agentic-enterprise-os-landscape.md), not repeated
here.

## Products and Timeline: what "Agentforce 360" comprises

- **Agentforce 360 Platform** — "the foundation for enterprise-grade AI agents, now featuring a new
  conversational builder" [sf-360-ga], GA 2025-10-13.
- **Agentforce Builder** (the new, conversational one — the GA press release does not use the name
  "Agent Builder") — "a new conversational development studio that lets teams design, test, and
  deploy agents using natural language" [sf-360-ga]. It has two views: build with "natural language
  in Canvas view" or "write directly in Script view" [builder-migration], and edits in either view
  carry over to the other. **Starting the week of July 13, 2026, agent creation moved exclusively to
  the new builder**: "Starting the week of July 13, 2026, agent creation will move exclusively to the
  new builder" [builder-migration]. Agents already built on the legacy builder "will continue to work
  and remain editable" [builder-migration] — legacy agents are not shut down, only new creation there
  stops.
- **Agent Script** — the DSL that Agentforce Builder's Script view writes directly, and that
  Agentforce DX deploys as metadata (see [Agent Script and Agentforce DX](#agent-script-and-agentforce-dx)).
  "Developers can define guardrails, tool use, and logic using Agent Script" [sf-360-ga].
- **Agentforce Vibes** — "extends low-code development to AI, letting builders 'vibe-code' apps
  grounded in company data and governance" [sf-360-ga].
- **Data 360** — "now activates a company's data, structured or unstructured, to give every agent
  business context" [sf-360-ga]; billed with its own volume-tiered Flex Credit multipliers (see
  [Pricing](#pricing-flex-credits-rate-card-as-of-2026-11-03)).
- **Headless 360** — announced 2026-04-15 [sf-headless360] (third-party event coverage ties this to
  TrailblazerDX (TDX) 2026, not independently confirmed on the press page itself): exposes
  Salesforce capability "as an API, MCP tool, or CLI command" [sf-headless360], bundling "more than
  60 new MCP tools and 30+ preconfigured coding skills" [sf-headless360] (the release's own appendix
  headline totals these as "100+ new tools and skills" [sf-headless360]). The announcement labels its
  availability only as "Available today" at the appendix level [sf-headless360], without a
  feature-by-feature GA/preview breakdown in the text read in this pass.
- **Claudeforce** — not a Salesforce product name on its own but the public name for the expanded
  Salesforce/Anthropic partnership announced 2026-08-26; see
  [Claude inside the trust boundary](#claude-inside-salesforces-trust-boundary-via-amazon-bedrock).
- **"Agent360"** is not a Salesforce name anywhere checked in this pass — it does not appear on any
  first-party page fetched here; treat any reference to it as a miscapture of "Agentforce 360."

## Claude inside Salesforce's trust boundary via Amazon Bedrock

Salesforce's 2025-10-14 announcement of an expanded Anthropic partnership states the integration in
Anthropic's own voice, quoted on Salesforce's press page: "Anthropic is the first LLM provider fully
integrated within the Salesforce trust boundary, with all of Claude's traffic contained in the
Salesforce virtual private cloud" [sf-anthropic-1014]. That page names the target sectors as
"financial services, healthcare, cybersecurity, and life sciences" [sf-anthropic-1014]. **This is a
"first" claim attributed to Anthropic/Salesforce's own announcement, not independently checked
against competing vendors' integration depth in this pass.**

**Claudeforce** (2026-08-26) expands this into several concrete roles [claudeforce]:

- Claude is "available in Agentforce, where it serves as a reasoning model for the Atlas Reasoning
  Engine," powers "Agentforce Vibes and Agentforce Coworker by default," and "is available in Agent
  Builder" [claudeforce].
- "Through Amazon Bedrock, Claude is available within the Salesforce Trust Boundary" [claudeforce] —
  the same mechanism as the 2025-10-14 announcement, now named explicitly as the Bedrock path.
- Claude "is the default model for Slack and powers Slackbot by default" [claudeforce].
- **"Salesforce in Claude"** — the reverse direction, Salesforce inside Anthropic's own Claude
  surface — ships "a Plugin with 37 prebuilt sales skills, including meeting prep, deal health
  review, and pipeline review," letting sellers "work with live revenue data and take governed
  actions from within Claude" [claudeforce]. Salesforce's own 2026-08-26 announcement put it at
  pilot stage, quoted verbatim: "Salesforce in Claude is available to select pilot customers now and
  expects to launch in open beta in September 2026" [claudeforce]. **Anthropic's own page confirms
  that beta shipped on schedule.** Dated 2026-09-15, it states: "Today we are releasing Salesforce in
  Claude in beta," and describes its reach more broadly than "select pilot customers": "Salesforce in
  Claude is available in beta on all paid Claude plans" [claude-in-claude].

**The model catalog is bigger than the simple admin toggle suggests.** Salesforce's developer docs
describe a simple binary at the org level: "The Salesforce Default model option for Agentforce is a
managed mix of trusted models (currently including GPT-4o) ... The AWS-Hosted option uses Anthropic
Claude Sonnet 4 on Amazon Bedrock" [dev-models]. The same page's full model table, read the same
session, lists at least seven separately selectable Claude variants under a "Salesforce Trust
Boundary" annotation: Claude Haiku 4.5, Claude Haiku 5.5, Claude Sonnet 4.5, Claude Sonnet 4.6,
Claude Sonnet 5, Claude Sonnet 5.5, and Claude Opus 5.5, each on Amazon Bedrock [dev-models] — plus
Amazon's own Nova Lite/Pro/2-Lite models under the same Trust Boundary label [dev-models]. The
single-sentence "AWS-Hosted = Sonnet 4" framing and the fuller per-model table read as two different
snapshots of the same catalog, not reconciled on the page itself — **not resolved further here**; see
[Unverified](#what-this-pass-did-not-settle).

**Atlas Reasoning Engine is constrained to Salesforce-managed models.** Per Salesforce's own
Agent Script recipe documentation: "The reasoning engine is limited: The Atlas reasoning engine is
constrained to Salesforce-managed models. However, custom actions using prompt templates, Apex, or
the Models API can reference" other configured models [atlas-model-config] — bring-your-own-LLM is
documented as available for custom actions/prompts, not for the reasoning engine itself.

## Agentforce Registry and MuleSoft Agent Fabric

Salesforce documents **two separately named registry/governance surfaces** for agent tooling, and
they are not the same mechanism:

1. **Agentforce Registry** (Setup → Agentforce Registry → MCP Servers) governs MCP tool
   registration for an org's own agents. Registering an external MCP server surfaces each discovered
   tool with a sync status — `IN_SYNC`, `OUT_OF_SYNC`, `NOT_REGISTERED` ("Salesforce found the tool on
   the remote server but hasn't yet added it to the allowlist" [mcp-registry]), or `ORPHANED` ("on the
   allowlist, but the remote server no longer advertises it" [mcp-registry]) — and only allowlisted
   tools become callable actions. A `securityWarning` field flags "characters that can signal a tool
   poisoning" risk — "mixed scripts that manipulate an Agentforce agent into unexpected behavior,"
   which "corresponds to the Risk Assessment panel shown during registration in the UI" [mcp-registry].
   The documentation page fetched for this (the API Catalog Connect REST API guide) carries no GA,
   preview, or beta label of its own.
2. **MCP Risk Score**, inside **Security Center**, is a different, tenant-wide feature shipped in the
   **Winter '27 (264) release** (blog dated 2026-10-13): "Security Center now surfaces a Low, Medium,
   or High risk score for every third-party MCP server," "scanned at registration and continuously
   monitored for change" [winter27-blog]. That same release post states as a blanket policy, "All
   features are generally available (GA) unless otherwise noted" [winter27-blog] — read as GA absent
   a feature-specific exception, though this pass did not check every individual Winter '27 feature
   page for such an exception.

**MuleSoft Agent Fabric** is a third, separately MuleSoft-branded layer, not the Agentforce Registry
above. Per the architect.salesforce.com deep dive [mulesoft-fabric]:

- **Agent Registry**: "provides a centralized catalog of all AI agents and tools across the
  organization" [mulesoft-fabric] — catalogs agents on MuleSoft or other platforms, MCP servers, and
  LLM providers, and documents support for A2A-compliant agents and MCP servers in its Exchange
  section.
- **Agent Broker**: "an intelligent routing solution that dynamically matches tasks to the best fit
  agent or tool" [mulesoft-fabric]; its own card follows the A2A specification and reaches external
  systems through MCP servers.
- **Agent Governance**: "utilizes Flex Gateway and its support for Model Context Protocol (MCP)"
  [mulesoft-fabric] and explicitly names the "Agent2Agent (A2A) protocol" [mulesoft-fabric] — the one
  component of the four whose description names both protocols directly.
- **Agent Visualizer**: "provides real-time observability through a dynamic, interactive map of agent
  interactions" [mulesoft-fabric].

None of the four component descriptions on that page carries a GA/preview/beta label; third-party
launch coverage from 2025 claimed an October 2025 GA for the Registry and Broker specifically, but
that is secondary coverage, not confirmed on the first-party page fetched here — **flagged
unconfirmed**, not asserted.

**A2A: Salesforce's own documentation disagrees with itself.** MuleSoft Agent Fabric's component
descriptions above name the A2A protocol explicitly, but whether *Agentforce Agents themselves* have
direct A2A support is not settled across Salesforce's own first-party pages checked in this pass:

- An architect.salesforce.com recipe for connecting agents states, as its premise, "In the absence
  of direct A2A support on Agentforce Agents" [agentic-patterns], and recommends a MuleSoft connector
  workaround to expose an agent as an A2A server instead.
- MuleSoft's own A2A-bridge documentation agrees with that premise: "Salesforce Agentforce agents and
  Microsoft Copilot Studio agents, aren't A2A-compliant on their own" [a2a-bridge]. For Agentforce
  specifically, "the Bridge translates A2A to the Agentforce Agent API" [a2a-bridge] — and on that
  path, "The Agentforce API doesn't support push notifications" [a2a-bridge].
- Salesforce's own Agentforce interoperability guide contradicts both of the above: "Agentforce A2A
  Outbound is the native way for Agentforce agents to collaborate directly with a third party agent"
  [interop-guide], and, for the reverse direction, "A2A Inbound allows external third-party agents to
  natively call upon the specialized skills and data of an Agentforce agent" [interop-guide].

None of the three pages carries a publication date or a GA/preview/beta label for the A2A capability
itself. **This is presented here as an unresolved contradiction inside Salesforce's own
documentation, in both directions, not as a settled fact** — see
[Unverified](#what-this-pass-did-not-settle).

## Agent Script and Agentforce DX

**Agent Script's authoring toolchain is open source; its runtime is not.** The
`salesforce/agentscript` GitHub repository states: "Apache 2.0 — see LICENSE.txt for the full text"
[agentscript-repo]. Its own README lists what's "genuinely open" as the parser, linter, LSP and
developer tooling, editor integrations (VS Code and Monaco), the UI playground, and the documentation
and formal spec [agentscript-repo] — and is explicit about the boundary: "What we're not open
sourcing (yet) is the runtime" [agentscript-repo]; compiled output runs only on Salesforce's own
infrastructure. The repository page carries no stated release date (only a copyright-footer year);
third-party event coverage ties the open-sourcing to TrailblazerDX (TDX) 2026 (April 15–16, 2026),
which also coincides with the Headless 360 announcement date above — **not independently confirmed
as the open-source release date on a first-party page in this pass.**

**Agent Script's own general-availability date could not be confirmed from a single first-party
page in this pass.** Secondary sources disagree (a developer how-to guide claims February 2026; a
release-note index references "Spring '26"; a Summer '26-dated guide implies a later milestone) — no
first-party Salesforce page naming "Agent Script" and a specific GA date together was found and
fetched in this pass. Treat any specific Agent Script GA date as unconfirmed.

**Agentforce DX** is the pro-code developer surface. Per Salesforce's own guide: "Agentforce DX
extends these tools [Salesforce CLI, VS Code extensions, Agentforce Vibes IDE, DevOps Center, scratch
orgs and sandboxes] to work with agents" and states the core design premise directly — "Agents are
metadata, just like any other Salesforce customization" [agent-dx]. The documented workflow: author
or edit an Agent Script file with VS Code or CLI commands, "generate and validate the authoring
bundle," preview the agent "in either simulated or live mode," publish, then "retrieve any metadata
changes you made in the org back to your DX project" and commit to version control [agent-dx].
Testing runs through "CLI commands, your org's Agentforce Testing Center UI, or testing APIs"
[agent-dx]. The guide documents activation and deployment to scratch orgs, sandboxes, and production
orgs, but this pass found no dedicated first-party "rollback" command for agent metadata — version
control and re-deploying an earlier committed version is the documented recovery path (see also
[Best Practices](#best-practices-agent-development-lifecycle) on agent versioning).

## Pricing: Flex Credits Rate Card (as of 2026-11-03)

The cited rate card PDF now states "Updated as of November 3, 2026" on its own last page
[rate-card]. An earlier draft of this doc cited the 2026-08-18 version of the same document
[rate-card-aug]; the multipliers the two versions share are unchanged, but the November version adds
several rows not present in August (listed below). **Salesforce republishes this PDF at the same URL
pattern periodically** (`salesforce.com/.../agentforce/Flex-Credits-Rate-Card-<date>.pdf`) — re-check
the current file before quoting any multiplier in a budget; the figures below are a dated snapshot,
not a standing price.

| Category | Usage type | Production multiplier | Sandbox multiplier |
|---|---|---|---|
| Agentforce Actions | Standard / Custom Action | 20 | 16 |
| Agentforce Voice Actions | Standard / Custom Voice Action | 30 | 24 |
| Bring Your Own LLM | Starter Prompts | 2 | 2 |
| Salesforce-enabled foundational LLMs | Basic Prompts | 2 | 2 |
| Salesforce-enabled foundational LLMs | Standard Prompts | 4 | 4 |
| Salesforce-enabled foundational LLMs | Advanced Prompts | 16 | 16 |
| Service | Help Agent Resolutions | 400 | 0 |
| Service | IT and HR Employee Agent Resolutions *(new since August)* | 400 | 0 |
| Sales | Customer Engagement / Leads Worked *(new since August)* | 400 | 320 |
| Speech Foundations | Speech to Text (per hour) | 150 | 150 |
| Speech Foundations | Text to Speech (per 1M chars) | 6,000 | 6,000 |
| Speech Foundations | Translation (per 1M chars) | 4,000 | 4,000 |
| Customer 360 Platform | Headless Platform Interaction *(collapses two prior TBA rows)* | TBA | — |
| Personalization | Personalization Decisioning (per 1K decisions) | 100 | 100 |
| Slack Workspace *(new since August)* | Slackbot Standard Action | 40 (flat, per workspace) | — |
| Slack Workspace *(new since August)* | Slackbot Advanced Action | 200 (flat, per workspace) | — |

All figures from [rate-card]. **New since the August 2026 version**: "IT and HR Employee Agent
Resolutions," at the same 400/0 rate as the existing Help Agent Resolutions row; a new Sales
category, "Customer Engagement / Leads Worked" (400 production / 320 sandbox); a new Slack Workspace
section, billed "per Slack Workspace" [rate-card], with a flat "Slackbot Standard Action" multiplier
of 40 and "Slackbot Advanced Action" at 200 (not split by production/sandbox); and the Customer 360
Platform section, which the August version listed as two separate TBA rows (Salesforce Record
Operation / CRUD, and Salesforce Process Invocation), is collapsed in November into a single
"Headless Platform Interaction" row, still TBA [rate-card].

Data 360 billing uses a separate, four-tier volume schedule (Base tier up to 300k credits, down to a
Tier 4 rate after 12.5M credits/month) across **eleven** usage types — Prep, Unification,
Segmentation, Activation, Zero-Copy Sharing-Out, Queries, Unstructured Processing, Intelligent
Processing, Streaming Pipeline, Real-Time Pipeline, and Code Extension [rate-card] (an earlier draft
of this doc undercounted these as "ten" by compressing two pairs — Unstructured/Intelligent
Processing and Streaming/Real-Time Pipeline — into one list item each; corrected here). See the rate
card directly for the full per-tier table; not reproduced here in full to avoid a second point of
drift from the source. Footnote 2 on the card restricts the "Salesforce-enabled foundational LLMs"
row to "Agentforce 1 Edition Customers and Agentforce for Sales/Service/Industries Customers and any
other Products that no longer use Einstein Requests" [rate-card].

**Current list prices**, from Salesforce's own pricing page, accessed 2026-11-12 [agentforce-pricing]:

- Flex Credits: "$500" per 100,000 credits (USD).
- Conversations: "$2" per conversation (USD).
- Agentforce add-ons: "$125" user/month; Agentforce Industries add-ons: "$150" user/month.
- **Max Edition**: "from $550" user/month, including "2.75M Flex Credits per org per year"
  [agentforce-pricing].
- **Agentforce User License**: "$5" USD/user/month (requires Flex Credits) [agentforce-pricing].
- **Agentforce Coworker User License**: "$50" USD/user/month [agentforce-pricing].
- Salesforce Foundations: "$0" [agentforce-pricing].
- **Flex Credits and Conversations cannot both be used in the same org.** The pricing page's own FAQ
  states this directly — question: "Can I use both Flex Credits and conversation pricing at the same
  time?"; answer: "No. Flex Credits and Conversations will not be supported in the same org."
  [agentforce-pricing]. An earlier draft of this doc dropped this claim as unverified; it is restored
  here, confirmed verbatim at source.

The pricing page fetched in this pass lists included credits only for Max Edition (2.75M/org/year);
it does not state separate included-credit figures for other editions. Earlier research notes cited
differing historical figures (1M for an "Agentforce 1" edition, 2.5M on a regional page) — **neither
was independently re-verified at source in this pass**; treat them as unconfirmed.

## EU Operating Zone (Hyperforce)

The Hyperforce EU Operating Zone is a paid, separately licensed add-on, now branded on its own FAQ
page's main heading simply as "Hyperforce Operating Zone" (the page's original
`data-residence-eu-oz` URL now redirects to a `public-cloud-infrastructure/operating-zone` path,
updated in the citation here [eu-oz-1]). That FAQ states scope only generically: "includes a select
set of products and features that have been vetted to meet the offering's strict obligations"
[eu-oz-1], and a product page adds: "These products span Sales Cloud, Service Cloud, the Salesforce
Platform, industries, and more" [eu-oz-2].

**Neither EU Operating Zone page checked in this pass names "Agentforce" or "Agentforce 360
Platform"** as included, and neither states which cloud infrastructure provider (AWS or otherwise)
underlies the zone, nor where LLM inference (including Claude on Amazon Bedrock) physically runs for
a tenant inside it [eu-oz-1] [eu-oz-2]. **This is a documented silence on both questions across the
two pages checked here, not a stated inclusion or a stated exclusion** — the same "absence, not
refutation" caveat the companion Microsoft 365 Copilot analysis applies to SharePoint Skills' silence
on Agent 365. A broader statement does exist at the Models API level, independent of the EU
Operating Zone specifically: "A geo-aware model minimizes latency by automatically routing your LLM
request to a nearby data center based on where Data 360 is provisioned for your org," naming "Amazon
Bedrock: Anthropic Claude," "Azure OpenAI," "OpenAI," and "Vertex AI (Google)" as the providers this
applies to [dev-models] — this describes general geo-aware routing, not an EU-Operating-Zone-specific
residency guarantee, and was not cross-checked against the EU Operating Zone pages directly.

## Data Masking and the Einstein Trust Layer for agents

Salesforce's own help article, titled "Data Masking Limitations in Agentforce" (fetched via
polyfetch, since this page serves a JS-only shell to a plain fetch), states the core fact plainly: "In
Einstein Trust Layer, pattern-based and field-based data masking for large language models (LLMs) is
disabled for agents" [masking-agents]. The article gives the documented reason: "masking can help
protect sensitive and personally identifiable information from exposure to the LLMs, in some cases,
it can affect the accuracy and relevance of the agent's response because the context needed for the
response is masked" [masking-agents], with a worked example (a masked reference account loses the
detail an agent needs to find similar accounts).

**This is not actually in conflict with other Trust Layer documentation once scope is accounted
for** — both the help article and a 2025-06-10 Salesforce blog post describe the same split:

- **Disabled**: any time a prompt template or the reasoning engine runs *through an agent action*.
  "When a prompt template is called through an agent action, data masking is disabled"
  [masking-agents].
- **Still enabled**: out-of-the-box generative features and prompt templates run *directly*, outside
  an agent action. "When a prompt template is used directly, for example, in service replies, data
  masking is applied based on the configuration in the Einstein Trust Layer" [masking-agents]. The
  blog states the same split from the product-history side: "Out-of-the-box generative AI features
  such as Service Replies and Field Summaries will continue to apply data masking" and "data masking
  will also remain enabled for prompt templates executed within Prompt Builder or via Flow"
  [masking-blog], tracing the agent-specific change to "last year" (i.e., 2024, from the post's
  2025-06-10 publication date) [masking-blog] and citing reported "accuracy degradation in agent
  responses when masking is enabled" as the stated motivation [masking-blog].
- **This holds even for Claude inside the trust boundary.** The help article addresses this directly:
  "When using an LLM hosted within the Salesforce trust boundary, the data doesn't leave the
  Salesforce trust boundary. Data masking remains disabled for agents in this case, but the data
  stays within the Salesforce trust boundary, and our zero data retention policy still applies"
  [masking-agents] — i.e., Salesforce's documented compensating control for agent actions is the
  trust-boundary/zero-retention contract, not masking.

A separate, distinct protection surface appears in the same help site's navigation but was not
examined further in this pass: "Mask Protected Data in Agentforce Session Logs (Beta)" — this masks
protected data in session/observability logs after the fact, a different mechanism from the pre-send
masking discussed above, and its beta status and mechanics are **not verified beyond the navigation
label** found during this fetch.

## Best Practices: Agent Development Lifecycle

Salesforce's architecture reference site documents a five-phase Agent Development Lifecycle (ADLC)
[adlc]:

1. **Ideation and Design** — "the foundational phase where an agent's strategic purpose and
   operational boundaries are defined" [adlc].
2. **Development** (the "inner loop") — "the hands-on construction phase where the design blueprint
   is turned into a functional agent," in Agent Builder, Agentforce DX, and the Python SDK [adlc].
3. **Testing and Validation** — explicitly framed as a departure from traditional software testing:
   "Testing AI agents introduces a paradigm shift from the deterministic validation of traditional
   software" [adlc], combining unit, end-to-end, adversarial, human-in-the-loop, and scale testing.
   Sandbox use is called out directly: testing should "always" happen in a non-production
   environment such as "a copy of a production environment, offering a more realistic testing
   ground" [adlc], because agents can modify CRM data.
4. **Deployment** — "a managed process focused on ensuring the validated agent is what users
   interact with" [adlc]: packaging, CI/CD, and phased rollout. Version control is explicit: agent
   definitions are "stored in a source control system like Git" [adlc], with agent versioning that
   lets teams test a new version without affecting the live one and roll back to a prior version.
   Rollout is gradual by design: "new agent versions are released to a small subset of users first
   using strategies like Canary Releases" [adlc]. Activation is a distinct, explicit gate: "it is
   imperative for a system administrator to actively 'activate' the agent" [adlc], and a new version
   "doesn't go live until you explicitly activate it" [adlc] — the page does not describe a separate
   formal multi-party approval workflow beyond this activation step and the CI/CD pipeline's own
   end-to-end tests, which "act as a quality gate" at each stage [adlc].
5. **Monitoring and Tuning** (the "outer loop") — "not the end of the Agent Development Lifecycle; it
   is the beginning of its continuous 'outer loop'" [adlc]: performance tracking, analytics, tuning,
   and retrieval-augmented-generation refinement.

## Trajectory

Dated milestones independently fetched and quoted in this pass:

| Date | Item | Source |
|---|---|---|
| 2025-10-13 | Agentforce 360 reaches general availability | [sf-360-ga] |
| 2025-10-14 | Anthropic/Salesforce regulated-industries expansion; "first LLM provider fully integrated within the Salesforce trust boundary" | [sf-anthropic-1014] |
| 2026-04-15 | Headless 360 announced (60+ MCP tools, 30+ coding skills) | [sf-headless360] |
| 2026-07-13 (week of) | New agents can only be created in the new Agentforce Builder; legacy agents keep running | [builder-migration] |
| 2026-08-26 | Claudeforce: Claude as Atlas reasoning model, default for Vibes/Coworker/Slack, via Bedrock inside the trust boundary; "Salesforce in Claude" plugin (37 skills) pilot | [claudeforce] |
| 2026-08-18 | Flex Credits Rate Card, an earlier version this doc previously cited, "Updated as of August 18, 2026" | [rate-card-aug] |
| 2026-09-15 | Anthropic's own page confirms "Salesforce in Claude" shipped in beta "on all paid Claude plans" | [claude-in-claude] |
| 2026-10-13 | Winter '27 (264) release post; MCP Risk Score in Security Center; "all features are GA unless otherwise noted" | [winter27-blog] |
| 2026-11-03 | Flex Credits Rate Card, the version cited in this doc, "Updated as of November 3, 2026" | [rate-card] |

**Earlier milestones carried from prior secondary research notes, not independently re-fetched in
this pass** — presented for orientation only, each unconfirmed at first-party source here: Agentforce
general availability (cited as 2024-10-29), Agentforce 2.0 (2024-12-17), Flex Credits' own launch
(2025-05-15), and Agentforce 3 with Command Center and an MCP client pilot (2025-06-23). Treat these
four as background context, not as verified facts of this analysis.

## Announced vs. Shipped

| Item | Announced (date + source) | Status (GA/beta/preview + source) |
|---|---|---|
| Agentforce 360 (platform) | 2025-10-13 [sf-360-ga] | GA, self-stated: "available globally today" [sf-360-ga]; components continue arriving "in pilot and beta over the coming months" [sf-360-ga] |
| New Agentforce Builder (Canvas/Script) | 2025-10-13 [sf-360-ga] | Mandatory for new agents from the week of 2026-07-13; legacy builder stays usable, not shut down [builder-migration] |
| Agent Script authoring toolchain (parser/linter/LSP/editor/playground) | Tied by secondary coverage to TDX 2026 (2026-04-15/16); no date on the repo page itself | Apache-2.0, open [agentscript-repo]; runtime explicitly NOT open-sourced [agentscript-repo]; product-wide GA date for Agent Script itself **unconfirmed** — no single first-party page found naming both the feature and a GA date |
| Headless 360 | 2026-04-15 [sf-headless360] | "Available today" at the appendix level [sf-headless360]; no feature-by-feature GA/preview breakdown read in this pass |
| MuleSoft Agent Fabric (Registry/Broker/Governance/Visualizer) | Documented on an undated architect.salesforce.com page [mulesoft-fabric] | No GA/preview/beta label on the page itself; third-party 2025 launch coverage claims October 2025 GA for Registry+Broker — **secondary-only, unconfirmed here** |
| Agentforce Registry (Setup MCP registration, Risk Assessment panel) | Documented in an undated API Catalog ConnectAPI guide [mcp-registry] | No GA/preview/beta label on the page fetched |
| MCP Risk Score (Security Center) | Winter '27 (264) release post, 2026-10-13 [winter27-blog] | Stated GA per the release's blanket "GA unless otherwise noted" policy [winter27-blog]; not individually re-checked for an exception |
| Claude via Amazon Bedrock inside the Salesforce Trust Boundary | 2025-10-14 [sf-anthropic-1014] | Mixed by sub-scope, on a single page, directly fetched and re-checked: "Agentforce powered by Anthropic is available today for select customers" and "Claude and Slack bi-directional integrations are available today" [sf-anthropic-1014] — but "the new collaboration on regulated industry solutions and the Agentforce 360 integration for Claude are currently under development, with more details on availability to be shared in the coming months" [sf-anthropic-1014]. One announcement, two sub-scopes at different maturity — not two disagreeing copies, as an earlier draft of this doc framed it |
| Claudeforce / "Salesforce in Claude" (37 prebuilt skills) | 2026-08-26 [claudeforce] | Pilot customers at announcement; "expects to launch in open beta in September 2026" [claudeforce] — confirmed shipped on schedule by Anthropic's own 2026-09-15 page: "Today we are releasing Salesforce in Claude in beta," "available in beta on all paid Claude plans" [claude-in-claude] |
| Data masking disabled for agent actions | Standing documented behavior, traced to "last year" (2024) by a 2025-06-10 post [masking-blog] | Current and documented [masking-agents] [masking-blog] — not a conflict once the agent-action vs. direct-template scope is applied |
| Direct A2A protocol support on Agentforce Agents | n/a | **Contradicted across Salesforce's own documentation.** The agentic-patterns recipe ("In the absence of direct A2A support on Agentforce Agents" [agentic-patterns]) and MuleSoft's own A2A-bridge doc ("aren't A2A-compliant on their own" [a2a-bridge]) agree there is no native support; Salesforce's own Agentforce interoperability guide calls "Agentforce A2A Outbound... the native way for Agentforce agents to collaborate directly with a third party agent" and describes a native Inbound path too [interop-guide]. None of the three pages carries a date or status label — unresolved, not settled |
| Flex Credits vs. Conversations combinability | n/a | Settled: "No. Flex Credits and Conversations will not be supported in the same org" [agentforce-pricing] — restored after an earlier draft of this doc dropped it as unverified |

## What this pass did not settle

- **The "AWS-Hosted" model identity** — the developer-docs prose line names Claude Sonnet 4
  [dev-models] while the same page's full model table lists many more individually selectable Claude
  variants under the same Trust Boundary heading; a specific `help.salesforce.com` admin-setting
  article (the kind that would show the live admin-UI label) could not be located and fetched in this
  pass. Treat the single-model framing as possibly stale, not as confirmed current behavior.
- **Edition-level included-credit figures** other than Max Edition's 2.75M/org/year [agentforce-pricing]
  — prior notes cite 1M and 2.5M for other editions/regions/years; neither re-verified at source here.
- **Pre-2025-10 trajectory dates** (Agentforce GA 2024-10-29, Agentforce 2.0 2024-12-17, Flex Credits
  launch 2025-05-15, Agentforce 3 2025-06-23) — carried from prior secondary research notes only, not
  independently re-fetched in this pass.
- **"Agents callable as MCP tools" as a Winter '27 feature** — appeared in prior triage notes; not
  found on the Winter '27 platform-release blog fetched in this pass [winter27-blog]. Unconfirmed.
- **A Gemini model option inside Agentforce's model picker** — appears only in third-party blog
  snippets and a secondary search summary in this pass, never on a first-party page fetched directly.
  Dropped as unverified.
- **Where Claude-on-Bedrock inference physically runs for an EU Operating Zone tenant** — absence
  confirmed across the two EU OZ pages checked (see [EU Operating Zone](#eu-operating-zone-hyperforce));
  not stated on either page, in either direction.
- **Dreamforce 2026 product statuses** (Koa GA timing, long-horizon agents/"Hunter," Agent Optimizer,
  Superagent, AI Skills, third-party orchestration) — out of scope for this pass; see
  [Scope](#scope).
- **Direct A2A protocol support on Agentforce Agents** — Salesforce's own documentation disagrees
  with itself (see [A2A](#agentforce-registry-and-mulesoft-agent-fabric) above): the agentic-patterns
  recipe [agentic-patterns] and MuleSoft's own A2A-bridge doc [a2a-bridge] both premise "no direct A2A
  support," while the Agentforce interoperability guide [interop-guide] calls Outbound "the native
  way" and describes a native Inbound path too. None of the three pages carries a date or status
  label. Left as an open contradiction, not resolved either way in this pass.

## Cross-References

- [agentic-enterprise-os-landscape.md](../frameworks/agentic-enterprise-os-landscape.md) — the
  survey-level "agentic enterprise OS" row this doc extends with first-party pricing (the rate card),
  Agentforce Registry/MuleSoft Agent Fabric governance detail, and the Claude/Bedrock posture; its own
  Salesforce row should cite the dated rate card here rather than restate a snapshot figure on its own.
- [ag-ui-protocol-landscape.md](../protocols/ag-ui-protocol-landscape.md) — covers Salesforce's
  non-adoption of AG-UI in favor of an MCP/MuleSoft-centered strategy; this doc adds the MuleSoft
  Agent Fabric component breakdown and the A2A contradiction inside Salesforce's own documentation
  behind that strategy.
- [CC-business-api-integrations.md § Salesforce](../../cc-native/plugins-ecosystem/CC-business-api-integrations.md)
  — Salesforce's own Hosted MCP Servers reaching GA 2026-04-29, from the Claude Code integration
  angle; this doc covers the same registry/MCP surface from the Agentforce platform side.
- [microsoft-365-copilot-analysis.md](microsoft-365-copilot-analysis.md) — a comparable enterprise
  agent-platform analysis; both place Claude behind a vendor-operated trust boundary with distinct,
  vendor-specific contractual postures (Salesforce's single Bedrock-based trust boundary here vs.
  Microsoft's three different subprocessor/Foundry postures there), and both apply the same
  "documented silence is not a stated exclusion" caveat to a residency question (EU Operating Zone
  here, the EU Data Boundary there).

## Sources

| Source | Content |
|---|---|
| [Agentforce 360 GA announcement][sf-360-ga] | 2025-10-13 GA statement; Agentforce Builder, Agent Script, Vibes, Data 360 descriptions |
| [Anthropic/Salesforce regulated-industries announcement][sf-anthropic-1014] | 2025-10-14; "first LLM provider fully integrated within the Salesforce trust boundary" |
| [Claudeforce announcement][claudeforce] | 2026-08-26; Claude's roles across Atlas, Vibes, Coworker, Agent Builder, Slack; "Salesforce in Claude" plugin |
| [Headless 360 announcement][sf-headless360] | 2026-04-15; MCP tools/skills counts, "Available today" |
| [New Agentforce Builder migration page][builder-migration] | Canvas/Script views; 2026-07-13 mandatory-new-builder cutover; legacy agents keep running |
| [Supported Models (developer docs)][dev-models] | Salesforce Default vs. AWS-Hosted framing; full Trust-Boundary Claude model table; geo-aware routing providers |
| [Agent Script model-config recipe][atlas-model-config] | Atlas Reasoning Engine constrained to Salesforce-managed models; BYO scope |
| [salesforce/agentscript GitHub repo][agentscript-repo] | Apache-2.0 toolchain; runtime explicitly excluded |
| [Agentforce DX guide][agent-dx] | CLI/VS Code workflow; agents as metadata; retrieve/deploy/activate/test |
| [MuleSoft Agent Fabric deep dive][mulesoft-fabric] | Agent Registry/Broker/Governance/Visualizer component descriptions; MCP + A2A |
| [Agentic patterns recipe][agentic-patterns] | "In the absence of direct A2A support on Agentforce Agents" |
| [MuleSoft A2A bridge guide][a2a-bridge] | "Salesforce Agentforce agents ... aren't A2A-compliant on their own"; bridge mechanics; no push notifications |
| [Agentforce interoperability guide][interop-guide] | "Agentforce A2A Outbound is the native way..."; A2A Inbound description — contradicts the two sources above |
| [Manage external MCP servers (API Catalog ConnectAPI)][mcp-registry] | Agentforce Registry mechanics; tool-poisoning security warning; allowlist sync states |
| [Winter '27 platform release post][winter27-blog] | 2026-10-13; MCP Risk Score; "264" release numbering; blanket GA policy |
| [Flex Credits Rate Card, 11.3.2026][rate-card] | Full multiplier table; "Updated as of November 3, 2026"; new rows vs. the August version |
| [Flex Credits Rate Card, 08.18.2026 (superseded)][rate-card-aug] | The earlier version this doc previously cited as primary |
| [Agentforce pricing page][agentforce-pricing] | Current list prices, accessed 2026-11-12; Flex Credits/Conversations non-combinability FAQ |
| [Hyperforce Operating Zone FAQ][eu-oz-1] | "select set of products and features ... vetted"; no Agentforce/cloud-provider statement (URL redirected since original fetch) |
| [Hyperforce EU Operating Zone product page][eu-oz-2] | Product-scope statement: "Sales Cloud, Service Cloud, the Salesforce Platform, industries, and more" |
| [Data Masking Limitations in Agentforce (Salesforce Help)][masking-agents] | Verbatim masking-disabled-for-agents statement and trust-boundary clause |
| [LLM data masking blog, 2025-06-10][masking-blog] | Scope split: agent actions vs. direct prompt templates/out-of-the-box features |
| [Agent Development Lifecycle][adlc] | Five-phase ADLC; sandbox testing, Git versioning, canary rollout, explicit activation |
| ["Salesforce in Claude" (Anthropic), 2026-09-15][claude-in-claude] | Confirms beta shipped: "available in beta on all paid Claude plans" |
| [polyfetch-scrape USING.md][polyfetch] | Fetch tooling used for JS-rendered `developer.salesforce.com` / `help.salesforce.com` pages |

[sf-360-ga]: https://www.salesforce.com/news/press-releases/2025/10/13/agentic-enterprise-announcement/
[sf-anthropic-1014]: https://www.salesforce.com/news/press-releases/2025/10/14/anthropic-regulated-industries-partnership-expansion-announcement/
[claudeforce]: https://www.salesforce.com/news/press-releases/2026/08/26/salesforce-and-anthropic-announce-claudeforce/
[sf-headless360]: https://www.salesforce.com/news/stories/salesforce-headless-360-announcement/
[builder-migration]: https://www.salesforce.com/agentforce/agent-builder/migration/
[dev-models]: https://developer.salesforce.com/docs/ai/agentforce/guide/supported-models.html
[atlas-model-config]: https://developer.salesforce.com/sample-apps/agent-script-recipes/architectural-patterns/model-config
[agentscript-repo]: https://github.com/salesforce/agentscript
[agent-dx]: https://developer.salesforce.com/docs/ai/agentforce/guide/agent-dx.html
[mulesoft-fabric]: https://architect.salesforce.com/fundamentals/mulesoft-agent-fabric-deep-dive
[agentic-patterns]: https://architect.salesforce.com/fundamentals/agentic-patterns
[a2a-bridge]: https://docs.mulesoft.com/general/exp-services-create-a2a-bridge
[interop-guide]: https://www.salesforce.com/agentforce/resources/interoperability-guide/
[mcp-registry]: https://developer.salesforce.com/docs/platform/api-catalog-connectapi/guide/manage-external-mcp-servers.html
[winter27-blog]: https://www.salesforce.com/blog/platform-winter-27-release/
[rate-card]: https://www.salesforce.com/en-us/wp-content/uploads/sites/4/assets/pdf/agentforce/Flex-Credits-Rate-Card-11.3.2026.pdf
[rate-card-aug]: https://www.salesforce.com/en-us/wp-content/uploads/sites/4/assets/pdf/agentforce/Flex-Credits-Rate-Card-08.18.2026.pdf
[agentforce-pricing]: https://www.salesforce.com/agentforce/pricing/
[eu-oz-1]: https://www.salesforce.com/platform/public-cloud-infrastructure/operating-zone/
[eu-oz-2]: https://salesforce.com/eu/products/platform/hyperforce/hyperforce-eu-oz
[masking-agents]: https://help.salesforce.com/s/articleView?id=ai.agent_trust_data_masking.htm&type=5
[masking-blog]: https://www.salesforce.com/blog/llm-data-masking/
[adlc]: https://architect.salesforce.com/fundamentals/agent-development-lifecycle
[claude-in-claude]: https://claude.com/resources/articles/salesforce-in-claude
[polyfetch]: https://github.com/qte77/polyfetch-scrape
