---
title: CC Community Skills Landscape
description: Survey of community-built Claude Code skill libraries — gstack (founder/engineering workflows), pm-skills (product management framework), claude-code-best-practice (knowledge base), BHIL (AI-first development methodology with artifact chains), claude-howto (example-driven learning), and dispatch (context window multiplication via background workers).
category: landscape
status: research
created: 2026-03-13
updated: 2026-04-04
validated_links: 2026-04-04
---

**Status**: Research (informational)

## Summary

Seven community skill libraries demonstrate distinct models for packaging CC capabilities: gstack enforces cognitive mode-switching through role-locked skills, pm-skills delivers professional frameworks as installable plugins, claude-code-best-practice curates a knowledge index of CC patterns and open questions, BHIL provides an AI-first development methodology with traceable artifact chains, claude-howto delivers example-driven learning with production-ready templates, dispatch fans out work to parallel background agents for context window multiplication, and superpowers enforces a complete TDD-driven development methodology with subagent orchestration.

## gstack (Garry Tan)

**Repo**: [garrytan/gstack](https://github.com/garrytan/gstack) | **Stars**: 4,000+ | **License**: MIT

8 skills targeting founder/engineering workflows with browser automation:

| Skill | Role | What It Does |
|-------|------|-------------|
| `/plan-ceo-review` | Founder | 11-phase plan review in EXPANSION / HOLD SCOPE / REDUCTION mode. Mandatory ASCII diagrams, error registries, TODOS.md entries. 9 "Prime Directives" govern every review. |
| `/plan-eng-review` | Engineering manager | Step 0 Scope Challenge gates BIG vs SMALL change review. Per-issue `AskUserQuestion` with lettered options. Produces reuse analysis and "NOT in scope" section. |
| `/review` | Security auditor | Two-pass PR audit: CRITICAL (SQL injection, TOCTOU, unvalidated LLM output) then INFORMATIONAL. Terse `file:line` output. Reads versioned `checklist.md`. |
| `/ship` | Release engineer | Automated: fetch/merge main, parallel test suites, review checklist, 4-digit VERSION bump, CHANGELOG, coherent commits, PR creation. Stops only on merge conflicts, test failures, or critical review issues. |
| `/browse` | QA inspector | Persistent headless Chromium daemon (~100ms round trips after first 3s startup). 50+ commands across navigate/read/snapshot/interact/inspect. Ref-based element selection via accessibility tree (`@e`, `@c`). |
| `/qa` | QA lead | Full/Quick/Regression modes. Weighted health score across 8 categories. 7-category issue taxonomy. Framework-specific guidance (Next.js, Rails, WordPress, SPAs). JSON snapshots for trend tracking. |
| `/setup-browser-cookies` | Session manager | Imports cookies from installed Chromium browsers (Chrome, Arc, Brave, Edge, Comet) via dark-themed web UI. Domain names only — no values exposed. |
| `/retro` | Engineering manager | Git history analysis with configurable time windows. Work session detection (45-min gaps), hourly commit distribution, contributor leaderboard, hotspot files, test/production ratio. |

### Cognitive Mode-Switching

The central design principle: *"Planning is not review. Review is not shipping. Founder taste is not engineering rigor."*

- **Hard role assignment**: each skill installs a specific persona that cannot drift
- **Mode-lock**: once a user selects EXPANSION/HOLD SCOPE/REDUCTION in `/plan-ceo-review`, the agent commits fully
- **Per-issue interruption**: both plan skills enforce one `AskUserQuestion` per issue — no batching
- **Mechanical handoffs**: `/ship` invokes the `/review` checklist and stops at critical findings

### Browser Automation Architecture

- **Daemon model**: Bun-compiled binary (~58MB) + persistent Chromium process. State file at `/tmp/browse-server.json`
- **Cookie persistence**: cookies and storage survive context recreation events
- **Multi-workspace isolation**: port derived from `CONDUCTOR_PORT` env var for parallel sessions
- **Token efficiency**: accessibility tree snapshots instead of full DOM. "In a 20-command session, MCP tools burn 30,000-40,000 tokens on protocol framing alone. gstack burns zero."
- **Security**: bearer token auth (random UUID), state file chmod 600

### Conductor Integration

[conductor.build](https://conductor.build) runs multiple CC sessions in parallel. Integration is via `CONDUCTOR_PORT` environment variable — each session gets isolated workspace and browser instance. No SDK dependency; pure env var convention.

## pm-skills (Pawel Huryn)

**Repo**: [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | **Stars**: 6,800+ | **License**: MIT

65 skills and 36 chained workflow commands across 8 plugins:

| Plugin | Skills | Commands | Domain |
|--------|--------|----------|--------|
| `pm-execution` | 15 | 10 | PRDs, OKRs, roadmaps, sprints, retrospectives, stakeholder maps |
| `pm-product-discovery` | 13 | 5 | Ideation, OSTs, assumption testing, interviews |
| `pm-product-strategy` | 12 | 5 | Vision, canvases, pricing, competitive frameworks |
| `pm-market-research` | 7 | 3 | Personas, segmentation, journey maps, market sizing |
| `pm-go-to-market` | 6 | 3 | GTM strategy, ICPs, growth loops, battlecards |
| `pm-marketing-growth` | 5 | 2 | Positioning, North Star, naming |
| `pm-data-analytics` | 3 | 3 | SQL generation, cohort analysis, A/B testing |
| `pm-toolkit` | 4 | 5 | Resume review, NDA drafting, privacy policy, grammar |

### Key Insight: Plugins as Framework Delivery

pm-skills is the clearest public example of CC plugins as a **domain expertise distribution platform**:

- **Framework encoding**: each skill embeds a complete named methodology (Teresa Torres' OST, Strategyzer's BMC, SMART/OKR metrics) — not generic prompts
- **Dual installation surface**: same skills install via `claude plugin install` (CLI) and Claude Cowork (GUI), reaching both developers and non-technical PMs
- **Cross-AI portability**: README notes compatibility with Gemini CLI, OpenCode, Cursor, Codex CLI, Kiro via folder copying
- **Commands as orchestrators**: `/discover` chains 7 sequential steps across multiple skills — workflow orchestration on top of atomic capabilities
- **Intellectual attribution**: credits 12 named PM thought leaders; skills cite specific book titles
- **Brand integration**: `plugin.json` points to productcompass.pm — plugins as lead-generation vehicle

### Skill Authoring Patterns

- **Single-file simplicity**: each skill is one `SKILL.md` — no YAML, no imports, no external refs
- **Noun/verb naming discipline**: skills = nouns (`stakeholder-map`), commands = verbs (`write-prd`)
- **No cross-plugin dependencies**: CONTRIBUTING.md forbids cross-plugin references; inter-plugin discovery via natural language suggestions
- **Validation**: `validate_plugins.py` enforces naming and metadata compliance at contribution time
- **Marketplace manifest**: root `.claude-plugin/marketplace.json` registers all 8 plugins (`"$schema": "https://anthropic.com/claude-code/marketplace.schema.json"`)

## claude-code-best-practice (shanraisshan)

**Repo**: [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | **Stars**: 31.8K | **Author**: Claude Community Ambassador

*"practice made claude perfect"* — a **living community knowledge base** and curated reference index, not a skill library or plugin.

### Organizational Framework: A/C/S Tags

All CC features categorized under three primary tags:

| Tag | Meaning | Role |
|-----|---------|------|
| **A** (Agents) | Autonomous actors in isolated contexts | Custom tools, persistent identity |
| **C** (Commands) | Knowledge-injected prompt templates | Workflow orchestration |
| **S** (Skills) | Configurable, discoverable capabilities | Context forking |

### Content Structure

| Section | Entries | Coverage |
|---------|---------|----------|
| Concepts Table | 12 | Subagents, Commands, Skills, Workflows, Hooks, MCP Servers, Plugins, Settings, Status Line, Memory, Checkpointing, CLI Startup Flags |
| Hot Features | 8+ | Power-ups, Ultraplan, CC Web, No Flicker, Computer Use, Auto Mode, Channels, Slack, Code Review, GHA, Chrome Extension, Scheduled Tasks, Voice, Simplify & Batch, Agent Teams, Remote Control, Worktrees, Ralph |
| Orchestration Workflow | 1 | Visual diagram: Command -> Agent -> Skill architecture |
| Development Workflows | 9+ | everything-claude-code (137K stars), Superpowers (135K), Spec Kit (85K), gstack, GSD, BMAD-METHOD, OpenSpec, oh-my-claudecode, Compound Engineering, HumanLayer — with uniqueness badges and component breakdowns |
| Tips and Tricks | 38+ | Across 7 categories (prompting, planning, workflows, debugging, utilities, daily) |
| Startup Comparison | 5 | CC features vs commercial tool equivalents |
| Open Research Questions | 13 | Across 4 domains |
| Technical Reports | 9 | Deep-dives on specific CC features |

### Open Research Questions (13)

Organized across 4 domains — memory/instructions (4), agents/skills/workflows (6), specs/documentation (3). Key questions include:

- Selection criteria: command vs. agent vs. skill vs. vanilla CC
- Optimal CLAUDE.md content scope and staleness detection
- Built-in plan mode vs. custom planning enforcement
- Conflict resolution between personal and community skills
- Why Claude ignores explicit MUST directives

### Relevance

Valuable as a **community health indicator** and discovery entry point. The open research questions surface gaps in CC documentation and community understanding. The workflow pattern catalog (with star counts) tracks ecosystem adoption velocity.

## BHIL AI-First Development Toolkit (camalus)

**Repo**: [camalus/BHIL-AI-First-Development-Toolkit][bhil] | **Stars**: 115 | **License**: MIT

A production-grade methodology for AI-native development using traceable artifact chains. Core thesis: *"The bottleneck in AI-assisted development is not code generation. It is specification quality."*

### Artifact Chain

PRD → SPEC → ADR → TASK → CODE → REVIEW → DEPLOY, with sprint retrospectives feeding back to requirements. Each artifact carries unique IDs enabling machine-actionable traceability.

### CC Integration

| Component | Path | Purpose |
|-----------|------|---------|
| CLAUDE.md | root | Project config auto-loaded by CC |
| Agents | `.claude/agents/` | Custom subagent definitions |
| Skills | `.claude/skills/` | `new-sprint`, `new-adr`, `validate` workflows |
| Rules | `.claude/rules/` | Path-scoped coding standards |
| Settings | `.claude/settings.json` | Model routing, permission hooks |

### AI-Native ADR Extensions

Beyond traditional architecture decisions, three LLM-specific decision types:

- **Model Selection ADRs** — benchmarks, costs, latency tradeoffs
- **Prompt Strategy ADRs** — approach, versioning, evaluation criteria
- **Agent Orchestration ADRs** — pattern selection and rationale

### Key Differentiator

Where gstack focuses on cognitive mode-switching and pm-skills on domain framework delivery, BHIL provides **process infrastructure** — the artifact chain that connects sprint planning to deployment with machine-readable traceability. Compatible with CC, RuFlo (Agentics Foundation), and RuVector.

### Adoption Considerations

**Strengths**: Full SDLC coverage, traceable artifact IDs, CC-native configuration (.claude/ directory), methodology-agnostic (works with any sprint framework).

**Risks**: Early stage (3 commits, 115 stars). Heavy methodology — may be more structure than small projects need. No plugin marketplace integration.

## claude-howto (luongnv89)

**Repo**: [luongnv89/claude-howto][claude-howto] | **Stars**: 18.9K | **License**: MIT

Example-driven learning guide for Claude Code — 10 sequential modules covering slash commands, memory, skills, subagents, MCP, hooks, plugins, checkpoints, advanced features, and CLI. Bridges the gap between official reference docs and production-ready implementation.

### Key Templates

- **Subagent definitions**: code-reviewer, test-engineer, security-auditor, documentation-writer
- **Hook scripts**: security scanning (PreToolUse), commit validation, formatting, team notifications
- **Skill bundles**: code-review, brand-voice, doc-generation
- **CLAUDE.md templates**: team, directory, and personal memory levels
- **MCP configs**: GitHub, database, filesystem, multi-server examples

### Relevance

Learning resource with production-ready templates, not a plugin. Where claude-code-best-practice indexes *what exists* and gstack delivers *opinionated workflows*, claude-howto demonstrates *how to combine* CC features into automated pipelines (11–13 hour structured curriculum, beginner → advanced).

**Notable fork**: [akolaarthurali/claude-howto-Master-Claude-Code-in-a-Weekend](https://github.com/akolaarthurali/claude-howto-Master-Claude-Code-in-a-Weekend) (3 stars) — repackaged as a weekend crash course. Same v2.2.0 content; signals demand for condensed onboarding formats but no original content beyond the upstream.

## Dispatch (bassimeledath)

**Repo**: [bassimeledath/dispatch](https://github.com/bassimeledath/dispatch) | **Stars**: 352 | **License**: MIT

A CC skill that **10x's effective context window** by dispatching tasks to background AI workers. The main session becomes a lightweight orchestrator — work fans out to parallel agents, each with their own full context window.

### How It Works

```
Without dispatch:                    With dispatch:
Task 1 → fills context              /dispatch all 5 tasks
Task 2 → context grows              Workers execute in parallel
Task 3 → losing track               Main session stays lean
Task 5 → new session needed          Questions surface when needed
```

1. User invokes `/dispatch <task>` (optionally specifying model)
2. Dispatcher generates a checklist (sole main-session artifact)
3. Background worker executes with full independent context
4. Worker surfaces questions via IPC — no context restart
5. Results surface on completion or on-demand status check

### Architecture

| Layer | Role |
|-------|------|
| **Host dispatcher** | Runs in main CC session, creates checklists, coordinates |
| **Background workers** | Claude, Cursor, or Codex CLIs with fresh contexts |
| **IPC system** | Async question/answer flow preserving worker context continuity |

### Multi-Backend Support

Config at `~/.dispatch/config.yaml` — three sections:

- **Backends**: CLI command definitions (Claude, Cursor, Codex)
- **Models**: Model names mapped to backend providers
- **Aliases**: Named shortcuts with optional system prompts

Auto-discovery generates initial config on first run. Last-mentioned model takes precedence.

### Installation

```bash
npx skills add bassimeledath/dispatch -g      # user-level
npx skills add bassimeledath/dispatch         # project-level
```

### Key Differentiator

Inverts traditional context usage: *"the main session becomes a mediator, not the thinker."* Unlike manual `claude --background` or multi-terminal approaches, dispatch automates worker lifecycle, error handling, progress tracking, and worktree isolation. Example: `/dispatch use sonnet to find better design patterns for the auth module`.

### Relevance

Addresses the core context exhaustion problem from a different angle than GSD (meta-prompting), RTK (output compression), or Boucle (read deduplication). Dispatch **multiplies** available context by parallelizing across independent agent processes.

## Superpowers (obra / Jesse Vincent)

**Repo**: [obra/superpowers][superpowers] | **Stars**: 135K | **License**: MIT | **Version**: v5.0.7

*"An agentic skills framework & software development methodology that works."* Composable skills and initial instructions that enable coding agents to execute structured development workflows autonomously.

### Core Philosophy

Test-driven development, systematic processes over ad-hoc approaches, complexity reduction, evidence-based validation. Goal: *"Claude to be able to work autonomously for a couple hours at a time without deviating from the plan."*

### Foundational Workflow Stages

1. **Brainstorming** — design refinement through Socratic questioning
2. **Git worktrees** — isolated development environments
3. **Implementation planning** — task decomposition (2–5 min granularity)
4. **Subagent-driven execution** — autonomous task completion with review
5. **TDD** — mandatory RED-GREEN-REFACTOR cycle enforcement
6. **Code review** — plan-compliance verification (two-stage: spec + quality)
7. **Branch completion** — merge decision and cleanup

### Skills Inventory

| Category | Skills |
|----------|--------|
| Testing | test-driven-development (RED-GREEN-REFACTOR with anti-patterns) |
| Debugging | systematic-debugging (4-phase root cause), verification-before-completion |
| Collaboration | brainstorming, writing-plans, executing-plans, dispatching-parallel-agents, requesting/receiving-code-review, using-git-worktrees, finishing-a-development-branch, subagent-driven-development |
| Meta | writing-skills (new skill creation), using-superpowers (framework intro) |

### Installation

Available via official CC marketplace (`/plugin install superpowers@claude-plugins-official`), plus Cursor, Codex, OpenCode, GitHub Copilot CLI, and Gemini CLI. Skills trigger automatically based on context — mandatory workflows, not suggestions.

### Key Differentiator

Where gstack locks cognitive *modes* and pm-skills delivers domain *frameworks*, superpowers enforces a complete **development methodology** — spec-before-code, subagent-per-task, mandatory TDD, chunked design presentation. Multi-runtime: 7 agent platforms supported. Largest community in the CC skills space (135K stars, 28 contributors).

## Cross-References

- [CC-skills-adoption-analysis.md](../cc-native/agents-skills/CC-skills-adoption-analysis.md) — native skills format and adoption
- [CC-plans-as-skill-rule-templates.md](../cc-native/agents-skills/CC-plans-as-skill-rule-templates.md) — plan-to-skill extraction (gstack's `/plan-*` skills are concrete examples)
- [CC-official-plugins-landscape.md](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) — official plugin ecosystem
- [CC-community-plugins-landscape.md](CC-community-plugins-landscape.md) — plugin catalogs
- [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) — claude-mem persistent memory

## Sources

| Source | Content |
|---|---|
| [gstack][gstack] | Founder/engineering workflow skills |
| [pm-skills][pm-skills] | Product management skill framework |
| [claude-code-best-practice][ccbp] | Community knowledge base |
| [BHIL AI-First Development Toolkit][bhil] | AI-native methodology with artifact chains |
| [claude-howto][claude-howto] | Example-driven CC learning guide (10 modules, templates) |
| [dispatch][dispatch] | Context window multiplication via background workers |
| [superpowers][superpowers] | Agentic skills framework & dev methodology (135K stars) |

[gstack]: https://github.com/garrytan/gstack
[pm-skills]: https://github.com/phuryn/pm-skills
[ccbp]: https://github.com/shanraisshan/claude-code-best-practice
[bhil]: https://github.com/camalus/BHIL-AI-First-Development-Toolkit
[claude-howto]: https://github.com/luongnv89/claude-howto
[dispatch]: https://github.com/bassimeledath/dispatch
[superpowers]: https://github.com/obra/superpowers
