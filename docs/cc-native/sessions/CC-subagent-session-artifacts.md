---
title: CC Subagent Session Artifacts
purpose: Reference for subagent session artifacts — worktree lifecycle, meta.json tombstones, transcript storage, and cleanup behavior.
created: 2026-04-13
updated: 2026-11-26
validated_links_on: 2026-04-13
status: research
---

## What It Is

When Claude Code spawns subagents via the Agent tool, each subagent produces session artifacts: transcripts, worktree directories (if isolated), and metadata files. This doc covers the artifact structure, worktree lifecycle, and cleanup behavior.

## Worktree Isolation

Subagents can run in their own temporary git worktree by setting `isolation: worktree` in the [subagent frontmatter][sub-agents-frontmatter]. Each subagent gets an isolated copy of the repository under `<repo>/.claude/worktrees/` (the `agent-<hash>` name is observed only, unverified). By default (`worktree.baseRef: "fresh"`) it branches from the repository's default branch on the remote, fetching it if the repo has not been fetched in 24 hours (5-second cap) and falling back to local HEAD when there is no remote or cached `origin/HEAD`; `"head"` branches from the current local HEAD instead. Subagent worktrees use the same base as `--worktree` (checked 2026-11-26).

Source: [Sub-agents — Supported frontmatter fields][sub-agents-frontmatter], [Worktrees — Isolate subagents with worktrees][subagent-worktrees]

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

**Note**: the [sub-agents page](https://code.claude.com/docs/en/sub-agents) documents per-subagent `agent-{agentId}.meta.json` files next to the `.jsonl` transcript, used to look up an agent ID by name after a restart; the field structure is not documented. The fields shown here (`agentType`, `worktreePath`, `description`) were observed from Opus 4.6 session artifacts, 2026-04-13 (unverified).

## Transcript Storage

Subagent transcripts are stored alongside the parent session's transcripts:

```text
~/.claude/projects/<project-key>/<parent-session-id>/subagents/agent-<agentId>.jsonl
```

The `<project-key>` is the working directory path with `/` replaced by `-` (e.g., `-home-user-repos-my-project`; observed, unverified for `projects/`). Each `.jsonl` file contains the full subagent conversation: messages, tool calls, and tool results.

Source: [.claude directory — Application data][claude-directory]

## Cleanup Lifecycle

### Worktree cleanup

When a subagent finishes, Claude Code keeps the worktree if git shows changed files, untracked files or new commits; otherwise it can remove the worktree right away. A kept worktree stays on disk until the periodic sweep can remove it without losing work (the keep-or-remove prompt applies to interactive `--worktree` session exits, not to subagent completion):

| Condition | Behavior |
|---|---|
| No changes | Worktree can be removed right away |
| Changed files, untracked files or new commits | Worktree kept until the periodic sweep can remove it without losing work |
| Orphaned (crash/interrupt) | A periodic sweep removes worktrees Claude created for subagents and background sessions once older than [`cleanupPeriodDays`][settings], unless they hold changed or untracked files or unpushed commits, or a checked-out submodule holds changes or cannot be inspected (v2.1.274+); locks Claude set for dead sessions are released |

Worktrees of `--worktree` sessions you have not backgrounded are **never** removed by the automatic sweep, and neither are worktrees you created with `git worktree add` outside `.claude/worktrees/`; the sweep covers subagent and background-session worktrees, so a backgrounded `--worktree` session can be swept.

Source: [Worktrees — Clean up subagent and background-session worktrees][worktree-cleanup]

### Transcript cleanup

Subagent transcripts follow the same cleanup as parent session transcripts: the `subagents/` directory is removed with the parent session transcript when it ages out past [`cleanupPeriodDays`][settings] (default: 30 days, minimum 1).

Source: [.claude directory — Application data][claude-directory], [Settings reference — cleanupPeriodDays][settings]

### meta.json cleanup

meta.json files are retained alongside the subagent `.jsonl` transcript for history/debugging. They presumably follow the same `cleanupPeriodDays` lifecycle as transcripts, inferred from the directory-level rule above (unverified for meta.json specifically).

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
| [CC worktrees — isolate subagents][subagent-worktrees] | Subagent worktree behavior |
| [CC worktrees — clean up subagent and background-session worktrees][worktree-cleanup] | Cleanup rules for worktrees |
| [CC .claude directory][claude-directory] | `~/.claude/` application data and cleanup |
| [CC settings reference][settings] | `cleanupPeriodDays` definition |
| Opus 4.6 session artifacts, 2026-04-13 | meta.json structure observation |

[sub-agents]: https://code.claude.com/docs/en/sub-agents
[sub-agents-frontmatter]: https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields
[subagent-worktrees]: https://code.claude.com/docs/en/worktrees#isolate-subagents-with-worktrees
[worktree-cleanup]: https://code.claude.com/docs/en/worktrees#clean-up-subagent-and-background-session-worktrees
[claude-directory]: https://code.claude.com/docs/en/claude-directory#application-data
[settings]: https://code.claude.com/docs/en/settings-reference#cleanupperioddays
