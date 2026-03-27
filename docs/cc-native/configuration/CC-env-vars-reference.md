---
title: CC Environment Variables Reference
purpose: Consolidated reference for CLAUDE_CODE_* and related env vars relevant to autonomous agent workflows. Not exhaustive — links to official docs for the full list.
created: 2026-03-27
updated: 2026-03-27
validated_links: 2026-03-27
---

**Status**: Adopt

## What It Is

Claude Code exposes behavior through environment variables set in `settings.json` (`env` block), shell profile, or CI configuration. The [official env vars reference][env-vars] lists 80+ variables. This document extracts the subset relevant to autonomous agent workflows, cost control, and headless execution, organized by category with cross-references to existing analysis docs.

## Scope

This doc covers vars observed in agent workflows. For the **complete authoritative list**, see the [official env vars reference][env-vars]. For settings.json keys (not env vars), see the [official settings reference][settings].

## Variable Reference

### Model & Agent Selection

<!-- markdownlint-disable MD013 -->

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `ANTHROPIC_MODEL` | `sonnet` | Primary model alias or full ID | [env-vars][env-vars] |
| `CLAUDE_CODE_SUBAGENT_MODEL` | (inherits primary) | Model for Agent tool subagents and teammates | [env-vars][env-vars] |
| `CLAUDE_CODE_EFFORT_LEVEL` | (unset) | Reasoning effort: `low`, `medium`, `high`, `max` (Opus 4.6 only), `auto` | [env-vars][env-vars] |

<!-- markdownlint-enable MD013 -->

Cross-ref: [CC-model-provider-configuration.md](CC-model-provider-configuration.md)

### Agent Teams

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | `0` | Enable agent teams (`1` to enable) | [env-vars][env-vars] |

Cross-ref: [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md)

### Context & Token Control

<!-- markdownlint-disable MD013 -->

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | `0` | Prevent extended context window (stays at 200K) | [env-vars][env-vars] |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | `0` | Remove built-in git workflow instructions from context | [env-vars][env-vars] |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | ~95 | Auto-compaction trigger threshold (% of context window). Official docs say ~95%; observed triggers at ~78-85% ([#18264][gh-18264], [#18241][gh-18241]) | [env-vars][env-vars] |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | (model context size) | Override context capacity in tokens for compaction calculations | [env-vars][env-vars] |

<!-- markdownlint-enable MD013 -->

Cross-ref: [CC-extended-context-analysis.md](../context-memory/CC-extended-context-analysis.md), [CC-memory-system-analysis.md](../context-memory/CC-memory-system-analysis.md)

### Traffic & Telemetry

<!-- markdownlint-disable MD013 -->

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | `0` | Equivalent of `DISABLE_AUTOUPDATER` + `DISABLE_FEEDBACK_COMMAND` + `DISABLE_ERROR_REPORTING` + `DISABLE_TELEMETRY` | [env-vars][env-vars] |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | `0` | Enable OTel metrics/logs export | [env-vars][env-vars], [monitoring][monitoring] |
| `DISABLE_AUTOUPDATER` | `0` | Prevent automatic CC updates | [env-vars][env-vars] |
| `DISABLE_COST_WARNINGS` | `0` | Suppress cost warning messages | [env-vars][env-vars] |

<!-- markdownlint-enable MD013 -->

Cross-ref: [CC-version-pinning-resilience.md](../ci-execution/CC-version-pinning-resilience.md), [monitoring docs][monitoring]

### Session Guards & Runtime

<!-- markdownlint-disable MD013 -->

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDECODE` | Set by CC | Session guard — set to `1` in shells CC spawns. Clear to enable recursive spawning | [env-vars][env-vars] |
| `CLAUDE_CODE_TMPDIR` | `/tmp` (Unix) | Override temp directory. CC appends `/claude/` | [env-vars][env-vars] |
| `CLAUDE_CODE_SIMPLE` | `0` | Minimal mode (set by `--bare` flag). Disables hooks, plugins, MCP, auto memory, CLAUDE.md | [env-vars][env-vars] |

<!-- markdownlint-enable MD013 -->

Cross-ref: [CC-recursive-spawning-patterns.md](../agents-skills/CC-recursive-spawning-patterns.md)

### Runtime-Injected Variables (Not User-Configurable)

These vars are set by CC at runtime and observed via `env` inside a session. They are **not documented** in the official env vars page and cannot be configured by users.

<!-- markdownlint-disable MD013 -->

| Variable | Observed Value | Purpose | Observation |
|---|---|---|---|
| `CLAUDE_CODE_ENTRYPOINT` | `cli` | How CC was launched | CC 2.1.83, Codespaces, 2026-03-27 |
| `CLAUDE_CODE_SSE_PORT` | (dynamic) | SSE event stream port for IDE extensions | CC 2.1.83, Codespaces, 2026-03-27 |
| `CLAUDE_CODE_HOST_HTTP_PROXY_PORT` | (dynamic) | HTTP proxy port for sandboxed network access | CC 2.1.83, Codespaces, 2026-03-27 |
| `CLAUDE_CODE_HOST_SOCKS_PROXY_PORT` | (dynamic) | SOCKS proxy port for sandboxed network access | CC 2.1.83, Codespaces, 2026-03-27 |
| `SANDBOX_RUNTIME` | `1` | Set when running inside CC's sandbox | CC 2.1.83, Codespaces, 2026-03-27 |

<!-- markdownlint-enable MD013 -->

### Memory & Instructions

<!-- markdownlint-disable MD013 -->

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | `0` | Disable auto memory system | [env-vars][env-vars] |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | `0` | Load CLAUDE.md from `--add-dir` directories | [env-vars][env-vars] |

<!-- markdownlint-enable MD013 -->

Cross-ref: [CC-memory-system-analysis.md](../context-memory/CC-memory-system-analysis.md)

## Configuration Methods

Variables can be set via (in priority order, per [settings docs][settings]):

1. **Managed settings** (highest) — cannot be overridden
2. **CLI flags** — `--model`, `--effort`, etc.
3. **Shell environment** — `export VAR=value` before launching `claude`
4. **`settings.json` `env` block** — persistent per-project or user-level

See [examples/settings.json](../examples/settings.json) for a working `env` block.

## Discovery Method

To observe all CC-injected vars in a running session:

```bash
env | grep -E '^(CLAUDE|ANTHROPIC|SANDBOX|DISABLE)' | sort
```

Note: Runtime-injected vars (`CLAUDE_CODE_SSE_PORT`, `SANDBOX_RUNTIME`, etc.) reflect session state and are not user-configurable.

## Sources

<!-- markdownlint-disable MD013 -->

| Source | Content |
|---|---|
| [CC env vars reference][env-vars] | Official complete list (80+ vars) |
| [CC settings reference][settings] | `settings.json` keys and `env` block |
| [CC monitoring docs][monitoring] | OTel configuration and metrics |
| [CC statusline docs][statusline] | Statusline JSON schema and examples |
| CC 2.1.83 `env` output, Codespaces, 2026-03-27 | Runtime-injected vars observation |

<!-- markdownlint-enable MD013 -->

[env-vars]: https://code.claude.com/docs/en/env-vars
[settings]: https://code.claude.com/docs/en/settings
[monitoring]: https://code.claude.com/docs/en/monitoring-usage
[statusline]: https://code.claude.com/docs/en/statusline
[gh-18264]: https://github.com/anthropics/claude-code/issues/18264
[gh-18241]: https://github.com/anthropics/claude-code/issues/18241
