---
title: New-sources batch — agentic-AI security, KV-cache, tooling
status: done
issue: 374
created: 2026-07-08
updated: 2026-07-08
---

**Status**: Reference (plan)

Durable record of the 2026-07-08 new-sources batch — analysis docs added to the corpus ahead of the
[#354](https://github.com/qte77/ai-agents-research/issues/354) graph rebuild, so the regenerated graph
reflects real new content. Tracker: [#374](https://github.com/qte77/ai-agents-research/issues/374).

## Context

User supplied ~14 links (heavily agentic-AI security) + "company brain" + KV caches; a backlog scout
also surfaced triage/rxiv candidates. All researched first-party (multi-agent fan-out; dynamic/SPA
sources rendered via [polyfetch-scrape](https://github.com/qte77/polyfetch-scrape), e.g. the Berkeley
coverage-map). Routing verified against existing coverage to extend/cross-ref rather than duplicate.

## Delivered (3 PRs)

| PR | Deliverable |
|---|---|
| #372 | NEW `sdlc-lcm/agentic-ai-vulnerability-landscape.md` — operational vuln layer: OWASP AIVSS, MITRE ATLAS (+ AI Incident Sharing), Microsoft MDASH/Vuln.AI, Berkeley Vulnerability Initiative, 2 arXiv surveys. Cross-links (not dup) the MAESTRO/governance docs. |
| #373 | NEW `non-cc/kv-cache-serving-landscape.md` — cross-vendor prompt-caching (Anthropic/OpenAI/Gemini) + serving internals (PagedAttention, RadixAttention, quantization, GQA/MLA, Mooncake/LMCache). Fixed a stale fact in `CC-prompt-caching-behavior.md` (Opus 4.8 min = 1,024, not 4,096). |
| this | NEW `cc-community/CC-codex-plugin-cc-analysis.md`; EXTEND `repo-to-docs-tools-landscape.md` (OpenWiki) + `agentic-enterprise-os-landscape.md` (company brain); CONTRIBUTING polyfetch/doc-pipeline pointer; this plan. |

## Placement decisions (rationale)

- **Security → `sdlc-lcm/`** (not non-cc): joins the existing security cluster (MAESTRO, governance); new doc takes the *vuln-discovery/scoring* angle, cross-refs the *governance-framework* angle.
- **KV-cache → `non-cc/`**: cross-vendor serving infra (Anthropic = one of three vendor rows); the CC-specific caching view stays in cc-native.
- **Company brain → EXTEND `agentic-enterprise-os-landscape.md`**: a synthesis label (agent-memory + KG/GraphRAG + informal ontology + permissioning + write-back), not a distinct category; 2 of 4 sources are vendor marketing. No standalone doc unless it gains non-vendor traction.
- **Papers**: folded into the security landscape; `docs/research/rxiv-agentic-papers.md` left untouched (auto-generated).

## Follow-ups (tracked in #374)

- [#354](https://github.com/qte77/ai-agents-research/issues/354) graph rebuild once these land.
- Scout backlog (13 candidates) — checklist in #374; write when picked up, re-verify first-party.
