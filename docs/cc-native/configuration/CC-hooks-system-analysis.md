---
title: CC Hooks System Analysis
source: https://code.claude.com/docs/en/hooks
purpose: Analysis of Claude Code hooks system for automation, quality gates, and headless CC workflow integration.
created: 2026-03-07
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Generally available (v1.0.38+, extensively evolved through v2.1.218)

## What Hooks Are

Shell commands that execute in response to CC lifecycle events. Configured in
`.claude/settings.json` (project) or `~/.claude/settings.json` (user). Hooks
run locally, outside the sandbox, with full system access.

## Hook Events

| Event | Trigger | Since | Key Use Cases |
| ----- | ------- | ----- | ------------- |
| `PreToolUse` | Before any tool executes | v1.0.38 | Approval/denial gates, context injection via `additionalContext` (v2.1.9), input modification via `updatedInput` (v2.1.0) |
| `PostToolUse` | After any tool completes | v1.0.38 | Logging, trace collection, quality checks |
| `Stop` | Before session ends | v1.0.38 | Cleanup, final validation, re-prompting (Ralph Wiggum pattern) |
| `SessionStart` | Session begins | v1.0.62 | Repo maintenance, env setup; deferred for ~500ms faster startup (v2.1.47) |
| `Setup` | Repo initialization | v2.1.10 | One-time repo maintenance tasks |
| `PermissionRequest` | User prompted for permission | v2.0.45 | Automatic approval/denial policies (v2.0.54: processes 'always allow') |
| `SubagentStart` | Subagent spawns | v2.0.43 | Subagent monitoring; `agent_id`/`agent_transcript_path` fields added to `SubagentStop` hooks (v2.0.42), not `SubagentStart` |
| `TeammateIdle` | Agent Teams teammate becomes idle | v2.1.33 | Work redistribution, progress tracking |
| `TaskCompleted` | Agent Teams task finishes | v2.1.33 | Dependency unblocking, aggregation triggers |
| `WorktreeCreate` | Git worktree created | v2.1.50 | Environment setup for isolated agents |
| `WorktreeRemove` | Git worktree removed | v2.1.50 | Cleanup after agent completes |

## Hook Configuration

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "echo 'checking bash command'" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          { "type": "command", "command": "/path/to/trace-collector.sh" }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "make validate" }
        ]
      }
    ]
  }
}
```

### Key Configuration Fields

| Field | Description | Since |
| ----- | ----------- | ----- |
| `matcher` | Tool name filter (`*` for all, specific tool name) | v1.0.38 |
| `command` | Shell command to execute (string form — passed to shell) | v1.0.38 |
| `args` | `string[]` exec form — spawns the command directly without a shell, so path placeholders never need quoting. Mutually exclusive with `command`. | v2.1.139 |
| `continueOnBlock` | `PostToolUse` only. When `true`, a blocking hook result feeds the rejection reason back to Claude as context and continues the turn instead of halting. (Not found in current first-party hooks docs' schema as of 2026-07-23 — may be renamed/superseded; current docs describe the equivalent behavior via a hook's returned `decision: "block"`/`reason` and `hookSpecificOutput.additionalContext`. Verify the field name before relying on it.) | v2.1.139 |
| `once` | Runs once per session, then is removed. Only honored for hooks declared in **skill frontmatter**; ignored in settings files and agent frontmatter (see examples below, which predate this scoping). | v2.1.0 |
| `model` | Custom model for hook evaluation | v2.0.41 |
| `tool_use_id` | Available in hook input | v2.0.43 |

### Hook Return Values

Hooks can return JSON to influence CC behavior:

- **`additionalContext`**: Inject context into the agent's next turn (PreToolUse, v2.1.9)
- **`updatedInput`**: Modify tool input with ask decision (PreToolUse, v2.1.0)
- **Approval/denial**: PermissionRequest hooks can auto-approve or auto-deny (v2.0.45)

### HTTP Hooks (v2.1.63+)

Hooks support JSON POST/receive for external service integration. Enables
webhook-style automation without local scripts.

### Agent Frontmatter Hooks (v2.1.0)

Agent definitions (`.claude/agents/`) can include hooks in their frontmatter:
PreToolUse, PostToolUse, Stop. These are scoped to the agent's execution only.

## Applicability

| Use Case | Fit | Rationale |
| -------- | --- | --------- |
| **Trace collection** | Strong | `PostToolUse` hook sends tool events to an OTLP receiver; replaces manual artifact parsing |
| **Quality gates** | Strong | `Stop` hook runs a validation command before marking a task passed |
| **Permission automation** | Medium | `PermissionRequest` auto-approves known-safe operations for `claude -p` runs |
| **Agent Teams monitoring** | Medium | `TeammateIdle` / `TaskCompleted` hooks track parallel task progress |
| **Headless baseline collection** | Weak | Hooks run in interactive sessions; `claude -p` has limited hook support |

### Common Usage Patterns

Hooks are typically introduced through:

- Agent frontmatter hooks in `.claude/agents/` definitions
- `<user-prompt-submit-hook>` feedback in interactive sessions
- Dedicated hook scripts stored in the repository alongside other automation

### Potential Integration

Replace `your-validation-command` with the validation command for your project (e.g., `make validate`, `make quick_validate`, or a direct invocation of your linter/test runner):

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "your-validation-command" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "scripts/trace-hook.sh" }
        ]
      }
    ]
  }
}
```

**Recommendation**: Adopt `Stop` hook for validation gates first (low risk,
high value). The underlying OTel full-span-logging request that limited
`PostToolUse` trace collection
([#2090](https://github.com/anthropics/claude-code/issues/2090), duplicate
[#9584](https://github.com/anthropics/claude-code/issues/9584)) was closed by
Anthropic as not planned (2026-01-30) — treat artifact-based collection as the
durable approach rather than deferring pending an upstream fix.

## References

- [CC Hooks docs](https://code.claude.com/docs/en/hooks)
- [CC CHANGELOG.md](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) (version gates for hook events/fields)
- [CC Settings docs](https://code.claude.com/docs/en/settings)
- [CC Agent Teams docs](https://code.claude.com/docs/en/agent-teams) (TeammateIdle, TaskCompleted hooks)
- [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md) (Agent Teams analysis)
- [CC-ralph-enhancement-research.md](../agents-skills/CC-ralph-enhancement-research.md) (Stop hook pattern for autonomous loops)
