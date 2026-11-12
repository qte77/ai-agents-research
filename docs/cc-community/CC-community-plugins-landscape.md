---
title: CC Community Plugins Landscape
description: Survey of community plugin catalogs — awesome-claude-code (curated resource list) and awesome-claude-code-plugins (installable plugin registry with marketplace format).
category: landscape
status: research
created: 2026-03-13
updated: 2026-11-12
validated_links: 2026-11-12
---

## Summary

Two community-maintained catalogs serve complementary roles: awesome-claude-code is a broad curated resource list (~100-200+ entries across 9 categories), while awesome-claude-code-plugins is a structured plugin registry (~136 installable plugins across 13 categories with marketplace format). Together they represent the community ecosystem around Claude Code extensions.

## awesome-claude-code (hesreallyhim)

**Repo**: [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | **License**: CC BY-NC-ND 4.0

A curated "awesome list" of Claude Code resources — links, tools, configurations, and methodologies. Not a plugin registry; catalogs anything useful for CC users.

### Categories (9)

| Category | Description | Notable Entries |
|----------|-------------|-----------------|
| Agent Skills | Model-controlled specialized task configs | 16+ entries; Claude Scientific Skills, DevOps/security skills |
| Workflows & Knowledge Guides | Development methodologies and project guidance | 22+ entries; Ralph Wiggum Pattern (5+ implementations), Auto-Claude (multi-agent SDLC with kanban) |
| Tooling | Applications built on CC | IDE integrations, usage monitors (ccflare), orchestrators, config managers |
| Status Lines | Terminal customizations | CC usage metrics display |
| Hooks | Lifecycle hook configurations | Pre/post tool call, session, stop events |
| Slash Commands | Custom prompt/action definitions | ~40+ entries (largest section) |
| CLAUDE.md Files | Language/domain-specific instruction files | Project templates and examples |
| Alternative Clients | Non-default UIs and front-ends | Community-built interfaces |
| Official Documentation | Anthropic reference materials | Canonical docs links |

### Contribution Model

- Submissions via automated GitHub issue template ("Recommend a new resource here")
- **Unique constraint**: *"The only person who is allowed to submit PRs to this repo is Claude"* — humans open issues, Claude Code handles PRs
- Multiple display formats: Awesome, Extra, Classic, Flat views + CSV table

### Key Patterns

- **Ralph Wiggum Pattern** has a dedicated subcategory with 5+ implementations cataloged
- Strong representation of DevOps, infrastructure automation, and security tooling
- Multiple session management and context continuity solutions
- Serves as community health indicator — entry velocity tracks ecosystem adoption

## awesome-claude-code-plugins (ccplugins)

**Repo**: [ccplugins/awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins) | **License**: Apache-2.0

A structured plugin registry organized around Claude Code's installable plugin format (`/plugin` command, `.claude-plugin/marketplace.json`).

### Categories (13)

| Category | Plugins | Notable Focus |
|----------|---------|---------------|
| Official Claude Code Plugins | 5 | Anthropic-maintained |
| Code Quality Testing | 16 | Linting, testing, review automation |
| Development Engineering | 15 | Language-specific tooling, frameworks |
| Git Workflow | 14 | Review, branching, commit messaging |
| Project & Product Management | 10 | Agile, roadmapping, stakeholder tools |
| Business Sales | 8 | CRM, outreach, pipeline management |
| Workflow Orchestration | 8 | Multi-step automation, pipelines |
| Design UX | 8 | UI patterns, accessibility, prototyping |
| Documentation | 8 | Doc generation, API docs, changelogs |
| Marketing Growth | 7 | SEO, content, analytics |
| Security, Compliance & Legal | 7 | Vulnerability scanning, policy generation |
| Automation DevOps | 5 | CI/CD, infrastructure, deployment |
| Data Analytics | 5 | Dashboards, data processing, visualization |
| **Total** | **~136** | |

### Plugin System

- **Install**: `claude plugin install [plugin-name]` or `/plugin marketplace add user-or-org/repo-name`
- **Package format**: `.claude-plugin/marketplace.json` in a Git repo
- **Composability**: each plugin bundles slash commands + subagents + MCP servers + hooks as a single unit
- **Role-specific subagents**: plugins target named roles (data-scientist, frontend-developer, legal-advisor)
- **100% Python** implementation

### Contribution Model

- Open contributions: anyone can create and share a marketplace by publishing `.claude-plugin/marketplace.json`
- Decentralized: submit a link to your marketplace repo for inclusion

## Comparison

| Dimension | awesome-claude-code | awesome-claude-code-plugins |
|-----------|--------------------|-----------------------------|
| **Type** | Curated resource list (links, repos) | Installable plugin registry |
| **Scope** | Anything useful for CC users | Installable plugins only |
| **Entry format** | Free-form links to external repos | Plugin packages with manifest |
| **Installability** | Manual setup per resource | One-command via `/plugin` |
| **Business coverage** | Technical/developer focus | Includes Sales, Marketing, Legal |
| **Contribution** | Issue-only; Claude submits PRs | Open PRs; decentralized marketplaces |
| **License** | CC BY-NC-ND 4.0 (restrictive) | Apache-2.0 (permissive) |
| **Size** | ~100-200+ resources | ~136 plugins |
| **Unique content** | Workflow methodologies, CLAUDE.md examples, alternative clients | Business-function plugins, formal marketplace format |

## TTS / Voice Output Plugins (Emerging Category)

8+ community projects add text-to-speech output to Claude Code. All converge on the same pattern: Stop hook → sentence chunking → TTS → non-blocking playback. CC has native `/voice` for STT input but **no native TTS output**.

| Project | Engine | Key Feature | Local/OSS |
|---------|--------|-------------|-----------|
| [ybouhjira/claude-code-tts][tts-ybou] | OpenAI API | Worker pool, cross-platform, `speak-text` CLI | No |
| [~cg/claude-code-tts][tts-cg] | Kokoro | Smart interruption, markdown stripping | Yes |
| [ktaletsk/claude-code-tts][tts-ktal] | Kokoro | Audio ducking | Yes |
| [LAURA-agent/Claude-to-Speech][tts-laura] | ElevenLabs | Invisible markers, smart defaults (silent for code) | No |
| [mbailey/voicemode][tts-voice] | Kokoro/cloud | Full 2-way voice (Whisper STT + TTS), MCP server | Yes |
| [johnmatthewtennant/mcp-voice-hooks][tts-mcp] | Various | MCP server for voice I/O | Depends |
| [husniadil/cc-hooks][tts-hooks] | Multi-provider | Sound effects, TTS announcements | Depends |
| [shanraisshan/claude-code-hooks][tts-shanr] | Various | Voice via hooks (Stop, PreToolUse, PostToolUse) | Depends |

**Common pattern**: All use the Stop hook (fires after full response). No project has achieved true mid-generation streaming — CC exposes no streaming hook in interactive mode. `--output-format stream-json` enables token-level streaming but only in headless mode (`claude -p`).

**TTS engines used**: Kokoro (most popular local), OpenAI TTS API (most polished cloud), ElevenLabs (highest quality cloud), espeak-ng (fallback). [RealtimeTTS][realtimetts] library provides sentence-boundary detection with 12+ engine backends.

## STT / Voice Input (Community Alternatives)

CC has native push-to-talk voice dictation via `/voice` — cloud-only, requires Claude.ai account, 20 languages, coding-tuned transcription. See [official voice dictation docs][voice-docs] for details. The community projects below address gaps: local/offline STT, continuous listening, and wake-word activation.

### Local STT Engines

| Engine | Params | Latency (10s audio) | Designed For | Notes |
|--------|--------|---------------------|-------------|-------|
| [Moonshine][moonshine] | 34M (tiny) – 245M (medium) | 34ms (tiny, MacBook) – 802ms (medium, RPi5) | Edge/mobile/IoT | Variable-length input, no zero-padding; 8 languages ([source][moonshine]) |
| [whisper.cpp][whispercpp] | 39M (tiny) – 1.5B (large) | ~200-500ms (medium, CPU) | Desktop/server | C++ port of OpenAI Whisper; GPU acceleration; 99 languages |
| [Vosk][vosk] | 50MB (small model) | Real-time streaming | Lightweight/embedded | Continuous listening built-in; offline; 20+ languages |

### Community Voice Input Projects

| Project | Engine | Integration | Status |
|---------|--------|-------------|--------|
| [jarrodwatts/claude-stt][claude-stt] | Moonshine ONNX | Plugin: hotkey → local STT → keyboard injection (xdotool/accessibility API) | **Archived** — superseded by native `/voice` |
| [Traves-Theberge/Wake-Word][wake-word] | Picovoice Porcupine | Electron app: "Hey Claude" wake-word → launch Claude CLI | Active |
| [mbailey/voicemode][tts-voice] | Whisper (local) | MCP server: 2-way voice (STT + Kokoro TTS), webrtcvad silence detection | Active |
| [SergeyKirk/hey-claude][hey-claude] | Picovoice Porcupine | macOS: always-on "Hey Claude" → execute via Claude Code | Active |
| bacharyehya/talk-to-claude (`github.com/bacharyehya/talk-to-claude`, 404 as of 2026-11-02 — repo removed; retained for provenance) | Various | MCP: wake-word activated voice conversations | Removed |

**Key gap**: CC's native `/voice` is cloud-only and push-to-talk. No native continuous listening, no local STT, no wake-word activation. Community projects fill these gaps but require separate installation.

## Notable Plugin Profile: claude-seo (Marketing Growth)

**Repo**: [AgriciDaniel/claude-seo][claude-seo] | **Homepage**: [claude-seo.md][claude-seo-site] | **License**: MIT | **CC version**: 1.0.33+ (plugin install) | **Category**: Marketing Growth

Representative example of the Marketing Growth category. Per the [repo README][claude-seo-readme], the plugin now ships **26 sub-skills and 19 specialist subagents**, with 9 optional extensions (up from 3) adding live SEO data sources, exposed through a single `/seo` command. **Refreshed 2026-11-12** (`gh api`): 28,262★/3,649 forks, last pushed 2026-11-11 — up sharply from the 2026-04-15 snapshot this section originally recorded (23 skill directories, 17 subagents, 3 extensions). The repo's own README now states this 26/19 count directly, so the earlier "GitHub short description undercounts the README" discrepancy no longer applies. Selected subcommands:

| Command | Purpose |
|---------|---------|
| `/seo audit <url>` | Full site audit with parallel subagent delegation |
| `/seo page <url>` | Deep single-page analysis |
| `/seo technical <url>` | Technical SEO audit (9 categories) |
| `/seo content <url>` | E-E-A-T and content-quality analysis (Sept 2025 Quality Rater Guidelines) |
| `/seo schema <url>` | Detect, validate, and generate Schema.org markup |
| `/seo geo <url>` | Generative Engine Optimization — AI Overviews, ChatGPT, Perplexity, Copilot |
| `/seo sitemap <url>` / `/seo sitemap generate` | Analyze or generate XML sitemaps with industry templates |
| `/seo hreflang <url>` | Hreflang/i18n audit; validates self-references, return tags, x-default, ISO-639-1 + ISO-3166-1 codes |
| `/seo local <url>` / `/seo maps [cmd]` | Local SEO (GBP, citations, reviews, map pack) and maps intelligence (geo-grid) |
| `/seo google [cmd] [url]` / `/seo google report [type]` | Google Search Console, PageSpeed, CrUX, Indexing, GA4 APIs + PDF/HTML report generation |
| `/seo cluster <seed>` | SERP-based semantic clustering and content architecture |
| `/seo sxo <url>` | Search Experience Optimization — page-type, user stories, personas |
| `/seo drift baseline\|compare\|history <url>` | SEO baseline capture and drift monitoring over time |
| `/seo ecommerce <url>` | Product schema, marketplace intelligence |
| `/seo backlinks <url>` | Backlink profile analysis via free sources (Moz, Bing, Common Crawl) |
| `/seo competitor-pages <url>` | "X vs Y" / "alternatives to X" page generation with Product schema |
| `/seo programmatic <url>` | Programmatic-SEO analysis with quality gates (warn at 100+, hard stop at 500+ pages) |
| `/seo firecrawl`, `/seo dataforseo`, `/seo image-gen` | Optional paid extensions |

**Install** (requires Claude Code 1.0.33+):

```bash
/plugin marketplace add AgriciDaniel/claude-seo
/plugin install claude-seo@AgriciDaniel-claude-seo
```

Manual install via `git clone` + `install.sh` (Unix) or `install.ps1` (Windows) is also documented. The repo explicitly rejects the `irm … | iex` Windows pattern on supply-chain-risk grounds and recommends review-before-run.

**Notable patterns**:

- `/seo audit` fans out to **up to 15 specialists (8 always + 7 conditional)** per the [`seo-audit` SKILL.md][seo-audit-skill] — one of the more aggressive parallel-subagent fan-outs observed in a public plugin. Conditional subagents spawn on signal detection (e.g., `seo-local` when a brick-and-mortar business is detected, `seo-google` when Google API credentials are present). Relevant to the patterns catalogued in [CC-agent-teams-orchestration](../cc-native/agents-skills/CC-agent-teams-orchestration.md).
- `/seo geo` is an early plugin explicitly targeting **GEO/AEO** (AI-answer citability across AI Overviews, ChatGPT, Perplexity, Copilot) rather than classical search ranking.
- `/seo drift` implements change-monitoring via stored baselines — a pattern worth watching for other domain plugins (security, compliance, docs drift).
- Programmatic SEO quality gates (hard stop at 500+ pages without audit) are a rare example of a plugin enforcing scale-safety guardrails in prompt-driven workflows.

## Notable Plugin Profile: ponytail (Code Quality — Cross-Agent)

**Repo**: [DietrichGebert/ponytail][ponytail] | **License**: MIT | **Stars**: ~16.6k | **Language**: JavaScript (~91%)

A cross-agent ruleset/plugin that enforces YAGNI-first minimalism across all major AI coding platforms. Tagline: *"Makes your AI agent think like the laziest senior dev in the room. The best code is the code you never wrote."*

### Decision Hierarchy

The plugin installs a structured decision ladder agents must traverse before writing any new code:

1. Does this code need to exist at all?
2. Standard library?
3. Native platform features?
4. Existing dependencies?
5. Custom implementation (last resort)

### Platform Support

Ponytail is notable for being one of the few plugins explicitly targeting all major AI coding agents from a single repo:

| Platform | Integration method |
|----------|--------------------|
| Claude Code | `/plugin marketplace add DietrichGebert/ponytail` |
| GitHub Copilot CLI | `.github/copilot-instructions.md` ruleset copy |
| Cursor | `.cursor/rules/` ruleset copy |
| Windsurf | `.windsurf/rules/` ruleset copy |
| Codex | Plugin install command |
| Cline / Kiro / Aider | Platform-specific rule files |

The repo ships Node.js lifecycle hooks (`hooks/`), platform-specific markdown rule files, and an optional `~/.config/ponytail/config.json` for default-mode configuration.

**Install (Claude Code)**:

```bash
/plugin marketplace add DietrichGebert/ponytail
```

**Notable pattern**: Unusually high star count (~16.6k) for a code-quality plugin reflects broad cross-ecosystem appeal — the minimalism philosophy is platform-agnostic and the multi-platform distribution lowers the barrier for polyglot teams.

## Notable Plugin Profile: squid (Agentic Engineering Pipeline)

**Repo**: [iusztinpaul/squid][squid] | **Writeup**: [decodingai][squid-writeup] | **License**: Apache-2.0 | **Stars**: ~114 | **Category**: Workflow Orchestration

An opinionated full-lifecycle engineering pipeline that mirrors a real team across five role subagents — `product-architect` → `software-engineer` → `tester` → `pr-reviewer` → `oncall-engineer` — plus an optional self-improve meta-agent. Core principle: *no agent both writes code and decides if it's correct*. Human gates sit at plan approval and final merge. Architectural memory is externalised to ADR files (`docs/adr/<NNNN_title>.md`) and a DDD `docs/glossary.md`; `/scaffold` generates `AGENTS.md` + folder skeletons for Python/TypeScript/Go.

| Command | Purpose |
|---------|---------|
| `/scaffold` | Bootstrap stack + `AGENTS.md` + folder skeleton |
| `/plan <spec>` | Groom a spec into a Tasks Plan; create branch + worktree |
| `/implement-night <plan>` | Full 5-agent pipeline (async, ≤5 retry loops, 2 human gates) |
| `/implement-task` | Single task — SWE ↔ Tester loop only |
| `/review`, `/review-ci` | Acceptance/diff review + On-Call CI validation |

**Install** (Claude Code plugin):

```bash
/plugin marketplace add iusztinpaul/squid
/plugin install squid@iusztinpaul
# or via the skills runner:
npx skills add iusztinpaul/squid
```

**Env vars**: none documented — configuration is per-project via `AGENTS.md` + `.claude/settings.json`.

**Notable pattern**: the ADR layer (architectural memory) and the Tasks Plan (feature → task decomposition) make squid a worked example of memory + goal-tracking *inside* a CC pipeline — threads picked up in the deferred agentic-memory / goal-attribution research. Relevant to [CC-agent-teams-orchestration](../cc-native/agents-skills/CC-agent-teams-orchestration.md).

## Notable Plugin Profile: Impeccable (pbakaus — Design, Cross-Agent)

**Repo**: [pbakaus/impeccable][impeccable] | **License**: Apache-2.0 | **Stars**: 108,300★/6,438 forks (`gh api`, 2026-11-12) | **Category**: Design review

Impeccable is a "design vocabulary for your coding agent" — 24 slash commands grouped into Steer (`bolder`, `quieter`, `distill`, `colorize`, `typeset`, `layout`, `animate`, `delight`, `overdrive`), Review (`critique`, `audit`), Finish (`polish`, `harden`, `clarify`, `adapt`, `optimize`, `onboard`), and Iterate-live (`live`, `generate`), plus `shape`/`init`/`document`/`extract` for setup. Its own framing: each command "loads a playbook written for that one move and points it at one target," addressing the recurring "AI slop" look (Inter font, purple-to-blue gradients, cards nested in cards) that shows up "across models and projects" when an agent is given no design direction. A **62-rule, no-LLM detector** (`npx impeccable detect`) catches pattern tells plus accessibility/contrast issues on a rendered page, runs in CI with `--github` annotations, and backs a design hook that scans every UI file an agent edits before it calls the work done.

Explicitly cross-agent, not CC-exclusive: works with Claude Code, Cursor, Codex CLI, GitHub Copilot, Devin, Replit Agent, Gemini CLI, Grok Build, OpenCode, Google Antigravity, Kiro, Trae, Rovo Dev, Qoder, Mistral Vibe, Pi, Hermes Agent, DeepSeek Harness and Veto, each with its own skills-folder path documented in the README; a Chrome extension overlays the same findings on any live page. **Claude Code install**: `/plugin marketplace add pbakaus/impeccable`, then `/plugin install impeccable@pbakaus-impeccable` (or `npx impeccable install`, which detects installed tools and offers the hook).

**Caveat**: "Live mode" apply can fall back to running the `codex` or `claude` CLI with `--dangerously-bypass-approvals-and-sandbox` / `--permission-mode bypassPermissions` and the user's inherited environment when no live session is polling — the README itself flags this as a step worth reviewing before using live mode in an unfamiliar repo.

## Notable Plugin Profile: Elephant-Goldfish Model (Google — Design/Spec Review, Cross-Agent)

**Repo**: [google/elephant-goldfish-model][egm] | **License**: Apache-2.0 | **Stars**: 17,685★/1,322 forks (`gh api`, 2026-11-12) | **Category**: Spec review

EGM pairs two agent roles for spec-driven work: "Elephant," a context-holding drafter that keeps the project's context and drafts a specification, and "Goldfish," a fresh-context reviewer that examines the draft and its referenced source material without the drafting conversation — "Design with an elephant. Review with a goldfish," per the README. A human still makes the architectural trade-offs and approves the specification before implementation. Skills cover brainstorm, draft, resolve, bootstrap, review, review-loop and drift-report; if the host agent cannot spin up a genuinely fresh subagent context for the Goldfish step, EGM stops the review rather than fake it.

Not CC-exclusive — Claude Code is one of four installable surfaces: `claude plugin marketplace add google/elephant-goldfish-model` then `claude plugin install egm@egm`, alongside Codex CLI, Antigravity CLI, and a separate ChatGPT/Codex-desktop plugin listing. The README states plainly that EGM is "not an officially supported Google product." Conceptually the same shape as the fresh-context-reviewer pattern this corpus has already noted elsewhere (independent verification by an agent with no memory of the authoring conversation), here applied to specs rather than diffs.

## Notable Plugin Profile: codex-plugin-cc (OpenAI Codex → CC delegation)

[openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) — an **official OpenAI** plugin (Apache-2.0, ~26.9k★, v1.0.6) that runs Codex from inside a CC session for review or task delegation. Notable for building entirely on CC's own extension surface: slash commands (`/codex:review`, `/codex:adversarial-review`, `/codex:rescue`, `/codex:transfer`, …), a `codex-rescue` subagent, and a **`Stop`-hook review gate** that can block Claude's response when Codex flags issues; plus background delegation and full session transfer. A rival lab productizing cross-agent delegation on CC primitives. Full analysis: [CC-codex-plugin-cc-analysis.md](CC-codex-plugin-cc-analysis.md).

## Community Mod Catalogs

Mods — plugins whose JavaScript/TypeScript handlers run inside Claude Code and can draw UI (first-party
coverage: [CC-mods-function-hooks-analysis.md](../cc-native/plugins-ecosystem/CC-mods-function-hooks-analysis.md))
— gained community catalogs within weeks of becoming default-on in v2.1.287. Checked 2026-10-22; none of
these is Anthropic's.

| Catalog | What it is | Licence / size | Notes |
|---|---|---|---|
| [claude-mods.com][mods-dir] | Mod directory; labels itself "Unofficial directory" | No licence stated; "278 mods listed" | Operator not named on the page |
| [OneWave-AI/claude-code-mods][onewave] | 11 mods (README: "Eleven mods"; repo description says ten): burn-meter, launch-codes, session-wrapped, boss-fight, code-pet, inner-monologue, sportscaster, agent-narrator, swarm, agent-race, inbox-alerts | MIT; 23★, created 2026-10-02 | Self-described "Anthropic Partner Network firm" (unverified). `inbox-alerts` "Polls Gmail, Slack, and Google Calendar every two minutes through the claude.ai connectors" |
| [whyashthakker/awesome-claude-code-mods][awesome-mods] | 50-mod collection, introduced by its author's [explainx.ai post][explainx-mods] (Yash Thakker, 2026-10-03) | MIT; 88★, created 2026-10-03 | Claims "50 of 50 pass strict validation" (unverified) |
| [ruvnet field guide (gist)][ruvnet-mods] | "Claude Code Mods: a field guide" — how-to, no mod code | No licence stated | Partly outdated: tells readers to `export CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`, which "Claude Code v2.1.287 and later ignores" per the [first-party docs][mods-overview-cc]. Its own advice: "Grep them before you trust any guide, this one included." |

**Install-path caution.** OneWave, the explainx post and the ruvnet gist all suggest adding
`CLAUDE_CODE_PLUGIN_DIRS` to the `env` block of `~/.claude/settings.json`, which loads those mod
directories into *every* session (the explainx post itself says it "could not verify end to end in the
app"). Since "Mods aren't sandboxed" ([first-party docs][mods-overview-cc]), our advice is to prefer the per-session
`--plugin-dir` or a marketplace install, and run `claude plugin validate` on a mod before trusting it.

## Notable Plugin Profile: lot-map (Live Session Map Mod)

**Repo**: [alexeyw/lot-map][lot-map] | **License**: MIT (LICENSE file, "Copyright (c) 2026 Aleksei
Volodin") | **Stars**: 407★/45 forks (`gh api`, 2026-11-12) | **Category**: Agent observability /
visualization

lot-map is a concrete example of a [mod](../cc-native/plugins-ecosystem/CC-mods-function-hooks-analysis.md)
(`hooks/hooks.json` → `{"modules": ["./register.tsx"]}`, the mod file layout documented above) rather
than an external app: it draws a live node-map in a pane beside the chat, with tool calls, model
steps, hooks, skills and subagents each sending a pulse from a centre node (default label "CLAUDE")
out to one of ten "stations" — You, Model, Memory, Files, Shell, Network, Browser, Agents, Skills,
Hooks — as they happen; a spoke thickens the more its station is used, and a fading route line traces
the last few hops. Its own README: "Built and tested on Claude Code 2.1.321 on macOS; users report it
working on Windows as well" (mods require CC v2.1.287+, per the native-feature doc above). The README's
own demo GIF is explicitly "a made-up session replayed through the mod's own drawing code," not a
captured real run.

**Basics** (first-party, `gh api`, 2026-11-12): repo created 2026-11-09, last pushed 2026-11-12 — a
3-day-old repo already at 407★/45 forks; `plugin.json` reports version 0.5.1; no GitHub Releases or
tags exist, so version history lives only in `CHANGELOG.md` and `plugin.json`, not GitHub Releases.
`plugin.json`'s `userConfig.language` options list six languages (`en`, `ru`, `es`, `fr`, `de`, `it`);
the GitHub repo short description says "in five languages" — a stale count against the live
`plugin.json`.

**Install**: `/plugin install lot-map --marketplace alexeyw/lot-map`. The pane opens by itself when a
session starts; in a terminal it needs at least 144 columns and draws text only, otherwise `/lot-map`
opens it.

**How it integrates with CC**: it hooks the session's start, prompts, turns, model steps, tool calls,
skills and compaction, plus three settings-hook events — `PreToolUse` (reads whether a settings hook
refused, asked permission, or took a moment on a call), and `UserPromptSubmit`/`SessionStart` (reads
context a settings hook added). Per its README, verbatim: "Each of its hooks passes the event on as it
came and returns what came back as it was: it changes no input, no result, no context and no
permission decision, and makes none of its own." This is a read-only observation layer built on the
native Mods mechanism above — a contrast with [Agent Flow](CC-agent-flow-visualizer-analysis.md),
which captures the same kind of session activity from *outside* the process, via an HTTP hook server
and Codex rollout-file tailing. It also asks Claude Code for context-window usage after each model
step (`$.session.usage()`) and persists one thing between sessions — the name of the model last used
per project folder (`$.store`), so it can flag a model change — confirmed by a read of
`hooks/register.tsx` on 2026-11-12.

**Privacy claim**: its README states, verbatim, that the mod "makes no network requests, reads no
files, runs no processes, calls no model and adds nothing to the conversation"; `PRIVACY.md` makes
the same claims across separate bullets, in different wording. This is self-reported; a read of
`hooks/register.tsx` and `hooks/map.ts` (2026-11-12) found no calls
to network, filesystem, process-spawn or model namespaces — consistent with the claim, but a source
read is not an independent audit. The same README also states the counterweight any mod carries by
design: it "is handed every call's whole input, including command lines and the text written to
files," and takes only short labels from that (a file's last two path segments, a URL's host, a shell
command's name, never a full command line or file contents) — per the native Mods docs above, "a mod
can read and write your files, start processes, and make network requests" with the installing user's
own access, so this scoping is enforced by the mod's own code, not by a sandbox.

**Caution**: very young (created 2026-11-09) with a fast-moving CHANGELOG — 0.3.6 through 0.5.1 all
land on 2026-11-11, including one feature (a Hooks-station row) removed in 0.4.0 for an unnamed plugin
catalogue's verification rule, then restored in 0.5.0 — so no settled track record yet. The README
itself flags the update-trust model: a marketplace added from this repo follows its `main` branch, "so
an update brings whatever is there: read the diff before updating if that matters to you."

## Ecosystem Observations

1. **Business-function plugins** (Sales, Marketing, Legal) exist only in the ccplugins registry — the awesome-claude-code list is developer-focused
2. **Ralph Wiggum Pattern** appears in both catalogs, confirming community convergence on autonomous loop workflows
3. **5 official plugins** are tracked by ccplugins, establishing a baseline for the official-to-community plugin ratio (~1:27)
4. **Git workflow** is disproportionately represented (14 plugins in ccplugins + numerous entries in awesome-cc), suggesting this is the primary CC extension use case

## Cross-References

- [CC-official-plugins-landscape.md](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) — official Anthropic plugins (the 5 tracked by ccplugins)
- [CC-plugin-packaging-research.md](../cc-native/plugins-ecosystem/CC-plugin-packaging-research.md) — plugin packaging format and distribution
- [CC-community-skills-landscape.md](CC-community-skills-landscape.md) — skill libraries (gstack, pm-skills)
- [CC-cowork-plugins-enterprise-analysis.md](../cc-native/plugins-ecosystem/CC-cowork-plugins-enterprise-analysis.md) — Cowork/enterprise plugin distribution

## Sources

| Source | Content |
|---|---|
| [awesome-claude-code][acc] | Curated resource list |
| [awesome-claude-code-plugins][accp] | Installable plugin registry with marketplace format |
| [squid][squid] | Agentic engineering pipeline plugin (5-agent; ADR memory + Tasks Plan task decomposition) |
| [squid writeup][squid-writeup] | Author's setup rationale (decodingai) |
| [pbakaus/impeccable][impeccable] (README + `gh api`, 2026-11-12) | Design-vocabulary plugin: commands, 62-rule detector, cross-agent install table |
| [google/elephant-goldfish-model][egm] (README + `gh api`, 2026-11-12) | Elephant/Goldfish drafter-reviewer spec-review plugin |
| [claude-mods.com][mods-dir] · [OneWave-AI/claude-code-mods][onewave] · [awesome-claude-code-mods][awesome-mods] · [explainx.ai post][explainx-mods] · [ruvnet gist][ruvnet-mods] | Community mod catalogs and guides (checked 2026-10-22) |
| [Mods overview][mods-overview-cc] | First-party: "Mods aren't sandboxed"; `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` ignored from v2.1.287 |
| [alexeyw/lot-map][lot-map] (README, LICENSE, PRIVACY.md, CHANGELOG.md, `plugin.json`, `hooks/register.tsx`, `hooks/map.ts` + `gh api`, 2026-11-12) | Live session-map mod: repo stats, license, install, hooked events, privacy claims, source read for network/fs/process calls |

[ponytail]: https://github.com/DietrichGebert/ponytail
[mods-dir]: https://claude-mods.com/
[onewave]: https://github.com/OneWave-AI/claude-code-mods
[awesome-mods]: https://github.com/whyashthakker/awesome-claude-code-mods
[explainx-mods]: https://www.explainx.ai/blog/awesome-claude-code-mods-50-open-source-mods-install-guide-2026
[ruvnet-mods]: https://gist.github.com/ruvnet/a485e930b148185197fc53fd38b429ea
[mods-overview-cc]: https://code.claude.com/docs/en/plugins/mods/overview
[squid]: https://github.com/iusztinpaul/squid
[squid-writeup]: https://www.decodingai.com/p/squid-my-agentic-coding-setup-may-2026
[impeccable]: https://github.com/pbakaus/impeccable
[egm]: https://github.com/google/elephant-goldfish-model
[acc]: https://github.com/hesreallyhim/awesome-claude-code
[accp]: https://github.com/ccplugins/awesome-claude-code-plugins
[claude-seo]: https://github.com/AgriciDaniel/claude-seo
[claude-seo-site]: https://claude-seo.md
[claude-seo-readme]: https://github.com/AgriciDaniel/claude-seo/blob/main/README.md
[seo-audit-skill]: https://github.com/AgriciDaniel/claude-seo/blob/main/skills/seo-audit/SKILL.md
[tts-ybou]: https://github.com/ybouhjira/claude-code-tts
[tts-cg]: https://git.sr.ht/~cg/claude-code-tts
[tts-ktal]: https://github.com/ktaletsk/claude-code-tts
[tts-laura]: https://github.com/TwinPeaksTownie/Claude-to-Speech
[tts-voice]: https://github.com/mbailey/voicemode
[tts-mcp]: https://github.com/johnmatthewtennant/mcp-voice-hooks
[tts-hooks]: https://github.com/husniadil/cc-hooks
[tts-shanr]: https://github.com/shanraisshan/claude-code-hooks
[realtimetts]: https://github.com/KoljaB/RealtimeTTS
[voice-docs]: https://code.claude.com/docs/en/voice-dictation
[moonshine]: https://github.com/moonshine-ai/moonshine
[whispercpp]: https://github.com/ggml-org/whisper.cpp
[vosk]: https://alphacephei.com/vosk/
[lot-map]: https://github.com/alexeyw/lot-map
[claude-stt]: https://github.com/jarrodwatts/claude-stt
[wake-word]: https://github.com/Traves-Theberge/Wake-Word
[hey-claude]: https://github.com/SergeyKirk/hey-claude
