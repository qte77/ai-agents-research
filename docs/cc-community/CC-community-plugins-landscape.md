---
title: CC Community Plugins Landscape
description: Survey of community plugin catalogs — awesome-claude-code (curated resource list) and awesome-claude-code-plugins (installable plugin registry with marketplace format).
category: landscape
status: research
created: 2026-03-13
updated: 2026-04-23
validated_links: 2026-04-23
---

**Status**: Research (informational)

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
| [bacharyehya/talk-to-claude][talk-to-claude] | Various | MCP: wake-word activated voice conversations | Active |

**Key gap**: CC's native `/voice` is cloud-only and push-to-talk. No native continuous listening, no local STT, no wake-word activation. Community projects fill these gaps but require separate installation.

## Notable Plugin Profile: claude-seo (Marketing Growth)

**Repo**: [AgriciDaniel/claude-seo][claude-seo] | **Homepage**: [claude-seo.md][claude-seo-site] | **License**: MIT | **CC version**: 1.0.33+ (plugin install) | **Category**: Marketing Growth

Representative example of the Marketing Growth category. Per the [repo README][claude-seo-readme] (commit dated 2026-04-14, repo pushed 2026-04-15), the plugin ships **23 skill directories, 17 subagent definitions, and 3 extensions** (DataForSEO, Firecrawl, Banana) exposed through a single `/seo` command with ~27 subcommands. (GitHub short description still advertises "19 sub-skills, 12 subagents" — the README is authoritative; verified against the `skills/` and `agents/` directory listings via `gh api` on 2026-04-23.) Selected subcommands:

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
[claude-stt]: https://github.com/jarrodwatts/claude-stt
[wake-word]: https://github.com/Traves-Theberge/Wake-Word
[hey-claude]: https://github.com/SergeyKirk/hey-claude
[talk-to-claude]: https://github.com/bacharyehya/talk-to-claude
