---
title: CC Monitoring & Telemetry (First-Party OTel)
purpose: Claude Code's first-party OpenTelemetry integration — span hierarchy, distributed-trace propagation, privacy-default gates, and metric cardinality controls for monitoring CC agent behavior.
category: analysis
created: 2026-06-27
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Assess

## What It Is

Claude Code is itself an OTel-instrumented client. Enabling `CLAUDE_CODE_ENABLE_TELEMETRY=1` emits metrics (time series) and logs/events via standard OTLP; distributed tracing is available in beta via `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` + `OTEL_TRACES_EXPORTER`. This makes every OTel-native backend a candidate CC observability backend out of the box. Source: [Claude Code — Monitoring usage][cc-monitoring] (first-party). Extracted from the broader [agent-observability-methods-analysis.md](../../non-cc/agent-observability-methods-analysis.md) platform catalog so CC's own telemetry surface has a first-party home.

## Span Hierarchy (Beta Traces)

```text
claude_code.interaction                        # root span: one per user prompt
├── claude_code.llm_request                    # API call to Anthropic Messages
├── claude_code.hook                           # requires detailed beta tracing
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user       # permission-wait time
    ├── claude_code.tool.execution             # actual tool run
    └── (Task tool) subagent claude_code.llm_request / claude_code.tool spans
```

