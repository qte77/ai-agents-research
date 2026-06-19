---
title: Agent Frameworks & Infrastructure Landscape
purpose: Catalog of multi-agent orchestration frameworks, LLM-orchestration/routing tools, agent memory infrastructure, agent-oriented foundation models, and specialist models agents call as tools beyond Claude Code — restored and refreshed from the archived frameworks-infrastructure landscape.
category: landscape
status: research
created: 2026-06-14
updated: 2026-06-19
validated_links: 2026-06-19
---

**Status**: Research (informational)

Catalog of agent frameworks and supporting infrastructure beyond Claude Code. Restored from `docs/archive/landscape-agent-frameworks-infrastructure.md` (archived 2026-04-23), distilled to durable facts and first-party links; project-specific integration boilerplate was dropped. Tool/version facts are a **February–March 2026 snapshot** unless noted — verify before relying. Where a tool already has a dedicated analysis in `docs/non-cc/`, it is cross-linked rather than duplicated.

## 1. Multi-Agent Orchestration Frameworks

- [LangGraph](https://github.com/langchain-ai/langgraph) — graph-based stateful orchestration with checkpointing and conditional routing (MIT); the base for many harnesses below.
- [CrewAI](https://github.com/crewAIInc/crewAI) — role-based crews with sequential/hierarchical/consensus execution (MIT).
- [AutoGen / AG2](https://github.com/ag2ai/ag2) — conversational multi-agent framework with group chat and code execution (Apache-2.0).
- [PydanticAI](https://github.com/pydantic/pydantic-ai) — type-safe agents on Pydantic v2 with durable execution + MCP/A2A; the framework this repo's evaluation work builds on.
- [LlamaIndex Agents](https://github.com/run-llama/llama_index) — RAG-optimized agents over 100+ data sources.
- [Letta](https://github.com/letta-ai/letta) — stateful agents with hierarchical self-editing memory, by the [MemGPT](https://arxiv.org/abs/2310.08560) authors (Apache-2.0).
- [Agno](https://github.com/agno-agi/agno) — high-performance multi-agent runtime with built-in memory/session, FastAPI app, strong MCP support.
- [Microsoft Agent Framework](https://github.com/microsoft/semantic-kernel) — unifies Semantic Kernel + AutoGen (public preview Oct 2025); dual agent/workflow orchestration, A2A + MCP, .NET + Python.
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) — lightweight provider-agnostic agents with handoffs, guardrails, tracing (Mar 2025).
- [Google ADK](https://github.com/google/adk-python) — LLM/Workflow/Custom agents with built-in eval + MCP; deploys to Vertex AI Agent Engine (Apr 2025).
- [AWS Agent Squad](https://github.com/awslabs/agent-squad) — intent-classification query routing across agents, Python + TypeScript.
- [Swarms](https://github.com/kyegomez/swarms) — enterprise swarm orchestration (hierarchical/parallel/graph), Apache-2.0.
- [Fetch.ai uAgents](https://github.com/fetchai/uAgents) — blockchain-integrated autonomous agents with on-chain payments (Agentverse).
- [DeerFlow (ByteDance)](https://github.com/bytedance/deer-flow) — LangGraph super-agent harness with Markdown skills + sandboxed execution. Full analysis: [deerflow-analysis.md](deerflow-analysis.md).
- [DeepAgents (LangChain)](https://github.com/langchain-ai/deepagents) — planning + sub-agent harness. Full analysis: [deepagents-analysis.md](deepagents-analysis.md).
- [Flue (Astro)](https://github.com/withastro/flue) — durable, sandboxed TypeScript agent framework from the Astro team: every session is recorded to a durable stream and safely resumed after a crash; agents/workflows/sandboxes/tools/skills + multi-agent swarms, model-agnostic and MCP-native, built on the Pi agent harness (Apache-2.0, [flueframework.com](https://www.flueframework.com)).

## 2. LLM Orchestration & Routing

- [LangChain](https://github.com/langchain-ai/langchain) — broad LLM app framework, 100+ integrations (MIT).
- [Haystack (deepset)](https://github.com/deepset-ai/haystack) — production RAG/pipeline framework (Apache-2.0).
- [DSPy (Stanford)](https://github.com/stanfordnlp/dspy) — "programming, not prompting": modules + optimizers auto-tune prompts/weights; v3.1 (Jan 2026), Agenspy adds MCP/A2A.
- [Restack](https://github.com/restackio) — event-driven, durable agent backend with task queues (Apache-2.0).
- **Routers, gateways & aggregators** now live in a dedicated catalog → [llm-routers-gateways-landscape.md](llm-routers-gateways-landscape.md) (29 provider-agnostic tools: OpenRouter, Withmartian/Martian, LiteLLM, Portkey, Mammouth, Requesty, Helicone, Vercel/Cloudflare AI Gateway, OpenRouter Fusion, …). CC-side routing config: [CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md).

## 3. Lightweight & Specialized Frameworks

- [Atomic Agents](https://github.com/BrainBlend-AI/atomic-agents) — modular Pydantic/Instructor pipelines with strict I/O schemas.
- [smolAgents (HuggingFace)](https://github.com/huggingface/smolagents) — minimalist code-first agents with HF model access.
- [Youtu-Agent (Tencent)](https://github.com/Tencent/Youtu-agent) — async, YAML-configured agents; 71.47% WebWalkerQA, OSS-model friendly.
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT), [BabyAGI](https://github.com/yoheinakajima/babyagi), [SuperAGI](https://github.com/TransformerOptimus/SuperAGI) — the original autonomous-task-loop projects (recursive planning; AutoGPT/BabyAGI/SuperAGI respectively minimal→GUI).
- [Rippletide](https://www.rippletide.com/) — neuro-symbolic "hypergraph decision engine" for autonomous sales agents (zero-hallucination claims).
- [autoharness (Kayba)](https://github.com/kayba-ai/autoharness) — autonomous, benchmark-driven optimizer for an *existing* agent harness: runs proposal→evaluate→promote-champion loops (overnight) using pluggable generators (`claude_code`, `codex_cli`, `openai_responses`) and benchmark adapters (`pytest`, `harbor`, `tau2_bench`, `hal`, …) (MIT, Python 3.11+). Online learning counterpart: ACE (§4); benchmarks → [CC-evaluation-data-resources-landscape.md](../cc-community/CC-evaluation-data-resources-landscape.md).

## 4. Agent Memory Infrastructure

Non-CC memory frameworks; for memory tools that integrate *with Claude Code* (MemSearch, Claude-Mem, MemPalace, ByteRover) see [CC-community-tooling-landscape.md](../cc-community/CC-community-tooling-landscape.md).

The field has reframed memory as **context engineering** — assembling persistent, evolving state across sessions rather than just enlarging the context window.

- [Graphiti (Zep)](https://github.com/getzep/graphiti) — real-time temporal knowledge-graph engine; P95 ~300ms hybrid (vector + BM25 + graph) retrieval, MCP server, Apache-2.0.
- [Zep](https://github.com/getzep/zep) — memory platform on Graphiti; temporal KG, multi-language SDKs ([paper](https://arxiv.org/abs/2501.13956)).
- [Mem0](https://github.com/mem0ai/mem0) — universal memory layer; claims +26% vs OpenAI Memory, 90% lower tokens on LOCOMO ([paper](https://arxiv.org/abs/2504.19413)), Apache-2.0.
- [Cognee](https://github.com/topoteretes/cognee) — open-source KG memory engine, 30+ data types, MCP server; raised $7.5M seed (Feb 2026).
- [A-MEM](https://github.com/agiresearch/A-mem) — Zettelkasten-style agentic memory with dynamic linking ([paper](https://arxiv.org/abs/2502.12110)).
- [LangMem](https://github.com/langchain-ai/langmem) — LangGraph-native semantic/episodic/procedural memory (MIT).
- [Gulp.ai (Osmosis)](https://docs.gulp.ai/introduction) — agent-improvement API enriching prompts with past-interaction knowledge.
- [ACE — Agentic Context Engine (Kayba)](https://github.com/kayba-ai/agentic-context-engine) — self-improving context layer: a three-role loop (Agent / Reflector / SkillManager) curates a persistent "Skillbook" of strategies that evolves with every task, so agents stop repeating mistakes without fine-tuning or a vector DB (Apache-2.0, [paper](https://arxiv.org/abs/2510.04618)). PydanticAI-based; ships an MCP server (`ace-mcp`) and a Claude Code runner. Offline benchmark-driven counterpart: autoharness (§3).

## 5. Foundation Models for Agents

Frontier model facts and pricing change fast and live in [CC-models-reference.md](../cc-native/configuration/CC-models-reference.md) (Fable 5 card + free-tier/OSS provider table) and [CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md) (how to route CC to them). Notable agent-oriented / OSS entries:

- [DeepSeek V3.2 / V3.2-Speciale / R1](https://api-docs.deepseek.com/news/news251201) — reasoning-first, agent-trained models (V3.2-Speciale synthesized 1,800+ environments, 85K+ instructions; integrates thinking into tool use). Cost-efficient OSS.
- [Devstral (Mistral)](https://mistral.ai/news/devstral) — Apache-2.0 agentic-coding model family (All Hands AI / OpenHands lineage). Devstral Small 2 (24B) hits 68.0% SWE-Bench Verified (123B: 72.2%) — the top open-source agentic-coding scores; runs on a single RTX 4090 / 32GB Mac, ~30–50× cheaper than Sonnet, and is a listed [Claude Code model backend](https://huggingface.co/mistralai/Devstral-Small-2-24B-Instruct-2512) via OpenAI-compatible routing. Capabilities are folding into the unified Mistral Small 4 line.
- [Arcee Foundation Models (AFM)](https://www.arcee.ai/) — ~4.5B CPU-optimized enterprise model for private/offline deployment.

## 6. Specialist Models Agents Call as Tools

Non-LLM foundation models an agent invokes as a *tool* for one narrow capability (forecasting, ranking, etc.) — distinct from the agent-driving LLMs in §5. Listed when reachable from an agent via an endpoint or SDK.

- [TimesFM (Google Research)](https://github.com/google-research/timesfm) — time-series **forecasting** foundation model (v2.5: ~200M params, up to 16k context, point + quantile forecasts; PyTorch + JAX/Flax, Apache-2.0). Not an agent LLM — an agent calls it for numeric forecasting, exposed for programmatic/agent use via Vertex AI Model Garden and BigQuery ML.

## Production Patterns & Reference Frameworks

- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) — principles for production-grade LLM agents.
- [Agents Towards Production](https://github.com/NirDiamant/agents-towards-production) — end-to-end playbooks for shipping agents.
- [Learn Harness Engineering (WalkingLabs)](https://github.com/walkinglabs/learn-harness-engineering) — project-based course on *harness engineering* for reliable AI coding agents: structuring Instructions, State, Verification, Scope, and Session Lifecycle around the model instead of fine-tuning it (12 lectures + 6 projects, framed around Claude Code / Codex; MIT). Maps onto [CC-agentic-harness-patterns-analysis.md](../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md).
- [Hands-On Modern RL (WalkingLabs)](https://github.com/walkinglabs/hands-on-modern-rl) — practice-first RL curriculum from classic control to LLM post-training (RLHF, DPO, GRPO, RLVR, DeepSeek-R1) and agentic RL (multi-turn credit assignment, tool-use trajectories, Deep Research); Python/PyTorch (CC BY-NC-SA 4.0, non-commercial).

## Cross-References

- [CC-community-tooling-landscape.md](../cc-community/CC-community-tooling-landscape.md) — CC-integrating memory and tooling
- [CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md) — model/provider configuration and free-tier reference
- [CC-agent-observability-methods-analysis.md](../cc-community/CC-agent-observability-methods-analysis.md) — observability/tracing platforms (separate restore)
- [CC-research-agents-landscape.md](../cc-community/CC-research-agents-landscape.md) — research/discovery agents
- [CC-ai-security-governance-analysis.md § MCP Ecosystem Security](../cc-community/CC-ai-security-governance-analysis.md#mcp-ecosystem-security) — MCP server threat model
