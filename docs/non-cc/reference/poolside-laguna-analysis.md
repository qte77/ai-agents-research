---
title: Poolside Laguna S 2.1 — Long-Horizon Agentic Coding Model
source: https://poolside.ai/blog/introducing-laguna-s-2-1
purpose: Evaluate Poolside's Laguna S 2.1 as a frontier agentic-coding model for long-horizon autonomous coding tasks
created: 2026-09-24
updated: 2026-11-26
validated_links_on: 2026-09-24
status: assess
---

## What It Is

[Laguna S 2.1][poolside-blog] is [Poolside's][poolside-home] frontier agentic-coding model: a
118B-parameter Mixture-of-Experts model with 8B activated parameters per token and a 1M-token
context window, purpose-built for long-horizon autonomous coding work. Per the launch blog post
(accessed 2026-09-24), it went from training start to launch in under nine weeks and was released
2026-07-21. Poolside also offers a lighter sibling, **Laguna XS 2.1** (33B total / 3B active
parameters, 256K context), described on the [company homepage][poolside-home] as "our lightest and
fastest agentic coding model," designed to run on-device.

Poolside describes itself as a company building "open-weight foundation models" for software
(accessed 2026-09-24). **License note:** the homepage uses the term "open-weight" without naming a license, but the
launch blog post (checked 2026-11-26) says Laguna S 2.1 is on Hugging Face under OpenMDW-1.1; the
Hugging Face org page says the same. The homepage and the Laguna XS 2.1 entry name no license (as of 2026-09-24).

## Capabilities and Benchmarks

All figures below are **vendor-reported** in Poolside's own launch blog post; no independent
verification was found.

- **Terminal-Bench 2.1:** 70.2% with "max thinking" mode enabled.
- **SWE-Bench Multilingual:** 78.5%.
- **SWE-Bench Pro:** 59.4%.
- **DeepSWE v1.1:** 40.4% with thinking enabled, vs. 16.5% without — the blog post's largest
  cited thinking-mode delta.
- **SWE Atlas:** 46.2%.

The blog post also describes qualitative "resourcefulness" demonstrations: building a functional
browser engine from scratch, optimizing Poolside's own agent harness (reporting a 5.2% speedup and
about 70% lower memory allocation; the chart shows 71.1%), and independently re-deriving a solution approach to Erdős problem #397 in
Perl. These are self-reported case studies, not benchmarked claims, and are noted here as such.

**"Max thinking" mode** (the post: it lifts Terminal-Bench 2.1 from 60.4% to 70.2%) automatically sizes the reasoning budget per problem rather than using a
fixed budget (the automatic sizing is unverified).

## Availability

Per the launch blog post and homepage (accessed 2026-09-24): available via Hugging Face,
OpenRouter, and Vercel AI Gateway; local inference is supported via vLLM, SGLang, and Ollama;
third-party agent-framework integrations are listed for Cline, Hermes Agent, and Kilo (the blog also lists OpenCode, OpenClaw, pi and Poolside's own pool agent, and Baseten hosting). A free web
chat is available at `chat.poolside.ai` (linked from the launch blog post). No first-party mention of Claude Code integration was
found as of 2026-09-24.

## Adoption Decision

**Assess.** The benchmark numbers (where comparable to other models tracked in this corpus, e.g.
via [`devin-cli-analysis.md`](../coding-agents/devin-cli-analysis.md) or
[`research-agents-landscape.md`](../knowledge-management/research-agents-landscape.md)) are competitive, and the
sub-nine-week train-to-launch cycle and 1M-token context are notable. However: all performance
claims are vendor-reported with no independent benchmark run found, the license for S 2.1 is stated as OpenMDW-1.1 (not an OSI license name we have reviewed; terms unread), and the only first-party pricing is the launch blog's OpenRouter endpoints (free at 256K context; paid at 1M context, $0.10 input, $0.20 output, $0.01 cache-read per 1M tokens, checked 2026-11-26). **Assess**, pending a read of the license terms and independent benchmark
corroboration.

## Action Items

- Read the OpenMDW-1.1 license terms (Hugging Face model card) before treating "open-weight" as
  equivalent to a specific OSI license.
- Watch for independent (non-Poolside) benchmark runs of Laguna S 2.1 on Terminal-Bench / SWE-Bench
  variants.
- Check whether Cline, Hermes Agent, or Kilo (already tracked partially elsewhere in this corpus)
  publish their own first-party confirmation of the Laguna integration.

## Sources

| Source | Content |
|---|---|
| [Poolside — Introducing Laguna S 2.1][poolside-blog] | Model specs (118B/8B-active MoE, 1M context), benchmark table, release date (2026-07-21), availability, qualitative demos |
| [poolside.ai][poolside-home] | Company description, Laguna XS 2.1 sibling model, "open-weight" terminology, availability channels |

[poolside-blog]: https://poolside.ai/blog/introducing-laguna-s-2-1
[poolside-home]: https://poolside.ai
