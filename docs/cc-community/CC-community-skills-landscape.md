---
title: CC Community Skills Landscape
purpose: Survey of community-built Claude Code skill libraries — gstack (founder/engineering workflows), pm-skills (product management framework), claude-code-best-practice (knowledge base), claude-howto (example-driven learning), agent-skills (Google SDLC engineering), caveman (terse-output token compression), last30days (real-time social research across 14+ platforms), agent-native (composable cross-agent meta-skills via @agent-native/skills CLI), modern-web-guidance (browser-vendor web-platform skill).
status: research
created: 2026-03-13
updated: 2026-11-22
validated_links: 2026-10-11
---

## Summary

Nine community skill libraries demonstrate distinct models for packaging CC capabilities: gstack enforces cognitive mode-switching through role-locked skills, pm-skills delivers professional frameworks as installable plugins, claude-code-best-practice curates a knowledge index of CC patterns and open questions, claude-howto delivers example-driven learning with production-ready templates, superpowers enforces a complete TDD-driven development methodology with subagent orchestration, agent-skills encodes Google engineering practices across the full SDLC, caveman compresses agent output via telegraphic-speech intensity levels, and last30days fans out real-time social research across 14+ platforms with engagement-scored synthesis, and agent-native packages composable cross-agent meta-skills installed à la carte via the `@agent-native/skills` CLI. Two later additions (2026-09-30, scored against the [agent substrate rubric][rubric]): coleam00/excalidraw-diagram-skill (a single diagram-generation skill with no license file) and cloudflare/security-audit-skill (a six-phase audit skill with adversarial validation and a JSON-schema-verified findings trail — the strongest `Traceable` score in this set). A third addition (2026-10-06, not rubric-scored — every skills·* cell is already filled in the census, so a new row would not move one): cathrynlavery/diagram-design, an editorial diagram-generation skill (44 diagram types by live file count; the README tagline says 42) spanning five hosts (Claude Code, Codex, GitHub Copilot, Factory Droid, Pi). A fourth addition (2026-10-11, also not rubric-scored — a new diagram/illustration row does not move a filled skills census cell): wheresryan22/anatomy, a Claude Code Agent Skill that turns a technical idea into an audited, interactive isometric SVG/WebGL/3D figure of a real machine. A fifth (2026-11-14, not rubric-scored): GoogleChrome/modern-web-guidance, a browser-vendor skill that retrieves current web-platform guides on demand through a bundled CLI, packaged as plugins for Claude Code and other hosts.

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
| Development Workflows | 9+ | everything-claude-code (137K stars), Superpowers (135K), Spec Kit (see [spec-driven-frameworks-landscape.md](../non-cc/frameworks/spec-driven-frameworks-landscape.md)), gstack, GSD, BMAD-METHOD, OpenSpec, oh-my-claudecode, Compound Engineering, HumanLayer — with uniqueness badges and component breakdowns |
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

## claude-howto (luongnv89)

**Repo**: [luongnv89/claude-howto][claude-howto] | **Stars**: 18.9K | **License**: MIT

Example-driven learning guide for Claude Code — 10 sequential modules covering slash commands, memory, skills, subagents, Model Context Protocol (MCP), hooks, plugins, checkpoints, advanced features, and CLI. Bridges the gap between official reference docs and production-ready implementation.

### Key Templates

- **Subagent definitions**: code-reviewer, test-engineer, security-auditor, documentation-writer
- **Hook scripts**: security scanning (PreToolUse), commit validation, formatting, team notifications
- **Skill bundles**: code-review, brand-voice, doc-generation
- **CLAUDE.md templates**: team, directory, and personal memory levels
- **MCP configs**: GitHub, database, filesystem, multi-server examples

### Relevance

Learning resource with production-ready templates, not a plugin. Where claude-code-best-practice indexes *what exists* and gstack delivers *opinionated workflows*, claude-howto demonstrates *how to combine* CC features into automated pipelines (11–13 hour structured curriculum, beginner → advanced).

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

## agent-skills (Addy Osmani)

