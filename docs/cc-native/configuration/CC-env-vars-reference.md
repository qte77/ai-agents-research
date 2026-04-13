---
title: CC Environment Variables Reference
purpose: Consolidated reference for CLAUDE_CODE_* and related env vars relevant to autonomous agent workflows, including undocumented vars from binary string extraction.
created: 2026-03-27
updated: 2026-04-13
validated_links: 2026-04-13
---

**Status**: Adopt

## What It Is

Claude Code exposes behavior through environment variables set in `settings.json` (`env` block), shell profile, or CI configuration. The [official env vars reference][env-vars] lists 80+ variables. This document extracts the subset relevant to autonomous agent workflows, cost control, and headless execution, organized by category with cross-references to existing analysis docs.

## Scope

This doc covers vars observed in agent workflows. For the **complete authoritative list**, see the [official env vars reference][env-vars]. For settings.json keys (not env vars), see the [official settings reference][settings].

## Variable Reference

### Model & Agent Selection

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `ANTHROPIC_MODEL` | `sonnet` | Primary model alias or full ID | [env-vars][env-vars] |
| `CLAUDE_CODE_SUBAGENT_MODEL` | (inherits primary) | Model for Agent tool subagents and teammates | [env-vars][env-vars] |
| `CLAUDE_CODE_EFFORT_LEVEL` | (unset) | Reasoning effort: `low`, `medium`, `high`, `max` (Opus 4.6 only), `auto` | [env-vars][env-vars] |

Cross-ref: [CC-model-provider-configuration.md](CC-model-provider-configuration.md)

### Agent Teams

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | `0` | Enable agent teams (`1` to enable) | [env-vars][env-vars] |

Cross-ref: [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md)

