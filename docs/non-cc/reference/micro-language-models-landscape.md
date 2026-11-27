---
title: Micro and Small Language Models Landscape
purpose: "What micro and small language models are for in agent systems (instant on-device openers, edge inference, cheap narrow tasks), with each source at its own evidence level."
created: 2026-11-27
updated: 2026-11-27
validated_links_on: 2026-11-27
status: assess
---

## What It Is

Agent systems pay for a large model on every step, in both latency and cost. Three uses of much smaller models recur in
the sources below: an **instant opener** on the device while a cloud model finishes the reply, a **small fine-tuned model**
that handles one narrow, high-volume job cheaply, and a **minimal local runtime** that makes a small model runnable
anywhere. This doc keeps each source at its own evidence level (paper, vendor claim, code, commentary) and does not rank
them.

"Micro language model" is used here only in the sense of the arXiv paper below, which coins the term for 8M-30M
parameter generative models. The word is not standardised: the agency blog listed under
[Not included](#not-included) uses "micro model" for single-task classifiers instead.

For typed-output classifiers that route, gate or score in one forward pass, see
[system-1-decision-models-landscape.md](system-1-decision-models-landscape.md); for local embedders and vector stores, see
[on-device-semantic-search-landscape.md](../context-memory/on-device-semantic-search-landscape.md). Neither is repeated here.

## Instant openers: micro language models (paper)

**Evidence: peer-style paper plus the authors' repo.** The paper ([arXiv 2604.19642][paper], submitted 2026-04-21) argues that
smartwatches and smart glasses cannot run even 100M-1B parameter models continuously, while cloud inference adds
multi-second latency. Its answer is a collaborative split: an on-device model of 8M-30M parameters writes the first 4-8
words of the reply, and a cloud model continues from that prefix, so the user is reading while the cloud tokens arrive.

- **Model scale:** the HTML version trains decoder-only models of 8.8M-29.5M parameters from scratch on chat-style data and
  reports the 14-29M models as competitive with several 70M-256M baselines on its rubric-based short-dialogue evaluation
  (author-run, not independently reproduced).
- **Error recovery:** three correction styles (explicit, natural, humor-aware) handle the case where the local opener
  goes wrong. In a 15-participant user study, `μLM-28M` plus `Qwen3-235B-A22B` was rated equivalent to the standalone large
  model in 49% of cases, preferred in 28% and not preferred in 23% (read 2026-11-27, paper HTML). Fifteen participants is a
  small sample.
- **Code:** the abstract states the checkpoint and demo are available; the HTML links the repo
  [Sensente/micro-language-model-project][swen-repo] (MIT per its LICENSE file, 19 stars, read 2026-11-27), which names a
  28M checkpoint (`Swen-28M`) on Hugging Face and pairs it with `gpt-4o` in the demo. The repo's own description tags the
  paper as an EMNLP 2026 main-track paper; this doc did not check that against the conference.
- **Fit for agents:** the pattern is a latency mask, not a reasoning aid. It applies where a human waits on a spoken or
  glanced reply; it does not help headless tool loops.

## Narrow fine-tuned small model: SPREAD on Nemotron (vendor claim)

**Evidence: vendor announcement, unverified.** SPREAD's story (dated 2026-10-21, [spread.ai][spread]) says it post-trained an
NVIDIA Nemotron 3.5 Lightning 30B-A3B open model and compressed it to NVIDIA's 4-bit NVFP4 format, for engineering-ticket
analysis at a car maker. Treat every figure below as SPREAD's own, from a benchmark it ran and did not publish in that page
(read 2026-11-27):

- It says the model "outperforms frontier models on 9 of 10 tasks"; on ticket analysis 79% against 44% for the best
  frontier model, and 81% against 52% on dataset queries; the body text says 1,200 real-world engineering tasks and "9 of 10 measures", also against a 4x larger Nemotron model.
- A median answer in 0.36 seconds; fine-tuning on 5,061 examples; a 4.3-hour pipeline on NVIDIA H200 GPUs.
- One quote in the page is from NVIDIA's regional lead; the page does not name an independent evaluator.

Not "micro" by the paper's definition: 30B total parameters with a mixture-of-experts design (the "A3B" in the model name
indicates about 3B active; this doc did not check that against NVIDIA's model card). It belongs here as an example of the
"small, narrow, own-environment" claim, and as a claim to test on your own data before relying on it. For the do-it-yourself
route, see [Train your own: Unsloth][train-own] and [Serving without training][serve-local] in the System-1 doc.

## Minimal local runtime: llama2.c (code)

**Evidence: documented, widely used code.** [karpathy/llama2.c][llama2c] (MIT per its LICENSE file; about 20.3k stars, last
pushed 2024-08-06, read 2026-11-27) trains the Llama 2 architecture in PyTorch and runs inference from one C file of roughly
700 lines (`run.c`). Its README says very small models can do useful work when the domain is narrow, and shows a 15M
parameter model trained on TinyStories running at about 110 tokens/s on the author's M1 MacBook Air (author's measurement,
read 2026-11-27). It is a teaching and tiny-model reference, not a production server.

