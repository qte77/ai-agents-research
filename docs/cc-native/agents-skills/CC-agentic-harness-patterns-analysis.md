---
title: 12 Agentic Harness Patterns (Bilgin Ibryam)
source: https://generativeprogrammer.com/p/12-agentic-harness-patterns-from
purpose: Taxonomy of reusable harness-level patterns extracted from the Claude Code source leak.
status: research
created: 2026-04-06
updated: 2026-11-27
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

Shell commands fire automatically at specific agent lifecycle points, outside the prompt. 25+ hook points at the time of the leak analysis (34 documented events (checked 2026-11-26), see the matrix below): `PreToolUse`, `PostToolUse`, `SessionStart`, `CwdChanged`. Mandatory actions belong in hooks, not instructions.

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
- Second matrix table (read 2026-11-27): vendor docs for [Copilot CLI][m7-cp-ref], [VS Code agents][m7-vs-tools], [Cursor][m7-cu-agent], [Cline][m7-cl-cli], [Aider][m7-ai-cmds], [Amp][m7-am-tools] and [Windsurf as Devin Desktop][m7-ws-local]; per-cell links in the table
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

How five terminal harnesses (first table) and seven more (second table, every row read 2026-11-27) implement the mechanics behind the patterns above. Cells come from each
vendor's own docs read on 2026-11-15 for the first six rows and 2026-11-27 for the seven rows marked so (links in the table notes); "not documented" means the pages read
are silent, not that the feature is absent. Per-tool depth lives in the analysis docs:
[Codex CLI](../../non-cc/coding-agents/codex-cli-analysis.md),
[Gemini CLI](../../non-cc/coding-agents/gemini-cli-analysis.md),
[OpenCode](../../non-cc/coding-agents/opencode-analysis.md),
[Pi](../../non-cc/coding-agents/pi-analysis.md). Headless sign-in and billing are compared in
[CC-web-auth-setup-analysis.md § Other Coding CLIs](../ci-remote/CC-web-auth-setup-analysis.md#other-coding-clis-headless-sign-in-and-billing)
and not repeated here. Image, PDF, video and voice input across 15 harnesses are compared in
[coding-agents-comparison-landscape.md](../../non-cc/coding-agents/coding-agents-comparison-landscape.md).

Status 2026-11-18: the Gemini CLI column describes the repository as read on 2026-11-15; Google stopped serving free, AI Pro, AI Ultra and Google One users on 2026-06-18 and points them to Antigravity CLI ([tier reconciliation](../../non-cc/coding-agents/gemini-cli-analysis.md)). Antigravity CLI is not a column here; its sandbox, resume and headless docs are in [antigravity-analysis.md](../../non-cc/coding-agents/antigravity-analysis.md#antigravity-cli-agy-first-party-docs-checked-2026-11-18).

Status 2026-11-27: the last seven rows (instruction and memory files through cloud or remote runs) were read from each vendor's docs on 2026-11-27; the first six rows are from 2026-11-15 and were not re-read. This applies to the first table; the second table was read in full on 2026-11-27. "Not documented" again means the pages read are silent.

What each system saves on resume, and what it does not restore, is in [workflow-frameworks-landscape.md § Checkpoint and resume matrix](../../non-cc/frameworks/workflow-frameworks-landscape.md#checkpoint-and-resume-matrix).

| Mechanic | Claude Code | Codex CLI | Gemini CLI | OpenCode | Pi |
|---|---|---|---|---|---|
| Built-in tools | Dedicated file, search and shell tools plus MCP ([inventory](../configuration/CC-tools-inventory.md)) | Not enumerated on the pages read; MCP via `config.toml` | File system, shell, web fetch/search, plus MCP ([README][gem-readme]) | Including `read`, `write`, `edit`, `patch`, `glob`, `grep`, `shell`, `webfetch`, `websearch`, `skill`, `subagent`, `question` ([tools][oc-tools], [permissions][oc-perm]) | Eight: `read`, `bash`, `powershell`, `edit`, `write`, `grep`, `find`, `ls` ([extensions][pi-ext]) |
| Sandbox | Bash sandbox, off by default; Seatbelt on macOS, bubblewrap on Linux/WSL2 ([docs][cc-sandbox]) | OS sandbox: Seatbelt, `bwrap` + seccomp, Windows MXC; network off by default ([docs][codex-sec]) | Opt-in via `-s`, `GEMINI_SANDBOX` or settings; Seatbelt profiles, Docker, Podman, `runsc`, `lxc` ([docs][gem-sandbox]) | Not documented on the permissions, tools and config pages read | None built in; containerize it (Docker, Gondolin micro-VM, OpenShell) ([README][pi-readme]) |
| Permissions | Six modes (`default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`) plus allow/ask/deny rules ([docs][cc-modes]) | Sandbox mode (`read-only`, `workspace-write`, `danger-full-access`) crossed with approval policy (`on-request`, `never`, `granular`); `approvals_reviewer = "auto_review"` routes approvals to a reviewer agent ([docs][codex-sec]) | Policy engine with rules per mode: `default`, `autoEdit`, `plan`, `yolo` ([docs][gem-policy]) | Ordered `permissions` rules, effect `allow`/`deny`/`ask`, last match wins; separate tighten-only `policies` ([docs][oc-perm]) | None built in; an extension can block in `tool_call` ([README][pi-readme], [extensions][pi-ext]) |
| Compaction | Automatic, plus `/compact` ([docs][cc-how]) | Automatic and `/compact`; the `PreCompact`/`PostCompact` hook trigger is `manual` or `auto` ([hooks][codex-hooks], [commands][codex-cmds]) | Automatic at 50% of context by default (`model.compressionThreshold`), plus `/compress` ([configuration][gem-config], [commands][gem-commands]) | Automatic by default, keeps about 15,000 recent tokens ([docs][oc-compaction]) | Automatic when context passes window minus `reserveTokens` (default 16,384), plus `/compact` ([docs][pi-compaction]) |
| Hooks (documented event rows or headings; counts are not capability ratings) | 34 events in the lifecycle table (checked 2026-11-26) ([docs][cc-hooks]) | 14 events, including `PreCompact`, `PermissionRequest`, `SubagentStart` ([docs][codex-hooks]) | 11 events, including `BeforeTool`, `PreCompress` ([docs][gem-hooks]) | Plugins "add tools, hooks, integrations, commands, agents"; event list not read ([docs][oc-build-plugin]) | Extension events, e.g. `tool_call` (can block or mutate), `session_before_compact` ([docs][pi-ext]) |
| Resume | `--continue`, `--resume`, fork, rewind checkpoints ([docs][cc-how], [CLI][cc-cli]) | `codex resume`, `/resume`, `/fork`; non-interactive `codex exec resume [id\|name]` with `--last` and `--all` (re-checked 2026-11-18, [commands][codex-cmds]) | `--resume` (latest, index or UUID), `/resume`, tagged checkpoints, `/rewind`, `/restore` (index and UUID re-checked 2026-11-18; [sessions][gem-session], [commands][gem-commands]) | Sessions live in a shared background server ([CLI][oc-cli]); `opencode run --continue` and `--session <id>`, `opencode session list` and `opencode session delete` (re-checked 2026-11-27, [commands][oc-cmds]) | `--continue`, `--resume`, `/resume`, `/fork`, tree-structured branches ([docs][pi-sessions]) |
| Instruction and memory files (read 2026-11-27) | `CLAUDE.md` at managed, user, project and local levels, concatenated up the tree; `@path` imports; auto memory on by default locally; `AGENTS.md` read only when no `CLAUDE.md` ([docs][cc-memory]) | `AGENTS.md` (or `AGENTS.override.md`) from `~/.codex` then project root down, 32 KiB cap by default; separate local memory store ([AGENTS.md][cx-agents], [memories][cx-mem]) | `GEMINI.md` (global, workspace, parents), `@file.md` imports, `/memory`; experimental Auto Memory proposes updates for review ([GEMINI.md][gem-md], [Auto Memory][gem-automem]) | `AGENTS.md` global plus each one from workspace upward; falls back to `CLAUDE.md`; memory store not documented on the pages read ([docs][oc-instr]) | Context files `AGENTS.md` or `CLAUDE.md` from agent directory, working directory and parents; `SYSTEM.md` replaces the system prompt; memory: not documented on the pages read ([config][pi-conf]) |
| Skills (read 2026-11-27) | `SKILL.md` folders on the Agent Skills open standard, plus Claude Code extensions such as invocation control ([docs][cc-skills]) | Agent Skills standard; name and description first, full `SKILL.md` on use; in CLI, IDE extension and desktop app ([docs][cx-skills]) | Agent Skills standard; `activate_skill` tool after a consent prompt; `.gemini/skills/` or `.agents/skills/` ([docs][gem-skills]) | `SKILL.md` in `.opencode/skills/<id>`; also searches `~/.claude/skills` and `~/.agents/skills`; loaded by the `skill` tool ([docs][oc-skills]) | Agent Skills specification; `SKILL.md` folders loaded when the description matches ([docs][pi-skills]) |
| Plugins or extensions (read 2026-11-27) | Plugin: folder of skills, agents, hooks, MCP servers; manifest `.claude-plugin/plugin.json`; installed with `/plugin` from marketplaces ([docs][cc-plugins]) | Plugins bundle skills and MCP servers, shared with ChatGPT; `/plugins` browser in the CLI; IDE extension unsupported ([docs][cx-plugins]) | Extensions bundle prompts, MCP servers, commands, themes, hooks, subagents, skills; gallery at geminicli.com ([docs][gem-ext]) | `plugins` config array of npm packages or local directories, plus files in `.opencode/plugins/` ([docs][oc-plugins]) | Packages bundle extensions, skills, prompt templates, themes; `pi install` from npm, git or path ([docs][pi-pkg]) |
| Subagents (read 2026-11-27) | Built-in (Explore, Plan, general-purpose) and custom Markdown in `.claude/agents/`; separate background agents run sessions in parallel ([docs][cc-subagents]) | Built-in `default`, `worker`, `explorer`; custom TOML in `.codex/agents/`; spawns several in parallel, collects results ([docs][cx-sub]) | Built-in `codebase_investigator`, `cli_help`, `generalist` and `browser_agent` (off by default); custom Markdown in `.gemini/agents/`; `@name` forces one; on by default ([docs][gem-sub]) | Markdown agents in `.opencode/agents/` with `mode: subagent`; subagents run in the background as child sessions and report back when idle; concurrency limit not stated ([agents][oc-agents], [tools][oc-tools]) | None built in; README says Pi skips sub-agents ([README][pi-readme]) |
| MCP configuration (read 2026-11-27) | `claude mcp add`; remote HTTP and local stdio; scopes local (default, `~/.claude.json`), project (`.mcp.json`), user ([docs][cc-mcp]) | stdio and streamable HTTP; `config.toml` in `~/.codex` or project `.codex/`; `codex mcp add`, `login` ([docs][cx-mcp]) | `mcpServers` in `settings.json`; stdio, SSE or streamable HTTP; per-server `trust` ([docs][gem-mcp]) | `mcp.servers` in `opencode.jsonc` (V2); local and remote types, OAuth default for remote; `opencode mcp add` ([docs][oc-mcp]) | stdio or streamable HTTP; `~/.pi/agent/mcp.json`, project `.pi/mcp.json` after trust; `pi mcp add` ([docs][pi-mcp]) |
| Headless and CI mode (read 2026-11-27) | `-p`; `--output-format` text, json or stream-json; `--bare`; official `anthropics/claude-code-action@v1` ([docs][cc-headless], [Action][cc-gha]) | `codex exec`; `--json` JSONL, `--output-schema`; read-only sandbox by default; `openai/codex-action@v1` ([exec][cx-exec], [Action][cx-gha]) | `-p` or non-TTY; `--output-format` json or stream-json; Action repo `google-github-actions/run-gemini-cli` exists, its docs not read ([docs][gem-headless], [repo][gem-gha]) | `opencode run`, `--format json` for newline-delimited JSON; the commands page shows a GitHub Actions example with `opencode run --standalone`; a dedicated GitHub page exists only in the previous-version docs ([CLI][oc-cli], [commands][oc-cmds], [v1][oc-gh]) | `--print`, `--mode json` (JSONL), `--mode rpc`; GitHub Action not documented on the pages read ([CLI][pi-cli]) |
| Cloud or remote runs (read 2026-11-27) | Cloud sessions from web, phone, desktop or terminal (`--cloud`, `--teleport`); Remote Control drives a local session from claude.ai or mobile ([cloud][cc-web], [Remote Control][cc-rc]) | Codex Cloud runs tasks in hosted environments, startable from the CLI; remote connections to another computer or SSH host ([cloud][cx-cloud], [remote][cx-remote]) | Vendor-hosted runs not documented on the pages read; it can call remote Agent-to-Agent Protocol (A2A) subagents ([docs][gem-remote]) | Shared background server, `--server <url>` connects a client; `opencode pair --remote` pairs a phone to sessions on your computer; hosted runs not documented on the pages read ([CLI][oc-cli], [mobile][oc-mobile]) | Not documented on the pages read; RPC mode controls a separate Pi process ([CLI][pi-cli]) |

Second table, same rows (read 2026-11-27): GitHub Copilot CLI, VS Code Copilot Chat, Cursor, Cline, Aider, Amp and Windsurf, from each vendor's own docs. Windsurf's docs now live on docs.devin.ai, where the app is Devin Desktop and its default agent is Devin Local, shared with the Devin CLI. Resume cells list flags and commands; what each system restores is in [workflow-frameworks-landscape.md § Checkpoint and resume matrix][m7-resume].

| Mechanic | GitHub Copilot CLI | VS Code Copilot Chat | Cursor | Cline | Aider | Amp | Windsurf (Devin Desktop) |
|---|---|---|---|---|---|---|---|
| Built-in tools | Shell tools (`bash` or `powershell`, plus list, read, write and stop for shell sessions) and file tools (`view`, `create`, `edit`, `apply_patch`); `--available-tools` limits the set ([reference][m7-cp-ref]) | Tools tab in Agent Customizations toggles built-in, extension and MCP tools per harness; built-in shell and browser tools; `#` picks a tool ([docs][m7-vs-tools]) | Search, read, edit, terminal, web search, browser, image generation, ask-question tool, checkpoints ([docs][m7-cu-agent]) | `read_files`, `search_codebase`, `run_commands`, `fetch_web_content`, `apply_patch`, `editor`, `skills`, `ask_question`, `submit_and_exit`, plus MCP tools ([docs][m7-cl-tools]) | Edits files in the chat through edit formats; repo map; slash commands `/run`, `/test`, `/lint`, `/git`, `/web` ([commands][m7-ai-cmds], [modes][m7-ai-modes]) | Listed with `amp tools list`; Task tool for subagents; further tool pages not read ([tools][m7-am-tools]) | Not enumerated on the pages read; hook payloads name `exec` and `edit` tools ([hooks][m7-ws-hooks]) |
| Sandbox | Opt-in: `/sandbox enable` or `--sandbox`; writes limited to the working directory and temp folders, outbound internet on by default, local network off ([docs][m7-cp-sbx]) | Agent sandboxing configured separately; in the Copilot sandbox outbound network is allowed by default; `/sandbox policy` shows the effective limits ([docs][m7-vs-sec]) | Terminal sandbox restricts file and network access; set via Run Modes, `sandbox.json`, or `/sandbox` and `--sandbox <mode>` in the CLI ([terminal][m7-cu-term], [slash commands][m7-cu-slash], [parameters][m7-cu-params]) | No OS sandbox documented for the local agent on the pages read; the CLI has a `CLINE_SANDBOX` "sandbox mode" with its own data directory ([CLI][m7-cl-cli]); Cloud Agents run in an isolated sandbox ([cloud][m7-cl-cloud]) | Not documented on the pages read; the docs sitemap (132 URLs, read 2026-11-27) lists no sandbox page ([sitemap][m7-ai-map]) | Not documented for local runs on the pages read; orbs are cloud sandboxes, one machine per thread ([orbs][m7-am-orbs]) | Devin Local: OS-level sandbox (macOS Seatbelt, Linux `bwrap` and seccomp); filesystem and network filtering; the CLI flag `--sandbox` is marked research preview ([overview][m7-ws-local], [commands][m7-ws-cmds]) |
| Permissions | `--allow-tool` and `--deny-tool` patterns, `--allow-all`, `/permissions`; under allow-all, deny rules and enterprise restrictions still apply ([reference][m7-cp-ref]) | Permission levels (Manual and others) plus saved approvals and scopes; terminal command approvals; sensitive-edit approval ([docs][m7-vs-sec], [tools][m7-vs-tools]) | Terminal commands and MCP calls need approval by default; Run Modes range from an allowlist to an Auto-review classifier, best-effort rather than a hard boundary ([security][m7-cu-sec]) | Auto Approve toggles per category (read, edit, commands, browser); the model flags each command `requires_approval`; CLI defaults to yolo with a prompt, `--auto-approve false` for act mode ([auto approve][m7-cl-auto], [CLI][m7-cl-cli]) | No permission system on the pages read; `/add` puts files in scope, `--yes-always` accepts prompts, `--no-git` stops Git use ([options][m7-ai-opts], [Git][m7-ai-git]) | No approval before running tools by default; `amp.dangerouslyAllowAll`, `amp.mcpPermissions` settings; policy plugin suggested for untrusted repos ([tools][m7-am-tools], [settings][m7-am-set]) | Five modes (Code, Smart, Ask, Plan, Bypass Permissions); allow, ask and deny rules at project, user and organization level ([modes][m7-ws-modes], [permissions][m7-ws-perm]) |
| Compaction | `/compact [focus]`; the `preCompact` hook fires before manual or automatic compaction; background compaction at about 80% per the context article ([compaction by harness](../../non-cc/coding-agents/coding-agents-comparison-landscape.md#context-compaction-by-harness)) ([reference][m7-cp-ref], [hooks][m7-cp-hooks]) | Automatic when the context window fills (setting turns it off); `/compact` or the context-window control ([docs][m7-vs-sess]) | `/summarize` (alias `/compress`) ([slash commands][m7-cu-slash]); `preCompact` hook observes compaction ([hooks][m7-cu-hooks]) | `--compaction agentic\|basic\|off` (default `agentic`) in the CLI; `/smol` compresses history; `/newtask` starts fresh with distilled context ([CLI][m7-cl-cli], [commands][m7-cl-cmds]) | Summarizes chat history past `--max-chat-history-tokens`; `/clear`, `/reset` ([options][m7-ai-opts], [commands][m7-ai-cmds]) | Handoff: ask the agent to start a fresh thread with the context that matters ([threads][m7-am-threads]) | `/compact`; `PostCompaction` hook ([commands][m7-ws-ess], [hooks][m7-ws-hooks]) |
| Hooks (documented event rows or headings; counts are not capability ratings) | 14 events in the table, including `preCompact`, `permissionRequest`, `subagentStart`, `userPromptTransformed` ([docs][m7-cp-hooks]) | Preview; shares the Copilot harness and hook format with Copilot CLI; includes `preCompact`; `.github/hooks` files ([docs][m7-vs-hooks]) | `hooks.json` project or user level; events include `sessionStart`, `preToolUse`, `beforeShellExecution`, `beforeMCPExecution`, `preCompact`, `stop`; loads Claude Code hooks ([docs][m7-cu-hooks]) | SDK plugins hook `beforeRun`, `afterRun`, `beforeModel`, `afterModel`, `beforeTool`, `afterTool`, `onEvent`; `cline hook` handles a payload from stdin; CLI lifecycle hooks in `~/.cline/hooks`, `--hooks-dir`, `CLINE_HOOKS_DIR` ([plugins][m7-cl-sdkplug], [CLI][m7-cl-cli]) | Not documented on the pages read; closest are `--lint-cmd` and `--test-cmd` ([options][m7-ai-opts]) | Plugins react with `amp.on(...)` to `session.start`, `agent.start`, `tool.call`, `tool.result`, `agent.end` ([plugins][m7-am-plug]) | 8 event sections: `PreToolUse`, `PostToolUse`, `PermissionRequest`, `UserPromptSubmit`, `Stop`, `PostCompaction`, `SessionStart`, `SessionEnd`; config in `.devin/hooks.v1.json` ([hooks][m7-ws-hooks], [customizations][m7-ws-cust]) |
| Resume | `--continue`, `--resume`, `/resume`, `--connect` to a remote session, `/rewind` to an earlier turn, restore after a crash, opt-in ([reference][m7-cp-ref]); what is restored: [resume matrix][m7-resume] | Sessions list with Archived and Done filters; resume a saved session; Resume in Terminal continues in Copilot CLI on some session types ([docs][m7-vs-sess]) | `agent ls`, `agent resume`, `--continue`, `--resume=<id>` in the CLI; editor checkpoints restore files ([CLI][m7-cu-cli], [agent][m7-cu-agent]); what is restored: [resume matrix][m7-resume] | `--id <session>` in the CLI, `cline history`; shadow-Git checkpoints with Compare and Restore ([CLI][m7-cl-cli], [checkpoints][m7-cl-ckpt]); what is restored: [resume matrix][m7-resume] | `--restore-chat-history` reloads the chat file; every edit is a Git commit, `/undo` ([options][m7-ai-opts], [Git][m7-ai-git]); what is restored: [resume matrix][m7-resume] | `amp threads continue <id>`; threads open across web, CLI and apps; `amp threads list`, `search` ([threads][m7-am-threads]); what is restored: [resume matrix][m7-resume] | `devin -c`, `devin -r <id>`, `/resume`, `/continue`; `--cloud -r <url>` for cloud sessions ([commands][m7-ws-cmds], [essentials][m7-ws-ess]); the [resume matrix][m7-resume] row covers legacy Cascade, not Devin Local |
| Instruction and memory files (read 2026-11-27) | `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, user files in `~/.copilot/`, `@path` includes ([docs][m7-cp-instr], [reference][m7-cp-ref]); cross-session repository memory per our [Copilot CLI doc](../../non-cc/agents/github-copilot-cli-analysis.md) | `.github/copilot-instructions.md`, `AGENTS.md`, `CLAUDE.md`, `*.instructions.md` with `applyTo`; Copilot Memory (cloud), experimental local-storage option ([instructions][m7-vs-instr], [memory][m7-vs-mem]) | `.cursor/rules/*.mdc` (always, glob, on request) and `AGENTS.md`; no separate memory store on the pages read ([docs][m7-cu-rules]) | `.clinerules/`, `.cline/rules/`, `AGENTS.md`, `~/.agents/AGENTS.md`, and other tools' rule files ([rules][m7-cl-rules], [config][m7-cl-cfg]); Memory Bank is a rules-based practice, not a store ([memory bank][m7-cl-mb]) | `CONVENTIONS.md` loaded with `--read` or `.aider.conf.yml`; no memory store documented on the pages read ([docs][m7-ai-conv]) | `AGENTS.md` in the working directory, parents and subtrees; user `~/.config/amp/AGENTS.md`; `/etc/ampcode/AGENTS.md` ([docs][m7-am-agents]) | `AGENTS.md`, `AGENTS.local.md`, `.devin/rules/*.md` with `trigger` frontmatter, `~/.devin/global_rules.md`; legacy `.windsurf/` rules imported; memory store not documented for Devin Local on the pages read ([docs][m7-ws-cust]) |
| Skills (read 2026-11-27) | `SKILL.md` folders in `.github/skills/`, `.agents/skills/`, `.claude/skills/` and the `~/.copilot/` and `~/.agents/` equivalents; `/skills` manages them ([reference][m7-cp-ref], [docs][m7-cp-skills]) | `.github/skills/`, `~/.copilot/skills/` for the Copilot harness (`.claude/skills/` paths belong to the Claude harness row); a skill can run in a forked context ([docs][m7-vs-skills]) | Agent Skills in `.cursor/skills/`, `.agents/skills/` and the `~/` equivalents ([docs][m7-cu-skills]) | `SKILL.md` in `.cline/skills/`, `.agents/skills/`, `.claude/skills/` and `~/.cline/skills/`; metadata always loaded, body on match ([docs][m7-cl-skills]) | Not documented on the pages read (no skills page in the sitemap) | Skills in `.agents/skills/`, `.claude/skills/`, `~/.agents/skills/`, `~/.config/amp/skills/` ([docs][m7-am-skill]) | `.devin/skills/<name>/`, `.agents/skills/`, legacy `.windsurf/skills/`; global `~/.config/devin/skills/` ([docs][m7-ws-cust]) |
| Plugins or extensions (read 2026-11-27) | Directory with a `plugin.json` manifest, installed from marketplaces with `/plugin`; follows the Agent Plugins format shared across Copilot surfaces ([installing][m7-cp-plug], [plugins][m7-cp-plugc]) | Agent plugins install from marketplaces; skills, MCP servers and hooks appear alongside local ones; Local-harness customizations differ ([docs][m7-vs-plug]) | Plugins follow the Agent Plugins standard (`plugin.json`) or Cursor's own `.cursor-plugin/plugin.json` format, adding rules, agents, commands, hooks ([docs][m7-cu-plug]) | `cline plugin install` from a repository, URL or local path; plugins add tools, hooks and slash commands ([docs][m7-cl-plug]) | Not documented on the pages read (no plugin page in the sitemap) | TypeScript or JavaScript plugin modules in `.amp/plugins/` or `~/.config/amp/plugins/`; add tools, commands, event handlers ([docs][m7-am-plug]) | Plugins bundle skills, rules, hooks, MCP servers and subagents ([docs][m7-ws-cust]) |
| Subagents (read 2026-11-27) | Custom agents (`--agent`; `.github/` or `.claude/` folders), `/fleet` runs parts of a task as parallel subagents, `/subagents` sets models ([reference][m7-cp-ref], [agents][m7-cp-agents]) | Subagents delegate tasks in their own context; nested sessions are separate chats, optionally in a worktree ([docs][m7-vs-sub]) | Built-in subagents plus `.cursor/agents/` and `~/.cursor/agents/`; each in its own context; run in parallel; start from clean context ([docs][m7-cu-sub]) | `spawn_agent` tool; own context window each, run in parallel; approving the spawn approves its actions ([docs][m7-cl-sub]); CLI agent teams ([teams][m7-cl-teams]) | Not documented on the pages read; architect mode pairs an architect model with an editor model, which is a two-model split rather than subagents ([modes][m7-ai-modes]) | Task tool subagents with own context window; named helpers such as the oracle and librarian; automatic or on request ([tools][m7-am-tools], [models and subagents][m7-am-mod]) | Subagents in foreground or background, own conversation chain; custom profiles in `agents/<name>.md` or `agents/<name>/AGENT.md`; a Preview toggle ([docs][m7-ws-sub], [overview][m7-ws-local]) |
| MCP configuration (read 2026-11-27) | `~/.copilot/mcp-config.json`, workspace `.mcp.json`, `--additional-mcp-config` per session; GitHub's own server enabled with a default tool subset ([reference][m7-cp-ref]) | Workspace-root `.mcp.json` offered in the guided add flow; other config locations not read ([docs][m7-vs-mcp]) | `mcp.json`; stdio, SSE and streamable remote with OAuth; all connections need approval ([docs][m7-cu-mcp]) | `mcpServers` in `cline_mcp_settings.json`; `cline mcp add` with stdio or remote transports ([docs][m7-cl-mcp], [tools][m7-cl-tools]) | Not documented on the pages read (no MCP page in the sitemap) | `amp.mcpServers` in settings; `amp mcp add`; local or remote servers ([docs][m7-am-mcp]) | `.devin/mcp_config.json`, local override, user `~/.config/devin/mcp_config.json` ([docs][m7-ws-cust]) |
| Headless and CI mode (read 2026-11-27) | `-p`; `--output-format json` gives JSONL; `--no-ask-user`, `--allow-tool`; a GitHub Actions example is on the page ([docs][m7-cp-prog]) | No CLI print mode on the pages read (Copilot CLI is the terminal path); agent automations run on demand, on a schedule or, in the cloud, on repository events ([automations][m7-vs-auto]) | `agent -p`; `--force` runs without approvals; team admins can disable headless mode ([docs][m7-cu-head]) | `cline "prompt"` runs yolo by default; `--json`; `-p` is plan mode here; `--acp` for editor integration ([CLI][m7-cl-cli]) | `--message`, `--message-file`, `--yes-always`, and a Python scripting interface ([scripting][m7-ai-script], [options][m7-ai-opts]) | `-x` execute mode, piped input, `--stream-json`; `-ox` runs in an orb ([docs][m7-am-exec], [SDK][m7-am-sdk]) | Devin CLI: `devin -p "prompt"` prints and exits; fails in an untrusted directory unless `--respect-workspace-trust false` ([commands][m7-ws-cmds]) |
| Cloud or remote runs (read 2026-11-27) | `/delegate` hands work to the cloud agent for a pull request; `/remote on` steers a running CLI session from another device ([reference][m7-cp-ref]) | Cloud is an execution target of the Copilot harness (experimental); remote agent sessions run on another host; Local harness is deprecated, removal due February 2027 ([docs][m7-vs-harness], [sessions][m7-vs-sess]) | Cloud Agents run in isolated VMs, in parallel, steerable from Slack, Teams, Jira, Linear and GitHub ([docs][m7-cu-cloud]); self-hosted workers ([subagents][m7-cu-sub]) | Cloud Agents: browser task on a GitHub repository, own sandbox, returns a branch and pull request ([docs][m7-cl-cloud]) | Not documented on the pages read; `--watch-files` reacts to comments in files ([options][m7-ai-opts]) | Orbs: cloud sandbox per thread; `amp -ox`; runners; continue a CLI thread across clients ([orbs][m7-am-orbs], [remote][m7-am-remote]) | `devin --cloud` drives Devin Cloud sessions; Agent Command Center manages local and cloud agents ([commands][m7-ws-cmds], [center][m7-ws-acc]) |

Where this table and [§ Context compaction by harness](../../non-cc/coding-agents/coding-agents-comparison-landscape.md#context-compaction-by-harness) differ (VS Code's setting, Cline, Windsurf), that section's cells are from 2026-11-23 and narrower pages; the cells here are the newer read.

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
| 12 Lifecycle hooks | 34 events | 14 events | 11 events | Via plugins | Via extensions |

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
[cc-memory]: https://code.claude.com/docs/en/memory
[cc-skills]: https://code.claude.com/docs/en/skills
[cc-plugins]: https://code.claude.com/docs/en/plugins/overview
[cc-subagents]: https://code.claude.com/docs/en/sub-agents
[cc-mcp]: https://code.claude.com/docs/en/mcp
[cc-headless]: https://code.claude.com/docs/en/headless
[cc-gha]: https://code.claude.com/docs/en/github-actions
[cc-web]: https://code.claude.com/docs/en/claude-code-on-the-web
[cc-rc]: https://code.claude.com/docs/en/remote-control
[cx-agents]: https://learn.chatgpt.com/docs/agent-configuration/agents-md
[cx-mem]: https://learn.chatgpt.com/docs/customization/memories
[cx-skills]: https://learn.chatgpt.com/docs/build-skills
[cx-plugins]: https://learn.chatgpt.com/docs/plugins
[cx-sub]: https://learn.chatgpt.com/docs/agent-configuration/subagents
[cx-mcp]: https://learn.chatgpt.com/docs/extend/mcp
[cx-exec]: https://learn.chatgpt.com/docs/non-interactive-mode
[cx-gha]: https://learn.chatgpt.com/docs/github-action
[cx-cloud]: https://learn.chatgpt.com/docs/cloud
[cx-remote]: https://learn.chatgpt.com/docs/remote-connections
[gem-md]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/gemini-md.md
[gem-automem]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/auto-memory.md
[gem-skills]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/skills.md
[gem-ext]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/extensions/index.md
[gem-sub]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/core/subagents.md
[gem-mcp]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/mcp-server.md
[gem-headless]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/headless.md
[gem-gha]: https://github.com/google-github-actions/run-gemini-cli
[gem-remote]: https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/core/remote-agents.md
[oc-instr]: https://opencode.ai/docs/instructions
[oc-skills]: https://opencode.ai/docs/skills
[oc-plugins]: https://opencode.ai/docs/plugins
[oc-agents]: https://opencode.ai/docs/agents
[oc-mcp]: https://opencode.ai/docs/mcp-servers
[oc-gh]: https://opencode.ai/v1/docs/github/
[oc-cmds]: https://opencode.ai/docs/cli/commands
[oc-mobile]: https://opencode.ai/mobile
[pi-conf]: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/configuration.md
[pi-skills]: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md
[pi-pkg]: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md
[pi-mcp]: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/mcp.md
[pi-cli]: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/cli.md

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

[m7-resume]: ../../non-cc/frameworks/workflow-frameworks-landscape.md#checkpoint-and-resume-matrix
[m7-cp-ref]: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
[m7-cp-sbx]: https://docs.github.com/en/copilot/how-tos/cloud-and-local-sandboxes/using-local-sandboxing
[m7-cp-hooks]: https://docs.github.com/en/copilot/reference/hooks-reference
[m7-cp-instr]: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
[m7-cp-skills]: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-skills
[m7-cp-plug]: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing
[m7-cp-plugc]: https://docs.github.com/en/copilot/concepts/customizations/plugins
[m7-cp-agents]: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli
[m7-cp-prog]: https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/run-cli-programmatically
[m7-vs-tools]: https://code.visualstudio.com/docs/agents/run/tools
[m7-vs-sec]: https://code.visualstudio.com/docs/agents/run/security
[m7-vs-sess]: https://code.visualstudio.com/docs/agents/run/sessions/manage-sessions
[m7-vs-hooks]: https://code.visualstudio.com/docs/agent-customization/hooks
[m7-vs-instr]: https://code.visualstudio.com/docs/agent-customization/custom-instructions
[m7-vs-mem]: https://code.visualstudio.com/docs/agents/run/memory
[m7-vs-skills]: https://code.visualstudio.com/docs/agent-customization/agent-skills
[m7-vs-plug]: https://code.visualstudio.com/docs/agent-customization/agent-plugins
[m7-vs-sub]: https://code.visualstudio.com/docs/agents/run/subagents
[m7-vs-mcp]: https://code.visualstudio.com/docs/agent-customization/mcp-servers
[m7-vs-harness]: https://code.visualstudio.com/docs/agents/run/agent-harnesses
[m7-cu-agent]: https://cursor.com/docs/agent/overview
[m7-cu-term]: https://cursor.com/docs/agent/tools/terminal
[m7-cu-cli]: https://cursor.com/docs/cli/using
[m7-cu-sec]: https://cursor.com/docs/agent/security
[m7-cu-slash]: https://cursor.com/docs/cli/reference/slash-commands
[m7-cu-hooks]: https://cursor.com/docs/hooks
[m7-cu-rules]: https://cursor.com/docs/rules
[m7-cu-skills]: https://cursor.com/docs/skills
[m7-cu-plug]: https://cursor.com/docs/plugins
[m7-cu-sub]: https://cursor.com/docs/subagents
[m7-cu-mcp]: https://cursor.com/docs/mcp
[m7-cu-head]: https://cursor.com/docs/cli/headless
[m7-cu-cloud]: https://cursor.com/docs/cloud-agent
[m7-cu-params]: https://cursor.com/docs/cli/reference/parameters
[m7-cl-tools]: https://docs.cline.bot/tools-reference/all-cline-tools
[m7-cl-cloud]: https://docs.cline.bot/usage/cloud-agents
[m7-cl-auto]: https://docs.cline.bot/features/auto-approve
[m7-cl-cli]: https://docs.cline.bot/cli/cli-reference
[m7-cl-mb]: https://docs.cline.bot/best-practices/memory-bank
[m7-cl-teams]: https://docs.cline.bot/cli/agent-teams
[m7-vs-auto]: https://code.visualstudio.com/docs/agents/run/automations
[m7-cl-cmds]: https://docs.cline.bot/core-workflows/using-commands
[m7-cl-sdkplug]: https://docs.cline.bot/sdk/plugins
[m7-cl-ckpt]: https://docs.cline.bot/core-workflows/checkpoints
[m7-cl-rules]: https://docs.cline.bot/customization/cline-rules
[m7-cl-cfg]: https://docs.cline.bot/getting-started/config
[m7-cl-skills]: https://docs.cline.bot/customization/skills
[m7-cl-plug]: https://docs.cline.bot/customization/plugins
[m7-cl-sub]: https://docs.cline.bot/features/subagents
[m7-cl-mcp]: https://docs.cline.bot/mcp/mcp-overview
[m7-ai-cmds]: https://aider.chat/docs/usage/commands.html
[m7-ai-modes]: https://aider.chat/docs/usage/modes.html
[m7-ai-map]: https://aider.chat/sitemap.xml
[m7-ai-opts]: https://aider.chat/docs/config/options.html
[m7-ai-git]: https://aider.chat/docs/git.html
[m7-ai-conv]: https://aider.chat/docs/usage/conventions.html
[m7-ai-script]: https://aider.chat/docs/scripting.html
[m7-am-tools]: https://ampcode.com/docs/tools
[m7-am-orbs]: https://ampcode.com/docs/orbs
[m7-am-set]: https://ampcode.com/docs/cli/settings
[m7-am-threads]: https://ampcode.com/docs/threads
[m7-am-plug]: https://ampcode.com/docs/customize/plugins
[m7-am-agents]: https://ampcode.com/docs/customize/agents-md
[m7-am-skill]: https://ampcode.com/docs/customize/skills
[m7-am-mod]: https://ampcode.com/docs/models-and-subagents
[m7-am-mcp]: https://ampcode.com/docs/customize/mcp
[m7-am-exec]: https://ampcode.com/docs/cli/execute-mode
[m7-am-sdk]: https://ampcode.com/docs/sdk
[m7-am-remote]: https://ampcode.com/docs/cli/remote-control
[m7-ws-local]: https://docs.devin.ai/desktop/devin-local/overview
[m7-ws-modes]: https://docs.devin.ai/desktop/devin-local/modes
[m7-ws-perm]: https://docs.devin.ai/desktop/devin-local/permissions
[m7-ws-cust]: https://docs.devin.ai/desktop/devin-local/customizations
[m7-ws-hooks]: https://docs.devin.ai/cli/extensibility/hooks/lifecycle-hooks
[m7-ws-cmds]: https://docs.devin.ai/cli/reference/commands
[m7-ws-ess]: https://docs.devin.ai/cli/essential-commands
[m7-ws-sub]: https://docs.devin.ai/cli/subagents
[m7-ws-acc]: https://docs.devin.ai/desktop/agent-command-center
