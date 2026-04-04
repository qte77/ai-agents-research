---
title: CC Community Reimplementations Landscape
description: Survey of community reimplementations and educational deconstructions of Claude Code — cleanroom rebuilds, spec-derived ports, educational courses, and leak-derived alternatives.
category: landscape
status: research
created: 2026-04-04
updated: 2026-04-04
validated_links: 2026-04-04
---

**Status**: Research (informational)

## Summary

Multiple community projects have reimplemented or deconstructed Claude Code's architecture following the March 2026 npm sourcemap exposure. These range from cleanroom educational rebuilds to direct forks of leaked source. This landscape doc catalogs them with provenance classification to guide citation decisions.

## Overview

<!-- markdownlint-disable MD013 -->

| Repo | Language | Approach | Stars | License | Risk |
|------|----------|----------|-------|---------|------|
| [instructkr/claw-code][claw] | Rust 93% / Python 7% | Cleanroom | 164K | — | LOW |
| [Kuberwastaken/claude-code][claurst] (CLAURST) | Rust | Spec-derived | 7.9K | — | MEDIUM |
| [shareAI-lab/learn-claude-code][learn] | Python / TypeScript | Educational | 48K | MIT | LOW |
| [Gitlawb/openclaude][openclaude] | TypeScript 99.7% | Leak-derived | 13K | MIT | MEDIUM |
| [leaked-claude-code/leaked-claude-code][leaked] | TypeScript | Leaked source | — | — | **HIGH** |

<!-- markdownlint-enable MD013 -->

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

**Repo**: [Kuberwastaken/claude-code][claurst] | **Stars**: 7.9K | **Approach**: Spec-derived

Rust reimplementation built from behavioral specifications rather than copying source. Includes detailed technical breakdown of features discovered through reverse-engineering.

**Documented features** (unverified internal feature names):

- **BUDDY** — Tamagotchi-style companion with 18 procedurally-generated species, deterministic per-user via Mulberry32 PRNG
- **KAIROS** — Always-on proactive assistant with 15-second blocking budget
- **autoDream** — Four-phase background memory consolidation engine
- **Coordinator Mode** — Multi-agent orchestration with shared scratchpad ("Penguin Mode" kill switch)

**Provenance note**: Feature names and specs are reverse-engineered from the March 2026 sourcemap exposure. Do not treat these as confirmed CC features in other docs.

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

## leaked-claude-code/leaked-claude-code

**Excluded from analysis** — claims to contain full proprietary TypeScript source code (~512K lines) from the March 2026 npm sourcemap exposure. Includes alleged security bypass techniques. Included in landscape table for completeness only. Do not use as a source for factual claims elsewhere in this repository.

## Cross-References

- [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) — community dev tooling (RTK, everything-claude-code)
- [CC-community-plugins-landscape.md](CC-community-plugins-landscape.md) — community plugin catalogs
- [CC-sandboxing-analysis.md](../cc-native/sandboxing/CC-sandboxing-analysis.md) — what reimplementations may miss in sandbox behavior

## Sources

| Source | Content |
|---|---|
| [instructkr/claw-code][claw] | Cleanroom Rust/Python reimplementation |
| [Kuberwastaken/claude-code][claurst] | Spec-derived Rust reimplementation (CLAURST) |
| [shareAI-lab/learn-claude-code][learn] | Educational harness engineering course |
| [Gitlawb/openclaude][openclaude] | Multi-provider CLI (leak-derived) |
| [leaked-claude-code/leaked-claude-code][leaked] | Alleged proprietary source (excluded from analysis) |

[claw]: https://github.com/instructkr/claw-code
[claurst]: https://github.com/Kuberwastaken/claude-code
[learn]: https://github.com/shareAI-lab/learn-claude-code
[openclaude]: https://github.com/Gitlawb/openclaude
[leaked]: https://github.com/leaked-claude-code/leaked-claude-code
