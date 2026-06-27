# Non-CC Agent and Orchestrator Analyses

Standalone analyses of coding agents and orchestration tools beyond Claude Code.

## Orchestrators

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [air-analysis.md](air-analysis.md) | JetBrains Air (GUI) | No | No |
| [deerflow-analysis.md](deerflow-analysis.md) | ByteDance DeerFlow (LangGraph) | Yes | Yes (Apache 2.0) |
| [devteam-analysis.md](devteam-analysis.md) | agent-era/devteam (TUI) | No | Yes (MIT) |
| [omnigent-analysis.md](omnigent-analysis.md) | Omnigent (Databricks/Neon meta-harness; unifies Claude Code, Codex, Pi, custom agents) | Yes | Yes (Apache-2.0) |

## Agents

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [goose-analysis.md](goose-analysis.md) | Goose (AAIF; MCP co-creator, reference impl) | Yes | Yes (Apache-2.0) |
| [feynman-analysis.md](feynman-analysis.md) | Companion AI Feynman (research agent, multi-agent investigation) | Yes | Yes (MIT) |
| [hermes-agent-analysis.md](hermes-agent-analysis.md) | Nous Research Hermes (self-improving, multi-platform, 43K stars) | Yes | Yes (MIT) |
| [rowboat-analysis.md](rowboat-analysis.md) | Rowboat (AI coworker, knowledge graph from comms) | No | Yes (Apache-2.0) |
| [github-copilot-cli-analysis.md](github-copilot-cli-analysis.md) | GitHub Copilot CLI (terminal agent, same harness as Copilot coding agent) | Yes | No (proprietary) |
| [odysseus-analysis.md](odysseus-analysis.md) | Odysseus (self-hosted all-in-one AI workspace: chat, agents, research, email, calendar) | Yes | Yes (AGPL-3.0) |
| [databricks-genie-analysis.md](databricks-genie-analysis.md) | Databricks Genie One (agentic data coworker; Genie Ontology semantic graph + Genie Agents) | Partial (Slack/Teams/mobile) | No (proprietary; OSS lakehouse base) |

## Coding Agents & IDEs

Terminal/CLI agents and agentic IDEs beyond Claude Code — the former "Planned" backlog, now analyzed (access date 2026-06-16).

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [cline-analysis.md](cline-analysis.md) | Cline (autonomous coding agent; VS Code, CLI, SDK) | Yes | Yes (Apache-2.0) |
| [opencode-analysis.md](opencode-analysis.md) | opencode (terminal agent; TUI + headless CLI, 75+ providers) | Yes | Yes (MIT) |
| [codebuff-analysis.md](codebuff-analysis.md) | Codebuff (terminal agent; multi-agent orchestration, OpenRouter) | Yes | Yes (Apache-2.0) |
| [gemini-cli-analysis.md](gemini-cli-analysis.md) | Gemini CLI (Google; free tier ends 2026-06-18 → enterprise-only) — **Hold** | Yes | Yes (Apache-2.0) |
| [cursor-analysis.md](cursor-analysis.md) | Cursor (GUI AI editor, VS Code fork; Composer agent + CLI) | Partial | No |
| [antigravity-analysis.md](antigravity-analysis.md) | Google Antigravity (agent-first IDE + CLI; preview) | Partial | No |
| [kiro-analysis.md](kiro-analysis.md) | Kiro (AWS spec-driven agentic IDE) | Partial | No |
| [codex-cli-analysis.md](codex-cli-analysis.md) | OpenAI Codex CLI (terminal agent; sandbox, headless CI) | Partial | Yes (Apache-2.0) |
| [vscode-copilot-chat-analysis.md](vscode-copilot-chat-analysis.md) | VS Code Copilot Chat (GA agent mode) | No | Yes (MIT) |
| [devin-cli-analysis.md](devin-cli-analysis.md) | Devin CLI (Cognition; local agent + cloud handoff) | Partial | No |
| [windsurf-analysis.md](windsurf-analysis.md) | Windsurf (now Devin Desktop; Cognition-acquired) | No | No |
| [aider-analysis.md](aider-analysis.md) | Aider (OSS terminal pair-programmer; git-native, multi-LLM) | Yes | Yes (Apache-2.0) |
| [amazon-q-developer-analysis.md](amazon-q-developer-analysis.md) | Amazon Q Developer (CLI + IDE; deprecated 2026-04-30 → Kiro) — **Hold** | Partial | Yes (Apache-2.0 / MIT CLI) |
| [codebuddy-analysis.md](codebuddy-analysis.md) | CodeBuddy (Tencent Cloud AI coding agent; IDE + CLI) | Yes | No |
| [kilo-code-analysis.md](kilo-code-analysis.md) | Kilo Code (OSS agentic coding; VS Code/JetBrains/CLI, 500+ models) | Yes | Yes (MIT) |
| [trae-analysis.md](trae-analysis.md) | Trae (ByteDance VS Code-based agentic IDE) | No | No |
| [kimi-code-analysis.md](kimi-code-analysis.md) | Kimi Code (Moonshot terminal agent; Kimi K2.7-Code) | Yes | Yes (MIT) |
| [amp-analysis.md](amp-analysis.md) | Amp (Sourcegraph terminal-first multi-model agent) | Yes | No |
| [pi-analysis.md](pi-analysis.md) | Pi (minimal terminal coding agent CLI, 15+ providers; Omnigent harness) | Yes | Yes (MIT) |

