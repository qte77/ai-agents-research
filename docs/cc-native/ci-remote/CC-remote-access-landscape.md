---
title: CC Remote Access Landscape
source: https://www.omnara.com
purpose: Comparison of remote access options for monitoring and steering Claude Code sessions (autonomous loops, teams, baselines) from mobile/web.
created: 2026-03-07
updated: 2026-11-26
validated_links_on: 2026-10-06
status: research
---

## Problem Statement

Autonomous development loops and CC teams runs are long-running interactive
sessions. Currently, the developer must stay at the terminal to provide
input, approve permissions, or steer when stuck. Remote access enables
monitoring and steering from phone/web without being desk-bound.

## Options Compared

| Aspect | CC Remote Control | Happy Coder | Omnara | CloudCLI | Emdash | T3 Code | DIY (tmux + Tailscale) |
| ------ | ----------------- | ----------- | ------ | -------- | ------ | ------ | ---------------------- |
| **Type** | Built-in CC feature | Open source (MIT) | SaaS (YC S25) | Open source (AGPL-3.0, ~14.8k stars, checked 2026-11-26) | Multi-agent orchestrator | Open source (MIT) control plane for coding agents (~80.6k stars, checked 2026-11-26) | Self-hosted infrastructure |
| **Execution** | Local machine | Local machine | Local + cloud failover (third-party 2025 articles; pre-pivot, unverified at first party) | Cloud VMs | Local (git worktrees) | Local machine, or any host you run it on | Local machine |
| **Mobile app** | Claude iOS/Android | iOS, Android, Web | Dedicated iOS app | Browser-based | Web dashboard | iOS, Android, web | Terminal app (Termius, Blink) |
| **Voice input** | No | Yes | Yes (two-way; pre-pivot, unverified at first party) | No | No | Not verified | No |
| **Offline continuation** | No — auto-reconnects on wake | No — pauses | Yes — cloud sandbox | Yes — cloud-native | No — pauses | No — host must stay running and reachable | No — pauses |
| **Push notifications** | Yes | Yes | Yes | No | No | Not verified | No |
| **E2E encryption** | TLS (Anthropic) | Yes (TweetNaCl) | No | SSH | N/A | Not verified | VPN-encrypted |
| **Multi-agent** | One per instance | Multi-session parallel | Orchestration dashboard | Persistent sessions | Parallel worktrees | Threads, each can use its own git worktree | Multiple tmux panes |
| **Pricing** | Free (with CC sub) | Free | Self-serve $0 platform fee plus usage billing; Enterprise on request (checked 2026-11-26) | Free (infra costs) | Free (open source) | Free app; no token resale. T3 Connect machine cap is raised by a paid T3 Chat plan | Free (infra costs) |
| **Setup** | `claude remote-control` | `npm i -g happy-coder` | `curl install + omnara` | Docker/cloud setup | npm install | `curl -fsSL https://t3.codes/install.sh \| sh`, `npx t3@latest`, desktop app or package manager | tmux + Tailscale/WireGuard |
| **Tools supported** | CC only | CC + Codex | CC + Codex | CC + Cursor + Codex + Gemini | 25+ agents (provider-agnostic) | Claude Code, Codex, Cursor, OpenCode + any Agent Client Protocol (ACP) agent | Any terminal tool |
| **Open source** | No (native) | Yes (MIT) | Yes (Apache-2.0; repo now the managed-agent platform) | Yes | Yes | Yes (MIT; name and logos trademarked) | N/A |
| **Maintenance risk** | Anthropic-maintained | Active community | Pivoted once; small team | Community-maintained | Community-maintained | Young (repo created 2026-02-08), pre-1.0 (v0.1.12) | Zero external dependency |

## Detailed Notes

### CC Remote Control (Native)

Already analyzed in
[CC-remote-control-analysis.md](CC-remote-control-analysis.md). Built-in,
zero-cost, zero-setup. Limitation: no offline continuation — if the laptop
sleeps or the network drops, the session reconnects automatically once the
machine is back online (in server mode the `claude remote-control` process gives up after about 10 min of outage, resumable for about 4 hours; an interactive session keeps retrying until the terminal shows a failure, and a ~30 min presence-heartbeat failure also disconnects); no execution happens while the machine is actually
asleep ([source][cc-rc]). Reflects CC v2.1.212+, 2026-07-23.

