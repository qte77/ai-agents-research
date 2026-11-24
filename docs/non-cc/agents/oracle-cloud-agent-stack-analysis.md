---
title: Oracle Cloud Agent Stack Analysis — OCI Generative AI Agents, Enterprise AI Agents, AI Agent Studio for Fusion Applications
source: https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/overview.htm
purpose: "First-party fact-check of Oracle's two agent stacks (OCI Generative AI Agents; AI Agent Studio in Fusion Applications): roles, identity, licensing, Claude availability, MCP/A2A, regions; no prices."
created: 2026-11-20
updated: 2026-11-20
validated_links_on: 2026-11-20
status: assess
---

**Details:** Oracle has two separate agent stacks that share a brand but not a console, a policy
model or a licence: an **OCI** stack (Generative AI Agents, plus Enterprise AI Agents, GA 2026-03-31)
for developers on Oracle Cloud Infrastructure, and **AI Agent Studio** for business teams inside
**Fusion Applications** (ERP, HCM, SCM, CX). Everything below is from Oracle's own documentation,
release notes and press pages read on 2026-11-20; prices are left out on purpose.

## What It Is

| Stack | Kind | Built by | Where it runs |
|---|---|---|---|
| OCI Generative AI Agents | "fully managed" service for LLM agents with ready-to-use tools [oci-agents] | Developers and cloud admins | An OCI region ([Regions](#regions)) |
| OCI Enterprise AI Agents | Newer primitives on OCI Generative AI: an OpenAI-Responses-compatible API, projects, memory, vector stores, hosted applications [oci-enterprise-ai] | Developers | OCI regions, GA 2026-03-31 |
| AI Agent Studio for Fusion Applications | A "design-time environment" inside Fusion Applications to "create, configure, validate, and deploy AI agents" [aas-overview]; multi-agent teams per the capability list [aas-key] | Business and Fusion admins; partners | Inside the Fusion tenant |

The OCI Generative AI Agents tools are SQL, Retrieval-Augmented Generation (RAG), agent-as-tool, custom function calling and custom
API-endpoint calling, with guardrails (content moderation, prompt-injection and PII handling) and an
optional human-in-the-loop [oci-agents]. Enterprise AI Agents lists file search, code interpreter,
function calling and Model Context Protocol (MCP) calling of remote MCP servers, plus long- and short-term memory and
NL2SQL over a customer schema [oci-enterprise-ai]. Data platforms are out of scope here; for
data platforms in general see
[data-platforms-lakehouse-landscape.md](../infrastructure/data-platforms-lakehouse-landscape.md)
(it does not cover Oracle).

## Roles and identity

### OCI: IAM policies

OCI authorises with IAM policy statements over resource types, with compartments as the scope
[oci-agents-iam]:

- **Resource types:** `genai-agent`, `genai-agent-knowledge-base`, `genai-agent-data-source`,
  `genai-agent-data-ingestion-job`, `genai-agent-endpoint`, `genai-agent-work-request`,
  `genai-agent-session` and `genai-agent-tool`, plus the aggregate `genai-agent-family`.
- **Administrators:** `allow group <name> to manage genai-agent-family in compartment <name>` (or
  `in tenancy`) is the documented broad grant; the page points to per-resource-type verbs for
  narrower grants.
- **Invoke only:** the permission for chatting with an agent endpoint, `GENAI_AGENT_ENDPOINT_CHAT`,
  maps to the `use` verb, so chat itself needs `use` on the endpoint rather than `manage`. Caveat:
  `CreateSession` and `EndSession` map to the `manage` verb on `genai-agent-session`, so a client that
  opens and closes its own sessions needs more than endpoint `use` [oci-agents-iam].
- **Agents as principals:** an agent is itself a resource principal (`resource.type='genaiagent'`),
  and data-ingestion jobs are `genaiagentdataingestionjob`. The page's examples put these in dynamic
  groups and grant them what the agent needs: `use generative-ai-chat` (model calls), `read
  secret-bundle` (Vault secrets for Oracle Database or OpenSearch sources), `read
  database-tools-family`, and `read objects` for ingestion.
- **A privilege trap:** users who add Object Storage files to a knowledge base need `manage
  object-family` in the bucket's compartment on the page's example; Oracle suggests reviewing
  narrower Object Storage policies. Restricting by object name or prefix "isn't supported" for
  ingestion jobs.

Whether the OCI Enterprise AI Agents API keys and projects have their own policy verbs was not
checked; this pass read the Generative AI Agents policy page only.

### OCI: identity provider

OCI IAM provides sign-in, SSO and lifecycle management through identity domains, which can federate
to external identity providers [oci-iam-overview]. Which external IdPs (for example Entra ID) are
supported was not read in this pass; the overview page states only that IAM "integrates with
existing identity stores, external identity providers".

### Fusion: duty roles, not policies

AI Agent Studio uses Fusion Applications' own role model, not OCI IAM [aas-access]:

- **Build:** per-product administrator duty roles, assigned to job roles, with permission groups
  enabled in the Security Console and two security-import scheduled processes run first.
- **Extra privileges for builders:** an external REST API tool needs a Visual Builder backend
  privilege (`ORA_FND_TRAP_PRIV`); scheduling workflow agent teams needs the Fai Batch Job Manager
  duty; channels and the monitoring tab need their own permission groups [aas-access].
- **Invoke:** the same page defers end-user access to a separate FAQ ("How can I give users access
  to AI agents?"), which was not read in this pass. A search listing of the 26C guide mentioned a
  runtime duty plus an "Access Intelligent Agent Chat" privilege; seen only in a snippet, so
  unverified.
- **Caution on the access page:** "Using predefined roles might account for subscription
  consumption irrespective of whether you purchased the cloud service or not" [aas-access] — role
  assignment can therefore have licence effects.
- **IdP:** Fusion sign-in and SSO setup was not read in this pass (unverified).

## Licences: who needs one

| Stack | Basis | Source |
|---|---|---|
| Fusion embedded AI agents | Oracle states embedded AI "included with a Fusion Applications subscription at no extra cost" (Oracle product page by an Oracle Fusion executive, dated 2025-04-29 on the page but edited later, as it cites an August 2026 Gartner report; confirm in current terms) | [fusion-custom-ai] |
| Fusion custom AI (fully custom agents) | Planned: the page says custom AI "will be delivered as a separately priced offering" and "will use" seat-based and employee-based pricing (marked "Planned" there). The boundary between embedded and custom use is not documented on pages read in this pass | [fusion-custom-ai] |
| OCI Generative AI Agents and Enterprise AI Agents | OCI service consumption; the billing basis was not read in this pass (unverified) | n/a |

Practical reading, per Oracle's statements and not independently verified: embedded agents need no
extra licence; teams that build fully custom agents should confirm the custom-AI entitlement with
Oracle before assigning roles (see the caution above).

## Claude, MCP and A2A

- **Claude on OCI Generative AI: not listed.** Oracle's "Offered Pretrained Foundation Models" page on
  2026-11-20 lists Cohere, Google Gemini, Meta Llama, OpenAI gpt-oss and xAI Grok chat models; it
  names no Anthropic model [oci-models]. The Enterprise AI Agents release note lists OpenAI, xAI and
  Google models [oci-enterprise-ai]. Absence on those two pages is the evidence; no Oracle statement
  about Claude on OCI was found.
- **Claude in Fusion AI Agent Studio: announced.** Oracle's 2025-10-15 press release says AI Agent
  Studio supports "OpenAI, Anthropic, Cohere, Google, Meta, and xAI" models [aas-oct25]. How Claude
  is hosted for Fusion is not stated there, and the page does not establish that Claude is then
  available on OCI itself.
- **MCP:** AI Agent Studio can add an MCP tool pointing at an external server, with SSE or
  StreamableHTTP transport and a credential type; the 26C page shows both transports, and a search
  listing says 26D shows only StreamableHTTP [aas-mcp]. Oracle's Oct 2025 release announced MCP
  support and a credential store [aas-oct25]. OCI Enterprise AI Agents supports "MCP Calling" of
  remote MCP servers and can host agent applications built on MCP servers [oci-enterprise-ai].
- **A2A:** AI Agent Studio documents agent cards and an agent registry (A2A "components" page, 26B),
  announced in the same Oct 2025 release [aas-a2a], [aas-oct25]. Whether OCI Generative AI Agents
  speaks Agent-to-Agent Protocol (A2A) was not found.

## Regions

- OCI Generative AI Agents (overview page, 2026-11-20): Ashburn, Chicago, Phoenix, São Paulo,
  Frankfurt, London and Osaka [oci-agents].
- OCI Enterprise AI Agents (release note 2026-03-31): Chicago, Ashburn, Phoenix, Frankfurt, London,
  Osaka, Hyderabad, São Paulo and Riyadh [oci-enterprise-ai].
- Fusion AI Agent Studio follows the Fusion tenant's region; not checked further.

## Release status (dated)

| Item | Status | Date | Source |
|---|---|---|---|
| OCI Enterprise AI Agents | General availability | 2026-03-31 | [oci-enterprise-ai] |
| OCI Generative AI Agents | Latest service release note seen: routing-LLM selection | 2026-02-05 | [oci-agents-rn] |
| AI Agent Studio for Fusion Applications | Launched; expanded with marketplace, more LLMs, MCP and A2A cards | 2025-03-20 launch (Oracle press, via search listing, unverified), 2025-10-15 expansion | [aas-oct25] |
| Fusion guide edition seen | 26D title page (copyright 2025, 2026); 26B and 26C pages read for details | 2026-11-20 | [aas-access], [aas-mcp] |

## At a glance: Oracle

| Dimension | OCI Generative AI / Enterprise AI Agents | AI Agent Studio (Fusion) |
|---|---|---|
| Runtime | Managed agents on OCI; hosted applications | Inside Fusion Applications |
| Claude availability | Not listed on the model pages, 2026-11-20 | Announced as a supported model family (2025-10-15); hosting unstated |
| MCP / A2A | MCP calling (Enterprise AI Agents); A2A not found | MCP tool; A2A agent cards and registry |
| Memory | Conversation context; long and short-term memory (Enterprise) | Not checked |
| Agent identity and IdP | Agent resource principal, dynamic groups; OCI IAM identity domains | Fusion roles and users; SSO not checked |
| Least-privilege roles | `use` on `genai-agent-endpoint` to chat (session create/end need `manage genai-agent-session`); `manage genai-agent-family` to administer | Product duty roles; runtime duty and chat privilege (unverified) |
| Licences and who needs one | OCI consumption (basis unverified) | Embedded: with Fusion subscription; custom: separate, seat/employee-based (2025 statement) |
| Regions | 7 (agents), 9 (enterprise) | Fusion tenant region |
| Release status | Enterprise GA 2026-03-31 | Expanded 2025-10-15; guide 26D |

## Cross-References

- [microsoft-365-copilot-analysis.md](microsoft-365-copilot-analysis.md#roles-identity-and-licences) — the Azure and Entra counterpart
- [salesforce-agentforce-analysis.md](salesforce-agentforce-analysis.md#licences-and-roles-for-agentforce-agents) — the SaaS-vendor counterpart
- [agent-identity-auth-landscape.md](../../sdlc-lcm/agent-identity-auth-landscape.md#1-authenticate-the-agent-agent-as-a-first-class-principal) — agent identity across vendors
- [data-platforms-lakehouse-landscape.md](../infrastructure/data-platforms-lakehouse-landscape.md) — data platforms (general; no Oracle coverage)
- [ag-ui-protocol-landscape.md](../protocols/ag-ui-protocol-landscape.md) — Oracle Agent Spec and its Agent-User Interaction Protocol (AG-UI) alignment (March 2026)
- [CC-business-api-integrations.md](../../cc-native/plugins-ecosystem/CC-business-api-integrations.md#oracle-netsuite-official) — Oracle NetSuite's official MCP server for Claude Code
- [agentic-enterprise-os-landscape.md](../frameworks/agentic-enterprise-os-landscape.md) — name clash: ServiceNow Otto also has an "AI Agent Studio"; this doc means Oracle's, for Fusion Applications

## Sources

| Source | Content |
|---|---|
| [Overview of Generative AI Agents][oci-agents] | Tools, guardrails, regions (read 2026-11-20) |
| [Generative AI Agents IAM policies][oci-agents-iam] | Resource types, verbs, principals, example policies (2026-11-20) |
| [Generative AI Agents release notes][oci-agents-rn] | Release dates (2026-11-20) |
| [Enterprise AI Agents GA note][oci-enterprise-ai] | Responses API, MCP calling, memory, regions, 2026-03-31 |
| [Offered pretrained models][oci-models] | Model families listed, no Anthropic (2026-11-20) |
| [OCI IAM overview][oci-iam-overview] | Identity domains, federation, SSO |
| [Access Requirements for AI Agent Studio][aas-access] | Duty roles, privileges, consumption caution (26B page) |
| [Overview of AI Agent Studio (26D)][aas-overview] | Definition of the tool |
| [Key Capabilities of AI Agent Studio][aas-key] | Capability list, agent teams |
| [Add MCP Tool (26C)][aas-mcp] | MCP tool fields and transports |
| [Components in A2A (26B)][aas-a2a] | Agent card and registry |
| [AI Agent Studio expansion, 2025-10-15][aas-oct25] | LLM families, MCP, A2A cards, credential store |
| [Fusion custom AI page][fusion-custom-ai] | Embedded versus custom AI licence basis (page dated 2025-04-29, edited later) |

[oci-agents]: https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/overview.htm
[oci-agents-iam]: https://docs.oracle.com/en-us/iaas/Content/generative-ai-agents/iam-policies.htm
[oci-agents-rn]: https://docs.oracle.com/en-us/iaas/releasenotes/services/generative-ai-agents/
[oci-enterprise-ai]: https://docs.oracle.com/en-us/iaas/releasenotes/generative-ai/enterprise-ai.htm
[oci-models]: https://docs.oracle.com/en-us/iaas/Content/generative-ai/pretrained-models.htm
[oci-iam-overview]: https://docs.oracle.com/en-us/iaas/Content/Identity/getstarted/identity-domains.htm
[aas-access]: https://docs.oracle.com/en/cloud/saas/fusion-ai/26b/aiaas/access-ai-agent-studio.html
[aas-overview]: https://docs.oracle.com/en/cloud/saas/fusion-ai/26d/aiaas/overview-of-ai-agent-studio.html
[aas-key]: https://docs.oracle.com/en/cloud/saas/fusion-ai/26b/aiaas/key-capabilities.html
[aas-mcp]: https://docs.oracle.com/en/cloud/saas/fusion-ai/26c/aiaas/add-mcp-tool.html
[aas-a2a]: https://docs.oracle.com/en/cloud/saas/fusion-ai/26b/aiaas/components-in-a2a.html
[aas-oct25]: https://www.oracle.com/news/announcement/ai-world-oracle-expands-ai-agent-studio-for-fusion-applications-with-new-marketplace-llms-and-vast-partner-network-2025-10-15/
[fusion-custom-ai]: https://www.oracle.com/applications/fusion-ai/custom-ai/
