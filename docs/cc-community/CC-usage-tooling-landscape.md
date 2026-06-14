---
title: CC Usage-Observability Tooling Landscape
purpose: Token-usage and cost observability tools for Claude Code (and sibling agents) — CodeBurn, ccusage, Claude-Code-Usage-Monitor.
category: landscape
status: research
created: 2026-06-14
updated: 2026-06-14
validated_links: 2026-06-14
---

**Status**: Research (informational)

Tools that measure token usage and cost across coding-agent sessions. Split out of [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) (which keeps the cross-tool comparison table). They divide into **retrospective** measurement (CodeBurn cross-agent; ccusage CC/Codex-deep) and **predictive** monitoring (Claude-Code-Usage-Monitor). Where RTK reduces tokens *entering* context, these observe what was actually spent — optimization needs measurement.

## CodeBurn (AgentSeal)

**Repo**: [getagentseal/codeburn][codeburn] | **Stars**: 4K | **License**: MIT | **Latest**: Menubar v0.9.0 (2026-04-25) | **Stack**: TypeScript, Node.js 20+

Local-first TUI dashboard that tracks AI coding token usage and cost across multiple coding agents. Reads session data directly from disk — no API keys, no proxy ([README][codeburn]).

### Supported Agents

Per the [README][codeburn]: Claude Code, Claude Desktop, Codex, Cursor, cursor-agent, OpenCode, Pi, OMP (Oh My Pi), GitHub Copilot.

### Data Sources (Read-Only, On-Disk)

| Agent | Path |
|---|---|
| Claude | `~/.claude/projects/` (JSONL) |
| Cursor | `~/Library/Application Support/Cursor/` (SQLite, macOS) |
| Codex | `~/.codex/sessions/` (JSONL with timestamped token events) |
| OpenCode | `~/.local/share/opencode/` (SQLite) |
| GitHub Copilot | `~/.copilot/session-state/` |

### Features

