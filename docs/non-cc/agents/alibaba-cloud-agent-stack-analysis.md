---
title: Alibaba Cloud Agent Stack Analysis — Model Studio, AgentRun, AgentBay, Qwen-Agent
purpose: "First-party fact-check of Alibaba Cloud's agent stack (Model Studio, AgentRun, AgentBay, Qwen-Agent): permissions, identity, licensing, MCP/A2A and Claude availability; no prices."
created: 2026-11-20
updated: 2026-11-20
validated_links: 2026-11-20
status: assess
---

**Details:** Feeds the cloud-agent-stacks synthesis (plan 0014 K34). Scope is business-and-dev agents on Alibaba Cloud. ML training is out of scope; data
platforms are only linked ([data-platforms-lakehouse-landscape.md][data-platforms]). No prices are
given; billing metrics are named only. Evidence is as of 2026-11-20: *documented* (Alibaba help pages
read now, English, mostly `alibabacloud.com/help/en`; a few pages only resolved on the English
`help.aliyun.com` mirror), or **unverified** (including "unverified (search snippet)": a claim that
rests only on a web-search summary, with the page itself not read). Alibaba docs change quickly (pages cited below were
updated Aug-Nov 2026), so re-read before relying on a detail.

## What each name is

| Name | What it is | Evidence |
|---|---|---|
| Model Studio (Bailian) | model service plus agent/workflow application builder, knowledge bases, Model Context Protocol (MCP), API keys, workspaces | documented ([overview][ms-overview], [agent 2.0][ms-agent2]) |
| Agent application (Agent 2.0) | agent that plans over tools (MCP, knowledge base, skills); Agent 1.0 is legacy and cannot be upgraded | documented ([page][ms-agent2]); GA vs preview not stated on the page |
| AgentRun (Alibaba Cloud) | serverless agent runtime on Function Compute, with sandbox, model proxy, tool hub, observability; not the Parcha-ai AgentRun catalogued in [orchestrators-landscape.md](../orchestrators/orchestrators-landscape.md) | documented ([page][agentrun]); last updated 2026-08-22 |
| Agent Identity | workload identity, credential and user-pool service for agents | documented ([AgentRun tutorial][agentid]) |
| AgentBay | cloud execution environments for agents: browser, code space, cloud computer, mobile | documented ([overview][agentbay]); last updated 2026-08-24 |
| Agent Sandbox | sandbox product (code, browser, desktop, mobile types) with E2B-SDK compatibility and Kubernetes APIs; a help page reportedly documents migrating AgentBay's Linux desktop to it | overview documented ([page][sandbox]); migration page **unverified (search snippet)**; relation to the open-source OpenSandbox (below) **not stated** on the pages read |
| Qwen-Agent | open-source Python agent framework from the Qwen team | documented ([repo][qa-repo], [README][qa-readme]) |

## Build and runtime

- **Model Studio applications:** an agent application (Agent 2.0) treats knowledge bases, MCP
  services and other capabilities as tools and plans which to call; skills, shell/file sandbox tools
  (off by default) and short-term memory (0 to 30 turns; long-term memory "planned") are described.
  An application must be published before invocation; its API details sit under the publish channel
  ([Agent 2.0][ms-agent2]). Workflow applications for fixed processes: **unverified (search snippet)**.
- **AgentRun** offers no-code (AI Studio), low-code and pro-code creation, a serverless runtime with
  session affinity and scale to zero (Python, Node.js, Java), a model proxy (fallback, load balancing,
  token-rate limiting), sandboxes (code interpreter, browser; "Computer/Mobile Use (Planned)"), and OpenTelemetry
  tracing with token-level cost attribution. It integrates LangChain, AgentScope, CrewAI and Google
  ADK, and can plug in Mem0 and RAGFlow for memory/Retrieval-Augmented Generation (RAG) ([AgentRun][agentrun]).
