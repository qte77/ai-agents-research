---
title: CC /loop Command and Cron System Analysis
source: https://code.claude.com/docs/en/scheduled-tasks, gist by @sorrycc (v2.1.71 cli.js decompilation), empirical testing (cc-recursive-team-mode, 2026-03-23)
purpose: Analysis of the /loop slash command for recurring autonomous tasks, its CronCreate/List/Delete internals, and comparison with external scheduling approaches. Includes empirical finding that /loop accepts syntax in -p mode but exits after first iteration.
created: 2026-03-17
updated: 2026-10-18
validated_links: 2026-10-18
status: generally-available
---

**Details:** v2.1.71+, feature gate `tengu_kairos_cron` (polled every 5 min) — original gist-sourced finding, unconfirmed against first-party docs, which don't document internal feature gates. The feature now has an official first-party page, [Run prompts on a schedule][cc-sched-loop] ("`/loop` and the cron scheduling tools"), re-checked 2026-10-15; most of this doc's original gist/cli.js-decompilation and empirical findings are superseded or substantially extended below. The URL slug `scheduled-tasks` is this feature's own page — it is **not** the cloud Routines feature documented in [CC-web-scheduled-tasks-analysis.md](../ci-remote/CC-web-scheduled-tasks-analysis.md), which lives at the different URL `/docs/en/routines`.

## What `/loop` Is

Built-in slash command (a [bundled skill][bundled-skills]) that schedules recurring prompts within an
**interactive** CC session:

```text
/loop 5m check if the deployment finished
/loop 20m /code-review 1234
/loop 1h run make test and report results
/loop check the build every 2 hours
```

What you provide determines how the loop behaves ([source][cc-sched-loop]):

