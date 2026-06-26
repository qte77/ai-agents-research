---
title: CC Code-Analysis Tooling Landscape
purpose: Code-understanding tools that integrate with Claude Code — knowledge graphs, semantic LSP, structural search, and repository packers.
category: landscape
status: research
created: 2026-06-14
updated: 2026-06-25
validated_links: 2026-06-25
---

**Status**: Research (informational)

Code-analysis and code-context tools for Claude Code: knowledge-graph builders, live-LSP semantic toolkits, structural search/rewrite, and one-shot repository packers. Split out of [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) (which keeps the cross-tool comparison table). They split along **precompute-a-graph** (Graphify, Code-Review-Graph, codebase-memory-mcp) vs. **live-LSP** (Serena) vs. **on-demand structural search** (ast-grep MCP) vs. **embedded semantic search** (cocoindex-code) vs. **one-shot export** (Repomix, code2prompt).

## Graphify (safishamsi)

**Repo**: [safishamsi/graphify][graphify] | **Stars**: 16.5K | **License**: MIT

Transforms codebases, documentation, papers, and images into queryable knowledge graphs. Two-pass architecture: AST extraction via tree-sitter (local, deterministic) then LLM-powered semantic extraction (parallel subagents). Results merge into a NetworkX graph, clustered via Leiden community detection, exported as interactive HTML, JSON, and markdown reports.

### CC Integration

| Surface | Mechanism |
|---------|-----------|
| **Slash commands** | `/graphify .`, `/graphify query "..."`, `/graphify path`, `/graphify explain` |
| **PreToolUse hook** | Fires before Glob/Grep to surface graph structure instead of keyword search |
| **CLAUDE.md** | `graphify claude install` injects section directing Claude to read `GRAPH_REPORT.md` |
| **MCP server** | `python -m graphify.serve graph.json` exposes `query_graph`, `get_node`, `get_neighbors`, `shortest_path` |

### Key Features

- **71.5x token reduction** on mixed corpora versus raw file reading
- **20+ languages**: Python, TypeScript, Go, Rust, Java, C/C++, Ruby, C#, Kotlin, Scala, PHP, Swift, Lua, Zig, PowerShell, Elixir, Objective-C, Julia
- **Multimodal**: code, PDFs, markdown, screenshots, diagrams
- **Confidence tagging**: EXTRACTED (1.0), INFERRED (0.0–1.0), AMBIGUOUS
- **SHA256 caching**: only changed files reprocess; `--watch` mode for auto-sync
- **Wiki generation**: `--wiki` flag for agent-navigable knowledge bases
- **Privacy**: code processed locally via tree-sitter; only docs/images sent to LLM APIs

### Installation

```bash
pip install graphifyy && graphify install
```

Multi-platform: `--platform codex`, `opencode`, `claw`, `droid`, `trae`.

### Adoption Considerations

**Strengths**: Deepest CC integration in this category (hooks + slash commands + MCP + CLAUDE.md). No embeddings — Leiden clustering uses graph topology directly. Hyperedge support for n-way relationships. Rationale extraction from `# NOTE:`, `# HACK:`, `# WHY:` comments.

**Risks**: LLM-dependent for semantic pass (cost scales with repo size). PyPI package name is `graphifyy` (doubled y). Early stage relative to star count.

Cross-ref: [CC-repo-to-docs-tools-landscape.md](CC-repo-to-docs-tools-landscape.md) — complementary repo-to-docs generators

---

## Code-Review-Graph (tirth8205)

**Repo**: [tirth8205/code-review-graph][code-review-graph] | **Stars**: 7.1K | **License**: MIT

Persistent structural knowledge graph of codebases via tree-sitter AST parsing. Computes "blast radius" of changes — which functions, classes, and files are affected — to provide AI assistants with precisely scoped review context.

### Key Claims

- **8.2x average token reduction** across 6 repositories
- **Up to 49x fewer tokens** for monorepo daily tasks
- **100% recall** in impact analysis (no missed affected files)
- **Sub-2s incremental updates** (re-parses only modified files)

### CC Integration

`code-review-graph install` auto-configures Claude Code (plus Cursor, Windsurf, Zed, Continue, OpenCode, Antigravity). Exposes 22 MCP tools:

