### Added

- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: CC's request-bucket TTL model (main
  conversation vs. everything else), the `promptCacheTtl`/`subagentPromptCacheTtl` settings and
  `CLAUDE_CODE_PROMPT_CACHE_TTL`/`CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`/`FORCE_PROMPT_CACHING_5M`/
  `ENABLE_PROMPT_CACHING_1H` env vars with their precedence order, the `DISABLE_PROMPT_CACHING*`
  variables, a concise "actions that invalidate vs. keep the cache" summary, and a Cache Scope section
  (plan 0012 row N2).
- `docs/cc-native/configuration/CC-env-vars-reference.md`: new Prompt Caching subsection for the same
  TTL-selection and disable variables, cross-ref'd to the caching-behavior doc.
- `docs/cc-native/configuration/CC-cli-reference.md`: a `--resume` vs. `--continue` vs. `--fork-session`
  comparison table, including that a fork does not isolate the working directory (only the session
  identity forks — directory isolation is `--worktree`/`-w`).
- `docs/cc-native/sessions/CC-session-cost-analysis.md`: documented `SDKResultMessage` fields for
  `-p --output-format json` (`total_cost_usd`, `usage`, `modelUsage`, `duration_api_ms`, `num_turns`, …)
  with a jq recipe over those fields only; general claude.ai usage-limit best practices (flagged as not
  CC-specific); the Claude Code wrap-up allowance (CC v2.1.277+, Pro/Max/Team-Premium eligibility,
  frequency, and what it is and isn't).

### Changed

- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: corrected two stale claims found while
  re-verifying against the live docs — CC does **not** use the 5-minute ephemeral cache exclusively (it
  requests a 1-hour TTL by default on a Claude subscription within plan usage for the main conversation);
  and the claimed Bedrock exception for the Fable 5/Mythos 5 minimum cacheable prefix is contradicted by
  the current docs ("these minimums apply on every platform"), so it was removed. The minimum-cacheable-
  prefix table was also refreshed to include newer models (Opus 5.5, Opus 5, Sonnet 5.5, Haiku 5.5, Fable
  5.1, Mythos 5.1), all at 512 tokens.
