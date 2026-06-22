### Changed

- `docs/cc-native/configuration/CC-models-reference.md` + `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: **stale-fact refresh** against first-party Anthropic sources (claude-api reference) — Fable 5 tokenizer figure tightened to ≈1×–1.35× (was "~30%"); the Fable 5 CC-plan-access line reframed now that the 2026-06-22 credit-transition date has arrived; added the model-dependent **minimum cacheable prefix** (4096 tokens on Opus-tier, 2048 on Fable 5 / Sonnet 4.6). Partial #304.

### Fixed

- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: corrected the doubled `/docs/en/docs/` path segment in the prompt-caching, pricing, and messages source URLs to the canonical first-party form.
