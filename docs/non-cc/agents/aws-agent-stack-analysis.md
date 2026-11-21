---
title: AWS Agent Stack Analysis — Bedrock AgentCore, Agents Classic, Quick
purpose: First-party read of what AWS ships for business and developer agents (services, least-privilege IAM, identity and IdP integration, licences, regions, release status), with Claude availability; no prices.
created: 2026-11-20
updated: 2026-11-20
validated_links: 2026-11-20
status: assess
---

## What It Is

A first-party map of the AWS agent stack (Bedrock AgentCore, Bedrock Agents Classic, AWS Quick) for
business and developer agents, aimed at the roles, identity and licence questions a platform team asks.

**Scope.** Business and developer agents on AWS: what each service is, which IAM actions and managed policies
build, deploy and invoke an agent, how identity and IdP integration work, and who needs a licence. ML
training is out of scope; data platforms are covered in
[data-platforms-lakehouse-landscape.md][data-platforms]; prices are deliberately omitted. Evidence level is
**documented** (AWS docs read 2026-11-20) unless a line says otherwise. Product names are as the docs state
them today; AWS renames often.

## What each name is

| Name | What it is (per its own docs) | Status as read |
|---|---|---|
| **Amazon Bedrock AgentCore** | Modular agent platform: Harness, Runtime, Memory, Gateway, Identity, Code Interpreter, Browser, Observability, Payments, Evaluations, Optimization, Policy, Registry; each usable alone, framework- and model-agnostic ([overview][ac-overview]) | GA announced 2025-10-13 ([announcement][ac-ga]); individual later services (Payments, Optimization, Policy) carry no per-service stage on the overview page |
| **AWS Agent Registry** (AgentCore Registry) | Catalog for agents, Model Context Protocol (MCP) servers, skills and custom records across clouds; comparison with other registries in [Agent registries compared][registries] — not repeated here | GA, posted 2026-08-31 ([GA post][registry-ga]) |
| **Amazon Bedrock Agents Classic** | The older configure-an-agent service (action groups, knowledge bases) | New sign-ups closed; existing users continue; docs point to AgentCore and the Strands Agents SDK ([Bedrock user guide][agents-classic]) |
| **AWS Quick** | Workspace product for chat, research, flows, automation, apps and BI; "evolved from Amazon QuickSight", which continues as Quick Sight ([what is Quick][quick-what]) | Current product; no GA date read |
| **Amazon Q Business** | Earlier enterprise assistant | "No longer open to new customers"; docs point to Quick ([Q Business][qbiz]) |
| **Kiro** | AWS coding agent | Pointer only: [kiro-analysis.md][kiro] |

## Build and deploy: AgentCore services

- **Runtime** hosts agents and tools serverless with per-session isolation and supports MCP and A2A, the Agent-to-Agent Protocol (A2A
  governance and version caveats, including that AgentCore's sample pins an older `a2a-sdk` line:
  [ag-ui-protocol-landscape.md § A2A][a2a]); it names
  CrewAI, LangGraph, LlamaIndex, Google ADK, OpenAI Agents SDK and Strands Agents, and models including
  Anthropic's Claude, Amazon Nova, Gemini, OpenAI and Llama ([overview][ac-overview]).
- **Harness** is a managed agent loop (one API call, model + prompt + tools inline, microVM per session)
  ([overview][ac-overview]). Strands Agents, the AWS framework, is placed in
  [agent-frameworks-infrastructure-landscape.md][frameworks].
- **Gateway** turns APIs, Lambda functions and existing MCP servers into MCP tools; **Policy** intercepts each
  tool call at the Gateway and evaluates rules written in natural language or a Cedar-compatible language
  the docs call "Dogwood" ([overview][ac-overview]).
- **Memory** gives short-term (multi-turn) and long-term (cross-session) stores that can be shared across
  agents ([overview][ac-overview]).
- **Observability** emits OpenTelemetry-compatible traces, integrated with CloudWatch ([overview][ac-overview]).