- Impact radius computation
- Token-optimized review context generation
- Graph querying (callers, callees, test coverage)
- Semantic search across codebase entities

### Language Support (19)

Python, TypeScript, JavaScript, Go, Rust, Java, C, C++, Ruby, C#, Kotlin, PHP, Swift, Scala, Lua, Elixir, Dart, R, Jupyter notebooks.

### Architecture

- **Storage**: SQLite in `.code-review-graph/` — no external dependencies
- **Parsing**: tree-sitter grammars for structural extraction
- **Monorepo optimized**: reduces review context from 27,700+ files to ~15 files

### Adoption Considerations

**Strengths**: Complementary to graphify (structural blast-radius vs. semantic knowledge graph). Zero external dependencies (SQLite-only). One-command multi-editor install. Research-grade recall claims.

**Risks**: Token reduction claims are self-reported (no independent benchmark). Overlaps with graphify's AST extraction layer. Early stage.

Cross-ref: [CC-repo-to-docs-tools-landscape.md](CC-repo-to-docs-tools-landscape.md) — related code understanding tools

---

## Qodo (qodo-ai)

**Repos**: [qodo-ai/agents][qodo-agents] · [qodo-ai/open-aware][qodo-aware] | **License**: MIT (both) | **Cross-repo review**: [docs.qodo.ai governance][qodo-crr]

A code-review / code-intelligence platform with three surfaces relevant here, all MCP-based — so they plug into Claude Code (and other assistants) directly.

| Surface | What it is |
|---|---|
| **open-aware** | Free "deep code research" MCP server — semantic search (`get_context`), architectural Q&A (`deep_research`, `ask`) across **multiple repositories** with daily-updated indexes of popular OSS libraries. Goes beyond keyword search via vector embeddings; private repos need the paid Qodo Aware tier. |
| **agents** ("Qodo Commands Playbooks") | TOML-defined agent workflows for Qodo Command — code review, test generation, issue handling, docs/changelog, license-compliance, security-scorecard fixes. Each agent declares instructions, tools (MCP servers), arguments, a `plan`/`act` execution strategy, an output schema, and exit expressions. |
| **cross-repo code review** | Governance feature: traces a PR's impact bidirectionally across *related* repos (Code / Service / Data / Pipeline relationships) to surface breaking changes — a signature change, API-contract shift, or schema evolution — that single-repo review misses. Findings appear inline, tagged "Cross-repo". |

### Key Differentiator

Code-Review-Graph (above) computes structural blast radius **within one repo**; Qodo's cross-repo review extends impact tracing **across repository boundaries** (shared libraries, API contracts, schemas). open-aware is the semantic-index counterpart (multi-repo embeddings) to the AST-graph tools in this doc, and the `agents` TOML format is an openly reusable playbook pattern.

### Adoption Considerations

**Strengths**: MCP-native (works with CC out of the box); the agent playbooks are an open (MIT) TOML pattern reusable as a harness reference; cross-repo review fills a gap no AST-blast-radius tool here covers.

**Risks**: open-aware's free tier indexes only pre-indexed *public* repos — private-repo coverage and cross-repo review are paid/enterprise. Star/adoption figures not independently verified here.

Cross-ref: [CC-official-plugins-landscape.md](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) — the first-party `/code-review` plugin

---

## AI PR-review agents (SaaS)

