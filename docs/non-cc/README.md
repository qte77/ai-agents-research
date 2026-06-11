# Non-CC Agent and Orchestrator Analyses

Standalone analyses of coding agents and orchestration tools beyond Claude Code.

## Orchestrators

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [air-analysis.md](air-analysis.md) | JetBrains Air (GUI) | No | No |
| [deerflow-analysis.md](deerflow-analysis.md) | ByteDance DeerFlow (LangGraph) | Yes | Yes (Apache 2.0) |
| [devteam-analysis.md](devteam-analysis.md) | agent-era/devteam (TUI) | No | Yes (MIT) |

## Agents

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [goose-analysis.md](goose-analysis.md) | Goose (AAIF; MCP co-creator, reference impl) | Yes | Yes (Apache-2.0) |
| [feynman-analysis.md](feynman-analysis.md) | Companion AI Feynman (research agent, multi-agent investigation) | Yes | Yes (MIT) |
| [hermes-agent-analysis.md](hermes-agent-analysis.md) | Nous Research Hermes (self-improving, multi-platform, 43K stars) | Yes | Yes (MIT) |
| [rowboat-analysis.md](rowboat-analysis.md) | Rowboat (AI coworker, knowledge graph from comms) | No | Yes (Apache-2.0) |
| [github-copilot-cli-analysis.md](github-copilot-cli-analysis.md) | GitHub Copilot CLI (terminal agent, same harness as Copilot coding agent) | Yes | No (proprietary) |

## Knowledge Management

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [karpathy-llm-kb-analysis.md](karpathy-llm-kb-analysis.md) | Karpathy LLM Knowledge Base (markdown-first wiki) | Yes | Gist only |

## Context & Memory Infrastructure

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [openviking-analysis.md](openviking-analysis.md) | ByteDance OpenViking (filesystem-based context DB) | Yes | Yes (AGPL-3.0) |

## Infrastructure

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [insforge-analysis.md](insforge-analysis.md) | InsForge (backend platform for agentic development) | Yes | Yes (Apache-2.0) |
| [goclaw-analysis.md](goclaw-analysis.md) | GoClaw (multi-tenant agent gateway, Go, 7 channels) | Yes | Yes (CC BY-NC 4.0) |

## Frameworks

| Document | Type | Headless | Open Source |
|---|---|---|---|
| [simpleagents-analysis.md](simpleagents-analysis.md) | CraftsMan-Labs/SimpleAgents (Rust LLM SDK) | Yes | Yes (Apache-2.0) |
| [autoagent-analysis.md](autoagent-analysis.md) | HKUDS/AutoAgent (zero-code agent OS) | Yes | Yes (MIT) |

## Protocols & Interfaces

| Document | Scope |
|---|---|
| [ag-ui-protocol-landscape.md](ag-ui-protocol-landscape.md) | AG-UI (Agent-User Interaction protocol), A2UI (Google declarative generative-UI spec), OpenGenerativeUI (CopilotKit reference framework); 2026 ecosystem adoption + Salesforce non-adoption note |

## Planned

Cline, opencode, Codebuff, Gemini CLI, Cursor, Antigravity, Kiro, Codex CLI,
VS Code Copilot Chat, Devin CLI, Windsurf, Aider, Amazon Q,
CodeBuddy, Kilo Code, Trae, Kimi Code, Amp, Pi -- see
[coding-agent-eval plan](https://github.com/qte77/coding-agent-eval) for the
full landscape.

**Disambiguation.** [GitHub Copilot CLI](github-copilot-cli-analysis.md)
(analyzed above) and *Devin CLI* are interactive terminal agents. They share
branding — but not surface — with the *GitHub Copilot Coding Agent* (cloud;
assign an issue, it opens a PR) and *autonomous Devin*, which are covered
separately under CI automation in
[CC-github-actions-analysis.md](../cc-native/ci-remote/CC-github-actions-analysis.md#issue-lifecycle-automation-landscape).
