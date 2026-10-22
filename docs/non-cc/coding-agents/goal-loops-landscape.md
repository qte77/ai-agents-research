---
title: Goal Loops Across Coding Agents
purpose: Cross-vendor comparison of "keep working until done" features in coding agents — named goal commands, who judges completion, iteration bounds, and Stop-style hooks that can force another turn — with Claude Code's /goal as the reference point.
created: 2026-10-22
updated: 2026-10-22
validated_links: 2026-10-22
status: assess
---

**Details:** Every vendor cell below was fetched from the vendor's own docs on 2026-10-22 and
re-checked by a second, adversarial pass the same day. Claude Code's side is in
[CC-goal-analysis.md](../../cc-native/sessions/CC-goal-analysis.md). Claims are *documented*
unless marked otherwise; nothing here was run.

## What It Is

Several coding agents now ship a way to state an objective once and let the agent keep working
across turns until it is met. They share a name (`/goal` in six of the seven below) but differ on the
questions that matter for unattended use: **who decides the goal is met**, **what stops a run that
never converges**, and **whether a hook can force another turn**.

## Named goal features

| Agent | Feature | Who judges completion | Bound | Source |
|---|---|---|---|---|
| Claude Code | `/goal <condition>` | A separate small fast model, from the transcript only | A turn/time clause written into the condition | [CC-goal-analysis.md](../../cc-native/sessions/CC-goal-analysis.md) |
| OpenAI Codex | `/goal` (app, IDE extension, CLI; out of experimental 2026-05-21) | The agent: it "will stop running when it's confident it has reached the stopping condition" | None stated; the page says it "can work independently for multiple hours"; objective capped at 4,000 characters | [follow goals][codex-goals], [commands][codex-cmds], [changelog][codex-changelog] |
| Google Antigravity | `/goal` | The agent: "The goal ends only when the agent declares it complete" | "there's no iteration cap"; "Only one goal is active at a time in a conversation." | [goal command][ag-goal] |
| Kiro (CLI) | `/goal` | The agent, against criteria it writes: "The agent derives acceptance criteria from your goal statement" | "By default, the agent runs up to 5 iterations — increase this with --max" | [goal command][kiro-goal] |
| VS Code (Copilot agent) | Advanced Autopilot, inside the "Autopilot (Preview)" section | A separate model: "a small utility model reads a transcript of the chat and decides whether the task is done" | "Autopilot loops a maximum of three times before it stops." | [v1.124 release notes][vscode-124] |
| GitHub Copilot CLI | `/goal [OBJECTIVE]`, listed in the same row as `/autopilot [OBJECTIVE]` | Not stated on the command page | `--max-ai-credits N`; "Without an objective, autopilot infers intent from context" | [CLI command reference][copilot-cli-cmds] |
| Cursor | `/goal` | Not stated | Not stated; changelog: "Use /goal to give the agent a long-lived objective to work towards until it's fully complete." | [changelog 2026-08-19][cursor-goal] |

**Gemini CLI** has no `/goal` in its command reference. Its site says "Unpaid tier and Google One
users: Gemini CLI was replaced by Antigravity CLI on June 18th, 2026" — a scoped replacement, not
one for every tier ([Gemini CLI commands][gemini-cmds]). Kiro's CLI also gained `/autonomous on`
in v2.31.0 (2026-10-13) ([Kiro CLI changelog][kiro-changelog]); this corpus's
[kiro-analysis.md](kiro-analysis.md) still describes the older autopilot wording.

## Who decides "done"

- **A separate judge:** Claude Code and VS Code Advanced Autopilot. Both document a small model
  that reads the transcript, so the working agent cannot simply declare victory — but the judge
  sees only what the transcript shows.
- **The agent itself:** Codex, Antigravity and Kiro. Kiro narrows the risk by having the agent
  write acceptance criteria first; Codex and Antigravity rely on the agent's own confidence.
- **Not stated:** Cursor and Copilot CLI. Their pages describe the feature without the mechanism,
  so neither belongs in either group yet.

