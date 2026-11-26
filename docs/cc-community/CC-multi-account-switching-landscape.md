---
title: CC Multi-Account & Profile Switching Landscape
purpose: How to run multiple Claude Code subscription accounts — concurrently or switched — in one OS environment, via the native CLAUDE_CONFIG_DIR mechanism and community tools built on it.
created: 2026-07-23
updated: 2026-11-26
validated_links_on: 2026-07-23
status: assess
---

## What It Is

Claude Code supports **one authenticated account per configuration directory**. There is no
native profile or account switcher command — the capability has been requested upstream repeatedly
([#44687][gh-44687] (closed as duplicate), [#35856][gh-35856] (closed as completed; the reason is not
explained in the thread, unverified), [#64376][gh-64376] (closed as not planned), [#37554][gh-37554]
(closed as duplicate); checked 2026-11-26). The authentication page now documents a ["Log in with
multiple accounts"][auth-multi] pattern: one `CLAUDE_CONFIG_DIR` per account, each with its own settings,
session history and claude.ai login or API key. Caveat on that page: Console sign-ins without an API key
are stored outside the configuration directory, so separate directories don't keep two of them apart. This doc
covers the first-party isolation mechanism and the community tools that build multi-account
workflows — including **concurrent** sessions on different subscriptions — on top of it.

## First-Party Mechanism: `CLAUDE_CONFIG_DIR`

The [debug-your-config guide][debug-config] documents setting `CLAUDE_CONFIG_DIR` to a fresh directory in
place of `~/.claude` for a clean test session (first launch repeats the first-run setup screens), and
recommends `claude --safe-mode` first:

```bash
CLAUDE_CONFIG_DIR=~/claude-clean/config claude --setting-sources user
```

**Credential storage** (per the [authentication page's credential management section][auth-cred], checked
2026-11-26): with `CLAUDE_CONFIG_DIR` set, Claude Code keeps `.credentials.json` under that directory
and keys the macOS Keychain entry to that directory too, so a session with a different directory reads a
different entry.

| Platform | Credential storage | Per-config-dir account isolation |
|---|---|---|
| Linux / Windows | `.credentials.json` under the configuration directory | **Yes** — each dir prompts its own login |
| macOS | Keychain entry keyed to the directory (falls back to `.credentials.json`, mode `0600`, when the Keychain rejects the write) | **Yes** per the page; an earlier version of this doc, based on an older debug-guide sentence, said no |

This yields a zero-install concurrent multi-account pattern on every platform — one alias per
account, one terminal each, N independent sessions:

```bash
alias claude-work='CLAUDE_CONFIG_DIR=$HOME/.claude-work command claude'
alias claude-personal='CLAUDE_CONFIG_DIR=$HOME/.claude-personal command claude'
```

The variable is now listed in the [official env vars reference][env-vars] (checked 2026-11-26), which
mentions running multiple accounts side by side; it is ignored in project and local settings.
Cross-ref: [CC-env-vars-reference.md](../cc-native/configuration/CC-env-vars-reference.md).

## Repo Helper: `scripts/cc-multi-account.sh`

This repo ships [`scripts/cc-multi-account.sh`](../../scripts/cc-multi-account.sh), a small helper
built on the same `CLAUDE_CONFIG_DIR` mechanism (Linux/WSL2/Codespaces, where credentials live in the
config dir). You can run it directly or source it for short commands:

| Executed (`./cc-multi-account.sh …`) | Sourced (`source cc-multi-account.sh`) | Does |
|---|---|---|
| `<profile>` | `ccp <profile>` | Launch CC with `CLAUDE_CONFIG_DIR=$CC_PROFILE_HOME/<profile>`; first run prompts `/login` |
| `usage <profile>` | `ccu <profile>` | Per-account usage via `ccusage` (needs `npm i -g ccusage`) |
| `list` | `ccl` | List configured profiles |
| `sync <profile>` / `sync --all` | `ccsync <profile>` / `ccsync --all` | Re-apply the shared base settings to one or all profiles |
| `--help` | `cch` | Print usage |

| Env var | Default | Purpose |
|---|---|---|
| `CC_PROFILE_HOME` | `$HOME/.claude-profiles` | Where per-account config dirs live |
| `CC_BASE_SETTINGS` | `$HOME/.claude/settings.json` | Shared settings that `ccsync` applies to each profile |
| `CC_PROFILE_KEEP` | `theme preferredNotifChannel agentPushNotifEnabled skipWorkflowUsageWarning` | Keys a profile owns; `ccsync` never overwrites them |

Two behaviours matter:

- **Profiles drift.** `CLAUDE_CONFIG_DIR` relocates the whole config dir, so each profile gets its own
  `settings.json`, and a new profile starts without your permissions, hooks, plugins or env.
  `ccsync` merges `CC_BASE_SETTINGS` into the profile while keeping the `CC_PROFILE_KEEP` keys. It
  backs up to `settings.json.bak`, reports any key it drops, and never touches `.credentials.json`.
  It is deliberately not a symlink: CC writes to `settings.json`, so concurrent profiles would race
  on one file, and an atomic tmp-and-rename write silently replaces the symlink with a copy.
- **Permissions.** `ccp` and `ccsync` set the profile dirs to `700`. Under a default umask, `mkdir -p`
  leaves them `755`, so other local users could read `history.jsonl` and `projects/` transcripts,
  even though `.credentials.json` itself is `600`.

## Tools

| Tool | Mechanism | Concurrent? | Signals (checked 2026-11-26) | License |
|---|---|---|---|---|
| [claude-swap][claude-swap] | Backs up/rotates OAuth credentials per account (Keychain/file); scopes a terminal to one account; **auto-rotation on rate-limit** + usage TUI | **Yes** — explicit design goal | 4,979★, pushed 2026-11-26 (`gh api`, 2026-11-26; mechanism text rests on repo metadata, README not re-read) | MIT |
| [claude-multiprofile][multiprofile] | Native `CLAUDE_CONFIG_DIR` + per-profile macOS Keychain handling; also isolates Claude **Desktop** via `open -n` + `--user-data-dir` | **Yes** — incl. Desktop instances | 230★, v0.1.41 2026-11-25 (`gh api` 2026-11-26; mechanism text rests on repo metadata, README not re-read) | MIT |

**Recommendation shape**: no tool trust required → the alias pattern (works on macOS too, per the authentication page).
Concurrency with rotation/observability → claude-swap. Claude Desktop profiles too →
claude-multiprofile.

## What This Is Not (Disambiguation)

Adjacent categories that look similar but solve different problems:

| Category | Tool(s) | Difference |
|---|---|---|
| Multi-CLI **provider/API-key** management | CC Switch — see [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md#cc-switch-farion1231) | Which provider/model/key a CLI uses — not which *subscription account* is logged in |
| Gateway-level **quota harvesting** | CLIProxyAPI — see [CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md) | Wraps CC accounts into an API endpoint for downstream clients — not N interactive CC sessions |
| Usage/cost **observability** | [CC-usage-tooling-landscape.md](CC-usage-tooling-landscape.md) | Watches spend; claude-swap's usage TUI overlaps here but its core is account rotation |

## Not included

Entries removed under the [pruning rule](../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (alive, adopted or proven; checked 2026-11-22).

| Name | Reason | Date | Link |
|---|---|---|---|
| claude-code-profiles | Criterion 3: 109 stars; last push 2026-09-18 (`gh api` 2026-11-22); no named independent users or measured benefit in its README | 2026-11-22 | <https://github.com/quinnjr/claude-code-profiles> |
| claude-multisession | Criterion 3: 1 star; last push 2026-02-28 (`gh api` 2026-11-22); no named users | 2026-11-22 | <https://github.com/israads/claude-multisession> |

## Sources

| Source | Content |
|---|---|
| [CC debug-your-config guide][debug-config] | Clean-configuration test with `CLAUDE_CONFIG_DIR` (checked 2026-11-26) |
| [CC authentication page][auth-multi] | "Log in with multiple accounts" and [credential management][auth-cred] (primary first-party source, checked 2026-11-26) |
| [CC env vars reference][env-vars] | `CLAUDE_CONFIG_DIR` row, now listed (checked 2026-11-26; earlier gap closed) |
| [`scripts/cc-multi-account.sh`](../../scripts/cc-multi-account.sh) | Repo helper: commands, env vars, `ccsync` and permission behaviour (source read 2026-09-23) |
| [claude-swap][claude-swap] | Concurrent multi-account rotation; repo metadata via GitHub API, 2026-11-26 |
| [claude-multiprofile][multiprofile] | CLI + Desktop profile isolation; repo metadata via GitHub API, 2026-11-26 |
| [anthropics/claude-code#44687][gh-44687] | Upstream FR: multi-account support (closed as duplicate) |
| [anthropics/claude-code#35856][gh-35856], [#64376][gh-64376], [#37554][gh-37554] | Further upstream FRs: #35856 closed as completed (reason unexplained, unverified), #64376 not planned, #37554 duplicate |

[debug-config]: https://code.claude.com/docs/en/debug-your-config
[env-vars]: https://code.claude.com/docs/en/env-vars
[auth-multi]: https://code.claude.com/docs/en/authentication#log-in-with-multiple-accounts
[auth-cred]: https://code.claude.com/docs/en/authentication#credential-management
[claude-swap]: https://github.com/realiti4/claude-swap
[multiprofile]: https://github.com/jmdarre-v/claude-multiprofile
[gh-44687]: https://github.com/anthropics/claude-code/issues/44687
[gh-35856]: https://github.com/anthropics/claude-code/issues/35856
[gh-64376]: https://github.com/anthropics/claude-code/issues/64376
[gh-37554]: https://github.com/anthropics/claude-code/issues/37554
