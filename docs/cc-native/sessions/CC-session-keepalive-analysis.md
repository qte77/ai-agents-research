---
title: CC Session Keepalive Across Environments
source: https://code.claude.com/docs/en/remote-control, https://code.claude.com/docs/en/claude-code-on-the-web, https://docs.github.com/en/codespaces/setting-your-user-preferences/setting-your-timeout-period-for-github-codespaces
purpose: Actionable techniques to keep CC sessions alive on local machines, in containers, and in GitHub Codespaces.
created: 2026-03-25
updated: 2026-03-25
validated_links: 2026-03-25
---

**Status**: Research (informational)

## Three Kill Vectors

| Vector | Cause | Environments |
|--------|-------|-------------|
| Host sleep | Machine suspends, WebSocket drops | Local (macOS/Linux/Windows) |
| WSL VM shutdown | WSL2 VM idles out (default 60s) | Windows/WSL |
| CC idle timeout | No user interaction during background tasks ([#32050][gh-32050]) | All |
| Platform timeout | Codespace stops after inactivity (default 30 min, max 4h) ([source][gh-idle-timeout]) | Codespace |

## macOS

**Sleep prevention:** CC already spawns `caffeinate -i -t 300` internally during
active sessions ([#21432][gh-21432]). This prevents idle sleep but respawns every
5 min. For lid-close survival, add a hook with `caffeinate -s`
([source][apple-caffeinate]) or use system-wide `pmset`
([source][apple-pmset]):
`sudo pmset -c sleep 0 displaysleep 0 standby 0 tcpkeepalive 1`

**Survive terminal close:** Run CC inside tmux — detach/reattach freely.

**Auto-restart on schedule:** `/loop` expires after 7 days (see
[CC-loop-cron-analysis.md](../configuration/CC-loop-cron-analysis.md)), OAuth
after ~2 days ([#36807][gh-36807]). Use `launchctl` to restart the tmux+CC
session daily ([source][apple-launchd]). Cron doesn't work — runs outside the
user login session, no keychain/auth access.

## Linux

**Prevent sleep** ([source][freedesktop-inhibit]):
`systemd-inhibit --what=idle --who="Claude Code" claude`

**Survive terminal close:** tmux or screen.

**Auto-restart:** `systemd --user` timer ([source][freedesktop-timer]) — same
auth benefit as macOS launchctl.

## Windows (WSL)

CC runs inside WSL2. Two extra kill vectors beyond host sleep:

**WSL VM shutdown** — WSL2 VM idles out after 60s by default. Configure in
`%USERPROFILE%\.wslconfig` ([source][wsl-config]):

```ini
[wsl2]
vmIdleTimeout=-1          # never auto-shutdown VM (-1 = disabled)

[general]
instanceIdleTimeout=-1    # never auto-shutdown distro instance
```

Note: `vmIdleTimeout` requires Windows 11 ([source][wsl-config]). Behavior on
Windows 10 is unreliable.

**Host sleep prevention** — from PowerShell (admin) ([source][ms-powercfg]):

```powershell
powercfg /change standby-timeout-ac 0
powercfg /change hibernate-timeout-ac 0
```

**Survive terminal close:** tmux inside WSL, or Windows Terminal with
the WSL profile (closing the tab doesn't kill the WSL instance if other
sessions remain).

## Docker Container

Containers don't sleep. Keep container alive independently of CC:

```yaml
services:
  claude:
    image: nezhar/claude-container:latest
    volumes:
      - ./:/workspace
      - ~/.claude:/home/node/.claude  # persist auth
    environment:
      ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
    command: sleep infinity
```

Run CC via `docker exec -it claude claude`. Container survives CC exits.

## GitHub Codespace / Devcontainer

**1. Set max timeout** — GitHub Settings > Codespaces > Default idle timeout > 240 minutes. Or per-codespace:

```bash
gh codespace create --idle-timeout 240m
```

**2. Terminal keepalive** — terminal output resets the idle timer ([source][gh-idle-timeout]). CC thinking does not count. Add to `devcontainer.json`:

```json
{
  "postStartCommand": "nohup bash -c 'while true; do echo \"keepalive $(date +%H:%M)\"; sleep 300; done' &"
}
```

**3. tmux inside Codespace** — CC survives terminal tab switches and browser reconnects.

**4. For truly unattended work** — don't fight the 4h hard limit. Use `claude --remote` (cloud VM, survives everything). See [CC-cloud-sessions-analysis.md](../ci-remote/CC-cloud-sessions-analysis.md).

**Auth persistence:** Store `ANTHROPIC_API_KEY` as a Codespace secret
([source][gh-codespace-secrets]) — injected on every start. OAuth requires
`claude /login` after rebuild.

## CC-Internal Keepalive (All Environments)

**`/loop` as keepalive:** `/loop 5m echo keepalive` — keeps session active.

**Remote Control + tmux:** Best combo for long-running interactive sessions. See [CC-remote-control-analysis.md](../ci-remote/CC-remote-control-analysis.md).

## Known Upstream Issues

| Issue | Summary | Status |
|-------|---------|--------|
| [#21432][gh-21432] | Built-in caffeinate has no disable setting | Open |
| [#32982][gh-32982] | RC idle TTL ignores keepalives | **Partially fixed** v2.1.74 |
| [#34868][gh-34868] | RC WebSocket drops every ~25 min | Open |
| [#32050][gh-32050] | Idle timeout during background tasks | Open |
| [#36807][gh-36807] | OAuth expires, needs interactive re-login | Open |

## See Also

- [CC-remote-control-analysis.md](../ci-remote/CC-remote-control-analysis.md)
- [CC-remote-access-landscape.md](../ci-remote/CC-remote-access-landscape.md) — Happy Coder, Omnara, DIY tmux+Tailscale
- [CC-cloud-sessions-analysis.md](../ci-remote/CC-cloud-sessions-analysis.md) — `claude --remote`
- [CC-web-scheduled-tasks-analysis.md](../ci-remote/CC-web-scheduled-tasks-analysis.md) — `/schedule`
- [CC-loop-cron-analysis.md](../configuration/CC-loop-cron-analysis.md) — `/loop` internals + lock file bug
- [CC-sandbox-codespaces-friction.md](../sandboxing/CC-sandbox-codespaces-friction.md)

## References

[gh-idle-timeout]: https://docs.github.com/en/codespaces/setting-your-user-preferences/setting-your-timeout-period-for-github-codespaces
[gh-codespace-secrets]: https://docs.github.com/en/codespaces/managing-your-codespaces/managing-your-account-specific-secrets-for-github-codespaces
[apple-caffeinate]: https://ss64.com/mac/caffeinate.html
[apple-pmset]: https://support.apple.com/guide/mac-help/set-sleep-and-wake-settings-mchle41a6ccd/mac
[apple-launchd]: https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html
[freedesktop-inhibit]: https://www.freedesktop.org/software/systemd/man/latest/systemd-inhibit.html
[freedesktop-timer]: https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
[wsl-config]: https://learn.microsoft.com/en-us/windows/wsl/wsl-config
[ms-powercfg]: https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/powercfg-command-line-options
[gh-21432]: https://github.com/anthropics/claude-code/issues/21432
[gh-32050]: https://github.com/anthropics/claude-code/issues/32050
[gh-32982]: https://github.com/anthropics/claude-code/issues/32982
[gh-34868]: https://github.com/anthropics/claude-code/issues/34868
[gh-36807]: https://github.com/anthropics/claude-code/issues/36807
