---
title: CC Community Tooling Landscape
purpose: Survey of community developer tools that integrate with or enhance Claude Code — context compression, meta-prompting, spec-driven development, agent frameworks, file read deduplication.
category: landscape
status: research
created: 2026-03-13
updated: 2026-04-04
validated_links: 2026-04-04
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

Cross-ref: [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md)

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

**Risks**: Elastic License 2.0 (not OSS — requires commercial agreement for production). Cloud dependency for sync features. Overlaps with CC's built-in memory system (`~/.claude/memory/`).

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

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

All six address different layers of the agent stack — complementary, not competing.

Cross-ref: [CC-extended-context-analysis.md](../cc-native/context-memory/CC-extended-context-analysis.md) — CC's built-in context compaction (fifth approach)

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
