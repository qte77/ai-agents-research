---
title: OrcaReplay Analysis
source: https://github.com/Continuum-AI-Corp/OrcaReplay
purpose: Analysis of OrcaReplay, a record/replay/fork debugger for coding-agent runs, as first-party evidence for reproducible and traceable long-running agent work.
created: 2026-09-30
updated: 2026-09-30
validated_links: 2026-09-30
status: assess
---

## What It Is

[OrcaReplay][repo] is "time travel for AI agents": record any coding-agent run, replay it
deterministically offline with no model called, then fork it from any step onto a different model
([README][repo]). Built by the team behind [OrcaRouter][orcarouter] (a multi-provider LLM API gateway),
under **Apache-2.0** for the code (LICENSE-badge-linked, `gh api` confirmed: 268 stars, 64 forks, pushed
2026-09-29, created 2026-08-29) with a separate **CC BY 4.0** trace-format specification
(`spec/orca-trace-v0.md`).

This is a direct, first-party answer to two of this arc's coverage gaps — Long-running · Traceable and
Long-running · Reproducible — that the existing cloud-session, scheduled-task and keepalive docs in
[long-running.md](../../_topics/long-running.md) leave open: none of them describe a deterministic
rebuild of a past run or an audit trail that ties an output back to the exact steps that produced it.
OrcaReplay's own comparison table names the gap directly: "Runs the agent again and gets the same
answer" — observability tools ❌, OrcaReplay "✅ from the recording, byte-for-byte."

## How It Works

A single npm package (`orcareplay`) installs one `orca` CLI command — nothing is installed into the
target agent itself, per the README:

- `orca record claude` — records an agent run (Claude Code, Codex, Agents SDK, AI SDK, or "any," per
  the README's own compatibility badge) via a proxy that sits on the model API call.
- `orca replay last` — replays the recorded run with **no network call and no tokens spent**, reading
  the saved trace instead of re-invoking the model.
- `orca replay last --from 4 --model claude-haiku-4-5` — forks the run at a chosen checkpoint and
  continues from there on a **different model**, holding the file state and conversation prefix fixed
  so the model is the only changed variable.
- `orca quickstart` — a self-contained demo: a project with a real bug and a pre-recorded fix, replayed
  against the project with zero model calls, to demonstrate the mechanism without needing a live key.
- A separate capture path (`capture/capture.mjs`) records the harness's own assembled system prompt
  (scrubbed of machine-identifying details) per model, since "interactive prompts and `-p` prompts are
  not the same prompt, and neither is the same across models" (README, verbatim).

The trace format itself is an open, versioned specification (`orca-trace-v0.md`, CC BY 4.0), separate
from the Apache-2.0 CLI/proxy code — a deliberate split between a portable data format and its current
implementation.

## Rubric

Scored 2026-09-30 against the [agent-substrate-rubric.md](../../sdlc-lcm/agent-substrate-rubric.md) (subject: long-running / harness debugging), evidence from the [README][repo]:

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no data (a single-user CLI tool recording local runs; no multi-user trace-sharing workflow documented) | no (traces are local files; "works after you close the terminal... it is a file" — the README's own framing is explicitly local, not a service) | yes ("Reproduce the run byte-for-byte with no model called," the README's own headline claim, demonstrated in the `quickstart` with before/after test counts) | yes (works with "Claude Code · Codex · Agents SDK · AI SDK · any," per the compatibility badge, via "two env vars" rather than an SDK wrapper) | yes (a trace is forkable from any checkpoint onto a different model — a branch-like operation over recorded state, and the trace format itself is a versioned open spec) | yes (captures the full loop past the model API — the README states it sees "which tool call deleted the file," not just aggregate cost/token counts that observability tools report) |

## Adoption Decision

**Assess.** The mechanism is genuinely novel in this corpus (no existing doc covers deterministic
agent-run replay), the license is a real Apache-2.0 with a separately-licensed open trace spec, and the
`quickstart` path lets the claim be checked without a live model key. It is young (six weeks old as of
this check) and single-vendor; the "byte-for-byte" reproducibility claim rests on OrcaReplay's own demo
rather than an independent third-party reproduction. Re-assess after broader adoption or an independent
write-up.

## Cross-References

- [long-running.md](../../_topics/long-running.md) — the hub this doc fills gaps 7 and 8 for.
- [harnessx-analysis.md](harnessx-analysis.md), [weco-aide-recursive-self-improvement-analysis.md](weco-aide-recursive-self-improvement-analysis.md) — other single-tool harness-research pages at the same granularity; unlike those (harness structures that evolve from traces), OrcaReplay's traces are for **human debugging and model comparison**, not automated harness evolution.

## Sources

| Source | Content |
|---|---|
| [Continuum-AI-Corp/OrcaReplay README][repo] | Product description, CLI commands, capture mechanism, comparison table vs. observability tools, licensing (Apache-2.0 code / CC BY 4.0 trace spec) |
| `gh api repos/Continuum-AI-Corp/OrcaReplay`, 2026-09-30 | License, stars (268), forks (64), created/pushed dates |

[repo]: https://github.com/Continuum-AI-Corp/OrcaReplay
[orcarouter]: https://www.orcarouter.ai
