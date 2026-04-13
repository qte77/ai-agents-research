---
title: CC CLI Reference
purpose: Single canonical reference for all claude CLI flags, subcommands, and constraints. Other docs cross-ref here for flag definitions.
created: 2026-04-13
updated: 2026-04-13
validated_links: 2026-04-13
---

**Status**: Adopt

## What It Is

Complete reference for the `claude` CLI. Sourced from the [official CLI reference][cli-ref] and `claude --help` (Opus 4.6). The official docs note that `--help` does not list every flag — this document covers both.

For env vars see [CC-env-vars-reference.md](CC-env-vars-reference.md). For tools see [CC-tools-inventory.md](CC-tools-inventory.md).

## Subcommands

| Command | Description | Source |
|---|---|---|
| `claude` | Start interactive session | [cli-ref][cli-ref] |
| `claude "query"` | Start with initial prompt | [cli-ref][cli-ref] |
| `claude -p "query"` | Print mode (non-interactive), then exit | [cli-ref][cli-ref] |
| `cat file \| claude -p "query"` | Process piped content | [cli-ref][cli-ref] |
| `claude auth login` | Sign in. Accepts `--email`, `--sso`, `--console` | [auth][auth] |
| `claude auth logout` | Sign out | [cli-ref][cli-ref] |
| `claude auth status` | Auth status as JSON. `--text` for human-readable | [cli-ref][cli-ref] |
| `claude agents` | List configured subagents by source | [cli-ref][cli-ref] |
| `claude auto-mode defaults` | Print built-in auto-mode classifier rules as JSON | [auto-mode][auto-mode] |
| `claude auto-mode config` | Show effective auto-mode config with settings applied | [auto-mode][auto-mode] |
| `claude mcp` | Configure MCP servers | [mcp][mcp] |
| `claude plugin` | Manage plugins. Alias: `claude plugins` | [plugins-ref][plugins-ref] |
| `claude remote-control` | Start Remote Control server (no local session) | [remote-control][remote-control] |
| `claude setup-token` | Generate long-lived OAuth token for CI/scripts | [auth][auth] |
| `claude update` | Update to latest version | [cli-ref][cli-ref] |
| `claude doctor` | Health check for auto-updater | [cli-ref][cli-ref] |
| `claude install [target]` | Install native build (`stable`, `latest`, or version) | [cli-ref][cli-ref] |

**Analysis**: [CC-version-pinning-resilience.md](../ci-remote/CC-version-pinning-resilience.md), [CC-web-auth-setup-analysis.md](../ci-remote/CC-web-auth-setup-analysis.md)

## Session Flags

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `-c`, `--continue` | Resume most recent conversation in current directory | — | [cli-ref][cli-ref] |
| `-r`, `--resume` | Resume session by ID or name, or show picker | — | [cli-ref][cli-ref] |
| `--fork-session` | Create new session ID when resuming | With `--resume` or `--continue` | [cli-ref][cli-ref] |
| `-n`, `--name` | Set display name (shown in `/resume`, terminal title) | — | [cli-ref][cli-ref] |
| `--from-pr` | Resume sessions linked to a GitHub PR by number or URL | — | [cli-ref][cli-ref] |
| `--session-id` | Use a specific UUID for the session | Must be valid UUID | [cli-ref][cli-ref] |
| `--no-session-persistence` | Don't save session to disk | `--print` only | [cli-ref][cli-ref] |

**Analysis**: [CC-session-lifecycle-analysis.md](../sessions/CC-session-lifecycle-analysis.md)

## Output & Format Flags

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `-p`, `--print` | Non-interactive mode — print response and exit | — | [cli-ref][cli-ref] |
| `--output-format` | Output format: `text` (default), `json`, `stream-json` | `--print` only | [cli-ref][cli-ref] |
| `--input-format` | Input format: `text` (default), `stream-json` | `--print` only | [cli-ref][cli-ref] |
| `--include-partial-messages` | Include partial streaming events in output | `--print` + `--output-format stream-json` | [cli-ref][cli-ref] |
| `--include-hook-events` | Include hook lifecycle events in output stream | `--output-format stream-json` | [cli-ref][cli-ref] |
| `--replay-user-messages` | Echo user messages from stdin back on stdout | `--input-format stream-json` + `--output-format stream-json` | [cli-ref][cli-ref] |
| `--json-schema` | Validate final output against a JSON Schema | `--print` only | [structured-output][structured-output] |
| `--verbose` | Enable verbose logging, full turn-by-turn output | — | [cli-ref][cli-ref] |

**Analysis**: [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md), [CC-stream-json-protocol.md](CC-stream-json-protocol.md)

