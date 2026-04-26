---
title: CC 1.x Session Artifact Schema
purpose: Reference for the CC 1.x session JSONL wire format -- directory layout, event type catalog, and field reference -- for downstream consumers such as polyforge learnings-sync.sh and cc-meta bigpicture.
created: 2026-04-23
updated: 2026-04-23
validated_links: 2026-04-23
---

**Status**: Research

## What It Is

Claude Code persists every conversation to JSONL files under `~/.claude/`. This document specifies the on-disk layout and the event types written to those files. It is a companion to [CC-session-lifecycle-analysis.md](CC-session-lifecycle-analysis.md), which covers lifecycle and `/rename` bugs, and [CC-subagent-session-artifacts.md](CC-subagent-session-artifacts.md), which covers subagent-specific artifacts.

Source observations: CC 2.1.90, Codespaces, 2026-04-02. Field inventory from live JSONL inspection.

## Directory Layout

```text
~/.claude/
├── history.jsonl                          # global index -- one line per user prompt
├── projects/
│   └── <encoded-path>/                    # one dir per working directory
│       ├── <session-uuid>.jsonl           # full per-project transcript
│       └── <session-uuid>/
│           └── subagents/
│               └── agent-<hash>.jsonl     # subagent sidechain transcript
├── plans/
│   └── <slug>.md                         # plan-mode plan files (when /plan is used)
├── tasks/
│   └── <id>/
│       ├── .lock                          # advisory lock while task runs
│       └── .highwatermark                 # read cursor for task output polling
├── sessions/
│   └── <pid>.json                         # pid -> session metadata index
├── backups/
│   └── .claude.json.backup.<timestamp>    # rolling backups of .claude.json
└── settings.json                          # user-level CC settings
```

### Path encoding

`<encoded-path>` is the absolute working directory with every `/` replaced by `-`.
Example: `/workspaces/polyforge-orchestrator` -> `-workspaces-polyforge-orchestrator`.

Moving a repository to a different absolute path orphans its session history. See [CC-session-lifecycle-analysis.md](CC-session-lifecycle-analysis.md) for migration implications.

## `history.jsonl` -- Global Index

One JSON object per line. Written once per user prompt.

```json
{
  "display": "analyze the current branch",
  "pastedContents": {},
  "timestamp": 1775119522125,
  "project": "/workspaces/polyforge-orchestrator",
  "sessionId": "1fe13026-a984-4fc3-b261-acc40c7bdc59"
}
```

| Field | Type | Description |
|---|---|---|
| `display` | string | First user prompt text for the turn |
| `pastedContents` | object | Map of pasted file paths to content; empty `{}` when nothing was pasted |
| `timestamp` | number | Epoch milliseconds |
| `project` | string | Absolute working directory path |
| `sessionId` | string | UUID of the session |

**Note**: `history.jsonl` uses epoch milliseconds. Per-project JSONL files use ISO 8601 timestamps.

**Critical**: `/resume` does **not** use `history.jsonl` for discovery. It scans the per-project directory directly.
A session in `history.jsonl` without a matching per-project file is invisible to `/resume`.

## Per-Project JSONL -- Event Catalog

Each file at `~/.claude/projects/<encoded-path>/<session-uuid>.jsonl` contains one JSON object per line.
Records are appended in turn order. All records share a common envelope; `type` selects the event.

### Common envelope fields

| Field | Type | Notes |
|---|---|---|
| `type` | string | Event type |
| `sessionId` | string | Session UUID |
| `uuid` | string | Record UUID |
| `parentUuid` | string or null | Parent record UUID; `null` at session root |
| `isSidechain` | boolean | `true` for subagent sidechain records |
| `timestamp` | string | ISO 8601, e.g. `"2026-04-02T08:45:22.133Z"` |
| `userType` | string | `"external"` for interactive sessions |
| `entrypoint` | string | `"cli"` for terminal invocations |
| `cwd` | string | Working directory at write time |
| `version` | string | CC version, e.g. `"2.1.90"` |
| `gitBranch` | string | Active git branch (absent on some meta events) |
| `slug` | string | Auto-generated session name, e.g. `"keen-growing-flask"` (absent until first assistant turn) |
| `promptId` | string | Groups all records from one user prompt turn (optional) |

