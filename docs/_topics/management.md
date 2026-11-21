# Topic Hub: Agent Management

Running many agents: fleet policy, registries and inventory, cost attribution, identity, licences
and lifecycle. Pointers only; see [the hub index](README.md).

## Claude Code fleets

| Doc / section | What it covers | Bucket |
|---|---|---|
| [CC-managed-settings-fleet-analysis.md § Four delivery channels](../cc-native/configuration/CC-managed-settings-fleet-analysis.md#four-delivery-channels) | How the managed settings tier reaches a fleet | cc-native |
| [CC-managed-settings-fleet-analysis.md § Ranking and combining](../cc-native/configuration/CC-managed-settings-fleet-analysis.md#ranking-and-combining) | Which managed source wins, and how sources combine | cc-native |
| [CC-managed-settings-fleet-analysis.md § Checking that a policy is in force](../cc-native/configuration/CC-managed-settings-fleet-analysis.md#checking-that-a-policy-is-in-force) | Confirming a policy is applied | cc-native |
| [CC-managed-settings-fleet-analysis.md § Fleet scope: what this doesn't give you](../cc-native/configuration/CC-managed-settings-fleet-analysis.md#fleet-scope-what-this-doesnt-give-you) | Policy, not inventory: no org-level agent registry; telemetry instead | cc-native |
| [CC-permissions-bypass-analysis.md § Disabling Organization-Wide](../cc-native/sandboxing/CC-permissions-bypass-analysis.md#disabling-organization-wide) | Turning off permission bypass for an organization | cc-native |
| [CC-mods-function-hooks-analysis.md § Governance](../cc-native/plugins-ecosystem/CC-mods-function-hooks-analysis.md#governance) | Built-in guard mod that protects what an organization manages | cc-native |
| [CC-memory-system-analysis.md § Organization-Wide Managed CLAUDE.md](../cc-native/context-memory/CC-memory-system-analysis.md#organization-wide-managed-claudemd) | Organization-wide managed CLAUDE.md | cc-native |
| [CC-skills-adoption-analysis.md § Organization-Level Skill Provisioning (Claude Team and Enterprise)](../cc-native/agents-skills/CC-skills-adoption-analysis.md#organization-level-skill-provisioning-claude-team-and-enterprise) | Provisioning skills for Team and Enterprise | cc-native |
| [CC-multi-account-switching-landscape.md](../cc-community/CC-multi-account-switching-landscape.md) | Running several Claude Code subscription accounts via `CLAUDE_CONFIG_DIR` and tools built on it | cc-community |

## Cost attribution

| Doc / section | What it covers | Bucket |
|---|---|---|
| [CC-monitoring-telemetry-analysis.md § Cost attribution](../cc-native/configuration/CC-monitoring-telemetry-analysis.md#cost-attribution) | Team and cost-centre tags, per-subagent spend from `agent_id`, per-user options by billing path | cc-native |
| [CC-web-auth-setup-analysis.md § Monitoring Org Spend — Usage and Cost Admin API](../cc-native/ci-remote/CC-web-auth-setup-analysis.md#monitoring-org-spend--usage-and-cost-admin-api) | Org-wide spend by key and workspace | cc-native |

## Registries and inventory

| Doc / section | What it covers | Bucket |
|---|---|---|
| [agentic-enterprise-os-landscape.md § Agent registries compared](../non-cc/frameworks/agentic-enterprise-os-landscape.md#agent-registries-compared) | A2A agent cards, MCP Registry, AWS, Google Cloud, Agent 365, Agentforce: versions, ownership, retirement | non-cc |
| [microsoft-365-copilot-analysis.md § Governance: Agent 365 covers agents, not SharePoint skills](../non-cc/agents/microsoft-365-copilot-analysis.md#governance-agent-365-covers-agents-not-sharepoint-skills) | What Agent 365 governs and what it doesn't | non-cc |
| [microsoft-365-copilot-analysis.md § Microsoft agent stack (2026-11-18)](../non-cc/agents/microsoft-365-copilot-analysis.md#microsoft-agent-stack-2026-11-18) | Frontier, Foundry, Copilot Studio, Agent 365 and the other names | non-cc |
| [salesforce-agentforce-analysis.md § Agentforce Registry and MuleSoft Agent Fabric](../non-cc/agents/salesforce-agentforce-analysis.md#agentforce-registry-and-mulesoft-agent-fabric) | Agentforce Registry and MuleSoft Agent Fabric | non-cc |
| [zed-analysis.md § External agents and the ACP Registry](../non-cc/coding-agents/zed-analysis.md#external-agents-and-the-acp-registry) | Installing external agents from the ACP Registry | non-cc |

## Cloud agent stacks

| Doc / section | What it covers | Bucket |
|---|---|---|
| [cloud-agent-platforms-landscape.md](../non-cc/infrastructure/cloud-agent-platforms-landscape.md) | Six cloud agent stacks compared in one dated table (no prices) | non-cc |
| [aws-agent-stack-analysis.md](../non-cc/agents/aws-agent-stack-analysis.md) | AWS: AgentCore, Bedrock Agents, Amazon Quick; IAM roles, identity, licences | non-cc |
| [google-cloud-agent-stack-analysis.md](../non-cc/agents/google-cloud-agent-stack-analysis.md) | Google Cloud: Agent Platform, ADK, Gemini Enterprise; roles, identity, licences | non-cc |
| [microsoft-365-copilot-analysis.md § Roles, identity and licences](../non-cc/agents/microsoft-365-copilot-analysis.md#roles-identity-and-licences) | Azure/Foundry: RBAC roles, managed identity, Entra agent identity, licences | non-cc |
| [oracle-cloud-agent-stack-analysis.md](../non-cc/agents/oracle-cloud-agent-stack-analysis.md) | Oracle: OCI Generative AI Agents, Fusion AI Agent Studio; IAM, licences | non-cc |
| [ibm-agent-stack-analysis.md](../non-cc/agents/ibm-agent-stack-analysis.md) | IBM: watsonx Orchestrate and ADK; connections, MAU plans | non-cc |
| [alibaba-cloud-agent-stack-analysis.md](../non-cc/agents/alibaba-cloud-agent-stack-analysis.md) | Alibaba Cloud: Model Studio, AgentRun, Agent Identity; RAM policies, licences | non-cc |

## Identity, licences and lifecycle

| Doc / section | What it covers | Bucket |
|---|---|---|
| [agent-identity-auth-landscape.md § 1. Authenticate the agent (agent as a first-class principal)](../sdlc-lcm/agent-identity-auth-landscape.md#1-authenticate-the-agent-agent-as-a-first-class-principal) | The agent as a first-class principal | sdlc-lcm |
| [agent-identity-auth-landscape.md § 2. Authorize the agent on behalf of a human (delegated, scoped, auditable)](../sdlc-lcm/agent-identity-auth-landscape.md#2-authorize-the-agent-on-behalf-of-a-human-delegated-scoped-auditable) | Delegated, scoped, auditable authorization | sdlc-lcm |
| [salesforce-agentforce-analysis.md § Licences and roles for Agentforce agents](../non-cc/agents/salesforce-agentforce-analysis.md#licences-and-roles-for-agentforce-agents) | Licences and roles for Agentforce agents | non-cc |
| [salesforce-agentforce-analysis.md § Best Practices: Agent Development Lifecycle](../non-cc/agents/salesforce-agentforce-analysis.md#best-practices-agent-development-lifecycle) | Agent development lifecycle practices | non-cc |
| [agentic-sdlc-patterns.md § 1. ADLC (Agentic Development Lifecycle)](../sdlc-lcm/agentic-sdlc-patterns.md#1-adlc-agentic-development-lifecycle) | ADLC: lifecycle for LLM-centred products | sdlc-lcm |

Related hubs: [cost.md](cost.md), [security.md](security.md), [plugins.md](plugins.md), [long-running.md](long-running.md).
