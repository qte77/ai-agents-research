---
title: FrogNano Analysis
source: https://arxiv.org/abs/2609.07925
purpose: Analysis of FrogNano, a 4B coding agent trained exclusively via reinforcement learning on synthetically-generated software-engineering tasks.
created: 2026-09-24
updated: 2026-11-26
validated_links_on: 2026-09-24
status: assess
---

## What It Is

FrogNano ("Training a 4B Coding Agent via Online Task Synthesis," [arXiv:2609.07925][arxiv], submitted 2026-09-07) is a 4-billion-parameter coding agent post-trained **exclusively via reinforcement learning** — no distillation from a larger teacher model — on roughly 1,500 synthetic software-engineering (SWE) environments. Its central technique is an **online task-synthesis pipeline**: instead of drawing from a fixed static task set, it generates each new training task calibrated to the current checkpoint's "frontier of learnability." Per the abstract, the paper's evidence is that competitive small coding agents can be trained on synthetic tasks alone (no distillation), and that this learnability-frontier calibration is important to that result.

Authored by the **Froggy Team at Microsoft Research Montréal** (corresponding author Alessandro Sordoni, `froggy@microsoft.com`), with collaborators whose listed email domains indicate affiliation with Mila (Quebec AI Institute) and UC San Diego — per the arXiv HTML author block (accessed 2026-09-24).

## How It Works

- **Harness**: FrogNano is trained and evaluated inside **Leaf**, described in the paper as a lightweight coding-agent harness built for this project (confirmed in a benchmark-figure caption: "Qwen3.5-4B\* is calculated using Leaf harness. FrogNano numbers are averaged over three runs."). The same harness loop is used for both training and evaluation.
- **RL framework**: in its harness-design discussion, the paper cites the open-source [`slime`][slime] RL framework's `coding_agent_rl` example (specifically `github.com/THUDM/slime/tree/main/examples/coding_agent_rl`); the paper does not state that FrogNano's own training runs used `slime` directly.
- **Related, not reused**: the Froggy Team's earlier project [debug-gym][debug-gym] ([arXiv:2503.21557][debug-gym-arxiv]) — an interactive text-based debugging harness (`pdb`-style tool use) — is cited as related prior work, not the harness FrogNano trains in.

## What's Not Released

As of 2026-09-24 no FrogNano code, model weights, or public "Leaf" harness release was found on the arXiv page or the Froggy Team's project page ([microsoft.github.io/debug-gym][debug-gym]). That has changed (checked 2026-11-26): the project page links [FrogNano-4B][frognano-hf] (Apache-2.0, based on Qwen3.5-4B, model card dated 2026-09-22) and the [Leaf Harness repository][frognano-gh] ("Compact Coding Agent Harness", MIT, created 2026-08-25, pushed 2026-11-26). Whether training code is released is unverified. (Note: the lead URL `debug-gym.github.io` 404s — the live page is `microsoft.github.io/debug-gym`, a GitHub Pages site under the `microsoft` org rather than a dedicated `debug-gym` org.) This is a technical report describing a training methodology, not a product or open-source release announcement.

## Adoption Decision

**Assess, pending release.** The online-task-synthesis idea (calibrate task difficulty to the model's current learnability frontier, rather than a fixed curriculum) is a genuinely reusable training technique, and a 4B model competitive on SWE tasks would be attractive for resource-constrained deployment. As of 2026-09-24 there was nothing to adopt: no code, weights, or harness were public. That trigger has since fired (the weights are Apache-2.0 and the Leaf harness MIT, checked 2026-11-26), so this decision needs re-evaluation by the owner.

## Sources

| Source | Content |
|---|---|
| [arXiv:2609.07925][arxiv] (HTML) | Abstract, training methodology, author affiliations, Leaf-harness mentions (accessed 2026-09-24; the paper has since reached v5, 2026-10-05, and the caption quote above is unverified against it) |
| [FrogNano-4B model card][frognano-hf] · [Leaf Harness repo][frognano-gh] | Weights (Apache-2.0) and harness (MIT) (checked 2026-11-26) |
| [Froggy Team project page][debug-gym] | Confirms Microsoft Research Montréal affiliation and FrogNano description; as of 2026-11-26 links the technical report, FrogNano-4B on Hugging Face and the Leaf Harness repository (no code/weights link on 2026-09-24) |
| [`slime` RL framework][slime] | Cited in the paper's harness-design discussion |

[arxiv]: https://arxiv.org/abs/2609.07925
[debug-gym]: https://microsoft.github.io/debug-gym/
[debug-gym-arxiv]: https://arxiv.org/abs/2503.21557
[slime]: https://github.com/THUDM/slime
[frognano-hf]: https://huggingface.co/microsoft/FrogNano-4B-2609
[frognano-gh]: https://github.com/microsoft/FrogNano
