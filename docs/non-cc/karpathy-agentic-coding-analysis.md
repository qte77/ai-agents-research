---
title: "Karpathy on Agentic Coding — Vibe Coding to Agentic Engineering"
source: https://karpathy.bearblog.dev/
purpose: Primary-source map of Andrej Karpathy's agentic-coding arc (2023 LLM OS → 2025 Software 3.0 / vibe coding → 2026 agentic engineering) and its relevance to agentic-SDLC and harness design.
category: analysis
created: 2026-07-08
updated: 2026-07-08
validated_links: 2026-07-08
---

**Status**: Research (informational)

A curated map of Andrej Karpathy's **agentic-coding** thinking as it evolved 2023→2026 — distinct from
his LLM-wiki/knowledge-base artifact already covered in
[karpathy-llm-kb-analysis.md](karpathy-llm-kb-analysis.md). The through-line: the programmer as an
**orchestrator of fallible agents** on a controllable **autonomy dial**, not a code author. It grounds
the discipline framing in [../sdlc-lcm/agentic-engineering-disciplines-landscape.md](../sdlc-lcm/agentic-engineering-disciplines-landscape.md).

> **Sourcing note:** the blog posts ([bearblog][menugen]) and the talks (YouTube / YC Library) are
> first-party. The essay-tweets (vibe-coding coinage, LLM OS) are cited **by date**; x.com returns
> HTTP 402 to automated fetches, so their wording is corroborated via secondary write-ups, not a
> first-party fetch — flagged rather than asserted.

## The arc

- **LLM OS** (essay-tweet, 2023-09-28; developed in the *"Intro to Large Language Models"* talk,
  [YouTube][llm-intro], 2023-11): the LLM as an **OS kernel** orchestrating tools, memory
  (context window as RAM), and multimodal I/O — the conceptual seed of agent-as-orchestrator.
- **"Vibe coding"** (essay-tweet, 2025-02-02): coins the term — "giving in to the vibes," describing
  intent and running LLM-generated code without close review. The low-rigor end of the spectrum he
  later contrasts with agentic engineering.
- **"Vibe Coding MenuGen"** ([bearblog][menugen], 2025-04-27): field report — prototyping is fast, but
  the grind moves to browser-only SaaS dashboards (Vercel/Clerk/Stripe) "not accessible or manipulable
  by an LLM." Seeds the **"build for agents too"** (CLI/curl/markdown, not just GUIs) argument.
- **"Software Is Changing (Again)" / Software 3.0** (YC AI Startup School talk, 2025-06-17 —
  [YouTube][sw3-talk], [YC Library][sw3-yc]): the core talk. LLMs as a new computer programmed in
  English; the **autonomy slider** (tab-complete → select-edit → full-file → agent-mode, from his
  Tesla Autopilot experience); **"Iron Man suit, not Iron Man robot"** (augmentation with a dial, not
  full autonomy); keep the generation→verification loop with **"AI on a tight leash"**; *"demo is
  `works.any()`, product is `works.all()`"*; and redesign software/infra for **three audiences —
  humans, computers, and agents** (llms.txt, machine-readable docs). "The decade of agents."
- **"2025 LLM Year in Review"** ([bearblog][year-review], 2025-12-19): names **Claude Code** "the first
  convincing demonstration of what an LLM Agent looks like" — chained tool-use + reasoning running
  **locally** with the user's own environment/credentials (not a cloud sandbox).
- **"Sequoia Ascent 2026"** ([bearblog][sequoia], 2026-04-30): his sharpest statement — **vibe coding
  "raises the floor"** (no quality bar, ships slop) vs **agentic engineering "raises the ceiling"** (a
  professional discipline: spec design, plan supervision, diff review, permission/worktree management,
  eval-loop construction). *"You can outsource your thinking, but you can't outsource your
  understanding."*

## Why it matters

- **The autonomy slider + "keep AI on a leash"** is the conceptual backbone of this repo's harness and
  permission-model analyses (agent-mode gating, worktree isolation, approval loops) —
  [../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md](../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md).
- **"Build for agents too"** anticipates the `llms.txt` / `AGENTS.md` / machine-readable-docs thread
  (and OpenWiki-style agent-context tooling) cataloged elsewhere in the corpus.
- **"Agentic engineering as a discipline"** is the same thesis the estate's SDLC docs operationalize —
  spec-driven, eval-looped, review-gated agent work.
- CC-as-first-convincing-agent is a notable outside validation of this corpus's CC focus.

Cross-ref: [../sdlc-lcm/agentic-engineering-disciplines-landscape.md](../sdlc-lcm/agentic-engineering-disciplines-landscape.md) ·
[karpathy-llm-kb-analysis.md](karpathy-llm-kb-analysis.md)

## Sources

| Source | Content |
|---|---|
| [Vibe Coding MenuGen][menugen] | Field report; infra-not-model bottleneck; "build for agents" |
| [2025 LLM Year in Review][year-review] | Claude Code as the first convincing LLM agent |
| [Sequoia Ascent 2026][sequoia] | Vibe coding (floor) vs agentic engineering (ceiling) |
| [Software Is Changing (Again)][sw3-talk] · [YC Library][sw3-yc] | Software 3.0, autonomy slider, decade of agents |
| [Intro to Large Language Models][llm-intro] | LLM OS (agent-as-kernel) precursor |
| Karpathy essay-tweets (2025-02-02 vibe coding; 2023-09-28 LLM OS) | Term coinage — dated, x.com fetch blocked (secondary-corroborated) |

[menugen]: https://karpathy.bearblog.dev/vibe-coding-menugen/
[year-review]: https://karpathy.bearblog.dev/year-in-review-2025/
[sequoia]: https://karpathy.bearblog.dev/sequoia-ascent-2026/
[sw3-talk]: https://www.youtube.com/watch?v=LCEmiRjPEtQ
[sw3-yc]: https://www.ycombinator.com/library/MW-andrej-karpathy-software-is-changing-again
[llm-intro]: https://www.youtube.com/watch?v=zjkBMFhNj_g
