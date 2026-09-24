---
title: Netdata MCP Server Analysis
source: https://github.com/netdata/netdata
purpose: Netdata's built-in MCP server for incident-time infrastructure queries from Claude Code, Claude Desktop, Cursor, and other MCP clients — what it exposes, transports, and auth.
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
platform_scope: [claude-code, claude-desktop, cursor, vs-code, jetbrains, gemini-cli, codex-cli, crush, opencode]
---

**Status**: Assess

## What It Is

[Netdata][repo] is a large, established (GPL-3.0, Go, **80.6K stars**, latest release `v2.11.1`
(2026-09-16), per [`gh api repos/netdata/netdata`][repo], verified 2026-09-24) real-time
infrastructure-monitoring agent. Since v2.6.0 it ships a built-in **Model Context Protocol (MCP)
server**, letting AI
assistants query live observability data — metrics, alerts, logs, topology, and running processes
— directly from a monitored node, rather than the assistant having to shell out to `curl`/`ssh` or
be fed pasted dashboard screenshots. The corpus-relevant pattern is **incident-time infrastructure
grounding**: an agent (Claude Code, Claude Desktop, Cursor, …) gets first-class, structured, live
access to "what is actually happening on this box right now" for root-cause-analysis workflows.

## What It Exposes

Per the [MCP docs][mcp-docs] and [MCP server source][mcp-src] (`src/web/mcp/`):

- **Node discovery** — hardware, OS, version info, streaming topology
- **Metrics discovery** — full-text search across contexts, instances, dimensions, labels
- **Function discovery** — system functions (`processes`, `network-connections`, `streaming`,
  `systemd-journal`, `windows-events`, etc.)
- **Function execution** — run a discovered function on a connected node (verbatim from the docs:
  "requires Netdata Parent")
- **Log exploration** — access logs from a connected node (also "requires Netdata Parent")
- **Alert discovery + history** — active/raised alerts and complete transition logs
- **Metrics queries** — aggregations with ML-powered anomaly detection
- **Metrics scoring** — root-cause correlation/weighting across anomalous series

## Transports and Auth

| Transport | Endpoint | Notes |
|---|---|---|
| WebSocket | `ws://IP:19999/mcp` | Original transport; needs a bridge for stdio-only clients |
| HTTP Streamable | `http://IP:19999/mcp` | Direct client connections, Netdata v2.7.2+ |
| SSE | `http://IP:19999/sse` | Server-Sent Events, v2.7.2+ |
| stdio | via `nd-mcp` bridge | For clients that only speak stdio (v2.6.0+) |

(Some client JSON configs instead point SSE at `http://IP:19999/mcp?transport=sse` — a
query-parameter form of the same endpoint documented alongside the table above; the dedicated
`/sse` path is the canonical one in Netdata's own transport-options table, per
[`docs/netdata-ai/mcp/README.md`][mcp-docs].)

Auth is bearer-token based: a local API key auto-generated at
`/var/lib/netdata/mcp_dev_preview_api_key`, sent as `Authorization: Bearer <key>` (legacy
`?api_key=` query param also accepted). **Netdata Cloud MCP**
(`https://app.netdata.cloud/api/v1/mcp`) is a separate, single endpoint spanning all claimed
infrastructure, gated behind a paid plan and a `scope:mcp` API token. Visibility is hierarchical:
a standalone/child node only sees itself; a **Parent** sees all connected children; Cloud is meant
to span the whole fleet ([MCP docs][mcp-docs]).

## Client Setup (Claude Code, Cursor)

Netdata documents per-client connection guides; two concrete examples ([`mcp-clients/`][mcp-clients-docs]):

**Claude Code** — direct HTTP (v2.7.2+, no bridge):

```bash
claude mcp add --transport http --scope project netdata \
  http://YOUR_NETDATA_IP:19999/mcp \
  --header "Authorization: Bearer NETDATA_MCP_API_KEY"
```

**Cursor** — via `.cursor/mcp.json`; the documented local-deployment form (v2.6.0+, all versions)
uses the `nd-mcp` stdio bridge:

```json
{
  "mcpServers": {
    "netdata": {
      "type": "stdio",
      "command": "/usr/sbin/nd-mcp",
      "args": ["ws://YOUR_NETDATA_IP:19999/mcp"]
    }
  }
}
```

For v2.7.2+, the guide shows the same block with `"type"` switched to `streamable-http` or `sse`
and a `url`/`headers` pair replacing `command`/`args` (adapted from
[`mcp-clients/cursor.md`][mcp-clients-docs], not reproduced verbatim here).

Documented clients also include Claude Desktop, VS Code, JetBrains IDEs, Gemini CLI, OpenAI Codex
CLI, Crush, and OpenCode ([`mcp-clients/`][mcp-clients-docs]).

## Adoption Decision

**Assess.** Netdata is a mature, high-star, actively-maintained project, and the MCP surface is
first-class (native C implementation in `src/web/mcp/`, not a bolted-on bridge), which lowers
integration risk relative to a young wrapper project. It is filed as Assess rather than Trial/Adopt
because this pass is a read of the docs and source tree, not a live connect-and-query validation
against a running Netdata instance — that hands-on step is the natural follow-up before
recommending it for incident workflows in this corpus's own tooling.

Cross-ref: [CC-connectors-overview.md][connectors] — CC's own MCP client surface that a Netdata MCP
server would plug into.

## Sources

| Source | Content |
|---|---|
| [netdata/netdata][repo] (GitHub API) | Stars, license (GPL-3.0), language, activity, latest release — `gh api repos/netdata/netdata` + `.../releases/latest`, 2026-09-24 |
| [`docs/netdata-ai/mcp/README.md`][mcp-docs] | Data exposure, transports, auth, deployment options, supported clients |
| [`src/web/mcp/README.md`][mcp-src] | Transport adapters, tool surface, hierarchy/visibility model |
| [`docs/netdata-ai/mcp/mcp-clients/`][mcp-clients-docs] | Per-client (Claude Code, Cursor, …) connection instructions |

[repo]: https://github.com/netdata/netdata
[mcp-docs]: https://github.com/netdata/netdata/blob/master/docs/netdata-ai/mcp/README.md
[mcp-src]: https://github.com/netdata/netdata/blob/master/src/web/mcp/README.md
[mcp-clients-docs]: https://github.com/netdata/netdata/tree/master/docs/netdata-ai/mcp/mcp-clients
[connectors]: ../cc-native/plugins-ecosystem/CC-connectors-overview.md
