---
title: CC Tools Inventory
purpose: Point-in-time snapshot of all CC built-in tools, slash commands, and configuration surfaces with permission requirements and categories.
created: 2026-03-27
updated: 2026-04-05
validated_links: 2026-04-05
---

**Status**: Adopt

## What It Is

CC 2.1.83 ships 28 built-in tools. This is a categorized snapshot linking to the [official tools reference][tools-ref] as the authoritative source. Check that page for current descriptions — tools are added across CC releases.

## Tool Inventory (CC 2.1.83, 2026-03-27)

### File Operations

| Tool | Permission | Purpose |
|---|---|---|
| `Read` | No | Read file contents (text, images, PDFs, notebooks) |
| `Edit` | Yes | Targeted edits to files |
| `Write` | Yes | Create or overwrite files |
| `NotebookEdit` | Yes | Modify Jupyter notebook cells |
| `Glob` | No | Find files by pattern |
| `Grep` | No | Search file contents by regex |

### Execution

| Tool | Permission | Purpose |
|---|---|---|
| `Bash` | Yes | Execute shell commands |
| `PowerShell` | Yes | Execute PowerShell (Windows, opt-in preview) |

### Agent & Task Management

| Tool | Permission | Purpose |
|---|---|---|
| `Agent` | No | Spawn subagent with own context window |
| `TaskCreate` | No | Create task in task list |
| `TaskGet` | No | Get task details |
| `TaskList` | No | List all tasks |
| `TaskUpdate` | No | Update task status/dependencies |
| `TaskStop` | No | Kill background task |
| `TaskOutput` | No | (Deprecated) Read background task output — use `Read` instead |
| `TodoWrite` | No | Session task checklist (non-interactive / Agent SDK) |

### Planning & Navigation

| Tool | Permission | Purpose |
|---|---|---|
| `EnterPlanMode` | No | Switch to plan mode |
| `ExitPlanMode` | Yes | Present plan for approval |
| `EnterWorktree` | No | Create isolated git worktree |
| `ExitWorktree` | No | Exit worktree session |
| `LSP` | No | Code intelligence via language servers |

### Scheduling

| Tool | Permission | Purpose |
|---|---|---|
| `CronCreate` | No | Schedule recurring prompt in session |
| `CronDelete` | No | Cancel scheduled task |
| `CronList` | No | List scheduled tasks |

### External & MCP

| Tool | Permission | Purpose |
|---|---|---|
| `WebFetch` | Yes | Fetch URL content |
| `WebSearch` | Yes | Web search |
| `ListMcpResourcesTool` | No | List MCP server resources |
| `ReadMcpResourceTool` | No | Read MCP resource by URI |
| `ToolSearch` | No | Search/load deferred tools (MCP tool search) |

### Other

| Tool | Permission | Purpose |
|---|---|---|
| `AskUserQuestion` | No | Multiple-choice questions for requirements |
| `Skill` | Yes | Execute a skill in main conversation |

## Permission Model

- **"No"** = tool runs without user approval
- **"Yes"** = requires permission (configurable via `allow`/`ask`/`deny` rules in [settings][settings])
- Permission rules follow `Tool` or `Tool(specifier)` syntax — see [permission rule syntax][permissions]

## Slash Commands (CC 2.1.87, Binary String Extraction)

Commands extracted via `grep -oP` from CLI binary. **Documented** commands are linked; **undocumented** are marked.

### Documented

| Command | Purpose | Source |
|---|---|---|
| `/clear` | Clear conversation | [cli-ref][cli-ref] |
| `/commit` | Commit staged changes | [cli-ref][cli-ref] |
| `/config` | Open interactive config panel (`.claude.json` prefs) | [cli-ref][cli-ref] |
| `/exit` | Exit session | [cli-ref][cli-ref] |
| `/fast` | Toggle fast mode | [fast-mode][fast-mode] |
| `/feedback` | Submit feedback | [cli-ref][cli-ref] |
| `/login` | Authenticate | [cli-ref][cli-ref] |
| `/logout` | Sign out | [cli-ref][cli-ref] |
| `/loop` | Run on recurring interval | [cli-ref][cli-ref] |
| `/mcp` | Manage MCP servers | [mcp-docs][mcp-docs] |
| `/model` | Switch model | [model-config][model-config] |
| `/review-pr` | Review pull request | [cli-ref][cli-ref] |
| `/schedule` | Manage scheduled remote agents | [remote-control][remote-control] |
| `/status` | Show session status | [cli-ref][cli-ref] |

### Undocumented (String Extraction)

