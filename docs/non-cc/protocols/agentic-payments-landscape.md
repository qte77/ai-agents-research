---
title: Agentic Payments Landscape — Machine-Native Payment Rails for Agents
purpose: Survey of emerging agent payment protocols and rails (x402, Google AP2, Stripe MPP, L402, ACP, UCP, Visa and Mastercard agent programmes) that let autonomous agents pay for API/tool access or buy goods without a human in the loop per transaction.
category: landscape
created: 2026-07-08
updated: 2026-10-24
validated_links: 2026-10-24
status: research
---

**Machine-native payment rails** let an autonomous agent discover a paid tool/API, pay for it, and use
it — with no human provisioning a key per purchase. This is the "agent economics" plumbing beneath
autonomous multi-agent systems: *agent hits a paywall → wallet authorizes → agent retries and gets the
resource*. The corpus had **zero** coverage of this before (only a one-line Fetch.ai mention); this doc
catalogs the emerging, competing standards. It is tightly coupled to **agent identity/authentication**
(a payer needs a verifiable identity) — see
[../sdlc-lcm/agent-identity-auth-landscape.md](../../sdlc-lcm/agent-identity-auth-landscape.md) (AP2's
Mandates *are* the authorization primitive) and the security angle in
[../sdlc-lcm/agentic-ai-vulnerability-landscape.md](../../sdlc-lcm/agentic-ai-vulnerability-landscape.md).

## The standards

| Protocol | Backer / governance | Mechanism | Settlement | Maturity |
|---|---|---|---|---|
| **x402** | Coinbase-originated → **Linux Foundation** | HTTP `402` challenge/response; signed payment header | USDC on **Base** (EIP-3009 / Permit2) | Live, 20k+ payable endpoints (Apify) |
| **Google AP2** | Google (`google-agentic-commerce`) | **Mandates** (W3C VC): Intent→Cart→Payment, ECDSA/P-256 — an authorization layer, not a rail | Payment-method-agnostic | Early (v0.2.0, 2026-04-28) |
| **Stripe MPP** | Stripe + Tempo (Machine Payments Protocol) | HTTP `402` challenge; agent authorizes, retries, gets the resource plus a receipt | Cards via Shared Payment Tokens; USDC.e on Tempo, USDC on Solana | Documented in Stripe's docs |
| **L402** | Lightning Labs | HTTP `402` + `WWW-Authenticate: L402 macaroon=…, invoice=…`; credential = macaroon + invoice preimage | Bitcoin Lightning | Spec + reference repo (no maturity label) |
| **ACP** (Agentic Commerce Protocol — disambiguation below) | **OpenAI + Stripe** | Programmatic buyer→agent→business commerce flows | Stripe Shared Payment Token (underlying rail not specified) | Live (ChatGPT is first implementing platform) |
| **UCP** (Universal Commerce Protocol) | "UCP Authors": Google, Shopify, Etsy, Wayfair, Target, Walmart, Amazon, Microsoft, Meta, Salesforce, Stripe and others | Commerce protocol built on AP2, with MCP support; Shopify ships it as MCP servers | Payment-method-agnostic | Apache-2.0; no version stated |
| **Visa Intelligent Commerce** / **Trusted Agent Protocol** | Visa | Card credentials for agents; TAP signs agent requests (RFC 9421) so merchants can tell agents from bots | Visa network | Announced 2025-04-30; Connect in pilot (2026-04-08); TAP available since 2025-10-14 |
| **Mastercard Agent Pay** | Mastercard | Agentic Tokens; agent sends a Payment Data object | Mastercard network | Introduced 2025 (exact date unverified) |
| **Fetch.ai uAgents** | Fetch.ai (Agentverse) | On-chain agent payments | On-chain | Shipped (niche) |

### x402 (the anchor)

[x402][x402-repo] repurposes the dormant **HTTP 402 "Payment Required"** code: an agent requests a paid
resource, the server replies `402` with a payment challenge, the agent's wallet signs a blockchain
authorization (**EIP-3009 `TransferWithAuthorization`** or **Permit2**), retries with a payment header,
and the server verifies/settles. Originally built by **Coinbase**, it is now an **open-source protocol
under the Linux Foundation** — a real maturity signal (single-vendor → neutral governance). Settlement
is **USDC on Base**; two pricing schemes (`exact` fixed-price, `upto` capped-variable).

**Apify case study** ([blog][x402-apify-blog] · [docs][x402-apify-docs]): Apify made its Actor
marketplace payable via x402 without API keys — an agent funds a **Coinbase Agentic Wallet** (`awal`)
with USDC on Base, buys a **prepaid token balance** (`npx awal x402 pay`, $1 minimum, acts as a hard
spending cap), and each Actor run draws it down. Apify reports **~20,000+ x402-enabled Actors** (≈10×
growth) as of 2026-06-30; eligible Actors must be "pay-per-event," limited-permission, no Standby.
A prior community RFC to gate payments *inside the MCP server* per-tool-call
([apify-mcp-server#626][x402-mcp-issue], via a `@tomopay/gateway` supporting both x402 and Stripe MPP)
was **closed as superseded** by this platform-level integration — i.e., agent payments are landing at
the API/Actor layer, not (yet) inside MCP tool calls.

### Google AP2 (Agent Payments Protocol)

[AP2][ap2] (Apache-2.0; `v0.2.0`, 2026-04-28; Google `google-agentic-commerce` org) is a
**trust/authorization layer, not a settlement rail**: its core primitive is the **Mandate**, a
**W3C Verifiable Credential**, chained **Intent → Cart → Payment Mandate** and ECDSA/P-256-signed to
cryptographically prove a purchase was human-authorized ([AP2 repo][ap2]). It is payment-method-agnostic
(it rides on top of a rail rather than being one). Because Mandates are the "authorize on behalf of a
human" primitive, AP2 sits at the seam of payments and **agent identity/auth** — see
[../sdlc-lcm/agent-identity-auth-landscape.md](../../sdlc-lcm/agent-identity-auth-landscape.md).
Release history from the repo's tags: `v0.1.0` on 2025-09-16, `v0.2.0` on 2026-04-28, whose notes say
"This is the second release of AP2. It focuses on providing Human Not Present flows."
([release][ap2-v020]). Still current as of 2026-10-22.

### Stripe MPP (Machine Payments Protocol)

Stripe's docs define [MPP][stripe-mpp] as "an open protocol that lets agents pay for your APIs and
services programmatically without a checkout UI, co-authored by Stripe and Tempo." It uses the same
HTTP 402 pattern as x402: "your server returns an HTTP 402 response with payment details", and the
agent authorizes the payment, retries the request and gets the resource with a receipt. Per Stripe's
[machine payments overview][stripe-machine], MPP settles with cards (through Shared Payment Tokens — the
same token ACP uses — with a stated minimum: "For card payments through Shared Payment Tokens (SPTs),
the minimum amount is 0.50 USD") or stablecoins (USDC.e on Tempo, USDC on Solana), and Stripe accepts
x402 (USDC on Base) alongside it. The two are complementary rather than rivals in practice: the
[mpp.dev][mpp-dev] guide says to "configure mppx directly when one route must serve native MPP and x402
clients." This replaces this doc's earlier "not independently characterized" note.

### L402 (Lightning Labs)

[L402][l402-repo] is the Lightning Network's take on HTTP 402. The server answers with
`WWW-Authenticate: L402 macaroon="<base64>", invoice="<bolt11>"`; the client pays the invoice, which
reveals its preimage, and retries with the macaroon plus that preimage — per the
[spec][l402-spec], "the preimage is encoded as hex and the Macaroon is encoded as base64." The spec
itself warns that the scheme is "not considered to be a secure method of user authentication" without
TLS, since the credential is "passed over the network as cleartext." Lightning Labs positions it for
agents: "L402 allows services to charge for API endpoints in a way that is easy for AI agents to
participate" ([overview][l402-overview]). The fetched pages don't compare it with x402; the overlap
(both use 402, both target agents) and the difference (Lightning vs USDC on Base) are our reading.

### UCP (Universal Commerce Protocol) and Shopify

[UCP][ucp] stands for "Universal Commerce Protocol". Its site is copyrighted to "UCP Authors", lists
co-developers including Google, Shopify, Etsy, Wayfair, Target, Walmart, Amazon, Microsoft, Meta,
Salesforce and Stripe, states "Licensed under the Apache License, Version 2.0", and says "UCP is built on
industry standards", naming the Agent Payments Protocol (AP2) among them. Those co-developers are
listed for shopping; separate lists cover lodging and food, and an "Endorsed across the ecosystem"
section includes Visa, Mastercard, Amex and Adyen. No version number is stated.

[Shopify's agent docs][shopify-agents] are the most concrete implementation: Global Catalog, Storefront
Catalog, Cart, Checkout and Order tools exposed as "Shopify's UCP-compliant MCP servers", where Checkout
MCP will "Convert carts into checkouts and complete purchases for trusted agents." A Universal Cart sits
behind an early-access waitlist (the page offers "Join the early access waitlist"; it does not say the
feature is live). The page doesn't mention ACP.

### Card networks: Visa and Mastercard

- **Visa Intelligent Commerce** was [announced 2025-04-30][visa-vic], with partners "including
  Anthropic, IBM, Microsoft, Mistral AI, OpenAI, Perplexity, Stripe and Samsung"; the release is written
  in the future tense. **Intelligent Commerce Connect**, "part of the Visa Intelligent Commerce
  portfolio", was "Currently in pilot with select partners including Aldar, AWS, Diddo, Highnote, Mesh,
  Payabli, Sumvin" as of [2026-04-08][visa-connect], and that release names the Trusted Agent Protocol,
  MPP, ACP and UCP.
- **Visa Trusted Agent Protocol (TAP)**, [introduced 2025-10-14][visa-tap] and "available today in the
  Visa Developer Center and GitHub", is identity rather than payment: it uses "cryptographic standards
  (RFC9421)" ([overview][visa-tap-dev]) so merchants can tell legitimate agents from bots, with a sample
  implementation at [visa/trusted-agent-protocol][visa-tap-repo]. It belongs next to Web Bot Auth in
  [agent-identity-auth-landscape.md](../../sdlc-lcm/agent-identity-auth-landscape.md).
- **Mastercard Agent Pay**: Mastercard's [merchant developer guide][mc-guide] says "Card issuers cannot
  identify the transaction as agentic without an Agentic Token" and "For Mastercard Agent Pay
  transactions, the agent sends a Payment Data object in the message body." A June 2026 Mastercard
  release on a newer product (Agent Pay for Machines) says it "builds on Mastercard's Agent Pay program,
  introduced in 2025" ([release][mc-ap4m]). The exact launch date and any US-wide rollout claim could
  not be confirmed first-party (mastercard.com blocked most automated fetches on 2026-10-22).

### Merchant feeds: what agent storefronts ask merchants for

Before an agent can pay, it has to find and trust the product. The three biggest agent-commerce
surfaces each publish what they need (checked 2026-10-24):

- **OpenAI (ChatGPT, ACP):** a structured product feed whose required fields are `item_id`, `title`,
  `description`, `url`, `brand`, `seller_name`, `image_url`, `availability` and `price`; eligibility
  flags include `is_eligible_search` and `is_eligible_checkout`, and "Checkout requires a separately
  enabled integration" ([feed spec][openai-feed]). The page says nothing about how products are ranked.
- **Google (Gemini, AI Mode, UCP):** `native_commerce` opts listings into the "Buy Now" flow and
  `checkout_eligibility` "dictates whether the "Buy" button is displayed for a specific item"
  ([Merchant Center][google-native-commerce]); UCP checkout prep requires that "You must include return
  cost, return speed (window), and a link to the full policy" ([UCP guide][google-ucp-merchant], last
  updated 2026-10-02).
- **Shopify (Agentic Storefronts):** merchants should focus on "complete and well-structured product
  information in Shopify Catalog" (Shopify Help Center, plain text because it blocks link checkers:
  help.shopify.com/en/manual/online-sales-channels/agentic-storefronts/products).

None of these is "marketing to agents" in the persuasion sense: each asks for complete, structured,
accurate data plus clear policies, and leaves ranking unexplained.

### Fetch.ai

**Fetch.ai uAgents** already appears as a one-line mention in
[agent-frameworks-infrastructure-landscape.md](../frameworks/agent-frameworks-infrastructure-landscape.md)
(blockchain-integrated agents with on-chain payments via Agentverse).

### ACP (Agentic Commerce Protocol) — disambiguation

**ACP** in this document means the **Agentic Commerce Protocol** ([agenticcommerce.dev][acp]), built
by **Stripe and OpenAI**: "An open standard for programmatic commerce flows between buyers, AI
agents, and businesses," stated as "open source and community-designed" under **Apache-2.0**
([source][acp]). OpenAI is its first implementing AI platform, via ChatGPT; Stripe is its first
compatible payment processor, through its Shared Payment Token ([source][acp]). No version number is
stated on the protocol's overview page, but its [changelog][acp-changelog] lists dated releases:
**2025-09-29** (initial release of the Agentic Checkout and Delegate Payment specs), **2025-12-12**
(breaking changes to fulfillment fields/pricing), and **2026-01-30** (capability negotiation, a
payment-handlers framework — breaking — plus an extensions framework and an optional discount
extension). Clients are required to send a dated `API-Version` request header (e.g.
`API-Version: 2025-12-12`) ([source][acp-changelog]).

**This is a different protocol from the corpus's other "ACP" entries**, which share only the
three-letter acronym: the **Agent Client Protocol** (the IDE↔agent protocol implemented by Goose,
Zed, and most coding-agent docs in this corpus — e.g.
[goose-analysis.md § ACP](../agents/goose-analysis.md#acp-agent-client-protocol)) and the **Agent
Connect Protocol** (IBM, archived 2026-04 — see
[ag-ui-protocol-landscape.md](ag-ui-protocol-landscape.md)). Any future edit adding "ACP" to this
corpus should disambiguate explicitly, as done here.

### Lightsage payments tracker

[Lightsage's Agent Experience Arena — Payments][lightsage-payments] is a live, numbered adoption
tracker for x402, MPP, UCP, ACP and AP2: **"The Arena
separates public readiness from proof that a payment completed"** ([source][lightsage-payments]). As
observed 2026-10-15: **2,369 companies** in the directory (score version `agent-payments-v7`; only
the Top 100 shown on-page, the rest in a linked JSON), **0 rated "Sandbox-verified or stronger,"** and
the #1-ranked company, **Telnyx**, at **84/100 overall readiness** and **48/100 payment readiness**
(signals: x402, UCP, ACP, mcp, openapi) — the highest payment-readiness score on the page. Lightsage
itself ranks #23 (overall readiness 55, payment readiness 0). Last-scanned dates on the visible Top
100 run Aug 20–Oct 8 (year not stated on the page). Re-checked 2026-10-22: **2,370 companies**, still
**0** "Sandbox-verified or stronger"; #2 Xquik at 76 overall / 20 payment readiness (signals: MPP,
mcp, openapi). Lightsage sells agent-experience services to the developer-tool companies it scores —
see [evaluation-data-resources-landscape.md § Agent-readiness scoring](../../sdlc-lcm/evaluation-data-resources-landscape.md)
for the operator and the conflict-of-interest note.

Scoring, per the [methodology page][lightsage-payments-methodology]: **overall readiness = 70% agent
access + 30% payment readiness**, through an 8-level evidence ladder — *Not evaluated → Support
claimed → Payment signal detected → Unpaid challenge validated → Sandbox verified → Live verified →
Multi-payer verified → Certified*. The ladder's own top tier is self-referential ("Certified: Lightsage
has reviewed reproducible evidence and the result remains within its validity window") — i.e. Lightsage
verifies its own results, not an independent auditor — and the page states "Public scans never
authorize payments."

Lightsage's FAQ also gives usage guidance: "Pick UCP when the goal is direct buying from AI surfaces
such as Google AI Mode or Gemini" (vs. "Pick ACP when the main integration is agentic checkout:
product feed or cart discovery"). The acronym itself is now expanded from its own site — see § UCP
above.

## Why it matters / takeaways

- **New primitive, moving fast:** foundation governance (x402), a Google entrant (AP2), and a Stripe
  entrant (MPP) all within ~one quarter — autonomous agent-to-service payment is consolidating from
  research into rails.
- **A third-party readiness tracker now exists:** Lightsage's payments Arena scores real-world
  adoption of x402/MPP/UCP/ACP/AP2 across 2,370 companies (2026-10-22) — useful as an external signal,
  though it is self-scored by its own operator with no independent audit, and 0 companies clear its
  top evidence tier.
- **HTTP 402 is the shared pattern:** x402 (USDC on Base), MPP (cards and stablecoins) and L402
  (Lightning) all answer a request with 402 and accept a retry carrying payment proof; Stripe accepts
  both MPP and x402, and `mppx` can serve both from one endpoint.
- **Two layers, not one race (our reading):** API-call payment rails (x402, MPP, L402) sit beside commerce/checkout
  protocols (ACP, UCP) and trust layers (AP2 Mandates, Visa TAP, Mastercard Agentic Tokens). The card
  networks are joining at the trust layer, and both Visa's Connect release and UCP reference the other
  protocols rather than replacing them.
- **Distinct from human-account SaaS billing:** this is *not* Claude Code calling a Stripe MCP server
  on a human's account (see [../cc-native/plugins-ecosystem/CC-business-api-integrations.md](../../cc-native/plugins-ecosystem/CC-business-api-integrations.md)) — it's the agent itself as the payer.
- **Assess:** early, standards-in-flux, crypto-settlement caveats. Track x402/AP2 releases; revisit as
  MCP-level payment gating (deferred in #626) reappears.

## Sources

| Source | Content |
|---|---|
| [x402 (Coinbase/LF)][x402-repo] | x402 protocol home |
| [Apify: introducing x402][x402-apify-blog] · [Apify x402 docs][x402-apify-docs] | Live x402 integration + case study |
| [apify-mcp-server#626][x402-mcp-issue] | Closed RFC: MCP-level payment gating (x402 + Stripe MPP) |
| [google-agentic-commerce/AP2][ap2] | Google Agent Payments Protocol (v0.2.0) |
| [agenticcommerce.dev][acp] | Agentic Commerce Protocol (ACP) home — OpenAI + Stripe |
| [ACP changelog][acp-changelog] | Dated releases (2025-09-29, 2025-12-12, 2026-01-30) + `API-Version` header |
| [Lightsage Agent Experience Arena — Payments][lightsage-payments] · [methodology][lightsage-payments-methodology] | Live cross-protocol payment-readiness tracker (2,369 companies on 2026-10-15; 2,370 on 2026-10-22) |
| [AP2 v0.2.0 release][ap2-v020] | Release date and "Human Not Present" focus |
| [Stripe: MPP][stripe-mpp] · [machine payments][stripe-machine] · [mpp.dev][mpp-dev] | MPP definition, 402 flow, payment methods, SPT minimum, MPP + x402 on one endpoint |
| [L402 repo][l402-repo] · [spec][l402-spec] · [overview][l402-overview] | L402 header format, credential encoding, TLS warning, agent positioning |
| [ucp.dev][ucp] | UCP name, licence, co-developers, built on AP2 |
| [Shopify agent docs][shopify-agents] | UCP-compliant MCP servers, Checkout MCP, Universal Cart waitlist |
| [Visa Intelligent Commerce][visa-vic] · [Connect][visa-connect] · [TAP release][visa-tap] · [TAP overview][visa-tap-dev] · [TAP repo][visa-tap-repo] | Visa announcement, pilot status, Trusted Agent Protocol |
| [Mastercard agentic commerce guide][mc-guide] · [Agent Pay for Machines release][mc-ap4m] | Agentic Tokens, Payment Data object, "introduced in 2025" |
| Falsification pass, 2026-10-22 | 33 claims re-checked against these sources by an independent agent: 32 confirmed, 1 overstated (Universal Cart, corrected above) |

[x402-repo]: https://github.com/coinbase/x402
[x402-apify-blog]: https://blog.apify.com/introducing-x402-agentic-payments/
[x402-apify-docs]: https://docs.apify.com/platform/integrations/x402
[x402-mcp-issue]: https://github.com/apify/apify-mcp-server/issues/626
[ap2]: https://github.com/google-agentic-commerce/AP2
[acp]: https://agenticcommerce.dev
[acp-changelog]: https://agenticcommerce.dev/docs/changelog
[lightsage-payments]: https://lightsage.com/agent-experience-arena/payments
[lightsage-payments-methodology]: https://lightsage.com/agent-experience-arena/payments/methodology
[ap2-v020]: https://github.com/google-agentic-commerce/AP2/releases/tag/v0.2.0
[stripe-mpp]: https://docs.stripe.com/payments/machine/mpp
[stripe-machine]: https://docs.stripe.com/payments/machine
[mpp-dev]: https://mpp.dev
[l402-repo]: https://github.com/lightninglabs/L402
[l402-spec]: https://docs.lightning.engineering/the-lightning-network/l402/protocol-specification
[l402-overview]: https://docs.lightning.engineering/the-lightning-network/l402
[ucp]: https://ucp.dev
[shopify-agents]: https://shopify.dev/docs/agents
[visa-vic]: https://corporate.visa.com/en/sites/visa-perspectives/newsroom/new-era-of-commerce-ai-stablecoins.html
[visa-connect]: https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.22276.html
[visa-tap]: https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21716.html
[visa-tap-dev]: https://developer.visa.com/capabilities/trusted-agent-protocol/overview
[visa-tap-repo]: https://github.com/visa/trusted-agent-protocol
[mc-guide]: https://developer.mastercard.com/merchant-cloud/documentation/tutorials-and-guides/agentic-commerce-guide/22/
[mc-ap4m]: https://www.mastercard.com/us/en/news-and-trends/press/2026/june/mastercard-launches-agent-pay-for-machines.html
[openai-feed]: https://developers.openai.com/commerce/specs/feed
[google-native-commerce]: https://support.google.com/merchants/answer/17251586
[google-ucp-merchant]: https://developers.google.com/merchant/ucp/guides/overview/merchant-center
