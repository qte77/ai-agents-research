---
title: CC Community Reimplementations Landscape
description: Survey of community reimplementations and educational deconstructions of Claude Code — cleanroom rebuilds, spec-derived ports, educational courses, and leak-derived alternatives.
category: landscape
status: research
created: 2026-04-04
updated: 2026-04-05
validated_links: 2026-04-05
---

**Status**: Research (informational)

## Summary

Multiple community projects have reimplemented or deconstructed Claude Code's architecture following the March 2026 npm sourcemap exposure. These range from cleanroom educational rebuilds to direct forks of leaked source. This landscape doc catalogs them with provenance classification to guide citation decisions.

## Overview

| Repo | Language | Approach | Stars | License | Risk |
|------|----------|----------|-------|---------|------|
| [instructkr/claw-code][claw] | Rust 93% / Python 7% | Cleanroom | 164K | — | LOW |
| [Kuberwastaken/claude-code][claurst] (CLAURST) | Rust | Spec-derived | 7.9K | — | MEDIUM |
| [shareAI-lab/learn-claude-code][learn] | Python / TypeScript | Educational | 48K | MIT | LOW |
| [Gitlawb/openclaude][openclaude] | TypeScript 99.7% | Leak-derived | 13K | MIT | MEDIUM |
| [coder/claudecode.nvim][nvim] | Lua | Cleanroom | — | Apache-2.0 | LOW |
| [zackautocracy/claude-code][zack] | TypeScript | Leak-derived (snapshot) | 696 | — | **HIGH** |
| [leaked-claude-code/leaked-claude-code][leaked] | TypeScript | Leaked source | — | — | **HIGH** |

## Provenance & Risk Classification

| Classification | Definition | Citation Policy |
|----------------|------------|-----------------|
| **Cleanroom** | Built from public docs and observed behavior only | Safe to cite and analyze |
| **Spec-derived** | Built from specifications that may include reverse-engineered details | Cite with provenance note; do not reproduce internal feature names as confirmed |
| **Educational** | Deconstructs architecture for learning; built from public behavior | Safe to cite |
| **Leak-derived** | Built from or containing alleged proprietary source code | Reference existence only; do not cite code or link to specific files |

## instructkr/claw-code

**Repo**: [instructkr/claw-code][claw] | **Stars**: 164K | **Approach**: Cleanroom

Cleanroom reimplementation of an AI agent harness in Rust and Python. Described as the fastest repo to surpass 50K stars (2 hours after publication).

**Architecture**: Rust workspace with modular crates (API client, runtime, tools, commands, plugins, CLI, LSP). Python workspace for porting infrastructure and parity auditing.

**Key features**: Interactive REPL, OAuth and multi-provider API abstraction, plugin system with hook pipelines, session state compaction, MCP orchestration.

**Note**: Repository describes itself as studying a different AI agent harness system, not explicitly Claude Code. Temporary ownership transfer noted with maintenance continuing at a parity repo.

## Kuberwastaken/claude-code (CLAURST)

**Repo**: [Kuberwastaken/claude-code][claurst] | **Stars**: 8.1K | **License**: GPL-3.0 | **Approach**: Spec-derived

Two-phase clean-room project by Kuber Mehta: (1) an AI agent analyzed the leaked source and produced behavioral **specs** (`spec/`), (2) a separate AI agent implemented from specs alone in idiomatic Rust (`src-rust/`). Claims 100% behavioral coverage. Claims legal precedent via Phoenix Technologies v. IBM (1984) clean-room pattern. The README doubles as the **most detailed public technical breakdown** of CC internals from the `@anthropic-ai/claude-code@2.1.88` npm sourcemap exposure (2026-03-31).

### Documented Features (unverified internal feature names)

