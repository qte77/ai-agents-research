---
title: CC Agent Teams Orchestration
source: https://code.claude.com/docs/en/agent-teams
purpose: Analysis of Claude Code Agent Teams for parallel code review, cross-layer implementation, and adversarial debugging.
test_run: 2026-02-11 (parallel code review with 3 teammates)
created: 2026-02-08
updated: 2026-04-05
validated_links: 2026-04-05
---

**Status**: Research preview (disabled by default, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)

## What Agent Teams Offer

Coordinates multiple independent CC sessions with:

- **Lead/teammate hierarchy** with shared task list and mailbox messaging
- **Inter-agent communication** — direct teammate-to-teammate messaging via tmux (v2.1.33)
- **Parallel execution** — each teammate has its own context window
- **Task dependency management** with automatic unblocking
- **Quality gates** via `TeammateIdle` and `TaskCompleted` hook events (v2.1.33)
- **Delegate mode** — restricts lead to coordination only ([source][cc-teams-docs])
- **Plan approval** — teammates plan in read-only mode; lead approves/rejects autonomously ([source][cc-teams-docs])
- **Agent memory** — teammates have user/project/local scoped memory (v2.1.33)
- **Worktree isolation** — `isolation: worktree` gives each agent an isolated repo copy (v2.1.49–v2.1.50). Worktree auto-cleaned if agent makes no changes; path and branch returned if changes exist. `.claude/` project configs auto-shared across worktrees (v2.1.63) — no duplication or symlinking needed
- **Background agents** — `background: true` lets agents run while user works (v2.1.49, v2.0.60); Ctrl+F kills background agents (two-press confirmation, v2.1.49)
- **Agent frontmatter hooks** — PreToolUse, PostToolUse, Stop hooks in agent definitions (v2.1.0)
- **Agent spawning restrictions** — `Task(agent_type)` controls which agents can spawn (v2.1.33)
- **`claude agents` CLI** — manage agents from the command line (v2.1.50)

### How It Works

