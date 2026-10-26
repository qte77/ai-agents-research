### Changed

- `docs/cc-native/configuration/CC-models-reference.md`: replaced the stale "Fable 5 (newest model)" framing and
  "Opus-tier $5/$25" comparison with the current per-model price table (Fable/Mythos 5.1 and 5, Opus 5.5 down
  through 4.5, Sonnet 5.5/5/4.6/4.5, Haiku 5.5's two prompt-length tiers, Haiku 4.5) from the pricing page, and
  noted Sonnet 5's $2/$10 per-MTok rate is now standard, not introductory.
- `docs/cc-native/sessions/CC-session-cost-analysis.md`: fixed a doubled `docs/` segment in the pricing-page link;
  replaced the duplicated Opus/Sonnet/Haiku 4.6 price table with a pointer to CC-models-reference.md.
- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: replaced the flat 0.1x cache-hit multiplier with
  the per-model tiers (0.025x Fable/Mythos 5.1, 0.05x Opus/Sonnet 5.5, 0.1x others); requoted the Bedrock/Google
  Cloud cache-isolation sentence, which was no longer verbatim against the current prompt-caching docs.

### Added

- `docs/cc-native/sessions/CC-session-cost-analysis.md`: documented the price modifiers the usage object already
  exposes (`speed`/fast mode, `inference_geo`, cloud regional-endpoint premiums, long-context and Haiku 5.5
  prompt-length pricing, discount-stacking rules, tool-use overhead tokens, and Claude Managed Agents'
  $0.08/session-hour rate), and added a bounded Message Batches API section (discount, limits, unsupported
  parameters, best-effort caching, rate-limit exemption, `output-300k-2026-03-24` beta).
- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: added the platform-level facts missing from the
  doc (4-breakpoint limit, automatic caching's breakpoint slot, TTL-ordering rule, lifetime start, ZDR eligibility,
  no manual clear, best-effort caching with Batches) and a sibling "API-level invalidation" subsection next to the
  existing Claude Code invalidation list, recording — without resolving — a conflict between the API docs
  ("effort" changes always invalidate) and the Claude Code docs (no invalidation on the 5.5-series models).
