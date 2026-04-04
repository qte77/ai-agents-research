---
title: CC stream-json Protocol Reference
description: Undocumented NDJSON event format for --output-format stream-json, including event types, stream chaining, and community parsers.
created: 2026-04-04
updated: 2026-04-04
validated_links: 2026-04-04
---

**Status**: Research (informational)

## What It Is

`claude -p "task" --output-format stream-json --verbose` emits newline-delimited JSON (NDJSON) with token-level streaming events. This is the only programmatic way to access Claude Code's output as it generates. Headless mode only (`-p` flag required).

## Event Types

**Top-level `type` field:**

| Type | Purpose |
|------|---------|
| `system` | System messages (includes `system/api_retry`) |
| `stream_event` | Raw API streaming events (token-level) |
| `assistant` | Assistant message snapshots |
| `result` | Final result |
| `user` | User messages |

**`stream_event` subtypes** (in `.event.type`):

| Subtype | Content |
|---------|---------|
| `message_start` | New message begins |
| `content_block_start` | New content block (text, tool_use) |
| `content_block_delta` | Incremental content — `text_delta` or `input_json_delta` |
| `content_block_stop` | Content block complete |
| `message_delta` | Message-level updates (stop_reason, usage) |
| `message_stop` | Message complete |

**Example `text_delta` event:**

```json
{"type":"stream_event","event":{"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Hello"}}}
```

## Usage

```bash
# Basic streaming output
claude -p "explain TDD" --output-format stream-json --verbose

# With partial message snapshots
claude -p "task" --output-format stream-json --verbose --include-partial-messages

# Stream chaining between agents
claude -p --output-format stream-json "First task" \
  | claude -p --input-format stream-json --output-format stream-json "Process" \
  | claude -p --input-format stream-json "Final report"
```

**Required flags**: `--verbose` must be paired with `stream-json` or the CLI may fail silently. See [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md).

## Community Tools

| Tool | Purpose |
|------|---------|
| [claude-code-parser][parser] | TypeScript parser (11 kB, zero deps). First standalone documentation of the undocumented protocol, including deduplication algorithms and edge cases |
| [format-claude-stream][formatter] | Converts stream-json output to human-readable terminal text |

## Known Gaps

- [#24596][gh-24596] — `--output-format stream-json` lacks event type reference (Anthropic acknowledged)
- [#24594][gh-24594] — `--input-format stream-json` usage is completely undocumented
- No way to access stream-json events in interactive mode (only `-p` headless)

## Cross-References

- [CC-print-mode-gotchas.md](../sessions/CC-print-mode-gotchas.md) — headless mode caveats
- [CC-env-vars-reference.md](CC-env-vars-reference.md) — `CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK`

## Sources

| Source | Content |
|---|---|
| [claude-code-parser][parser] | Protocol documentation and TypeScript parser |
| [format-claude-stream][formatter] | Stream-json to text formatter |
| [GitHub #24596][gh-24596] | Missing event type docs |
| [GitHub #24594][gh-24594] | Undocumented input-format |
| [ruvnet/ruflo wiki][ruflo] | Stream chaining documentation |

[parser]: https://github.com/udhaykumarbala/claude-code-parser
[formatter]: https://github.com/Khan/format-claude-stream
[gh-24596]: https://github.com/anthropics/claude-code/issues/24596
[gh-24594]: https://github.com/anthropics/claude-code/issues/24594
[ruflo]: https://github.com/ruvnet/ruflo/wiki/Stream-Chaining
