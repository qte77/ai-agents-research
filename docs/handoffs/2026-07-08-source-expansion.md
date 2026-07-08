---
title: Handoff — 2026-07-08 source expansion + deferred graph rebuild (#354/#374)
purpose: Onboard a fresh session to finish the source-expansion effort — mainly the deferred graph rebuild that must now include all of this session's new docs.
created: 2026-07-08
updated: 2026-07-08
---

**Status**: Reference (handoff)

## TL;DR

Two waves of new sources landed 2026-07-08 (all merged to `main`). The **one open action** is the
deferred **#354 graph rebuild** — it must now incorporate *all* of them. Full map + rationale:
[../plans/2026-07-08-new-sources-batch.md](../plans/2026-07-08-new-sources-batch.md) (wave 1) and
[../plans/2026-07-08-source-expansion-wave2.md](../plans/2026-07-08-source-expansion-wave2.md) (wave 2).
Tracker: [#374](https://github.com/qte77/ai-agents-research/issues/374).

## Done (merged)

- **Wave 1:** #372 agentic-AI-vulnerability-landscape · #373 kv-cache-serving-landscape (+ CC-prompt-caching min-token fix) · #375 Codex-CC plugin + OpenWiki + company-brain + CONTRIBUTING polyfetch/doc-pipeline pointer.
- **Wave 2:** agents-cli, agentic-payments, karpathy-agentic-coding, agent-identity-auth (this PR).

## The open action — graph rebuild (#354)

1. `graphify` is installed: `uv tool install graphifyy` (package `graphifyy`, executable `graphify`).
   Python API via `uv tool run --from graphifyy python …` or the interpreter written to
   `graphify-out/.graphify_python` (`~/.local/share/uv/tools/graphifyy/bin/python`).
2. **Scope is near-full, not incremental:** `detect_incremental` (2026-07-08) already reported ~110+
   changed files vs a stale manifest (75+ docs → ~4-5 semantic subagents; 31 code/tooling files that
   `make graph-page` prunes anyway). Wave 2 adds ~4 more docs on top.
3. Flow: `/graphify --update` (or a full rebuild) → label the communities → `make graph-page` →
   commit `ui/graph.html` → push to `main` (gh-pages deploy) → check the box in #374 + comment #354.
4. It was deliberately deferred to a fresh session (context-exhaustion at the tail of a long build
   session) — run it with room to do the community-labeling + viz steps properly.

## Also open (lower priority)

- **Scout backlog** — 13 promotable triage/rxiv candidates as a checklist in #374 (parry, MOSS,
  silent-failure taxonomy, Probe-and-Refine, …; 4 flagged as borderline-dups to verify first). Write
  as new analysis docs when picked up; re-research first-party.

## Gotchas

- New scraping/PDF tooling is now documented in CONTRIBUTING's Research Workflow: **polyfetch-scrape**
  (fetch JS-SPA/blocked pages) and **doc-pipeline-engine** (PDF/Office → text), both via
  `uv run --directory`. Use them for dynamic/unparsable sources.
- Sourcing landmines recorded in the wave-2 plan: `ap2-protocol.org/specification/` 404s (use the
  GitHub repo); `docs.humanity.org/introduction/overview` 404s; x.com 402s automated fetch.
- Pre-existing unrelated link-rot to fix opportunistically: `usage.ai` 301 in `kiro-analysis.md`.