| Command | Observed Behavior | Notes |
|---|---|---|
| `/settings` | Routes to `update-config` skill (conversational, modifies `settings.json`) | **Not** an alias for `/config`; confirmed CC 2.1.87 |
| `/update-config` | Same skill as `/settings`, direct invocation | Asks "what would you like to configure?" |
| `/bash` | Unknown | String extraction, CC 2.1.87 |
| `/btw` | Side-question during task ([btw-gist][btw-gist]) | String extraction; community-documented |
| `/chrome` | Chrome extension related | String extraction, CC 2.1.87 |
| `/commit-push-pr` | Combined commit+push+PR workflow | String extraction, CC 2.1.87 |
| `/issue` | Create/reference GitHub issue | String extraction, CC 2.1.87 |
| `/remote-control` | Remote session management | String extraction, CC 2.1.87 |
| `/ultrareview` | Unknown — enhanced review? | String extraction, CC 2.1.87 |

## Configuration Surface (CC 2.1.87)

CC uses **three distinct configuration layers**. This was confirmed by cross-referencing the CLI binary, extension schema, and interactive `/config` panel.

### Layer 1: `.claude.json` — Interactive Preferences

Written by `/config` panel and UI interactions. Located at `~/.claude/.claude.json` or `.claude/.claude.json` per-project.

| Key | Type | `/config` Label | Source |
|---|---|---|---|
| `fastMode` | boolean | Fast mode (Opus 4.6 only) | `/config` panel observation |
| `respectGitignore` | boolean | Respect .gitignore in file picker | `/config` panel observation |
| `theme` | string | Theme | `/config` panel observation |
| `editorMode` | string | (not shown) | File observation |
| `diffTool` | string | (not shown) | File observation |
| `fileCheckpointingEnabled` | boolean | Rewind code (checkpoints) | `/config` panel observation |
| `terminalProgressBarEnabled` | boolean | Terminal progress bar | `/config` panel observation |
| `preferredNotifChannel` | string | Notifications | `/config` panel observation |
| `installMethod` | string | (not shown) | File observation |
| `autoInstallIdeExtension` | boolean | (not shown) | File observation |
| `claudeInChromeDefaultEnabled` | boolean | (not shown) | File observation |

**Not documented** in any first-party page. No dedicated reference exists.

### Layer 2: `settings.json` — Declarative Behavior Config

80+ keys for permissions, hooks, plugins, model, env, statusLine, etc. Documented at [settings][settings]. Written by `/settings` (update-config skill) or manually.

Cross-ref: [CC-env-vars-reference.md](CC-env-vars-reference.md), [CC-hooks-system-analysis.md](CC-hooks-system-analysis.md)

### Layer 3: `claudeCode.*` — VS Code Extension Settings

13 IDE-only settings in VS Code `settings.json`. Control how the extension **hosts** Claude, not how Claude **behaves**. Documented at [vs-code][vs-code].

| Setting | Purpose |
|---|---|
| `claudeCode.useTerminal` | Terminal vs native UI |
| `claudeCode.autosave` | Auto-save before read/write |
| `claudeCode.preferredLocation` | Default panel location |
| `claudeCode.initialPermissionMode` | Default permission mode |
| `claudeCode.allowDangerouslySkipPermissions` | Bypass mode |
| `claudeCode.environmentVariables` | Env vars for launch |
| `claudeCode.respectGitIgnore` | File picker gitignore |
| `claudeCode.disableLoginPrompt` | Suppress auth prompts |
| `claudeCode.useCtrlEnterToSend` | Send key behavior |
| `claudeCode.enableNewConversationShortcut` | Cmd+N shortcut |
| `claudeCode.hideOnboarding` | Hide onboarding |
| `claudeCode.claudeProcessWrapper` | Custom launcher |
| `claudeCode.usePythonEnvironment` | Python env |

### Overlap Between Layers

| Key | `.claude.json` | `settings.json` | `claudeCode.*` |
|---|---|---|---|
| `fastMode` | Yes | Yes | No |
| `respectGitignore` | Yes | Yes | Yes (`claudeCode.respectGitIgnore`) |

Precedence unclear. Behavior observed: `/config` panel writes to `.claude.json`; `settings.json` keys may override at runtime.

Cross-ref: [CC-binary-architecture.md](CC-binary-architecture.md)

## Internal and Feature-Gated Tools (Leak-Derived)

The following tools appear in the `@anthropic-ai/claude-code@2.1.88` npm sourcemap exposure (2026-03-31) but are not present in the public tool registry. Categorized by [CLAURST][claurst] analysis. **Unverified — Anthropic has not confirmed these tools.**

### Internal-Only Tools (`USER_TYPE === 'ant'`)

| Tool | Purpose | Gate |
|------|---------|------|
| `ConfigTool` | Modify settings programmatically | `ant` user type |
| `TungstenTool` | Advanced features (undocumented) | `ant` user type |
| `SuggestBackgroundPRTool` | Suggest background pull requests | `ant` user type |

### Feature-Gated Tools

