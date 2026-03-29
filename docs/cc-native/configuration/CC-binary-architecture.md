<!-- markdownlint-disable MD013 -->
---
title: CC Binary Architecture
purpose: Analysis of Claude Code CLI binary and VS Code extension internals — build system, shared codebase proof, internal API endpoints, and model ID inventory.
created: 2026-03-29
updated: 2026-03-29
validated_links: 2026-03-29
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

```
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

## Sources


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
[api-ref]: https://platform.claude.com/docs/en/api
[remote-control]: https://code.claude.com/docs/en/remote-control
[schema-store]: https://json.schemastore.org/claude-code-settings.json
[gh-11795]: https://github.com/anthropics/claude-code/issues/11795
[re-landscape]: ../../cc-community/CC-reverse-engineering-landscape.md