> **⚠ Placement — flagged for repositioning.** These are standalone SaaS code-review *products*, not community Claude Code integrations, so they do not fit this `cc-community` doc; queued for a move to a non-CC home (e.g. a `docs/non-cc/` code-review-products landscape). Retained here for now alongside the Qodo entry. Classification criteria: [CONTRIBUTING.md](../../CONTRIBUTING.md#classification-cc-community-vs-non-cc).

Adjacent to Qodo and Code-Review-Graph: hosted bots that review pull requests with whole-codebase context. Unlike the AST/graph tools above (which you run locally and an agent queries), these are GitHub/GitLab-app SaaS that comment on PRs directly; most also expose IDE or agent hooks.

- [CodeRabbit](https://www.coderabbit.ai/) — GitHub/GitLab/Azure/Bitbucket app + IDE (VS Code/Cursor/Windsurf) + CLI; bills itself "the most installed AI app on GitHub" (SaaS).
- [Greptile](https://www.greptile.com/) — a swarm of agents builds a codebase graph index, then reviews PRs in parallel; GitHub/GitLab, API, **MCP**, and a Claude Code plugin; SaaS or self-hosted in AWS.
- [Ellipsis](https://www.ellipsis.dev/) — GitHub-app code review plus automated bug fixes, Q&A, and changelogs (SaaS; free for public repos).
- [Sourcery](https://sourcery.ai/) — review focused on security and AI-generated-code defects; GitHub/GitLab, VS Code/JetBrains, fixes via coding agents (SaaS).
- [Qodo Merge / PR-Agent](https://github.com/qodo-ai/pr-agent) — the original open-source PR reviewer (Apache-2.0) behind Qodo; `/review` `/improve` `/describe` `/ask` via CLI, GitHub Action, Docker, or webhooks; GitHub/GitLab/Bitbucket/Azure/Gitea.
- [Graphite Diamond](https://graphite.com/) — AI reviewer bundled with Graphite's PR-stacking workflow; GitHub app, tuned for low false positives (SaaS).
- [Cursor Bugbot](https://cursor.com/bugbot) — Cursor's PR-review agent; comments on GitHub PRs and pushes fixes into the Cursor editor or a Background Agent; usage-based billing (SaaS).
- [Cubic](https://www.cubic.dev/) — YC-backed AI review plus whole-codebase bug scanning; GitHub app + IDE, one-click fixes, custom rules (SaaS).
- [Bito](https://bito.ai/) — codebase-aware AI Code Review Agent for GitHub/GitLab/Bitbucket (SaaS).
- [Korbit](https://www.korbit.ai/) — AI review across GitHub/GitLab/Bitbucket with bug explanations and auto-generated PR descriptions (SaaS).

These overlap heavily; the differentiators are codebase-context depth (Greptile's graph index), OSS vs SaaS (PR-Agent is the lone Apache-2.0 option), and agent/MCP reach (Greptile, CodeRabbit, Sourcery). Structural/AST counterpart: Code-Review-Graph above; cross-repo review: Qodo above.

---

## codebase-memory-mcp (DeusData)

**Repo**: [DeusData/codebase-memory-mcp][codebase-memory-mcp] | **Docs**: [deusdata.github.io][codebase-memory-mcp-docs] | **Stars**: 6.8K | **License**: MIT | **Version**: v0.8.1 (2026-06-12)

Single static binary that builds a persistent code knowledge graph for agents — no runtime dependencies, no external API. Combines 159 vendored tree-sitter grammars (syntactic parse), a clean-room hybrid-LSP type-resolution layer (Python, TS/JS, PHP, C#, Go, C/C++), and bundled `nomic-embed-code` embeddings (semantic search) into a SQLite-backed graph of typed nodes (Function, Class, Route) and edges (CALLS, IMPORTS, HTTP_CALLS).

### CC Integration

| Surface | Mechanism |
|---------|-----------|
| **MCP server** | 14 tools — `index_repository`, `search_graph`, `trace_path`, `query_graph` (Cypher-like read-only), `get_architecture`, `detect_changes`, `manage_adr`, `ingest_traces` |
| **PreToolUse hook** | Augments Grep/Glob with graph results before keyword search |
| **Auto-config** | `install` wires up Claude Code, Codex, Gemini CLI, Zed, OpenCode, Aider + others (PreToolUse hook for CC; SessionStart reminders for the rest) |

### Key Features

- **99.2% token reduction** claim: ~3,400 tokens for 5 structural queries vs ~412,000 via file-by-file grep
- **159 languages** (88 full AST, 71 additional); Linux kernel (~28M LOC) indexed in ~3 min, sub-ms queries
- **Install**: one-line `curl … | bash`, plus AUR / Homebrew / PyPI / npm; macOS / Linux / Windows

### Adoption Considerations

**Strengths**: Zero-dependency single binary (vs graphify's PyPI + LLM calls). Bundled local embeddings — semantic search with no API cost or data egress. Broadest language coverage in this category.

**Risks**: 99.2% reduction is self-reported (no independent benchmark). Hybrid-LSP type resolution is a clean-room reimplementation (only 7 languages fully resolved). Overlaps graphify and Code-Review-Graph on the AST/graph layer. Early stage (v0.x).

Cross-ref: Graphify and Code-Review-Graph above — same code→graph category; Serena below — live-LSP alternative

---

## cocoindex-code (cocoindex-io)

**Repo**: [cocoindex-io/cocoindex-code][cocoindex-code] | **Stars**: 2.2K | **License**: Apache-2.0 | **Version**: v0.2.36 (2026-06-19)

A lightweight embedded **semantic code-search** CLI (`ccc`) built on the Rust [CocoIndex](../non-cc/cocoindex-analysis.md) engine — natural-language queries over a codebase with a self-reported ~70% token saving vs file reading. tree-sitter AST chunking across 28+ languages, embeddings via local SentenceTransformers or 100+ providers (LiteLLM), incremental re-indexing of changed files only, and LMDB embedded storage (no external service).

### CC Integration

| Surface | Mechanism |
|---------|-----------|
| **MCP server** | `ccc mcp` — exposes code search to Claude Code, Codex, OpenCode |

### Adoption Considerations

**Strengths**: embeddings-based *semantic* search (vs the typed-graph approach of codebase-memory-mcp / Code-Review-Graph); embedded + incremental; a thin agent-integration layer over CocoIndex's Rust core. **Risks**: ~70% token-saving is self-reported (no independent benchmark); early stage (v0.x); embedding quality/cost depends on the chosen provider.

Cross-ref: [cocoindex-analysis.md](../non-cc/cocoindex-analysis.md) — the parent CocoIndex ETL/indexing engine; codebase-memory-mcp above — embedded typed-graph alternative

---

## Serena (oraios)

**Repo**: [oraios/serena][serena] | **Stars**: 25.2K | **License**: MIT | **Version**: v1.5.3 (2026-05-26)

LSP-based semantic coding toolkit — "an IDE for your agent." Unlike the AST/graph tools above (which precompute a graph), Serena drives live language servers via the Language Server Protocol, giving agents symbol-level operations: find symbol, find references, type hierarchy, rename/move refactor, safe delete, and diagnostics — atomic cross-file edits instead of text-replace guesswork.

### CC Integration

| Surface | Mechanism |
|---------|-----------|
| **MCP server** | 20+ symbol-level tools, configured as a launch command in CC. In a harness like CC the overlapping file/search/shell tools are often disabled, leaving Serena's semantic tools |
| **Memory** | Project memory files for long-lived workflows |
| **Install** | `uv tool install -p 3.13 serena-agent` then `serena init` |

### Key Features

- **40+ languages** via open-source language servers (Python, TS/JS, Go, Rust, C/C++, C#, Java, Kotlin, Scala, …); optional paid JetBrains backend
- Symbol-level retrieval/edit "especially in larger and more complex codebases"
- Free and OSS; reuses LLMs you already have

### Adoption Considerations

**Strengths**: Live LSP semantics (always current, no index to rebuild) vs the precomputed-graph approach of graphify / Code-Review-Graph / codebase-memory-mcp. Most-starred tool in this category. Symbol-aware refactors agents can't safely do via text edits.

**Risks**: Per-language LSP setup adds moving parts. Overlap with CC's built-in tools means the payoff is mainly in larger codebases. No headline token-reduction metric — efficiency comes from precise symbol queries, not corpus compression.

Cross-ref: [CC-official-plugins-landscape.md](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) — previously only named there (partner marketplace); analyzed here

---

## ast-grep MCP (ast-grep)

**Repo**: [ast-grep/ast-grep-mcp][ast-grep-mcp] | **Stars**: 419 | **License**: MIT | **Version**: unreleased (main branch)

Experimental MCP wrapper around the [ast-grep][ast-grep] Rust structural search/rewrite CLI. Exposes tree-sitter AST pattern matching to agents so they search by *syntax structure* (functions, classes, imports, call shapes) instead of text — fewer false positives than Grep, and structure-preserving rewrites.

### CC Integration

| Surface | Mechanism |
|---------|-----------|
| **MCP server** | 4 tools — `dump_syntax_tree`, `test_match_code_rule`, `find_code`, `find_code_by_rule` (YAML rules) |
| **Runtime** | Python + FastMCP; `uvx --from git+https://github.com/ast-grep/ast-grep-mcp`; JSON client config (CC / Cursor / Claude Desktop) |

### Key Features

- Structural patterns across JS/TS, Python, Rust, Go, Java, C/C++, C# and more (custom languages supported)
- **~75% fewer tokens** with the text output format vs JSON metadata
- `dump_syntax_tree` lets the agent learn a language's node types before writing a pattern

### Adoption Considerations

**Strengths**: Lightweight and on-demand — no index to build (vs the persistent-graph tools above). Precise structural search/rewrite; pairs well with a graph tool for navigation plus a pattern tool for edits.

**Risks**: Experimental, no tagged releases, low star count (the parent ast-grep CLI is mature; the MCP wrapper is early). Requires writing ast-grep patterns / YAML rules to get full value.

Cross-ref: complements the persistent-graph tools above (search/rewrite vs navigation)

---

## Repomix & code2prompt (repository packers)

A distinct sub-category: one-shot **context export** rather than a live MCP graph. Both flatten a repo into a single LLM-ready artifact with token counting, for pasting into a chat or seeding an agent's first turn.

### Repomix (yamadashy)

**Repo**: [yamadashy/repomix][repomix] | **Stars**: 26.2K | **License**: MIT | **Version**: v1.14.1 (2026-05-27)

Packs a repository into one AI-friendly file (XML / Markdown / JSON / plain text), respecting `.gitignore` and scanning for secrets via Secretlint. `--compress` uses tree-sitter to keep classes/functions/interfaces and drop bodies — **~70% token reduction** while preserving structure. Reports per-file and repo-wide token counts (`o200k_base` / `cl100k_base`). **CC integration**: MCP server (`pack_codebase`, `pack_remote_repository`, `read_repomix_output`, `grep_repomix_output`, …) plus official CC plugins — `repomix-mcp`, `repomix-commands`, `repomix-explorer` via `/plugin marketplace add yamadashy/repomix`. Run with `npx repomix@latest`.

### code2prompt (mufeedvh)

**Repo**: [mufeedvh/code2prompt][code2prompt] | **Stars**: 7.4K | **License**: MIT | **Version**: v4.2.0 (2025-12-11)

Rust CLI that renders a codebase into a single prompt with a source tree, Handlebars templating, git integration, and token counting. Ships an MCP server and a Python SDK (`pip install code2prompt-rs`); also `cargo install` / Homebrew.

### Adoption Considerations

**Use when**: you want a deterministic, whole-repo snapshot for a one-off question, an agent's first turn, or a non-CC LLM — no server to run. **Prefer the graph/LSP tools above** (codebase-memory-mcp, graphify, Serena) for repeated, large-codebase work, where re-sending a packed corpus every turn would blow the context budget. Repomix's `--compress` and these packers are complementary to RTK (output-side) and Boucle (read dedup), both in the [main tooling landscape](CC-community-tooling-landscape.md).

## Cross-References

- [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) — full cross-tool comparison + the rest of the CC tooling landscape
- [CC-repo-to-docs-tools-landscape.md](CC-repo-to-docs-tools-landscape.md) — repo-to-docs generators

[graphify]: https://github.com/safishamsi/graphify
[code-review-graph]: https://github.com/tirth8205/code-review-graph
[codebase-memory-mcp]: https://github.com/DeusData/codebase-memory-mcp
[codebase-memory-mcp-docs]: https://deusdata.github.io/codebase-memory-mcp/
[cocoindex-code]: https://github.com/cocoindex-io/cocoindex-code
[serena]: https://github.com/oraios/serena
[ast-grep-mcp]: https://github.com/ast-grep/ast-grep-mcp
[ast-grep]: https://github.com/ast-grep/ast-grep
[repomix]: https://github.com/yamadashy/repomix
[code2prompt]: https://github.com/mufeedvh/code2prompt
[qodo-agents]: https://github.com/qodo-ai/agents
[qodo-aware]: https://github.com/qodo-ai/open-aware
[qodo-crr]: https://docs.qodo.ai/governance/cross-repo-code-review