### Omnara

*Markets itself as a "command center for AI agents" — see the [agent control-surface naming landscape](../../non-cc/protocols/ag-ui-protocol-landscape.md#agent-control-surface-naming-2026) for how that framing compares across the category.*

- **YC S25 startup** (San Francisco, 3-person team) ([source][omnara-yc])
- **Pivoted**: the `omnara-ai/omnara` repo (Apache-2.0, not archived,
  last push 2026-11-26 per `gh api`, checked 2026-11-26) now describes itself as an open-source,
  self-hostable managed agent platform rather than the original CLI wrapper
  ([source][omnara-gh])
- **Key differentiator** (third-party 2025 articles; the current site describes resume from saved state after a crash, not sandbox failover, so treat as pre-pivot and unverified at first party): Cloud sandbox failover — if laptop goes
  offline, session continues in hosted sandbox. Code state preserved
  via git commits ([source][omnara-techmonk])
- **Architecture**: Headless daemon on local machine → outbound
  WebSocket → Omnara server → web/mobile clients
  ([source][omnara-hn])
- **Security concern**: No end-to-end encryption. Conversation state
  and code diffs transit through Omnara servers
  ([source][omnara-techmonk])
- **Voice** (pre-pivot, per a third-party article; the current site does not mention voice): Two-way voice coding mode for hands-free interaction
  ([source][omnara-hiretop])
- **Localhost previews**: Preview dev server on phone without SSH
  tunnels — *unverified as of 2026-10-23*: the only source was the iOS
  App Store listing, which now returns 404, and Omnara's site and README
  no longer mention an iOS app
- **Pricing** (checked 2026-11-26): Self-serve ($0 platform fee; Omnara-managed models billed at provider token rates; managed machines billed per GiB-hour; bring-your-own keys and machines free; 5% fee on credits), Enterprise (contact sales) and Omnara for Startups (credits) ([source][omnara-pricing]); the earlier $9 Pro tier and 10-session cap no longer appear. Local runs
  use your own Claude/Codex tokens

### CloudCLI

- **Open source** (AGPL-3.0, ~14.8k GitHub stars as of 2026-11-26 for the underlying
  siteboon/claudecodeui repo), cloud or self-hosted dev environments
  ([source][cloudcli-gh])
- **Multi-tool**: Works with five coding agents — Claude Code, Cursor CLI,
  Codex, Gemini CLI, and OpenCode; VS Code is an access surface (with
  browser, mobile, SSH), not a separate tool ([source][cloudcli])
- **Cloud-first by default**: Managed hosting or self-hosted; sessions run
  in VMs, not local machine ([source][cloudcli])

### Happy Coder

- **Free, open-source** (MIT license, fully auditable at
  [github.com/slopus/happy][happy-gh]) ([source][happy])
- **E2E encryption**: TweetNaCl (same protocol as Signal). Relay server
  only sees encrypted blobs. Keys never leave device ([source][happy-hn])
- **Zero-knowledge architecture**: Code and prompts never touch the server
  in plaintext ([source][happy])
- **Push notifications**: Alerts when CC needs permission or encounters
  errors ([source][happy])
- **Voice input**: Built-in voice-to-text for prompts ([source][zilliz])
- **Multi-session**: Spawn and control multiple CC instances in parallel
  ([source][happy])
- **Cross-platform**: iOS, Android, Web — instant device switching with
  one keypress ([source][happy])
- **Setup**: `npm install -g happy-coder` then run `happy` instead of
  `claude`. Scan QR to pair ([source][happy])
- **No telemetry**: All tracking explicitly disabled
  ([source][happy-gh])

### Emdash

- **Multi-agent orchestrator**: Runs numerous coding agents
  simultaneously, each in its own git worktree ([source][emdash])
- **Provider-agnostic**: Supports 25+ coding agents (Claude Code, Codex,
  Cursor, Amp, Antigravity, OpenCode, and others) ([source][emdash])
- **Issue integration**: Assign issues from Linear, Jira, GitHub, Notion,
  or Asana to agents and observe them working in parallel
  ([source][emdash])
- **Not a remote access tool per se** — more an orchestration layer that
  complements remote access

### T3 Code

- **Open-source control plane for coding agents** from T3 Tools, Inc.
  (`pingdotgg/t3code`): desktop, web and phone clients over one server.
  Source is MIT per the repo's `LICENSE` file, but the name, logos and
  branding are trademarked, so forks must rebrand ([source][t3code-gh])
- **Agents**: README lists Claude Code, Codex, Cursor, OpenCode, Grok Build,
  Antigravity, Kiro, Pi, Muse Code, fx and any Agent Client Protocol (ACP)
  agent; it drives agents already signed in on the host and does not resell
  tokens ([source][t3code-gh])
- **Remote access**: the agents run on the host machine; clients connect over
  LAN, Tailscale or "T3 Connect" (account sign-in, no router forwarding; set up with
  `t3 up`, optional per-device approval). The host must stay running
  ([source][t3code-remote]). No offline continuation, so it sits with the
  local-execution options above
- **Install**: desktop app, Homebrew cask, winget/scoop, `curl` script
  (`t3`), or `npx t3@latest`; iOS and Android apps in the stores
  ([source][t3code-gh])
- **Adoption and maturity**: about 80.6k stars, latest release v0.1.12
  (2026-11-25), repo created 2026-02-08 (`gh api`, checked 2026-11-26).
  README describes it as "Fast" — vendor marketing, not measured here
- **Not verified**: voice input, push notifications and end-to-end
  encryption are not stated in the README or the remote-access page
  (read 2026-11-24)

### DIY (tmux + Tailscale/SSH)

- **Maximum control**: tmux session + Tailscale/WireGuard VPN + mobile
  terminal (Termius, Blink)
- **No external dependencies**: No third-party servers handling
  code/conversations
- **Overhead**: Manual setup, no push notifications, raw terminal on
  mobile ("terminal on a phone screen is nobody's idea of a good time"
  ([source][zilliz]))
- **Already possible**: No new tooling needed if tmux is available

## Workflow Fit by Use Case

| Workflow | Best Option | Rationale |
| -------- | ----------- | --------- |
| Monitor autonomous loop from phone | CC Remote Control | Free, zero-setup, sufficient for steering |
| Monitor with push notifications | Happy Coder | Free, E2E encrypted, alerts on permission/error |
| Long runs where laptop may sleep | Omnara or tmux on server | CC RC drops on sleep; need offline continuation |
| CC teams monitoring | CC Remote Control | Multi-surface sync for single session |
| Parallel agent orchestration | Emdash | Parallel worktrees, issue tracker integration |
| Parallel baseline collection | CC Cloud Sessions (`--remote`) | See [CC-cloud-sessions-analysis.md](CC-cloud-sessions-analysis.md) |
| Security-sensitive work | Happy Coder or DIY | E2E encryption (Happy) or full control (DIY) |

### Decision Rule

**Start with CC Remote Control (free, native, zero-setup). If you need push
notifications, voice input, or E2E encryption, use Happy Coder (free,
open-source). Only evaluate Omnara if cloud sandbox failover is a real
bottleneck — i.e., autonomous loop runs regularly stall because the laptop
sleeps mid-session.**

### Risk Assessment

| Option | Risk | Mitigation |
| ------ | ---- | ---------- |
| CC Remote Control | Session pauses on laptop sleep/network drop (auto-reconnects on wake; server mode gives up after ~10 min) | No always-on requirement; in server mode avoid network outages longer than ~10 min |
| Happy Coder | Relay server dependency (encrypted, but still a hop) | Self-host relay if concerned; code is MIT-licensed |
| Omnara | Startup risk (3-person team, pivoted once); no E2E encryption | Don't send sensitive code; evaluate stability before adopting |
| Emdash | Orchestration complexity; community-maintained | Evaluate only when parallel agent runs are a real need |
| CloudCLI | Cloud-first doesn't fit local Model Context Protocol (MCP)/state workflows | Only for tasks that don't need local config |
| DIY | Setup overhead, raw terminal UX on mobile | One-time setup; acceptable for power users |

### Actionable Next Steps

1. **Try CC Remote Control** — see
   [CC-remote-control-analysis.md](CC-remote-control-analysis.md) for
   setup and decision rationale
2. **If you need push notifications or E2E encryption**: Install Happy
   Coder (`npm i -g happy-coder`)
3. **Measure**: Does the laptop actually sleep during long runs? If not,
   RC or Happy Coder is sufficient
4. **If sleep is a problem**: Evaluate Omnara's cloud sandbox failover on
   a non-sensitive test repo first

## Supporting Tools

Tools that complement any remote access method ([source][zilliz]):

| Tool | Purpose | Setup | Notes |
| ---- | ------- | ----- | ----- |
| **memsearch** | Persistent searchable recall across sessions/devices | CC plugin (hooks + skill, no MCP) | Markdown store + Milvus hybrid vector+BM25 search; full entry in [CC-memory-tooling-landscape.md](../../cc-community/CC-memory-tooling-landscape.md#memsearch-zilliztech) |

## See Also

- [CC-web-auth-setup-analysis.md](CC-web-auth-setup-analysis.md) — authentication methods for web, terminal, and headless modes

## Not included

Entries removed under the [pruning rule](../../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (alive, adopted or proven; checked 2026-11-22).

| Name | Reason | Date | Link |
|---|---|---|---|
| Tailnet Preview | Criterion 3: 1 star; last push 2026-09-23; no named independent users or standards body (`gh api` 2026-11-22) | 2026-11-22 | <https://github.com/elsheppo/tailnet-preview> |
| cc-tmux-worktree-orchestration | Criterion 3: 2 stars; last push 2026-01-29; no other adoption evidence (`gh api` 2026-11-22) | 2026-11-22 | <https://github.com/zc277584121/cc-tmux-worktree-orchestration> |
| Typeless | Criterion 3: voice-dictation app from an undisclosed company; its only adoption evidence is named testimonials the vendor publishes itself, and "4x faster than typing" is the vendor's own claim with no measurement behind it (typeless.com, fetched 2026-11-22) | 2026-11-22 | <https://www.typeless.com> |

## References

- [CC Remote Control docs][cc-rc] — native feature
- [Happy Coder][happy] — free, open-source, E2E encrypted mobile client
- [Happy Coder GitHub][happy-gh] — MIT-licensed source
- [Happy Coder (HN launch)][happy-hn] — community discussion
- [Omnara][omnara] — YC S25, cloud sandbox failover
- [Omnara GitHub][omnara-gh] — open-source repo (Apache-2.0)
- [Emdash][emdash] — multi-agent parallel orchestration
- [T3 Code GitHub][t3code-gh] — open-source multi-agent control plane (MIT), README read 2026-11-24
- [T3 Code remote-access doc][t3code-remote] — T3 Connect, LAN and Tailscale routes
- [CloudCLI][cloudcli] — open-source cloud dev environments
- [CloudCLI GitHub (siteboon/claudecodeui)][cloudcli-gh] — underlying open-source repo
- [Omnara pricing][omnara-pricing] — current pricing tiers
- [CC Cloud Sessions docs][cc-cloud] — Anthropic cloud execution
- [Zilliz mobile CC guide][zilliz] — comparison + supporting tools

[cc-rc]: https://code.claude.com/docs/en/remote-control
[happy]: https://happy.engineering
[happy-gh]: https://github.com/slopus/happy
[happy-hn]: https://news.ycombinator.com/item?id=44904039
[omnara]: https://www.omnara.com
[omnara-yc]: https://www.ycombinator.com/companies/omnara
[omnara-gh]: https://github.com/omnara-ai/omnara
[omnara-hn]: https://news.ycombinator.com/item?id=44878650
[omnara-techmonk]: https://techmonk.economictimes.indiatimes.com/news/ai/omnara-wants-to-put-your-coding-agent-on-your-phone/128286862
[omnara-hiretop]: https://hiretop.com/blog5/omnara-mobile-voice-interface-for-claude-code/
[emdash]: https://emdash.ai/
[t3code-gh]: https://github.com/pingdotgg/t3code
[t3code-remote]: https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md
[cloudcli]: https://cloudcli.ai
[cloudcli-gh]: https://github.com/siteboon/claudecodeui
[omnara-pricing]: https://www.omnara.com/pricing
[cc-cloud]: https://code.claude.com/docs/en/claude-code-on-the-web
[zilliz]: https://zilliz.com/blog/3-easiest-ways-to-use-claude-code-on-your-mobile-phone
