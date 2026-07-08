---
title: Agent Identity, Authentication & Personhood Landscape
purpose: Survey of how agents get identity and authorization, and how human-vs-agent is proven — the "who may act, and how is it proven" layer, distinct from CC-local runtime permissions.
category: landscape
created: 2026-07-08
updated: 2026-07-08
validated_links: 2026-07-08
---

**Status**: Assess

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
the substrate under [../non-cc/agentic-payments-landscape.md](../non-cc/agentic-payments-landscape.md)
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
- **ERC-8004 "Trustless Agents"** (Draft EIP) — on-chain Identity / Reputation / Validation registries
  (ERC-721 identity handle → off-chain agent registration JSON) for cross-org agent discovery/trust
  without pre-existing trust. Contracts deployed, EIP still Draft. [eips.ethereum.org][erc8004].
- **Privado ID "Know Your Agent" (KYA)** — gives agents a verifiable identity tied to a creator, with
  public reputation (W3C DIDs + ZK verifiable credentials); a SingularityNET trust registry. Bridges
  "is this a human" and "is this agent accountable." [privado.id][privado].

## 2. Authorize the agent on behalf of a human (delegated, scoped, auditable)

- **MCP Authorization (OAuth 2.1)** — MCP servers act as OAuth 2.1 **resource servers** validating
  tokens from an external authorization server; MUST implement RFC 9728 (Protected Resource Metadata),
  PKCE mandatory. Delegated human authority, not a durable agent identity. [modelcontextprotocol.io][mcp-authz].
- **Okta Cross-App Access (XAA) / Auth for GenAI** — an OAuth/OIDC extension using the IETF
  "Identity Assertion Authorization Grant" (ID-JAG); an enterprise IdP mediates agent-to-app and
  app-to-app connections, replacing long-lived API keys with real-time, revocable delegation + audit.
  [okta.com][xaa].
- **Google AP2 Mandates** — AP2's core primitive is the **Mandate**, a W3C Verifiable Credential;
  Intent → Cart → Payment Mandate chain, ECDSA/P-256-signed, cryptographically proving a purchase was
  human-authorized. A trust/authorization layer feeding [agentic payments](../non-cc/agentic-payments-landscape.md).
  [AP2 repo][ap2].

## 3. Personhood & the bot-vs-authorized-agent distinction

As agents pass CAPTCHAs, sites need a stronger signal than behavioral heuristics.

- **World ID / World (Worldcoin)** — one-time in-person **Orb** (iris) enrollment yields a reusable,
  ZK "proof of human" (no biometric template revealed on reuse); ~40M signed up; "Orb Mini" targeted
  2026. Explicitly framed against the agent era eroding anti-bot defenses. [world.org][worldid].
- **Humanity Protocol** — palm-vein biometric → "Proof-of-Trust"; zkProofer on-chain verification, no
  central raw-biometric storage; Mastercard partnership. ⚠️ Per Biometric Update (Feb 2026) it has
  pivoted *messaging* away from "proof-of-personhood" while keeping the tech — a moving target.
  [docs.humanity.org][humanity].
- **Cloudflare Web Bot Auth / signed agents** — an IETF-draft standard on **HTTP Message Signatures**
  (RFC 9421): an operator publishes a public key at a well-known URL
  (e.g. `anthropic.com/.well-known/http-message-signatures-directory`); requests are signed per-origin
  and verified server-side — cryptographic proof of *which* bot, replacing spoofable UA/IP. AWS WAF
  added support Nov 2025; OpenAI signs Operator requests this way. [blog.cloudflare.com][webbotauth].
- **Pay-or-authenticate (pay-per-crawl)** — repurposes HTTP 402: a crawler must both **pay** and
  **authenticate** (via Web Bot Auth) to proceed — a literal fusion of the identity and payment axes.
  [blog.cloudflare.com][paypercrawl].

## One-time / just-in-time permissions

- **Zero Standing Privileges / JIT access** — no standing privileged credentials; access (and, for
  agents, sometimes the identity itself) is provisioned at task start, scoped, and auto-revoked at
  completion. [beyondtrust.com][jit].
- **Human-in-the-loop approval gates** — HumanLayer's approval-gate SDK (12-Factor Agents "Factor 7")
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
  read for [../non-cc/agentic-payments-landscape.md](../non-cc/agentic-payments-landscape.md).
- **Assess:** standards are early and fragmented (OAuth-vs-workload-identity-vs-onchain), several EIPs
  Draft, one vendor already rebranding. Track MCP-OAuth, Entra Agent ID, and Web Bot Auth adoption.

## Sources

| Source | Content |
|---|---|
| [SPIFFE/SPIRE][spiffe] | Workload identity (SVIDs) |
| [Microsoft Entra Agent ID][entra] | Agent service-principal identity (GA 2026-04) |
| [ERC-8004][erc8004] | On-chain trustless-agent identity/reputation (Draft) |
| [Privado ID — Know Your Agent][privado] | DID + ZK-VC agent identity/reputation |
| [MCP Authorization][mcp-authz] | OAuth 2.1 resource-server model |
| [Okta Cross-App Access][xaa] | ID-JAG delegated agent authorization |
| [Google AP2 spec][ap2] | Mandate (W3C VC) authorization chain |
| [World ID][worldid] · [Humanity Protocol][humanity] | Proof-of-personhood credentials |
| [Cloudflare Web Bot Auth][webbotauth] · [pay-per-crawl][paypercrawl] | Signed agents; 402+auth fusion |
| [JIT / ZSP][jit] · [CC permissions][cc-perms] | Ephemeral perms; CC local rule-gate anchor |

[spiffe]: https://spiffe.io/docs/latest/spire-about/spire-concepts/
[entra]: https://learn.microsoft.com/en-us/entra/agent-id/what-is-microsoft-entra-agent-id
[erc8004]: https://eips.ethereum.org/EIPS/eip-8004
[privado]: https://www.privado.id/blog/privado-know-your-agent
[mcp-authz]: https://modelcontextprotocol.io/specification/draft/basic/authorization
[xaa]: https://developer.okta.com/blog/2025/09/03/cross-app-access
[ap2]: https://github.com/google-agentic-commerce/AP2
[worldid]: https://world.org/world-id
[humanity]: https://www.humanity.org/
[webbotauth]: https://blog.cloudflare.com/web-bot-auth/
[paypercrawl]: https://blog.cloudflare.com/introducing-pay-per-crawl/
[jit]: https://www.beyondtrust.com/resources/glossary/just-in-time-access
[cc-perms]: https://code.claude.com/docs/en/permissions
