---
title: Google Cloud Agent Stack Analysis — Gemini Enterprise Agent Platform, ADK, Gemini Enterprise
purpose: First-party read of what Google Cloud ships for business and developer agents (renamed platform, runtime, identity, gateway, registry, IAM roles, seats and editions, regions, release status), with Claude availability; no prices.
category: non-cc / agents
created: 2026-11-20
updated: 2026-11-20
validated_links: 2026-11-20
status: assess
---

**Scope.** Business and developer agents on Google Cloud: services, the IAM roles that build, deploy and
invoke agents, agent identity and IdP integration, and who needs a seat. ML training is out of scope; data
platforms are covered in [data-platforms-lakehouse-landscape.md][data-platforms]; prices are omitted.
Evidence is **documented** (Google docs read 2026-11-20) unless stated. The release notes are the dating
source: product pages often carry no stage label.

## Naming: Vertex AI is now Gemini Enterprise Agent Platform

The platform docs describe Gemini Enterprise Agent Platform as "an evolution of Vertex AI" and keep a
[name-change table][names]. Release notes dated 2026-04-22 record that Agent Builder is now part of the
platform and **Agent Engine is now Agent Runtime**, Agent Builder Sessions is Agent Platform Sessions, and
Memory Bank is Agent Platform Memory Bank ([release notes][relnotes]). Vertex AI Studio became Agent Studio.
Older posts and SDKs may still say Vertex AI or Agent Engine; the docs' API surface uses an `agentplatform`
Python client with `reasoningEngines` still in IAM permission names.

## What each name is

| Name | What it is (per docs) | Status as read |
|---|---|---|
| **Gemini Enterprise Agent Platform** | Build, scale, govern, optimize pillars; 200+ models in Model Garden ([overview][overview]) | Platform; stages are per feature |
| **Agent Development Kit (ADK)** | Modular, model-agnostic open-source framework; repo [google/adk-python][adk] is Apache-2.0, latest release v2.15.0 (2026-11-19) | Shipped |
| **Agent Studio / Agent Garden** | Low-code canvas and prebuilt agents/templates ([overview][overview]) | Per-feature; not dated here |
| **Agent Runtime** (ex Agent Engine) | Managed runtime for deployed agents, with Sessions, Memory Bank and sandboxed code execution; long-running operations up to 7 days per the 2026-04-22 note | Renamed 2026-04-22; GA date of the runtime itself not re-verified |
| **Agent Identity** | Per-agent identity tied to the agent's lifecycle | GA per release note of 2026-04-22; its newer `agentidentity.googleapis.com` API is in Preview |
| **Agent Gateway** | Policy enforcement and networking layer for agent, tool and model traffic; Model Armor attaches to it | GA per release notes of 2026-06-18 and 2026-06-24; Agent Gateway for GKE Preview 2026-11-12 |
| **Agent Registry** | Catalog of agents, MCP servers, tools and endpoints; comparison in [Agent registries compared][registries], not repeated | GA per release note of 2026-06-18 (standalone skills Preview) |
| **Managed Agents API** | Config-driven REST API for agents in a managed sandbox | Stage not read |
| **Gemini Enterprise** | Business product: search, assistant, no-code agents, agent marketplace ([overview][ge-overview]) | Editions below; no-code agent builder labelled preview in the editions table |
| **A2A** | Agent2Agent protocol, under the Linux Foundation; spec site and releases at [a2a-protocol.org][a2a]; v1.0.1 released 2026-05-28 per the [A2A repo][a2a-repo] | Open standard; Agent Runtime lists A2A as a supported way to use agents |

Note for the registry comparison: the enterprise-OS doc records no product-level label for Google's
registry on the two pages it read; the release notes (2026-06-18) do state GA. That doc is not edited here.

## Claude on Google Cloud

