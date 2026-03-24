---
title: CC Channels — Push Events via Telegram, Discord, iMessage
source: https://code.claude.com/docs/en/channels, https://code.claude.com/docs/en/channels-reference
purpose: Analysis of Claude Code channels for pushing external events into running sessions via MCP server plugins.
created: 2026-03-24
updated: 2026-03-24
validated_links: 2026-03-24
---

**Status**: Research preview (v2.1.80+, allowlisted plugins only)

## What Channels Are

An MCP server that **pushes** events into a running CC session — Claude reacts while you're away from the terminal. Two-way: Claude reads the event and replies back through the same channel (e.g., Telegram message in, reply back in Telegram). Events only arrive while the session is open.

Unlike web sessions (fresh cloud sandbox) or Remote Control (you drive), channels let **external systems push into your existing local session**.

### Supported Channels (Research Preview)

| Channel | Setup | Auth | Platform |
|---------|-------|------|----------|
| **Telegram** | BotFather → token → `/telegram:configure <token>` | Bot token | Cross-platform |
| **Discord** | Developer Portal → bot → `/discord:configure <token>` | Bot token + Message Content Intent |  Cross-platform |
| **iMessage** | No token needed — reads `~/Library/Messages/chat.db` | Full Disk Access | macOS only |
| **fakechat** | Demo — localhost:8787 chat UI | None | Any |

All pre-built plugins require [Bun](https://bun.sh) runtime.

### How It Works

1. Install plugin: `/plugin install telegram@claude-plugins-official`
2. Configure credentials: `/telegram:configure <token>`
3. Restart with channel: `claude --channels plugin:telegram@claude-plugins-official`
4. Pair sender: send bot a message → get pairing code → `/telegram:access pair <code>`
5. Lock down: `/telegram:access policy allowlist`

### CLI Flags

```bash
# Enable specific channels
claude --channels plugin:telegram@claude-plugins-official

# Multiple channels (space-separated)
claude --channels plugin:telegram@claude-plugins-official plugin:discord@claude-plugins-official

# Test custom channels during development
claude --dangerously-load-development-channels server:my-webhook
```

### Security

- **Sender allowlist**: only paired/approved IDs can push messages; others silently dropped
- **Per-session opt-in**: `--channels` flag required each session; being in `.mcp.json` is not enough
- **Permission relay**: allowlisted senders can approve/deny tool use remotely (if channel declares capability)
- **Enterprise**: disabled by default on Team/Enterprise; admin enables via `channelsEnabled` managed setting

### Requirements

- Claude.ai login (Console/API key auth not supported)
- CC v2.1.80+
- Bun runtime for pre-built plugins
- Team/Enterprise: admin must enable `channelsEnabled`

### Key Limitations

- **Research preview** — `--channels` only accepts Anthropic-maintained allowlisted plugins
- **Session must be open** — events don't arrive when session is closed
- **No cloud support** — channels push into local sessions, not web sessions
- **Permission pauses** — if Claude hits a permission prompt while away, session pauses unless using `--dangerously-skip-permissions` or channel has permission relay

## How Channels Compare

| Feature | What it does | Direction |
|---------|-------------|-----------|
| **Channels** | External systems push events into running local session | Inbound push |
| [CC Web sessions](../ci-execution/CC-cloud-sessions-analysis.md) | Fresh cloud sandbox from GitHub | Outbound delegation |
| [Claude in Slack](https://code.claude.com/docs/en/slack) | `@Claude` mention spawns web session | Outbound delegation |
| [Standard MCP](CC-connectors-overview.md) | Claude queries on demand | Outbound pull |
| [Remote Control](../ci-execution/CC-remote-control-analysis.md) | You drive local session from web/mobile | Bidirectional steering |

## Use Cases

| Use Case | Fit | Rationale |
|----------|-----|-----------|
| Chat bridge (phone → local session) | Strong | Ask Claude from Telegram/Discord, reply comes back in same chat |
| CI/deploy webhook receiver | Strong | Build custom channel for CI events, Claude reacts with files already open |
| Autonomous loop steering from mobile | Moderate | Alternative to Remote Control — push instructions via Telegram |
| Always-on monitoring | Weak | Requires persistent terminal; web scheduled tasks are more reliable |

### Decision Rule

**Use channels when external systems need to push events into your already-running local session. Use Remote Control when you want to drive the session yourself. Use web sessions or scheduled tasks for work that should run without your machine.**

## References

- [CC Channels docs][cc-channels]
- [CC Channels reference (build your own)][cc-channels-ref]
- [Official plugins repo][plugins-repo]

[cc-channels]: https://code.claude.com/docs/en/channels
[cc-channels-ref]: https://code.claude.com/docs/en/channels-reference
[plugins-repo]: https://github.com/anthropics/claude-plugins-official
