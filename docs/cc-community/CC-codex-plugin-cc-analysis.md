---
title: "Codex Plugin for Claude Code (openai/codex-plugin-cc)"
source: https://github.com/openai/codex-plugin-cc
purpose: Analysis of OpenAI's official Claude Code plugin that delegates to Codex — a rival lab building on CC's own hook/slash-command/subagent extension surface.
category: analysis
platform_scope: [claude-code, codex]
created: 2026-07-08
updated: 2026-07-08
validated_links: 2026-07-08
---

**Status**: Assess

## What It Is

[codex-plugin-cc][repo] is an **official OpenAI** Claude Code plugin (Apache-2.0; ~26.9k stars, v1.0.6
as of 2026-07-08) that lets a Claude Code user invoke **OpenAI Codex from inside their CC session** —
for code review or task delegation — without switching tools. Its README opener: *"Use Codex from
inside Claude Code for code reviews or to delegate tasks to Codex."*

Its research interest for this corpus is less the feature and more the **surface**: a competing lab
built a first-party integration entirely on Claude Code's *own* extension primitives — a concrete,
maintained reference for how the plugin + hook + subagent surface is meant to be composed. It is the
inverse direction of the community reimplementations catalogued in
[CC-community-reimplementations-landscape.md](CC-community-reimplementations-landscape.md) (which
rebuild CC), and distinct from `clawcodex` (a cleanroom Codex *reimplementation*) — this bridges an
external agent *into* CC.

## How It Works

Installed via the CC plugin marketplace, it wires into three extension mechanisms:

- **Slash commands:** `/codex:review`, `/codex:adversarial-review`, `/codex:rescue`,
  `/codex:transfer`, `/codex:status`, `/codex:result`, `/codex:cancel`, `/codex:setup`.
- **A registered subagent:** `codex:codex-rescue` (appears in `/agents`).
- **Hooks:** a `SessionStart` hook, plus an optional **`Stop` hook used as a review gate** — it can
  *block Claude's response* if Codex flags issues. This is the notable pattern: one agent gating
  another via the Stop hook.

Beyond synchronous review it supports **background task delegation** to Codex with job-status polling,
and **full session transfer** (conversation history) from CC into Codex. Requirements: a local Codex
CLI + `codex login`, a ChatGPT subscription or OpenAI API key, and Node.js ≥ 18.18.

## Adoption Decision

**Assess.** Not something this docs corpus *adopts*, but a high-signal artifact: it demonstrates the
Stop-hook-as-review-gate and subagent-registration patterns on a real, high-profile plugin, and shows
how cross-agent delegation is being productized on CC's surface. Watch it as a reference when
documenting CC's hook/plugin architecture; the cross-lab-delegation trend (CC ↔ Codex) is worth
tracking. Using it in practice couples a CC session to an OpenAI subscription/CLI — a dependency and
data-flow consideration, not a fit for key-free/offline workflows.

Cross-ref: [CC-community-plugins-landscape.md](CC-community-plugins-landscape.md) ·
[CC-official-plugins-landscape.md](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) ·
[codex-cli-analysis.md](../non-cc/codex-cli-analysis.md)

## Sources

| Source | Content |
|---|---|
| [openai/codex-plugin-cc][repo] | Plugin repo: README, slash commands, hooks, releases (Apache-2.0, v1.0.6, 2026-07-08) |

[repo]: https://github.com/openai/codex-plugin-cc
