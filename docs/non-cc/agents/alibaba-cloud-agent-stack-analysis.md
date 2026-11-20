---
title: Alibaba Cloud Agent Stack Analysis — Model Studio, AgentRun, AgentBay, Qwen-Agent
purpose: First-party fact-check of Alibaba Cloud's agent stack (Model Studio agent applications, AgentRun runtime, AgentBay/Agent Sandbox, open-source Qwen-Agent), its RAM permissions, identity, licence/consumption model, MCP/A2A and Claude availability, for the cloud-agent-stacks synthesis (plan 0014 K34); no prices.
category: non-cc/agents
created: 2026-11-20
updated: 2026-11-20
validated_links: 2026-11-20
status: assess
---

**Details:** Scope is business-and-dev agents on Alibaba Cloud. ML training is out of scope; data
platforms are only linked ([data-platforms-lakehouse-landscape.md][data-platforms]). No prices are
given; billing metrics are named only. Evidence is as of 2026-11-20: *documented* (Alibaba help pages
read now, English, mostly `alibabacloud.com/help/en`; a few pages only resolved on the English
`help.aliyun.com` mirror), or **unverified**. Alibaba docs change quickly (pages cited below were
updated Aug-Nov 2026), so re-read before relying on a detail.

## What each name is

| Name | What it is | Evidence |
|---|---|---|
| Model Studio (Bailian) | model service plus agent/workflow application builder, knowledge bases, MCP, API keys, workspaces | documented ([overview][ms-overview], [agent 2.0][ms-agent2]) |
| Agent application (Agent 2.0) | agent that plans over tools (MCP, knowledge base, skills); Agent 1.0 is legacy and cannot be upgraded | documented ([page][ms-agent2]); GA vs preview not stated on the page |
| AgentRun | serverless agent runtime on Function Compute, with sandbox, model proxy, tool hub, observability | documented ([page][agentrun]); last updated 2026-08-22 |
| Agent Identity | workload identity, credential and user-pool service for agents | documented ([AgentRun tutorial][agentid]) |
| AgentBay | cloud execution environments for agents: browser, code space, cloud computer, mobile | documented ([overview][agentbay]); last updated 2026-08-24 |
| Agent Sandbox (Function Compute) | newer sandbox product (code, browser, desktop, mobile); a help page documents migrating AgentBay's Linux desktop to it | overview documented ([page][sandbox]); migration page seen in search only, **not read** |
| Qwen-Agent | open-source Python agent framework from the Qwen team | documented ([repo][qa-repo], [README][qa-readme]) |

## Build and runtime

- **Model Studio applications:** an agent application (Agent 2.0) treats knowledge bases, MCP
  services and other capabilities as tools and plans which to call; skills, shell/file sandbox tools
  (off by default) and short-term memory (0 to 30 turns; long-term memory "planned") are described.
  An application must be published before invocation; its API details sit under the publish channel
  ([Agent 2.0][ms-agent2]). Workflow applications cover fixed processes (documented via search
  results; page not read here).
- **AgentRun** offers no-code (AI Studio), low-code and pro-code creation, a serverless runtime with
  session affinity and scale to zero (Python, Node.js, Java), a model proxy (fallback, load balancing,
  token-rate limiting), sandboxes (code interpreter, browser; desktop/mobile "planned"), and OpenTelemetry
  tracing with token-level cost attribution. It integrates LangChain, AgentScope, CrewAI and Google
  ADK, and can plug in Mem0 and RAGFlow for memory/RAG ([AgentRun][agentrun]).
- **AgentBay** provides four environments (browser, code space, cloud computer, mobile) through SDK and
  MCP ([overview][agentbay]).
- **Qwen-Agent:** Apache-2.0 per the repo LICENSE; latest GitHub release v0.0.26 (2025-05-29), last
  push 2026-03-04 (GitHub API, as of 2026-11-20), i.e. slow-moving. README documents MCP support and
  DashScope or self-hosted Qwen models.

## Models and Claude

- Model Studio's recommended-models page (updated 2026-11-16) lists Qwen (e.g. qwen4-max), DeepSeek,
  GLM, Kimi and MiniMax models ([models][ms-models]). **No Claude model appears** on the models page,
  the regions page, or the AgentBay/Agent Sandbox pages (string search, 0 hits, as of 2026-11-20).
  Conclusion: Claude is **not offered as a Model Studio model** on the evidence read; this is an
  absence from the pages searched, not a vendor statement.