Claude models are served on the platform: the [Claude page][claude-page] lists model names for the
Anthropic SDK path (the current list includes Claude Opus 5.5, Sonnet 5.5 and Haiku 5.5, read 2026-11-20).
CC setup is in [CC-model-provider-configuration.md § Google Vertex AI][cc-vertex]; not restated. In Gemini
Enterprise, Claude Opus 5.5 and Sonnet 5.5 are partner models for AI developer tools: an admin must enable them
and usage is billed pay-as-you-go ([editions][ge-editions]). Any extra enablement or quota step for Claude
on the platform was not read and is **unverified**.

## Least-privilege roles

All names read from the [IAM aiplatform roles page][roles] (2026-11-20).

| Persona | Predefined role | Note |
|---|---|---|
| Platform admin | `roles/aiplatform.admin` | Full access to all platform resources |
| Developer using everything | `roles/aiplatform.user` | "Use all resources"; includes `aiplatform.reasoningEngines.create/get/list/query/update/delete` |
| Agent catalog: view, create, task use | `roles/aiplatform.agentsViewer`, `agentsCreator`, `agentsUser`, `agentsAdmin` | Viewer read-only; Creator creates and discovers agents and auth providers; User also creates and cancels tasks; Admin manages agent memories and access policies. Some agent roles are marked Beta |
| Memory Bank | `roles/aiplatform.memoryViewer`, `memoryEditor`, `memoryUser` | Scoped to memories and revisions |
| Sessions | `roles/aiplatform.sessionViewer`, `sessionEditor`, `sessionUser` | Scoped to sessions and events |
| Registry | `agentregistry.*` permissions (for example `agentregistry.agents.get/list`) | `roles/agentregistry.viewer` is referenced on the Agent Identity page |
| Runtime service agent | `roles/aiplatform.reasoningEngineServiceAgent` | Google-managed; do not grant to principals |

Invoke path: no runtime-only predefined invoker role was found on the roles page. The Agent Identity
page's own guidance for agent-to-agent calls is a custom role holding only `aiplatform.reasoningEngines.query`
and `aiplatform.reasoningEngines.get`, bound to the target agent's resource, rather than a project-wide grant
([Agent Identity][ident]). That is the documented least-privilege pattern.

## Identity and IdP integration

- **Agents:** [Agent Identity][ident] gives each deployed agent a unique identity independent of the framework,
  protected by a Google-managed Context-Aware Access policy that binds credentials to the runtime via mTLS.
  It supports acting as itself or on behalf of a user; logs then show both identities. A limitation:
  Cloud Storage legacy bucket roles cannot be granted to agent identities. Create with
  `identity_type=AGENT_IDENTITY` (v1beta1 client in the page read). The docs also describe an auth manager
  with 2-legged and 3-legged OAuth and API-key providers for external services.
- **People (Gemini Enterprise):** identity is managed with IAM and Workforce Identity Federation (SSO), plus
  source-system ACLs for permission-aware search ([editions][ge-editions]). The Business edition is SaaS: no
  project IAM roles to manage.
- **Cloud console users:** standard Cloud Identity or federation; not re-read here.

## Licences: who needs a seat

- **Agent Platform:** consumption on a Cloud project; no seat for builders beyond IAM access.
- **Gemini Enterprise** is per-seat. Editions listed ([editions][ge-editions]): Business (1 to 500 users),
  Standard, Plus, Pay-as-you-go (no seat minimum) and Frontline (needs 150 or more users of Standard or Plus).
  Frontline users run agents their admin provisions; they cannot create custom skills. Building and
  publishing custom no-code agents is marked preview and not in every edition. Using your own full-code
  agents built outside Gemini Enterprise is a listed feature, with Frontline limited to admin-provisioned ones.
  Cloud console access is not in Business. AI developer tools need a project linked to a Cloud Billing
  account, and included seat credits cover first-party Gemini models only.

## Regions

