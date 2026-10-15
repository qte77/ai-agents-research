---
title: CC /goal Command Analysis
source: https://code.claude.com/docs/en/goal
purpose: Analysis of the /goal command, the session-scoped completion-condition loop that keeps Claude working across turns until a model-evaluated condition is met — its evaluation mechanism, lifecycle, version gates, and relation to other long-running-session approaches in this corpus.
created: 2026-10-15
updated: 2026-10-15
validated_links: 2026-10-15
status: generally-available
---

**Details:** `/goal` introduced v2.1.139 ([CHANGELOG][changelog-raw]); not labeled beta or
Research Preview on its docs page or in the introducing changelog entry (contrast the
Research-Preview-labeled agent view added the same release). All claims below are
**documented** — read from [code.claude.com/docs/en/goal][goal-docs] and the CC CHANGELOG as
cited; this corpus has not independently tested `/goal` (no `observed` claims here).

## What It Is

> Set a completion condition with /goal and Claude keeps working until it's met, a model
> judges it impossible, or an error you have to fix clears the goal.

`/goal <condition>` sets a completion condition; after each turn a model checks whether the
condition holds, and if not, Claude starts another turn instead of returning control to the
user. The docs frame it for "substantial work with a verifiable end state":

- Migrating a module to a new API until every call site compiles and tests pass
- Implementing a design doc until all acceptance criteria hold
- Splitting a large file into focused modules until each is under a size budget
- Working through a labeled issue backlog until the queue is empty

## How Evaluation Works

`/goal` is **"a wrapper around a session-scoped [prompt-based Stop hook][stop-hook]."** After
every turn, Claude Code sends the condition plus the conversation so far to the configured
small fast model, which returns one of three verdicts:

- **Not yet met** — Claude keeps working, taking the reason as guidance for the next turn
- **Met** — Claude Code clears the goal and records an achieved entry in the transcript
- **Impossible** — Claude Code clears the goal and records a failed entry with the reason;
  "You don't need to clear it yourself."

The evaluator "does not call tools, so it can only judge what Claude has already surfaced in
the conversation" — a condition must be something Claude's own output can demonstrate (e.g.
"`npm test` exits 0" is checkable; a condition resting on state Claude never prints is not).
[`ANTHROPIC_DEFAULT_HAIKU_MODEL`][model-config] redirects the evaluator, but the docs warn it
also "resolves the `haiku` alias to that model and runs background functionality, such as
conversation summarization, on it" — a single env var reaches further than `/goal` alone.
Evaluation tokens bill on the small fast model and are "typically negligible compared to
main-turn spend" (stated, not independently measured by this corpus).

If Claude answers the evaluator without using a tool for several turns running, "Claude Code
stops the loop, prints a warning, and returns control to you with the goal still set" —
evaluation resumes on the next prompt.

## Setting, Checking, Clearing

One goal is active per session; setting a new one replaces an active one. Setting a goal
starts a turn immediately, "with the condition itself as the directive" — no separate prompt
needed. The condition is capped at 4,000 characters and can carry a turn/time bound (e.g.
`or stop after 20 turns`), which Claude reports progress against and the evaluator judges from
the conversation.

`/goal` **does not change permission mode** — Manual mode still prompts for tool calls the
session's settings don't already allow, so unattended goal turns require running `/goal` in
[auto mode][auto-mode-config]. The docs describe the two as complementary: "auto mode removes
per-tool prompts, and `/goal` removes per-turn prompts."

