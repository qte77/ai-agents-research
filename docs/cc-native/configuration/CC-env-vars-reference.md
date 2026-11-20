---
title: CC Environment Variables Reference
purpose: Consolidated reference for CLAUDE_CODE_* and related env vars relevant to autonomous agent workflows, including undocumented vars from binary string extraction.
created: 2026-03-27
updated: 2026-11-20
validated_links: 2026-11-18
status: adopt
---

## What It Is

Claude Code exposes behavior through environment variables set in `settings.json` (`env` block), shell profile, or CI configuration. The [official env vars reference][env-vars] lists 80+ variables. This document extracts the subset relevant to autonomous agent workflows, cost control, and headless execution, organized by category with cross-references to existing analysis docs.

## Scope

This doc covers vars observed in agent workflows. For the **complete authoritative list**, see the [official env vars reference][env-vars]. For settings.json keys (not env vars), see the [official settings reference][settings].

## Variable Reference

### Model & Agent Selection

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `ANTHROPIC_MODEL` | `sonnet` | Primary model alias or full ID | [env-vars][env-vars] |
| `CLAUDE_CODE_SUBAGENT_MODEL` | (inherits primary) | Default model for subagents, agent-team teammates and workflow agents that get no model another way; an alias such as `haiku` or a full model name. Since v2.1.251 a model Claude passes at spawn time and a `model` field in the agent definition (including `inherit`) take precedence over it; before that the variable overrode both. `inherit` is the same as unset. Order: [CC-session-cost-analysis.md § Documented cost levers](../sessions/CC-session-cost-analysis.md#documented-cost-levers) | [env-vars][env-vars] |
| `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` | (unset) | `1` applies the model set in `CLAUDE_CODE_SUBAGENT_MODEL` to every subagent, teammate and workflow agent: definition `model` fields are ignored and Claude can't pass a model at spawn time. Forks and skills running in a subagent with `model: inherit` still use the parent's model; set alone, subagents use the main conversation's model (built-in Explore keeps its own). Check with `/tasks`. Requires v2.1.257+ ([subagents][subagents-one-model]) | [env-vars][env-vars] |
| `CLAUDE_CODE_EFFORT_LEVEL` | (unset) | Reasoning effort: `low`, `medium`, `high`, `xhigh`, `max`; outranks `--effort`, `/effort` and the effort settings (a `maxEffortLevel` cap still applies). `auto` or `unset` sends no effort level, so the API default applies. Support and defaults vary by model (see [Effort Levels](CC-model-provider-configuration.md#effort-levels)) | [env-vars][env-vars] |

Cross-ref: [CC-model-provider-configuration.md](CC-model-provider-configuration.md)

### Agent Teams

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | `0` | Enable agent teams (`1` to enable) | [env-vars][env-vars] |

Cross-ref: [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md)

### Context & Token Control

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | (unset) | `1` turns off 1M-window support: removes `[1m]` model variants from the picker and holds models that run with the 1M window by default to 200K (documented). From v2.1.323 the window assumed for a model ID Claude Code does not recognize is 1M instead of 200K; `1` keeps 200K, and the changelog warns that other vendors' smaller-window models can fail every turn until `/clear` once full | [env-vars][env-vars], [changelog][changelog] (2.1.323) |
| `CLAUDE_CODE_MAX_CONTEXT_TOKENS` | (unset) | Overrides the context window Claude Code assumes for the active model (documented); since v2.1.193 how it applies depends on how Claude Code resolves the model ID (see the model-config page's "Correct the window for a gateway or custom model ID"). From v2.1.325 it also sets the window for unrecognized IDs starting with `claude-`, such as a gateway's `claude-sonnet-latest` | [env-vars][env-vars], [changelog][changelog] (2.1.325) |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` | `0` | `1` removes the built-in commit and PR instructions and the git status snapshot from context, in any session; takes precedence over the `includeGitInstructions` setting | [env-vars][env-vars] |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | (built-in default) | Percentage (1-100) of the auto-compact window at which compaction triggers. It can only lower the threshold: "values above the default percentage are ignored". The docs give no default number (checked 2026-11-09); observed triggers at ~78-85% ([#18264][gh-18264], [#18241][gh-18241]) | [env-vars][env-vars] |
| `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS` | 200000 | Minimum conversation size for idle compaction (compacting a session left idle for about 54 minutes, before its one-hour prompt cache expires); turn the feature off with `"idleCompaction": false` in settings. v2.1.299+ ([changelog][gh-changelog-cc]); see [CC-prompt-caching-behavior.md](../context-memory/CC-prompt-caching-behavior.md#idle-compaction-before-the-cache-expires) | [env-vars][env-vars] |
| `CLAUDE_CODE_AUTO_COMPACT_WINDOW` | (model context size) | Auto-compact window in tokens (100000 to 1000000); wins over the command, flag and setting; formats and precedence in [CC-extended-context-analysis.md](../context-memory/CC-extended-context-analysis.md#setting-the-auto-compact-window-autocompact) | [env-vars][env-vars] |
| `DISABLE_AUTO_COMPACT` | (unset) | `1` turns off automatic compaction near the context limit and idle compaction; overrides the `autoCompactEnabled` setting. Manual `/compact` still works | [env-vars][env-vars] |
| `DISABLE_COMPACT` | (unset) | `1` turns off all compaction, automatic and the manual `/compact` command | [env-vars][env-vars] |
| `BASH_MAX_OUTPUT_LENGTH` | 30000 | Characters of Bash output read back into the tool result (maximum 150000). Lowering it trims what long command output adds to context | [env-vars][env-vars] |
| `MAX_MCP_OUTPUT_TOKENS` | 25000 | Token cap on an MCP tool response; CC warns above 10,000 tokens | [env-vars][env-vars] |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | (per model; 32000 for an unrecognized model ID, cap 128000) | Maximum output tokens for most requests | [env-vars][env-vars] |
| `MAX_THINKING_TOKENS` | (unset: adaptive models choose their own depth) | Fixed extended-thinking budget, capped one token below the request's max output tokens and never below 1,024 | [env-vars][env-vars] |
| `ENABLE_TOOL_SEARCH` | (unset = `true`) | Defers MCP tool definitions so they load on demand instead of all entering context up front, except where tool search stays off | [env-vars][env-vars] |

Cross-ref: [CC-extended-context-analysis.md](../context-memory/CC-extended-context-analysis.md), [CC-memory-system-analysis.md](../context-memory/CC-memory-system-analysis.md)

### Prompt Caching

Each TTL-selection variable takes `5m` or `1h` only and requires CC v2.1.242+; CC ignores any other value. Added 2026-10-15 — see [CC-prompt-caching-behavior.md][cc-caching-behavior] for the full precedence order and the request-bucket table these variables feed into.

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_PROMPT_CACHE_TTL` | (per-bucket default) | Prompt-cache TTL for the **main conversation** bucket (interactive turns, `-p` runs, Agent SDK turns). Takes precedence over the `promptCacheTtl` setting and over `ENABLE_PROMPT_CACHING_1H`; `FORCE_PROMPT_CACHING_5M` overrides it. v2.1.242+ | [env-vars][env-vars], [cc-caching][cc-caching] |
| `CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL` | (per-bucket default) | Prompt-cache TTL for everything **outside** the main conversation (subagents, workflows, background work). Takes precedence over the `subagentPromptCacheTtl` setting and over `ENABLE_PROMPT_CACHING_1H`; `FORCE_PROMPT_CACHING_5M` overrides it. The API bills 1-hour cache writes at a higher rate. v2.1.242+ | [env-vars][env-vars] |
| `ENABLE_PROMPT_CACHING_1H` | `0` | Request a 1-hour TTL instead of the 5-minute default, for both buckets. Mainly for API-key / Bedrock / Google Cloud Agent Platform / Microsoft Foundry / Claude Platform on AWS users — a Claude subscription within included usage already gets the 1-hour TTL automatically on the main conversation. Lower precedence than the two `CLAUDE_CODE_*_PROMPT_CACHE_TTL` variables above | [env-vars][env-vars] |
| `ENABLE_PROMPT_CACHING_1H_BEDROCK` | — | Deprecated; use `ENABLE_PROMPT_CACHING_1H` | [env-vars][env-vars] |
| `FORCE_PROMPT_CACHING_5M` | `0` | Force the 5-minute TTL for **both** buckets, overriding every other TTL control (both `CLAUDE_CODE_*_PROMPT_CACHE_TTL` variables, `ENABLE_PROMPT_CACHING_1H`, and the `promptCacheTtl`/`subagentPromptCacheTtl` settings). Useful for debugging cache behavior or overriding a longer TTL set in managed settings | [env-vars][env-vars] |
| `DISABLE_PROMPT_CACHING` | `0` | Disable prompt caching for all models (takes precedence over the per-model variables below) | [env-vars][env-vars] |
| `DISABLE_PROMPT_CACHING_HAIKU` / `_SONNET` / `_OPUS` / `_FABLE` | `0` | Disable prompt caching for the default Haiku / Sonnet / Opus model, or for Fable models. `_HAIKU` covers the main conversation too only on CC v2.1.283+ | [env-vars][env-vars] |

The matching `settings.json` keys — `promptCacheTtl` (main conversation) and `subagentPromptCacheTtl` (everything else) — take the same `5m`/`1h` values and sit one precedence level below their env-var counterparts. See the [settings reference][settings-ref] (`#promptcachettl`, `#subagentpromptcachettl`).

Cross-ref: [CC-prompt-caching-behavior.md][cc-caching-behavior]

### Traffic & Telemetry

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | `0` | Equivalent of `DISABLE_AUTOUPDATER` + `DISABLE_FEEDBACK_COMMAND` + `DISABLE_ERROR_REPORTING` + `DISABLE_TELEMETRY`. **Blocks Remote Control** — eligibility check uses this path. Use individual flags instead if Remote Control is needed. See [CC-remote-control-analysis.md](../ci-remote/CC-remote-control-analysis.md#environment-variable-blockers) | [env-vars][env-vars] |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | `0` | Enable OTel metrics/logs export (prerequisite for all `OTEL_*` vars below) | [env-vars][env-vars], [monitoring][monitoring] |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | `0` | Enable distributed tracing (beta) in addition to metrics/logs | [monitoring][monitoring] |
| `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL` | (unset) | Re-enable the session quality survey for enterprises capturing responses through OpenTelemetry (disabled by default when OTel is active). Set to `1` to opt in. (v2.1.136) | CHANGELOG v2.1.136 |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` | `1740000` (29 min) | Refresh interval for dynamic OTLP headers | [monitoring][monitoring] |
| `DISABLE_AUTOUPDATER` | `0` | Prevent automatic CC updates | [env-vars][env-vars] |
| `CLAUDE_CODE_DISABLE_FEATURE_FLAGS` | (unset) | `1` turns off feature-flag fetching; [Remote Control][remote-control] and the other features that need flags become unavailable, every flag uses its built-in default, and telemetry stays on unless `DISABLE_TELEMETRY` is also set. v2.1.319+; the older name `DISABLE_GROWTHBOOK` still works and is the only one v2.1.124–v2.1.318 read | [env-vars][env-vars], [changelog][changelog] (2.1.319) |
| `DISABLE_COST_WARNINGS` | `0` | Suppress cost warning messages | [env-vars][env-vars] |

Cross-ref: [CC-version-pinning-resilience.md](../ci-remote/CC-version-pinning-resilience.md), [monitoring docs][monitoring], [CC-monitoring-telemetry-analysis.md](CC-monitoring-telemetry-analysis.md)

### OpenTelemetry Exporter Configuration

Standard `OTEL_*` variables (per the [OpenTelemetry specification][otel-spec]) that Claude Code honours when `CLAUDE_CODE_ENABLE_TELEMETRY=1`. Source for all rows: [monitoring][monitoring].

| Variable | Default | Purpose |
|---|---|---|
| `OTEL_METRICS_EXPORTER` | — | Comma-separated: `otlp`, `prometheus`, `console`, `none` |
| `OTEL_LOGS_EXPORTER` | — | Comma-separated: `otlp`, `console`, `none` |
| `OTEL_TRACES_EXPORTER` | — | Comma-separated: `otlp`, `console`, `none`. Requires `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | — | `grpc`, `http/json`, `http/protobuf` (applies to all signals) |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | — | Collector endpoint for all signals (e.g. `http://localhost:4317`) |
| `OTEL_EXPORTER_OTLP_{METRICS,LOGS,TRACES}_{PROTOCOL,ENDPOINT}` | — | Per-signal overrides |
| `OTEL_EXPORTER_OTLP_HEADERS` | — | Auth headers (e.g. `Authorization=Bearer token`) |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY` / `_CLIENT_CERTIFICATE` | — | mTLS client key/cert file paths |
| `OTEL_METRIC_EXPORT_INTERVAL` | `60000` ms | Metrics export interval |
| `OTEL_LOGS_EXPORT_INTERVAL` | `5000` ms | Logs export interval |
| `OTEL_TRACES_EXPORT_INTERVAL` | `5000` ms | Span batch export interval |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | `delta` | Set to `cumulative` if backend requires it |
| `OTEL_RESOURCE_ATTRIBUTES` | — | Custom `key=value` attributes (comma-separated, no spaces in values) on every metric and event, e.g. `team.id`, `cost_center`; see [cost attribution][telemetry-cost-attr] |
| `OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES` | `true` | `false` keeps `OTEL_RESOURCE_ATTRIBUTES` keys in the resource block only, off metric labels |

### OpenTelemetry Privacy Gates

All disabled by default. Enabling `OTEL_LOG_RAW_API_BODIES` implies consent to everything the other three would reveal. Source: [monitoring][monitoring].

| Variable | Effect |
|---|---|
| `OTEL_LOG_USER_PROMPTS` | Include prompt text in `user_prompt` event and `claude_code.interaction` span attribute (`1` to enable) |
| `OTEL_LOG_TOOL_DETAILS` | Include tool parameters (Bash command, MCP tool name, Skill name, file path, subagent type) on tool events / span attributes |
| `OTEL_LOG_TOOL_CONTENT` | Include tool input/output content in span events (truncated at 60 KB; requires tracing) |
| `OTEL_LOG_RAW_API_BODIES` | Emit full Anthropic Messages API request/response as `api_request_body` / `api_response_body` events. `1` = inline 60 KB truncation; `file:<dir>` = untruncated to disk with `body_ref` pointer |

### OpenTelemetry Cardinality Controls

Toggle metric attributes to trade granularity for storage cost. Source: [monitoring][monitoring].

| Variable | Default | Effect |
|---|---|---|
| `OTEL_METRICS_INCLUDE_SESSION_ID` | `true` | Include `session.id` attribute on metrics |
| `OTEL_METRICS_INCLUDE_VERSION` | `false` | Include `app.version` attribute on metrics |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | `true` | Include `user.account_uuid` and `user.account_id` on metrics |

### Display & Terminal

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN` | (unset) | Set to `1` to opt out of the fullscreen alternate-screen renderer and keep the conversation in the terminal's native scrollback. Useful for tmux, logging pipelines, or terminals that mishandle alternate-screen. (v2.1.132) | CHANGELOG v2.1.132 |

### Update & Package Management

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` | (unset) | When set on Homebrew or WinGet installations, CC runs the package-manager upgrade command in the background and prompts to restart once a new version is available. (v2.1.129) | CHANGELOG v2.1.129 |

### Session Guards & Runtime

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDECODE` | Set by CC | Session guard — set to `1` in shells CC spawns. Clear to enable recursive spawning | [env-vars][env-vars] |
| `CLAUDE_CONFIG_DIR` | `~/.claude` | Override the configuration directory (settings, hooks, plugins, memory; on Linux/Windows also credentials → per-dir login = one account per dir, enabling concurrent multi-account sessions; macOS credentials stay in Keychain and carry over). **Documented only in the [debug-config guide][debug-config]** — absent from the official env vars list as of 2026-07-23 | [debug-config][debug-config] |
| `CLAUDE_CODE_TMPDIR` | `/tmp` (Unix) | Override temp directory. CC appends `/claude/` | [env-vars][env-vars] |
| `CLAUDE_CODE_AUTO_MODE_SERVER` | (depends on session) | Whether CC asks the server to review auto-mode actions; `0` = CC's own classifier requests. v2.1.271+ (direct API connection: v2.1.281+). Since v2.1.319, with telemetry or feature flags off (including behind LLM gateways), calls the server can't check are asked about or denied with no fallback to the built-in classifier unless this is `0` (Bedrock, Vertex and Foundry are unchanged); behind a gateway, `1` turns the server check on even with `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` set | [env-vars][env-vars], [changelog][changelog] (2.1.319) |
| `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS` | `120000` | Milliseconds before a still-running MCP tool call moves to a background task; `0` turns automatic backgrounding off and, interactively, makes Claude wait for MCP tasks. v2.1.212+ | [env-vars][env-vars] |
| `CLAUDE_CODE_DISABLE_MCP_TASK_BACKGROUND` | (unset) | `1` = in an interactive session Claude waits for an MCP task's result (a call still moves to the background after the auto-background threshold). The docs say v2.1.304+; the changelog lists it under 2.1.319, when MCP tasks started running in the background in the terminal | [env-vars][env-vars], [changelog][changelog] (2.1.319) |
| `CLAUDE_CODE_DISABLE_MCP_TASKS` | (unset) | `1` turns MCP tasks off. Changelog only (2.1.319); not in the env-vars page on 2026-11-15 | [changelog][changelog] (2.1.319) |
| `CLAUDE_CODE_SIMPLE` | `0` | Minimal mode (set by `--bare` flag). Disables hooks, plugins, MCP, auto memory, CLAUDE.md | [env-vars][env-vars] |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | (unset) | Return to the original working directory after each Bash command. `1` = reset cwd to project root after each command; unset = cwd persists across Bash calls. **Note**: `=0` behavior is undocumented — only `1` is confirmed. See [tools-reference § Bash tool behavior][tools-ref], [#9359][gh-9359], [#11067][gh-11067] | [env-vars][env-vars], [tools-ref][tools-ref] |

Cross-ref: [CC-recursive-spawning-patterns.md](../agents-skills/CC-recursive-spawning-patterns.md), [CC-bash-mode-analysis.md](CC-bash-mode-analysis.md), [CC-multi-account-switching-landscape.md](../../cc-community/CC-multi-account-switching-landscape.md) (multi-account patterns on `CLAUDE_CONFIG_DIR`)

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

### v2.1.321–325 Additions

Changelog entries unless marked "documented" (the [env-vars page][env-vars] on 2026-11-17).

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `CLAUDE_CODE_AUTO_MODE_MODEL` | (unset) | Model for auto-mode classifier requests, full model ID; requires v2.1.302+ (documented). v2.1.323: also honored in managed settings for Claude Desktop sessions on third-party providers, once Desktop includes that version | [env-vars][env-vars], [changelog][changelog] (2.1.323) |
| `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` | (unset) | `1` opts into Code Mode (v2.1.323, experimental; documented at the [Code Mode page][code-mode]). `0` in managed settings blocks it for an organization; ignored in project settings files. See [CC-tools-inventory](CC-tools-inventory.md#code-mode-v21323) | [code-mode][code-mode] |
| `CLAUDE_CODE_DISABLE_AGENT_PROGRESS_SUMMARIES` | (unset) | `1` turns off subagent progress summaries and the requests that write them (v2.1.323 entry; "available since 2.1.318"). Changelog only: not confirmed on the env-vars page | [changelog][changelog] (2.1.323) |
| `CLAUDE_CODE_RESUME_HINT_COMMAND` | (unset) | For a wrapper that starts Claude Code: the name the exit hint prints as `<name> --resume <session-id>`; ignored if not matching `^\w[\w-]*$` and ignored in a settings `env` block (documented; v2.1.323+) | [env-vars][env-vars] |
| `CLAUDE_CODE_PERFORCE_MODE` | (unset) | `1` makes Edit/Write/NotebookEdit fail with a `p4 edit <file>` hint when the target lacks the owner-write bit (documented). v2.1.323 adds a one-time startup notice naming it when Perforce settings are found and the mode is off | [env-vars][env-vars], [changelog][changelog] (2.1.323) |
| `CLAUDE_CODE_AUTOMOUNT_ROOTS` | (unset) | Automount root folders skipped when Claude Code looks above the working directory for `CLAUDE.md`, skills and `.mcp.json` (documented; v2.1.323+). v2.1.323: `/home` as an autofs map is handled without it; set this for a map root deeper than one folder below `/` | [env-vars][env-vars], [changelog][changelog] (2.1.323) |
| `CLAUDE_CODE_OVERLOADED_RETRY_MAX_DELAY_MS` | `32000` | Ceiling on backoff between retries of a `529` overloaded error (documented: whole ms, 32000 to 300000; values above 64000 need v2.1.323+, whose changelog raised the maximum from 64000 to 300000) | [env-vars][env-vars], [changelog][changelog] (2.1.323) |
| `CLAUDE_CODE_PLUGIN_DIR_WATCH` | (unset) | Controls whether a mod reloads when its files change (documented, v2.1.287+): skills-directory mods reload by default in any session taking more than one prompt, non-interactive included; `--plugin-dir` mods reload only in interactive terminal sessions unless set to `1`; `0` turns reloading off everywhere. v2.1.321 changelog: headless sessions reload mods in `.claude/skills` on file change | [env-vars][env-vars], [changelog][changelog] (2.1.321) |
| `VERTEX_REGION_CLAUDE_FABLE_5_2` | (unset) | Region override for Fable 5.2 on Google Cloud's Agent Platform; added v2.1.321 (documented). Fast mode there needs `global`, `us` or `eu` (see [CC-fast-mode-analysis](CC-fast-mode-analysis.md)) | [env-vars][env-vars] |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (hosted) | (see above) | v2.1.323 changelog: in Anthropic-hosted cloud sessions it stops applying to auto-memory extraction and, in some sessions, to `/btw`; the main conversation still follows it | [changelog][changelog] (2.1.323) |
| `MCP_SDK_GENERATION` | v2 | Pins the MCP client runtime (`v1` or `v2`; documented). v2.1.323: `v1` now runs the v2 client in a compatibility mode (earlier handshake, relaxed OAuth sign-in checks) because the v1 client is removed | [env-vars][env-vars], [changelog][changelog] (2.1.323) |
| `ALL_PROXY` | (unset) | v2.1.323: organization settings and policy requests no longer use a proxy set only by `ALL_PROXY` (set `HTTPS_PROXY`). v2.1.325: plugin marketplace and plugin downloads use a CONNECT tunnel when it is the only proxy, so a proxy refusing CONNECT now fails them | [changelog][changelog] (2.1.323, 2.1.325) |

## Configuration Methods

Variables can be set in the shell (`export VAR=value` before launching `claude`) or in an `env` block in a settings file. Per the [settings docs][settings-precedence], "Environment variables aren't a level in this stack": an `env` block "is an ordinary key and follows the levels above", so when several settings files set the same variable, the highest-precedence file wins:

1. **Managed settings** (highest)
2. **`--settings <file-or-json>`** for one session (the only command-line level; other flags such as `--model` "aren't part of this stack")
3. **`.claude/settings.local.json`**
4. **`.claude/settings.json`**
5. **`~/.claude/settings.json`**

Against the shell, the settings value wins: "When the same variable is set in both your shell and a settings file `env` block, the settings file value applies in most sessions" ([env-vars precedence][env-vars-precedence]). Project and local settings can't set some variables at all, such as `CLAUDE_CONFIG_DIR`, `HOME`, the claude.ai sign-in variables (`CLAUDE_CODE_OAUTH_TOKEN` and related) and the OpenTelemetry exporter variables (only off values such as `none` or `0` apply from those files); set those in the shell, user or managed settings (see the `env` entry in the [settings reference][settings-ref-env]).

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

The following variables were extracted from the CC 2.1.87 CLI binary via `strings` / `grep -boa`. Most are **not listed** in the [official env vars reference][env-vars] (one exception is noted below). Presence in the binary does not guarantee functionality — some may be deprecated, internal-only, or feature-gated.

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
| `CLAUDE_CODE_DISABLE_ADVISOR_TOOL` | Disables the advisor tool entirely — `/advisor` becomes unavailable, any configured `advisorModel` is ignored, and `--advisor` is accepted but has no effect | Documented: [CC-advisor-tool-analysis.md](CC-advisor-tool-analysis.md) |
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

### ANTHROPIC_* Documented (Recent Additions)

| Variable | Default | Purpose | Source |
|---|---|---|---|
| `ANTHROPIC_BEDROCK_SERVICE_TIER` | `default` | Select AWS Bedrock service tier: `default`, `flex`, or `priority`. Sent as the `X-Amzn-Bedrock-Service-Tier` request header. (v2.1.122) | CHANGELOG v2.1.122 |

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
| [Subagents — Run every subagent on one model][subagents-one-model] | `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` behaviour and exceptions (accessed 2026-11-19) |
| [CC prompt-caching docs][cc-caching] | TTL-selection variables, precedence order, disable variables (accessed 2026-10-15) |
| [CC settings reference][settings-ref] | `promptCacheTtl` / `subagentPromptCacheTtl` setting keys (accessed 2026-10-15) |
| [CC CHANGELOG][changelog] | 2.1.319 entries for the auto-mode, feature-flag and MCP-task variables (accessed 2026-11-15) |
| [CC debug-your-config guide][debug-config] | `CLAUDE_CONFIG_DIR` behavior + per-platform credential storage |
| [CC monitoring docs][monitoring] | OTel configuration and metrics |
| [CC statusline docs][statusline] | Statusline JSON schema and examples |
| CC 2.1.83 `env` output, Codespaces, 2026-03-27 | Runtime-injected vars observation |
| CC 2.1.87 CLI binary string extraction, Codespaces, 2026-03-29 | Undocumented vars via `grep -oP` |
| [TurboAI.dev version tracker][turboai] | 204 env vars, 41 feature gates tracked across releases |
| [unkn0wncode env vars gist][unkn0wncode] | Categorized 200+ env vars (v2.1.81) |
| [CC binary architecture][binary-arch] | Binary analysis methodology |
| [CC RE landscape][re-landscape] | Community reverse engineering tools and research |
| [CC CHANGELOG][changelog] | v2.1.321–325 variable additions and changes (accessed 2026-11-17) |
| [CC Code Mode page][code-mode] | `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` (accessed 2026-11-17) |

[env-vars]: https://code.claude.com/docs/en/env-vars
[settings]: https://code.claude.com/docs/en/settings
[settings-precedence]: https://code.claude.com/docs/en/settings#settings-precedence
[env-vars-precedence]: https://code.claude.com/docs/en/env-vars#precedence
[settings-ref-env]: https://code.claude.com/docs/en/settings-reference#env
[settings-ref]: https://code.claude.com/docs/en/settings-reference
[changelog]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
[code-mode]: https://code.claude.com/docs/en/code-mode
[remote-control]: https://code.claude.com/docs/en/remote-control
[cc-caching]: https://code.claude.com/docs/en/prompt-caching
[cc-caching-behavior]: ../context-memory/CC-prompt-caching-behavior.md
[debug-config]: https://code.claude.com/docs/en/debug-your-config
[tools-ref]: https://code.claude.com/docs/en/tools-reference#bash-tool-behavior
[monitoring]: https://code.claude.com/docs/en/monitoring-usage
[telemetry-cost-attr]: CC-monitoring-telemetry-analysis.md#cost-attribution
[otel-spec]: https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options
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
[gh-changelog-cc]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
[subagents-one-model]: https://code.claude.com/docs/en/sub-agents#run-every-subagent-on-one-model