### `permission-mode`

Written at session open.

```json
{"type":"permission-mode","permissionMode":"default","sessionId":"..."}
```

`permissionMode` values: `"default"`, `"acceptEdits"`, `"bypassPermissions"`.

### `file-history-snapshot`

Written before each user turn. Tracks file state for rollback.

```json
{
  "type": "file-history-snapshot",
  "messageId": "...",
  "snapshot": {"messageId":"...","trackedFileBackups":{},"timestamp":"..."},
  "isSnapshotUpdate": false
}
```

`trackedFileBackups` maps file paths to backup content when files are modified; empty `{}` when no files are tracked.

### `user`

Three subtypes by `message.content` shape:

**Interactive prompt** (human message):

```json
{
  "type": "user",
  "promptId": "dce0fbea-4974-4fd2-b975-dda94a80ea9e",
  "message": {"role":"user","content":"analyze the current branch"},
  "permissionMode": "default"
}
```

**Local command** (`!<cmd>` bash shorthand or `/command`):

```json
{
  "type": "user",
  "isMeta": true,
  "message": {"role":"user","content":"<local-command-caveat>...</local-command-caveat>"}
}
```

**Tool result** (response to an assistant `tool_use`):

```json
{
  "type": "user",
  "message": {
    "role": "user",
    "content": [{"tool_use_id":"toolu_...","type":"tool_result","content":[{"type":"text","text":"..."}]}]
  },
  "toolUseResult": { ... }
}
```

`toolUseResult` shape varies by tool:

| Tool | Shape |
|---|---|
| `Read` | `{"type":"text","file":{"filePath":"...","content":"...","numLines":N,...}}` |
| `Bash` | `{"stdout":"...","stderr":"...","interrupted":false,"isImage":false,"noOutputExpected":false}` |
| `Grep` (files mode) | `{"mode":"files_with_matches","filenames":[...],"numFiles":N}` |
| Agent | `{"status":"completed","agentType":"...","content":[...],"totalDurationMs":N,"totalTokens":N,...}` |

### `assistant`

```json
{
  "type": "assistant",
  "message": {
    "model": "claude-opus-4-6",
    "id": "msg_013iNyFWjR286puRSTQvdQFT",
    "role": "assistant",
    "content": [...],
    "stop_reason": "tool_use",
    "usage": {...}
  },
  "requestId": "req_011CZeej7LAmyRcoHieFAEoF"
}
```

Content block types in `message.content`:

| Block type | Description |
|---|---|
| `text` | Plain text response |
| `thinking` | Extended thinking block; `signature` field present; content may be redacted |
| `tool_use` | Tool invocation: `id`, `name`, `input`, `caller` |

`message.usage` fields:

| Field | Description |
|---|---|
| `input_tokens` | Input tokens for this turn |
| `output_tokens` | Output tokens |
| `cache_creation_input_tokens` | Tokens written to prompt cache |
| `cache_read_input_tokens` | Tokens read from prompt cache |
| `cache_creation` | `{ephemeral_5m_input_tokens, ephemeral_1h_input_tokens}` |
| `server_tool_use` | `{web_search_requests, web_fetch_requests}` |
| `service_tier` | `"standard"` or `"priority"` |
| `inference_geo` | Geography string or `"not_available"` |

### `attachment`

Metadata events injected into context; not sent to the model as user content.

**`deferred_tools_delta`** -- announces lazily-loaded tools:

```json
{
  "type": "attachment",
  "attachment": {
    "type": "deferred_tools_delta",
    "addedNames": ["EnterWorktree","WebFetch","WebSearch",...],
    "addedLines": [...],
    "removedNames": []
  }
}
```

**`companion_intro`** -- BUDDY companion announcement:

```json
{"type":"attachment","attachment":{"type":"companion_intro","name":"Glitch","species":"ghost"}}
```

### `system`

**`turn_duration`** -- written at end of each assistant turn:

