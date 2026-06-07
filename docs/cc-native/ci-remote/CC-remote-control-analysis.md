---
title: CC Remote Control Analysis
source: https://code.claude.com/docs/en/remote-control
purpose: Analysis of Claude Code Remote Control for mobile monitoring of long-running CC sessions and cross-device session continuity.
created: 2026-03-07
updated: 2026-06-07
validated_links: 2026-06-07
---

**Status**: Research preview (all plans; off by default on Team/Enterprise until an admin enables the Remote Control toggle) ([source][cc-rc])

## What Remote Control Is

A feature that connects `claude.ai/code` or the Claude mobile app (iOS/Android) to a Claude Code session running locally ([source][cc-rc]). The local machine does all execution; the web/mobile interface is a window into that session. Not cloud execution — that's [Claude Code on the web](CC-cloud-sessions-analysis.md).

### Key Mechanics

- **Local execution**: Filesystem, MCP servers, tools, and project configuration stay on your machine ([source][cc-rc])
- **Multi-surface sync**: Conversation stays in sync across terminal, browser, and phone — messages can be sent from any surface interchangeably ([source][cc-rc])
- **Auto-reconnect**: If laptop sleeps or network drops, session reconnects automatically when machine comes back online ([source][cc-rc])
- **Outbound-only**: No inbound ports opened; local session polls Anthropic API over HTTPS. All traffic over TLS ([source][cc-sec])
- **One remote session per CC instance**: Each CC instance supports one remote connection ([source][cc-rc])

### Starting a Session

Three invocation modes ([source][cc-rc-start]):

```bash
# Server mode — process waits for remote connections; serves many sessions
claude remote-control
claude remote-control --name "My Project"
claude remote-control --sandbox  # Enable filesystem/network sandboxing

# Interactive mode — full local terminal session that is ALSO drivable remotely
claude --remote-control          # alias: --rc
claude --remote-control "My Project"

# From an existing session (carries over conversation history)
/remote-control                  # alias: /rc
```

