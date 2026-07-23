---
title: Probe-and-Refine Tuning of Repository Guidance for Coding Agents
purpose: Analysis of a tuning procedure that iteratively rewrites a repo's AGENTS.md/CLAUDE.md-style guidance file to improve coding-agent resolve rates.
source: https://arxiv.org/abs/2606.20512
created: 2026-07-23
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Assess

## What It Is

"Probe-and-Refine Tuning of Repository Guidance for Coding Agents" (arXiv [2606.20512][paper], Asa Shepard and Jeannie Albrecht, Williams College) introduces **probe-and-refine tuning** — a lightweight, agent-loop-free procedure for improving a repository's guidance file (the AGENTS.md/CLAUDE.md-class artifact that steers a coding agent). Rather than hand-tuning that file or building a static knowledge base, the method synthesizes bug-fix probes and uses single-shot LLM calls to diagnose where the current guidance fails an agent, then edits the guidance accordingly.

## Method

Each tuning iteration runs 4 single-shot LLM calls, with no multi-step agent loop or tool use during the tuning process itself:

1. Generate a synthetic bug-fix probe
2. Attempt a fix under the current guidance file
3. Diagnose the failure
4. Edit the guidance file

Average run: ~4.5 iterations per repo, ~22 single-shot calls per iteration, 10 probes per iteration at temperature 0.9. The resulting guidance artifacts average 2,754 characters (range 1,935–2,972) — i.e., comparable in scale to a hand-written CLAUDE.md, not a large knowledge base.

## Results

Benchmark: SWE-bench Verified, 500 instances across 12 repositories (Django alone is 231/500, 46% of the set); agent model Qwen3.5-35B-A3B (MoE, 3B active params), 200 agent steps per instance, 4 independent trials.

Headline (arXiv abstract, final numbers): probe-and-refine guidance reaches a **33.0%** mean resolve rate vs. **28.3%** for the static knowledge base it was initialized from vs. **25.5%** unguided baseline (p<0.001 for both probe-and-refine contrasts).

Mechanism: the gain traces to **coverage, not patch quality** — refined guidance yields evaluable patches for 14.5 percentage points more instances, while per-patch precision stays statistically flat at ~59% (p=0.119) across all three conditions. In other words, the tuned guidance mainly helps the agent locate the right files to change, not produce better patches once it's there.

Two robustness checks: a step-budget experiment shows guidance is what lets the agent spend a larger step budget productively; a cross-model check with NVIDIA-Nemotron-3-Nano-30B-A3B shows the tuning loop degrades when that model can't produce sufficiently diagnostic output — though per-patch precision remains constant even then.

### Code release caveat

The companion repo ([github.com/asashepard/probe-and-refine-tuning][repo], MIT license — verified from the actual LICENSE file text, not a badge) is a version-drifted snapshot vs. the arXiv abstract: its README reports single-run numbers (34.2%/27.4%/22.8% resolve rates, 41/9/18 unique solves) rather than the paper's 4-trial means, lists only Shepard as sole author, uses a slightly different title ("Iterative Probe-and-Refine Tuning..."), and still carries a placeholder arXiv badge (`XXXX.XXXXX`). It has no releases or tags — unversioned, single main branch, created 2026-03-04, last pushed 2026-03-27, 4 stargazers (checked 2026-07-23, will drift by the time this is read). Treat the arXiv abstract, not the repo README, as the citable result.

## Corpus Relevance

This sits in `cc-native/context-memory` because its subject — tuning a repository-level agent-guidance file in the exact AGENTS.md/CLAUDE.md convention this repo itself uses — is squarely the context-memory research interest. [CC-memory-system-analysis.md](CC-memory-system-analysis.md) covers CLAUDE.md instruction adherence from the CC-native side; this paper is the closest first-party research on *how to systematically tune* such a file's content, rather than just how CC loads and weights it.

Unverified/out of scope for this doc: the arXiv "Comments" field (page count, venue) is unpopulated — this appears to be preprint-only with no confirmed conference/journal venue; author institutional affiliation is taken from the arXiv HTML byline only; no DOI beyond the arXiv default (10.48550/arXiv.2606.20512) was found.

## Sources

| Source | Content |
|---|---|
| [arXiv 2606.20512][paper] | Abstract, method, and headline/robustness results (v2, 2026-06-19) |
| [Companion repo][repo] | MIT LICENSE file (verified by content); README version-drift caveat |

[paper]: https://arxiv.org/abs/2606.20512
[repo]: https://github.com/asashepard/probe-and-refine-tuning