`/goal` with no argument shows status (condition, elapsed time, turns evaluated, token spend,
evaluator's most recent reason, or the last achieved condition if none is active). `/goal
clear` (aliases: `stop`, `off`, `reset`, `none`, `cancel`) removes an active goal; `/clear`
(new conversation) also removes it.

## Lifecycle

### Resuming a session

Claude Code restores a goal that was still active when the session ended, on every resume
route: `--continue`, `--resume` (session ID, name, or transcript file path), and the session
picker. **Before v2.1.239, the picker route was the one exception** — confirmed in the
CHANGELOG: `` /goal: resuming a session from the `claude --resume` picker now restores its
active goal `` (v2.1.239). Resume carries the condition over but resets the turn count, timer,
and token-spend baseline; it does not restore an already-achieved or cleared goal.

Resume-across-compaction specifically was unreliable before **v2.1.274**, per two CHANGELOG
entries from that release: `` Fixed hook-driven sessions (such as an active `/goal`) ending
with "Prompt is too long" instead of compacting when the context overflowed again after a
reactive compaction `` and `` Fixed an active `/goal` being lost when resuming (`--continue` /
`--resume`) a session that had compacted ``.

### Errors

Four kinds of failure **clear** the goal outright (Claude Code prints a warning starting
`Goal cleared after an unrecoverable error` and ending `Run /goal again to continue`):

- An authentication failure, when Claude Code manages its own credentials (a host-managed
  session — the desktop app or a cloud session — leaves the goal active instead, since the
  host restores access on its own)
- An exhausted credit balance
- A context overflow that auto-compaction couldn't clear
- A model that isn't available

Every other failure leaves the goal set. **In an interactive session on v2.1.269 or later**,
Claude Code also names the cause and either retries (transient failures, backing off, pausing
after three automatic retries) or pauses (a rate limit, a usage limit, or a hook that ended the
turn — resuming automatically once a usage-limit wait clears). This matches the CHANGELOG entry
at that version: `` Fixed `/goal` runs silently stalling after API errors, network drops, or
token limits: the goal now retries with backoff, or pauses and says why, including until a
usage limit resets ``. Setting [`CLAUDE_CODE_GOAL_CHECKIN_MINUTES`][env-vars]`=0` turns off both
automatic retries and check-ins (below).

### Background work defers evaluation

If a subagent or background shell is still running when a turn ends, Claude Code skips
evaluation for that turn and evaluates at the end of the next turn that finishes with no
background work running — delivering the result as a new turn once it finishes. *(Changelog-only,
not stated on the docs page: this deferral traces to a fix four releases after `/goal`
shipped — v2.1.143, `` Fixed `/goal` evaluator firing while background shells or delegated
subagents are still running ``.)*

Once background work has held the goal 30 minutes (the default), a check-in is due: Claude
Code lists the running tasks and asks Claude to keep waiting, or fix/stop anything stuck.
Check-ins require **v2.1.234 or later**; after the first, each later check-in waits twice as
long, up to four times the first interval (1h, then every 2h by default) — confirmed by the
CHANGELOG at that version (`` /goal: when background tasks keep a goal waiting for 30+ minutes,
Claude now checks in on them instead of waiting indefinitely... ``). **Idle check-ins** (Claude
Code starting a turn on its own while the session sits idle, rather than waiting for the next
turn-end) require **v2.1.236 or later**, and are capped at **three per goal between prompts**
since **v2.1.246** — before that version idle check-ins were uncapped, matching the CHANGELOG's
`` Changed idle sessions to start at most three check-ins on long-running background work per
goal; your next message allows three more ``. In a **non-interactive session (`-p`)**, the
turn-end path is the *only* way a check-in is delivered — there is no idle path to start a turn
with nobody watching.

### Interaction with `/loop`, scheduled tasks, headless `-p`, and subagents

The docs page gives its own three-way comparison for approaches that keep a session running:

| Approach | Next turn starts when | Stops when |
|---|---|---|
| `/goal` | The previous turn finishes, or an idle check-in / automatic retry comes due | A model confirms the condition met or impossible, a turn fails on an unrecoverable error, or `/goal clear` |
| `/loop` | A time interval elapses | You stop it, or Claude decides the work is done |
| Stop hook | The previous turn finishes | Your own script or prompt decides |

`/goal` and a Stop hook "both fire after every turn"; `/goal` is session-scoped and
type-and-go, where a Stop hook lives in settings, applies across sessions, and can run a
script for deterministic checks instead of a model-evaluated one. Scheduled work (cloud
routines, desktop scheduled tasks) is explicitly a different axis — it "runs independent of
any open session," unlike all three session-keepalive approaches above.

`/goal` "works in non-interactive mode, in the desktop app, and through Remote Control."
`claude -p "/goal <condition>"` runs the loop to completion in one invocation; with the
default text output "a goal that runs many turns can look stuck" since only the final response
prints, so the docs recommend `--output-format stream-json --verbose` to see each message as
it runs. Ctrl+C interrupts a non-interactive goal before it resolves.

**Subagents**: the docs state only that a running subagent (like a running background shell)
defers evaluation for that turn, and the v2.1.143 CHANGELOG entry above independently confirms
"delegated subagents" as one of the two deferral triggers. **Nothing in the docs page or the
CHANGELOG describes setting, checking, or clearing a `/goal` from inside a subagent itself** —
that is a documented absence, not inferred.

## Version Gate and Availability

| Version | What changed | Source |
|---|---|---|
| v2.1.139 | `/goal` added | CHANGELOG: `` Added `/goal` command: set a completion condition and Claude keeps working across turns until it's met. Works in interactive, `-p`, and Remote Control. Shows live elapsed/turns/tokens as an overlay panel `` |
| v2.1.234 | Background check-ins require this or later | docs page; CHANGELOG |
| v2.1.236 | Idle check-ins require this or later | docs page; CHANGELOG |
| v2.1.239 | `claude --resume` picker restores an active goal (previously the one resume route that didn't) | docs page; CHANGELOG |
| v2.1.246 | Idle check-ins capped at three per goal between prompts (previously uncapped) | docs page; CHANGELOG |
| v2.1.269 | Interactive sessions print retry/pause notices naming the cause | docs page; CHANGELOG |
| v2.1.274 | Fixed losing an active goal across a compacted resume, and a post-compaction overflow ending the turn instead of compacting | CHANGELOG |

**Plans and platforms**: the docs page does not state a Claude plan gate (Pro/Max/Team/
Enterprise) for `/goal` — this is an undocumented absence, not confirmed either way. Documented
platforms are interactive sessions, `-p`, the desktop app, and Remote Control; a cloud/web
session is mentioned only inside the auth-failure carve-out — "When a host manages them for
you, such as the desktop app or a cloud session, Claude Code leaves the goal active because
the host restores access on its own" — not listed as a generally supported route alongside the
other four.

**Requirements**: `/goal` is gated by "the same workspace trust rule as hooks in settings
files," because the evaluator is part of the hooks system. It is also unavailable when
`disableAllHooks` is `true` (after settings precedence) or `allowManagedHooksOnly` is set in
managed settings — in each case "the command tells you why instead of silently doing nothing."

## Limitations (as stated)

- The evaluator **cannot run commands or read files** — it judges only what Claude has already
  surfaced in the conversation, so a condition must be provable from Claude's own output.
- Condition text is capped at **4,000 characters**.
- **One goal per session**; a new `/goal` replaces an active one rather than queuing.
- `/goal` **does not change permission mode** — Manual mode still prompts.
- A no-progress loop (answering the evaluator without tool use) pauses the loop and returns
  control, but leaves the goal set rather than clearing it.
- Only four specific failure classes clear the goal outright; everything else retries or
  pauses rather than failing permanently or retrying forever.

## Relation to Long-Running / Unattended-Session Work in This Corpus

- [CC-loop-cron-analysis.md](../configuration/CC-loop-cron-analysis.md) — `/loop`'s own
  internals (`CronCreate`/`List`/`Delete`, durable vs. session-only jobs, the `-p`-mode
  exit-after-first-iteration bug); the docs page's own comparison table (above) is the
  first-party complement to that empirical write-up.
- [CC-hooks-system-analysis.md](../configuration/CC-hooks-system-analysis.md) — the Stop-hook
  mechanism `/goal` wraps; this doc covers hook events/configuration generally.
- [CC-session-keepalive-analysis.md](CC-session-keepalive-analysis.md) — keeping a session
  *alive* (not killed by the OS/terminal/host) across environments; complementary to `/goal`,
  which keeps a live session *working* rather than idle.
- [CC-web-scheduled-tasks-analysis.md](../ci-remote/CC-web-scheduled-tasks-analysis.md) —
  the scheduled-work axis the docs page explicitly distinguishes from all three
  session-keepalive approaches above.

**Design-lens note**: `/goal`'s evaluator re-judges a plain-text condition against the
conversation transcript after every turn, with no persistent artifact of its own beyond that
transcript. This workspace's own unattended-execution rule (a local operating convention, not
part of this repo) instead persists state as a plan file with a per-item done-when, so
progress and gating survive outside any single session or model call. This is a design-lens
comparison only — not a claim that one supersedes the other — since the rule's plan-file
discipline targets multi-PR arcs, while `/goal` targets a single session's turn loop.

## Sources

| Source | Content |
|---|---|
| [code.claude.com/docs/en/goal][goal-docs] | `/goal` command: mechanism, lifecycle, requirements, limitations |
| [CC CHANGELOG][changelog-raw] (v2.1.139, v2.1.143, v2.1.234, v2.1.236, v2.1.239, v2.1.246, v2.1.269, v2.1.274) | Version gates for `/goal`'s introduction and subsequent lifecycle fixes |

[goal-docs]: https://code.claude.com/docs/en/goal
[changelog-raw]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
[stop-hook]: https://code.claude.com/docs/en/hooks#prompt-based-hooks
[model-config]: https://code.claude.com/docs/en/model-config
[auto-mode-config]: https://code.claude.com/docs/en/auto-mode-config
[env-vars]: https://code.claude.com/docs/en/env-vars