- **TUI dashboard** with gradient charts and responsive panels
- **13 task categories** classified from tool patterns: Coding, Debugging, Feature Dev, Refactoring, Testing, Exploration, Planning, Delegation, Git Ops, Build/Deploy, Brainstorming, Conversation, General
- **[`codeburn optimize`](https://github.com/getagentseal/codeburn#optimize)** — surfaces nine waste patterns (files re-read across sessions, low Read:Edit ratio, unused MCP servers, ghost agents/skills/slash commands, bloated `CLAUDE.md`, wasted bash output, cache-creation overhead, context-heavy and low-worth sessions) with copy-paste token/$ fixes ranked into an A–F health grade
- **`codeburn compare`** — side-by-side model performance metrics
- **`codeburn report -p 30days`** — rolling-window analysis
- **`codeburn export`** — CSV/JSON across multiple time periods
- **Subscription tracking** — Claude Pro/Max, Cursor Pro
- **Currency conversion** — 162 ISO 4217 codes
- **Pricing data** sourced from LiteLLM with 24h cached refresh; hardcoded fallbacks for Claude and GPT-5 to prevent fuzzy-match errors

### Platform Support

macOS (native menubar app via `codeburn menubar`), Linux (CLI), Windows (CLI; Cursor support requires `better-sqlite3`).

### Installation

```bash
npm install -g codeburn
# or run without installing:
npx codeburn
```

### Key Differentiator

Where RTK reduces tokens *entering* context and caveman compresses tokens *leaving* the assistant, **CodeBurn observes** what was actually spent — across agents, models, and projects. Complementary to both: optimization needs measurement. Local-first (no API keys, no telemetry) makes it usable in air-gapped or compliance-sensitive environments.

Cross-ref: [CC-community-skills-landscape.md](CC-community-skills-landscape.md) — caveman (output compression skill); [CC-session-cost-analysis.md](../cc-native/sessions/CC-session-cost-analysis.md) — CC's native session-cost extraction via JSONL/jq

---

## ccusage (ryoppippi)

**Repo**: [ryoppippi/ccusage][ccusage] | **Stars**: 13.4K | **License**: MIT | **Version**: v18.0.11 (2026-04-19) | **Stack**: TypeScript

CLI tool that analyzes Claude Code / Codex CLI usage from local JSONL files. Established reference tool in the CC usage-tracking space — predates and is broader-adopted than CodeBurn ([README][ccusage]).

### Reports

- **Daily** — token usage and costs aggregated by date
- **Monthly** — long-horizon aggregation
- **Session** — usage grouped by conversation
- **Blocks** — 5-hour billing windows (matches Anthropic's plan limits)
- **Statusline** (Beta) — integration for hooks

### Capabilities

Per the [README][ccusage]:

- **Model tracking** — per-model breakdown with `--breakdown`
- **Cache token support** — tracks cache creation and cache read tokens separately (codeburn does not split these)
- **Offline mode** — `--offline` uses pre-cached pricing (no network)
- **MCP integration** — built-in MCP server for in-session queries
- **Multi-instance** — group usage by project
- **JSON export**

### Installation

```bash
npx ccusage@latest          # recommended — always latest
bunx ccusage
pnpm dlx ccusage
```

Reads `~/.claude/projects/` JSONL by default; data path is configurable.

### Key Differentiator

Where CodeBurn is **multi-agent** (Claude/Codex/Cursor/OpenCode/Copilot in one TUI), ccusage is **CC/Codex-focused** with deeper CC-specific features (cache token split, MCP server, statusline hook). The two are complementary, not redundant: ccusage for CC-deep analysis and in-session queries via MCP; CodeBurn for cross-agent comparison.

Cross-ref: [CC-session-cost-analysis.md](../cc-native/sessions/CC-session-cost-analysis.md) — manual JSONL/jq extraction patterns ccusage automates; [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md) — statusline hook integration point

---

## Claude-Code-Usage-Monitor (Maciek-roboblog)

**Repo**: [Maciek-roboblog/Claude-Code-Usage-Monitor][claude-monitor] | **Stars**: 7.8K | **License**: MIT | **Version**: v3.1.0 | **Stack**: Python 3.9+

Real-time terminal monitor for Claude Code with **predictions and warnings**, distinguishing it from after-the-fact analyzers like ccusage / CodeBurn ([README][claude-monitor]).

### Plan Support

Per the [README][claude-monitor]:

| Plan | Token limit |
|---|---|
| Pro | ~19,000 |
| Max5 | ~88,000 |
| Max20 | ~220,000 |
| **Custom** | P90 auto-detection over recent session blocks |

The Custom plan analyzes recent session blocks and computes a personalized 90th-percentile limit — adapts to actual usage patterns without manual configuration.

### Views

- **Realtime** — live progress bars + burn rate (default)
- **Daily** — aggregated table
- **Monthly** — long-trend analysis

### Methodology

P90 percentile analysis across all available session blocks; multi-session burn-rate analytics; intelligent session-limit detection. Stack: `pytz`, `rich`, `pydantic`, `numpy`, `pyyaml`, `sentry-sdk`.

### Installation

```bash
uv tool install claude-monitor       # recommended
pip install claude-monitor
```

### Key Differentiator

Only tool in this category that does **prediction** (not just retrospective measurement). ccusage and CodeBurn answer "what did I spend?"; claude-monitor answers "will I exhaust my window?" Useful pairing: claude-monitor for live discipline, ccusage for historical trend, CodeBurn for cross-agent comparison.

Cross-ref: [CC-session-cost-analysis.md](../cc-native/sessions/CC-session-cost-analysis.md) — Anthropic plan limits and 5-hour windows

## Cross-References

- [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) — full cross-tool comparison + the rest of the CC tooling landscape
- [CC-session-cost-analysis.md](../cc-native/sessions/CC-session-cost-analysis.md) — CC's native session-cost extraction

[codeburn]: https://github.com/getagentseal/codeburn
[ccusage]: https://github.com/ryoppippi/ccusage
[claude-monitor]: https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor
