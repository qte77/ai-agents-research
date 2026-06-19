---
title: OpenAI Agents SDK Analysis
source: https://openai.github.io/openai-agents-python/
purpose: Production-ready Python framework for building multi-agent workflows with handoffs, guardrails, sessions, and tracing — the successor to Swarm.
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
---

**Status**: Trial

## What It Is

The [OpenAI Agents SDK][docs] (`openai-agents-python`) is a lightweight,
MIT-licensed Python framework for building production multi-agent workflows.
OpenAI published it as the direct, production-ready successor to [Swarm][swarm]
(now Hold/deprecated); the Swarm README itself redirects users here.

The SDK reached v0.17.5 on 2026-06-11 (27 k GitHub stars as of 2026-06-16) and
is listed as GA — no preview or experimental qualification appears in the
repository or documentation (accessed 2026-06-16). It requires Python 3.10+
and is installed via `pip install openai-agents`. There is no separate pricing
for the SDK itself; usage costs derive from whichever LLM API calls are made
at runtime.

## How It Works

Four capabilities distinguish it from its Swarm predecessor:

### Handoffs

Agents declare a `handoffs` list of other `Agent` instances or `Handoff`
objects (created via `handoff()`). The LLM sees each handoff as a callable
tool (e.g., `transfer_to_refund_agent`). When invoked, execution delegates
to the target agent while remaining within a single continuous run — the
conversation thread is not broken. Callbacks (`on_handoff`), dynamic
enable/disable (`is_enabled`), and input filters for history trimming are
configurable per handoff. Nested handoffs are supported in beta.

### Guardrails

Three guardrail types provide validation at different stages:

- **Input guardrails** — screen the initial user message before the first
  agent processes it.
- **Output guardrails** — validate the final agent response before it is
  returned to the caller.
- **Tool guardrails** — wrap function-tool invocations with pre- and
  post-execution checks.

Each guardrail returns a `GuardrailFunctionOutput`; a failed check raises a
tripwire exception that halts execution. Input guardrails run in parallel with
the agent by default (lower latency) or in blocking mode (prevents agent
execution on failure). A common pattern is routing through a cheap, fast model
for abuse detection before engaging a more expensive reasoning model.

### Sessions and State

Session support persists conversation history across runs. Optional Redis
integration (extra dependency) enables distributed session storage. Human-in-
the-loop workflows pause execution for external approval before resuming.

### Tracing

Tracing is on by default. Every LLM generation, tool call, guardrail
evaluation, handoff, and audio event is recorded as a span within a trace,
exported in batches to OpenAI's Traces dashboard. The system uses a Python
`contextvar` so tracing is safe with concurrent async code. Sensitive data
capture can be disabled via `RunConfig.trace_include_sensitive_data`. Beyond
OpenAI's native dashboard, 31+ third-party integrations are documented,
including Weights & Biases, Langfuse, Datadog, MLflow, and Braintrust.
Custom processors can be registered with `add_trace_processor()`.

### Provider Agnosticism

Despite the OpenAI branding, the SDK is documented as supporting 100+ LLMs
via any OpenAI-compatible API endpoint. Non-OpenAI model users can still use
free tracing through an OpenAI API key without routing completions through
OpenAI.

## Adoption Decision

**Trial** — The SDK is mature (v0.17.5, GA, MIT, 27 k stars), actively
maintained, and the declared successor to Swarm. Its abstractions map directly
onto the agent patterns tracked in the [frameworks landscape][landscape]:
handoffs, guardrails, tracing, and session management are all first-class.
Provider agnosticism reduces lock-in risk. The "Trial" rating rather than
"Adopt" reflects that it is still sub-1.0 (semver signals API surface may
shift) and that the target persona here is Claude Code / Anthropic-stack
research, where the Anthropic SDK and Claude Code agent harness cover
overlapping ground. Teams building OpenAI-centric or provider-neutral Python
agent pipelines should adopt it; teams anchored to Claude Code native features
should assess need first.

Cross-ref the deprecated predecessor: [openai-swarm-analysis.md][swarm]

Cross-ref catalog entry: [agent-frameworks-infrastructure-landscape.md][landscape]

## Action Items

- Monitor v1.0 release for API stability signal; re-evaluate "Adopt" threshold.
- Evaluate tracing export compatibility with any existing observability stack
  (Langfuse, Datadog) against the 31+ listed integrations.
- For Claude Code agent research: assess whether handoff/guardrail patterns
  can inform the native CC agent-teams orchestration model.

## Sources

| Source | Content |
|---|---|
| [Agents SDK docs][docs] | Overview, features, installation — accessed 2026-06-16 |
| [GitHub repo][repo] | License (MIT), v0.17.5 release date, star count — accessed 2026-06-16 |
| [Handoffs docs][handoffs] | Handoff API, configuration options, nesting — accessed 2026-06-16 |
| [Guardrails docs][guardrails] | Guardrail types, execution modes, tripwires — accessed 2026-06-16 |
| [Tracing docs][tracing] | Span types, backends, 31+ integrations — accessed 2026-06-16 |
| [Swarm repo (deprecated)][swarm-repo] | Predecessor relationship, redirect notice — accessed 2026-06-16 |

[docs]: https://openai.github.io/openai-agents-python/
[repo]: https://github.com/openai/openai-agents-python
[handoffs]: https://openai.github.io/openai-agents-python/handoffs/
[guardrails]: https://openai.github.io/openai-agents-python/guardrails/
[tracing]: https://openai.github.io/openai-agents-python/tracing/
[swarm-repo]: https://github.com/openai/swarm
[swarm]: openai-swarm-analysis.md
[landscape]: agent-frameworks-infrastructure-landscape.md
