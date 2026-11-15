# Topic Hub: Cost

Token usage and spend: what drives them in Claude Code and agent sessions, the settings and habits
that lower them, and the tools that measure them. Pointers only; see [the hub index](README.md).

## What drives the bill

| Doc / section | What it covers | Bucket |
|---|---|---|
| [CC-prompt-caching-behavior.md § Why Hit Rates Are So High in CC](../cc-native/context-memory/CC-prompt-caching-behavior.md#why-hit-rates-are-so-high-in-cc) | Each request re-sends the whole prefix; cache reads dominate input | cc-native |
| [CC-prompt-caching-behavior.md § One week of sessions on one machine](../cc-native/context-memory/CC-prompt-caching-behavior.md#one-week-of-sessions-on-one-machine-2026-11-07-to-2026-11-14) | Measured share of cache reads, writes and idle rewrites over seven days | cc-native |
| [CC-prompt-caching-behavior.md § Actions That Invalidate vs. Keep the Cache](../cc-native/context-memory/CC-prompt-caching-behavior.md#actions-that-invalidate-vs-keep-the-cache) | Mid-session changes that force a full cache rewrite | cc-native |
| [CC-models-reference.md § Model Pricing (current lineup)](../cc-native/configuration/CC-models-reference.md#model-pricing-current-lineup) | Per-model input, output and cache prices | cc-native |
| [CC-extended-context-analysis.md § Pricing Model](../cc-native/context-memory/CC-extended-context-analysis.md#pricing-model) | How the 1M-token window is billed | cc-native |
| [CC-session-cost-analysis.md § Shared plan usage across Claude products](../cc-native/sessions/CC-session-cost-analysis.md#shared-plan-usage-across-claude-products) | Plan usage limits shared across Claude surfaces | cc-native |

## Levers

| Doc / section | Lever | Bucket |
|---|---|---|
| [CC-prompt-caching-behavior.md § TTL varies by request bucket and billing method](../cc-native/context-memory/CC-prompt-caching-behavior.md#ttl-varies-by-request-bucket-and-billing-method) | Cache TTL per request bucket, and how to choose it | cc-native |
| [CC-prompt-caching-behavior.md § Idle compaction (before the cache expires)](../cc-native/context-memory/CC-prompt-caching-behavior.md#idle-compaction-before-the-cache-expires) | Compacting an idle session before its cache expires | cc-native |
| [CC-env-vars-reference.md § Context & Token Control](../cc-native/configuration/CC-env-vars-reference.md#context--token-control) | Auto-compact threshold and window, compaction switches, Bash/MCP output caps, output and thinking budgets, MCP tool search | cc-native |
| [CC-env-vars-reference.md § Prompt Caching](../cc-native/configuration/CC-env-vars-reference.md#prompt-caching) | Cache TTL and disable variables | cc-native |
| [CC-env-vars-reference.md § Model & Agent Selection](../cc-native/configuration/CC-env-vars-reference.md#model--agent-selection) | Cheaper model for subagents; effort level | cc-native |
| [CC-model-provider-configuration.md § Effort Levels](../cc-native/configuration/CC-model-provider-configuration.md#effort-levels) | Effort levels per model | cc-native |
| [CC-memory-system-analysis.md § Path-Scoped Rules Deep Dive](../cc-native/context-memory/CC-memory-system-analysis.md#path-scoped-rules-deep-dive) | Rules and subdirectory CLAUDE.md files that load only when matching files are read | cc-native |
| [CC-memory-system-analysis.md § Anti-Patterns](../cc-native/context-memory/CC-memory-system-analysis.md#anti-patterns) | Keeping CLAUDE.md short; splitting it into rules or imports | cc-native |
| [CC-memory-system-analysis.md § `claudeMdExcludes`](../cc-native/context-memory/CC-memory-system-analysis.md#claudemdexcludes) | Skipping irrelevant CLAUDE.md files in a monorepo | cc-native |
| [CC-skills-adoption-analysis.md § Description budget (always loaded)](../cc-native/agents-skills/CC-skills-adoption-analysis.md#description-budget-always-loaded) | The always-loaded skill-description budget and how to take a skill out of it | cc-native |
| [CC-skills-adoption-analysis.md § Skills as the replacement for procedural CLAUDE.md content](../cc-native/agents-skills/CC-skills-adoption-analysis.md#skills-as-the-replacement-for-procedural-claudemd-content) | Moving procedures from CLAUDE.md into on-demand skills | cc-native |
| [CC-skills-adoption-analysis.md § `context: fork` — Mechanics and Economics](../cc-native/agents-skills/CC-skills-adoption-analysis.md#context-fork--mechanics-and-economics) | Running a skill in a forked context so its output does not stay in the parent | cc-native |
| [CC-recursive-spawning-patterns.md § Token Cost Warning](../cc-native/agents-skills/CC-recursive-spawning-patterns.md#token-cost-warning) | Each `claude -p` subprocess re-reads the full system prompt; minimal config for spawned runs | cc-native |
| [CC-agentic-harness-patterns-analysis.md § 5. Progressive Context Compaction](../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#5-progressive-context-compaction) | CC's compaction layers and what a compaction loses | cc-native |
| [CC-advisor-tool-analysis.md § Claude Code surface](../cc-native/configuration/CC-advisor-tool-analysis.md#claude-code-surface) | Cheaper executor model with a stronger advisor; compared with `opusplan` and per-subagent models | cc-native |
| [CC-fast-mode-analysis.md § Pricing](../cc-native/configuration/CC-fast-mode-analysis.md#pricing) | What fast mode costs | cc-native |
| [CC-extended-context-analysis.md § Mitigation](../cc-native/context-memory/CC-extended-context-analysis.md#mitigation) | Keeping long sessions out of the degraded zone | cc-native |
| [CC-memory-system-analysis.md § CLAUDE.md Growth and Catastrophic Remembering (arXiv 2608.11095)](../cc-native/context-memory/CC-memory-system-analysis.md#claudemd-growth-and-catastrophic-remembering-arxiv-260811095) | Instruction-file size loaded on every request | cc-native |
| [CC-skills-adoption-analysis.md § Skill Context Budgets](../cc-native/agents-skills/CC-skills-adoption-analysis.md#skill-context-budgets) | Progressive disclosure for skills | cc-native |
| [CC-session-cost-analysis.md § Message Batches API](../cc-native/sessions/CC-session-cost-analysis.md#message-batches-api) | Batch pricing for non-interactive work | cc-native |
| [CC-community-tooling-landscape.md § Token-Waste Reduction Stack](../cc-community/CC-community-tooling-landscape.md#token-waste-reduction-stack) | Layered approach: env settings, hook filters, wrappers, output styles, prompt compression | cc-community |
| [CC-community-tooling-landscape.md § Boucle Read-Once Framework](../cc-community/CC-community-tooling-landscape.md#boucle-read-once-framework) | Hook that warns on or blocks re-reading files already in context | cc-community |
| [CC-community-tooling-landscape.md § TokenEconomizer (microsoft)](../cc-community/CC-community-tooling-landscape.md#tokeneconomizer-microsoft) | Per-repo tool pruning and loop guard; reported savings not independently replicated | cc-community |
| [CC-community-tooling-landscape.md § RTK (Rust Token Killer)](../cc-community/CC-community-tooling-landscape.md#rtk-rust-token-killer) | Filtering CLI output before it enters context; an independent check found no savings on `cat`, `grep`, `pytest` or `ruff` | cc-community |
| [CC-community-skills-landscape.md § Caveman (JuliusBrussee)](../cc-community/CC-community-skills-landscape.md#caveman-juliusbrussee) | Terse output style to cut output tokens | cc-community |
| [CC-code-tooling-landscape.md § Research: do code maps help coding agents?](../cc-community/CC-code-tooling-landscape.md#research-do-code-maps-help-coding-agents) | Whether a code map saves exploration tokens | cc-community |
| [aider-analysis.md § Codebase mapping (repo map)](../non-cc/coding-agents/aider-analysis.md#codebase-mapping-repo-map) | A repo map capped by a token budget | non-cc |
| [fastcontext-analysis.md § Adoption Decision](../non-cc/context-memory/fastcontext-analysis.md#adoption-decision) | A dedicated, cheaper repo-exploration subagent | non-cc |
| [llm-routers-gateways-landscape.md § When to Use What](../non-cc/infrastructure/llm-routers-gateways-landscape.md#when-to-use-what) | Routing requests to cheaper models through a gateway | non-cc |
| [context-management.md](../cc-native/examples/rules/context-management.md) | Example rule: context-utilization target and compaction triggers | cc-native |

## Measuring

| Doc / section | What it covers | Bucket |
|---|---|---|
| [CC-session-cost-analysis.md § Cost Extraction Recipes](../cc-native/sessions/CC-session-cost-analysis.md#cost-extraction-recipes) | `jq` recipes over session transcripts | cc-native |
| [CC-session-cost-analysis.md § All sessions ranked by cache read (dominant cost driver)](../cc-native/sessions/CC-session-cost-analysis.md#all-sessions-ranked-by-cache-read-dominant-cost-driver) | Finding the sessions that cost most | cc-native |
| [CC-session-cost-analysis.md § CLI `-p --output-format json` Result Fields](../cc-native/sessions/CC-session-cost-analysis.md#cli--p---output-format-json-result-fields) | Per-run cost fields for headless runs | cc-native |
| [CC-web-auth-setup-analysis.md § Org-Level Rate Limits and Spend Caps](../cc-native/ci-remote/CC-web-auth-setup-analysis.md#org-level-rate-limits-and-spend-caps) | Spend caps and workspace limits for API keys | cc-native |
| [CC-web-auth-setup-analysis.md § Monitoring Org Spend — Usage and Cost Admin API](../cc-native/ci-remote/CC-web-auth-setup-analysis.md#monitoring-org-spend--usage-and-cost-admin-api) | Org spend reports per key, workspace and model | cc-native |
| [CC-session-cost-analysis.md § Relationship to Statusline](../cc-native/sessions/CC-session-cost-analysis.md#relationship-to-statusline) | Live cost and context in the status line; see the [statusline.sh](../cc-native/examples/statusline.sh) example | cc-native |
| [CC-usage-tooling-landscape.md § Optimization Rules](../cc-community/CC-usage-tooling-landscape.md#optimization-rules) | CodeBurn's waste-detection rules | cc-community |
| [CC-usage-tooling-landscape.md](../cc-community/CC-usage-tooling-landscape.md) | ccusage, Claude-Code-Usage-Monitor, cc-costline | cc-community |

Related hubs: [context.md](context.md), [harness.md](harness.md), [long-running.md](long-running.md).
