---
title: CC Usage-Observability Tooling Landscape
purpose: Token-usage and cost observability tools for Claude Code (and sibling agents) — CodeBurn, ccusage, Claude-Code-Usage-Monitor.
category: landscape
status: research
created: 2026-06-14
updated: 2026-06-22
validated_links: 2026-06-22
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
- **[`codeburn optimize`](https://github.com/getagentseal/codeburn#optimize)** — scans recent sessions for token-waste patterns, grades the setup A–F, and emits copy-paste token/$ fixes ranked by impact (full detector list in [Optimization Rules](#optimization-rules) below)
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

### Optimization Rules

`codeburn optimize` scans recent sessions (default ~30 days), ranks each finding by token/dollar impact, grades the setup A–F, and emits copy-paste fixes. The [README][codeburn] presents these as ~7 categories and `docs/architecture.md` lists 14, but the source of truth — [`src/optimize.ts`][codeburn-optimize] — runs **16 waste detectors**:

| # | Detector | Flags | Fix |
|---|----------|-------|-----|
| 1 | `detectCacheBloat` | Cache-creation tokens above the p25 baseline +40% (bloated MCP/skill warm-up) | Trim per-session loaded context |
| 2 | `detectLowReadEditRatio` | Read:edit ratio under 4:1 (high severity <2:1) → retries | "Read before edit; grep callers first" |
| 3 | `detectJunkReads` | Reads into generated/dependency dirs (`node_modules`, `.git`, `dist`, `.venv`…), ~600 tokens each | Exclude paths |
| 4 | `detectDuplicateReads` | Same file re-read within a session (high severity >30) | Cite `file:lines`, hold context |
| 5 | `detectUnusedMcp` | MCP servers configured but never invoked (24h grace for new configs) | Disable unused servers |
| 6 | `detectMcpToolCoverage` | MCP servers with >10 tools where <20% are ever called | Prune tools / split the server |
| 7 | `detectMcpProfileAdvisor` | Server invoked ≥80% in a few projects but loaded globally | Project-scope the server |
| 8 | `detectCapabilityReliability` | MCP/skill correlated with high retry/edit-cycle rates | Replace the unreliable capability |
| 9 | `detectLowWorthSessions` | Costly sessions with weak delivery (no edits ≥$3, or ≥3 retries) | Revisit the prompting approach |
| 10 | `detectContextBloat` | Effective input ≥75K tokens and input:output ≥25:1 (target 15:1) | Compact / clear stale context |
| 11 | `detectSessionOutliers` | Session costing ≥2× its project peer-session average | Investigate the cost anomaly |
| 12 | `detectBloatedClaudeMd` | `CLAUDE.md` >200 lines after `@`-import expansion (high >400) | Trim, hoist to skills |
| 13 | `detectBashBloat` | `BASH_MAX_OUTPUT_LENGTH` set above 15000 chars | Lower the cap |
| 14 | `detectGhostAgents` | `~/.claude/agents/` entries never invoked (~80 tok/session each) | Archive or delete |
| 15 | `detectGhostSkills` | `~/.claude/skills/` entries never invoked (~80 tok/session each) | Archive or delete |
| 16 | `detectGhostCommands` | `~/.claude/commands/` entries never referenced (~60 tok/session each) | Archive or delete |

Each finding ships estimated token/dollar savings plus copy-paste remediation (`CLAUDE.md` edits, env vars, or archival commands). No standalone docs site yet; the canonical, complete list lives in [`src/optimize.ts`][codeburn-optimize] — the [README][codeburn] grouping undercounts it.

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
[codeburn-optimize]: https://github.com/getagentseal/codeburn/blob/main/src/optimize.ts
[ccusage]: https://github.com/ryoppippi/ccusage
[claude-monitor]: https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor

## Sources

Each tool cites its repo inline via the reference-style link definitions above ([CodeBurn][codeburn], [ccusage][ccusage], [Claude-Code-Usage-Monitor][claude-monitor]).
