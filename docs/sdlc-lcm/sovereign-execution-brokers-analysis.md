---
title: Sovereign Execution Broker (SEB)
purpose: Runtime enforcement boundary requiring certificate-bound authority — not agent/LLM reasoning alone — before an autonomous agent can mutate production infrastructure.
source: https://arxiv.org/abs/2606.20520
created: 2026-07-23
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Assess

## What It Is

An arXiv paper, "Sovereign Execution Broker: Enforcing Certificate-Bound Authority in
Agentic Control Planes" (arXiv:2606.20520, DOI 10.48550/arXiv.2606.20520; authors Jun He,
Deying Yu; 19 pages, 6 figures, 10 tables), proposing **SEB** — a runtime boundary that sits
between an agentic control plane and the production infrastructure it acts on. The core
claim: an autonomous agent's internal reasoning (LLM output, planner state) is not
sufficient authority to mutate production systems; every mutating action must instead be
gated on a verified, certificate-bound grant of authority, checked at execution time.

Cross-listed cs.CR (primary), cs.AI, cs.DC, cs.LG. Current revision is v2 (submitted
2026-06-18 as v1 titled "Sovereign Execution Brokers," revised 2026-06-19 as v2, singular
title). Licensed CC BY 4.0.

## Architecture: Proposal / Admission / Execution

SEB separates agent action into three phases:

1. **Proposal** — the agent emits a requested change (its reasoning output), not yet
   trusted or acted on.
2. **Admission** — the proposal is checked against a certificate before it may proceed:
   validity window, revocation status, and whether the proposed change matches what the
   certificate actually authorizes.
3. **Execution** — only admitted proposals reach production; the broker also checks for
   **state drift** (divergence between the proposed system state and the actual observed
   state) and produces an auditable record of the decision and its outcome.

The effect is that authority to act is externally verified and revocable, rather than
implicit in the agent having reached a conclusion.

## Prototype & Evaluation

The paper describes a prototype implementation evaluated for latency overhead and for
behavior under fault injection. Exact numeric results were not reliably extractable from
the available fetch tooling (compressed PDF streams) and are not reported here — a direct
or rendered read of the PDF would be needed before citing specific figures. No linked
GitHub repository or code artifact for SEB was found; this appears to be a paper-only
submission as of v2.

A related paper, arXiv:2606.11632 ("Sovereign Assurance Boundary"), is reportedly the
source of the certificates SEB enforces against — noted here as likely context, not yet
independently confirmed against SEB's primary text.

## Corpus Relevance & Cross-References

SEB's certificate-bound authority model is the same "who may act, on whose authority"
question that [agent-identity-auth-landscape.md](agent-identity-auth-landscape.md) surveys
across SPIFFE/SPIRE, Entra Agent ID, and ERC-8004 — SEB adds a runtime *admission +
execution* enforcement point in front of production infrastructure specifically, rather
than an identity-issuance mechanism. It also bears on
[mas-security-framework.md](mas-security-framework.md)'s MAESTRO Layer 5 (Execution:
runtime safety) and Layer 7 (Orchestration: registration hijacking, execution order) —
SEB's admission/execution gating and state-drift checks are a concrete control candidate
for those layers.

## Sources

| Source | Content |
|---|---|
| [SEB abstract page][seb-abs] | Title, authors, categories, license, version history |
| [SEB PDF][seb-pdf] | Architecture (proposal/admission/execution), enforcement mechanics |
| [Sovereign Assurance Boundary][sab] | Related paper (certificate origin) — unconfirmed against SEB primary text |

[seb-abs]: https://arxiv.org/abs/2606.20520
[seb-pdf]: https://arxiv.org/pdf/2606.20520
[sab]: https://arxiv.org/abs/2606.11632