- Task-spawned subagents nest their own `llm_request` and `tool` spans under the parent's `claude_code.tool` span
- Retries on `claude_code.llm_request` are recorded as `gen_ai.request.attempt` span events with `attempt` and `client_request_id` attributes
- Tool span attributes include `file_path` (Read/Edit/Write), `full_command` (Bash), `skill_name` (Skill tool), `mcp_server_name`/`mcp_tool_name` (MCP tools), `subagent_type` (Task tool) — all gated behind `OTEL_LOG_TOOL_DETAILS`. Note this plain tool-span namespace is distinct from the redacted `attribution` namespace on metrics/events (see [Attribution Chain](#attribution-chain-skillpluginmcp))
- The `claude_code.hook` span (fields: `hook_event`, `hook_name`, `num_hooks`, gated `hook_definitions`, `duration_ms`, success/blocking/non-blocking-error/cancelled counts) sits behind a **second beta tier**: beyond `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, detailed tracing requires `ENABLE_BETA_TRACING_DETAILED=1` + `BETA_TRACING_ENDPOINT`, and in **interactive CLI sessions additionally org-level allowlisting** (Agent SDK / `claude -p` sessions are not org-gated). Content-bearing attrs (`new_context`, `system_prompt_preview`, `tool_input`, `response.model_output`; `user_system_prompt` also needs `OTEL_LOG_USER_PROMPTS`) live in this tier. The beta is imperfect in streaming/Agent-SDK mode ([#53954][gh-53954]: missing interaction/tool spans). Verified against live docs 2026-07-23; introduction versions not pinned in the public changelog — no version gate asserted

## Privacy-First Defaults

All sensitive attributes are **redacted unless explicitly unlocked**:

| Gate | What it reveals |
|---|---|
| `OTEL_LOG_USER_PROMPTS` | Prompt text on `user_prompt` events / interaction span |
| `OTEL_LOG_TOOL_DETAILS` | Bash command, MCP tool name, Skill name, file path, subagent type |
| `OTEL_LOG_TOOL_CONTENT` | Tool input/output content in span events (60 KB truncation) |
| `OTEL_LOG_RAW_API_BODIES` | Full Anthropic API request/response JSON (`1` inline / `file:<dir>` to disk with `body_ref`) |

This is notably stricter than most third-party LLM observability platforms, which default to capturing prompts and tool I/O.

## Log Events

Beyond the long-known content events (`user_prompt`, `assistant_response`, `tool_result`, `api_request`, `api_error`, `api_request_body`, `api_response_body`, `tool_decision`, `auth`, `mcp_server_connection`, `internal_error`, `plugin_installed`, `plugin_loaded`), two operationally significant events (verified live docs, 2026-07-23; introduction versions unpinned):

- **`claude_code.api_refusal`** — fired when the API refuses a request. Fields: `model`, `request_id`, `query_source`, `speed` (fast/normal), `attempt`, `effort`, `server_fallback_hop`, `has_category`, `has_explanation`, and (gated by `OTEL_LOG_TOOL_DETAILS`) `category` ∈ cyber/bio/frontier_llm/reasoning_extraction — plus the full [attribution chain](#attribution-chain-skillpluginmcp) below.
- **`claude_code.permission_mode_changed`** — fields `from_mode`/`to_mode` (default/plan/acceptEdits/auto/bypassPermissions) and `trigger` (shift_tab/exit_plan_mode/auto_gate_denied/auto_opt_in; absent for SDK/bridge-originated transitions). Useful for auditing when sessions escalate permissions.

## Attribution Chain (Skill/Plugin/MCP)

The **Cost Metric** and `api_refusal` event carry a redacted attribution namespace answering "which extension caused this spend/refusal": `agent.name`, `skill.name`, `plugin.name`, `marketplace.name`, `mcp_server.name`, `mcp_tool.name`. Redaction rules are non-obvious: built-in / bundled / user-authored / official-marketplace names pass **verbatim**; third-party plugin skills and plugins collapse to `"third-party"`; user-defined agents and user-configured MCP servers collapse to `"custom"`; `marketplace.name` appears only for official-marketplace plugins. This namespace is separate from (and more elaborate than) the plain `skill_name`/`mcp_server_name`/`mcp_tool_name`/`subagent_type` attrs on tool spans. Verified live docs, 2026-07-23.

## Distributed Trace Propagation

`TRACEPARENT` is auto-injected into Bash and PowerShell subprocesses so any W3C-compliant child can parent its spans under the active tool execution span. In Agent SDK and headless (`claude -p`) sessions, CC **reads** `TRACEPARENT` + `TRACESTATE` from its own environment so an embedding process can pass in its active context. Interactive sessions deliberately ignore inbound `TRACEPARENT` to prevent accidental inheritance from CI/container ambient values.

**Outbound proxy propagation**: when running through a custom `ANTHROPIC_BASE_URL` proxy, the `traceparent` header is suppressed by default (some proxies reject unrecognized headers); set `CLAUDE_CODE_PROPAGATE_TRACEPARENT=1` to propagate it to model and HTTP-MCP requests (also gates the subprocess `TRACEPARENT` var). Verified live docs, 2026-07-23; introduction version unpinned.

## Cardinality Controls

Toggle metric attributes to trade granularity for storage cost:

| Variable | Default | Attribute toggled |
|---|---|---|
| `OTEL_METRICS_INCLUDE_SESSION_ID` | `true` | `session.id` |
| `OTEL_METRICS_INCLUDE_VERSION` | `false` | `app.version` |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | `true` | `user.account_uuid`, `user.account_id` |

## Cross-References

- [CC-env-vars-reference.md § OpenTelemetry Exporter Configuration](CC-env-vars-reference.md#opentelemetry-exporter-configuration) — the full OTel exporter env-var surface
- [agent-observability-methods-analysis.md](../../non-cc/agent-observability-methods-analysis.md) — third-party observability platforms that ingest CC's OTel output (Logfire's "zero-config CC" path is CC→Logfire-as-MCP-server, not Logfire parsing CC's OTel)

## Sources

| Source | Content |
|---|---|
| [Claude Code — Monitoring usage][cc-monitoring] | First-party OTel: metrics, logs, events, attribution chain, beta distributed traces, privacy gates, cardinality controls (re-fetched 2026-07-23) |
| [anthropics/claude-code#53954][gh-53954] | Beta-tracing gap in streaming/Agent-SDK mode (live issue) |
| [CC-env-vars-reference.md](CC-env-vars-reference.md) | Full OTel exporter env-var configuration |

[cc-monitoring]: https://code.claude.com/docs/en/monitoring-usage
[gh-53954]: https://github.com/anthropics/claude-code/issues/53954