**Repo**: [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | **Stars**: 5,554 | **License**: MIT

19 production-grade SDLC skills, 7 slash commands, 3 agent personas, and 4 reference checklists. Platform-agnostic (Claude Code, Cursor, Gemini CLI, Windsurf, GitHub Copilot). Heavily influenced by [Google's engineering practices](https://google.github.io/eng-practices/) and [Software Engineering at Google](https://abseil.io/resources/swe-book).

### SDLC Phase Mapping

```text
DEFINE -> PLAN -> BUILD -> VERIFY -> REVIEW -> SHIP
/spec    /plan   /build   /test     /review   /ship
                                    /code-simplify
```

### All 19 Skills

| Phase | Skill | What It Does |
|-------|-------|-------------|
| Define | `idea-refine` | Structured divergent/convergent thinking to turn vague ideas into concrete proposals |
| Define | `spec-driven-development` | Write a PRD covering objectives, commands, structure, code style, testing, boundaries before any code |
| Plan | `planning-and-task-breakdown` | Decompose specs into small verifiable tasks with acceptance criteria and dependency ordering |
| Build | `incremental-implementation` | Thin vertical slices: implement, test, verify, commit. Feature flags, safe defaults, rollback-friendly |
| Build | `test-driven-development` | Red-Green-Refactor, test pyramid (80/15/5), DAMP over DRY, Beyonce Rule |
| Build | `context-engineering` | Feed agents the right information at the right time: rules files, context packing, MCP integrations |
| Build | `frontend-ui-engineering` | Component architecture, design systems, state management, WCAG 2.1 AA accessibility |
| Build | `api-and-interface-design` | Contract-first design, Hyrum's Law, One-Version Rule, error semantics, boundary validation |
| Verify | `browser-testing-with-devtools` | Chrome DevTools MCP for live runtime data: DOM, console, network, performance |
| Verify | `debugging-and-error-recovery` | Five-step triage: reproduce, localize, reduce, fix, guard |
| Review | `code-review-and-quality` | Five-axis review, ~100 line changes, severity labels, splitting strategies |
| Review | `code-simplification` | Chesterton's Fence, Rule of 500, reduce complexity preserving behavior |
| Review | `security-and-hardening` | OWASP Top 10 prevention, auth patterns, secrets management, dependency auditing |
| Review | `performance-optimization` | Measure-first: Core Web Vitals targets, profiling workflows, bundle analysis |
| Ship | `git-workflow-and-versioning` | Trunk-based development, atomic commits, commit-as-save-point pattern |
| Ship | `ci-cd-and-automation` | Shift Left, Faster is Safer, feature flags, quality gate pipelines |
| Ship | `deprecation-and-migration` | Code-as-liability mindset, compulsory vs advisory deprecation, zombie code removal |
| Ship | `documentation-and-adrs` | Architecture Decision Records, API docs, document the "why" |
| Ship | `shipping-and-launch` | Pre-launch checklists, feature flag lifecycle, staged rollouts, monitoring setup |

### Agent Personas (3) and Reference Checklists (4)

| Agent | Role | Perspective |
|-------|------|-------------|
| `code-reviewer` | Senior Staff Engineer | Five-axis code review: "would a staff engineer approve this?" |
| `test-engineer` | QA Specialist | Test strategy, coverage analysis, Prove-It pattern |
| `security-auditor` | Security Engineer | Vulnerability detection, threat modeling, OWASP assessment |

Checklists: `testing-patterns.md`, `security-checklist.md`, `performance-checklist.md`, `accessibility-checklist.md`.

### Google Engineering Practices Embedded

Hyrum's Law, Beyonce Rule, Test Pyramid (80/15/5), One-Version Rule, Change sizing (~100 LOC), Chesterton's Fence, Trunk-based development, Shift Left — sourced from [SWE Book](https://abseil.io/resources/swe-book) and [Eng Practices Guide](https://google.github.io/eng-practices/).

### Skill Design Pattern

Every skill follows: Frontmatter -> Overview -> When to Use -> Process -> **Rationalizations** (anti-rationalization table) -> Red Flags -> Verification. Key principle: *"Seems right" is never sufficient — every skill requires concrete evidence.*

### Key Differentiator

Where gstack locks cognitive *modes*, pm-skills delivers domain *frameworks*, and superpowers enforces *TDD methodology*, agent-skills embeds **Google senior-engineer culture** (Hyrum's Law, Beyonce Rule, Chesterton's Fence) into anti-rationalization-guarded workflows across the full SDLC. The anti-rationalization tables (per skill) are a unique contribution — they enumerate excuses agents use to skip steps and provide counter-arguments.

Cross-ref: [Addy Osmani: Claude Code Agent Teams](https://addyosmani.com/blog/claude-code-agent-teams/) (referenced in [CC-agent-teams-orchestration.md](../cc-native/agents-skills/CC-agent-teams-orchestration.md))

## Caveman (JuliusBrussee)

**Repo**: [JuliusBrussee/caveman][caveman] | **Stars**: ~122K | **License**: Apache-2.0 | **Version**: v4.2.0 (2026-11-22) | all as of 2026-11-22 ([GitHub API][caveman-api], [LICENSE][caveman-license], [releases][caveman-releases])

**Site**: [caveman.so][caveman-site], the project's own site (it links the repo; `getcaveman.dev` serves the same page and declares `caveman.so` canonical) · **Docs**: [docs.caveman.so][caveman-docs] (the repo's homepage field) · read 2026-11-22

Started in April 2026 as a skill pack that compresses agent **output** by switching the assistant into telegraphic-speech registers; tagline *"why use many token when few do trick"*. Since 4.0 it is a skill plus a local proxy and CLI for coding agents: the README lists 30+ supported agents, and describes the shorter-answers skill as one of six parts, each with its own on/off switch ([README][caveman]). Passes the pruning rule in [CONTRIBUTING § Pruning entries](../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter): usable artifact, not archived, last push 2026-11-22, well above 1,000 stars.

**Licence history** ([LICENSING.md][caveman-licensing]): releases before 3.0.0 kept the terms they shipped with (MIT for the skill and adoption surfaces, a source-available Business Source License for the runtime); from 3.0.0 the whole repository is Apache-2.0. The earlier "MIT" entry in this doc was correct for v1.6.0, whose LICENSE file is MIT ([v1.6.0 LICENSE][caveman-v160-license]). The hosted Caveman Cloud service is separate commercial software outside the repository licence.

### The six parts (v4.2.0 README, 2026-11-22)

| Part | What it does | Evidence level |
|------|--------------|----------------|
| Say less | The skill: terse output, code and error text untouched; modes `/caveman`, `/ultracave`, `/megacave` | Author-run, 10 questions on one model: 4,119 vs 4,334 output tokens for the plain instruction "Answer concisely." (about 3% less); `/ultracave` 2,693 (about 35% less). The README says it measured the 3.1.0 rules and has not re-run |
| Read less | Shrinks logs, JSON, CSV and test output before the model reads them; originals kept on disk | Author-run: 33.2% fewer input tokens over six synthetic large-output tasks (Aug 2026 engine); HTML not compressed yet |
| Auto | Routes each request to a model and effort level; needs a free account | Author-run interim: 0.46x the cost of Opus 5.5 at xhigh on 85 tasks; the README states the score gap is unresolved |
| Blocks | Code mode: reusable scripts kept in the repo | Pre-release (v0.1.0-rc.5), own repo [caveman-ai/blocks](https://github.com/caveman-ai/blocks) |
| Waste fixes | `caveman learn` ranks where tokens go; keeps the prompt cache warm while you pause | "Not measured yet" per the README |
| Browse | Compressed web pages for the agent | Author-run, one 200-row table |

All numbers above are self-reported by the author, as is the README's Terminal-Bench comparison. Two outside sources, checked 2026-11-22:

- **JetBrains A/B** ([JetBrains AI blog, July 2026][caveman-jetbrains]): a paired A/B on Claude Code over 86 of the 87 SkillsBench tasks, with the skill forced on. Measured output-token saving was 8.5% against the advertised 65%, which the post calls "the ceiling, not the usual-case result"; average task score was 0.326 without the skill and 0.311 with it, a difference that a sign test puts at p = 0.82 (not significant).
- **CAVEWOMAN paper** ([arXiv 2606.24083][caveman-cavewoman], submitted 2026-06-23; the README attributes it to Adobe Research, the abstract page lists no affiliation): in a study of eight models on five datasets, caveman-style output compression cut realised cost by 1.4-2.4x per model on most API models, while compressing the user's prompt raised net cost (about 1.15x on the five-benchmark mean) as accuracy fell. It studies the style, not this repository's code.

The earlier figures in this entry (about 75% headline, 65% average over 10 tasks with a 22-87% range) no longer appear in the README, so they are dropped.

### Skills

| Skill | Purpose |
|-------|---------|
| `/caveman` · `/ultracave` · `/megacave` | The output voice at three compression levels (`megacave` uses Classical Chinese; v1.6.0 offered this as `/caveman wenyan` modes) |
| `caveman-commit` | One-line conventional commit |
| `caveman-review` | One finding per line |
| `caveman-compress` | Shrinks memory files such as `CLAUDE.md`, keeps a backup; README bench on five files: 4,138 vs 6,198 tokens (22.8-49.1% each, author-run; replaces the earlier "~46% average") |
| `caveman-stats` · `caveman-help` | Token usage for the session; quick reference |
| `cavecrew` | Subagents that report back tersely |
| `investigate-first`, `lean-build`, `surgical-patch`, `safe-refactor`, `migration`, `verify-and-stop` | Work-pattern skills that aim to write less code |

### Installation

```bash
# Everything (skill + CLI/proxy); needs Node.js 22.13+
npx @caveman-ai/cli@latest

# Skill only
npx skills add JuliusBrussee/caveman -g

# Claude Code plugin
claude plugin marketplace add JuliusBrussee/caveman && claude plugin install caveman@caveman

# Gemini CLI
gemini extensions install https://github.com/JuliusBrussee/caveman
```

### Activation

Type `/caveman` (`$caveman` in Codex) if it does not start on its own; `stop caveman` returns to normal ([README][caveman]). The old trigger phrases listed here before are not in the current README.

### Privacy and cost caveats

Per the README: the skill sends nothing, except `/caveman-compress`, which sends the file to your model provider. The CLI sends usage statistics by default (opt out with `caveman telemetry off` or `DO_NOT_TRACK=1`). Auto sends request content to Caveman Cloud once you sign in. The skill rules cost about 1,160 input tokens, and the README notes shorter answers save nothing where billing is per request (GitHub Copilot). The README header also promotes a separate desktop coding app, Caveman Code, with its own vendor benchmark; not assessed here.

### Key Differentiator

Where RTK compresses **tool output** going *into* context (see [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md)), caveman began as compression of the **assistant's own output** and now also covers the input side (Read less) and routing. By the author's own numbers the output-voice gain over a plain "Answer concisely." instruction is small (about 3%), and the one independent A/B measured 8.5% on agentic tasks; the larger author-run figures are for the input side and routing.

Cross-ref: [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) — RTK (output ingestion compression), CodeBurn (token-usage observability)

## last30days (mvanhorn)

**Repo**: [mvanhorn/last30days-skill][last30days] | **Stars**: 34,179 | **License**: MIT | **Version**: v3.x

Real-time social-research skill. Fans out parallel searches across 14+ platforms simultaneously and synthesizes results with an AI judge:

**Platforms searched**: Reddit (with top comments), X/Twitter, YouTube (full transcripts), TikTok, Instagram Reels, Hacker News, Polymarket (prediction markets with real-money odds), GitHub, Bluesky, Threads, Pinterest, Digg (AI-curated X leaderboard), Perplexity Sonar (grounded web), editorial web coverage.

**Design pattern**: Parallel fan-out — all sources queried concurrently, results scored by engagement metrics (upvotes, views, prediction odds), duplicate stories merged into clusters, AI-judge synthesis with citations. Pre-research entity resolution identifies relevant handles, subreddits, and hashtags before searching.

**Installation**:

```bash
# Claude Code (recommended)
/plugin marketplace add mvanhorn/last30days-skill

# Other agents (50+ hosts)
npx skills add mvanhorn/last30days-skill -g
```

**Key differentiator**: Only real-time social-consensus skill in the landscape — ranks by actual engagement rather than SEO/editorial algorithms, includes prediction-market odds alongside discourse, and outputs shareable self-contained HTML briefs. No tracking; research stays local.

## agent-native skills (Builder.io)

**Repo**: [BuilderIO/skills][builderio-skills] | **Stars**: 1.5K | **License**: MIT | **Version**: v0.2.35 (2026-06-19, npm `@agent-native/skills`)

Ten à-la-carte, cross-agent **meta-skills** — orchestration, review, and guardrail capabilities rather than a full methodology. Installed via the `@agent-native/skills` CLI through the shared `.agents` path (Codex, Pi, Cursor, OpenCode, GitHub Copilot / VS Code) plus Claude Code's native skills path. Visual outputs render as MDX.

| Skill | Purpose |
|-------|---------|
| `/visual-plan` | Turn text plans into interactive visual plans (diagrams, file maps, annotated code) |
| `/visual-recap` | Turn a branch/commit/PR diff into a visual recap with annotated diffs |
| `/agent-watchdog` | Audit another agent's work from a Codex/Claude Code transcript, PR, branch, or run summary |
| `/plan-arbiter` | Compare competing agent plans and choose one executable direction |
| `/plow-ahead` | Work through ordinary ambiguity and finish with a clear decision recap |
| `/efficient-fable` | Use Claude Fable as orchestrator, architect, synthesizer, and final judge |
| `/efficient-frontier` | Apply the same orchestration to any high-cost frontier model |
| `/stay-within-limits` | Check current 5-hour and weekly usage before substantial work |
| `/quick-recap` | Append a concise final status block to every completed response |
| `/read-the-damn-docs` | Web-search authoritative docs before guessing from stale model memory |

### Installation

```bash
npx @agent-native/skills@latest add                  # choose skills interactively
npx @agent-native/skills@latest add --skill quick-recap
```

### Key Differentiator

Where gstack locks cognitive *modes*, pm-skills delivers domain *frameworks*, superpowers enforces a *TDD methodology*, and agent-skills embeds *Google SDLC culture*, agent-native ships **composable cross-agent meta-skills** adopted individually — orchestration (`/plan-arbiter`, `/efficient-fable`), self-audit (`/agent-watchdog`), and budget/quality guardrails (`/stay-within-limits`, `/read-the-damn-docs`). The Fable-orchestration skills and the usage-budget skill are distinctive in this set.

Cross-ref: [CC-skills-adoption-analysis.md](../cc-native/agents-skills/CC-skills-adoption-analysis.md) — native skills format these install into.

## coleam00 (Cole Medin): excalidraw-diagram-skill

**Repo**: [coleam00/excalidraw-diagram-skill][excalidraw-skill] | **Stars**: 5,240 (2026-11-12) | **License**: none
found — the repo ships no `LICENSE` file and GitHub's own license detector returns `null`; only
`.gitignore`, `README.md`, `SKILL.md`, and `references/` are present (checked via the GitHub contents
API, 2026-09-30). A single skill that generates `.excalidraw` JSON diagrams designed to "argue, not
display" — a depth-assessment step, a research mandate for technical diagrams (look up real event/API
names before drawing), a visual-pattern library (fan-out, convergence, tree, timeline, assembly line),
and a mandatory render-view-fix loop (`uv run python render_excalidraw.py`) that reads the rendered PNG
back before declaring the diagram done.

`subject: skills`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no data [SKILL.md][excalidraw-skill] (rule 6: a git-hosted static artifact with no documented contribution flow; full repo tree checked 2026-10-02, no CONTRIBUTING file or PR template) | no data [SKILL.md][excalidraw-skill] (rule 6: a git-hosted static artifact with no documented contribution flow; full repo tree checked 2026-10-02, no CONTRIBUTING file or PR template) | n/a [SKILL.md][excalidraw-skill] (a static procedure, not a generated/extracted artifact — "reproducible rebuild" doesn't apply) | yes [SKILL.md][excalidraw-skill] ("All colors and brand-specific styles live in one file: `references/color-palette.md`... To make this skill produce diagrams in your own brand style, edit `color-palette.md`" — a documented config/extension point, not a rewrite) | yes [SKILL.md][excalidraw-skill] (plain-file, git-hosted; no license, but the source itself is version-controlled) | no data [SKILL.md][excalidraw-skill] (no logging of what it renders; the render-view-fix loop is a quality check, not an audit trail) |

`scored 2026-09-30`

## cathrynlavery/diagram-design

**Repo**: [cathrynlavery/diagram-design][diagram-design] | **Stars**: 43,595 | **Forks**: 2,820 |
**License**: MIT | pushed 2026-10-06 (`gh api`, 2026-10-06)

A Claude Code skill and multi-host Agent-Skills plugin, distinct from the single-renderer
excalidraw-diagram-skill above: it targets five hosts out of the box. The repo's own description field:
*"Editorial diagram design for Claude Code, Codex, GitHub Copilot, Factory Droid, and Pi. 42 diagram
types. Self-contained HTML + SVG. No shadows. No Mermaid slop."* Each diagram renders to a
dependency-free HTML+SVG file (no JS, no shadows). The description field says "42 diagram types"; a
live count of `skills/diagram-design/references/type-*.md` files (`gh api`, 2026-10-06) returns
**44** — architecture, flowchart, sequence, ER, swimlane, Gantt, scatter, treemap and Wardley among
them, plus (per the README's own 2.5.10 changelog note, verbatim) *"ten more layout grammars —
Sankey, fishbone, Wardley map, kanban, user journey, deployment, dependency graph, UML class, story
map, and database schema."* The 42-vs-44 gap is most likely post-description additions
(`type-architecture-delta.md`, `type-axonometric-plan.md`); cite the live count, not the tagline.

### Installation (per host)

| Host | Command |
|---|---|
| Claude Code | `/plugin marketplace add cathrynlavery/diagram-design` |
| Codex | `codex plugin marketplace add cathrynlavery/diagram-design` |
| GitHub Copilot | `copilot plugin marketplace add cathrynlavery/diagram-design` |
| Factory Droid | `droid plugin marketplace add https://github.com/cathrynlavery/diagram-design` |
| Pi | `pi install https://github.com/cathrynlavery/diagram-design` |
| Kiro | Import the Agent Skill from the repo's `skills/diagram-design` subdirectory URL |
| OpenCode | Symlink or copy `skills/diagram-design/` into `.opencode/skills/` |

### Design Philosophy

States "No Figma. No generic rounded boxes. No 30-minute color-picking sessions." (README). Fixed
styling constraints: one accent color with 1–2 focal elements per diagram, three typefaces (Instrument
Serif / Geist / Geist Mono), 1px hairlines, no shadows, max 10px border-radius, and coordinates/widths
kept divisible by 4 to avoid an AI-generated look. A brand-onboarding step extracts colors/fonts from a
target website; a separate import path redraws existing draw.io/Mermaid/Excalidraw diagrams at a chosen
fidelity (faithful/balanced/simplified); exports to PNG, SVG, HTML, or diagram-block JSON.

### Adoption Considerations

**Strengths**: five first-class host integrations plus a documented import/symlink path for two more;
MIT; 44 diagram types (live count) in one skill is a broader surface than any single-purpose diagram
tool in this doc (excalidraw-diagram-skill above covers one renderer); dependency-free HTML+SVG output
opens offline in a browser with no server or JS runtime.

**Risks**: fast-moving (repo created 2026-04-16, still pushing commits as of 2026-10-06) — installs are
explicitly unpinned-by-design on two hosts ("Droid tracks Git plugins by commit rather than the
manifest's display version"; "the unpinned Git install is intentional" for Pi, per the README), so a
team pinning exact output needs to track upstream commits itself; "Official builds come only from this
repository" (README) names LittleMight as the sole official publisher, implying unofficial-copy risk
for any other listing; the fixed house style (fonts/colors/grid) trades flexibility for consistency,
which may not suit every brand; overlaps with excalidraw-diagram-skill and any Mermaid-based workflow
for teams already standardized on one of those.

Cross-ref: [CC-skills-adoption-analysis.md](../cc-native/agents-skills/CC-skills-adoption-analysis.md) —
native skills format this installs into. See [visualization.md](../_topics/visualization.md) for this
corpus's other diagram/visualization tools.

## wheresryan22/anatomy

**Repo**: [wheresryan22/anatomy][anatomy] | **Stars**: 3,109 | **Forks**: 235 | **License**: MIT
(confirmed by reading the `LICENSE` file — "MIT License / Copyright (c) 2026 Ryan") | created
2026-10-08, pushed 2026-10-11 (`gh api`, 2026-10-11) — 3 days old.

A Claude Code [Agent Skill][cc-skills-doc] — a plain folder with a
`SKILL.md` at its root, not a plugin — that has Claude invent a real physical machine whose mechanism
*is* the technical idea being explained, then builds that machine as a crafted isometric figure. The
repo's own description field: "A Claude Code skill that turns a technical idea into a detailed,
interactive isometric figure of a real machine. It makes SVG with optional WebGL shaders and 3D, for
docs, articles and landing pages." Example prompt (README): `/anatomy explain how a token bucket rate
limiter works, interactive`.

### What It Outputs

Three kinds of figure sharing one drawing kit and isometric camera (README, "What it makes"):

| Kind | What it is |
|---|---|
| **SVG** | The core — solid isometric parts with four-tone shading, shipped as a standalone HTML page, a lone `.svg` file, or React/Next.js components |
| **SVG + WebGL** | A shader canvas sandwiched between back/front SVG layers, for fire, water, steam, or glow that flat lines can't draw — the SVG still reads without WebGL |
| **3D** (beta) | Parts that physically turn — re-projected and re-shaded every frame by the kit's own rules |

### Install

Four paths in, all installing the same `SKILL.md` folder — no plugin marketplace:

| Path | Command | Installs to |
|---|---|---|
| skills CLI, user-level | `npx skills add wheresryan22/anatomy -g -a claude-code` | `~/.claude/skills/anatomy` |
| skills CLI, project-level | `npx skills add wheresryan22/anatomy` | `.claude/skills/anatomy` |
| git clone | `git clone https://github.com/wheresryan22/anatomy.git .claude/skills/anatomy` | either path |
| ZIP download | unpack, rename to `anatomy`, move into the skills folder | `~/.claude/skills/anatomy` |

Zero npm dependencies — Node's built-in modules only (React 18+ is needed only for the optional React
output).

### Self-Verification Loop

`kit/audit.mjs` proves the geometry (nothing passes through anything, every pipe/cable end sits on a
mount, overlaps draw in depth order); `scripts/capture.mjs` and `scripts/drive.mjs` then screenshot the built
figure in headless Chrome, and the skill instructs Claude to read every PNG it produces before
declaring the figure done — the same render-view-fix discipline as `coleam00/excalidraw-diagram-skill`
above, with a geometric proof step added on top.

### Adoption Considerations

**Strengths**: zero dependencies; MIT; self-contained output (static HTML/SVG, no server or API key);
a concrete audit-plus-visual-verification loop rather than a one-shot render.

**Risks**: very new (3 days old at time of writing) with no independent usage signal beyond platform
stars; "slow on purpose" per its own README (a full build-plus-audit cycle can take minutes; a full 3D
orbit audit takes 15–20 minutes for 30 parts); the 3D mode is explicitly beta — "proved on its example
and one test figure, not yet on a production figure" (README).

Cross-ref: `coleam00/excalidraw-diagram-skill` and `cathrynlavery/diagram-design` above — same
diagram/illustration-generation category, but anatomy's isometric-machine metaphor and audited 3D
geometry are a different rendering approach from either. See
[visualization.md](../_topics/visualization.md) for this corpus's other diagram/visualization tools.

## cloudflare/security-audit-skill

**Repo**: [cloudflare/security-audit-skill][cf-sec-audit] | **Stars**: 23,302 | **License**: MIT |
pushed 2026-09-14

A coding-agent skill that runs a structured six-phase security audit — reconnaissance, coverage-led
hunting, candidate validation, structured output, independent record verification, target-neutral
reporting — and "seeded Cloudflare's vulnerability discovery harness" described in
[Cloudflare's own blog post][cf-blog]. Every finding lands in one of three verdicts (`confirmed`,
`needs_validation`, `rejected`) validated against a JSON schema by a zero-dependency validator that the
orchestrating agent runs at each audit phase — not in CI; **adversarial validation** is a named
design principle — "the agent that
checks a finding is never the agent that found it." A `coverage-ledger.json` tracks what was checked
(not just what was found), and multiple runs against the same repo are additive: "the skill uses prior
ledgers and findings to target gaps, revalidate changed source, and carry forward current-source
evidence."

`subject: skills`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no data [README][cf-sec-audit] (rule 6: a git-hosted static artifact with no documented contribution flow; full repo tree checked 2026-10-02, no CONTRIBUTING file or PR template) | no data [README][cf-sec-audit] (rule 6: a git-hosted static artifact with no documented contribution flow; full repo tree checked 2026-10-02, no CONTRIBUTING file or PR template) | partial [README][cf-sec-audit] (the `.cjs` validators are deterministic, zero-dependency; the hunting/validation phases themselves are LLM sub-agent calls with no pinned model) | yes [README][cf-sec-audit] (13 hunting-class reference files cover different target types — web, cloud, client-side, supply-chain, binary — swappable per audit scope) | yes [README][cf-sec-audit] (per-repo `coverage-ledger.json` and `findings.json` are additive across runs, so state accumulates rather than resets) | yes [README][cf-sec-audit] (`confirmed` verdicts carry "a complete source trace and bounded observed result"; independent-verifier re-checks before a finding is finalized) |

`scored 2026-09-30`

See also the offensive-security skill bundles [Claude-BugHunter][cbh], [pentest-ai-agents][psa] and [communitytools][ct] (authorized testing), compared in [agentic-ai-vulnerability-landscape.md](../sdlc-lcm/agentic-ai-vulnerability-landscape.md#7-offensive-security-agents-authorized-testing).

## GoogleChrome/modern-web-guidance

**Repo**: [GoogleChrome/modern-web-guidance][mwg-repo] | **Stars**: 14,896 | **License**: Apache-2.0 |
created 2026-03-23, pushed 2026-11-10 (`gh api`, 2026-11-14) | **Docs**: [developer.chrome.com][mwg-docs]

A vendor-maintained skill, unlike the community libraries above: the README says it is "Stewarded by the
Google Chrome, Microsoft Edge, Mozilla Firefox, and MDN teams". It targets one failure: coding agents
"often default to older patterns because LLM training data contains vast amounts of legacy code".

**Skill, tool or package? All three, in layers.**

- **Skill (the core).** Two Agent Skills under `skills/`: `modern-web-guidance` and `chrome-extensions`
  (Manifest V3). The main `SKILL.md` describes itself as a "Search tool for modern web development best
  practices" and tells the agent to run it first for HTML/CSS and client-side JS work, and not for
  backend, infra or tooling tasks.
- **CLI tool inside the skill.** The skill doesn't inline its guides; it has the agent run
  `npx -y modern-web-guidance@latest search "<query>"` (then `retrieve <id>`), so only the matching guide
  enters the context. A third command, `legacy-scan`, scans a codebase for legacy patterns. Guides cover
  250 web features and 203 use cases (README counts), including WebMCP guides for exposing page
  functions as agent tools.
- **npm package.** `modern-web-guidance` on npm (v1.0.0, 121 published versions since 2026-04-30,
  Apache-2.0; the package's `bin` is the skill's own `modern-web.mjs`).
- **Plugin packaging for many hosts.** The same repo ships a Claude Code plugin and marketplace
  (`.claude-plugin/marketplace.json`, marketplace `googlechrome`: `/plugin marketplace add
  GoogleChrome/modern-web-guidance`, then `/plugin install modern-web-guidance@googlechrome`), a GitHub
  Copilot plugin, a Gemini CLI extension, a VS Code `chatSkills` contribution, and documented installs for
  Codex, Antigravity, Grok Build, Kimi Code, `npx skills` and `gh skill`.

**Eval loop.** The README describes how guides are kept: expert-written guides, tasks on real web apps
with Playwright graders, graders calibrated to pass 100% of golden solutions and fail 100% of the
unmodified app, then coding agents run with and without the skill. Guides that agents no longer need are
pruned ("uplift" = guided minus unguided pass rate). The README's latest snapshot (vendor-run, 2026-11-08)
reports Claude Code (Opus 5.5) at 57% → 88% on 215 tasks, with Codex CLI and Antigravity in the same
range; the [eval dashboard][mwg-evals] has per-guide breakdowns.

**Why it matters here.** It is the clearest example so far of a browser vendor shipping guidance *to
agents* as a skill with retrieval on demand rather than a long prompt, and of a skill maintained by
measured uplift. Cross-ref: WebMCP in
[browser-agents-landscape.md](../non-cc/agents/browser-agents-landscape.md#webmcp), and the agent-readiness material in
[ai-crawlers-discoverability-landscape.md](../non-cc/infrastructure/ai-crawlers-discoverability-landscape.md).

## cursor/plugins pstack (Lauren Tan)

**Repo**: [cursor/plugins `pstack/`][pstack-repo] | **License**: MIT (`pstack/LICENSE`, plugin.json 0.15.46) |
repo 17,719 stars, `pstack/` last touched 2026-11-19 (`gh api`, 2026-11-20)

A skill pack published in Cursor's own plugin repository (described as "Cursor plugin specification and
official plugins") but also installable in Claude Code (`/plugin marketplace add cursor/plugins`, then
`/plugin install pstack@cursor-plugins`). The author's stated aim (README, a claim not a measurement) is
less but higher-quality code so that several agents can run in parallel with trust. The entry point is
`/poteto-mode`, which per the README picks one of 22 playbooks (bug fix, perf, hillclimb, refactoring,
babysit a PR, shipping, autonomous run, session pickup, worktree cleanup, opening a PR, and others),
copies its steps into a todo list and calls the other skills as needed; `skills/` holds 58 entries
(directory count, 2026-11-20). `/setup-pstack` writes model choices; in Claude Code it saves them to
`~/.claude/rules/pstack-models.md`, and Cursor-only steps (Bugbot, automations) are skipped with a note.
Defaults route many roles to named frontier models and a three-model review panel; that is configuration
in the README, not a tested result.

**Why it matters here.** A vendor-hosted, cross-harness workflow pack on the gstack/Superpowers
model: methodology delivered as a playbook-router skill plus a Claude Code adapter generated from the
Cursor tree.

## Cross-References

- [CC-skills-adoption-analysis.md](../cc-native/agents-skills/CC-skills-adoption-analysis.md) — native skills format and adoption
- [CC-plans-as-skill-rule-templates.md](../cc-native/agents-skills/CC-plans-as-skill-rule-templates.md) — plan-to-skill extraction (gstack's `/plan-*` skills are concrete examples)
- [CC-official-plugins-landscape.md](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) — official plugin ecosystem
- [CC-community-plugins-landscape.md](CC-community-plugins-landscape.md) — plugin catalogs
- [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) — claude-mem persistent memory
- [agents-cli-analysis.md](../non-cc/frameworks/agents-cli-analysis.md) — Google agents-cli installs as a CC skill-pack (`npx skills add`) but is cross-agent; deeper analysis lives in non-cc

## Not included

Entries removed under the [pruning rule](../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (alive, adopted or proven; checked 2026-11-21).

| Name | Reason | Date | Link |
|---|---|---|---|
| BHIL AI-First Development Toolkit | 134 stars (repo now at PolymathWizard); no measured benefit or named independent users found in its README, docs or tree (it ships eval and ADR templates only); last push 2026-03-28 (`gh api` 2026-11-21) | 2026-11-21 | <https://github.com/PolymathWizard/BHIL-AI-First-Development-Toolkit> |
| dispatch | 411 stars; no measured benefit or named independent users in its README or tree; no releases; last push 2026-04-06 (`gh api` 2026-11-21) | 2026-11-21 | <https://github.com/bassimeledath/dispatch> |
| claude-howto fork (Master Claude Code in a Weekend) | 11 stars; a repackaged copy of luongnv89/claude-howto with no original content; last push 2026-03-27 (`gh api` 2026-11-21) | 2026-11-21 | <https://github.com/akolaarthurali/claude-howto-Master-Claude-Code-in-a-Weekend> |
| coleam00/skills | 777 stars; its README states no measured benefit and names no independent users (`gh api` 2026-11-21) | 2026-11-21 | <https://github.com/coleam00/skills> |
| stevesolun/ctx | 593 stars; its benchmark folder documents a protocol, not a published result, and says controlled fixtures do not measure recommendation relevance; no named independent users (`gh api` 2026-11-21) | 2026-11-21 | <https://github.com/stevesolun/ctx> |

## Sources

| Source | Content |
|---|---|
| [gstack][gstack] | Founder/engineering workflow skills |
| [pm-skills][pm-skills] | Product management skill framework |
| [claude-code-best-practice][ccbp] | Community knowledge base |
| [claude-howto][claude-howto] | Example-driven CC learning guide (10 modules, templates) |
| [superpowers][superpowers] | Agentic skills framework & dev methodology (135K stars) |
| [agent-skills][agent-skills] | Google SDLC engineering skill pack (5,554 stars) |
| [modern-web-guidance][mwg-repo] · [docs][mwg-docs] · [eval dashboard][mwg-evals] | Browser-vendor web-platform skill, CLI, plugin manifests, eval loop |
| [caveman][caveman] | Output-voice skill plus local token-saving proxy and CLI (~122K stars, Apache-2.0, v4.2.0, 2026-11-22) |
| [caveman LICENSE][caveman-license] · [LICENSING.md][caveman-licensing] · [v1.6.0 LICENSE][caveman-v160-license] · [releases][caveman-releases] · [repo API][caveman-api] | Caveman licence history, latest version and repo stats, checked 2026-11-22 |
| [JetBrains A/B][caveman-jetbrains] | Independent paired A/B of caveman on SkillsBench: 8.5% output-token saving, no significant score difference (p = 0.82), checked 2026-11-22 |
| [CAVEWOMAN, arXiv 2606.24083][caveman-cavewoman] | Study of caveman-style output and input compression across eight models, checked 2026-11-22 |
| [last30days][last30days] | Real-time social research across 14+ platforms (34K+ stars) |
| [agent-native skills][builderio-skills] | Composable cross-agent meta-skills (visual plan/recap, watchdog, guardrails) |
| [coleam00/excalidraw-diagram-skill][excalidraw-skill] | Excalidraw diagram-generation skill (5,240 stars, no license file, 2026-11-12) |
| [cloudflare/security-audit-skill][cf-sec-audit] | Six-phase coding-agent security-audit skill (23,302 stars, MIT) |
| [Claude-BugHunter][cbh] · [pentest-ai-agents][psa] · [communitytools][ct] | Offensive-security skill bundles for authorized testing (stars and details in the linked comparison, 2026-11-17) |
| [Cloudflare: Build your own vulnerability harness][cf-blog] | Cloudflare's own account of the harness this skill seeded |
| [cathrynlavery/diagram-design][diagram-design] | Editorial diagram-design skill for Claude Code, Codex, Copilot, Droid, Pi — 44 types by live count, README tagline says 42 (43,595 stars, MIT; `gh api` 2026-10-06) |
| [cursor/plugins pstack][pstack-repo] | Playbook-router skill pack (22 playbooks) for Cursor, installable in Claude Code (MIT; `gh api` 2026-11-20) |
| [wheresryan22/anatomy][anatomy] | Isometric interactive figure-generation Agent Skill, audited geometry + screenshot verification loop (3,109 stars, MIT; `gh api` 2026-10-11) |

[agent-skills]: https://github.com/addyosmani/agent-skills
[gstack]: https://github.com/garrytan/gstack
[pm-skills]: https://github.com/phuryn/pm-skills
[ccbp]: https://github.com/shanraisshan/claude-code-best-practice
[claude-howto]: https://github.com/luongnv89/claude-howto
[superpowers]: https://github.com/obra/superpowers
[caveman]: https://github.com/JuliusBrussee/caveman
[caveman-api]: https://api.github.com/repos/JuliusBrussee/caveman
[caveman-license]: https://github.com/JuliusBrussee/caveman/blob/main/LICENSE
[caveman-licensing]: https://github.com/JuliusBrussee/caveman/blob/main/LICENSING.md
[caveman-v160-license]: https://github.com/JuliusBrussee/caveman/blob/v1.6.0/LICENSE
[caveman-jetbrains]: https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/
[caveman-cavewoman]: https://arxiv.org/abs/2606.24083
[caveman-releases]: https://github.com/JuliusBrussee/caveman/releases
[caveman-site]: https://caveman.so/
[caveman-docs]: https://docs.caveman.so/caveman
[last30days]: https://github.com/mvanhorn/last30days-skill
[builderio-skills]: https://github.com/BuilderIO/skills
[excalidraw-skill]: https://github.com/coleam00/excalidraw-diagram-skill
[cf-sec-audit]: https://github.com/cloudflare/security-audit-skill
[cbh]: https://github.com/elementalsouls/Claude-BugHunter
[psa]: https://github.com/0xSteph/pentest-ai-agents
[ct]: https://github.com/transilienceai/communitytools
[cf-blog]: https://blog.cloudflare.com/build-your-own-vulnerability-harness
[diagram-design]: https://github.com/cathrynlavery/diagram-design
[anatomy]: https://github.com/wheresryan22/anatomy
[cc-skills-doc]: https://code.claude.com/docs/en/skills
[rubric]: ../sdlc-lcm/agent-substrate-rubric.md
[mwg-repo]: https://github.com/GoogleChrome/modern-web-guidance
[pstack-repo]: https://github.com/cursor/plugins/tree/main/pstack
[mwg-docs]: https://developer.chrome.com/docs/modern-web-guidance
[mwg-evals]: https://googlechrome.github.io/modern-web-guidance-src/
