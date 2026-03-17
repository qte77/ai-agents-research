---
title: CC Sandbox Friction in Codespaces — Research Summary
description: Analysis of sandbox friction points in Codespace/devcontainer environments and mitigation strategies.
source: https://code.claude.com/docs/en/sandboxing, https://code.claude.com/docs/en/settings#sandbox-settings, https://code.claude.com/docs/en/security
category: analysis
created: 2026-03-17
updated: 2026-03-17
validated_links: 2026-03-17
---

**Status**: Research (informational)

## Problem

CC's Bash sandbox (`bubblewrap` on Linux) adds a second isolation layer inside
an already-isolated Codespace container, causing repeated friction for
multi-repo workflows.

## Four Friction Points Identified

| Friction | Root Cause | Solution |
|---|---|---|
| Cross-repo writes blocked | `write.allowOnly` defaults to CWD | Use `allowWrite: ["/workspaces"]` (additive, merges across scopes) ([source][cc-sandbox-settings]) |
| Git/gh operations fail | Same — `.git/` writes outside CWD rejected | Same fix. Note: `excludedCommands: ["git"]` does NOT work ([source][gh-28730]) |
| Credential sourcing blocked | `source` denied + fresh shell per Bash call | Use Codespace encrypted secrets (injected as env vars at container creation) |
| Settings don't hot-reload | Sandbox is an OS-level process primitive, baked at startup | Pre-configure correctly; restart session for changes ([source][cc-sandboxing]) |

## Key External Findings

- **`excludedCommands` + `permissions.allow` both required**
  ([source][bjorn-til]): `allow` grants permission to run, `excludedCommands`
  runs unsandboxed. Need BOTH.
- **Path prefixes silently ignored if wrong** ([source][gh-32287]): `//` =
  absolute, `~/` = home, `/` = relative to settings file. No error on
  misconfiguration.
- **`.claude/skills/` write-denied via `denyWithinAllow`** — intentional CC
  enforcement, not removable via settings.
- **Trail of Bits recommends disabling CC sandbox entirely** in devcontainers
  ([source][tob-devcontainer]) — container IS the sandbox.
- **VS Code IPC escape risk** ([source][maron-docker]): VS Code Dev Containers
  inject IPC socket paths into the container environment. Claude Code (or any
  process) can reconstruct the IPC bridge and escape.

## Solution: Option C — Hybrid

**Network sandbox ON, filesystem sandbox relaxed.** Container provides
filesystem isolation; CC provides network exfiltration protection.

```json
"sandbox": {
  "enabled": true,
  "autoAllowBashIfSandboxed": true,
  "network": {
    "allowedHosts": ["api.github.com", "raw.githubusercontent.com"]
  },
  "filesystem": {
    "allowWrite": ["/workspaces"]
  }
}
```

### Why not fully disable?

Network isolation remains valuable even inside a container — it prevents prompt
injection attacks from exfiltrating data to attacker-controlled servers
([source][cc-security]). The container alone does not restrict outbound network
traffic.

### Options Considered

| Option | Filesystem | Network | Friction | Security |
|---|---|---|---|---|
| A: Full sandbox | Restricted | Restricted | High | Double isolation |
| B: Sandbox OFF | Open | Open | None | Container only |
| **C: Hybrid** | **Open** | **Restricted** | **Low** | **Container + network isolation** |

## See Also

- [CC-sandboxing-analysis.md](CC-sandboxing-analysis.md) — full sandbox
  configuration reference with inline citations
- [CC-sandbox-platforms-landscape.md](CC-sandbox-platforms-landscape.md) —
  external sandbox platforms (E2B, OpenSandbox, gVisor)

## References

- [CC Sandboxing docs][cc-sandboxing]
- [CC Sandbox settings][cc-sandbox-settings]
- [CC Security docs][cc-security]
- [#28730 — excludedCommands doesn't bypass bwrap][gh-28730]
- [#32287 — silent path prefix misconfiguration][gh-32287]
- [bjorn.now — dual permission+exclusion requirement][bjorn-til]
- [Trail of Bits — claude-code-devcontainer][tob-devcontainer]
- [Stefan Maron — VS Code IPC escape in devcontainers][maron-docker]

[cc-sandboxing]: https://code.claude.com/docs/en/sandboxing
[cc-sandbox-settings]: https://code.claude.com/docs/en/settings#sandbox-settings
[cc-security]: https://code.claude.com/docs/en/security
[gh-28730]: https://github.com/anthropics/claude-code/issues/28730
[gh-32287]: https://github.com/anthropics/claude-code/issues/32287
[bjorn-til]: https://bjorn.now/til/2026-01-10-claude-code-sandbox-exclusion-requires-both-permissions-allow-and-sandbox-excludedcommands/
[tob-devcontainer]: https://github.com/trailofbits/claude-code-devcontainer
[maron-docker]: https://stefanmaron.com/posts/claude-code-standalone-docker-sandbox/
