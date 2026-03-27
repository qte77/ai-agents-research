---
title: CC Tools Inventory
purpose: Point-in-time snapshot of all CC built-in tools with permission requirements and categories.
created: 2026-03-27
updated: 2026-03-27
validated_links: 2026-03-27
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

## Cross-References

- [CC-bash-mode-analysis.md](CC-bash-mode-analysis.md) — Bash tool and `!` mode deep-dive
- [CC-hooks-system-analysis.md](CC-hooks-system-analysis.md) — PreToolUse/PostToolUse hook events
- [CC-env-vars-reference.md](CC-env-vars-reference.md) — `BASH_DEFAULT_TIMEOUT_MS`, `BASH_MAX_OUTPUT_LENGTH`

## Sources

| Source | Content |
|---|---|
| [CC tools reference][tools-ref] | Authoritative tool list, descriptions, permission requirements |
| [CC settings — permissions][permissions] | Permission rule syntax and tool-specific patterns |
| CC 2.1.83, Codespaces, 2026-03-27 | Version this snapshot was taken from |

[tools-ref]: https://code.claude.com/docs/en/tools-reference
[settings]: https://code.claude.com/docs/en/settings
[permissions]: https://code.claude.com/docs/en/permissions#tool-specific-permission-rules
