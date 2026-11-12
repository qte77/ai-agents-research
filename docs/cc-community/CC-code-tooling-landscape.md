---
title: CC Code-Analysis Tooling Landscape
purpose: Code-understanding tools that integrate with Claude Code — knowledge graphs, semantic LSP, structural search, and repository packers.
category: landscape
status: research
created: 2026-06-14
updated: 2026-11-12
validated_links: 2026-11-12
---

Code-analysis and code-context tools for Claude Code: knowledge-graph builders, live-LSP semantic toolkits, structural search/rewrite, and one-shot repository packers. Split out of [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) (which keeps the cross-tool comparison table). They split along **precompute-a-graph** (Graphify, AxiomCode Graph, Graphicle, Code-Review-Graph, codebase-memory-mcp) vs. **live-LSP** (Serena) vs. **on-demand structural search** (ast-grep MCP) vs. **trigram-indexed text search** (tgrep) vs. **local hybrid lexical+semantic search** (zg, XERJ) vs. **embedded semantic search** (cocoindex-code) vs. **one-shot export** (Repomix, code2prompt).

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

Cross-ref: [repo-to-docs-tools-landscape.md](../non-cc/knowledge-management/repo-to-docs-tools-landscape.md) — complementary repo-to-docs generators

---

## AxiomCode Graph (AxiomCodeAI)

