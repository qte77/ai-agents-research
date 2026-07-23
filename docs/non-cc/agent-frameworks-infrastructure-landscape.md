---
title: Agent Frameworks & Infrastructure Landscape
purpose: Catalog of multi-agent orchestration frameworks, LLM-orchestration/routing tools, agent memory infrastructure, agent-oriented foundation models, and specialist models agents call as tools beyond Claude Code — restored and refreshed from the archived frameworks-infrastructure landscape.
category: landscape
status: research
created: 2026-06-14
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Research (informational)

Catalog of agent frameworks and supporting infrastructure beyond Claude Code. Restored from `docs/archive/landscape-agent-frameworks-infrastructure.md` (archived 2026-04-23), distilled to durable facts and first-party links; project-specific integration boilerplate was dropped. Tool/version facts are a **February–March 2026 snapshot** unless noted — verify before relying. Where a tool already has a dedicated analysis in `docs/non-cc/`, it is cross-linked rather than duplicated.

## 1. Multi-Agent Orchestration Frameworks

- [LangGraph](https://github.com/langchain-ai/langgraph) — graph-based stateful orchestration with checkpointing and conditional routing (MIT); the base for many harnesses below.
- [CrewAI](https://github.com/crewAIInc/crewAI) — role-based crews with sequential/hierarchical/consensus execution (MIT).
- [AutoGen / AG2](https://github.com/ag2ai/ag2) — conversational multi-agent framework with group chat and code execution (Apache-2.0).
- [PydanticAI](https://github.com/pydantic/pydantic-ai) — type-safe agents on Pydantic v2 with durable execution + MCP/A2A; the framework this repo's evaluation work builds on. Its [capabilities system][pai-caps] (Jun 2026) bundles instructions + tools + model settings into composable units that support **on-demand / deferred loading** (`defer_loading=True`) — a capability's context is injected only when the agent requests it, trimming per-run tokens (PydanticAI's progressive-disclosure / "skills" answer); capability-scoped hooks fire only on load. Companion managed services: the Pydantic AI Gateway (routing) and [Logfire](agent-observability-methods-analysis.md) observability. A community **full-stack starter** ([Vstorm template](https://pydantic.dev/articles/full-stack-ai-agent-template-pydantic-ai), Jun 2026) scaffolds a production PydanticAI app — Next.js 15 + FastAPI + Postgres/Mongo + Redis, WebSocket streaming, JWT auth, Alembic migrations, Logfire/OpenTelemetry tracing, Docker deploy (LangChain swappable for PydanticAI). A separate capability library, [`pydantic-ai-harness`](https://github.com/pydantic/pydantic-ai-harness) ("batteries for your agent", MIT, 595★; iterates faster than core), ships ready agent capabilities — a sandboxed **CodeMode** (Python via the Monty sandbox), filesystem + shell tools (path-traversal guards / allowlists / timeouts), and provider-adaptive web search — on a *fall-up* model (a local implementation works with any model, auto-switching to provider-native when available); 30+ capabilities are on the roadmap. It is the product face of Pydantic's "harness > model" thesis (see [agentic-engineering-disciplines-landscape.md](../sdlc-lcm/agentic-engineering-disciplines-landscape.md)).
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
- [Flue (Astro)](https://github.com/withastro/flue) — durable, sandboxed TypeScript agent framework from the Astro team; **1.0 Beta** (~2026-06-16, Apache-2.0, [flueframework.com](https://www.flueframework.com)). Harness-first model on the **Pi** agent loop (via `@flue/runtime`): **Durable Streams** record every prompt/tool-response/model-choice to an append-only log, so a fresh process resumes from the last checkpoint after a crash or provider timeout. Ships a **just-bash** in-memory sandbox (no Docker/VM) plus a `local()` sandbox; MCP-native and model-agnostic; **channels** ingest events from Slack/Teams/Discord/GitHub/Linear; on Cloudflare Workers each agent becomes a Durable Object (SQLite FS, `runFiber`/`stash`/`onFiberRecovered`). Supports **subagents / task delegation** (swarm-style coordination is not documented in first-party sources); `SuperagenticAI/pyflue` is a community Python port, not first-party.
- [multica](https://github.com/multica-ai/multica) — source-available platform (modified Apache 2.0: no third-party hosted-service/resale + a frontend logo clause — not OSI open-source) that turns coding-agent CLIs into managed teammates: create issues → assign to an agent or a squad, a local daemon executes and streams progress over WebSocket, with autopilot (cron/webhook) scheduling and a reusable skill library. Integrates 13 agent CLIs (Claude Code, Codex, GitHub Copilot CLI, OpenClaw, OpenCode, Hermes, Gemini, Pi, Cursor Agent, Kimi, Kiro CLI, Antigravity, Qoder CLI); Go + Postgres 17/pgvector backend, Next.js 16 UI. Install `brew install multica-ai/tap/multica` or the `install.sh` script; CLI flows `multica login` → `multica daemon start` → `multica issue create` / `multica workspace switch`. Auth is browser-based via `multica login` — no env vars documented.
- [sudocode](https://github.com/sudocode-ai/sudocode) — git-native agent orchestrator (Apache-2.0, verified from LICENSE; TypeScript): human requirements live as version-controlled **specs**, agent runtime context as **issues**, linked bidirectionally (blocks / related / parent-child / discovered-from) and persisted as JSONL committed to git with a local SQLite cache. Runs Claude Code / Codex / Cursor (+more via Agent Client Protocol, added v0.1.19) in parallel with dependency-ordered (topological) execution and a kanban-style real-time UI. `npm install -g sudocode`; ships CLI + local server/UI + MCP server. v0.2.0 (2026-03-18); 287★, last push 2026-03-18 (`gh api`, 2026-07-23). Directly comparable to multica above (multi-CLI, issue-driven, local daemon) — sudocode is git-repo-resident and OSS where multica is a source-available managed platform.

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
- [autoharness (Kayba)](https://github.com/kayba-ai/autoharness) — autonomous, benchmark-driven optimizer for an *existing* agent harness: runs proposal→evaluate→promote-champion loops (overnight) using pluggable generators (`claude_code`, `codex_cli`, `openai_responses`) and benchmark adapters (`pytest`, `harbor`, `tau2_bench`, `hal`, …) (MIT, Python 3.11+). Online learning counterpart: ACE (§4); benchmarks → [evaluation-data-resources-landscape.md](../sdlc-lcm/evaluation-data-resources-landscape.md).
- [VibeFlow](https://vibeflow.ai) — YC S25 no-code / visual full-stack **app** builder: natural-language → deployable web apps with an **editable, n8n-style visual backend workflow editor** (business logic is inspectable, not a black box), a Convex real-time DB, GitHub deploy + custom domains, "AI Agent Nodes" for in-flow LLM steps, and ~15+ integrations (Stripe/Slack/Notion/…). Web-only, closed SaaS, freemium (paid tiers not surfaced as of 2026-06-20). Name collisions: `pe-menezes/vibeflow` (a CC/Cursor spec-driven tool) and `vibeflowing-inc/vibe_figma` are **not** this product.
- [Warp](https://www.warp.dev/) — "agentic development environment" (ADE): a terminal-rooted agent platform spanning inline completions → prompt-driven agentic workflows → system-triggered autonomous agents, plus **Oz**, an orchestration platform for cloud coding agents. Industry framing: [GV — From Terminal to Agent](https://www.gv.com/news/ai-agent-warp) (Zach Lloyd, 2025).

## 4. Agent Memory Infrastructure

Non-CC memory frameworks; for memory tools that integrate *with Claude Code* (MemSearch, Claude-Mem, MemPalace, ByteRover) see [CC-community-tooling-landscape.md](../cc-community/CC-community-tooling-landscape.md).

The field has reframed memory as **context engineering** — assembling persistent, evolving state across sessions rather than just enlarging the context window.

- [Graphiti (Zep)](https://github.com/getzep/graphiti) — real-time temporal knowledge-graph engine; P95 ~300ms hybrid (vector + BM25 + graph) retrieval, MCP server, Apache-2.0.
- [Zep](https://github.com/getzep/zep) — memory platform on Graphiti; temporal KG, multi-language SDKs ([paper](https://arxiv.org/abs/2501.13956)).
- [Mem0](https://github.com/mem0ai/mem0) — universal memory layer; claims +26% vs OpenAI Memory, 90% lower tokens on LOCOMO ([paper](https://arxiv.org/abs/2504.19413)), Apache-2.0.
- [Cognee](https://github.com/topoteretes/cognee) — Apache-2.0 KG memory engine, 30+ data types, MCP server; raised $7.5M seed (Feb 2026).
- [A-MEM](https://github.com/agiresearch/A-mem) — Zettelkasten-style agentic memory with dynamic linking ([paper](https://arxiv.org/abs/2502.12110)).
- [LangMem](https://github.com/langchain-ai/langmem) — LangGraph-native semantic/episodic/procedural memory (MIT).
- [MemoryOS](https://github.com/BAI-LAB/MemoryOS) — hierarchical short/mid/long-term memory OS for personalized agents; +49.11% F1 over baselines on LoCoMo (self-reported), EMNLP 2025 Oral (Apache-2.0).
- [EverOS (EverMind-AI)](https://github.com/EverMind-AI/EverOS) — **Markdown-native, local-first** portable memory layer (9.4K★, Apache-2.0): plain Markdown files as source of truth over a SQLite + LanceDB hybrid index, file-watch cascade sync, multimodal ingest (text/image/PDF/audio/office), LLM-driven extraction/ranking, and an OpenAI-compatible endpoint; user-owned and self-evolving across apps — a files-first contrast to Mem0's graph-first and MemoryOS's hierarchical designs.
- [Gulp.ai (Osmosis)](https://docs.gulp.ai/introduction) — agent-improvement API enriching prompts with past-interaction knowledge.
- [ACE — Agentic Context Engine (Kayba)](https://github.com/kayba-ai/agentic-context-engine) — self-improving context layer: a three-role loop (Agent / Reflector / SkillManager) curates a persistent "Skillbook" of strategies that evolves with every task, so agents stop repeating mistakes without fine-tuning or a vector DB (Apache-2.0, [paper](https://arxiv.org/abs/2510.04618)). PydanticAI-based; ships an MCP server (`ace-mcp`) and a Claude Code runner. Offline benchmark-driven counterpart: autoharness (§3).
- [learnings-ralphy (qte77 estate)](https://github.com/qte77/learnings-ralphy) — **file-based compound-learning memory**, the filesystem-as-memory complement to the graph/vector engines above: plain-Markdown `CLAUDE.md` + `AGENT_LEARNINGS.md` / `LEARNINGS.md` as durable, git-versioned agent memory with an explicit promotion path (inline fix → `AGENT_LEARNINGS.md` → always-loaded `.claude/rules/` → skills). `learnings-ralphy` distills these **across the whole repo estate** on a weekly loop (synthesize → PRD → TDD → write-back PR). EverOS (above) is the productized markdown-native analog; the trade-off vs the graph engines is recall (grep/LLM over files) for zero infra and full git auditability.
- [MemoryWAM](https://github.com/yangsizhe/MemoryWAM) — an **embodied/robotics-vision** persistent-memory mechanism, distinct in kind from the LLM-conversational/session memory tools above: a video-DiT + action-DiT dual-arm manipulation policy conditions on long, non-Markovian task histories via a hybrid cache (sliding-window recent frames + event-boundary anchor frames + compact learnable "gist tokens"), cutting inference complexity from O(N) to O(N/d) vs. keeping the full history (Apache-2.0, verified via `gh api` license lookup; [paper](https://arxiv.org/abs/2606.20562), arXiv:2606.20562, 2026-06-18). Evaluated on RMBench across nine dual-arm manipulation tasks; 55★, project-page-style repo (no training codebase) as of 2026-07-23.
- [Marginal Advantage Accumulation (MAA)](https://arxiv.org/abs/2606.20475) — offline memory-curation method for LLM-agent self-evolution (Alibaba International Digital Commerce Group; arXiv:2606.20475, 2026-06-18): accumulates signed evidence per memory operation across batches of experience traces (semantic-identity merging + baseline-differenced signals + EMA) so a persistent skill/memory bank keeps only robustly-effective operations, without live environment rollouts. Best result in 14/16 settings across 4 datasets × 4 target models, and beat the online SkillOpt baseline on the two strongest models; reports ~75% lower optimization-phase token cost than online methods (paper claims; methodology not independently verified; no code release found).

## 5. Foundation Models for Agents

Frontier model facts and pricing change fast and live in [CC-models-reference.md](../cc-native/configuration/CC-models-reference.md) (Fable 5 card + free-tier/OSS provider table) and [CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md) (how to route CC to them). Notable agent-oriented / OSS entries:

- [DeepSeek V3.2 / V3.2-Speciale / R1](https://api-docs.deepseek.com/news/news251201) — reasoning-first, agent-trained models (V3.2-Speciale synthesized 1,800+ environments, 85K+ instructions; integrates thinking into tool use). Cost-efficient OSS.
- [Devstral (Mistral)](https://mistral.ai/news/devstral) — Apache-2.0 agentic-coding model family (All Hands AI / OpenHands lineage). Devstral Small 2 (24B) hits 68.0% SWE-Bench Verified (123B: 72.2%) — the top open-source agentic-coding scores; runs on a single RTX 4090 / 32GB Mac, ~30–50× cheaper than Sonnet, and is a listed [Claude Code model backend](https://huggingface.co/mistralai/Devstral-Small-2-24B-Instruct-2512) via OpenAI-compatible routing. Capabilities are folding into the unified Mistral Small 4 line.
- [Arcee Foundation Models (AFM)](https://www.arcee.ai/) — ~4.5B CPU-optimized enterprise model for private/offline deployment.
- [UniRL (Tencent Hunyuan)](https://github.com/Tencent-Hunyuan/UniRL) — unified RL **post-training** framework: one loop (sample → score → advantage → policy update → weight sync) across diffusion, autoregressive VLM/LLM, and unified models, with team algorithms Flow-DPPO / DRPO / CPPO. *Training infrastructure, not an agent or a model an agent calls* — listed as the RL post-training layer behind agent-oriented multimodal models (Hunyuan, Qwen, Stable Diffusion).

## 6. Specialist Models Agents Call as Tools

Non-LLM foundation models an agent invokes as a *tool* for one narrow capability (forecasting, ranking, etc.) — distinct from the agent-driving LLMs in §5. Listed when reachable from an agent via an endpoint or SDK.

- [TimesFM (Google Research)](https://github.com/google-research/timesfm) — time-series **forecasting** foundation model (v2.5: ~200M params, up to 16k context, point + quantile forecasts; PyTorch + JAX/Flax, Apache-2.0). Not an agent LLM — an agent calls it for numeric forecasting, exposed for programmatic/agent use via Vertex AI Model Garden and BigQuery ML.
- [LuxTTS](https://github.com/ysharma3501/LuxTTS) — text-to-speech **voice-cloning** model (~150× realtime, 48kHz, sub-1GB VRAM; Apache-2.0). Not an agent LLM — an agent calls it for the speech-output half of a voice loop (agent text → TTS → audio); voice/TTS sits at the edge of this corpus's scope, listed for completeness.

## 7. RAG & Retrieval Infrastructure

Retrieval is the sibling of memory (§4): §4 persists evolving agent *state*; this section is how agents *retrieve* over corpora. Tool facts verified first-party 2026-06-20; star counts are GitHub-rendered (approximate). For incremental code/RAG ETL see [cocoindex-analysis.md](cocoindex-analysis.md); for a filesystem-first retrieval contrast see [openviking-analysis.md](openviking-analysis.md).

**Pipeline taxonomy**: Naive RAG (index→retrieve→read, single-hop) → Advanced RAG (pre/post-retrieval transforms) → Modular RAG (interoperable, multi-hop) → **Agentic RAG** (the agent plans retrieval, reflects, and calls tools). Survey: [Singh et al. 2025, arXiv:2501.09136](https://arxiv.org/abs/2501.09136).

### GraphRAG family

- [Microsoft GraphRAG](https://github.com/microsoft/graphrag) — entity/relationship extraction → Leiden community detection → Global / Local / DRIFT search over community summaries (MIT, v3.1.0, ~34k★). Indexing is compute-heavy; built for reasoning over large private corpora. Paper: [Edge et al. 2024, arXiv:2404.16130](https://arxiv.org/abs/2404.16130).
- [LightRAG (HKUDS)](https://github.com/HKUDS/LightRAG) — dual-layer KG + vector with five query modes (local/global/hybrid/naive/mix); positioned as an efficient GraphRAG alternative (MIT, v1.5.3, ~37k★).
- [RAPTOR](https://arxiv.org/abs/2401.18059) — recursive embed→cluster→summarize tree; retrieves across abstraction levels (MIT; ICLR 2024; paper reports +20% absolute on QuALITY with GPT-4).
- [nano-graphrag](https://github.com/gusye1234/nano-graphrag) — ~1,100-LOC hackable GraphRAG; swappable LLM/embedding/vector backends (Faiss/Neo4j/Ollama), async (MIT, ~3.9k★).

### Hybrid search & query transforms

- **BM25 + dense** — sparse keyword precision + dense semantic recall, fused via Reciprocal Rank Fusion or weighted combination.
- **Reciprocal Rank Fusion (RRF)** — rank-position-only fusion, default k=60 (Cormack et al., SIGIR 2009).
- [ColBERT (Stanford)](https://github.com/stanford-futuredata/ColBERT) — token-level late interaction (MaxSim); v2 adds residual compression; usable as retriever or reranker (MIT; [arXiv:2112.01488](https://arxiv.org/abs/2112.01488)).
- **HyDE** — the LLM drafts a hypothetical answer whose embedding retrieves real docs, bridging the query↔document vocabulary gap ([Gao et al. 2022, arXiv:2212.10496](https://arxiv.org/abs/2212.10496)); plus multi-query expansion and step-back prompting.

### Rerankers

- [Cohere Rerank](https://cohere.com/rerank) — cross-encoder rerank API (rerank-v4.0 pro/fast, 100+ languages); commercial.
- **Cross-encoders** — joint query+document forward pass (via sentence-transformers); higher accuracy than bi-encoders at O(n) per-candidate cost; run as a second stage after ANN retrieval. ColBERT (above) is the late-interaction middle ground.
- [bge-reranker-v2-m3](https://huggingface.co/BAAI/bge-reranker-v2-m3) — multilingual cross-encoder (BAAI, Apache-2.0); pairs with bge-m3 dense embeddings and is a strong default second stage after BM25+dense fusion.
- [Qwen3-Reranker](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B) — instruction-aware cross-encoder family (Alibaba, Apache-2.0; 0.6B/4B/8B, long context); the 0.6B is CPU-viable, larger sizes trade latency for quality.
- [mxbai-rerank](https://github.com/mixedbread-ai/mxbai-rerank) — DeBERTa-based cross-encoders in three sizes (mixedbread, Apache-2.0); a permissive-license alternative to bge-reranker.
- [FlashRank](https://github.com/PrithivirajDamodaran/FlashRank) — lightweight CPU reranker (Apache-2.0); bundles tiny cross-encoders (optional GGUF listwise) with no PyTorch dependency — for latency-sensitive post-retrieval.
- [rerankers](https://github.com/AnswerDotAI/rerankers) — unified Python API over cross-encoders, ColBERT, MonoT5, RankGPT, FlashRank and hosted APIs (answerdotai, Apache-2.0); swap backends without code changes, handy for A/B eval. [RAGatouille](https://github.com/AnswerDotAI/RAGatouille) makes ColBERT indexing + reranking practical in a few lines.
- **Hosted alternatives** (managed comparison points for local-first stacks): Voyage `rerank-2.5`, ZeroEntropy `zerank-2`, and Contextual AI `ctxl-rerank-v2` add instruction-following without fine-tuning (Contextual also ships open weights); Jina `reranker-m0` is multimodal (CC BY-NC). Per-search (Cohere) vs per-token (Voyage/ZeroEntropy) billing makes headline cost comparison non-trivial.

### Embedding models

- [SPECTER2](https://huggingface.co/allenai/specter2) — scientific-document embeddings (AllenAI; citation-proximity-trained, task-adaptive adapters), a strong default for scholarly-paper similarity where general-purpose embeddings underperform (Apache-2.0). SciNCL is a citation-neighbour-sampled alternative.
- General-purpose text embeddings (sentence-transformers bi-encoders, BAAI **bge**, **nomic-embed**) cover cross-domain corpora; prefer a domain-tuned model when the corpus is narrow (e.g. SPECTER2 for papers).

### Vector databases

- [Qdrant](https://github.com/qdrant/qdrant) — dense + sparse + multi-vector (ColBERT), built-in RRF/DBSF hybrid fusion, quantization (Apache-2.0, Rust).
- [Milvus](https://github.com/milvus-io/milvus) — cloud-native distributed; HNSW/IVF/DiskANN; billion-vector scale (Apache-2.0).
- [Weaviate](https://github.com/weaviate/weaviate) — vector + keyword + RAG in a single query; integrated auto-vectorization (BSD-3-Clause).
- [Chroma](https://github.com/chroma-core/chroma) — minimal API, in-memory → production (Apache-2.0).
- [pgvector](https://github.com/pgvector/pgvector) — vectors inside Postgres: ACID, JOINs, no separate system (PostgreSQL License).
- [Pinecone](https://www.pinecone.io/) — fully managed serverless ANN; no self-hosted option (proprietary).
- [LanceDB](https://github.com/lancedb/lancedb) — embedded, multimodal, Lance columnar format, zero-copy + versioning (Apache-2.0).
- [sqlite-vec](https://github.com/asg017/sqlite-vec) — vector search as a single-file **SQLite extension**; runs in-process and compiles to **WASM** for in-browser KNN, so precomputed embeddings can ship inside a static site with no server (Apache-2.0). Brute-force (no ANN index yet, pre-1.0) — fine at small/medium corpus sizes.

### RAG evaluation

- [RAGAs](https://github.com/explodinggradients/ragas) — reference-free metrics (faithfulness, answer relevancy, context precision/recall) via LLM-as-judge (Apache-2.0; [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)).
- [TruLens](https://github.com/truera/trulens) — OTel tracing + LLM-as-judge feedback with agentic evaluators (MIT).
- [DeepEval](https://github.com/confident-ai/deepeval) — pytest-style LLM-output tests: RAG metrics + G-Eval + hallucination detection (Apache-2.0). Eval cross-ref: [evaluation-data-resources-landscape.md](../sdlc-lcm/evaluation-data-resources-landscape.md).

### Graph visualization

The post-retrieval / analysis layer: once a GraphRAG pipeline or knowledge graph (the GraphRAG family above) is built, these render it for inspection. JS browser libraries dominate for embeddable / static-site graphs; desktop and GPU tools handle large-scale exploration. Licenses verified first-party 2026-06-28.

- [vis-network](https://github.com/visjs/vis-network) — force-directed interactive renderer with physics layout out of the box (dual **Apache-2.0 OR MIT**); this repo's own knowledge graph ships as a static `ui/graph.html` rendered by vis-network (graphify output).
- [D3.js](https://github.com/d3/d3) — low-level SVG/Canvas toolkit (**ISC**, formerly BSD); maximal control, but you author the force-simulation and layout yourself — not a drop-in graph renderer.
- [Cytoscape.js](https://github.com/cytoscape/cytoscape.js) — graph-theory library with built-in layouts for browser + Node (**MIT**); strong for biological / network analysis.
- [Sigma.js](https://github.com/jacomyal/sigma.js) — WebGL-accelerated renderer for large graphs in the browser (**MIT**).
- [Gephi](https://github.com/gephi/gephi) — open-source desktop graph-analysis app (**GPL-3.0**; some NetBeans modules CDDL); ForceAtlas2 layout + interactive exploration for big static graphs.
- [PyGraphistry](https://github.com/graphistry/pygraphistry) — **BSD-3-Clause** Python client that pushes data to a **Graphistry** GPU server whose rendering engine is **commercial / closed** (open-core: the client alone is just data-shaping).
- [Neo4j Bloom](https://neo4j.com/product/bloom/) — codeless graph-exploration UI bundled with Neo4j; **freemium** (local DB only — remote/sharing/perspectives require paid Neo4j Enterprise). OSS alternative: [Neo4j Browser](https://github.com/neo4j/neo4j-browser) (**GPL-3.0** Cypher IDE).

## 8. Output Validation, Guardrails & Verification

Validation is the post-generation sibling of retrieval (§7): enforcing that agent output conforms to a **schema/contract**, a **policy**, or **ground truth** before it is used. Tool facts (license, mechanism) verified first-party 2026-06-22. For the governance/threat-model framing (NIST AI RMF, OWASP LLM Top 10, MAESTRO) see [ai-security-governance-analysis.md](../sdlc-lcm/ai-security-governance-analysis.md) and [mas-security-framework.md](../sdlc-lcm/mas-security-framework.md).

### Structured-output / schema enforcement

- [Instructor](https://github.com/567-labs/instructor) — wraps any LLM call, validates the response against a Pydantic model, and re-prompts on validation failure (MIT). Thinnest provider-agnostic retrofit; no constrained decoding.
- [Outlines](https://github.com/dottxt-ai/outlines) — constrained decoding via finite-state machines over the model vocabulary: guarantees JSON-schema / regex / grammar conformance *during* generation (Apache-2.0); requires local or served model access.
- [BAML](https://github.com/BoundaryML/baml) — schema-as-contract DSL with Schema-Aligned Parsing (post-hoc, tolerant of markdown/CoT preambles), compiled to typed functions in several languages (Apache-2.0). Fits contract-first pipelines even when a model lacks native tool-calling.
- [Guidance](https://github.com/guidance-ai/guidance) — grammar-constrained generation interleaving prompt control flow with sampling (MIT); local/vLLM backends.
- [Pydantic AI](https://github.com/pydantic/pydantic-ai) / [Marvin](https://github.com/PrefectHQ/marvin) — agent frameworks that validate outputs against Pydantic models by construction, with auto-retry on mismatch (MIT / Apache-2.0).

### Guardrails / policy

- [Guardrails AI](https://github.com/guardrails-ai/guardrails) — composable pre/post validator pipeline (PII, toxicity, schema, relevance) with a Hub of pre-built validators and retry-on-violation (Apache-2.0).
- [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) — Colang DSL for dialog-flow rails (topicality, jailbreak, self-check input/output) that models full conversation state, not just single-turn I/O (NVIDIA).
- [LLM Guard](https://github.com/protectai/llm-guard) — provider-agnostic input/output scanners: PII anonymization, prompt-injection classifiers, toxicity, secrets detection (MIT).
- **Safety classifiers** — Llama Guard / ShieldGemma are fine-tuned hazard-taxonomy classifiers run as a pre/post filter (Llama / Gemma community licenses, use restrictions); Lakera Guard is the hosted closed-source equivalent.

### Verification / fact-checking

- [Bespoke-MiniCheck](https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B) — fast claim-vs-document grounding checker; a binary support score maps naturally onto confidence-tagging of extracted facts (**CC BY-NC 4.0 — non-commercial**; commercial license separate).
- [FActScore](https://github.com/shmsw25/FActScore) — decomposes long output into atomic claims and verifies each against a knowledge source (MIT); higher latency, gold-standard for biographical/encyclopedic factuality.
- **Self-consistency** (sample-N + semantic majority vote for output stability) and **property-based testing** (assert output *properties* — schema shape, field presence, value bounds — across prompt variations) are dependency-light techniques rather than tools.
- For CI eval gates, [DeepEval](https://github.com/confident-ai/deepeval) (under RAG evaluation above) doubles as a faithfulness/hallucination output-quality gate.

## Production Patterns & Reference Frameworks

- [12-Factor Agents][12fa-blog] ([GitHub mirror][12fa-gh]) — principles for production-grade LLM agents (Dex Horthy / HumanLayer, 2025-04-03). Full treatment: [mas-design-principles.md](../sdlc-lcm/mas-design-principles.md).
- [Agents Towards Production](https://github.com/NirDiamant/agents-towards-production) — end-to-end playbooks for shipping agents.
- [Learn Harness Engineering (WalkingLabs)](https://github.com/walkinglabs/learn-harness-engineering) — project-based course on *harness engineering* for reliable AI coding agents: structuring Instructions, State, Verification, Scope, and Session Lifecycle around the model instead of fine-tuning it (12 lectures + 6 projects, framed around Claude Code / Codex; MIT). Maps onto [CC-agentic-harness-patterns-analysis.md](../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md).
- [Hands-On Modern RL (WalkingLabs)](https://github.com/walkinglabs/hands-on-modern-rl) — practice-first RL curriculum from classic control to LLM post-training (RLHF, DPO, GRPO, RLVR, DeepSeek-R1) and agentic RL (multi-turn credit assignment, tool-use trajectories, Deep Research); Python/PyTorch (CC BY-NC-SA 4.0, non-commercial).
- [Compiling Agentic Workflows into LLM Weights](https://arxiv.org/abs/2605.22502) — Dennis et al. (2026-05-21) argue for *compiling* an agent's orchestration procedure into the weights of a small fine-tuned model instead of an external framework, reporting near-frontier quality at ~2 orders-of-magnitude lower cost — with no context-window or orchestration overhead — across travel-booking, support, and insurance-claims workflows (14–55 nodes). A weight-level counterpoint to the graph/framework orchestration in §1 (paper claims; methodology not independently verified).
- [Beyond Global Replanning: Hierarchical Recovery for Cross-Device Agent Systems](https://arxiv.org/abs/2606.20487) — Yao et al. (Shanghai Jiao Tong University et al., arXiv:2606.20487, 2026-06-18) propose **H-RePlan**, splitting multi-device agent failure recovery into device-local strategy recovery vs. orchestrator-level global replanning via a compact cross-layer failure abstraction, plus **HeraBench** (23 seed tasks → 174 fault-injected variants across a 4-device Linux+Android testbed) to evaluate the distinction. Reported vs. a UFO3-GUI baseline: 75.84% vs 46.86% completion, 36.78% vs 13.79% perfect-pass rate, and ~5.44× lower token cost per perfect pass (paper claims; methodology not independently verified; no code/benchmark repo published as of 2026-07-23).

## Cross-References

- [CC-community-tooling-landscape.md](../cc-community/CC-community-tooling-landscape.md) — CC-integrating memory and tooling
- [CC-model-provider-configuration.md](../cc-native/configuration/CC-model-provider-configuration.md) — model/provider configuration and free-tier reference
- [agent-observability-methods-analysis.md](agent-observability-methods-analysis.md) — observability/tracing platforms (separate restore)
- [research-agents-landscape.md](research-agents-landscape.md) — research/discovery agents
- [ai-security-governance-analysis.md § MCP Ecosystem Security](../sdlc-lcm/ai-security-governance-analysis.md#mcp-ecosystem-security) — MCP server threat model
- [ag-ui-protocol-landscape.md](ag-ui-protocol-landscape.md) — the MCP / A2A / AG-UI protocol-interop triangle these frameworks implement

[12fa-blog]: https://www.hlyr.dev/blog/12-factor-agents
[12fa-gh]: https://github.com/humanlayer/12-factor-agents
[pai-caps]: https://pydantic.dev/articles/pydantic-ai-capabilities

## Sources

Each framework / tool entry cites its repo or docs inline (reference-style and inline links above); framework stars were `gh api`-verified at the snapshot dates noted in the relevant sections.
