---
title: CC Subagent Session Artifacts
purpose: Reference for subagent session artifacts — worktree lifecycle, meta.json tombstones, transcript storage, and cleanup behavior.
created: 2026-04-13
updated: 2026-04-13
validated_links: 2026-04-13
status: research
---

## What It Is

When Claude Code spawns subagents via the Agent tool, each subagent produces session artifacts: transcripts, worktree directories (if isolated), and metadata files. This doc covers the artifact structure, worktree lifecycle, and cleanup behavior.

## Worktree Isolation

Subagents can run in their own temporary git worktree by setting `isolation: worktree` in the [subagent frontmatter][sub-agents-frontmatter]. Each subagent gets an isolated copy of the repository at `<repo>/.claude/worktrees/agent-<hash>`, branching from the default remote branch (`origin/HEAD`).

Source: [Sub-agents — Supported frontmatter fields][sub-agents-frontmatter], [Common workflows — Subagent worktrees][subagent-worktrees]

## meta.json Structure

Each subagent worktree session produces a `meta.json` alongside its `.jsonl` transcript. This file is a tombstone recording the subagent's configuration:

```json
{
  "agentType": "general-purpose",
  "worktreePath": "<repo>/.claude/worktrees/agent-<hash>",
  "description": "<task label passed to the Agent tool>"
}
```

| Field | Purpose |
|---|---|
| `agentType` | Which [built-in subagent type][sub-agents] was used (`general-purpose`, `Explore`, `Plan`, etc.) |
| `worktreePath` | Absolute path where the temporary worktree was created on disk |
| `description` | Task label passed to the Agent tool by the parent conversation |

The `worktreePath` is historical only — worktrees are cleaned up on completion (see below). The path is never re-used; it records where the worktree *was*, not where it *is*.

**Note**: meta.json is **not documented** in any first-party source. Structure observed from Opus 4.6 session artifacts, 2026-04-13.

## Transcript Storage

Subagent transcripts are stored alongside the parent session's transcripts:

```text
~/.claude/projects/<project-key>/<parent-session-id>/subagents/agent-<hash>.jsonl
```

The `<project-key>` is the working directory path with `/` replaced by `-` (e.g., `-home-user-repos-my-project`). Each `.jsonl` file contains the full subagent conversation: messages, tool calls, and tool results.

Source: [.claude directory — Application data][claude-directory]

## Cleanup Lifecycle

### Worktree cleanup

When a subagent finishes, worktree cleanup depends on whether changes were made:

| Condition | Behavior |
|---|---|
| No changes | Worktree + branch auto-removed |
| Changes or commits exist | Parent session prompted to keep or remove |
| Orphaned (crash/interrupt) | Auto-removed at startup after [`cleanupPeriodDays`][settings] if no uncommitted changes, untracked files, or unpushed commits |

User-created worktrees (`--worktree` flag) are **never** removed by the automatic sweep — only subagent worktrees.

Source: [Common workflows — Worktree cleanup][worktree-cleanup]

### Transcript cleanup

Subagent transcripts follow the same cleanup as parent session transcripts: deleted at startup once older than [`cleanupPeriodDays`][settings] (default: 30 days).

Source: [.claude directory — Application data][claude-directory], [Settings — cleanupPeriodDays][settings]

### meta.json cleanup

meta.json files are retained alongside the subagent `.jsonl` transcript for history/debugging. They follow the same `cleanupPeriodDays` lifecycle as transcripts.

## Cross-References

- [CC-session-lifecycle-analysis.md](CC-session-lifecycle-analysis.md) — parent session persistence model
- [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md) — agent teams (multi-session orchestration)
- [CC-recursive-spawning-patterns.md](../agents-skills/CC-recursive-spawning-patterns.md) — `CLAUDECODE` guard and recursive spawning
- [CC-tools-inventory.md](../configuration/CC-tools-inventory.md) — Agent tool permissions
- [CC-cli-reference.md](../configuration/CC-cli-reference.md) — `--worktree` flag details
- [CC-binary-architecture.md](../configuration/CC-binary-architecture.md) — `~/.claude/` directory map

## Sources

| Source | Content |
|---|---|
| [CC sub-agents — frontmatter][sub-agents-frontmatter] | `isolation: worktree` field documentation |
| [CC common workflows — subagent worktrees][subagent-worktrees] | Subagent worktree behavior |
| [CC common workflows — worktree cleanup][worktree-cleanup] | Cleanup rules for worktrees |
| [CC .claude directory][claude-directory] | `~/.claude/` application data and cleanup |
| [CC settings][settings] | `cleanupPeriodDays` definition |
| Opus 4.6 session artifacts, 2026-04-13 | meta.json structure observation |

[sub-agents]: https://code.claude.com/docs/en/sub-agents
[sub-agents-frontmatter]: https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields
[subagent-worktrees]: https://code.claude.com/docs/en/common-workflows#subagent-worktrees
[worktree-cleanup]: https://code.claude.com/docs/en/common-workflows#worktree-cleanup
[claude-directory]: https://code.claude.com/docs/en/claude-directory#application-data
[settings]: https://code.claude.com/docs/en/settings#available-settings
