---
title: 12 Agentic Harness Patterns (Bilgin Ibryam)
source: https://generativeprogrammer.com/p/12-agentic-harness-patterns-from
purpose: Taxonomy of reusable harness-level patterns extracted from the Claude Code source leak.
status: research
created: 2026-04-06
updated: 2026-11-22
validated_links_on: 2026-11-18
---

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
| "-Engineering" ladder (Flow / Harness / Context / Loop / Spec) | Disciplines synthesis | `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md` §1 |

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

**Research on what compaction loses (2026-11).** [ARCBench][arcbench] (Zha et al., VU Amsterdam, arXiv
2611.03223) tested ten compactors on the pi agent harness and others, not Claude Code's own. Across
models, rule violations rose from 9.6% with full context to 37.8% after compaction (Table 3), and runs
whose summary still contained the rule violated it 2.6 times as often as the baseline (§4.2). Only a
compaction prompt that explicitly preserves rules beat full context (9.0% against 11.9%). The set is
small: "seventeen English cases". A second preprint (Chu, University at Albany, [arXiv
2611.06545][handoff-paper]) audits agents' own hand-off summaries on Qwen3 and gpt-oss models in a custom
harness. Summaries sometimes state restrictions or approvals the record doesn't support (1.2–2.4% of
held-out summaries for restrictions). Replacing "Some actions need approval." with "Only actions that
the rules or the user's request say need approval require it." cut unsupported restrictions from 5.0%
to 1.8% on the development set and from 1.8% to 0.3% on held-out templates (pre-specified tests);
neutralizing false approvals cut unauthorized actions from 24 to 7 of 120 runs (post hoc). Code:
[`Chuw1/handoff-audit`][handoff-audit] (MIT). *Our reading:* keep standing rules in CLAUDE.md or rules
files, which Claude Code reloads after compaction, rather than stating them once in conversation; word
approval rules by where the requirement comes from; and check plan or hand-off files for approvals
nobody gave.

## Category 2: Workflow and Orchestration (3 patterns)

### 6. Explore-Plan-Act Loop

Three phases with increasing write permissions: Explore (read-only) -> Plan (discussion with user) -> Act (full tool access). Ensures understanding before editing.

**Practitioner additions (single-source, [ai-that-works][aiw-talks] practitioner talks; hosts discuss their own workflow, so these are
claims, not shipped code).**

- *Proof before research.* The 2026-02-10 episode and the 2026-02-24 live session add a step before
  research: have the agent write and run a small program against the real SDK or API ("learning tests")
  and carry the findings into later phases. Stated reason: docs and model memory can describe behavior
  the runtime does not show. The host also called these a contract to re-run on upgrades, and "proof" a
  third research type next to code and web research. Not independently corroborated; the episode credits
  Michael Feathers' legacy-code book for the term, which we did not check.
- *Questions, then blind research.* In the 2026-01-27 session the ticket is first turned into a list of
  objective questions about the code; a fresh context answers them without being told what is being
  built. Stated reason: a model that knows the goal bakes implementation choices into the research.
  Compare the research-plan-implement gates in
  [CC-memory-system-analysis.md](../context-memory/CC-memory-system-analysis.md).
- *Back pressure and one step per loop.* In the 2025-10-28 Ralph episode the hosts describe tests,
  types and builds as the governor of an unattended loop, and bound each run to one meaningful step,
  then check, commit, exit and rerun, instead of asking the model to keep working. HumanLayer authors
  also wrote the post the corpus already cites for back pressure
  ([CC-community-tooling-landscape.md](../../cc-community/CC-community-tooling-landscape.md)), so this is
  not a second source. Loop mechanics: [CC-ralph-enhancement-research.md](CC-ralph-enhancement-research.md).

### 7. Context-Isolated Subagents

Separate agents with distinct context windows, system prompts, and restricted tool access. Research agents cannot edit code; planning agents cannot execute commands. Each sees only task-relevant information.

**Cross-ref**: This repo documents lead/teammate hierarchy, shared task lists, and inter-agent messaging in [CC-agent-teams-orchestration.md](CC-agent-teams-orchestration.md).

### 8. Fork-Join Parallelism

Multiple subagents spawned in parallel, each in an isolated git worktree. Cached context reused by each fork. Results merge when all complete.