**Repo**: [AxiomCodeAI/axiomcodegraph][axiomcode] | **Stars**: 609 | **License**: FSL-1.1-Apache-2.0 (Functional Source License — free for internal use, non-commercial research/education and professional services; converts to Apache-2.0 two years after each version's release; **not** an OSI-approved open-source license while under FSL) | **Version**: npm `@axiomcode/code-graph`, `gh api` 2026-11-12

Builds a codebase knowledge graph from **formal methods** rather than tree-sitter syntax matching: each call edge is resolved from the receiver's declared/inferred type "the way the compiler does" — scored against Java bytecode and the TypeScript type checker — instead of guessed from a name match. Supports Java, TypeScript and Python (stable); JavaScript and C# (beta).

### Benchmarks (self-reported against named competitors, README, `gh api` 2026-11-12)

On 748 held-out Defects4J bugs, the tests AxiomCode selects from source include every bug-revealing test for 94.9% of bugs (best tree-sitter-based competitor in the same table, "GitNexus": 61.5%; Graphify: 48.7%; Code-Review-Graph: 21.9%). Call-to-declaration linking accuracy scored against ground truth (five open-source projects per language): 96.5% (Java, vs. bytecode) and 88.8% (TypeScript, vs. the type checker), against the next-best tool in each row of the same table: GitNexus at 78.9% for Java, Code-Review-Graph at 71.6% for TypeScript (GitNexus trails on TypeScript, at 65.1%). The README also claims "up to 50% fewer tool calls to explore a new codebase."

### CC Integration

Repo topics list `claude-code`, `codex`, `cursor`, `antigravity`, `gemini`, `mcp` — an installable CLI/MCP server exposing the graph for impact/blast-radius queries, call paths and cross-file coverage.

### Adoption Considerations

**Strengths**: the only precomputed-graph tool in this doc that resolves calls from a compiler-equivalent type signal rather than syntax matching (Serena, below, also avoids syntax matching, but via a live LSP server rather than a precomputed graph), with accuracy gains that hold up against five named competitors on an independent benchmark (Defects4J); actively maintained (pushed 2026-11-09, created 2026-08-22).

**Risks**: **FSL, not a standard permissive license** — production use that competes with AxiomCode's own offering is restricted until each release's two-year Apache-2.0 conversion date; JavaScript/C# support is beta; young project relative to its star count; only Java and TypeScript have independent ground truth for the headline benchmark.

Cross-ref: Graphify and Code-Review-Graph below — AxiomCode Graph's own benchmark names both as comparators; Graphicle below — a different Graphify-lineage competitor

---

## Graphicle (Graphicle-AI)

**Repo**: [Graphicle-AI/graphicle][graphicle] | **Stars**: 561 | **License**: Apache-2.0 | **Version**: v0.1.11 (README benchmark label), `gh api` 2026-11-12

A Rust port of Graphify's code-graph engine, explicitly credited as such — "Graphify, ported to Rust. Plus memory... Graphicle is not affiliated with Graphify Labs" (README) — with an added agent-memory layer in the same binary. Maps a repository into a code graph and "remembers your project's docs, decisions and past agent sessions," giving cited excerpts (file + line) from both.

### Benchmarks (self-reported, `docs/benchmarks.md`, against named Graphify version)

Graphicle 0.1.11 vs. Graphify 0.9.100, one machine: first build of Kubernetes v1.37.1 (code-only graph) in 1 min 14s vs. 29 min 18s (23.9×); across 13 codebases, 3.4–23.9× less build time in 34 of 39 measurements (Graphify was faster only on no-change incremental updates, where it "now stops early"). On agent memory (LoCoMo-10, pre-release build, one open model — Qwen3.8-27B — as every system's reader/judge): 87.7 accuracy, level with Hindsight 0.10.2 (87.3) and above Mem0 OSS 2.2.1 (81.9), at ~12 model calls per conversation against 160 (Hindsight) and 332 (Mem0).

### CC Integration

`graphicle setup` indexes the repo, builds the graph, and auto-connects Claude Code, Cursor, Codex, VS Code and Claude Desktop — one MCP server per agent; Claude Code additionally gets five tools and session capture, plus an `AGENTS.md` section and git hooks that keep the graph current after every commit.

### Adoption Considerations

**Strengths**: direct, benchmarked lineage from Graphify with a stated large speed advantage on both first build and incremental updates; folds agent memory into the same binary instead of requiring a second tool; `graphicle disconnect` reverses every file `setup` touched, with backups.

**Risks**: pre-1.0 (v0.1.11), very young (created 2026-10-14); all benchmark numbers are the vendor's own, against named-version competitors it chose, and the memory comparison uses a single open model as reader/judge for every system including competitors (disclosed, not independently confirmed); overlaps directly with Graphify, and for the memory half with every cross-agent memory tool in [CC-memory-tooling-landscape.md](CC-memory-tooling-landscape.md) — pick one per role.

Cross-ref: [Graphify](#graphify-safishamsi) above — the engine Graphicle ports; [CC-memory-tooling-landscape.md](CC-memory-tooling-landscape.md) — cross-agent memory tools, for the memory half of Graphicle's scope

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

Cross-ref: [repo-to-docs-tools-landscape.md](../non-cc/knowledge-management/repo-to-docs-tools-landscape.md) — related code understanding tools

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

## codebase-memory-mcp (DeusData)

**Repo**: [DeusData/codebase-memory-mcp][codebase-memory-mcp] | **Docs**: [deusdata.github.io][codebase-memory-mcp-docs] | **Stars**: ~19K (2026-06-28) | **License**: MIT | **Version**: v0.8.1 (2026-06-12)

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

A lightweight embedded **semantic code-search** CLI (`ccc`) built on the Rust [CocoIndex](../non-cc/context-memory/cocoindex-analysis.md) engine — natural-language queries over a codebase with a self-reported ~70% token saving vs file reading. tree-sitter AST chunking across 28+ languages, embeddings via local SentenceTransformers or 100+ providers (LiteLLM), incremental re-indexing of changed files only, and LMDB embedded storage (no external service).

### CC Integration

| Surface | Mechanism |
|---------|-----------|
| **MCP server** | `ccc mcp` — exposes code search to Claude Code, Codex, OpenCode |

### Adoption Considerations

**Strengths**: embeddings-based *semantic* search (vs the typed-graph approach of codebase-memory-mcp / Code-Review-Graph); embedded + incremental; a thin agent-integration layer over CocoIndex's Rust core. **Risks**: ~70% token-saving is self-reported (no independent benchmark); early stage (v0.x); embedding quality/cost depends on the chosen provider.

Cross-ref: [cocoindex-analysis.md](../non-cc/context-memory/cocoindex-analysis.md) — the parent CocoIndex ETL/indexing engine; codebase-memory-mcp above — embedded typed-graph alternative

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

## tgrep (microsoft)

**Repo**: [microsoft/tgrep][tgrep] | **Stars**: 3,346 | **License**: MIT | **Version**: v1.0.10 (2026-09-21)

Trigram-indexed grep with a client/server architecture, built to search large codebases locally faster than plain regex scanning. A trigram index narrows each query to candidate files before the regex engine verifies matches, so tgrep skips reading files that cannot match.

### How It Works

- **Server mode** (`tgrep serve .`) builds a hybrid mmap-plus-mutable-overlay index and watches the filesystem asynchronously; clients connect over JSON-RPC 2.0 on a TCP loopback port
- **Without a server**, `tgrep index .` builds an on-disk index that searches use directly; with neither, tgrep falls back to a full filesystem scan (like plain grep) and warns on stderr
- **`--no-index`** forces a fresh-disk read when a search must reflect files changed since the last index build
- **Built into GitHub Copilot CLI** to power its grep searches across large repos

### Performance (self-reported)

Per its own `BENCHMARKS.md` (August 24, 2026 sweep): tgrep beat ripgrep in 17 of 18 repo/platform combinations, with speedups from 0.93× to 51.9×, measured as client/server search latency with the index already built (not indexing time) — no independent benchmark exists.

### Adoption Considerations

**No first-party Claude Code integration.** `install-agent.sh`, the official agent installer, wires only **Codex** and **pi** (`--agent codex,pi`) — it does not target Claude Code as of 2026-09-24. A Claude Code user can still run tgrep as a faster local `grep`/`rg` substitute via Bash, or hand-wire its stdio MCP server into `.mcp.json` the way any other MCP server is added, but neither path is documented or maintained by the project itself.

**Strengths**: a pre-built index makes repeat searches on large repos far faster than a cold ripgrep scan; Microsoft-maintained with active CI and a fast release cadence (v1.0.10 as of 2026-09-21).

**Risks**: the index can lag filesystem changes between refreshes (mitigated by `--no-index` at the cost of speed); the speedup benchmark is self-reported; no CC-native install path.

Cross-ref: ast-grep MCP above — structural AST search vs. tgrep's indexed regex/text search; both are on-demand, with no persistent knowledge graph

---

## zg / zvec-grep (zvec-ai)

**Repo**: [zvec-ai/zvec-grep][zvec-grep] | **Stars**: 3,752 | **License**: Apache-2.0 | **Version**: v0.2.0 (2026-08-27)

Local-first search layer that unifies ripgrep (exact/regex), BM25 (lexical ranking), and vector search (semantic) behind one interface, "for humans and agents." Built on [zvec][zvec] (Alibaba's vector engine); the documented implementation is TypeScript/Node.js ≥22 (npm), with a separate Rust implementation developed in the repo's `rust/` subdirectory.

### CC Integration (first-party, direct)

`zg --install --target claude` configures Claude Code specifically — it manages `~/.claude.json`, `~/.claude/settings.json`, and `~/.claude/CLAUDE.md` (honoring a `CLAUDE_CONFIG_DIR` override), adds a managed `zvec_grep` MCP entry, local MCP tool approval, and search guidance. The same installer also targets Codex, Qwen Code, Qoder, OpenCode, Cursor, GitHub Copilot, and VS Code.

### Default Agent Toolset

| Tool | Use it when |
|---|---|
| `zvec_grep_search` | The answer is workspace-grounded and wording/location is unknown, or semantic/fuzzy/relationship/chronology/cross-file synthesis is required |

Agents are steered to use native grep/rg for exact lookups (a known word, quote, filename, key) and `zvec_grep_search` for everything else — the two are complementary, not a full grep replacement.

### Adoption Considerations

**Strengths**: unlike tgrep above (no CC target at all) and ast-grep MCP (manual JSON client config only), zg ships an explicit, documented `--target claude` installer that writes CC's own config files directly; combines exact, lexical, and semantic retrieval in one local index rather than requiring a separate vector DB; broad multi-agent install coverage (8 named harnesses/IDEs).

**Risks**: young (repo created 2026-07-10); the dual TS/Rust implementation is a maintenance surface to watch; no independent benchmark of its own retrieval-quality claims (the repo carries internal `zg-retrieval-metric-review.md` / `zg-retrieval-only-sweqa20-design.md` design docs, not third-party validation).

Cross-ref: cocoindex-code above — the other embeddings-based semantic search tool in this doc; zg adds exact ripgrep + BM25 lexical ranking in the same local index rather than embeddings alone

---

## XERJ (xerj-org)

**Repo**: [xerj-org/xerj][xerj] | **Stars**: 18,868 (GitHub's Trendshift badges label it "#1 Rust Repository of the Day/Week") | **License**: Apache-2.0 | **Version**: v1.0.0-rc.101 (README, `gh api` 2026-11-12)

Local-first, Elasticsearch-API-compatible search engine and MCP server: one Rust binary indexes code, docs, logs, JSONL/CSV and PDFs for BM25 full-text, vector and hybrid search. Its flagship coding-agent use case is **reference coding** — `xerj autoindex` clones and indexes the open-source repos closest to a task so a coding agent reuses how they solved the same problem instead of writing from memory.

### CC Integration

`xerj init` wires Claude Code and Cursor directly (MCP + an installed skill), one command. Also exposes an MCP recipe for agent memory (`/memory`) and a batch-search tool (`xerj_batch_search`).

### Benchmarks

The README's own "controlled study" reports a 2.7× cut in a coding agent's output tokens on a reference-coding task at the same 16/16 solve rate, plus "roughly 5x in everyday work" from field reports. The README does not state, and this doc did not independently verify, the more specific claim (from the social post that queued this entry) that the gain holds only on libraries the agent hasn't seen before and disappears on popular/well-known code. A separate, optional small model, **XERJ Query-1** (off by default), answers questions by running a short program over facts the user wrote into the store rather than retrieving-then-generating; on the project's own 160-question test it reports 1 wrong answer (124 right, 35 declined) vs. 9–15 for "RAG with Opus 5.5," at a self-reported $42 vs. $13,400–$694,000 per million questions. Query-1's training/eval data are not public, so this number can't be independently replicated.

### Adoption Considerations

**Strengths**: Elasticsearch-compatible API lowers migration friction for teams already on that query shape; single binary, no JVM; default embedder is lexical/offline, with an opt-in ~90MB neural embedder; explicit `xerj init` path for Claude Code and Cursor.

**Risks**: very young (repo created 2026-06-30) for an 18.8k-star project — the Trendshift badges corroborate a real, fast-growing GitHub trend rather than confirming the count is organic, but adoption/maturity signals (issue backlog, release cadence) are worth checking independently; XERJ Query-1's accuracy claim can't be replicated without its training/eval data; the "no gain on popular code" nuance is unverified against the README.

Cross-ref: [zg / zvec-grep](#zg--zvec-grep-zvec-ai) above — the other hybrid lexical+vector search tool with a first-party Claude Code installer; [CC-memory-tooling-landscape.md](CC-memory-tooling-landscape.md) — for XERJ's agent-memory recipe specifically

---

## jevgrep (dzhng)

**Repo**: [dzhng/jevgrep][jevgrep] | **Stars**: 1,848 | **License**: MIT (confirmed against
`LICENSE`) | **Version**: latest tag v0.7.0, latest GitHub Release v0.6.0 (provider selection requires 0.3.0+), pushed 2026-09-29
(`gh api`, 2026-09-30)

A CLI (`jg`) that answers a natural-language question about a repository ("Where is
authentication checked before a request reaches a handler?") with a compact file list, selected
source excerpts with line references, and declaration/call locations — a starting point for a
coding agent, not a generated answer. It uses [Jev][typesafe-jev-code] to judge relevance across
folders, files, and declarations; a bundled agent skill (`jg skill`, via the
[Vercel `skills` CLI][skills-cli]) teaches Claude Code, Codex, and OpenCode to call it. Declaration
parsing covers Python, TypeScript/JavaScript, Go, and Rust; other text falls back to a generic
mode. Requires a key for Vercel AI Gateway, TypeSafe, OpenRouter, OpenCode Zen, or a custom
TypeSafe-compatible endpoint.

### What jevgrep measured

Its own ten-task SWE-bench comparison (frozen package, exact public skill): both with and without
jevgrep, **8 of 10 tasks solved**; total agent cost fell from $7.62 to $5.44, a measured 28.6%
reduction (rounded to "~30%" in its README banner), excluding Jev's own cost. A later rerun that
*includes* Jev's cost reports 25.8% lower total cost at the same 8/10 solve rate. These are the
project's own single-run measurements, not an independent replication, and the README says so:
"single-run observations do not establish statistical equivalence or a speed improvement."

### Adoption Considerations

**Strengths**: ships an installable agent skill rather than requiring hand-written prompting
instructions; supports five provider backends, so it is not locked to a single paid API; default
filtering excludes hidden/dependency/binary/credential files from what it sends to Jev.

**Risks**: still young (repo created 2026-09-26); the only reported comparison is a 10-task SWE-bench
sample; depends on Jev (or an alternative provider) for every relevance judgment, so an outage or
missing key blocks the search rather than degrading gracefully.

Cross-ref: [system-1-decision-models-landscape.md § Tools built on Jev][decision-models-landscape-code]

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

## Floorplan (haydenschmitty)

**Repo**: [haydenschmitty/floorplan][floorplan] | **Stars**: 3,682★/299 forks (`gh api`, 2026-11-12) | **License**: MIT | **Version**: 0.7.3

A different category from the graph/LSP/search/packer tools above: Floorplan asks Claude Code or Codex to read a codebase and draw an **interactive, zoomable visual map** — parts, files and web requests, each given a plain-English name, with every connection shown, including requests that cross from a frontend repo to a backend repo. It runs locally, updates incrementally (re-reading only what changed), and exports a map as one self-contained HTML file. Two features go beyond mapping: a **Health check** that flags classic AI-assisted-app mistakes (secrets committed to code, open Supabase tables, permissive Firebase rules, fakeable Stripe webhooks, sign-in-less endpoints) with a ready-to-paste fix per finding, and a **Recent work** view that highlights exactly which map nodes the agent's last changes touched and why. It can also draw a **blueprint** — the same map shape, dashed to mark it as a plan — from a PRD or spec for work not yet built.

The project's own README distinguishes itself from two similar tools it names directly: [Archify][archify] (any of 10 diagram types, including non-code processes, for Claude Code/Codex/Cursor/OpenCode) and [Understand Anything][understand-anything] (a full code knowledge graph down to functions, for Claude Code/Codex/Cursor/Copilot/Gemini CLI) — Floorplan's own framing is "understand and check an app you own" versus "draw a diagram" (Archify) or "study a large codebase function by function" (Understand Anything); it positions itself as complementary to both rather than a replacement. **Caveat**: at two weeks old (created 2026-10-27) this is an early-stage project with no independent review found.

## Cross-References

- [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) — full cross-tool comparison + the rest of the CC tooling landscape
- [repo-to-docs-tools-landscape.md](../non-cc/knowledge-management/repo-to-docs-tools-landscape.md) — repo-to-docs generators
- [code-review-products-landscape.md](../non-cc/infrastructure/code-review-products-landscape.md) — standalone SaaS PR-review products (CodeRabbit, Greptile, Ellipsis, …) moved out of this doc per #326

[graphify]: https://github.com/safishamsi/graphify
[axiomcode]: https://github.com/AxiomCodeAI/axiomcodegraph
[graphicle]: https://github.com/Graphicle-AI/graphicle
[xerj]: https://github.com/xerj-org/xerj
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
[tgrep]: https://github.com/microsoft/tgrep
[zvec-grep]: https://github.com/zvec-ai/zvec-grep
[zvec]: https://github.com/alibaba/zvec
[jevgrep]: https://github.com/dzhng/jevgrep
[typesafe-jev-code]: https://docs.typesafe.ai/
[skills-cli]: https://github.com/vercel-labs/skills
[decision-models-landscape-code]: ../non-cc/reference/system-1-decision-models-landscape.md#tools-built-on-jev
[floorplan]: https://github.com/haydenschmitty/floorplan
[archify]: https://github.com/tt-a1i/archify
[understand-anything]: https://github.com/Egonex-AI/Understand-Anything

## Sources

Each tool cites its repository/docs inline via the reference-style link definitions above (Graphify, AxiomCode Graph, Graphicle, Code-Review-Graph, Qodo, codebase-memory-mcp, Serena, ast-grep MCP, tgrep, zg (zvec-grep), XERJ, jevgrep, Repomix, code2prompt, Floorplan).
