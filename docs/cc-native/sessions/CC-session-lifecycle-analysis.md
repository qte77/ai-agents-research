---
title: CC Session Lifecycle — Naming, Persistence, and /rename Bugs
purpose: Analysis of session creation, naming, persistence, /resume discovery, and known /rename bugs with reproduction evidence.
created: 2026-03-27
updated: 2026-03-27
validated_links: 2026-03-27
---

**Status**: Research

## What It Is

CC sessions have a lifecycle: create → auto-name (slug) → optionally `/rename` → persist to JSONL → discover via `/resume` → cleanup after `cleanupPeriodDays`. This doc covers the persistence model, the split between global and per-project storage, and the known bugs around `/rename` not persisting.

## Session Storage Model

### Two storage locations

| Location | Content | Used by |
|---|---|---|
| `~/.claude/history.jsonl` | Global index — one line per user prompt: `sessionId`, `display` (prompt text), `project`, `timestamp` | Unknown — not used by `/resume` |
| `~/.claude/projects/<key>/<id>.jsonl` | Per-project transcript — full conversation with messages, usage, tool results | `/resume` session discovery |

The `<key>` is derived from the working directory path with `/` replaced by `-` (e.g., `-workspaces-Agents-eval`). The `<id>` is the session UUID.

**Critical**: `/resume` only lists sessions that have a `.jsonl` file in the per-project directory. Sessions in `history.jsonl` without a corresponding project JSONL are invisible to `/resume`.

Source: observed CC 2.1.83, Codespaces, 2026-03-27. `history.jsonl` fields: `["display","pastedContents","project","sessionId","timestamp"]`.

### Session identification fields

Each JSONL message carries:

| Field | Purpose | Set by |
|---|---|---|
| `sessionId` | UUID, primary key | CC at session start |
| `slug` | Auto-generated display name (e.g., `stateful-dreaming-donut`) | CC auto-title logic |
| `version` | CC version | CC |
| `gitBranch` | Current git branch | CC |

Source: per-project JSONL inspection, CC 2.1.83

## `/rename` Command

From the [commands reference][commands]:

> `/rename [name]` — Rename the current session and show the name on the prompt bar. Without a name, auto-generates one from conversation history.

CLI equivalent: `--name <name>` flag at launch ([CLI reference][cli]).

### How `/rename` persists

`/rename` writes a `system` event with `subtype: "local_command"` to the session JSONL:

```json
{
  "type": "system",
  "subtype": "local_command",
  "content": "<command-name>/rename</command-name>\n<command-args>my-name</command-args>",
  "slug": "stateful-dreaming-donut"
}
```

**The `slug` field is NOT updated** to the custom name. All subsequent messages continue to carry the original auto-generated slug. The rename is only recorded as a command event, not as a slug change.

Source: session `ea0fa2d5` JSONL, CC 2.1.83, 2026-03-27. 115 messages all show `slug: "stateful-dreaming-donut"` after `/rename office-worker-workflows-research`.

## `/resume` Command

From the [commands reference][commands]:

> `/resume [session]` — Resume a conversation by ID or name, or open the session picker.

CLI equivalent: `claude --resume [value]` or `claude --continue` (most recent).

Discovery mechanism: scans `~/.claude/projects/<key>/` for `.jsonl` files. Sessions without a project JSONL are not discoverable.

## Known Bugs

### 1. Slug not updated after `/rename`

**Observed**: `/rename` records the command event but does not update the `slug` field on subsequent messages. The `/resume` picker likely reads `slug`, not the rename event, so the custom name may not appear.

**Reproduction**: CC 2.1.83, session `ea0fa2d5`, Codespaces, 2026-03-27. `/rename office-worker-workflows-research` succeeded, but all 115 messages retain `slug: "stateful-dreaming-donut"`.

### 2. Auto-title overwrites custom name

After resuming a renamed session and sending new messages, the auto-title logic re-triggers and overwrites the custom name. The rename only survives one resume cycle.

**Upstream**: [anthropics/claude-code#25090][gh-25090] (open, has repro)

### 3. Context compaction resets name

Compaction re-triggers auto-title generation, overwriting the custom name set via `/rename`.

**Upstream**: [anthropics/claude-code#33898][gh-33898] (open, has repro)

### 4. `/rename` breaks in-session `/resume` picker

After `/rename`, the in-session `/resume` picker shows only the renamed session instead of all sessions. Workaround: use `claude --resume` from a new terminal.

**Upstream**: [anthropics/claude-code#37083][gh-37083] (open, has repro)

### 5. CLI `--resume` doesn't find renamed sessions

`claude -r <custom-name>` fails to find sessions renamed via `/rename`.

**Upstream**: [anthropics/claude-code#27195][gh-27195] (open)

### 6. `--resume` + `--print` ignores renamed sessions

Headless resume mode doesn't accept custom names.

**Upstream**: [anthropics/claude-code#34360][gh-34360] (open, has repro)

### 7. Session JSONL missing despite history entry

A session can exist in `history.jsonl` (global index) but have no per-project JSONL file. In this case, `/rename` has nowhere to persist the name, and `/resume` cannot discover the session.

**Possible causes**: `cleanupPeriodDays` purged the file (default 30 days, [settings docs][settings]), `--no-session-persistence` was active, session ran from a different project path, or abnormal exit before first JSONL flush.

## Session Cleanup

Retention is controlled by the `cleanupPeriodDays` setting (default: 30 days). Sessions inactive longer than this period are deleted at startup. Setting to `0` disables persistence entirely — no `.jsonl` files are written and `/resume` shows no conversations.

Source: [settings docs][settings]

## Cross-References

- [CC-session-cost-analysis.md](CC-session-cost-analysis.md) — JSONL structure, usage fields, cost extraction
- [CC-session-keepalive-analysis.md](CC-session-keepalive-analysis.md) — Session timeout and keepalive strategies

## Sources

| Source | Content |
|---|---|
| [CC commands reference][commands] | `/rename`, `/resume`, `/clear` behavior |
| [CC CLI reference][cli] | `--name`, `--resume`, `--continue`, `--no-session-persistence` flags |
| [CC settings docs][settings] | `cleanupPeriodDays` retention control |
| [#25090][gh-25090] | Name disappears after second exit |
| [#33898][gh-33898] | Name reverts after compaction |
| [#37083][gh-37083] | `/rename` breaks `/resume` picker |
| [#27195][gh-27195] | CLI resume by name fails |
| [#34360][gh-34360] | `--resume` + `--print` ignores renamed sessions |
| CC 2.1.83, session `ea0fa2d5`, Codespaces, 2026-03-27 | Slug-not-updated reproduction |

[commands]: https://code.claude.com/docs/en/commands
[cli]: https://code.claude.com/docs/en/cli-reference
[settings]: https://code.claude.com/docs/en/settings
[gh-25090]: https://github.com/anthropics/claude-code/issues/25090
[gh-33898]: https://github.com/anthropics/claude-code/issues/33898
[gh-37083]: https://github.com/anthropics/claude-code/issues/37083
[gh-27195]: https://github.com/anthropics/claude-code/issues/27195
[gh-34360]: https://github.com/anthropics/claude-code/issues/34360