- **AgentBay** provides four environments (browser, code space, cloud computer, mobile) through SDK and
  MCP ([overview][agentbay]).
- **OpenSandbox:** Alibaba's open-source sandbox is covered in
  [CC-sandbox-platforms-landscape.md](../../cc-native/sandboxing/CC-sandbox-platforms-landscape.md);
  none of the AgentBay, Agent Sandbox or AgentRun pages read mention it, so any relation is
  **unverified**.
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
  Claude Code as a supported *client tool* pointing at the plan's own OpenAI/Anthropic-compatible base URL
  ([Token Plan Team][token-plan]). Both mean "Claude-shaped API/client, Qwen model", not Claude.
- AgentRun's model proxy can point at API or self-hosted models, so a customer's own Claude API key
  behind a custom endpoint is architecturally possible; not documented as a supported Claude path.

## MCP and A2A

- **MCP:** agent and workflow applications use official or custom MCP services; AgentRun converts
  agents, sandboxes and API tools into MCP and can bundle them behind an MCP gateway
  ([AgentRun][agentrun]); AgentBay offers an MCP integration ([overview][agentbay]).
- **A2A (consumer side, documented):** Model Studio's third-party agent integration page ([page][ms-a2a], read
  2026-11-20; it sits under the Multimodal Interaction Developer Suite, so scope is that suite, not all of Model Studio) says integrations
  "must be based on the Google A2A protocol" and links the Agent-to-Agent Protocol (A2A) 0.2.5 specification; it lists AgentCard fields, with an `apiKey` security option.
- **A2A (AgentRun, tutorial only):** the "Xixi Coffee Shop" best-practice page ([page][ms-a2acase],
  updated 2026-08-24, read 2026-11-20) deploys a template whose "order" and "delivery" agents appear as
  "A2A services" in its web UI. It is a worked example; the AgentRun data-structure page read
  ([ProtocolConfiguration][ar-proto], read 2026-11-20) shows `HTTP` as the example protocol type and does not mention A2A,
  so a native AgentRun A2A endpoint and its spec version are **not stated** on the pages read.

## Identity, IdP and least privilege

- **Model Studio roles:** three workspace roles: super administrator (a primary account or a RAM user
  with `AliyunBailianFullAccess`), workspace administrator, regular user. Only super administrators
  set model rate limits or fine-tuning access; both admins manage users and API keys; regular users use
  authorized resources ([permissions][ms-perm]). Holding `AliyunBailianFullAccess` is what makes a RAM
  user a super administrator; the other five policies grant management/data API permissions but,
  per the [RAM page][ms-ram], no workspace permissions, which are assigned inside Model Studio. A workspace is the smallest permission and cost
  allocation unit and cannot span regions.
- **RAM system policies (documented, [RAM permissions][ms-ram], updated 2026-10-11):**
  `AliyunBailianFullAccess`, `AliyunBailianReadOnlyAccess`, `AliyunBailianControlFullAccess`,
  `AliyunBailianControlReadOnlyAccess`, `AliyunBailianDataFullAccess`, `AliyunBailianDataReadOnlyAccess`.
  Per the page, `AliyunBailianFullAccess` also does not grant workspace permissions by itself (see the
  super-administrator reading above); the page and the permissions page are not fully consistent,
  so verify in the console. Custom policies need `AliyunRAMFullAccess`. **Least-privilege reading:** builders get workspace admin plus a
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
  ([tutorial][agentid]). Activating Model Studio on a primary account grants it
  `AliyunBailianFullAccess` by default ([RAM permissions][ms-ram]).
- **Workforce SSO:** RAM supports user-based SSO (SAML only) and role-based SSO (SAML 2.0 for console login,
  OIDC via `AssumeRoleWithOIDC` for API access) ([SSO overview][ram-sso]; documented, read 2026-11-20,
  page metadata "Updated at" 2026-05-27). Named IdPs: AD FS, Entra ID, Okta, Google Workspace, Alibaba Cloud IDaaS.

