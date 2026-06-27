---
title: "Multi-Agent System Design Principles"
purpose: Core design principles for multi-agent systems synthesized from 12-Factor Agents, Anthropic Effective Harnesses, and PydanticAI.
created: 2026-02-09
updated: 2026-06-27
validated_links: 2026-06-27
---

**Status**: Adopt

Synthesized from
[12-Factor Agents][12fa-blog] (Dex Horthy / [HumanLayer][humanlayer], 2025-04-03; accessed 2026-06-19),
[Anthropic Effective Harnesses][ant-harness],
and [PydanticAI][pydantic-ai].
HumanLayer is the org behind the spec and ships a human-in-the-loop approval-gate SDK
that implements factor #7 directly. Factor numbering follows the canonical post — they
have been renumbered across releases, so the access date matters.
GitHub mirror: [github.com/humanlayer/12-factor-agents][12fa-gh].

## 12-Factor Agents

### #1: Natural Language to Tool Calls

Convert natural language into structured tool calls that deterministic code
can execute via a simple switch-statement dispatcher. The LLM produces JSON;
the harness executes it — keeping model reasoning separate from application
logic. CC: tool-use architecture (model emits structured JSON, harness
dispatches execution).

### #2: Own Your Prompts

Treat prompts as first-class, testable code artifacts — not framework black
boxes hidden behind abstraction layers. Version-control and test them like
any other source. CC: CLAUDE.md and skills files are engineered,
version-controlled prompt artifacts that encode agent behavior explicitly.

### #3: Own Your Context Window

Structure and control how information is presented to the LLM. Curate what
enters the context window rather than letting frameworks decide. Related
principle from 12-Factor App: store configuration in environment variables,
not code or JSON files; use typed settings classes (e.g., `BaseSettings`)
with env-var prefixes per module.

### #4: Tools Are Just Structured Outputs

Decouple the LLM's JSON output from application execution. Tool calls are
simply structured data the model emits; deterministic code handles the side
effects. Related principle from 12-Factor App: treat LLM providers, trace
stores, and databases as swappable resources behind interfaces.
Plugin/registry patterns enable runtime discovery without vendor lock-in.

### #5: Unify Execution State and Business State

Consolidate agent execution state and business-domain state into a single
source of truth rather than maintaining parallel state machines. Reduces
drift and makes agent behavior auditable.

### #6: Launch/Pause/Resume with Simple APIs

Serialize durable state so agents can be interrupted and resumed through
straightforward APIs — no bespoke recovery logic per workflow. CC: headless
mode + cloud sessions provide the launch/pause/resume surface.

### #7: Contact Humans with Tool Calls

Request human input and approval via structured tool definitions, not special
tokens or out-of-band syntax. Human contact is just another tool call with a
well-typed schema. CC: permission prompts expose this pattern natively;
HumanLayer's approval-gate SDK implements it as a first-class service.

### #8: Own Your Control Flow

Build control structures appropriate for the specific use case rather than
relying on generic agent loops. Agent components should behave as stateless
pure functions: `(context) -> result`. Persist state externally (database,
trace store). Enables horizontal scaling and deterministic behavior.

### #9: Compact Errors into Context Window

Incorporate error messages back into the context window so the agent can
self-heal on the next step. Component errors produce structured partial
results, not crashes. Per-component timeouts prevent cascading failures.

### #10: Small, Focused Agents

Design agents with narrow scopes (roughly 3–20 steps) to keep context
windows manageable and behavior predictable. Same architecture in all
environments; environment variables control behavior differences, not code
branches.

### #11: Trigger from Anywhere

Outer-loop agents should be launchable via HTTP, message queue, Slack,
email, SMS, or cron — not tied to a single entry point. CC: GitHub Actions
triggers and remote cloud sessions provide this multi-channel activation
surface.

### #12: Make Your Agent a Stateless Reducer

Implement agents as functional transformations of state: `(state, event) ->
(state, actions)`. Structured logging with JSON output; traces capture agent
event streams; queryable audit trails for debugging and compliance.

## 12-Factor App Alignment

The factors above blend 12-Factor Agents (Horthy/HumanLayer, 2025) with
principles from the original [12-Factor App][12fa-app] methodology (Heroku,
2011) where they map directly: config in environment (#3), backing services
(#4), stateless processes (#8), dev/prod parity (#10), logs as event streams
(#12).

## Anthropic Harnesses

### Incremental Boundaries

Break long-running tasks into checkpoints where state
is saved and validated. Each stage produces typed output
consumable by the next. Explicit boundary methods define
what context passes forward.

### Structured State Management

Use typed data structures for all inter-component state.
No raw dicts or untyped strings between stages. Explicit
context arguments, no implicit data passing.

## Framework Patterns

### Typed Outputs

Use validated models for agent outputs, not unstructured
text. Schema enforcement at boundaries catches errors
early and provides self-documenting API contracts.

### Provider Abstraction

Abstract LLM provider details behind a unified interface.
Same agent code works across providers (OpenAI,
Anthropic, Gemini, local). Configurable via environment
variables.

## Agent/Plugin Design Checklist

For security-specific checks, see the
[Security Checklist](mas-security-framework.md#security-checklist).

- [ ] **Stateless Reducer**: Pure function, no shared state
- [ ] **Own Context Window**: Manages own context
- [ ] **Structured Outputs**: Typed validated model
- [ ] **Own Control Flow**: Handles errors and timeouts
- [ ] **Compact Errors**: Structured results, not exceptions
- [ ] **Single Responsibility**: One task per component
- [ ] **Type-Safe Boundaries**: Contracts enforced
- [ ] **Environment Config**: Settings via env vars
- [ ] **Graceful Degradation**: Partial results on failure
- [ ] **Observable**: Structured logs and traces

## References

- [12-Factor Agents — canonical post][12fa-blog] (Dex Horthy / HumanLayer, 2025-04-03; accessed 2026-06-19)
- [12-Factor Agents — GitHub mirror][12fa-gh]
- [HumanLayer][humanlayer] — human-in-the-loop approval-gate SDK (implements factor #7)
- [Anthropic: Effective Harnesses][ant-harness]
- [PydanticAI][pydantic-ai]
- [12-Factor App][12fa-app] (Heroku, 2011) — original methodology
- [OWASP MAESTRO][owasp-maestro]

[12fa-blog]: https://www.hlyr.dev/blog/12-factor-agents
[12fa-gh]: https://github.com/humanlayer/12-factor-agents
[12fa-app]: https://12factor.net/
[humanlayer]: https://www.humanlayer.dev/
[ant-harness]: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
[pydantic-ai]: https://ai.pydantic.dev/
[owasp-maestro]: https://genai.owasp.org/resource/multi-agentic-system-threat-modeling-guide-v1-0/
