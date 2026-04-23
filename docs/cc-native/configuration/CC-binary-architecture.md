---
title: CC Binary Architecture
purpose: Analysis of Claude Code CLI binary and VS Code extension internals — build system, shared codebase proof, internal API endpoints, model IDs, directory map, /stats data flow, /voice timeline.
created: 2026-03-29
updated: 2026-04-13
validated_links: 2026-04-13
---

**Status**: Research (informational)

## What It Is

Claude Code ships as two closed-source artifacts that share a single bundled JavaScript codebase:

1. **CLI binary** — `~/.local/share/claude/versions/<version>` (~213MB single-executable Bun app) ([frr-build][frr-build])
2. **VS Code extension** — `extension.js` (1.8MB) + `webview/index.js` (4.6MB) in `anthropic.claude-code-<version>-<platform>/`

Both are minified JS bundles with no source maps. The CLI binary embeds a JavaScriptCore runtime via Bun's single-executable packaging ([frr-build][frr-build]). A community attempt to restore source via source maps was taken down by Anthropic via DMCA ([ghuntley][ghuntley], [hn-thread][hn-thread]).

## Shared Codebase Proof

The `claude-code-settings.schema.json` (80+ settings including `plansDirectory`) is embedded in **both** artifacts:

```bash
# Extension — explicit JSON file
grep -c "plansDirectory" <extension>/claude-code-settings.schema.json  # 1

# CLI binary — embedded in JS bundle
grep -boa "plansDirectory" <cli-binary>  # 8 byte-offset matches
```

Confirmed via byte-offset extraction (CC 2.1.87, 2026-03-29):

```text
106947304:plansDirectory
112354169:plansDirectory
...
```

Context at first offset shows Zod schema definition:

```javascript
plansDirectory:y.string().optional().describe(
  "Custom directory for plan files, relative to project root.
   If not set, defaults to ~/.claude/plans/")
```

**Verified** (CC 2.1.87, 2026-03-29): Setting `"plansDirectory": "./plans"` in `settings.json` saves plan files to `./plans/` relative to project root. Works at both user (`~/.claude/settings.json`) and project (`.claude/settings.json`) scope. Absolute paths also work. Similarly, `autoMemoryDirectory` redirects auto-memory storage (user-level only — ignored in project settings per schema description).

### Redirecting CC Data: Settings vs Symlinks

Two approaches to centralizing CC artifacts outside `~/.claude/`:

**Option A: `settings.json` keys** (per-setting, portable)

```json
{
  "plansDirectory": "/path/to/plans",
  "autoMemoryDirectory": "/path/to/memory"
}
```

Only covers `plans/` and `memory/`. Sessions, transcripts, tool results, and subagent logs remain in `~/.claude/projects/`.

**Option B: Symlinks** (comprehensive, dotfiles-friendly)

```bash
ln -sfn /path/to/data/projects ~/.claude/projects
ln -sfn /path/to/data/plans ~/.claude/plans
```

Covers everything — sessions, transcripts, tool results, plans, memory. CC reports symlink source paths but reads/writes at the physical location. No `settings.json` changes needed.

**Why symlinks matter in Codespaces**: `~/.claude/` is wiped on rebuild, `/workspaces/` persists. Symlinks to `/workspaces/<org>/.claude/` survive rebuilds when re-established via dotfiles install script.

**Recommendation**: Symlinks for Codespaces/devcontainers. Settings for per-project overrides.

Cross-ref: [CC-tools-inventory.md](CC-tools-inventory.md) — three-layer config surface

## Extraction Methodology

```bash
# Extract all CLAUDE_CODE_* env vars
grep -oP 'CLAUDE_CODE_[A-Z_]+' <binary> | sort -u

# Extract URLs
strings <binary> | grep -oP 'https://[a-zA-Z0-9._:/-]{15,}' | sort -u

# Extract model IDs
strings <binary> | grep -oP 'claude-[a-z0-9.-]+' | sort -u

# Extract tool names
strings <binary> | grep -oP '"(Bash|Read|Write|Edit|Glob|...)\b' | sort -u

# Extract context around a specific string
grep -boa "targetString" <binary>  # get byte offsets
dd if=<binary> bs=1 skip=<offset-50> count=200 | tr '\0' '\n' | strings
```