CC's native implementation of this pattern via the `context: fork` skill frontmatter
field (v2.1.0) is documented in depth — including the context-as-stack model, turn-boundary
rewinding, and a comparison of the four CC forking mechanisms — in
[CC-skills-adoption-analysis.md][context-fork-section].
The "harness engineering" / "context engineering" / "flow engineering" terminology
ladder — including AlphaCodium's Flow Engineering (arXiv:2401.08500, GPT-4 CodeContests
pass@5 19%→44%) and OpenAI's Feb 2026 "Harness Engineering" post — is tracked in
[agentic-engineering-disciplines-landscape.md §1][disciplines-ladder], not in the skills doc.

[context-fork-section]: CC-skills-adoption-analysis.md#context-fork--mechanics-and-economics
[disciplines-ladder]: ../../sdlc-lcm/agentic-engineering-disciplines-landscape.md

## Category 3: Tools and Permissions (3 patterns)

### 9. Progressive Tool Expansion

Starts with fewer than 20 default tools (Read, Edit, Write, Bash, Grep, Glob). Model Context Protocol (MCP) tools, remote tools, and custom skills activate on demand.

**Decision rule and measurement (single-source, [ai-that-works][aiw-talks] practitioner talks).** In the
2026-03-24 episode the hosts argue: if you control the integration, call the SDK or first-party API; use
MCP for tools your users bring themselves; promote a popular MCP to a first-class integration. Stated
reason: every tool definition costs context on every call. The token figures
quoted for popular MCP servers differ between the episode README and the transcript, so none are
repeated here. Anthropic's [Writing tools for agents][writing-tools] corroborates the direction
("more tools don't always lead to better outcomes"). To measure a definition's cost yourself, run the
same one-line prompt headless with and without the server and compare the cache-creation fields of the
`stream-json` usage output (the 2025-09-16 episode demonstrates this; field meanings in
[CC-prompt-caching-behavior.md](../context-memory/CC-prompt-caching-behavior.md)).

### 10. Command Risk Classification

Deterministic pre-parsing and per-tool permission gating. Each tool has individual allow, ask, and deny rules with pattern matching. Auto-mode classifier auto-approves low-risk actions; safety classifier handles dangerous commands.

*Speculative reads (single-source, hypothetical).* In the 2026-01-06 latency episode a host sketched
pre-running read-only tool calls while the user is still typing, with every write tool blocked, to hide
latency at the cost of extra spend. It was a design sketch, not a shipped feature. Different mechanism
from speculation during code generation in
[programmatic-tool-calling-analysis.md](../../non-cc/protocols/programmatic-tool-calling-analysis.md).

### 11. Single-Purpose Tool Design

Replaces general shell with purpose-built tools for common operations: FileReadTool, FileEditTool, GrepTool, GlobTool. Typed inputs, constrained scope, dedicated permission rules.

**Result shape (single-source, [ai-that-works][aiw-talks] 2025-10-21).** A host who built a small agentic
retrieval agent live reported that the details that mattered were in tool results, not tool prompts:
paths printed relative to an injected working directory, an explicit truncation notice that says what was
cut and how to continue, timeouts on every subprocess call, and a parse-error nudge shown to the model
once and then dropped from history. Anthropic's [Writing tools for agents][writing-tools] supports the
truncation and error points (steer the agent with instructions when truncating; actionable errors over
opaque codes) and states that Claude Code caps tool responses at 25,000 tokens by default (read
2026-11-22). The relative-path and timeout points rest on the talk alone.

## Category 4: Automation (1 pattern)

### 12. Deterministic Lifecycle Hooks

Shell commands fire automatically at specific agent lifecycle points, outside the prompt. 25+ hook points at the time of the leak analysis (33 documented events as of 2026-11-15, see the matrix below): `PreToolUse`, `PostToolUse`, `SessionStart`, `CwdChanged`. Mandatory actions belong in hooks, not instructions.

**Evidence: a Stop hook as the goal check (KernelSeek).** In *Ask, Don't Equip* (Oliaro et al.,
Snowflake AI Research and CMU, [arXiv 2611.03517][kernelseek]), both arms ran in Claude Code
(`claude-opus-4-8` headless for the tool-rich baseline). KernelSeek kept the harness minimal, enforced
the goal as a computed predicate in a Stop hook, and had a human ask short questions at decision
points, later distilled into a 101-entry question bank packaged as a skill. Its attention kernel
reached 1.13× FlashAttention-3 against 0.48× for the baseline (Table 2), from a single run per arm. Two
cautions from the paper: the one time the hook delegated its verdict to a model judge, "it accepted a
premature claim that a human then overturned", and the baseline's knowledge store was "actively
harmful". Code: [`Snowflake-AI-Research/flash-cuda`][flash-cuda] (Apache-2.0).

