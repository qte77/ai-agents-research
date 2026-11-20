---
title: IBM Agent Stack Analysis — watsonx Orchestrate and its Agent Development Kit
purpose: First-party fact-check of IBM's agent stack (watsonx Orchestrate agent builder, ADK, external-agent and MCP/A2A support, model choice incl. Claude, identity, licence metrics, regions) for the cloud-agent-stacks synthesis (plan 0014 K34); no prices.
category: non-cc/agents
created: 2026-11-20
updated: 2026-11-20
validated_links: 2026-11-20
status: assess
---

**Details:** Scope is the business-and-dev agent path on IBM: **watsonx Orchestrate** (agent builder,
runtime, catalog) and its open-source **Agent Development Kit (ADK)**. ML training is out of scope; data
platforms are only linked ([data-platforms-lakehouse-landscape.md][data-platforms]). No prices are
given; licence metrics are named only. Evidence is as of 2026-11-20 and labelled *documented* (vendor
docs read now), *vendor claim*, or **unverified** (could not be read first-party). The IBM product docs
site (`ibm.com/docs`) and `cloud.ibm.com/docs` are JavaScript or access-blocked for our fetchers, so
everything on IAM role names is explicitly unverified; the ADK docs site and the pricing page were
readable.

## What each name is

| Name | What it is | Evidence |
|---|---|---|
| watsonx Orchestrate | IBM's SaaS agent platform: build native agents, import external ones, tools/catalog, control plane, chat channels | documented ([ADK docs][adk-agents], [pricing page][wxo-pricing]) |
| Agent Development Kit (ADK) | Python library + `orchestrate` CLI to author, import and deploy agents/tools; MIT licence | documented ([repo][adk-repo], LICENSE read via GitHub API) |
| Developer Edition | local, self-contained copy of Orchestrate run via a docker engine for iteration before connecting to a remote instance | documented ([ADK README][adk-readme]) |
| watsonx.ai agents / Agent Lab | IBM's model-platform side; Orchestrate can register watsonx.ai agents as *external* agents | partly documented ([agents overview][adk-agents]); Agent Lab itself **unverified** |
| watsonx.governance | agent inventory/lifecycle monitoring | **unverified** first-party here; the ADK docs expose a "governance-monitoring" API (agent monitoring setup), see [Governance hooks](#governance-hooks) |

## Build and runtime

- **Native agents** combine an LLM, instructions, tools, collaborator agents, optional knowledge and
  optional scheduling; **external agents** are integrated from other platforms (watsonx.ai,
  Salesforce Agentforce, third-party frameworks) through protocols such as `external_chat` or A2A
  (documented, [agents overview][adk-agents]).
- ADK 2.20.0 (2026-11-11 per the [release notes][adk-release]) adds live-agent escalation, registering
  external agents for the **control plane only**, PKCE for OAuth 2.0 authorization-code connections and
  an `external_chat/A2A/1.0.0` provider. GitHub's latest *release* object is 2.19.1 (2026-10-22, as of
  2026-11-20; MIT), so the docs run ahead of GitHub releases — treat the docs date as the newer signal.
- Agents are versioned and released per **environment** (draft/live) through ADK commands and an
  agent-releases API (documented in the [docs index][adk-index]).
- Memory: an Agentic SDK exposes `/memories` and `/memories/search` APIs for "runs-on" custom agents
  ([memory page][adk-memory]); runtime memory for native agents beyond that was not read.

## Models and Claude

- Built-in models listed in the [LLM docs][adk-llm]: gpt-oss-120b (Groq or AWS Bedrock; watsonx.ai on
  AWS GovCloud), Gemma 4 31B via Bedrock (public preview), GPT-5.4 via Azure OpenAI, and
  **claude-sonnet-4-6 via AWS Bedrock (public preview)**.
