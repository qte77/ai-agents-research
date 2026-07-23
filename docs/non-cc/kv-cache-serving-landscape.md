---
title: KV-Cache Serving Landscape — Vendor Prompt Caching & Inference Internals
purpose: Survey of KV (key-value) cache mechanisms in LLM serving — vendor prompt-caching APIs (Anthropic/OpenAI/Gemini) and open serving-stack internals (paging, prefix reuse, quantization, eviction, architectural sharing, offload/disaggregation).
category: landscape
created: 2026-07-08
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Reference (informational catalog)

How the **KV cache** — the per-token key/value tensors that make autoregressive decoding tractable —
is managed, reused, compressed, and offloaded across LLM serving. Two layers: (1) the **vendor
prompt-caching APIs** a Claude Code / agent consumer bills against, and (2) the **serving-engine
internals** underneath them.

This complements [../cc-native/context-memory/CC-prompt-caching-behavior.md](../cc-native/context-memory/CC-prompt-caching-behavior.md),
which covers Anthropic prompt caching from the **CC client / session-economics** angle only (what CC
sends, hit-rate, cost). This doc adds the **cross-vendor comparison** and the **serving mechanism**
that doc doesn't. See also the KV-cache-invalidation gotcha for self-hosted backends in
[../cc-native/configuration/CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md)
(`CLAUDE_CODE_ATTRIBUTION_HEADER=0`).

## 1. Vendor prompt-caching APIs (KV reuse as a billing/latency feature)

All three expose **cross-request KV reuse** (skip prefill on a shared prefix) as an API feature. Exact
prefix match only — no semantic/fuzzy matching. Cache **read** is ~90% cheaper than base input.

| Vendor | Mechanism | Min prefix | TTL | Read / write pricing |
|---|---|---|---|---|
| **Anthropic** | Explicit `cache_control` breakpoints (auto or ≤4 manual); cumulative-hash prefix | 1,024 (Opus 4.8, Sonnet 5/4.6/4.5); 4,096 (Opus 4.6/4.5, Haiku 4.5); 2,048 (Opus 4.7); 512 (Fable 5/Mythos 5) | 5-min default (free refresh) / 1-hour opt-in | read 0.1×; write 1.25× (5m) / 2× (1h) |
| **OpenAI** | Automatic prefix caching (no flag); hash of ~first 256 tokens; optional `prompt_cache_key` for routing affinity | 1,024 (then 128-tok increments) | 5–60 min inactivity, up to 1 h; extended tier to 24 h | read 0.1× (90% off) |
| **Google Gemini** | Implicit (on by default, 2.5+) + explicit `CachedContent` resource (generateContent API) | 2,048 (2.5 Flash/Pro); 4,096 (3.x preview) | implicit auto; explicit default 1 h, configurable | cached-token rate (~0.1×) **plus** a per-hour storage rate |

Anthropic's per-model minimums verified against the [prompt-caching docs][anthropic-caching]
(2026-07-08); Bedrock differs (Fable 5 / Mythos 5 = 1,024 there). CC itself uses the 5-min tier
exclusively — see [CC-prompt-caching-behavior.md](../cc-native/context-memory/CC-prompt-caching-behavior.md).

## 2. Serving-engine internals

### Memory management / paging

- **PagedAttention** ([arXiv 2309.06180][paged] · [vLLM][vllm]) — KV cache as OS-style paged virtual
  memory: non-contiguous blocks, near-zero fragmentation, cross-sequence sharing. **Shipped** — the de
  facto standard, echoed by TensorRT-LLM / SGLang / TGI.
- **vAttention** ([arXiv 2405.04437][vattention], Microsoft) — CUDA virtual-memory demand paging to
  keep KV contiguous without block indirection. Research/early.

### Cross-request reuse (prefix caching)

- **vLLM Automatic Prefix Caching** ([docs][vllm-apc]) — content-hashed KV blocks; only complete
  blocks reused; LRU eviction. **Shipped**, default-on recently.