## Licences and consumption — who needs one

- **No per-user software licence** was found for building or invoking agents; billing is consumption:
  model calls by input/output tokens, knowledge base pay-as-you-go, some MCP services per model call
  or with third-party API fees, cache hits ([Agent 2.0][ms-agent2]); AgentRun billing by invocations
  and resources on Function Compute is **unverified (search snippet)**.
- **Seat-based exception:** the **Token Plan (Team Edition)** is a subscription billed in Credits whose
  minimum unit is a *seat* bound to one member and one API key (not shareable); limited to interactive
  use in coding/agent tools, with automated scripts and backends not permitted; Singapore only
  ([Token Plan Team][token-plan], updated 2026-11-17). So: developers using coding agents need a seat;
  production agents call the pay-as-you-go API.

## Regions

Model Studio regions named: Singapore, US (Virginia), Germany (Frankfurt), Japan (Tokyo), China
(Beijing), China (Hong Kong) ([regions][ms-regions], updated 2026-11-12). Region fixes data storage;
a separate "service deployment scope" fixes inference location (e.g. Global, US, EU). Endpoints and keys
are region-specific; the legacy DashScope domain gets no new features after 2026-09-30 in favour of
workspace-dedicated domains. Token Plan Team: Singapore only. International vs mainland: all pages
read were English; **mainland-only features were not mapped**, and "AI guardrails" is stated as China
(Beijing) only.

## At a glance

| Dimension | Alibaba Cloud |
|---|---|
| Runtime | Model Studio managed apps; AgentRun serverless (Function Compute); AgentBay and Agent Sandbox for tool environments |
| Claude availability | Not found on any page read; Anthropic-compatible API serves Qwen; Claude Code listed as a client tool |
| MCP / A2A | MCP: documented in apps, AgentRun, AgentBay; A2A: third-party agent integration in Model Studio's Multimodal Interaction Developer Suite must use A2A (links the 0.2.5 spec); AgentRun tutorial; native AgentRun A2A endpoint not stated |
| Memory | Agent 2.0 short-term 0-30 turns, long-term planned; AgentRun with Mem0/RAGFlow |
| Agent identity and IdP | Agent Identity (OIDC inbound incl. Okta/Entra, STS/OAuth outbound); RAM SAML 2.0 / OIDC SSO (documented) |
| Least-privilege roles | Six `AliyunBailian*` policies + workspace roles; AgentRun action-level RAM (no system policy names found) |
| Licences and who needs one | Mostly pay-as-you-go (AgentRun billing unverified, search snippet); seat-based Token Plan (Team) for interactive coding tools; no prices here |
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
| [RAM SSO overview][ram-sso] | SAML 2.0 / OIDC SSO, IdPs, user- vs role-based |
| [Third-party agent integration][ms-a2a] | must use A2A (links 0.2.5 spec), AgentCard; Multimodal Interaction Developer Suite |
| [Xixi Coffee Shop tutorial][ms-a2acase] | AgentRun A2A multi-agent example |
| [ProtocolConfiguration][ar-proto] | AgentRun protocol type (`HTTP` as example; no A2A mention) |
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
[ram-sso]: https://www.alibabacloud.com/help/en/ram/user-guide/sso-overview
[ms-a2a]: https://www.alibabacloud.com/help/en/model-studio/multimodal-integration-a2a
[ms-a2acase]: https://www.alibabacloud.com/help/en/agentrun/cech-coffee-shop-agenrun-a2a-protocol-multi-agent-case
[ar-proto]: https://www.alibabacloud.com/help/en/agentrun/api-agentrun-2025-09-10-struct-protocolconfiguration
[qa-repo]: https://github.com/QwenLM/Qwen-Agent
[qa-readme]: https://github.com/QwenLM/Qwen-Agent/blob/main/README.md