Claude on AWS has two separate paths. Amazon Bedrock is AWS-managed: CC setup (env variables) is in
[CC-model-provider-configuration.md § AWS Bedrock][cc-bedrock]; not restated. **Claude Platform on AWS** is
the Anthropic-managed path, documented separately by [Claude Code][cc-cpoaws]; the corpus tracks which
features differ in [CC-advisor-tool-analysis.md][cc-advisor] (the advisor tool is available to API callers
there, not to Claude Code). For an
AgentCore-hosted agent calling Claude, the documented execution-role actions are `bedrock:InvokeModel` and
`bedrock:InvokeModelWithResponseStream` ([runtime permissions][ac-perm]).

## Least-privilege roles

| Persona | What to grant | Source and caveat |
|---|---|---|
| **Platform admin / builder** | AWS managed policy `BedrockAgentCoreFullAccess` (full AgentCore access plus IAM list/get and pass-role for roles with "BedrockAgentCore" in the name) | [Managed policies][ac-mp]. Broad by design |
| **Deployer (CLI)** | No single policy: the identity running `agentcore deploy` needs CDK and CloudFormation stack permissions, ability to pass or create IAM roles, and S3, ECR, CodeBuild, CloudWatch Logs and AgentCore access | [Runtime permissions][ac-perm] says outright that "there isn't one least-privilege policy" for every project |
| **Runtime execution role** (the agent itself) | A role the Runtime assumes: Bedrock model invocation, workload-token actions, plus per-resource needs | [Runtime permissions][ac-perm] |
| **Invoker** | `bedrock-agentcore:InvokeAgentRuntime` (also `InvokeAgentRuntimeForUser`, `InvokeAgentRuntimeCommand`, `InvokeHarness`, `InvokeCodeInterpreter`) on the specific runtime ARN, or a JWT bearer token when the runtime uses an inbound JWT authorizer | Action names from the [service authorization reference][ac-actions]; no narrower AWS managed invoker policy was found on the managed-policy page |
| **Classic Bedrock Agents** | A service role for the agent; for multi-agent collaboration the page grants `bedrock:GetAgentAlias` and `bedrock:InvokeAgent` to the supervisor agent's service role. The caller-side grant was not read here | [Bedrock Agents permissions][agents-perm]; caller side **unverified** |

Three service-linked or service-role policies exist only for AgentCore internals
(`BedrockAgentCoreNetworkServiceRolePolicy`, `BedrockAgentCoreRuntimeIdentityServiceRolePolicy`,
`BedrockAgentCoreRuntimeInstancesServiceRolePolicy`) and cannot be attached to users
([managed policies][ac-mp]).

**Watch-out (documented).** `BedrockAgentCoreFullAccess` includes `GetWorkloadAccessTokenForUserId`, which
issues workload tokens from a caller-supplied user ID without IdP token verification. AWS recommends a
custom policy and, where JWTs are available, denying that action and granting only
`GetWorkloadAccessTokenForJWT` ([runtime permissions][ac-perm]). Treat the full-access policy as a
bootstrap, not a production grant.

## Identity and IdP integration

- **Humans (console, CLI):** federation with an IdP, with IAM Identity Center recommended for centralized
  access ([IAM overview][ac-iam]).
- **Inbound to Runtime or Gateway:** an OAuth 2.0 JWT authorizer, "IdP agnostic": configured with an
  OIDC or RFC 8414 discovery URL, allowed audiences, clients and scopes. For shared issuers such as GitHub
  Actions or GitLab, add a claim rule so only your tokens pass ([inbound authorizer][ac-inbound]). SigV4
  (IAM) inbound is the alternative ([Runtime auth][ac-rtauth]).
- **Agent identity:** AgentCore Identity models agents as workload identities and says it works with
  existing IdPs (Cognito, Okta, Entra ID, Auth0 named) without user migration ([overview][ac-overview];
  [Identity][ac-identity]).
