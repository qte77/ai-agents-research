---
title: CC Monitoring & Telemetry (First-Party OTel)
purpose: Claude Code's first-party OpenTelemetry integration — span hierarchy, distributed-trace propagation, privacy-default gates, and metric cardinality controls for monitoring CC agent behavior.
category: analysis
created: 2026-06-27
updated: 2026-06-27
validated_links: 2026-06-27
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
- Tool span attributes include `file_path` (Read/Edit/Write), `full_command` (Bash), `skill_name` (Skill tool), `subagent_type` (Task tool) — all gated behind `OTEL_LOG_TOOL_DETAILS`

## Privacy-First Defaults

All sensitive attributes are **redacted unless explicitly unlocked**:

| Gate | What it reveals |
|---|---|
| `OTEL_LOG_USER_PROMPTS` | Prompt text on `user_prompt` events / interaction span |
| `OTEL_LOG_TOOL_DETAILS` | Bash command, MCP tool name, Skill name, file path, subagent type |
| `OTEL_LOG_TOOL_CONTENT` | Tool input/output content in span events (60 KB truncation) |
| `OTEL_LOG_RAW_API_BODIES` | Full Anthropic API request/response JSON (`1` inline / `file:<dir>` to disk with `body_ref`) |

This is notably stricter than most third-party LLM observability platforms, which default to capturing prompts and tool I/O.

## Distributed Trace Propagation

`TRACEPARENT` is auto-injected into Bash and PowerShell subprocesses so any W3C-compliant child can parent its spans under the active tool execution span. In Agent SDK and headless (`claude -p`) sessions, CC **reads** `TRACEPARENT` + `TRACESTATE` from its own environment so an embedding process can pass in its active context. Interactive sessions deliberately ignore inbound `TRACEPARENT` to prevent accidental inheritance from CI/container ambient values.

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
| [Claude Code — Monitoring usage][cc-monitoring] | First-party OTel: metrics, logs, beta distributed traces, privacy gates, cardinality controls |
| [CC-env-vars-reference.md](CC-env-vars-reference.md) | Full OTel exporter env-var configuration |

[cc-monitoring]: https://code.claude.com/docs/en/monitoring-usage