A [gist by cedrickchee][gist] ("The rise of micro-LLMs", last active 2026-03-06 per the page, read 2026-11-27) comments on
the project. It is secondary commentary; facts above come from the repo.

## Edge inference extreme: a bare-metal assembly OS (experiment)

**Evidence: one-day-old personal experiment.** [mitkox/qwen38-27b-baremetal-os][baremetal] (MIT per its LICENSE file; 18 stars;
created 2026-11-26, read 2026-11-27) extends the third-party `alesha-pro/llm.asm` project. Its README describes a 33 KB
bootable x86-64 assembly kernel that chats with a 27B Qwen model, reading 28.6 GB Q8_0 weights through a shared-memory PCI
device (ivshmem) on KVM, and reports 3.6 tokens/s on 16 virtual CPUs (the author's measurement; not reproduced here).

A 27B model is not micro or small; it is an inference-engineering curiosity. The relevant small-model part is earlier in the
same README: a `Qwen3-0.6B` variant of the same bare-metal OS, which the author reports at about 135 tokens/s on a KVM EPYC
host against a self-run `llama.cpp` comparison (author's benchmark). No claim is made here about production use.

## Not included

| Source | Reason |
|---|---|
| [Trigma, "Micro Models in NLP"][trigma] | Agency blog, no primary data of its own; it defines "micro model" as a single-task classifier, which differs from the paper's usage. Its one citable fact (DistilBERT size and retention) should be cited from the DistilBERT paper, not this page. |

## Sources

| Source | Content |
|---|---|
| [arXiv 2604.19642][paper] | μLM definition, 8M-30M scale, collaborative generation, user study (abstract and HTML read 2026-11-27) |
| [Sensente/micro-language-model-project][swen-repo] | Paper authors' repo: licence, checkpoint link, demo (read 2026-11-27) |
| [SPREAD Nemotron story][spread] | Vendor claim: results, training pipeline, latency |
| [karpathy/llama2.c][llama2c] | README, LICENSE, stars, push date |
| [cedrickchee gist][gist] | Commentary only |
| [mitkox/qwen38-27b-baremetal-os][baremetal] | README, LICENSE, creation date |
| Trigma "Micro Models in NLP" (`https://trigma.com/artificial-intelligence/micro-models-in-nlp/`) | Excluded, see above; plain text because not linked |

[paper]: https://arxiv.org/abs/2604.19642
[swen-repo]: https://github.com/Sensente/micro-language-model-project
[spread]: https://www.spread.ai/resources/stories/spread-nvidia-nemotron-engineering-model
[llama2c]: https://github.com/karpathy/llama2.c
[gist]: https://gist.github.com/cedrickchee/462e8661d9c231deb90513849778e8fc
[baremetal]: https://github.com/mitkox/qwen38-27b-baremetal-os
[trigma]: https://trigma.com/artificial-intelligence/micro-models-in-nlp/
[train-own]: system-1-decision-models-landscape.md#train-your-own-unsloth-decision-model-training
[serve-local]: system-1-decision-models-landscape.md#serving-without-training-hugging-face-transformers-serve-and-ollama
