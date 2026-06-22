---
title: 12 Agentic Harness Patterns (Bilgin Ibryam)
source: https://generativeprogrammer.com/p/12-agentic-harness-patterns-from
purpose: Taxonomy of reusable harness-level patterns extracted from the Claude Code source leak.
category: analysis
status: research
created: 2026-04-06
updated: 2026-06-22
validated_links: 2026-06-22
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

**Cross-ref**: This repo documents the three-gate trigger (24h + 5 sessions + lock) and four phases (Orient, Gather Signal, Consolidate, Prune & Index) in [CC-community-reimplementations-landscape.md](../../cc-community/CC-community-reimplementations-landscape.md).

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

CC's native implementation of this pattern via the `context: fork` skill frontmatter
field (v2.1.0) is documented in depth — including the context-as-stack model, turn-boundary
rewinding, and a comparison of the four CC forking mechanisms — in
[CC-skills-adoption-analysis.md][context-fork-section].
The skills doc also documents "harness engineering" (coined by Viv Trivedy) as a subset of
"context engineering" (coined by Dex Horthy) for reference.

[context-fork-section]: CC-skills-adoption-analysis.md#context-fork--mechanics-and-economics

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

[HumanLayer][humanlayer] provides a structured approval-gate SDK that intercepts agent
tool calls for human review before execution. This is complementary to CC's built-in
permission prompts and `PermissionRequest` hooks: CC's hooks handle automated allow/deny
logic, while HumanLayer adds a structured human-in-the-loop layer for cases where
automated approval rules are insufficient.

## Author

[Bilgin Ibryam](https://github.com/bibryam) -- Principal PM at Diagrid (Dapr). Apache Software Foundation Member. Previously 9 years at Red Hat, before that BBC News. Author of *Kubernetes Patterns* (O'Reilly, 2nd ed. 2023), *Camel Design Patterns*, and the new [Prompt Patterns](https://www.promptpatterns.dev/) catalog.

Pattern taxonomist by trade: Kubernetes patterns -> Camel patterns -> Prompt patterns -> Agentic harness patterns.

## Sources

- [12 Agentic Harness Patterns from Claude Code](https://generativeprogrammer.com/p/12-agentic-harness-patterns-from) (2026-04-05)
- [Practical Lessons From the Claude Code Leak](https://generativeprogrammer.com/p/practical-lessons-from-the-claude) (2026-04-03)
- [Skill Issue: Harness Engineering for Coding Agents][skill-issue-post] (Kyle, hlyr.dev, 2026-03-12) — harness engineering framing, HumanLayer mention
- [HumanLayer][humanlayer] — human-in-the-loop approval-gate SDK for agent tool calls
- [Kubernetes Patterns (O'Reilly)](https://k8spatterns.com/)
- [Prompt Patterns catalog](https://www.promptpatterns.dev/)
- [The Generative Programmer Substack](https://generativeprogrammer.com/)
- ["Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems" (arXiv 2604.14228)](https://arxiv.org/abs/2604.14228) — academic design-space analysis of CC's source (Liu et al., 2026)

## Security-Domain Application: Defending Code Reference Harness

**Source**: [anthropics/defending-code-reference-harness][dcrh] | First-party Anthropic reference implementation

A concrete application of Context-Isolated Subagents + Fork-Join Parallelism to autonomous vulnerability discovery. The harness encodes these two harness patterns into a seven-stage security pipeline:

**Pipeline** (build → recon → find → verify → dedupe → report → patch):

1. **Build** — compile target with ASAN into Docker image
2. **Recon** — lightweight agent proposes input-parsing subsystems to attack
3. **Find** — parallel agents craft malformed inputs until reproducible crashes (Fork-Join: multiple find-agents run concurrently, each in an isolated gVisor container)
4. **Verify** — separate grader agent reproduces crashes in a fresh container (Context-Isolated Subagent: verifier has no access to find-agent context)
5. **Dedupe** — judge agent compares findings against known bugs
6. **Report** — exploitability analysis and severity assessment
7. **Patch** — fix proposals validated through build/test cycle

**Sandboxing model**: each pipeline agent runs inside a dedicated gVisor container on a `vp-internal` Docker network; egress is restricted to `api.anthropic.com:443` only via a proxy sidecar. Entry point `bin/vp-sandboxed` refuses to run unless gVisor and the proxy are active. See also: [CC-sandbox-platforms-landscape.md](../sandboxing/CC-sandbox-platforms-landscape.md#defending-code-reference-harness-gvisor-pattern).

**Shipped CC skills**: `/quickstart`, `/threat-model`, `/vuln-scan`, `/triage`, `/patch`, `/customize`

**Companion products**: [Claude Security][claude-security] (managed hosted product for multi-project vuln discovery with false-positive reduction); Glasswing partnership (security team collaboration program).

[dcrh]: https://github.com/anthropics/defending-code-reference-harness
[claude-security]: https://claude.com/product/claude-security
[skill-issue-post]: https://www.hlyr.dev/blog/skill-issue-harness-engineering-for-coding-agents
[humanlayer]: https://www.humanlayer.dev/

## Academic Design-Space Analysis (arXiv 2604.14228)

["Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems"](https://arxiv.org/abs/2604.14228) (Liu, Zhao, Shang, Shen, 2026) reverse-engineers CC's published TypeScript source — an academic complement to Ibryam's pattern taxonomy above, framing the same artifact as a *design space*. It extracts five design motivations and traces them to concrete mechanisms:

- **Seven-mode permission system** + an ML-based command risk classifier — cf. patterns 9–10 (Progressive Tool Expansion, Command Risk Classification).
- **Five-layer context-compaction pipeline** — cf. pattern 5 (Progressive Context Compaction).
- **Four extensibility mechanisms** — MCP, plugins, skills, hooks.
- **Subagent + worktree delegation** and append-oriented session management.

It compares CC against a second system ("OpenClaw") to show how deployment context drives divergent architectural choices, and closes with six open design directions. Cross-ref: [CC-reverse-engineering-landscape.md](../../cc-community/CC-reverse-engineering-landscape.md) for the broader source/binary analysis lineage.

## Action Items

- [ ] Map remaining patterns to existing analyses (6/12 mapped above)
- [ ] Track Ibryam's Prompt Patterns catalog for convergence with CC skills format
- [ ] Monitor for community implementations of these patterns outside CC