- **SGLang RadixAttention** ([arXiv 2312.07104][sglang] · [docs][radix]) — a radix tree over all KV,
  automatic longest-prefix match across branching/forking (agents, tree search); LRU/LFU/… eviction;
  **HiCache** tiers it GPU→CPU→disk. **Shipped**. More flexible than vLLM's fixed block granularity.

### Quantization

- **FP8 KV cache** ([vLLM][vllm-fp8] · [TensorRT-LLM][trtllm-quant]) — 8-bit K/V, hardware-native on
  Hopper/Ada+. **Shipped** production knob. NVFP4 KV emerging on Blackwell.
- **KIVI** ([arXiv 2402.02750][kivi]), **KVQuant** ([arXiv 2401.18079][kvquant]) — tuning-free 2-bit /
  outlier-aware low-bit for long context. **Research** (not mainline defaults).
- **UltraQuant / Ultra-TurboQuant** ([arXiv 2606.20474][ultraquant], AMD) — 4-bit K/V for context-heavy
  agentic serving; Ultra-TQ = optimized rotation+codebook (TurboQuant-derived), UltraQuant = hardware-
  native FP4 via AMD CDNA4 scaled-MFMA. Vs. vLLM's FP8 KV baseline on AMD MI355X: P50 TTFT 3.47x faster
  in cache-pressured late rounds (2.3x averaged), 1.63x output throughput — though FP8 stays ahead
  (0.86x) in early "warm" rounds, so the gain is concentrated in the long-context/high-concurrency
  regime. **Research** prototype; no public code repo found as of 2026-07-23.

### Eviction / sparsity (mostly research)

- **H2O** ([2306.14048][h2o]) heavy-hitter eviction · **StreamingLLM / attention sinks**
  ([2309.17453][streamingllm]) — the sinks idea influenced production sliding-window configs ·
  **SnapKV** ([2404.14469][snapkv]) prompt-side compression · **Scissorhands** ([2305.17118][scissorhands]).
  No major stack ships eviction-based compression as a default path as of mid-2026.

### Architectural (small-by-construction)

- **MQA** ([1911.02150][mqa]) and **GQA** ([2305.13245][gqa]) — shared K/V heads; GQA is the default
  for most open frontier models (Llama, Mistral, Gemma). **MLA** (Multi-head Latent Attention,
  [DeepSeek-V2][mla]) — low-rank latent KV, savings beyond GQA at MHA quality; **shipped** in
  DeepSeek models + increasingly in vLLM/SGLang kernels. **CLA** ([2405.12981][cla]) cross-layer
  sharing — research.

### Offload & disaggregation

- **DistServe** ([2401.09670][distserve]) disaggregated prefill/decode — research prototype, but the
  *pattern* ships (vLLM experimental disagg-prefill, NVIDIA Dynamo). **Mooncake**
  ([2407.00079][mooncake], Kimi/Moonshot) KVCache-centric pooled CPU/DRAM/SSD — **production**.
  **LMCache** ([repo][lmcache] · [tech report][lmcache-paper]) pluggable tiered KV offload — vLLM's
  standard offload/disagg backend, **shipped**.

### Checkpoint/restore (execution-state migration)

- **Execution-State Capsules / FlashRT** ([arXiv 2606.20537][capsules] · [repo][flashrt], Apache-2.0)
  — graph-bound checkpoint/restore of the *complete* execution state (KV + recurrent + conv + MTP
  state + metadata, not just KV) at a committed boundary; CUDA kernels replay captured graph plans
  over contiguous static buffers with no block-table indirection, an explicit contrast to
  PagedAttention/RadixAttention. **Physical-AI/robotics-flavored**: validated on Jetson AGX Thor and
  DGX Spark edge hardware alongside datacenter GPUs, ships production VLA control (Pi0/Pi0.5/GROOT
  N1.6-N1.7/Pi0-FAST) plus LLM serving (Qwen3.6-27B). TTFT speedup over cold prefill scales 3.9x (2k
  tokens) to 27x (16k tokens); sub-millisecond GPU-resident snapshot/restore. Positioned as
  complementary to, not competing with, mainstream high-throughput KV-cache serving. **Research/early**
  — repo ~3 months old, 448 stars.

