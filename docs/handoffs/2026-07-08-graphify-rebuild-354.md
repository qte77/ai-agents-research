---
title: Handoff — execute the #354 graphify rebuild
purpose: Onboard a fresh session to run the deferred graph rebuild end-to-end, using the approved plan.
created: 2026-07-08
updated: 2026-07-08
---

**Status**: Reference (handoff)

> **DONE — executed by PR #379 (2026-07-10, 637 nodes; #354 closed).** Retained for method reference
> only. Do **not** re-run as a per-doc update — a fine-chunk re-extract is denser than the uniform
> base graph and lopsides it (see AGENT_LEARNINGS). A refresh must be a full uniform rebuild.

## TL;DR

Run the deferred **#354** graph rebuild so the published knowledge graph + gh-pages site include this
session's new docs (waves 1+2). The **execution-ready plan with the full command/file map** is
[../plans/2026-07-08-graphify-rebuild-354.md](../plans/2026-07-08-graphify-rebuild-354.md) — read it
first; it has everything so you don't re-map. Tracker [#374](https://github.com/qte77/ai-agents-research/issues/374).

## Do this

1. **Sanity check** you're at repo root with a clean `main`, and `graphify` resolves:
   `uv tool run --from graphifyy python -c "import graphify"` (install once: `uv tool install graphifyy`).
2. **Run `/graphify --update`** — it drives detect → extract (AST ∥ ~4 semantic subagents over ~75
   changed docs) → `build_merge` → cluster → community-labeling. Expect ~430–470 nodes (**not 583** —
   key-free is sparser; that's accepted). ~4–5 subagents, token-heavy → you're in a focused session.
3. **`make graph-page`** → regenerates the committed **`ui/graph.html`** (restyle + prune tooling nodes).
4. **Verify:** `make test` green; `make preview` renders `ui/graph.html`; graph-diff shows new
   payments/identity-auth/kv-cache/security/Karpathy nodes.
5. **Ship:** branch `chore/graphify-rebuild-354`; commit **only `ui/graph.html`** (+ a `### Changed`
   changelog fragment) — `graphify-out/` is gitignored, never commit it; PR → green CI → admin-merge
   (lychee may trip on unrelated pre-existing rot, e.g. `usage.ai` in kiro — merge past) → prune. The
   gh-pages workflow deploys on the `ui/` change.
6. **Close #354** (comment the node count + that it covers waves 1+2) and tick the graph-rebuild box on #374.

## Don't

- Don't chase 583 nodes — key-free extraction is inherently sparser (the accepted #354 tradeoff).
- Don't commit `graphify-out/` (gitignored). Don't run `make graph-page` before `graph.json` exists.
- Don't let the extraction subagents drift — scope them to the graphify extraction-spec only (no
  skills, no `.claude` edits).

## Gotchas carried from this session

- Sourcing landmines (if you touch the docs): `ap2-protocol.org/specification/` 404s (use the GitHub
  repo); `docs.humanity.org/introduction/overview` 404s; `x.com` 402s WebFetch; PDFs need
  doc-pipeline-engine (no local `poppler`). polyfetch-scrape renders JS-SPA/blocked pages.
- Run `make check_docs` directly; `make lint` aborts at the lychee flake before markdownlint.
