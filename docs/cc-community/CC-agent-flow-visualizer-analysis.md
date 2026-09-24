---
title: "Agent Flow: Real-Time Claude Code / Codex Run Visualizer"
source: https://github.com/patoles/agent-flow
purpose: Analysis of Agent Flow — a VS Code extension and standalone web app that replays a Claude Code or Codex agent session as an interactive node graph, for debugging and understanding agent behavior.
category: analysis
platform_scope: [claude-code, codex]
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Trial

## What It Is

[Agent Flow][repo] turns a Claude Code (or Codex) agent session into a live, interactive node
graph — tool calls, branching, subagent coordination, and return flows rendered as they happen,
instead of only the final transcript. Its own framing: *"Claude Code is powerful, but its
execution is a black box — you see the final result, not the journey."* Built by the creator of
CraftMyGame (an AI-agent-driven game creation platform) while debugging that project's own agent
behavior.

Basics (first-party, 2026-09-24): [patoles/agent-flow][repo]; Apache-2.0; 1,655 stars, 195 forks;
TypeScript; repo created 2026-03-21, last push 2026-07-11 (~2.5 months with no commits as of this
writing).

## How It Works

Two independent data-capture paths feed the same graph renderer:

1. **Claude Code hooks** — a lightweight local HTTP hook server receives events directly from
   Claude Code for zero-latency streaming; Agent Flow auto-configures these hooks the first time
   its panel opens (re-run via the "Agent Flow: Configure Claude Code Hooks" command)
2. **Codex rollout tailing** — reads `~/.codex/sessions/**/rollout-*.jsonl` (respecting
   `CODEX_HOME`), surfacing tool calls, reasoning, and Codex's own authoritative token counts
3. **JSONL log replay** — point the app at any compatible JSONL event log to replay or watch
   activity after the fact

Both runtimes' sessions can be watched concurrently and shown side by side, or restricted to one
via an `agentVisualizer.runtime` setting. The UI adds a canvas (pan/zoom/click to inspect), a
timeline and transcript panel, a file-attention heatmap, and tabbed multi-session tracking.

### Installation

Three ways to run it, in increasing order of setup:

| Method | Command | Notes |
|---|---|---|
| Standalone (no VS Code) | `npx agent-flow-app` | Opens a browser UI; starts a local server (default port 3001) |
| VS Code extension | Install from the marketplace, then run "Agent Flow: Open Agent Flow" | Auto-configures CC hooks on first open |
| From source | `git clone` → `pnpm i` → `pnpm run setup` → `pnpm run dev` | For contributors / customization |

Requires Node.js 20+ and pnpm for the source path.

## Adoption Considerations

**Strengths**: solves a real, specific pain point (CC's execution is genuinely opaque without
something like this); two independent capture paths (hooks + rollout tailing) mean it doesn't
depend on Claude Code alone; the zero-config `npx agent-flow-app` path lowers the trial barrier;
Apache-2.0.

**Risks**: no commits since 2026-07-11 (~2.5 months as of 2026-09-24) — maintenance cadence
unclear; 27 open issues against 1,655 stars; trademarks on the "Agent Flow" name are asserted
separately (`TRADEMARK.md`) even though the code is Apache-2.0; no independent review of what the
local hook server does with session data beyond what the README states (local-only, no mention of
telemetry).

Cross-ref: [CC-hooks-system-analysis.md](../cc-native/configuration/CC-hooks-system-analysis.md) —
the PreToolUse/PostToolUse hook-event surface Agent Flow's HTTP hook server consumes.

## Sources

| Source | Content |
|---|---|
| [patoles/agent-flow][repo] | Repository README, install methods, license, stars (2026-09-24) |

[repo]: https://github.com/patoles/agent-flow