| Tool | Purpose | Feature Gate |
|------|---------|-------------|
| `BriefTool` | Upload/summarize files to claude.ai | — |
| `SendMessageTool` | Inter-agent messaging (UDS Inbox) | `COORDINATOR_MODE` |
| `ListPeersTool` | Discover active CC sessions | `COORDINATOR_MODE` |
| `TeamCreateTool` | Create agent team | `tengu_amber_flint` |
| `TeamDeleteTool` | Delete agent team | `tengu_amber_flint` |
| `MonitorTool` | Monitor MCP servers | — |
| `WorkflowTool` | Execute workflow scripts | `WORKFLOW_SCRIPTS` |
| `SleepTool` | Async delays | — |
| `SnipTool` | History snippet extraction | `HISTORY_SNIP` |
| `McpAuthTool` | MCP server authentication | — |
| `SyntheticOutputTool` | Structured output via dynamic JSON schemas | — |
| `VerifyPlanExecutionTool` | Verify plan execution | `CLAUDE_CODE_VERIFY_PLAN` |
| `CtxInspectTool` | Context window inspection | `CONTEXT_COLLAPSE` |
| `TerminalCaptureTool` | Terminal panel capture | `TERMINAL_PANEL` |
| `REPLTool` | Interactive VM shell | `--bare` mode |

### Kairos-Exclusive Tools (Unreleased)

| Tool | Purpose | Feature Gate |
|------|---------|-------------|
| `SendUserFile` | Push files to user devices | `KAIROS` |
| `PushNotification` | Send push notifications | `KAIROS` |
| `SubscribePR` | Monitor and review PRs autonomously | `KAIROS` |

### Compile-Time Feature Flags

| Flag | Gates |
|------|-------|
| `PROACTIVE` / `KAIROS` | Always-on assistant mode |
| `KAIROS_BRIEF` | Brief command for concise output |
| `BRIDGE_MODE` | Remote control via claude.ai |
| `DAEMON` | Background daemon mode |
| `VOICE_MODE` | Voice input |
| `WORKFLOW_SCRIPTS` | Workflow automation |
| `COORDINATOR_MODE` | Multi-agent orchestration |
| `TRANSCRIPT_CLASSIFIER` | AFK mode (ML auto-approval) |
| `BUDDY` | Companion pet system |
| `NATIVE_CLIENT_ATTESTATION` | Client authenticity verification |
| `HISTORY_SNIP` | History snipping |
| `EXPERIMENTAL_SKILL_SEARCH` | Skill discovery |

Runtime feature gating uses GrowthBook with `tengu_`-prefixed flags and `getFeatureValue_CACHED_MAY_BE_STALE()` to avoid blocking the main loop.

Cross-ref: [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md) — UDS Inbox and Coordinator Mode; [CC-community-reimplementations-landscape.md](../../cc-community/CC-community-reimplementations-landscape.md) — CLAURST full tool registry source

## Cross-References

- [CC-bash-mode-analysis.md](CC-bash-mode-analysis.md) — Bash tool and `!` mode deep-dive
- [CC-hooks-system-analysis.md](CC-hooks-system-analysis.md) — PreToolUse/PostToolUse hook events
- [CC-env-vars-reference.md](CC-env-vars-reference.md) — `BASH_DEFAULT_TIMEOUT_MS`, `BASH_MAX_OUTPUT_LENGTH`
- [CC-binary-architecture.md](CC-binary-architecture.md) — Binary analysis methodology
- [CC RE landscape](../../cc-community/CC-reverse-engineering-landscape.md) — Community RE tools

## Sources

| Source | Content |
|---|---|
| [CC tools reference][tools-ref] | Authoritative tool list, descriptions, permission requirements |
| [CC CLI reference][cli-ref] | Official slash command documentation |
| [CC settings — permissions][permissions] | Permission rule syntax and tool-specific patterns |
| [CC VS Code docs][vs-code] | Extension settings (`claudeCode.*`) |
| CC 2.1.83, Codespaces, 2026-03-27 | Tool inventory snapshot version |
| CC 2.1.87 CLI binary string extraction, 2026-03-29 | Slash commands, config keys, undocumented commands |
| CC 2.1.87 `/config` panel observation, 2026-03-29 | `.claude.json` key inventory |
| [ZhangHanDong /btw gist][btw-gist] | `/btw` command analysis |
| [CLAURST README][claurst] | Internal/gated tool registry, feature flags |

[tools-ref]: https://code.claude.com/docs/en/tools-reference
[cli-ref]: https://code.claude.com/docs/en/cli-reference
[settings]: https://code.claude.com/docs/en/settings
[permissions]: https://code.claude.com/docs/en/permissions#tool-specific-permission-rules
[vs-code]: https://code.claude.com/docs/en/vs-code
[fast-mode]: https://code.claude.com/docs/en/fast-mode
[mcp-docs]: https://code.claude.com/docs/en/mcp
[model-config]: https://code.claude.com/docs/en/model-config
[remote-control]: https://code.claude.com/docs/en/remote-control
[btw-gist]: https://gist.github.com/ZhangHanDong
[claurst]: https://github.com/Kuberwastaken/claude-code
