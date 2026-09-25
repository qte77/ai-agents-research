---
title: Programmatic and Speculative Tool Calling
source: https://arxiv.org/abs/2608.06370
purpose: Evaluate the evidence for programmatic tool calling (PTC) over JSON tool calling, and speculative PTC (sPTC) as a technique for overlapping expensive tool/sub-LLM calls with code generation
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

Two related first-party sources on **programmatic tool calling** — exposing tools as typed
function stubs a model calls from generated code, rather than as JSON objects matched against a
schema per turn:

1. **["The Bitter Lesson of Tool Calling"][ptc-paper]** (Patel, Sen, Lumer, Subbiah; submitted
   2026-08-06) — a systematic evaluation of programmatic tool calling (PTC) against native JSON
   tool calling across 14 language models on the BFCL v4 benchmark, under conditions including
   parallel execution and context degradation.
2. **[`alexzhang13/spec-ptc`][sptc-gh]** — a reference implementation of **speculative
   programmatic tool calling (sPTC)**, a technique that speculatively launches tool and sub-LLM
   calls *while* the root model is still streaming the code block that will eventually call them,
   so expensive calls overlap with token generation instead of following it serially.

## The Bitter Lesson of Tool Calling (paper)

Per the [arXiv abstract page][ptc-paper] (accessed 2026-09-24): the paper's headline finding is
that "programmatic tool calling matches or exceeds native JSON tool calling in 11 of 14 models,"
with one model (GPT-5.6, per the abstract) showing a 10.6% improvement. The evaluation covers
BFCL v4 under real-world conditions — parallel tool execution and context-degradation scenarios —
and reports that PTC remains stable where standard JSON tool calling shows measurable performance
decline as context degrades. The paper frames typed Python function stubs as enabling natural
chaining and parallelization that JSON schemas do not.

This finding is directly relevant to Claude's own first-party
[programmatic tool calling feature][claude-ptc-docs] (linked from the `spec-ptc` README, see
below) — this doc does not evaluate that CC-side feature itself, only the independent research
result about the PTC-vs-JSON approach in general.

## Speculative Programmatic Tool Calling (`spec-ptc`)

`spec-ptc`'s own README states the technique plainly: "sPTC is the general technique of
speculating tool and sub-LLM calls that will happen as the root LLM is generating the codeblock,
allowing the [caller] to batch and asynchronously compute these expensive calls while the full
codeblock is still being generated" (accessed 2026-09-24). It positions itself against harness
designs like **Recursive Language Models (RLMs)** and **CodeAct**, where sub-LLM calls embedded in
generated code are often the dominant share of runtime.

**Repository facts** (`gh api repos/alexzhang13/spec-ptc`, accessed 2026-09-24): 214 stars, 17
forks, **MIT** license, created 2026-08-21, latest tagged release `v0.1.1` (published 2026-08-24).

**Mechanism** (per the README):

- A `Speculator` object tracks tools decorated with `@spec.tool(speculatable=True, pure=True)`.
- A **shadow REPL** snapshots local variables into a discarded fork and launches speculative calls
  as closed statements complete while tokens are still streaming in.
- When the real code executes, a speculated call that already resolved returns immediately (a
  "hit"); an unresolved one runs normally (a "miss").
- A standalone `spec-ptc-daemon` runs the same shadow-and-store logic out of process over a
  Unix socket, for harnesses that cannot embed the library directly.
- The repo ships reference wrappers for **Claude Code** (as a `PreToolUse` hook), **OpenCode**,
  and **Pi-mono** (see [`pi-analysis.md`](../pi-analysis.md),
  [`opencode-analysis.md`](../opencode-analysis.md)), and links Claude's own
  [programmatic tool calling docs][claude-ptc-docs] as the underlying PTC pattern it speculates
  on top of.

Install: `pip install spec-ptc`.

## Adoption Decision

**Assess.** The paper is independent, multi-model evidence — not a single vendor's benchmark —
for a concrete claim (PTC ≥ JSON tool calling in 11/14 models, more stable under context
degradation), which is useful corroboration for anyone deciding between tool-calling styles in a
harness. `spec-ptc` is a small (214-star), very new (five weeks old as of 2026-09-24) reference
implementation rather than a production-hardened library, but its direct wrapper for Claude Code
and its explicit link to Claude's own programmatic-tool-calling docs make it a concrete,
inspectable example of the sPTC pattern against a harness already tracked in this corpus.

## Action Items

- If Claude's own [programmatic tool calling][claude-ptc-docs] feature gets a dedicated `cc-native`
  doc, cross-link it from here (and vice versa) rather than duplicating its description.
- Watch `spec-ptc` for adoption signals beyond its own reference wrappers (e.g. an upstream harness
  vendoring the daemon).
- No further action on the paper itself; its BFCL v4 methodology is externally reviewable via
  arXiv.

## Sources

| Source | Content |
|---|---|
| [arXiv:2608.06370 — "The Bitter Lesson of Tool Calling"][ptc-paper] | Title, authors, abstract, submission date (2026-08-06), headline finding (PTC ≥ JSON in 11/14 models) |
| [alexzhang13/spec-ptc README][sptc-gh] | sPTC technique description, mechanism (Speculator/shadow REPL/daemon), harness wrappers, install instructions |
| `gh api repos/alexzhang13/spec-ptc` | Stars (214), forks (17), license (MIT), created (2026-08-21), accessed 2026-09-24 |
| `gh api repos/alexzhang13/spec-ptc/releases/latest` | Latest tag `v0.1.1`, published 2026-08-24, accessed 2026-09-24 |

[ptc-paper]: https://arxiv.org/abs/2608.06370
[sptc-gh]: https://github.com/alexzhang13/spec-ptc
[claude-ptc-docs]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling
