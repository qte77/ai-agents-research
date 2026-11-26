---
title: Agent Identity, Authentication & Personhood Landscape
purpose: Survey of how agents get identity and authorization, and how human-vs-agent is proven — the "who may act, and how is it proven" layer, distinct from CC-local runtime permissions.
created: 2026-07-08
updated: 2026-11-26
validated_links_on: 2026-10-24
status: assess
---

The **identity / authorization / personhood** layer for agents: *who is allowed to act, on whose
authority, and how is human-vs-agent proven.* This is a different axis from two things already in the
corpus — **CC-local runtime permissions** (allow/deny/ask + OS sandbox, see
[../cc-native/sandboxing/CC-permissions-bypass-analysis.md](../cc-native/sandboxing/CC-permissions-bypass-analysis.md)
and [CC-sandboxing-analysis.md](../cc-native/sandboxing/CC-sandboxing-analysis.md)) and **CC's own
product auth** ([../cc-native/ci-remote/CC-web-auth-setup-analysis.md](../cc-native/ci-remote/CC-web-auth-setup-analysis.md))
— which answer "how does *Claude Code itself* authenticate," whereas this doc is "how do *agents in
general* get identity/authorization, and how is human-vs-agent distinguished."

It joins the security cluster: [agentic-ai-vulnerability-landscape.md](agentic-ai-vulnerability-landscape.md)
(vuln scoring/discovery), [ai-security-governance-analysis.md](ai-security-governance-analysis.md)
(governance frameworks), [mas-security-framework.md](mas-security-framework.md) (MAESTRO). It is also
the substrate under [../non-cc/protocols/agentic-payments-landscape.md](../non-cc/protocols/agentic-payments-landscape.md)
— x402 needs a payer identity; AP2's Mandates *are* the "authorize on behalf of a human" instance of
this topic.

Three axes structure the space (most 2026 systems combine them):

## 1. Authenticate the agent (agent as a first-class principal)

The agent has its own identity, independent of any human.

- **SPIFFE / SPIRE** — workload identity: SPIRE issues short-lived, auto-rotating **SVIDs** (X.509 or
  JWT) asserting "this workload, this context, this identity," independent of any OAuth session.
  Increasingly proposed as the substrate under agentic systems. [spiffe.io][spiffe].
- **Microsoft Entra Agent ID** (GA April 2026) — an agent identity is a dedicated **service principal**
  in Entra ID (a genuine non-human identity that may also be "authorized to impersonate" a user);
  agents built in Azure AI Foundry / Copilot Studio auto-register. [learn.microsoft.com][entra].
  Foundry's current docs describe it as a specialised Entra identity type with a parent
  "blueprint" per agent; roles and tool authentication are in
  [microsoft-365-copilot-analysis.md § Roles, identity and licences](../non-cc/agents/microsoft-365-copilot-analysis.md#roles-identity-and-licences) (read 2026-11-20).
- **ERC-8004 "Trustless Agents"** (Draft EIP) — on-chain Identity / Reputation / Validation registries
  (ERC-721 identity handle → off-chain agent registration JSON) for cross-org agent discovery/trust
  without pre-existing trust. Contracts deployed, EIP still Draft. [eips.ethereum.org][erc8004].
- **Agent Mesh** (`google/agentmesh`, formerly `google/sam`; Apache-2.0, 1,211★, created 2026-04-21,
  `gh api` 2026-11-22) — a private network for agents giving each node a verifiable identity, built on
  two stated principles: "Nothing is reachable by default" (a node exposes no services until
  configured, and policy grants are by service name rather than network address) and
  "Identity comes from your identity provider" (a node enrolls via an OIDC or bootstrap
  token; `agentmesh-control-plane` turns that into a short-lived, offline-verifiable credential
  bound to the node's key). `agentmesh-node` runs beside the agent for enrollment + local
  exposure, `agentmesh-router` relays nodes that cannot connect directly (NAT traversal), and
  `agentmesh-one` bundles control plane, router and web console for single-machine setups.
  Pre-1.0 per its own README, which also says it is not an officially supported Google product.
- **Cloud agent identities** — AWS AgentCore Identity (inbound JWT from any OIDC IdP, outbound OAuth
  credential vault) and Google Cloud's Agent Identity (per-agent principal, GA 2026-04-22) are covered
  per cloud in [aws-agent-stack-analysis.md § Identity and IdP integration](../non-cc/agents/aws-agent-stack-analysis.md#identity-and-idp-integration)
  and [google-cloud-agent-stack-analysis.md § Identity and IdP integration](../non-cc/agents/google-cloud-agent-stack-analysis.md#identity-and-idp-integration).
  All six clouds side by side: [cloud-agent-platforms-landscape.md](../non-cc/infrastructure/cloud-agent-platforms-landscape.md).

## 2. Authorize the agent on behalf of a human (delegated, scoped, auditable)

- **MCP Authorization (OAuth 2.1)** — Model Context Protocol (MCP) servers act as OAuth 2.1 **resource servers** validating
  tokens from an external authorization server; MUST implement RFC 9728 (Protected Resource Metadata),
  PKCE mandatory. Delegated human authority, not a durable agent identity. [modelcontextprotocol.io][mcp-authz].
  Current revision (2026-07-28, re-checked 2026-10-24): "Authorization is **OPTIONAL** for MCP
  implementations"; clients "**MUST** implement Resource Indicators for OAuth 2.0 as defined in RFC
  8707", and servers "**MUST NOT** accept or transit any other tokens" — tokens are bound to the one
  server they were issued for. "Dynamic Client Registration is deprecated and retained for backwards
  compatibility" in favour of Client ID Metadata Documents. Anthropic's connector directory adds its
  own bar: "use OAuth 2.0 for authenticated services", and every tool carries a `title` and a
  `readOnlyHint` or `destructiveHint` ([submission requirements][claude-connector-submission]).
- **Okta Cross-App Access (XAA) / Auth for GenAI** — an OAuth/OIDC extension using the IETF
  "Identity Assertion Authorization Grant" (ID-JAG); an enterprise IdP mediates agent-to-app and
  app-to-app connections, replacing long-lived API keys with real-time, revocable delegation + audit.
  [okta.com][xaa].
- **Google AP2 Mandates** — AP2's core primitive is the **Mandate**, a W3C Verifiable Credential;
  Intent → Cart → Payment Mandate chain, ECDSA/P-256-signed, cryptographically proving a purchase was
  human-authorized. A trust/authorization layer feeding [agentic payments](../non-cc/protocols/agentic-payments-landscape.md).
  [AP2 repo][ap2].

**Design lens: authorization when agents fan out.** A practitioner post by Johnny Watson (LinkedIn, 2026-11-10; opinion, no product named) argues that gateway-style governance (policy proxies, MCP gateways) assumes linear chains. Once a step fans out into parallel branches that act (update records, send messages, move money), every branch waits on one central service. The post names four costs: shared fate when that service slows or fails, bursts that size it for everyone's peak, tail latency at the join, and organisation or cloud boundaries with no shared gateway. Its example: if 1 in 100 governed calls times out, a run with 100 of them hits at least one 63% of the time (1 − 0.99¹⁰⁰ ≈ 0.63, which checks out). The proposed inversion: define policy centrally, let bounded authority travel with each branch and be verified locally at the consequential boundary, send evidence back off the critical path, and keep a central stop. It also names the costs this incurs: revocation within a bounded window, global limits such as a spend cap split across branches, and staged policy rollouts ([post][watson-fanout]). This is an argument, not a measured result; it fits the token-binding direction of the specs above (MCP's per-server tokens, Okta XAA's revocable delegation, AP2's signed mandates), which make authority portable and checkable at the edge.

## 3. Personhood & the bot-vs-authorized-agent distinction

As agents pass CAPTCHAs, sites need a stronger signal than behavioral heuristics.

- **World ID / World (Worldcoin)** — one-time in-person **Orb** (iris) enrollment yields a reusable,
  ZK "proof of human" (no biometric template revealed on reuse); ~40M signed up; "Orb Mini" targeted
  2026. Explicitly framed against the agent era eroding anti-bot defenses. [world.org][worldid].
- **Humanity Protocol** — palm-vein biometric → "Proof-of-Trust"; zkProofer on-chain verification, no
  central raw-biometric storage; Mastercard partnership. ⚠️ Per Biometric Update (Feb 2026) it has
  pivoted *messaging* away from "proof-of-personhood" while keeping the tech — a moving target.
  [docs.humanity.org][humanity].
- **Cloudflare Web Bot Auth / signed agents** — built on **HTTP Message Signatures** (RFC 9421, a
  Proposed Standard, Feb 2024); the key-directory and architecture documents are IETF Internet-Drafts: an operator publishes a public key at a well-known URL
  (e.g. `anthropic.com/.well-known/http-message-signatures-directory`); requests are signed per-origin
  and verified server-side — cryptographic proof of *which* bot, replacing spoofable UA/IP. AWS WAF
  added support Nov 2025; OpenAI signs Operator requests this way. [blog.cloudflare.com][webbotauth]. Crawler-side detail and a dated vendor table: [web-scraping-extraction-landscape.md § Agent Identity and Vendor Handling](../non-cc/infrastructure/web-scraping-extraction-landscape.md#agent-identity-and-vendor-handling); publisher side: [ai-crawlers-discoverability-landscape.md](../non-cc/infrastructure/ai-crawlers-discoverability-landscape.md).
- **Visa Trusted Agent Protocol (TAP)** — Visa's version of the same idea for commerce: introduced
  2025-10-14 and "available today in the Visa Developer Center and GitHub", built on "cryptographic
  standards (RFC9421)" so merchants can tell legitimate agents from bots
  ([announcement][visa-tap-release] · [overview][visa-tap-overview] · sample
  [visa/trusted-agent-protocol][visa-tap-repo]). Identity, not payment — the payment side is in
  [agentic-payments-landscape.md § Card networks](../non-cc/protocols/agentic-payments-landscape.md#card-networks-visa-and-mastercard).
- **Pay-or-authenticate (pay-per-crawl)** — repurposes HTTP 402: a crawler must both **pay** and
  **authenticate** (via Web Bot Auth) to proceed — a literal fusion of the identity and payment axes.
  [blog.cloudflare.com][paypercrawl].

## One-time / just-in-time permissions

- **Zero Standing Privileges / JIT access** — no standing privileged credentials; access (and, for
  agents, sometimes the identity itself) is provisioned at task start, scoped, and auto-revoked at
  completion. [beyondtrust.com][jit].
- **Human-in-the-loop approval gates** — HumanLayer's approval-gate SDK (12-Factor Agents "Factor 7"; no PyPI release since 2025-06)
  is already cited in [mas-design-principles.md](mas-design-principles.md).
- **Claude Code's permission model** (local reference anchor, *not* an instance of the above) —
  per-tool-call allow / ask / deny, evaluated deny → ask → allow, managed via `/permissions` and
  `.claude/settings.json`. A single-vendor, local, pre-configured rule-gate — no external IdP, no token
  exchange, no cross-org delegation. [code.claude.com][cc-perms].

## Takeaways

- **Two questions, often conflated:** *authenticate the agent* (SPIFFE, Entra Agent ID, ERC-8004) vs
  *authorize it for a human* (MCP-OAuth, XAA, AP2 Mandates). Pick the axis a given standard actually
  addresses before comparing.
- **Personhood is now infrastructure, not research:** World ID's scale + Cloudflare's Sept-15-2026
  default bot policy give the human-vs-agent line real commercial/legal weight.
- **Identity underpins payments:** AP2 Mandates and x402 payer identities make this doc a prerequisite
  read for [../non-cc/protocols/agentic-payments-landscape.md](../non-cc/protocols/agentic-payments-landscape.md).
- **Assess:** standards are early and fragmented (OAuth-vs-workload-identity-vs-onchain), several EIPs
  Draft, one vendor already rebranding. Track MCP-OAuth, Entra Agent ID, and Web Bot Auth adoption.

## Not included

Entries removed under the [pruning rule](../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (alive, adopted or proven; checked 2026-11-22).

| Name | Reason | Date | Link |
|---|---|---|---|
| Privado ID "Know Your Agent" | Fails criterion 1 (not publicly available): the vendor's own post (2026-01-21) says KYA is "currently available under private access" to selected customers and partners, with its SDK by request; one named adopter (Billions), vendor-stated | 2026-11-22 | <https://www.privado.id/blog/privado-know-your-agent> |

## Sources

| Source | Content |
|---|---|
| [Johnny Watson, "Your agents can fan out. Can their authority?" (LinkedIn, 2026-11-10)][watson-fanout] | Opinion: governance for parallel agent branches; costs of central gateways |
| [SPIFFE/SPIRE][spiffe] | Workload identity (SVIDs) |
| [Microsoft Entra Agent ID][entra] | Agent service-principal identity (GA 2026-04) |
| [ERC-8004][erc8004] | On-chain trustless-agent identity/reputation (Draft) |
| [Agent Mesh][sam] (`google/agentmesh`) | P2P agent-network identity/discovery; 1,211★, Apache-2.0, `gh api` 2026-11-22 |
| [MCP Authorization][mcp-authz] | OAuth 2.1 resource-server model |
| [Okta Cross-App Access][xaa] | ID-JAG delegated agent authorization |
| [Google AP2 spec][ap2] | Mandate (W3C VC) authorization chain |
| [World ID][worldid] · [Humanity Protocol][humanity] | Proof-of-personhood credentials |
| [Cloudflare Web Bot Auth][webbotauth] · [pay-per-crawl][paypercrawl] | Signed agents; 402+auth fusion |
| [Visa TAP release][visa-tap-release] · [overview][visa-tap-overview] · [repo][visa-tap-repo] | Visa's RFC 9421 signed-agent protocol (verified 2026-10-22) |
| [Claude connector submission][claude-connector-submission] | Directory OAuth and tool-annotation requirements (checked 2026-10-24) |
| [JIT / ZSP][jit] · [CC permissions][cc-perms] | Ephemeral perms; CC local rule-gate anchor |

[spiffe]: https://spiffe.io/docs/latest/spire-about/spire-concepts/
[entra]: https://learn.microsoft.com/en-us/entra/agent-id/what-is-microsoft-entra-agent-id
[erc8004]: https://eips.ethereum.org/EIPS/eip-8004
[sam]: https://github.com/google/agentmesh
[mcp-authz]: https://modelcontextprotocol.io/specification/latest/basic/authorization
[visa-tap-release]: https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21716.html
[visa-tap-overview]: https://developer.visa.com/capabilities/trusted-agent-protocol/overview
[visa-tap-repo]: https://github.com/visa/trusted-agent-protocol
[claude-connector-submission]: https://claude.com/docs/connectors/building/submission
[xaa]: https://developer.okta.com/blog/2025/09/03/cross-app-access
[ap2]: https://github.com/google-agentic-commerce/AP2
[worldid]: https://world.org/world-id
[humanity]: https://www.humanity.org/
[webbotauth]: https://blog.cloudflare.com/web-bot-auth/
[paypercrawl]: https://blog.cloudflare.com/introducing-pay-per-crawl/
[jit]: https://www.beyondtrust.com/resources/glossary/just-in-time-access
[cc-perms]: https://code.claude.com/docs/en/permissions
[watson-fanout]: https://www.linkedin.com/posts/johnny-watson-39890a8_your-agents-can-fan-out-can-their-authority-share-7525809949105459200-nHK8/