- Lead spawns teammates, coordinates work; each teammate is a full CC instance
- Shared task list (pending/in-progress/completed) with dependency tracking
- Teammates load project context (project instructions, MCP servers, skills) automatically
- Lead's conversation history does NOT carry over to teammates
- Display modes: in-process (single terminal, Shift+Down to cycle teammates) or split panes (tmux/iTerm2, click into pane)
- `--teammate-mode` CLI flag: `in-process`, `tmux`, or `auto` (default). `auto` uses split panes if already inside tmux, in-process otherwise
- `teammateMode` in `settings.json` for persistent config; iTerm2 split panes require [`it2` CLI](https://github.com/mkusaka/it2) + Python API enabled

### Configuration

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

### Delegate Mode

Restricts lead to coordination-only (spawn, assign, synthesize). Blocks direct implementation. Toggle with **Shift+Tab** after starting a team. ([source][cc-teams-docs])

**Use when**: Lead keeps implementing instead of delegating; 3+ teammates. **Skip when**: Task is already pure coordination; small teams.

### Agent Customization (v2.0.59+)

- `--agent` CLI flag overrides agent configuration for a session
- `agent` setting customizes main thread behavior
- `--resume` reuses `--agent` value from previous session (v2.1.32)
- Agent disabling via `Task(AgentName)` syntax (v2.1.0)
- `skills` frontmatter auto-loads skills for subagents (v2.0.43)
- Bedrock/Vertex/Foundry support for teammates (v2.1.45)

### Agent Teams vs Subagents (Task tool)

| Aspect | Subagents | Agent Teams |
| -------- | ----------- | ------------- |
| Context | Own window; results return to caller | Own window; fully independent |
| Communication | Report back to main agent only | Teammates message each other directly |
| Coordination | Main agent manages all work | Shared task list with self-coordination |
| Best for | Focused tasks where only the result matters | Complex work requiring discussion and collaboration |
| Token cost | Lower: results summarized back | Higher: each teammate is a separate instance |

## Use Cases

| Use Case | Fit | Rationale |
| -------- | --- | --------- |
| Parallel code review (security + performance + coverage) | Strong | 3 reviewers run simultaneously with different lenses |
| Cross-layer feature implementation (backend + tests) | Strong | Enforces role separation (architect/developer/reviewer) |
| Research + competing hypotheses debugging | Strong | Adversarial debate addresses anchoring bias |

**Overlaps**: Subagents for fire-and-forget work (replace only when inter-agent communication needed). An autonomous development loop can support teams mode for inter-story parallelism. Skills load automatically in teammates.

## Key Limitations

1. **No session resumption (in-process)** — `/resume` and `/rewind` do not restore in-process teammates; lead may message non-existent agents ([source][cc-teams-docs])
2. **Task status can lag** — teammates sometimes don't mark tasks complete, blocking dependents
3. **No nested teams** — teammates can't spawn their own teams or teammates ([source][cc-teams-docs])
4. **One team per session** — clean up current team before starting a new one ([source][cc-teams-docs])
5. **Lead is fixed** — session that creates the team is lead for its lifetime; no promotion or transfer ([source][cc-teams-docs])
6. **Permissions set at spawn** — all teammates inherit lead's mode; can change individually after spawn but not at spawn time ([source][cc-teams-docs])
7. **Shutdown can be slow** — teammates finish current request/tool call before exiting ([source][cc-teams-docs])
8. **Linear token cost** — each teammate is a separate Claude instance ([source][cc-teams-docs])
9. **Experimental, disabled by default** ([source][cc-teams-docs])
10. **Split panes require tmux or iTerm2** — not supported in VS Code terminal, Windows Terminal, or Ghostty ([source][cc-teams-docs])
11. **Agent Teams crash fixes ongoing** — v2.1.34, v2.1.41 addressed model identifier and crash issues
12. **`isolation: "worktree"` silently ignored with `team_name`** — worktree creation skipped; all teammates run in lead's CWD causing file-edit race conditions. Agent Teams remain experimental (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, [docs][cc-teams-docs]). The official [Limitations section][cc-teams-limits] lists 8 items but does not mention this bug. `isolation: "worktree"` is [documented as a subagent frontmatter field][cc-subagent-isolation] ("creates a temporary git worktree so the agent works on an isolated copy of the repo") and works correctly for non-team subagents (v2.1.49+). Root cause: teammate subprocess spawn command omits worktree flags when `team_name` is present ([repro in #38949][wt-38949]). No Anthropic fix timeline as of v2.1.83 (2026-03-26). Issues: [#38949][wt-38949] (has repro, 2026-03-25), [#33045][wt-33045] (oldest, 7 comments, 2026-03-18), [#37549][wt-37549] (2026-03-22). Feature request: [#37587][wt-37587] (extend `EnterWorktree` for team orchestration). **Mitigations**: (a) standalone `Agent` + `isolation: "worktree"` without `team_name` — worktrees work but lose team coordination (shared task list, SendMessage); (b) teams without worktree + file-partitioned tasks — no conflicts if each teammate edits different files; (c) accept shared-CWD chaos — agents self-heal via cherry-picks but waste tokens (validated: 10 PRs across 2 team runs, all delivered despite races, CC v2.1.83, 2026-03-26).

[wt-38949]: https://github.com/anthropics/claude-code/issues/38949
[wt-33045]: https://github.com/anthropics/claude-code/issues/33045
[wt-37549]: https://github.com/anthropics/claude-code/issues/37549
[wt-37587]: https://github.com/anthropics/claude-code/issues/37587
[cc-teams-limits]: https://code.claude.com/docs/en/agent-teams#limitations
[cc-subagent-isolation]: https://code.claude.com/docs/en/sub-agents#supported-frontmatter-fields

## When to Use Each Mode

**Single CC Session**: Sequential workflows, prompt engineering, pipeline debugging, single-file changes, test writing. Full context retention, lower cost.

**Agent Teams**: 3+ independent files, multiple review perspectives, competing approaches, large refactoring. See Test Results section below.

## Benchmarking a MAS vs CC-Style Baselines

Compare a multi-agent system (MAS) against simpler patterns using the same evaluation pipeline.

**Example baselines** (all within a shared codebase):

1. **MAS** (e.g., Manager → Researcher → Analyst → Synthesizer): Sequential delegation with approval loop, structured data models, token tracking, observability
2. **Single-Agent**: One agent, one pass, no delegation — tests value of multi-agent orchestration
3. **Parallel-Agents**: Independent agents via `asyncio.gather`, coordinator merges — tests parallel vs sequential

**Evaluation**: All produce a structured output scored via a shared evaluation pipeline.

| Tier | Measures |
| ---- | -------- |
| 1 | Multi-agent vs single-pass quality |
| 2 | Approval loop value (validation vs no validation) |
| 3 | Coordination overhead (delegation chain efficiency) |

**Hypothesis**: Approval loop is key for Tier 2 quality. If single-agent matches, multi-agent overhead unjustified. If parallel matches at lower latency, reconsider sequential.

**Key components**: agent system, orchestration layer, evaluation pipeline, data models, chat and eval configuration files.

## Tracing & Observability

**Gap**: A MAS with application-level tracing (e.g., Logfire/Phoenix) needs equivalent coverage for CC baselines.

### Approach Comparison

| Dimension | OTel -> Phoenix (recommended) | Hooks -> Phoenix | Artifact collection |
| --------- | ----------------------------- | ---------------- | ------------------- |
| Same Phoenix instance | Yes | Yes | No (file-based) |
| Token/cost tracking | Yes | No | No |
| Tool-level traces | Yes | Yes | Yes (via a trace adapter parsing `raw_stream.jsonl`) |
| LLM-call traces | Yes | No | No |
| Trace spans | No — upstream limitation | No | Yes — via artifact collection |
| Setup complexity | Medium (Collector) | Low (script) | Low (parse files) |
| Unified dashboard | Yes | Yes | No |
| In settings.json | Yes (vars exist, currently disabled) | No | No |

**Task Tool Metrics** (v2.1.30): Task completions now include per-task metrics (tokens consumed, tool uses, duration) natively in the task completion response — no OTel required. Useful for cost/performance tracking per teammate without additional infrastructure.

**Upstream limitation**: CC OTel exports metrics and logs only — no trace spans. This is a known limitation tracked in [anthropics/claude-code#9584](https://github.com/anthropics/claude-code/issues/9584) and [#2090](https://github.com/anthropics/claude-code/issues/2090). Until resolved, trace-level execution analysis requires artifact collection: parse `raw_stream.jsonl` for `TeamCreate`, `Task`, `TodoWrite` events into structured trace data.

### OTel -> Phoenix (Recommended)

Can be configured in `.claude/settings.json`. Richest data, reuses an existing Phoenix OTLP endpoint.

**Full enabled config** (`settings.json` env section):

```json
{
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://localhost:4317",
    "OTEL_EXPORTER_OTLP_METRICS_PROTOCOL": "grpc"
}
```

**Optional**: `OTEL_LOG_TOOL_DETAILS`: `"1"`, `OTEL_LOG_USER_PROMPTS`: `"1"`, `OTEL_RESOURCE_ATTRIBUTES`: `"project=your-project-name"`, `OTEL_METRIC_EXPORT_INTERVAL`: `"10000"` (10s for testing)

**Infrastructure**: A Phoenix container accepts OTLP on `:4317` (gRPC) and `:6006` (HTTP). No additional infrastructure needed once Phoenix is running.

### Hooks -> Phoenix (Fallback)

`PostToolUse` hook script sending traces to Phoenix OTLP endpoint. Lower setup (single script), coarser data (tool-level only, no token/cost). Sufficient for coarse Tier 3 execution graphs.

### Langfuse (Last Resort)

Official CC integration. Turnkey setup but splits observability across two platforms. Use only if OTel approach proves insufficient.

### Integration Points

CC OTel integrates at the infrastructure level (env vars + Phoenix endpoint), separate from any application-level instrumentation (e.g., PydanticAI Logfire). It can be enabled or disabled without touching application source code.

### References

- [CC Monitoring/OTel docs][cc-mon] — env var reference, metrics/events
- [CC Settings docs][cc-set] — `CLAUDE_CODE_ENABLE_TELEMETRY`
- [CC ROI Measurement Guide][cc-roi] — Docker Compose, Prometheus/OTel setups
- [CC on Bedrock monitoring][cc-bed]
- [OTel exporter spec][otel-spec]
- [Langfuse CC integration][langfuse]
- [Phoenix Arize docs][phoenix-docs]

[cc-mon]: https://code.claude.com/docs/en/monitoring-usage
[cc-set]: https://code.claude.com/docs/en/settings
[cc-roi]: https://github.com/anthropics/claude-code-monitoring-guide
[cc-bed]: https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md
[otel-spec]: https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md
[langfuse]: https://langfuse.com/integrations/other/claude-code
[phoenix-docs]: https://docs.arize.com/phoenix

## Recommendation

**Useful but premature as core infrastructure.**

**Adopt now**: Parallel code reviews, multi-angle research, competing hypotheses debugging. Low-risk, high-value, clear boundaries.

**Wait on**: Replacing an autonomous development loop or subagent architecture. Limitations (no resumption, task lag, no nested teams) make it unreliable for structured workflows.

**When ready**: Enable in `settings.json`, start with review/research tasks, pre-approve common operations, use delegate mode for 3+ teammates.

### Observability Strategy for CC Evaluation

- **Artifact collection is primary** for evaluation: parse `raw_stream.jsonl` for `TeamCreate`, `Task`, `TodoWrite` events into structured trace data → feed evaluation pipeline
- **OTel is supplementary** for cost/token dashboards only (metrics + logs, no trace spans due to upstream limitation)
- **`settings.json` OTel vars** (`OTEL_EXPORTER_OTLP_PROTOCOL`, `OTEL_LOGS_EXPORTER`, `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`) are disabled by default (empty string values). Enable to collect cost/token metrics in Phoenix; does not provide trace spans.

## Trace & Communication Storage

Agent Teams artifacts stored under `~/.claude/`:

```text
~/.claude/
├── teams/
│   └── {team-name}/
│       ├── config.json              # Team metadata and member roster
│       └── inboxes/
│           ├── {agent-1}.json       # Mailbox for agent 1
│           ├── {agent-2}.json       # Mailbox for agent 2
│           └── {agent-n}.json       # Mailbox for agent n
├── tasks/
│   └── {team-name}/
│       ├── 1.json                   # Task 1 metadata
│       ├── 2.json                   # Task 2 metadata
│       └── n.json                   # Task n metadata
└── transcripts/                     # Full teammate session logs (if enabled)
    └── {session-id}.jsonl
```

### 1. Team Configuration

**Location**: `~/.claude/teams/{team-name}/config.json`

Contains complete team orchestration metadata:

```json
{
  "name": "parallel-code-review",
  "description": "Parallel review of src/pipeline.py...",
  "createdAt": 1770854157287,
  "leadAgentId": "team-lead@parallel-code-review",
  "leadSessionId": "e41ee506-14e0-49c7-b933-de43cac57810",
  "members": [
    {
      "agentId": "security-reviewer@parallel-code-review",
      "name": "security-reviewer",
      "agentType": "general-purpose",
      "model": "claude-opus-4-6",
      "prompt": "MANDATORY: Read project instructions first...",
      "color": "blue",
      "planModeRequired": false,
      "joinedAt": 1770854199673,
      "tmuxPaneId": "in-process",
      "cwd": "/workspaces/your-project",
      "backendType": "in-process"
    }
    // ... other members
  ]
}
```

**Key fields**:

- `members[]`: Complete roster with prompts, models, colors, join timestamps
- `model`: Shows which model each teammate uses (Opus 4.6 for teammates, Sonnet 4.5 for lead)
- `prompt`: Full prompt given to each teammate at spawn time
- `backendType`: Execution mode (`in-process` vs split panes)

### 2. Inter-Agent Messages (Mailboxes)

**Location**: `~/.claude/teams/{team-name}/inboxes/{agent-name}.json`

Each agent has its own mailbox file containing all messages received:

```json
[
  {
    "from": "quality-reviewer",
    "text": "## Quality Review Findings: src/pipeline.py\n\n...",
    "summary": "Quality review findings for src/pipeline.py",
    "timestamp": "2026-02-11T23:57:29.518Z",
    "color": "green",
    "read": true
  },
  {
    "from": "security-reviewer",
    "text": "# Security Review: src/pipeline.py\n\n...",
    "summary": "Security review findings for src/pipeline.py",
    "timestamp": "2026-02-11T23:57:55.822Z",
    "color": "blue",
    "read": true
  }
]
```

**Message types captured**:

- **Review findings**: Full markdown-formatted reports
- **Idle notifications**: JSON structured `{"type":"idle_notification",...}`
- **Task assignments**: JSON structured `{"type":"task_assignment",...}`
- **Peer DM summaries**: Brief snippets when teammates message each other

**Practical example from test run**:

- `team-lead.json`: Received 3 complete review reports + idle notifications
- `security-reviewer.json`: Received task assignments from lead
- `quality-reviewer.json`: Received task assignments from lead
- `coverage-reviewer.json`: Received task assignments from lead

### 3. Task Tracking

**Location**: `~/.claude/tasks/{team-name}/{task-id}.json`

Each task is tracked in its own JSON file:

```json
{
  "id": "1",
  "subject": "Security review of src/pipeline.py",
  "description": "Review src/pipeline.py for...",
  "activeForm": "Reviewing security vulnerabilities",
  "owner": "security-reviewer",
  "status": "completed",
  "blocks": ["4"],
  "blockedBy": []
}
```

**Key behaviors**: File locking prevents race conditions on task claiming. Teammates inherit lead's permissions. Context is fully isolated per teammate.

### Example Results

3-teammate parallel code review of a single source file:

- **Team**: Lead + security/quality/coverage reviewers (one model each)
- **Execution**: ~26 seconds for 3 complete reviews (quality first, coverage +6s, security +20s)
- **Dependencies**: Tasks 1-3 ran in parallel; task 4 (aggregation) waited for all 3
- **Output**: Full review content preserved in mailboxes

### Trace Correlation Strategy

- **Application traces** (MAS): Application-level tracing (e.g., Phoenix OTLP endpoint, Logfire SDK)
- **Agent Teams traces** (CC orchestration): `~/.claude/teams/` + `~/.claude/tasks/`, file-based JSON
- **Unified approach**: Application-level tracing for the MAS layer, CC artifact files for the orchestration layer; cross-reference by timestamps

## UDS Inbox — Inter-Session IPC (Unreleased)

Unix Domain Socket messaging layer for local inter-session communication between CC instances. This is the networking substrate underneath Coordinator Mode and Agent Teams.

**Provenance**: Sourced from `@anthropic-ai/claude-code@2.1.88` npm sourcemap exposure ([2026-03-31][register-leak]). Not officially documented by Anthropic.

### Architecture

- UDS messaging server starts automatically at session launch (skipped in `--bare` mode)
- Socket location: `~/.claude/sessions/`
- **Dual addressing**: local paths (`uds:/.../sock`) and remote endpoints (`bridge:...`)

### Core Tools

| Tool | Purpose |
|------|---------|
| `SendMessage` | Inter-session data exchange |
| `ListPeers` | Discover active CC sessions on the machine |
| Coordinator dispatch | Route tasks to worker agents |

Workers respond via XML-based `<task-notification>` protocol with fields for status, summary, token usage, and duration.

### Transport Layer Comparison

| Transport | Direction | Purpose | Protocol |
|-----------|-----------|---------|----------|
| IDE WebSocket | IDE ↔ Claude | Editor integration (selection, diff, file context) | WebSocket JSON-RPC 2.0 (MCP) |
| Channels | External → Claude | Push events from Telegram, Discord, iMessage | MCP over channel adapters |
| **UDS Inbox** | Claude ↔ Claude | Inter-session IPC on same machine | Unix Domain Sockets |

Cross-ref: [CC-ide-integration-protocol.md](../configuration/CC-ide-integration-protocol.md) — WebSocket IDE protocol; [CC-channels-analysis.md](../plugins-ecosystem/CC-channels-analysis.md) — external push channels

## Coordinator Mode — Internal Orchestration (Unreleased)

Multi-agent orchestration mode activated via `CLAUDE_CODE_COORDINATOR_MODE=1`. Transforms CC from a single agent into a coordinator that spawns and manages multiple worker agents in parallel. The coordinator itself has **no filesystem/shell tools** — it is a pure management layer that relies on UDS Inbox for all worker communication.

**Provenance**: Sourced from `@anthropic-ai/claude-code@2.1.88` npm sourcemap exposure ([2026-03-31][register-leak]). Not officially documented by Anthropic.

### Four-Phase Workflow

| Phase | Actor | Purpose |
|-------|-------|---------|
| Research | Workers (parallel) | Investigate codebase, find files, understand problem |
| Synthesis | **Coordinator** | Read findings, understand problem, craft implementation specs |
| Implementation | Workers | Make targeted changes per spec, commit |
| Verification | Workers | Test changes work |

### Key Mechanisms

- **Shared scratchpad** (`tengu_scratch` feature gate) — durable cross-worker knowledge sharing directory
- **Agent Teams/Swarm** (`tengu_amber_flint` feature gate) — in-process teammates via `AsyncLocalStorage` for context isolation, or process-based teammates via tmux/iTerm2 panes
- **Penguin Mode kill switch** (`tengu_penguins_off`) — disables fast mode for coordinator sessions
- **Anti-lazy-delegation rule**: coordinator prompt forbids *"based on your findings"* — must read actual findings and specify exactly what to do

### Relationship to Agent Teams

Coordinator Mode and Agent Teams are complementary:

- **Agent Teams** (current, experimental): User-facing team orchestration via shared task list + mailboxes. Communication via file-based JSON inboxes under `~/.claude/teams/`
- **Coordinator Mode** (unreleased): Internal orchestration layer using UDS for real-time IPC. Coordinator has no tools except worker management

Cross-ref: [CC-community-reimplementations-landscape.md](../../cc-community/CC-community-reimplementations-landscape.md) — CLAURST documents Coordinator Mode phases and tool registry

### Sources

| Source | Author | Key Content |
| ------ | ------ | ----------- |
| [Official CC Agent Teams docs][cc-teams-docs] | Anthropic | Architecture, task lists, mailbox, storage |
| [Agent Teams Announcement][anthropic-teams] | Anthropic | Feature announcement |
| [Claude Code Swarms][addy-swarms] | Addy Osmani | Swarm patterns, competing hypotheses |
| [Setup and Use Guide][medium-setup] | D. Sobaloju | Practical examples, troubleshooting |
| [Agent Orchestration Analysis][linkedin-trace] | Sigrid Jin | `~/.claude/teams` structure analysis |
| [Agent Teams Guide][claudefast] | Community | Multi-session orchestration guide |
| [Porting to OpenCode][dev-opencode] | Uenyioha | Architecture comparison |
| [Aura Frog Guide][aura-frog] | Community | Structured workflow integration |
| [C Compiler with 16 Agents][compiler-case] | Anthropic/Register | 2,000 sessions, 100k-line compiler |

[cc-teams-docs]: https://code.claude.com/docs/en/agent-teams
[anthropic-teams]: https://www.anthropic.com/engineering/building-c-compiler
[addy-swarms]: https://addyosmani.com/blog/claude-code-agent-teams/
[medium-setup]: https://darasoba.medium.com/how-to-set-up-and-use-claude-code-agent-teams-and-actually-get-great-results-9a34f8648f6d
[linkedin-trace]: https://www.linkedin.com/pulse/how-claude-code-orchestrate-team-agents-sigrid-jin--msedc
[claudefast]: https://claudefa.st/blog/guide/agents/agent-teams
[dev-opencode]: https://dev.to/uenyioha/porting-claude-codes-agent-teams-to-opencode-4hol
[aura-frog]: https://github.com/nguyenthienthanh/aura-frog/blob/main/aura-frog/docs/AGENT_TEAMS_GUIDE.md
[compiler-case]: https://www.theregister.com/2026/02/09/claude_opus_46_compiler/
[register-leak]: https://www.theregister.com/2026/03/31/anthropic_claude_code_source_code/
[techsy-leaked]: https://techsy.io/blog/claude-code-leaked-features-2026
[minbook-hidden]: https://minbook.dev/en/blog/claude-code-anatomy-hidden-features/
[zread-coordinator]: https://zread.ai/instructkr/claude-code/19-coordinator-mode
