<!-- markdownlint-disable MD024 no-duplicate-heading -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Types of changes**: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`

## [Unreleased]

### Added

- `CC-github-actions-analysis.md`: `/install-github-app` interactive wizard (pre-flight warnings, OAuth/API-key chooser, workflow selector); Custom App for Bedrock/Vertex; pin v1.0 GA (2025-08-26); GitHub App provenance from [github.com/apps/claude](https://github.com/apps/claude)
- `devstral-analysis.md`: Mistral Devstral (Apache 2.0); Small 1.0/1.1/2 (24B) at 46.8/53.6/**68.0%** SWE-Bench, Devstral 2 (123B) at 72.2%; 256k, vision, single-GPU local; runs under Claude Code; new "Coding Models" section in `non-cc/README.md`
- `CC-llms-txt-analysis.md`: HuggingScience (huggingscience.co) as `llms-full.txt` adoption beyond product docs — 100+ scientific models across 17 domains
- `CC-office-document-skills.md`, `CC-web-scraping-plugins-analysis.md`: engine-layer cross-links (dated 2026-04-26) to doc-pipeline-engine `landscape-{output,ingest}.md` (#131, #132)
- `CC-community-tooling-landscape.md`: ccusage (13.4K, MIT, v18.0.11), Claude-Code-Usage-Monitor (7.8K, MIT, v3.1.0), CodeBurn (4K, MIT) + 7-category Optimization Rules taxonomy (file-read repeats, read:edit ratio, bash output cap, unused MCP, ghost agents/skills, bloated configs, cache overhead); cross-refs on RTK/Boucle to measurement layer
- `CC-community-skills-landscape.md`: Caveman (46.9K, MIT, v1.6.0) — output-compression skill pack
- `Makefile`: docs-lint build tooling (`setup_*`, `check_*`, `autofix`, `lint`) per `qte77/so101-biolab-automation` (PR #98)
- `CC-skills-adoption-analysis.md`: Skill Context Budgets — 100/5k/unlimited disclosure tiers, 25k auto-compaction budget, 1%/8000-char description budget (PR #96)
- `CC-community-tooling-landscape.md`: Graphify (16.5K), MemPalace (33.6K), Code-Review-Graph (7.1K); claude-mem (45.2K), CC Switch (38.9K), opensrc
- `CC-community-skills-landscape.md`: superpowers (135K, TDD methodology), dispatch (context window multiplication), claude-howto weekend fork note
- `non-cc/`: feynman (3.8K), insforge (7.3K), goclaw (2.4K), rowboat (11.1K), hermes-agent (43.2K)
- `cc-native/model-internals/`: emotion vectors (171), first-party interpretability index (21 publications)
- `CONTRIBUTING.md`: cc-community vs non-cc classification, `platform_scope` frontmatter, doc standards (validated_links, status badge, Sources section)
- `docs/learnings/`: cross-repo compound learnings hub

### Changed

- `.claude/settings.json`: `env.BASH_MAX_OUTPUT_LENGTH=15000` (default 30000) — CodeBurn rule #3, ~3.8K tokens/session saved on bash output cap
- `CC-community-tooling-landscape.md`: `platform_scope` frontmatter, comparison table 10→13 tools
- `CC-repo-to-docs-tools-landscape.md`: cross-references; link Graphify and Code-Review-Graph
- `non-cc/README.md`: Infrastructure section (InsForge, GoClaw); expand Agents (Feynman, Hermes, Rowboat)
- `README.md`: contents table with expanded non-cc and cc-community; concise entrypoint structure
- `CC-community-skills-landscape.md`: claude-code-best-practice → 31.8K stars + A/C/S tag framework
- `cc-native/`: session JSONL cost extraction (jq recipes, Opus 4.6 pricing); /rename bugs + 6 upstream issues; prompt caching (96.3% hit, 85% savings); CLAUDE_CODE_* env vars consolidated; 28 built-in tools snapshot (CC 2.1.83)
- Restructure: split `ci-execution/` → `sessions/`/`sandboxing/`/`ci-remote/`; rename `community/` → `cc-community/`; move `analysis/landscape/best-practices/research/` → `docs/todo/`; `sources:` frontmatter → Sources section (9 docs); Sources tables on 5 cc-community docs
- Renamed CABIO → RAPID across sdlc-lcm docs (PR #57)
- CI: monitors `cc-status-monitor.yaml` inline PR creation, `outages.jsonl` as sole DB; upgrade `actions/checkout` v4→v6 + `setup-python` v5→v6
- `PULL_REQUEST_TEMPLATE.md`: CI validation + security checklist

### Fixed

- `CC-repo-to-docs-tools-landscape.md`: typo `llmstxt` → `llms-txt`; markdownlint cleanup (PR #97)
- `CC-changelog-feature-scan.md`: relative path fix; `docs.anthropic.com` → `code.claude.com` redirects (PR #97)
- `CC-agent-teams-orchestration.md`: remove dead Aura Frog row; `docs.arize.com/phoenix` → `arize.com/docs/phoenix` (PR #97)
- Permanent redirects: `agentskills.io`, `docs.insforge.dev` (PR #97)

### Removed

- `CC-context-caching-patterns.md` (third-party FACT/Arcade.dev, not CC-native)
- `ci-execution/` (replaced by sessions/sandboxing/ci-remote)
- `docs/sdlc-lcm/`: SDLC/LCM specs, runbooks, OSS ALM landscape (PRs #51, #54)
- `.github/README.md`, `.github/ISSUE_TEMPLATE/`, workflow YAML headers
- `triage/status-monitor/2026-03-18-status-report.md`: redundant timestamped copy

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