- Claude availability is narrow: "selected regions only", not EU regions, not HIPAA tenants; the docs
  list AWS us-east-1, ap-southeast-1, ap-south-1 and IBM Cloud Dallas, Toronto, Sydney, Tokyo, Sao
  Paulo ([model availability][adk-llmstart], as of 2026-11-20).
- Bring-your-own: virtual models can be registered for providers including `anthropic` (API key via a
  connection) and Bedrock-hosted Claude ([managing models][adk-llm]); model policies (public preview)
  add load-balance/fallback across virtual models ([policies][adk-policies]). Premier models such as
  GPT-5.4 are off by default and need a tenant admin to enable them; the docs state they add cost
  measured in MAUs ([premier models][adk-premier]).

## MCP and A2A

- **MCP:** local and remote MCP toolkits can be imported as tools, and the ADK docs include MCP-based
  workflow publishing in public preview (index entries in [docs index][adk-index]).
- **A2A:** external agents can be discovered from an A2A agent card; A2A 1.0.0 provider added in ADK
  2.20.0; LangGraph agents can be A2A-enabled ([connect to external agents][adk-connect]).
- How Orchestrate itself is exposed as an A2A *server* was not verified; an A2A protocol-version API
  exists in the API index.

## Identity, IdP and least privilege

- **Authentication to an instance** (documented, [environment page][adk-env]): environment types
  `ibm_iam` (IBM Cloud IAM), `mcsp` (AWS, Multi-Cloud SaaS Platform; v2 by default) and `cpd` (on-prem);
  a custom IAM token endpoint is required for HIPAA clusters.
- **Connections** carry per-tool credentials (OAuth2, API key, SSO on-behalf-of); a tutorial shows
  OAuth On-Behalf-Of SSO from Microsoft Entra ID to Workday ([index][adk-index]). This is outbound
  agent-to-system identity; **no separate "agent identity" object** was found.
- **IdP (workforce SSO into Orchestrate):** **unverified.** The only first-party SSO material read is
  the Entra-to-Workday outbound tutorial above; IBM IAM federation/App ID options were not confirmed.
- **Roles for build/deploy/invoke:** **unverified.** IBM Cloud IAM role names and the action-to-role
  mapping for Orchestrate could not be read (docs pages are script-rendered). Do not cite role names
  from this note. Ask the lead to re-check via a browser session on `ibm.com/docs` (Orchestrate
  "Managing users and roles").

## Governance hooks

The ADK API index lists tenant-permission sync/revoke, model-policy and "governance-monitoring"
endpoints (check availability, set up and read agent monitoring). The enterprise-OS doc compares how
registries/inventories work across vendors: see
[Agent registries compared][registries]; IBM is not a row there as of this pass.

## Licences — who needs one

From the [pricing page][wxo-pricing] (plan names and allowance *types* only, no prices):

- Plans: Trial (30-day free), Essentials, Standard, Premium (Premium adds data isolation, HIPAA-ready
  option; contact sales).
- The tiers are differentiated by **monthly active users (MAU) allowance**, **messages per month**,
  document volume for agent knowledge, channels (webchat, voice, Slack, Teams) and caps on message
  use per user. This is a consumption/capacity model keyed to *active users*, not a named per-seat
  licence (reading of the table; vendor documents, not a contract).
- Premier LLMs and some add-on agents are separately metered (MAU-based or API-call allowances).
- The Developer Edition and ADK are free to install (MIT); a remote instance needs an Orchestrate
  plan.

## At a glance