Bounds diverge just as much: an explicit cap (VS Code 3, Kiro 5 by default), a spend cap
(Copilot's credits), a clause the user writes (Claude Code), or, for Antigravity, an explicitly
stated absence of any cap.

## Stop hooks that force another turn

The scriptable alternative to a goal is a hook that runs when the agent tries to stop and can send
it back to work:

| Agent | Hook | Effect | Cap | Source |
|---|---|---|---|---|
| Claude Code | `Stop` | exit 2 or `"decision": "block"` continues; `stop_hook_active` flags a hook-driven turn | 8 consecutive continuations | [CC-goal-analysis.md](../../cc-native/sessions/CC-goal-analysis.md) |
| OpenAI Codex | `Stop` | `"decision": "block"` makes Codex "continue and automatically creates a new continuation prompt"; input has `stop_hook_active` | Not stated | [hooks][codex-hooks] |
| GitHub Copilot CLI | `agentStop` | "can block and force continuation" | "After 8 consecutive block continuations, the CLI overrides the hook and ends the turn anyway." | [hooks configuration][copilot-hooks] |
| Google Antigravity | `Stop` | `decision: "continue"` re-enters the execution loop | Not stated | [hooks][ag-hooks] |
| Devin | `Stop` | `"decision": "block"` (documented example) | Not stated | [lifecycle hooks][devin-hooks] |
| Cursor | `stop` | A non-empty `followup_message` is submitted as the next user message | `loop_limit`, default 5 | [hooks][cursor-hooks] |
| Amp | `agent.end` (plugin API) | Can return `continue` | `maxContinuations`, default 5 | [plugin API][amp-plugin] |

Claude Code, Codex and Copilot CLI share the same shape (block, a re-entry flag, Copilot and Claude
Code even the same cap of 8), which makes a stop-hook script the most portable of these mechanisms.

## Not found (pages checked, 2026-10-22)

A first-pass search found no named goal feature in: opencode (commands, TUI, plugins, permissions
pages), Aider (options, lint/test pages), Jules (docs and changelog), Roo Code (auto-approve
docs), Amp and Devin (manual / docs index — both have stop hooks, above), and Copilot Studio
(what's-new page). These are absences in the pages named, not a site-wide check. Bolt, Lovable and
Azure AI Foundry were only searched, not read first-party.

## Practices that hold across vendors

Our synthesis, not any vendor's guidance:

- **Prefer an outside check to self-judgement.** Where the agent judges itself (Codex,
  Antigravity, Kiro), put the real check in the objective — tests, a build, a lint gate — and ask
  for its output; Kiro's derived acceptance criteria are the closest built-in version of this.
- **Always set a bound you can see.** Antigravity documents none and Codex states none, so add a
  stop clause or run under a spend/turn limit from the harness.
- **Reach for the stop hook when the check is deterministic.** The block-plus-flag contract is
  nearly identical in Claude Code, Codex and Copilot CLI, so one script can gate all three.
- **Keep the plan outside the session.** Every goal here is per conversation; the durable task list
  belongs in a file — see
  [CC-goal-analysis.md § Pairing `/goal` With a Persistent Task List](../../cc-native/sessions/CC-goal-analysis.md#pairing-goal-with-a-persistent-task-list).

## Sources

| Source | Content |
|---|---|
| [Codex: follow goals][codex-goals] | Self-judged stopping condition; multi-hour runs |
| [Codex: developer commands][codex-cmds] | `/goal` subcommands, 4,000-character limit |
| [Codex changelog][codex-changelog] | 2026-05-21: goal mode out of experimental (app, IDE, CLI) |
| [Codex hooks][codex-hooks] | `Stop` block, `stop_hook_active` |
| [Gemini CLI commands][gemini-cmds] | No `/goal`; scoped replacement by Antigravity CLI |
| [Antigravity `/goal`][ag-goal] | Agent-declared completion, no iteration cap, one goal per conversation |
| [Antigravity hooks][ag-hooks] | `Stop` with `decision: "continue"` |
| [Kiro `/goal`][kiro-goal] | Derived acceptance criteria, 5-iteration default, `--max` |
| [Kiro CLI changelog][kiro-changelog] | `/autonomous on`, v2.31.0 |
| [VS Code 1.124 release notes][vscode-124] | Advanced Autopilot: small utility model judges, 3 loops |
| [Copilot CLI command reference][copilot-cli-cmds] | `/goal` and `/autopilot`, `--max-ai-credits` |
| [Copilot hooks configuration][copilot-hooks] | `agentStop` block, cap of 8 |
| [Cursor changelog 2026-08-19][cursor-goal] | `/goal` announcement |
| [Cursor hooks][cursor-hooks] | `stop` hook `followup_message`, `loop_limit` |
| [Devin lifecycle hooks][devin-hooks] | `Stop` hook `"decision": "block"` |
| [Amp plugin API][amp-plugin] | `agent.end` `continue`, `maxContinuations` |

[codex-goals]: https://learn.chatgpt.com/use-cases/follow-goals
[codex-cmds]: https://learn.chatgpt.com/docs/developer-commands?surface=cli
[codex-changelog]: https://learn.chatgpt.com/docs/changelog
[codex-hooks]: https://learn.chatgpt.com/docs/hooks
[gemini-cmds]: https://geminicli.com/docs/reference/commands/
[ag-goal]: https://antigravity.google/docs/commands/goal/
[ag-hooks]: https://antigravity.google/docs/hooks
[kiro-goal]: https://kiro.dev/docs/cli/chat/goal
[kiro-changelog]: https://kiro.dev/changelog/cli/
[vscode-124]: https://code.visualstudio.com/updates/v1_124
[copilot-cli-cmds]: https://docs.github.com/en/copilot/reference/cli-command-reference
[copilot-hooks]: https://docs.github.com/en/copilot/reference/hooks-configuration
[cursor-goal]: https://cursor.com/changelog/08-19-26
[cursor-hooks]: https://cursor.com/docs/agent/hooks
[devin-hooks]: https://docs.devin.ai/cli/extensibility/hooks/lifecycle-hooks.md
[amp-plugin]: https://ampcode.com/manual/plugin-api
