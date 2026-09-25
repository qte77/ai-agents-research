---
title: Apache Maka (Incubating) — Local-First Agent Workspace
purpose: Assess Apache Maka's event-sourced, local-first agent runtime and its Apache Incubator status
source: https://github.com/apache/maka
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Trial

## What It Is

[Apache Maka (Incubating)][repo] is a local-first AI agent workspace — a
"high-performance agent workspace that keeps a complete record of everything
it did," with Desktop, TUI, and CLI clients sharing one "Runtime Host"
execution authority. Its defining architectural claim, per the README: "the
log is the runtime" — every model message, tool call, permission decision,
and termination is recorded as an append-only `RuntimeEvent`, and the UI, the
next prompt, and crash recovery are all *projections* of that log rather than
a separate source of truth, so stale tool output can leave the next prompt
without ever leaving the log. Session data, settings, and run records stay on
the user's machine by default; the user supplies their own model (a cloud
API, a local model, or a compatible gateway).

The project also ships a benchmarking mode: Maka is evaluated against other
agent harnesses on the same model with an official verifier, and per-task
results ship in [`docs/eval/`][eval] with every report — "measured, not
claimed" is the project's own framing.

## Incubation Status

Maka is an **Apache Incubator podling** ("(Incubating)" appears throughout
the README and project name), not a graduated top-level Apache project.
**No Apache-approved release exists yet** — the README states that when one
does, the signed source archive will be the official release, with
development builds as the current interim channel. Readers evaluating Maka
for production use should treat this as pre-release, ASF-governed but
not-yet-released software.

## Repo Stats (2026-09-24)

5,645 stars · 529 forks · 504 open issues+PRs combined · Apache License 2.0 ·
TypeScript · created 2026-05-27 · last push 2026-09-24 (same day as this
verification).

## Corpus Relevance

No directly comparable "local-first agent workspace with an event-sourced,
append-only runtime log" is tracked elsewhere in this corpus.
[agent-observability-methods-analysis.md](../protocols/agent-observability-methods-analysis.md)
covers a different layer — SaaS/OTel tracing add-ons for cloud-hosted
agents — rather than a local execution log that *is* the runtime record.

## Sources

| Source | Content |
|---|---|
| [apache/maka repo][repo] | README, incubation status, architecture claims (first-party) |
| GitHub API repo metadata, 2026-09-24 | Stars(5,645)/forks(529)/open issues(504), license, dates |

[repo]: https://github.com/apache/maka
[eval]: https://github.com/apache/maka/tree/main/docs/eval
