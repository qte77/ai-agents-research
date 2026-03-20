# .github/ — CI Automation

Automated monitors track Claude Code changes, community content, and platform status, then open triage PRs for human review.

```text
Sources (Statuspage API, CC CHANGELOG, blogs, Reddit, X)
  → Cron workflows → Python scripts → Triage PRs
```

## Monitors

| Workflow | Schedule | Sources | Output |
|---|---|---|---|
| [`cc-status-monitor`](workflows/cc-status-monitor.yaml) | Every 4h | Statuspage API | `triage/status-monitor/outages.jsonl` + `outage-stats.md` |
| [`cc-changelog-monitor`](workflows/cc-changelog-monitor.yaml) | Mon 09:00 UTC | CC CHANGELOG, Anthropic blog, GitHub issues | `triage/cc-changelog/` timestamped reports |
| [`cc-changelog-community-monitor`](workflows/cc-changelog-community-monitor.yaml) | Mon 10:00 UTC | claudelog.com, awesome-claude-code, Reddit, X | `triage/community/` timestamped reports |

**Manual trigger:** `gh workflow run <workflow>.yaml [--ref <branch>]`

## Key conventions

- **Scripts** (`scripts/`): stdlib-only Python. Exit `0` = no changes, `1` = new content → PR created.
- **State** (`state/`): JSON cursor files ("last seen"). Committed with triage PRs to persist across runs.
- **Composite action** (`actions/create-triage-pr/`): Used by all 3 monitors. Pass `skip-report: 'true'` to skip timestamped report copy (status monitor).

## Adding a new monitor

1. Add script in `scripts/` following exit code convention
2. Add workflow in `workflows/` with cron schedule
3. Use `create-triage-pr` action for output (`skip-report: 'true'` if no timestamped report needed)
4. Add state file to `state/` if the script needs cursor tracking