| Feature | Details |
|---------|---------|
| **BUDDY** | Tamagotchi companion: 18 species via Mulberry32 PRNG (seed: `userId` + `'friend-2026-401'`). Rarity tiers (Common 60% → Legendary 1%), 1% shiny chance. 5 stats (DEBUGGING, PATIENCE, CHAOS, WISDOM, SNARK). ASCII sprites, soul prompt. `/buddy` shipped v2.1.89 (April 1, 2026) |
| **KAIROS** | Always-on proactive assistant: tick engine with 15-second blocking budget, max 2 proactive messages per evaluation. Append-only daily logs. Brief output mode. 3 exclusive tools: `SendUserFile`, `PushNotification`, `SubscribePR`. Feature flags: `PROACTIVE` + `KAIROS` (both disabled) |
| **Auto-Dream** | Background memory consolidation: three-gate trigger (24h + 5 sessions + lock), four phases (Orient → Gather Signal → Consolidate → Prune & Index). Read-only bash. Forked subagent. Telemetry: `tengu_auto_dream_fired/completed/failed` |
| **Coordinator Mode** | Multi-agent orchestration via `CLAUDE_CODE_COORDINATOR_MODE=1`. Four phases: Research → Synthesis → Implementation → Verification. Shared scratchpad (`tengu_scratch`). UDS Inbox for inter-session IPC. `<task-notification>` XML protocol. Anti-lazy-delegation prompt rule |
| **UltraPlan** | Cloud-offloaded planning: remote CCR session running Opus 4.6, 30-min budget, 3s polling. `__ULTRAPLAN_TELEPORT_LOCAL__` sentinel. **Now officially documented**: [code.claude.com/docs/en/ultraplan][ultraplan] |
| **Undercover Mode** | Prevents `USER_TYPE === 'ant'` employees from leaking codenames in public commits. No force-OFF. Suppresses: animal codenames (Capybara, Tengu, Fennec), unreleased model versions, internal tooling names, "Claude Code" attribution |
| **Penguin Mode** | Fast mode internal codename. API endpoint: `api/claude_code_penguin_mode`. Kill switch: `tengu_penguins_off`. Config: `penguinModeOrgEnabled` |

### Additional Coverage

- **40+ tool registry** including internal-only tools (ConfigTool, TungstenTool, SuggestBackgroundPRTool) and feature-gated tools — cross-ref: [CC-tools-inventory.md](../cc-native/configuration/CC-tools-inventory.md)
- **15 API beta headers** including unreleased: `redact-thinking`, `afk-mode`, `advisor-tool`, `token-efficient-tools`
- **12 compile-time feature flags** (PROACTIVE, KAIROS, DAEMON, BRIDGE_MODE, VOICE_MODE, COORDINATOR_MODE, BUDDY, etc.)
- **Upcoming models**: Capybara v2 (with fast tier, 1M context), Opus 4.7, Sonnet 4.8 referenced in code
- **System prompt architecture**: `SYSTEM_PROMPT_DYNAMIC_BOUNDARY` marker splitting static (cacheable) vs dynamic (per-user) sections
- **Model codename history**: Fennec→Opus, Sonnet 1M→Sonnet 4.5→Sonnet 4.6
- **Computer Use "Chicago"**: `@ant/computer-use-mcp`, screenshot/click/keyboard, Max/Pro gated

### Provenance Assessment

Despite the "clean-room" claim, the specs were **AI-generated from leaked source** — the separation is AI-to-AI, not human-to-human. The GPL-3.0 license does not resolve the underlying IP question. Feature names and specs are reverse-engineered from the `@anthropic-ai/claude-code@2.1.88` npm sourcemap exposure ([2026-03-31][register-leak]). Do not treat these as confirmed CC features in other docs.

## shareAI-lab/learn-claude-code

**Repo**: [shareAI-lab/learn-claude-code][learn] | **Stars**: 48K | **License**: MIT | **Approach**: Educational

Comprehensive educational project teaching "harness engineering" — building infrastructure for AI agents to operate in specific domains. Deconstructs CC architecture through 12 progressive sessions.

**Sessions** (s01–s12): Basic agent loops → tools → planning → context management → task systems → multi-agent team coordination.

**Platform**: Interactive Next.js web interface, docs in EN/CN/JP.

**Philosophy**: "Prompt plumbing agents are the fantasy of programmers who don't train models." Focus on harness engineering, not prompt-chaining.

**Companion projects**: Kode-cli (open-source agent CLI), Kode-agent-sdk (embeddable agent library), claw0 (always-on assistant patterns).

## Gitlawb/openclaude

**Repo**: [Gitlawb/openclaude][openclaude] | **Stars**: 13K | **License**: MIT | **Approach**: Leak-derived

Open-source multi-provider CLI derived from the March 2026 Claude Code source exposure. Strips telemetry and adds provider-agnostic functionality.

**Multi-provider support**: OpenAI, Gemini, DeepSeek, Ollama, GitHub Models, Codex. Provider selection via `/provider` command or environment variables.

**Features**: Bash/file tools, grep/glob, slash commands, MCP integration, web search (DuckDuckGo/Firecrawl), agent routing for cost optimization.

**Provenance note**: Explicitly acknowledges derivation from leaked source. "Not an authorized fork or open-source release by Anthropic." Claude remains trademarked by Anthropic. 304 commits, actively maintained.