**Cross-ref**: This repo documents the full hook lifecycle in [CC-hooks-system-analysis.md](../configuration/CC-hooks-system-analysis.md).

[HumanLayer][humanlayer] began as a structured approval-gate SDK that intercepts agent
tool calls for human review before execution. This is complementary to CC's built-in
permission prompts and `PermissionRequest` hooks: CC's hooks handle automated allow/deny
logic, while an approval gate adds a structured human-in-the-loop layer for cases where
automated approval rules are insufficient.

**Status as of 2026-11-22 (first-party sources)**: the approval-gate SDK has had no release since 2025-06. The PyPI package
`humanlayer` was last uploaded 2025-06-03 (0.7.9), and the current [repo][humanlayer-gh] no longer
holds an SDK: its README describes a product that runs coding agents (Claude Code, Codex, OpenCode, Pi)
on your machines and lets a team steer them from a desktop app, a web app and a per-host daemon
(Apache-2.0 per the LICENSE file; 12.9k stars; last push 2026-11-22; download via the
[site][humanlayer] and release notes, 0.202.0 dated 2026-11-14, rather than GitHub releases, which hold
only nightly pre-releases). The earlier name "CodeLayer" (used in 2025 [ai-that-works](https://github.com/ai-that-works/ai-that-works) episodes) is not used on the current README or site;
`codelayer` survives as an internal agent module in the daemon source. The tool passes the
[pruning filter](../../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter)
(usable artifact, alive, 12.9k stars). Treat it as a candidate for team-level orchestration of
coding agents, not as an approval-gate library. Practitioner context: [Ralph enhancement research](CC-ralph-enhancement-research.md),
[extended context analysis](../context-memory/CC-extended-context-analysis.md).

## Author

[Bilgin Ibryam](https://github.com/bibryam) -- Principal PM at Diagrid (Dapr). Apache Software Foundation Member. Previously 9 years at Red Hat, before that BBC News. Author of *Kubernetes Patterns* (O'Reilly, 2nd ed. 2023), *Camel Design Patterns*, and the new [Prompt Patterns](https://www.promptpatterns.dev/) catalog.

Pattern taxonomist by trade: Kubernetes patterns -> Camel patterns -> Prompt patterns -> Agentic harness patterns.

## Sources

- [12 Agentic Harness Patterns from Claude Code](https://generativeprogrammer.com/p/12-agentic-harness-patterns-from) (2026-04-05)
- [Practical Lessons From the Claude Code Leak](https://generativeprogrammer.com/p/practical-lessons-from-the-claude) (2026-04-03)
- [Skill Issue: Harness Engineering for Coding Agents][skill-issue-post] (Kyle, hlyr.dev, 2026-03-12) — harness engineering framing, HumanLayer mention
- Repos and releases (`gh api`, 2026-11-18): [claude-agent-sdk-python][sdk-py] (MIT, v0.2.184), [claude-agent-sdk-typescript][sdk-ts] (Anthropic Commercial Terms per its LICENSE file), [langchain-ai/deepagents][deepagents-gh] (MIT, 0.7.39), [earendil-works/pi][pi-gh] (MIT, v1.5.2; eight built-in tools per its [extensions doc][pi-ext]), [HKUDS/OpenHarness][openharness-gh] (MIT, v0.1.9)
- [Agent SDK overview][agent-sdk-docs] and [Writing tools for agents][writing-tools] (Anthropic; read 2026-11-18) — build-vs-adopt section; licenses and versions from each repo's LICENSE file and releases via `gh api`, 2026-11-18
- [ai-that-works 2025-09-16, "Bash vs. MCP"][aiw-2025-09-16] — practitioner talk (BoundaryML and HumanLayer hosts; a conversation, not shipped code), read 2026-11-22: measuring tool-definition token cost from `stream-json` usage
- [ai-that-works 2025-10-21, "Agentic RAG + Context Engineering"][aiw-2025-10-21] (RAG: retrieval-augmented generation) — practitioner talk (BoundaryML and HumanLayer hosts; a conversation, not shipped code), read 2026-11-22: tool-result shape
- [ai-that-works 2025-10-28, "Ralph Wiggum under the hood"][aiw-2025-10-28] — practitioner talk (BoundaryML and HumanLayer hosts; a conversation, not shipped code), read 2026-11-22: back pressure, one step per loop
- [ai-that-works 2026-01-06, "Understanding Latency in AI Applications"][aiw-2026-01-06] — practitioner talk (BoundaryML and HumanLayer hosts; a conversation, not shipped code), read 2026-11-22: speculative reads (design sketch)
- [ai-that-works 2026-01-27, "No Vibes Allowed"][aiw-2026-01-27] — practitioner talk (BoundaryML and HumanLayer hosts; a conversation, not shipped code), read 2026-11-22: questions, then blind research
- [ai-that-works 2026-02-10, "Agentic Backpressure Deep Dive"][aiw-2026-02-10] — practitioner talk (BoundaryML and HumanLayer hosts; a conversation, not shipped code), read 2026-11-22: proof before research
- [ai-that-works 2026-02-24, "No Vibes Allowed February"][aiw-2026-02-24] — practitioner talk (BoundaryML and HumanLayer hosts; a conversation, not shipped code), read 2026-11-22: learning tests in a live session
- [ai-that-works 2026-03-24, "MCP is Dead?"][aiw-2026-03-24] — practitioner talk (BoundaryML and HumanLayer hosts; a conversation, not shipped code), read 2026-11-22: MCP vs first-party decision rule
- [HumanLayer][humanlayer] · [repo][humanlayer-gh] (`gh api` and README, PyPI JSON, release notes; read 2026-11-22) — original approval-gate SDK (dormant, last PyPI upload 2025-06-03) and current multiplayer coding-agent workspace
- [ARCBench (arXiv 2611.03223)][arcbench] — rule compliance after context compaction
- [Unsupported policy in hand-off summaries (arXiv 2611.06545)][handoff-paper] · [code][handoff-audit] — hand-off summaries that invent approvals or restrictions
- [KernelSeek (arXiv 2611.03517)][kernelseek] · [code][flash-cuda] — Stop-hook goal predicate, question bank as a skill
- [Kubernetes Patterns (O'Reilly)](https://k8spatterns.com/)
- [Prompt Patterns catalog](https://www.promptpatterns.dev/)
- [The Generative Programmer Substack](https://generativeprogrammer.com/)
- ["Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems" (arXiv 2604.14228)](https://arxiv.org/abs/2604.14228) — academic design-space analysis of CC's source (Liu et al., 2026); companion code: [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code)
- ["Applying Anthropic Primitives at Large Enterprises: Harness Paradigm for Knowledge Work" (arXiv 2608.20622)](https://arxiv.org/abs/2608.20622) — Salapa, 2026-08-20; harness-as-enterprise-infrastructure position paper
- ["An Empirical Study of Harness Design for Coding Agents" (arXiv 2609.20804)](https://arxiv.org/abs/2609.20804) — Fan et al. (UMass Amherst / Zoom / Emory / UNC Charlotte), 2026-09-17; 176-setting component ablation study

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

**Companion products**: [Claude Security][claude-security] (managed hosted product for multi-project vuln discovery with false-positive reduction); [Project Glasswing][glasswing], announced 2026-04-07, an Anthropic initiative with named launch partners (AWS, Apple, Microsoft, the Linux Foundation and others) to secure critical software using the gated Claude Mythos Preview. On 2026-10-06 Anthropic launched an expanded Cyber Verification Program with three access tiers and said existing Glasswing members "will transition to the Specialized Access tier".

[dcrh]: https://github.com/anthropics/defending-code-reference-harness
[glasswing]: https://www.anthropic.com/glasswing
[claude-security]: https://claude.com/product/claude-security
[skill-issue-post]: https://www.hlyr.dev/blog/skill-issue-harness-engineering-for-coding-agents
[humanlayer]: https://www.humanlayer.dev/
[aiw-talks]: https://github.com/ai-that-works/ai-that-works/tree/main
[aiw-2025-09-16]: https://github.com/ai-that-works/ai-that-works/tree/main/2025-09-16-coding-agent-tools-bash-vs-mcp
[aiw-2025-10-21]: https://github.com/ai-that-works/ai-that-works/tree/main/2025-10-21-agentic-rag-context-engineering
[aiw-2025-10-28]: https://github.com/ai-that-works/ai-that-works/tree/main/2025-10-28-ralph-wiggum-coding-agent-power-tools
[aiw-2026-01-06]: https://github.com/ai-that-works/ai-that-works/tree/main/2026-01-06-latency
[aiw-2026-01-27]: https://github.com/ai-that-works/ai-that-works/tree/main/2026-01-27-no-vibes-allowed
[aiw-2026-02-10]: https://github.com/ai-that-works/ai-that-works/tree/main/2026-02-10-agentic-backpressure-deep-dive
[aiw-2026-02-24]: https://github.com/ai-that-works/ai-that-works/tree/main/2026-02-24-no-vibes-february
[aiw-2026-03-24]: https://github.com/ai-that-works/ai-that-works/tree/main/2026-03-24-mcp-is-dead
[humanlayer-gh]: https://github.com/humanlayer/humanlayer

## Academic Design-Space Analysis (arXiv 2604.14228)

["Dive into Claude Code: The Design Space of Today's and Future AI Agent Systems"](https://arxiv.org/abs/2604.14228) (Liu, Zhao, Shang, Shen, 2026) reverse-engineers CC's published TypeScript source — an academic complement to Ibryam's pattern taxonomy above, framing the same artifact as a *design space*. It extracts five design motivations and traces them to concrete mechanisms:

- **Seven-mode permission system** (leak-era count; the docs list six modes as of 2026-11-15) + an ML-based command risk classifier — cf. patterns 9–10 (Progressive Tool Expansion, Command Risk Classification).
- **Five-layer context-compaction pipeline** — cf. pattern 5 (Progressive Context Compaction).
- **Four extensibility mechanisms** — MCP, plugins, skills, hooks.
- **Subagent + worktree delegation** and append-oriented session management.

It compares CC against a second system ("OpenClaw") to show how deployment context drives divergent architectural choices, and closes with six open design directions. Cross-ref: [CC-reverse-engineering-landscape.md](../../cc-community/CC-reverse-engineering-landscape.md) for the broader source/binary analysis lineage.

### Enterprise Harness-as-Infrastructure Position (arXiv 2608.20622)

[Applying Anthropic Primitives at Large Enterprises: Harness Paradigm for Knowledge Work][salapa-harness] (George Juraj Salapa, submitted 2026-08-20) argues the coding-agent harness should be treated as enterprise infrastructure rather than a coding tool. It converges on three claims from recent work: harnesses suffice at the task level and outperform more elaborate agent architectures on enterprise work; harness choice accounts for more of the variance in benchmark results than model choice does; and the gap between that finding and enterprise adoption is governance, not capability. The proposed architecture — built on a reference harness the paper calls "microcc" — runs one harness unmodified as the backbone across every deployment, so reviewing what gets built collapses to reading its instructions file, via four mechanisms: credential-scoped tooling (one generic request tool plus a scoped credential per backend, instead of hand-built methods), authorization logic kept outside the harness (letting one artifact serve as a cron backbone, a chat-surface engine, and a terminal tool), and registration as a side effect of pushing code (turning an access audit into a text-file review).

### Empirical Study of Harness Design Components (arXiv 2609.20804)

[An Empirical Study of Harness Design for Coding Agents][fan-harness-study] (Fan, Zhang, Ma, Hu, Wang, Song, Liu, Zamani, Wang — UMass Amherst, Zoom Video Communications, Emory University, UNC Charlotte; submitted 2026-09-17) decomposes the harness into individual components instead of treating it as a monolith, evaluating **176 matched settings** — five context-management strategies × four context-window budgets, plus targeted ablations of planning and action space — across four models on two benchmarks. Findings: context management matters more as the context budget shrinks, mainly by preventing overflow failures; rule-based filtering before LLM-based summarization is the most cost-efficient combination; planning scaffolds weaker models but mostly adds cost for stronger ones; and bash-capable models are cheaper with a bash-only interface on command-line tasks, while weaker models do better with predefined tools. Positioned as a modular framework for tailoring harness design to a model's capability and compute budget — an empirical complement to Ibryam's pattern taxonomy and Liu et al.'s design-space analysis above.

[salapa-harness]: https://arxiv.org/abs/2608.20622
[fan-harness-study]: https://arxiv.org/abs/2609.20804

## Cross-Harness Matrix (checked 2026-11-15)

How five terminal harnesses implement the mechanics behind the patterns above. Cells come from each
vendor's own docs read on 2026-11-15 (links in the table notes); "not documented" means the pages read
are silent, not that the feature is absent. Per-tool depth lives in the analysis docs:
[Codex CLI](../../non-cc/coding-agents/codex-cli-analysis.md),
[Gemini CLI](../../non-cc/coding-agents/gemini-cli-analysis.md),
[OpenCode](../../non-cc/coding-agents/opencode-analysis.md),
[Pi](../../non-cc/coding-agents/pi-analysis.md). Headless sign-in and billing are compared in
[CC-web-auth-setup-analysis.md § Other Coding CLIs](../ci-remote/CC-web-auth-setup-analysis.md#other-coding-clis-headless-sign-in-and-billing)
and not repeated here. Image, PDF, video and voice input across 15 harnesses are compared in
[coding-agents-comparison-landscape.md](../../non-cc/coding-agents/coding-agents-comparison-landscape.md).

Status 2026-11-18: the Gemini CLI column describes the repository as read on 2026-11-15; Google stopped serving free, AI Pro, AI Ultra and Google One users on 2026-06-18 and points them to Antigravity CLI ([tier reconciliation](../../non-cc/coding-agents/gemini-cli-analysis.md)). Antigravity CLI is not a column here; its sandbox, resume and headless docs are in [antigravity-analysis.md](../../non-cc/coding-agents/antigravity-analysis.md#antigravity-cli-agy-first-party-docs-checked-2026-11-18).

What each system saves on resume, and what it does not restore, is in [workflow-frameworks-landscape.md § Checkpoint and resume matrix](../../non-cc/frameworks/workflow-frameworks-landscape.md#checkpoint-and-resume-matrix).

| Mechanic | Claude Code | Codex CLI | Gemini CLI | OpenCode | Pi |
|---|---|---|---|---|---|
| Built-in tools | Dedicated file, search and shell tools plus MCP ([inventory](../configuration/CC-tools-inventory.md)) | Not enumerated on the pages read; MCP via `config.toml` | File system, shell, web fetch/search, plus MCP ([README][gem-readme]) | Including `read`, `write`, `edit`, `patch`, `glob`, `grep`, `shell`, `webfetch`, `websearch`, `skill`, `subagent`, `question` ([tools][oc-tools], [permissions][oc-perm]) | Eight: `read`, `bash`, `powershell`, `edit`, `write`, `grep`, `find`, `ls` ([extensions][pi-ext]) |
| Sandbox | Bash sandbox, off by default; Seatbelt on macOS, bubblewrap on Linux/WSL2 ([docs][cc-sandbox]) | OS sandbox: Seatbelt, `bwrap` + seccomp, Windows MXC; network off by default ([docs][codex-sec]) | Opt-in via `-s`, `GEMINI_SANDBOX` or settings; Seatbelt profiles, Docker, Podman, `runsc`, `lxc` ([docs][gem-sandbox]) | Not documented on the permissions, tools and config pages read | None built in; containerize it (Docker, Gondolin micro-VM, OpenShell) ([README][pi-readme]) |
| Permissions | Six modes (`default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`) plus allow/ask/deny rules ([docs][cc-modes]) | Sandbox mode (`read-only`, `workspace-write`, `danger-full-access`) crossed with approval policy (`on-request`, `never`, `granular`); `approvals_reviewer = "auto_review"` routes approvals to a reviewer agent ([docs][codex-sec]) | Policy engine with rules per mode: `default`, `autoEdit`, `plan`, `yolo` ([docs][gem-policy]) | Ordered `permissions` rules, effect `allow`/`deny`/`ask`, last match wins; separate tighten-only `policies` ([docs][oc-perm]) | None built in; an extension can block in `tool_call` ([README][pi-readme], [extensions][pi-ext]) |
| Compaction | Automatic, plus `/compact` ([docs][cc-how]) | Automatic and `/compact`; the `PreCompact`/`PostCompact` hook trigger is `manual` or `auto` ([hooks][codex-hooks], [commands][codex-cmds]) | Automatic at 50% of context by default (`model.compressionThreshold`), plus `/compress` ([configuration][gem-config], [commands][gem-commands]) | Automatic by default, keeps about 15,000 recent tokens ([docs][oc-compaction]) | Automatic when context passes window minus `reserveTokens` (default 16,384), plus `/compact` ([docs][pi-compaction]) |
| Hooks (documented event rows or headings; counts are not capability ratings) | 33 events in the lifecycle table ([docs][cc-hooks]) | 14 events, including `PreCompact`, `PermissionRequest`, `SubagentStart` ([docs][codex-hooks]) | 11 events, including `BeforeTool`, `PreCompress` ([docs][gem-hooks]) | Plugins "add tools, hooks, integrations, commands, agents"; event list not read ([docs][oc-build-plugin]) | Extension events, e.g. `tool_call` (can block or mutate), `session_before_compact` ([docs][pi-ext]) |
| Resume | `--continue`, `--resume`, fork, rewind checkpoints ([docs][cc-how], [CLI][cc-cli]) | `codex resume`, `/resume`, `/fork`; non-interactive `codex exec resume [id\|name]` with `--last` and `--all` (re-checked 2026-11-18, [commands][codex-cmds]) | `--resume` (latest, index or UUID), `/resume`, tagged checkpoints, `/rewind`, `/restore` (index and UUID re-checked 2026-11-18; [sessions][gem-session], [commands][gem-commands]) | Sessions live in a shared background server; resume flags not documented on the pages read ([CLI][oc-cli]) | `--continue`, `--resume`, `/resume`, `/fork`, tree-structured branches ([docs][pi-sessions]) |

### Which patterns each harness shows

Only patterns the vendor docs make checkable are compared. Not compared here: 2 (scoped assembly),
3 (tiered memory), 4 (dream consolidation), 8 (fork-join), 9 (progressive tool expansion).

| Pattern | Claude Code | Codex CLI | Gemini CLI | OpenCode | Pi |
|---|---|---|---|---|---|
| 1 Persistent instruction file | `CLAUDE.md` | `AGENTS.md` | `GEMINI.md`, hierarchical (`/memory`) | `AGENTS.md` (per our [OpenCode doc](../../non-cc/coding-agents/opencode-analysis.md)) | `AGENTS.md`, `SYSTEM.md` (per our [Pi doc](../../non-cc/coding-agents/pi-analysis.md)) |
| 5 Compaction (single-stage; the pattern above is multi-stage) | Automatic plus `/compact` | Automatic plus `/compact` | Automatic plus `/compress` | Automatic | Automatic plus `/compact` |
| 6 Explore-plan-act | Plan mode | `/plan` | `/plan`, read-only | `plan` agent, edits denied except plan files | Skipped by design ([README][pi-readme]) |
| 7 Context-isolated subagents | Yes | Subagents exist (`/subagents`, `SubagentStart` hook); isolation not verified | Subagents exist (`/agents`); isolation not verified | `subagent` permission, shipped `general` and `explore` agents | Skipped by design ([README][pi-readme]) |
| 10 Command risk classification | Rules plus auto-mode classifier | Rules plus optional `auto_review` reviewer agent | Per-tool rules by mode | Per-resource rules | None built in |
| 11 Single-purpose tools | Yes | Not documented on the pages read | Partial: three tool categories, one of them general shell | Yes | Yes |
| 12 Lifecycle hooks | 33 events | 14 events | 11 events | Via plugins | Via extensions |

**Reading it.** All three of Claude Code, Codex and Gemini CLI pair an OS sandbox with approval rules;
Codex turns its sandbox on by default, while Claude Code and Gemini CLI make it opt-in; OpenCode ships permission rules and, on the pages read,
no sandbox; Pi pushes both sandbox and permissions to the user. Hook coverage runs from a fixed event
table (Claude Code, Codex, Gemini CLI) to a code-level extension API (Pi, OpenCode). Gemini CLI is
now aimed at Code Assist Standard/Enterprise accounts, plus legacy paid API or Vertex keys, per its [README][gem-readme]. OpenCode's current docs are the V2 line, which renamed `permission`/`bash`/`task`
to `permissions`/`shell`/`subagent` ([permissions][oc-perm]); its analysis doc cites v1.17.7.

[gem-readme]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/README.md
[gem-sandbox]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/sandbox.md
[gem-policy]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/reference/policy-engine.md
[gem-hooks]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/hooks/index.md
[gem-session]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/session-management.md
[gem-commands]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/reference/commands.md
[gem-config]: https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md
[codex-sec]: https://learn.chatgpt.com/docs/agent-approvals-security
[codex-hooks]: https://learn.chatgpt.com/docs/hooks
[codex-cmds]: https://learn.chatgpt.com/docs/developer-commands?surface=cli
[oc-tools]: https://opencode.ai/docs/tools
[oc-perm]: https://opencode.ai/docs/permissions
[oc-compaction]: https://opencode.ai/docs/compaction
[oc-build-plugin]: https://opencode.ai/docs/build/plugins
[oc-cli]: https://opencode.ai/docs/cli
[pi-readme]: https://github.com/earendil-works/pi/blob/main/README.md
[pi-ext]: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md
[pi-compaction]: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/compaction.md
[pi-sessions]: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/sessions.md
[cc-sandbox]: https://code.claude.com/docs/en/sandboxing
[cc-modes]: https://code.claude.com/docs/en/permission-modes
[cc-hooks]: https://code.claude.com/docs/en/hooks
[cc-how]: https://code.claude.com/docs/en/how-claude-code-works
[cc-cli]: https://code.claude.com/docs/en/cli-reference

## Build vs Adopt a Harness (checked 2026-11-18)

Three levels, from least to most inherited. The choice is about how much of the loop, tool set and
safety layer you want to own, not about capability: the fixed-model evidence in
[agent-evaluation-metrics-landscape.md § Cost-Performance Efficiency](../../sdlc-lcm/agent-evaluation-metrics-landscape.md#cost-performance-efficiency-pareto)
finds harness choice moves cost more than score on coding tasks, so measure before assuming a custom
loop buys anything.

1. **Minimal loop on a client SDK.** Anthropic's own docs name two options: write the tool loop
   yourself, or let the client SDK's beta tool runner drive it ([Agent SDK overview][agent-sdk-docs]).
   You then own permissions, sandboxing, compaction and resume, the mechanics compared in the
   [Cross-Harness Matrix](#cross-harness-matrix-checked-2026-11-15).
2. **Tool-set design (applies at every level).** Anthropic's [Writing tools for agents][writing-tools]
   (2025-09-11) advises a few tools aimed at high-impact workflows rather than wrapping every API
   endpoint, consolidating multi-step operations, prefixing related tools, returning token-efficient
   and meaningful output, and iterating against evals with held-out tasks. Pi ships eight built-in
   tools and leaves sandboxing and permissions to the user (matrix above). The harness-design study
   above ([2609.20804](#empirical-study-of-harness-design-components-arxiv-260920804)) found a
   bash-only interface cheaper for bash-capable models on command-line tasks, while weaker models did
   better with predefined tools.
3. **Adopt a harness and extend it.**

| Option | What you inherit | License and version (as of 2026-11-18) | Caveat |
|---|---|---|---|
| Claude Agent SDK (Python, TypeScript) | Claude Code's built-in tools, hooks, subagents, MCP, permissions, sessions; the SDK runs the Claude Code binary ([docs][agent-sdk-docs]) | Python repo: MIT file, v0.2.184 (2026-11-18). TypeScript repo: LICENSE file points to Anthropic's Commercial Terms; the docs say use is governed by those terms | Third parties may not offer claude.ai login or rate limits for products built on it; use API-key auth (per the docs) |
| [deepagents](../../non-cc/frameworks/deepagents-analysis.md) | Sub-agents with isolated context, filesystem tools, context offloading, sandboxed shell, memory, skills, MCP, human approval (per its README); built on LangGraph | MIT, deepagents 0.7.39 (2026-11-16) | Model-agnostic Python library; version cadence is fast, pin it |
| [Pi](../../non-cc/coding-agents/pi-analysis.md) | Eight-tool minimal terminal agent with an extension API | MIT, v1.5.2 (2026-11-10) | No built-in sandbox or permissions (matrix above) |
| [OpenHarness](../../non-cc/frameworks/openharness-analysis.md) | Python harness infrastructure with tools, skills, memory and multi-agent coordination (README) | MIT, latest GitHub release v0.1.9 (2026-05-07); last push 2026-06-04 | Pre-1.0 and quiet for five months; the README names v0.1.7 (2026-04-18) as latest, so its version note lags the releases page |

**Rule of thumb (our judgment, not a sourced finding).** Start from the minimal loop if the agent has
a handful of tools and you need full control; adopt the Agent SDK if you want Claude Code's behavior
inside your own application; adopt deepagents or Pi if you need a non-Claude model or a smaller
surface. Re-run the same task set on two candidates before committing, holding model, tools, prompts
and budget fixed.

[agent-sdk-docs]: https://code.claude.com/docs/en/agent-sdk/overview
[sdk-py]: https://github.com/anthropics/claude-agent-sdk-python
[sdk-ts]: https://github.com/anthropics/claude-agent-sdk-typescript
[deepagents-gh]: https://github.com/langchain-ai/deepagents
[pi-gh]: https://github.com/earendil-works/pi
[openharness-gh]: https://github.com/HKUDS/OpenHarness
[writing-tools]: https://www.anthropic.com/engineering/writing-tools-for-agents

## Action Items

- [ ] Map remaining patterns to existing analyses (6/12 mapped above)
- [ ] Track Ibryam's Prompt Patterns catalog for convergence with CC skills format
- [ ] Monitor for community implementations of these patterns outside CC

[arcbench]: https://arxiv.org/abs/2611.03223
[handoff-paper]: https://arxiv.org/abs/2611.06545
[handoff-audit]: https://github.com/Chuw1/handoff-audit
[kernelseek]: https://arxiv.org/abs/2611.03517
[flash-cuda]: https://github.com/Snowflake-AI-Research/flash-cuda