[Agent locations][locations] (read 2026-11-20) list one set of regions for Runtime, Sessions, Memory Bank,
Sandboxes and Agent Gateway: 23 region names across the US, Europe and Asia-Pacific (some marked with a
dagger restriction), v1 for GA features and v1beta1 for Preview. Agent Gateway for GKE currently lists only
europe-west1 and us-central1. Data residency here covers data at rest (source, sessions, memories); model
processing follows the model endpoint's location.

## At a glance

| Dimension | Google Cloud |
|---|---|
| Runtime | Agent Runtime (ex Agent Engine), ADK or other frameworks, sandboxes for code and computer use |
| Claude availability | Yes: Claude models on the platform; partner models in Gemini Enterprise developer tools are pay-as-you-go |
| MCP / A2A | A2A supported; Agent Registry and Gateway govern MCP servers; MCP detail not re-read |
| Memory | Agent Platform Memory Bank and Sessions, IAM-controlled |
| Agent identity and IdP | Agent Identity (per-agent, mTLS-bound); Workforce Identity Federation for Gemini Enterprise users |
| Least-privilege roles | `aiplatform.user` is broad; scoped agents, memory and session roles; custom role with `reasoningEngines.query` for invoking |
| Licences and seats | Platform consumption-based; Gemini Enterprise per seat (Business, Standard, Plus, Frontline, Pay-as-you-go) |
| Regions | 23 region names listed for runtime features; GKE gateway two regions |
| Release status | Rename 2026-04-22; Agent Identity GA 2026-04-22; Registry and Gateway GA 2026-06-18 |

## Sources

| Ref | Source | Established |
|---|---|---|
| [overview] | [Agent Platform overview][overview] | Pillars, components, Vertex lineage |
| [names] | [Name changes][names] | Old to new names |
| [relnotes] | [Release notes][relnotes] | Dated rename and GA/Preview events |
| [roles] | [IAM aiplatform roles][roles] | Role names and permissions |
| [ident] | [Agent Identity][ident] | Per-agent identity, A2A least privilege |
| [locations] | [Agent locations][locations] | Region list |
| [claude-page] | [Claude on the platform][claude-page] | Claude model names |
| [ge-overview] | [Gemini Enterprise overview][ge-overview] | Editions, connectors |
| [ge-editions] | [Gemini Enterprise editions][ge-editions] | Seats, identity, partner models |
| [adk] | [google/adk-python][adk] | Apache-2.0, v2.15.0 (GitHub API, 2026-11-20) |
| [a2a] | [A2A site][a2a] | Protocol, Linux Foundation |
| [a2a-repo] | [A2A repo][a2a-repo] | v1.0.1, 2026-05-28 |

## Cross-References

- [agentic-enterprise-os-landscape.md § Agent registries compared][registries] — registry comparison.
- [CC-model-provider-configuration.md][cc-vertex] — Claude via Vertex.
- [aws-agent-stack-analysis.md](aws-agent-stack-analysis.md),
  [microsoft-365-copilot-analysis.md](microsoft-365-copilot-analysis.md) — sibling cloud stacks.
- [data-platforms-lakehouse-landscape.md][data-platforms] — data platforms, not covered here.

[overview]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/overview
[names]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/vertex-ai-name-changes
[relnotes]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/release-notes
[roles]: https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform
[ident]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/runtime/agent-identity
[locations]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/resources/agent-locations
[claude-page]: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude/use-claude
[ge-overview]: https://docs.cloud.google.com/gemini/enterprise/docs/overview
[ge-editions]: https://docs.cloud.google.com/gemini/enterprise/docs/editions
[adk]: https://github.com/google/adk-python
[a2a]: https://a2a-protocol.org/latest/
[a2a-repo]: https://github.com/a2aproject/A2A
[registries]: ../frameworks/agentic-enterprise-os-landscape.md#agent-registries-compared
[cc-vertex]: ../../cc-native/configuration/CC-model-provider-configuration.md#google-vertex-ai
[data-platforms]: ../infrastructure/data-platforms-lakehouse-landscape.md
