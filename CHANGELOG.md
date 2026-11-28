<!-- markdownlint-disable MD024 no-duplicate-heading -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Types of changes**: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`

<!-- scriv-insert-here -->

## [0.29.0] - 2026-11-28

### Added

- Graph databases doc: "Higher-order and layered relationships" section (n-ary data models, multilayer and temporal pointers, HyperNetX, XGI, pymnet, HyperGraphDB, `caviri/rete`); replaced the unchecked-hyperedge note (plan 0018 N67).

- `docs/sdlc-lcm/github-platform-capabilities-analysis.md`: GitHub platform map (Actions, Codespaces and dev containers, rulesets and enforcement, organization and enterprise features, agent surfaces) with plan tiers read from GitHub's docs (plan 0018 N68).

- `docs/sdlc-lcm/code-forge-ci-alternatives-landscape.md`: dated landscape of code forges, CI/CD systems and GitHub Actions runner services that compete with GitHub, with licence, agent surface and migration path per row; vendor speed and price claims marked (plan 0018 N69).

- Frameworks landscape: Hindsight agent memory, Docker Agent, Pydantic AI Coder and Pax beta with a practitioner write-up, and an *Agentic GraphRAG* book pointer (plan 0018 N70).

- Plan 0018 N71: shadow-comparison migration validation (Anthropic's Rust migration, GitHub Scientist) in the legacy migration doc; GUARD and Self-Improvement Memory in the Weco recursive self-improvement doc; the over-edit study in the evaluation metrics landscape; `awslabs/codekb` in the repo-to-docs landscape.

- Micro and small language models landscape (`docs/non-cc/reference/micro-language-models-landscape.md`): μLM paper (arXiv 2604.19642), SPREAD Nemotron as a vendor claim, llama2.c, a bare-metal assembly OS experiment (plan 0018 N72).

- Agent and connector sources (plan 0018 N73): n8n Nod in the computer-use landscape, the Hugging Face PyBot swarm report in the orchestrators landscape, an OpenResearch shared-project example, PandaDoc's Claude connector in the connectors overview, and IBM Bob in the IBM agent stack analysis.

- Coding agents comparison: "Where media is processed" section (local resize and PDF steps per harness read at release tags, model-side input types, GPT-6.2 Astra has no video input) (plan 0018 N74).

- Cross-Harness Matrix: seven capability rows (instruction and memory files, skills, plugins, subagents, MCP configuration, headless and CI, cloud and remote runs) for Claude Code, Codex CLI, Gemini CLI, OpenCode and Pi, read from vendor docs 2026-11-27 (plan 0018 N75).

- Cross-Harness Matrix: second table with GitHub Copilot CLI, VS Code Copilot Chat, Cursor, Cline, Aider, Amp and Windsurf (Devin Desktop) for all 13 mechanics, read from vendor docs 2026-11-27 (plan 0018 N78).

- Coding agents comparison: "Configuration and policy by harness" section (settings files and precedence, environment variables, managed or enterprise policy, project overrides and instruction files for Claude Code and ten other harnesses, from vendor docs) (plan 0018 N80).

- `docs/sdlc-lcm/code-forge-ci-alternatives-landscape.md`: new § Capability map across forges, comparing GitHub, GitLab, Codeberg/Forgejo, Gitea, Bitbucket Cloud and Azure DevOps across 16 capabilities (CI, runners, merge queues, protection, scanning, packages, SSO, audit, MCP, vendor agents) with plan tiers and "not documented" markers (plan 0018 N81).

- `docs/sdlc-lcm/distributed-systems-concepts-landscape.md`: distributed systems concept map for agent systems (fallacies, paper timeline, borders, contracts, communication, layers, topologies, patterns), with secondary-only claims labelled (plan 0018 N82).

- `docs/sdlc-lcm/test-eval-driven-development-landscape.md`: comparison of TDD, BDD, property-based testing and eval-driven development with the EDDOps paper, LangChain and Airbnb practice, and a tripwire section (mutation testing, RED-first, guardrail tripwires); links existing EDD coverage (plan 0018 N83).

- `docs/sdlc-lcm/privacy-law-touchpoints-landscape.md`: requirements map of EU GDPR, UK GDPR, CCPA/CPRA and PIPEDA with KB touchpoints and interactions; Quebec Law 25 and Bill C-27 status marked unverified where first-party pages could not be read (plan 0018 N84).

- Meta-levels table in the Weco AIDE² analysis: MAML, learned optimizers, OPRO, Promptbreeder, TextGrad, DSPy, AlphaEvolve, AFlow, ADAS, STOP, Gödel Agent and Darwin Gödel Machine, each from its abstract page; cross-references from the MOSS and skill-evolution docs (plan 0018 N85).

- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: "Diverge and converge" section (Double Diamond framing, how agent harnesses widen then narrow, table linking ten places in the knowledge base) (plan 0018 N86).

- `docs/non-cc/coding-agents/coding-agents-comparison-landscape.md`: "Prompt-to-app builders" section covering Lovable, Bolt.new, v0 and Replit from vendor docs, plus notes on bolt.diy, the Firebase Studio sunset and HeyBoss (plan 0018 N88).

### Changed

- Plan 0018 opened (hypergraphs and layered graphs, GitHub platform and alternatives, 2026-11-27 sources); plan 0017 superseded, its open owner rows moved over unchanged.

- CONTRIBUTING: volatile claims (counts, stars, versions, prices, GA or beta status, availability, benchmark numbers) carry one inline read date, `(read YYYY-MM-DD)`; `validated_links_on` stays link liveness only; the research lane brief uses the same form (plan 0016 N41, owner 2026-11-27).

- Definition sources for knowledge graph (Hogan et al.), hyperedge (HyperNetX docs) and a HybridRAG row distinct from hybrid search (Sarmah et al.) (plan 0018 N77).

- `docs/non-cc/frameworks/workflow-frameworks-landscape.md`: checkpoint and resume matrix gains GitHub Copilot CLI, VS Code Copilot Chat, Cursor, Cline, Aider, Amp and Windsurf rows; Codex CLI, Gemini CLI and OpenCode rows re-checked at vendor docs and release-tag source (plan 0018 N79).

- Link check: Box legal and pricing pages and Snowflake's legal pages are excluded (403 to lychee; verified live with polyfetch, owner OK 2026-11-27), so the enterprise data-API table now links them instead of citing plain-text URLs.

## [0.28.0] - 2026-11-27

### Added

- Feasibility study (plan 0017 N66): running the doc-link graph over a document management system (SharePoint and OneDrive, Google Drive, Box, Confluence, Nextcloud, OpenCloud), with listing, link-extraction and auth per store, existing products, an adapter sketch for `doc_graph.py`, a recommendation and an effort estimate.

- `agentic-enterprise-os-landscape.md` § Enterprise data APIs for agents: auth model, licence or plan, unattended access, terms on automation or AI, and official MCP server for Microsoft Graph and Copilot APIs, Google Workspace, Salesforce, Databricks, AWS, Google Cloud, Atlassian, Slack, ServiceNow, Snowflake, Box, Notion, SAP, Workday, OpenCloud and Nextcloud, each cell from the vendor's own pages or marked unverified (plan 0017 N65).

### Changed

- Doc graph: physics slows down and stops instead of halting abruptly, docs cluster more closely around their topic hub, and the Colour by, Filters and a new separate Updated panel start closed (plan 0016 N58).

- Plan 0017 opens for doc-graph focus, kit colours and encoding, harness subscriptions, Microsoft 365 Copilot APIs, an enterprise data-API table and a document-management graph study; plan 0016 is superseded and its open rows move to it.

- Doc-graph and index page colours now come from an unedited copy of the EyeRest brand kit (`ui/eyerest.css`, kit 0.5.0), pinned by a sha256 test; the graph folder colours use the kit's data tokens and `style.css` no longer defines colours (plan 0017 N59).

- Doc graph: clicking or tapping a doc keeps it and its linked docs coloured and dims the rest (clicking empty space clears it, and search dimming still applies); edges use one colour and fade when zoomed out, and a selected doc's own edges stay highlighted (plan 0017 N60).

- Harness subscriptions (plan 0017 N64a): Copilot CLI Microsoft Entra sign-in, OpenCode on Copilot plans, Claude and Codex agents on a Copilot plan, unofficial Copilot-subscription proxies, and two Claude Code patterns (Remote Control is subscription-only; a gateway credential replaces the subscription login).

- Microsoft 365 Copilot analysis: Graph Copilot APIs subsection (endpoint table, Chat API limits, absences, four ways to use the licence from outside, API terms 3(b)(12), (13) and (18)) and a corrected Chat API permissions label (plan 0017 N64b).

- Idle compaction in `CC-prompt-caching-behavior.md`: add changelog entries 2.1.326 and 2.1.332, and rewrite the note on why idle compaction did not fire before the long gaps, with a stopped-host explanation marked as inference (plan 0017 N64c).

- Refreshed 18 `docs/sdlc-lcm/` docs against first-party sources: corrected stale versions, counts and attributions (for example the Artificial Analysis index v2.1, Claude Code AGENTS.md fallback, MAESTRO attribution) and marked unsourced claims unverified (plan 0016 N61, R1).

- Refreshed 17 `docs/cc-community/` analyses against first-party sources: current star counts, versions and licences, corrected stale claims (Ultraplan removal, multi-account `CLAUDE_CONFIG_DIR` docs, Gmail connector send, vision token formula), and marked unsourced figures as unverified (plan 0016 N61, lane R2).

- Refresh 23 `docs/cc-native` docs (top level, agents-skills, ci-remote, context-memory, model-internals) against first-party sources: renamed or moved docs URLs, removed Ultraplan, updated hook, permission, network, caching and skill-budget facts, and re-dated star and release counts.

- Refreshed 19 `docs/cc-native/configuration/` and `docs/cc-native/sandboxing/` docs against first-party sources: corrected stale versions, availability, prices, repository figures and issue states, and marked unsourced claims unverified (plan 0016 N61, R4).

- Refreshed 20 `docs/cc-native/plugins-ecosystem/` and `docs/cc-native/sessions/` docs against first-party sources: corrected stale counts, versions, plan lists and renamed commands (for example `claude purge`, `claude --cloud`, Firecrawl pricing, fast-mode models) and marked unsourced claims unverified (plan 0016 N61, R5).

- Refreshed 35 `docs/non-cc/` docs (agents, orchestrators, protocols, reference) against first-party sources: updated versions, star counts, prices, repo moves and model rosters, and marked claims no longer found at source unverified (plan 0016 N61, R6).

- Refreshed 37 `docs/non-cc/coding-agents/` and `docs/non-cc/frameworks/` docs against first-party sources: updated versions, star counts, pricing and plan tiers, model lists and vendor renames (for example Amp modes, Codebuff shutdown notice, Cursor and Trae pricing), and marked unsourced claims unverified (plan 0016 N61, R7).

- Refreshed 35 `docs/non-cc/` docs (context-memory, infrastructure, knowledge-management) against first-party sources: updated versions, star counts, prices and repo moves (for example OpenViking's architecture and retrieval, the Opennote sunset, FastContext's withdrawn paper, KV-cache pricing) and marked unsourced claims unverified (plan 0016 N61, R8).

- Refresh follow-ups (plan 0016 N61): MAESTRO attributed to the Cloud Security Alliance, MITRE ATLAS counts updated, the German wiki incident claims sourced to the paper abstract, canonical URLs for Gemini, Air, Codex and Claude Code docs, SAP MCP status, the hooks event list pointer, the spec-driven framework snapshots, and two `purpose` lines aligned with their bodies.

- Doc graph: doc size follows its link count (square-root scale); "Colour by" gains "age" (oldest `--border` to newest `--primary`, undated docs muted; in this mode search and focus dim by fading, since `--border` is the oldest colour); the timeline panel switches between Updated and Added, and the age colours follow the chosen date (plan 0017 N63).

## [0.27.0] - 2026-11-25

### Added

- `CC-connectors-overview.md` § Public Connectors Directory: the directory's counts and filters as read on 2026-11-25, what the Anthropic verified label means per Anthropic's verification page, and a ten-row table of well-known entries checked at their own directory pages (plan 0016 N42).

- `agentic-engineering-disciplines-landscape.md` § Four rings: prompt, context, harness and loop engineering as a simplified nested picture (Shittu Olumide's diagram), with the contested outermost layer and the academic progression (arXiv 2608.21884, 2606.20683); the loop-engineering section cites the 217-repository study; glossary row and context/harness hub rows (plan 0016 N57).

### Changed

- `scripts/cc_cache_usage.py` counts a turn as a cache miss when it writes again part of the prefix the previous turn had cached (the rule credited to cachemiss), not when it writes more than it reads; `CC-prompt-caching-behavior.md` explains how to run it, and `CC-usage-tooling-landscape.md` points to the hit/miss coverage (plan 0016 N55).

## [0.26.0] - 2026-11-25

### Added

- Bundled `/claude-api` skill: what it is, folder layout (`shared/` 64 files), subcommands, observed on-disk unpack behaviour (not documented) and its own "cached tables" caveat, in `CC-skills-adoption-analysis.md`, with a pointer from `CC-changelog-feature-scan.md` (plan 0016 N50).

- KV-cache serving landscape: cache-timing audits and attacks, KV-cache reconstruction defences, vendor cache isolation, and local cache persistence with open weights (plan 0016 N53).

- `scripts/cc_cache_usage.py`: a stdlib report of one Claude Code session's prompt-cache usage from its transcript (cache reads and writes by lifetime, rewrites after idle gaps, a hit/miss prediction checked against the outcome, compaction markers), with unit tests (plan 0016 N54).

### Changed

- Prompt caching: idle-compaction wording (about 54 minutes vs about an hour, resume does not compact, needs a running session), a second one-session measurement, cost-lever evidence by level, stopped-host options, hit/miss prediction and a claims-checked table (plan 0016 N51, N52).

## [0.25.0] - 2026-11-25

### Added

- Surrogate-harness training for RLM harnesses (arXiv 2611.28298) in the Prime Agent analysis with a cross-reference from the programmatic tool calling analysis; EGGROLL and chat-data.com as dated lines in the agent frameworks landscape (plan 0016 N35, N39).

- Agent tools (plan 0016 N36): T3 Code column and note in the remote-access landscape, a `vercel/board` section in the cross-session messaging analysis, OntoBricks and a Kumo Engine pointer in the semantic-layers landscape, linked from the Genie analysis.

- `make kb-papers` exports the arXiv papers cited in `docs/` but missing from the rxiv feed to `triage/kb-papers/arxiv-kb.jsonl` (arXiv API metadata, paperverse JSONL schema; plan 0016 N37).

- Firecrawl hosted connector route (ChatGPT plugin, Claude directory connector, hosted MCP with OAuth) in the CC web-scraping plugins analysis, and Alexandria provider-count figures reconciled by source and date in the web-scraping landscape.

- Plan 0016 (`docs/plans/2026-11-24-0016-graph-ui-sources-paperverse-feed.md`, #1071): doc-graph page facets and timeline, the 2026-11-24 sources, the KB papers export and the paperverse sync fix, run as parallel worktree lanes; plan 0015 superseded, its open rows moved over unchanged.

- shrink-anything (dead-code and unused-dependency remover that keeps a cut only if your own tests pass) added next to fast-anything in the CC community tooling landscape (plan 0016 N46).

- Workflow landscape: Prefect, Dagster and Apache Airflow with their AI/agent surfaces (MCP servers, agent skills, LLM providers), and a Kaval.AI entry in the agent-frameworks catalog (plan 0016 N47).

- CC community skills landscape: scottduncanai/pid-to-knowledge-graph, a Claude skill that builds a process knowledge graph from piping and instrumentation diagram (P&ID) PDFs (plan 0016 N48).

### Changed

- Doc graph page: filter chips with counts (status, doc type, platform), a details panel on node click, a "recently updated" timeline, a folder or topic-hub colour mode, hub-edge clustering with physics that stops once the layout settles, and docs in no hub hidden until ticked; graph nodes now carry `purpose`, `created` and `updated`.

- Site start page (`ui/index.html`): current doc conventions, status rings and scheduled workflows; topic hubs and glossary cards.

- Doc graph: the hub index star sits fixed at the centre; the details panel labels hubs and folder indexes, shows a hub's intro and doc count, fills missing dates from git history (the Pages build now checks out full history) and hides empty rows; physics runs gently for 2 s after layout and each filter change, then stops; the start page is now a redirect to the graph, and the header links to the GitHub README (plan 0016 N44).

- Doc graph: topic clusters are softer (hubs move with their docs, wider overlapping clouds, weaker springs; physics still stops after 1 s); the timeline offers full history (weekly bars) next to the last 90 days; "Colour by" and "Filters" are collapsible panels (plan 0016 N49).

### Fixed

- Doc graph: topic hubs are fixed on a ring around the hub index and each doc is seeded near its first checked hub, so clusters show from the first frame; central gravity is on, physics runs for 1 s after load and after each filter change, then stops, and the view re-fits (plan 0016 N45).

## [0.24.0] - 2026-11-24

### Added

- `microsoft-365-copilot-analysis.md`: Autopilot Learn page (preview), Copilot UX components with SharePoint Framework `.sppkg` packaging (GA 2026-10-28), the plugin-versus-app extensibility framing, one Frontier item, and refreshed Frontier links (plan 0015 N8)

- GEPA (reflective, Pareto-based prompt and text optimizer, paper arXiv:2507.19457) entry next to DSPy in the agent-frameworks landscape, with its DSPy relationship and dated first-party figures

- SlopCodeBench erosion and verbosity metrics (checkpoint-based code-degradation benchmark) in the agent evaluation metrics landscape

- `agentic-ai-vulnerability-landscape.md`: the lethal trifecta (Simon Willison, 2025-06-16) as a defense row, linked to the Supabase MCP case; lead from the ai-that-works triage (plan 0015 N9)

- Harness patterns: practitioner-talk additions (proof before research, questions-then-blind research, back pressure per loop, MCP vs first-party rule and token-cost measurement, tool-result shape, speculative reads), labelled single-source (plan 0015 N9)

- `agent-evaluation-metrics-landscape.md`: practitioner eval practices from ai-that-works episodes, all labelled single-source (model-swap relative gate with repeats and no default price, runtime invariant checks, scenario tests with soft metrics, SlopCodeBench-author slop patterns) (plan 0015 N9)

- Concepts from the ai-that-works show, labelled as single-source practitioner claims: memory pipeline split by learning source (`CC-memory-system-analysis.md`), information-not-instructions rule for skills (`CC-skills-adoption-analysis.md`), instrument-before-the-bug observability stance with an OpenTelemetry attribute-type caveat (`agent-observability-methods-analysis.md`), separate projections of an event log (`mas-design-principles.md`) (plan 0015 N9)

- Agentic-systems guides folded in: context failure modes with two primary papers (`CC-extended-context-analysis.md`), a rollout-and-governance section from a Databricks guide (`agentic-engineering-disciplines-landscape.md`) and the guided-waterfall supervisor pattern (`mas-design-principles.md`), each labelled by evidence level

- `CC-extended-context-analysis.md`: how the auto-compact window and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` combine (they stack: trigger ≈ window × percentage), when `/autocompact` first appeared (v2.1.221 floor; first changelog mention v2.1.234), Anthropic's session-management article and a community guide as related reading

- `goal-tracking-attribution-landscape.md`: "Core vs context: classifying work (Moore)" section (quadrants and actions per a slide-deck summary of *Dealing with Darwin*, single-source AI-angle essay, work-item classification how-to as corpus synthesis, adjacent concepts) (read 2026-11-23)

- Lindenberg newsletter lenses (labelled practitioner, single-source) with first-party checks: Atuin Agent Threads and CortexDB supersession in `CC-memory-tooling-landscape.md`, NVIDIA NeMo Switchyard in `CC-harnessrouter-analysis.md`, last-green-ref pattern after Scion in `software-factory-landscape.md`, dual-run rollout in `system-1-decision-models-landscape.md`, join-key checks in `semantic-layers-data-catalog-landscape.md`, and the own-history searcher test in `CC-code-tooling-landscape.md`

- LiteLLM Lens (early access): trace service and a private-preview CLI that compares harness × model configurations, in `llm-routers-gateways-landscape.md`, with a pointer from the harness-benchmarking method in `agent-evaluation-metrics-landscape.md`

- `agentic-engineering-disciplines-landscape.md`: "Loop engineering in practice" subsection (Anthropic first-party loop types, anatomy, stop conditions, maker/checker, budgets, vendor-cluster provenance with per-source stakes); loop-engineering row corrected (earliest dated use: Osmani 2026-06-07); Lindenberg design lenses for pointable work and the code/cognitive/intent debt split (Storey, Thoughtworks Radar, Osmani)

- Topic hub `docs/_topics/model-internals.md` (interpretability and hidden-state docs); every content doc now sits in a hub, so the unhubbed ratchet `MAX_UNHUBBED` drops from 3 to 0 (plan 0015 X2b)

- `CC-prompt-caching-behavior.md`: preserved-thinking subsection (supported models, model/account binding, drop behaviour and cache cost, owner observation of the cross-organization notice in CC v2.1.330) (read 2026-11-23)

- Dated, hedged entries for mobile-agent-testers and fast-anything (new Claude Code plugins) in `CC-community-tooling-landscape.md`, and OpenComputer (open-source Devin alternative) in `devin-cli-analysis.md`

- `computer-use-agents-landscape.md`: app bridges instead of screens: MCP for Blender, Bonsai (IFC/BIM add-on for Blender) and two community Bonsai MCP bridges, plus the IFC-MCQ benchmark; hub row in `agentic-web.md`.

- `/tui` row in `CC-tools-inventory.md` (fullscreen vs classic renderer, `/tui classic` since v2.1.327, the failed-start fallback since v2.1.236) and a `CLAUDE_CODE_NO_FLICKER` row in `CC-env-vars-reference.md`.

- Doc graph (`ui/doc-graph.json`): each doc now carries clustering facets: `status`, `doc_type` (from the filename suffix) and `platforms` (from `platform_scope`, or `claude-code` for `cc-native/` and `cc-community/` docs without one); tests first. The page does not filter on them yet.

- `docs/schema/frontmatter.schema.json` (JSON Schema 2020-12): the single source of the content-doc frontmatter rules, with each key's RDF term (`x-rdf`, e.g. `updated` → `dcterms:modified`); `doc_frontmatter.py` and `doc_status.py` read it via `lib/frontmatter_schema.py` (tests first, including one that every rule in the schema is enforced); CONTRIBUTING §1 links to it instead of restating it. An empty `title` is now flagged.

### Changed

- Paper triage pins `qte77/gha-rxiv-paper-eval` v0.7.0: an unparseable extraction reply gets one retry, and the run summary reports the extraction parse-failure count (plan 0015 13-A9)

- Paper triage pins `qte77/gha-rxiv-paper-eval` v0.7.1: a paper whose extraction retry call fails still counts in the parse-failure line (plan 0015 13-A9)

- `CC-official-plugins-landscape.md` § Security Guidance rewritten for plugin v2.0.21 from its own README, `hooks.json` and hook script: post-edit pattern warnings (not a blocking `PreToolUse` hook), an LLM diff review on Stop, an agentic commit and push review, the per-prompt `UserPromptSubmit` git baseline, credentials, cost log and environment switches; fit is now pattern warnings on, LLM reviews per repo (plan 0015 N10)

- `CC-agentic-harness-patterns-analysis.md`: HumanLayer's current status, dated 2026-11-22 (the approval-gate SDK has had no PyPI release since 2025-06; the product now runs coding agents for teams), with a Sources row; the SDK mentions in `mas-design-principles.md`, `agent-identity-auth-landscape.md` and `software-factory-landscape.md` now say so (plan 0015 N9)

- `CC-official-plugins-landscape.md`: pruned one community-guide entry (Cuttlesoft blog post) to a Not included table under the well-known, performance-optimised rule (plan 0015 P2)

- Pruned the agent skill evolution landscape under the pruning rule: moved three paper-only entries (WikiSkill, AutoTailor, Skill++) to Not included; kept SkillLift, NVlabs/Skill2Env and Adaptive Skill Granularity, whose paper names its code repo (fact check 2026-11-22); SkillLift's star count and last push refreshed

- Agentic database access landscape: pruned under the D8 rule (DualSQL moved to Not included, no code or weights released; all database MCP servers, benchmarks, BIRD-RL and OpenLineage kept) (plan 0015 P2)

- KV-cache serving landscape checked under the pruning rule: nothing moved; FlashRT and kvcached star counts refreshed, and UltraQuant's code status corrected (its paper says the Ultra-TQ kernel is upstreamed in vLLM; the FP4 kernel release is planned)

- `semantic-layers-data-catalog-landscape.md`: moved MQO-MCP and the three paper-only self-evolving-ontology entries (OaK, SciToolAgent-Evo, Evo-DKD) to Not included under the well-known, performance-optimised rule; corrected the AtScale homepage status (plan 0015 P2)

- Pruned the repo-to-docs tools landscape under the pruning rule: moved GitSummarize to Not included (466 stars, last push 2025-04-03); kept DeepWiki, Code2Tutorial, Understand Anything, OpenWiki and OpenKB

- `agent-code-analysis-landscape.md`: Grim Prompter and VulnAgent-R2 moved to Not included under the pruning rule; agent-audit (reproducible first-party benchmark) and VIPER-MCP (artifact package released with the paper) kept after fact-check; agent-audit licence recorded as MIT (plan 0015 P2)

- Agent evaluation metrics landscape checked under the pruning rule: nothing moved; Tracely's link and facts corrected (its original repo is live again with 1,122 stars; a separate copy has 848)

- Review fixes after plan 0015's P2 sweep: the security-guidance section's local timing figures are relabelled as another session's unconfirmed report; the lane and falsifier briefs require searching a paper's HTML or PDF for code, checking every copy of a repo and stating only what was read (with an `AGENT_LEARNINGS.md` entry); plan rows 13-A7 and 13-A9 show their owner and data gates

- `agent-design-formats-landscape.md`: star counts, DESIGN.md file count, Figma MCP server name and beta scope, DTCG 2025.10 date and Style Dictionary v5.8.0 re-checked at source on 2026-11-22 (plan 0015 R1)

- `goal-tracking-attribution-landscape.md`: Jira Align link moved to its current URL; Tability's agent check-ins and MCP server added from its own pages, checked 2026-11-22 (plan 0015 R1)

- `kv-cache-serving-landscape.md`: H2O and KVQuant marked as dated research concepts, with their reference repos and last-push dates (`gh api`, 2026-11-22) (plan 0015 R1)

- `repo-to-docs-tools-landscape.md`: Understand Anything, OpenWiki and OpenKB star counts and OpenWiki v0.9.0 re-checked with `gh api` on 2026-11-22 (plan 0015 R1)

- `agent-code-analysis-landscape.md`: Specula is now Specular (`specular-org/Specular`); repo link, star count and its arXiv:2607.25333 paper added; rename noted in `agentic-engineering-disciplines-landscape.md` (plan 0015 R1)

- `CC-mods-function-hooks-analysis.md`: built-in mods list updated with `cc-plugin-easel` (documented) and `cc-plugin-privacy` (observed, source README read), new `mods/` directory contents incl. `hipaa-default`; `CC-skills-adoption-analysis.md`: new subsection on skills and plugins synced from claude.ai (opt-out settings, cadence, `CLAUDE_CODE_SYNC_SKILLS`, namespace reservation and its revert, per-skill list display), read 2026-11-23

- Coding-agents comparison: context compaction by harness (auto trigger, manual command, setting names) and a subscription sign-in subsection (vendor terms wording, limits, data handling) under model access and billing

- `make check_frontmatter` now requires `purpose` to be one non-empty line of at most 200 characters (tests first); 59 docs' purposes shortened, with any fact not already in the body moved to the `**Details:**` line; CONTRIBUTING §1 states the limit.

