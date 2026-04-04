---
title: CC Reverse Engineering Landscape
purpose: Survey of community tools, blogs, and trackers that reverse engineer Claude Code internals — system prompts, binary analysis, env vars, API interception.
created: 2026-03-29
updated: 2026-03-29
validated_links: 2026-03-29
---

**Status**: Research (informational)

## What It Is

Claude Code is closed-source (CLI binary + VS Code extension ship as minified JS bundles). A growing community ecosystem reverse engineers its internals via API interception, binary string extraction, prompt capture, and traffic analysis. This doc surveys the landscape as of 2026-03-29.

Cross-ref: [CC-binary-architecture.md][binary-arch] — our own binary analysis findings

## System Prompt Extraction

### Piebald-AI/claude-code-system-prompts

The most comprehensive resource. Extracts prompts from CC's compiled source via a script run against the npm package. Tracks changes across **136 CC versions** since v2.0.14.

- ~60 core system prompt fragments (conditionally assembled)
- ~40 system reminders (context notifications)
- ~30 agent/sub-agent prompts (Plan, Explore, Task, slash commands)
- ~25 data prompts (SDK references, API docs across 8 languages)
- 18+ built-in tool descriptions

URL: [piebald-prompts][piebald-prompts]

### Agiflow — Prompt Augmentation Architecture

Documents five injection mechanisms across three layers:

| Layer | Mechanism | How |
|---|---|---|
| System | Output Styles | Mutates system prompt array |
| Message | CLAUDE.md | Injected as `<system-reminder>` in user messages |
| Message | Slash Commands | String substitution with `<command-message>` markers |
| Message | Skills | Two-step tool_use/tool_result injection |
| Conversation | Sub-agents | Isolated conversations via Agent tool with separate system prompts |

URL: [agiflow][agiflow]

### BeyondTheHype — Inside Claude Code

System prompt analysis documenting growth from 1,800 to 2,500+ words. Methodology: HTTPS interception via custom API base URL + ProxyMan + WebCrack for JS deobfuscation.

URL: [beyondthehype][beyondthehype]

### sabrina.dev — Sub-Agent RE

Documented TODO tool system prompt, task state management (pending/in_progress/completed), WebFetch configuration, and reference to "ULTRACLAUDE.md" experimental mode.

URL: [sabrina][sabrina]

## Binary & Architecture Analysis

### frr.dev — Native Build Analysis

Documents that the CLI binary is a **~213MB single-executable Bun application** with JavaScriptCore runtime. The Bun runtime extracts and executes embedded JS at launch.

URL: [frr-build][frr-build]

### Yuyz0112/claude-code-reverse

Tool that monkey-patches `cli.js` to intercept `beta.messages.create` calls. Provides `parser.js` and `visualize.html` for log analysis.

Discovered: quota verification via Haiku 3.5, topic detection prompts, context compression, IDE integration reading open file paths, todo-based memory in `~/.claude/todos/`, sub-agent architecture.

URL: [yuyz-repo][yuyz-repo] | Docs: [yuyz-docs][yuyz-docs]

### Kir Shatrov — API Interception via mitmproxy

Used `ANTHROPIC_BASE_URL=http://localhost:8000/` to intercept traffic. Found 11 tools, documented that CC uses Sonnet for reasoning and Haiku for lightweight tasks. Every user input undergoes topic classification. Bash commands trigger two separate LLM security assessment calls.

URL: [shatrov][shatrov]

### ZhangHanDong — `/btw` Command Deep Dive

Deep Mach-O arm64 binary analysis. Documented `/btw` (side-question) internals including regex triggers, tool schema transmission, `skipCacheWrite: true`, and the `VF1()` message filter (line 380492 in cli.js) that strips orphaned tool_use blocks. Confirmed API interception via `NODE_OPTIONS` hooks.

URL: [btw-gist][btw-gist]

### ghuntley.com/tradecraft

Claims Claude Code can decompile its own bundled JS. Content partially paywalled. A separate community repo that restored source via source maps was **taken down by Anthropic via DMCA**. Referenced on Hacker News ([hn-thread][hn-thread]).

URL: [ghuntley][ghuntley]

## Version Tracking & Feature Gates

### TurboAI.dev — Version Tracker

Tracks every CC release with structured diffs. As of v2.1.86 (2026-03-27):