```json
{
  "type": "system",
  "subtype": "turn_duration",
  "durationMs": 111491,
  "messageCount": 7,
  "isMeta": false
}
```

**`local_command`** -- records slash commands such as `/rename`:

```json
{
  "type": "system",
  "subtype": "local_command",
  "content": "<command-name>/rename</command-name>\n<command-args>my-name</command-args>",
  "slug": "stateful-dreaming-donut"
}
```

The `slug` field here is **not** updated after `/rename`. All subsequent records carry the original auto-generated slug.
See [CC-session-lifecycle-analysis.md](CC-session-lifecycle-analysis.md) for the full `/rename` bug catalog.

### `last-prompt`

Tail marker written at session close:

```json
{"type":"last-prompt","lastPrompt":"! git branch -a","sessionId":"..."}
```

## Subagent Sidechain Transcripts

Subagent records live at:

```text
~/.claude/projects/<project-key>/<parent-session-id>/subagents/agent-<hash>.jsonl
```

Sidechain records are structurally identical to parent session records but carry `"isSidechain": true` and an `agentId` field.
The `agentId` matches the `<hash>` in the filename and the `agentId` in the parent session's Agent tool result.

See [CC-subagent-session-artifacts.md](CC-subagent-session-artifacts.md) for `meta.json` tombstone structure and worktree cleanup.

## `sessions/<pid>.json` -- PID Index

Maps a process ID to session metadata. Not documented in first-party cleanup tables.

```json
{
  "sessionId": "1fe13026-a984-4fc3-b261-acc40c7bdc59",
  "cwd": "/workspaces/polyforge-orchestrator",
  "startedAt": "2026-04-02T08:45:22.000Z",
  "name": "keen-growing-flask"
}
```

Files for dead PIDs may be cleaned up, but the exact lifecycle is undocumented.
Source: [CC-binary-architecture.md](../configuration/CC-binary-architecture.md).

## Stability Notes

| Field / Feature | Stability | Notes |
|---|---|---|
| `sessionId`, `uuid`, `parentUuid` | Stable | Core identity; safe for downstream indexing |
| `timestamp` ISO 8601 (project JSONL) | Stable | Standard format |
| `timestamp` epoch ms (`history.jsonl`) | Stable | Consistent across observed versions |
| `cwd`, `version`, `gitBranch`, `slug` | Stable | Present on all non-meta records since CC 2.1.83+ |
| `message.usage` shape | Experimental | Subfields added between minor versions; parse defensively |
| `attachment.type` values | Experimental | New types may be added without notice |
| `toolUseResult` shape | Experimental | Per-tool; not documented in first-party sources |
| `sessions/<pid>.json` | Undocumented | Not in first-party cleanup tables; treat as ephemeral |
| `plans/` and `tasks/` layout | Undocumented | Internal structure not verified |
| `thinking` block `signature` | Experimental | Cryptographic; content may be empty or redacted |

## Cross-References

- [CC-session-lifecycle-analysis.md](CC-session-lifecycle-analysis.md) -- session naming, `/rename` bugs, path migration risk, `cleanupPeriodDays`
- [CC-session-cost-analysis.md](CC-session-cost-analysis.md) -- cost extraction from `message.usage`
- [CC-subagent-session-artifacts.md](CC-subagent-session-artifacts.md) -- subagent worktrees, `meta.json`, sidechain transcripts
- [CC-binary-architecture.md](../configuration/CC-binary-architecture.md) -- full `~/.claude/` directory map

## Sources

| Source | Content |
|---|---|
| Live JSONL inspection, CC 2.1.90, Codespaces, 2026-04-02 | All field observations |
| [CC-session-lifecycle-analysis.md](CC-session-lifecycle-analysis.md) | `history.jsonl` fields, path encoding, cleanup period |
| [CC-subagent-session-artifacts.md](CC-subagent-session-artifacts.md) | Sidechain path, `meta.json` |
| [CC-binary-architecture.md](../configuration/CC-binary-architecture.md) | `sessions/<pid>.json` lifecycle gap |