## coder/claudecode.nvim

**Repo**: [coder/claudecode.nvim][nvim] | **License**: Apache-2.0 | **Approach**: Cleanroom

Pure Lua Neovim plugin that reverse-engineered the Claude Code IDE integration protocol (WebSocket JSON-RPC 2.0 / MCP). Achieved 100% compatibility with the VS Code extension protocol without accessing proprietary source.

**Key contribution**: First public documentation of the IDE integration protocol — WebSocket transport (not SSE despite `CLAUDE_CODE_SSE_PORT` name), per-session auth tokens at `~/.claude/ide/<port>.lock`, localhost-only binding, and the complete tool interface (selection tracking, native diff, file context).

**Provenance note**: Built entirely from observed behavior and public API contracts. No leaked source involved.

Cross-ref: [CC-ide-integration-protocol.md](../cc-native/configuration/CC-ide-integration-protocol.md)

## zackautocracy/claude-code

**Repo**: [zackautocracy/claude-code][zack] | **Stars**: 696 | **Approach**: Leak-derived (snapshot)

Read-only source snapshot from the `@anthropic-ai/claude-code@2.1.88` npm sourcemap exposure ([2026-03-31][register-leak]). Not a reimplementation — a navigable archive maintained for *"educational, defensive security research, and software supply-chain analysis"* by a university student (autocracy101).

Powers [ccunpacked.dev][ccunpacked] — a visual architecture explorer with interactive codebase tiles, agent loop walkthrough, tool/command catalogs, and hidden features documentation.

**Provenance note**: Contains alleged proprietary source (~512K LOC TypeScript, ~1,906 files). Reference existence and architectural observations only; do not cite code.

Cross-ref: [CC-reverse-engineering-landscape.md](CC-reverse-engineering-landscape.md) — ccunpacked.dev visual guide entry

## leaked-claude-code/leaked-claude-code

**Excluded from analysis** — claims to contain full proprietary TypeScript source code (~512K lines) from the March 2026 npm sourcemap exposure. Includes alleged security bypass techniques. Included in landscape table for completeness only. Do not use as a source for factual claims elsewhere in this repository.

## Cross-References

- [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) — community dev tooling (RTK, everything-claude-code)
- [CC-community-plugins-landscape.md](CC-community-plugins-landscape.md) — community plugin catalogs
- [CC-reverse-engineering-landscape.md](CC-reverse-engineering-landscape.md) — ccunpacked.dev and other RE tools
- [CC-sandboxing-analysis.md](../cc-native/sandboxing/CC-sandboxing-analysis.md) — what reimplementations may miss in sandbox behavior
- [CC-tools-inventory.md](../cc-native/configuration/CC-tools-inventory.md) — internal/gated tools appendix (sourced from CLAURST)
- [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — Auto-Dream section
- [CC-agent-teams-orchestration.md](../cc-native/agents-skills/CC-agent-teams-orchestration.md) — UDS Inbox and Coordinator Mode
- [CC-plans-as-skill-rule-templates.md](../cc-native/agents-skills/CC-plans-as-skill-rule-templates.md) — UltraPlan section

## Sources

| Source | Content |
|---|---|
| [instructkr/claw-code][claw] | Cleanroom Rust/Python reimplementation |
| [Kuberwastaken/claude-code][claurst] | Spec-derived Rust reimplementation (CLAURST) |
| [shareAI-lab/learn-claude-code][learn] | Educational harness engineering course |
| [Gitlawb/openclaude][openclaude] | Multi-provider CLI (leak-derived) |
| [coder/claudecode.nvim][nvim] | Cleanroom Neovim IDE integration (Lua, Apache-2.0) |
| [leaked-claude-code/leaked-claude-code][leaked] | Alleged proprietary source (excluded from analysis) |
| [zackautocracy/claude-code][zack] | Source snapshot powering ccunpacked.dev (leak-derived) |

[claw]: https://github.com/instructkr/claw-code
[claurst]: https://github.com/Kuberwastaken/claude-code
[learn]: https://github.com/shareAI-lab/learn-claude-code
[openclaude]: https://github.com/Gitlawb/openclaude
[nvim]: https://github.com/coder/claudecode.nvim
[leaked]: https://github.com/leaked-claude-code/leaked-claude-code
[zack]: https://github.com/zackautocracy/claude-code
[ccunpacked]: https://ccunpacked.dev/
[ultraplan]: https://code.claude.com/docs/en/ultraplan
[register-leak]: https://www.theregister.com/2026/03/31/anthropic_claude_code_source_code/
