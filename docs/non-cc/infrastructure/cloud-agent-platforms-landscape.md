---
title: Cloud Agent Platforms Compared — AWS, Google Cloud, Azure, Oracle, IBM, Alibaba Cloud
purpose: One dated comparison of six cloud agent stacks (runtime, Claude availability, MCP/A2A, memory, agent identity and IdP, least-privilege roles, licences, regions, release status), built from the per-cloud analyses; no prices.
created: 2026-11-20
updated: 2026-11-20
validated_links: 2026-11-20
status: assess
---

## What It Is

A side-by-side reading of the six cloud agent stacks analysed in this corpus. Every cell condenses the
"At a glance" table of the per-cloud doc linked in its column header; the evidence, dates, caveats and
sources live there, so check the per-cloud doc before relying on a cell. Business and developer agents
are in scope; model training is out; prices are deliberately left out (licence *models* only). Data
platforms are covered in [data-platforms-lakehouse-landscape.md][data-platforms]; agent registries in
[agentic-enterprise-os-landscape.md § Agent registries compared][registries]. As of 2026-11-20.

## Comparison

| Dimension | [AWS][aws] | [Google Cloud][gcp] | [Azure (Foundry)][azure] | [Oracle][oracle] | [IBM][ibm] | [Alibaba Cloud][alibaba] |
|---|---|---|---|---|---|---|
| Agent runtime | AgentCore Runtime (serverless, session-isolated); Bedrock Agents classic closed to new users | Agent Runtime (formerly Agent Engine) on Gemini Enterprise Agent Platform | Foundry Agent Service: prompt, voice and hosted (container) agents | OCI Generative AI / Enterprise AI Agents; AI Agent Studio inside Fusion | watsonx Orchestrate SaaS (AWS, IBM Cloud, GovCloud), on-premises | Model Studio apps; AgentRun serverless; AgentBay / Agent Sandbox |
| Claude availability | Yes: Bedrock and Claude Platform on AWS | Yes: on Agent Platform and as Anthropic-managed Claude Models on Google Cloud | Yes: Azure-hosted or Anthropic-hosted (Global Standard only) | Not on OCI model pages; announced for Fusion AI Agent Studio (2025), hosting unstated | `claude-sonnet-4-6` via Bedrock, public preview, SaaS tenants in selected regions | Not found on any page read |
| MCP / A2A | Both on Runtime; Gateway turns APIs into MCP tools | A2A supported; Registry and Gateway govern MCP servers | MCP tools; A2A v1.0 GA (v0.3 preview) | MCP in Enterprise AI Agents and Agent Studio; A2A in Agent Studio | MCP toolkits (index entry only); A2A client, 1.0.0 provider | MCP documented; A2A unverified |
| Memory | AgentCore Memory (short and long term) | Memory Bank and Sessions | Memory listed as a Foundry tool | Long- and short-term memory (Enterprise AI Agents) | `/memories` APIs for custom agents | Short-term turns; long-term planned |
| Agent identity and IdP | AgentCore Identity; inbound JWT from any OIDC IdP; IAM Identity Center | Agent Identity (per agent, GA 2026-04-22); Workforce Identity Federation | Entra agent identity per agent (blueprint); Entra ID | Agent resource principal, dynamic groups; OCI IAM identity domains | Per-tool connections (OAuth, on-behalf-of SSO); no distinct agent identity found | Agent Identity (OIDC inbound incl. Okta, Entra ID; STS/OAuth outbound) |
| Least-privilege roles | Per-resource `InvokeAgentRuntime` and custom policies; `BedrockAgentCoreFullAccess` is broad | Custom role with `reasoningEngines.query`/`.get`; `aiplatform.user` is broad | Foundry Agent Consumer (invoke), Foundry User (build) | `use genai-agent-endpoint` (plus `manage genai-agent-session` for sessions) | Not confirmed (IAM pages JS-rendered) | Six `AliyunBailian*` policies plus workspace roles |
| Licence model | AgentCore consumption; Amazon Quick and Kiro per user | Platform consumption; Gemini Enterprise per seat | Azure consumption; Copilot / Agent 365 per user | OCI consumption; Fusion-embedded with subscription, custom agents planned seat/employee-based | Plan tiers by monthly active users, messages, documents | Mostly pay-as-you-go; seat-based Token Plan (Team) |
| Regions | Up to 22, feature-dependent | 23 region names | Claude: no EU Data Zone | 7 (agents), 9 (enterprise) | AWS, IBM Cloud, GovCloud, on-premises | Six Model Studio regions |
| Release status | AgentCore GA 2025-10-13; Registry GA 2026-08-31 | Agent Identity GA 2026-04-22; Registry and Gateway GA 2026-06-18 | Learn pages read 2026-11-20 (no label recorded) | Enterprise AI Agents GA 2026-03-31 | ADK docs 2.20.0 (2026-11-11) | Agent 2.0 status unstated |

## Reading the table

- **Claude.** Claude is first-party on three clouds (AWS, Google Cloud, Azure), each with both a
  cloud-hosted and an Anthropic-hosted path; IBM reaches it through Bedrock in preview; Oracle and
  Alibaba list no Claude model on the pages read. Setup for Claude Code on the first three is in
  [CC-model-provider-configuration.md][cc-provider].
- **Agent identity is now a cloud primitive.** AWS, Google, Azure, Oracle and Alibaba each give an
  agent its own principal; IBM's documented model authenticates per tool connection. The
  cross-vendor view is in [agent-identity-auth-landscape.md § 1][agent-identity].
- **Invoke-only roles are rarely packaged.** Of the pages read, only Azure names a ready-made invoke
  role (Foundry Agent Consumer); AWS and Google point to custom, per-resource policies, Oracle grants
  by policy verb, and IBM's roles were not readable. The broad built-in roles grant far more than
  invoking an agent.
- **Licences split by layer.** The agent runtimes bill by consumption; per-user seats sit on the user-facing products (Amazon Quick, Kiro, Gemini Enterprise,
  Microsoft 365 Copilot and Agent 365, Alibaba's Token Plan), Oracle ties embedded agents to the Fusion
  subscription, and IBM meters monthly active users instead.
- **A2A is the uneven column.** Supported on AWS, Google, Azure, Oracle's Agent Studio and IBM;
  unverified on Alibaba. Protocol caveats are in [ag-ui-protocol-landscape.md § A2A][a2a].

**GitHub Copilot SDK.** Not a cloud platform but an embeddable agent engine: `microsoft/copilot-sdk`
(MIT, generally available per its README) runs the Copilot CLI's engine inside an app, with a Copilot
subscription or your own model key; see [github-copilot-cli-analysis.md § Copilot SDK][copilot-sdk].

## Cross-References

- Per-cloud analyses: [AWS][aws] · [Google Cloud][gcp] · [Azure / Microsoft][azure] · [Oracle][oracle] · [IBM][ibm] · [Alibaba Cloud][alibaba]
- [agentic-enterprise-os-landscape.md][registries] — enterprise agent platforms and registries compared
- [agent-identity-auth-landscape.md][agent-identity] — agent identity across vendors
- [CC-model-provider-configuration.md][cc-provider] — running Claude Code on Bedrock, Google Cloud and Foundry
- [data-platforms-lakehouse-landscape.md][data-platforms] — data platforms (linked, not covered here)

## Sources

| Source | Content |
|---|---|
| [aws-agent-stack-analysis.md][aws], [google-cloud-agent-stack-analysis.md][gcp], [microsoft-365-copilot-analysis.md § Roles, identity and licences][azure], [oracle-cloud-agent-stack-analysis.md][oracle], [ibm-agent-stack-analysis.md][ibm], [alibaba-cloud-agent-stack-analysis.md][alibaba] | Per-cloud facts, each first-party checked 2026-11-20 with two falsification passes; every cell here condenses their "At a glance" tables |

[aws]: ../agents/aws-agent-stack-analysis.md
[gcp]: ../agents/google-cloud-agent-stack-analysis.md
[azure]: ../agents/microsoft-365-copilot-analysis.md#roles-identity-and-licences
[oracle]: ../agents/oracle-cloud-agent-stack-analysis.md
[ibm]: ../agents/ibm-agent-stack-analysis.md
[alibaba]: ../agents/alibaba-cloud-agent-stack-analysis.md
[copilot-sdk]: ../agents/github-copilot-cli-analysis.md#copilot-sdk-embed-the-clis-agent-engine
[registries]: ../frameworks/agentic-enterprise-os-landscape.md#agent-registries-compared
[agent-identity]: ../../sdlc-lcm/agent-identity-auth-landscape.md#1-authenticate-the-agent-agent-as-a-first-class-principal
[cc-provider]: ../../cc-native/configuration/CC-model-provider-configuration.md
[a2a]: ../protocols/ag-ui-protocol-landscape.md#a2a-agent-to-agent-protocol
[data-platforms]: data-platforms-lakehouse-landscape.md
