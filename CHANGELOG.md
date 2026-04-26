<!-- markdownlint-disable MD024 no-duplicate-heading -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Types of changes**: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`

## [Unreleased]

### Added

- `docs/cc-community/CC-community-tooling-landscape.md`: ccusage (13.4K stars, MIT, ryoppippi, v18.0.11) — CC/Codex JSONL usage analyzer with daily/monthly/session/blocks reports, cache-token split, offline mode (`--offline`), built-in MCP server, statusline hook (Beta); reads `~/.claude/projects/`
- `docs/cc-community/CC-community-tooling-landscape.md`: Claude-Code-Usage-Monitor (7.8K stars, MIT, Maciek-roboblog, v3.1.0) — predictive real-time TUI with P90-based custom plan auto-detection, burn-rate analytics, Pro/Max5/Max20 plan-aware limits; Python 3.9+ via `uv tool install` or `pip`
- `docs/cc-community/CC-community-tooling-landscape.md`: CodeBurn (4K stars, MIT, AgentSeal) — cross-agent token-usage TUI dashboard reading on-disk session data from Claude Code, Codex, Cursor, OpenCode, Copilot and others; 13 task categories, `optimize`/`compare`/`export` subcommands, LiteLLM-sourced pricing, native macOS menubar app
- `docs/cc-community/CC-community-tooling-landscape.md`: cross-refs added on RTK and Boucle sections linking to caveman, the new measurement-layer tools (CodeBurn / ccusage / Claude-Code-Usage-Monitor), and CC hooks system
- `docs/cc-community/CC-community-skills-landscape.md`: Caveman (46.9K stars, MIT, v1.6.0) — telegraphic-speech output-compression skill pack (Lite/Full/Ultra plus Wenyan variants); skills `caveman-commit`, `caveman-review`, `caveman-help`, `caveman-compress`; multi-agent install (Claude Code marketplace, Gemini extensions, npx skills, standalone hook); self-reported ~65% avg output-token savings (22–87% range)
- `Makefile`: build tooling for docs linting — sudo-less install recipes for Node.js, lychee, markdownlint-cli2 (`setup_node`, `setup_lychee`, `setup_mdlint`, `setup_all`), plus `check_links`, `check_docs`, `autofix`, `lint` targets; adapted from the authoritative `qte77/so101-biolab-automation` Makefile conventions (PR #98)
- `docs/cc-native/agents-skills/CC-skills-adoption-analysis.md`: new Skill Context Budgets subsection documenting three-level progressive disclosure (~100 tokens metadata / <5k SKILL.md body / unlimited bundled), shared 25k-token auto-compaction budget with 5k per-skill preservation, 1% / 8000-char description budget with 250-char per-skill cap and `SLASH_COMMAND_TOOL_CHAR_BUDGET` override, and the framing quote on skills as the replacement for procedural CLAUDE.md content (PR #96)
- `docs/cc-community/CC-community-tooling-landscape.md`: Graphify (16.5K stars, code→knowledge graph, CC hooks/MCP), MemPalace (33.6K stars, palace-metaphor memory, 19 MCP tools), Code-Review-Graph (7.1K stars, AST blast-radius, 22 MCP tools)
- `docs/non-cc/feynman-analysis.md`: Companion AI Feynman research agent (3.8K stars, 4 sub-agents, experiment replication)
- `docs/non-cc/insforge-analysis.md`: InsForge agent backend platform (7.3K stars, auth/DB/storage/functions semantic layer)
- `docs/non-cc/goclaw-analysis.md`: GoClaw multi-tenant agent gateway (2.4K stars, Go, 7 messaging channels, 8-stage pipeline)
- `docs/non-cc/rowboat-analysis.md`: Rowboat AI coworker (11.1K stars, knowledge graph from communications, Obsidian-compatible)
- `docs/non-cc/hermes-agent-analysis.md`: Nous Research Hermes Agent (43.2K stars, self-improving skills, 7 platforms)
- `CONTRIBUTING.md`: classification guidance for cc-community vs non-cc placement, `platform_scope` frontmatter field

### Fixed

- `docs/cc-community/CC-repo-to-docs-tools-landscape.md`: typo `CC-llmstxt-analysis.md` → `CC-llms-txt-analysis.md` (broken relative link regression from the URL triage batches PR); opportunistic markdownlint cleanup (MD031 / MD032 / MD040) in the same file (PR #97)
- `docs/cc-native/configuration/CC-changelog-feature-scan.md`: relative path `plugins-ecosystem/` → `../plugins-ecosystem/` (pre-existing broken internal link), resolve two permanent redirects `docs.anthropic.com/en/docs/claude-code/{hooks-guide,sdk}` → `code.claude.com/docs/en/{hooks-guide,agent-sdk/overview}` (PR #97)
- `docs/cc-native/agents-skills/CC-agent-teams-orchestration.md`: remove Aura Frog guide row + link def (external repo returned 404); resolve `docs.arize.com/phoenix` → `arize.com/docs/phoenix` permanent redirect (PR #97)
- `docs/non-cc/{hermes-agent,insforge}-analysis.md`, `docs/cc-native/plugins-ecosystem/CC-cowork-skills-api-workflows.md`: resolve permanent redirects on `agentskills.io` and `docs.insforge.dev` (PR #97)

### Changed

- `docs/cc-community/CC-repo-to-docs-tools-landscape.md`: consolidate cross-references, link Graphify and Code-Review-Graph
- `docs/non-cc/README.md`: add Infrastructure section (InsForge, GoClaw), expand Agents section (Feynman, Hermes, Rowboat)
- `README.md`: update contents table with expanded non-cc and cc-community descriptions
- `docs/cc-community/CC-community-tooling-landscape.md`: add `platform_scope` frontmatter, update comparison table (10→13 tools)

- `docs/cc-native/model-internals/`: new category for model-level interpretability research
- `docs/cc-native/model-internals/CC-emotion-vectors-interpretability.md`: Anthropic emotion concepts paper analysis (171 vectors, causal behavioral influence)
- `docs/cc-native/model-internals/CC-first-party-interpretability-index.md`: curated index of 21 Anthropic research publications (sycophancy, reasoning traces, safety classifiers, alignment steering)
- `docs/cc-community/CC-community-skills-landscape.md`: superpowers (135K stars, TDD methodology), dispatch (context window multiplication), claude-howto weekend fork note
- `docs/cc-community/CC-community-tooling-landscape.md`: claude-mem (45.2K stars, persistent memory), CC Switch (38.9K stars, multi-CLI provider management), opensrc (npm source fetcher)

### Changed

- `docs/cc-community/CC-community-skills-landscape.md`: claude-code-best-practice updated to 31.8K stars with A/C/S tag framework
- `CONTRIBUTING.md`: doc standards (frontmatter, validated_links, status badge, Sources section, naming, anti-patterns)
- `docs/cc-native/sessions/CC-session-cost-analysis.md`: transcript JSONL cost extraction with jq recipes, Opus 4.6 pricing
- `docs/cc-native/sessions/CC-session-lifecycle-analysis.md`: /rename bugs, slug persistence, 6 upstream issues
- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: server-side caching, 96.3% hit rate, 85% cost savings
- `docs/cc-native/configuration/CC-env-vars-reference.md`: consolidated CLAUDE_CODE_* env vars
- `docs/cc-native/configuration/CC-tools-inventory.md`: 28 built-in tools snapshot (CC 2.1.83)
- `docs/learnings/`: cross-repo compound learnings hub

### Changed

- Split `ci-execution/` (16 docs) into `sessions/` (4), `sandboxing/` (4), `ci-remote/` (8)
- Rename `community/` → `cc-community/` (all docs are CC-scoped)
- Move `CC-changelog-feature-scan.md`, `CC-inline-visuals-analysis.md` into `configuration/`
- Move `analysis/`, `landscape/`, `best-practices/`, `research/` → `docs/todo/` (Agents-eval era, pending review)
- Fix `sources:` in frontmatter → Sources section (9 docs)
- Add Sources tables to 5 cc-community docs

### Removed

- `CC-context-caching-patterns.md`: FACT/Arcade.dev third-party pattern, not CC-native
- `ci-execution/` directory (replaced by sessions/, sandboxing/, ci-remote/)

- `docs/sdlc-lcm/`: SDLC phase spec, LCM product lifecycle spec, release runbook, OSS ALM landscape, agentic SDLC patterns, multi-agent onboarding outlook (PRs #51, #54)
- `.github/README.md`: CI automation overview — monitors, scripts, state, triage pipeline
- `.github/ISSUE_TEMPLATE/`: bug report, question, and config templates
- Header comments on all 3 workflow YAMLs describing purpose and output

### Changed

- Renamed CABIO → RAPID across sdlc-lcm docs (PR #57)

### Changed

- `cc-status-monitor.yaml`: replace `create-triage-pr` with inline PR creation — no timestamped report copies, `outages.jsonl` as sole database
- `cc-status-monitor.yaml`, `cc-changelog-monitor.yaml`, `cc-changelog-community-monitor.yaml`: upgrade `actions/checkout` v4→v6 and `actions/setup-python` v5→v6 (Node.js 24)
- `PULL_REQUEST_TEMPLATE.md`: add CI validation and security checklist sections
- `README.md`: simplify as concise entrypoint with why/what/how structure

### Removed

- `triage/status-monitor/2026-03-18-status-report.md`: redundant timestamped copy of `outage-stats.md`

---

### Added

- `docs/cc-native/plugins-ecosystem/CC-connectors-overview.md`: MCP connectors analysis — prebuilt integrations (Google Drive/Gmail/Calendar, GitHub, Slack, M365), custom connector types, platform availability, Google connector deep-dives, applicability to coding agent workflows
- `docs/cc-native/plugins-ecosystem/CC-cowork-skills-api-workflows.md`: Cowork, Skills API, CC Web, Chrome extension programmatic workflow analysis — API endpoints, cross-surface availability, community orchestration tools, multi-repo cloud execution patterns
- `.github/scripts/lib/monitor_utils.py`: shared utilities (keyword extraction, doc scanning, coverage checking, state management, HTTP fetching)
- `.github/scripts/native-sources-monitor.py`: native sources monitor (Anthropic Blog, CC GitHub Issues/Discussions)
- `.github/state/native-monitor-state.json`: state tracking for native sources monitor
- `docs/cc-native/CC-inline-visuals-analysis.md`: Claude inline visuals (custom charts, diagrams, interactive visualizations in conversation, March 12 2026)
- `docs/community/CC-community-skills-landscape.md`: community skill libraries (gstack, pm-skills, claude-code-best-practice)
- `docs/community/CC-community-plugins-landscape.md`: community plugin catalogs (awesome-claude-code, awesome-claude-code-plugins)
- `docs/community/CC-community-tooling-landscape.md`: developer tooling (RTK context compression)
- `docs/community/CC-domain-claudemd-showcase.md`: domain-specific CLAUDE.md patterns (genome analysis)
- `docs/cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`: plan file anatomy, plan mode mechanics, plan-to-skill/rule extraction
- `cc-changelog-community-monitor.yaml`: community source monitor workflow (claudelog, awesome-claude-code, awesome-claude-code-plugins)
- `.github/scripts/community-monitor.py`: companion script for community source monitoring
- `.github/actions/create-triage-pr/action.yaml`: reusable composite action for triage PR creation

### Changed

- `CC-remote-control-analysis.md`: add `/mobile` slash command with source reference
- `community-monitor.py`: add Reddit (r/ClaudeAI) and X (#ClaudeCode) sources with OAuth2/Bearer auth, graceful skip on missing secrets
- `cc-changelog-community-monitor.yaml`: pass `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `X_BEARER_TOKEN` secrets as env vars
- DRY monitor scripts: extract shared functions into `lib/monitor_utils.py`, update `changelog-compare.py` and `community-monitor.py` to import from shared lib
- `cc-changelog-monitor.yaml`: add native sources monitor step, extend triage PR condition
- Rename `changelog-monitor.yaml` to `cc-changelog-monitor.yaml`
- Restructure `docs/` into `docs/cc-native/` (Anthropic features) and `docs/community/` (third-party)
- DRY both monitor workflows via `create-triage-pr` composite action
- `cc-changelog-monitor.yaml`: scope `--docs-dir` to `docs/cc-native/` (was `docs/`)
- `cc-changelog-community-monitor.yaml`: align schedule to Monday 10:00 UTC (1h after native)
- `CC-changelog-feature-scan.md`: group sections under `[yyyy-MM-dd]` date heading
- `CC-agent-teams-orchestration.md`: expand worktree isolation (auto-cleanup, config sharing v2.1.63), add Task Tool Metrics (v2.1.30)
- `CC-memory-system-analysis.md`: add agent memory frontmatter (v2.1.33), add `includeGitInstructions` setting (v2.1.69)
- `CC-ralph-enhancement-research.md`: note `.claude/` config sharing resolved by v2.1.63
- `CC-version-pinning-resilience.md`: add structured output schema note for `-p` mode (v2.1.22)

