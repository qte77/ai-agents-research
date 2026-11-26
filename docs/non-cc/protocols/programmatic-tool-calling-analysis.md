---
title: Programmatic and Speculative Tool Calling
source: https://arxiv.org/abs/2608.06370
purpose: Evaluate the evidence for programmatic tool calling (PTC) over JSON tool calling, and speculative PTC (sPTC) as a technique for overlapping expensive tool/sub-LLM calls with code generation
created: 2026-09-24
updated: 2026-11-26
validated_links_on: 2026-11-18
status: assess
---

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
with the GPT-5.6 family showing a 10.6% improvement (per the abstract). The evaluation covers
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
generated code are often the dominant share of runtime. For training a model to fit an RLM harness, see [Prime Agent § Training the Model for an RLM Harness](../coding-agents/prime-agent-analysis.md#training-the-model-for-an-rlm-harness).

**Repository facts** (`gh api repos/alexzhang13/spec-ptc`, checked 2026-11-26): 233 stars, 15
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
  and **Pi-mono** (see [`pi-analysis.md`](../coding-agents/pi-analysis.md),
  [`opencode-analysis.md`](../coding-agents/opencode-analysis.md)), and links Claude's own
  [programmatic tool calling docs][claude-ptc-docs] as the underlying PTC pattern it speculates
  on top of.

Install: `pip install spec-ptc`.

Naming note: Claude Code's experimental **Code Mode** (v2.1.323, a session mode where Claude writes
JavaScript that makes several tool calls via a `REPL` tool) is a CLI feature, distinct from the API's
programmatic tool calling and from Cloudflare's Model Context Protocol (MCP) "Code Mode"; see
[CC-tools-inventory.md § Code Mode](../../cc-native/configuration/CC-tools-inventory.md#code-mode-v21323).

## Tool use across model kinds

Placement note: the corpus had no dedicated tool-use landscape, so this section extends the doc
that already covers BFCL v4. One section per sub-topic; scores carry dates.

### LLM function-calling benchmarks

| Benchmark | What it measures | Version / date | Source |
|---|---|---|---|
| BFCL (Berkeley Function Calling Leaderboard) | Single-call to agentic function calling; V4 is described as "holistic agentic evaluation" (V3 added multi-turn); format-sensitivity cases apply only to prompt-based (non-FC) models | V4; page last updated 2026-04-12 (read 2026-11-18); no scores quoted here because the leaderboard table was not readable in the fetch | [leaderboard][bfcl] |
| τ-bench | Tool-agent-user dialogues with domain policies (retail, airline); scores the final database state; introduces pass^k for reliability across repeated trials | arXiv 2406.12045, 2024-06-17. At submission "gpt-4o … succeed on <50% of the tasks" and "pass^8 <25% in retail" (2024 models, not current) | [τ-bench][taubench] |
| τ²-Bench | Adds a telecom domain where agent and user both act on shared state; the paper reports "significant performance drops when agents shift from no-user to dual-control" | arXiv 2506.07982, 2025-06-09 | [τ²-Bench][tau2] |

Self-reported leaderboard claims need care: the xLAM abstract ([arXiv 2409.03215][xlam], 2024-09-05)
claims first place on BFCL at that time, a snapshot that has since moved.

### Failure modes and tool-set size (preprints, all read on their arXiv pages 2026-11-18)

- **Schema bias.** [Liu et al., arXiv 2609.34971][schema-bias] (2026-09-28): the same executable
  action described by different but equivalent tool schemas changes outcomes; across eleven LLMs and
  up to 32 schema variants, "success rates range from complete failure to 97% depending solely on the
  schema", and training repairs a variant "only when that variant appears in the training data".
- **Interface drift and distractor tools.** [Chattopadhyay et al., arXiv 2610.23342][drift]
  (2026-10-16): after tool descriptions, schemas, or the candidate list change post-deployment,
  a training-free validate-and-repair layer lifted Qwen3.5-9B from 0.580 to 0.805 on BFCL-200 and
  from 0.717 to 0.813 on their DICE-300 set; their ablation attributes most damage to candidate-set
  drift, "especially distractor tools" (a direct tool-set-size effect). One 9B model, authors' own
  subsets, so this does not generalize to frontier models.
- **Stage-wise diagnosis.** [ToolRobustBench, arXiv 2608.23635][trb] (2026-08-23): 15,456 perturbed
  instances over 7 models; clean success is high but uneven, robustness drops, and
  tool-output (observation) perturbation is the dominant bottleneck. The abstract on the page
  appeared cut off mid-sentence, so only the quoted points are relied on.
- **Finding the tool in a large registry.** [Zhang et al., arXiv 2610.19068][tool-disc]
  (2026-10-13), on ToolBench: embedding the query and retrieving tools beats generating hypothetical
  signatures first on single-tool queries, and the reverse holds on multi-tool queries, at every
  retrieval budget k=1 to 20; the extra discovery call "roughly doubles inference cost".
  Cross-reference: Claude Code defers MCP tool definitions behind on-demand tool search
  ([how it works][cc-how]), the vendor-side answer to large tool sets; the corpus has not measured it.
- **Calling style.** The Bitter Lesson paper above (programmatic vs JSON) is the call-format axis.

### Action models and computer-use action spaces

- **Large action models** are models trained for function calling and agent tasks rather than chat.
  Salesforce's xLAM family ([arXiv 2409.03215][xlam], 2024-09-05) is the documented open example:
  five models, 1B to 8x22B parameters.
- **Computer-use action spaces** extend tool calling to GUI control, scored on OSWorld
  ([arXiv 2404.07972][osworld], submitted 2024-04-11): 369 tasks, humans above 72.36% against 12.24%
  for the best model at the time, with deficiencies mainly in GUI grounding. That figure is two
  years old and no longer a state-of-the-art claim. For current computer-use tools and
  scores see [computer-use-agents-landscape.md](../agents/computer-use-agents-landscape.md); for agents
  that gate steps with decision models see
  [system-1-decision-models-landscape.md § Tools built on Jev][s1-tools] for computer-use agents that
  gate steps with decision models and [microsoft-365-copilot-analysis.md][m365] for a vendor's
  computer-use feature.

### Decision models and VLMs as tools

- **Decision models** (typed one-pass classifiers) gate or route tool calls; see
  [system-1-decision-models-landscape.md § Tool-call gating][s1-gate] rather than a restatement here.
- **VLMs as tools** (screenshot or image interpretation called from an agent): see
  [CC-vlm-screen-sharing-landscape.md](../../cc-community/CC-vlm-screen-sharing-landscape.md).

### Grep and lexical search as an agent tool

Evidence lives in one place:
[CC-code-tooling-landscape.md § Grep vs. semantic search for coding agents][grep-home].

## Adoption Decision

**Assess.** The paper is independent, multi-model evidence — not a single vendor's benchmark —
for a concrete claim (PTC ≥ JSON tool calling in 11/14 models, more stable under context
degradation), which is useful corroboration for anyone deciding between tool-calling styles in a
harness. `spec-ptc` is a small (233-star as of 2026-11-26), very new (five weeks old as of 2026-09-24) reference
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
| `gh api repos/alexzhang13/spec-ptc` | Stars (233), forks (15), license (MIT), created (2026-08-21), checked 2026-11-26 |
| `gh api repos/alexzhang13/spec-ptc/releases/latest` | Latest tag `v0.1.1`, published 2026-08-24, accessed 2026-09-24 |
| BFCL leaderboard; τ-bench; τ²-Bench; xLAM; OSWorld | Benchmark versions, dates, and quoted abstract claims (read 2026-11-18) |
| arXiv 2609.34971, 2610.23342, 2608.23635, 2610.19068 | Schema bias, interface drift, stage-wise failure diagnosis, tool discovery at scale (abstract pages, 2026-11-18) |

[ptc-paper]: https://arxiv.org/abs/2608.06370
[sptc-gh]: https://github.com/alexzhang13/spec-ptc
[claude-ptc-docs]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling
[bfcl]: https://gorilla.cs.berkeley.edu/leaderboard.html
[taubench]: https://arxiv.org/abs/2406.12045
[tau2]: https://arxiv.org/abs/2506.07982
[xlam]: https://arxiv.org/abs/2409.03215
[osworld]: https://arxiv.org/abs/2404.07972
[schema-bias]: https://arxiv.org/abs/2609.34971
[drift]: https://arxiv.org/abs/2610.23342
[trb]: https://arxiv.org/abs/2608.23635
[tool-disc]: https://arxiv.org/abs/2610.19068
[cc-how]: https://code.claude.com/docs/en/how-claude-code-works
[s1-tools]: ../reference/system-1-decision-models-landscape.md#tools-built-on-jev
[s1-gate]: ../reference/system-1-decision-models-landscape.md#3-tool-call-gating
[m365]: ../agents/microsoft-365-copilot-analysis.md
[grep-home]: ../../cc-community/CC-code-tooling-landscape.md#grep-vs-semantic-search-for-coding-agents