| Metric | Count |
|---|---|
| Environment variables | 204 |
| Feature gates | 41 |
| Models | 16 |
| Slash commands | 22 |
| Dynamic configs | 29 |

Notable undocumented vars tracked: `CLAUDE_TRUSTED_DEVICE_TOKEN` (enterprise SSO), `CLAUDE_PLUGIN_DATA` (plugin state), `CLAUDE_STREAM_IDLE_TIMEOUT_MS` (session watchdog).

URL: [turboai][turboai]

### unkn0wncode — Environment Variables Gist

Comprehensive categorized list of ~200+ env vars (v2.1.81) including model selection, feature flags, OAuth, MCP, remote/collab, and advanced internals.

URL: [unkn0wncode][unkn0wncode]

## Settings Schema

### JSON Schema Store

Full `claude-code-settings.json` schema published at SchemaStore but **not linked from official CC docs** (tracked in [gh-11795][gh-11795]).

URL: [schema-store][schema-store]

### xdannyrobertsx — Settings Schema Gist

Community documentation of the settings schema with annotations.

URL: [xdanny-gist][xdanny-gist]

## Web Tools Internals

### Liran Yoffe — WebFetch & WebSearch Cost Analysis

Reverse engineered both web tools via API interception:

| Tool | Implementation | Cost Estimate |
|---|---|---|
| **WebFetch** | Local fetch via Axios → Haiku secondary conversation. 15-min cache. No JS rendering | ~$33/1000 requests |
| **WebSearch** | Server-side `web_search_20250305` tool → Opus secondary conversation with 31,999-token thinking budget. Up to 8 searches/request. Likely Brave Search backend | ~$145/1000 requests |

URL: [yoffe][yoffe]

## Community Resources

### ClaudeLog

Community resource by InventorBlack (Claude Developer Ambassador). Configuration guides, experiments, and mechanics documentation. Not affiliated with Anthropic.

URL: [claudelog][claudelog]

## Our Findings (qte77, 2026-03-29)

Documented in this repo:

- **Three-layer config system**: `.claude.json` vs `settings.json` vs `claudeCode.*` — [CC-tools-inventory.md][tools-inv]
- **150+ undocumented env vars** from binary string extraction — [CC-env-vars-reference.md][env-ref]
- **Internal API endpoints**, model IDs, slash commands — [CC-binary-architecture.md][binary-arch]
- **`/settings` routes to `update-config` skill** (not an alias for `/config`) — [CC-tools-inventory.md][tools-inv]

Tracking issue: [qte77/ai-agents-research#70][tracking-issue]

## Sources


[piebald-prompts]: https://github.com/Piebald-AI/claude-code-system-prompts
[agiflow]: https://agiflow.io/blog/claude-code-internals-reverse-engineering-prompt-augmentation/
[beyondthehype]: https://beyondthehype.dev/p/inside-claude-code-prompt-engineering-masterpiece
[sabrina]: https://www.sabrina.dev/p/reverse-engineering-claude-code-using
[frr-build]: https://www.frr.dev/posts/claude-code-native-build-bun/
[yuyz-repo]: https://github.com/Yuyz0112/claude-code-reverse
[yuyz-docs]: https://yuyz0112.github.io/claude-code-reverse/
[shatrov]: https://kirshatrov.com/posts/claude-code-internals
[btw-gist]: https://gist.github.com/ZhangHanDong
[ghuntley]: https://ghuntley.com/tradecraft/
[hn-thread]: https://news.ycombinator.com/item?id=43217357
[turboai]: https://www.turboai.dev/blog/claude-code-versions
[unkn0wncode]: https://gist.github.com/unkn0wncode/f87295d055dd0f0e8082358a0b5cc467
[schema-store]: https://json.schemastore.org/claude-code-settings.json
[gh-11795]: https://github.com/anthropics/claude-code/issues/11795
[xdanny-gist]: https://gist.github.com/xdannyrobertsx/0a395c59b1ef09508e52522289bd5bf6
[yoffe]: https://medium.com/@liranyoffe/reverse-engineering-claude-code-web-tools-1409249316c3
[claudelog]: https://claudelog.com/
[binary-arch]: ../cc-native/configuration/CC-binary-architecture.md
[tools-inv]: ../cc-native/configuration/CC-tools-inventory.md
[env-ref]: ../cc-native/configuration/CC-env-vars-reference.md
[tracking-issue]: https://github.com/qte77/ai-agents-research/issues/70

