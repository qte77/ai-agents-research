---
title: JetBrains Air Analysis
source: https://air.dev
purpose: Analysis of JetBrains Air as an agentic development environment for multi-agent orchestration.
created: 2026-03-20
updated: 2026-11-26
validated_links_on: 2026-11-21
status: assess
---

**Details:** Public preview; macOS only, Windows/Linux planned 2026 (unverified: current docs describe Air in IDEs, an Air Gateway CLI, Air Teams in the cloud and mobile, and steer Air app users to Air in IDEs)

## What It Is

JetBrains Air is an **agentic development environment** (not an IDE or coding
agent itself) that orchestrates multiple coding agents in parallel. Built by
JetBrains, it wraps existing agents -- Codex, Claude Agent, Gemini CLI, and
Junie -- into a unified task management interface.

> Status 2026-11-18: Gemini CLI stopped serving free, AI Pro and AI Ultra users on 2026-06-18 ([gemini-cli-analysis.md](../coding-agents/gemini-cli-analysis.md)); the JetBrains docs (checked 2026-11-26) list Claude Agent, OpenAI Codex, GitHub Copilot and Junie for Air Teams cloud tasks, and name Gemini CLI only as an example of an agent to run locally in Air in IDEs.

**Key distinction**: Air is an orchestrator, not an agent. It delegates to
agents rather than writing code itself.

## Core Capabilities

- **Multi-agent parallel execution**: Run Codex, Claude Agent, Gemini CLI,
  Junie concurrently on different tasks
- **Task isolation**: Git worktrees, Docker containers (both unverified), or cloud environments
  (available to some customers) per task
- **Codebase-aware context**: Reference files, commits, classes, methods,
  symbols, images when defining tasks
- **Built-in diff viewer** with commenting for agent feedback
- **Interactive plan mode**: Refine tasks step-by-step before execution
- **Agent Client Protocol (ACP)** support: agents added through `acp.json` run locally

## Agent Support

| Agent | Status |
|---|---|
| Claude Agent (Anthropic) | Supported |
| OpenAI Codex | Supported |
| Gemini CLI | Local only (Air in IDEs; not an Air Teams cloud agent) |
| Junie (JetBrains) | Supported |
| GitHub Copilot | Supported (Air Teams cloud tasks) |
| ACP-compatible agents | Supported locally via `acp.json`; not available in Air Teams |

## Execution Environments

- **Local** (default)
- **Git Worktree** -- isolated branch per task (unverified)
- **Docker** -- containerized sandboxing (unverified)
- **Cloud** -- Air Teams cloud environments, available to some customers (JetBrains product page, checked 2026-11-26); Bring Your Own Cloud (AWS) was added in the week of 2026-10-11

## Key Differentiators

- **JetBrains ecosystem**: 26 years of IDE tooling; built-in terminal, Git
  client, preview
- **Not a replacement for IDEs**: Designed to complement JetBrains IDEs, not
  replace them
- **Agent-agnostic**: Switch agents freely across projects
- **BYOK + JetBrains AI subscription**: Dual auth model; Air Teams cloud tasks always use JetBrains AI credits

## Limitations

- macOS only (preview; unverified)
- CLI: an Air Gateway CLI exists (the changelog lists a JetBrains Central CLI); headless or non-interactive use is unverified
- No SDK
- Not open source
- Requires JetBrains AI subscription or provider API keys
- Claude subscriptions work only through the terminal surface of Air in IDEs (Claude Code in the terminal), not the chat/SDK surface, which needs an API key

## Relevance to coding-harness-eval

**Tier 2** (AI IDE / orchestrator, no headless). Air cannot be included in
the automated harness comparison unless a headless mode is confirmed (unverified; a CLI exists). However,
it is relevant as a **competing orchestration pattern** -- Air's multi-agent
parallel task model with git worktree isolation mirrors what the
coding-harness-eval harness builds programmatically.

## Sources

| Source | Content |
|---|---|
| [air.dev](https://air.dev) | Product page |
| [JetBrains blog](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/) | Launch announcement |
| [Air in IDEs quickstart](https://www.jetbrains.com/help/air/air-in-ides-quickstart.html) | Setup and usage |
