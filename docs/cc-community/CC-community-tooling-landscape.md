---
title: CC Community Tooling Landscape
purpose: Survey of community developer tools that integrate with or enhance Claude Code — context compression, meta-prompting, spec-driven development, agent frameworks, file-read deduplication, source enrichment, provider management, design systems. Memory, code-analysis, and usage-observability tools live in linked topic docs; this doc keeps the cross-tool comparison.
category: landscape
status: research
platform_scope: [claude-code, cursor, codex, gemini-cli, opencode, windsurf, zed, antigravity]
created: 2026-03-13
updated: 2026-06-19
validated_links: 2026-06-19
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

Cross-ref: [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md); [CC-community-skills-landscape.md](CC-community-skills-landscape.md) — caveman (output-side compression); the [usage-observability tools](CC-usage-tooling-landscape.md) (measurement layer)

### Token-Waste Reduction Stack

A layered approach to keeping context in Claude's ~75k-token "smart zone" via deterministic developer-side output filtering, rather than relying on the model to decide what matters ([context-efficient-backpressure][hlyr-backpressure], 2025-12-09).

| Layer | Mechanism | Tool / Pattern | Known limitation |
|---|---|---|---|
| **1 — Env vars** | `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1` strips built-in git-workflow tokens from context in headless mode (CC v2.1.69+) | Shell env / `.env` | Headless-only; no effect in interactive sessions |
| **2 — Native hook filters (DIY)** | `run_silent()` PostToolUse bash wrapper: captures stdout to a temp file, emits `✓ <desc>` on exit 0, surfaces full output only on non-zero exit; pair with failFast flags (`pytest -x`, `jest --bail`, `go test -failfast`) to halt at first failure | CC PostToolUse hook | Must be written per project; no packaging or reuse mechanism built in |
| **3 — Wrapper scripts** | RTK intercepts shell command outputs via hooks — see [RTK section above](#rtk-rust-token-killer); independently verified zero savings on `cat`/`grep`/`pytest`/`ruff` | [RTK][rtk-repo] | Does not filter content RTK doesn't recognise; zero gains on passthrough categories |
| **4 — Output-style skills** | caveman and similar skills compress the model's own response verbosity | See [CC-community-skills-landscape.md][skills-landscape] | Output-side only; does not reduce tool or shell output |

Layer 1 cross-ref: [CC-changelog-feature-scan.md](../cc-native/configuration/CC-changelog-feature-scan.md) — env var inventory.
Layer 2 cross-ref: [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md) — PostToolUse hook mechanism.

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

## Detailed Tool Landscapes

Per-tool entries for three categories have moved to focused topic docs; the cross-tool comparison below still covers all of them:

- [CC-memory-tooling-landscape.md](CC-memory-tooling-landscape.md) — persistent memory: ByteRover, Claude-Mem, MemPalace, MemSearch
- [CC-code-tooling-landscape.md](CC-code-tooling-landscape.md) — code analysis: Graphify, Code-Review-Graph, codebase-memory-mcp, Serena, ast-grep MCP, Repomix, code2prompt
- [CC-usage-tooling-landscape.md](CC-usage-tooling-landscape.md) — usage observability: CodeBurn, ccusage, Claude-Code-Usage-Monitor

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
| **MemSearch** | Persistent memory (cross-agent) | Plugin (hooks + skill, no MCP) | Markdown source-of-truth + Milvus hybrid search | Active (~2K stars, v0.4.7) |
| **Code-Review-Graph** | Structural code analysis | MCP server (22 tools, auto-config) | AST-based blast radius for reviews | Active (7.1K stars) |
| **codebase-memory-mcp** | Code→graph + LSP + embeddings | MCP (14 tools) + PreToolUse hook + auto-config | Single-binary knowledge graph | Active (3.2K stars, v0.7.0) |
| **Serena** | Semantic code (live LSP) | MCP server (20+ tools) | Symbol-level retrieve/edit/refactor | Active (25.2K stars, v1.5.3) |
| **ast-grep MCP** | Structural search/rewrite | MCP server (4 tools) | tree-sitter AST patterns | Experimental (419 stars, no release) |
| **Repomix** | Repo→single-file context export | MCP server + official CC plugins | tree-sitter compression + token counts | Stable (26.2K stars, v1.14.1) |
| **code2prompt** | Repo→single-prompt context export | MCP server + CLI | Templated export + token counts | Stable (7.4K stars, v4.2.0) |
| **CodeBurn** | Token-usage observability (cross-agent) | CLI (reads on-disk session data) | Cross-agent dashboard, 13 task categories, optimize/compare | Active (4K stars) |
| **ccusage** | Token-usage observability (CC/Codex) | CLI + MCP server + statusline | JSONL analyzer, cache-token split, offline mode | Stable (13.4K stars, v18.0.11) |
| **Claude-Code-Usage-Monitor** | Predictive usage monitoring | Real-time TUI | P90-based limit prediction, burn-rate analytics, plan-aware | Active (7.8K stars, v3.1.0) |

All twenty-two address different layers of the agent stack — complementary, not competing. The five code-analysis tools (graphify, Code-Review-Graph, codebase-memory-mcp, Serena, ast-grep MCP) split along precompute-a-graph vs. live-LSP vs. on-demand-structural-search; the two repo packers (Repomix, code2prompt) are one-shot context export rather than a live server. Full per-tool entries for the memory, code-analysis, and usage-observability rows are in the topic docs linked above.

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
| [MemSearch][memsearch] | Markdown + Milvus persistent memory for CC/OpenCode/Codex, hooks+skill (no MCP), hybrid vector+BM25 (~2K stars, MIT) |
| [Code-Review-Graph][code-review-graph] | AST-based blast radius analysis, 22 MCP tools (7.1K stars) |
| [codebase-memory-mcp][codebase-memory-mcp] | Single-binary code knowledge graph: 159 tree-sitter grammars + hybrid LSP + embeddings, 14 MCP tools (3.2K stars, MIT) |
| [Serena][serena] | LSP-based semantic coding MCP toolkit, 20+ symbol-level tools, 40+ languages (25.2K stars, MIT) |
| [ast-grep MCP][ast-grep-mcp] | MCP wrapper for ast-grep structural AST search/rewrite, 4 tools (419 stars, MIT) |
| [Repomix][repomix] | Repo→single-file packer, tree-sitter `--compress`, MCP server + CC plugins (26.2K stars, MIT) |
| [code2prompt][code2prompt] | Repo→single-prompt CLI with token counting, MCP server + Python SDK (7.4K stars, MIT) |
| [CodeBurn][codeburn] | Cross-agent token-usage TUI dashboard (4K stars, MIT) |
| [ccusage][ccusage] | CC/Codex JSONL usage analyzer, MCP-integrated (13.4K stars, MIT) |
| [Claude-Code-Usage-Monitor][claude-monitor] | Predictive real-time usage monitor with P90-based limits (7.8K stars, MIT) |
| [Context-Efficient Backpressure for Coding Agents][hlyr-backpressure] | 4-layer token-waste reduction ladder: env vars, hook filters, wrapper scripts, output-style skills (hlyr.dev, 2025-12-09) |

[awesome-design-md]: https://github.com/VoltAgent/awesome-design-md
[graphify]: https://github.com/safishamsi/graphify
[mempalace]: https://github.com/MemPalace/mempalace
[memsearch]: https://github.com/zilliztech/memsearch
[code-review-graph]: https://github.com/tirth8205/code-review-graph
[codebase-memory-mcp]: https://github.com/DeusData/codebase-memory-mcp
[serena]: https://github.com/oraios/serena
[ast-grep-mcp]: https://github.com/ast-grep/ast-grep-mcp
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
[cc-switch]: https://github.com/farion1231/cc-switch
[opensrc]: https://github.com/vercel-labs/opensrc
[hlyr-backpressure]: https://www.hlyr.dev/blog/context-efficient-backpressure
[skills-landscape]: CC-community-skills-landscape.md
[codeburn]: https://github.com/getagentseal/codeburn
[ccusage]: https://github.com/ryoppippi/ccusage
[claude-monitor]: https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor
