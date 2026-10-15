---
title: CC Web Scheduled Tasks — Cloud Recurring Automation
source: https://code.claude.com/docs/en/routines
purpose: Analysis of cloud-native scheduled tasks for recurring autonomous work without local machine dependency.
created: 2026-03-24
updated: 2026-10-15
validated_links: 2026-10-15
status: available
---

**Details:** Available (all CC Web users — Pro, Max, Team, Enterprise). Vendor marks the underlying feature as **research preview** — behavior, limits, and API surface may change.

> **Note**: Anthropic renamed this feature to **Routines** (canonical page: [routines][cc-sched], H1 "Automate work with routines"). A routine now supports three trigger types — Schedule, API (HTTP POST to a per-routine `/fire` endpoint), and GitHub event (PR/release webhooks) — not only recurring schedules. This doc covers only the **Schedule-trigger** subset of Routines.
>
> **URL-slug trap, found 2026-10-15**: the old `scheduled-tasks` URL slug this doc's title echoes has been repurposed. `https://code.claude.com/docs/en/scheduled-tasks` is now Anthropic's page for the **session-scoped `/loop` command and its `CronCreate`/`CronList`/`CronDelete` tools** — a different, local feature, covered in [CC-loop-cron-analysis.md](../configuration/CC-loop-cron-analysis.md) — not the cloud Routines this doc covers. Follow the `routines` URL, not `scheduled-tasks`, for the content below.

## What It Is

Recurring prompts that run on Anthropic cloud infrastructure on a schedule. Tasks keep working even when your computer is off — no persistent terminal or local machine needed. Each run clones the repo fresh and creates a session you can review.

### Compare Scheduling Options

| Aspect | Cloud (this doc) | Desktop | `/loop` |
|--------|-----------------|---------|---------|
| Runs on | Anthropic cloud | Your machine | Your machine |
| Requires machine on | No | Yes | Yes |
| Requires open session | No | No | Yes |
| Persistent across restarts | Yes | Yes | Restored on `--resume` if unexpired |
| Access to local files | No (fresh clone) | Yes | Yes |
| MCP servers | Connectors per task | Config files + connectors | Inherits from session |
| Permission prompts | No (runs autonomously) | Configurable per task | Inherits from session |
| Customizable schedule | Via `/schedule update` in the CLI | Yes | Yes |
| Minimum interval | 1 hour | 1 minute | 1 minute |

For `/loop` details, see [CC-loop-cron-analysis.md](../configuration/CC-loop-cron-analysis.md).

### Creating a Scheduled Task

Three entry points:

