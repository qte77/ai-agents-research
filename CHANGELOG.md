<!-- markdownlint-disable MD024 no-duplicate-heading -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Types of changes**: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`

## [Unreleased]

### Changed

- `README.md`: restructured to the qte77 README canon (Hero → Badges → What → How → Why → Refs → License) — added License/Changelog/CI badges, folded the 10-row Contents table and the monitor table into `What` bullets that defer to [`docs/architecture.md`](docs/architecture.md), renamed "Related Repos" → "Refs" (links only), and trimmed local-dev into `How`. Closes #280.
- `docs/architecture.md`: corrected the stale `src/pages_build.py` reference to `scripts/pages_build.py` (the module moved this cycle).
- `src/pages_build.py` → `scripts/pages_build.py`: co-located the pure site-build module with its only consumer (`render-graph-page.py`), dropped the `sys.path` shim, and removed the now-empty `src/`. `tests/` kept at root (67 module tests unchanged); `make test` comment updated.
- `docs/sdlc-lcm/{README,agentic-sdlc-patterns,lcm-spec,sdlc-spec,multi-agent-onboarding-outlook}.md`: per-doc **legacy notes** added — RAPID is legacy (`RAPID-spec-forge` archived 2026-04-26, superseded by [qte77/qte77](https://github.com/qte77/qte77)). Flags the five docs that still presented RAPID as an active methodology, completing the partial #275 cockpit-only correction.
- `.claude/rules/read-discipline.md` + `AGENT_LEARNINGS.md`: promoted the recurring **"verify subagent findings before acting"** learning to an always-loaded rule (subagent sweeps returned false negatives 3×+ this cycle — incl. "create-new" calls on already-existing docs).
- `lychee.toml`: exclude `clarivate.com` (confirmed 403 bot-block via WebFetch, 2026-06-21) — sibling to the existing research-discovery 403 excludes (scispace/perplexity/qa.allen.ai). `marktechpost.com` 500 was transient (re-verified 200), left unchanged.

### Fixed

- `.github/scripts/build-rxiv-index.py`: `render()` no longer emits a double blank line (markdownlint MD012) when a paper has empty `extracted` metadata — consecutive blanks are collapsed before output. Regression test added (`tests/test_build_rxiv_index.py`). Closes #274.
- `docs/cc-community/CC-agent-observability-methods-analysis.md` + `lychee.toml`: repoint the dead Langtrace link (`www.langtrace.ai/` returns 404) to the canonical [Scale3-Labs/langtrace](https://github.com/Scale3-Labs/langtrace) repo and drop the `langtrace.ai` lychee exclude (the `docs.langtrace.ai` setup link still resolves). Closes #242.

### Added

- `docs/cc-community/CC-openmontage-analysis.md`: **OpenMontage** (calesthio, AGPL-3.0) — agentic video production as a `CLAUDE.md`→`AGENT_GUIDE.md` domain-controller workspace (three-layer skill architecture, runtime capability discovery, checkpoint-gated pipelines); plus a **Palmier** concepts + coding-agent→video pivot-signal note (timeline-as-MCP-workspace, control/generation-plane split). Cross-refs `CC-domain-claudemd-showcase.md`.
- `Makefile`: `setup_shellcheck` recipe (+ wired into `setup_all`) — installs shellcheck user-locally so `make check_actions` (actionlint) runs its shellcheck integration locally, matching CI's pre-installed shellcheck. Closes #185.
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: new **§7 RAG & Retrieval Infrastructure** (pipeline taxonomy; GraphRAG family — Microsoft GraphRAG / LightRAG / RAPTOR / nano-graphrag; hybrid search, RRF, ColBERT, HyDE; rerankers; vector DBs; RAG eval — RAGAs / TruLens / DeepEval) + **"Compiling Agentic Workflows into LLM Weights"** ([arXiv:2605.22502](https://arxiv.org/abs/2605.22502)) under Production Patterns. First-party-verified; star/benchmark figures hedged.
- `docs/cc-community/CC-code-tooling-landscape.md`: **cocoindex-code** (embedded AST + embeddings semantic code-search CLI + `ccc mcp` server, Apache-2.0) added as the embedded-semantic-search entry; `docs/non-cc/cocoindex-analysis.md` cocoindex-code stats refreshed (→~2.2k★, v0.2.36) + bidirectional cross-ref.
- `docs/non-cc/databricks-genie-analysis.md`: Databricks **Genie One** (agentic data coworker, GA 2026-06-16) — **Genie Ontology** authority-ranked, MCP-exposed semantic graph (Public Preview) + **Genie Agents**; first-party Databricks blog + press release; benchmark/pricing claims hedged; OKF-vs-Genie-Ontology cross-ref.
- `docs/non-cc/opennote-analysis.md`: **Opennote** (AI tutor in notes; YC S25, Llama-backed) — Feynman video lessons, Turing coding sidekick, MIT Python/TS SDKs via `opennote-dev`; pricing/user-count secondary-sourced.
- `docs/non-cc/open-knowledge-format-analysis.md`: extended — v0.1 spec precision (`okf_version`, three conformance MUST rules, strict versioning, consumer-tolerance rules), two-pass enrichment-agent detail, star count ~2.2k → ~4.5k, and a new **OKF vs Databricks Genie Ontology** comparison.
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: **Flue** stub expanded to 1.0 Beta (Durable Streams, Pi harness via `@flue/runtime`, just-bash sandbox, Cloudflare Durable Objects); the unverified "multi-agent swarms" claim corrected to subagents/task delegation. **VibeFlow** (YC S25 no-code/visual full-stack app builder) added to §3.
- `docs/non-cc/web-scraping-extraction-landscape.md`: **Magnitude** (magnitude.run, Apache-2.0) vision-first browser automation/testing added to Browser Automation, with a disambiguation note vs the separate `magnitude.dev` CLI coding agent.
- `docs/non-cc/ag-ui-protocol-landscape.md`: new **Agent Control-Surface Naming (2026)** section — command-center / HUD framing taxonomy (Devin Desktop, Omnara, flightdeckhq/flightdeck, Ralph, Vibe Kanban), the live-generative-UI positioning gap, and myth-busting on third-party "Hermes/Ralph HUD" coinages.
- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: **Instruction Adherence Patterns** (CLAUDE.md `<system-reminder>` deprioritization; conditional `<important if="…">` XML blocks; foundational-vs-conditional split; HumanLayer `improve-claude-md` skill) and **Context Engineering Workflow (ACE-FCA)** (Research→Plan→Implement, frequent intentional compaction, review-leverage hierarchy) — first-party sourced to hlyr.dev (Dex Horthy, 2026-03-17 and 2025-08-29); the previously dangling "context rot analysis" reference now resolves to the new Context Quality Degradation section.
- `docs/cc-native/context-memory/CC-extended-context-analysis.md`: **Context Quality Degradation** section (instruction budget, smart/dumb zone ~75k tokens, ~100k practitioner reset threshold, degradation signals) — sourced to hlyr.dev "Long-Context Isn't the Answer" (2026-03-23) and "Context-Efficient Backpressure" (2025-12-09).
- `docs/cc-native/agents-skills/CC-skills-adoption-analysis.md`: **`context: fork` — Mechanics and Economics** subsection (context-as-stack model, turn-boundary forking, prompt-caching economics, four CC forking mechanisms compared) — sourced to hlyr.dev "Context Forking…" (Kyle, 2026-05-15; CC v2.1.0).
- `docs/cc-native/agents-skills/CC-ralph-enhancement-research.md`: **History and Naming** section (Ralph Wiggum origin, overbaking, Cursed Lang, Desired State Loops) — sourced to hlyr.dev "A Brief History of Ralph" (Dex Horthy, 2026-01-06).
- `docs/cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md`: Pattern #8 cross-ref to the new `context: fork` section + HumanLayer human-in-the-loop approval-layer note (PermissionRequest hooks) — sourced to hlyr.dev "Skill Issue: Harness Engineering…" (2026-03-12).
- `docs/cc-community/CC-community-tooling-landscape.md`: **Token-Waste Reduction Stack** subsection — 4-layer ladder (env vars → DIY PostToolUse `run_silent()`/failFast filters → wrapper scripts (RTK) → output-style skills (caveman)) — sourced to hlyr.dev "Context-Efficient Backpressure" (2025-12-09).
- Subdirectory README one-liners refreshed (`context-memory`, `agents-skills`, `cc-community`) to surface the new sections.
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: ACE — Agentic Context Engine (Kayba, §4, Apache-2.0, arXiv:2510.04618), autoharness (Kayba, §3, benchmark-driven harness optimizer, MIT), and TimesFM (Google Research, new §6 "Specialist Models Agents Call as Tools"). (PR #262)
- `docs/cc-community/CC-community-skills-landscape.md`: agent-native skills (BuilderIO/skills, MIT, v0.2.35) — 10 composable cross-agent meta-skills as the 11th library; Summary count Ten → Eleven. (PR #263)
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: Flue (withastro, §1, Apache-2.0) — durable sandboxed agent framework on the Pi harness; plus Learn Harness Engineering and Hands-On Modern RL (WalkingLabs) under Production Patterns & Reference Frameworks. (PR #264)
- `ui/` branded GitHub Pages site: EyeRest-themed landing page (`index.html`, System/Light/Dark theme picker), restyled knowledge graph (`graph.html`), `style.css`, `favicon.svg`, vendored `vis-network` + self-hosted Inter/JetBrains Mono fonts. (PR #253)
- `.github/workflows/gh-pages.yaml`: GitHub Actions Pages deploy (Pages API); repo Pages source set to "GitHub Actions". (PR #253)
- `src/pages_build.py` + `tests/test_pages_build.py`: pure, unit-tested helpers (EyeRest restyle, tooling-node pruning, woff2 validation). (PR #253)
- `.github/scripts/lib/` pure-logic modules (`status_report`, `status_incidents`, `changelog`, `native_sources`, `community_sources`, expanded `monitor_utils`) + a stdlib `unittest` suite under `tests/` (67 tests total); `make test`. (PRs #256–#259)
- `Makefile`: `graph-page`, `graph-fonts`, `preview`, and `test` targets. (PRs #253, #256)
- `.github/workflows/rxiv-paper-eval.yaml`: fourth monitor — weekly Tuesday ArXiv preprint eval via `qte77/gha-rxiv-paper-eval@v0.2.2`, GITHUB_TOKEN-only auth posture (no PAT), outputs to `triage/rxiv/`. (PR #175)
- `.github/state/rxiv-paper-eval-state.json` + dedup step in rxiv triage job: content-hash skip keyed by `(server, year, week)` so same-params re-dispatch on a different UTC day no longer opens duplicate PRs. Closes #181. (PR #182)
- `Makefile` + `.github/workflows/lint.yaml`: actionlint v1.7.12 as third lint job; path filter widened to `.github/workflows/**` + `.github/actions/**`. (PR #182)
- `.github/actions/create-triage-pr/action.yaml`: prepends an H1 master title (new `report-title` input) and `mkdir -p` the destination dir so new monitor subdirs work on first run. (PRs #171, #182)
- Rxiv triage assembly: simulated-prepend markdownlint validation before PR creation — md-dirty output fails the job. (PR #179)
- `docs/cc-native/ci-remote/CC-github-actions-analysis.md`: **GitHub App Permission Surface** (10-scope dump) + **Auth Path Constraints** sections (all 5 `claude-code-action` auth paths are Claude-only). Closes #163. (PR #172)
- `docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md`: Friction 3 — bwrap bind-mount holds project-root config files (`CHANGELOG.md`, `README.md`, `pyproject.toml`, `Makefile`, `.claude/settings.json` — set varies by project) open via fd, blocking `git unlink(2)` on `git switch` / `git restore` / `git pull` / `gh pr merge`; recovery workaround via `git update-ref` + `git reset HEAD` + Claude Code Edit/Write tool (which uses `O_TRUNC` instead of `unlink`). Tracks anthropics/claude-code#17727
- `AGENT_LEARNINGS.md`: second learned pattern — bwrap bind-mount blocks `git unlink` on project-root config files; pointer to Friction 3
- `docs/cc-native/plugins-ecosystem/CC-office-document-skills.md`: engine-layer cross-link (dated 2026-04-26) to `qte77/doc-pipeline-engine/docs/landscape-output.md` per #131
- `docs/cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md`: engine-layer cross-link (dated 2026-04-26) to `qte77/doc-pipeline-engine/docs/landscape-ingest.md` per #132

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

### Removed

- `scripts/graphify-publish-pages.py` + the `Makefile` `graph-publish` target: superseded by `make graph-page` (render + EyeRest-restyle into committed `ui/graph.html`) and the `gh-pages.yaml` workflow. (PR #253)
- `gh-pages` branch: deleted — deploys now come from the GitHub Actions artifact. (PR #253)
- `docs/TODO.md`: GitHub issues are the authoritative roadmap; the static file duplicated CHANGELOG (Done items) and drifted from issue state (Next/Backlog). Remaining pending items migrated to #191 (research backlog tracking issue); deferred items dropped.

### Fixed

- `docs/cc-community/CC-mas-design-principles.md`: corrected the "12-Factor Agents (Selected)" section — it listed Heroku **12-Factor App** factors (config-in-env, backing services, stateless processes, dev/prod parity, logs as event streams) mislabeled as agent factors. Reconciled to HumanLayer's actual **12-Factor Agents** (Dex Horthy, 2025-04-03), folding the original App principles in as alignment notes; hlyr.dev canonical post now cited as primary alongside the GitHub mirror (accessed 2026-06-19). `docs/non-cc/agent-frameworks-infrastructure-landscape.md` 12-Factor bullet repointed to this doc + the canonical URL.
- `docs/cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md`: normalized non-canonical cross-ref path `../../../docs/cc-community/` → `../../cc-community/` (resolved correctly, so lychee never flagged it — lychee does not resolve relative Markdown paths). (PR #269)
- Monitor scripts (`community-monitor.py`, `native-sources-monitor.py`): CodeQL `py/bad-tag-filter` hardening — the `<script>`/`<style>` strip regex is now case- and trailing-whitespace-tolerant via `monitor_utils.strip_html_noise`. (PR #255)
- `Makefile` setup_lychee: tarball-wrapper-dir bug — switch to `mktemp + install -m 755` mirroring `lycheeverse/lychee-action`. Closes #160. (PRs #170, #174)
- Triage-output generators (`monitor_utils.build_report`, `changelog-compare.build_report`, `status-stats.generate_report`) + `create-triage-pr` H1 prepend: md-lint-clean output going forward; historical `triage/**/*.md` cleaned in one pass. Closes #159. (PR #171)
- `learnings-aggregator.py` + 7 mirrored `docs/learnings/per-repo/*.md`: strip upstream frontmatter, conditional H1 demotion (only when upstream has its own H1). (PR #173)
- Bump `actions/setup-node@v4 → v6`, `actions/cache@v4 → v5`, `actions/download-artifact@v4 → v8` (Node 20 deprecation; 2026-06-02 cutover). (PR #177)
- `cc-status-monitor.yaml` Collect-incidents step: convert `ARGS="..."` string to bash array (shellcheck SC2086, surfaced by actionlint). (PR #182)
- `docs/cc-community/CC-repo-to-docs-tools-landscape.md`: typo `CC-llmstxt-analysis.md` → `CC-llms-txt-analysis.md` (broken relative link regression from the URL triage batches PR); opportunistic markdownlint cleanup (MD031 / MD032 / MD040) in the same file (PR #97)
- `docs/cc-native/configuration/CC-changelog-feature-scan.md`: relative path `plugins-ecosystem/` → `../plugins-ecosystem/` (pre-existing broken internal link), resolve two permanent redirects `docs.anthropic.com/en/docs/claude-code/{hooks-guide,sdk}` → `code.claude.com/docs/en/{hooks-guide,agent-sdk/overview}` (PR #97)
- `docs/cc-native/agents-skills/CC-agent-teams-orchestration.md`: remove Aura Frog guide row + link def (external repo returned 404); resolve `docs.arize.com/phoenix` → `arize.com/docs/phoenix` permanent redirect (PR #97)
- `docs/non-cc/{hermes-agent,insforge}-analysis.md`, `docs/cc-native/plugins-ecosystem/CC-cowork-skills-api-workflows.md`: resolve permanent redirects on `agentskills.io` and `docs.insforge.dev` (PR #97)

### Changed

- `docs/non-cc/ag-ui-protocol-landscape.md` + `docs/sdlc-lcm/{multi-agent-onboarding-outlook,oss-alm-landscape}.md`: **RAPID cockpit** references corrected — RAPID (and predecessor CABIO) are **legacy** (RAPID-spec-forge archived 2026-04-26, superseded by qte77/qte77). Removed the AG-UI doc's forward-looking RAPID cross-ref; flagged the two sdlc-lcm cockpit mentions as legacy. (polyforge-/office-forge-orchestrator verified NOT to be RAPID successors.)
- `docs/cc-community/CC-office-worker-workflows.md`: **Vibe Kanban** reframed to *sunsetting* — Bloop AI shut down 2026-04-10 (repo stays Apache-2.0 at `BloopAI/vibe-kanban`, local-only; community edition under discussion); corrected stale "30K+ users / 100K+ PRs" to ~27k stars / ~2,400 PRs, and "Best-of-N" to "Attempts" (manual selection).
- `docs/cc-native/configuration/README.md`, `docs/cc-native/README.md`, `docs/cc-community/README.md`, `docs/learnings/README.md`: indexed orphaned docs surfaced by the full-repo doc-hierarchy audit — 6 configuration docs (subdir count 9 → 14), CC-vlm-screen-sharing-landscape, and 4 auto-aggregated AGENT_LEARNINGS mirrors. (PR #269)
- `docs/cc-community/CC-code-tooling-landscape.md`: refreshed codebase-memory-mcp entry — docs-site link, stars 3.2K → 6.8K, v0.7.0 → v0.8.1; frontmatter dates bumped. (PRs #262, #265)
- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: refreshed against current code.claude.com/docs/en/memory — `autoMemoryDirectory` + v2.1.59 requirement, MEMORY.md 25 KB / 200-line threshold, `CLAUDE_CODE_NEW_INIT`, AGENTS.md handling, `claudeMd` managed-settings key. (PR #265)
- `lychee.toml`: added `theregister.com` to the exclude list (intermittent anti-bot 403 in CI). (PR #264)
- `docs/cc-community/README.md`: skills-landscape index row updated to 11 libraries (added last30days, agent-native). (PR #267)
- GitHub Pages now deploys via the Actions workflow instead of a `gh-pages` branch push; the published knowledge graph prunes tooling/code nodes (`scripts/`, `tests/`, `ui/`, `src/`, `.github/scripts/`). (PR #253)
- `.github/scripts/` monitors (status, changelog, native-sources, community) refactored to thin IO entry points with pure logic extracted to importable `.github/scripts/lib/` modules — behavior-preserving (`status-stats` + `changelog-compare` output byte-identical on fixtures). (PRs #256–#259)
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
