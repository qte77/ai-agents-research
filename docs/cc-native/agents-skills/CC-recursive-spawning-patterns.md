---
title: CC Recursive Spawning Patterns
source: https://code.claude.com/docs/en/sub-agents, https://code.claude.com/docs/en/env-vars, https://github.com/anthropics/claude-agent-sdk-python/issues/573, https://dev.to/jungjaehoon/why-claude-code-subagents-waste-50k-tokens-per-turn-and-how-to-fix-it-41ma
purpose: Analysis of recursive claude -p invocation patterns, the CLAUDECODE=1 session guard, and spawning method trade-offs for autonomous agent orchestration.
created: 2026-03-17
updated: 2026-11-18
status: research
---

## What Recursive Spawning Is

Running `claude -p` as a subprocess from within a Claude Code session or an
external harness. Each invocation starts with a fresh context window -- no
session state carries over. This is the primitive behind autonomous development
loops (Ralph pattern) and CI/CD integrations.

```bash
claude -p "your prompt"
claude -p "your prompt" --output-format json
git diff main...HEAD | claude -p "Write a PR description..."
```

## The `CLAUDECODE=1` Session Guard

Claude Code sets `CLAUDECODE=1` in its process environment. Child processes
inherit this variable. When a spawned `claude` CLI detects `CLAUDECODE=1`, it
rejects the session:

```text
Error: Claude Code cannot be launched inside another Claude Code session.
```

The guard prevents accidental infinite recursion but must be explicitly cleared
for intentional recursive patterns:

```bash
# From INSIDE a Claude Code session (hook, plugin, subagent, Bash tool):
CLAUDECODE= claude -p "your prompt"          # clears guard for child
# or:
unset CLAUDECODE; claude -p "your prompt"    # removes it entirely
```

In the Claude Agent SDK (`subprocess_cli.py`), filter the environment before
spawning:

```python
env = {**os.environ}
del env["CLAUDECODE"]
subprocess.run(["claude", "-p", prompt], env=env)
```

**Without clearing `CLAUDECODE`, recursive spawning from within CC is
impossible.**

