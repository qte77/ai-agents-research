---
title: Omnigent — Meta-Harness for Multi-Agent Unification
source: https://omnigent.ai/
purpose: Evaluate Omnigent as a meta-harness layer for unifying Claude Code, Codex, Pi, and custom agents with policy governance and OS-level sandboxing
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
platform_scope: [claude-code, codex, pi, custom-agents, openai-agents]
---

**Status**: Assess

## What It Is

[Omnigent][omnigent-home] is an open-source meta-harness that sits above individual AI agent frameworks,
providing a unified layer for running and supervising multiple agents — [Claude Code][omnigent-home],
Codex, Pi, and custom YAML-defined agents — without rewriting code per-agent. It was introduced by
the Databricks AI team and Neon in June 2026 as an alpha release.

The key framing from [the Databricks blog][databricks-blog]: a meta-harness operates at a layer above
individual agent frameworks, enabling agents "to become interoperable parts of a richer system" rather
than siloed tools.

Cross-ref: [Agent Frameworks & Infrastructure Landscape](agent-frameworks-infrastructure-landscape.md)

## How It Works

**Architecture (fetched from [omnigent.ai][omnigent-home] and [GitHub][omnigent-gh], 2026-06-16):**

Sessions run through a sandboxed runner (local, [Modal][omnigent-home], or Daytona) connected to a server
that manages policies and session history. Access is via CLI, web UI, native apps, mobile, and REST API.
Sessions are persistent and cross-device: start in terminal, continue in browser, pick up on mobile.

**Agent integration:**

Omnigent supports switching between Claude Code (via the `claude-sdk` harness), Codex, Pi, OpenAI agents,
and custom agents with one-line config changes. Claude Code uses Anthropic-compatible gateway endpoints;
Codex uses OpenAI-compatible ones. Model routing is declared in per-agent YAML under the `executor`
section, and models can be swapped mid-session with `/model` while preserving conversation history and
tool state — documented in the [models reference][omnigent-models].

For Databricks routing, model names require a `databricks-` prefix, which directs requests through the
workspace's Foundation Model API.

**Policy governance:**

- **Contextual policies** — dynamic session-state-aware rules; e.g., require human approval after a
  package download, restrict write access to files the agent created
- **Spend caps** — monitor LLM cost per session; pause and prompt after a configurable threshold
- **Risk-based escalation** — route actions to human review based on session risk signals

**OS-level sandboxing (Databricks security team contribution):**

A flexible sandbox can intercept and transform network requests and prevent agents from accessing
sensitive credentials. Filesystem and network restrictions apply with credential isolation. Cloud
sandboxes (Modal, Daytona, Islo) provide disposable ephemeral environments.

**Built-in agents:**

- **Polly** — coding orchestrator agent
- **Debby** — debate/deliberation model
- Custom agents defined via YAML configuration

**Collaboration:**

Real-time session sharing via URL with comment and steering capabilities for co-driving with teammates.

**Technical facts (GitHub, 2026-06-16):**

- Stars: 1.9k
- Primary language: Python (83.1%), TypeScript (16.2%)
- Requires Python 3.12+
- Install: `uv tool install omnigent` or `brew install omnigent-ai/tap/omnigent`
- License: Apache-2.0
- Status: alpha

## Adoption Decision

**Assess** — Omnigent addresses a genuine gap: there is no established neutral layer for routing work
across Claude Code, Codex, Pi, and custom agents with unified policy controls. The Databricks AI + Neon
lineage gives it a credible security posture (OS sandbox, credential isolation) beyond what individual
agent harnesses provide.

For this repo's agent-research context, the CC integration surface is meaningful — Claude Code is a
first-class supported harness with explicit `claude-sdk` routing — making this directly relevant to
ongoing multi-agent orchestration research.

**Trade-offs and risks:**

- Alpha status means the API surface and YAML schema will change; any integration built today carries
  migration risk.
- 1.9k stars (June 2026) is early-adopter territory; community and ecosystem are not yet established.
- Policy expressiveness (contextual rules, spend caps) is useful but the implementation details are not
  yet documented beyond high-level examples.
- Sandboxing is a first-class feature but cloud sandbox providers (Modal, Daytona, Islo) introduce
  external dependencies and latency.
- The model-routing approach (YAML executor sections, `/model` mid-session swap) is pragmatic but adds
  a new config dialect on top of per-agent configs already maintained.

**Not recommended for production** until the API stabilizes past alpha. Worth prototyping the
Claude Code + policy-governance path to assess real friction.

## Action Items

- Prototype: install via `uv tool install omnigent` and wire up a Claude Code session to validate the
  `claude-sdk` harness integration and spend-cap policy behavior.
- Track: watch [omnigent-ai/omnigent][omnigent-gh] for a beta/stable tag before committing to the
  YAML config schema.
- Evaluate: compare Omnigent's contextual policy controls against native Claude Code hooks
  (`.claude/settings.json` permissions, `PreToolUse` hooks) to identify whether the meta-layer adds
  meaningful governance beyond what CC already provides.
- Monitor: Databricks Foundation Model API routing (`databricks-` prefix) is worth evaluating if the
  repo's research expands to workspace-level model governance.

## Sources

| Source | Content |
|---|---|
| [omnigent.ai][omnigent-home] | Architecture, features, sandbox, policy controls, supported agents, alpha status |
| [omnigent-ai/omnigent (GitHub)][omnigent-gh] | Stars, license, language, install methods, README feature list |
| [Omnigent models docs][omnigent-models] | Claude Code harness, model routing, Databricks prefix, mid-session swap |
| [Databricks blog: Introducing Omnigent][databricks-blog] | Meta-harness definition, Databricks + Neon authorship, launch date (June 2026), policy and sandbox details |

[omnigent-home]: https://omnigent.ai/
[omnigent-gh]: https://github.com/omnigent-ai/omnigent
[omnigent-models]: https://omnigent.ai/docs/build/models
[databricks-blog]: https://www.databricks.com/blog/introducing-omnigent-meta-harness-combine-control-and-share-your-agents
