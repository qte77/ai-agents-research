---
title: KV-Cache Serving Landscape — Vendor Prompt Caching & Inference Internals
purpose: "Survey of KV (key-value) cache mechanisms in LLM serving: vendor prompt-caching APIs (Anthropic, OpenAI, Gemini) and open serving-stack internals such as paging, prefix reuse and offload."
created: 2026-07-08
updated: 2026-11-25
validated_links_on: 2026-09-24
status: reference
---

**Details:** informational catalog

How the **KV cache** — the per-token key/value tensors that make autoregressive decoding tractable —
is managed, reused, compressed, and offloaded across LLM serving. Two layers: (1) the **vendor
prompt-caching APIs** a Claude Code / agent consumer bills against, and (2) the **serving-engine
internals** underneath them.

This complements [../cc-native/context-memory/CC-prompt-caching-behavior.md](../../cc-native/context-memory/CC-prompt-caching-behavior.md),
which covers Anthropic prompt caching from the **CC client / session-economics** angle only (what CC
sends, hit-rate, cost). This doc adds the **cross-vendor comparison** and the **serving mechanism**
that doc doesn't. See also the KV-cache-invalidation gotcha for self-hosted backends in
[../cc-native/configuration/CC-model-provider-configuration.md](../../cc-native/configuration/CC-model-provider-configuration.md)
(`CLAUDE_CODE_ATTRIBUTION_HEADER=0`).

## 1. Vendor prompt-caching APIs (KV reuse as a billing/latency feature)

All three expose **cross-request KV reuse** (skip prefill on a shared prefix) as an API feature. Exact
prefix match only — no semantic/fuzzy matching. Cache **read** is ~90% cheaper than base input.

| Vendor | Mechanism | Min prefix | TTL | Read / write pricing |
|---|---|---|---|---|
| **Anthropic** | Explicit `cache_control` breakpoints (auto or ≤4 manual); cumulative-hash prefix | 1,024 (Opus 4.8, Sonnet 5/4.6/4.5); 4,096 (Opus 4.6/4.5, Haiku 4.5); 2,048 (Opus 4.7); 512 (Fable 5.x/Mythos 5.x, Opus 5/5.5, Sonnet 5.5, Haiku 5.5) | 5-min default (free refresh) / 1-hour opt-in | read 0.1×; write 1.25× (5m) / 2× (1h) |
| **OpenAI** | Automatic prefix caching (no flag); hash of ~first 256 tokens; optional `prompt_cache_key` for routing affinity | 1,024 (then 128-tok increments) | 5–60 min inactivity, up to 1 h; extended tier to 24 h | read 0.1× (90% off) |
| **Google Gemini** | Implicit (on by default, 2.5+) + explicit `CachedContent` resource (generateContent API) | 2,048 (2.5 Flash/Pro); 4,096 (3.x preview) | implicit auto; explicit default 1 h, configurable | cached-token rate (~0.1×) **plus** a per-hour storage rate |

