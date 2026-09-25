---
title: Source expansion (wave 2) — agents-cli, agentic payments, Karpathy, agent identity/auth
status: done
issue: 374
created: 2026-07-08
updated: 2026-09-23
---

**Status**: Reference (plan)

Durable record + source map for the **second wave** of new sources added 2026-07-08, ahead of the
deferred [#354](https://github.com/qte77/ai-agents-research/issues/354) graph rebuild. Wave 1 is
[2026-07-08-0004-new-sources-batch.md](2026-07-08-0004-new-sources-batch.md); umbrella tracker
[#374](https://github.com/qte77/ai-agents-research/issues/374).

## Current status (merged from the 2026-07-08 source-expansion handoff)

- **Done (merged):** wave 1 — #372 agentic-AI-vulnerability-landscape · #373 kv-cache-serving-landscape
  (+ CC-prompt-caching min-token fix) · #375 Codex-CC plugin + OpenWiki + company-brain + CONTRIBUTING
  polyfetch/doc-pipeline pointer. Wave 2 — the four docs below.
- **#354 graph rebuild — DONE:** executed by PR #379 (2026-07-10, 637 nodes; #354 closed). Method in
  [2026-07-08-0006-graphify-rebuild-354.md](2026-07-08-0006-graphify-rebuild-354.md).
- **Scout backlog** (13 promotable triage/rxiv candidates in #374) — drained by the 2026-07-23 arc,
  [2026-07-23-0007-corpus-update-new-sources.md](2026-07-23-0007-corpus-update-new-sources.md).
- **Tooling:** polyfetch-scrape (fetch JS-SPA/blocked pages) and doc-pipeline-engine (PDF/Office →
  text), both via `uv run --directory` — documented in CONTRIBUTING's Research Workflow.
- **Pre-existing link-rot** to fix opportunistically: `usage.ai` 301 in `kiro-analysis.md`.

## What was added (wave 2)

| Doc | Home | Anchor sources (first-party) |
|---|---|---|
| `non-cc/frameworks/agents-cli-analysis.md` | non-cc / Frameworks | github.com/google/agents-cli; google.github.io/agents-cli (Apache-2.0, v1.0.0 Pre-GA) |
| `non-cc/protocols/agentic-payments-landscape.md` | non-cc / Protocols & Interfaces | github.com/coinbase/x402; blog.apify.com/introducing-x402-agentic-payments; docs.apify.com/platform/integrations/x402; apify/apify-mcp-server#626; github.com/google-agentic-commerce/AP2 |
| `non-cc/reference/karpathy-agentic-coding-analysis.md` | non-cc / Reference & Background | karpathy.bearblog.dev (menugen, year-in-review-2025, sequoia-ascent-2026); YT `LCEmiRjPEtQ`; YC Library "software-is-changing-again" |
| `sdlc-lcm/agent-identity-auth-landscape.md` | sdlc-lcm (security cluster) | spiffe.io; learn.microsoft.com Entra Agent ID; eips.ethereum.org/EIPS/eip-8004; privado.id; modelcontextprotocol.io authz; developer.okta.com XAA; github.com/google-agentic-commerce/AP2; world.org; humanity.org; blog.cloudflare.com web-bot-auth + pay-per-crawl; beyondtrust.com JIT; code.claude.com/docs/en/permissions |

## Placement rationale (verified against coverage)

- **agents-cli → non-cc/Frameworks** (not cc-community): cross-agent tool (CC one of 3+ hosts), subject is ADK/Gemini-Enterprise. Cross-ref added from `cc-community/CC-community-skills-landscape.md` (it ships as a CC skill-pack) per CONTRIBUTING's "spans-both → deeper analysis + cross-ref."
- **agentic payments → non-cc/Protocols & Interfaces**: new topic (zero prior coverage). x402 anchor + AP2 (Mandate = W3C VC, *authorization* layer not a rail) + Stripe MPP (via #626, closed RFC) + Fetch.ai cross-link.
- **agent identity/auth → sdlc-lcm** (security cluster): new topic; different axis from CC-local sandbox perms. Three axes — authenticate-the-agent / authorize-on-behalf-of-human / personhood — + one-time/JIT. Bidirectionally cross-linked with the payments doc (AP2 Mandates are the payments↔identity seam).
- **Karpathy agentic-coding → new doc** (distinct from the existing KB-pattern `karpathy-llm-kb-analysis.md`); essay-tweets cited by date (x.com 402s automated fetch — blogs/talks are the first-party anchors).

## Sourcing caveats (for re-verification)

- **AP2 canonical = the GitHub repo** `google-agentic-commerce/AP2`; `ap2-protocol.org/specification/` **404s** (do not use).
- **Humanity Protocol**: `docs.humanity.org/introduction/overview` 404s → homepage used; project is rebranding away from "proof-of-personhood" (Biometric Update, Feb 2026) — recheck.
- **Karpathy x.com tweets**: content secondary-corroborated (x.com returns 402 to WebFetch).

## Full session source set for the graph rebuild

Wave 1 (merged): #372 `agentic-ai-vulnerability-landscape`, #373 `kv-cache-serving-landscape` (+ CC-prompt-caching refresh), #375 (Codex-CC plugin, OpenWiki, company-brain, CONTRIBUTING polyfetch/doc-pipeline pointer).
Wave 2 (this PR): the four above. **All of these must be in scope for the #354 rebuild.**

## Follow-ups (tracked in #374)

- [x] **#354 graph rebuild** — done, PR #379 (see Current status).
- [x] Scout backlog (13 candidates) — drained by the 2026-07-23 arc (see Current status).
