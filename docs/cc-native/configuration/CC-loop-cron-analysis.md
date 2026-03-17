---
title: CC /loop Command and Cron System Analysis
source: https://code.claude.com/docs/en/slash-commands (inferred), gist by @sorrycc (v2.1.71 cli.js decompilation)
purpose: Analysis of the /loop slash command for recurring autonomous tasks, its CronCreate/List/Delete internals, and comparison with external scheduling approaches.
created: 2026-03-17
updated: 2026-03-17
---

**Status**: Generally available (v2.1.71+, feature gate `tengu_kairos_cron`)

## What `/loop` Is

Built-in slash command that schedules recurring prompts within an **interactive**
CC session:

```text
/loop 5m check if the deployment finished
/loop 20m /review-pr 1234
/loop 1h run make test and report results
/loop check the build every 2 hours
```

- **Default interval**: 10 minutes
- **Units**: seconds, minutes, hours, days -- natural language intervals also work
- **Max**: 50 scheduled jobs per session
- **Feature gate**: `tengu_kairos_cron` (polled every 5 min)

## Implementation

Under the hood, `/loop` is syntactic sugar over three internal tools:

- `CronCreate` -- schedule a recurring prompt
- `CronList` -- view active schedules
- `CronDelete` -- remove a schedule

These tools are available to the model within the session but are not exposed
as user-facing slash commands beyond `/loop`.

## Critical Limitation: Session-Bound Only

**`/loop` is incompatible with `-p` (print mode).** Print mode exits on
completion -- there's no persistent session for the cron scheduler to fire in.
`/loop` only works in interactive terminal sessions.

```bash
# DOES NOT WORK -- -p exits immediately, /loop never fires
claude --dangerously-skip-permissions -p "/loop 5m check deploy"

# WORKS -- interactive session with bypass
claude --dangerously-skip-permissions
# then inside the session:
/loop 5m check deploy
```

## `/loop` + `--dangerously-skip-permissions`

This combination works in interactive mode and is the most autonomous CC
configuration:

```bash
# Start interactive session with no permission checks
claude --dangerously-skip-permissions
# Inside session:
/loop 5m /review-pr 1234
/loop 10m run make test and fix any failures
/loop 1h check CI status and report
```

Each loop iteration fires with full bypass permissions -- Claude can read,
write, execute, and network without any prompts. See
[CC-permissions-bypass-analysis.md](../ci-execution/CC-permissions-bypass-analysis.md)
for security implications.

## Comparison: `/loop` vs Ralph Loop vs GitHub Actions

<!-- markdownlint-disable MD013 -->

| Feature | `/loop` | Ralph (`claude -p` loop) | GitHub Actions |
|---|---|---|---|
| State persistence | Session only (lost on exit) | External files (prd.json, git) | Workflow artifacts |
| Context management | Single accumulating context | Fresh context per iteration | Fresh per run |
| TDD enforcement | None | Built-in | Custom |
| Story dependencies | None | `depends:` in prd.json | `needs:` in workflow |
| Permission control | Inherits session mode | Per-invocation flag | Per-step |
| Survives disconnection | No | Yes (script continues) | Yes (cloud) |
| Nested teams | Yes (if teams enabled) | N/A (subprocess) | N/A |
| Best for | Monitoring, polling, light automation | Structured multi-story dev | CI/CD, scheduled builds |

<!-- markdownlint-enable MD013 -->

See [CC-ralph-enhancement-research.md](../agents-skills/CC-ralph-enhancement-research.md)
for Ralph loop details and
[CC-github-actions-analysis.md](../ci-execution/CC-github-actions-analysis.md)
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

<!-- markdownlint-disable MD013 -->

| Source | Content |
|---|---|
| gist by @sorrycc (v2.1.71 cli.js decompilation) | `/loop` internals, CronCreate/List/Delete tools, feature gate |
| [Official agent teams docs](https://code.claude.com/docs/en/agent-teams) | Permission inheritance for recurring tasks |

<!-- markdownlint-enable MD013 -->