| What you provide | Example | What happens |
|---|---|---|
| Interval and prompt | `/loop 5m check the deploy` | Runs on a fixed cron schedule |
| Prompt only | `/loop check the deploy` | Runs at an interval **Claude chooses dynamically** each iteration (1 minute to 1 hour, based on what it observed) |
| Interval only, or nothing | `/loop` | The built-in maintenance prompt runs (continue unfinished work, tend to the current branch's PR, then cleanup passes), or a project's own `loop.md` if one exists |

This supersedes this doc's earlier claim of a flat **"default interval: 10 minutes"** — no such default exists in the current docs; omitting the interval now means Claude self-paces instead.

- **Units**: `s`/`m`/`h`/`d` -- natural language intervals also work (e.g. `every 2 hours`); seconds round up to the nearest minute (cron's 1-minute granularity), and odd intervals like `7m` round to the nearest clean cron step
- **Max**: 50 scheduled jobs per session (unchanged, re-confirmed 2026-10-15)
- **Feature gate**: `tengu_kairos_cron` — see the Details line above
- **Self-paced loops appear in the task list** like any fixed-interval one, so `CronList`/cancellation work the same way; they're also subject to the 7-day expiry below
- **`/loop 20m /code-review 1234`-style skill re-runs** only execute skills Claude is [allowed to invoke on its own][skill-invocation]; built-in commands (`/permissions`, `/model`, `/clear`), `disable-model-invocation: true` skills, skills withheld by a `skillOverrides` setting or a `Skill` deny rule, and MCP prompts (`/mcp__server__name`) instead reach Claude as plain text on a scheduled fire
- A session with the [Monitor tool available][monitor-tool] may use it directly for a dynamic `/loop` request instead of polling — streaming a background script's output back is often more token-efficient and responsive than re-running a prompt on an interval

### Customize the default prompt with `loop.md`

A bare `/loop` (no prompt) runs a built-in maintenance prompt unless a project defines `.claude/loop.md` (project-level, takes precedence) or `~/.claude/loop.md` (user-level) — plain Markdown, written as if typing the `/loop` prompt directly, truncated past 25,000 bytes. Edits take effect on the next iteration. `loop.md` sets a single default prompt for bare `/loop` only; Claude Code ignores it whenever a prompt is supplied on the command line ([source][cc-sched-loop]).

[bundled-skills]: https://code.claude.com/docs/en/skills#bundled-skills
[skill-invocation]: https://code.claude.com/docs/en/skills#control-who-invokes-a-skill
[monitor-tool]: https://code.claude.com/docs/en/tools-reference#monitor-tool

## Implementation

Under the hood, `/loop` is syntactic sugar over internal tools, officially documented as of 2026-10-15 ([source][cc-sched-loop]):

- `CronCreate` -- schedule a new task; takes a 5-field cron expression, the prompt to run, and whether it recurs or fires once
- `CronList` -- list scheduled tasks with their IDs, schedules, next run times (next-run times require CC v2.1.299+), and prompts
- `CronDelete` -- cancel a task by its 8-character ID
- `ScheduleWakeup` -- used internally by a **self-paced** loop to schedule its next wakeup, or to end the loop by calling it with `stop: true`. If an iteration ends without rescheduling or stopping, Claude Code schedules one fallback wakeup ~20 minutes later and ends the loop if that iteration doesn't reschedule either.

These tools are available to the model within the session but are not exposed
as user-facing slash commands beyond `/loop`; ask Claude in natural language
("what scheduled tasks do I have?", "cancel the deploy check job") to reach them indirectly.

### Durable vs session-only jobs — revised 2026-10-15, evidence is mixed, not a clean supersession

This doc originally reported, from @anthropic-ai/claude-code@2.1.88 cli.js
decompilation (2026-03-31), that `CronCreate` took an undocumented `durable: true`
parameter gating whether a job survived a CC restart, with the `/loop` skill
creating session-only jobs by default. **The current first-party page describes a
different default, with no `durable` parameter named** ([source][cc-sched-loop]):

- Tasks are session-scoped, but on `--resume`/`--continue`, Claude Code restores
  **every** task scheduled with `CronCreate` by default, **except**: recurring
  tasks that have [expired](#seven-day-expiry) (7 days), one-shot tasks whose
  fire time has passed, and a **self-paced `/loop`** specifically (which is never
  restored — run `/loop` again to restart it). Background Bash and Monitor tasks
  are never restored on resume, either.
- With [feature-flag fetching][feature-flags] turned **off**, Claude Code
  "stores a task **you asked to keep across sessions**" in the project's
  `.claude/scheduled_tasks.json` (quoted verbatim, [source][cc-sched-loop] —
  returns an error instead of scheduling if `.claude` or that file is a symlink);
  a saved task only runs in the project folder where it was created — copying the
  file into a new worktree lists the tasks there but doesn't run them.

Whether a `durable: true`-style opt-in still exists as an internal, undocumented
`CronCreate` parameter is **unverified** at this 2026-10-15 re-check, and the
evidence is mixed rather than cleanly superseding the original finding: resume-
restoration is now documented as the *default* for everything but self-paced
loops and expired/past-due tasks, which is new and not what the gist-based
finding described — but the page's own phrase "a task **you asked to keep
across sessions**" (quoted above) still implies *some* distinct, opt-in form of
cross-session persistence, under a name and mechanism the public page doesn't
specify. Read the two bullets above as: ordinary resume-restoration no longer
needs an opt-in, but the page leaves room for a separate, still-undocumented
"keep across sessions" request that may be what the gist's `durable: true` named.
Re-confirm against a current build before relying on either reading.

[feature-flags]: https://code.claude.com/docs/en/env-vars#features-that-need-feature-flag-fetching

### State Files

- **`scheduled_tasks.json`** — job definitions (in `.claude/`), written specifically when [feature-flag fetching][feature-flags] is off ([source][cc-sched-loop]); whether it is also used with fetching on is unverified (see above)
- **`scheduled_tasks.lock`** — mutex preventing concurrent sessions from firing
  the same job. Contains `sessionId`, `pid`, `acquiredAt`. CC checks if the
  holding PID is alive before honoring the lock. *(Original gist/empirical
  finding; the current first-party page doesn't mention a lock file either way.)*

**Known bug**: `scheduled_tasks.lock` is written to `.claude/` in the working
tree instead of `~/.claude/`, polluting the repo with ephemeral runtime state.
Not gitignored by default.

- [#32108][gh-32108] — lock written to main repo instead of worktree
- [#33565][gh-33565] — should be globally gitignored

**Workaround**: Add `.claude/scheduled_tasks.lock` to `.gitignore`.

[gh-32108]: https://github.com/anthropics/claude-code/issues/32108
[gh-33565]: https://github.com/anthropics/claude-code/issues/33565

## Critical Limitation: Session-Bound Only

**`/loop` accepts syntax in `-p` mode but does not persist.** The session exits
after the first iteration, killing the cron scheduler. The cron job is created
(with a job ID and auto-expiry), the first prompt executes, but subsequent fires
never happen because the process is gone.

*Re-check 2026-10-15*: this finding is from CC v2.1.81 (2026-03), six months and
many releases before this re-check, and the current first-party page states the
general rule only in session-exit terms — "Tasks only fire while Claude Code is
running and idle. Closing the terminal or letting the session exit stops them
firing" — without calling out `-p` mode specifically. Since `-p` mode's own
contract is to run one turn and exit, this is the expected consequence of `-p`
itself rather than a `/loop`-specific bug, but the exact behavior (job created
then immediately orphaned, vs. refused outright) is unverified against a current
build; re-test before relying on it.

The current page also documents an official workaround this doc didn't have
before: **backgrounding the session** — see [Agent view][agent-view] — "carries
`/loop` tasks over to a background session, which keeps running without a
terminal" ([source][cc-sched-loop]). That is a different mechanism from `-p` (it
keeps an interactive session alive off-screen rather than running one autonomous
turn), but it is the documented way to run `/loop` unattended without a foreground
terminal.

[agent-view]: https://code.claude.com/docs/en/agent-view#from-inside-a-session

Tested 2026-03-23 (CC v2.1.81), lock file confirmed 2026-03-25 (CC v2.1.83):

```bash
# APPEARS TO WORK but exits after first iteration
$ claude -p "/loop say hi every 30 seconds"
# Output: "Scheduled. Every 1 minute (rounded up from 30s)..."
# Then: "Hi!"
# Then: process exits — cron job dies with session

# WORKS -- interactive session persists for recurring fires
claude --dangerously-skip-permissions
# then inside the session:
/loop 5m check deploy
```

**Key detail**: `/loop` rounds intervals up to 1-minute minimum (cron
granularity).

### Seven-day expiry

Recurring tasks auto-expire 7 days after creation — unchanged, re-confirmed 2026-10-15. The task fires one final time, then deletes itself. A self-paced loop is also subject to this expiry. For longer-lived recurring work, cancel and recreate before expiry, or use [Routines](../ci-remote/CC-web-scheduled-tasks-analysis.md) or Desktop scheduled tasks instead.

### Disable the scheduler

Set `CLAUDE_CODE_DISABLE_CRON=1` in the environment to disable the scheduler entirely: the cron tools and `/loop` become unavailable, and any already-scheduled tasks stop firing ([source][cc-sched-loop]).

### Stop a loop

To stop a **self-paced** `/loop` while it waits for its next iteration, press `Esc` — this clears the pending wakeup so it doesn't fire again. A fixed-interval loop, or one scheduled by asking Claude directly, isn't affected by `Esc` and keeps running until cancelled ([source][cc-sched-loop]) or the 7-day expiry above.

## `/loop` + `--dangerously-skip-permissions`

This combination works in interactive mode and is the most autonomous CC
configuration:

```bash
# Start interactive session with no permission checks
claude --dangerously-skip-permissions
# Inside session:
/loop 5m /code-review 1234
/loop 10m run make test and fix any failures
/loop 1h check CI status and report
```

Each loop iteration fires with full bypass permissions -- Claude can read,
write, execute, and network without any prompts. See
[CC-permissions-bypass-analysis.md](../sandboxing/CC-permissions-bypass-analysis.md)
for security implications.

## Comparison: `/loop` vs Ralph Loop vs GitHub Actions

| Feature | `/loop` | Ralph (`claude -p` loop) | GitHub Actions |
|---|---|---|---|
| State persistence | Session-scoped; restored on `--resume`/`--continue` except a self-paced loop, expired recurring tasks, and past-due one-shot tasks (see [Durable vs session-only jobs](#durable-vs-session-only-jobs--revised-2026-10-15-evidence-is-mixed-not-a-clean-supersession) above) | External files (prd.json, git) | Workflow artifacts |
| Context management | Single accumulating context | Fresh context per iteration | Fresh per run |
| TDD enforcement | None | Built-in | Custom |
| Story dependencies | None | `depends:` in prd.json | `needs:` in workflow |
| Permission control | Inherits session mode | Per-invocation flag | Per-step |
| Survives disconnection | No from a foreground terminal; yes if the session is [backgrounded](#critical-limitation-session-bound-only) first | Yes (script continues) | Yes (cloud) |
| Nested teams | Yes (if teams enabled) | N/A (subprocess) | N/A |
| Best for | Monitoring, polling, light automation | Structured multi-story dev | CI/CD, scheduled builds |

See [CC-ralph-enhancement-research.md](../agents-skills/CC-ralph-enhancement-research.md)
for Ralph loop details and
[CC-github-actions-analysis.md](../ci-remote/CC-github-actions-analysis.md)
for GitHub Actions integration.

## Practical Patterns

**Deploy monitoring:**

```text
/loop 5m check if the deployment on staging finished. If it did, run the smoke tests and report results.
```

**PR babysitting:**

```text
/loop 10m check PR #42 CI status. If all checks pass, post "Ready for review" comment.
```

**Iterative code review:**

```text
/loop 20m /code-review src/app/
```

## When to Use `/loop` vs External Schedulers

**Use `/loop` when:**

- Task is monitoring/polling (deployment status, CI checks, PR reviews)
- Single session is acceptable (no disconnection survival needed)
- Context accumulation is desired (each iteration builds on previous)
- Quick setup matters more than durability

**Use external schedulers (cron, GitHub Actions, Ralph) when:**

- Task must survive disconnection or machine sleep
- Fresh context per iteration is preferred (prevents context rot)
- Structured workflows with dependencies are needed
- Audit trail or artifact persistence is required

## Sources

| Source | Content |
|---|---|
| [Run prompts on a schedule][cc-sched-loop] | Official first-party page (found 2026-10-15): self-paced loops, `loop.md`, `CronCreate`/`CronList`/`CronDelete`/`ScheduleWakeup`, resume-restore rules, 7-day expiry, `CLAUDE_CODE_DISABLE_CRON`, skill-invocation reach rules |
| gist by @sorrycc (v2.1.71 cli.js decompilation) | Original `/loop` internals, feature gate, and the `durable: true` claim this doc's 2026-10-15 pass found only partly corroborated — see [Durable vs session-only jobs](#durable-vs-session-only-jobs--revised-2026-10-15-evidence-is-mixed-not-a-clean-supersession) |
| [Official agent teams docs](https://code.claude.com/docs/en/agent-teams) | Permission inheritance for recurring tasks |

[cc-sched-loop]: https://code.claude.com/docs/en/scheduled-tasks