**Caveat**: `grep -c` returns 0 on binaries without newlines. Use `grep -boa` for byte-offset matching, or `grep -oP` via the count returned by the shell (`$?`).

Cross-ref: [CC RE landscape][re-landscape] — community tools for deeper analysis

## Internal API Endpoints (String Extraction)

Extracted from CLI binary v2.1.87. **Not documented** in first-party docs unless noted.

### Anthropic API (api.anthropic.com)

| Endpoint | Inferred Purpose | Documented? |
|---|---|---|
| `/v1/messages` | Main inference API | Yes — [api-ref][api-ref] |
| `/v1/models/claude-opus-4-6` | Model availability check | Partially — [model-config][model-config] |
| `/api/claude_cli_feedback` | Feedback submission | No |
| `/api/claude_code/metrics` | Telemetry/usage metrics | No |
| `/api/claude_code/organizations/metrics_enabled` | Org metrics check | No |
| `/api/claude_code_shared_session_transcripts` | Shared session transcripts | No |
| `/api/oauth/claude_cli/create_api_key` | OAuth key creation | No |
| `/api/oauth/claude_cli/roles` | OAuth role check | No |
| `/api/web/domain_info` | Domain info lookup | No |
| `/mcp-registry/v0/servers` | MCP server registry | No |

### Other Services

| URL | Inferred Purpose | Notes |
|---|---|---|
| `mcp-proxy.anthropic.com` | MCP proxy relay | String extraction |
| `beacon.claude-ai.staging.ant.dev` | Staging telemetry | String extraction |
| `downloads.claude.ai/.../claude-plugins-official` | Official plugin distribution | String extraction |
| `storage.googleapis.com/claude-code-dist-*` | CLI binary distribution bucket | String extraction |
| `json.schemastore.org/claude-code-settings.json` | Settings schema ([schema-store][schema-store]) | Not linked from official docs ([gh-11795][gh-11795]) |
| `claude.ai/code/scheduled` | Scheduled triggers UI | Documented — [remote-control][remote-control] |
| `platform.claude.com/v1/oauth/token` | Platform OAuth token exchange | String extraction |
| `raw.githubusercontent.com/.../security.json` | Plugin security checks | String extraction |
| `raw.githubusercontent.com/.../plugin-installs.json` | Plugin install stats | String extraction |

## Model ID Inventory (String Extraction)

All model IDs found in CLI binary v2.1.87. Includes current, deprecated, and **potentially unreleased** models.

### Current (CC 2.1.87)

| Model ID | Family |
|---|---|
| `claude-opus-4-6` | Opus 4.6 |
| `claude-sonnet-4-6` | Sonnet 4.6 |
| `claude-haiku-4-5-20251001` | Haiku 4.5 |
| `claude-sonnet-4-5-20250929` | Sonnet 4.5 |
| `claude-opus-4-20250514` | Opus 4.0 |
| `claude-sonnet-4-20250514` | Sonnet 4.0 |

### Potentially Unreleased (String Extraction)

| Model ID | Notes |
|---|---|
| `claude-opus-4-5-20251101` | Opus 4.5 — not in current model docs |
| `claude-opus-4-1-20250805` | Opus 4.1 — not in current model docs |

### Deprecated (Still in Binary)

| Model ID | Successor |
|---|---|
| `claude-3-7-sonnet-20250219` | Sonnet 4.0 |
| `claude-3-5-sonnet-20241022` | Sonnet 4.0 |
| `claude-3-5-haiku-20241022` | Haiku 4.5 |
| `claude-3-opus-20240229` | Opus 4.0 |
| `claude-3-haiku-20240307` | Haiku 4.5 |
| `claude-3-sonnet-20240229` | (retired) |

Cross-ref: [CC-model-provider-configuration.md](CC-model-provider-configuration.md)

## `~/.claude/` Directory Map (CC 2.1.87)

Direct observation, Codespaces, 2026-03-29.

### Persistent (survives session restarts)

