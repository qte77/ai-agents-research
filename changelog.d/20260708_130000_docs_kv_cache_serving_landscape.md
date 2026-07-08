### Added

- `docs/non-cc/kv-cache-serving-landscape.md`: new landscape on KV-cache serving — a cross-vendor prompt-caching comparison (Anthropic/OpenAI/Gemini: minimums, TTL, pricing) plus open serving-stack internals (PagedAttention/vLLM, SGLang RadixAttention, FP8/KIVI quantization, H2O/StreamingLLM eviction, GQA/MLA architectural sharing, Mooncake/LMCache offload-disaggregation) with a 2026 state-of-the-art synthesis.

### Changed

- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: corrected the stale model-dependent minimum cacheable-prefix tiers (Opus 4.8 is **1,024** tokens, not 4,096; added Sonnet 5, Haiku 4.5, Opus 4.7, Fable 5/Mythos 5 — verified against the Anthropic caching docs, 2026-07-08); added a Related section cross-linking the new KV-cache serving landscape and the KV-invalidation gotcha in `CC-model-provider-configuration.md`.