### Fixed

- `changelog-monitor.yaml`: remove non-existent `changelog-scan` label from `gh pr create`, update paths for restructured docs

## [0.3.0] - 2026-03-12

### Added

- `CC-sandbox-platforms-landscape.md`: sandbox platforms landscape analysis
- `CC-version-pinning-resilience.md`: version pinning resilience research
- `CC-bash-mode-analysis.md`: bash mode analysis
- `CC-web-scraping-plugins-analysis.md`: web scraping plugins analysis
- `CC-changelog-feature-scan.md`: changelog feature scan (v2.1.0-2.1.71)

### Changed

- `CC-remote-access-landscape.md`: updated with new findings

## [0.2.0] - 2026-03-08

### Added

- `CC-plugin-packaging-research.md`: Common Pitfalls section

## [0.1.0] - 2026-03-08

### Added

- `CC-agent-teams-orchestration.md`: agent teams orchestration analysis
- `CC-chrome-extension-analysis.md`: Chrome extension analysis
- `CC-cli-anything-analysis.md`: CLI-anything analysis
- `CC-cloud-sessions-analysis.md`: cloud sessions analysis
- `CC-cowork-plugins-enterprise-analysis.md`: Cowork plugins enterprise analysis
- `CC-extended-context-analysis.md`: extended context (1M) analysis
- `CC-fast-mode-analysis.md`: fast mode analysis
- `CC-github-actions-analysis.md`: GitHub Actions analysis
- `CC-hooks-system-analysis.md`: hooks system analysis
- `CC-llms-txt-analysis.md`: llms.txt analysis
- `CC-memory-system-analysis.md`: memory system analysis
- `CC-model-provider-configuration.md`: model provider configuration
- `CC-official-plugins-landscape.md`: official plugins landscape
- `CC-plugin-packaging-research.md`: plugin packaging research
- `CC-ralph-enhancement-research.md`: Ralph enhancement research
- `CC-remote-access-landscape.md`: remote access landscape
- `CC-remote-control-analysis.md`: remote control analysis
- `CC-sandboxing-analysis.md`: sandboxing analysis
- `CC-skills-adoption-analysis.md`: skills adoption analysis