| Item | IBM watsonx Orchestrate (+ ADK) |
|---|---|
| Runtime | SaaS multi-tenant on AWS and IBM Cloud, AWS GovCloud (US), on-prem/air-gapped options; local Developer Edition |
| Claude availability | claude-sonnet-4-6 via AWS Bedrock, public preview, selected regions, not EU/HIPAA; BYO Anthropic API key possible (documented) |
| MCP / A2A | MCP toolkits local+remote (documented); A2A client for external agents, 1.0.0 provider in ADK 2.20.0 (documented) |
| Memory | Agentic SDK `/memories` APIs for custom agents (documented); native-agent memory unverified |
| Agent identity and IdP | `ibm_iam`/`mcsp`/`cpd` auth; per-tool connections (OAuth, OBO SSO); no distinct agent-identity object found; workforce SSO/IdP unverified |
| Least-privilege roles | **Unverified** (IBM docs not readable) |
| Licences and who needs one | Plan tiers by MAU, messages, doc volume; premier models metered extra; no per-seat licence found; no prices here |
| Regions | AWS and IBM Cloud regions, GovCloud (US), on-prem; Claude only in 3 AWS + 5 IBM Cloud regions |
| Release status | ADK 2.20.0 docs 2026-11-11 (GitHub latest release 2.19.1, 2026-10-22); Claude preview; model policies preview |

## Cross-References

- [microsoft-365-copilot-analysis.md](microsoft-365-copilot-analysis.md) — sibling cloud agent stack
  (same conventions, licences table)
- [salesforce-agentforce-analysis.md](salesforce-agentforce-analysis.md) — Agentforce, an external
  agent type Orchestrate can integrate
- [agentic-enterprise-os-landscape.md][registries] — agent registries compared
- [data-platforms-lakehouse-landscape.md][data-platforms] — data platforms (linked only)

## Sources

| Source | Content |
|---|---|
| [ADK documentation index][adk-index] | page inventory: agents, MCP toolkits, A2A, environments, governance APIs, versions |
| [Agents overview][adk-agents] | native vs external agents, collaborators, scheduling |
| [Connect to external agents][adk-connect] | A2A / external_chat integration, LangGraph |
| [LLM docs: managing models][adk-llm] | built-in models, virtual models, Anthropic/Bedrock providers |
| [LLM getting started][adk-llmstart] | availability by deployment type; Claude region list |
| [Model policies][adk-policies] | fallback/load-balance, public preview |
| [Enabling premier models][adk-premier] | premier models off by default, MAU cost note |
| [Environments][adk-env] | `ibm_iam` / `mcsp` / `cpd` environment types |
| [SDK memory][adk-memory] | memory APIs for custom agents |
| [ADK release notes][adk-release] | 2.20.0 (2026-11-11) |
| [ADK repo][adk-repo] / [README][adk-readme] | MIT licence, Developer Edition, latest GitHub release 2.19.1 |
| [Orchestrate pricing page][wxo-pricing] | plan names and allowance metrics (prices deliberately not recorded) |

[data-platforms]: ../infrastructure/data-platforms-lakehouse-landscape.md
[registries]: ../frameworks/agentic-enterprise-os-landscape.md#agent-registries-compared
[adk-index]: https://developer.watson-orchestrate.ibm.com/llms.txt
[adk-agents]: https://developer.watson-orchestrate.ibm.com/agents/overview.md
[adk-connect]: https://developer.watson-orchestrate.ibm.com/agents/connect_agent.md
[adk-llm]: https://developer.watson-orchestrate.ibm.com/llm/managing_llm.md
[adk-llmstart]: https://developer.watson-orchestrate.ibm.com/llm/getting_started_llm.md
[adk-policies]: https://developer.watson-orchestrate.ibm.com/llm/model_policies.md
[adk-premier]: https://developer.watson-orchestrate.ibm.com/llm/enable_premier_models.md
[adk-env]: https://developer.watson-orchestrate.ibm.com/environment/initiate_environment.md
[adk-memory]: https://developer.watson-orchestrate.ibm.com/sdk/memory.md
[adk-release]: https://developer.watson-orchestrate.ibm.com/release/release.md
[adk-repo]: https://github.com/IBM/ibm-watsonx-orchestrate-adk
[adk-readme]: https://github.com/IBM/ibm-watsonx-orchestrate-adk/blob/main/README.md
[wxo-pricing]: https://www.ibm.com/products/watsonx-orchestrate/pricing
