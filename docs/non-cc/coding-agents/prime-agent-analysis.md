---
title: Prime Agent Analysis
source: https://github.com/PrimeIntellect-ai/prime-agent
purpose: Analysis of Prime Agent, Prime Intellect's open-source self-improving coding harness built on the Recursive Language Model (RLM) abstraction, for long-horizon coding and autonomous-task workflows.
created: 2026-09-24
updated: 2026-11-26
validated_links_on: 2026-09-24
status: assess
---

## What It Is

Prime Agent is Prime Intellect's open-source, self-improving coding-agent harness for long-horizon coding and autonomous-task workflows ([repo][repo]). The accompanying paper describes it as "an open-source harness for long-horizon evaluation and coding-agent workflows" ([arXiv:2608.23552][paper]).

- **License**: MIT
- **Stars**: 22,931 (checked 2026-11-26)
- **Language**: Rust (primary, about 26.2 MB; Python about 2.9 MB; checked 2026-11-26), with a persistent Python REPL as the model's control environment

## Architecture

Two abstractions anchor the design ([repo][repo], [paper][paper]):

- **Recursive Language Model (RLM)** — the model's context is treated as variables and its tools as function calls inside a persistent REPL (the harness itself is primarily Rust, with a Python REPL as the control environment; the RLM abstraction is language-agnostic), rather than a flat prompt-and-response loop.
- **Continual Harness** — supplemental prompts, histories, memories, and skills persist as durable state across task trajectories instead of resetting each session, while the base system prompt stays immutable.

Supporting mechanisms documented in the repo:

- **Subagent spawning** (`rlm.spawn()`) for parallel or background sub-tasks, with direct agent-to-agent communication between running processes.
- **Refinement** (`/refine`) applies evidence-backed updates to harness state rather than ad hoc prompt edits.
- **Daemon-backed background sessions** with reattachment, plus an "Agents View" for human inspection.
- **Autonomous mode** with configurable turn, token, and time budgets.
- **Executable skills** distributed as importable Python packages.

Worker and kernel processes isolate session lifecycle, but the repo explicitly states this is **not a security sandbox** — sessions run with user-level permissions, so running the harness requires trusted code sources.

## Reported Results

Per the paper ([arXiv:2608.23552][paper], authors Seth Karten, Alex L. Zhang, Kevin Thomas and 8 others, submitted 2026-08):

- ARC-AGI-3 RHAE Best@1 raised from 30% to 95.5% (the paper's abstract reports the number but does not isolate which harness feature drives it).
- Strong results reported on long-context coding and GPU-kernel-generation tasks.
- On Factorio specifically: "refinement allows for continuous technology progression and dedicated subagents enable parallelized work."

## Training the Model for an RLM Harness

A separate paper trains the model to fit an RLM-style harness rather than building the harness ([arXiv:2611.28298][rlm-cg], Zhang, Chakraborty and Khattab, v1 2026-11-20; authors' own results, not independently reproduced). Its **surrogate harness training** builds easier synthetic environments that reproduce what one model call would see inside the harness on the real task, with fake tools or sub-calls, and trains the model on rollouts from them. The released model, RLM-27B, is Qwen3.8-27B after full-parameter supervised fine-tuning (SFT) on those synthetic rollouts, not reinforcement learning (RL); the paper also reports RL on the synthetic tasks as a comparison.

- **Average score over eight long-context benchmarks (Table 4, [HTML][rlm-cg-html], read 2026-11-24):** RLM-27B 58.5 vs 46.1 for the untrained RLM harness on the same base model (+12.4 points, about +27% relative). The comparison rows with RL instead of SFT score 52.9 (RL on the synthetic tasks) and 48.5 (RL on short tasks).
- **Chained tasks (Table 6):** full-chain solve rate 55.2% for RLM-27B vs 19.3% for Qwen3.8-27B in the same harness; 77.5% for RLM-27B with additional recursion SFT data (depth 3).
- **Cost:** the paper states about 2x fewer inference tokens in the abstract and, for root trajectories in section 4.2, 3x fewer turns and 6x fewer input tokens.
- **Artifacts:** code [`alexzhang13/harness-cg`][rlm-cg-repo] (MIT per its LICENSE file; 24 stars, `gh api` 2026-11-26) and a synthetic SFT [dataset][rlm-cg-data].

For the RLM and CodeAct framing of sub-LLM calls, see [programmatic-tool-calling-analysis.md](../protocols/programmatic-tool-calling-analysis.md#speculative-programmatic-tool-calling-spec-ptc).

## Sources

| Source | Content |
|---|---|
| [PrimeIntellect-ai/prime-agent][repo] | Repo README — architecture, features, license, star count |
| [arXiv:2608.23552][paper] | Paper "Prime Agent: A Self-Improving RLM Harness" — authors, benchmark results |
| [arXiv:2611.28298][rlm-cg] ([HTML][rlm-cg-html]) | Surrogate harness training paper — method, Tables 4 and 6, token and turn savings |
| [alexzhang13/harness-cg][rlm-cg-repo] | LICENSE file (MIT), stars (`gh api` 2026-11-24) |
| [synthetic-rlm-sft-data][rlm-cg-data] | Dataset link as given in the paper (listing not opened) |

[repo]: https://github.com/PrimeIntellect-ai/prime-agent
[paper]: https://arxiv.org/abs/2608.23552
[rlm-cg]: https://arxiv.org/abs/2611.28298
[rlm-cg-html]: https://arxiv.org/html/2611.28298
[rlm-cg-repo]: https://github.com/alexzhang13/harness-cg
[rlm-cg-data]: https://huggingface.co/datasets/a1zhang/synthetic-rlm-sft-data
