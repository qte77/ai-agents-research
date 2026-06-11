---
title: CC Community Tooling Landscape
purpose: Survey of community developer tools that integrate with or enhance Claude Code — context compression, meta-prompting, spec-driven development, agent frameworks, file read deduplication, persistent memory, knowledge graphs, code analysis.
category: landscape
status: research
platform_scope: [claude-code, cursor, codex, gemini-cli, opencode, windsurf, zed, antigravity]
created: 2026-03-13
updated: 2026-06-10
validated_links: 2026-06-10
---

**Status**: Research (informational)

## RTK (Rust Token Killer)

Rust-based CLI proxy that intercepts shell command outputs and compresses them before they enter the LLM context window. Integrates transparently with Claude Code via hooks ([rtk-repo][rtk-repo]).

- **Stack**: Rust, zero dependencies, <10ms overhead per command
- **Integration**: `rtk init --global` rewrites commands via CC hooks — `git status` becomes `rtk git status` transparently
- **Lossless on failure**: `tee` mode saves full unfiltered output to `~/.local/share/rtk/tee/`
- **Analytics**: `rtk gain` shows token savings, `rtk discover` finds missed opportunities

### Independent Benchmark (2026-03-26, v0.33.1)

5 repos, 9 categories, 2,100 measurements. Deterministic: 699/700 ops <10-byte variance. Issue: [rtk-839][rtk-839].

| Category | Claimed | Measured | Notes |
|---|---|---|---|
| `ls` | -80% | **-72%** | Effective on verbose/large repos |
| `git log` | -80% | **-98%** | Truncation, not compression |
| `git status` | -80% | **-46%** | Verbose only; `--porcelain` = 0% |
| `cat`, `grep`, `pytest`, `ruff` | -70–90% | **0%** | Byte-identical passthrough |

**Verdict**: Effective on `ls`/`git log`/`docker ps`; zero on `cat`/`grep`/`pytest`/`ruff`. The 80% headline does not hold under independent testing — real savings ~22% in sandboxed CC, ~72% unsandboxed (inflated by `git log` truncation).

**Recommendation**: Keep installed — free savings on verbose output with negligible overhead. Set expectations accordingly.

Cross-ref: [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md); [CC-community-skills-landscape.md](CC-community-skills-landscape.md) — caveman (output-side compression); CodeBurn / ccusage / Claude-Code-Usage-Monitor below (measurement layer)

---

## GSD (Get Shit Done)

Meta-prompting, context engineering, and spec-driven development system for AI coding agents. Sits on top of CC (and 7 other runtimes) to manage context rot and orchestrate subagents ([gsd-repo][gsd-repo]).

- **Stack**: Node.js >= 20, zero production deps, npm package `get-shit-done-cc` ([npm][gsd-npm])
- **Stars**: 44.5K | **License**: MIT | **Version**: 1.30.0 (2026-03-27)
- **Runtimes**: Claude Code, OpenCode, Gemini CLI, Codex, Copilot, Cursor, Windsurf, Antigravity

### Architecture

18 specialized subagent prompts (planner, executor, verifier, debugger, UI auditor, assumptions analyzer, etc.) orchestrated via structured workflows. CC integration via hooks:

| Hook | Purpose |
|---|---|
| `gsd-context-monitor.js` | Track context window fill level |
| `gsd-prompt-guard.js` | Validate prompt quality before execution |
| `gsd-workflow-guard.js` | Enforce workflow phase transitions |
| `gsd-statusline.js` | Status display |
| `gsd-check-update.js` | Version check |

### Key Differentiators

- **Context engineering**: Manages context rot during long sessions — the core problem GSD solves
- **Spec-driven**: Structured specs → planning → execution → verification loop
- **Multi-runtime**: Broadest runtime support (8 agents) in the space
- **Headless SDK**: `gsd-sdk` (v1.30.0) enables autonomous/CI execution

### Known Gaps (77 open issues)

