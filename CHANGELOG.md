<!-- markdownlint-disable MD024 no-duplicate-heading -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Types of changes**: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`

<!-- scriv-insert-here -->

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