| Path | Purpose | Evidence |
|---|---|---|
| `projects/<hash>/` | Transcripts (`.jsonl`), tool results, subagent logs, memory | Direct observation |
| `sessions/<pid>.json` | Session index keyed by PID. Fields: `sessionId`, `cwd`, `startedAt`, `name`. **Not listed** in first-party [.claude directory cleanup tables](https://code.claude.com/docs/en/claude-directory#application-data) — appears in neither "cleaned automatically" nor "kept until you delete". Cleanup lifecycle undocumented. Observation: Opus 4.6, 2026-04-13 | Direct observation |
| `plans/` | Plan mode output files | Verified — `plansDirectory` setting |
| `file-history/<session>/` | File checkpoints for rewind feature (`fileCheckpointingEnabled`) | Direct observation |
| `history.jsonl` | User command history with timestamps and session IDs | Direct observation |
| `.credentials.json` | OAuth tokens (`claudeAiOauth.accessToken`) — **sensitive** | Direct observation |
| `.claude.json` | Interactive preferences (theme, fastMode, etc.) — see [CC-tools-inventory.md](CC-tools-inventory.md) | Direct observation |
| `settings.json` | Behavior config — see [settings docs][settings] | Documented |
| `backups/` | Timestamped `.claude.json` backups | Direct observation |

### Transient / Conditional

| Path | Purpose | Evidence |
|---|---|---|
| `cache/` | Only `changelog.md` (fetched from GitHub). **Not login tokens** | Direct observation — only 1 file |
| `telemetry/` | OTel export staging. **Empty unless `CLAUDE_CODE_ENABLE_TELEMETRY=1`** | Binary: `lH(process.env.CLAUDE_CODE_ENABLE_TELEMETRY)`. Exports at 300s intervals. See [monitoring docs][monitoring] |
| `session-env/<session>/` | Per-session environment snapshots | Direct observation |
| `shell-snapshots/` | Bash shell state snapshots (aliases, functions) | Direct observation |
| `plugins/` | Plugin cache, blocklist, marketplace metadata. Contains `installed_plugins.json` with `projectPath` entries scoping installs to projects — stale paths cause plugins to silently stop loading for that project. See [plugins reference](https://code.claude.com/docs/en/plugins-reference). Observation: Opus 4.6, 2026-04-13 | Rebuilt on install |
| `mcp-needs-auth-cache.json` | MCP auth state cache | Transient |

### Not in `~/.claude/` (stored elsewhere)

| Path | Purpose |
|---|---|
| `~/.local/share/claude/versions/<version>` | CLI binary (Bun single-executable) |
| `~/.vscode-remote/extensions/anthropic.claude-code-*/` | VS Code extension |

## `/stats` and `/usage` Data Flow

Both commands compute from transcript `.jsonl` files — no separate output file.

| Command | Data Source | Introduced | Evidence |
|---|---|---|---|
| `/stats` | Aggregates `"usage"` blocks across all project transcripts + `sessions/*.json` index | v2.0.64 ([changelog][cc-changelog]) | v2.1.69 fix: "crash when transcript files contain entries with missing or malformed timestamps" |
| `/usage` | Current session in-memory counters (`totalCostUSD`, `totalAPIDuration`, etc.) | Unknown (VS Code: v2.1.6) | Binary: in-memory state struct with `totalCostUSD`, `totalToolDuration`, `turnToolCount` |

`stats-cache.json`: Constant `YA9="stats-cache.json"` exists in binary with `require("fs/promises")` — likely a computed cache to avoid re-scanning all transcripts. Not found on disk (may be temp-dir-only or feature-gated). The **transcripts are the persistent source of truth**.

Per-message usage block format (from transcript `.jsonl`):

```json
{"usage":{"input_tokens":1,"cache_creation_input_tokens":390,
  "cache_read_input_tokens":250273,"output_tokens":137,
  "server_tool_use":{"web_search_requests":0,"web_fetch_requests":0}}}
```

Retention controlled by `cleanupPeriodDays` setting (default: 30). Changelog: "Fixed tool result files never being cleaned up, ignoring the `cleanupPeriodDays` setting."

## `/voice` Timeline

Voice mode first appears in changelog at **v2.1.69** (bug fixes + STT language additions). No "Added voice mode" entry exists in the full changelog (goes back to v0.2.21) — introduction version unclear.

| Version | Entry | Type |
|---|---|---|
| v2.1.69 | Added Voice STT for 10 new languages (20 total) | Feature |
| v2.1.69 | Fixed voice space bar stuck after failed activation | Bug fix |
| v2.1.70 | Fixed voice mode on Windows native binary | Bug fix |
| v2.1.73 | Fixed voice session corruption on slow connection | Bug fix |
| v2.1.76 | Improved `/voice` to show dictation language on enable | Enhancement |
| v2.1.78 | Fixed voice on WSL2 with WSLg | Bug fix |
| v2.1.83 | Fixed 1-8s UI freeze on startup with voice enabled | Bug fix |
| v2.1.84 | Stats screenshot (Ctrl+S in /stats) 16x faster | Enhancement |

Settings key: `voiceEnabled:y.boolean().optional()` — toggled via `/voice` command or `settings.json`.

## Sources

| Source | Content |
|---|---|
| CC 2.1.87 CLI binary, Codespaces, 2026-03-29 | All string extractions in this doc |
| CC 2.1.87 VS Code extension, Codespaces, 2026-03-29 | Schema + extension.js analysis |
| CC 2.1.87 `~/.claude/` directory, Codespaces, 2026-03-29 | Directory map observations |
| CC 2.1.87 transcript `.jsonl`, Codespaces, 2026-03-29 | Usage block format |
| [CC changelog][cc-changelog] | `/stats` v2.0.64, `/voice` v2.1.69+, `cleanupPeriodDays` |
| [frr.dev — CC native build][frr-build] | Bun single-executable architecture analysis |
| [ghuntley.com/tradecraft][ghuntley] | Source-map restoration attempt; DMCA takedown |
| [HN discussion (item 43217357)][hn-thread] | Community discussion of decompilation |
| [CC settings reference][settings] | Official settings documentation |
| [CC monitoring docs][monitoring] | Telemetry, OTel configuration |
| [CC model configuration][model-config] | Official model docs |
| [JSON Schema Store][schema-store] | Settings schema (not linked from official docs) |
| [GitHub issue #11795][gh-11795] | Request to link schema from official docs |
| [CC RE landscape][re-landscape] | Community reverse engineering tools and research |

| Source | Content |
|---|---|
| CC 2.1.87 CLI binary, Codespaces, 2026-03-29 | All string extractions in this doc |
| CC 2.1.87 VS Code extension, Codespaces, 2026-03-29 | Schema + extension.js analysis |
| [frr.dev — CC native build][frr-build] | Bun single-executable architecture analysis |
| [ghuntley.com/tradecraft][ghuntley] | Source-map restoration attempt; DMCA takedown |
| [HN discussion (item 43217357)][hn-thread] | Community discussion of decompilation |
| [CC settings reference][settings] | Official settings documentation |
| [CC model configuration][model-config] | Official model docs |
| [JSON Schema Store][schema-store] | Settings schema (not linked from official docs) |
| [GitHub issue #11795][gh-11795] | Request to link schema from official docs |
| [CC RE landscape][re-landscape] | Community reverse engineering tools and research |

[frr-build]: https://www.frr.dev/posts/claude-code-native-build-bun/
[ghuntley]: https://ghuntley.com/tradecraft/
[hn-thread]: https://news.ycombinator.com/item?id=43217357
[settings]: https://code.claude.com/docs/en/settings
[model-config]: https://code.claude.com/docs/en/model-config
[monitoring]: https://code.claude.com/docs/en/monitoring-usage
[api-ref]: https://platform.claude.com/docs/en/api
[remote-control]: https://code.claude.com/docs/en/remote-control
[schema-store]: https://www.schemastore.org/claude-code-settings.json
[gh-11795]: https://github.com/anthropics/claude-code/issues/11795
[re-landscape]: ../../cc-community/CC-reverse-engineering-landscape.md
[cc-changelog]: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
