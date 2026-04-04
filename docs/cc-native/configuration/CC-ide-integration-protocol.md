---
title: CC IDE Integration Protocol
description: WebSocket-based MCP protocol between Claude Code CLI and IDE extensions — discovery, auth, transport, and community reimplementations.
created: 2026-04-04
updated: 2026-04-04
validated_links: 2026-04-04
---

**Status**: Research (informational)

## What It Is

Claude Code communicates with IDE extensions (VS Code, JetBrains) via a **WebSocket JSON-RPC 2.0 (MCP) server** — not SSE despite the `CLAUDE_CODE_SSE_PORT` variable name. The protocol enables IDE features: diff viewing, selection context, diagnostics sharing, Jupyter cell execution.

## Discovery & Auth

1. IDE extension starts a WebSocket server on a random high port
2. Extension sets `CLAUDE_CODE_SSE_PORT=<port>` and `ENABLE_IDE_INTEGRATION=true` in the terminal environment
3. Lock file written at `~/.claude/ide/<port>.lock`:
   ```json
   {
     "workspaceFolders": ["/path/to/project"],
     "pid": 12345,
     "ideName": "vscode",
     "transport": "ws",
     "token": "<random-auth-token>"
   }
   ```
4. Lock file: `0600` permissions, directory: `0700`
5. Server binds to `127.0.0.1` only
6. Each IDE activation generates a fresh random auth token

## Transport

- **Protocol**: WebSocket (RFC 6455), NOT plain SSE
- **Message format**: JSON-RPC 2.0 (MCP protocol)
- **Tools implemented**: Same tool names, parameters, and response formats as VS Code extension
- **Server name**: `ide` (hidden from `/mcp` listing)

## Community Reimplementations

| Project | Editor | Approach |
|---------|--------|----------|
| [coder/claudecode.nvim][nvim] | Neovim | Pure Lua, 100% protocol compatibility. Full reverse-engineering of VS Code extension protocol |
| [manzaltu/claude-code-ide.el][emacs] | Emacs | Elisp IDE integration |

## Known Issues

| Issue | Description |
|-------|-------------|
| [#1234][gh-1234] | Request to document IDE protocol for third-party editors |
| [#16912][gh-16912] | IntelliJ SSE connection never established (Windows) |
| [#13933][gh-13933] | `/ide` fails in devcontainer (lock file path) |
| [#23119][gh-23119] | IDE integration broken v2.1.23+ (Windows) |
| [#14421][gh-14421] | IDE lock file deleted in IntelliJ WSL terminal |

## Cross-References

- [CC-env-vars-reference.md](CC-env-vars-reference.md) — `CLAUDE_CODE_SSE_PORT`, `CLAUDE_CODE_AUTO_CONNECT_IDE`
- [CC-community-reimplementations-landscape.md](../../cc-community/CC-community-reimplementations-landscape.md)

## Sources

| Source | Content |
|---|---|
| [coder/claudecode.nvim][nvim] | Reference reimplementation (Neovim, Lua) |
| [GitHub #1234][gh-1234] | IDE protocol documentation request |

[nvim]: https://github.com/coder/claudecode.nvim
[emacs]: https://github.com/manzaltu/claude-code-ide.el
[gh-1234]: https://github.com/anthropics/claude-code/issues/1234
[gh-16912]: https://github.com/anthropics/claude-code/issues/16912
[gh-13933]: https://github.com/anthropics/claude-code/issues/13933
[gh-23119]: https://github.com/anthropics/claude-code/issues/23119
[gh-14421]: https://github.com/anthropics/claude-code/issues/14421