| Issue | Severity |
|---|---|
| [#1451][gsd-1451] Worktree merge overwrites earlier worktrees | Bug — data loss |
| [#1457][gsd-1457] Verifier accepts circular tests and `it.skip` | Verification integrity |
| [#1459][gsd-1459] Phases marked Complete without real verification | Verification integrity |
| [#1461][gsd-1461] settings.json overwritten on update | Config preservation |
| [#1431][gsd-1431] Agents present unvalidated assumptions as decisions | Reliability |
| [#1466][gsd-1466] Hardcoded `--base main` in ship.md | Portability |

### Adoption Considerations

**Strengths**: Broadest multi-runtime support, active development (5 releases in 10 days), large community (44.5K stars), pragmatic philosophy (anti-enterprise-ceremony).

**Risks**: Verification integrity issues undermine core promise ([#1457][gsd-1457], [#1459][gsd-1459]). Agent hallucination/assumption problem ([#1431][gsd-1431]). SDK is early-stage. Update process erodes user config ([#1461][gsd-1461]).

Cross-ref: [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md), [CC-community-skills-landscape.md](CC-community-skills-landscape.md)

---

## everything-claude-code

**Repo**: [affaan-m/everything-claude-code][ecc] | **Stars**: 50K+ | **License**: MIT

Comprehensive agent, skill, and workflow framework for Claude Code. Won the Anthropic Build with Claude hackathon (June 2025).

### What It Provides

| Category | Count | Examples |
|----------|-------|---------|
| **Agents** | 36 | Code reviewer, debugger, data scientist, security auditor, DevOps, PM |
| **Skills** | 156 | Code generation, testing, documentation, refactoring, deployment |
| **Command shims** | 72 | Pre-built slash commands wrapping common workflows |
| **Hooks** | Architecture | PreToolUse/PostToolUse pipeline for quality gates and automation |

### Architecture

Layered system: skills compose into agents, agents are dispatched by command shims, hooks enforce quality gates across the pipeline. Designed for drop-in adoption — install the plugin and skills/agents become available immediately.

### Adoption Considerations

**Strengths**:

- Broadest single-package coverage of CC extensibility (agents + skills + hooks + shims)
- Active community (50K+ stars, hackathon-validated)
- MIT licensed, installable as plugin

**Risks**:

- Large surface area — may conflict with project-specific skills or hooks
- Shim commands may shadow custom slash commands
- Quality varies across 156 skills — not all independently validated

---

## Boucle Read-Once Framework

**Repo**: [Bande-a-Bonnot/Boucle-framework][boucle] | **License**: MIT

PreToolUse hook that deduplicates file reads within a session. When Claude requests a file already read in the current context, the hook blocks the redundant read and returns a cache notice instead.

### How It Works

1. **PreToolUse hook** intercepts `Read` tool calls
2. Checks if file path was already read in the current session
3. If cached: blocks the read, returns "file already in context" (~2K tokens saved per blocked re-read)
4. **PostCompact integration**: clears the cache after `/compact` (compacted context no longer contains the file contents)

### Token Savings

~40% token reduction on file-read-heavy sessions. Savings depend on how often Claude re-reads files — common in long sessions with context compaction cycles.

### Configuration

Default mode is **warn** (logs but does not block) to avoid conflicts with the Edit tool, which requires a preceding Read. Switch to **block** mode after validating it doesn't break your edit workflow.

Cross-ref: [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md) — PreToolUse hook mechanism Boucle relies on

---

## OpenHarness (HKUDS)

**Repo**: [HKUDS/OpenHarness][openharness] | **Stars**: 3.3K | **License**: MIT | **Version**: 0.1.0 (2026-04-01)

Open-source Python agent harness framework — infrastructure plumbing between LLMs and tools. Implements 10 core subsystems compatible with CC conventions (markdown skills, plugin architecture, CLAUDE.md, hooks, MCP).

### Core Subsystems

| Subsystem | Purpose | CC Equivalent |
|-----------|---------|---------------|
| **Engine** | Streaming tool-call loop with retry | CC agent loop |
| **Tools** | 43+ integrated tools (file I/O, shell, web, MCP) | CC built-in tools |
| **Skills** | On-demand markdown knowledge loading | `.claude/skills/` |
| **Plugins** | Extensions for commands, hooks, agents | `.claude-plugin/` |
| **Permissions** | Multi-level safety with path rules | `settings.json` permissions |
| **Hooks** | PreToolUse/PostToolUse lifecycle events | CC hooks system |
| **Commands** | 54 built-in directives (/commit, /plan, etc.) | CC slash commands |
| **Memory** | Persistent cross-session knowledge | CC memory system |
| **Coordinator** | Subagent spawning and team management | CC agent teams |
| **UI** | React (Ink) TUI + backend protocol | CC terminal UI |

### Multi-Provider Support

- **Anthropic format** (default): Claude, Moonshot/Kimi, Vertex, Bedrock
- **OpenAI format** (`--api-format openai`): OpenAI, DeepSeek, DashScope, GitHub Models, Groq, Ollama

### Adoption Considerations

**Strengths**: Most complete open harness (10 subsystems, 43 tools, 114 tests, 6 E2E suites). CC-convention compatible — skills, plugins, CLAUDE.md, hooks all work. Multi-provider. MIT licensed.

**Risks**: Early stage (v0.1.0, 3.3K stars). Not a CC replacement — lacks CC's model quality, context window management, and Anthropic infrastructure. Python-only (CC is TypeScript/Node).

---

## ByteRover CLI (campfirein)

**Repo**: [campfirein/byterover-cli][byterover] | **Stars**: 4.1K | **License**: Elastic License 2.0 | **Paper**: [arXiv:2604.01599][byterover-paper]

Portable memory layer for autonomous coding agents. Persistent hierarchical context trees (Domain→Topic→Subtopic→Entry) with cloud sync and sub-100ms retrieval without vector databases.

### Architecture

- **Context Tree**: LLM-curated hierarchical knowledge storage in human-readable markdown
- **Adaptive Knowledge Lifecycle**: Importance scoring + recency decay
- **5-tier progressive retrieval**: Escalates to LLM reasoning only for novel queries
- **MCP integration**: `brv mcp` starts an MCP server for CC to access memory natively

### CC Integration

ByteRover integrates with Claude Code via MCP protocol. Run `brv mcp` to expose the memory layer as an MCP server, giving CC access to persistent cross-session knowledge, semantic search, and context tree operations.

### Adoption Considerations

**Strengths**: Research-backed ([arXiv:2604.01599][byterover-paper] — SOTA on LoCoMo benchmark), 20+ LLM provider support, cloud sync with SOC 2 Type II, active development (48 releases, 2,391 commits).

**Risks**: Elastic License 2.0 (not OSS — requires commercial agreement for production). Cloud dependency for sync features. Overlaps with CC's built-in memory system (`~/.claude/memory/`). Standalone daemon CLI — install alongside CC via MCP, not embeddable in plugins.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## Claude-Mem (thedotmack / Alex Newman)

**Repo**: [thedotmack/claude-mem][claude-mem] | **Stars**: 45.2K | **License**: AGPL-3.0 | **Version**: 6.5.0

Persistent memory compression system for Claude Code. Automatically captures everything Claude does during coding sessions, compresses it with AI, and injects relevant context back into future sessions for continuity.

### Architecture

| Component | Purpose |
|-----------|---------|
| **Lifecycle Hooks** (5) | SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd |
| **Worker Service** | Express API on port 37777, managed by Bun runtime, includes web viewer UI |
| **SQLite Storage** | Sessions, observations, summaries with FTS5 full-text search |
| **Chroma Vector DB** | Hybrid semantic/keyword search |
| **MCP Tools** | 3-layer progressive disclosure workflow |

### MCP Search Pattern (Token-Efficient)

| Tool | Purpose | Cost |
|------|---------|------|
| `search` | Compact index retrieval with IDs | ~50–100 tokens/result |
| `timeline` | Chronological context around observations | moderate |
| `get_observations` | Full detail for filtered IDs | ~500–1,000 tokens/result |

Progressive disclosure: start with index → assess via timeline → fetch full detail only for relevant matches. Estimated **10x token savings** over naive retrieval.

### Installation

```bash
npx claude-mem install                          # CLI install
/plugin marketplace add thedotmack/claude-mem   # marketplace install
```

**Note**: npm global install provides only the SDK library; proper plugin registration requires `npx claude-mem install`.

### Key Features

- AI-compressed semantic summaries of session activity
- Automatic context injection into new sessions
- `<private>` tags for content exclusion
- Citation system referencing past observations by ID
- Web viewer UI at localhost:37777
- Notification integrations (Telegram, Discord, Slack)

### Live Observer Architecture

A dedicated observer AI watches each session in real-time, generating searchable observations with before-and-after context — capturing causality and decision chains, not just snapshots. Observations are auto-categorized by type (decisions, bugfixes, features, discoveries) and queryable by file path or semantic concept (e.g., "decisions about token refresh").

### RAD Protocol (Coming Soon)

**Real-Time Agent Data** — an open protocol standardizing how AI agents capture and retrieve working memory. Positioned as a counterpart to RAG (Retrieval Augmented Generation). Hook-based architecture for temporal awareness.

### Adoption Considerations

**Strengths**: Largest community memory solution (45.2K stars), progressive disclosure saves tokens, hybrid search (FTS5 + vector), multi-platform (CC + Gemini CLI), web UI for browsing history, [dedicated docs site][claude-mem-docs].

**Risks**: AGPL-3.0 (copyleft — commercial use requires compliance). Ragtime subdirectory under separate PolyForm Noncommercial License. Heavy dependencies (Bun + uv + Chroma). Overlaps with CC's built-in memory system and ByteRover.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## CC Switch (farion1231)

**Repo**: [farion1231/cc-switch][cc-switch] | **Stars**: 38.9K | **License**: TBD | **Commits**: 1,376

Cross-platform desktop app managing 5 AI CLI tools: Claude Code, Codex, Gemini CLI, OpenCode, and OpenClaw. Consolidates provider management, eliminating manual config file editing.

### Features

| Feature | Description |
|---------|-------------|
| **Provider switching** | One-click switching between 50+ built-in API provider presets, no config file editing |
| **MCP/Prompts/Skills** | Unified management across all 5 tools with bidirectional sync |
| **System tray** | Quick-access provider switching without opening the app |
| **Cloud sync** | Dropbox, OneDrive, iCloud, WebDAV support |
| **Usage tracking** | Cost monitoring and request logging across tools |
| **Session browser** | Search conversation history across all supported apps |
| **Deep links** | `ccswitch://` protocol for config imports |

### Installation

Available for Windows (MSI/portable), macOS (DMG/Homebrew), and Linux (deb/rpm/AppImage). Multi-language: English, 中文, 日本語.

### Key Differentiator

Only tool that manages provider configuration **across multiple AI CLIs** from a single GUI. Where RTK optimizes output and GSD orchestrates workflows, CC Switch operates at the **infrastructure layer** — which provider, which model, which API key, across which tools.

Cross-ref: [CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md) — CC's native provider config

---

## opensrc (vercel-labs)

**Repo**: [vercel-labs/opensrc][opensrc] | **Stars**: 1.5K | **License**: Apache-2.0

Fetches npm package **source code** (not just type definitions) to give AI coding agents deeper implementation context. Solves the problem of agents only seeing type signatures without understanding internal behavior.

### How It Works

1. Queries npm registry for package repository URLs
2. Auto-detects installed versions from lockfiles (package-lock.json, pnpm-lock.yaml, yarn.lock)
3. Clones repositories at matching git tags
4. Stores sources in `opensrc/<package-name>/`
5. Optionally modifies `.gitignore`, `tsconfig.json`, `AGENTS.md`

### CLI Usage

```bash
npx opensrc zod              # fetch version matching lockfile
npx opensrc zod@3.22.0       # exact version
npx opensrc facebook/react   # GitHub repo
npx opensrc list             # show fetched sources
npx opensrc remove zod       # clean up
```

### Output Structure

```text
opensrc/
├── settings.json       # user preferences
├── sources.json        # package index with versions/paths
└── zod/
    └── src/            # actual source code
```

### Key Differentiator

Complements the context management stack from a different angle: RTK **reduces** noise, Boucle **deduplicates** reads, dispatch **multiplies** context, opensrc **deepens** context with actual implementations. TypeScript/npm ecosystem specific.

---

## awesome-design-md (VoltAgent)

**Repo**: [VoltAgent/awesome-design-md][awesome-design-md] | **Stars**: 21,849 | **License**: MIT

Curated collection of **58 DESIGN.md files** capturing design systems from popular websites in LLM-consumable Markdown. Each file includes color palettes, typography rules, component styles, layout principles, responsive behavior, and an explicit **Agent Prompt Guide** section. Format designed for Google Stitch and general-purpose coding agents.

### DESIGN.md Format (9 Sections)

1. Visual Theme & Atmosphere — mood, density, design philosophy
2. Color Palette & Roles — semantic names with hex codes (40+ per file)
3. Typography Rules — font families, 16-role hierarchy with px/weight/line-height
4. Component Stylings — buttons (5 variants), cards, inputs, navigation
5. Layout Principles — spacing scale (8px base), grid widths, border-radius (7 levels)
6. Depth & Elevation — 5-level system with exact CSS shadow values
7. Do's and Don'ts — design guardrails and anti-patterns
8. Responsive Behavior — 5 breakpoints, collapsing strategies, touch targets (44x44px min)
9. Agent Prompt Guide — color reference table, 4 example component prompts, 7 iteration principles

### 58 Design Systems (7 Categories)

AI & ML (12): Claude, Mistral AI, Replicate, xAI, ElevenLabs. Developer Tools (14): Cursor, Linear, PostHog, Sentry, Vercel. Infrastructure (6): Stripe, MongoDB, HashiCorp. Design & Productivity (10): Figma, Notion, Framer, Miro. Fintech (4): Coinbase, Revolut, Wise. Enterprise (7): Airbnb, Apple, IBM, SpaceX, Spotify. Car Brands (5): BMW, Ferrari, Tesla.

### Key Differentiator

A new artifact type: design systems encoded for LLM consumption rather than human developers or design tool plugins. The Agent Prompt Guide section is a novel contribution — ready-to-use component prompts with iteration instructions. Files capture publicly visible CSS values, not proprietary design tokens. 21.8K stars in 6 days (riding Google Stitch launch wave).

**Who is VoltAgent**: Open-source [TypeScript AI Agent Framework](https://voltagent.dev) for enterprise multi-agent systems (tool calling, persistent memory, supervisor orchestration, 40+ integrations). The awesome-design-md repo is a community/marketing project.

**Gap**: No public tooling for generating DESIGN.md from arbitrary sites — extraction appears manual/internal.

Cross-ref: [CC-domain-claudemd-showcase.md](CC-domain-claudemd-showcase.md) — CLAUDE.md as domain controller, analogous pattern

---

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

## MemPalace (milla-jovovich)

**Repo**: [milla-jovovich/mempalace][mempalace] | **Stars**: 33.6K | **License**: MIT | **Version**: 3.0.0

Local-first AI memory system storing conversation histories verbatim using a spatial "palace" metaphor. Achieved 96.6% R@5 on [LongMemEval benchmark][longmemeval] — the highest published result — without cloud dependencies.

### Palace Architecture

| Layer | Metaphor | Purpose |
|-------|----------|---------|
| **Wings** | Projects or people | Top-level partitioning |
| **Rooms** | Topic categories | Within-wing organization |
| **Halls** | Memory types | Cross-wing shared categories (facts, events, discoveries) |
| **Closets** | Summaries | Pointers to original content |
| **Drawers** | Verbatim files | Raw original data |
| **Tunnels** | Cross-references | Links between rooms across wings |

34% retrieval improvement over unstructured search from this hierarchical organization.

### Memory Stack

| Layer | Content | Size | Timing |
|-------|---------|------|--------|
| L0 | Identity/system prompt | ~50 tokens | Always loaded |
| L1 | Critical facts | ~120 tokens (AAAK) | Always loaded |
| L2 | Room recall (recent sessions) | On demand | When topic emerges |
| L3 | Deep semantic search | On demand | When explicitly queried |

### CC Integration

```bash
claude plugin marketplace add milla-jovovich/mempalace   # marketplace install
claude mcp add mempalace -- python -m mempalace.mcp_server  # MCP install
```

19 MCP tools for search and memory operations. Also supports ChatGPT, Cursor, Gemini, and local models (Ollama, Mistral).

### Adoption Considerations

**Strengths**: Highest published LongMemEval score (96.6% raw mode, reproducible via `/benchmarks`). Free and fully local. ChromaDB + SQLite knowledge graph. Specialist agent support with per-agent memory wings.

**Risks**: AAAK compression is lossy and regresses to 84.2% ([README candid note][mempalace]). Overlaps with CC's built-in memory, ByteRover, and Claude-Mem. ChromaDB dependency adds install complexity.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

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

## codebase-memory-mcp (DeusData)

**Repo**: [DeusData/codebase-memory-mcp][codebase-memory-mcp] | **Stars**: 3.2K | **License**: MIT | **Version**: v0.7.0 (2026-05-30)

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

**Use when**: you want a deterministic, whole-repo snapshot for a one-off question, an agent's first turn, or a non-CC LLM — no server to run. **Prefer the graph/LSP tools above** (codebase-memory-mcp, graphify, Serena) for repeated, large-codebase work, where re-sending a packed corpus every turn would blow the context budget. Repomix's `--compress` and these packers are complementary to RTK (output-side) and Boucle (read dedup), both above.

---

## CodeBurn (AgentSeal)

**Repo**: [getagentseal/codeburn][codeburn] | **Stars**: 4K | **License**: MIT | **Latest**: Menubar v0.9.0 (2026-04-25) | **Stack**: TypeScript, Node.js 20+

Local-first TUI dashboard that tracks AI coding token usage and cost across multiple coding agents. Reads session data directly from disk — no API keys, no proxy ([README][codeburn]).

### Supported Agents

Per the [README][codeburn]: Claude Code, Claude Desktop, Codex, Cursor, cursor-agent, OpenCode, Pi, OMP (Oh My Pi), GitHub Copilot.

### Data Sources (Read-Only, On-Disk)

| Agent | Path |
|---|---|
| Claude | `~/.claude/projects/` (JSONL) |
| Cursor | `~/Library/Application Support/Cursor/` (SQLite, macOS) |
| Codex | `~/.codex/sessions/` (JSONL with timestamped token events) |
| OpenCode | `~/.local/share/opencode/` (SQLite) |
| GitHub Copilot | `~/.copilot/session-state/` |

### Features

- **TUI dashboard** with gradient charts and responsive panels
- **13 task categories** classified from tool patterns: Coding, Debugging, Feature Dev, Refactoring, Testing, Exploration, Planning, Delegation, Git Ops, Build/Deploy, Brainstorming, Conversation, General
- **[`codeburn optimize`](https://github.com/getagentseal/codeburn#optimize)** — surfaces nine waste patterns (files re-read across sessions, low Read:Edit ratio, unused MCP servers, ghost agents/skills/slash commands, bloated `CLAUDE.md`, wasted bash output, cache-creation overhead, context-heavy and low-worth sessions) with copy-paste token/$ fixes ranked into an A–F health grade
- **`codeburn compare`** — side-by-side model performance metrics
- **`codeburn report -p 30days`** — rolling-window analysis
- **`codeburn export`** — CSV/JSON across multiple time periods
- **Subscription tracking** — Claude Pro/Max, Cursor Pro
- **Currency conversion** — 162 ISO 4217 codes
- **Pricing data** sourced from LiteLLM with 24h cached refresh; hardcoded fallbacks for Claude and GPT-5 to prevent fuzzy-match errors

### Platform Support

macOS (native menubar app via `codeburn menubar`), Linux (CLI), Windows (CLI; Cursor support requires `better-sqlite3`).

### Installation

```bash
npm install -g codeburn
# or run without installing:
npx codeburn
```

### Key Differentiator

Where RTK reduces tokens *entering* context and caveman compresses tokens *leaving* the assistant, **CodeBurn observes** what was actually spent — across agents, models, and projects. Complementary to both: optimization needs measurement. Local-first (no API keys, no telemetry) makes it usable in air-gapped or compliance-sensitive environments.

Cross-ref: [CC-community-skills-landscape.md](CC-community-skills-landscape.md) — caveman (output compression skill); [CC-session-cost-analysis.md](../cc-native/sessions/CC-session-cost-analysis.md) — CC's native session-cost extraction via JSONL/jq

---

## ccusage (ryoppippi)

**Repo**: [ryoppippi/ccusage][ccusage] | **Stars**: 13.4K | **License**: MIT | **Version**: v18.0.11 (2026-04-19) | **Stack**: TypeScript

CLI tool that analyzes Claude Code / Codex CLI usage from local JSONL files. Established reference tool in the CC usage-tracking space — predates and is broader-adopted than CodeBurn ([README][ccusage]).

### Reports

- **Daily** — token usage and costs aggregated by date
- **Monthly** — long-horizon aggregation
- **Session** — usage grouped by conversation
- **Blocks** — 5-hour billing windows (matches Anthropic's plan limits)
- **Statusline** (Beta) — integration for hooks

### Capabilities

Per the [README][ccusage]:

- **Model tracking** — per-model breakdown with `--breakdown`
- **Cache token support** — tracks cache creation and cache read tokens separately (codeburn does not split these)
- **Offline mode** — `--offline` uses pre-cached pricing (no network)
- **MCP integration** — built-in MCP server for in-session queries
- **Multi-instance** — group usage by project
- **JSON export**

### Installation

```bash
npx ccusage@latest          # recommended — always latest
bunx ccusage
pnpm dlx ccusage
```

Reads `~/.claude/projects/` JSONL by default; data path is configurable.

### Key Differentiator

Where CodeBurn is **multi-agent** (Claude/Codex/Cursor/OpenCode/Copilot in one TUI), ccusage is **CC/Codex-focused** with deeper CC-specific features (cache token split, MCP server, statusline hook). The two are complementary, not redundant: ccusage for CC-deep analysis and in-session queries via MCP; CodeBurn for cross-agent comparison.

Cross-ref: [CC-session-cost-analysis.md](../cc-native/sessions/CC-session-cost-analysis.md) — manual JSONL/jq extraction patterns ccusage automates; [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md) — statusline hook integration point

---

## Claude-Code-Usage-Monitor (Maciek-roboblog)

**Repo**: [Maciek-roboblog/Claude-Code-Usage-Monitor][claude-monitor] | **Stars**: 7.8K | **License**: MIT | **Version**: v3.1.0 | **Stack**: Python 3.9+

Real-time terminal monitor for Claude Code with **predictions and warnings**, distinguishing it from after-the-fact analyzers like ccusage / CodeBurn ([README][claude-monitor]).

### Plan Support

Per the [README][claude-monitor]:

| Plan | Token limit |
|---|---|
| Pro | ~19,000 |
| Max5 | ~88,000 |
| Max20 | ~220,000 |
| **Custom** | P90 auto-detection over recent session blocks |

The Custom plan analyzes recent session blocks and computes a personalized 90th-percentile limit — adapts to actual usage patterns without manual configuration.

### Views

- **Realtime** — live progress bars + burn rate (default)
- **Daily** — aggregated table
- **Monthly** — long-trend analysis

### Methodology

P90 percentile analysis across all available session blocks; multi-session burn-rate analytics; intelligent session-limit detection. Stack: `pytz`, `rich`, `pydantic`, `numpy`, `pyyaml`, `sentry-sdk`.

### Installation

```bash
uv tool install claude-monitor       # recommended
pip install claude-monitor
```

### Key Differentiator

Only tool in this category that does **prediction** (not just retrospective measurement). ccusage and CodeBurn answer "what did I spend?"; claude-monitor answers "will I exhaust my window?" Useful pairing: claude-monitor for live discipline, ccusage for historical trend, CodeBurn for cross-agent comparison.

Cross-ref: [CC-session-cost-analysis.md](../cc-native/sessions/CC-session-cost-analysis.md) — Anthropic plan limits and 5-hour windows

---

## Comparison

| Tool | Layer | CC Integration | Approach | Maturity |
|---|---|---|---|---|
| **RTK** | Tool output compression | Hooks (transparent rewrite) | Reduce input noise | Stable (v0.33.1) |
| **GSD** | Meta-prompting + orchestration | Hooks + slash commands | Structured workflows, subagents | Active (v1.30.0, rapid iteration) |
| **everything-claude-code** | Agent/skill framework | Plugin (drop-in) | Bundled agents, skills, shims | Active (50K+ stars) |
| **Boucle** | File read deduplication | PreToolUse hook | Prevent redundant reads | Early (MIT) |
| **OpenHarness** | Full agent harness | CC-convention compatible | Open harness framework (10 subsystems) | Early (v0.1.0, 3.3K stars) |
| **ByteRover** | Persistent memory | MCP server | Hierarchical context trees, cloud sync | Active (4.1K stars, 48 releases) |
| **Claude-Mem** | Persistent memory + compression | Hooks + MCP + plugin | AI-compressed observations, progressive search | Active (45.2K stars, v6.5.0) |
| **CC Switch** | Multi-CLI provider management | Desktop app (GUI) | Unified config across 5 AI CLIs | Active (38.9K stars, 1,376 commits) |
| **opensrc** | Source code enrichment | CLI (npx) | Fetch npm package sources for agent context | Early (1.5K stars) |
| **awesome-design-md** | Agent-consumable design systems | Markdown files (drop-in) | 58 DESIGN.md files for UI generation | Viral (21.8K stars in 6 days) |
| **Graphify** | Code→knowledge graph | Hooks + slash commands + MCP + CLAUDE.md | Semantic knowledge graphs from repos | Active (16.5K stars) |
| **MemPalace** | Persistent memory | MCP server + plugin marketplace | Verbatim palace-metaphor memory | Active (33.6K stars, v3.0.0) |
| **Code-Review-Graph** | Structural code analysis | MCP server (22 tools, auto-config) | AST-based blast radius for reviews | Active (7.1K stars) |
| **codebase-memory-mcp** | Code→graph + LSP + embeddings | MCP (14 tools) + PreToolUse hook + auto-config | Single-binary knowledge graph | Active (3.2K stars, v0.7.0) |
| **Serena** | Semantic code (live LSP) | MCP server (20+ tools) | Symbol-level retrieve/edit/refactor | Active (25.2K stars, v1.5.3) |
| **ast-grep MCP** | Structural search/rewrite | MCP server (4 tools) | tree-sitter AST patterns | Experimental (419 stars, no release) |
| **Repomix** | Repo→single-file context export | MCP server + official CC plugins | tree-sitter compression + token counts | Stable (26.2K stars, v1.14.1) |
| **code2prompt** | Repo→single-prompt context export | MCP server + CLI | Templated export + token counts | Stable (7.4K stars, v4.2.0) |
| **CodeBurn** | Token-usage observability (cross-agent) | CLI (reads on-disk session data) | Cross-agent dashboard, 13 task categories, optimize/compare | Active (4K stars) |
| **ccusage** | Token-usage observability (CC/Codex) | CLI + MCP server + statusline | JSONL analyzer, cache-token split, offline mode | Stable (13.4K stars, v18.0.11) |
| **Claude-Code-Usage-Monitor** | Predictive usage monitoring | Real-time TUI | P90-based limit prediction, burn-rate analytics, plan-aware | Active (7.8K stars, v3.1.0) |

All twenty-one address different layers of the agent stack — complementary, not competing. The five code-analysis tools (graphify, Code-Review-Graph, codebase-memory-mcp, Serena, ast-grep MCP) split along precompute-a-graph vs. live-LSP vs. on-demand-structural-search; the two repo packers (Repomix, code2prompt) are one-shot context export rather than a live server.

Cross-ref: [CC-extended-context-analysis.md](../cc-native/context-memory/CC-extended-context-analysis.md) — CC's built-in context compaction

## Sources

| Source | Content |
|---|---|
| [RTK repository][rtk-repo] | CLI proxy, hook integration, benchmarks |
| [rtk-ai/rtk#839][rtk-839] | Independent benchmark findings |
| [GSD repository][gsd-repo] | Meta-prompting + context engineering framework |
| [everything-claude-code][ecc] | Agent/skill/hook framework (50K+ stars) |
| [Boucle-framework][boucle] | Read-once file deduplication hook |
| [OpenHarness][openharness] | Open-source agent harness framework (10 subsystems, 43 tools) |
| [ByteRover CLI][byterover] | Portable memory layer for coding agents (MCP, context trees) |
| [ByteRover paper][byterover-paper] | arXiv:2604.01599 — agent-native memory via hierarchical context |
| [Claude-Mem][claude-mem] | Persistent memory compression system (45.2K stars) |
| [CC Switch][cc-switch] | Cross-platform multi-CLI provider management (38.9K stars) |
| [opensrc][opensrc] | npm package source fetcher for agent context (1.5K stars) |
| [awesome-design-md][awesome-design-md] | 58 DESIGN.md files for agent-consumable UI generation (21.8K stars) |
| [Graphify][graphify] | Code→knowledge graph via slash commands, hooks, MCP (16.5K stars) |
| [MemPalace][mempalace] | Local-first AI memory with palace metaphor, 96.6% LongMemEval (33.6K stars) |
| [Code-Review-Graph][code-review-graph] | AST-based blast radius analysis, 22 MCP tools (7.1K stars) |
| [codebase-memory-mcp][codebase-memory-mcp] | Single-binary code knowledge graph: 159 tree-sitter grammars + hybrid LSP + embeddings, 14 MCP tools (3.2K stars, MIT) |
| [Serena][serena] | LSP-based semantic coding MCP toolkit, 20+ symbol-level tools, 40+ languages (25.2K stars, MIT) |
| [ast-grep MCP][ast-grep-mcp] | MCP wrapper for ast-grep structural AST search/rewrite, 4 tools (419 stars, MIT) |
| [Repomix][repomix] | Repo→single-file packer, tree-sitter `--compress`, MCP server + CC plugins (26.2K stars, MIT) |
| [code2prompt][code2prompt] | Repo→single-prompt CLI with token counting, MCP server + Python SDK (7.4K stars, MIT) |
| [CodeBurn][codeburn] | Cross-agent token-usage TUI dashboard (4K stars, MIT) |
| [ccusage][ccusage] | CC/Codex JSONL usage analyzer, MCP-integrated (13.4K stars, MIT) |
| [Claude-Code-Usage-Monitor][claude-monitor] | Predictive real-time usage monitor with P90-based limits (7.8K stars, MIT) |

[awesome-design-md]: https://github.com/VoltAgent/awesome-design-md
[graphify]: https://github.com/safishamsi/graphify
[mempalace]: https://github.com/MemPalace/mempalace
[longmemeval]: https://github.com/xiaowu0162/LongMemEval
[code-review-graph]: https://github.com/tirth8205/code-review-graph
[codebase-memory-mcp]: https://github.com/DeusData/codebase-memory-mcp
[serena]: https://github.com/oraios/serena
[ast-grep-mcp]: https://github.com/ast-grep/ast-grep-mcp
[ast-grep]: https://github.com/ast-grep/ast-grep
[repomix]: https://github.com/yamadashy/repomix
[code2prompt]: https://github.com/mufeedvh/code2prompt
[rtk-repo]: https://github.com/rtk-ai/rtk
[rtk-839]: https://github.com/rtk-ai/rtk/issues/839
[gsd-repo]: https://github.com/gsd-build/get-shit-done
[gsd-npm]: https://www.npmjs.com/package/get-shit-done-cc
[gsd-1451]: https://github.com/gsd-build/get-shit-done/issues/1451
[gsd-1457]: https://github.com/gsd-build/get-shit-done/issues/1457
[gsd-1459]: https://github.com/gsd-build/get-shit-done/issues/1459
[gsd-1461]: https://github.com/gsd-build/get-shit-done/issues/1461
[gsd-1431]: https://github.com/gsd-build/get-shit-done/issues/1431
[gsd-1466]: https://github.com/gsd-build/get-shit-done/issues/1466
[ecc]: https://github.com/affaan-m/everything-claude-code
[boucle]: https://github.com/Bande-a-Bonnot/Boucle-framework
[openharness]: https://github.com/HKUDS/OpenHarness
[byterover]: https://github.com/campfirein/byterover-cli
[byterover-paper]: https://arxiv.org/abs/2604.01599
[claude-mem]: https://github.com/thedotmack/claude-mem
[claude-mem-docs]: https://docs.claude-mem.ai/introduction
[cc-switch]: https://github.com/farion1231/cc-switch
[opensrc]: https://github.com/vercel-labs/opensrc
[codeburn]: https://github.com/getagentseal/codeburn
[ccusage]: https://github.com/ryoppippi/ccusage
[claude-monitor]: https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor
