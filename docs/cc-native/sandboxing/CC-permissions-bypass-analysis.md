---
title: CC Permissions Bypass Analysis
source: https://code.claude.com/docs/en/settings, https://code.claude.com/docs/en/security
purpose: Analysis of --dangerously-skip-permissions flag, permission modes, team inheritance, and safer alternatives for headless/CI execution.
created: 2026-03-17
updated: 2026-03-17
---

**Status**: Research (informational)

## What `--dangerously-skip-permissions` Does

Bypasses **all** permission checks -- file edits, bash commands, network
requests, MCP tools, subagent spawning. Every action auto-approves without
confirmation.

```bash
claude --dangerously-skip-permissions
# Combined with print mode (standard headless pattern):
claude --dangerously-skip-permissions -p "your prompt"
```

This is the most common autonomous usage: CI/CD pipelines, Ralph-style loops,
GitHub Actions. The flag removes all interactive prompts that would block
non-interactive mode.

## Permission Inheritance in Teams

If the lead is run with `--dangerously-skip-permissions`, **all teammates also
bypass permission checks**. Individual teammate modes can be adjusted after
spawning, but not at spawn time.

```text
Lead (--dangerously-skip-permissions)
  |-- Teammate A (inherits bypass)
  |-- Teammate B (inherits bypass)
  |-- Teammate C (inherits bypass -- can be changed post-spawn)
```

See [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md)
for team architecture details.

## The 5 Permission Modes

| Mode | Behavior | Risk |
|---|---|---|
| **Default** | Asks for everything | Lowest -- blocks on every action |
| **`acceptEdits`** | Auto-approves file edits, asks for bash/network | Low |
| **`plan`** | Requires plan approval before implementation | Low |
| **`dontAsk`** | Auto-approves everything matching `settings.json` allowlist | Medium -- granular control |
| **`bypassPermissions`** | Auto-approves ALL actions | Highest -- no guardrails |

## Safer Alternative: `settings.json` Allowlists

The `dontAsk` mode with explicit allowlists gives ~90% of the speed without
the risk:

```json
{
  "permissions": {
    "allow": [
      "Bash(make *)",
      "Bash(git *)",
      "Bash(uv run *)",
      "Write",
      "Edit"
    ]
  }
}
```

This auto-approves listed patterns while still prompting for unlisted actions
(e.g., network requests, MCP tool calls).

## Disabling Organization-Wide

Server-managed settings can force-disable bypass mode:

```json
{
  "disableBypassPermissionsMode": "disable"
}
```

## Known Bugs

| Bug | Description | Status |
|---|---|---|
| [#29110](https://github.com/anthropics/claude-code/issues/29110) | `bypassPermissions` mode on spawned agents (via Task tool) is ineffective -- agents still can't use Write/Edit/Bash | Open (2026-03) |
| [#29064](https://github.com/anthropics/claude-code/issues/29064) | Teammates spawned with `mode: "plan"` get stuck in infinite plan-approval loops -- never exit plan mode | Open (2026-03) |

## Security Considerations

| Risk | Mitigation |
|---|---|
| Cascading destructive ops | Use in disposable environments (Docker, Codespaces) |
| Infinite resource loops | Set timeouts on `claude -p` calls |
| Credential exposure | Don't mount secrets; use `.env` deny rules |
| Unintended file deletion | Git commit before each iteration (Ralph pattern) |

## `dangerouslyDisableSandbox` vs `--dangerously-skip-permissions`

These are **separate mechanisms**:

- **`--dangerously-skip-permissions`** (CLI flag): Bypasses the permission
  prompt system -- all tool calls auto-approve.
- **`dangerouslyDisableSandbox`** (Bash tool parameter): Per-command escape
  hatch from the filesystem/network sandbox. Can be disabled via
  `sandbox.allowUnsandboxedCommands: false`.

The sandbox ([CC-sandboxing-analysis.md](CC-sandboxing-analysis.md)) enforces
OS-level filesystem and network isolation regardless of permission mode.
Bypassing permissions does not bypass the sandbox.

## Sources

| Source | Content |
|---|---|
| [Official settings docs](https://code.claude.com/docs/en/settings) | Permission modes, allowlists |
| [Official security docs](https://code.claude.com/docs/en/security) | Security model, sandbox separation |
| [#29110](https://github.com/anthropics/claude-code/issues/29110) | Bypass ineffective on Task tool agents |
| [#29064](https://github.com/anthropics/claude-code/issues/29064) | Plan mode infinite loop |

## See Also

- [CC-web-auth-setup-analysis.md](../ci-remote/CC-web-auth-setup-analysis.md) — authentication methods and API key setup for headless/CI
- [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md) — `--bare` auth breakage, stream-json pitfalls
