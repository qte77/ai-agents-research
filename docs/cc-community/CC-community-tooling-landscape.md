---
title: CC Community Tooling Landscape
purpose: Survey of community developer tools that integrate with or enhance Claude Code — context compression, meta-prompting, spec-driven development, agent frameworks, cross-session cost control, source enrichment, provider management, session-workflow enforcement. Memory, code-analysis, and usage-observability tools live in linked topic docs; this doc keeps the cross-tool comparison.
status: research
platform_scope: [claude-code, cursor, codex, gemini-cli, opencode, windsurf, zed, antigravity]
created: 2026-03-13
updated: 2026-11-23
validated_links: 2026-11-12
---

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

| Layer | Mechanism | Tool / Pattern | Evidence (who measured, when) | Known limitation |
|---|---|---|---|---|
| **1 — Env vars** | `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1` (or `"includeGitInstructions": false` in settings) strips the built-in commit/PR instructions and the git status snapshot from context (CC v2.1.69+) | Shell env / `.env` / settings | not measured | The docs state no headless-only scope, so it applies to interactive sessions too (our reading of the [settings reference][cc-settings-ref-git], checked 2026-11-19); cloud sessions never include the snapshot anyway. No source sizes the saving; you lose the built-in git guidance |
| **2 — Native hook filters (DIY)** | `run_silent()` PostToolUse bash wrapper: captures stdout to a temp file, emits `✓ <desc>` on exit 0, surfaces full output only on non-zero exit; pair with failFast flags (`pytest -x`, `jest --bail`, `go test -failfast`) to halt at first failure | CC PostToolUse hook | not measured (pattern from [hlyr-backpressure][hlyr-backpressure], 2025-12-09) | Must be written per project; no packaging or reuse mechanism built in |
| **3 — Wrapper scripts** | RTK intercepts shell command outputs via hooks — see [RTK section above](#rtk-rust-token-killer); a third-party benchmark measured zero savings on `cat`/`grep`/`pytest`/`ruff` | [RTK][rtk-repo] | third-party: this repo owner's run, not RTK's authors: [rtk-839][rtk-839], 2026-03-26 (v0.33.1), see [Independent Benchmark](#independent-benchmark-2026-03-26-v0331) | Does not filter content RTK doesn't recognise; zero gains on passthrough categories |
| **4 — Output-style skills** | caveman and similar skills compress the model's own response verbosity (caveman 4.x also ships a separate input-shrinking proxy, see its entry) | See [CC-community-skills-landscape.md][skills-landscape] | independent: JetBrains, July 2026 — 8.5% fewer output tokens with caveman forced on (a ceiling, p = 0.82 on quality; [details][skills-caveman]) | Output-side only; does not reduce tool or shell output |
| **5 — Context/prompt compression (library)** | Prune low-information tokens from the prompt before the model call — [LLMLingua][llmlingua] (perplexity-based; LLMLingua-2 is task-agnostic and 3–6× faster). *Adjacent mechanism:* [semantic-router][semantic-router] skips the LLM call entirely for recognized intents (routing, not compression) | [LLMLingua][llmlingua] · [semantic-router][semantic-router] | vendor claim, README "up to 20x" (LLMLingua, read 2026-11-22); not measured on a CC workload | General-purpose libraries, **not CC-native** — wire in upstream via a model gateway/proxy or PreToolUse hook |
| **6 — Cross-session learned control** | Learns per repository which tools go unused, which facts the agent keeps rediscovering and when a turn loops, then prunes tools, injects facts or redirects | [TokenEconomizer](#tokeneconomizer-microsoft) | author-run, [paper][tokeneconomizer-paper] (read 2026-11-09), not independently replicated | Early (v0.1.0); savings figures are the authors' own; tool pruning edits `.claude/settings.local.json` |
| **7 — Tool-output sandbox** | Keeps raw tool output out of the context: a hook sends large reads, fetches and shell results to a local sandbox and index, and only a short result or search hit reaches the model | [context-mode][context-mode] (34.4K stars, Elastic License 2.0 — source-available, not open source; `gh api` 2026-11-22) | author-run, bench 2026-11-01 on a 2.0.0 pre-release build: 99.4% median reduction in output *bytes* over 36 rows with 10 KB or more of raw output (bytes, not tokens or session cost) | Savings are per tool call, not per session; the licence bars offering it as a hosted service; needs Node 24.15+ |
| **8 — Compression proxy** | A local proxy compresses what the agent sends to the model (repeated JSON, logs, search results); `headroom wrap claude` routes Claude Code through it | [Headroom][headroom] (80.4K stars, Apache-2.0; `gh api` 2026-11-22) | author-run, seeded benchmark (seed 20260902; README read 2026-11-22): 21–57% fewer input tokens on four agent scenarios, 90%+ on repeated JSON/log lines, little on prose | Sits between agent and provider (a proxy, not a hook); savings scale with repetitive payloads; the README labels output-token savings an estimate |

Layer 1 cross-ref: [CC-changelog-feature-scan.md](../cc-native/configuration/CC-changelog-feature-scan.md) — env var inventory.
Layer 2 cross-ref: [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md) — PostToolUse hook mechanism.
Layers 7–8 note: both were added 2026-11-22 under the pruning rule (alive, 34K+ stars each, measured by their own authors only). Code-index MCPs that cut tokens by answering from an index instead of file reads (Serena and similar) sit in [CC-code-tooling-landscape.md](CC-code-tooling-landscape.md), not here. Savings figures in the Evidence column are not comparable across layers: bytes of tool output, input tokens, and output tokens measure different things.
Layer 5 note: compression (LLMLingua) shrinks the prompt *text*; routing (semantic-router) skips the LLM *call* for known intents. Both sit upstream of CC, not as plugins — the headline ratios (LLMLingua "up to 20×") are first-party README claims, not measured against a CC workload.

---

## GSD (Get Shit Done)

GSD (Get Shit Done, a meta-prompting and spec-driven development system for Claude Code) is archived: its repository ([gsd-repo][gsd-repo], archived, last push 2026-05-31, ~64K stars, `gh api` 2026-11-21) states that development continues as GSD Core in a separate repository ([open-gsd/gsd-core][gsd-core]).

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

Cross-ref: [CC-community-skills-landscape.md](CC-community-skills-landscape.md) (§ Superpowers) — the closest peer at equivalent scale (~135K★), methodology-first vs. this collection's framework-first packaging.

---

## TokenEconomizer (microsoft)

**Repo**: [microsoft/TokenEconomizer][tokeneconomizer] | **License**: Apache-2.0 | **Version**: v0.1.0 (2026-10-26) | **Paper**: [arXiv:2610.22732][tokeneconomizer-paper]

A hook plugin from UC Berkeley, Microsoft Research and Microsoft Security that learns from earlier sessions in the same repository and uses that to cut repeated token cost in later ones. It changes nothing in the agent or its model; it works through the agent's hooks and settings. Every other tool in the [Token-Waste Reduction Stack](#token-waste-reduction-stack) acts within one call or one session; this one carries what it learned across sessions.

| Mechanism | What it does | Default |
|---|---|---|
| **Micro-skills** | A fact-proposer model drafts repository facts from repeated failures; confirmed facts are injected at session start | Off (the proposer adds model calls) |
| **Tool pruning** | A tool unused over *p* = 10 prompts across at least *m* = 2 sessions, or over *s* = 5 sessions, is left out through the agent's own settings (on Claude Code: single tools, written to `.claude/settings.local.json`) | On |
| **Loop guard** | When a turn keeps hitting the same failures, a judge model at confidence ≥ 0.7 adds at most one redirect note; the README says "it never stops a turn itself" | On |

- **Claude Code integration**: plugin hooks for SessionStart, UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop and SessionEnd (`plugin/hooks/hooks.json`). Installed from a local clone with `claude plugin marketplace add "$PWD/TokenEconomizer"`, then `claude plugin install tokeneconomizer@tokeneconomizer`. Supported Claude Code versions are 2.1.300 to 2.1.310; older ones are "not supported".
- **Other agents**: Codex, GitHub Copilot CLI and Pi are supported; opencode, Cursor Agent, Grok Build, Hermes Agent and Antigravity CLI are experimental. Tool pruning writes to each agent's own settings, so it removes single tools on Claude Code but whole Model Context Protocol (MCP) servers on Copilot CLI.
- **Costs and data**: its own model calls (proposer, judge, redirect) run through the user's agent on the same plan, need no separate API key, and are counted in its reports. What it learns stays in `~/.tokeneconomizer`.
- **Reported results** (by the authors, not independently replicated): on SWE-Bench tasks, "18.4–30.9% lower mean cost" across five agent–model combinations, cheaper in all 30 repository × combination cells, and Pass@1 up in 4 of 5.

**Caution:** tool pruning writes to `.claude/settings.local.json`. Review what it writes before enabling it on a repository whose settings other people rely on.

Cross-ref: [CC-usage-tooling-landscape.md](CC-usage-tooling-landscape.md) (measurement layer); [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md) (the hook events it uses)

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

## abide (coldteadotai)

**Repo**: [coldteadotai/abide][abide] | **Stars**: 457 | **License**: MIT (confirmed against
`LICENSE`) | **Version**: latest tag v0.0.4, no GitHub Release (pushed 2026-09-29, `gh api` 2026-09-30)

Hooks into Claude Code, Codex, and OpenCode to catch AGENTS.md/CLAUDE.md rules that no linter can
check — "never let a raw error reach a user," "don't create premature abstractions" — and has the
agent repair the break in the same turn. On every edit (or turn, for rules that only make sense
against a whole diff) it asks [Jev][typesafe-jev], TypeSafe's decision model, one typed question
per rule and gets a calibrated probability back; Jev sees only the rule and the diff, never the
conversation, so edit 200 is checked the same as edit 1. A committed, human-readable
`.abide/rubric.json` holds the compiled rules, each tagged with the exact instruction-file line it
came from, so a wrong verdict is a rule to rewrite rather than a black box.

### Measured vs. the project's own claims

The README reports a replay of **93 real Claude Code sessions (1,256 edits, 147 turns) in two
repos against their own AGENTS.md**, for 22 cents: Jev flagged 39 edits and 15 turns, and an
**unnamed** independent reviewer confirmed **10 of those 39** edit-level catches and **11 of those
15** turn-level catches. The often-quoted "1 in 13 turns break a rule" and "300 ms per check, a
tenth of a cent per turn" figures come from this same self-run replay (dated 2026-09-18, direct to
TypeSafe pricing) — not an independent benchmark. "Up to 100× cheaper" than an ordinary LLM call is
the project's own arithmetic (a typed question needs no free-text generation to parse).

### Adoption Considerations

**Strengths**: works across three agents (Claude Code, Codex, OpenCode) from one `npx` install;
per-repo `.abide/rubric.json` is auditable and repo-portable; `abide calibrate`/`abide tune` give a
documented path for fixing rules that never fire, rather than silently ignoring them.

**Risks**: depends on a TypeSafe (or Vercel AI Gateway) API key and third-party inference for every
edit — an outage or missing key fails open (the edit goes through unchecked, logged as a miss);
the confirmation numbers above are a small, self-selected replay with an unnamed reviewer, not a
published methodology or dataset.

### Complementary Verification Evidence (Complete and Correct, 2026-09)

Abide narrows one question in a legacy-code rewrite — "did this edit break a rule the team already
wrote down" — but that is only one piece of the larger "is it complete, is it correct" evidence a
migration needs. Three sources not otherwise in this corpus, verified first-party:

- **[SWE Refactor Bench][swe-refactor-bench]** (arXiv:2608.23564) ran 520 agent-driven,
  whole-repository stack migrations across 8 frontier models through a three-stage protocol (old
  stack removed → existing tests pass → 6 independent agents hunt for a hidden behavioral
  difference): only 28 of 520 runs (5.4%) pass all three stages. The paper names **Blindness** — an
  agent that keeps or copies the original implementation so a green test suite reports success
  without actually migrating anything — as a dominant failure mode a green suite alone cannot catch.
- **GAO-25-107795** (`gao.gov/products/gao-25-107795`; plain text because gao.gov returns 403 to lychee) puts the US federal government's most critical legacy systems at
  23–60 years old, and states that "as of February 2025, agencies have completed three of the 10"
  modernizations GAO flagged in 2019 — the slow-review backdrop that per-edit rule enforcement and
  migration benchmarks are both trying to relieve.
- **[FreshBrew][freshbrew]** (arXiv:2510.04852) is a second, independent migration benchmark testing
  AI agents' Java-to-JDK-17 modernization across 228 repositories — further evidence that
  build/test-suite compliance and true modernization completeness are two different measurements.

American Express's own COBOL→Java parity harness (the **Locksmith Loop**: a deterministic oracle
comparing COBOL and generated Java under identical inputs, reaching 91.90% branch coverage on an
internal production-like program with no human intervention) is analyzed in depth elsewhere in this
repo and not restated here: [agentic-legacy-migration-validation-analysis.md](../sdlc-lcm/agentic-legacy-migration-validation-analysis.md).

