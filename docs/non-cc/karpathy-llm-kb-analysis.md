---
title: "Karpathy LLM Knowledge Base: Markdown-First Alternative to RAG"
purpose: Analyse Karpathy's LLM wiki pattern and gap-compare against ai-agents-research
created: 2026-04-06
updated: 2026-04-06
validated_links: 2026-04-06
---

**Status**: Assess

## What It Is

A markdown-first knowledge management pattern where the LLM acts as author, editor, and librarian of a persistent wiki — replacing vector-DB RAG with explicit structure, summaries, and backlinks. Published by Andrej Karpathy in April 2026 as an [idea gist][gist] with no dedicated repository.

## Architecture

![Three-layer architecture comparison](images/karpathy-llm-kb-architecture.svg)

Three immutable layers:

| Layer | Role | Owner |
|---|---|---|
| **Raw sources** | Immutable ingest of articles, papers, data | Human (capture) |
| **Wiki** (`.md` files) | Compiled summaries, entity pages, cross-refs | LLM (maintenance) |
| **Schema** (`CLAUDE.md`-style) | Conventions, workflows, structure rules | Human (curation) |

### Operations Cycle

![Operations cycle: Ingest-Query-Lint](images/karpathy-llm-kb-workflow.svg)

| Operation | Description |
|---|---|
| **Ingest** | LLM reads new raw source, writes summaries, updates ~10-15 wiki pages, logs activity |
| **Query** | LLM searches wiki pages, synthesises answer with citations; valuable answers filed back as pages |
| **Lint** | Periodic LLM pass finding contradictions, stale claims, orphan pages, missing cross-refs |

Navigation relies on an `index.md` content catalogue and an append-only `log.md` — no embedding infrastructure required.

### Design Principles

- **File-over-app** — markdown + git outlast any vendor platform
- **LLM handles bookkeeping** — humans focus on curation and strategy
- **Compounding knowledge** — each ingest/query enriches the wiki; no re-synthesis from scratch
- **Sandbox hygiene** — raw sources separated from compiled wiki; controlled promotion
- **Tooling**: Obsidian (browsing), git (versioning), Web Clipper (capture)

Reported scale: ~100 articles, ~400 K words — sufficient for index-based navigation without RAG.

## Gap Analysis Against ai-agents-research

| Capability | Karpathy pattern | ai-agents-research | Gap? |
|---|---|---|---|
| Markdown-first storage | `.md` files, git-versioned | 118 `.md` files, git-versioned | **No gap** |
| Raw ingest stage | `raw/` directory, Web Clipper | `triage/` + [3 automated monitors][monitors] | **No gap** — monitors are more systematic |
| Structured compilation | LLM reads raw, writes wiki pages | Human reviews triage PR, authors analysis doc | **Real** — no LLM compilation step |
| Schema / conventions | `CLAUDE.md`-style schema file | [CONTRIBUTING.md][contributing] + `.claude/rules/` + `.markdownlint.json` | **No gap** — governance is more detailed |
| Index pages | Single `index.md` catalogue | Subdirectory READMEs with doc tables + [architecture.md][arch] | **No gap** — multi-level indexing is richer |
| Cross-references | LLM-maintained backlinks | Manual reference-style links + "See Also" sections | **Partial** — links exist but no orphan detection |
| Lint / health checks | LLM-driven semantic lint | [markdownlint][mlint] (structural) + `validated_links` dates | **Partial** — structural lint exists, semantic lint does not |
| Activity log | `log.md` with parseable prefixes | [CHANGELOG.md][changelog] (Keep a Changelog) + git history | **No gap** |

### Value-Add Opportunities

Two real gaps where adoption would compound existing strengths:

1. **LLM compilation from triage to draft** — Triage monitors already produce structured reports. An LLM step could generate draft analysis docs from triage output, reducing the manual authoring bottleneck. Fits naturally as a skill or CI step between monitor output and PR creation.

2. **Orphan / stale-link detection** — Backlinks exist but are manually maintained. A lightweight script or skill checking for docs with zero inbound links and broken relative paths would close this gap without requiring LLM-driven semantic linting.

### Relevance to qte77

This repository already implements the Karpathy pattern's core thesis — structured markdown managed by conventions, with automated ingest and human-curated promotion. The pattern validates the existing architecture rather than replacing it. The two value-add opportunities above are incremental enhancements, not architectural shifts.

The gist's abstract, domain-agnostic framing makes it a useful reference for any qte77 repo adopting a knowledge-base pattern (e.g. `coding-agent-eval` documentation, cross-repo learnings).

## Sources

| Source | Content |
|---|---|
| [Karpathy gist — llm-wiki.md][gist] | First-party architecture description (three layers, operations, principles) |
| [Karpathy X post (original)][x-post] | Original announcement with scale numbers (~100 articles, ~400 K words) |
| [Karpathy X post (follow-up)][x-followup] | Follow-up noting viral response, links to gist |
| [TechBuddies analysis][techbuddies] | Third-party deep-dive with RAG comparison table |

[gist]: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
[x-post]: https://x.com/karpathy/status/2039805659525644595
[x-followup]: https://x.com/karpathy/status/2040470801506541998
[techbuddies]: https://www.techbuddies.io/2026/04/04/inside-karpathys-llm-knowledge-base-a-markdown-first-alternative-to-rag-for-autonomous-archives/
[monitors]: ../../.github/workflows/cc-changelog-monitor.yaml
[contributing]: ../../CONTRIBUTING.md
[arch]: ../architecture.md
[mlint]: ../../.markdownlint.json
[changelog]: ../../CHANGELOG.md