## Current state of the art (2026)

- **Production table stakes:** PagedAttention block memory + exact-prefix caching (vLLM APC / SGLang
  RadixAttention / vendor prompt-caching); **GQA** (increasingly **MLA**) as the default architecture;
  **FP8 KV** as a routine quantization knob; disaggregated prefill/decode with tiered KV offload
  (Mooncake, LMCache, Dynamo) going mainstream.
- **Still research:** token eviction/sparsity (H2O, sinks, SnapKV) and sub-4-bit KV quantization
  (KIVI, KVQuant); cross-layer sharing (CLA).
- **Trend:** from "compress a standard KV cache after the fact" → "architect the model so the KV cache
  is small by construction (MLA/GQA/CLA)" + "treat the KV cache as a first-class distributed/tiered
  storage system (Mooncake/LMCache/disaggregation)."

## Sources

| Source | Content |
|---|---|
| [Anthropic prompt caching][anthropic-caching] | Per-model minimums, TTL, pricing (verified 2026-07-08) |
| [OpenAI prompt caching][openai-caching] · [Gemini caching][gemini-caching] | Vendor prefix/context caching |
| [PagedAttention][paged] · [vLLM APC][vllm-apc] | Paged memory + prefix caching |
| [SGLang / RadixAttention][sglang] · [docs][radix] | Radix-tree prefix reuse + HiCache |
| [FP8 KV (vLLM)][vllm-fp8] · [TensorRT-LLM][trtllm-quant] · [KIVI][kivi] · [KVQuant][kvquant] · [UltraQuant][ultraquant] | Quantization |
| [H2O][h2o] · [StreamingLLM][streamingllm] · [SnapKV][snapkv] · [Scissorhands][scissorhands] | Eviction/sparsity |
| [MQA][mqa] · [GQA][gqa] · [MLA][mla] · [CLA][cla] | Architectural KV reduction |
| [DistServe][distserve] · [Mooncake][mooncake] · [LMCache][lmcache] | Offload / disaggregation |
| [Execution-State Capsules][capsules] · [FlashRT][flashrt] | Checkpoint/restore, physical-AI/robotics serving |

[anthropic-caching]: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[openai-caching]: https://developers.openai.com/api/docs/guides/prompt-caching
[gemini-caching]: https://ai.google.dev/gemini-api/docs/caching
[paged]: https://arxiv.org/abs/2309.06180
[vllm]: https://github.com/vllm-project/vllm
[vattention]: https://arxiv.org/abs/2405.04437
[vllm-apc]: https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html
[sglang]: https://arxiv.org/abs/2312.07104
[radix]: https://github.com/sgl-project/sglang
[vllm-fp8]: https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/
[trtllm-quant]: https://nvidia.github.io/TensorRT-LLM/
[kivi]: https://arxiv.org/abs/2402.02750
[kvquant]: https://arxiv.org/abs/2401.18079
[h2o]: https://arxiv.org/abs/2306.14048
[streamingllm]: https://arxiv.org/abs/2309.17453
[snapkv]: https://arxiv.org/abs/2404.14469
[scissorhands]: https://arxiv.org/abs/2305.17118
[mqa]: https://arxiv.org/abs/1911.02150
[gqa]: https://arxiv.org/abs/2305.13245
[mla]: https://arxiv.org/abs/2405.04434
[cla]: https://arxiv.org/abs/2405.12981
[distserve]: https://arxiv.org/abs/2401.09670
[mooncake]: https://arxiv.org/abs/2407.00079
[lmcache]: https://github.com/LMCache/LMCache
[lmcache-paper]: https://arxiv.org/abs/2510.09665
[ultraquant]: https://arxiv.org/abs/2606.20474
[capsules]: https://arxiv.org/abs/2606.20537
[flashrt]: https://github.com/flashrt-project/FlashRT