In the [VS Code extension](https://code.claude.com/docs/en/vs-code), use `/remote-control` or `/rc` (requires CC v2.1.79+; no name arg or QR code).

Server mode flags ([source][cc-rc-start]):

| Flag | Description |
|---|---|
| `--name "My Project"` | Custom session title visible in claude.ai/code session list |
| `--spawn <mode>` | `same-dir` (default), `worktree` (isolated per session), `session` (single-session, rejects others) |
| `--capacity <N>` | Max concurrent sessions (default: 32; not with `--spawn=session`) |
| `--verbose` | Detailed connection and session logs |
| `--sandbox` / `--no-sandbox` | Enable/disable filesystem and network sandboxing (off by default) |

Press spacebar to show QR code for quick phone access. Press `w` to toggle between `same-dir` and `worktree` spawn modes at runtime. Session URL is displayed for browser access.

To download the Claude mobile app, use the `/mobile` slash command inside Claude Code — it displays a QR code for iOS/Android ([source][cc-rc-guide]).

### Connecting from Another Device

1. Open session URL directly in browser
2. Scan QR code with Claude mobile app
3. Find session by name in `claude.ai/code` session list (computer icon + green dot = online)

### Configuration

Enable for all sessions automatically:

```text
/config → "Enable Remote Control for all sessions" → true
```

### Mobile Push Notifications

When Remote Control is active, Claude can push to your phone — typically when a long-running task finishes or it needs a decision; you can also request one in-prompt (e.g. "notify me when the tests finish"). Enable via `/config` → **Push when Claude decides** (Desktop: Settings → Claude Code). Requires CC **v2.1.110+** and the Claude mobile app signed into the same account ([source][cc-rc]).

### Requirements

| Requirement | Detail | Source |
|---|---|---|
| **Plan** | Pro, Max, Team, Enterprise. API-key-only billing does not qualify | [requirements][cc-rc-req] |
| **Auth** | OAuth via `/login` — API keys and `setup-token` long-lived tokens are not supported | [requirements][cc-rc-req], [troubleshooting][cc-rc-troubleshoot] |
| **Team/Enterprise admin** | Admin must enable Remote Control toggle at `claude.ai/admin-settings/claude-code` (off by default) | [requirements][cc-rc-req], [troubleshooting][cc-rc-troubleshoot] |
| **Managed policy** | IT admins can disable Remote Control per-device via `disableRemoteControl` in [managed settings][cc-settings-files], independent of the org-wide toggle | [troubleshooting][cc-rc-troubleshoot] |
| **Version** | CC v2.1.51+ (VS Code `/remote-control` needs v2.1.79+; push notifications need v2.1.110+) | [rc][cc-rc] |
| **Workspace trust** | Must have run `claude` in the project dir at least once to accept the trust dialog | [requirements][cc-rc-req] |

### Network Allowlist (what to permit)

All Remote Control traffic is **outbound HTTPS on port 443** — no inbound ports. In a firewall/proxy environment, do **not** block these ([network config][cc-netcfg], [troubleshooting][cc-rc-troubleshoot]):

| Host | Purpose | Required for RC |
|---|---|---|
| `api.anthropic.com` | RC registration, polling, short-lived credentials; Claude API; WebFetch domain safety check | **Yes** |
| `claude.ai` | claude.ai OAuth login + the web/mobile client side of the session | **Yes** |
| `platform.claude.com` | Anthropic Console account auth | Only if using Console auth |
| operational telemetry (rides `api.anthropic.com`) | The RC **eligibility check** goes through this path | **Effectively yes** — suppressing it breaks RC (see blockers below) |
| `downloads.claude.ai`, `raw.githubusercontent.com`, Sentry, `bridge.claudeusercontent.com` | Updates, release notes, error reporting, Chrome-extension bridge | Optional — safe to block without breaking RC |

Proxy notes ([network config][cc-netcfg]): `HTTPS_PROXY`/`NO_PROXY` respected; **SOCKS unsupported**; TLS-inspection proxies work if the root CA is trusted (`NODE_EXTRA_CA_CERTS`); mTLS via `CLAUDE_CODE_CLIENT_CERT`/`CLAUDE_CODE_CLIENT_KEY`. Under Bedrock/Vertex/Foundry, model traffic leaves `api.anthropic.com` — but RC itself is unavailable there anyway (see blockers).

### Environment Variable Blockers

These env vars **break the Remote Control eligibility check** and cause "Remote Control is not yet enabled for your account" ([source][cc-rc-troubleshoot]):

| Variable | Effect on Remote Control |
|---|---|
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | **Blocks** — blanket flag that includes telemetry suppression; eligibility check goes through this path |
| `DISABLE_TELEMETRY` | **Blocks** — eligibility check fails when telemetry is suppressed |
| `CLAUDE_CODE_USE_BEDROCK` | **Blocks** — Remote Control requires claude.ai auth, not third-party providers |
| `CLAUDE_CODE_USE_VERTEX` | **Blocks** — same reason |
| `CLAUDE_CODE_USE_FOUNDRY` | **Blocks** — same reason |

**Workaround**: Replace `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` with the individual flags that don't block Remote Control:

```json
{
  "env": {
    "DISABLE_AUTOUPDATER": "1",
    "DISABLE_FEEDBACK_COMMAND": "1",
    "DISABLE_ERROR_REPORTING": "1"
  }
}
```

This preserves most traffic reduction while keeping Remote Control functional. Omit `DISABLE_TELEMETRY` — that's the specific flag that blocks the eligibility check.

**Per-project override**: If `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` is set globally in `~/.claude/settings.json`, override it at project level in `.claude/settings.local.json` (gitignored):

```json
{
  "env": {
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "",
    "DISABLE_AUTOUPDATER": "1",
    "DISABLE_FEEDBACK_COMMAND": "1",
    "DISABLE_ERROR_REPORTING": "1"
  }
}
```

Project-level env vars override user-level per [settings scope precedence][cc-settings].

Source: [CC settings — configuration scopes][cc-settings]

Cross-ref: [CC-env-vars-reference.md](../configuration/CC-env-vars-reference.md) for full variable definitions

### Limitations

1. **One remote session at a time** per CC instance ([source][cc-rc])
2. **Terminal must stay open** — closing terminal or stopping `claude` ends the session ([source][cc-rc])
3. **~10 minute network timeout** — extended outage causes session exit ([source][cc-rc])
4. **No inbound connections** — security model is outbound HTTPS polling only ([source][cc-sec])
5. **Ultraplan disconnects RC** — starting an ultraplan session drops any active Remote Control session; both occupy the claude.ai/code interface and only one can connect ([source][cc-rc])

### Remote Control vs Claude Code on the Web

| Aspect | Remote Control | Claude Code on the Web |
| ------ | -------------- | ---------------------- |
| Execution | Your machine | Anthropic-managed cloud VM |
| Local MCP/tools | Available | Not available |
| Project config | Full local config | Needs setup script |
| Use case | Continue local work from another device | Start tasks without local setup |
| Offline survival | Reconnects after sleep | Runs independently of your machine |

## Applicability to Common Workflows

| Workflow | Fit | Rationale |
| -------- | --- | --------- |
| Monitor autonomous development loop from phone | Strong | Watch iterations progress without staying at desk; send corrections if stuck |
| Monitor CC teams runs | Strong | Same — observe parallel agent coordination remotely |
| Interactive development (debugging, iteration) | Moderate | Useful for remote coding sessions |
| Batch processes | Weak | No need for interactive monitoring on non-interactive runs |
| Headless `claude -p` invocations | None | Print mode exits on completion; no persistent session to connect to |

### Decision Rule

**Use Remote Control to monitor long-running interactive sessions (autonomous loops, teams mode) from mobile. Not useful for headless/print-mode invocations.**

### Potential Integration

```makefile
# Example (NOT implemented — YAGNI until measured need)
loop_remote:
    cd $(PROJECT_DIR) && claude remote-control --name "Loop: $(shell date +%Y%m%d-%H%M)"
```

**Recommendation**: No project-level integration needed. Remote Control is a per-developer workflow preference. Developers can run `claude remote-control` manually when they want mobile access. Document the pattern in a usage guide if demand arises.

## References

- [CC Remote Control docs][cc-rc]
- [CC Claude Code on the Web docs][cc-web]
- [CC CLI Reference][cc-cli]
- [CC Security][cc-sec]

[cc-rc]: https://code.claude.com/docs/en/remote-control
[cc-rc-req]: https://code.claude.com/docs/en/remote-control#requirements
[cc-rc-start]: https://code.claude.com/docs/en/remote-control#start-a-remote-control-session
[cc-rc-troubleshoot]: https://code.claude.com/docs/en/remote-control#troubleshooting
[cc-netcfg]: https://code.claude.com/docs/en/network-config
[cc-settings-files]: https://code.claude.com/docs/en/settings#settings-files
[cc-rc-guide]: https://claudefa.st/blog/guide/development/remote-control-guide "Claude Code Remote Control: Complete Setup Guide"
[cc-web]: https://code.claude.com/docs/en/claude-code-on-the-web
[cc-cli]: https://code.claude.com/docs/en/cli-reference
[cc-sec]: https://code.claude.com/docs/en/security
[cc-settings]: https://code.claude.com/docs/en/settings#configuration-scopes