Anthropic's per-model minimums verified against the [prompt-caching docs][anthropic-caching]
(2026-07-08; 512-token list re-read 2026-11-23). An earlier note here said Bedrock uses 1,024 for Fable 5 / Mythos 5; that was corrected on 2026-10-15 (see [CC-prompt-caching-behavior.md](../../cc-native/context-memory/CC-prompt-caching-behavior.md#minimum-cacheable-prefix)). CC picks the TTL tier per request (it is not limited to the 5-min tier); see
[CC-prompt-caching-behavior.md](../../cc-native/context-memory/CC-prompt-caching-behavior.md).

## 2. Serving-engine internals

### Memory management / paging

- **PagedAttention** ([arXiv 2309.06180][paged] · [vLLM][vllm]) — KV cache as OS-style paged virtual
  memory: non-contiguous blocks, near-zero fragmentation, cross-sequence sharing. **Shipped** — the de
  facto standard, echoed by TensorRT-LLM / SGLang / TGI.
- **vAttention** ([arXiv 2405.04437][vattention], Microsoft) — CUDA virtual-memory demand paging to
  keep KV contiguous without block indirection. Research/early.
- **kvcached** ([site][kvcached-site] · [repo][kvcached-repo], Apache-2.0) — applies the OS-style
  virtual-memory idea one level up from PagedAttention: decouples GPU *virtual* addressing from
  *physical* KV allocation so vLLM (≥v0.8.4) and SGLang (≥v0.4.9) can elastically share one GPU across
  multiple LLM instances with no engine-code changes, plus a frontend router and per-model sleep mode.
  **Shipped** — v0.1.5 (2026-04-07), 2,054 stars (`gh api` 2026-11-22), and listed under the README's own "Trusted and
  deployed by" logos (Google, LinkedIn, Intel, AMD, Red Hat, and others; accessed 2026-09-24). Vendor-
  reported benchmark: **2–28x TTFT reduction** serving three Llama-3.1-8B instances on one A100-80G
  under intermittent-peak load, vs. static per-model memory reservation.

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
  outlier-aware low-bit for long context. **Research** (not mainline defaults). KVQuant is cited as a
  research concept, not an option to deploy: its [reference repo][kvquant-repo] was last pushed 2024-08-13
  (`gh api`, 2026-11-22).
- **UltraQuant / Ultra-TurboQuant** ([arXiv 2606.20474][ultraquant], AMD) — 4-bit K/V for context-heavy
  agentic serving; Ultra-TQ = optimized rotation+codebook (TurboQuant-derived), UltraQuant = hardware-
  native FP4 via AMD CDNA4 scaled-MFMA. Vs. vLLM's FP8 KV baseline on AMD MI355X: P50 TTFT 3.47x faster
  in cache-pressured late rounds (2.3x averaged), 1.63x output throughput — though FP8 stays ahead
  (0.86x) in early "warm" rounds, so the gain is concentrated in the long-context/high-concurrency
  regime. **Research**; the paper (HTML version, appendix A.2, read 2026-11-22) says the Ultra-TQ decode
  kernel was upstreamed into vLLM mainline and the UltraQuant FP4 kernel is planned as a follow-up release.

### Eviction / sparsity (mostly research)

- **H2O** ([2306.14048][h2o]) heavy-hitter eviction · **StreamingLLM / attention sinks**
  ([2309.17453][streamingllm]) — the sinks idea influenced production sliding-window configs ·
  **SnapKV** ([2404.14469][snapkv]) prompt-side compression · **Scissorhands** ([2305.17118][scissorhands]).
  No major stack ships eviction-based compression as a default path as of mid-2026. H2O is cited as
  a research concept, not an option to deploy: its [reference repo][h2o-repo] was last pushed
  2024-08-01 (`gh api`, 2026-11-22).

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
  — repo ~3 months old, 821 stars (`gh api` 2026-11-22).

## Cache timing, isolation and local reuse

Defensive/academic summary of what a prompt cache's timing exposes, how vendors isolate it, and
whether a client can rebuild or host one locally. Builds on the vendor table in section 1 and the
engines in section 2 (vLLM APC, SGLang, LMCache, Mooncake); the CPU-side analogue is in
[detokenization-leaks-analysis.md](../../sdlc-lcm/detokenization-leaks-analysis.md).

### What timing can and cannot reveal

A cache hit skips prefill, so time-to-first-token (TTFT) is lower; a client sees hit or miss, never the
cached tensors. Evidence levels below are peer-reviewed or preprint as stated.

- **Provider audit** ([Gu et al., 2502.07776][gu-audit], ICML 2025): statistical timing audit. In the
  paper's results it found global (cross-user) sharing in 7 providers (Azure, Deep Infra, Fireworks,
  Lepton, OpenAI, Perplexity, Replicate) and per-organization sharing only for Anthropic (Claude 3
  Haiku) and OpenAI GPT-4o mini. The abstract reports the OpenAI embedding model as decoder-only,
  inferred from timing. **As of the paper (v1 2025-02, v2 2025-07)**; vendors changed policies after
  disclosure, so it is not a current-state statement.
- **PromptPeek** ([Wu et al., NDSS][promptpeek]): self-hosted multi-tenant serving (SGLang, vLLM
  class) that shares KV blocks across users lets one tenant reconstruct another's prompt; the paper
  concludes such serving needs careful resource management. Targets self-hosted engines, not closed APIs.
- **InputSnatch** ([2411.18191][inputsnatch], preprint, no venue listed) and **Early Bird**
  ([2409.20002][earlybird], accepted at IEEE TIFS) apply the same timing idea to prefix and semantic
  caches. Success figures are in the papers, not repeated here (not stated on the abstract pages).

### Prompt reconstruction from KV caches and defences

- **KV-Cloak** ([2508.09442][kvcloak], NDSS 2026): threat model is a party with access to the KV cache
  itself; the paper shows direct inversion, collision and injection attacks and proposes reversible
  matrix obfuscation of the cache, reporting reconstruction reduced to noise with minimal overhead.
- **SafeKV** ([2508.08438][safekv], preprint, no venue): isolate only blocks detected as sensitive
  instead of isolating everything; reports up to 40.58% lower TTFT overhead and up to 2.66x
  throughput versus full isolation (abstract, as of v2 2026-02-09).

### Vendor isolation

- **Anthropic** ([docs][anthropic-caching], read 2026-11-25): "Different organizations never share
  caches, even if they use identical prompts." On the Claude API, Claude Platform on AWS and
  Microsoft Foundry caches are also isolated between workspaces; on Claude Models on Google Cloud
  (Google managed) and Amazon Bedrock "caches are isolated by organization only".
- **OpenAI** ([docs][openai-caching], read 2026-11-25): "Caches are not shared across organizations
  and cannot be reused across regional processing boundaries." Separate `prompt_cache_key` values
  per customer "help prevent cache-hit probing across customers" (a mitigation, not a guarantee).

### Local persistence and reuse (open weights only)

| Item | What it does | Evidence / status (as of 2026-11-25) |
|---|---|---|
| **llama.cpp server** ([repo][llamacpp]) | `--slot-save-path` plus `POST /slots/{id}?action=save` / `restore` write a slot's prompt cache to a file and reload it; `cache_prompt` reuse defaults on | MIT, 136,235 stars, pushed 2026-11-25; documented in the server README |
| **CacheGen** ([2310.07240][cachegen]) | Compresses and streams KV caches; reports 3.5-4.3x smaller cache and 3.2-3.7x lower fetch+processing delay vs prior reuse systems | SIGCOMM'24; [repo][cachegen-repo] 176 stars, no licence field, last push 2024-10-09 (stale) |
| **CacheBlend** ([2405.16444][cacheblend]) | Reuses non-prefix KV caches (RAG chunks) with partial recompute; 2.2-3.3x lower TTFT, 2.8-5x throughput vs full recompute | Preprint; abstract page links [LMCache][lmcache]; standalone [repo][cacheblend-repo] 207 stars, no licence field, last push 2025-07-15 |
| **SCBench** ([2412.10319][scbench]) | Benchmark of long-context methods from a KV-cache angle (12 tasks, 8 solution categories); sub-O(n) memory methods struggle in multi-turn | ICLR 2025. Measures accuracy under KV reuse, **not** cache hit rate or TTFT savings |

### Verdict

A closed provider's prompt cache cannot be rebuilt or hosted locally: the cache holds tensors tied to
closed weights and is isolated per organization (Anthropic also per workspace). The client can observe
only hit/miss (billing counts and TTFT). Local caching and persistence need open weights and an
engine such as vLLM, SGLang, LMCache or llama.cpp.

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
| [kvcached][kvcached-repo] · [site][kvcached-site] | OS-style virtual-memory KV manager for elastic multi-LLM GPU sharing |
| [SGLang / RadixAttention][sglang] · [docs][radix] | Radix-tree prefix reuse + HiCache |
| [FP8 KV (vLLM)][vllm-fp8] · [TensorRT-LLM][trtllm-quant] · [KIVI][kivi] · [KVQuant][kvquant] ([repo][kvquant-repo], last push 2024-08) · [UltraQuant][ultraquant] | Quantization |
| [H2O][h2o] ([repo][h2o-repo], last push 2024-08) · [StreamingLLM][streamingllm] · [SnapKV][snapkv] · [Scissorhands][scissorhands] | Eviction/sparsity |
| [MQA][mqa] · [GQA][gqa] · [MLA][mla] · [CLA][cla] | Architectural KV reduction |
| [DistServe][distserve] · [Mooncake][mooncake] · [LMCache][lmcache] | Offload / disaggregation |
| [Execution-State Capsules][capsules] · [FlashRT][flashrt] | Checkpoint/restore, physical-AI/robotics serving |
| [Gu et al. audit][gu-audit] · [PromptPeek][promptpeek] · [InputSnatch][inputsnatch] · [Early Bird][earlybird] | Cache-timing attacks and audits |
| [KV-Cloak][kvcloak] · [SafeKV][safekv] | KV-cache reconstruction defences |
| [llama.cpp][llamacpp] · [CacheGen][cachegen] · [CacheBlend][cacheblend] · [SCBench][scbench] | Local persistence/reuse and benchmark |

[anthropic-caching]: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
[openai-caching]: https://developers.openai.com/api/docs/guides/prompt-caching
[gemini-caching]: https://ai.google.dev/gemini-api/docs/caching
[paged]: https://arxiv.org/abs/2309.06180
[vllm]: https://github.com/vllm-project/vllm
[vattention]: https://arxiv.org/abs/2405.04437
[kvcached-site]: https://kvcached.org
[kvcached-repo]: https://github.com/ovg-project/kvcached
[vllm-apc]: https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html
[sglang]: https://arxiv.org/abs/2312.07104
[radix]: https://github.com/sgl-project/sglang
[vllm-fp8]: https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/
[trtllm-quant]: https://nvidia.github.io/TensorRT-LLM/
[kivi]: https://arxiv.org/abs/2402.02750
[kvquant]: https://arxiv.org/abs/2401.18079
[kvquant-repo]: https://github.com/SqueezeAILab/KVQuant
[h2o]: https://arxiv.org/abs/2306.14048
[h2o-repo]: https://github.com/FMInference/H2O
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
[gu-audit]: https://arxiv.org/abs/2502.07776
[promptpeek]: https://www.ndss-symposium.org/ndss-paper/i-know-what-you-asked-prompt-leakage-via-kv-cache-sharing-in-multi-tenant-llm-serving/
[inputsnatch]: https://arxiv.org/abs/2411.18191
[earlybird]: https://arxiv.org/abs/2409.20002
[kvcloak]: https://arxiv.org/abs/2508.09442
[safekv]: https://arxiv.org/abs/2508.08438
[llamacpp]: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
[cachegen]: https://arxiv.org/abs/2310.07240
[cachegen-repo]: https://github.com/UChi-JCL/CacheGen
[cacheblend]: https://arxiv.org/abs/2405.16444
[cacheblend-repo]: https://github.com/YaoJiayi/CacheBlend
[scbench]: https://arxiv.org/abs/2412.10319
