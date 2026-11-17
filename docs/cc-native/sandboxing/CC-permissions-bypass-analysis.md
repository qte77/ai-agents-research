---
title: CC Permissions Bypass Analysis
source: https://code.claude.com/docs/en/settings, https://code.claude.com/docs/en/security
purpose: Analysis of --dangerously-skip-permissions flag, permission modes, team inheritance, and safer alternatives for headless/CI execution.
created: 2026-03-17
updated: 2026-11-17
status: research
---

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

## The Six Permission Modes

Six modes per the [permission-modes docs][cc-modes] (checked 2026-11-15); this table had five before `auto` was added.

| Mode | Behavior | Risk |
|---|---|---|
| **Default** | Asks for everything | Lowest -- blocks on every action |
| **`acceptEdits`** | Auto-approves file edits, asks for bash/network | Low |
| **`plan`** | Requires plan approval before implementation | Low |
| **`auto`** | Runs everything, with background safety checks by a classifier | Medium -- see [the auto-mode error rates](../../sdlc-lcm/agentic-ai-vulnerability-landscape.md#guardrail-layers-a-comparison) |
| **`dontAsk`** | Auto-approves everything matching `settings.json` allowlist | Medium -- granular control |
| **`bypassPermissions`** | Auto-approves ALL actions | Highest -- no guardrails |

### Deny instead of prompting (v2.1.319)

For unattended runs, the [permissions docs][cc-permissions] add a settings key: "To deny calls that would wait on a permission prompt, so an unattended session keeps working, set `permissions.denyInsteadOfPrompting` to `true` in your user or managed settings. `dontAsk` is a permission mode of its own, while this key works with the permission mode you're in." Per the [changelog][cc-changelog] (2.1.319), it applies "in terminal sessions, subagents and teammates." (Checked 2026-11-15.)

## Safer Alternative: `settings.json` Allowlists

The `dontAsk` mode with explicit allowlists gives ~90% of the speed without
the risk:

```json
{
  "permissions": {
    "allow": [
      "Bash(make test)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(uv run pytest *)",
      "Write",
      "Edit"
    ]
  }
}
```

This auto-approves listed patterns while still prompting for unlisted actions
(e.g., network requests, MCP tool calls). Name the subcommand before the `*`:
`Bash(git *)` or `Bash(make *)` would approve every git or make invocation, including
injected options such as `git -c core.fsmonitor=<script> …`, and Claude Code warns at
startup about allow rules with a `*` before the subcommand
([permissions docs](https://code.claude.com/docs/en/permissions#wildcard-patterns)).

### Permission behaviour changes in v2.1.321–325

Changelog entries unless marked.

- **`PreToolUse` allow, then a failing permission check (v2.1.323).** If a tool's permission check errors after a `PreToolUse` hook returned "allow", the call is decided as if no hook had answered.
- **Bash checks (v2.1.321, v2.1.323).** `cp` and `mv` spelled by a path such as `/bin/cp` get the same path checks as bare `cp`/`mv` (v2.1.321). Some commands that could run differently from how they were checked now ask (v2.1.323). A start-up warning flags Bash allow rules with a `*` in a variable's value, such as `Bash(PORT=* npm run dev)` (v2.1.323).
- **Scheduled skills (v2.1.325).** Scheduled tasks and `/loop` ask before running a skill that declares `allowed-tools` or hooks; `Skill(name)` in `permissions.allow` runs it unattended. "Always allow" in Desktop, IDE and SDK hosts offers a rule alone only when saving it would allow that command again, so a scheduled task that relied on one can now wait for you.
- **Asks added (v2.1.323).** `/security-review` asks before Claude runs it; skills' inline git commands stop in bare-repository worktrees and similar folders until allowed (outside auto mode and bypass); artifact updates ask first, even under an allow rule, when people outside the organization can see the artifact or Claude cannot check who can.
- **Mod tool calls (v2.1.321).** A mod's own `$.tool.call` and `$.mcp.call` raise no prompt, even under `ask` rules or in `dontAsk` and `-p` runs; deny rules and organization policy still apply.
- **Managed `policyHelper` (v2.1.323).** No longer takes environment variables from user or `--settings` files; set them in managed `env` or the launching shell.
- **Untrusted workspaces (v2.1.323).** Under `--trust-workspace false` on self-hosted runners and in VS Code untrusted folders, repository settings can no longer disable your hooks or turn plugins on or off.

## Auto Mode Hard-Deny Rules (v2.1.136)

`settings.autoMode.hard_deny` accepts the same rule syntax as `permissions.deny` but for the auto mode classifier specifically. Rules listed here block unconditionally regardless of user intent or allow exceptions — they cannot be overridden by an `allow` entry or a user confirmation.

```json
{
  "autoMode": {
    "hard_deny": [
      "Bash(rm -rf *)",
      "WebFetch(domain:internal.corp)"
    ]
  }
}
```

Use this for absolute red lines (data exfiltration paths, destructive commands) that should never be approved even in auto mode. Distinct from `permissions.deny` which governs the interactive permission prompt system.

Source: CHANGELOG v2.1.136

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
| [CC CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) | v2.1.321–325 permission entries (accessed 2026-11-17) |

## See Also

- [CC-cli-reference.md](../configuration/CC-cli-reference.md) — canonical flag definitions (`--dangerously-skip-permissions`, `--permission-mode`, `--allowedTools`)
- [CC-web-auth-setup-analysis.md](../ci-remote/CC-web-auth-setup-analysis.md) — authentication methods and API key setup for headless/CI
- [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md) — `--bare` auth breakage, stream-json pitfalls

[cc-permissions]: https://code.claude.com/docs/en/permissions
[cc-changelog]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
[cc-modes]: https://code.claude.com/docs/en/permission-modes