## Model & Execution Flags

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `--model` | Model alias (`sonnet`, `opus`) or full ID | — | [model-config][model-config] |
| `--effort` | Reasoning effort: `low`, `medium`, `high`, `max` (Opus 4.6 only) | Session-scoped, not persisted | [model-config][model-config] |
| `--fallback-model` | Auto-fallback model when primary is overloaded | `--print` only | [cli-ref][cli-ref] |
| `--max-turns` | Limit agentic turns; exits with error when reached | `--print` only | [cli-ref][cli-ref] |
| `--max-budget-usd` | Maximum dollar spend before stopping | `--print` only | [cli-ref][cli-ref] |
| `--betas` | Beta headers for API requests | API key users only | [cli-ref][cli-ref] |

**Analysis**: [CC-model-provider-configuration.md](CC-model-provider-configuration.md), [CC-fast-mode-analysis.md](CC-fast-mode-analysis.md), [CC-session-cost-analysis.md](../sessions/CC-session-cost-analysis.md)

## System Prompt Flags

`--system-prompt` and `--system-prompt-file` are mutually exclusive. Append flags can combine with either replacement flag. For most use cases, prefer append to preserve built-in capabilities.

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `--system-prompt` | Replace entire default system prompt | Mutually exclusive with `--system-prompt-file` | [cli-ref][cli-ref] |
| `--system-prompt-file` | Replace with file contents | Mutually exclusive with `--system-prompt` | [cli-ref][cli-ref] |
| `--append-system-prompt` | Append text to default prompt | — | [cli-ref][cli-ref] |
| `--append-system-prompt-file` | Append file contents to default prompt | — | [cli-ref][cli-ref] |
| `--exclude-dynamic-system-prompt-sections` | Move per-machine sections to first user message for better prompt-cache reuse | Ignored with `--system-prompt`/`--system-prompt-file` | [cli-ref][cli-ref] |

**Analysis**: [CC-prompt-caching-behavior.md](../context-memory/CC-prompt-caching-behavior.md)

## Security & Permissions Flags

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `--permission-mode` | Start in mode: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions` | Overrides `defaultMode` from settings | [permission-modes][permission-modes] |
| `--dangerously-skip-permissions` | Skip all permission prompts (alias for `--permission-mode bypassPermissions`) | — | [permission-modes][permission-modes] |
| `--allow-dangerously-skip-permissions` | Add `bypassPermissions` to Shift+Tab cycle without starting in it | — | [permission-modes][permission-modes] |
| `--enable-auto-mode` | Unlock auto mode in Shift+Tab cycle | Team/Enterprise/API plan + Sonnet 4.6 or Opus 4.6 | [auto-mode][auto-mode] |
| `--permission-prompt-tool` | MCP tool to handle permission prompts non-interactively | Non-interactive mode | [cli-ref][cli-ref] |
| `--allowedTools` | Tools that execute without permission prompts | [Permission rule syntax][perm-syntax] | [cli-ref][cli-ref] |
| `--disallowedTools` | Tools removed from model context entirely | — | [cli-ref][cli-ref] |
| `--tools` | Restrict available built-in tools (`""`, `"default"`, or tool names) | — | [cli-ref][cli-ref] |

**Analysis**: [CC-permissions-bypass-analysis.md](../sandboxing/CC-permissions-bypass-analysis.md), [CC-tools-inventory.md](CC-tools-inventory.md)

## Plugins & MCP Flags

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `--mcp-config` | Load MCP servers from JSON files or strings | Space-separated | [mcp][mcp] |
| `--strict-mcp-config` | Only use MCP servers from `--mcp-config`, ignore all others | — | [cli-ref][cli-ref] |
| `--plugin-dir` | Load plugins from directory (repeatable) | Session only | [cli-ref][cli-ref] |
| `--channels` | MCP server channel notifications to listen for | Research preview; requires Claude.ai auth | [channels][channels] |
| `--dangerously-load-development-channels` | Enable non-allowlisted channels for local dev | Prompts for confirmation | [channels-ref][channels-ref] |
| `--chrome` | Enable Chrome browser integration | — | [chrome][chrome] |
| `--no-chrome` | Disable Chrome browser integration | — | [chrome][chrome] |

**Analysis**: [CC-chrome-extension-analysis.md](../plugins-ecosystem/CC-chrome-extension-analysis.md), [CC-plugin-packaging-research.md](../plugins-ecosystem/CC-plugin-packaging-research.md), [CC-channels-analysis.md](../plugins-ecosystem/CC-channels-analysis.md)

## Agent & Worktree Flags

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `--agent` | Specify agent for the session (overrides `agent` setting) | — | [cli-ref][cli-ref] |
| `--agents` | Define custom subagents via JSON (same fields as frontmatter + `prompt`) | — | [sub-agents][sub-agents] |
| `--teammate-mode` | Agent team display: `auto` (default), `in-process`, `tmux` | — | [agent-teams][agent-teams] |
| `-w`, `--worktree` | Start in isolated git worktree (optional name) | — | [worktrees][worktrees] |
| `--tmux` | Create tmux session for worktree; `--tmux=classic` for traditional tmux | Requires `--worktree` | [cli-ref][cli-ref] |

**Analysis**: [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md), [CC-recursive-spawning-patterns.md](../agents-skills/CC-recursive-spawning-patterns.md)

## Remote & Cloud Flags

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `--remote` | Create new web session on claude.ai with task description | — | [web-sessions][web-sessions] |
| `--teleport` | Resume a web session in local terminal | — | [web-sessions][web-sessions] |
| `--remote-control`, `--rc` | Start interactive session with Remote Control enabled | Optional name argument | [remote-control][remote-control] |
| `--remote-control-session-name-prefix` | Prefix for auto-generated Remote Control session names | Defaults to hostname | [remote-control][remote-control] |

**Analysis**: [CC-cloud-sessions-analysis.md](../ci-remote/CC-cloud-sessions-analysis.md), [CC-remote-control-analysis.md](../ci-remote/CC-remote-control-analysis.md)

## Configuration Flags

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `--bare` | Minimal mode: skip hooks, plugins, MCP, auto memory, CLAUDE.md. Sets `CLAUDE_CODE_SIMPLE` | — | [bare-mode][bare-mode] |
| `--settings` | Load additional settings from JSON file or string | — | [cli-ref][cli-ref] |
| `--setting-sources` | Comma-separated sources to load: `user`, `project`, `local` | — | [cli-ref][cli-ref] |
| `--add-dir` | Grant file access to additional directories | Most `.claude/` config not discovered from these | [permissions][permissions] |
| `--disable-slash-commands` | Disable all skills and commands for session | — | [cli-ref][cli-ref] |

**Analysis**: [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md)

## Initialization Flags

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `--init` | Run initialization hooks and start interactive mode | — | [cli-ref][cli-ref] |
| `--init-only` | Run initialization hooks and exit (no session) | — | [cli-ref][cli-ref] |
| `--maintenance` | Run maintenance hooks and start interactive mode | — | [cli-ref][cli-ref] |

**Analysis**: [CC-hooks-system-analysis.md](CC-hooks-system-analysis.md)

## Debug & Diagnostics Flags

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `--debug` | Enable debug mode with optional category filter (e.g. `"api,hooks"`, `"!statsig,!file"`) | — | [cli-ref][cli-ref] |
| `--debug-file` | Write debug logs to file (implicitly enables debug) | Takes precedence over `CLAUDE_CODE_DEBUG_LOGS_DIR` | [cli-ref][cli-ref] |
| `-v`, `--version` | Print version number | — | [cli-ref][cli-ref] |

## IDE Flag

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `--ide` | Auto-connect to IDE if exactly one valid IDE is available | — | [cli-ref][cli-ref] |

**Analysis**: [CC-ide-integration-protocol.md](CC-ide-integration-protocol.md)

## File Resources Flag

| Flag | Description | Constraints | Source |
|---|---|---|---|
| `--file` | Download file resources at startup. Format: `file_id:relative_path` | Repeatable | [cli-ref][cli-ref] |

## Sources

| Source | Content |
|---|---|
| [CC CLI reference][cli-ref] | Authoritative flag and subcommand documentation |
| [CC settings][settings] | `settings.json` keys, permission rules |
| [CC env vars][env-vars] | Environment variables reference |
| [CC tools reference][tools-ref] | Built-in tool descriptions and permissions |
| `claude --help` (Opus 4.6, 2026-04-13) | Runtime flag listing (subset of full reference) |

[cli-ref]: https://code.claude.com/docs/en/cli-reference
[auth]: https://code.claude.com/docs/en/authentication
[auto-mode]: https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode
[permission-modes]: https://code.claude.com/docs/en/permission-modes
[perm-syntax]: https://code.claude.com/docs/en/settings#permission-rule-syntax
[permissions]: https://code.claude.com/docs/en/permissions#additional-directories-grant-file-access-not-configuration
[model-config]: https://code.claude.com/docs/en/model-config
[mcp]: https://code.claude.com/docs/en/mcp
[plugins-ref]: https://code.claude.com/docs/en/plugins-reference#cli-commands-reference
[channels]: https://code.claude.com/docs/en/channels
[channels-ref]: https://code.claude.com/docs/en/channels-reference#test-during-the-research-preview
[chrome]: https://code.claude.com/docs/en/chrome
[remote-control]: https://code.claude.com/docs/en/remote-control
[web-sessions]: https://code.claude.com/docs/en/claude-code-on-the-web
[sub-agents]: https://code.claude.com/docs/en/sub-agents
[agent-teams]: https://code.claude.com/docs/en/agent-teams
[worktrees]: https://code.claude.com/docs/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees
[bare-mode]: https://code.claude.com/docs/en/headless#start-faster-with-bare-mode
[structured-output]: https://code.claude.com/docs/en/agent-sdk/structured-outputs
[settings]: https://code.claude.com/docs/en/settings
[env-vars]: https://code.claude.com/docs/en/env-vars
[tools-ref]: https://code.claude.com/docs/en/tools-reference
