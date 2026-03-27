---
title: CC Web Scheduled Tasks — Cloud Recurring Automation
source: https://code.claude.com/docs/en/web-scheduled-tasks
purpose: Analysis of cloud-native scheduled tasks for recurring autonomous work without local machine dependency.
created: 2026-03-24
updated: 2026-03-24
validated_links: 2026-03-24
---

**Status**: Available (all CC Web users — Pro, Max, Team, Enterprise)

## What It Is

Recurring prompts that run on Anthropic cloud infrastructure on a schedule. Tasks keep working even when your computer is off — no persistent terminal or local machine needed. Each run clones the repo fresh and creates a session you can review.

### Compare Scheduling Options

| Aspect | Cloud (this doc) | Desktop | `/loop` |
|--------|-----------------|---------|---------|
| Runs on | Anthropic cloud | Your machine | Your machine |
| Requires machine on | No | Yes | Yes |
| Requires open session | No | No | Yes |
| Persistent across restarts | Yes | Yes | No (session-scoped) |
| Access to local files | No (fresh clone) | Yes | Yes |
| MCP servers | Connectors per task | Config files + connectors | Inherits from session |
| Minimum interval | 1 hour | 1 minute | 1 minute |

For `/loop` details, see [CC-loop-cron-analysis.md](../configuration/CC-loop-cron-analysis.md).

### Creating a Scheduled Task

Three entry points:

1. **Web**: [claude.ai/code/scheduled](https://claude.ai/code/scheduled) → New scheduled task
2. **Desktop**: Schedule page → New task → New remote task
3. **CLI**: `/schedule` (guided) or `/schedule daily PR review at 9am`

### Configuration

| Setting | Details |
|---------|---------|
| **Prompt** | Self-contained instructions (runs autonomously, no steering) |
| **Model** | Selectable per task |
| **Repositories** | One or more GitHub repos; cloned fresh each run from default branch |
| **Branch permissions** | Default: `claude/`-prefixed branches only. Toggle "Allow unrestricted" per repo |
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

Tasks may run a few minutes after scheduled time (consistent offset per task).

### Managing Tasks

- **Run now**: trigger immediately from task detail page
- **Pause/resume**: toggle in Repeats section
- **Edit**: change prompt, schedule, repos, environment, connectors
- **Delete**: removes task; past run sessions remain
- **CLI**: `/schedule list`, `/schedule update`, `/schedule run`

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

## See Also

- [CC-cloud-sessions-analysis.md](CC-cloud-sessions-analysis.md) — cloud VM execution model (shared infrastructure)
- [CC-loop-cron-analysis.md](../configuration/CC-loop-cron-analysis.md) — session-scoped `/loop` command
- [CC-github-actions-analysis.md](CC-github-actions-analysis.md) — GH Actions as alternative scheduling
- [CC-web-auth-setup-analysis.md](CC-web-auth-setup-analysis.md) — authentication for web features

## References

- [CC Web Scheduled Tasks docs][cc-sched]
- [CC Cloud Environment docs][cc-cloud]
- [CC Desktop Scheduled Tasks docs][cc-desktop]

[cc-sched]: https://code.claude.com/docs/en/web-scheduled-tasks
[cc-cloud]: https://code.claude.com/docs/en/claude-code-on-the-web#cloud-environment
[cc-desktop]: https://code.claude.com/docs/en/desktop#schedule-recurring-tasks
