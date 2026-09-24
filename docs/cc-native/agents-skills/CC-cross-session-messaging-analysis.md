---
title: CC Cross-Session Messaging
source: https://code.claude.com/docs/en/cross-session-messaging
purpose: Analysis of Claude Code's first-party cross-session messaging — independent sessions you start and steer yourself message each other, distinct from agent-team/subagent mailboxes.
created: 2026-09-23
updated: 2026-09-23
validated_links: 2026-09-23
---

**Status**: Adopt — on by default with nothing to enable wherever the version/platform gate is met, same-machine messaging generally available on every provider since v2.1.248 (cross-machine messaging still needs a claude.ai-authenticated Remote Control connection), and inbound is safe-by-default (a session that prompts for permissions delivers messages; a `bypassPermissions` session holds them for approval). The only open item is a version-gate conflict on native Windows (see [Availability](#availability)), which affects when the feature turns on there, not whether it is safe to use once it has.

## What It Is

Cross-session messaging lets one Claude Code session deliver a plain-text message to another, so a change or finding in one session reaches another session mid-task instead of the user copy-pasting between terminals ([cross-session-messaging][cc-xsm]). Claude discovers reachable sessions with the `ListAgents` tool and delivers with `SendMessage`; a message is text Claude writes for the other session, never the sender's conversation history or files. To move a whole conversation or its context, the docs point at [resuming a session][cc-sessions-resume] instead ([cross-session-messaging][cc-xsm]).

The feature shipped in the week-of-2026-08-03 digest as its own headline item, gated at v2.1.224, described there as: "Your Claude Code sessions can now message each other. Claude discovers your other sessions with the `ListAgents` tool and sends with `SendMessage`, either when you ask it to or on its own... Available on macOS and Linux" ([whats-new/2026-w32][cc-w32]).

Claude decides to send a message on its own when it sees the need — for example after a change in one session affects work another session is doing — or the user can ask for one. The documented use cases: handing over a finding, coordinating parallel [worktrees][cc-worktrees], getting a status report from long-running work, and messaging across machines ([cross-session-messaging][cc-xsm]).

## `ListAgents` / `SendMessage` and `/list-agents` (`/peers`)

The user never calls `ListAgents` or `SendMessage` directly — the docs are explicit that Claude discovers the target and sends on its own. To name a target, the user `@`-mentions a session by name (typeahead, requires v2.1.232+) the same way a subagent is `@`-mentioned, or asks in plain language and lets Claude decide ([cross-session-messaging][cc-xsm]).

`/list-agents` (alias `/peers`) lists every session Claude can reach:

- **This session's own name** (the first line, when present) — the name peers use to message it back.
- **Subagents** running inside the current session.
- **Teammates** — this session's own [agent team](CC-agent-teams-orchestration.md) teammates. Before v2.1.239, teammates didn't appear in the listing, though Claude could already message them by name.
- **Other local sessions** on the same machine, including background sessions — a session appears only when it binds an [inbox socket](#the-inbox-socket-and-messaging-env-vars).
- **Cloud sessions**, shown while connected to Remote Control, labeled `cloud`.
- **Remote Control sessions on other machines**, labeled `Remote Control`; a dropped connection shows as `offline`.

While the session is connected to Remote Control, `/list-agents` withholds local sessions' working directories and any session name it can't attribute to a person (shown as `(unnamed session)`), and the output notes when details were withheld ([cross-session-messaging][cc-xsm]).

## How It Differs From Subagents and Agent Teams

`SendMessage` is one tool that serves three different relationships, and the docs draw the line explicitly:

| Relationship | Scope | Messaging characteristics |
|---|---|---|
| Subagent | Within a single session | Same `SendMessage` tool; in-session messaging, not this page's subject |
| [Agent team](CC-agent-teams-orchestration.md) teammate | Sessions Claude spawns and supervises as a coordinated team | Structured protocol messages stay within the team; plain-text cross-session messages are a separate channel |
| Cross-session peer (this doc) | Independent sessions the **user** starts and steers | Plain text only, ~1M-char cap, discovered via `ListAgents`/`/list-agents` |

The docs' own guidance on which feature to reach for: "Use messaging between independent sessions that you start and steer yourself... For a coordinated team of sessions Claude spawns and supervises, use [agent teams](CC-agent-teams-orchestration.md)" ([cross-session-messaging][cc-xsm]). Related, distinct features it also calls out: resuming a session (to continue one conversation or move its context), [agent view][cc-agent-view] (to watch/steer many sessions from one place), [Remote Control][cc-remote-control] (to steer a session from a phone rather than have sessions message each other), and [channels][cc-channels] (to push external events like CI results into a session).

This resolves a framing gap in [CC-agent-teams-orchestration.md](CC-agent-teams-orchestration.md): a limitation documented there is specific to the Agent-Teams protocol-message channel — it does not apply to this plain-text independent-session channel, which is a separate mechanism entirely (see [Limits](#limits) below). See also the [correction note](CC-agent-teams-orchestration.md#uds-inbox--inter-session-ipc-unreleased) added there.

Same-machine, cross-repo messaging works with no configuration: "two sessions can reach each other only when they can see the same files" — no `team_name`, no worktree config. Each session registers itself in files on disk, so three independent `claude` sessions each `cd`'d into a different git repo on one machine can already reach each other ([cross-session-messaging][cc-xsm]).

## Delivery And Trust Model

### Message delivery mechanics

The receiving Claude reads a message between tool calls during an active turn (a running tool is never interrupted); if the receiving session is idle, Claude Code starts a new turn with the message. An `@` mention of a file or MCP resource inside a message arrives as plain text — Claude Code attaches nothing automatically. Before v2.1.251, an `@` mention that started a new turn did attach the file or resource on the receiving side (docs page only — no distinct CHANGELOG line found for this specific behavior change; see [Availability](#other-stated-gates-docs-page-only-not-independently-changelog-confirmed)) ([cross-session-messaging][cc-xsm]).

Claude Code refuses to send a message (in the sending session, before it leaves) when: it is over the ~1M-character size cap; a rapid burst to the target has exceeded what that session's inbox accepts; the reply-target socket on this machine fails a safety check (e.g., a symlinked target); or the message addresses the sending session's own name.

Once past the sender-side refusal checks, the receiving session's inbound check resolves to one of three outcomes:

- **Delivered** — Claude Code passes the message to the receiving Claude.
- **Held** — set aside undelivered until the user approves it or a mode/settings change allows it.
- **Refused** — dropped without delivery.

Once delivered, a message counts toward usage like a typed prompt, and the receiving Claude can reply the same way — except in the one-way cross-machine case ([cross-session-messaging][cc-xsm]).

### `crossSessionInbound`: accept / hold / refuse

`crossSessionInbound` controls what a session does with messages arriving from a user's other sessions ([cross-session-messaging][cc-xsm]):

| Value | Behavior |
|---|---|
| `accept` | Claude Code delivers each message to Claude |
| `hold` | Claude Code shows a notice per message and doesn't deliver it; a later `accept` releases held messages |
| `refuse` | Claude Code drops each message without delivering it |

The `/config` row **"Messages from your other sessions"** sets this (requires v2.1.232+) and writes to user settings; it doesn't appear when managed settings or `--settings` already sets the key.

When no `crossSessionInbound` value applies, Claude Code decides per message from both sessions' permission modes, grouped into two classes — bypassing (`bypassPermissions`, and plan mode in interactive terminal sessions with bypass available) versus prompting (`auto`, `acceptEdits`, `dontAsk`, and default):

- **Receiving session prompts**: delivers each message; holds one only when the sender identifies itself as bypassing.
- **Receiving session bypasses**: holds each message for approval; delivers only when the sender also identifies as bypassing.

A held-by-default message opens an approval dialog (Approve delivers; Deny or a `dialogExpiry` timeout — default five minutes — drops it). Claude Code holds at most 100 messages this way, past which it drops the oldest.

### `isolatePeerMachines`

Set `isolatePeerMachines: true` to require explicit user approval before any `SendMessage` reaches a session beyond the local machine — even in `bypassPermissions` mode, which otherwise skips ordinary permission prompts. A `true` from any settings scope applies (so a checked-in project file can turn the requirement on but not off), and it does not prompt for same-machine sends ([cross-session-messaging][cc-xsm]).

### How the receiving session treats an incoming message

Claude Code tells the receiving Claude the message came from another session, not the user, and constrains it: it can't approve anything (a message is never treated as the user's consent, so it can't answer a pending permission prompt); it can't change configuration (Claude Code instructs it never to change permission settings, `CLAUDE.md`, or other config because another session asked); commands in the message text (e.g. `/compact`) arrive as inert plain text and are never executed; and ordinary permission prompts still fire for anything the message asks the receiving session to do ([cross-session-messaging][cc-xsm]).

### Turning it off

Receiving and sending are independent controls. To stop receiving: set `crossSessionInbound: "refuse"`. To stop sending/listing: add permission deny rules naming the bare tool names `SendMessage` and `ListAgents` (denying `SendMessage` also removes messaging to subagents and agent-team teammates, since they share the tool). An organization can combine both in managed settings:

```json
{
  "permissions": { "deny": ["SendMessage", "ListAgents"] },
  "crossSessionInbound": "refuse"
}
```

With this set, the session still binds an inbox socket but drops everything that arrives without delivering it, and shows no visible change in its own `/status` — confirm the policy by checking the applicable settings files rather than session status ([cross-session-messaging][cc-xsm]).

## `notify_when_idle`

Requires v2.1.236+ in both sessions. Only the Claude in a main conversation can subscribe, and only to the user's own sessions on the same machine — a subagent or agent-team teammate that sets it gets no subscription, and Claude asking for a notice from a teammate, subagent, or a session beyond the local machine causes Claude Code to refuse the whole call (including any attached message) and report the refusal back.

Claude attaches `notify_when_idle` to `SendMessage`'s input, either bundled with a message or standalone (standalone, it subscribes without starting a turn or spending tokens in the watched session, and fires immediately if that session is already idle). "Idle" means the watched session finished a turn with nothing queued. The notice is one-shot — sent once, no polling either direction — and if none arrives within 12 hours Claude Code drops the subscription and tells Claude so it stops waiting. Each side's inbound controls apply to the notice like a message: `refuse` on either side means nothing arrives (and the subscription silently expires after 12 hours); `hold` on either side delivers the notice with less detail (the watched session omits its one-line status; the asking session shows the notice in the transcript without delivering it to Claude) ([cross-session-messaging][cc-xsm]).

## Cross-Machine Messaging Via Remote Control

Where a message goes determines how it travels:

| Target location | Transport |
|---|---|
| Same machine | Per-session Unix domain socket (macOS/Linux) or named pipe (native Windows) — never through Anthropic servers |
| Another of the user's machines | Through Anthropic servers, arriving over that machine's Remote Control connection |
| Cloud session | Through Anthropic servers, straight to the cloud session |

Starting a new conversation with a session on another machine (rather than only replying to one that messaged first) requires v2.1.225+ and a target session that already appears in `/list-agents`; before v2.1.225 a session could only reply to an inbound message, not originate one. A session shown as `offline` can still be messaged — the send goes through once that machine's Remote Control connection reconnects.

Cloud and other-machine sessions appear in `/list-agents` only while the current session is itself connected to Remote Control, and Claude finds them only from a session where a claude.ai sign-in is the active authentication — Claude cannot find them with an API key, or on Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, or Microsoft Foundry ([cross-session-messaging][cc-xsm]).

If the sending session isn't connected to Remote Control when it messages a session beyond the local machine, the message still goes through, but carries no reply address, so the receiving Claude cannot answer it — this is the "one-way cross-machine" exception noted under [message delivery](#delivery-and-trust-model) ([cross-session-messaging][cc-xsm]).

## The Inbox Socket And Messaging Env Vars

Claude Code binds an inbox socket per session with messaging enabled — a Unix domain socket on macOS/Linux (including WSL2) or a named pipe on native Windows — where other local sessions deliver messages. `/status` shows it in a `Peer address` row (prefixed `uds:`), or `unavailable` with a reason if Claude Code couldn't set one up.

Two environment variables expose the same channel to hooks and Bash commands, exported before any hook runs (including `SessionStart`), each session exporting its own value rather than inheriting a parent's:

- **`CLAUDE_CODE_MESSAGING_SOCKET`** — the socket's path.
- **`CLAUDE_CODE_MESSAGING_TOKEN`** — a per-session auth token. A script posting to its own session's socket can send `{"type":"auth","token":"<token>"}` as the connection's first line. On macOS/Linux the auth line is optional (Claude Code accepts a connection with or without it); on native Windows it is required, and a connection whose first line isn't a valid auth line is closed with nothing delivered.

On macOS/Linux, Claude Code restricts the socket to the OS user and refuses to create it in a directory it can't accept (falling back to a private per-user directory, `/tmp/cc-socks-<uid>`); on native Windows it requires the auth-token handshake instead. A connection must send a complete line within 30 seconds or Claude Code closes it.

Messages arriving on the socket go through the same `crossSessionInbound` checks as any peer message, with one exception: when no `crossSessionInbound` value applies, Claude Code delivers a message it can verify came from the session's own child process (e.g. a hook or Bash command posting back to its own socket) — verified by process evidence on Linux, or by the `CLAUDE_CODE_MESSAGING_TOKEN` auth line on macOS (after the posting process exits) and on native Windows (the only verification method there). Sandboxed Bash commands need `sandbox.network.allowAllUnixSockets` / `sandbox.network.allowUnixSockets` to reach the socket at all ([cross-session-messaging][cc-xsm]).

## Limits

Per the docs, these are properties of the channel itself, not platform gaps:

- **Plain text only** — structured agent-team protocol messages stay within a team; this channel never carries them.
- **Same-machine message size cap** — refused at the sender once the serialized message passes about a million characters; nothing reaches the receiving session.
- **Burst throttling at the sender** — once a rapid burst to one session exceeds what that session's inbox accepts, further sends are refused in the sending session (Claude is told to batch or wait). Before v2.1.236, such sends were reported as sent while silently dropped on the receiving side.
- **Loop throttling at the receiver** — the receiving session rate-limits repeated messages per sender, drops identical repeats within a short window, and queues at most 50 accepted messages for Claude to read, so a message loop between two sessions stops on its own ([cross-session-messaging][cc-xsm]).

This design-choice framing is worth noting against [CC-agent-teams-orchestration.md](CC-agent-teams-orchestration.md)'s limitation #12 ("structured messages cannot be broadcast"): that limitation describes the Agent-Teams protocol-message channel specifically and doesn't extend to this plain-text channel, which was never meant to carry structured broadcasts.

## Availability

### Confirmed gates (CHANGELOG-verified)

Cross-checked each stated gate against the [`anthropics/claude-code` CHANGELOG][cc-changelog] (fetched 2026-09-23):

| Gate | CHANGELOG entry | Confirms |
|---|---|---|
| v2.1.224 | "Added cross-session `SendMessage`: Claude Code sessions can now message each other, on any of your machines, with `ListAgents` to discover them (macOS and Linux)"; also adds `crossSessionInbound`/`dialogExpiry` | Base feature ships, macOS/Linux, with inbound controls |
| v2.1.225 | "`SendMessage` can now start a conversation with your Remote Control sessions on other machines by name... instead of only replying after they message you first" | Originating (not just replying to) a cross-machine conversation |
| v2.1.232 | "Type `@` in the prompt to mention another Claude session by name; Claude then uses `SendMessage` to reach that session directly"; "Added `/config` rows for 'Dialog expiry' and 'Messages from your other sessions'" | `@`-mention typeahead; `/config` UI for `crossSessionInbound`/`dialogExpiry` |
| v2.1.236 | "Added `notify_when_idle` to cross-session `SendMessage`... macOS and Linux" | `notify_when_idle` |
| v2.1.239 | "`ListAgents` and `/list-agents` now list your live teammates (previously only subagents and other sessions appeared...)"; "`ListAgents` now tells a session its own name... instead of 'no agent named...'" | Teammates appear in listing; session sees its own name |
| v2.1.247 | "Changed cross-session peer messages to collapse by default to a one-line `Message from @<sender>: <first line>` preview; Ctrl+O expands the full body" | Preview-line UI (was full text before) |
| v2.1.248 | "Added cross-session messaging (`SendMessage` / `ListAgents`) between sessions on the same machine on Bedrock, Vertex, and Foundry, and when telemetry is disabled" | Same-machine messaging on those providers / with flag-fetching off |
| v2.1.271 | "Fixed cross-session messages held by the receiving session's permission-mode policy leaving no trace: headless senders now get a delivery notice..." | Delivery notices reach `claude -p` senders |

### Native Windows — unresolved discrepancy

The docs page states native Windows requires **v2.1.234+**, both in its opening note and in its Availability section ("v2.1.224 or later on macOS, Linux, and WSL 2, and v2.1.234 or later on native Windows"). The CHANGELOG's v2.1.234 entry has no cross-session-messaging line for Windows at all; the first (and only) explicit Windows-availability entry found is at **v2.1.239**: "Windows: cross-session messaging is now available, so Claude Code sessions across your machines can message each other with `SendMessage` and find each other with `ListAgents`, as on macOS and Linux." **This is unreconciled as of 2026-09-23** — the two first-party sources disagree by five patch releases, and no CHANGELOG entry at v2.1.234–v2.1.238 supports the docs page's earlier date. Confirm against `claude --version` behavior on a native-Windows install before relying on either number.

### Other stated gates (docs page only, not independently CHANGELOG-confirmed)

The docs page also states, without a distinct CHANGELOG line found for it: before v2.1.251, an `@` mention in a message that started a new turn attached the file/MCP resource on the receiving side (v2.1.251's changelog entries cover file-tool symlink and plugin-path fixes but no line matching this specific behavior change) — included above with the caveat that it is sourced from the docs page alone.

### Platform / provider matrix

- **Operating system**: macOS, Windows, and Linux (including WSL2).
- **Same-machine messaging**: available on every provider, including Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, and Microsoft Foundry, and with feature-flag fetching off — gated at v2.1.248+ on those providers/configurations. Delivered over the local socket, never through Anthropic servers.
- **Beyond-machine messaging**: requires the current session to be connected to Remote Control with a claude.ai sign-in as its active authentication; unreachable with an API key or on Bedrock/Claude-Platform-on-AWS/Google-Cloud-Agent-Platform/Microsoft-Foundry.

To check a session, run `/list-agents` (`/peers`): if the command isn't recognized, the session lacks the feature (check `claude --version` first); if it works but a send doesn't arrive, the cause is narrower — a deny rule, the receiver's inbound controls, a missing Remote Control connection, or an `offline` target ([cross-session-messaging][cc-xsm]).

## Sources

| Source | Content |
|---|---|
| [CC cross-session messaging][cc-xsm] | Full feature description: tools, delivery/trust model, `notify_when_idle`, cross-machine transport, inbox socket + env vars, limits, availability |
| [CC what's new — 2026-w32][cc-w32] | Ship-week digest confirming v2.1.224 headline gate and macOS/Linux initial availability |
| [anthropics/claude-code CHANGELOG][cc-changelog] | Version-gate verification for v2.1.224, .225, .232, .236, .239, .247, .248, .271; surfaces the native-Windows gate discrepancy (page: v2.1.234, CHANGELOG: v2.1.239) |

[cc-xsm]: https://code.claude.com/docs/en/cross-session-messaging
[cc-w32]: https://code.claude.com/docs/en/whats-new/2026-w32
[cc-changelog]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
[cc-sessions-resume]: https://code.claude.com/docs/en/sessions#resume-a-session
[cc-worktrees]: https://code.claude.com/docs/en/worktrees
[cc-agent-view]: https://code.claude.com/docs/en/agent-view
[cc-remote-control]: https://code.claude.com/docs/en/remote-control
[cc-channels]: https://code.claude.com/docs/en/channels