- **Outbound:** credential providers hold OAuth2 tokens, API keys, client certificates or SAML assertions
  so agents never hold long-term secrets or refresh tokens ([credential providers][ac-outbound]).
- **Quick:** console-provisioned accounts use IAM Identity Center or IAM federation ([what is Quick][quick-what]);
  the email sign-up path needs no AWS account ([setup][quick-setup]).

## Licences: who needs one

AgentCore is consumption-billed with no upfront commitments or minimums ([overview][ac-overview]); the
docs read describe no per-seat licence for builders or callers of a deployed agent beyond IAM access
(**inferred** from absence, not stated). **AWS Quick is
per-user.** Documented plans: Free, Plus and Max (email sign-up, no AWS account) and Essentials,
Professional and Enterprise (console-provisioned, per-user subscriptions on standard AWS billing)
([Quick setup][quick-setup], [Quick plans][quick-plans]). Plans differ in monthly per-user allowances of "agent
hours" and index storage, with limit profiles an admin can set per user or role; Quick Automate and
dashboard authoring need Enterprise. Allowance figures change, so read the live page.
**Kiro** (developer IDE and CLI) is also per-user: Free, Pro, Pro+, Pro Max and Power individual plans, with
Team and Enterprise adding SAML/SCIM SSO through IAM Identity Center ([kiro-analysis.md][kiro]).
Amazon Q Developer is covered in [amazon-q-developer-analysis.md][qdev]. Amazon Q Business charged for user-subscription tiers plus index
capacity ([Q Business][qbiz]); its tier names were not read and are **unverified**.

## Regions

The [AgentCore region table][ac-regions] (read 2026-11-20) lists 22 columns including GovCloud (US-West).
Runtime microVMs, Gateway, Identity, Observability and Policy show "Yes" in every column; Harness, Memory,
Runtime Instances and Agent Registry are subsets (Registry 10 of the 22 columns, so the
five-region count at GA has grown). Check the table for the exact region before planning.

## At a glance

| Dimension | AWS |
|---|---|
| Runtime | AgentCore Runtime (serverless, session-isolated) and Harness; Agents Classic closed to new users |
| Claude availability | Yes: Bedrock (AWS-managed, [CC doc][cc-bedrock]) and Claude Platform on AWS (Anthropic-managed, [CC docs][cc-cpoaws]); Runtime names Claude among supported models |
| MCP / A2A | MCP and A2A on Runtime (A2A caveats: [ag-ui § A2A][a2a]); Gateway exposes APIs and Lambda as MCP tools |
| Memory | AgentCore Memory (short- and long-term, shareable) |
| Agent identity and IdP | AgentCore Identity (workload identities); inbound JWT from any OIDC/OAuth IdP; IAM Identity Center for people |
| Least-privilege roles | `BedrockAgentCoreFullAccess` is broad; per-resource invoke and custom policies recommended; no one deploy policy |
| Licences and seats | AgentCore consumption-only (no seat found, inferred); AWS Quick per-user plans; Kiro per-user plans ([kiro-analysis.md][kiro]); Q Business closed to new customers |
| Regions | AgentCore in up to 22 listed regions, feature-dependent |
| Release status | AgentCore GA 2025-10-13; Registry GA 2026-08-31; Agents Classic maintenance; Quick current |

## Sources