- `microsoft-365-copilot-analysis.md`: the 2026-12-09 change to the EU/EFTA/UK Anthropic subprocessor setting (tenants with no selection move to "All users"), from the Microsoft Learn page dated 2026-11-20; follows the M365 drift report (#1037).

- `CC-models-reference.md`, `CC-advisor-tool-analysis.md`, `CC-prompt-caching-behavior.md`, `CC-cowork-skills-api-workflows.md`: Fable 5.2 / Opus 5.5 / Sonnet 5.5 release and retirement dates, default effort, Fable 5.2 breaking changes (prefix check, thinking-block binding, `computer_20251124`, advisor pairing), Fable/Mythos verification programs and Opus 4.8 / Opus 5 fallback routing, deprecations, the 0.025x cache-read multiplier and 512-token minimum for Fable 5.2 / Mythos 5.2, the announcement's canonical URL; claude.ai file-creation settings (read 2026-11-23)
- `kv-cache-serving-landscape.md`: Anthropic 512-token minimum list brought up to date; stale Bedrock 1,024 note and "5-min tier only" claim replaced with pointers to the corrected caching doc

- `CC-model-provider-configuration.md`, `CC-models-reference.md`: provider facts consolidated into the provider-configuration doc (free-tier table moved with four rows re-checked at source, 2026-11-23; the models doc keeps a pointer under the same heading); Infomaniak section refreshed from the vendor's models and prices pages (current model ids, CHF prices, vendor-claim labels, third-party catalog noted)
- `codex-cli-analysis.md`, `gemini-cli-analysis.md`: new Providers sections from each vendor's docs (Codex `model_providers`, Azure, built-in Bedrock and Google Cloud providers, Responses-API requirement; Gemini CLI Vertex AI, API key and base-URL overrides, no documented OpenAI-compatible, Azure or Bedrock route)

- Refreshed CLI-Anything (stars, v0.4.0 release, CLI-Hub registry counts) and Trail-code (stars, README claims, version) facts

- `semantic-layers-data-catalog-landscape.md` § Formal Ontologies & Semantic Web now covers RDFS (RDF Schema 1.1), which the glossary row already pointed to; `docs/learnings/README.md` uses `purpose:` instead of `description:`.

- `lychee.toml`: exclude `pdma.org`, which returns 403 to lychee in CI and locally while the page is live (owner OK, 2026-11-24).

- `platform_scope` now takes only harness and agent-host slugs from the list in `docs/schema/frontmatter.schema.json`, as an inline list (tests first); synonyms merged (`codex-cli`/`openai-codex` → `codex`, `copilot`/`github-copilot-cli` → `github-copilot`); in 34 docs, editors, surfaces, operating systems, channels, clouds and providers moved to the `**Details:**` line, and 12 docs with no harness left dropped the key.

- `docs/schema/frontmatter.schema.json`: each `status` value now has its own RDF mapping (`x-rdf-values`): the rings adopt/trial/assess/hold as a `schema:reviewRating` of 4 to 1, `research` and `reference` as `dcterms:type`, `archived` as `schema:creativeWorkStatus`; `validated_links_on` maps approximately to `schema:lastReviewed` (tests first).

- Frontmatter key `validated_links` renamed to `validated_links_on` (owner 2026-11-24) in the schema file, 264 docs, the learnings aggregator, CONTRIBUTING and the add-source skill; the old key now fails the check with a pointer to the schema.

### Removed

- Community monitor: the Reddit and X sources, their fetchers and the three secret mappings in the workflow; they never ran because the secrets were unset (owner decision 2026-11-23, plan row 13-O11, #726)

## [0.23.0] - 2026-11-22

### Added

- Claude Code stop-hook loop cap: `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` (default 8, `0` disables) and `stop_hook_active` in `CC-hooks-system-analysis.md`, with an env-var row (owner observation 2026-11-20)

- Agent management: new `CC-managed-settings-fleet-analysis.md` (managed-settings delivery channels, ranking, Enterprise group configs, fail-closed startup, managed-only keys, verification), a cost-attribution section in `CC-monitoring-telemetry-analysis.md` with two `OTEL_*` env-var rows, and an agent-registries comparison (A2A Agent Card, MCP Registry, AWS, Google, Agent 365, Agentforce) in `agentic-enterprise-os-landscape.md` (plan 0014 K15)

- Five pointer-only topic hubs: evals and benchmarks, security, data, agentic web, and agent management, registered in the hub index and CONTRIBUTING (plan 0014 K24)

- Microsoft 365 Copilot vs Salesforce Agentforce 360 comparison table and a worked list-price example (re-checked 2026-11-20) in the agentic enterprise OS landscape (plan 0014 K25)

- AWS and Google Cloud agent-stack analyses (AgentCore, Agents Classic, Quick; Gemini Enterprise Agent Platform, Agent Identity, Gemini Enterprise seats): services, least-privilege roles, IdP integration, licences, regions, dated status, no prices (plan 0014 K34)

- Cloud agent stacks: Microsoft Foundry "Roles, identity and licences" with an at-a-glance table, a new Oracle Cloud agent stack analysis (OCI Generative AI Agents, Enterprise AI Agents, AI Agent Studio), and a Copilot SDK section in the Copilot CLI doc (plan 0014 K34)

- Cloud agent stacks: new `ibm-agent-stack-analysis.md` (watsonx Orchestrate and ADK: Claude via Bedrock preview, MCP/A2A, MAU-based plans) and `alibaba-cloud-agent-stack-analysis.md` (Model Studio, AgentRun, AgentBay, Qwen-Agent: RAM policies, Agent Identity, seat-based Token Plan; no Claude found), with IAM role gaps marked unverified (plan 0014 K34)

- `cloud-agent-platforms-landscape.md`: six cloud agent stacks (AWS, Google Cloud, Azure, Oracle, IBM, Alibaba Cloud) compared in one dated table — runtime, Claude availability, MCP/A2A, memory, agent identity, least-privilege roles, licence models, regions, release status; no prices (plan 0014 K34)

- Claude Duet, OpenAI dots and Cue (Manus) rows in the Always-on Teammate Agents table of the Hermes analysis (plan 0014 K40)

- Fold-ins from owner names: Anthropic's components-of-agent-memory post (CC memory doc), hypergraph-vs-graph evidence (frameworks doc), Hermes memory design vs Claude Code and § 4 plus an always-on teammate-agent peer table (Grok Bot, Muse, Rakazo, OpenMausBot, Tucano), an OpenBot refresh, and refreshed Hermes counts (plan 0014 K40)

- Fold-ins from owner names: TrustGraph (ontology-runtime row) and selfgraph (HydraDB companion SDK) in the frameworks landscape, Cursor's pstack plugin in the CC community skills landscape, Qodo's auto-approval and agent-session review in the PR-review landscape, and the "Society of AI Scientists" preprint in the research-agents landscape (alphaXiv only, no arXiv ID found); city2graph dropped as geospatial with no agent angle (plan 0014 K41)

- `docs/glossary.md`: where each recurring term and abbreviation is defined (term, expansion, owner section; no definitions), linked from the topic-hub index and a new CONTRIBUTING anti-pattern; the source-adding skill now checks it before defining a term (plan 0015 C1, owner decision D7)

- `make check_coverage` checks that content docs expand each glossary abbreviation they use, or link `docs/glossary.md` (plan 0015 C2)

- `make check_frontmatter` (new CI job "Doc frontmatter", lenient): checks content docs against the CONTRIBUTING §1–§2 schema (required keys, ISO dates, keys that left frontmatter, unknown keys, lifecycle-only `status`, one URL in `source:`) and reports without failing until the F3 migration (plan 0015 F2)

- Knowledge-management topic hub (`docs/_topics/knowledge-management.md`) linking wikis, LLM-maintained knowledge bases, knowledge-organisation methods and enterprise knowledge layers (plan 0015 T2)

- Knowledge-management: new `knowledge-organisation-methods-landscape.md` (MOC, backlinks, Zettelkasten, PARA, Diátaxis, Obsidian, frontmatter schemas compared), refreshed Karpathy KB counts and gap analysis, fixed broken anchors and Sources table in `repo-to-docs-tools-landscape.md`, Onyx facts re-checked (plan 0015 T2)

- `make check_coverage` (new CI job "Doc coverage"): every content doc must be linked from its folder's README index and from at least one other doc or repo-root file; CONTRIBUTING § Index maintenance now states the rule for all folders (plan 0015 X1)

- `make check_coverage` now also fails on duplicate topic-hub rows (same doc and section) and on more unhubbed docs than the `MAX_UNHUBBED` ratchet (71, only ever lowered); the D6 hub exemptions are in CONTRIBUTING § Index maintenance, duplicate rows in `memory.md`, `harness.md` and `plugins.md` are merged, and `data.md` points to the knowledge-graph, memory and RAG hubs instead of repeating their rows (plan 0015 X2)

- `make check_coverage` also checks section anchors: every `#fragment` in a doc-to-doc link must match a heading (GitHub slug rules) or explicit anchor in its target; four broken anchors fixed (plan 0015 X3)

- Agent-memory landscape § 4: GrepMem (arXiv 2611.25123), lossless index-free memory as grep over an append-only history log (not rubric-scored), with a memory hub mention (owner fold-in)

- Coding-agents comparison: new "Model access and billing" section comparing 15 harnesses on bring-your-own-key, custom base URL or gateway, vendor pricing model and documented cost controls, plus a pointer from the routers and gateways landscape (plan 0015 N1a/N1b)

- Token-Waste Reduction Stack in the CC community tooling landscape gains an Evidence column (who measured each layer's saving, and when) and two layers: the context-mode tool-output sandbox and the Headroom compression proxy, each with author-run figures labelled as such (plan 0015 N1c).

- Coding agents and harnesses comparison (`coding-agents-comparison-landscape.md`), starting with image, PDF, video and voice input across 15 harnesses, each cell sourced to the vendor's own docs and dated (plan 0015 N3).

- LeanRDF (rdf-lean) entry in the semantic-layers landscape § Formal Ontologies & Semantic Web: RDF and RDFS entailment written in Lean 4, an untrusted Elpi search that emits certificates, and a small checker proven sound that accepts or rejects each step. Added on owner request; it meets D8 criterion 3 only through its self-reported W3C test-suite results (47 stars, one author). Cross-referenced from the agent-substrate reference architecture. Glossary rows for RDFS, triple, entailment, Lean and Elpi; the RDF bullet now defines a triple (plan 0015 N6)

- Agent evaluation metrics landscape: "Verifiable rewards (RLVR)" (named in Tulu 3, arXiv 2411.15124; RLVR-World and an RLVR-exploration paper as training work; Modal's open-model list as a vendor source; the eval-side lesson that needs no training) and "Update-regression gate" (Safe Personal RSI, arXiv 2611.23651: adopt a self-edit only if safety does not regress; self-reported results and caveats). Glossary rows for RLVR and RSI (plan 0015 N7)

### Changed

- Release flow moved to the estate's reusable workflows: `bump.yaml` (signed bump commit, scriv collected via uvx) replaces the local `bump-my-version.yaml`, and `release.yaml` tags and publishes the GitHub Release in one run, replacing `tag-release.yaml`; `publish-release.yaml` stays as a manual fallback. CONTRIBUTING's release steps updated.

- Microsoft 365 Copilot and Copilot Studio list prices in the Microsoft vs Salesforce worked example confirmed from the rendered pricing pages (plan 0014 K25)

- Community monitor: drops the claudelog source (its truncated changelog lines duplicate the changelog monitor), and a run that fetches no entries from any source, or leaves an empty report, now fails the job instead of opening an empty triage PR; seven notable uncovered awesome-list tools are folded into the community tooling landscape (plan 0014 K27).

- Re-verified IBM and Alibaba agent-stack claims: IBM A2A server role is documented as not yet implemented, Alibaba A2A (Model Studio consumer side, AgentRun tutorial) and RAM SAML/OIDC SSO are now documented; IBM IAM roles and workforce SSO stay unverified (plan 0014 K34)

- Salesforce Agentforce analysis: re-pointed the MuleSoft A2A bridge source to its new docs path (`/agent-fabric/services-create-a2a-bridge`), re-read all three A2A-contradiction sources on 2026-11-20 (quotes and the "contradicted" finding unchanged), and corrected one partial quote.

- Glossary abbreviations (MCP, RAG, A2A, AG-UI and others) are expanded at first use in 132 docs, and `make check_coverage` now fails on an unexpanded one (plan 0015 C2)

- CONTRIBUTING §1–§2: the frontmatter schema (required and optional keys; `sources`, `description`, `release`, `version`, `license`, `authority` and `category` leave frontmatter) and a lifecycle-only `status` vocabulary (`adopt`, `trial`, `assess`, `hold`, `research`, `reference`, `archived`; plan-only `draft`, `approved`, `done`, `superseded`), with release status, licence and version on the `**Details:**` line (plan 0015 F1, owner decision D5)

- Content-doc frontmatter migrated to the CONTRIBUTING §1–§2 schema: release and licence words moved out of `status:` to the `**Details:**` line, `category`/`description`/`sources`/`version`/`authority` removed from frontmatter (sources moved into each doc's Sources section), missing dates and `validated_links` filled; `status:` accepts lifecycle and plan tokens only, and `make check_frontmatter` is now strict; `learnings-aggregator.py` writes the same schema (plan 0015 F3)

- The doc graph page is simpler and faster: docs only (no cited-domain nodes), live search that dims non-matching docs as you type (Enter zooms to the first match), one checkbox per topic hub plus "Unfiled" and "Select all", colour by top-level folder, and a click opens the doc on GitHub. Its JSON is a slim projection (`site_graph`: title, bucket, hubs, one edge per linked pair), and the Pages site now redeploys on every push to `main` (plan 0015 G2)

- CONTRIBUTING gains the pruning rule (alive, adopted or proven; failures go to a `## Not included` table before Sources). Applied to the flagged entries: Vault-LD, Auto Ontology MCP, Agent Zero Memory, mxbai-rerank and Memorable moved to Not included; Memento cut to one dated line; Graft updated as Trail-code; reranker and LlamaParse pricing facts re-verified at vendor docs (plan 0015 P1)

- `agent-frameworks-infrastructure-landscape.md` § 4: Memento 3 and Neo4j Agent Memory moved to Not included under the pruning rule; MemoProAgent's code link added (plan 0015 P2)

- `CC-memory-tooling-landscape.md`: Operator Memory, open-second-brain, agent-second-brain and claude-second-brain moved to Not included under the pruning rule; ByteRover (archived) reduced to one dated line; Roampal Core's benchmark sentence corrected (plan 0015 P2)

- Prune CC-code-tooling-landscape: move Qodo open-aware and Qodo agents to Not included (D8 pruning rule, plan 0015 p2c)

- CC community tooling landscape: pruned seven entries (Boucle, Parry Guard, Dippy, cogit, ultraship, fable-baton, Selective Context) to a Not included table and shortened the archived GSD entry to one dated line (plan 0015 P2 batch 2)

- Pruned the CC community skills landscape under the D8 rule: BHIL, dispatch, a claude-howto fork, coleam00/skills and stevesolun/ctx moved to a new Not included table (plan 0015 P2)

- CC community plugins landscape: pruned 15 entries (voice/TTS hooks, squid, three mod catalogs) to a Not included table under the D8 rule (plan 0015 P2)

- Semantic-layers doc gains a "Choosing a structure" section (tags to knowledge graph, typed links vs hyperlinks); graph-databases doc gains "Property Graph vs RDF" and refreshed W3C, GQL and TinkerPop status (plan 0015 T1)

- Data platforms landscape gains a data lake vs lakehouse vs warehouse comparison and refreshed versions; agent-frameworks memory section gains a memory-taxonomy pointer with refreshed star counts; graph-visualization list is now a dated comparison table without this repo's own-site claim (plan 0015 T3)

- RAG and retrieval section gains a "RAG patterns at a glance" comparison (plain, hybrid, reranking, GraphRAG, agentic) with first-party sources, documented hybrid-fusion modes per engine, refreshed versions, stars and licenses for GraphRAG, LightRAG, FAISS, pgvector, Elasticsearch, OpenSearch, Qdrant, Milvus, Weaviate and RAGAs, and abbreviations expanded (plan 0015 T4)

- `adding-research-source` skill v0.2: new enrich-a-topic mode (gap survey, up to three worktree lanes on separate files, two falsification passes, lead adds hub and index rows) with reusable lane and falsifier briefs under `references/` (plan 0015 W1)

- Topic hubs: 46 pointer rows added for 45 docs that were in no hub; the unhubbed ratchet drops from 71 to 26 (plan 0015 X2)

- Caveman entry in the community skills landscape now cites the project's own site (caveman.so; getcaveman.dev serves the same page with caveman.so as canonical) and its docs (docs.caveman.so, the repo's homepage field)
- Caveman entry: new "Caveman Code (the coding-agent app)" subsection: a closed-source macOS and web app that runs Claude, Codex and Cursor plus Caveman's own open-model agent; plans and credit cap; self-reported Terminal-Bench 4 and DeepSWE results against Claude Code and Codex, including the loss the page reports; helper models trim-1, compact-1, router-1

- CC session cost analysis: Documented cost levers re-read against the live costs page (2026-11-22); added reference figures, TPM/RPM table, `modelPricing`, prompt cache line, agent-team and background token use; subagent env-var facts reattributed to the env vars page

- Doc graph page: the hub index (`docs/_topics/README.md`) is drawn as a hollow star so it no longer looks like an ordinary doc; the search box moved to the top of the side panel, and the version line moved into the top bar, right of the theme picker; hovering "Unfiled", "Exempt by rule" or "Not hub content" says which rule puts a doc there (owner request 2026-11-22)

- TrustGraph entry: v3.0.0 exists only as release candidates; latest stable PyPI release is 2.11.7 (checked 2026-11-22)

- Caveman entry in the community skills landscape refreshed to v4.2.0 (Apache-2.0 since 3.0.0, ~122K stars, as of 2026-11-22): now a skill plus local proxy; dropped benchmark figures no longer in the README; remaining numbers dated and marked author-run (plan 0015 N2).

- The doc graph no longer lumps every doc in no topic hub under "Unfiled": it splits them as `make check_coverage` does, into "Unfiled" (the docs the hub ratchet counts), "Exempt by rule" (D6) and "Not hub content" (README indexes, plans, research notes and example files), each with its own checkbox and count. Both read one function, `doc_coverage.hub_filing` (plan 0015 N4)

- Node 24 only: the lint and rxiv-paper-eval workflows set up Node 24 instead of 20, and `make setup_node` installs Node 24.22.3 instead of 22.11.0 (the lint workflow installs markdownlint-cli2 through it)

- `CC-usage-tooling-landscape.md`: pruned cc-costline (28 stars, no licence) and agentacct (early alpha, created 2026-07) to `## Not included` under the D8 rule (plan 0015 P2)

- CC remote-access landscape pruned under the D8 rule: Tailnet Preview, cc-tmux-worktree-orchestration and Typeless moved to Not included; Omnara repo status corrected (not archived) and CloudCLI star count refreshed (plan 0015 P2)

- Orchestrators landscape pruned under the D8 rule: agent-era/devteam (266 stars, no named users) moved to Not included; other entries kept (plan 0015 P2)

- Pruned the LLM routers and gateways landscape against the well-known, performance-optimised filter: Lightport, RelayPlane, ClawRouters, ShareAI and the Pandora routing paper moved to Not included; RouteLLM shortened to one dated line; AISIX and Arch Gateway (now Plano) facts corrected.

- Code-review products landscape: P2 pruning (plan 0015) moves Ellipsis to Not included, and updates the PR-Agent repo link and the Graphite reviewer name.

- CC community reimplementations landscape: pruned under the D8 rule (leaked-claude-code mirror moved to Not included, repo 404); corrected openclaude owner, licence (custom notice, not MIT), stars and version, and the snapshot repo's rename (plan 0015 P2)

- CC multi-account landscape pruned under the D8 rule: claude-code-profiles and claude-multisession moved to Not included (plan 0015 P2)

- CC reverse engineering landscape: D8 pruning pass (plan 0015 P2); no entries moved, `Yuyz0112/claude-code-reverse` shortened to one dated stale-but-adopted line, CL4R1T4S star count corrected.

- Research-agents landscape pruned under the D8 rule: CEDAR, RankEvolve, dataroom, MLR-Copilot and Open Coscientist moved to Not included; AI-Researcher, STORM, Agent Laboratory and OpenScholar cut to one dated line; corrected the IdeaScientist and Épi release facts (plan 0015 P2)

- Web-scraping landscape: pruned per the D8 rule. Moved scrapelex, paperscraper and eurlex (R) to `## Not included`, and marked Requests-HTML as stale but adopted (its "unmaintained since 2019" corrected) (plan 0015 P2).

- On-device semantic search landscape: P2 pruning pass; all entries kept, Voy marked stale with a dated line (plan 0015).

- `system-1-decision-models-landscape.md`: probably, jev-browser and the JEV-as-a-Judge paper moved to Not included under the pruning rule; RouteLLM reduced to one dated stale line; JevK5's JevBench rank corrected (fifth in v1.4.2.2, with Plumb-4B built on it); mentions of the dropped names removed from the non-cc README, the harness hub, jev-analysis and the reference-architecture row count (plan 0015 P2)

- Pruned `docs/sdlc-lcm/evaluation-data-resources-landscape.md` under the D8 rule (plan 0015 P2): moved LoopArena, E-Commerce Bench, MCPHallu, LifeVal, MiniCorp, the Omi medical STT benchmark, awesome-reasoning, SqueezeBench, CLEAR, AgentQuest, Yupp.ai, SWIF2T, SciXGen, StatLLM, MatSci-NLP, Trelis Function Calling, KnowLM-Tool and X-Fact to a new `## Not included` section; marked AutoGenBench archived (its parent repo) and StableToolBench stale.

- Pruned `agentic-ai-vulnerability-landscape.md` (plan 0015 P2, `p2m`): moved Secure Agentics Adrian to Not included (criterion 3)
- System-1 decision models landscape: dropped the Adrian use-case examples, Sources rows and links that pointed at its removed section (plan 0015 P2)

- Pruning pass on the graph databases and query languages landscape (plan 0015 P2): every entry judged against the pruning rule, none moved; Kuzu row marked stale but adopted

- AI crawlers and discoverability landscape: P2 pruning pass; three open-source generative engine optimisation (GEO) trackers and tools moved to Not included, AutoGEO code folded into its paper row (plan 0015).

- Pruned the spec-driven frameworks landscape: moved AB Method to Not included (no measured benefit or named independent users).

- Pruning pass on the agentic enterprise OS landscape (plan 0015 P2): HugAgentOS moved to Not included (635 stars, no paper, named users or measured benefit)
- Agentic enterprise OS landscape: AutoAgent marked stale but adopted (last push 2025-10-16); HugAgentOS dropped from the related list in `octop-analysis.md` (plan 0015 P2)

- Pruned the CC sandbox platforms landscape (plan 0015 P2): Maritime and Ephemora Cell moved to Not included; forkd renamed sandstorm (6.1k stars, v0.6.0), OpenSandbox stars refreshed.

- Pruning pass over the browser agents landscape (plan 0015 P2): every entry kept; ChatGPT Atlas stays as one dated line (deprecated, pointing to ChatGPT Work), and Perplexity Comet availability is now sourced to its product page.

- Agentic payments landscape: P2 pruning pass kept every entry; repointed the x402 link to its canonical repo `x402-foundation/x402` (`coinbase/x402` is now a fork).

- AG-UI protocol landscape pruned under the D8 rule: flightdeckhq/flightdeck (31 stars, no named users) moved to Not included; other entries kept (plan 0015 P2)

- Agent identity and auth landscape (plan 0015 P2): Privado ID Know Your Agent moved to Not included (private access only); SAM entry corrected to its renamed repo `google/agentmesh` (1,211 stars)

- Pruned the computer-use agents landscape against the well-known, performance-optimised filter: all four open-model entries kept, and the archived UI-TARS-desktop entry shortened to one dated line.

- Plan 0015 records the owner decisions of 2026-11-22: V1 (in-site doc view) decided no; 13-O5, 13-O10 and 13-O11 deferred; 13-O12 shipped as a shared rule in qte77/claude-code-plugins#303 ("a monitor step fails on any exit code it doesn't expect"), and the `AGENT_LEARNINGS.md` entry now points at it; 13-A2 done after a fresh session confirmed the shared rules still load. The plan's opening status is refreshed for the next session

- Hub coverage (plan 0015 X2): the owner's exemption list is in `doc_coverage.hub_exempt` (learnings notes, Claude Code reference indexes, the agent-substrate pair and two single-case analyses), `oss-alm-landscape` is filed under the management hub, and the `MAX_UNHUBBED` ratchet drops from 26 to 3; the three model-internals docs stay unfiled until their own hub (row X2b, deferred)

### Removed

- The graphify knowledge-graph page (`graph.html`), its render script, restyle and pruning helpers, the `make graph-build`, `graph-html`, `graph-query`, `graph-explain`, `graph-path` and `graph-page` targets, and the graph's own commit in `build.json`; the site now links the doc graph directly, and `architecture.md` § Knowledge Graph (graphify) is now § Doc Graph and Site (plan 0015 G1)

- `non-cc/orchestrators/devteam-analysis.md` archived (owner approval, plan 0015 P2): devteam fails the pruning rule's criterion 3. The doc moved to `docs/archive/non-cc/orchestrators/` with an archive banner, its non-cc README row is gone, and the orchestrators landscape's Not included row links the archived copy

### Fixed

- Abbreviation check: ignores frontmatter, HTML comments, URLs and link targets; counts plurals and hyphen compounds ("MCPs", "MCP-based") as uses; an expansion wrapped across lines counts; only a relative inline or reference-style link to the glossary exempts a doc; fences close only on a matching run, so mixed or nested fences no longer end a block early (plan 0015 C2 fact-check)
- `adding-research-source` skill: `refresh-docs` is named as a workflow, the link-check merge and exclude rules are aligned with CONTRIBUTING, and lanes are told to expand abbreviations (plan 0015 W1 fact-check)

- `.gitignore` now ignores `.claude/worktrees/`, and the evaluation-data landscape drops a Jenova benchmark link that returns 410 Gone (plan 0015 H1)

- Apache Maka analysis: the `docs/eval/` results folder was removed upstream (link 404); point at the `products/eval/` Harbor runner instead

## [0.22.0] - 2026-11-19

### Added

- Salesforce Agentforce analysis refresh: Copilotforce section (announcement-level), a table separating Salesforce CRM, Copilotforce and Microsoft's own Salesforce connectors, plus AgentExchange, Einstein naming lineage, role products, agent surfaces, and licences and roles pointers.

- Claude Code Code Mode disambiguation (Cloudflare, API programmatic tool calling), auto mode availability/classifier/defaults section (stale CLI-reference gating corrected), and `/autocompact` window settings with precedence versus `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, `--autocompact` and `DISABLE_AUTO_COMPACT`.

- Owner fold-ins (plan 0014 K38): Opal name-collision note, LiteLLM `agent_eval` (preview), AgentRun, Open Coscientist (source-available), Shepherd repo refresh, Opencontroller source, and a caveated rust-anything entry.

- `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` in the env-vars reference, and the v2.1.251 precedence change for `CLAUDE_CODE_SUBAGENT_MODEL` (post-session docs audit, plan 0014).

- New landscape `docs/non-cc/infrastructure/graph-databases-query-languages-landscape.md`: dated table of graph query languages (Cypher, GQL, SPARQL, Gremlin, Datalog), agent-relevant graph databases with licences and status (Kuzu archived, FalkorDB SSPL, Memgraph BSL), text-to-query evidence, and vendor and vendor-labs graph MCP servers, linking the HelixDB, LatticeDB and Minigraf analyses (plan 0014 K18).

- Knowledge-graph and ontology evidence: GraphRAG-vs-vector-RAG, KG-construction and LLM-edge provenance subsection and a temporal-KG-memory evidence subsection in the frameworks landscape, and an ontology generation and ontology-constrained extraction subsection in the semantic-layers landscape (plan 0014 K19).

- Computer-use agents landscape (new, plan 0014 K20): first-party Claude computer use (tool version, models, Desktop), OpenAI/Google/open-model status, OSWorld family with dated scores, pixel versus accessibility-tree trade-off and safety guidance; OSWorld row in the benchmark status table updated and cross-linked.

- Browser agents landscape (new): Claude in Chrome vs Chrome DevTools MCP vs Playwright MCP comparison, WebMCP status at source, agentic browsers (Atlas now deprecated), Online-Mind2Web and other benchmarks with dated, labelled scores, and prompt-injection safety; Chrome extension analysis refreshed to the GA state and Playwright/DevTools MCP versions updated (plan 0014 K21).

### Changed

- Microsoft 365 Copilot analysis: Frontier section rebuilt from the admin, individuals, support and Agent 365 pages (three programs, gates, licences, named items); new "What each name is" table and a Licences subsection (E3, E5, E7 Frontier Suite, Business plans, Copilot add-ons, usage-based billing, admin roles); Copilotforce pointer.

- Salesforce Agentforce analysis: scattered Einstein/Agentforce naming text replaced by one dated first-party lineage table. Corrected earlier claims: the Sales Cloud guide does not contradict itself (October 2025 in both places), Service Cloud to Agentforce Service is now Trailhead-sourced with conflicting naming noted, and the Einstein Copilot rename dates remain open.

- Owner decisions of 2026-11-19 recorded in plan 0014 (G1–G6 defaults accepted; K34 approved with Oracle, IBM, Alibaba and the Copilot SDK added and no prices); herdr and Zeron moved from the cc-community tooling landscape to the agent-frameworks landscape; the undated anti-bot tool list in the scraping landscape trimmed to pointers; the OpenResearch language citation repointed from the GitHub API to the repo page (#865).

- Software factory landscape: dated evidence subsection separating company claims (Stripe Part 2, Uber) from measured studies (AIDev, review-agent effectiveness, post-merge maintenance, SWE-CC, FeatureArc, FlowAgent); spec-driven landscape refreshed with 2026-11-19 stars and releases, Tessl status corrected (licence stays MIT), Kiro specs workflow moved into kiro-analysis (plan 0014 K12).

- Genie Ontology analysis re-checked against its docs and release notes (one dated rollout sequence, modeled vs learned knowledge, benchmark setting) and the OKF analysis updated for spec v0.2 (provenance, trust and lifecycle fields; two breaking changes) (plan 0014 K19).

- Cost hub follow-ups (plan 0014 K23): one per-model effort table with current defaults (`medium` on Fable 5.2, Opus 5.5, Sonnet 5.5 and Haiku 5.5), resolution order and per-model persistence; the fast-mode doc now points at it; `ultracode` no longer described as forcing `xhigh`; `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` corrected (applies to any session, not headless-only); new "Documented cost levers" section (`/usage`, `/context`, `/clear`, `/compact`, output styles, subagent model order) with a cost-hub row.

## [0.21.0] - 2026-11-18

### Added

- `docs/sdlc-lcm/mas-benchmarking-best-practices.md` § 3.5: Text2WetLab as a second, third-party worked example (grader attacks, a judge capped by deterministic checks, replay on grader change, source and licence per task, held-out set before release) and wet-lab protocol references (LAB-Bench, BioPlanner, SiLA 2, Autoprotocol, LabOP, PyLabRobot), linking to agentic-cax-gauge for CAD.

- `docs/sdlc-lcm/mas-benchmarking-best-practices.md` § 3.5: benchmark lifecycle (design, validate, release, maintain) covering construct, task and outcome validity, controls before ranking, recomputable reference answers, a fixed review rubric, provenance, run hygiene and documentation, with agentic-cax-gauge as a labelled worked example.

- 2.1.317–2.1.319 features: `CLAUDE_CODE_AUTO_MODE_SERVER`, `CLAUDE_CODE_DISABLE_FEATURE_FLAGS`, `CLAUDE_CODE_MCP_AUTO_BACKGROUND_MS`, `CLAUDE_CODE_DISABLE_MCP_TASK_BACKGROUND`, `CLAUDE_CODE_DISABLE_MCP_TASKS` in `CC-env-vars-reference.md`; `permissions.denyInsteadOfPrompting` in `CC-permissions-bypass-analysis.md`; Claude apps gateway pooled-budget rules and `/usage` spend in `CC-model-provider-configuration.md`.

- `docs/cc-native/ci-remote/CC-web-auth-setup-analysis.md` (plan 0014 K4): three subsections on scripted runs. "Terms That Apply to Scripted Runs" quotes the Claude Code legal page, the Agent SDK overview and the Consumer Terms. "What a Scripted Run Bills" covers plan login vs API key, monthly API credits on Max/Ultra/Team, cloud sessions, scheduled tasks, Managed Agents, `setup-token`, and `--bare` becoming the `-p` default. "Other Coding CLIs" compares Codex, Gemini CLI, Copilot CLI, Cursor CLI, opencode Go, Z.ai and MiniMax. Also a decision-matrix row and hub rows in cost.md and long-running.md.

- `docs/sdlc-lcm/agentic-ai-vulnerability-landscape.md`: "Prompt injection: attacks and defenses" section (plan 0014 K5) — attack taxonomy (direct/indirect, tool/MCP, memory, screen, multi-agent), defense table (instruction hierarchy, spotlighting, CaMeL, detectors, sandboxing), benchmarks, Claude Code documented surface; cross-linked from the ATLAS rows, the Prompt Injection Resistance metric and the safety benchmark list.

- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md` § Judge Calibration, Trace Evals and Eval Statistics: judge agreement and bias checks (position, verbosity, self-enhancement), pairwise vs pointwise, judge drift, outcome vs process and trace grading (TRAIL, Agent-as-a-Judge), eval error bars, pass@k vs pass^k, and the Inspect AI harness (epoch reducers, scorers).
- `docs/sdlc-lcm/evaluation-data-resources-landscape.md`: Inspect AI row in the frameworks table.

- `docs/sdlc-lcm/agentic-ai-vulnerability-landscape.md`: "Guardrail layers: a comparison" section (plan 0014 K8) — seven-layer table (filters, classifiers, rails, policy engines, approval, sandboxes, monitors) mapped to Claude Code hooks/permissions/sandbox/auto-mode classifier and vendor products, guardrail-evaluation results (auto-mode FPR/FNR, adaptive-attack bypass), approval fatigue.

- `docs/cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md`: "Cross-Harness Matrix" section (plan 0014 K9) comparing Claude Code, Codex CLI, Gemini CLI, OpenCode and Pi on tools, sandbox, permissions, compaction, hooks and resume, plus a pattern-coverage table for seven of the 12 patterns; unverified cells marked "not documented".

- `docs/plans/2026-11-15-0014-kb-strengthening.md` (#848): plan for strengthening the corpus across the owner's 2026-11-15 topic list (25 agent rows, 6 owner gates with defaults), based on four same-day coverage audits; carries over plan 0013's open rows with a `13-` prefix. Plan 0013 is marked superseded.

- Monthly decision-model eval now lists each weekly paper run's decide() share (read from the committed `triage/rxiv/` reports) and flags it in the `decision-drift` issue when the share falls more than 0.10 for three runs in a row (plan 0014 13-A7 part 2).

- Claude Code v2.1.321–325 folded into `docs/cc-native/` (plan 0014 K29): 12 env-var rows in `CC-env-vars-reference.md`, Code Mode in `CC-tools-inventory.md`, the sandbox auto-allow default change and worktree/symlink rules in `CC-sandboxing-analysis.md`, permission, Remote Control, fast-mode-on-Vertex, 1M-window and plugin/mod changes in the matching docs.

- `docs/sdlc-lcm/agentic-ai-vulnerability-landscape.md`: new section 7 comparing nine offensive-security and reverse-engineering agent tools (ARTEX, Claude-BugHunter, pentest-ai-agents, communitytools, Decepticon, xalgorix, HexStrike AI, REA, ghidra-mcp) on harness, license, autonomy, scope controls and finding verification; refreshed `rea-analysis.md` (stars, release, ghidra-mcp comparator) and added a pointer in `CC-community-skills-landscape.md`.

- `CC-memory-tooling-landscape.md`: new "Second-brain vaults" section comparing gbrain, COG-second-brain, open-second-brain, agent-second-brain and claude-second-brain (store, harnesses, retrieval, write path, license, stars as of 2026-11-17; COG skill-count inconsistency confirmed); ai-memory stars and version refreshed; pointer added in `karpathy-llm-kb-analysis.md`.

- Harness creation and benchmarking (plan 0014 K10): harness-search results table in `weco-aide-recursive-self-improvement-analysis.md` (HarnessFlow, Harness², Self-HPO, AIDE², RRSI; one canonical home, pointer left in the disciplines landscape), harness-benchmarking method in `agent-evaluation-metrics-landscape.md` § Cost-Performance Efficiency, and a build-vs-adopt section (Agent SDK, deepagents, Pi, OpenHarness) in `CC-agentic-harness-patterns-analysis.md`.

- Orchestrators landscape (six analyses by pattern, Claude Code primitives vs non-CC table, multi-agent failure modes from five papers); agent-teams "Unreleased" sections re-checked and recursive-spawning page updated for nested subagents (plan 0014 K11).

- Checkpoint/resume matrix, watchdog and liveness design and long-run failure evidence in `workflow-frameworks-landscape.md`; API and GitHub triggers and unattended permission posture in `CC-web-scheduled-tasks-analysis.md` (plan 0014 K13).

- Plan-file formats across agents, replanning/drift paper leads and plan-state goal predicates (goal-loops landscape, goal-tracking landscape); corrected Claude Code plan storage (plan 0014 K14)

- New `agentic-database-access-landscape.md` (database MCP servers, text-to-SQL benchmarks, write safety, migrations, lineage) plus a DB-write bullet in the vulnerability landscape (plan 0014 K16).

- New data-platforms and lakehouse landscape: open table formats, branching, catalogs, warehouse-native agents, local scratch engines, cost controls (plan 0014 K17).

- Scraping landscape: agent identity (Web Bot Auth, signed agents), dated vendor anti-bot handling table, dated search API prices, scrape-quality evidence and a short legal note; crawler doc gets a pay-per-crawl status check (plan 0014 K22).

- Tool use across model kinds (function-calling benchmarks, failure modes, action models) in `programmatic-tool-calling-analysis.md`, and a canonical grep-vs-semantic-search evidence section in `CC-code-tooling-landscape.md` (plan 0014 K30).

- `microsoft-365-copilot-analysis.md`: new "Microsoft agent stack" section (computer-using agents incl. Project Opal, the Frontier program, Agent Builder vs Copilot Studio vs declarative agents, Foundry Agent Service, Microsoft IQ grounding layers, Dataverse and Fabric); Cowork, Copilot Code and Managed Runtime re-checked 2026-11-18 (Ignite GA announcements vs Learn preview notices, new SDK/CLI package names); pointer from `CC-model-provider-configuration.md` § Microsoft Azure Foundry.

- Fold 10 preprints (INFUSE, SkillLifeBench, skill scanner, OAP, MAS-Guard, SWE-MISBEHAVIOR, AuthorizationBench, Prompt Lottery, trace-detector audit, cached-trace scoring) into the prompt-injection, guardrail and judge/trace-eval sections (plan 0014 K32).

### Changed

- `docs/non-cc/infrastructure/web-scraping-extraction-landscape.md` (plan 0014 K3): added a "Rendered-session scripting: polyfetch-scrape" subsection (v0.11.0 state, per-feature versions), a catalog-level note on Patchright's console/pageerror limits and its bearing on the moli spike criterion, a headed-launch finding in Anti-Bot Bypass, and corrected the header note (polyfetch keeps its own implementation docs, not only probe findings).

- Dated corrections: the Gemini CLI API-key free tier (now 250 requests/day, Flash only), Codex GPT-5.5 retirement for ChatGPT sign-in, the Cursor CLI's `agent` command name, and Copilot's legacy premium-request page. Moved two `long-running.md` hub rows that sat outside the table.

- `docs/sdlc-lcm/mas-benchmarking-best-practices.md` § 3.3: pointer to the new eval-methods section.

- Plan 0014: rows K26–K28 for the monitor backlogs found on 2026-11-15 (changelog monitor's "scanned through" header overstates coverage; community monitor's uncovered tools and empty reports; 669 of 703 relevant papers never cited in the corpus); K12 points at the company-wave research done the same day.

- Plan 0014: rows 13-A4 (first scheduled Clef paper run checked: 88/100 decided by Clef, 0 failures; 21 of 67 extractions fail to parse) and 13-A6 (shadow `relevance_score` shows a 1–10 label) struck; new row 13-A9 for the extraction-yield fix upstream; 13-A7 gets its first weekly data point.

- `CONTRIBUTING.md` § Auto-generated content: fold-in rule for papers the rxiv run rates relevant (each one cited, routed to an open plan row as a lead, at most four per row, or dropped with a class reason); the triage PR note in `rxiv-paper-eval.yaml` now asks for that before merge. Applied to the October–November reports (645 papers: 14 cited, 52 routed, 579 dropped), with the routed IDs in plan 0014's source map and a new row K32 for papers that fit shipped sections.

- Gemini CLI to Antigravity CLI refresh (plan 0014 K33): reconciled tier wording at Google's own pages, added first-party Antigravity CLI install/auth/resume/sandbox/headless/licence facts, and dated status notes in six docs that compare Gemini CLI.

- Plan 0014: new row K33, refreshing the corpus for Gemini CLI's replacement by Antigravity CLI (owner request).

- Evaluation landscape § 2 Benchmarks: dated or removed undated scores (OSWorld "~5%", SWE-EVO, LoopArena, Exgentic, LiveBench, GAIA2), added a benchmark status table, a validity-audit table, and short contamination and cyber-benchmark sections (plan 0014 K7).

- Plan 0014: session status refreshed for a hand-off. New owner-gated row K34 proposes covering the Azure, Google Cloud and AWS agent stacks (services, roles, identity and IdP, licences).

### Fixed

- `CC-extended-context-analysis.md`: drop the long-context premium above 200K tokens, which no longer exists — current models bill the full 1M window at standard per-token rates (Haiku 5.5 has its own over-100K tier). Adds which models default to 1M, plan gating per the model-config docs (Opus 4.6 at 1M included on Max/Ultra/Team/Enterprise; Sonnet 4.6 at 1M needs usage credits), and removes the dead long-context rate-limit link (plan 0014 K1).

- Changelog monitor coverage tagging (plan 0014 K26): a feature line now counts as covered when every backticked setting, variable or flag it names (an assignment like `VAR=1` matches `VAR`) appears backticked in one doc's body. Tokens backticked in more than three docs (common commands and flags such as `/usage`) are treated as generic and ignored, so they can't mark an unrelated fix as covered. Before, only filenames and H2/H3 headings were indexed, so documented settings stayed UNCOVERED. Since v2.1.71 this moves 93 → 1,077 of 7,940 changelog lines to covered; "covered" means the setting or command is documented somewhere, not that every fix to it is. Tests pin the rule and guard that the scan doc still yields a cutoff.
- `CC-changelog-feature-scan.md`: the frontmatter range is now labelled as the monitor's comparison cutoff, not documentation coverage.

- `docs/non-cc/coding-agents/codex-cli-analysis.md`: dated correction, the `untrusted` approval policy is retired and `auto_review` is a reviewer setting.
- `docs/non-cc/coding-agents/gemini-cli-analysis.md`: dated correction, latest release is v0.68.0 (2026-11-10).

- Post-merge falsification of the 2026-11-17 fold-ins: `agentic-ai-vulnerability-landscape.md` § 7 no longer says every listed tool states authorized-use-only (ghidra-mcp doesn't), and separates Decepticon's engagement-level approval from per-call gates; `CC-memory-tooling-landscape.md` scopes open-second-brain's snapshot claim to what its docs say and completes its harness list.

- rxiv paper eval: pass the agent-strict prompt as `relevance_prompt_template`, the input gha-rxiv-paper-eval v0.6.1 reads, instead of the deprecated `relevance_prompt` alias that logged a warning on every run (seen on the 2026-11-17 scheduled run).

## [0.20.0] - 2026-11-15

### Added

- `.github/workflows/decision-model-eval.yaml` + `.github/scripts/eval-decision-models.py` (manual):
  runs decision models (default Cloudflare `clef-flash` and `clef`, through `decide()` from
  qte77/.github pinned to 43ad121) over the G1 gold sets and writes `records.jsonl` + `summary.md`:
  ROC-AUC with a seeded bootstrap interval (papers only), Brier, accuracy, and a `hi` sweep with a
  rule fixed before the run (smallest `hi` whose acted decisions are wrong at most 5% of the time).
  Transient errors are retried; escalated items are counted and left out. Fails when a model answers
  nothing. Scoring in `lib/decision_eval.py`, 17 tests. Plan 0012 row H1.

- `docs/non-cc/infrastructure/semantic-layers-data-catalog-landscape.md` § Agent-native ontology
  tools: Auto Ontology MCP (gogoymh), a third-party standalone port of NVIDIA Auto Ontology.
  It runs on local SQLite, uses the MCP client's own model and adds a knowledge store that
  exports to Obsidian. The entry notes that it shares its package name with NVIDIA's own MCP
  client, and that its README warns datasource passwords are stored in plain text. Hub row in
  `docs/_topics/knowledge-graphs.md`.

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: seven owner-screenshot leads
  verified at first-party sources. Kept five — § Strands Decider (AWS / Strands Labs, a LoRA
  pointer head on Qwen3.5-2B), § Vega (Nandakishor M's follow-on to Laya, an energy-landscape
  readout engine), § Drex (Nace.AI, a 8B–35B family under a custom RAIL-M license), § Serving
  without training (Hugging Face `transformers serve`'s unreleased `/v1/systemone` endpoint and
  Ollama 0.35's native support), and two new entries in § Tools built on Jev (OntoSmith,
  edgextract) — plus a JevEval bullet in § Use cases → 5. Dropped one unverifiable sub-claim
  (Vega's benchmark wins over "hosted Jev 1.13.0"). The Strands Decider entry now cites
  Strands' own 2026-11-09 post on replacing Claude Sonnet 4.6 for Amazon ticket labelling; it
  was first dropped as unsourced after only the launch blog and README were checked.

- `docs/non-cc/reference/system-1-decision-models-landscape.md` § Cloudflare Clef: results of the
  first decision-model run on this repo's gold sets (2026-11-10). Clef reached ROC-AUC 0.970 on
  the 100 papers, with a recommended `hi` of 0.75 at 90% coverage; Clef-flash reached 0.958.
  The section notes the limits: in-sample threshold, agent labels, and an issue set whose 3
  negatives are planted fixtures.

- `docs/cc-community/CC-community-tooling-landscape.md`: Plannotator (MIT or Apache-2.0), a local
  browser review surface for agent plans, diffs and documents. In Claude Code it hooks
  `PermissionRequest` on `ExitPlanMode`, adds a hooks module for non-blocking review, and
  supports nine other harnesses. The entry covers its privacy and sharing model, and it gets a
  Comparison row and a cross-reference from `CC-hooks-system-analysis.md`.

- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §1: Strands Agents
  (AWS), an Apache-2.0 Python/TypeScript agent SDK. The entry covers its `harness-sdk` monorepo
  (renamed from `sdk-python`), the Strands harness (with its self-reported cost comparisons
  against Claude Code), Strands Evals, the AgentCore deployment target and the Claude Code plugin.

- `docs/non-cc/agents/salesforce-agentforce-analysis.md` (plan 0013 A10): first-party fact-check of
  Salesforce Agentforce 360 — the platform and its component products, Claude via Amazon Bedrock
  inside the Salesforce trust boundary (Claudeforce), the Agentforce Registry and the separately
  branded MuleSoft Agent Fabric, Agent Script / Agentforce DX, the 2026-08-18 Flex Credits rate
  card, the Hyperforce EU Operating Zone, and an "announced vs. shipped" table. Resolves the
  "masking disabled for agents" question against Salesforce's own help article and a corroborating
  blog post (it is a documented agent-action-vs-direct-template scope split, not a conflict), and
  corrects a prior research note's A2A claim against Salesforce's own architecture recipe page.
  Cross-linked from `agentic-enterprise-os-landscape.md`, `ag-ui-protocol-landscape.md`,
  `CC-business-api-integrations.md`, and `microsoft-365-copilot-analysis.md`.

- `docs/non-cc/agents/microsoft-365-copilot-analysis.md` § Training and certification: a
  Learn-sourced table of agent-relevant Microsoft credentials (AB-900, AB-620, AB-100, AB-730,
  AB-731, AI-103, AI-500, SC-500), plus the Learn-confirmed retirement dates for AI-102, PL-200,
  and AZ-500 — with a note that the commonly cited AI-102→AI-103 / PL-200→AB-410 / AZ-500→SC-500
  replacements trace to Microsoft Partner Center, not to any Learn page.
- `docs/non-cc/agents/github-copilot-cloud-agent-analysis.md` § GitHub certifications: GH-300
  (GitHub Copilot) and GH-600 (GitHub Certified: Agentic AI Developer), the latter confirmed to
  exist via Microsoft Learn's certification catalog API rather than taken from the certification
  poster alone. Plan 0013 row A9.

- `.github/workflows/decision-model-eval.yaml`, `.github/scripts/eval-decision-models.py`, `.github/scripts/lib/decision_eval.py`: monthly drift check for the decision models. The gold-set eval runs on the 1st of each month with Clef, Clef-flash and Jev 1.13.0, writes `metrics.json`, compares with the committed `.github/scripts/data/gold/baseline.json` (ROC-AUC drop above 0.03, recommended `hi` moving by 0.05 or more) and opens, updates or closes one `decision-drift` issue (plan 0013 row A7, part 1).

- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §4: WikiTrace
  (arXiv:2611.14320, Lee/Choi/Baek/Hwang, KAIST AI · DeepAuto.ai) — an evidence-linked memory
  that links each lesson to a compilation and the raw trajectory it came from, so an agent can
  check an underspecified, conflicting, or failure-sourced lesson before acting instead of
  trusting it outright. Self-reports the best average score against four prior memory methods,
  an insights-only ablation and no memory across eight evaluation suites, cutting the regression
  rate on tasks solvable without memory
  from 6.5% to 4.5% (paper claims; methodology not independently verified). Code released
  (Apache-2.0, 10★).
- `docs/_topics/memory.md`: hub row for the WikiTrace addition.

- `docs/cc-community/CC-community-plugins-landscape.md` § Community Mod Catalogs: Notable Plugin
  Profile for lot-map (MIT; 407★/45 forks, `gh api` 2026-11-12) — a Claude Code mod that draws a
  live node-map pane of tool calls, hooks, subagents and skills as they happen, built on the
  native Mods mechanism rather than an external hook server. Includes a source read of
  `hooks/register.tsx`/`hooks/map.ts` cross-checking its self-reported no-network/no-fs/no-process
  privacy claim.
- `docs/_topics/visualization.md`: hub row for the lot-map addition.

- `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: a second first-party pass (2026-11-12)
  covering Microsoft products the corpus lacked — Microsoft Copilot Cowork (GA June 2026,
  disambiguated from Anthropic's Claude Cowork), the 2026-09-25 "new Copilot" (Home, Copilot Code,
  Autopilot — confirmed "previously called Scout"), Microsoft Copilot Managed Runtime (preview,
  hosts line-of-business apps, not agents), declarative agent manifest 1.9's `agent_skills`
  property and Fabric capability, Researcher/Analyst, and the Microsoft 365/Agent 365 SDKs and
  Agent Store. Updates the Scope/Details/Timeline/Pricing sections and the "Two things called
  skill" item on custom skills in declarative agents (mechanism now vendor-documented; GA-by-date
  claim still unconfirmed).
- `docs/non-cc/frameworks/agentic-enterprise-os-landscape.md`: extends the Microsoft Copilot Studio
  row with the Microsoft Foundry "managed runtime" caveat — the Foundry Copilot harness (preview)
  and Foundry hosted agents (containerized; "managed runtime" is marketing-page wording only, GA
  unverified), disambiguated from Copilot Studio's own (renamed) harness.
- `docs/cc-native/plugins-ecosystem/CC-cowork-plugins-enterprise-analysis.md`: disambiguation note
  pointing to Microsoft Copilot Cowork, a different, Microsoft-branded product.

- `docs/sdlc-lcm/software-factory-landscape.md` §(c): Anthropic's own 2026-10-13 engineering post on
  migrating its monorepo off git to an in-house system (Scion) as daily merges rose from ~2,500 to
  30,000+ per day — a vendor-reported internal case alongside the existing Cloudflare Astro case.
- `docs/cc-native/configuration/CC-models-reference.md`: Claude Fable 5.2 / Mythos 5.2 (CC v2.1.321+),
  pricing table rows, and the headline benchmark figures stated directly in Anthropic's 2026-11-09
  announcement.
- `docs/sdlc-lcm/evaluation-data-resources-landscape.md`: the `claude-api` skill's `build-eval` and
  `hillclimb` commands (claude.dev, Lance Martin, 2026-09-28), which operationalize the EDD loop
  already documented there, plus the self-reported 66.1%→87.9% result on Anthropic's own skill.
- `docs/cc-native/configuration/CC-tools-inventory.md`: the account-email-in-outbound-request guardrail
  (CC v2.1.317/v2.1.321 CHANGELOG entries, verbatim) alongside the still-open `claude-code#107757`
  privacy issue it is adjacent to.
- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: the `v2.1.277` CHANGELOG line, quoted
  verbatim, confirming the already-documented AGENTS.md-fallback behavior and its `/config` toggle.
- `docs/cc-native/plugins-ecosystem/CC-cowork-plugins-enterprise-analysis.md`: the Claude for Financial
  Advisors Cowork plugin (2026-09-14, updated 2026-10-27) and the Claude for Nonprofits plugin
  (2026-10-26), distinct from the existing financial-services and Cowork-templates coverage.

- `docs/sdlc-lcm/ai-security-governance-analysis.md` § Defensive Tooling: Stroq (local
  tool-call-gating + secret-leak tracing for coding-agent sessions), Tracekit (tamper-evident
  signed audit log for tool calls, mapped to EU AI Act / ISO 42001 / NIST AI RMF / OWASP), and
  devvm (per-project Lima VM sandbox for coding-agent hooks and local MCP servers).
- `docs/sdlc-lcm/agent-code-analysis-landscape.md` §3: Grim Prompter (agent-driven,
  file-and-line-cited threat modeling) and OpenQodex (scanner-then-agent-review pre-push
  pipeline).
- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md` § Evaluation Platform Integration: Waza
  (Microsoft's Go CLI for authoring and grading agent-skill eval scenarios).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §1/§3: ToolCallJudge
  (Pydantic AI Harness's tool-call-approval gate), Harness² (Google Research's recursive
  harness-optimization loop) and OpenHuman (a Rust agent harness self-benchmarked against
  Hermes).
- `docs/cc-community/CC-code-tooling-landscape.md`: Floorplan, a Claude Code/Codex plugin that
  draws an interactive map of a codebase, with a Health check and a Recent-work view.
- `docs/cc-community/CC-community-plugins-landscape.md`: new Notable Plugin Profiles for
  Impeccable (cross-agent design-vocabulary/slop-detector plugin) and Elephant-Goldfish Model
  (Google's drafter/fresh-context-reviewer spec-review plugin).
- `docs/cc-community/CC-community-tooling-landscape.md`: cogit, a Claude Code plugin that
  records the intent behind agent-written code as git-linked "thought commits."
- `docs/non-cc/agents/skill-recorder-analysis.md` (new doc): Microsoft Skill Recorder, which
  turns a recorded or imported screen session into a reusable Skill or Automation via the
  GitHub Copilot CLI, for Scout/Copilot Cowork/Copilot Studio.
- `docs/_topics/harness.md` and `docs/_topics/skills.md`: hub rows for the Harness²/OpenHuman/
  ToolCallJudge and Skill-Recorder/Waza additions above.

- `docs/cc-community/CC-memory-tooling-landscape.md`: CortexDB (liliang-cn) — Go agent memory +
  RDF knowledge graph in one SQLite file, with a Claude Code plugin and early-access mod — and
  Leviathan (elstongun) — a Rust full-text/memory index for agents over large datasets, with a
  self-reported 245x token reduction vs. grep.
- `docs/cc-community/CC-code-tooling-landscape.md`: AxiomCode Graph (compiler-accurate,
  type-resolved code knowledge graph; FSL-1.1-Apache-2.0), Graphicle (a Rust port of Graphify's
  code graph plus an agent-memory layer, benchmarked against Graphify and against seven memory
  systems), and XERJ (an Elasticsearch-compatible local search engine/MCP server with a
  first-party Claude Code/Cursor installer and a reference-coding token-savings case study).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §4: Kortix CompanyOS
  (shared company memory in a multiplayer cloud-agent harness; Elastic License 2.0, not the
  README's "Open Source" framing), MemoProAgent/MemoProBench (arXiv:2610.22671 — the paper found
  at this ID does not match the names "ProPerAgent"/"ProPerMem" or the "Meta" attribution the
  source post used), and ReHarness (arXiv:2610.12668, backward-revised harness state for agentic
  continual learning). §7 Agent-native graph & hybrid RAG platforms: Carrel (self-hosted
  ontology-augmented knowledge base, MIT) and RAGFlow (agent-native RAG database, 94k★,
  Apache-2.0).
- `docs/non-cc/knowledge-management/research-agents-landscape.md` §1: Épi (arXiv:2610.24944),
  a persistent, self-improving research agent with hierarchical memory.
- `docs/_topics/memory.md`, `knowledge-graphs.md`, `rag.md`, `code-tooling.md`: hub rows for the
  above.

- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md` § Evaluator Alignment / § Tool Call Accuracy:
  DUET (co-evolving solver/grader agents, arXiv:2610.04087) and MCP-Injector (MCP tool-call fault
  injection, arXiv:2610.32555, NeurIPS 2026).
- `docs/sdlc-lcm/evaluation-data-resources-landscape.md` § Benchmarks: LifeVal (arXiv:2611.06687) and
  MiniCorp (arXiv:2610.05912) added to the general/real-world-agent benchmark row.
- `docs/non-cc/reference/weco-aide-recursive-self-improvement-analysis.md`: four more
  self-improving-harness papers — Harness² (arXiv:2610.14224), RSI-Dojo (arXiv:2611.03698), InfraRSI
  (arXiv:2611.11558), and Self-HPO (arXiv:2610.22791).
- `docs/non-cc/frameworks/agent-skill-evolution-research-landscape.md`: Adaptive Skill Granularity
  (arXiv:2610.31461) and Skill++ (arXiv:2611.00544), batch-triage additions (not rubric-scored).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` § Memento: notes the later
  Memento 3 paper (arXiv:2610.11794) as a distinct method from a mostly different author list sharing
  one author with the original Memento paper.
- `docs/_topics/harness.md`, `docs/_topics/skills.md`: hub rows updated for the above.

- `docs/cc-native/configuration/CC-tools-inventory.md`: `/powerup` (interactive feature lessons, CC v2.1.90) in the documented slash-command table (plan 0013 row A11).

- `docs/_topics/cost.md`: topic hub for token usage and spend (cost drivers, levers, measurement tools), pointers only; registered in the hub index and CONTRIBUTING.
- `CC-prompt-caching-behavior.md`: one week of sessions on one machine (2026-11-07 to 2026-11-14) — 98.6% of input tokens were cache reads; cache rewrites after idle gaps of over an hour were 52% of cache writes in main conversations.
- `CC-env-vars-reference.md`: documented rows for `DISABLE_AUTO_COMPACT`, `DISABLE_COMPACT`, `BASH_MAX_OUTPUT_LENGTH`, `MAX_MCP_OUTPUT_TOKENS`, `CLAUDE_CODE_MAX_OUTPUT_TOKENS`, `MAX_THINKING_TOKENS` and `ENABLE_TOOL_SEARCH`, checked against the env-vars page on 2026-11-15; `CLAUDE_CODE_MAX_OUTPUT_TOKENS` moved out of the undocumented list.

### Changed

- `make reconcile` also lists open plan rows that cite no checkable PR/issue ("verify by hand";
  informational, exit code unchanged). `lib/plan_reconcile.py` `unchecked_open_rows()`, 2 tests.
- Plan 0012: D2 struck (qte77/.github#47 merged 2026-10-26, found stale on 2026-11-10); its live
  call moved into H1's done-when. `AGENT_LEARNINGS.md` records the blind spot.

- Plan 0012: H1's Clef part is shipped (Jev waits on K0). C1 is shipped: live triage checks
  passed in five consumer repos. P1 is shadow-only first, and P2's done-when compares against the
  Llama-70B baseline on the gold set.
- `.github/scripts/eval-decision-models.py`: the summary prints the real negative count, not a
  hardcoded 3.

- `docs/non-cc/reference/system-1-decision-models-landscape.md` § Cloudflare Clef: the gold-set
  results now include Jev 1.13.0 (2026-11-11). On papers Jev scored ROC-AUC 0.968 with a
  recommended `hi` of 0.70 at 91% coverage, overlapping Clef within the bootstrap intervals; on
  issues it scored 62/62. Median call time from a runner was 0.14–0.15 s.
- Plan 0012: H1 and P2 struck. Papers use Clef at `hi` 0.75; issue triage uses Clef in shadow mode.

- `.github/workflows/issue-triage.yaml`: pinned gha-issue-triage v0.6.0 and turned on
  `decide-shadow`. Triage comments here now carry a fixed-format decision-model section
  (value, probability and band from Clef). Labels still come only from the existing triage.
- Plan 0012: P1 struck (v0.6.0 released, six consumer repos bumped); labels from the decision
  model are deferred until the shadow mode has data from real issues.

- Plan 0012: P2's code merged in gha-rxiv-paper-eval (release and opt-in pending); P1's PR open in
  shadow mode; Q1 shipped; `TYPESAFE_API_KEY` set here; new row N13 for the 2026-11-11 owner
  screenshot batch (417 tiered, 186 useful leads, routed to this repo and three siblings).

- `.github/workflows/rxiv-paper-eval.yaml`: pinned gha-rxiv-paper-eval v0.6.0 and turned on its
  decision-model path. Relevance asks Clef 27B first, with `hi` 0.75 from the H1 gold-set run.
  Uncertain papers and escalations fall back to the agent-strict chat call. The decision path
  gets the same agent-strict criterion, minus the chat reply-format sentence; a unit test keeps
  the two in sync. The base URL is now passed as the `LLM_BASE_URL` secret, so the
  `LLM_BASE_URL` repo variable is no longer read. A feed week with 0 rows now fails the eval.

- `docs/architecture.md`, `docs/UserStory.md`: the monthly `decision-model-eval` drift check (baseline file, `decision-drift` issue, manual runs summary-only) and the skipped-source reporting in the content monitors are documented, with a user story for each.

- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §1 Archon: refreshed to v0.14.0 (2026-11-07). Archon runs Claude Code, Codex and Pi as separately installed providers (since v0.12.0; the 2026-09-30 entry wrongly called it Claude-Code-run), Slack moved to a plugin (v0.13.0), the SDLC pack reaches GitHub only through the `forge-github` plugin and `archon metrics` was added (v0.14.0); telemetry on by default; README quotes that no longer appear were replaced.
- `docs/cc-community/CC-community-skills-landscape.md` § coleam00: star counts and skill count refreshed (2026-11-12); pointer to Archon and the author's YouTube channel.

- `CLAUDE.md` is now a one-line file importing `@AGENTS.md` instead of a symlink to it. Plan 0013
  row A2 notes that gha-issue-triage must follow that import, because its repo-context loader
  reads `CLAUDE.md`.

- Plans: plan 0012 (decision models) and plan 0001 (user-level rules) are closed. Owner rows
  were closed with their defaults (R8, R13, plan 0001 row 7), K0 was closed as done, and the
  remainder moved to the new plan 0013 (#800): sibling Dependabot PRs, the `AGENTS.md`
  fallback in gha-issue-triage, the community monitor's skip report, the first scheduled Clef
  paper run, and owner items.

- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md` § Cost-Performance Efficiency (Pareto):
  updated the Artificial Analysis Coding Agent Index entry from v1.5 to v2.0 (FrontierCode v1.1
  replaced DeepSWE v1.1; SWE-Atlas-QnA renamed SWE-Atlas-QnA-AA; equal-weight composite; "each
  public row is an agent variant, not a model"), and added the data-API scope note ("no longer
  publishes a Coding Index or an Agentic Index") and a Terms-of-Use note (personal/non-commercial
  use, no reproduction, no automated scraping) — this corpus does not copy its scores, costs, or
  rankings.
- `docs/sdlc-lcm/evaluation-data-resources-landscape.md` § 2. Benchmarks: enriched the Code / SWE
  bullet with a harness-level-vs-model-level breakdown of SWE-bench / SWE-bench Verified,
  Terminal-Bench, and Scale SWE-bench Pro, plus a corrected Epoch AI note (it runs its own
  scaffold plus named third-party scaffolds on SWE-bench Verified, not zero-shot as first
  assumed); linked WebDev Arena in the Leaderboards bullet to Arena.ai ("formerly LMArena").
- `docs/_topics/harness.md`: added a pointer row to the new benchmarks breakdown and a one-line
  addition to the existing Pareto-section row noting the Coding Agent Index v2.0 update.

- `.github/workflows/issue-triage.yaml`: gha-issue-triage v0.6.0 → v0.7.0. Triage now reads `AGENTS.md` through this repo's `@AGENTS.md` import in `CLAUDE.md` (qte77/gha-issue-triage#132), and the shadow section shows `relevance_score` as a 1–10 level instead of `-` (qte77/gha-issue-triage#133).

- `.github/workflows/issue-triage.yaml`: gha-issue-triage v0.7.0 → v0.7.1, which prints each shadow `relevance_score` answer's raw number to the job log, to confirm its zero-based reading (qte77/gha-issue-triage#136; plan 0013 row A6).

- Microsoft 365 Copilot ecosystem analysis: re-checked ~47 load-bearing claims against current
  first-party pages (`microsoft-365-copilot-analysis.md`). Added a previously-unreported,
  not-yet-shipped Microsoft Copilot blog announcement (2026-11-05) that Claude processing is
  planned to move into the EU Data Boundary for EU/EFTA tenants by end of 2026, without changing
  the doc's current-state claim that Claude remains excluded today; softened the Copilot Studio
  GPT-5.5/GPT-4.1/GPT-5 retirement rows from "retired"/"reached" to "scheduled, completion
  unconfirmed on the page" (the Learn page's own content metadata is unchanged since before those
  dates); refreshed several re-checked dates from 2026-11-09 to 2026-11-12; updated two citation
  URLs to their current canonical Learn paths (`connect-to-ai-subprocessor`,
  `manage-byo-mcp-server`, both still resolving via redirect from the prior URL).
- Microsoft MXC analysis: refreshed star count (3,116 → 3,132) and re-confirmed the "Claude Code
  support is announcement-only" absence claim against the full text of Claude Code's own
  sandboxing docs (`microsoft-mxc-analysis.md`).
- Microsoft Skill Recorder analysis: corrected a misattribution — the "Scout/Cowork/Copilot Studio"
  consumer-surface claim is sourced to the repo's GitHub description field, not its README body,
  which never names those surfaces; added the Ubuntu/Linux install path the README's own
  instructions point to but the doc had omitted; refreshed star count (5,760 → 5,762)
  (`skill-recorder-analysis.md`).

- `docs/cc-community/CC-community-plugins-landscape.md` § claude-seo: refreshed the stale
  2026-04-15 snapshot (23 skills/17 subagents/3 extensions, 2026-04-23 counts) to the repo's
  current README and `gh api` figures (26 skills/19 subagents/9 extensions, 28,262★).

- Plan 0012: E1 struck. The estate decision-model conventions are now in
  `qte77/.github` `actions/decide/CONVENTIONS.md`, linked from the decide README and both ported
  actions. New struck row N14 records the 2026-11-11 owner leads: Strands Agents,
  Auto Ontology MCP and Plannotator.

- Plan 0012: N13 struck. The 2026-11-11 owner screenshot leads have been verified and folded
  into the corpus (#790–#793) and into agentic-cax-gauge. All agent rows are closed; what's
  left is optional or rests with the owner.

- Plan 0013: O3 is struck. The gha-issue-triage lint failure came from an old pin of the shared
  workflow (fixed in qte77/gha-issue-triage#131), not from the Actions setting. Five new agent
  rows: drift checks for the decision models (A7), out-of-sample gold sets (A8), AI
  certification paths (A9), a Salesforce Agentforce 360 analysis (A10), and `/powerup` in the
  tools inventory (A11).

- `docs/plans/2026-11-12-0013-followups-after-0012.md`: opening status brought up to date (A1, A3, A9–A11 and A7 part 1 shipped; A2/A6 code in gha-issue-triage v0.7.0/v0.7.1 and pinned in all consumers), A2 and A7 rows record what is left, and four owner rows added with defaults: link-check excludes for three bot-blocked links (O6), the Mythos-on-AMD note (O7), the SoTA Letters leads kept here (O8), re-cloning coding-harness-eval (O9).

- `.claude/settings.json`: allow the read-only `make check_status`, `make check_actions`, `make help`, `make census` and `shellcheck *`, alongside the existing exact make-target rules, so sessions without a local settings file (cloud, CI, other machines) don't prompt for them.

- `lychee.toml`: exclude `developer.salesforce.com` and `architect.salesforce.com` (host-level, replacing the single developer.salesforce.com blog URL) and the one path `arena.ai/leaderboard/webdev`. Every URL on them returns 403 to lychee both locally and in CI (a persistent bot-block, unlike runner-IP 403s that pass on a local recheck); one page per host was checked live on 2026-11-13. The Salesforce and harness-comparison docs added on 2026-11-12 had turned the link check red on every run, including `main`.

- `docs/cc-native/configuration/CC-models-reference.md`: dated note on the hardware Claude runs on, cited to Anthropic's S-1/A (filed 2026-11-10: four chip families, one fungible compute pool, Claude used to bring up new chip platforms) and AMD's 2026-07-22 release (up to 2 GW of MI450 Series GPUs, builds on existing MI355X use). A time figure for Mythos on AMD hardware, shared on X, is left out: the filing's text gives only the old "many months" baseline, and its source wasn't traced (plan 0013 O7).
- `lychee.toml`: exclude Anthropic PBC's SEC EDGAR filings path (`sec.gov/Archives/edgar/data/2130357/`). SEC returns 403 to clients without a contact user agent; owner-approved.

- `docs/plans/2026-11-12-0013-followups-after-0012.md`: row O1 done (owner set the Workers AI token in gha-rxiv-paper-eval; a manual self-test run returned real Workers AI verdicts), with a correction: the self-test already used Workers AI on `main`.

- `docs/plans/2026-11-12-0013-followups-after-0012.md`: owner row O10 records the Cloudflare account-details audit: what shipped (`qte77/ldnmxx-hack#373`, `qte77/qte77.github.io#62`) and the open owner decisions.

- `docs/plans/2026-11-12-0013-followups-after-0012.md`: row O10 trimmed to what shipped; the open Cloudflare decisions and removal steps moved to the owner's private notes.

- `docs/plans/2026-11-12-0013-followups-after-0012.md`: rows O4 (operator commands: first tranche shipped in six repos, remaining hits counted) and O5 (stale token variables traced and removed where the container allows) updated.

- `tag-release.yaml` and `publish-release.yaml` re-pinned from `qte77/.github@613b950` to `qte77/.github@a32769a` (main, 2026-11-12, qte77/.github#64). Inputs/outputs used by this repo are unchanged at the new pin.

- `.claude/settings.json`: allow more read-only calls seen often in recent sessions: `~/.local/bin/lychee *` (the user-local install path, which `lychee *` doesn't match), `gh run watch *`, `gh secret list *` (names only, never values), `gh search prs *`, `gh label list *`, and the Cloudflare docs search MCP tool.

- `docs/cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md`: correct the Glasswing mention. Project Glasswing is Anthropic's 2026-04-07 initiative with launch partners to secure critical software using the gated Claude Mythos Preview, not a "security team collaboration program". Since the expanded Cyber Verification Program launched (2026-10-06), its members "will transition" to that program's Specialized Access tier. The mention is now linked.
- `docs/sdlc-lcm/agentic-ai-vulnerability-landscape.md`: size ATLAS's "Poison Training Data" with Souly et al. (arXiv 2510.07192): 250 poisoned documents backdoored 600M–13B models regardless of size. The backdoor tested is narrow, and the paper is a preprint (plan 0013 O8).

- `.claude/settings.json`: set `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` to 60, so long research and PR/CI sessions compact earlier with room left for reasoning and recovery.

- `docs/sdlc-lcm/agent-identity-auth-landscape.md`: design lens on authorization when agents fan out into parallel acting branches. It adds the costs of central gateways and the "authority travels with the branch" alternative, cited to a practitioner post (opinion) and tied to the token-binding specs already in the doc.

- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md`, `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md`: TruLens now lists its seven agent evaluators, Agent GPA result, MCP span type, v2.16.0, and Snowflake stewardship.
- `docs/non-cc/infrastructure/llm-routers-gateways-landscape.md`: LiteLLM row refreshed (v1.109.1, stars) and the announced Customer Portal (per-customer budgets, OSS vs Enterprise limits).
- `docs/non-cc/frameworks/agentic-enterprise-os-landscape.md`: add Lyzr Agent Studio to the enterprise vendor tier, with a caveat on deployment modes and vendor claims.

- `docs/non-cc/infrastructure/ai-crawlers-discoverability-landscape.md`: new section "GEO and AEO: what is canonical". It covers the KDD 2024 paper and its repo, the IETF aipref drafts and their actual scope, Netlify's "Agent Experience" as a separate idea, and how GEO differs from classic SEO.
- `docs/sdlc-lcm/evaluation-data-resources-landscape.md`: Cloudflare's isitagentready.com added as a third agent-readiness scorer, with a note that agent-readiness-kit aggregates Ora and Cloudflare rather than adding a fourth score.

- `docs/non-cc/infrastructure/ai-crawlers-discoverability-landscape.md`: OpenAI's Business Hub (Businesses in ChatGPT, beta, 2026-11-10) and its stated limits; ASO and LEO added to the GEO label list with their competing expansions; agent-facing optimization research (Toolflation, "AX is the New AEO").
- `docs/non-cc/knowledge-management/research-agents-landscape.md`: field evidence on agent search sessions from arXiv 2601.17617 (SIGIR 2026) under the `/deep-research` mapping.

- `docs/non-cc/infrastructure/ai-crawlers-discoverability-landscape.md`: GEO field refresh. Google's AI optimization guide (what to ignore), the Search Console AI-features opt-out and generative-AI reports, Microsoft Advertising's *A Guide to GEO* and Bing's AI Performance report, where Google and Microsoft disagree; a research table of ten GEO papers (C-SEO Bench, AutoGEO, E-GEO, ranking-manipulation and tool-selection studies); trackers with MCP access and open-source GEO projects; checklist extended. Corrects the claim that no first-party AI-visibility reporting exists.

- `docs/cc-community/CC-community-skills-landscape.md`: add GoogleChrome/modern-web-guidance, a browser-vendor Agent Skill with a bundled retrieval CLI, an npm package and plugin packaging for Claude Code and other hosts, plus its uplift-based eval loop.

- `docs/plans/2026-11-12-0013-followups-after-0012.md`: row O2 (marketplace SEO/ASO) dropped by the owner; a research pass on marketing for agents replaces it.

- `docs/plans/2026-11-12-0013-followups-after-0012.md`: row O4 done: older plans across six public repos cleaned (live plans reworded, closed plans marked as records).

- `docs/plans/2026-11-12-0013-followups-after-0012.md`: status as of 2026-11-14 (research fold-ins, auto-compact, status-monitor fix); new owner rows O11 (`#726`) and O12 (shared-rule promotion); `#588` listed under Deferred.

- `docs/sdlc-lcm/software-factory-landscape.md`: add the 2026 wave of company pipelines, each from its own source: Stripe Minions, Ramp Inspect, WorkOS Horizon, OpenAI Symphony, Delinea (StrongDM) Software Factory with its `attractor` spec, and the Vercel factory template. Also notes the `open-inspect` repo against the ai-that-works ep. #73 entry.

- Ten papers from the W45 arXiv triage folded into existing docs, each checked against the full paper: ARCBench and hand-off-summary policy (`CC-agentic-harness-patterns-analysis.md` § 5), KernelSeek (§ 12), HarnessFlow and Meta-Harness (`agentic-engineering-disciplines-landscape.md`), task-tampering injection and LatentTriad (`agentic-ai-vulnerability-landscape.md` § 6), A.S.E 2.0 (`agent-code-analysis-landscape.md`), code maps with Claude Code (`CC-code-tooling-landscape.md`), Terminal-Bench 2.1 and MCPHallu (`evaluation-data-resources-landscape.md`); topic hubs updated.

- `.claude/settings.json`: drop the project-level `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` (60). Project settings override user settings, so it was overriding the owner's user-scope value (50).
- `AGENTS.md`: link `CONTRIBUTING.md` and `AGENT_LEARNINGS.md` instead of `@`-importing them; the imports loaded about 7.4k tokens into every request in this repo.

- `rxiv-paper-eval.yaml`: pin `qte77/gha-rxiv-paper-eval` to v0.6.1 (workflow `uses:` and `eval_ref`, in lockstep). v0.6.1 parses extraction replies that the model wraps in a ```json fence; since W26 these were stored as `_raw` while the log reported "extract OK" (qte77/gha-rxiv-paper-eval#109).

### Fixed

- `.github/workflows/rxiv-paper-eval.yaml`: the week resolver skips feed CSVs under 1 KB. The feed
  now seeds a header-only file for the new ISO week each Monday; on 2026-11-10 the resolver picked
  that stub (W46), loaded 0 papers and finished green, so W45 was never evaluated.
- `docs/cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`: the Plugin Structure skill
  link pointed at a claude-plugins.dev mirror that now returns 402; it points at the skill in
  Anthropic's official plugin marketplace repo.

- `docs/non-cc/reference/system-1-decision-models-landscape.md` § Strands Decider: Strands' own
  2026-11-09 post documents replacing Claude Sonnet 4.6 for Amazon ticket labelling; the entry
  had wrongly dropped that claim as unsourced.
- `docs/non-cc/protocols/ag-ui-protocol-landscape.md`: the Strands/AgentCore row now notes that
  Strands' own docs list AG-UI only as a community-tier, Python-only page.

- `docs/non-cc/agents/salesforce-agentforce-analysis.md` (plan 0013 A10): applied an independent
  falsification pass. The A2A section now presents a genuine, unresolved contradiction inside
  Salesforce's own documentation (an architecture recipe and MuleSoft's own A2A-bridge guide say
  Agentforce Agents have no direct A2A support; Salesforce's own Agentforce interoperability guide
  says the opposite) instead of treating one side as settled. Switched the primary Flex Credits rate
  card citation to the 2026-11-03 version (new IT/HR Employee Agent Resolutions, Sales, and Slack
  Workspace rows; corrected the Data 360 usage-type count from ten to eleven) and restored the
  verified "Flex Credits and Conversations will not be supported in the same org" FAQ claim. Fixed a
  "Work Summaries" → "Field Summaries" typo, replaced a mischaracterized "two regional copies
  disagreeing" claim with the actual one-page, two-sub-scope wording, added Anthropic's own
  confirmation that "Salesforce in Claude" shipped in beta on schedule, and updated the Hyperforce
  Operating Zone URL after its redirect. Reworded the `CC-business-api-integrations.md` cross-link to
  stop conflating the Agentforce Registry's per-tool risk assessment with Security Center's separate
  tenant-wide MCP Risk Score, and carried the A2A-contradiction framing into
  `agentic-enterprise-os-landscape.md` and `ag-ui-protocol-landscape.md`.

- `.github/scripts/community-monitor.py`, `.github/scripts/lib/monitor_utils.py`: a source whose
  credentials are unset (Reddit, X) is now listed as skipped, with the missing variables, in the
  report and the triage PR, instead of showing as a source that returned nothing. The workflow
  writes the report to the run summary and adds a warning annotation per skipped source (#726).
  A source whose fetch fails is listed the same way (`fetch failed (<exception type>)`) in every
  monitor that uses `run_monitor`.

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: edgextract's library default
  decision model is `nimble` (Bespoke Labs), not `tev1` — the entry had the quickstart's explicit
  `--model tev1` and the README's actual stated default backwards. The JevEval (DeepEval) quote
  is corrected to the source's own wording and capitalization ("You define the logic, Jev makes
  the decisions, and DeepEval calculates the score," not "does the calculation"). The gold-set
  pricing comparison ("about 6× Jev's") is corrected to match the doc's own earlier pricing
  paragraph ("roughly 5.7×" — Clef is 5.7× Jev's rate, not 6×; 6× was only true of Clef-flash).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md`: the Strands Agents entry
  quoted AWS's AgentCore page as saying agents are "built on any framework" — that exact phrase
  appears nowhere on AgentCore's marketing or FAQ pages. Replaced with the page's actual hero-text
  quote, "Build with any framework, any model."
- `docs/non-cc/protocols/ag-ui-protocol-landscape.md`: the AWS Strands Agents / Bedrock AgentCore
  row said the TypeScript AG-UI integration "is still an open PR" — `ag-ui-protocol/ag-ui#1681`
  merged on 2026-05-26, six months before this row's own "checked 2026-11-11" stamp, and ships as
  the `@ag-ui/aws-strands` npm package. Strands' own docs page still says "This feature is only
  supported in Python," which the row now cites directly instead of the stale PR-status claim.
- `docs/cc-community/CC-community-plugins-landscape.md`: the lot-map entry said the Hooks-station
  row removed in 0.4.0 was "restored in 0.5.1" — the repo's own CHANGELOG shows it was restored in
  0.5.0 (0.5.1 only restored a demo video file). Also softened the privacy-claim attribution: the
  verbatim "makes no network requests..." sentence is the README's wording; `PRIVACY.md` states
  the same substance across separate bullets in different wording, not verbatim.

All other checked claims across #782, #786, #787, #788, #795, #797, #779 and #784 (licenses,
star/fork counts, benchmark numbers against the `decision-model-eval.yaml` run artifacts, and
every other quoted sentence) were confirmed against first-party sources and left unchanged.

- `docs/cc-community/CC-code-tooling-landscape.md` (AxiomCode Graph): removed an unsupported claim
  that the repo's topic list carries "open-source"-adjacent framing (no such topic exists);
  corrected the TypeScript call-linking "next-best tool" figure (Code-Review-Graph at 71.6%, not
  GitNexus's 65.1%, which is the next-best for Java only); scoped the "only tool in this doc"
  claim to precomputed-graph tools (Serena, in the same doc, also resolves calls without syntax
  matching, via a live LSP server).
- `docs/cc-community/CC-memory-tooling-landscape.md` (Leviathan): corrected the benchmark citation
  — the memory-benchmark table is sourced from `docs/MEMORY.md`, not solely `docs/BENCHMARKS.md`;
  replaced an imprecise "and 20 more" agent count with the README's own total (24 agents).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md`: corrected a misattributed
  quote on Carrel (the "status rules" / "current and historical views" text is `docs/architecture.md`'s
  framing, not the top-level README's); corrected a wrong absence claim on Kortix CompanyOS — its
  own linked docs (`kortix.com/docs/guide`) name a dedicated Claude Code integration ("Each turn
  runs through Claude Code, Anthropic's own program, on the session's computer"), not merely a
  generic MCP connector; softened RAGFlow's "four thinking-effort tiers" claim with a note that the
  v1.0.0 release notes describe this as replaced by an "Agentic Chat" mode, even though the live
  README's Key Features section still listed the four tiers as of 2026-11-12.
- `docs/non-cc/knowledge-management/research-agents-landscape.md` (Épi): corrected "5.4 points
  higher than Codex" to the paper's own wording, "a 5.4% higher total benchmark score than Codex."
- `docs/sdlc-lcm/software-factory-landscape.md` (Anthropic/Scion): replaced a fabricated quote —
  "the limit moved from writing code to the surrounding systems" does not appear in Anthropic's
  source-control post — with its actual verbatim sentence ("The bottleneck, now, is all of the
  developer infrastructure built for human scale: source control, builds, and CI").
- `docs/cc-native/configuration/CC-models-reference.md` (Fable/Mythos 5.2): restored "Claude" in
  the quoted CVE-rediscovery sentence ("10.2% more vulnerabilities than Claude Opus 5.5 and 14.4%
  more than Claude Mythos 5.1"), which the merged PR had silently dropped from a quoted string.

Adversarial falsification pass on the 2026-11-12 PRs #790 and #791 (research-subagent content,
spot-checked only at merge time): 8 repos (metadata, LICENSE, README and cited docs files), 3 arXiv
abstracts, 3 CC CHANGELOG entries, GitHub issue #107757, and 7 Anthropic/claude.dev/Kortix web pages.
Every other claim checked in this pass was confirmed; not independently re-checked: MemoProAgent's
granular benchmark figures beyond its headline numbers, the three arXiv "no code repository found"
claims (checked only on the abstract page, not site-wide), one secondary detail on the Nonprofits
Design Partner Circle, the hillclimb revert-logic paraphrase, and one CortexDB live-view detail
(`serve_graph_3d`).

- `docs/non-cc/reference/weco-aide-recursive-self-improvement-analysis.md` § InfraRSI: the
  "two-level self-improvement loop" line was a paraphrase dressed as a direct quote; replaced with
  the abstract's actual wording ("a two-level Recursive Self-Improvement loop" / "revising priors
  online within runs and distilling experience across clusters").
- `docs/cc-community/CC-code-tooling-landscape.md` § Floorplan: `Version: 0.7.3` was already one
  release behind at check time — the project's own `plugin.json`/`CHANGELOG.md` show `0.8.0`,
  published the same day (2026-11-12).
- `docs/cc-community/CC-community-tooling-landscape.md` § cogit: corrected a wrong "single-agent,
  works with Claude Code today, no other harness documented" claim and its unsourced quote — the
  README documents Claude Code *and* Codex CLI as supported harnesses, each with its own install
  path, plus a Node 22.13+ requirement the entry omitted.
- `docs/cc-community/CC-community-plugins-landscape.md` § Impeccable: the Claude Code install step
  cited a `/plugin install impeccable@pbakaus-impeccable` command that doesn't appear in the
  README (which instead says to open `/plugin` and install Impeccable); and the live-mode caveat
  misattributed the README's "review it before using live mode in an unfamiliar repo" warning —
  that sentence is about the separate `impeccable:manual-edit-validate` script, not the
  bypass-approvals-and-sandbox fallback it was attached to.
- `docs/sdlc-lcm/agent-code-analysis-landscape.md` § OpenQodex: fixed a non-verbatim quote
  ("who calls this function" → the README's actual "who calls a function").
- `docs/sdlc-lcm/ai-security-governance-analysis.md` § Tracekit: corrected a mischaracterized demo
  description — the README's tamper demo rewrites a logged "deny" decision to "allow" in a copy of
  a verified run, not "an agent editing its own log... to hide a deletion."

All other claims added by #792 and #793 (paper facts, author lists, star/fork/license figures,
README quotes and numeric self-reports across DUET, MCP-Injector, LifeVal, MiniCorp, Harness²,
RSI-Dojo, InfraRSI, Self-HPO, Adaptive Skill Granularity, Skill++, Memento 3, Sharpening Tax,
OpenHuman, Elephant-Goldfish Model, Stroq, Tracekit's own metrics, devvm, Grim Prompter, OpenQodex's
other claims, Waza, ToolCallJudge and claude-seo's refreshed counts) were checked against the
arXiv abstract pages, `gh api`, and project READMEs and are confirmed as written.

- `docs/cc-native/plugins-ecosystem/CC-cowork-plugins-enterprise-analysis.md`: second, independent
  adversarial re-check of the Microsoft new-products content (#799) and its first falsification
  pass (#803). Fixes a verbatim-quote mismatch in the Cowork disambiguation note — Microsoft's
  announcement blog says it "integrated the technology behind Claude Cowork into Microsoft 365
  Copilot" (confirmed against the blog), not "built 'integrat[ing] the technology...' into"; the
  stray "built" and the wrong `[ing]` bracket are removed and the quote now matches the sibling doc
  (`microsoft-365-copilot-analysis.md`), which already had it right.
- `docs/non-cc/frameworks/agentic-enterprise-os-landscape.md`: fixes a misattributed citation — the
  Copilot Studio row cited its own `what's new` page for the GitHub→Microsoft Copilot harness
  rename, but that page (fetched fresh, content-dated 2026-11-04) still calls it the "GitHub
  Copilot harness" throughout and never states a rename. The rename is documented on Microsoft's
  billing/licensing FAQ page ("Apps are built with the Microsoft Copilot harness (formerly the
  GitHub Copilot harness)"), which is now cited instead, with a note that the what's-new page
  hasn't caught up.
- `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: two minor quote-fidelity fixes applying
  the bracket convention #803 itself established for a quoted fragment's capitalization — two
  quotes ("a list of objects…", "a plugin can include…") silently lowercase a source sentence's
  capital first letter without the bracket the doc uses everywhere else for this ("[A]n optional…",
  "[c]an be created…"); both now read "[a] list…" / "[a] plugin…" for consistency. Also softens an
  evidence-level overstatement: "Home and Code began rolling out to Frontier" and "Autopilot
  expanded to private preview" stated as completed fact, sourced only to the 2026-09-25 blog post
  that *announces* both for "the coming weeks" / "the end of the month" — now "were slated to"
  with a note that the cited post announces rather than confirms shipping.

All other #803 fixes and a broad sample of #799's "confirmed" claims (Cowork/Code/Managed
Runtime/Researcher/Analyst/Agent 365 SDK model names, dates, caps, and quotes) were re-verified
against freshly fetched first-party Microsoft pages and held up.

- `microsoft-365-copilot-analysis.md`: two stray "93-claim" references corrected to "85-claim" to
  match the Results table (no other page in the corpus corroborates a 93-claim combined total).

- `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: adversarial re-check of the 2026-11-12
  Microsoft new-products pass (#799) against every cited first-party page. Corrects two
  misattributed citations (the declarative-agent build-tooling claim cited `da-overview` instead
  of `da-agents-overview`, in both the prose and the Build paths table), an overstated "public
  preview" claim for Microsoft Copilot Managed Runtime that no cited page actually uses (the
  09-25 blog and the overview page both say only "preview"), a wrong structural claim about where
  the manifest's Worker agent object sits relative to `agent_skills` (earlier on the page, not
  "two sections later"), and three small verbatim-quote mismatches (a silently dropped "(Model
  Context Protocol)" expansion, a capitalization change inside a Foundry harness quote, and a
  "This is a preview feature" claim applied to a page that actually reads "This feature is in
  preview"). Also softens an unsupported "FAQ pages" reference for Foundry hosted agents to the
  one Learn page actually fetched.
- `docs/non-cc/frameworks/agentic-enterprise-os-landscape.md`: same "FAQ pages" softening for the
  Foundry hosted-agents caveat.

- `docs/non-cc/reference/weco-aide-recursive-self-improvement-analysis.md` § Sharpening Tax: the
  2026-10-06 "no code repository" note was stale — `changdaeoh/sharpening-tax` now exists
  (CC BY-NC 4.0).

- `docs/cc-native/examples/statusline.sh`: check that `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` is numeric and pass it to awk with `-v`, instead of interpolating the env var into the awk program.

- `.github/scripts/build-rxiv-index.py`: recover paper summaries, methods and findings that the triage action dropped into `_raw` since 2026 W26 (the extraction model wraps its JSON in a ```json fence, which the action's strict parser rejects). The cumulative index now shows summaries for 1,162 of 1,919 papers (was 53). Replies cut off at the token limit or with invalid JSON stay empty.

- `.github/scripts/lib/status_incidents.py`, `.github/workflows/cc-status-monitor.yaml`: the status monitor read `status.anthropic.com`, which has answered the weekly run with HTTP 403 since 2026-08-24, and the step swallowed the error, so 12 runs went green without collecting anything. It now reads `status.claude.com` (same Statuspage API) and fails the run on any collector error.

### Dropped (researched, not added)

- RoboArchitect (arXiv:2610.42141) and JIT-Agent (arXiv:2608.25593): both are agent-harness
  design/evolution papers in which persistent memory is a secondary feature, not the core
  contribution — out of this corpus's memory/KG/code-graph/search/RAG scope.
- Memento: already covered in `agent-frameworks-infrastructure-landscape.md` §4.
- Two owner-screenshot infographics (token-cost optimization; six AI-harness terms): no URL to
  verify at first-party.

## [0.19.0] - 2026-11-09

### Added

- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: idle compaction — Claude Code compacts
  a 200K+ token session left idle for about 54 minutes before its one-hour prompt cache expires
  (`idleCompaction`, default on, v2.1.290+ setting; feature history 2.1.299–2.1.318 from the
  changelog). New env var row `CLAUDE_CODE_IDLE_COMPACT_MIN_TOKENS` in `CC-env-vars-reference.md`;
  cross-link from `CC-extended-context-analysis.md`.

- `docs/non-cc/infrastructure/semantic-layers-data-catalog-landscape.md`: JSON-LD 1.1 in the Formal
  Ontologies section (W3C Recommendation; JSON form of Linked Data, usable as RDF), why agents meet it
  (schema.org markup, Google's JSON-LD recommendation), and YAML-LD (W3C Working Draft) behind Vault-LD.

- `.github/scripts/lib/m365_drift.py`, `.github/scripts/m365-drift-monitor.py`: a watched entry may carry
  an optional `due` date (YYYY-MM-DD); the weekly M365 drift monitor now flags it once that date has
  passed, even when the page's `ms.date` and quote are unchanged (the 2026-10-31 retirement went
  unflagged). The state file keeps extra fields across runs (`build_new_state`). Tests in
  `tests/test_m365_drift.py` (8 new). Closes the remaining #705 items.

- `make reconcile` (`.github/scripts/plan-reconcile.py`, `.github/scripts/lib/plan_reconcile.py`,
  `tests/test_plan_reconcile.py`, 13 tests): reads the newest plan's remaining-work table, looks up
  every cited PR/issue in any repo through `gh`, and flags open rows whose PRs are all merged/closed,
  struck rows with an open reference, and references it could not check. References in backticks are
  treated as context. Documented in `CONTRIBUTING.md`; plan 0012's "How to run it" now starts with it.
- `AGENT_LEARNINGS.md`: the stale-gate recurrence (D0/C1 merged 2026-10-24, read as blocked until
  2026-11-09) and the update-branch-before-merge pattern.

- `.github/workflows/plan-reconcile-monitor.yaml`: weekly `make reconcile` (Monday 14:00 UTC) that
  opens or updates a single `plan-drift` issue while any row of the newest plan disagrees with the
  live state of the PRs/issues it cites, and closes it once every row agrees. A failed `gh`
  preflight fails the job instead of filing an issue. Documented in `docs/architecture.md`,
  `AGENT_LEARNINGS.md` and plan 0012.

- `docs/cc-native/agents-skills/CC-dynamic-workflows-analysis.md`: "Collecting results" — where a
  workflow run's run record and journal land on disk, what each holds per run outcome, and why a
  `completed` run can still miss agents (observed CC 2.1.316/2.1.319, undocumented; #743).

### Changed

- `.github/state/m365-drift-state.json`: `due` dates on the 2026-11-12 and 2026-12-01 entries; new
  watched quotes for the 2026-11-01 PowerShell retirement and the structured-document-generation GA
  roadmap feed.
- `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: the 2026-10-31, 2026-11-01 and October GA
  timeline rows marked passed, with what the pages said on 2026-11-09 (none confirms the event).

- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: rules in parent folders load in practice
  but are undocumented (observed CC 2.1.303); symlinked rules outside the working directory are
  documented as external imports needing approval, with an observed headless exception for
  `~/.claude/rules/`; project settings files are read from the working directory (local file: git
  root). Plan 0001 row 6 done.

- `docs/plans/2026-10-10-0012-decision-models-estate.md`: cross-repo references made explicit
  (C1, P2, Q1), history references marked as context; R10 struck (qte77/qte77 commits verified since
  2026-11-02).

- Plans 0001, 0007–0012 and the `adding-research-source` skill: merge-bypass flags and token-unset
  command prefixes reworded in plain language (owner rule 2026-11-09: no operator commands in public
  files).

- `docs/cc-native/configuration/CC-tools-inventory.md`: `idleCompaction` listed among the settings-file
  keys, linking to the idle-compaction section of the prompt-caching doc.

- `docs/architecture.md`, `README.md`, `docs/UserStory.md`: `make reconcile` (plan rows vs live
  PR/issue state) and the M365 drift monitor's `due` dates documented; the workflows line in the
  directory map now lists the health monitors, release and Pages workflows.

### Fixed

- Dead links from the link-rot report (#748): Ephemora Cell now cites its PyPI v1.0.4.2 release (GitHub
  repo gone; test/coverage figures corrected to the README badges, star count dropped);
  OpenResearch platform requirements cite openresearch.sh/docs/install (repo `docs/` removed);
  Visa Intelligent Commerce cites Visa's 2025-04-30 press release (partner quote corrected); the
  unsourced Skywork review (CodeBuddy) and Lushbinary frontmatter source were removed — no claim
  depended on them alone.

## [0.18.0] - 2026-11-09

### Added

- `docs/cc-native/configuration/CC-advisor-tool-analysis.md`: first-party coverage of Anthropic's
  advisor tool — the `advisor_20260301` API beta (`advisor-tool-2026-03-01` header) that lets an
  executor model consult a stronger advisor mid-request — covering tool parameters, model
  pairing, billing/usage accounting, the Claude Code `/advisor` surface, and an unresolved
  platform-availability conflict between the API and Claude Code docs on Claude Platform on AWS.
- `docs/cc-native/configuration/CC-env-vars-reference.md`: `CLAUDE_CODE_DISABLE_ADVISOR_TOOL` is
  now documented (was binary string-extraction only).
- `docs/cc-native/configuration/CC-tools-inventory.md`: `/advisor` slash command and
  `advisorModel` settings.json key.
- `docs/cc-native/configuration/CC-cli-reference.md`: `--advisor` hidden CLI flag.
- `docs/cc-community/CC-community-reimplementations-landscape.md`: note that the leaked
  `advisor-tool` beta header shipped as `advisor-tool-2026-03-01`.

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

- `docs/non-cc/infrastructure/semantic-layers-data-catalog-landscape.md`: NVIDIA Auto Ontology
  (Apache-2.0) — LLM-drafted, human-certified business ontology over relational sources in
  Postgres + pgvector, SQL-only text-to-SQL agent, read-only MCP server; ingestion-auth caution; not
  rubric-scored (gap-driven policy). Hub row in `docs/_topics/knowledge-graphs.md`.
- `docs/non-cc/infrastructure/web-scraping-extraction-landscape.md`: agent-desktop (vercel-labs,
  Apache-2.0, v1.2.0) as the desktop counterpart of accessibility-tree browser automation — OS a11y
  APIs on macOS/Windows/Linux, headless refs, skill + MCP server. `jev-desktop` skill listed under
  Tools built on Jev in `system-1-decision-models-landscape.md`.

- `docs/cc-community/CC-community-tooling-landscape.md`: TokenEconomizer (microsoft, Apache-2.0,
  v0.1.0, arXiv:2610.22732) — cross-session cost control via plugin hooks (micro-skills, tool pruning,
  loop guard); new layer 6 in the Token-Waste Reduction Stack and a Comparison row.

- `docs/non-cc/infrastructure/microsoft-mxc-analysis.md`: Microsoft MXC (Execution Containers; MIT,
  v1.0 GA 2026-10-07) — cross-platform sandbox SDK for agent-generated code: AppContainer/WFP process
  container on Windows, Bubblewrap on Linux, Seatbelt on macOS; closed, deny-by-default JSON policy;
  Enforcement/Learning/Permissive modes; Required telemetry in the 1.1.0-alpha contract. Claude Code
  support is a Microsoft announcement only. Indexed in `docs/non-cc/README.md`; linked from
  `CC-sandboxing-analysis.md` (Windows row) and `nvidia-openshell-analysis.md`.

- `docs/non-cc/coding-agents/zed-analysis.md`: Zed as an agent host — Zed Agent, external agents over
  ACP (Claude Agent runs the Claude Agent SDK via `agentclientprotocol/claude-agent-acp`), terminal
  threads, the ACP configuration boundary, ACP spec status (stable protocol version 1), Zeta edit
  predictions; GPL-3.0-or-later + Apache-2.0. Indexed in `docs/non-cc/README.md`; linked from Goose's
  ACP section.

### Changed

- `docs/cc-native/ci-remote/CC-web-auth-setup-analysis.md`: refreshed the authentication precedence
  table to 7 entries (was 6), adding "Anthropic profile and federation credentials" between
  `CLAUDE_CODE_OAUTH_TOKEN` and subscription OAuth; added the docs' own `-p`-mode nuance ("the key is
  always used when present", no approval prompt); new subsection on confirming which org/workspace a
  key resolves to via response headers, and on scoping an `apiKeyHelper` key to headless runs only.

- `docs/cc-native/agents-skills/CC-cross-session-messaging-analysis.md`: added the observed
  `notify_when_idle` notice wording (session-registry check for the one-line status detail) and a
  new "In Practice" section of peer-messaging observations.

- `docs/cc-native/sessions/CC-print-mode-gotchas.md`: new "Unattended Headless Lanes" section —
  project `permissions.allow` rules waiting on workspace trust (never shown in `-p`), a stale
  `GH_TOKEN`/`GITHUB_TOKEN` shadowing `gh` auth, the `--permission-prompts none` flag, and a `/goal`
  headless run reporting success with an empty `result`. Also adds the file's first `## Sources`
  section.

- `.github/workflows/rxiv-paper-eval.yaml`: pinned gha-rxiv-paper-eval v0.5.1, so a weekly run whose
  every relevance call fails (as W42 did on an expired token) now fails the job instead of ending
  green with no triage PR.

- `docs/cc-native/configuration/CC-models-reference.md`: replaced the stale "Fable 5 (newest model)" framing and
  "Opus-tier $5/$25" comparison with the current per-model price table (Fable/Mythos 5.1 and 5, Opus 5.5 down
  through 4.5, Sonnet 5.5/5/4.6/4.5, Haiku 5.5's two prompt-length tiers, Haiku 4.5) from the pricing page, and
  noted Sonnet 5's $2/$10 per-MTok rate is now standard, not introductory.
- `docs/cc-native/sessions/CC-session-cost-analysis.md`: fixed a doubled `docs/` segment in the pricing-page link;
  replaced the duplicated Opus/Sonnet/Haiku 4.6 price table with a pointer to CC-models-reference.md.
- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: replaced the flat 0.1x cache-hit multiplier with
  the per-model tiers (0.025x Fable/Mythos 5.1, 0.05x Opus/Sonnet 5.5, 0.1x others); requoted the Bedrock/Google
  Cloud cache-isolation sentence, which was no longer verbatim against the current prompt-caching docs.

- `docs/cc-native/configuration/CC-fast-mode-analysis.md`: refreshed against the Claude Code and API
  fast-mode pages (2026-10-26) — Opus 5.5 (GA on the API) / Opus 5 / Opus 4.8 supported, Opus 4.7
  removed; Claude Code default history (v2.1.154 / v2.1.219 / v2.1.280); API `speed` parameter, beta
  header, rate-limit headers and 429 behaviour vs Claude Code's auto-fallback; fast = exactly 2x
  standard price; no Batch API / Priority Tier; VS Code toggle; the two pages' platform lists
  recorded side by side.
- `docs/cc-native/configuration/CC-tools-inventory.md`: `fastMode` row no longer says "Opus 4.6 only".

- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md`: Hallucination Detection now cites Anthropic's
  help-center article on incorrect or misleading responses (vendor acknowledgement, verbatim quotes,
  read 2026-10-26).

- `docs/cc-native/sessions/CC-goal-analysis.md`: new "Measured: headless batch runs" section from
  two batches of `claude -p "/goal …"` runs against task files (20 runs on 2026-10-24, 17 on
  2026-10-29). Every run's result metadata read `success`/`completed` whether or not the goal was
  met, the final message was empty in 13 of 37 runs, `permission_denials` were recorded without
  ending any run, and a cloud `/goal` over 4,000 characters left the session idle. The task-list
  pattern is no longer marked untested.

- `CONTRIBUTING.md`: Commit & PR asks vendor-affiliated contributors to disclose the affiliation, keeps existing doc
  titles, index rows and `status` maintainer-owned, and states that `main` requires signed commits.

- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: the effort-vs-cache "two statements"
  are reconciled — Claude Code's gateway guide documents that CC sends per-turn effort as
  `output_config.effort` on `role: "system"` entries (the API's per-message-effort exception, beta
  `mid-conversation-output-config-2026-07-01`).
- `docs/cc-native/configuration/CC-fast-mode-analysis.md`: platform lists reconciled (Google Cloud's
  Agent Platform is the Google-managed product, not the Anthropic-managed one; Foundry fast mode is
  API-only, not in Claude Code); Opus 4.8 fast mode deprecated 2026-10-30, removal 2026-11-30; both
  pages now label Opus 5.5 available; Ultra plan name; status `available`.
- `docs/cc-native/configuration/CC-advisor-tool-analysis.md`: platform "conflict" resolved (Claude Code
  disables the advisor on Claude Platform on AWS; the API page dropped its not-available sentence);
  compatibility table is 12 entries / 14 models; Haiku 5.5 is an accepted advisor; Haiku 4.5's
  executor-only role is stated in the Claude Code docs.

- `docs/cc-native/agents-skills/CC-skills-adoption-analysis.md`: `anthropics/skills` refreshed (19 skill
  folders, five-plugin `anthropic-agent-skills` marketplace, spec moved to agentskills.io, per-skill
  licensing, 190.3k★ on 2026-11-09).
- `docs/cc-native/plugins-ecosystem/CC-office-document-skills.md`: the docx/pdf/pptx/xlsx skills moved
  from a proprietary license to Apache 2.0 on 2026-11-06; marketplace install commands added.

- `docs/cc-community/CC-memory-tooling-landscape.md`: Claude-Mem refreshed to v15.13.0 / 115.2K stars —
  cross-agent adapters, 9 Claude Code hook events, per-user worker port `37700 + (uid % 100)`, hosted
  observer option, telemetry on by default; RAD protocol no longer in the README; unsourced
  "largest community memory solution" claim dropped.

- `docs/non-cc/coding-agents/deepseek-harness-analysis.md`: dsh-superagent prototype (MIT, 2026-10-31) —
  a proactive one-repository coding agent bundled for DeepSeek Harness: GitHub/Feishu triggers,
  router + per-Ticket worker sessions, 5 s / 30 min execution limits, no sandbox (runs as the operator's
  OS user); press-reported article figures left out (no first-party copy).
- `docs/plans/2026-10-10-0012-decision-models-estate.md`: N12 (owner leads 2026-11-09) shipped.

- `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: re-read the Microsoft "Claude models from
  Anthropic" page after its 2026-11-04 revision (drift report #749) — quotes now say "Claude models";
  added the commercial-cloud default-on statement, the EU/EFTA/UK re-opt-in requirement, the
  sovereign-cloud exclusion, and the two-year / seven-year retention for flagged Data Retention content.

- `docs/non-cc/coding-agents/opencode-analysis.md`: Anomaly's Rune UI framework (MIT, pre-release;
  recreating OpenCode Desktop is its announced flagship test).

### Fixed

- `.github/scripts/learnings-aggregator.py`: change detection now hashes the upstream
  `AGENT_LEARNINGS.md` instead of the rendered mirror, whose `updated:` date changed every run, so
  the weekly job no longer opens a date-only PR. The first run after this lands rewrites the state
  file once.

- `docs/cc-community/CC-community-plugins-landscape.md`: unlinked `bacharyehya/talk-to-claude`, whose repo
  now returns 404, so the repo-wide link check passes again.
- `docs/non-cc/context-memory/mitosis-cortex-analysis.md`: `verginglabs.com` now returns 404; the Verging
  Labs citation points to its 2026-10-12 Wayback snapshot instead.
- `lychee.toml`: excluded the one Constellation Research article cited in `kiro-analysis.md`; it returns
  403 to CI runners but loads normally elsewhere.

- `docs/cc-native/configuration/CC-env-vars-reference.md`: configuration precedence was wrong —
  environment variables aren't a settings level, `--settings` is the only command-line level, and a
  settings `env` block overrides the same variable exported in the shell in most sessions; listed the
  variables project/local files can't set. `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` no longer claims a
  documented ~95 % default.
- `docs/cc-native/examples/settings.json`: eight `Bash(git:<sub>:*)` rules matched nothing (`:*` works
  only at the end of a pattern) — including the `git push` deny and `git commit` ask; rewritten as
  `Bash(git push *)` etc., read-only git allows dropped (built-in read-only set).
- `docs/cc-native/configuration/CC-bash-mode-analysis.md`, `docs/cc-native/sandboxing/CC-permissions-bypass-analysis.md`:
  stopped recommending `Bash(git *:*)` / `Bash(git *)` / `Bash(make *)`; the permissions docs say to put
  the `*` after the subcommand (a leading `*` also matches injected options such as `git -c`).
- `docs/cc-native/configuration/CC-tools-inventory.md`: "Precedence unclear" answered for
  `respectGitignore`; the `fastMode` `.claude.json` cell and the VS Code key marked unverified.
- `CC-remote-control-analysis.md`, `CC-model-provider-configuration.md`: `.claude/settings.local.json`
  isn't automatically gitignored when created by hand; three dead settings-page anchors repointed.
- `docs/cc-native/sessions/CC-print-mode-gotchas.md` (observation, 2026-10-29): strip
  `GH_TOKEN`/`GITHUB_TOKEN` per `gh`/git network call, not for the whole `claude -p` process — the
  Codespaces commit signer needs `GITHUB_TOKEN`.

## [0.17.0] - 2026-10-24

### Added

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: Microsoft-Decision-1 (Microsoft
  Foundry, released 2026-10-09) — a Qwen3.5-9B-based decision-scoring model using Jev's own
  `noul`/`choice`/`score` vocabulary over a `/v1/systemone` endpoint. Flags a status conflict
  between the launch blog ("public preview") and the Foundry catalog ("Generally available (GA)"),
  and a second conflict between two Microsoft blogs' numbers for the same Xbox Research case study
  (GPT-5/80–100x vs. GPT-6 Sol/14x). Decodes the launch post's embedded chart data to recover
  per-model accuracy/latency/calibration figures its own prose omits — on calibration,
  Microsoft-Decision-1 ranks third behind Jev and Quyet-1.0-Large. Narrows (without closing) the
  model-routing, tool-call-gating, and reranking gaps in § Use cases.

- `.github/scripts/data/gold/`: two independently-labelled gold sets for relevance decisions
  (plan 0012 row G1) — 100 arXiv papers under the agent-strict criterion
  (`AGENT_STRICT_PROMPT` in `.github/scripts/lib/relevance_eval.py`), reconstructed exactly from
  the production top-100 candidate pool, and 62 GitHub issues across 8 qte77 repos under the
  inverse of `gha-issue-triage`'s `irrelevant` predicate. Each set ships an unlabelled items file
  plus a labels file, labeller "agent pass 1"; a blind second pass and reconciliation follow.

- `docs/_topics/harness.md`: the system-1 row names the JevSpawn paper.

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: JevSpawn (arXiv:2610.00437,
  Fudan/SJTU/Shanghai Innovation Institute) — a compositional-action-space agent policy that
  extends the Jev-style finite-field interface (fields inferred per branch, not predefined); its
  default pipeline runs on Qwen3.8-27B, not Jev, but the paper measures a "TypeSafe Jev variant"
  head-to-head against it across eight benchmark tasks: roughly comparable task quality but
  "1.4 to 2.1 times" the latency on every task. Code released, no `LICENSE` file. Added to
  § Use cases › Tool-call gating.
- `docs/non-cc/infrastructure/jev-analysis.md`: one-line Cross-References pointer to the new
  JevSpawn section — the corpus's first measured (not self-reported) latency/quality comparison
  of Jev itself inside an agent's next-action loop.

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: Cloudflare Clef / Clef-flash /
  clef-omni (Workers AI, launched 2026-10-01/10-09) as a fourth major-vendor Jev-style decision
  model, and Unsloth's "train your own decision model" path (`FastDecisionModel`/`DecisionTrainer`,
  v0.1.904-beta) as a new "Train your own" section connecting Clef's head design, Laya's local
  serving, and the `LocalLLaMA/typed-decisions` dataset. Reconciles Clef's launch blog claim of
  leading "the Jev Decision Index" against its own HF cards' "internal run" label, and the blog's
  10-benchmark table against the cards' wider table where Jev leads on general-reasoning rows
  (GPQA Diamond, MMLU-Pro, BBH). Narrows (without closing) the §4 Reranking gap with Clef's own
  nDCG@10 numbers on ToolRet and BRIGHT.

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: AnyJev (nokia-applied-research —
  Nokia/Tencent Hunyuan/HK PolyU, Apache-2.0, arXiv:2610.00831) as a new open-weight Jev-family
  entry — training-free `Decider`/`L0` plus self-distilled `Tacit` checkpoints and a `POST
  /v1/decide` gateway, with its `state`+`questions`/`state`+`question` API shape compared against
  the System One vocabulary and its benchmark numbers marked self-reported — and
  typesafe-computer-use (awlevin, MIT) in §3 Tool-call gating as a macOS computer-use agent driven
  by the real, hosted TypeSafe Jev model, with its cost/latency table flagged as a single
  maintainer's single-task measurement.

- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md`: five sources (plan 0012
  row N1) — OpenRig (YAML-defined persistent agent teams over Claude Code/Codex, with Pi/Oh My Pi
  as a documented third runtime) and TrueForge (open-source agent harness benchmarked against
  Claude Managed Agents and deepagents, no figures in its own README) in §1; AECP
  (arXiv:2610.06481, artifact-exclusive multi-agent communication, cross-ref'd to
  `mas-security-framework.md`'s Layer 1 prompt-injection mitigation) in §1; MemoType/TriMEM
  (arXiv:2610.11573, typed memory-retrieval routing) as a sibling to the Weighted Memory
  Tree/JITMEM cluster in §4; and GraphJin (GraphQL + MCP governed data access for agents, since
  2019 — explicitly flagged as data access, not a knowledge graph) in §7's agent-native graph
  platforms. Disambiguates `mvschwarz/openrig` from the unrelated `openRigProject/openRig`
  ham-radio repo.

- `docs/cc-community/CC-community-skills-landscape.md`: `wheresryan22/anatomy`, a Claude Code Agent
  Skill (`SKILL.md`, no plugin marketplace) that turns a technical idea into an audited, interactive
  isometric SVG/WebGL/3D figure of a real machine (MIT, 3,109 stars, 3 days old).
- `docs/cc-native/configuration/CC-model-provider-configuration.md`: a `#### Strata` entry under
  Local Models — a local Qwen3.8-Flash-Next inference engine that documents a Claude Code
  `ANTHROPIC_BASE_URL` setup for its Anthropic-compatible endpoint verbatim in its own README (MIT,
  21,540 stars), plus a separate setup/ops MCP server distinct from the inference endpoint.

- `docs/non-cc/infrastructure/web-scraping-extraction-landscape.md`: moli (lexmount; from-scratch
  Rust headless-browser kernel for AI agents, dual MIT/Apache-2.0, CLI/CDP/WebDriver Classic/BiDi,
  agent skills) next to the Lightpanda entry, with moli's own vendor-reported benchmark comparison
  against Lightpanda.
- `docs/sdlc-lcm/agentic-ai-vulnerability-landscape.md`: Uber ADR (Agentic AI Detection and Response;
  Apache-2.0, open source, MLSys 2026 Industry Track paper arXiv:2605.17380) as a new row and
  subsection alongside Secure Agentics Adrian and Microsoft MDASH; production-deployment and
  benchmark figures marked self-reported.
- `docs/non-cc/knowledge-management/research-agents-landscape.md`: IdeaScientist (arXiv:2610.04074),
  an RL-trained gap-finding/innovation/report-writing agent pipeline for research ideation, as a new
  §1 bullet.
- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md`: "What Does a Harness Buy? Tokens, Mostly"
  (arXiv:2610.04433) under the Cost-Performance Efficiency (Pareto) metric — holding the model fixed
  across Claude Code/mini-SWE-agent/OpenCode on SWE-bench Verified, harness choice barely moves score
  but changes cost per task by up to 3x; new `docs/_topics/harness.md` row for this doc.
- `docs/non-cc/infrastructure/rea-analysis.md` (new doc): REA (morluto/rea), an MCP server/CLI giving
  coding agents reverse-engineering tools for native binaries, JS/Electron apps, .NET assemblies and
  websites; MIT, multi-agent (Claude Code, Codex, Cursor, Gemini CLI, Grok Build). No existing
  landscape fit its subject (reverse-engineering third-party software, not CC internals or
  agent-code security scanning), so this is a new standalone doc.
- `docs/non-cc/context-memory/minigraf-analysis.md` (new doc): Minigraf, an embedded bi-temporal
  Datalog graph database (Rust/Python/WASM/mobile, dual MIT/Apache-2.0) pitched as agent memory;
  notes that its cited "third-party" agent-memory demo is the maintainer's own project (same name in
  the LICENSE-MIT copyright and the Maven Java/JVM group ID). Added to all three
  `docs/_topics/{knowledge-graphs,memory,rag}.md` hubs following the HelixDB/LatticeDB convention.

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: the Artificial Analysis Decision
  Index v1.0 (third-party benchmark, launched 2026-10-13) — composition (four 25%-weighted evals:
  AA-Omniscience-Decision, HLE-MultiChoice, When2Call, WildGuardTest), the full 13-decision-model
  comparison table (cost, latency, sub-scores) reconciled against the live leaderboard's own
  embedded data (including its own `defaultSlugs` field, which distinguishes AA's "default" 11 from
  the 2 it excludes — Jev 1.13 and Clef-Flash), per-eval leaders, LLM baselines (Claude Haiku 5.5
  Low, GPT-6 Luna Low), and calibration notes from the launch article's own frozen snapshot.
  Explicitly distinguishes this from the unrelated community "Decision Index"
  (`multimodalart/jev-decision-index`) already cited for Perplexity's pplx-decider, Fastino's
  GLiDE, and Liquid AI's d1. Adds four decision models new to this corpus, named in the AA legend:
  GLiDE (Fastino Labs, a separate "thinking" model distinct from GLiNER2.5-Decide, confirmed via
  Fastino's own comparison-table post), Celeris-1 Decision (Celeris Labs, diffusion-based, hosted
  only — "no open weights and no fine-tuning in this release"), d1 (Liquid AI, hosted + open-weight
  `d1-3B`/`d1-omni-600M` under a custom `lfm1.0` license, plus the same-day `d1-ultra` launch, now
  the index's top scorer), and Mercury Decide (Inception Labs, hosted-only, documented only at
  `docs.inceptionlabs.ai`, no mention on the company's own homepage or blog). Flags a contrast
  between GLiDE's self-reported lead over Jev on the community index (64.81 vs. 57.91) and its
  materially different, lower score on the independent AA index (53.91, below either tracked Jev
  version).

- `docs/cc-native/sandboxing/CC-sandbox-platforms-landscape.md`: Maritime (Maritime AI, Inc.,
  Delaware) — Firecracker-microVM hosting for persistent agents — as a new column in the Platform
  Comparison table and a subsection alongside Blaxel/forkd; boot/wake timings and pricing marked
  self-reported.
- `docs/sdlc-lcm/evaluation-data-resources-landscape.md`: Ora (era labs) and Lightsage as the first
  two vendors in a new "agent-readiness scoring for websites/APIs" category in §2 Benchmarks —
  Ora's site-scan research numbers and Lightsage's Agent Experience Arena/DevTool Arena method and
  sample size, both marked self-reported and dated.
- `docs/non-cc/protocols/agentic-payments-landscape.md`: Lightsage's Agent Experience Arena —
  Payments as a live adoption tracker for x402/MPP/UCP/ACP/AP2 (2,369 companies, 0
  sandbox-verified-or-better); adds ACP (Agentic Commerce Protocol, OpenAI + Stripe,
  agenticcommerce.dev) as a new protocol row with an explicit disambiguation from the corpus's other
  "ACP" usages (Agent Client Protocol, Agent Connect Protocol). UCP left unexpanded — no first-party
  definition found.
- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md`: Artificial Analysis's Coding Agent Index
  (v1.5) and Endpoint Accuracy Index (BFCL v4-500 tool-use weighting) as a Landscape Reference under
  the Cost-Performance Efficiency (Pareto) metric — both have first-party methodology pages; the
  Decision Index is explicitly out of scope here (tracked separately against
  system-1-decision-models-landscape.md).

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

- `docs/cc-native/ci-remote/CC-web-auth-setup-analysis.md`: extends §3 (plan 0012 row N3/lane G2) with
  the Claude Console platform-admin surface a headless org API key touches — the two unrelated quota
  systems (claude.ai weekly/five-hour pool vs. Console pay-as-you-go) and the auto-created Claude Code
  workspace that bridges them; the three API key types (personal, service account, legacy workspace);
  the `anthropic-workspace-id` header requirement for a multi-workspace key, its 400 error, and the
  `ANTHROPIC_CUSTOM_HEADERS` (CC v2.1.227+) workaround since Claude Code has no native workspace-id
  flag for a plain Console key; why claude.ai connectors go dark under API-key auth, quoting the CC MCP
  docs directly; org-level rate limits and spend caps (Start/Build/Scale/Custom tiers) distinct from the
  claude.ai weekly pool; the Usage and Cost Admin API; API data retention for Claude Code (ZDR scope,
  the 6-year server-side transcript retention vs. the local `cleanupPeriodDays` setting, HIPAA
  exclusion); a pointer-only, verbatim-quoted citation of the Usage Policy's agentic-use clause; and
  one-line notes on Batch processing, the Files API, the Agent Skills API, the Playground, and the
  connectors/plugins marketplace. All claims verified first-party against `platform.claude.com/docs/en/`
  and `code.claude.com/docs/en/` pages fetched 2026-10-15.

- `docs/cc-native/sessions/CC-goal-analysis.md`: the `/goal` command — a session-scoped
  completion-condition loop wrapping a prompt-based Stop hook, evaluated by the small fast
  model after every turn. Covers the evaluator's transcript-only visibility, resume/compaction
  lifecycle, the four unrecoverable-error classes vs. retry/pause for everything else,
  background-work-deferred evaluation and check-in cadence, and version gates from `/goal`'s
  introduction (v2.1.139) through v2.1.274, cross-verified against the CC CHANGELOG. Notes two
  undocumented absences (no stated plan gate; no documented `/goal`-inside-a-subagent behavior)
  rather than inferring them. Cross-links `/loop`, hooks, session-keepalive, and scheduled-tasks
  coverage already in the corpus, plus a one-line design-lens comparison to this workspace's
  unattended-execution rule.

- `docs/cc-native/plugins-ecosystem/CC-official-plugins-landscape.md`: a new "`/code-review`
  command and ultrareview" section, next to the existing `code-review@claude-plugins-official`
  plugin entry — the bundled `/code-review` command (any plan, no install, alias `/review` since
  v2.1.223, formerly named `/simplify` before v2.1.147), `ultrareview`/`/code-review ultra`
  (research-preview cloud review: 3 free runs on Pro/Max then typically $5–$25, typically 15–25
  minutes, 500-file/8,000-line defaults, Bedrock/Agent Platform/Foundry/ZDR/HIPAA fall back to a
  local review, CMEK can't run it), and the separate managed GitHub PR "Code Review" service
  (Team/Enterprise, Quick/Standard/Deep). Corrected the plugin entry's usage line: because plugin
  commands are namespaced, the installed plugin runs as `/code-review:code-review`, not bare
  `/code-review` — confirmed via `claude plugin list` and this session's own skill list (CC
  2.1.302) alongside the plugin's README (4-agent confidence-scoring architecture, author Boris
  Cherny, v1.0.0).

- `docs/cc-native/sessions/CC-goal-analysis.md`: "Pairing `/goal` With a Persistent Task List".
  A durable task list (plan file, backlog, issue queue) holds the work across sessions, and `/goal`
  drives one session through it. Covers how to write the condition (name the file, scope to items
  Claude can finish, make the evidence visible, pick a reachable end state, bound it), failure modes
  (compaction, permission mode, subagents, mid-run list edits, headless runs), and a command Stop
  hook as the deterministic alternative (exit 2 / `decision: "block"`, `stop_hook_active`,
  8-continuation cap). Labelled as a design pattern, not tested.

- `docs/non-cc/coding-agents/goal-loops-landscape.md`: goal loops across coding agents — `/goal` in
  Codex, Antigravity, Kiro, Copilot CLI and Cursor, VS Code Advanced Autopilot, and Stop-style hooks
  in Codex, Copilot CLI, Antigravity, Devin, Cursor and Amp. Compares who judges completion (a
  separate model in Claude Code and VS Code; the agent itself in Codex, Antigravity and Kiro; not
  stated for Cursor and Copilot) and the bounds. Every cell fetched first-party and re-checked by an
  adversarial pass, 2026-10-22.
- `docs/cc-native/sessions/CC-goal-analysis.md`: "Offloading and Batch Runs" — `claude -p` starts in
  Manual mode from v2.1.302, so an unattended goal needs a permission mode; exit codes don't separate
  met/impossible/bounded; one goal per process for batches; cloud sessions and routines don't mention
  `/goal`; Anthropic's explore → spec → `/goal` guidance.

- `docs/non-cc/reference/system-1-decision-models-landscape.md` § Tools built on Jev: jkudish/jev-browser
  (MIT, v0.8.9) — Playwright browser-use where Jev picks each action and scores goal-met/stuck, with
  the README's and awesome-jev's conflicting form-submit claims both recorded; plus the two CC0
  community catalogs cobanov/awesome-jev and MrJev/awesome-jev as discovery sources (MrJev states it
  is not affiliated with TypeSafe AI; its awesome-jev-1 and jev-browser repos are stale forks, so
  upstream is cited).
- `docs/non-cc/infrastructure/jev-analysis.md`: cross-reference updated.

- `docs/cc-community/CC-community-plugins-landscape.md` § Community Mod Catalogs: claude-mods.com
  (unofficial, 278 mods), OneWave-AI/claude-code-mods (MIT, 11 mods incl. a Gmail/Slack/Calendar
  poller), whyashthakker/awesome-claude-code-mods (MIT, 50 mods, via explainx.ai) and ruvnet's field
  guide (partly outdated) — with a caution against loading unreviewed, unsandboxed mods into every
  session via `CLAUDE_CODE_PLUGIN_DIRS`.

- `docs/sdlc-lcm/evaluation-data-resources-landscape.md` § Benchmarks: Omi Health's medical
  speech-to-text benchmark (edition 2026-10-18.1; 1,513 recordings) as a vendor-run, self-scored entry —
  Omi's own model leads and is sold as an API, the recordings' source and release status aren't stated,
  and the open MIT scorer repo uses a different public set (PriMock57, CC BY 4.0) whose leaderboard
  excludes Omi's model.

- `docs/non-cc/knowledge-management/onyx-analysis.md`: Onyx (onyx-dot-app; DanswerAI, Inc.) — open-core
  company knowledge/context layer (MIT outside `ee/`), 50+ connectors, agentic RAG, deep research,
  custom agents, and an MCP server for Claude Code/Codex/OpenCode; v4.9.2. Records its unbenchmarked
  "cheaper than MCP search" claim and the curl-pipe-bash installer as watch-outs. Indexed in
  `docs/non-cc/README.md` and `docs/_topics/rag.md`.

- `docs/cc-native/configuration/CC-tools-inventory.md` § Slash Commands: `/focus` — toggles the focus view
  (last prompt, one-line tool-call summary with diffstats, final response; fullscreen only), persisted
  across sessions and overridable with the `viewMode` setting; `/focus [on|off]` from Remote Control
  (v2.1.281+). Plan 0012 row R11.

- `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: new analysis doc — a first-party fact-check
  and practitioner how-to for the Microsoft 365 Copilot ecosystem (Copilot in SharePoint Skills and
  structured document generation, Microsoft Copilot Studio model selection and BYO MCP, Work IQ,
  Microsoft Agent 365 governance/licensing/APIs, the EU Data Boundary/Flex Routing/Multi-Geo residency
  story including Claude-on-Foundry's own lack of an EU Data Zone deployment type, Claude's
  contractual postures across this family, and a documented Customer-Key-vs-Double-Key-Encryption
  trade-off for Copilot access). 85 claims split by verdict × bucket (3 refuted, 24 partly, 47
  supported, 11 unverifiable); disambiguates "Microsoft 365 Copilot" from GitHub Copilot and
  separates "Copilot in SharePoint Skills" from "custom skills in declarative agents". Adds a
  vendor-sourced feasibility table for eight operational/automation scenarios, a numbers-free
  pricing pointer, "Lockdown limits", a change-feed table, and **guardrails for SharePoint and
  Microsoft 365 agent skills**. Verified 2026-10-23 by an independent falsifier (23 of 25
  load-bearing claims confirmed verbatim, none wrong) and enriched with the SharePoint model note,
  two-step external-model gating, the GCC Anthropic opt-in, per-model Claude postures and the
  Copilot Studio model-retirement dates.
- `docs/non-cc/README.md`: Agents-table row for the new doc.
- `docs/_topics/skills.md`: hub row for Copilot in SharePoint Skills (non-cc bucket).

- `docs/non-cc/infrastructure/ai-crawlers-discoverability-landscape.md`: AI crawler tokens and what each
  controls (training / search / user-triggered fetch), which ones may ignore robots.txt (OpenAI ChatGPT-User,
  Perplexity-User), Cloudflare AI Crawl Control, pay per crawl (closed beta, HTTP 402) and Content Signals
  (`use=` key), and Google's and Bing's first-party guidance for AI answers. Plan 0012 row R1.

- `docs/non-cc/infrastructure/code-review-products-landscape.md`: GitHub Copilot code review (GA; ruleset
  auto-review, AI credits + Actions minutes, shared read-only MCP config), pointing to the cloud-agent doc.

- `docs/non-cc/agents/github-copilot-cloud-agent-analysis.md`: Copilot on github.com — cloud agent,
  automations (launched 2026-06-02; schedule/issue/PR triggers; not in public repos), MCP config
  (GitHub + Playwright MCP on by default, `COPILOT_MCP_` secrets, no OAuth remotes, tools only),
  repository instructions incl. `AGENTS.md`/`CLAUDE.md`/`GEMINI.md`, automatic code review (ruleset
  rule, AI credits + Actions minutes, external-licence setting) and responsible-use mitigations;
  github/github-mcp-server (MIT, v2.0.3). 19/19 claims confirmed by an independent falsifier.

- `.github/workflows/m365-drift-monitor.yaml` + `.github/scripts/m365-drift-monitor.py` +
  `.github/scripts/lib/m365_drift.py`: weekly monitor that checks the Microsoft Learn pages cited
  by the Microsoft 365 Copilot doc for an `ms.date` change or a vanished stored quote, upserting a
  single `m365-drift` tracking issue for a human to triage (#705). Watch list + last-seen state in
  `.github/state/m365-drift-state.json`; refreshed state commits via the shared `create-triage-pr`
  action, same as the other state-backed monitors.

- `.github/state/m365-drift-state.json`: two dated seeds for the M365 drift monitor (#705) — the
  Copilot Studio retirement-table rows for GPT-5.5 Chat (2026-10-31) and GPT-4.1 / GPT-5
  (2026-11-12). Each is a `#fragment` key on the `authoring-select-agent-model` page, so the
  monitor flags the row when it vanishes or changes; the fragment is not sent on fetch.

### Changed

- `docs/cc-community/CC-community-tooling-landscape.md`: refreshed herdr's stale stats (40,485 →
  43,400 stars, v0.9.1 → v0.9.3) in all three places it is recorded, and added the v0.9.2
  self-reported-resume capability (agents can now self-report their resume command) alongside the
  existing session-restart risk note, which still stands — the original OS processes still do not
  survive a restart.

- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: corrected two stale claims found while
  re-verifying against the live docs — CC does **not** use the 5-minute ephemeral cache exclusively (it
  requests a 1-hour TTL by default on a Claude subscription within plan usage for the main conversation);
  and the claimed Bedrock exception for the Fable 5/Mythos 5 minimum cacheable prefix is contradicted by
  the current docs ("these minimums apply on every platform"), so it was removed. The minimum-cacheable-
  prefix table was also refreshed to include newer models (Opus 5.5, Opus 5, Sonnet 5.5, Haiku 5.5, Fable
  5.1, Mythos 5.1), all at 512 tokens.

- `docs/cc-native/plugins-ecosystem/CC-mods-function-hooks-analysis.md`: refreshed against the live
  mods overview/admin/reference/create pages (2026-10-15) — fixed two verbatim-quote drifts (the
  settings-hooks comparison sentence; the Versionable rubric cell's unsupported "GitHub repo with a
  marketplace file" quote, re-sourced to `mods/create`), documented the two built-in mods added since
  the last pass (`cc-plugin-plugin-authoring`, `cc-plugin-you-should-know`, for six total), and added
  the guard's `allowModsToOverrideDenyRules`/`allowManagedHooksOnly`/`disableAllHooks` options.
- `docs/cc-native/plugins-ecosystem/CC-channels-analysis.md`: refreshed against the live channels and
  channels-reference pages (2026-10-15) — added the v2.1.234+ permission-relay gates (credential
  masking, registered-channel-only relay, `(value unserializable)`), the Console-API-key-org default,
  the `-p`-mode tool restrictions, and the v2 MCP client protocol-revision registration gap; the
  `v2.1.80+` version gate is now labeled as an earlier, unconfirmed finding since the current pages
  state no minimum version.
- `docs/cc-native/ci-remote/CC-web-scheduled-tasks-analysis.md`: refreshed against the live Routines
  page (2026-10-15) — added one-off scheduled runs, the per-trigger hourly usage limits, the 72-hour
  GitHub-reconnect grace window, and two comparison-table rows (Permission prompts, Customizable
  schedule); removed an unverifiable "Allow unrestricted" branch-permission toggle claim; fixed the
  Adaptable rubric cell's verbatim quote and softened the Versionable cell's unsupported "past run
  sessions remain" claim; clarified that the URL slug `scheduled-tasks` now belongs to a *different*
  feature (`/loop`, covered in `CC-loop-cron-analysis.md`), not this doc's Routines.
- `docs/cc-native/configuration/CC-loop-cron-analysis.md`: substantially refreshed — this feature now
  has an official first-party page (`code.claude.com/docs/en/scheduled-tasks`) superseding most of the
  doc's original gist/cli.js-decompilation and empirical sourcing. Corrected the "default interval: 10
  minutes" claim (no such default; an omitted interval now means Claude self-paces 1 min–1 h) and the
  "`durable: true`" persistence claim (the current page describes resume-restoration as the default
  for all `CronCreate` tasks except a self-paced loop and expired/past-due tasks, with no such
  parameter documented). Added self-paced loops, `loop.md`, the `ScheduleWakeup` tool, Monitor-tool
  integration, skill-invocation reach rules on a scheduled fire, `CLAUDE_CODE_DISABLE_CRON`, the
  `Esc`-to-stop a self-paced loop, and the documented session-backgrounding workaround for the
  session-bound limitation. Added the missing `validated_links` frontmatter field.
- `docs/cc-native/CC-first-party-docs-index.md`: added rows for `plugins/mods/overview`,
  `plugins/mods/admin`, `plugins/mods/reference`, `channels-reference`, `slash-commands`, `goal`,
  `scheduled-tasks`, `routines`, `desktop-scheduled-tasks`, and `hooks` (reference), found while
  navigating the docs for this refresh.

- `docs/cc-native/configuration/CC-tools-inventory.md`: replaced the stale `/ultrareview` row
  ("Unknown — enhanced review?") and a stale `/review-pr` row (which cited `cli-ref` for a command
  absent from that reference, the live `commands` page, and the full Claude Code CHANGELOG, v0.2.21
  through v2.1.302) with verified `/code-review`, `/review`, `/simplify`, and `/ultrareview` rows,
  plus a detailed subsection covering targets, effort levels, flags, alias/rename version gates,
  and ultrareview's scope, billing, limits, and platform restrictions — verified against the live
  `code-review-local`, `ultrareview`, and `commands` pages (CC 2.1.302).
- `docs/cc-native/plugins-ecosystem/CC-official-plugins-landscape.md`: corrected the code-review
  plugin's author/version attribution — an independent fact-check of this PR found the two
  first-party files disagree: `.claude-plugin/plugin.json` names the author "Anthropic" and has
  no version field, while the README's own `## Author`/`## Version` sections give "Boris Cherny"
  and "1.0.0". Both are now cited to the file that actually states them.
- `docs/cc-native/configuration/CC-loop-cron-analysis.md` (coordinator-requested follow-up, not an
  owner-approved fence widening): replaced the three stale `/review-pr 1234` example-target
  mentions (lines 20, 39, 185) with `/code-review 1234`, a documented target form. Bumped
  `updated:`/`validated_links:` to 2026-10-18.

- `AGENTS.md`: the Rules line says where the shared rules come from, and that cloud, GHA and
  other-machine sessions don't get them.
- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: the context-management link points
  at the plugins SoT.

- `docs/sdlc-lcm/agentic-sdlc-patterns.md` § ADLC: practitioner variant where each stage commits an
  artifact the next reads (intent file, skills, `CLAUDE.md`, hooks), with a production alert writing a
  new intent file to close the Observe→Correct gap — plus a caution that an alert path with no human
  turns log text into agent instructions (prompt injection). Opinion source, plain-text LinkedIn URL.

- `docs/non-cc/protocols/agentic-payments-landscape.md`: agent payment protocols refresh. New sections
  for Stripe MPP (Machine Payments Protocol, co-authored with Tempo; HTTP 402; cards via SPTs and
  stablecoins; serves x402 clients too), L402 (Lightning Labs; macaroon + invoice preimage; TLS
  warning), UCP (Universal Commerce Protocol, Apache-2.0, built on AP2) with Shopify's UCP-compliant
  MCP servers, and the card networks (Visa Intelligent Commerce and Connect pilot, Visa Trusted Agent
  Protocol, Mastercard Agent Pay and Agentic Tokens). AP2 release history, Lightsage re-check (2,370
  companies), takeaways and the comparison table updated. 33 claims re-checked by an independent
  falsification pass (32 confirmed, 1 overstated and corrected); Mastercard's exact launch date stays
  unverified.

- `docs/sdlc-lcm/evaluation-data-resources-landscape.md` § Agent-readiness scoring: DevTool Arena
  re-checked 2026-10-22 — now at devtoolarena.com, operator "API-Rex, Inc., doing business as
  Lightsage"; 11 boards across 7 agents (`llms.txt`), Claude Code API board 187 companies / 45
  categories; new discoverability view (46 use cases × 5 prompts, 19 agent/model columns); no dates,
  method or data licence on the boards, changelog as the only dated record. Adds a conflict-of-interest
  note (Lightsage sells $100–$1,000/month plans to the companies it ranks; submissions collect contact
  details) and Lightsage's "Agent-Led Growth" framing as vendor terminology. Scores are cited, not copied.

- `docs/non-cc/README.md`, `docs/_topics/long-running.md`: index rows for the new landscape.

- `docs/cc-native/plugins-ecosystem/CC-mods-function-hooks-analysis.md`: VS Code (2.1.299+) and
  Bedrock (2.1.304+) version gates; `mods/` re-checked (last change 2026-10-20) and its licence noted —
  "© Anthropic PBC. All rights reserved", so published source, not open source; the claude.dev mods
  showcase and the community `next-steps@claude-community` mod.

- `docs/non-cc/protocols/ag-ui-protocol-landscape.md`: OpenUI (Thesys, MIT, 13k★) — a generative-UI
  payload language (OpenUI Lang) plus React/Vue/Svelte/Angular renderers that streams over AG-UI and
  ships an A2UI v1.0 client; self-reported "up to 67% fewer tokens than JSON". New section, decision-matrix
  row and source.

- `docs/cc-native/agents-skills/CC-skills-adoption-analysis.md`: re-confirmed against the live Agent
  Skills specification that `allowed-tools` is the only tool-related field (Experimental) and that
  the optional package directories are `scripts/`, `references/` and `assets/` — no `evals/`; the
  skill-creator plugin's `evals/evals.json` is a plugin convention. Adds a Claude Code ↔ OpenAI Codex
  CLI SKILL.md / MCP / AGENTS.md parity table. Split out of #704.

- `docs/non-cc/protocols/ag-ui-protocol-landscape.md` § A2A: status re-checked 2026-10-24 — v1.0.1 still
  latest, AAIF Growth Stage, nine-seat TSC (Bloomberg added), A2A CLI, unreleased `dev-1.1` work
  (`SendLiveMessage`, AI Catalog discovery), and vendors still on v0.x naming (Copilot Studio, AgentCore SDK pin;
  ADK Experimental). Plan 0012 row R3.
- `docs/non-cc/frameworks/agentic-enterprise-os-landscape.md`: Copilot Studio "A2A GA" scoped to the standard
  harness (GitHub Copilot harness is preview) and sourced to the what's-new page.
- `docs/non-cc/protocols/agentic-payments-landscape.md`: new "Merchant feeds" section — what OpenAI (ACP feed),
  Google (Merchant Center native commerce, UCP) and Shopify (Agentic Storefronts) ask merchants to provide.

- `docs/sdlc-lcm/evaluation-data-resources-landscape.md`: Ora refreshed (127,521 sites, average 43, 6% B+,
  2026-10-24); new "Making a business agent-ready" paragraph — Google needs no special markup or schema for
  AI features, NLWeb (MIT, now `nlweb-ai/NLWeb`), Checkatrade's Claude connector. Plan 0012 row R2.
- `docs/sdlc-lcm/agent-identity-auth-landscape.md`: MCP authorization updated to the 2026-07-28 revision
  (RFC 8707 audience binding, DCR deprecated for Client ID Metadata Documents) plus Claude connector
  directory requirements (R2); Visa Trusted Agent Protocol next to Web Bot Auth (R5).

- `docs/cc-native/context-memory/CC-llms-txt-analysis.md`: llms.txt v2 (2026-08-10) — context-expansion
  tooling dropped, Optional sections no longer carry mechanical semantics, `page.md`, Markdown alternate
  links; Google needs no AI text files.
- `docs/non-cc/README.md`: index row for the new landscape.

- `docs/non-cc/agents/github-copilot-cli-analysis.md`: the CLI now reads `AGENTS.md`/`CLAUDE.md`/
  `GEMINI.md` (the "not AGENTS.md" gap is closed) and is billed in GitHub AI Credits, not premium requests.
- `docs/sdlc-lcm/multi-agent-onboarding-outlook.md`: Copilot row notes AGENTS.md/CLAUDE.md/GEMINI.md.
- `docs/cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md`: Playwright MCP licence/release,
  on by default in Copilot cloud agent, README security and CLI+skills notes.
- `docs/non-cc/README.md`: index row for the new doc.

- `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: removed the ShareGate article and the
  "Governing SharePoint Skills and Agents" webinar (vladtalkstech.com, drewmadelung.com) from the
  Sources table and their link definitions (owner, 2026-10-24); no claim in the body cited them.

- `docs/non-cc/infrastructure/web-scraping-extraction-landscape.md`: moli fit verdict — not a Patchright
  replacement (no Python API, no stealth goal, installer-script distribution, vendor-only fidelity numbers);
  facts re-checked at source 2026-10-24. Closes #665.

- `docs/architecture.md`: Automated Monitors lists the M365 drift monitor (#720); Lint Gate notes lychee
  is authenticated with the workflow token (#721).
- `docs/plans/2026-10-10-0012-decision-models-estate.md`: C1 and K0 brought current (gha-issue-triage#115
  merged; the 2026-10-22 token re-set); R6 struck (qte77#198); N10 records the 2026-10-23/24 work; new rows
  R12 (all-failed paper triage must fail), R13 (GitHub changelog monitor, owner), R14 (polyforge leftovers).
- `AGENT_LEARNINGS.md`: rotating github.com 503s = unauthenticated lychee; green runs that did nothing.

- Goal-loop facts (verified 2026-10-22) added to `codex-cli-analysis.md`, `cursor-analysis.md`,
  `antigravity-analysis.md`, `vscode-copilot-chat-analysis.md` and `github-copilot-cli-analysis.md`, each
  pointing to `goal-loops-landscape.md`; `kiro-analysis.md` notes `/autonomous on` (CLI v2.31.0) and its
  `/goal` defaults. Plan 0012 row R4.

- `docs/cc-native/configuration/CC-tools-inventory.md`: `/focus` row now gives `viewMode`'s values
  (`"default"`, `"verbose"`, `"focus"`), scope (any settings file) and default (unset), verified against
  the settings reference 2026-10-24.

### Removed

- `.claude/rules/context-management.md`, `compound-learning.md`, `core-principles.md`: the shared
  estate rules now load once, at user level, from `~/.claude/rules/` symlinked to the
  claude-code-plugins rules SoT (plan 0001). Repo sessions on this machine loaded them up to four
  times, in three versions of core-principles.

- `docs/cc-native/agents-skills/CC-skills-adoption-analysis.md`: the Claude Code ↔ OpenAI Codex CLI
  parity table (added in #708) — every row repeated facts already in `agents-md-cookbook-analysis.md`,
  `codex-cli-analysis.md` or the ecosystem table above it; replaced by a one-line pointer to the
  AGENTS.md compatibility matrix (owner, 2026-10-24). The spec re-check stays.

### Fixed

- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md`: Tracely link moved to `jwuthri-cloud/Tracely-ai`
  (the original `Jwuthri/Tracely-ai` returns 404); star count refreshed.
- `docs/cc-native/ci-remote/CC-remote-access-landscape.md`: Omnara's iOS App Store listing returns 404 and
  the site no longer mentions an iOS app — link removed, the claim it sourced marked unverified.

- `docs/non-cc/infrastructure/jev-analysis.md`: feelings v0.10.0 figures re-read from `results.json`/
  `ytdlp.json` at the tag — Opus 5.5 averaged 0.96 ROC-AUC (was 0.97), yt-dlp per-question AUC 0.76–0.99
  across both Jev runners (was 0.77); adds the Claude-baseline harness disclosure (tool-less `claude -p`)
  and a measurement caveat on cue leakage in mutation-built benchmarks. Closes #622.

- `.github/workflows/lint.yaml`: the "Run lychee" step now passes `GITHUB_TOKEN: ${{ github.token }}` so
  lychee authenticates its github.com requests (`--github-token`, env `GITHUB_TOKEN`). Without it, CI link
  checks failed on rotating github.com 503s under throttling. Matches `link-rot-monitor.yaml` and the
  shared `lint-md-links.yml` (lychee-action defaults `token` to `github.token`); the custom workflow from #141 is kept.

## [0.16.0] - 2026-10-10

### Added

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: new "October 2026: major vendors ship Jev-style decision models" section with sub-sections for the **OpenAI Decisions API** (`gpt-6-luna`; public beta per the guide/changelog, "limited preview" per the one-day-later DevDay recap — all three first-party pages quoted) and **Perplexity pplx-decider** (Apache-2.0 open weights on Hugging Face plus a hosted Decisions API using Jev's own `noul`/`choice`/`score` vocabulary; resolves the model card's "private repository" wording against the Hugging Face API's live `gated: false`/`private: false` metadata; documents the community-run, not Perplexity-run, "Decision Index" benchmark). Adds first-party Perplexity cookbook examples to § Use cases: an action-gate cookbook that is this corpus's first documented approve/deny gate on an already-formed tool call for a Jev-style model, a browser-agent next-action cookbook, a ticket-triage routing cookbook, and a citation-accuracy grounding check cross-referenced from the judge use case. Narrows (without closing) the model-routing gap now that OpenAI and Perplexity both name "routing" as a use case. Records the self-reported, unverified Maziyar Panahi LinkedIn leaderboard (24 models, 669 clinical decisions) that triggered this update, including a site-wide check showing the leaderboard itself is not publicly published.

- `docs/non-cc/infrastructure/web-scraping-extraction-landscape.md`: Firecrawl Universal Scrape (2026-10-08) — `/scrape` extended to third-party provider data through the Alexandria provider layer.

- `docs/_topics/harness.md`: the system-1 row names the OpenAI Decisions API and Perplexity pplx-decider.

- `docs/_topics/`: hub rows for MIRA and the system-1 use-case map (harness) and Octop (memory).

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: § Use cases › Model routing — a self-reported practitioner cascade (Jev triage → Grok 4.7 → Claude → human approval) from a 2026-10-08 LinkedIn post.

- `docs/non-cc/reference/weco-aide-recursive-self-improvement-analysis.md`: MIRA (arXiv:2610.02525), a hierarchical meta-reasoner/executor split for long-horizon research agents (theorem proving, neural-architecture research) with a trained actor-critic variant (MIRA-AC); compared against the doc's existing agentic-meta-reasoning entry; no code repository found (checked abstract page and GitHub); not rubric-scored (no open-cell impact).
- `docs/non-cc/agents/octop-analysis.md`: Octop (TencentCloud, MIT) — self-hosted multi-user, multi-agent assistant: single-process LangGraph harness, per-row user/agent isolation, AgentTeams (Beta) coordinator, hierarchical-recall memory with a LangGraph SQLite checkpointer, and outbound ACP delegation to Claude Code, OpenCode, CodeBuddy, and Codex.
- `docs/non-cc/frameworks/agentic-enterprise-os-landscape.md`: Octop added to Tier 2's open-source self-operating workspaces, alongside AutoAgent, Odysseus, Goose, multica, and HugAgentOS.
- `docs/non-cc/README.md`: Octop row added to the Agents table.

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: a "Use cases" section organizing the system-1 decision-model landscape by six agent-pipeline use cases — model routing, guardrails, tool-call gating, reranking, LLM output evals/judging, and confidence-gated human-in-the-loop escalation — each sourced to a first-party README/docs/paper, with explicit gap notes for reranking and model routing (no corpus Jev-family model documents either). Re-fetched GLiNER2.5-Decide's own announcement and Secure Agentics Adrian's README verbatim to source four of the six use cases directly. `docs/non-cc/infrastructure/jev-analysis.md` gets a one-line pointer to the new section.

### Changed

- `.github/workflows/rxiv-paper-eval.yaml`: each week's papers are ranked by topic-keyword overlap and the top 100 go to the LLM (`max_llm_calls`), instead of the first 50 rows in feed order (`max_papers`). The dispatch input is now `max_llm_calls` (default 100).

- `docs/non-cc/infrastructure/jev-analysis.md`: new short "Competition" section pointing to the new OpenAI/Perplexity sections.

### Fixed

- `.github/workflows/rxiv-paper-eval.yaml`: the triage branch now includes the week key (`chore/rxiv-paper-triage-<server>-<year>-W<week>-<date>`), so runs for different weeks on the same day no longer collide; `CONTRIBUTING.md` states the remaining rule (one run at a time, merge each triage PR before the next).

- `.github/workflows/rxiv-paper-eval.yaml`: the triage report skips papers the feed lists twice in one week; the repeated headings failed markdownlint MD024 and stopped the W26 backfill.

- `docs/non-cc/infrastructure/jev-analysis.md` (and the two docs that repeat it): the qte77/feelings pre-CI gate numbers now come from the post-P5 run (feelings#45): 76% caught, 2 of 59 clean flagged (3.4%), 23% held-out false flags, about 67x faster and 51x cheaper than Claude; the earlier figures predated the removal of a new-file cue.
- `docs/non-cc/reference/system-1-decision-models-landscape.md`: pplx-decider's "61.56 vs 57.9" is reconciled — it is Decision Index edition 0.2.1, reproduced from the published area weights; edition 0.3's `balanced_skill` blends in private tests and is not comparable. The Panahi leaderboard note now flags the unexplained "tied at #1" and the "42% less" claim (52% at published prices).

## [0.15.0] - 2026-10-06

### Added

- `docs/cc-native/plugins-ecosystem/CC-claude-science-analysis.md`: Claude Science, Anthropic's desktop AI workbench for scientists (sandbox, provenance-recorded artifacts, reviewer, plans, platform discrepancy across sources).
- `docs/non-cc/knowledge-management/research-agents-landscape.md`: Polaron (materials from microscopy, §2), Claude Science (§1, beside OpenScience), and a new §5 Research Communities with the AIDDA Institute (AI-driven algorithm discovery).

- `docs/sdlc-lcm/ai-security-governance-analysis.md`: Reward Hacking and Evaluation Awareness — MacDiarmid et al. (arXiv:2511.18397), EvilGenie (arXiv:2511.21654), Nguyen et al. (arXiv:2507.01786).
- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md`: Verbalized Confidence Calibration (Brier) metric — ConfidenceBench (arXiv:2607.20526), ConfTuner (arXiv:2508.18847), Aggarwal (arXiv:2608.27167).
- `docs/non-cc/knowledge-management/research-agents-landscape.md`: RankEvolve (arXiv:2609.39551), multi-agent auto-research harness.

- `docs/cc-community/CC-community-skills-landscape.md`: cathrynlavery/diagram-design — editorial diagram-generation skill for Claude Code, Codex, GitHub Copilot, Factory Droid, and Pi (43,595 stars, MIT; 44 diagram types by live file count, README tagline says 42).
- `docs/cc-community/CC-memory-tooling-landscape.md`: Operator Memory (aerovato) — cross-agent "self-improving context engine" storing specs/decisions/lessons as git-tracked Markdown across `.operator/`, `.operator-shared/`, and `~/.operator/user/` (359 stars, BSD-3-Clause).

- `docs/non-cc/reference/system-1-decision-models-landscape.md` + `docs/non-cc/infrastructure/jev-analysis.md`: pg-jev (realZachi/pg-jev) — PostgreSQL extension exposing Jev as SQL functions; added to the "Tools built on Jev" and ecosystem lists.
- `docs/cc-native/ci-remote/CC-remote-access-landscape.md`: Tailnet Preview (elsheppo/tailnet-preview) — Tailscale-based web-preview tool with a Codex agent-skill tie-in, added to the DIY (tmux + Tailscale/SSH) section.

- `docs/non-cc/knowledge-management/karpathy-llm-kb-analysis.md`: CorpusMap (arXiv:2609.37226), entity-page navigation layer for agentic search over document corpora.
- `docs/non-cc/orchestrators/raven-analysis.md`: Raven's arXiv technical report (arXiv:2609.33439), compared against the README (no numeric results in the abstract).
- `docs/non-cc/reference/weco-aide-recursive-self-improvement-analysis.md`: ActiveSaddler (arXiv:2610.00906), curriculum-driven harness optimization; Sharpening Tax (arXiv:2610.01509), RL post-training coverage-loss critique; FineEnvs' cited-papers list resolved from its Space bibliography.
- `docs/non-cc/infrastructure/semantic-layers-data-catalog-landscape.md`: three self-evolving-ontology papers — OaK (arXiv:2608.22974), SciToolAgent-Evo (arXiv:2607.28692), Evo-DKD (arXiv:2507.21438) — added alongside EvoOntology; not rubric-scored (no code, no open-cell impact).

- Cross-links: EvilGenie in the benchmarks list, Brier metric ↔ system-1 decision models, Claude Science ↔ bubblewrap quirks; `_topics/harness.md` and `_topics/long-running.md` rows.

- `docs/_topics/`: hub rows for diagram-design (visualization), Operator Memory (memory), Raven (harness) and the remote-access landscape (long-running); harness, rag and knowledge-graphs rows now name ActiveSaddler, Sharpening Tax, CorpusMap and the self-evolving-ontology papers.
- `docs/non-cc/reference/system-1-decision-models-landscape.md`: link to the Brier calibration metric.

- `.github/scripts/lib/relevance_eval.py`: `agent-strict` prompt variant for `llm-model-eval.yaml`, with a unit test that keeps the production workflow's prompt identical to it.

### Changed

- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md`: refreshed the one-line Haystack entry with its current self-description, license/star count, and `v3.3.0` version gate.

### Fixed

- `.github/workflows/issue-triage.yaml`: issue triage runs again. GitHub Models was retired on 2026-07-30, so the action now calls Cloudflare Workers AI (`@cf/meta/llama-3.3-70b-instruct-fp8-fast`) through `qte77/gha-issue-triage` v0.4.0 (`api_base` + `llm-api-key`). `permissions: models: read` is no longer needed (#527).

- `.github/workflows/rxiv-paper-eval.yaml`: the weekly arXiv eval runs again. GitHub Models was retired on 2026-07-30, so the eval now calls Cloudflare Workers AI (`@cf/meta/llama-3.3-70b-instruct-fp8-fast`) through `qte77/gha-rxiv-paper-eval` v0.5.0 (`api_base` + `llm-api-key`). Dependabot PRs skip the eval, since they get no repo secrets (#527).

- `docs/sdlc-lcm/agent-code-analysis-landscape.md`: corrected the stale "secondary source" / "unverified" SkillSpector mentions to cross-link the first-party-verified entry in `agentic-ai-vulnerability-landscape.md`.

- `docs/cc-native/plugins-ecosystem/CC-claude-science-analysis.md`: export, sharing and replay are now documented from the artifacts and multiple-computers pages (the earlier "sources don't say" was wrong); the platform table is a dated timeline from the changelog, not a disagreement; Pro auto-review is off by default.
- `docs/sdlc-lcm/ai-security-governance-analysis.md`: MacDiarmid et al. first impart reward-hacking knowledge before RL; the subsection no longer frames all three papers as about coding agents.
- `docs/cc-native/model-internals/CC-first-party-interpretability-index.md`: the "From Shortcuts to Sabotage" row described a different paper's chain; it now states the post's own finding and links arXiv:2511.18397.
- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md`: ConfidenceBench's 0.367 is no longer called "worst"; notes the benchmark cannot be re-run independently.
- `docs/non-cc/knowledge-management/research-agents-landscape.md`: Claude Science moved to §1 beside OpenScience; AIDDA's unsourced "same loop as autoresearch" removed.

- `.github/workflows/rxiv-paper-eval.yaml`: the weekly arXiv eval uses an agent-strict relevance prompt (#594). On weeks 22–30 with Llama 3.3 70B, agreement with the earlier labels rose from 46.0% to 83.6% and false accepts fell from 135 to 16; most remaining disagreements were non-agent papers the old labels had accepted.

## [0.14.0] - 2026-10-02

### Added

- `docs/cc-native/ci-remote/CC-cloud-sessions-analysis.md`, `CC-web-scheduled-tasks-analysis.md`: dated agent-substrate-rubric rows, scored 2026-10-02 from current Anthropic docs (plan 0010, rows U1/U2).
- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: a confirmed-open answer on whether ACE-FCA's `research.md`/`plan.md`/`implement.md` phase artifacts are git-tracked (row A1), and a new rubric row scoring `AGENTS.md` itself as a cross-agent instruction file (row M1).
- `docs/cc-native/plugins-ecosystem/CC-mods-function-hooks-analysis.md`: new doc — Claude Code mods (function hooks): the `$` API, governance, and the built-in `AGENTS.md`/`diff` mods, rubric-scored (row M1).
- `docs/cc-native/plugins-ecosystem/CC-official-plugins-landscape.md`: a full `code-modernization` plugin entry (from its own README/LICENSE/plugin.json), rubric-scored (row M2).
- `docs/_topics/plugins.md`: hub row for the new mods doc.

- `docs/non-cc/context-memory/redis-iris-analysis.md`: new doc. Redis Iris's Context Retriever is the first corpus row to score `partial` on context·Shared and context·Distributed (both previously fully open); Agent Memory scored separately under the memory subject.
- `docs/non-cc/context-memory/hyperspell-analysis.md`: new doc. Hyperspell checked as a context lead (plan 0010, row L1); classified as memory instead — context cells unaffected.
- `docs/cc-community/CC-community-skills-landscape.md`: stevesolun/ctx added and rubric-scored (plan 0010, row L3); does not fill skills·Shared or skills·Distributed.
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md`: ACM (arXiv:2608.11166) added and rubric-scored (plan 0010, row L3); does not fill skills·Shared or skills·Distributed.

- `docs/non-cc/reference/weco-aide-recursive-self-improvement-analysis.md`: two new harness-subject entries (plan 0010 rows M3–M4). FineEnvs multi-harness RL (HF Space `FineEnvs/multi-harness-rl` + Apache-2.0 companion repo `adithya-s-k/FineEnvs`): trains one small model across unmodified OpenCode/Claude Code/Codex/Mini-SWE-Agent harnesses via an OpenEnv capture proxy, Harbor-served sandboxed tasks, and Async GRPO in TRL; rubric-scored. Agentic meta-reasoning (arXiv 2609.38147, "Thinking Before Thinking"): an inference-time controller harness over worker agents with a compact persistent-memory run state; paper only, no code found, scored accordingly.
- `docs/_topics/harness.md`, `docs/non-cc/README.md`: extended the existing `weco-aide-recursive-self-improvement-analysis.md` row descriptions for the two new entries above.

- `docs/cc-native/agents-skills/CC-skills-adoption-analysis.md`: a section and rubric row on organization-level skill provisioning (Claude Team and Enterprise), from Anthropic's Help Center article. Shared and Distributed are `yes`: the first corpus row to reach `yes` on those skills cells.

- `.github/scripts/lib/doc_census.py`, `.github/scripts/build-doc-census.py`, `make census`: a tested, stdlib-only census of every agent-substrate rubric row in `docs/`. It reads both formats (six-column tables, including indented ones and ones with a leading `Tool` column, and inline `**Rubric**` paragraphs) and prints the 8 × 6 evidence matrix. Open cells read "open (best: no data)" or "open (best: no)" (plan 0010, T1).

### Changed

- `docs/sdlc-lcm/agent-substrate-rubric.md`: new scoring rule 6 (plan 0010, decision C0). Static artifacts in git (skill repos, CLAUDE.md/AGENTS.md, plugin and ontology files) are scored on how they are governed and synced: `partial` on Shared and Distributed when the repo has a documented contribution flow. Rows that mix a git-hosted artifact with a runtime store are split. Rule 5's example is now a research paper, so the two rules agree. Owner may override.
- `docs/plans/2026-10-01-0010-open-substrate-cells.md`: plan 0010 approved (#576).

- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: corrected the `AGENTS.md` bullet in Key Behaviors — CC now reads `AGENTS.md` directly by default (v2.1.277+) as a built-in mod, superseding the older import/symlink-only description.

- `docs/_topics/context.md`, `docs/_topics/memory.md`, `docs/_topics/skills.md`, `docs/non-cc/README.md`: new rows for the above.

- `docs/sdlc-lcm/agent-substrate-rubric.md` rule 6: for a vendor's instruction-file mechanism (CLAUDE.md, AGENTS.md), the vendor's documented team sharing through source control counts as the cited flow (plan 0010, R1).
- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: the mixed CLAUDE.md + auto memory row is split into two rows, and the AGENTS.md row is re-scored under rule 6.
- Skills and context rows re-scored under rule 6: runtypelabs/skills is `partial` (documented PR flow); coleam00/skills, the excalidraw skill, Cloudflare's security-audit skill and context-engineering-intro are `no data` (no documented contribution flow, full repo tree checked).

- `docs/sdlc-lcm/agent-substrate-rubric.md` rule 4: scored rows name their subject with a `subject:` tag next to the date; `make census` builds the matrix from these tags and lists untagged rows separately.

- Every scored rubric row in `docs/` (75 rows in 25 docs) now carries a `subject:` tag, so `make census` regenerates the reference architecture's evidence matrix from the corpus (plan 0010, T1 part 2).
- `.github/scripts/lib/doc_census.py`: a table takes its nearest `subject:` tag, so two tables under one heading can have different subjects. An inline row ends where the next list item starts, and the first score per property wins.

- `docs/sdlc-lcm/agent-substrate-reference-architecture.md`: the evidence matrix and "What stays open" now reflect plan 0010 (75 rows, 28 docs). context·Shared and context·Distributed are `partial` (Redis Iris's Context Retriever; CLAUDE.md under rule 6). skills·Shared and skills·Distributed are `yes` (organization-level skill provisioning). plugins·Traceable is `yes` (Code Modernization). context·Reproducible is confirmed open. `make census` reproduces all 48 cells.

### Fixed

- `docs/cc-native/plugins-ecosystem/CC-official-plugins-landscape.md`: Code Modernization's Reproducible score goes `yes` → `partial`. The proof step is deterministic, but the analysis and rewrite run as agents with no pinned model (the rubric's "pinned code but unpinned model" case).

- `.github/scripts/lib/doc_census.py`: a score written in bold or italics (`**partial**`) is now read correctly instead of falling back to `no data`.

## [0.13.1] - 2026-10-01

### Fixed

- `docs/non-cc/agents/openresearch-analysis.md`: removed a quote the about page does not contain ("a prior project by the same team"; the page actually opens "We started alphaXiv…"), and dropped an unsupported claim that `orx discover`/`orx paper` run on alphaXiv (the README does not name their backend).
- `docs/non-cc/agents/feynman-analysis.md`: the cross-link no longer says OpenResearch shares Feynman's alphaXiv backend.

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: corrected a wrong kev-vs-Jev accuracy figure and co-author count, softened an overclaimed "ran Jev on dev and test sets" to dev-sets-only, fixed an overclaimed Hugging Face "pinned"/"with tags" claim for Laya, and replaced a stale "pointer belongs there at merge" note with the now-current cross-reference fact.
- `docs/non-cc/protocols/openai-apps-plugins-analysis.md`: corrected the marketplace.json entry count and source-type breakdown (65 entries, 3 git-backed, not "all local"), fixed a citation that attributed a coverage-gap list and a CC score to the wrong doc, re-cited two facts to the page that actually states them, and fixed two misquotes (paraphrase-as-verbatim-quote).
- `docs/sdlc-lcm/agent-substrate-reference-architecture.md`: fixed an off-by-one row count in the Skills·Shared tally.
- `docs/sdlc-lcm/software-factory-landscape.md`: corrected a wrong claim that Flue has no findable GitHub repo/license, an undercount of files in the `ai-that-works` episode directories, two misquotes (Augment Code, Lockheed Martin), an overclaim that Hitachi "coined" rather than first adopted the term, and an overclaim that "graph engineering" is an established industry term rather than a weeks-old, contested coinage.
- `docs/non-cc/infrastructure/code-review-products-landscape.md`: corrected PR-Agent's license from Apache-2.0 to MIT in both places it appears.
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md`: dropped an unsupported Slack/Notion/GitHub/Gmail connector list attributed to HydraDB's own sources, removed a fabricated Paperclip README quote, and fixed a date error conflating two separate Intent-Router eval log entries.
- `docs/cc-community/CC-community-skills-landscape.md`: corrected an overclaimed "runs in CI on every push" for the security-audit-skill validator (it runs as part of the skill's own workflow; the repo has no CI configured).
- `docs/cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`: re-cited two rubric-cell quotes to the CC Plugins overview page, which actually contains them, instead of the manifest reference page.
- `docs/cc-community/CC-community-tooling-landscape.md`: corrected a tool-count off-by-one ("twenty-six" to "twenty-seven").
- `docs/non-cc/agents/goose-analysis.md`: downgraded two AAIF rubric cells (Shared, Adaptable) from "yes" to "partial" to match the doc's own hedge that no charter/membership/decision process is documented.
- `docs/non-cc/infrastructure/semantic-layers-data-catalog-landscape.md`: downgraded EvoOntology's Reproducible score to "partial" (unpinned, swappable backbone LLM), and fixed three misquotes (open-ontologies Traceable cell, EU AI Act Article 12, EvoOntology's Candidate-vs-Parent rule).
- `docs/non-cc/agents/openresearch-analysis.md`: corrected an overclaimed "Rust/Tauri" runtime description to match the doc's own "Tauri-style, not the Tauri framework" hedge, and fixed a Rust-byte-count percentage (74% to 70%).
- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: corrected Dan Shapiro's framework from "five-levels" to "six-level" to match the doc's own Sources row, and fixed a wrong X/Twitter URL path segment (`article` to `status`) in two places.
- `docs/non-cc/reference/orcareplay-analysis.md`: replaced a fabricated "time travel for AI agents" tagline with the README's actual framing, and corrected an overstated repo age ("six weeks" to "about a month, created 2026-08-29").
- `docs/non-cc/infrastructure/jev-analysis.md`: removed a fabricated "atomic questions, composed in code" quotation and fixed a rate-limits quote that reordered and altered the source's sentence.
- `docs/cc-community/CC-harnessrouter-analysis.md`: rescored the Versionable cell from "no data" to "partial" (versioned code, unversioned state — the rubric's own partial trap), and dropped quotation marks around a phrase that is this doc's own framing, not a HarnessRouter quote.
- `docs/cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md`: corrected an overclaimed "end-to-end" timing figure and an overclaimed baseline for jev-ultrafast's reported 25% task-time reduction, matching the README's own narrower framing.
- `docs/non-cc/protocols/agent-plugins-standard-analysis.md`: fixed a verb-form alteration inside a quoted sentence from the Mitosis plugin README.

- `docs/non-cc/agents/goose-analysis.md`: the AAIF governance paragraph and rubric cells now follow the published [AAIF charter](https://github.com/aaif/foundation/blob/main/foundation-charter.pdf), board and Technical Committee pages. #545 had said no charter or decision process is published, and the #572 correction repeated it, but the charter is in the `aaif/foundation` repo. It names a Governing Board, a Technical Committee and a TSC per hosted project. Shared and Adaptable stay `partial` with corrected reasons; Versionable goes `no data` → `partial` (the charter is in git, as a single PDF).
- `docs/non-cc/protocols/ag-ui-protocol-landscape.md`: removed a third-party "see also" link (salesforceben.com) that blocks every fetch route and has no archive copy; the first-party Salesforce sources beside it remain.

## [0.13.0] - 2026-09-30

### Added

- `docs/non-cc/protocols/openai-apps-plugins-analysis.md`: OpenAI's current unified ChatGPT + Codex plugin system compared against CC plugin packaging and the Agent Plugins standard — manifest (`plugin.json`/`mcp.json` declaring the Agent Plugins v1.0.0 schema, a confirmed shipped implementation by a TSC member), the three things named "marketplace" (universal reviewed directory, unreviewed local/repo/personal catalogs, and the unrelated OpenAI Marketplace partner/procurement program), pinning (a per-plugin lockfile with an unfilled integrity placeholder in the one shipped example inspected, daily unversioned MCP-server rescans), the two-stage automated + human review pipeline, and the one-directional CC-to-OpenAI plugin conversion path. Keeps the 2023 ChatGPT plugins beta and the 2024 GPT Store apart as legacy eras from the current system. Rubric-scored against `sdlc-lcm/agent-substrate-rubric.md`.
- `docs/_topics/plugins.md`, `docs/non-cc/README.md`: pointer rows for the new page.

- `docs/sdlc-lcm/software-factory-landscape.md`: disambiguates three unrelated senses of "software factory" — the historical Japanese-industrial and Microsoft (Greenfield & Short, 2004) lineages, DevSecOps-vendor framing (Lockheed Martin, VMware, self-reported), and the agentic-AI sense (CircleCI, Augment Code, freeCodeCamp, the `ai-that-works` episode cluster, HumanLayer's `wsff.md` dissent, and Cloudflare's Astro issue-triage production case). Rubric-scores Cloudflare's `triagebot-action` GitHub Action; the `ai-that-works` episodes and Flue are cited as sources, not scored, for lack of a verifiable shipped artefact. Includes a convergence finding (independent sources keep human gates at spec/merge) and a design lens pairing it with this repo's own unattended-execution phase discipline and an owner-surfaced "fluid software" opinion (rUv, LinkedIn, cited as plain text).
- `docs/sdlc-lcm/README.md`, `docs/_topics/long-running.md`: pointer rows for the new page.

- `docs/non-cc/agents/openresearch-analysis.md`: new analysis of OpenResearch (alphaXiv) — a local-first, git-native workspace turning Claude Code/Codex/OpenCode/Cursor/Google Antigravity into autonomous research/experiment agents, running anywhere (local/SSH/Slurm/Kubernetes/Ray/HF Jobs/Modal/Tinker); rubric-scored; cross-linked both ways with `feynman-analysis.md` (same alphaXiv paper-discovery backend, separate product). Indexed in `docs/non-cc/README.md` and `docs/_topics/harness.md` (plan 0009 row K7).
- `docs/cc-community/CC-community-tooling-landscape.md`: `human-review` (petergyang) — a visual HTML/Markdown review skill that batches Google-Doc-style comments/edits back to the waiting agent, rubric-scored and added to the Comparison table and Sources; cross-linked from the ACE-FCA human-review-gate section of `CC-memory-system-analysis.md` (plan 0009 row K8).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §2: Intent-Router (angel291592) — an intent-compiler skill that converges a vague request into a typed, evidence-backed `IntentSpec` before handoff to a router/agent/workflow, positioned upstream of Jev/Laya-style typed decisions, rubric-scored (plan 0009 row K3).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §7: LlamaParse (LlamaIndex) — the hosted, proprietary document-parsing API LiteParse's own README contrasts itself with (four parsing tiers, bounding-box grounding, version-pinned reproducibility), rubric-scored next to the LiteParse entry (plan 0009 row K1).

- `docs/non-cc/infrastructure/semantic-layers-data-catalog-landscape.md` § Agent-native ontology
  tools: rubric-scores **Utopia** (deeplethe, Apache-2.0), a bottom-up bitemporal ontology platform
  whose `docs/decisions/` folder documents real extraction failures (reversed edges, transitive-
  closure explosions) behind its append-only correction ledger; cross-references and adds
  CHANGELOG-verified compliance-bug evidence (silent empty causal chains, a SHACL validator
  matching no data, dropped RDF provenance metadata — all from Semantica's own v0.6.7 release) for
  the already-documented Semantica entry (§7 of `agent-frameworks-infrastructure-landscape.md`),
  plus the EU AI Act Article 12 record-keeping deadline (now 2027-12-02 for Annex III).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` § 4 Agent Memory
  Infrastructure: rubric-scores **HydraDB** (AGPL-3.0), an object-store-native distributed graph
  database trading RAM ($65–146/GB-mo) for S3-compatible storage (~$0.023/GB-mo) via a
  compare-and-swap writer lease fenced by SlateDB write epochs. § 1: adds a first-party-verified
  addendum (Cordis DI framework's "spatiotemporal composability" paper, the `.agents/notes/`
  decision-record tree) to the existing DeepSeek Harness (`dsh`) profile in
  `docs/non-cc/coding-agents/deepseek-harness-analysis.md`, cross-referenced rather than duplicated.
- `docs/cc-community/CC-community-tooling-landscape.md` § abide: adds complementary,
  independently-verified migration-validation evidence — SWE Refactor Bench (arXiv:2608.23564,
  520 agent migrations, the "Blindness" failure mode), the GAO-25-107795 federal legacy-system
  report, and FreshBrew (arXiv:2510.04852) — cross-referencing the corpus's existing American
  Express Locksmith Loop analysis (`docs/sdlc-lcm/agentic-legacy-migration-validation-analysis.md`)
  rather than restating it.
- Design-lens citations throughout from André Lindenberg's *Artificial Engineering* newsletter
  (five issues: *The Change of Mind Is Information*, *Audit the Auditor*, *The Graph Doesn't Need
  RAM Anymore*, *Everything Is a Plugin, Proven*, *Complete and Correct*), cited as opinion/design
  framing only — every factual claim traces to its own primary source (repo, CHANGELOG, arXiv
  abstract, or GAO report), independently re-verified rather than taken from the article's own
  numbers.
- `docs/_topics/knowledge-graphs.md`, `docs/_topics/memory.md`, `docs/_topics/harness.md`: pointer
  rows/updates for the new entries above.

- `docs/non-cc/infrastructure/jev-analysis.md`: Jev (TypeSafe AI) "System One" decision model — question types (`noul`/`choice`/`score`), pricing and limits, and the qte77/feelings measured pilot using it as a pre-CI code-review gate (184 labelled changes, 78% catch rate / 1.7% false-positive rate at the shipped 0.70 threshold, roughly 70x faster than the fastest and 80x cheaper than the cheapest Claude model tested, a held-out-codebase threshold-transfer failure, and the reword lesson that cut one question's false positives from 6.7% to 0%), rubric-scored against `sdlc-lcm/agent-substrate-rubric.md`.
- `docs/non-cc/infrastructure/code-review-products-landscape.md`: open-code-review (Alibaba; Apache-2.0), a hybrid deterministic-pipeline + LLM-agent PR reviewer, rubric-scored.
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` § 8: a new "Decision models (typed yes/no, choice, score)" sub-list (Jev, and Laya as the open-weight, schema-compatible alternative), and a `.feels()`/`.fill<T>()` sentence extending the BAML bullet.
- `docs/_topics/code-tooling.md`, `docs/non-cc/README.md`: pointer rows for the new Jev page and the open-code-review addition.

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: new landscape page surveying open-weight and research alternatives to TypeSafe's Jev — Laya, kev, CLM/CLM-8B, GLiNER2.5-Decide, RuVector, the JEV-as-a-Judge paper (CMU, arXiv:2609.26550), plus lighter mentions of probably, JevK5, and SemIf — all rubric-scored against the agent substrate rubric. Indexed in `docs/non-cc/README.md` and `docs/_topics/harness.md` (plan 0009 row J3, #517).
- `docs/cc-community/CC-community-tooling-landscape.md`: `abide` (coldteadotai) — AGENTS.md rule enforcement via a per-edit/turn Jev decision-model question, across Claude Code, Codex, and OpenCode.
- `docs/cc-community/CC-code-tooling-landscape.md`: `jevgrep` (dzhng) — a question-driven code-search CLI that uses Jev to judge file/declaration relevance for a coding agent.

- `.github/scripts/lib/doc_graph.py` + `tests/test_doc_graph.py`: deterministic structural doc graph (plan 0009 row G, option B; #504), built test-first. Doc nodes with bucket, status (via `doc_status`) and title; external-domain nodes; aggregated `link` / `hub` / `cites` edges with line numbers; code fences ignored; `docs/archive/` excluded; byte-identical JSON regardless of input order.
- `.github/scripts/build-doc-graph.py` and `make graph-data`: write the graph to `ui/doc-graph.json` (no LLM, stdlib only).

- `ui/doc-graph.html`: live structural doc graph page (plan 0009 row G slice 2; #504) rendering the deterministic `doc-graph.json` with the vendored vis-network, in EyeRest tokens. Docs are dots, topic hubs diamonds, cited domains squares (toggle, hidden by default), with search, a details panel and a GitHub link per doc. Linked from the landing page and the README.

- `ui/build-info.js`, `scripts/build-site-info.py`, `pages_build.read_version` / `site_info` (test-first): every page shows the release version, last-modified date and commit link from a deploy-time `build.json`. The knowledge graph shows its own last-rebuild commit and date, not the deploy's. The deploy injects the tag into the published copy only, so `ui/graph.html`'s history still dates the real rebuild.

- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md` § 1 "-engineering" ladder: new
  **Graph engineering** row (Hamel Husain's coining post, verified via Turing Post's independent
  account and its debunking of viral Microsoft/Stanford/Anthropic misattribution) plus two design-lens
  paragraphs — graph engineering as the wiring already present in shipped software factories, and
  three 2026 data points on the Harness-engineering Verification axiom's cost: Dan Shapiro's
  five-levels framework, METR's RCT (developers estimated 20% faster, measured 19% slower), Faros
  AI's telemetry (+242.7% incidents/PR, +54% bugs/developer, re-verified at source), **Specula**
  (arXiv:2607.25333 — 48 projects, 249 bugs/207 new/68 confirmed/24 fixed, $19–168 median $57,
  93%/47% Sonnet-4.6/Haiku-4.5 spec quality, all figures pulled directly from the paper PDF), and
  **Bend 2** (Apache-2.0, 23,165★, README-quoted proof-gating mechanism) against Martin Kleppmann's
  seL4 formal-verification cost anchor (8,700 LOC / 20 person-years / 200,000 Isabelle lines), and
  SysMoBench's own SIGOPS write-up (~46%/41% conformance/invariant aggregate + 3 named LLM modeling
  failure modes). All quotes and figures verified against their primary source (arXiv PDF, `gh api`
  repo/README fetch, vendor's own published page) in this same session, including two corrections
  made after an adversarial advisor pass: Shapiro's Level 3/4 quotes were re-fetched verbatim rather
  than taken from the newsletter's paraphrase, and Bend's mechanism description was re-grounded in
  its own README instead of the newsletter's framing.
- `docs/sdlc-lcm/software-factory-landscape.md` § (c): one-sentence cross-reference tying the
  graph-engineering framing to the existing four-source human-gate convergence already documented
  there.
- `docs/_topics/harness.md`: one pointer row for the new Graph-engineering/Verification-axiom
  content above.
- Design-lens citations from André Lindenberg's *Artificial Engineering* newsletter (four issues:
  *From Loops to Graphs*, *The Most Expensive Rung on the Ladder*, *The Half We Don't Budget For*,
  *Laws Instead of Diffs*), cited as opinion/design framing only — every factual claim traces to its
  own primary source (arXiv abstract/PDF, `gh api`, a vendor's own published telemetry, or a named
  blog post), independently re-verified rather than taken from the article's own numbers.

- `docs/sdlc-lcm/agent-substrate-reference-architecture.md` (plan 0009 row Y): synthesis of the 61
  rubric rows across 21 corpus docs into one store-first reference architecture for shared, versioned,
  traceable agent memory and context — the argument (Reproducible as the discriminating property; the
  model as a client of a version-controlled store), an 8-subject × 6-property evidence matrix with every
  cell linked to its scored row, five layers (store, propose→gate→commit write path, share, trace, human
  gates at spec and merge), a composed rubric row, the census-confirmed open cells, and a mapping of the
  layers to qte77 estate repos already described in the corpus. Adds no new facts and re-scores nothing.
- `docs/sdlc-lcm/README.md`, `docs/sdlc-lcm/agent-substrate-rubric.md` (Sources), `docs/_topics/README.md`:
  one pointer row/line each to the new page.

### Changed

- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §4: extended the Sumanth077/Hands-On-AI-Engineering bullet with `ai_agents/grounded_document_agent` (LlamaParse-backed, citation-grounded local PDF Q&A example).
- `docs/_topics/rag.md`: extended the existing § 7 hub row to name document parsing (LiteParse, LlamaParse).
- `docs/_topics/harness.md`: added hub rows for OpenResearch, Intent-Router, and human-review.

- `docs/sdlc-lcm/agentic-sdlc-patterns.md`: repointed the "Gap: no review agent" row to the new Jev analysis page (still Trial, not adopted).

- `docs/cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md`: added `jev-ultrafast` (browser-use) to the Alternative MCP Options table — a decision-model-driven browser agent, distinct from browser-use itself.
- `docs/non-cc/protocols/agents-md-cookbook-analysis.md`: cross-linked `abide` from the Coldtea field-study section (same maker).
- `docs/cc-community/CC-codex-plugin-cc-analysis.md`: cross-linked `abide` as the same one-agent-gates-another Stop-hook pattern applied to rule enforcement rather than code review.
- `docs/_topics/plugins.md`, `docs/_topics/code-tooling.md`: extended existing hub rows to name `jev-ultrafast` and `jevgrep`.

- `.github/workflows/gh-pages.yaml`: the deploy now builds `doc-graph.json` from `docs/` (stdlib, no LLM) and also runs on changes to `docs/**` and the graph builder. The JSON is gitignored and never committed.

- `docs/cc-native/**`: doc status moved from the body `**Status**:` badge into a frontmatter `status:` token (63 docs, #348). Any extra badge text (license, version, availability) moves to a `**Details:**` line in the same place. Two badges without a vocabulary word get a default token and keep the full badge text as Details: `CC-sandbox-bwrap-host-quirks.md` → `reference`, `CC-cowork-plugins-enterprise-analysis.md` → `generally-available`.

- `docs/sdlc-lcm/**`, `docs/plans/**`, `docs/non-cc/{agents,coding-agents,context-memory,knowledge-management,orchestrators,protocols}/**`: doc status moved from the body `**Status**:` badge into frontmatter `status:` (95 docs, #348), extra badge text kept as a `**Details:**` line. Plans keep their existing `status:` (draft/approved/done); their `Reference (plan)` label badge is dropped.

- `docs/non-cc/{frameworks,infrastructure,reference}/**`, `docs/cc-community/**`: doc status moved from the body `**Status**:` badge into frontmatter `status:` (56 docs, #348). This completes the corpus migration: `check-doc-status.py --strict` now reports 0 residual badges.

- `CONTRIBUTING.md` §1–§2: doc status lives only in frontmatter `status:`. §2 "Status Badge" is replaced by "Frontmatter status", which points to `VOCAB` in `.github/scripts/lib/doc_status.py` as the one list of tokens. Extra detail goes on a `**Details:**` line (#348).
- `Makefile` `check_status`: now runs `--strict`, so CI (`lint.yaml`) fails on any body `**Status**:` badge.
- `docs/architecture.md` "Frontmatter Conventions": now points to CONTRIBUTING §1–§2 instead of keeping its own copy, which had drifted (`description:` vs `purpose:`).
- `.claude/skills/adding-research-source`: writes `status:` in frontmatter instead of a badge.
- `docs/plans/2026-07-05-0003-status-frontmatter-migration.md`: marked done.

- `README.md`: new "Current focus" bullet linking the agent substrate rubric and the reference architecture (plan 0009, #509).
- `docs/UserStory.md`: adds the arc's user story (tools scored on one six-property rubric). The constraints now match the repo: stdlib doc tooling (validators, doc graph) is in scope, and CI documentation validation is no longer listed as out of scope.
- `docs/plans/2026-09-27-0009-focus-shared-memory-context.md`: arc closed; every row shipped or dropped.

## [0.12.0] - 2026-09-30

### Added

- `docs/cc-native/sessions/CC-session-cost-analysis.md`: redeemable limit resets (help-center article 17007452): refills the five-hour *or* the weekly limit; redeemed via Settings > Usage → "Reset for free", with no button in the CC terminal or IDE. Also records the in-app UI text, which conflicts with the article (it says a reset refills *both* limits), and CC's auto-continue at limit reset (v2.1.234+, v2.1.271+).

- `docs/cc-native/sessions/CC-session-cost-analysis.md`: Fable models on subscription plans (help-center article 15424964). On Max and premium seats, Fable has a 50% weekly sub-cap that also draws from the regular weekly limits; on Pro and standard seats it runs on usage credits. Adds the CC version gates (Fable 5: v2.1.170+, Fable 5.1: v2.1.255+).

- `docs/sdlc-lcm/agent-substrate-rubric.md`: a single scoring rubric for the plan 0009 research. It scores shared, distributed, reproducible, adaptable, versionable and traceable across memory, ontology, graphs/RAG, context, skills, plugins, harness and long-running tasks, with evidence rules and a per-tool table format. Linked from the `sdlc-lcm` index and `docs/_topics/`.

- `.github/workflows/llm-model-eval.yaml`, `.github/scripts/eval-relevance-models.py`, `.github/scripts/lib/relevance_eval.py`: one-off `workflow_dispatch` eval comparing three Cloudflare Workers AI models (`@cf/meta/llama-3.1-8b-instruct-fp8`, `@cf/qwen/qwen3-30b-a3b-fp8`, `@cf/google/gemma-4-26b-a4b-it`) against the retired GitHub Models gpt-4o-mini verdicts for the rxiv-paper-eval relevance filter, now that GitHub Models has been retired (2026-07-30). Reproduces the retired pipeline's exact prompt/parsing (`qte77/gha-rxiv-paper-eval` v0.4.0 `eval_papers.py`) over weeks 22/23/24/25/30, under `strict`/`relaxed` generation configs, with a preflight step that detects an under-scoped Workers AI token (401/403) before burning the full run.

- `.github/scripts/lib/relevance_eval.py`, `eval-relevance-models.py`, `.github/workflows/llm-model-eval.yaml`: `prompt_variant` choice input (`default` | `no-borderline-yes`). The new variant drops only the production prompt's "When borderline, prefer YES" sentence, to test whether it drives false accepts (#527). The summary records the variant.

- `docs/_topics/context.md`, `docs/_topics/skills.md`, `docs/_topics/plugins.md`, `docs/_topics/harness.md`, `docs/_topics/long-running.md`: 5 new topic hubs completing the plan 0009 agent substrate rubric's 8-subject coverage. Linked from `docs/_topics/README.md` and the rubric's Subjects table.

- `docs/non-cc/context-memory/mitosis-cortex-analysis.md`: analysis of Mitosis Labs' hosted Cortex memory system (kNN + full-text + one-hop graph fusion, no LLM at query time, per-team isolation), rubric-scored against `sdlc-lcm/agent-substrate-rubric.md`; flags that the plan's cited "Agentic Memory Index" benchmark site moved from `x402oracle.com` to `verginglabs.com` with a different overall score.
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` § 4: AgentiCow (copy-on-write vector memory branching), Beads/bd (Dolt-backed distributed agent memory/task graph), lossless-memory (timestamp-first, never-summarize personal memory), the Weighted Memory Tree and JITMEM papers, and a worked-example pointer to Sumanth077/Hands-On-AI-Engineering — all rubric-scored.
- `docs/cc-community/CC-memory-tooling-landscape.md`: agent-memory (tigerless-labs), a markdown-native long-term memory runtime shared by Claude Code, Codex CLI and Hermes, rubric-scored.
- `docs/_topics/memory.md`, `docs/non-cc/README.md`: pointer rows for the above.

- `docs/non-cc/infrastructure/semantic-layers-data-catalog-landscape.md` § Formal Ontologies: a new "Agent-native ontology tools (2026 MCP wave)" subsection covering Ontology Atlas (git-versioned Markdown ontology, MCP-native), open-ontologies (Rust MCP server, Lean-4-certified plan/apply/rollback), EvoOntology (self-evolving ontology layer for data agents, arXiv:2609.15779), and AWS context-ontology-accelerator (namespace-RBAC, AWS CDK-deployed semantic context platform) — all rubric-scored against `sdlc-lcm/agent-substrate-rubric.md`. The AWS accelerator's namespace-scoped RBAC and CDK microservice deployment are the first `Shared`/`Distributed` = `yes` evidence in the ontology docs.
- `docs/_topics/knowledge-graphs.md`: a pointer row for the new subsection.

- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` § 7: a new "Agent-native graph & hybrid RAG platforms" subsection — SSTorytime (Postgres graph via MCP), Omnigraph (git-branching multi-agent lakehouse graph), Semantica (graph-native decision infrastructure), WeKnora (Tencent RAG/agent/wiki platform), and BrainAPI (event-centric graph memory, BSL-1.1) — all rubric-scored, adding first Shared evidence (Omnigraph, WeKnora score `yes`) to the Graphs/RAG subject; Reproducible remains largely open (only SSTorytime documents an LLM-free ingestion path).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` § 7 intro: LiteParse (run-llama), a local LLM-free PDF/document parser that feeds RAG ingestion.
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` § 4/§ 7: rubric rows for Microsoft GraphRAG, LightRAG and Cognee (row G graph-system decision), plus a Sumanth077/Hands-On-AI-Engineering pointer to its `agentic_rag_system` example.
- `docs/_topics/rag.md`: pointer rows for the above.

- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: four new subsections, all rubric-scored against `sdlc-lcm/agent-substrate-rubric.md` and fetched first-party 2026-09-30 — "CLAUDE.md Growth and Catastrophic Remembering (arXiv 2608.11095)" (empirical instruction-file bloat study, cross-referenced to CC's own stripped maintainer HTML comments), "Practitioner Template: context-engineering-intro" (coleam00's MIT-licensed PRP starter template, 13.9k★), "A Non-CC Comparison: Topic-Label Gating (TrackPoint)" (vendor pattern compared to CC's MEMORY.md-index/topic-file split; self-reported, unverified), and "Scored on the Agent Substrate Rubric" (CC's CLAUDE.md/auto memory system scored from a fresh fetch of `code.claude.com/docs/en/memory` — Shared and Versionable move to `partial`, Distributed to a sourced `no`, Traceable to `partial` via the `InstructionsLoaded` hook and `/doctor prompt-audit`). Partly fills plan-0009 Context coverage gaps 1–4; the ACE-FCA phase artifacts (`research.md`/`plan.md`/`implement.md`) named in gap 4 stay unresolved since no first-party source states they are git-tracked.
- `docs/_topics/context.md`: 3 new pointer rows for the above.

- `docs/non-cc/protocols/agent-plugins-standard-analysis.md`: a "Concrete implementation: Mitosis Memory (`mitosis-agent-plugin`)" section — the Agent Plugins 1.0.0 open standard's first confirmed client implementation found in this corpus (Mitosis Labs' MIT-licensed `mitosis-agent-plugin` + `mitosis-memory-skills`, bundling a remote MCP server with seven memory skills across four clients), rubric-scored, with the "no confirmed client implementations" hedge updated accordingly. Cross-linked from `mitosis-cortex-analysis.md`.
- `docs/non-cc/agents/goose-analysis.md`: an "Agentic AI Foundation (AAIF): governance and hosted projects" section — the foundation's 8 working groups and 6 hosted projects (MCP, AGENTS.md, agentgateway, A2A, Agent Router, Goose), and why its relevance to skills/plugins standards is indirect (via MCP and AGENTS.md, not a dedicated skills/plugin spec — that's the separate Agent Plugins standard).
- `docs/cc-community/CC-community-skills-landscape.md`: new entries for `coleam00/skills` (34-skill PIV loop + hooks, MIT), `coleam00/excalidraw-diagram-skill` (no LICENSE file — confirmed via the GitHub contents API), and `cloudflare/security-audit-skill` (six-phase audit skill with adversarial validation and a JSON-schema-verified findings trail — the strongest Traceable score in the set), all rubric-scored.
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` § 1: extended the existing Runtype bullet with `runtypelabs/skills` (official platform + tool-design skills, MIT), rubric-scored.
- `docs/non-cc/frameworks/agent-skill-evolution-research-landscape.md` (new page): four skill-construction/evolution research efforts — WikiSkill (arXiv:2608.27454), AutoTailor (arXiv:2609.13548), SkillLift (arXiv:2609.15396 + `WalteR-MittY-pro/SkillLift`, MIT), and NVlabs Skill2Env (Apache-2.0) — each rubric-scored, with `n/a` used where a property doesn't apply to a research paper.
- `docs/cc-native/plugins-ecosystem/CC-plugin-packaging-research.md` § 5: closes coverage gap 10 (Plugins · Reproducible) — Claude Code's plugin manifest `version` field and marketplace `ref`/`sha`/`sha256` source pinning, quoted from the current first-party manifest and marketplace references, with a rubric table for the packaging system itself (Reproducible scored `partial`: the pinning primitive exists but is opt-in).
- `docs/_topics/skills.md` and `docs/_topics/plugins.md`: pointer rows for all of the above.
- Considered and not added: `github.com/tysoncung` (personal account; its only two agent-adjacent repos, `notion-agent-hub` MIT and `awesome-vibe-coding` CC0-1.0, are a small Notion/MCP hub and a generic curated list, neither skills/plugins-specific) and "Xpert plugins" (a batch-2 screenshot lead with no identifiable first-party source).

- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §1: four new rubric-scored entries fetched first-party 2026-09-30 — Archon (coleam00, MIT, "the first open-source harness builder for AI coding"), Paperclip (paperclipai, MIT, org-chart agent-team orchestration), AX (google/ax, Apache-2.0, Kubernetes-style declarative agent orchestrator built on Agent Substrate), and OperatingSystem-1's harness tools (`mcp-git-coord` — no LICENSE file despite the README's own "MIT" claim — plus `openclaw-operator`, confirmed to be a dormant fork of `stubbi/openclaw-operator`, not original work; the entry cross-refs `goclaw-analysis.md`, confirming against `openclaw.ai` that this is the same OpenClaw platform GoClaw reimplements, not a different product).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §4: the existing `Sumanth077/Hands-On-AI-Engineering` bullet now also names `self_evolving_code_review_agent` and `multi_agent_coding_assistant` as harness-relevant examples (one-line mention, no rubric, per the bullet's existing precedent).
- `docs/non-cc/infrastructure/nvidia-openshell-analysis.md` (new page): NVIDIA OpenShell — kernel-enforced, formally-verified policy runtime for agent fleets (Apache-2.0, 11,079★), rubric-scored. Indexed in `docs/non-cc/README.md`.
- `docs/non-cc/reference/orcareplay-analysis.md` (new page): OrcaReplay — record/replay/fork debugger for coding-agent runs with byte-for-byte deterministic offline replay (Apache-2.0 code / CC BY 4.0 trace spec, 268★), rubric-scored. Direct first-party evidence filling plan-0009 gaps 7 (Long-running · Traceable) and 8 (Long-running · Reproducible). Indexed in `docs/non-cc/README.md`.
- `docs/non-cc/reference/weco-aide-recursive-self-improvement-analysis.md`: two new subsections — RRSI (google-research/rrsi, Apache-2.0, code available; git-worktree-per-candidate harness versioning fills gap 9, Harness · Versionable) and ROFT (arXiv 2609.35741, CC BY 4.0, paper only, no code URL found).
- `docs/cc-community/CC-harnessrouter-analysis.md`: refreshed stars (2,496 → 2,789) and latest release (`v0.23.11` → `v0.26.16`), and a new rubric section scored against `sdlc-lcm/agent-substrate-rubric.md`.
- `docs/_topics/harness.md`: 5 new pointer rows (HarnessRouter, the frameworks-landscape §1 orchestration tools, OpenShell, OrcaReplay, the RRSI/ROFT comparison).
- `docs/_topics/long-running.md`: 2 new pointer rows (OrcaReplay; google/ax `suspend`/`resume` + Paperclip heartbeat agents).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §1: the Runtype entry gains `runtypelabs/hermes-runtype-otel` (MIT, per-turn OTel traces from Hermes, rubric-scored) and `runtypelabs/persona` (MIT chat widget, unscored UI layer).

### Changed

- `docs/UserStory.md`: added the browse-by-subject story (`docs/_topics/` hubs) and updated success criterion 1 to the `docs/non-cc/<section>/` layout plus the hub-row step.

- `docs/sdlc-lcm/agent-substrate-rubric.md`: Subjects table now points Skills, Plugins, Harness and Long-running at their new hubs instead of "hub planned, row C"; Context now also links `context.md`.

- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: `updated`/`validated_links` bumped to 2026-09-30.

- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md`, `docs/cc-community/CC-harnessrouter-analysis.md`, `docs/non-cc/reference/weco-aide-recursive-self-improvement-analysis.md`: `updated`/`validated_links` bumped to 2026-09-30.

- `README.md`, `docs/UserStory.md`: the topic-hub subject list now names the five hubs added in plan 0009 row C (context, skills, plugins, harness, long-running tasks).

## [0.11.0] - 2026-09-25

### Added

- `docs/_topics/`: cross-subject topic hubs (memory, knowledge graphs, RAG, code tooling, visualization) that point at docs and sections across `cc-native/`, `cc-community/`, `non-cc/` and `sdlc-lcm/`; linked from `README.md` (#309).

### Changed

- `docs/non-cc/knowledge-management/repo-to-docs-tools-landscape.md`, `deepwiki-analysis.md`: the DeepWiki landscape entry is now a pointer; its unique facts moved into the full analysis (#309).
- `docs/non-cc/context-memory/cocoindex-analysis.md`: dropped the duplicated `cocoindex-code` stats and specifics, which had drifted inside the file; `cc-community/CC-code-tooling-landscape.md` is the canonical `cocoindex-code` entry (#309).

- `CONTRIBUTING.md`, `docs/architecture.md`: directory trees list `docs/_topics/`.
- `.claude/skills/adding-research-source/SKILL.md`: new docs on a hub subject get a row in the matching `docs/_topics/` hub.

## [0.10.0] - 2026-09-25

### Changed

- `scripts/restructure_links.py`, `docs/non-cc/.restructure-map.tsv`, `docs/non-cc/orchestrators/`: #309 Phase 1, step 1 of the `docs/non-cc/` faithful-9 subdir restructure. Added a stdlib-only, typed move-and-rewrite tool that repoints every relative markdown link repo-wide when docs move (inline links, reference-style definitions, anchors kept, fenced code blocks left alone), backed by a generated filename-to-subdir mapping file for all 93 `docs/non-cc/` docs. Used it to move the smallest section, Orchestrators (6 docs: `air-`, `deerflow-`, `devteam-`, `omnigent-`, `qm-`, `raven-analysis.md`), into `docs/non-cc/orchestrators/`, updating `docs/non-cc/README.md`'s index and every inbound cross-reference. The remaining 8 sections (Agents, Coding Agents & IDEs, Knowledge Management, Reference & Background, Context & Memory Infrastructure, Infrastructure, Frameworks, Protocols & Interfaces) move in follow-up PRs using the same tool.

- `docs/non-cc/knowledge-management/`: moved the 6 knowledge management docs into their own subdirectory with `scripts/restructure_links.py`; all relative links repo-wide rewritten (#309 Phase 1 step 2).

- `docs/non-cc/protocols/`: moved the 7 protocols docs into their own subdirectory with `scripts/restructure_links.py`; all relative links repo-wide rewritten (#309 Phase 1 step 3).

- `docs/non-cc/reference/`: moved the 8 reference docs into their own subdirectory with `scripts/restructure_links.py`; all relative links repo-wide rewritten (#309 Phase 1 step 4).

- `docs/non-cc/context-memory/`: moved the 9 context memory docs into their own subdirectory with `scripts/restructure_links.py`; all relative links repo-wide rewritten (#309 Phase 1 step 5).

- `docs/non-cc/agents/`: moved the 10 agents docs into their own subdirectory with `scripts/restructure_links.py`; all relative links repo-wide rewritten (#309 Phase 1 step 6).

- `docs/non-cc/infrastructure/`: moved the 12 infrastructure docs into their own subdirectory with `scripts/restructure_links.py`; all relative links repo-wide rewritten (#309 Phase 1 step 7).

- `docs/non-cc/frameworks/`: moved the 13 frameworks docs into their own subdirectory with `scripts/restructure_links.py`; all relative links repo-wide rewritten (#309 Phase 1 step 8).

- `docs/non-cc/coding-agents/`: moved the 22 coding agents docs into their own subdirectory with `scripts/restructure_links.py`; all relative links repo-wide rewritten (#309 Phase 1 step 9).

- `CONTRIBUTING.md`, `docs/architecture.md`: directory trees list the 9 `docs/non-cc/<section>/` subdirs.
- `.claude/skills/adding-research-source/SKILL.md`: new non-cc docs go into the `docs/non-cc/<section>/` subdir that matches their README section.

- **Breaking for inbound links:** all 93 `docs/non-cc/*.md` URLs moved to `docs/non-cc/<section>/*.md` (9 section subdirs: orchestrators, agents, coding-agents, knowledge-management, reference, context-memory, infrastructure, frameworks, protocols; #489–#498). GitHub does not redirect moved files, so update any external link or bookmark to the new path. The section index is `docs/non-cc/README.md`.

### Removed

- `scripts/restructure_links.py`, `tests/test_restructure_links.py`, `docs/non-cc/.restructure-map.tsv`: one-off #309 Phase 1 move tooling, removed after all 9 moves (#489–#497). Recoverable from commit `7179e0a`.

## [0.9.1] - 2026-09-25

### Added

- `docs/cc-native/sessions/CC-session-cost-analysis.md`: new "Shared plan usage across Claude products" section — the one usage limit shared by claude.ai/Claude Code/Claude Desktop, the five-hour reset shown at Settings > Usage, sign-in-based metering (Enterprise seat pool vs API-key pay-per-token), the owner-observed per-product usage split undocumented in the help center, and a "Local tools vs plan usage" subsection on why `/stats` and CodeBurn's transcript-based commands undercount total plan usage (with `codeburn quota` as the live-data exception).

- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: added Agent Zero Memory (arXiv:2608.29606, provenance-aware three-structure memory, 95.60% LongMemEval / 93.60% LoCoMo self-reported, "up to 20x lower cost per query" per the paper) and HarnessEvolve (arXiv:2609.00829, reference-trajectory-based agent self-evolution with quality/performance gates) to the Agent Memory Infrastructure catalog; both paper-only, no code/project link found in the abstract or HTML paper body.
- `docs/cc-native/agents-skills/CC-skills-adoption-analysis.md`: added Repo-To-Skill / DisCo (arXiv:2609.02749, AREX-Skill Library distilling 5,000+ skills from 1,000 ML repos; 134.3%/34.4% MLE-bench/PaperBench gains with GPT-5.5) to the Ecosystem Context table and paragraphs, with its `VectorSpaceLab/AREX-Skill` code repo verified via `gh api` (Apache-2.0, 308 stars).

### Changed

- `.github/scripts/lib/changelog.py`, `.github/scripts/changelog-compare.py`, `.github/workflows/cc-changelog-monitor.yaml`: the changelog monitor now fetches `claude-code`'s `releases.atom` and, when it parses successfully, uses its per-id dedup ledger (`.github/state/native-monitor-state.json`, key `cc-changelog-releases`) to decide which feed-covered versions are new and to annotate each with its release date; the scan-doc version-range cutoff acts as the bootstrap/window-rollout safety net and as the fallback for any version the feed doesn't cover — a feed/changelog skew gap, or the feed being unavailable entirely. `CHANGELOG.md` remains the sole content source in both paths (#410).

- `README.md`, `docs/UserStory.md`, `docs/architecture.md`, `docs/non-cc/README.md`, `docs/non-cc/air-analysis.md`, `docs/non-cc/devteam-analysis.md`, `docs/non-cc/karpathy-llm-kb-analysis.md`, `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: `coding-agent-eval` references repointed to `coding-harness-eval` (repo renamed on GitHub; old URLs redirect).

- `docs/cc-community/CC-usage-tooling-landscape.md`: corrected CodeBurn's stale "Menubar v0.9.0 (2026-04-25)" / "Node.js 20+" notes to the current `v0.9.25` (2026-09-21, GitHub Releases + npm registry) and `>=22.13.0` engine requirement; added the confirmed `codeburn doctor` subcommand and `export --billing` flag; added one-line local-transcripts-only blind-spot notes to both CodeBurn and ccusage, cross-linked to the new section above.

## [0.9.0] - 2026-09-24

### Added

- `docs/cc-native/agents-skills/CC-cross-session-messaging-analysis.md`: new analysis of Claude Code's first-party cross-session messaging — `ListAgents`/`SendMessage`, `/list-agents` (`/peers`), the delivery/trust model (`crossSessionInbound` accept/hold/refuse, `isolatePeerMachines`), `notify_when_idle`, cross-machine messaging via Remote Control, the inbox socket (`CLAUDE_CODE_MESSAGING_SOCKET`/`CLAUDE_CODE_MESSAGING_TOKEN`), limits, and version gates (v2.1.224 base feature through v2.1.271) cross-checked against the `anthropics/claude-code` CHANGELOG — flags an unreconciled native-Windows gate discrepancy between the docs page (v2.1.234) and the CHANGELOG (v2.1.239). Closes #438.
- `docs/cc-native/agents-skills/CC-agent-teams-orchestration.md`: currency-pass correction on the "UDS Inbox (Unreleased)" section — the leaked mechanism it described has shipped as the documented cross-session messaging feature; cross-referenced to the new doc.

- `docs/cc-community/CC-memory-tooling-landscape.md`: five new cross-agent/procedural-memory tool entries — `ai-memory` (akitaonrails, Rust, MIT, cross-agent handoff wiki), `claude-reflect` (BayramAnnakov, MIT, correction/preference capture into CLAUDE.md/AGENTS.md), `Core` (RedPlanetHQ, AGPL-3.0, self-hosted personal AI OS delegating to Claude Code/Codex, 88.24% self-reported LoCoMo), `deja-vu` (vshulcz, MIT, Go, retroactive cross-agent session index, 88.1% hit@1 LongMemEval-S / 70.5% hit@1 LoCoMo self-reported), and `engrim` (timgordontg, MIT, SQLite episodic store across 7 agent environments). New rows added to the LongMemEval and LOCOMO benchmark tables for the tools reporting scores.

- `docs/cc-community/CC-community-tooling-landscape.md`: TeamAI-CLI (Tencent) — git-backed shared skills/rules/MCP/hooks across 15+ agent harnesses; herdr (herdrdev) and Zeron (zeronsh) — persistent/local-first coding-agent session runtimes. Three new Comparison rows + Sources entries.
- `docs/cc-community/CC-code-tooling-landscape.md`: tgrep (microsoft) — trigram-indexed grep, no first-party Claude Code integration (Codex/pi only); zg / zvec-grep (zvec-ai) — local ripgrep+BM25+vector search with a documented `zg --install --target claude` installer.
- `docs/cc-community/CC-agent-flow-visualizer-analysis.md`: new analysis of Agent Flow (patoles) — real-time Claude Code / Codex run visualization via hooks + Codex rollout tailing.
- `docs/cc-community/CC-book-to-skill-analysis.md`: new analysis of book-to-skill (virgiliojr94) — converts books/documents into on-demand Claude Code Skills, with a first-party reproducible 24×–51× token-cost benchmark.

- `docs/cc-community/CC-harnessrouter-analysis.md`: new analysis of HarnessRouter, an Apache-2.0 self-hosted unified API (the Unified Harness Protocol, UHP) that routes a single client contract across multiple coding-agent harnesses (Codex, Claude Code, Hermes, DeepSeek Harness, Pi) — Gateway/Runner/Console architecture, Docker install, and an Assess verdict pending maturity.
- `docs/cc-community/CC-netdata-mcp-analysis.md`: new analysis of Netdata's built-in MCP server for incident-time infrastructure queries — data exposure (metrics, alerts, logs, function execution), transport options (WebSocket, HTTP Streamable, SSE, stdio bridge), bearer-token auth, and concrete Claude Code / Cursor connection config.

- `docs/cc-native/sandboxing/CC-sandbox-platforms-landscape.md`: three new Platform Details entries — Blaxel (microVM sandboxes, ~25ms resume, verified pricing), Ephemora Cell (capability-based WASM sandbox for untrusted AI-generated code/MCP tools, 42★ Apache-2.0), forkd (Firecracker microVM fan-out runtime, 2.9k★ Apache-2.0, cross-referenced to the Fork-Join Parallelism pattern).
- `docs/cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md`: two new subsections under Academic Design-Space Analysis — "Applying Anthropic Primitives at Large Enterprises" (arXiv 2608.20622, Salapa) and "An Empirical Study of Harness Design for Coding Agents" (arXiv 2609.20804, Fan et al., 176-setting component ablation).
- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: a context-files correctness ablation (arXiv 2607.27250, Khatri) under Instruction Adherence Patterns with a scope note distinguishing correctness from adherence, plus a new "Enterprise Agent Memory Beyond CC" section comparing Claude Managed Agents memory stores, Microsoft Copilot Studio memory, and the Grounding Agent Memory research (arXiv 2609.11060, Microsoft).
- `docs/cc-native/agents-skills/CC-ralph-enhancement-research.md`: cross-reference to `anthropics/cwc-long-running-agents`, Anthropic's reference hooks/subagent kit for long-running agent harnesses, alongside the existing "Effective Harnesses" blog citation.

Plan 0008 row 20, batch 05.

- `docs/cc-native/ci-remote/CC-cloud-sessions-analysis.md`: documents Claude Code's self-hosted environments (public beta, Team/Enterprise) — named environments grouping self-hosted runners, network/credential model, and Zero Data Retention exclusion — cross-checked against `code.claude.com/docs/en/self-hosted-environments`.
- `docs/cc-native/configuration/CC-bash-mode-analysis.md`: adds "Is Bash All You Need?" (Microsoft/CMU, arXiv:2609.11999) as related third-party evidence for bash-as-tool-interface design, with the paper's benchmark deltas (TheAgentCompany, APEX-Agents) and PTC comparison.
- `docs/cc-native/model-internals/CC-first-party-interpretability-index.md`: adds "Evaluating and Improving LLM Self-Modeling" (arXiv:2608.30980, Anthropic co-authored) to the Foundational Interpretability table, and a new "Agent Autonomy & Deployment" section covering Anthropic's "Measuring Agent Autonomy" research (Claude Code + public-API session analysis).
- `docs/cc-native/plugins-ecosystem/CC-office-document-skills.md`: adds LandingAI's `ade-document-processing-skills` (MIT, Claude Code/Cursor/Roo Code) to Layer 3 community skills.
- `docs/cc-native/plugins-ecosystem/CC-mcp-hardware-standard-analysis.md`: new doc analyzing Anthropic's Model Hardware Standard (MHS) research preview — physical lab/manufacturing hardware integration, its relationship to MCP (a transport, not a superset), partners, and applicability.

- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: 16 new first-party-verified entries from screenshot-lead research batch 07 — Fractal and Agent Reach (orchestration/tooling), Graft (codebase-context GraphRAG variant), exxperts/IWE/LightMem/Maximem Synap/MemMachine/Memento/Memorable/Metis/Neo4j Agent Memory/Reef (agent memory infrastructure), TradingAgents (production reference framework), and two memory-research papers (memory portability across model upgrades; fragility of self-improving agents). Extended the existing Agno entry with its AgentOS/"self-driving agent platform" positioning, license and star count.

- `docs/non-cc/research-agents-landscape.md`: CEDAR (Sakana AI, Yingtao Tian — LLM-agent MCTS for goal-directed complex-system design, ALIFE 2026), Hyperresearch (jordan-gibbs — Claude Code deep-research skill, MIT), OpenScience (Synthetic Sciences — open-source AI research workbench, Apache-2.0), and ScientistTwo (Google Cloud AI Research — autonomous end-to-end research + self-peer-review system) to §1 Autonomous Research Agents; Hyperresearch also added as a row + rewritten Takeaway in the `/deep-research` harness mapping table.
- `docs/non-cc/agentic-enterprise-os-landscape.md`: Glean Independent Agents (Tier 1 enterprise vendor platforms, with a caveat noting its A2A/AG-UI posture was not confirmed) and HugAgentOS (Tier 2 open-source self-operating workspaces — ZJU-REAL, source-available Apache-2.0 + Additional Terms, ontology-as-control-plane).

- `docs/non-cc/prime-agent-analysis.md`: new doc on Prime Intellect's Prime Agent, an open-source self-improving RLM coding harness (arXiv:2608.23552).
- `docs/non-cc/semantic-layers-data-catalog-landscape.md`: Vault-LD (Markdown-vault-as-linked-data spec) added to Formal Ontologies & Semantic Web; Symbolic Separation (arXiv:2609.17107) added to The Agent-Native Layer.
- `docs/non-cc/web-scraping-extraction-landscape.md`: Lightpanda (from-scratch Zig headless browser) added to Browser Automation; Docling Graph (IBM-sponsored doc-to-knowledge-graph pipeline) added to Document-Specific Extraction.
- `docs/non-cc/ag-ui-protocol-landscape.md`: OpenBot (CopilotKit governed AI-coworker template with CEL policy gateway) section added.
- `docs/non-cc/agent-observability-methods-analysis.md`: Superlog (OTel + MCP telemetry-investigation tool) added to the Multi-Agent Observability Pattern section.

- `docs/non-cc/agent-plugins-standard-analysis.md`: new analysis of the Agent Plugins open standard (v1.0.0) for packaging Agent Skills and MCP servers across AI agent clients — spec structure, TSC governance (Amazon/Cursor/Microsoft/OpenAI/Vercel core maintainers), dual CC-BY-4.0/Apache-2.0 licensing, and its parallel to the AGENTS.md config-fragmentation problem.
- `docs/non-cc/ai-trader-analysis.md`: new analysis of ai4trade.ai's root SKILL.md as an agent onboarding/routing surface for Claude Code, Codex, and Cursor — trading-signal publishing, copy trading, and challenge mechanics, with an explicit unverifiable/hedged section for the missing repo/license/maintainer information.
- `docs/non-cc/apache-maka-analysis.md`: new analysis of Apache Maka (Incubating), a local-first agent workspace whose append-only `RuntimeEvent` log is the runtime source of truth — architecture, Apache Incubator podling status (no ASF release yet), and verified repo stats.
- `docs/non-cc/auto-agi-compiler-analysis.md`: new analysis of RightNow AI's AUTO compiler and its "Auto: The AGI Compiler" paper (arXiv:2607.04542) — deterministic-span extraction to sandboxed WASM binaries, with the paper's benchmark figures clearly labeled as self-reported and the repo flagged as dormant since 2026-07-07.
- `docs/non-cc/corsair-analysis.md`: new analysis of Corsair's unified integration/managed-OAuth layer for agents — flags a GitHub license-detector mismatch (`other`/`NOASSERTION`) against the repo's own unmodified Apache-2.0 `LICENSE` file text.
- `docs/non-cc/deepcode-analysis.md`: new analysis of HKUDS's DeepCode coding-agent harness — current "Open Agentic Coding" framing superseding its original Paper2Code positioning, release history (v2.2.0), and cross-references to the corpus's other HKUDS-lab entries (AutoAgent, OpenHarness, CLI-Anything).
- `docs/non-cc/deepseek-harness-analysis.md`: new analysis of DeepSeek Harness (`dsh`), DeepSeek AI's plugin-native agent harness built on Cordis — developer-preview status, disabled Issues/PRs, and its 234K-star/six-week growth curve reported as-verified via the GitHub API.

- `docs/non-cc/ecdysis-analysis.md`: new analysis of Ecdysis (arXiv:2609.11677) — a failure-aggregation method for training self-evolving LLM-agent runtime harnesses (Failure-Driven Collaborative Refinement); CAS/Beijing Institute of Technology/Tsinghua-affiliated authors, 14-star reference repo with no LICENSE file, self-reported 18.56% accuracy gain / 1.84x faster training.
- `docs/non-cc/frognano-analysis.md`: new analysis of FrogNano (arXiv:2609.07925) — a 4B coding agent from Microsoft Research Montréal's Froggy Team, post-trained via RL-only online task synthesis; no public code/weights/"Leaf" harness release found as of 2026-09-24.
- `docs/non-cc/helixdb-analysis.md`: new analysis of HelixDB — a Rust graph-vector database for knowledge graphs and AI-agent memory (Apache-2.0, 6,087 stars, v3.3.0); covers the multi-language SDK query model and the `helix chef` agent-handoff bootstrapper.
- `docs/non-cc/latticedb-analysis.md`: new analysis of LatticeDB — an embedded single-file Zig graph+vector+full-text database (MIT, 685 stars, v0.15.0); self-reported benchmarks carried with the project's own head-to-head-vs-orientation caveat.
- `docs/non-cc/mex-analysis.md`: new analysis of mex — a Git-shared, human-approval-gated project memory and code-drift-detection CLI for coding agents (MIT, 1,705 stars, v0.8.2); leads with its no-autonomous-write approval boundary.

- `docs/non-cc/nooa-analysis.md`: new analysis of NVIDIA-NeMo Labs' NOOA object-oriented agent framework — Python-class-as-agent paradigm, `...`-body agentic methods, live-object REPL execution, Apache-2.0 license (verified from `LICENSE`, not the GitHub detector).
- `docs/non-cc/openrath-analysis.md`: new analysis of OpenRath, a PyTorch-like multi-agent/multi-session Python runtime (Session/Sandbox/Memory/Tool/Agent/Workflow/Selector) and its v2.0.0 durable-execution layer.
- `docs/non-cc/poolside-laguna-analysis.md`: new analysis of Poolside's Laguna S 2.1 long-horizon agentic coding model (118B/8B-active MoE, 1M context) — benchmarks marked vendor-reported; license flagged unverified ("open-weight" only, no stated license terms).
- `docs/non-cc/programmatic-tool-calling-analysis.md`: new analysis combining the "Bitter Lesson of Tool Calling" arXiv paper (PTC ≥ JSON tool calling in 11/14 models) with the `spec-ptc` speculative-PTC reference implementation and its Claude Code / OpenCode / Pi-mono wrappers.
- `docs/non-cc/qm-analysis.md`: new analysis of QM, Y Combinator's multiplayer agent harness (personal + shared scopes, harness-agnostic core driving Pi/OpenCode/Codex/Claude Code) — YC affiliation confirmed via the `yc-software` GitHub org profile.
- `docs/non-cc/qwenpaw-analysis.md`: new analysis of QwenPaw, AgentScope's self-hosted personal AI assistant on the Qwen model family — three-tier memory via ReMe, multi-channel access, five-layer sandboxing.
- `docs/non-cc/on-device-semantic-search-landscape.md`: extended Layer B with LEANN — recompute-not-store vector index (97% storage savings claim), HNSW/DiskANN backends, native Claude Code MCP server, first-party SWE-Bench Pro recall claim marked vendor-reported.
- `docs/non-cc/pi-analysis.md`: extended with a new "Fork: omp (oh-my-pi)" section covering the Stencil Labs fork's provider/tool/LSP/DAP counts, Rust core, and the omp.sh homepage's separate "omp²" marketing framing.

- `docs/non-cc/raven-analysis.md`: new analysis of Raven (EverMind-AI), a "harness of harnesses" multi-agent orchestrator with a benchmark-gated self-evolution loop (Evolver), EverOS-backed memory, and 13 pluggable third-party coding-agent backends including Claude Code — Apache-2.0, 4,058★ (verified via `gh api`, accessed 2026-09-24).
- `docs/non-cc/ripwire-analysis.md`: new analysis of Ripwire (redhat-et), a zero-dependency C++23 CLI with an optional MCP server producing deterministic, confidence-disclosed repo-context maps (call graphs, impact analysis, quality deltas) for coding agents — Apache-2.0, 2,334★ (verified via `gh api`, accessed 2026-09-24).
- `docs/non-cc/shepherd-analysis.md`: new analysis of Shepherd (arXiv 2605.10913, no institutional affiliation stated in either source) recording agent execution as a reversible, Git-like trace for meta-agent supervision — reports 28.8%→54.7% pair-coding success and a 12.8% Terminal-Bench 2.0 gain over MetaHarness; MIT, 2,440★.
- `docs/non-cc/weco-aide-recursive-self-improvement-analysis.md`: new analysis of Weco AI's AIDE² experiment (blog + arXiv 2609.26457), where an outer-loop agent rewrote the inner-loop AIDE research agent's own code across 100 iterations — flags that the blog's KernelBench reward-hacking figures (63%→34%) and the arXiv abstract's held-out-task-family figure (55%→32%) are easy to conflate but measure different task families; no AIDE² code repo found.
- `docs/non-cc/repo-to-docs-tools-landscape.md`: added OpenKB (VectifyAI) as a sixth entrant — a document-to-wiki CLI (PDF/Word/Markdown/PowerPoint/HTML/Excel/CSV/URLs) built on Karpathy's LLM-wiki concept and PageIndex's vectorless retrieval, OKF-compatible, distilling Claude Code/Codex/Gemini skills — Apache-2.0, 4,556★ (verified via `gh api`, accessed 2026-09-24).

- `docs/sdlc-lcm/agentic-ai-vulnerability-landscape.md`: five screenshot-lead topics verified first-party and added — two open-source vendor security tools in §2 (Secure Agentics **Adrian**, a runtime AI-agent monitor that analyses tool calls and reasoning traces in-flight; NVIDIA **SkillSpector**, a static+LLM security scanner for agent skills with 71 vulnerability patterns) and three 2026 arXiv preprints in §6 (**Collective Loss of Control**, an epidemic model of agent-to-agent unsafe-behavior contagion with the RogueHandoff-20 benchmark; **ContextLeak**, an RL-crafted malicious-tool-description context-exfiltration attack; **Mind Viruses**, an Anthropic-co-authored study of self-propagating ideas in multi-agent LLM systems). Epistemic-role table and Sources table extended to match; `updated`/`validated_links` bumped to 2026-09-24.

- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md`: Retrieval-Invoked Actual-Use Effect (RAE) metric (arXiv:2609.00549, "Skill Following") as a new Tool Selection Accuracy sibling entry; Recent Advance notes for "When Tools Get in the Way" (arXiv:2609.14157, tool-availability accuracy collapse + scope-aware-instruction fix) and MSCE memory-skill co-evolution (arXiv:2607.16621); Landscape References for Tracely (trace-native CI/CD regression testing) and MemTensor/MemOS.
- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: quantified Harness Effect evidence (arXiv:2607.06906) for the Agent = Model + Harness thesis; a 2026 harness-evolution research cluster (HarnessDev, AutoDesign, RobustSGPO) cross-referenced to `harnessx-analysis.md`; Anthropic's AI-Native SDLC Playbook (intent.md/spec.md/plan.md, CLAUDE.md/Skills/Hooks/Evals loop) and SMART (arXiv:2609.05364, design-docs-as-source ML performance tool) in §3.

- `docs/sdlc-lcm/agentic-legacy-migration-validation-analysis.md`: new analysis of American Express's "Locksmith Loop" (arXiv:2607.28271) — agentic Witness Search + parity-preserving mutations for deterministic COBOL-to-Java migration validation without a hand-written oracle; 91.90% branch coverage on an internal production COBOL program.
- `docs/sdlc-lcm/automata-agent-traces-analysis.md`: new analysis of "Automata from Agent Traces" (arXiv:2608.23670) — compact FSM reconstruction from agent trace corpora for model-agnostic failure prediction (AUROC up to 0.94) and safety auditing.
- `docs/sdlc-lcm/detokenization-leaks-analysis.md`: new analysis of "Detokenization Leaks" (arXiv:2609.06674) — a CPU cache-timing side channel reconstructing locally-hosted LLM output; clarifies Claude Code is named once in the intro as an example framework and is not itself evaluated or attacked (a hosted-API client, not a local-inference target).
- `docs/sdlc-lcm/fm-bench-analysis.md`: new analysis of FM-Bench (arXiv:2608.18423) — a long-horizon (20 in-game years, ~340-400 decision stops) competitive-multi-agent management benchmark; 15 frontier models compared, ranking uncorrelated with scale/price/vendor.
- `docs/sdlc-lcm/german-wiki-incident-analysis.md`: new analysis of "The Mechanics of a Swarm" (arXiv:2609.12748) — externally reconstructed unintended multi-agent coordination episode on a German-language ProWiki install, including the authors' own §6 self-corrections between v1 and v2.

- `docs/sdlc-lcm/mas-security-framework.md`: extended Layer 2 (Agent Logic) with a new threat row for the "Daydreaming" black-box skill-exfiltration attack (arXiv:2608.26733) — 86.8% skill-capability reconstruction from task outputs alone, showing file-hiding and disclosure-filtering are insufficient by themselves.

- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: added Runtype, a hosted AI product development platform (Flows/Agents/Evals/Records/Tools exposed through chat/REST/Slack/Discord/MCP/A2A Surfaces) with Claude Code onboarding via a hosted MCP server and Enterprise-only self-hosting (BYOC); pricing tiers verified first-party, licence/open-source status of the core platform not stated in first-party docs (checked 2026-09-24).

### Changed

- `.github/workflows/tag-release.yaml`, `.github/workflows/publish-release.yaml`: replaced the hand-rolled steps with thin callers of the estate's reusable `qte77/.github/.github/workflows/tag-release.yml` and `publish-release.yml`, pinned to `613b950b4045cc099ca23f8b7344459c3dc22cb3` (2026-09-22). Triggers unchanged (push-to-main on `pyproject.toml`; `workflow_dispatch` with optional `tag`). `tag-release` overrides `version_regex` for this repo's `current_version = "..."` convention; both callers grant only `contents: write`, which is all the reusable jobs use. `bump-my-version.yaml` is unchanged. Refs #347.

- `lychee.toml`: exact-URL excludes for the pwc.com PDF, the beyondtrust.com glossary page and the producthunt amp page (403 bot-blocks), plus `ampcode.com` (persistent HTTP/2 protocol error to lychee). All four return 200 via polyfetch (2026-09-23).

- `docs/cc-community/CC-community-tooling-landscape.md`, `docs/cc-community/CC-code-tooling-landscape.md`: bumped `updated:`/`validated_links:` to 2026-09-24.

- `docs/cc-community/CC-usage-tooling-landscape.md`: extended with an `agentacct` entry (local-first, cross-agent work-step/cost tracker for Claude Code, Codex, OpenCode, Hermes, and others) alongside CodeBurn, ccusage, Claude-Code-Usage-Monitor, and cc-costline.

- `docs/cc-native/agents-skills/CC-skills-adoption-analysis.md`: extended with six screenshot-lead topics, each verified first-party — the `@skills` path-based, no-install protocol (`SylphAI-Inc/atskills`, arXiv:2608.12610v1, integrated into the AdaL agent harness); the GitSkills dataset (arXiv:2608.10906, 3,797,117 SKILL.md files across 282,200 GitHub repos); `HKUDS/OpenSpace`, a skill management layer scored by task-outcome evidence; SkillZip Pro's execution-aware skill-bundle compression research (arXiv:2608.30785; its linked code repo 404'd, so the entry cites the paper only); the WebDev-Skills-Bench benchmark finding skill injection is frequently net-negative for web-dev coding tasks (arXiv:2608.23067); and a current-stats refresh plus `prompt-audit` skill note for `anthropics/skills`.

- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: bumped `updated:`/`validated_links:` to 2026-09-24.

- `docs/non-cc/agentic-enterprise-os-landscape.md`: frontmatter `purpose`/`platform_scope` updated to list Glean and HugAgentOS; Tier 2 intro softened from "each" to "most" have a dedicated analysis.

- `docs/non-cc/agents-md-cookbook-analysis.md`: added a field-study evidence subsection (Coldtea, 2026-08-21) — 100-repo sample, 27% top-1,000 adoption, median 1,198-word files, 784 "don't" bullets across 86% of sampled repos, 90% must/always/never phrasing — and refreshed repo stats (7→19 stars, last push 2026-07-21→2026-08-08) via GitHub API re-verification.

- `docs/non-cc/kimi-code-analysis.md`: extends Adoption Decision with Anthropic's September 2026 threat-intelligence report (GTG-16002) allegation that Moonshot proxied ~300k Kimi requests to Claude Opus and extracted Claude's chain-of-thought reasoning traces for training; Anthropic says it does not know whether customers were notified. Framed explicitly as Anthropic's own allegation, not an independent finding.
- `docs/non-cc/kv-cache-serving-landscape.md`: adds kvcached (Apache-2.0, OS-style virtual-memory KV manager for elastic multi-LLM GPU sharing) to the Memory management / paging section.
- `docs/non-cc/llm-routers-gateways-landscape.md`: adds Pandora's AI Model Routing Box (arXiv:2608.20316, Google DeepMind) to the Model-Fusion / Ensemble Routing table.

- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md`, `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: bumped `updated:`/`validated_links:` to 2026-09-24.

- `docs/sdlc-lcm/ai-security-governance-analysis.md`: capability laundering via task decomposition (Russinovich et al., arXiv:2609.15383) added to "Agentic AI Attack Surfaces"; BenchShield reward-integrity instrumentation (arXiv:2609.11028) added as a new "Cross-Framework Mapping" subsection; Microsoft's Agent Governance Toolkit and Vercel Labs' deepsec added to "Defensive Tooling". Bumped `updated:`/`validated_links:` to 2026-09-24.
- `docs/sdlc-lcm/evaluation-data-resources-landscape.md`: E-Commerce Bench (QwenLM; long-horizon autonomous business-operation benchmark) and LoopArena (AMAP-ML; models as runtime loop-engineering controllers) added to the §2 Benchmarks catalog. Bumped `updated:`/`validated_links:` to 2026-09-24.
- `docs/sdlc-lcm/mas-benchmarking-best-practices.md`: FUSE (arXiv:2609.17496, verifiable social-reasoning benchmark) added to §3.2 Trust & Validation; Physics of Agents (arXiv:2608.16578, statistical mechanics of collective LLM-agent behavior) added to §4 Multi-Agent Systems. Bumped `updated:`/`validated_links:` to 2026-09-24.

- `docs/sdlc-lcm/agent-code-analysis-landscape.md`: extended §3 (agents-as-scanner) with Specula (`specula-org/Specula`) — agentic TLA+ formal-verification bug finder for concurrent/distributed system code.
- `docs/sdlc-lcm/agent-identity-auth-landscape.md`: extended §1 (authenticate the agent) with SAM (`google/sam`) — zero-trust P2P agent-identity network; noted the "Sovereign Agent Mesh" expansion is unconfirmed against the repo's own README.
- `docs/sdlc-lcm/agentic-sdlc-patterns.md`: extended §3 (Spec-Driven Development) with SpecShip (`aws-samples/sample-specship`) — a "Kiro Power" spec-driven autonomous engineering workflow with adversarial-validation quality gates; added a `## Sources` section.

- `docs/cc-community/README.md`, `docs/cc-native/plugins-ecosystem/README.md`, `docs/cc-native/README.md`, `docs/non-cc/README.md`, `docs/sdlc-lcm/README.md`: indexed the 33 previously un-indexed row-20 docs (4 cc-community, 1 cc-native/plugins-ecosystem, 23 non-cc, 5 sdlc-lcm) plus 3 stray unindexed non-cc docs (`agents-md-cookbook-analysis.md`, `moss-self-evolving-agent-analysis.md`, `on-device-semantic-search-landscape.md`); bumped `cc-native/plugins-ecosystem` doc count 10 → 11.

- `CONTRIBUTING.md` §Cutting a release: notes that `tag-release`/`publish-release` are thin callers of the pinned `qte77/.github` reusable workflows, and that the pin needs a manual refresh (no upstream tags for Dependabot).

### Dropped (screenshot-lead research batch 06, no qualifying first-party source)

- Aibrix (TikTok/Linux Foundation self-hosted inference platform, Anthropic API-compatible) — first-party sources (GitHub repo, docs, quickstart) show an OpenAI-compatible-only gateway with no Anthropic Messages API support, and no Linux Foundation / LF AI & Data affiliation found; the lead's core premise didn't verify.
- Company OS for AI-Native Teams (Claude org-wide skill file deployment) — sole source is a third-party newsletter interview, not a vendor doc, GitHub repo, arXiv page, or official blog.

## [0.8.0] - 2026-09-23

### Added

- `docs/non-cc/agent-frameworks-infrastructure-landscape.md` (§1): expanded the **PydanticAI** entry with its new [capabilities system](https://pydantic.dev/articles/pydantic-ai-capabilities) (Jun 2026) — composable instructions + tools + model-settings bundles with **on-demand / deferred loading** (`defer_loading=True`) for token savings, capability-scoped hooks, and the Pydantic AI Gateway + Logfire companions. First-party source.
- `docs/cc-native/agents-skills/CC-ralph-enhancement-research.md`: new **SantanderAI/ralph** entry under External Pattern Research — Banco Santander AI Lab's multi-CLI Ralph harness (Claude Code / Codex / Gemini / Devin; Apache-2.0, v0.1.0) with live `.ralph/.env` reload, token-exhaustion agent rotation, systemd RAM caps, and project-level distributed skills (`juez` / `maestro`); plus the `ralph-vault-skill` knowledge-vault companion.

- `docs/cc-community/CC-community-tooling-landscape.md`: Google Labs `design.md` — canonical DESIGN.md format spec + `@google/design.md` CLI (lint/diff/export), as the spec behind the awesome-design-md collection.
- `docs/cc-community/CC-code-tooling-landscape.md`: Qodo (qodo-ai) section — `agents` TOML playbooks, `open-aware` deep-code-research MCP server, and cross-repo code-review governance.
- `docs/cc-community/CC-memory-tooling-landscape.md`: "memory should change future behavior" design lens (André Lindenberg) in the Memory Taxonomy section.
- `docs/cc-community/CC-vlm-screen-sharing-landscape.md`: baidu/Unlimited-OCR long-document OCR VLM (edge-of-scope note, deferred to polyfetch-scrape for depth).
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: Tencent Hunyuan UniRL RL post-training framework (thin mention, §5; flagged as training infra, not an agent).
- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: Kaggle/Google "The New SDLC With Vibe Coding" whitepaper (vibe-coding ladder) and `cobusgreyling/loop-engineering` (loop-engineering row).
- `docs/cc-community/CC-vlm-screen-sharing-landscape.md`: opendatalab/MinerU document-extraction tool (alongside Unlimited-OCR; MCP server for Claude Desktop/Cursor), deferred to polyfetch-scrape.
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: Warp agentic development environment (+ Oz cloud-agent orchestration) and the Vstorm PydanticAI full-stack starter template.
- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: "factory engineers, not product engineers" framing (Zach Lloyd/Warp) and the Talking AI podcast perspective.
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: LuxTTS TTS voice-cloning model (§6 specialist-models-agents-call-as-tools, flagged not-an-agent).
- `docs/cc-community/CC-code-tooling-landscape.md`: AI PR-review agents roundup (CodeRabbit, Greptile, Ellipsis, Sourcery, Qodo Merge/PR-Agent, Graphite Diamond, Cursor Bugbot, Cubic, Bito, Korbit).
- `docs/cc-community/CC-community-tooling-landscape.md`: related design source + token standard (Figma Dev Mode MCP, W3C Design Tokens/DTCG, Style Dictionary).

- `docs/non-cc/web-scraping-extraction-landscape.md`: Scrape.do (managed scraping platform — 110M+ proxies, HTML/JSON/XML/MD output, low-cost).

- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: Pydantic's *The Harness Thesis* + *What Makes a Good Harness* (disclosure / steering axioms) as harness-engineering first-party anchors, and the *Applied GenAI Maturity Model* as an org-adoption governance lens.
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: the `pydantic-ai-harness` capability library (CodeMode / filesystem / shell / provider-adaptive web search; MIT, 595★) in the PydanticAI entry, and EverOS (Markdown-native, local-first memory layer; Apache-2.0, 9.4K★) in §4 Agent Memory.

- `docs/non-cc/hermes-agent-analysis.md`: SimpleX as a Hermes messaging channel (privacy-preserving, no user identifiers; AGPLv3), with a dated note that the channel roster expanded to 27+ platforms at Hermes v0.17.0; integrations-index + SimpleX Chat sources.

- `docs/cc-native/agents-skills/CC-output-verification-analysis.md`: a first-party guide to verifying Claude Code's own agentic outputs — per-mechanism matrix (workflow / team / subagent / plan / memory), hooks as the deterministic backbone (with the non-uniform `exit 2` semantics), `--json-schema` structured-output validation + the `error_max_structured_output_retries` fail signal, the CLAUDE.md-as-user-message memory gotcha, and the DIY (no first-party eval runner) pattern. Closes #320.

- Backfilled a `## Sources` section into the 9 convention-named docs that had neither heading: `CC-code-tooling-landscape`, `CC-usage-tooling-landscape`, `agent-frameworks-infrastructure-landscape`, `agent-observability-methods-analysis`, `deerflow-analysis`, `opensrc-analysis`, `agent-evaluation-metrics-landscape`, `evaluation-data-resources-landscape`, `oss-alm-landscape`. Closes #308.

- `docs/non-cc/spec-driven-frameworks-landscape.md`: standalone SDD-framework comparison (spec-kit 115.9K / OpenSpec 57.1K / BMAD 49.8K / Agent-OS / Kiro / Tessl; gh-verified stars) — the deep-dive promoted from the §3 stub in the agentic-engineering disciplines landscape. Part of #321.
- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: added Anthropic's first-party "Effective Context Engineering for AI Agents" (Sept 2025) canonical anchor to the ACE-FCA section (write/select/compress/isolate). Part of #321.

- `docs/non-cc/workflow-frameworks-landscape.md`: agentic workflow framework landscape — Anthropic's 5 "Building Effective Agents" patterns (workflows-vs-agents), a control-flow/durability framework table (gh-verified stars), the durable-execution layer (Temporal / Inngest / Restate, with `(workflow_id, step_id)` idempotency), and an 8-item S0–S2 anti-pattern taxonomy + best-practices checklist. Cross-refs the CC Workflow tool and the agent-frameworks catalog rather than duplicating them. Closes #319.

- `docs/cc-community/CC-community-plugins-landscape.md`: **squid** plugin profile — iusztinpaul's Claude Code agentic-engineering pipeline (5 role subagents Product Architect → SWE → Tester → PR Reviewer → On-Call; ADRs as architectural memory + Tasks Plan as task decomposition; `/scaffold` `/plan` `/implement-night` `/implement-task` `/review` slash commands; env vars: none documented).
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md` (§1): **multica** (multica-ai) — source-available (modified Apache 2.0) multi-agent orchestration platform routing issues to agents/squads across 13 agent CLIs; local daemon + autopilot scheduling, Go + Postgres/pgvector; `multica login` / `daemon start` / `issue create` (browser auth, no env vars).
- `docs/non-cc/web-scraping-extraction-landscape.md` (Document-Specific Extraction): **olmOCR** (AllenAI) — GPU PDF/image → Markdown/Dolma OCR pipeline on a fine-tuned Qwen2.5-VL 7B; document-ingestion front-end for RAG/knowledge bases; install/CLI/flags captured leanly with upstream link (default model `allenai/olmOCR-2-7B-1025-FP8`).
- `docs/non-cc/goose-analysis.md`: new **Install, CLI & Configuration** section — `goose session` / `configure` / `update`, install one-liners, and provider/runtime env vars (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`, `GOOSE_VERSION`, `CONFIGURE`); `validated_links` refreshed for the aaif-goose migration.
- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: cited **Lenny's Newsletter (AI)** as a practitioner-perspective source on agentic adoption.

- `docs/sdlc-lcm/goal-tracking-attribution-landscape.md`: NEW landscape — the top-down goal→spec→build→learning attribution loop, with the qte77 estate as the worked reference (`qte77/qte77` `goals.json` OKR schema + `cto-handbook-mapping.md`; `liminal-flux-gh-acc` per-run `performance-log.jsonl` tracing + cost gates; `research-ralphy` research→PRD attribution; ralph-loop `prd.json` story tracking) and the commercial OKR/PM baseline (Jira Align, WorkBoard/Quantive, Tability, Productboard, LinearB) it diverges from — none agent-native despite the 2026 MCP-access layer. Status: Assess.

- `docs/non-cc/agentic-enterprise-os-landscape.md`: NEW landscape — the "agentic enterprise OS" pattern across three tiers: enterprise vendor platforms (Salesforce Agentforce 360, Microsoft Copilot Studio + Agent 365, ServiceNow Otto, SAP Joule Studio, Databricks Genie), open-source self-operating workspaces/runtimes (AutoAgent, Odysseus, Goose, multica), and qte77 estate orchestrators (polyforge, office-forge, liminal-flux-gh-acc). Framed honestly against Gartner's "AI agent development platforms" category (not a real "agent OS" category); documents the agent-native goal-attribution gap — none of the enterprise platforms exposes a machine-writable goal schema or per-run cost+outcome attribution, and none has adopted AG-UI. Status: Assess.

- `docs/non-cc/agent-frameworks-infrastructure-landscape.md` (§4): **estate file-based compound-learning memory** bullet — plain-Markdown `CLAUDE.md`/`AGENT_LEARNINGS.md`/`LEARNINGS.md` as durable git-versioned agent memory with an explicit promotion path, distilled cross-repo by `learnings-ralphy`; the filesystem-as-memory complement to the graph/vector memory engines.
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md` (§7): new **Graph visualization** subsection — vis-network, D3.js, Cytoscape.js, Sigma.js, Gephi, PyGraphistry/Graphistry, Neo4j Bloom/Browser (licenses verified first-party; this repo's `ui/graph.html` is the vis-network worked example).
- `docs/non-cc/semantic-layers-data-catalog-landscape.md`: new **Formal Ontologies & Semantic Web** section — RDF/OWL/SKOS/SPARQL/SHACL, open- vs closed-world, and the connect/exclude/enhance framing vs LLM-embedded KGs.

- `.github/workflows/link-rot-monitor.yaml` + a `make check_links_report` target: a weekly scheduled lychee link-check that opens/updates a single `link-rot` tracking issue on broken links and auto-closes it when links are healthy again — catches external link rot proactively (between docs PRs) instead of ambushing the next one. Keeps the custom `lint.yaml` PR gate (per the #141 decision) and reuses the same `lychee.toml`, so excludes/accepts stay single-sourced. Sets `GITHUB_TOKEN` on the lychee step to cut github.com rate-limit false negatives.

- `docs/plans/2026-07-05-status-frontmatter-migration.md` + `docs/handoffs/2026-07-05-status-frontmatter-migration.md`: durable plan + onboarding handoff for #348 (migrate doc `status` into YAML frontmatter, drop the body badge), with a complete source map (grep commands, counts, file:line lists, vocabulary, transform rule) so a future session executes without re-mapping. Migration itself is deferred (YAGNI — nothing reads `status:` yet). Introduces `docs/handoffs/` for cross-session handoff notes.

- `docs/sdlc-lcm/agentic-ai-vulnerability-landscape.md`: new landscape covering the operational agentic-AI vulnerability layer — OWASP AIVSS scoring, MITRE ATLAS (machine-readable threat KB + AI Incident Sharing), vendor discovery/remediation systems (Microsoft MDASH, Vuln.AI), the Berkeley Vulnerability Initiative tracker, and two arXiv attack/defense surveys. Sectioned by epistemic role; cross-linked with `mas-security-framework.md` and `ai-security-governance-analysis.md` (extends, does not duplicate, their MAESTRO/ATLAS/NIST material).

- `docs/non-cc/kv-cache-serving-landscape.md`: new landscape on KV-cache serving — a cross-vendor prompt-caching comparison (Anthropic/OpenAI/Gemini: minimums, TTL, pricing) plus open serving-stack internals (PagedAttention/vLLM, SGLang RadixAttention, FP8/KIVI quantization, H2O/StreamingLLM eviction, GQA/MLA architectural sharing, Mooncake/LMCache offload-disaggregation) with a 2026 state-of-the-art synthesis.

- `docs/cc-community/CC-codex-plugin-cc-analysis.md`: analysis of OpenAI's official Codex→CC plugin (Apache-2.0) — slash commands, `codex-rescue` subagent, `Stop`-hook review gate, background delegation, session transfer; a rival lab building on CC's own extension surface.
- `docs/plans/2026-07-08-new-sources-batch.md`: durable plan record for the new-sources batch (tracker #374).

- `docs/non-cc/agents-cli-analysis.md`: Google agents-cli — a skill-pack that upskills a coding agent (Claude Code, Antigravity, Codex) to build/evaluate/deploy ADK agents on the Gemini Enterprise Platform (Apache-2.0; v1.0.0 but Pre-GA). Cross-ref'd from the CC-community skills landscape (it installs as a CC skill-pack).
- `docs/non-cc/agentic-payments-landscape.md`: new landscape on machine-native agent payment rails — x402 (Coinbase → Linux Foundation; HTTP 402; USDC/Base), Google AP2 (Mandates = W3C Verifiable Credentials), Stripe MPP, Fetch.ai — with the Apify x402 case study.
- `docs/non-cc/karpathy-agentic-coding-analysis.md`: primary-source map of Andrej Karpathy's agentic-coding arc (LLM OS → vibe coding → Software 3.0 / autonomy slider → agentic engineering).
- `docs/sdlc-lcm/agent-identity-auth-landscape.md`: new landscape on agent identity / authentication / personhood — SPIFFE, Microsoft Entra Agent ID, MCP-OAuth, Okta Cross-App Access, AP2 Mandates, World ID / Humanity Protocol, Cloudflare Web Bot Auth — organized by the authenticate-the-agent / authorize-on-behalf-of-human / personhood axes, plus one-time/JIT permissions. Joins the sdlc-lcm security cluster.

- `docs/plans/2026-07-08-graphify-rebuild-354.md` + `docs/handoffs/2026-07-08-graphify-rebuild-354.md`: execution-ready plan + next-session handoff for the deferred #354 graph rebuild, with a full command/file/source map (graphify runtime, the `--update` flow, `make graph-page` → `ui/graph.html`, gh-pages deploy) so a fresh session runs it without re-gathering context.

- `AGENT_LEARNINGS.md`: two learnings — reconcile git HEAD/issue state vs the conversation summary before executing tracked work in a continued session; and never partial-update a uniformly-built graphify graph (density lopsiding + `build_merge` source_file matching).

- `.claude/skills/adding-research-source/`: a repo-native Claude Code skill (agentskills.io-conformant) codifying this corpus's source-onboarding workflow — first-party research → placement decision tree (cc-native / cc-community / non-cc / sdlc-lcm) → doc conventions → lint → one-PR-per-topic — with an Explore research-subagent brief and a `scripts/batch-sources.workflow.js` batch workflow (parallel research + adversarial verify) for large source drops. `.gitignore` un-ignores this specific skill; other `.claude/skills/` remain plugin-deployed.

- `docs/non-cc/web-scraping-extraction-landscape.md` (Browser Automation): new **Accessibility-tree page representation** subsection — the a11y tree as a third page-representation for LLMs, between raw DOM/HTML and vision/screenshots; ~80–90 % smaller than the DOM and redesign-stable, but an assistive-tech-shaped subset. Includes the Playwright 1.57 `page.accessibility.snapshot()` removal → `aria_snapshot` migration and the Patchright 1.58.2 version gate (`page.locator("body").aria_snapshot()`; no `Page.aria_snapshot` shortcut, no `mode="ai"`).
- `docs/cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md` (Alternative MCP Options): upgraded the agent-browser tools table with first-party license/language and a **representation** column (accessibility tree vs custom DOM vs pixel), added the previously-absent **Stagehand** (Browserbase, MIT), and a counterexample note for the pixel/screenshot-based agents (Anthropic Computer Use, OpenAI Operator). Licenses verified first-party via GitHub repo metadata (2026-07-10).

- `.github/scripts/lib/doc_status.py` + `.github/scripts/check-doc-status.py`: a stdlib doc-status validator (#348 consumer). Lenient mode (wired into `make lint` via `make check_status`, and a new `status` CI job) checks that any frontmatter `status:` token is in the controlled vocabulary; `--strict` additionally forbids residual body `**Status**:` badges (the doc-level badge in the preamble — an in-section `**Status**:` line describing an upstream project is left alone). Unit tests in `tests/test_doc_status.py`.
- `.github/workflows/lint.yaml`: added a `tests` job (`make test`) so unit tests gate PRs, and a `status` job (`make check_status`); extended the path triggers to `.github/scripts/**`, `scripts/**`, and `tests/**`.

- `docs/cc-community/CC-multi-account-switching-landscape.md`: multi-account/profile switching for CC — native `CLAUDE_CONFIG_DIR` mechanism (first-party-verified: documented only in the debug-your-config guide; per-platform credential isolation — Linux/Windows per-dir, macOS Keychain carries over), tool table (claude-swap, claude-code-profiles, claude-multiprofile, claude-multisession), disambiguation vs CC Switch (provider mgmt) and CLIProxyAPI (gateway quota harvesting).
- `docs/plans/2026-07-23-corpus-update-new-sources.md`: durable plan for the 2026-07-23 corpus-update + new-sources arc (backlog drain #374, fresh mining, stale-fact refresh cohort).

- `docs/sdlc-lcm/agent-silent-failure-taxonomy-analysis.md`: arXiv:2606.14589 — longitudinal five-class taxonomy of silent failures from 22 production incident postmortems (CC BY 4.0; artifact repo + PyPI governance engine first-party per the paper's Comments field).
- `docs/sdlc-lcm/sovereign-execution-brokers-analysis.md`: arXiv:2606.20520 — brokered agent-execution control plane.
- `docs/sdlc-lcm/ledger-state-tool-calling-analysis.md`: arXiv:2606.20529 — LedgerAgent ledger-state tool-calling.
- `docs/sdlc-lcm/agent-probabilistic-verification-analysis.md`: arXiv:2606.20510 — efficient and sound probabilistic verification of agent behavior.

- `docs/non-cc/moss-self-evolving-agent-analysis.md`: MOSS (arXiv:2605.22794) — self-evolution via source-level rewriting; CC is one of four pluggable coding-agent providers.
- `docs/non-cc/agents-md-cookbook-analysis.md`: tool-agnostic AGENTS.md template kit (Taiizor, MIT).
- `docs/cc-native/context-memory/CC-repo-guidance-probe-refine-analysis.md`: Probe-and-Refine tuning of repo guidance files for coding agents (arXiv:2606.20512).
- `docs/cc-native/model-internals/CC-code-correctness-hidden-states-analysis.md`: third-party probing research — code correctness linearly decodable pre-generation (arXiv:2606.14530); directory scope widened to include selected third-party interpretability work.

- `docs/non-cc/on-device-semantic-search-landscape.md`: promoted tracker #383's completed research to a durable doc — ternlight (Hold: WASM-only, brute-force O(n), 128-token cap) vs the decoupled Python-native stack (Assess: fastembed/sentence-transformers/model2vec × FAISS/usearch/LanceDB/Chroma/…), sqlite-vec brute-force-only gotcha, multimodal text-first guidance, recommended stack.

- `.claude/workflows/refresh-docs.js`: generalized, args-driven stale-fact refresh workflow (read-only checker per doc + adversarial verifier per correction set); documented in `docs/architecture.md` §Automated Monitors.

- `scripts/cc-multi-account.sh`: helper for running N Claude Code accounts concurrently in one OS via per-account `CLAUDE_CONFIG_DIR` (`ccp`/`ccu`/`ccl` functions + a documented zero-install alias alternative); companion to `docs/cc-community/CC-multi-account-switching-landscape.md`, with per-account usage stats via `ccusage`.

- `docs/sdlc-lcm/agent-code-analysis-landscape.md`: new landscape on static (SCA) and dynamic (DCA) code analysis for AI coding agents — both directions (analysis OF agent code; agents AS scanner). Covers garak (verified probe families), Semgrep Guardian (launch 2026-06-23; unconfirmable rule counts omitted), CodeQL/Bandit/Trivy/agent-audit, AgentSight (eBPF) + VIPER-MCP (hybrid, 106 zero-days/67 CVEs), the agents-as-scanner blueprint (Google Cloud 2026-07-16, −7-day TTE) + VulnAgent-R2/VulnLLM-R, a verified GitHub·GitLab·Codeberg-Forgejo CI matrix (Codeberg confirmed thin), sandboxing-as-analysis-boundary (CC's "no traffic inspection" gap), and the OWASP Top 10 for Agentic Applications 2026 (distinct from MAESTRO/LLM Top 10). Cross-refs the existing vulnerability/governance/MAESTRO docs rather than duplicating.

- `scripts/cc-multi-account.sh`: direct-execution dispatch — `./cc-multi-account.sh <profile>` launches, `list`/`ls` lists profiles, `usage <profile>` shows per-account stats, and `-h`/`--help`/no-args print the usage header (unknown options exit 2 with help on stderr). Sourcing is unchanged and still defines `ccp`/`ccu`/`ccl`; the header now documents both modes and why sourcing is required for the short commands.

- `scripts/cc-multi-account.sh`: `ccsync <profile>` / `ccsync --all` (and `./cc-multi-account.sh sync <profile>`) re-applies the shared `~/.claude/settings.json` to per-account profiles, keeping per-profile UI keys (`CC_PROFILE_KEEP`), backing up to `settings.json.bak`, reporting dropped keys, and never touching `.credentials.json`.

- `docs/plans/2026-09-23-0008-backlog-triage-prs-issues.md`: read-only triage of all open PRs, branches and issues (29 PRs, 10 issues) with a single remaining-work table (gate + done-when per row).
- `docs/plans/2026-06-11-0001-plugin-rules-codeburn-merge.md`: the untracked 2026-06-11 plugin-rules/CodeBurn handoff promoted to a plan, with a 2026-09-23 status check (not shipped yet).

- `docs/cc-community/CC-multi-account-switching-landscape.md`: "Repo Helper" section for `scripts/cc-multi-account.sh` — executed and sourced commands (incl. `sync` / `ccsync`), the `CC_PROFILE_HOME`, `CC_BASE_SETTINGS` and `CC_PROFILE_KEEP` env vars with defaults, and the settings-drift and `700`-permission behaviour.

### Changed

- `docs/cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md`: cite the companion code repo [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code) for the arXiv 2604.14228 design-space analysis.
- `docs/cc-community/CC-vlm-screen-sharing-landscape.md`: refresh the **PixelRAG** entry (~3.3k★ → ~4.2k★, v0.3.0).
- `docs/cc-community/CC-research-agents-landscape.md`: turn the bare `/deep-research` mention in the local-deep-research entry into an actual cross-ref to the bundled-workflow section (reuses the existing anchor).
- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: cite the Startup CTO Handbook as the traditional engineering-leadership baseline the agentic disciplines diverge from (Cross-References + Sources), linking the qte77 estate mapping note.

- `docs/cc-community/CC-code-tooling-landscape.md` → `docs/non-cc/code-review-products-landscape.md`: moved the standalone SaaS PR-review roundup (CodeRabbit, Greptile, Ellipsis, Sourcery, Qodo Merge/PR-Agent, Graphite Diamond, Cursor Bugbot, Cubic, Bito, Korbit) to a non-CC landscape — they are multi-platform products, not CC integrations. Qodo (`open-aware` MCP + cross-repo review) and Code-Review-Graph stay in the cc-community doc. Closes #326.

- `docs/cc-community/CC-community-tooling-landscape.md` → `docs/non-cc/agent-design-formats-landscape.md`: moved the agent-consumable design-format cluster (awesome-design-md corpus, Google Labs DESIGN.md spec + CLI, and the Figma Dev Mode MCP / W3C token chain) to a non-CC landscape — they are multi-agent formats, not CC integrations. Refreshed stale figures (awesome-design-md 21.8K→93.8K stars; design.md license open→Apache-2.0, 22.1K stars). Claude Code's Figma surface stays cross-referenced via the first-party Figma MCP plugin. Part of #329.

- Relocated mislabeled docs out of `docs/cc-community/` (classification hygiene, #329): the 6-doc MAS/methodology cluster (`mas-design-principles`, `mas-benchmarking-best-practices`, `mas-security-framework`, `ai-security-governance-analysis`, `agent-evaluation-metrics-landscape`, `evaluation-data-resources-landscape`) → `docs/sdlc-lcm/`; `research-agents-landscape` + `repo-to-docs-tools-landscape` → `docs/non-cc/`; `agent-observability-methods-analysis` → `docs/non-cc/` with Claude Code's first-party OTel telemetry extracted to a new `docs/cc-native/configuration/CC-monitoring-telemetry-analysis.md`. All de-`CC-`prefixed; cross-references and directory READMEs updated.

- `docs/cc-community/CC-community-tooling-landscape.md` → new `docs/non-cc/openharness-analysis.md` + `docs/non-cc/opensrc-analysis.md`: moved OpenHarness (HKUDS open Python agent harness) and opensrc (Vercel Labs npm-source fetcher) out of the CC tooling landscape into standalone non-cc analyses — both are agent-agnostic tools, not CC integrations. Refreshed stale stars (OpenHarness 3.3K→14.2K; opensrc 1.5K→2.6K). Comparison table 21→19 tools; READMEs + autoagent cross-ref updated. Layer-5 compression libs and CL4R1T4S intentionally kept in place. Closes #329.

- `CONTRIBUTING.md`: a `## References` section is now accepted as equivalent to `## Sources` (the convention allows either heading).

- `docs/sdlc-lcm/goal-tracking-attribution-landscape.md`: added a **substrate-thread** synthesis (file/graph/vector memory → KG/GraphRAG/visualization → ontology/semantic-layer → goal graph → enterprise-OS) and a bidirectional cross-ref to the new enterprise-OS landscape; corrected liminal-flux to "six action roles across an 8-phase progression".
- Pass 2 connections wiring: `multi-agent-onboarding-outlook.md` and `agent-frameworks-infrastructure-landscape.md` now cross-ref `ag-ui-protocol-landscape.md` (the MCP / A2A / AG-UI protocol triangle); `codex-cli-analysis.md` and `gemini-cli-analysis.md` now cross-ref the `AGENTS.md`/`GEMINI.md` convergence in `multi-agent-onboarding-outlook.md`; `CC-community-tooling-landscape.md` cross-refs Superpowers from the everything-claude-code entry.

- `Makefile`: hoisted the markdown-lint file list into a single `DOC_LINT_GLOB` variable shared by `check_docs` + `autofix`, and widened it to also lint the root governance docs (`CLAUDE.md`, `AGENTS.md`, `AGENT_LEARNINGS.md`, `AGENT_REQUESTS.md`).
- `docs/architecture.md`: updated the lint-scope row to match the widened glob, and documented the `uv tool install graphifyy` key-free graphify install path (previously only the side-loaded `GRAPHIFY=` path was noted).
- `README.md`: added an inbound link to `docs/UserStory.md` (a current requirements doc that was previously unlinked/undiscoverable).

- `docs/non-cc/fastcontext-analysis.md`: flagged **under review** (#362) — Microsoft's upstream `microsoft/fastcontext` repo was removed (GitHub 404); `source:` + `[repo]` repointed to the arXiv paper and a live community fork; the HuggingFace model URL (401 auth-wall on a live page) is excluded in `lychee.toml` pending re-verification.

- `Makefile`: `lint` now runs `check_docs` + `check_actions` before the network-dependent `check_links`, so a transient lychee failure can no longer mask markdownlint/actionlint locally (root cause of a markdownlint error reaching CI in #366).
- `docs/architecture.md`: corrected the automated-monitor count (three → four), added root `scripts/`/`tests/`/`ui/`/`changelog.d/` to the directory tree, and documented `link-rot-monitor` as a fifth (health, not content) scheduled workflow.

- `lychee.toml`: exclude `ai-incidents.mitre.org` (upstream untrusted SSL cert chain — browser-OK, fails automated verification), cited in the new agentic-AI vulnerability landscape.

- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: corrected the stale model-dependent minimum cacheable-prefix tiers (Opus 4.8 is **1,024** tokens, not 4,096; added Sonnet 5, Haiku 4.5, Opus 4.7, Fable 5/Mythos 5 — verified against the Anthropic caching docs, 2026-07-08); added a Related section cross-linking the new KV-cache serving landscape and the KV-invalidation gotcha in `CC-model-provider-configuration.md`.

- `docs/non-cc/repo-to-docs-tools-landscape.md`: added OpenWiki (LangChain, MIT) — an agent-oriented repo→docs generator that appends pointers into `AGENTS.md`/`CLAUDE.md`, distinct from human-facing DeepWiki-style tools.
- `docs/non-cc/agentic-enterprise-os-landscape.md`: added a "company brain" subsection (a synthesis label over agent-memory + KG/ontology + permissioning + write-back; cross-linked to the memory/semantic-layer docs, not a standalone doc).
- `CONTRIBUTING.md`: Research Workflow now points to `polyfetch-scrape` (fetch dynamic/blocked pages) and `doc-pipeline-engine` (process PDF/Office → text) via `uv run --directory`, alongside the existing `rtk` pointer.

- `docs/plans/2026-07-08-graphify-rebuild-354.md` + its handoffs: marked `done` (the rebuild was executed by PR #379 — 637 nodes, #354 closed) so they no longer read as pending work; steps retained as method reference.

- `ui/graph.html`: rebuilt the published knowledge graph for #354 via key-free `/graphify --update`, incorporating waves 1+2 (agentic-AI security/vulnerability, KV-cache serving, agentic payments, agent identity/auth, Karpathy, Codex-CC/OpenWiki/company-brain tooling). 28 changed `docs/` files re-extracted (semantic subagents, docs-only scope), merged into the 427-node baseline → ~635 published nodes / 752 edges across 105 communities (21 curated legend labels). Finer per-chunk extraction yielded a denser graph than the prior 583, not sparser.

- `docs/cc-native/configuration/CC-env-vars-reference.md`: added `CLAUDE_CONFIG_DIR` (verified zero-coverage gap; noted its absence from the official env-vars list as of 2026-07-23) + cross-ref to the new landscape.
- `docs/cc-native/configuration/CC-model-provider-configuration.md`: CLIProxyAPI entry now disambiguates gateway-level multi-account from native CLI multi-account sessions.
- `.claude/skills/adding-research-source/scripts/batch-sources.workflow.js`: tolerate args delivered as a JSON-encoded string (harness stringification made the workflow no-op).

- `docs/cc-community/CC-community-tooling-landscape.md`: added Parry Guard (CC-hook injection/secrets/exfil scanner, local DeBERTa + AST layers; Codex support unreleased-main-only per its own release notes), Dippy (PreToolUse bash auto-approval with steerable deny messages, vendored zero-dep parser), and cc-sessions (DAIC session/workflow enforcement, 1,550★ but dormant since 2025-10) — sections + comparison rows + sources; all facts first-party verified with adversarial re-check (counts/license/version).
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: added sudocode to §1 (git-native spec/issue-graph orchestrator running CC/Codex/Cursor via ACP, Apache-2.0) alongside the comparable multica entry.
- `docs/non-cc/spec-driven-frameworks-landscape.md`: added AB Method (fractal roadmap→tasks→missions TDD workflow, dual-runtime CC+Codex with runtime-adaptive subagent nesting, v3.7.1) — table row, differ-bullet, sources.

- `docs/sdlc-lcm/evaluation-data-resources-landscape.md`: added Every Eval Ever (arXiv:2606.14516).
- `docs/sdlc-lcm/mas-benchmarking-best-practices.md`: added Contagion Networks (arXiv:2606.20493) + Multi-LCB (arXiv:2606.20517, beside the existing LiveCodeBench mention).
- `docs/sdlc-lcm/agentic-ai-vulnerability-landscape.md`: added Defensive Misdirection (arXiv:2606.20470) + guardrail-DoS (arXiv:2606.14517; corrected count — 1 surrogate + 8 transfer targets).
- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md`: added StreamMemBench (arXiv:2606.14571) + SIMMER (arXiv:2606.14574).
- `docs/sdlc-lcm/README.md`: four new index rows.

- `docs/non-cc/research-agents-landscape.md`: added the Perplexity Computer knowledge-work study (arXiv:2606.07489; fabricated "8,357 users" stat corrected to the paper's actual methodology).
- `docs/non-cc/kv-cache-serving-landscape.md`: added UltraQuant 4-bit KV caching (arXiv:2606.20474) + Execution-State Capsules/FlashRT checkpoint-restore (arXiv:2606.20537).
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: added MemoryWAM (arXiv:2606.20562) + MAA (arXiv:2606.20475) to §4, H-RePlan (arXiv:2606.20487) to Production Patterns.
- `docs/cc-community/CC-memory-tooling-landscape.md`: added roampal-core (outcome-based memory MCP server, Apache-2.0).
- `docs/cc-community/CC-usage-tooling-landscape.md`: added cc-costline (7d/30d spend statusline; NO license file — all-rights-reserved by default).
- Index updates: `cc-native/README.md` counts (context-memory 5, model-internals 3), both subdir READMEs, `cc-community/README.md` coverage rows.

- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: corrected a misattribution — the *write/select/compress/isolate* taxonomy is LangChain's, not Anthropic's (the Sept-2025 Anthropic post never uses it); now maps ACE-FCA to Anthropic's actual long-horizon techniques (compaction, sub-agent architectures, structured note-taking → AGENT_LEARNINGS.md + auto-memory).
- `docs/cc-native/configuration/CC-monitoring-telemetry-analysis.md`: five verified additions (live docs 2026-07-23, versions unpinned) — `CLAUDE_CODE_PROPAGATE_TRACEPARENT` outbound proxy propagation; new Log Events section (`api_refusal`, `permission_mode_changed` + event inventory); new Attribution Chain section (redacted `agent.name`/`skill.name`/`plugin.name`/`marketplace.name`/`mcp_server.name`/`mcp_tool.name` namespace vs plain tool-span attrs); two-tier beta tracing gates (`ENABLE_BETA_TRACING_DETAILED` + endpoint + interactive-CLI org allowlist).
- `docs/sdlc-lcm/evaluation-data-resources-landscape.md`: new "EDD as Methodology" lead section — Anthropic Demystifying-evals (2026-01-09), OpenAI eval-driven guidance, Braintrust/DeepEval term anchors, Husain counterweight; provenance hedged, cross-refs the disciplines landscape.
- `docs/cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md`: fixed a false internal cross-ref (claimed the skills doc documents "harness engineering (Viv Trivedy)" — zero occurrences there); now points at the disciplines landscape §1 ladder (AlphaCodium Flow Engineering 19%→44% pass@5, OpenAI Harness Engineering Feb 2026) + new cross-ref table row.

Closes #321 (tasks 2–5; task 1 shipped 2026-06-27 via the spec-driven landscape).

- Stale-fact refresh of the 27-doc `validated_links: 2026-03-*` cohort (first `refresh-docs` run, ~50 agents): ~110 adversarially-verified corrections applied across 24 docs (3 clean) — version gates, feature renames, count/roster drift, dead-URL replacements — spanning cc-community (2), agents-skills (1), ci-remote (6), configuration (3), plugins-ecosystem (7), sandboxing (3), sessions (2), non-cc (1); all touched docs bumped to `updated`/`validated_links: 2026-07-23`.
- `lychee.toml`: exact-URL exclude for the bot-blocking (403) Salesforce MCP-GA blog cite (page verified live via WebFetch 2026-07-23; owner-approved).

- `ui/graph.html`: full uniform knowledge-graph rebuild after the 2026-07-23 arc — **785 nodes / 865 edges / 92 communities** (was 637 nodes), built from the integrated arc content (13 new docs, ~30 extended, 24 refreshed); 120 unchanged files replayed from the extraction cache (uniform density preserved), 95 new/changed files re-extracted via 12 cap-safe subagent chunks.

- `docs/plans/2026-07-23-corpus-update-new-sources.md`: arc closed — `status: done`, all phase items ticked, and an Outcome section recording the 12 merged PRs, delivered totals (15 new docs, ~30 extends, 24 refreshed, 637→785-node graph), and reusable merge-mechanics learnings (stacked PRs auto-close on base deletion; octopus branches can't be replayed after squash; CodeFactor re-reports after every `update-branch`).

- `docs/plans/`: files renamed to `YYYY-MM-DD-NNNN-<slug>.md` (0001–0008, creation order); convention and index updated in `docs/plans/README.md`, inbound links repointed (`AGENT_LEARNINGS.md`, `.github/scripts/lib/doc_status.py`).

- `CONTRIBUTING.md`, `docs/architecture.md`: directory trees now list `cc-multi-account.sh` under `scripts/`.

### Removed

- `docs/handoffs/`: the three handoffs were merged into their plans (0003 status migration, 0005 source expansion, 0006 graphify rebuild) — plans now carry their own onboarding. Dropped the `.claude/handoffs/` `.gitignore` entry.

### Fixed

- Landscape docs: corrected `updated`/`validated_links` to 2026-06-26 (stamped a day early in #325) and cross-linked the AI PR-review "to be repositioned" marker to #326.

- `docs/cc-community/CC-vlm-screen-sharing-landscape.md`: repoint the Unlimited-OCR / MinerU document-extraction cross-refs from `polyfetch-scrape` to the in-repo scraping/extraction single-source-of-truth (`web-scraping-extraction-landscape.md`).

- Stamped `updated`/`validated_links` → 2026-06-27 on the 9 docs relocated by #329 (the 6 MAS docs now in `sdlc-lcm/`, plus `research-agents-landscape`, `repo-to-docs-tools-landscape`, and `agent-observability-methods-analysis` in `non-cc/`) — they were edited and lychee-re-validated on the 27th.

- `docs/non-cc/github-copilot-cli-analysis.md`: repoint the misdirected "AGENTS.md convergence" cross-reference from `CC-skills-adoption-analysis.md` (which has no AGENTS.md content) to `multi-agent-onboarding-outlook.md`, and fold the note into the existing Cross-References entry (removing the redundant duplicate). (#355)

- `CONTRIBUTING.md`: corrected the Directory Structure tree to match reality — added `docs/archive/`, `docs/learnings/`, `docs/cc-native/model-internals/`, root `changelog.d/`, `scripts/`, `ui/`, and `.github/state/`; removed the retired `docs/todo/`. Fixed 3 stale `docs/todo/` prose references to `docs/archive/` (including the incorrect "`docs/todo/` is in `lychee.toml` `exclude_path`" claim — it is `docs/archive/`).

- Link rot (surfaced by #361 lychee, blocking all PRs on `main`): repointed the moved OpenRouter Claude Code integration URL (`/docs/guides/`→`/docs/cookbook/`) in `docs/cc-native/configuration/CC-model-provider-configuration.md`.

- `docs/cc-community/CC-vlm-screen-sharing-landscape.md`: resolved a frontmatter↔badge contradiction (`status: research` but badge `Assess`) — aligned the badge to `Research (informational)`, matching the frontmatter and sibling landscape docs.

- `docs/non-cc/cocoindex-analysis.md`: removed a duplicate `**Status**` line inside the Adoption Decision section.
- `docs/non-cc/fastcontext-analysis.md`: finalized the #362 note — analysis kept (arXiv paper is authoritative; upstream Microsoft repo removed).

- `docs/cc-native/CC-first-party-docs-index.md`: "Building effective agents" URL 404'd (`platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/building-effective-agents` — page moved) → repointed to the canonical `https://www.anthropic.com/engineering/building-effective-agents`.
- `docs/non-cc/amp-analysis.md`: `[amp-pricing]` 404'd (`ampcode.com/pricing` removed) → repointed to `https://ampcode.com/manual`, which now carries the credit/pricing model. These two dead links were failing the repo-wide lychee check on every PR.

- `.github/workflows/rxiv-paper-eval.yaml`: bump `eval_ref` v0.2.2 → v0.4.0, in lockstep with the reusable-workflow pin — the v0.4.0 workflow unconditionally passes `--max-llm-calls`, which the v0.2.2 script rejects (exit 2), leaving the PR-path eval permanently red (bit #390). Upstream skew-guard tracked in qte77/gha-rxiv-paper-eval#80; GitHub Models retirement (2026-07-30) migration tracked in qte77/gha-rxiv-paper-eval#81.

- `docs/non-cc/agent-observability-methods-analysis.md`: removed dead o-mega.ai listicle source (404, article unrecoverable).

- `docs/non-cc/kiro-analysis.md`: de-linked the usage.ai AWS-May-2026 source (dead — redirect loop as of 2026-07-23; retained as plain-text provenance).

- `docs/non-cc/semantic-layers-data-catalog-landscape.md`: de-linked the dead AtScale homepage (`atscale.com` hard-404 on GET+HEAD as of 2026-07-23; kept AtScale as text + the working MQO-MCP GitHub reference).

- `scripts/cc-multi-account.sh`: profile directories are now `chmod 700` — a default umask left them 755, so other local users could read `history.jsonl` and `projects/` transcripts.

- `docs/cc-native/configuration/CC-inline-visuals-analysis.md`: removed the "database architecture diagrams, process flowcharts" example — its only source (a claude.com use-case page) 404s and has no successor on academy.claude.com (#417).
- `lychee.toml`: dropped the `vibekanban.com` exclude — the SSL cert is valid again and the links pass (#254).

- `.claude/settings.json`: removed the six `Bash(git -C * <subcommand> *)` allow rules. A `*` before the subcommand also matches injected git options such as `-c core.fsmonitor=<script>`, so these auto-approved arbitrary command execution. Read-only git needs no allow rule: Claude Code's built-in read-only command set covers it.

- `docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md`, `CC-sandbox-platforms-landscape.md`, `CC-sandboxing-analysis.md`: `sandbox-runtime` links repointed from `anthropic-experimental/` to `anthropics/sandbox-runtime` (repo moved; issue #139 404'd at the old path).

## [0.7.0] - 2026-06-23

### Added

- `docs/cc-native/agents-skills/CC-dynamic-workflows-analysis.md`: new **Observability & tracing** section — workflow/subagent execution emits OpenTelemetry (metrics + logs GA; traces beta via `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA`). Per-subagent `claude_code.llm_request` / `claude_code.tool` spans **nest under the parent Agent-tool span** (`agent_id` / `parent_agent_id`) → a real agent-trajectory trace; partial `gen_ai.*` GenAI conventions. Any OTLP backend (Arize Phoenix, Pydantic Logfire, Datadog, Tempo) ingests it **generically — none has a CC-specific integration**. Cross-refs `CC-agent-observability-methods-analysis.md`. First-party: code.claude.com/docs/en/monitoring-usage.

- `docs/cc-native/agents-skills/CC-dynamic-workflows-analysis.md`: new **Across surfaces** section — dynamic workflows and their primitives across interactive / headless `claude -p` / Agent SDK, with first-party-verified headless nuances: background agents are **awaited** (10-min default cap from **v2.1.182**, `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`), `--bare` skips skills/hooks/MCP/memory (slated to become the `-p` default), and user-invoked skills/custom commands work in `-p` since **v2.1.181**. Answers "are workflows usable in the SDK / `-p` / interactive?" (yes, all three).

- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: new **§8 Output Validation, Guardrails & Verification** — structured-output enforcement ([Instructor](https://github.com/567-labs/instructor), [Outlines](https://github.com/dottxt-ai/outlines), [BAML](https://github.com/BoundaryML/baml), Guidance, Pydantic AI / Marvin), guardrails/policy ([Guardrails AI](https://github.com/guardrails-ai/guardrails), NeMo Guardrails, LLM Guard, safety classifiers), and verification/fact-checking (Bespoke-MiniCheck, FActScore, self-consistency, DeepEval gate). Fills a verified coverage gap (only incidental mentions existed); cross-refs the security/governance docs. Licenses verified first-party — NeMo `NOASSERTION` noted as NVIDIA-only, Bespoke-MiniCheck flagged CC BY-NC.

- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: new **credo-framed synthesis** landscape — the **"-engineering"** disciplines ladder (prompt → context → harness → loop → flow → spec, with first-party coiners: Lütke/Karpathy + Anthropic for context engineering, WalkingLabs + OpenAI for harness engineering, Itamar Friedman/AlphaCodium for flow engineering) and the **"-driven development"** ladder (TDD → BDD → EDD → SDD + Dave Farley), composed into a **five-layer stack** (Disciplines → Methodology → Execution → Feedback → Compound) with **EDD as the keystone**. Cross-links the shipped workflows / observability / eval docs; spec-driven-frameworks table (spec-kit 114.8k★ / OpenSpec / BMAD / Kiro); `open-agentic-coding-harness` as the reference implementation. Indexed in `sdlc-lcm/README.md`.

## [0.6.0] - 2026-06-22

### Added

- `docs/cc-native/configuration/CC-model-provider-configuration.md`: **5 hosted CC-integrated gateways** (Portkey, Martian, Vercel AI Gateway, Zuplo, RelayPlane) back-ported as a compact CC-config table — each `ANTHROPIC_BASE_URL` / auth pattern verified against the gateway's own Claude Code docs (2026-06-22). Defers to `llm-routers-gateways-landscape.md` for the full catalog (router-architecture consolidation, DRY). Partial #304.
- `docs/non-cc/aider-analysis.md`: expanded the **repo-map** mechanism — symbol extraction, PageRank-style graph ranking over the dependency graph, `--map-tokens` (default 1,000), and dynamic auto-sizing (first-party `aider.chat/docs/repomap.html`). Partial #304.

- `docs/cc-community/CC-research-agents-landscape.md` + `CC-memory-tooling-landscape.md`: **`## Sources` tables** — added the CONTRIBUTING-mandated Sources section to both landscape docs. `CC-research-agents` converted ~45 inline body links to reference-style + a Sources table; `CC-memory-tooling` wraps its existing reference definitions in a Sources table.

- `docs/non-cc/agent-frameworks-infrastructure-landscape.md` (§7 RAG & Retrieval): new **Embedding models** subsection ([SPECTER2](https://huggingface.co/allenai/specter2) scholarly-document embeddings + SciNCL; general-purpose note) and **[sqlite-vec](https://github.com/asg017/sqlite-vec)** in Vector databases (single-file SQLite extension, WASM/in-browser KNN so precomputed embeddings ship inside a static site). Fills the §7 embeddings gap and the static-serverless vector-search angle; provenance for the paperverse semantic-"near" roadmap.

- `docs/non-cc/agent-frameworks-infrastructure-landscape.md` (§7 Rerankers): added permissive-license OSS rerankers — [bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3), [Qwen3-Reranker](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B), [mxbai-rerank](https://github.com/mixedbread-ai/mxbai-rerank), [FlashRank](https://github.com/PrithivirajDamodaran/FlashRank), and the [rerankers](https://github.com/AnswerDotAI/rerankers) unified wrapper + [RAGatouille](https://github.com/AnswerDotAI/RAGatouille) — plus a hosted-alternatives note (Voyage/ZeroEntropy/Contextual instruction-following; Jina multimodal). Previously only Cohere Rerank + generic cross-encoders + ColBERT were listed. Self-reported/unverified benchmark figures and NC-licensed/unmaintained entries were deliberately excluded.

### Changed

- `docs/non-cc/llm-routers-gateways-landscape.md`: bottom cross-ref now records that the five CC-integrated gateways are back-ported into the CC config doc, with the landscape kept as the single authoritative catalog (license/pricing/breadth).

- `CONTRIBUTING.md`: **rxiv dispatch serialization note** in Auto-generated content — never fire two same-day `rxiv-paper-eval` dispatches concurrently (the date-stamped `chore/rxiv-paper-triage-<date>` branch collides; the second push is rejected). Cross-refs upstream `gha-rxiv-paper-eval#71`.

- `docs/non-cc/rowboat-analysis.md`: **freshness refresh** against the first-party repo — star count 11.1K → **15K** (forks 1K → 1.5K), language share to TypeScript 96.6%, `updated`/`validated_links` bumped to 2026-06-22. Reconciled the misattribution concern: `rowboatlabs/rowboat` is correctly identified (local-first AI coworker → Obsidian knowledge graph), and the `claude-code`/`claude-cowork` GitHub topic tags are discovery-only — there is no Claude-specific integration surface (model-agnostic via MCP / bring-your-own API key).

- `docs/cc-native/configuration/CC-models-reference.md` + `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: **stale-fact refresh** against first-party Anthropic sources (claude-api reference) — Fable 5 tokenizer figure tightened to ≈1×–1.35× (was "~30%"); the Fable 5 CC-plan-access line reframed now that the 2026-06-22 credit-transition date has arrived; added the model-dependent **minimum cacheable prefix** (4096 tokens on Opus-tier, 2048 on Fable 5 / Sonnet 4.6). Partial #304.

### Fixed

- `docs/cc-native/README.md`: corrected stale subdirectory doc counts — sessions 5→7, sandboxing 4→5, plugins-ecosystem 8→10 (verified against `git ls-files`).

- `docs/cc-native/context-memory/CC-prompt-caching-behavior.md`: corrected the doubled `/docs/en/docs/` path segment in the prompt-caching, pricing, and messages source URLs to the canonical first-party form.

## [0.5.0] - 2026-06-22

### Added

- `docs/cc-community/CC-memory-tooling-landscape.md`: **Memory Taxonomy** section — CoALA working/episodic/semantic/procedural framing plus a classification table normalizing Mem0 / Cognee / Letta / Zep-Graphiti / A-MEM / LangMem / MemoryOS onto those axes (mappings flagged approximate; full descriptions stay in non-cc §4, not duplicated) — and a **Benchmarks** section (LongMemEval + LOCOMO) with the per-framework numbers flagged as vendor self-reported, not benchmark-author-audited.
- `docs/non-cc/agent-frameworks-infrastructure-landscape.md`: added **MemoryOS** (hierarchical short/mid/long-term memory OS, EMNLP 2025) to §4 Agent Memory Infrastructure. (#276)

- `docs/cc-community/CC-community-tooling-landscape.md`: **Layer 5 — context/prompt compression (library)** added to the Token-Waste Reduction Stack — LLMLingua family + Selective Context (prompt compression) and semantic-router (adjacent: routing, which skips LLM calls for recognized intents). Flagged as upstream, **not CC-native** libraries; first-party compression ratios cited as vendor README claims, not measured against a CC workload. (#276)

- `docs/non-cc/ag-ui-protocol-landscape.md`: dedicated **A2A** (agent↔agent — Agent Card / Task lifecycle / JSON-RPC+SSE+gRPC; Google→Linux Foundation, v1.0.1), **AGNTCY** ("Internet of Agents" infra stack — OASF / Agent Directory / SLIM / Identity / ACP; Cisco→LF), and **MCP-as-spec** (2025-11-25 revision: experimental Tasks, OIDC/OAuth client-ID-metadata, enum/URL elicitation, icon metadata) sections — completing the Protocol Triangle beyond the existing AG-UI/A2UI frontend coverage. Purpose/scope broadened accordingly. (#276)

- `docs/cc-community/CC-research-agents-landscape.md`: **local-deep-researcher** (langchain-ai LangGraph *reference* impl — explicitly distinguished from the look-alike LearningCircuit `local-deep-research`) and **dataroom** (hanxiao/Jina local-gather → frontier-synthesize harness, Pi-based) added to §1 + the `/deep-research` mapping table.
- `docs/cc-community/CC-vlm-screen-sharing-landscape.md`: **PixelRAG** (StarTrail-org) added to Observed Implementations — pixel-native RAG (Qwen3-VL-Embedding) shipping a Claude Code `pixelbrowse` plugin.
- `docs/cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md`: **Academic Design-Space Analysis** section for arXiv 2604.14228 ("Dive into Claude Code"), mapping its findings onto the Ibryam pattern taxonomy. (#276)

- `docs/non-cc/semantic-layers-data-catalog-landscape.md`: **new landscape** — the semantic-layer (Cube, dbt MetricFlow, Malloy, AtScale) and data-catalog (DataHub, OpenMetadata, Unity Catalog OSS, Apache Atlas, Google Dataplex) substrate for **agentic data access**, classified by *agent surface* (official MCP server / SDK / NL query). Frames the agent-native evolution via Databricks Genie Ontology + Open Knowledge Format cross-refs. Added to `docs/non-cc/README.md` Infrastructure. (#276)

## [0.4.0] - 2026-06-22

### Changed

- `.claude/settings.json`: add `env.BASH_MAX_OUTPUT_LENGTH=15000` (CodeBurn `detectBashBloat` rule — caps bash tool output to trim per-session tokens). Re-homed from closed PR #206 per #243.
- `lychee.toml`: set `timeout = 30` (lychee default is 20) — keeps genuinely-slow hosts (apmdigest/techsy/qa.allen.ai/e2b.dev/…) link-checked instead of timing out into the exclude list. Orthogonal to transient 5xx, which `max_retries` handles.
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

- `docs/cc-community/CC-usage-tooling-landscape.md`: **CodeBurn Optimization Rules** — the full 16-detector `codeburn optimize` taxonomy table (cache bloat, read:edit ratio, junk/duplicate reads, MCP coverage/profile, ghost agents/skills/commands, bash & `CLAUDE.md` bloat, …), sourced to `src/optimize.ts` (README's ~7-category grouping undercounts). Re-homed from closed PR #206 per #243.
- `docs/cc-native/ci-remote/CC-github-actions-analysis.md`: **`/install-github-app` interactive wizard** (pre-flight warnings, OAuth-token vs API-key chooser, workflow selector), **Custom GitHub App (Bedrock/Vertex)** setup, App provenance, and the `CLAUDE_CODE_OAUTH_TOKEN` path in Manual Setup. Re-homed from PR #206 per #243.
- `docs/cc-native/context-memory/CC-llms-txt-analysis.md`: **Pattern Adoption Beyond Product Docs** — HuggingScience (`/llms-full.txt` for 100+ scientific models across 17 domains) as an `llms-full.txt` adoption example beyond product docs. Re-homed from PR #206 per #243.
- `pyproject.toml` + `.github/workflows/{bump-my-version,tag-release,publish-release}.yaml` + `changelog.d/`: **operator-driven release flow** adapted from [qte77/paperverse](https://github.com/qte77/paperverse) — bump-my-version (version SSOT in `[tool.bumpversion]`) + scriv changelog fragments, run ephemerally via `pipx` (no repo venv/lockfile). Adds `make changelog_new`/`changelog_preview`/`changelog_release` recipes and a CONTRIBUTING "Release & Changelog" section. Adopts the `changelog.d/` fragment workflow deferred in #217. Closes #217.
- `docs/cc-native/configuration/CC-tools-inventory.md`: documented the **WebFetch default User-Agent** (`Claude-User (claude-code/2.1.185; +https://support.anthropic.com/)`, captured 2026-06-22, no override path) and a **bimodal bot-block model** (server WAF 403 vs CC-side denylist) with an observed status-code table (clarivate/g2/crunchbase 403, reddit denylist, langtrace 404, marktechpost 200). Closes #188.
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
