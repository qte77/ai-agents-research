---
title: Apache Maka (Incubating) — Local-First Agent Workspace
purpose: Assess Apache Maka's event-sourced, local-first agent runtime and its Apache Incubator status
source: https://github.com/apache/maka
created: 2026-09-24
updated: 2026-11-26
validated_links_on: 2026-09-24
status: trial
---

## What It Is

[Apache Maka (Incubating)][repo] is a local-first AI agent workspace — a
"high-performance agent workspace that keeps a complete record of everything
it did," with terminal and desktop shells running the same workbench UI against one "Runtime Host"
process (README, checked 2026-11-26). Its defining architectural claim, per the README as read
on 2026-09-24 (that wording is no longer in the README, checked 2026-11-26): "the
log is the runtime" — every model message, tool call, permission decision,
and termination is recorded as an append-only `RuntimeEvent`, and the UI, the
next prompt, and crash recovery are all *projections* of that log rather than
a separate source of truth, so stale tool output can leave the next prompt
without ever leaving the log. Session data, settings, and run records stay on
the user's machine by default; the user supplies their own model (a cloud
API, a local model, or a compatible gateway).

The project also ships an evaluation runner: [`products/eval/`][eval] is a containerized
Harbor evaluation runner against the native host (README, checked 2026-11-22). Our
2026-09-24 reading recorded per-task results against other agent harnesses under
`docs/eval/`; that folder is no longer in the repository (checked 2026-11-22).

## Incubation Status

Maka is an **Apache Incubator podling** ("(Incubating)" appears throughout
the README and project name), not a graduated top-level Apache project.
**The latest Apache-approved release is `0.2.2` (incubating)** — the
[downloads page][downloads] lists 0.2.2 as the latest release (2026-10-30) with a signed source archive, and states that the signed source archive is the release (checked 2026-11-26). Development builds remain the
other channel. Maka is still an incubating podling, not a top-level project, so readers evaluating
it for production use should weigh that status.

## Repo Stats (checked 2026-11-26)

6,010 stars · 582 forks · 405 open issues+PRs combined · Apache License 2.0 ·
Rust (the TypeScript part is the plugin SDK package) · created 2026-05-27 · last push 2026-11-26.
Earlier snapshot (2026-09-24): 5,645 stars, 529 forks, 504 open issues+PRs, labelled TypeScript.

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
| [Maka downloads page][downloads] | Latest approved release 0.2.2 (2026-10-30), signed source archive, incubation wording (checked 2026-11-26) |
| GitHub API repo metadata, 2026-11-26 | Stars(6,010)/forks(582)/open issues(405), language, license, dates |

[repo]: https://github.com/apache/maka
[eval]: https://github.com/apache/maka/tree/main/products/eval
[downloads]: https://maka.apache.org/en/downloads/