### Context & Token Control

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | `0` | Prevent extended context window (stays at 200K) | [env-vars][env-vars] |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | `0` | Remove built-in git workflow instructions from context | [env-vars][env-vars] |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | ~95 | Auto-compaction trigger threshold (% of context window). Official docs say ~95%; observed triggers at ~78-85% ([#18264][gh-18264], [#18241][gh-18241]) | [env-vars][env-vars] |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | (model context size) | Override context capacity in tokens for compaction calculations | [env-vars][env-vars] |

Cross-ref: [CC-extended-context-analysis.md](../context-memory/CC-extended-context-analysis.md), [CC-memory-system-analysis.md](../context-memory/CC-memory-system-analysis.md)

### Traffic & Telemetry

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | `0` | Equivalent of `DISABLE_AUTOUPDATER` + `DISABLE_FEEDBACK_COMMAND` + `DISABLE_ERROR_REPORTING` + `DISABLE_TELEMETRY`. **Blocks Remote Control** — eligibility check uses this path. Use individual flags instead if Remote Control is needed. See [CC-remote-control-analysis.md](../ci-remote/CC-remote-control-analysis.md#environment-variable-blockers) | [env-vars][env-vars] |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | `0` | Enable OTel metrics/logs export | [env-vars][env-vars], [monitoring][monitoring] |
| `DISABLE_AUTOUPDATER` | `0` | Prevent automatic CC updates | [env-vars][env-vars] |
| `DISABLE_COST_WARNINGS` | `0` | Suppress cost warning messages | [env-vars][env-vars] |

Cross-ref: [CC-version-pinning-resilience.md](../ci-remote/CC-version-pinning-resilience.md), [monitoring docs][monitoring]

### Session Guards & Runtime

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDECODE` | Set by CC | Session guard — set to `1` in shells CC spawns. Clear to enable recursive spawning | [env-vars][env-vars] |
| `CLAUDE_CODE_TMPDIR` | `/tmp` (Unix) | Override temp directory. CC appends `/claude/` | [env-vars][env-vars] |
| `CLAUDE_CODE_SIMPLE` | `0` | Minimal mode (set by `--bare` flag). Disables hooks, plugins, MCP, auto memory, CLAUDE.md | [env-vars][env-vars] |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | (unset) | Return to the original working directory after each Bash command. `1` = reset cwd to project root after each command; unset = cwd persists across Bash calls. **Note**: `=0` behavior is undocumented — only `1` is confirmed. See [tools-reference § Bash tool behavior][tools-ref], [#9359][gh-9359], [#11067][gh-11067] | [env-vars][env-vars], [tools-ref][tools-ref] |

Cross-ref: [CC-recursive-spawning-patterns.md](../agents-skills/CC-recursive-spawning-patterns.md), [CC-bash-mode-analysis.md](CC-bash-mode-analysis.md)

### Runtime-Injected Variables (Not User-Configurable)

These vars are set by CC at runtime and observed via `env` inside a session. They are **not documented** in the official env vars page and cannot be configured by users.

| Variable | Observed Value | Purpose | Observation |
|---|---|---|---|
| `CLAUDE_CODE_ENTRYPOINT` | `cli` | How CC was launched | CC 2.1.83, Codespaces, 2026-03-27 |
| `CLAUDE_CODE_SSE_PORT` | (dynamic) | WebSocket (JSON-RPC 2.0 / MCP) port for IDE extensions. Despite the name, this is **not SSE** — it is a WebSocket server with per-session auth token stored at `~/.claude/ide/<port>.lock`. Localhost-only binding (`127.0.0.1`). Protocol reverse-engineered by [coder/claudecode.nvim][claudecode-nvim]. See also `ENABLE_IDE_INTEGRATION` | CC 2.1.83, Codespaces, 2026-03-27 |
| `CLAUDE_CODE_HOST_HTTP_PROXY_PORT` | (dynamic) | HTTP proxy port for sandboxed network access | CC 2.1.83, Codespaces, 2026-03-27 |
| `CLAUDE_CODE_HOST_SOCKS_PROXY_PORT` | (dynamic) | SOCKS proxy port for sandboxed network access | CC 2.1.83, Codespaces, 2026-03-27 |
| `SANDBOX_RUNTIME` | `1` | Set when running inside CC's sandbox | CC 2.1.83, Codespaces, 2026-03-27 |

### Memory & Instructions

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | `0` | Disable auto memory system | [env-vars][env-vars] |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | `0` | Load CLAUDE.md from `--add-dir` directories | [env-vars][env-vars] |

Cross-ref: [CC-memory-system-analysis.md](../context-memory/CC-memory-system-analysis.md)

## Configuration Methods

Variables can be set via (in priority order, per [settings docs][settings]):

1. **Managed settings** (highest) — cannot be overridden
2. **CLI flags** — `--model`, `--effort`, etc.
3. **Shell environment** — `export VAR=value` before launching `claude`
4. **`settings.json` `env` block** — persistent per-project or user-level

See [examples/settings.json](../examples/settings.json) for a working `env` block.

### MCP servers and PATH

MCP servers and hook commands are spawned from Claude Code's own process environment — **not** via a login shell. Shell profile files (`.bashrc`, `.zshrc`, `.profile`) are not sourced. If a tool binary (e.g., `npx`, `node`) is installed to a non-standard location, it must be either:

1. Symlinked to a directory already in CC's inherited `PATH` (e.g., `~/.local/bin/`)
2. Added via the `env` block in `settings.json`: `"PATH": "/custom/bin:${PATH}"`
3. Specified as an absolute path in the MCP server `command` field

This commonly affects user-local Node.js installs (e.g., `~/.local/share/node/bin/`) that rely on `.bashrc` PATH additions. MCP servers using `npx` will fail with "command not found" unless the symlink or env override is in place.

Source: [CC plugins reference — environment variables](https://code.claude.com/docs/en/plugins-reference), [CC MCP docs](https://code.claude.com/docs/en/mcp). Observation: Opus 4.6, 2026-04-13.

## Discovery Method

To observe all CC-injected vars in a running session:

```bash
env | grep -E '^(CLAUDE|ANTHROPIC|SANDBOX|DISABLE)' | sort
```

Note: Runtime-injected vars (`CLAUDE_CODE_SSE_PORT`, `SANDBOX_RUNTIME`, etc.) reflect session state and are not user-configurable.

## Undocumented Variables (Binary String Extraction)

The following variables were extracted from the CC 2.1.87 CLI binary via `strings` / `grep -boa`. They are **not listed** in the [official env vars reference][env-vars]. Presence in the binary does not guarantee functionality — some may be deprecated, internal-only, or feature-gated.

**Method**: `grep -oP 'CLAUDE_CODE_[A-Z_]+' <binary> | sort -u` against `/home/vscode/.local/share/claude/versions/2.1.87` ([frr-build][frr-build]).

Cross-ref: [CC-binary-architecture.md](CC-binary-architecture.md), [CC RE landscape][re-landscape]

### Feature Flags & Experimental

| Variable | Inferred Purpose | Notes |
|---|---|---|
| `CLAUDE_CODE_ENABLE_CFC` | Unknown feature gate | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_ENABLE_XAA` | Unknown feature gate | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_ENABLE_TASKS` | Enable task system | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION` | Prompt suggestions | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_ENABLE_FINE_GRAINED_TOOL_STREAMING` | Tool-level streaming. Adds `eager_input_streaming: true` to tool definitions. Reduces permission prompt latency from 10-20s to 1-3s (especially Bedrock). Now GA across all platforms. `1` to enable, `0` to disable | String extraction, CC 2.1.87; confirmed GA |
| `CLAUDE_CODE_ENABLE_TOKEN_USAGE_ATTACHMENT` | Token usage in responses | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING` | SDK checkpoint support | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | Extended telemetry | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED` | Force plan mode | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_PLAN_MODE_INTERVIEW_PHASE` | Plan mode phase control | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_PLAN_V` | Plan version selector | String extraction, CC 2.1.87 |

### Disable Flags

| Variable | Inferred Purpose | Notes |
|---|---|---|
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` | Disable adaptive thinking | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_ADVISOR_TOOL` | Disable advisor tool | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_ATTACHMENTS` | Disable file attachments | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` | Disable background tasks | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_CLAUDE_MDS` | Disable CLAUDE.md loading | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_COMMAND_INJECTION_CHECK` | Skip security check on Bash | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_CRON` | Disable cron scheduling | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` | Disable beta features | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_FAST_MODE` | Disable fast mode toggle | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` | Disable quality surveys | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING` | Disable file checkpoints | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_LEGACY_MODEL_REMAP` | Disable model alias remapping | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK` | Disable non-streaming fallback | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL` | Skip official plugin auto-install | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_PRECOMPACT_SKIP` | Disable pre-compaction optimization | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` | Disable terminal title updates | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_THINKING` | Disable thinking entirely | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_DISABLE_VIRTUAL_SCROLL` | Disable virtual scrolling | String extraction, CC 2.1.87 |

### Teams & Collaboration

| Variable | Inferred Purpose | Notes |
|---|---|---|
| `CLAUDE_CODE_TEAMMATE_COMMAND` | Command to invoke teammate agent | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_TEAM_NAME` | Team identifier | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_IS_COWORK` | Cowork mode detection | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_AGENT_LIST_IN_MESSAGES` | Expose agent list in messages | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_AGENT_NAME` | Agent identity | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_AGENT_RULE_DISABLED` | Disable agent rules | String extraction, CC 2.1.87 |

### Plugin & MCP Internals

| Variable | Inferred Purpose | Notes |
|---|---|---|
| `CLAUDE_CODE_PLUGIN_CACHE_DIR` | Plugin cache directory | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_PLUGIN_SEED_DIR` | Plugin seed/template directory | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_PLUGIN_USE_ZIP_CACHE` | Use zip-based plugin cache | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` | Git timeout for plugin ops | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_SYNC_PLUGIN_INSTALL` | Synchronous plugin install | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_SYNC_PLUGIN_INSTALL_TIMEOUT_MS` | Timeout for sync install | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_MCP_INSTR_DELTA` | MCP instruction delta | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_MCP_SERVER_NAME` | MCP server name override | String extraction, CC 2.1.87; also in [turboai][turboai] |
| `CLAUDE_CODE_MCP_SERVER_URL` | MCP server URL override | String extraction, CC 2.1.87; also in [turboai][turboai] |
| `CLAUDE_CODE_USE_COWORK_PLUGINS` | Enable Cowork plugin mode | String extraction, CC 2.1.87 |

### OAuth & Auth

| Variable | Inferred Purpose | Notes |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | OAuth access token | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_OAUTH_REFRESH_TOKEN` | OAuth refresh token | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_OAUTH_CLIENT_ID` | OAuth client ID | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_OAUTH_SCOPES` | OAuth scopes | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_OAUTH_TOKEN_FILE_DESCRIPTOR` | OAuth token via fd | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_CUSTOM_OAUTH_URL` | Custom OAuth endpoint | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_SESSION_ACCESS_TOKEN` | Session token | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_WEBSOCKET_AUTH_FILE_DESCRIPTOR` | WebSocket auth via fd | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_API_KEY_FILE_DESCRIPTOR` | API key via fd | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` | API key helper cache TTL | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH` | Skip Bedrock auth | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH` | Skip Vertex auth | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH` | Skip Foundry auth | String extraction, CC 2.1.87 |

### Runtime Limits & Performance

| Variable | Inferred Purpose | Notes |
|---|---|---|
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Response token limit | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_MAX_RETRIES` | Max API retries | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY` | Parallel tool limit | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | Read tool token cap | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_IDLE_THRESHOLD_MINUTES` | Idle timeout | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_IDLE_TOKEN_THRESHOLD` | Idle token limit | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_STALL_TIMEOUT_MS_FOR_TESTING` | Stall detection timeout | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_SLOW_OPERATION_THRESHOLD_MS` | Slow op warning threshold | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_BLOCKING_LIMIT_OVERRIDE` | Blocking call limit | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_GLOB_HIDDEN` | Include hidden files in Glob | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_GLOB_NO_IGNORE` | Ignore .gitignore in Glob | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_GLOB_TIMEOUT_SECONDS` | Glob timeout | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` | SessionEnd hook timeout | String extraction, CC 2.1.87 |

### Remote & IDE

| Variable | Inferred Purpose | Notes |
|---|---|---|
| `CLAUDE_CODE_REMOTE` | Remote session flag | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_REMOTE_SESSION_ID` | Remote session identifier | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` | Remote environment type | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_REMOTE_MEMORY_DIR` | Remote memory directory | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_REMOTE_SEND_KEEPALIVES` | Remote keepalive flag | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_CONTAINER_ID` | Container identifier | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_IDE_HOST_OVERRIDE` | IDE host override | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL` | Skip IDE extension install | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_IDE_SKIP_VALID_CHECK` | Skip IDE validation | String extraction, CC 2.1.87 |
| `CLAUDE_CODE_AUTO_CONNECT_IDE` | Auto-connect to IDE | String extraction, CC 2.1.87 |

### ANTHROPIC_* Undocumented

| Variable | Inferred Purpose | Notes |
|---|---|---|
| `ANTHROPIC_FOUNDRY_API_KEY` | Microsoft Foundry API key | String extraction, CC 2.1.87 |
| `ANTHROPIC_FOUNDRY_AUTH_TOKEN` | Foundry auth token | String extraction, CC 2.1.87 |
| `ANTHROPIC_FOUNDRY_BASE_URL` | Foundry endpoint | String extraction, CC 2.1.87 |
| `ANTHROPIC_FOUNDRY_RESOURCE` | Foundry resource ID | String extraction, CC 2.1.87 |
| `ANTHROPIC_SMALL_FAST_MODEL` | Haiku-tier model override | String extraction, CC 2.1.87 |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Haiku model AWS region | String extraction, CC 2.1.87 |
| `ANTHROPIC_CUSTOM_MODEL_OPTION` | Custom model option | String extraction, CC 2.1.87 |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` | Custom model display name | String extraction, CC 2.1.87 |
| `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` | Custom model description | String extraction, CC 2.1.87 |
| `ANTHROPIC_UNIX_SOCKET` | Unix socket transport | String extraction, CC 2.1.87 |
| `ANTHROPIC_BETAS` | Beta feature flags | String extraction, CC 2.1.87 |
| `ANTHROPIC_CUSTOM_HEADERS` | Custom HTTP headers | String extraction, CC 2.1.87 |
| `ANTHROPIC_LOG` | SDK logging level | String extraction, CC 2.1.87 |

## Sources

| Source | Content |
|---|---|
| [CC env vars reference][env-vars] | Official complete list (80+ vars) |
| [CC settings reference][settings] | `settings.json` keys and `env` block |
| [CC monitoring docs][monitoring] | OTel configuration and metrics |
| [CC statusline docs][statusline] | Statusline JSON schema and examples |
| CC 2.1.83 `env` output, Codespaces, 2026-03-27 | Runtime-injected vars observation |
| CC 2.1.87 CLI binary string extraction, Codespaces, 2026-03-29 | Undocumented vars via `grep -oP` |
| [TurboAI.dev version tracker][turboai] | 204 env vars, 41 feature gates tracked across releases |
| [unkn0wncode env vars gist][unkn0wncode] | Categorized 200+ env vars (v2.1.81) |
| [CC binary architecture][binary-arch] | Binary analysis methodology |
| [CC RE landscape][re-landscape] | Community reverse engineering tools and research |

[env-vars]: https://code.claude.com/docs/en/env-vars
[settings]: https://code.claude.com/docs/en/settings
[tools-ref]: https://code.claude.com/docs/en/tools-reference#bash-tool-behavior
[monitoring]: https://code.claude.com/docs/en/monitoring-usage
[statusline]: https://code.claude.com/docs/en/statusline
[gh-9359]: https://github.com/anthropics/claude-code/issues/9359
[gh-11067]: https://github.com/anthropics/claude-code/issues/11067
[gh-18264]: https://github.com/anthropics/claude-code/issues/18264
[gh-18241]: https://github.com/anthropics/claude-code/issues/18241
[turboai]: https://www.turboai.dev/blog/claude-code-versions
[unkn0wncode]: https://gist.github.com/unkn0wncode/f87295d055dd0f0e8082358a0b5cc467
[binary-arch]: CC-binary-architecture.md
[re-landscape]: ../../cc-community/CC-reverse-engineering-landscape.md
[frr-build]: https://www.frr.dev/posts/claude-code-native-build-bun/
[claudecode-nvim]: https://github.com/coder/claudecode.nvim
