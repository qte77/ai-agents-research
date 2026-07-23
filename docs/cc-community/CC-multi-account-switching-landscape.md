---
title: CC Multi-Account & Profile Switching Landscape
purpose: How to run multiple Claude Code subscription accounts — concurrently or switched — in one OS environment, via the native CLAUDE_CONFIG_DIR mechanism and community tools built on it.
created: 2026-07-23
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Assess

## What It Is

Claude Code supports **one authenticated account per configuration directory**. There is no
native profile or account switcher — the capability has been requested upstream repeatedly
([#44687][gh-44687] (closed as duplicate), [#35856][gh-35856], [#64376][gh-64376],
[#37554][gh-37554]; all closed, none resulted in a documented feature as of 2026-07-23). This doc
covers the first-party isolation mechanism and the community tools that build multi-account
workflows — including **concurrent** sessions on different subscriptions — on top of it.

## First-Party Mechanism: `CLAUDE_CONFIG_DIR`

The [debug-your-config guide][debug-config] documents pointing `CLAUDE_CONFIG_DIR` at another
directory to "bypass everything under `~/.claude`" — settings, hooks, plugins, memory, and
(platform-dependent) credentials:

```bash
cd /tmp && CLAUDE_CONFIG_DIR=/tmp/claude-clean claude
```

**Credential isolation is platform-dependent** (per the same page):

| Platform | Credential storage | Per-config-dir account isolation |
|---|---|---|
| Linux / Windows | Under the configuration directory | **Yes** — each dir prompts its own login |
| macOS | Keychain | **No** — credentials "carry over to the clean session"; tools below implement their own isolation |

On Linux/Windows this yields a zero-install concurrent multi-account pattern — one alias per
account, one terminal each, N independent sessions:

```bash
alias claude-work='CLAUDE_CONFIG_DIR=$HOME/.claude-work command claude'
alias claude-personal='CLAUDE_CONFIG_DIR=$HOME/.claude-personal command claude'
```

Note the variable is absent from the [official env vars reference][env-vars] as of 2026-07-23 —
the debug guide links to that page for it, but only the debug guide documents the behavior.
Cross-ref: [CC-env-vars-reference.md](../cc-native/configuration/CC-env-vars-reference.md).

## Tools

| Tool | Mechanism | Concurrent? | Signals (2026-07-23) | License |
|---|---|---|---|---|
| [claude-swap][claude-swap] | Backs up/rotates OAuth credentials per account (Keychain/file); scopes a terminal to one account; **auto-rotation on rate-limit** + usage TUI | **Yes** — explicit design goal | 1,276★, pushed 2026-07-23 | MIT |
| [claude-code-profiles][cc-profiles] | Shell wrapper setting `CLAUDE_CONFIG_DIR` per named profile; one active profile per shell | Sequential switching by design (separate shells parallelize incidentally) | 56★, v1.1.0 2026-07-06 | MIT |
| [claude-multiprofile][multiprofile] | Native `CLAUDE_CONFIG_DIR` + per-profile macOS Keychain handling; also isolates Claude **Desktop** via `open -n` + `--user-data-dir` | **Yes** — incl. Desktop instances | 42★, v0.1.4 ~2026-05 | MIT |
| [claude-multisession][multisession] | Per-session dirs under `~/.claude-sessions/` (own creds/history/memory); settings shareable via symlink | **Yes** | 1★, single push 2026-02 — stale | MIT |

**Recommendation shape**: Linux/Windows + no tool trust required → the alias pattern.
Concurrency with rotation/observability → claude-swap. Claude Desktop profiles too →
claude-multiprofile.

## What This Is Not (Disambiguation)

Adjacent categories that look similar but solve different problems:

| Category | Tool(s) | Difference |
|---|---|---|
| Multi-CLI **provider/API-key** management | CC Switch — see [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md#cc-switch-farion1231) | Which provider/model/key a CLI uses — not which *subscription account* is logged in |
| Gateway-level **quota harvesting** | CLIProxyAPI — see [CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md) | Wraps CC accounts into an API endpoint for downstream clients — not N interactive CC sessions |
| Usage/cost **observability** | [CC-usage-tooling-landscape.md](CC-usage-tooling-landscape.md) | Watches spend; claude-swap's usage TUI overlaps here but its core is account rotation |

## Sources

| Source | Content |
|---|---|
| [CC debug-your-config guide][debug-config] | `CLAUDE_CONFIG_DIR` behavior, per-platform credential storage (primary first-party source) |
| [CC env vars reference][env-vars] | Confirmed gap: variable not listed (checked 2026-07-23) |
| [claude-swap][claude-swap] | Concurrent multi-account rotation; repo metadata via GitHub API, 2026-07-23 |
| [claude-code-profiles][cc-profiles] | Profile-switching wrapper; repo metadata via GitHub API, 2026-07-23 |
| [claude-multiprofile][multiprofile] | CLI + Desktop profile isolation; repo metadata via GitHub API, 2026-07-23 |
| [claude-multisession][multisession] | Per-session config dirs; repo metadata via GitHub API, 2026-07-23 |
| [anthropics/claude-code#44687][gh-44687] | Upstream FR: multi-account support (closed as duplicate) |
| [anthropics/claude-code#35856][gh-35856], [#64376][gh-64376], [#37554][gh-37554] | Further upstream FRs, all closed unimplemented |

[debug-config]: https://code.claude.com/docs/en/debug-your-config
[env-vars]: https://code.claude.com/docs/en/env-vars
[claude-swap]: https://github.com/realiti4/claude-swap
[cc-profiles]: https://github.com/quinnjr/claude-code-profiles
[multiprofile]: https://github.com/jmdarre-v/claude-multiprofile
[multisession]: https://github.com/israads/claude-multisession
[gh-44687]: https://github.com/anthropics/claude-code/issues/44687
[gh-35856]: https://github.com/anthropics/claude-code/issues/35856
[gh-64376]: https://github.com/anthropics/claude-code/issues/64376
[gh-37554]: https://github.com/anthropics/claude-code/issues/37554