## Knowledge Management

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [karpathy-llm-kb-analysis.md](karpathy-llm-kb-analysis.md) | Karpathy LLM Knowledge Base (markdown-first wiki) | Yes | Gist only |
| [deepwiki-analysis.md](deepwiki-analysis.md) | DeepWiki (Cognition/Devin auto-generated repo wikis + chat Q&A) | No (hosted) | No |
| [repo-to-docs-tools-landscape.md](repo-to-docs-tools-landscape.md) | Repo-to-docs AI tools catalog (DeepWiki, Code2Tutorial, GitSummarize, Understand Anything); multi-platform | — | Mixed |
| [research-agents-landscape.md](research-agents-landscape.md) | Research/discovery agents catalog (STORM, GPT-Researcher, Elicit, FutureHouse, OpenScholar, PaperQA2) + mapping to CC's /deep-research harness | — | Mixed |
| [open-knowledge-format-analysis.md](open-knowledge-format-analysis.md) | Open Knowledge Format (Google Cloud agent-readable data-catalog spec, v0.1) | — (spec) | Yes (Apache-2.0) |
| [opennote-analysis.md](opennote-analysis.md) | Opennote (AI tutor in notes; video lessons; YC S25, Llama-backed) | No (hosted) | Partial (MIT SDKs; closed core) |

## Reference & Background

| Document | Topic | Access |
|---|---|---|
| [intro-autonomous-robots-analysis.md](intro-autonomous-robots-analysis.md) | Introduction to Autonomous Robots (open textbook, MIT Press) | Open access |
| [harnessx-analysis.md](harnessx-analysis.md) | HarnessX — composable/evolvable agent harness foundry (arXiv 2606.14249) | Preprint (code TBD) |

## Context & Memory Infrastructure

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [openviking-analysis.md](openviking-analysis.md) | ByteDance OpenViking (filesystem-based context DB) | Yes | Yes (AGPL-3.0) |
| [fastcontext-analysis.md](fastcontext-analysis.md) | Microsoft FastContext (Qwen3-4B repo-exploration subagent; parallel READ/GLOB/GREP) | Yes | Yes (MIT) |
| [cocoindex-analysis.md](cocoindex-analysis.md) | CocoIndex (incremental ETL for AI context/RAG; MCP code-search variant) | Yes | Yes (Apache-2.0) |
| [opensrc-analysis.md](opensrc-analysis.md) | opensrc (Vercel Labs; fetches npm package source code for agent context) | Yes | Yes (Apache-2.0) |