- Model Studio exposes an **Anthropic-compatible Messages endpoint** and an OpenAI-compatible one, but
  the examples serve Qwen models through them ([overview][ms-overview]). A Team token plan lists
  Claude Code as a supported *client tool* pointing at that Anthropic-compatible URL
  ([Token Plan Team][token-plan]). Both mean "Claude-shaped API/client, Qwen model", not Claude.
- AgentRun's model proxy can point at API or self-hosted models, so a customer's own Claude API key
  behind a custom endpoint is architecturally possible; not documented as a supported Claude path.

## MCP and A2A

- **MCP:** agent and workflow applications use official or custom MCP services; AgentRun converts
  agents, sandboxes and API tools into MCP and can bundle them behind an MCP gateway
  ([AgentRun][agentrun]); AgentBay offers an MCP integration ([overview][agentbay]).
- **A2A:** an AgentRun case-study page titled as an A2A multi-agent example appeared in search; support
  level and spec version were **not read** (unverified).

## Identity, IdP and least privilege

- **Model Studio roles:** three workspace roles: super administrator (a primary account or a RAM user
  with `AliyunBailianFullAccess`), workspace administrator, regular user. Only super administrators
  set model rate limits or fine-tuning access; both admins manage users and API keys; regular users use
  authorized resources ([permissions][ms-perm]). A workspace is the smallest permission and cost
  allocation unit and cannot span regions.
- **RAM system policies (documented, [RAM permissions][ms-ram], updated 2026-10-11):**
  `AliyunBailianFullAccess`, `AliyunBailianReadOnlyAccess`, `AliyunBailianControlFullAccess`,
  `AliyunBailianControlReadOnlyAccess`, `AliyunBailianDataFullAccess`, `AliyunBailianDataReadOnlyAccess`.
  The page states these do not grant workspace permissions; those are granted inside Model Studio. Custom
  policies need `AliyunRAMFullAccess`. **Least-privilege reading:** builders get workspace admin plus a
  Data or Control policy; invoke-only callers get a regular-user workspace role and a workspace API key
  (a reading of the tables, not a vendor-stated recipe).
- **AgentRun RAM:** the RAM authorization page lists actions such as `agentrun:CreateAgentRuntime`,
  `CreateAgentRuntimeEndpoint`, `PublishRuntimeVersion`, `UpdateAgentRuntime` plus read actions; no
  system policy names were found, and no explicit invoke action was listed (`agentrun:GetAccessToken` is
  the nearest, purpose unconfirmed) ([RAM page][agentrun-ram]).
- **Agent identity and IdP:** Agent Identity supports **inbound** OAuth2/OIDC JWT validation (IdPs named:
  Alibaba Cloud, Okta, Microsoft Entra ID), **outbound** credentials (STS temporary credentials,
  third-party API keys/OAuth tokens, e.g. DingTalk) and a function-compute execution role; creating a
  workload identity needs `agentidentity:CreateWorkloadIdentity` plus RAM role/policy create actions
  ([tutorial][agentid]).
- **Workforce SSO:** RAM supports SAML 2.0 and OIDC role-based SSO and user SSO; Entra ID and Okta are
  named examples, IDaaS as a bridge ([SSO overview][ram-sso], search summary; page not read in full).

## Licences and consumption — who needs one

- **No per-user software licence** was found for building or invoking agents; billing is consumption:
  model calls by input/output tokens, knowledge base pay-as-you-go, some MCP services per model call
  or with third-party API fees, cache hits ([Agent 2.0][ms-agent2]); Function Compute-based AgentRun is
  billed by invocations and resources (search summary of its docs, not read).
- **Seat-based exception:** the **Token Plan (Team Edition)** is a subscription billed in Credits whose
  minimum unit is a *seat* bound to one member and one API key (not shareable); limited to interactive
  use in coding/agent tools, with automated scripts and backends not permitted; Singapore only
  ([Token Plan Team][token-plan], updated 2026-11-17). So: developers using coding agents need a seat;
  production agents call the pay-as-you-go API.
- Primary account activation grants `AliyunBailianFullAccess` by default ([RAM permissions][ms-ram]).

## Regions

Model Studio regions named: Singapore, US (Virginia), Germany (Frankfurt), Japan (Tokyo), China
(Beijing), China (Hong Kong) ([regions][ms-regions], updated 2026-11-12). Region fixes data storage;
a separate "service deployment scope" fixes inference location (e.g. Global, US, EU). Endpoints and keys
are region-specific; the legacy DashScope domain gets no new features after 2026-09-30 in favour of
workspace-dedicated domains. Token Plan Team: Singapore only. International vs mainland: all pages
read were English; **mainland-only features were not mapped**, and "AI guardrails" is stated as China
(Beijing) only.

## At a glance