1. **Web**: [claude.ai/code/routines](https://claude.ai/code/routines) → New routine
2. **Desktop**: Routines (sidebar) → New routine → choose **Cloud** (choosing **Local** creates a Desktop scheduled task instead)
3. **CLI**: `/schedule` (guided) or `/schedule daily PR review at 9am` — also available under the alias `/routines`

### Configuration

| Setting | Details |
|---------|---------|
| **Prompt** | Self-contained instructions (runs autonomously, no steering) |
| **Model** | Selectable per task |
| **Repositories** | One or more GitHub repos; cloned fresh each run from default branch (or from a triggering PR's head commit, if it's the first repo and a GitHub PR event fired the run) |
| **Branch permissions** | Claude pushes to a `claude/`-prefixed branch by default, unless the routine's prompt directs it elsewhere; GitHub branch protection rules/rulesets are the documented way to restrict which branches a run can push to. (Checked 2026-10-15: the current docs no longer describe a per-repo "Allow unrestricted" toggle this doc previously cited — removed as unverifiable against the live page.) |
| **Environment** | Cloud environment (network access, env vars, setup script) — see [cloud sessions](CC-cloud-sessions-analysis.md#environment-configuration) |
| **Connectors** | MCP connectors (Slack, Linear, Google Drive, etc.) — all included by default |
| **Schedule** | Hourly, Daily, Weekdays, Weekly. Custom intervals via `/schedule update` |

### Frequency Options

| Frequency | Behavior |
|-----------|----------|
| Hourly | Every hour |
| Daily | Once/day at specified time (default 9:00 AM local) |
| Weekdays | Daily, skipping Saturday/Sunday |
| Weekly | Once/week on specified day and time |

A run can start several minutes after its scheduled time — the live page gives no fixed/deterministic offset for routines (that "consistent, deterministic delay" wording belongs to Desktop scheduled tasks, a different feature, and this doc previously borrowed it in error). If timing on the hour matters, the docs suggest picking a time a few minutes past the hour, e.g. 9:07 instead of 9:00, to start closer to on-time.

### One-off Runs

A schedule trigger can also fire a routine a single time at a specific future timestamp instead of recurring, e.g. `/schedule tomorrow at 9am, summarize yesterday's merged PRs` or `/schedule in 2 weeks, open a cleanup PR that removes the feature flag`. After it fires, the trigger auto-disables and the web UI marks the routine **Ran**; editing the routine with a new one-off time re-arms it. One-off runs count against the same hourly limits as other scheduled runs (below).

### Usage Limits

Found 2026-10-15, not previously in this doc. Separately from subscription usage, each way of starting a run has its own hourly cap: scheduled runs (including one-off runs) are capped at 100/hour per account; **Run now**, API fires, and re-arming a one-off routine share a 30/hour cap per routine; **Run now** and re-arming are also capped at 100/hour per account; and API fires are capped at 100/hour per account, counted separately from **Run now**. None of these caps has overage — a run over the limit waits or fails until the window resets. If a GitHub connection goes missing or expires, a routine skips runs for up to 72 hours before it turns itself off; reconnecting GitHub within that window resumes it automatically.

### Managing Tasks

- **Run now**: trigger immediately from task detail page
- **Pause/resume**: toggle in Repeats section
- **Edit**: change prompt, schedule, repos, environment, connectors
- **Delete**: removes task; past run sessions remain
- **CLI**: `/schedule list`, `/schedule update`, `/schedule run`; CC v2.1.227+ also answers natural-language questions about run history, e.g. `/schedule why did my nightly review do nothing this morning?`, by reading a run's log for tool errors, permission denials, and the final result

## Use Cases

| Use Case | Example |
|----------|---------|
| PR review | Review open PRs each morning |
| CI failure triage | Analyze overnight failures, surface summaries |
| Doc sync | Update documentation after PRs merge |
| Dependency audit | Weekly security/update scan |
| Cross-repo validation | `make validate` across multiple repos on weekday mornings |

### Decision Rule

**Use cloud scheduled tasks for recurring autonomous work that should run reliably without your machine. Use Desktop scheduled tasks when you need local files/tools. Use `/loop` for quick polling within a session.**

## Scored on the Agent Substrate Rubric

Routines (the Schedule-trigger subset this doc covers), scored 2026-10-02 against the [agent substrate rubric][rubric] from the current [Routines][cc-sched] docs, re-fetched this date. This fills a long-running coverage gap plan 0009 named: no rubric row existed for scheduled tasks. Distributed reuses the evidence already scored for [cloud sessions][cloud-sessions-rubric], since every routine run executes as one.

`subject: long-running`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no [cc-sched][cc-sched] ("Routines belong to your individual claude.ai account. They are not shared with teammates, and their runs count against your account's usage and limits") | yes [cloud-sessions-rubric][cloud-sessions-rubric] (every run executes as a cloud session, on the same Anthropic-managed or self-hosted runner-fleet infrastructure scored there) | no [cc-sched][cc-sched] (the creation form has "a model selector," and "Claude uses the selected model on every run" — a named model, not a pinned snapshot id; the rubric's own guidance treats LLM-driven work with no fixed model/version as `no`, not `no data`) | yes [cc-sched][cc-sched] ("change the name, prompt, repositories, environment, connectors, or any of the routine's triggers" at any time, with no rebuild — re-verified verbatim 2026-10-15) | partial [cc-sched][cc-sched] (each run opens as its own session, independent of the routine, that you can rename, archive, or delete from the session's own menu — but the routine's own prompt/config carries no revision history or rollback of its own; the current page no longer states what happens to past run sessions when the routine itself is deleted, so that specific claim from an earlier pass of this doc is dropped as unverified) | partial [cc-sched][cc-sched] (each run is a full, reviewable session, and the CLI can read a run's log to "explain what happened, including tool errors, permission denials, and the final result" on request, requires CC v2.1.227+ — but "a green status... does not mean the task in your prompt succeeded," so nothing short of opening the transcript closes the loop) |

Re-verified against the live [Routines][cc-sched] page 2026-10-15. Trigger types, the core frequency presets, and the minimum one-hour interval still match; the comparison table gained two rows (Permission prompts, Customizable schedule — added above), one-off scheduled runs and per-action hourly limits were net-new and are now covered above, the Branch permissions row's "Allow unrestricted" toggle claim is no longer supported by the live page and was removed, and the Adaptable and Versionable rubric cells needed verbatim-quote or evidence corrections (both fixed above).

## See Also

- [CC-cloud-sessions-analysis.md](CC-cloud-sessions-analysis.md) — cloud VM execution model (shared infrastructure)
- [CC-loop-cron-analysis.md](../configuration/CC-loop-cron-analysis.md) — session-scoped `/loop` command
- [CC-github-actions-analysis.md](CC-github-actions-analysis.md) — GH Actions as alternative scheduling
- [CC-web-auth-setup-analysis.md](CC-web-auth-setup-analysis.md) — authentication for web features

## References

- [CC Web Scheduled Tasks docs][cc-sched]
- [CC Cloud Environment docs][cc-cloud]
- [CC Desktop Scheduled Tasks docs][cc-desktop]
- [Agent Substrate Rubric][rubric]

[cc-sched]: https://code.claude.com/docs/en/routines
[cc-cloud]: https://code.claude.com/docs/en/claude-code-on-the-web#the-cloud-environment
[cc-desktop]: https://code.claude.com/docs/en/desktop-scheduled-tasks
[rubric]: ../../sdlc-lcm/agent-substrate-rubric.md
[cloud-sessions-rubric]: CC-cloud-sessions-analysis.md#scored-on-the-agent-substrate-rubric
