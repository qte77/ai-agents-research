---
title: 12 Agentic Harness Patterns (Bilgin Ibryam)
source: https://generativeprogrammer.com/p/12-agentic-harness-patterns-from
purpose: Taxonomy of reusable harness-level patterns extracted from the Claude Code source leak.
category: analysis
status: research
created: 2026-04-06
updated: 2026-04-06
validated_links: 2026-04-06
---

**Status**: Research (informational)

## Summary

Bilgin Ibryam (author of [Kubernetes Patterns](https://k8spatterns.com/), O'Reilly) reverse-engineered the March 31 2026 Claude Code source leak into 12 reusable **harness-level** design patterns. These are architectural primitives at the agent runtime layer -- distinct from model-level or prompt-level patterns. Published April 5 2026 as a follow-up to his [Practical Lessons From the Claude Code Leak](https://generativeprogrammer.com/p/practical-lessons-from-the-claude) (April 3 2026).

Key thesis: *"The moat is not the model, it is the harness."*

## Cross-References in This Repository

| Pattern | Existing Analysis | File |
|---------|------------------|------|
| Persistent Instruction File | CLAUDE.md coverage | `docs/cc-native/context-memory/CC-memory-system-analysis.md` |
| Dream Consolidation | Auto-Dream 4-phase pipeline | `docs/cc-native/context-memory/CC-memory-system-analysis.md:207-246` |
| Context-Isolated Subagents | Agent teams orchestration | `docs/cc-native/agents-skills/CC-agent-teams-orchestration.md` |
| Fork-Join Parallelism | Worktree isolation | `docs/cc-native/agents-skills/CC-agent-teams-orchestration.md` |
| Deterministic Lifecycle Hooks | Hooks system analysis | `docs/cc-native/configuration/CC-hooks-system-analysis.md` |
| Progressive Context Compaction | Context compaction in changelogs | `triage/cc-changelog/2026-03-16-changelog-triage.md:113` |
| Progressive Tool Expansion | Tools inventory (28 public + gated) | `docs/cc-native/configuration/CC-tools-inventory.md` |
| Command Risk Classification | Sandbox internals | `docs/cc-native/sandboxing/` |

## Category 1: Memory and Context (5 patterns)

### 1. Persistent Instruction File

Project-level config (`CLAUDE.md`) loaded automatically at session start. Defines build commands, test commands, architecture rules, naming conventions. Ships with the repository.

### 2. Scoped Context Assembly

Dynamically loads instructions from multiple files at different scopes: organization, user, project root, parent directories, child directories. Import syntax allows splitting without duplication. The agent sees different rules depending on working directory.

### 3. Tiered Memory

Three layers: compact index (capped at 200 lines) stays in context permanently; topic-specific files load on demand; full session transcripts stay on disk for searched access.

### 4. Dream Consolidation

Background process runs periodically during idle time to review, deduplicate, prune, and reorganize agent memory. Referenced as `autoDream` mode with 8 phases and 5 types of context compaction. Merges duplicates, prunes contradictions, keeps index tight.

**Cross-ref**: This repo documents the three-gate trigger (24h + 5 sessions + lock) and four phases (Orient, Gather Signal, Consolidate, Prune & Index) in [CC-community-reimplementations-landscape.md](../../../docs/cc-community/CC-community-reimplementations-landscape.md).

### 5. Progressive Context Compaction

Multiple compression stages for conversations of different ages. Recent turns stay at full detail; older turns lightly summarized; very old turns aggressively collapsed. Four layers: `HISTORY_SNIP`, Microcompact, `CONTEXT_COLLAPSE`, Autocompact.

## Category 2: Workflow and Orchestration (3 patterns)

### 6. Explore-Plan-Act Loop

Three phases with increasing write permissions: Explore (read-only) -> Plan (discussion with user) -> Act (full tool access). Ensures understanding before editing.

### 7. Context-Isolated Subagents

Separate agents with distinct context windows, system prompts, and restricted tool access. Research agents cannot edit code; planning agents cannot execute commands. Each sees only task-relevant information.

**Cross-ref**: This repo documents lead/teammate hierarchy, shared task lists, and inter-agent messaging in [CC-agent-teams-orchestration.md](CC-agent-teams-orchestration.md).

### 8. Fork-Join Parallelism

Multiple subagents spawned in parallel, each in an isolated git worktree. Cached context reused by each fork. Results merge when all complete.

## Category 3: Tools and Permissions (3 patterns)

### 9. Progressive Tool Expansion

Starts with fewer than 20 default tools (Read, Edit, Write, Bash, Grep, Glob). MCP tools, remote tools, and custom skills activate on demand.

### 10. Command Risk Classification

Deterministic pre-parsing and per-tool permission gating. Each tool has individual allow, ask, and deny rules with pattern matching. Auto-mode classifier auto-approves low-risk actions; safety classifier handles dangerous commands.

### 11. Single-Purpose Tool Design

Replaces general shell with purpose-built tools for common operations: FileReadTool, FileEditTool, GrepTool, GlobTool. Typed inputs, constrained scope, dedicated permission rules.

## Category 4: Automation (1 pattern)

### 12. Deterministic Lifecycle Hooks

Shell commands fire automatically at specific agent lifecycle points, outside the prompt. 25+ hook points: `PreToolUse`, `PostToolUse`, `SessionStart`, `CwdChanged`. Mandatory actions belong in hooks, not instructions.

**Cross-ref**: This repo documents the full hook lifecycle in [CC-hooks-system-analysis.md](../configuration/CC-hooks-system-analysis.md).

## Author

[Bilgin Ibryam](https://www.linkedin.com/in/bibryam/) -- Principal PM at Diagrid (Dapr). Apache Software Foundation Member. Previously 9 years at Red Hat, before that BBC News. Author of *Kubernetes Patterns* (O'Reilly, 2nd ed. 2023), *Camel Design Patterns*, and the new [Prompt Patterns](https://www.promptpatterns.dev/) catalog.

Pattern taxonomist by trade: Kubernetes patterns -> Camel patterns -> Prompt patterns -> Agentic harness patterns.

## Sources

- [12 Agentic Harness Patterns from Claude Code](https://generativeprogrammer.com/p/12-agentic-harness-patterns-from) (2026-04-05)
- [Practical Lessons From the Claude Code Leak](https://generativeprogrammer.com/p/practical-lessons-from-the-claude) (2026-04-03)
- [Kubernetes Patterns (O'Reilly)](https://k8spatterns.com/)
- [Prompt Patterns catalog](https://www.promptpatterns.dev/)
- [The Generative Programmer Substack](https://generativeprogrammer.com/)

## Action Items

- [ ] Map remaining patterns to existing analyses (6/12 mapped above)
- [ ] Track Ibryam's Prompt Patterns catalog for convergence with CC skills format
- [ ] Monitor for community implementations of these patterns outside CC