Design lens — Lindenberg's *Complete and Correct* argues the rules worth checking in a migration are
business rules recovered from the legacy code, each traced back to the line it came from; Abide's
committed `.abide/rubric.json` gives that same traceability for a written-down engineering rule, but
by its own design "sets aside rules a diff alone can't settle, and much legacy knowledge is that
kind" (Lindenberg, *Complete and Correct*, LinkedIn, 2026-09-26;
`linkedin.com/pulse/complete-correct-andré-lindenberg-wukfe`).

Cross-ref: [agents-md-cookbook-analysis.md § Field-Study Evidence](../non-cc/protocols/agents-md-cookbook-analysis.md#field-study-evidence-coldtea-aug-2026) — Coldtea Engineering's own AGENTS.md field study, which abide's rule-enforcement product builds on; [CC-codex-plugin-cc-analysis.md](CC-codex-plugin-cc-analysis.md) — the same one-agent-gates-another Stop-hook pattern, applied there to code review rather than rule enforcement; [system-1-decision-models-landscape.md](../non-cc/reference/system-1-decision-models-landscape.md) — the wider system-1 decision-model landscape Jev belongs to; [agentic-legacy-migration-validation-analysis.md](../sdlc-lcm/agentic-legacy-migration-validation-analysis.md) — American Express's Locksmith Loop, the deterministic-oracle counterpart for the "is it correct" half of the same migration problem

---

## cc-sessions (GWUDCAP)

**Repo**: [GWUDCAP/cc-sessions][cc-sessions] | **Stars**: 1,550 | **License**: MIT | **Version**: v0.3.6 (2025-10-17; README banner stale at "v0.3.0")

Opinionated session/workflow manager that gates Edit/Write/MultiEdit behind a **Discussion-Alignment-Implementation-Check (DAIC)** protocol, binds task files to git branches, and delegates heavy work to 5 specialized subagents.

### How It Works

1. Edits are blocked until Claude proposes specific todos and the user approves via a trigger phrase (defaults "mek:", "start^:", "finito", "squish" — all remappable via `sessions config triggers`); mid-plan deviation throws the session back to discussion mode
2. Tasks are markdown files with frontmatter (status/branch/success-criteria); the installer creates matching git branches and blocks edits/commits off the task's assigned branch
3. Five subagents installed to `.claude/agents/`: context-gathering, logging, code-review, context-refinement, service-documentation — each in its own context window
4. Dual-packaged with feature parity: npm and PyPI (`npx cc-sessions` / `pipx run cc-sessions`), installed per-repo; updates/uninstalls are backup-first (`.claude/.backup-*`)

### Adoption Considerations

- Highest adoption in this batch (1,550 stars) but **no main-branch commits or releases since 2025-10-17** (~9 months as of 2026-07-23) — maintenance status unclear
- DAIC overlaps CC's native plan mode conceptually; the differentiator is *enforcement* (hard tool-gating + branch discipline) vs. guidance
- Same opinionated-workflow niche as GSD (above) — see Comparison

Cross-ref: [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md)

---

## TeamAI-CLI (Tencent)

**Repo**: [Tencent/teamai-cli][teamai-cli] | **Stars**: 4,981 | **License**: MIT (Tencent-preambled `LICENSE`; GitHub's detector reports "Other" because of the added copyright header, but the license body is the standard MIT text) | **Version**: v0.25.0 (2026-09-22)

Git-backed shared foundation for a team's AI assets — skills, rules, MCP servers, hooks, docs, and agent config — kept in sync across every teammate's machine and across 15+ agent harnesses (Claude Code, Codex, Cursor, GitHub Copilot CLI, CodeBuddy, WorkBuddy, OpenCode, Pi Coding Agent, OpenClaw, Hermes, DeepSeek Harness, Qoder, Kiro, ZCode, Oh My Pi, and others).

### How It Works

1. A team admin runs `teamai init <git-repo-url>` against a shared repo (any Git host — GitHub, GitLab, GitCode, CNB, TGit, or self-hosted) with write access granted to the team.
2. Teammates run the same command — project-scoped (default) or `--scope user` — and every AI session then automatically pulls the latest skills, rules, and harness config from that repo.
3. Three-layer model: **Team Execution** (skills, rules, docs, environment, agents, hooks, MCP, models) feeds **Team Context** (learnings, a codebase graph, a team wiki), which rolls up into **Team Improvement** (usage tracking, session history, a dashboard).
4. Onboarding is a single skill-install prompt (`Install the teamai skill: .../skills/teamai , load the teamai skill, then set up TeamAI for my team from scratch`), or `npm install -g teamai-cli` for a CLI-first setup.

### Adoption Considerations

**Strengths**: broadest harness coverage in this doc (15+ named CLIs); git-native sync needs no separate server; MIT-licensed with active CI and a fast release cadence (v0.25.0 as of 2026-09-22).

**Risks**: centralizing skills/rules/MCP config in one shared repo makes that repo a single point of failure and drift for the whole team; no independent review of what "learnings" or "codebase graph" capture or retain.

Cross-ref: **CC Switch** section above — TeamAI syncs the *content* a team shares (skills/rules/MCP config); CC Switch manages the *infrastructure* layer (provider/API key) per machine — complementary, not overlapping.

---

## herdr & Zeron (agent session runtimes)

Moved to [agent-frameworks-infrastructure-landscape.md § Agent session runtimes: herdr and Zeron](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#agent-session-runtimes-herdr-and-zeron) on 2026-11-19: both are agent-agnostic runtimes rather than Claude Code tooling.

---

## human-review (petergyang)

**Repo**: [petergyang/human-review][human-review] | **Stars**: 1,302 | **License**: MIT (confirmed
against `LICENSE`; the README's own "## License" section also states MIT) | **Version**: v0.8.2
(`gh api` 2026-09-30), pushed 2026-09-17

A visual editor for HTML and Markdown files, installed as a `/human-review` skill (Claude Code,
Codex, ChatGPT, or any coding agent with skill support): open a file or a `localhost` URL, make
direct text/list/link/image edits and drag-reorder blocks in the browser, or leave Google-Doc-style
comments anchored to exact text, an image, a chart, or a section, then click **Send** to batch
every edit and comment back to the waiting agent in one message instead of a long chat instruction.
Runs entirely local via a bundled CLI/server (`cli.js`/`server.js`/`sdk.js`) — "Everything runs on
your computer. Human Review doesn't require an account, cloud service, database, or API key." In
Claude Code the agent waits in the background and picks up feedback the moment Send is clicked; in
Codex and other agents it picks it up on its next turn or a follow-up message. Feedback left but
never sent is preserved for the next open (Restore or Discard); a `SKILL.md` teaches the agent the
review protocol.

### How It Works

- Install: paste `Install the /human-review skill globally from https://github.com/petergyang/human-review`
  into any agent, or `npx -y human-review setup --global`
- Open: `/human-review (your file)` for a static HTML/Markdown file, or `/human-review (localhost URL)`
  for a running app
- Edits: bold/italic text, bulleted/numbered lists (Tab/Shift+Tab indent), links (⌘K), image
  resize/move/paste, whole-block drag-reorder, element deletion with Undo
- Comments: select a phrase, click an image/chart/section, or edit an already-sent comment (a
  reworded comment reaches the agent on the next Send)
- HTML files auto-save direct edits/resizes locally (Discard/Revert all restores them); Markdown
  and localhost reviews apply only once the batch is sent

### Adoption Considerations

**Strengths**: fills the exact gap the ACE-FCA human-review-gate pattern in this repo names but
doesn't itself tool (see cross-ref below); zero infrastructure (no account/cloud/DB/API key);
comments are anchored, batched feedback rather than a typed chat instruction, giving the agent the
same one-comment-one-meaning precision a code review gives; agent-agnostic (any harness with skill
support).

**Risks**: young project (no stated release cadence beyond git tags; last push 2026-09-17);
comments/edits are local browser state for the current review session, not a persisted
cross-session audit trail — closing the tab without Send discards unsent Markdown/localhost
feedback (HTML direct edits persist to disk regardless); single-reviewer design, not a
multi-reviewer/concurrent-comment tool.

`subject: harness`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no [README][human-review] (one reviewer's browser session per review; no multi-user concurrent-comment semantics documented) | no [README][human-review] (local CLI/server only — "everything runs on your computer," no sync or remote-access feature) | n/a [README][human-review] (a UI/feedback-relay tool, not a state-rebuild target) | yes [README][human-review] (works across "Claude Code, Codex, or your favorite coding agent" via a documented `SKILL.md` protocol) | no [README][human-review] (feedback is applied to the file and then cleared from the review session; no independent history of past reviews) | yes [README][human-review] (comments are anchored to the exact text/element and delivered as a discrete, attributable batch the agent applies) |

`scored 2026-09-30`

Cross-ref: [CC-memory-system-analysis.md § Three-Phase Workflow with Human-Review Gates](../cc-native/context-memory/CC-memory-system-analysis.md#three-phase-workflow-with-human-review-gates) — human-review is a concrete tool for the review gates that section describes conceptually

## Plannotator (backnotprop)

**Repo**: [backnotprop/plannotator][plannotator] | **Stars**: 10,062 | **License**: MIT or Apache-2.0
at your option (`LICENSE-MIT` + `LICENSE-APACHE`; the README says "Dual-licensed under Apache 2.0
or MIT at your option"; GitHub's API shows only Apache-2.0) | **Version**: v0.28.61 (2026-11-10),
created 2025-12-28 (`gh api` 2026-11-11)

A "local, browser-based review surface for AI coding agents" (README). When the agent finishes a
plan, a diff, or a Markdown/HTML document, Plannotator opens it in the browser. You annotate it,
approve or deny, and the structured feedback goes back to the agent; the next round shows a plan
diff. Same job as human-review above, built around plan mode rather than a skill.

### How It Integrates With Claude Code

- Installed as a plugin: `/plugin marketplace add backnotprop/plannotator`, then
  `/plugin install plannotator@plannotator`.
- Its `hooks.json` registers three hooks:
  - **`PermissionRequest`** on `ExitPlanMode` runs `plannotator` (timeout 345,600 s). Plan review
    therefore needs no command: the plan opens when Claude asks to leave plan mode.
  - **`PreToolUse`** on `EnterPlanMode` runs `plannotator improve-context`.
  - **`SessionStart`** on `compact` prints its Inbox reminder.
- The plugin also loads a hooks module (`mod/register.ts`). Per the README, on Claude Code
  2.1.287 or newer this makes review non-blocking: "Claude ends its turn and your decision arrives
  later as a message" (turn it off with `PLANNOTATOR_CLAUDE_MOD=0`). A worked example of a mod:
  [CC-mods-function-hooks-analysis.md](../cc-native/plugins-ecosystem/CC-mods-function-hooks-analysis.md).
- Slash commands: `/plannotator-annotate` (file, folder or URL), `/plannotator-last` (the agent's
  last message) and `/plannotator-review` (the uncommitted diff, or a GitHub PR / GitLab MR).

### Beyond Claude Code

The README names ten harnesses: Claude Code, Codex, Copilot CLI, Gemini CLI, OpenCode, Kiro,
Droid, Amp, DeepSeek Harness and Pi. Plan interception depends on each harness's hooks; on Droid
it is "Commands only, no plan interception yet". A Plannotator Inbox lets agents leave questions
and files while they keep working, over plugins or MCP.

### Data and Sharing

- "Plannotator does not collect usage telemetry or analytics" (README). Plans, diffs and
  annotations stay local by default; network use is opt-in (URL fetching, your own GitHub/GitLab
  CLI, an AI provider you configure, sharing). The app checks GitHub for the latest release when
  it loads.
- Link sharing: large shares are encrypted with AES-256-GCM before upload and the server stores
  only ciphertext. The README says link sharing "is moving to deprecated support". Its
  replacement for team sharing, **Workspaces**, is "a separate hosted product", so the local
  storage model does not apply there. No price is published; the product site describes a
  waitlist (not read verbatim).

### Adoption Considerations

**Strengths**: hooks into the plan-mode exit itself, so every plan gets a review step with no
command to remember; deny-with-feedback and plan diffs between rounds; ten harnesses; local by
default with no telemetry; widely adopted (10k stars, against human-review's 1.3k).

**Risks**: the non-blocking flow depends on a recent Claude Code version and on hooks modules,
and was not tested here; team sharing is moving to a hosted product with no published terms; a
fast release cadence (v0.28.61 within eleven months) means behaviour can shift between installs.

Not rubric-scored yet.

Cross-ref: [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md)
(`PermissionRequest`), and the human-review gate pattern above.

---

## Registry catch-up: awesome-list entries (2026-11-20)

Five entries that the community monitor flagged from the two awesome lists and that this corpus
did not yet cover. Star counts, licences and descriptions come from each repo's `gh api` record and
`LICENSE` file on 2026-11-20; what each tool does is the repo's own description, not tested here.
Not scored. Each flagged name's outcome (folded, covered or dropped, with a reason) is in [the K27 name-outcomes record](../../triage/community/2026-11-20-k27-name-outcomes.md).

| Tool | Stars | Licence | What the repo describes |
|---|---|---|---|
| [claude-code-infrastructure-showcase][infra-showcase] | 10,058 | MIT | Reference library, not an app: auto-activating skills via hooks, modular skills, agents, a dev-docs system that survives context resets |
| [QualityLayer (formerly Claude CodePro)][codepro] | 2,152 | Source-available commercial ("QualityLayer"), not OSI | Plan, implement and verify workflow across coding agents |
| [skill-codex][skill-codex] | 1,479 | MIT | Claude Code skill that delegates prompts to Codex |
| [claude-codex-settings][codex-settings] | 1,214 | Apache-2.0 | Shared Claude Code, Codex and Cursor configs, plugins and hooks |
| [claude-code-docs (ericbuess)][docs-mirror] | 1,005 | MIT (per `LICENSE`) | Local mirror of the official Claude Code docs |

---

## New and unproven: agent plugins (2026-11-23)

Two Claude Code plugins that are days old. Stars, licence, dates and latest release come from each repo's `gh api` record on 2026-11-23, the `LICENSE` file (MIT in both; no other licence file in either tree) and the README. Everything about what they do is the README's own account; nothing here was installed or run. Both are **new; adoption not yet shown**: no named independent users, so these are watch entries, not recommendations.

| Tool | Created, stars | Latest release | What the README describes | Caveats stated in or by the README |
|---|---|---|---|---|
| [mobile-agent-testers][mat] | created 2026-11-16, 1,324 stars | v0.1.0 (2026-11-19) | A GitHub Actions workflow plus Claude Code plugin: each "tester" is a Claude Code agent with its own iOS Simulator or Android emulator and a persona (device, language, text size), which explores the app and writes a bug report with screenshots | The README's own example runs (LocalSend, AnkiDroid, a Flutter sample) are the author's runs on public apps, not user reports. Model cost reported at $0.15 to $0.55 per phone in those runs (vendor claim). It "sometimes misreads a screen" (3 of 20 agents in one run flagged the Simulator keyboard), covers main paths only, and agents explore, so runs are not repeatable; it is not a replacement for scripted tests. Hosted runners are meant for the repo's own project; the author is exploring a hosted version for teams with private apps |
| [fast-anything][fast-anything] | created 2026-11-21, 2,951 stars | v0.8.5 (2026-11-23) | A CLI, Claude Code plugin and MCP server that profiles a Python, Node, Ruby, Java, Go and other app, has the coding agent port only the hot function to Rust, replays recorded real calls to check identical results, and swaps it in reversibly | Speed-ups in the README (for example 116x on a Python fuzzy-dedupe example, 3x on Java) are the author's runs on one i5-10500 Windows machine over its own `examples/`, not independent benchmarks. It ports top-level deterministic functions over plain data, and needs a Rust toolchain. Agent-neutral: `--agent` takes `claude`, `codex` or any command reading a prompt on stdin |

---

## Detailed Tool Landscapes

Per-tool entries for three categories have moved to focused topic docs; the cross-tool comparison below still covers all of them:

- [CC-memory-tooling-landscape.md](CC-memory-tooling-landscape.md) — persistent memory: ByteRover, Claude-Mem, MemPalace, MemSearch
- [CC-code-tooling-landscape.md](CC-code-tooling-landscape.md) — code analysis: Graphify, Code-Review-Graph, codebase-memory-mcp, Serena, ast-grep MCP, Repomix, code2prompt
- [CC-usage-tooling-landscape.md](CC-usage-tooling-landscape.md) — usage observability: CodeBurn, ccusage, Claude-Code-Usage-Monitor

Design-systems / format tooling (awesome-design-md, Google Labs DESIGN.md spec + CLI) has moved to a non-CC home — multi-agent, not CC-specific:

- [agent-design-formats-landscape.md](../non-cc/infrastructure/agent-design-formats-landscape.md) — agent-consumable design formats (incl. the CC-supported Figma Dev Mode MCP context)

## Comparison

| Tool | Layer | CC Integration | Approach | Maturity |
|---|---|---|---|---|
| **RTK** | Tool output compression | Hooks (transparent rewrite) | Reduce input noise | Stable (v0.33.1) |
| **GSD** | Meta-prompting + orchestration | Hooks + slash commands | Structured workflows, subagents | Archived; continues as GSD Core (`gh api` 2026-11-21) |
| **everything-claude-code** | Agent/skill framework | Plugin (drop-in) | Bundled agents, skills, shims | Active (50K+ stars) |
| **TokenEconomizer** | Cross-session cost control | Plugin hooks (6 events) + `settings.local.json` | Micro-skills, tool pruning, loop guard learned per repository | Early (v0.1.0, Apache-2.0) |
| **ByteRover** | Persistent memory | MCP server | Hierarchical context trees, cloud sync | Archived (4,943 stars, `gh api` 2026-11-21) |
| **Claude-Mem** | Persistent memory + compression (cross-agent) | Hooks + MCP + plugin | AI-compressed observations, progressive search | Active (115.2K stars, v15.13.0) |
| **CC Switch** | Multi-CLI provider management | Desktop app (GUI) | Unified config across 5 AI CLIs | Active (38.9K stars, 1,376 commits) |
| **abide** | AGENTS.md rule enforcement | Hooks (Claude Code, Codex, OpenCode) | Per-edit/turn Jev decision-model question per rule, agent self-repairs | Early (457 stars, v0.0.4) |
| **cc-sessions** | Session/workflow enforcement | Hooks + subagents + trigger phrases | DAIC tool-gating, task↔branch binding | Adopted but dormant (1,550 stars, v0.3.6, no commits since 2025-10) |
| **TeamAI-CLI** | Team-shared AI config | Skill + CLI (git-backed shared repo) | Sync skills/rules/MCP/hooks across 15+ harnesses | Active (4,981 stars, v0.25.0) |
| **Graphify** | Code→knowledge graph | Hooks + slash commands + MCP + CLAUDE.md | Semantic knowledge graphs from repos | Active (16.5K stars) |
| **MemPalace** | Persistent memory | MCP server + plugin marketplace | Verbatim palace-metaphor memory | Active (33.6K stars, v3.0.0) |
| **MemSearch** | Persistent memory (cross-agent) | Plugin (hooks + skill, no MCP) | Markdown source-of-truth + Milvus hybrid search | Active (~2K stars, v0.4.7) |
| **Code-Review-Graph** | Structural code analysis | MCP server (22 tools, auto-config) | AST-based blast radius for reviews | Active (7.1K stars) |
| **codebase-memory-mcp** | Code→graph + LSP + embeddings | MCP (14 tools) + PreToolUse hook + auto-config | Single-binary knowledge graph | Active (~19K stars, v0.8.1) |
| **Serena** | Semantic code (live LSP) | MCP server (20+ tools) | Symbol-level retrieve/edit/refactor | Active (25.2K stars, v1.5.3) |
| **ast-grep MCP** | Structural search/rewrite | MCP server (4 tools) | tree-sitter AST patterns | Experimental (419 stars, no release) |
| **Repomix** | Repo→single-file context export | MCP server + official CC plugins | tree-sitter compression + token counts | Stable (26.2K stars, v1.14.1) |
| **code2prompt** | Repo→single-prompt context export | MCP server + CLI | Templated export + token counts | Stable (7.4K stars, v4.2.0) |
| **CodeBurn** | Token-usage observability (cross-agent) | CLI (reads on-disk session data) | Cross-agent dashboard, 13 task categories, optimize/compare | Active (4K stars) |
| **ccusage** | Token-usage observability (CC/Codex) | CLI + MCP server + statusline | JSONL analyzer, cache-token split, offline mode | Stable (13.4K stars, v18.0.11) |
| **Claude-Code-Usage-Monitor** | Predictive usage monitoring | Real-time TUI | P90-based limit prediction, burn-rate analytics, plan-aware | Active (7.8K stars, v3.1.0) |
| **human-review** | Visual review + feedback relay | Skill (any agent with skill support) | Google-Doc-style comments/edits batched to the waiting agent | Active (1,302 stars, v0.8.2) |
| **Plannotator** | Plan/diff review + feedback relay | Plugin: `PermissionRequest` hook on `ExitPlanMode` + hooks module | Browser annotation, approve/deny with structured feedback; plan diffs between rounds | Active (10,062 stars, v0.28.61) |

All twenty-four address different layers of the agent stack — complementary, not competing. The five code-analysis tools (graphify, Code-Review-Graph, codebase-memory-mcp, Serena, ast-grep MCP) split along precompute-a-graph vs. live-LSP vs. on-demand-structural-search; the two repo packers (Repomix, code2prompt) are one-shot context export rather than a live server. Full per-tool entries for the memory, code-analysis, and usage-observability rows are in the topic docs linked above.

Cross-ref: [CC-extended-context-analysis.md](../cc-native/context-memory/CC-extended-context-analysis.md) — CC's built-in context compaction

## Not included

Entries removed under the [pruning rule](../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (alive, adopted or proven; checked 2026-11-21).

| Name | Reason | Date | Link |
|---|---|---|---|
| Boucle Read-Once Framework | 126 stars (`gh api` 2026-11-21); the README's "40%" appears only in a sample stats printout with no stated method, and it names no independent users | 2026-11-21 | <https://github.com/Bande-a-Bonnot/Boucle-framework> |
| Parry Guard | 46 stars (`gh api` 2026-11-21); no detection benchmark, only author-reported latency, and the README calls it early development; no named independent users | 2026-11-21 | <https://github.com/vaporif/parry-guard> |
| Dippy | 244 stars (`gh api` 2026-11-21); the README's "up to 40% faster" is unbenchmarked and no false-allow rate is published; no named independent users | 2026-11-21 | <https://github.com/ldayton/Dippy> |
| cogit | 213 stars, repo created 2026-10-27 (`gh api` 2026-11-21); its 94% figure is the recorder's own accuracy (parent match over 109 messages), not a user-facing benefit, which its docs say is not measured yet; no named independent users | 2026-11-21 | <https://github.com/erensrtky/cogit> |
| ultraship | 124 stars (`gh api` 2026-11-21); README reports no measured benefit and no named independent users | 2026-11-21 | <https://github.com/Houseofmvps/ultraship> |
| fable-baton | 30 stars (`gh api` 2026-11-21); its own benchmark (n=2 per cell, one small project) shows the top model's output tokens falling 38–44% but total cost about the same, so no measured net benefit | 2026-11-21 | <https://github.com/realgarit/fable-baton> |
| Selective Context | Not alive: last push 2024-02-12, last release 0.1.4 on PyPI (2023-10-28); an EMNLP 2023 paper (arXiv:2310.06201), but at 426 stars below the ~1,000 that would keep a dated line | 2026-11-21 | <https://github.com/liyucheng09/Selective_Context> |

## Sources

| Source | Content |
|---|---|
| [mobile-agent-testers][mat] · [fast-anything][fast-anything] | Two new Claude Code plugins: README, MIT `LICENSE`, `gh api` records and releases (read 2026-11-23); self-reported claims only |
| [RTK repository][rtk-repo] | CLI proxy, hook integration, benchmarks |
| [rtk-ai/rtk#839][rtk-839] | Independent benchmark findings |
| [GSD repository][gsd-repo] · [GSD Core][gsd-core] | Meta-prompting + context engineering framework; archived, README points to GSD Core (`gh api` 2026-11-21) |
| [everything-claude-code][ecc] | Agent/skill/hook framework (50K+ stars) |
| [context-mode][context-mode] | Tool-output sandbox plugin: README, LICENSE (Elastic License 2.0), v2.2.1 release (`gh api` 2026-11-22) |
| [Headroom][headroom] | Compression proxy: README benchmark table, Apache-2.0 LICENSE, v0.45.0 release (`gh api` 2026-11-22) |
| [TokenEconomizer][tokeneconomizer] · [paper][tokeneconomizer-paper] | Cross-session cost control plugin: README, `plugin/hooks/hooks.json`, v0.1.0 release (Apache-2.0; read 2026-11-09) |
| [ByteRover CLI][byterover] | Portable memory layer for coding agents (MCP, context trees) |
| [ByteRover paper][byterover-paper] | arXiv:2604.01599 — agent-native memory via hierarchical context |
| [Claude-Mem][claude-mem] | Persistent memory compression system, cross-agent (115.2K stars, v15.13.0; `gh api` 2026-11-09) |
| [CC Switch][cc-switch] | Cross-platform multi-CLI provider management (38.9K stars) |
| [abide][abide] | AGENTS.md rule enforcement via a Jev decision-model question per rule, per edit/turn, across Claude Code/Codex/OpenCode (457 stars, MIT) |
| [SWE Refactor Bench (arXiv:2608.23564)][swe-refactor-bench] | 520 agent migrations, 3-stage verification, "Blindness" failure mode (abstract fetched 2026-09-30) |
| GAO-25-107795 (`gao.gov/products/gao-25-107795`) | Federal legacy-system age (23–60 yrs) and 2019-modernization completion status (fetched 2026-09-30) |
| [FreshBrew (arXiv:2510.04852)][freshbrew] | Java-to-JDK-17 agent migration benchmark, 228 repositories (abstract fetched 2026-09-30) |
| André Lindenberg — *Complete and Correct* (LinkedIn, 2026-09-26; `linkedin.com/pulse/complete-correct-andré-lindenberg-wukfe`) | Design lens: recovered business rules as the unit a migration rubric should check (LinkedIn — not link-checked) |
| [cc-sessions][cc-sessions] | DAIC session/workflow enforcement, npm+PyPI dual-packaged (1,550 stars, MIT, v0.3.6) |
| [TeamAI-CLI][teamai-cli] | Git-backed shared AI config (skills/rules/MCP/hooks) across 15+ agent harnesses (4,981 stars, MIT, v0.25.0) |
| [human-review][human-review] | Visual HTML/Markdown review — comments and edits batched to the waiting agent (1,302 stars, MIT, v0.8.2) |
| [Plannotator repository][plannotator] | README (integrations, privacy, sharing), `hooks.json`, `LICENSE-MIT`/`LICENSE-APACHE`, v0.28.61 release; `gh api` 2026-11-11 |
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
| [LLMLingua][llmlingua] | Microsoft prompt-compression library (LLMLingua / LongLLMLingua / LLMLingua-2); README compression claims (6.3K stars, MIT) |
| Registry catch-up repos: [infrastructure showcase][infra-showcase] · [QualityLayer][codepro] · [skill-codex][skill-codex] · [claude-codex-settings][codex-settings] · [claude-code-docs][docs-mirror] | Stars, licences and descriptions from each repo's `gh api` record and `LICENSE`/README, 2026-11-20 |
| [semantic-router][semantic-router] | Aurelio Labs semantic routing/decision layer — skips LLM calls for recognized intents (3.6K stars, MIT) |

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
[gsd-core]: https://github.com/open-gsd/gsd-core
[ecc]: https://github.com/affaan-m/everything-claude-code
[tokeneconomizer]: https://github.com/microsoft/TokenEconomizer
[tokeneconomizer-paper]: https://arxiv.org/abs/2610.22732
[byterover]: https://github.com/campfirein/byterover-cli
[byterover-paper]: https://arxiv.org/abs/2604.01599
[claude-mem]: https://github.com/thedotmack/claude-mem
[cc-switch]: https://github.com/farion1231/cc-switch
[abide]: https://github.com/coldteadotai/abide
[typesafe-jev]: https://docs.typesafe.ai/
[swe-refactor-bench]: https://arxiv.org/abs/2608.23564
[freshbrew]: https://arxiv.org/abs/2510.04852
[cc-sessions]: https://github.com/GWUDCAP/cc-sessions
[teamai-cli]: https://github.com/Tencent/teamai-cli
[human-review]: https://github.com/petergyang/human-review
[plannotator]: https://github.com/backnotprop/plannotator
[hlyr-backpressure]: https://www.hlyr.dev/blog/context-efficient-backpressure
[skills-landscape]: CC-community-skills-landscape.md
[codeburn]: https://github.com/getagentseal/codeburn
[ccusage]: https://github.com/ryoppippi/ccusage
[claude-monitor]: https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor
[llmlingua]: https://github.com/microsoft/LLMLingua
[context-mode]: https://github.com/mksglu/context-mode
[headroom]: https://github.com/headroomlabs-ai/headroom
[skills-caveman]: CC-community-skills-landscape.md#caveman-juliusbrussee
[semantic-router]: https://github.com/aurelio-labs/semantic-router
[cc-settings-ref-git]: https://code.claude.com/docs/en/settings-reference#includegitinstructions
[infra-showcase]: https://github.com/diet103/claude-code-infrastructure-showcase
[codepro]: https://github.com/maxritter/qualitylayer
[skill-codex]: https://github.com/skills-directory/skill-codex
[codex-settings]: https://github.com/fcakyon/claude-codex-settings
[docs-mirror]: https://github.com/ericbuess/claude-code-docs
[mat]: https://github.com/pierridotite/mobile-agent-testers
[fast-anything]: https://github.com/EL4CTEO/fast-anything