| Ref | Source | Established |
|---|---|---|
| [ac-overview] | [AgentCore overview][ac-overview] | Services, frameworks, models, consumption billing |
| [ac-ga] | [AgentCore GA announcement][ac-ga] | GA 2025-10-13 |
| [registry-ga] | [AWS Agent Registry GA][registry-ga] | GA 2026-08-31 |
| [ac-mp] | [Managed policies][ac-mp] | `BedrockAgentCoreFullAccess` and service-role policies |
| [ac-perm] | [Runtime permissions][ac-perm] | Deploy and execution-role needs; workload-token watch-out |
| [ac-actions] | [Service authorization reference][ac-actions] | Action names |
| [ac-iam] | [IAM and AgentCore][ac-iam] | Federation, Identity Center |
| [ac-inbound] | [Inbound JWT authorizer][ac-inbound] | IdP-agnostic JWT config |
| [ac-rtauth] | [Runtime inbound and outbound auth][ac-rtauth] | SigV4 and JWT paths |
| [ac-identity] | [AgentCore Identity][ac-identity] | Workload identities, IdPs |
| [ac-outbound] | [Credential providers][ac-outbound] | Credential types |
| [ac-regions] | [Supported regions][ac-regions] | Region table |
| [agents-classic] | [Bedrock Agents][agents-classic] | Classic closed to new sign-ups |
| [agents-perm] | [Agents permissions][agents-perm] | Service role, `bedrock:InvokeAgent` |
| [quick-what] | [What is Quick][quick-what] | Quick scope, QuickSight lineage |
| [quick-setup] | [Setting up Quick][quick-setup] | Plan names, IAM Identity Center |
| [quick-plans] | [Quick pricing page][quick-plans] | Six plan names, allowance concept (figures not copied) |
| [qbiz] | [Q Business][qbiz] | Closed to new customers |

## Cross-References

- [agentic-enterprise-os-landscape.md § Agent registries compared][registries] — registry comparison.
- [CC-model-provider-configuration.md][cc-bedrock] — Claude via Bedrock.
- [kiro-analysis.md][kiro], [amazon-q-developer-analysis.md][qdev] — AWS developer agents.
- [ag-ui-protocol-landscape.md § A2A][a2a] — A2A governance and version caveats.
- [microsoft-365-copilot-analysis.md](microsoft-365-copilot-analysis.md) and
  [salesforce-agentforce-analysis.md](salesforce-agentforce-analysis.md) — sibling enterprise stacks.
- [data-platforms-lakehouse-landscape.md][data-platforms] — data platforms, not covered here.

[ac-overview]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
[ac-ga]: https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available/
[registry-ga]: https://aws.amazon.com/about-aws/whats-new/2026/08/aws-agent-registry-generally-available
[ac-mp]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/security-iam-awsmanpol.html
[ac-perm]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-permissions.html
[ac-actions]: https://docs.aws.amazon.com/service-authorization/latest/reference/list_amazonbedrockagentcore.html
[ac-iam]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/security-iam.html
[ac-inbound]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/inbound-jwt-authorizer.html
[ac-rtauth]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-oauth.html
[ac-identity]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity.html
[ac-outbound]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/identity-outbound-credential-provider.html
[ac-regions]: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-regions.html
[agents-classic]: https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html
[agents-perm]: https://docs.aws.amazon.com/bedrock/latest/userguide/agents-permissions.html
[quick-what]: https://docs.aws.amazon.com/quick/latest/userguide/what-is.html
[quick-setup]: https://docs.aws.amazon.com/quick/latest/userguide/setting-up.html
[quick-plans]: https://aws.amazon.com/quick/pricing/
[qbiz]: https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/what-is.html
[registries]: ../frameworks/agentic-enterprise-os-landscape.md#agent-registries-compared
[cc-bedrock]: ../../cc-native/configuration/CC-model-provider-configuration.md#aws-bedrock
[kiro]: ../coding-agents/kiro-analysis.md
[qdev]: ../coding-agents/amazon-q-developer-analysis.md
[frameworks]: ../frameworks/agent-frameworks-infrastructure-landscape.md
[a2a]: ../protocols/ag-ui-protocol-landscape.md#a2a-agent-to-agent-protocol
[cc-cpoaws]: https://code.claude.com/docs/en/claude-platform-on-aws
[cc-advisor]: ../../cc-native/configuration/CC-advisor-tool-analysis.md
[data-platforms]: ../infrastructure/data-platforms-lakehouse-landscape.md