## Infrastructure

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [insforge-analysis.md](insforge-analysis.md) | InsForge (backend platform for agentic development) | Yes | Yes (Apache-2.0) |
| [goclaw-analysis.md](goclaw-analysis.md) | GoClaw (multi-tenant agent gateway, Go, 7 channels) | Yes | Yes (CC BY-NC 4.0) |
| [searxng-analysis.md](searxng-analysis.md) | SearXNG (self-hostable metasearch for agent web-search) | Yes | Yes (AGPL-3.0) |
| [web-scraping-extraction-landscape.md](web-scraping-extraction-landscape.md) | Scraping / crawling / extraction tool catalog (SSOT; HTTP clients, browser automation, AI-native scrapers, search APIs, managed platforms, doc extraction, anti-bot) | — | Mixed |
| [code-review-products-landscape.md](code-review-products-landscape.md) | Standalone SaaS PR-review products (CodeRabbit, Greptile, Ellipsis, Sourcery, Qodo Merge, Graphite, Cursor Bugbot, Cubic, Bito, Korbit); multi-platform, not CC-specific | — | Mixed |
| [agent-design-formats-landscape.md](agent-design-formats-landscape.md) | Agent-consumable design formats (awesome-design-md corpus; Google Labs DESIGN.md spec + CLI; Figma/W3C token chain); multi-platform, not CC-specific | — | Mixed |
| [llm-routers-gateways-landscape.md](llm-routers-gateways-landscape.md) | LLM routers / gateways / aggregators catalog (29 tools: OpenRouter, LiteLLM, Portkey, Bifrost, Vercel/Cloudflare AI Gateway, OpenRouter Fusion) | — | Mixed |
| [semantic-layers-data-catalog-landscape.md](semantic-layers-data-catalog-landscape.md) | Semantic-layer + data-catalog substrate for agentic data access (Cube, dbt MetricFlow, Malloy, AtScale, DataHub, OpenMetadata, Unity Catalog, Atlas, Dataplex) — MCP/SDK agent surfaces; cross-refs Genie Ontology + OKF | — | Mixed |

## Frameworks

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [simpleagents-analysis.md](simpleagents-analysis.md) | CraftsMan-Labs/SimpleAgents (Rust LLM SDK) | Yes | Yes (Apache-2.0) |
| [autoagent-analysis.md](autoagent-analysis.md) | HKUDS/AutoAgent (zero-code agent OS) | Yes | Yes (MIT) |
| [deepagents-analysis.md](deepagents-analysis.md) | langchain-ai/deepagents (deep-agents: planning + subagents + virtual FS, on LangGraph) | Yes | Yes (MIT) |
| [openharness-analysis.md](openharness-analysis.md) | HKUDS/OpenHarness (open Python agent harness; 10 subsystems, CC-convention compatible, multi-provider) | Yes | Yes (MIT) |
| [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) | Landscape catalog: orchestration frameworks, LLM routing, memory infrastructure, agent models | — | Mixed |
| [openai-swarm-analysis.md](openai-swarm-analysis.md) | OpenAI Swarm (deprecated educational multi-agent; superseded by Agents SDK) | Yes | Yes (MIT) |
| [openai-agents-sdk-analysis.md](openai-agents-sdk-analysis.md) | OpenAI Agents SDK (multi-agent: handoffs, guardrails, sessions, tracing; GA successor to Swarm) | Yes | Yes (MIT) |

## Protocols & Interfaces

| Document | Scope |
|---|---|
| [ag-ui-protocol-landscape.md](ag-ui-protocol-landscape.md) | AG-UI (Agent-User Interaction protocol), A2UI (Google declarative generative-UI spec), OpenGenerativeUI (CopilotKit reference framework); 2026 ecosystem adoption + Salesforce non-adoption note |
| [agentcanvas-analysis.md](agentcanvas-analysis.md) | AgentCanvas — renders Pydantic AI + Logfire execution traces as interactive HTML diagrams (OTel agent observability) |
| [agent-observability-methods-analysis.md](agent-observability-methods-analysis.md) | Survey of 18 OTel observability platforms + 5 tracing patterns for agent behavior (Langfuse, Arize Phoenix, Logfire, …); CC's own first-party telemetry split to cc-native |

## Backlog status

The former coding-agent backlog — Cline, opencode, Codebuff, Gemini CLI, Cursor,
Antigravity, Kiro, Codex CLI, VS Code Copilot Chat, Devin CLI, Windsurf, Aider,
Amazon Q, CodeBuddy, Kilo Code, Trae, Kimi Code, Amp, Pi — is now analyzed under
[Coding Agents & IDEs](#coding-agents--ides) above. See the
[coding-agent-eval plan](https://github.com/qte77/coding-agent-eval) for the
broader comparison landscape.

**Disambiguation.** [GitHub Copilot CLI](github-copilot-cli-analysis.md)
(analyzed above) and *Devin CLI* are interactive terminal agents. They share
branding — but not surface — with the *GitHub Copilot Coding Agent* (cloud;
assign an issue, it opens a PR) and *autonomous Devin*, which are covered
separately under CI automation in
[CC-github-actions-analysis.md](../cc-native/ci-remote/CC-github-actions-analysis.md#issue-lifecycle-automation-landscape).