| Item | Alibaba Cloud |
|---|---|
| Runtime | Model Studio managed apps; AgentRun serverless (Function Compute); AgentBay/Agent Sandbox for tool environments |
| Claude availability | Not found on any page read; Anthropic-compatible API serves Qwen; Claude Code listed as a client tool |
| MCP / A2A | MCP: documented in apps, AgentRun, AgentBay; A2A: unverified (case-study page only) |
| Memory | Agent 2.0 short-term 0-30 turns, long-term planned; AgentRun with Mem0/RAGFlow |
| Agent identity and IdP | Agent Identity (OIDC inbound incl. Okta/Entra, STS/OAuth outbound); RAM SAML/OIDC SSO |
| Least-privilege roles | Six `AliyunBailian*` policies + workspace roles; AgentRun action-level RAM (no system policy names found) |
| Licences and who needs one | Mostly pay-as-you-go; seat-based Token Plan (Team) for interactive coding tools; no prices here |
| Regions | Six Model Studio regions; Token Plan Team Singapore only |
| Release status | Agent 2.0 status unstated; AgentRun docs 2026-08-22; Qwen-Agent Apache-2.0, v0.0.26 (2025-05-29) |

## Cross-References

- [qwenpaw-analysis.md](qwenpaw-analysis.md) — related Qwen-family agent project in this corpus
- [ibm-agent-stack-analysis.md](ibm-agent-stack-analysis.md) — sibling cloud agent stack
- [microsoft-365-copilot-analysis.md](microsoft-365-copilot-analysis.md) — conventions and licence framing
- [agentic-enterprise-os-landscape.md][registries] — agent registries compared
- [data-platforms-lakehouse-landscape.md][data-platforms] — data platforms (linked only)

## Sources

| Source | Content |
|---|---|
| [Model service overview][ms-overview] | OpenAI/Anthropic-compatible endpoints, workspace domains (updated 2026-11-16) |
| [Recommended models][ms-models] | Qwen/DeepSeek/GLM/Kimi/MiniMax list; no Claude |
| [Agent Application (Agent 2.0)][ms-agent2] | tools, memory, publishing, billing metrics |
| [Permission management][ms-perm] | workspace roles and capability matrix (updated 2026-11-05) |
| [RAM permissions][ms-ram] | six system policies (updated 2026-10-11) |
| [Regions and deployment scopes][ms-regions] | regions, endpoints, scopes |
| [Token Plan (Team)][token-plan] | seat model, Credits, Singapore only |
| [AgentRun][agentrun] | runtime, sandbox, MCP, model proxy |
| [AgentRun RAM authorization][agentrun-ram] | action list |
| [Agent Identity in AgentRun][agentid] | inbound/outbound identity, IdPs |
| [AgentBay][agentbay] / [Agent Sandbox][sandbox] | execution environments |
| [RAM SSO overview][ram-sso] | SAML/OIDC SSO (secondary read) |
| [Qwen-Agent][qa-repo] / [README][qa-readme] | Apache-2.0, release v0.0.26 |

[data-platforms]: ../infrastructure/data-platforms-lakehouse-landscape.md
[registries]: ../frameworks/agentic-enterprise-os-landscape.md#agent-registries-compared
[ms-overview]: https://www.alibabacloud.com/help/en/model-studio/what-is-model-studio
[ms-models]: https://www.alibabacloud.com/help/en/model-studio/models
[ms-agent2]: https://help.aliyun.com/en/model-studio/new-single-agent-application
[ms-perm]: https://www.alibabacloud.com/help/en/model-studio/permission-management-overview
[ms-ram]: https://www.alibabacloud.com/help/en/model-studio/bailian-ram-permission
[ms-regions]: https://www.alibabacloud.com/help/en/model-studio/regions/
[token-plan]: https://www.alibabacloud.com/help/en/model-studio/token-plan-team-overview
[agentrun]: https://www.alibabacloud.com/help/en/agentrun/what-is-agentrun
[agentrun-ram]: https://help.aliyun.com/en/agentrun/api-agentrun-2025-09-10-ram
[agentid]: https://help.aliyun.com/en/agentidentity/using-agent-identity-in-agenrun
[agentbay]: https://www.alibabacloud.com/help/en/agentbay/product-overview/what-is-eds-agentbay
[sandbox]: https://www.alibabacloud.com/help/en/agent-sandbox/agent-sandbox-overview
[ram-sso]: https://help.aliyun.com/en/ram/sso-overview
[qa-repo]: https://github.com/QwenLM/Qwen-Agent
[qa-readme]: https://github.com/QwenLM/Qwen-Agent/blob/main/README.md