**Source**: [claude-agent-sdk-python#573](https://github.com/anthropics/claude-agent-sdk-python/issues/573) --
SDK bug where `subprocess_cli.py` inherited `CLAUDECODE=1` without filtering,
breaking hooks/plugins that spawn child CC instances.

## Token Cost Warning

Each `claude -p` subprocess re-ingests the full system prompt:
`~/.claude/settings.json`, all MCP tool descriptions, plugins, skills,
`CLAUDE.md`. A single subprocess turn can consume **~50K tokens** before doing
any work.

**Mitigations**:

- Use isolated config (`--no-plugins`, minimal MCP) for child processes
- Set `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`
- Set `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1` to skip git context
- Set `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` to prevent extended context

**Source**: [DEV Community -- "Why Each Subprocess Burns 50K Tokens"](https://dev.to/jungjaehoon/why-claude-code-subagents-waste-50k-tokens-per-turn-and-how-to-fix-it-41ma)

## Key Environment Variables

| Variable | Purpose |
|---|---|
| `CLAUDECODE=1` | **Session guard** -- set by CC; blocks nested launches. Clear with `CLAUDECODE=` or `unset CLAUDECODE` for recursive spawning |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | Enable agent teams |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for subagents/teammates |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1` | Save context in headless loops |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT=1` | Prevent extended context in headless runs |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` | Reduce API calls |

## Spawning Methods Comparison

| Method | How | Nested? | `CLAUDECODE` guard | Session |
|---|---|---|---|---|
| `claude -p` (external harness) | Shell subprocess | Yes (unlimited) | N/A -- parent isn't CC | Fresh each call |
| `claude -p` (from within CC) | `CLAUDECODE= claude -p` | Yes (unlimited) | **Must clear** | Fresh each call |
| Agent Teams (in-process) | `TeamCreate` + `Agent` | **No** -- can't spawn sub-teams | Handled internally | Persistent within team |
| Agent Teams (tmux) | `--teammate-mode tmux` | Teammates get Agent tool | Handled internally | Persistent within team |
| Subagents (`Agent` tool) | Within single session | Up to 3 layers by default (see update below) | Handled internally | Own context; summary returns to parent |
| Claude Agent SDK | `subprocess_cli.py` | Yes | **Must filter** `os.environ` | Fresh per call |

## Update 2026-11-18: Nested Subagents Now Documented

The "1 level deep" entry in the table above was true when this page was written. Per the
[sub-agents docs](https://code.claude.com/docs/en/sub-agents) and the
[env-vars reference](https://code.claude.com/docs/en/env-vars), subagents can now spawn their own subagents:
`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` sets the number of layers below the main conversation, default 3, and `1`
turns nesting off. The env-vars page dates the variable to v2.1.217 (default 1, so no nesting) and the raised
default of 3 to v2.1.219, matching the [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md).
At the limit the `Agent` tool is withheld from subagents (a fork keeps it, but the call errors). Omitting `Agent`
from a subagent's `tools` also stops it spawning. This is in-session nesting; the `claude -p` route and the
`CLAUDECODE=1` guard above are unchanged by it (not re-tested here).

Agent teams still do not nest: the [agent teams docs](https://code.claude.com/docs/en/agent-teams) list "no nested
teams" and one team per session as current limitations, and an in-process teammate's own subagents run in the
foreground. Of the issues cited below, [#31977](https://github.com/anthropics/claude-code/issues/31977)
(teammates lack the `Agent` tool) was closed as not planned on 2026-06-16, and
[#30008](https://github.com/anthropics/claude-code/issues/30008) (print mode hangs with in-process teammates) was
closed as completed on 2026-03-05 (issue states checked 2026-11-18; behaviour not re-tested here).

## Relationship to Agent Teams and Ralph

**Agent Teams** ([CC-agent-teams-orchestration.md](CC-agent-teams-orchestration.md))
spawn teammates as in-process CC instances with shared task lists. Key
constraint: **no nested teams** -- teammates cannot spawn their own teams.
Known bugs as of 2026-03 (see the 2026-11-18 update above for issue states): teammates lack the Agent tool in `in-process` mode
([#31977](https://github.com/anthropics/claude-code/issues/31977));
`--print` mode + teams hangs
([#30008](https://github.com/anthropics/claude-code/issues/30008), fixed in
recent versions).

**Ralph loop** ([CC-ralph-enhancement-research.md](CC-ralph-enhancement-research.md))
is the battle-tested external harness pattern: a shell script calls `claude -p`
once per story with fresh context. Filesystem (prd.json, git state) provides
continuity. Each call is independent -- no session coupling.

**No true "recursive team mode" exists** (as of 2026-11-18; agent teams document no nesting). The closest pattern is a shell
harness (Ralph) calling `claude -p` with
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` per iteration, but each iteration's
teams are independent.

## Cross-References

- [CC-cli-reference.md](../configuration/CC-cli-reference.md) — canonical flag definitions (`-p`, `--output-format`)
- [CC-subagent-session-artifacts.md](../sessions/CC-subagent-session-artifacts.md) — subagent worktree lifecycle, meta.json, transcript storage

## Sources

| Source | Content |
|---|---|
| [Official sub-agents docs](https://code.claude.com/docs/en/sub-agents) | Subagent architecture |
| [claude-agent-sdk-python#573](https://github.com/anthropics/claude-agent-sdk-python/issues/573) | `CLAUDECODE=1` guard bug in SDK |
| [DEV Community](https://dev.to/jungjaehoon/why-claude-code-subagents-waste-50k-tokens-per-turn-and-how-to-fix-it-41ma) | 50K token cost per subprocess |
| [haasonsaas/claude-recursive-spawn](https://github.com/haasonsaas/claude-recursive-spawn) | Bash script with depth control, JSON parsing |
| [#31977](https://github.com/anthropics/claude-code/issues/31977) | No Agent tool in in-process teammates (closed not planned 2026-06-16) |
| [#30008](https://github.com/anthropics/claude-code/issues/30008) | Teams + print mode hang (closed completed 2026-03-05) |
| [Environment variables reference](https://code.claude.com/docs/en/env-vars) | `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, checked 2026-11-18 |
| [Agent teams docs](https://code.claude.com/docs/en/agent-teams) | No nested teams, checked 2026-11-18 |
| [Claude Code CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) | v2.1.217 and v2.1.219 spawn-depth entries |
