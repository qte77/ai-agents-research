---
title: Graphify rebuild (#354) — incorporate the new-sources docs → gh-pages
status: approved
issue: 354
created: 2026-07-08
updated: 2026-07-08
---

**Status**: Reference (plan)

Staged, execution-ready plan for the deferred [#354](https://github.com/qte77/ai-agents-research/issues/354)
graph rebuild. **Approved but not yet executed** — deliberately handed to a fresh, focused session
(the extraction is token-heavy). Handoff: [../handoffs/2026-07-08-graphify-rebuild-354.md](../handoffs/2026-07-08-graphify-rebuild-354.md).
Tracker: [#374](https://github.com/qte77/ai-agents-research/issues/374).

## Context

The key-free `/graphify` rebuild yields fewer concept nodes than a prior graph (427 vs 583) — inherent
to key-free extraction (session model, no LLM key), and **accepted**. The recorded decision: defer the
rebuild until new sources are added so it reflects real content, not a parity chase. Waves 1+2 are now
merged (#372/#373/#375/#376): ~9 new/changed analysis docs (agentic-AI security, KV-cache serving,
Codex-CC/OpenWiki/company-brain tooling, agentic payments, agent identity/auth, Karpathy). Rebuild so
the published graph + gh-pages site reflect them.

**Node-count expectation:** ~430–470 (427 baseline + new docs), **not 583**. Sparser is the accepted
key-free tradeoff, not a regression.

## Approach

Run the **`/graphify --update`** skill flow (re-extract changed files, `build_merge` into the existing
`graphify-out/graph.json`), then `make graph-page` → commit `ui/graph.html`. Fallback: a full
`/graphify` rebuild (hits cache for unchanged files).

## Code / file / source map (don't re-gather)

### graphify runtime

- Installed via `uv tool install graphifyy` (package `graphifyy`; executables `graphify`, `graphify-mcp`).
- Python API interpreter: `~/.local/share/uv/tools/graphifyy/bin/python`, also written to
  `graphify-out/.graphify_python`. Run headless API as `uv tool run --from graphifyy python -c "…"`.
- Skill: `.claude/skills/graphify/SKILL.md` (full pipeline) + `references/update.md` (the `--update`
  flow: `detect_incremental` → populate `.graphify_detect.json` → extract → `build_merge` → Steps 4–8).

**Changed-set (detect_incremental, 2026-07-08):** ~110 files vs a stale manifest — ~75 docs (semantic),
~31 code/tooling (AST, free, pruned from the published graph), 1 image. Unchanged hit the semantic cache.

### Extraction

- AST: `graphify.extract.extract(code_files, cache_root=Path('.'))` → `.graphify_ast.json`.
- Semantic: **general-purpose subagents**, ~20 docs/chunk (~4 agents), prompt = `references/extraction-spec.md`
  verbatim (write each chunk to `graphify-out/.graphify_chunk_NN.json`). Scope tightly: extraction only,
  no skills, no `.claude` edits (derail risk — AGENT_LEARNINGS).
- Merge: `graphify.build.build_merge([new_extraction], graph_path='graphify-out/graph.json', prune_sources=changed)`.

### Render / deploy

- `make graph-page` → `graph-html` (`graphify export html`) + `scripts/render-graph-page.py`.
- `scripts/pages_build.py`: `filter_graph_data()` prunes tooling nodes (`scripts/ tests/ ui/ src/ .github/scripts/`);
  `restyle_graph()` applies EyeRest theme, injects fonts/favicon/title, vendors vis-network. **Unit-tested** in `tests/` (`make test`).
- **Committed artifact: `ui/graph.html`** (the gh-pages deploy source — see
  [../architecture.md](../architecture.md#knowledge-graph-graphify)). `graphify-out/` (graph.json,
  GRAPH_REPORT.md, caches) is **gitignored** — never commit it.
- Deploy: pushing `ui/graph.html` to `main` triggers the gh-pages Actions workflow →
  `qte77.github.io/ai-agents-research/graph.html`.

## Steps

1. Interpreter ready (`graphify-out/.graphify_python`).
2. `detect_incremental(Path('.'))` → confirm ~110; populate `.graphify_detect.json` (changed + all_files).
3. Extract: AST (code) ∥ ~4 semantic subagents (docs); cache hits for unchanged.
4. `build_merge` → cluster → analyze → regenerate `graph.json` + `GRAPH_REPORT.md`.
5. Label communities (2–5 words each) from node lists.
6. `make graph-page` → `ui/graph.html`.
7. Verify (below).
8. Branch `chore/graphify-rebuild-354`; commit **only `ui/graph.html`** + a changelog fragment
   (`### Changed`); PR; green CI → admin-merge → prune; gh-pages deploys.
9. Close #354 (comment: rebuilt, N nodes, waves 1+2) + check the box on #374.

## Verification

1. `graph.json` non-empty; node count ~430–470 (not 583); graph-diff shows new payments/identity-auth/
   kv-cache/security/Karpathy nodes.
2. `make test` → pages_build + render tests green.
3. `make graph-page` regenerates `ui/graph.html`; `make preview` renders; code/tooling nodes pruned;
   EyeRest theme + fonts + favicon present.
4. `make check_docs` (only the changelog fragment is new md) → 0.
5. Post-merge: gh-pages graph reflects the new docs.

## Gotchas

- Key-free = fewer nodes (~430–470, not 583). `graphify-out/` gitignored — ship only `ui/graph.html`.
  `make graph-page` needs `graph.json` first (build via `/graphify`). Extraction-spec-only subagent
  prompt. Unique branch name (avoid same-day collisions). Token-heavy → focused session.
