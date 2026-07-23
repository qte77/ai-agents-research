---
title: Research Agents & Discovery Platforms Landscape
purpose: Catalog of autonomous research agents, scientific-domain models, and literature discovery/analysis platforms for research automation, with a mapping of deep-research agents to Claude Code's bundled /deep-research harness.
category: landscape
status: research
created: 2026-06-14
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Research (informational)

Survey of agents and platforms for autonomous scientific discovery, literature search, and paper analysis. Restored from `docs/archive/landscape-research-agents.md` (archived 2026-04-23) and trimmed to the durable catalog; project-specific integration notes were dropped. For agent *frameworks* and infrastructure see [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md); for evaluation tooling see [evaluation-data-resources-landscape.md](../sdlc-lcm/evaluation-data-resources-landscape.md).

## 1. Autonomous Research Agents

Agents that conduct multi-step research and generate research outputs.

- [DeepResearch (Alibaba-NLP)][deepresearch-alibaba] — 30.5B-param long-horizon information-seeking agent (3.3B active/token, 128K ctx); ReAct + "IterResearch Heavy" modes, on-policy RL. On HF/ModelScope/OpenRouter.
- [AI-Researcher (HKUDS)][ai-researcher] — NeurIPS 2025 Spotlight; end-to-end literature→manuscript pipeline with a Writer Agent and the Scientist-Bench benchmark ([paper][ai-researcher-paper]).
- [The AI Scientist v2 (Sakana AI)][ai-scientist-v2] — produced the first peer-review-accepted fully-AI-generated workshop paper (Apr 2025); agentic tree-search + VLM feedback, ~$6–15/paper ([paper][ai-scientist-v2-paper]).
- [GPT-Researcher][gpt-researcher] — LangGraph multi-agent deep web+local research producing cited long-form reports; STORM-inspired.
- [STORM / Co-STORM (Stanford)][storm] — multi-perspective knowledge curation generating Wikipedia-style cited articles; 70K+ preview users, FreshWiki/WildSeek datasets.
- [Agent Laboratory][agent-laboratory] — human-in-the-loop end-to-end research assistant (lit review → experiments → report).
- [MLR-Copilot][mlr-copilot] — three-phase ML-research automation (idea → implementation → execution) ([paper][mlr-copilot-paper]).
- [SciSciGPT][sciscigpt] — open-source "science of science" collaborator proposing an LLM-agent capability-maturity model.
- [autoresearch (Karpathy)][autoresearch] — minimalist overnight ML research: agents edit one `train.py`, fixed 5-min GPU runs, single metric (val bits-per-byte), meta-programmed via `program.md`.
- [Kosmos (Edison Scientific)][kosmos] — autonomous scientist using structured world models; claims ~6 months of PhD-equivalent work per run (proprietary).
- [Denario (AstroPilot-AI)][denario] — AG2 + LangGraph multi-agent pipeline producing publication-ready LaTeX; uses CMBAgent as backend.
- [CMBAgent][cmbagent] — AG2-based autonomous "Planning & Control" multi-agent system; 1st place, NeurIPS 2025 Fair Universe Competition.
- [OpenAI Deep Research][openai-deep-research] — agentic ChatGPT capability; API as `o3-deep-research` ($10/$40 per MTok, 200K ctx, MCP connectors), led HLE at launch.
- [Gemini Deep Research][gemini-deep-research] — Gemini 3 Pro long-horizon agent via the Interactions API (`deep-research-pro-preview-12-2025`); 46.4% HLE, 66.1% DeepSearchQA, background execution + remote MCP.
- [AutoScientists (mims-harvard)][autoscientists] — decentralized team of AI agents for long-running computational-science experiments, self-organizing around promising hypotheses; **packaged as Claude Code subagents** coordinating via a local ClawInstitute server (no central planner). BioML-Bench 74.4% mean leaderboard percentile (629★, Python) — the most direct CC-harness tie-in here.
- [local-deep-research (LearningCircuit)][local-deep-research] — LLM-agnostic deep-research assistant: local (Ollama/LM Studio/llama.cpp) + cloud (Claude, OpenAI, Gemini, OpenRouter), LangGraph agent strategies, 20+ search sources (arXiv/PubMed/SearXNG/…), cited reports; 95.7% SimpleQA. MIT, 8.5k★, v1.7.0 (2026-06) — a close OSS parallel to CC's [`/deep-research`](../cc-native/agents-skills/CC-dynamic-workflows-analysis.md#bundled-workflow-deep-research).
- [local-deep-researcher (langchain-ai)][local-deep-researcher] — **distinct from the above** despite the near-identical name: LangChain's minimal LangGraph *reference* implementation of the search→summarize→reflect loop (Ollama/LMStudio, local-only by default) — the canonical starting pattern, not a full assistant. MIT, ~9.2k★.
- [dataroom (hanxiao / Jina)][dataroom] — self-hosted research *harness*: a local LLM (Qwen3.6 on a single GPU) runs the mechanical search/read/rerank via Jina CLI tools and emits a structured "dataroom" knowledge package for a frontier model to synthesize — the "cheap local gathering, expensive frontier reasoning" split. Pi-based (see [pi-analysis.md](pi-analysis.md)); ~168★, new.
- [Perplexity Computer][perplexity-computer] — Perplexity's general-purpose autonomous agent orchestrator (launched Feb 2026, MCP tool/connector calls; follows 2025's Comet browser agent). HBS+Perplexity production-data study ([paper][perplexity-computer-paper], Feb 27–May 27, 2026; 10,000 matched query pairs drawn from a pool of 100,000 dual-product users, multiple pairs per user permitted) finds 26min of autonomous machine work per session vs. 33s for Search, 55% lower per-query dissatisfaction (1.3% vs. 2.9%), -87%/-94% time/cost vs. Search+human workflows (79–92%/87–96% across 18 occupational domains), and +38% knowledge-domain scope per query (2.40 vs. 1.74 domains).

**Domain-specific science agents**: [Coscientist (CMU, Nature)][coscientist] — GPT-4 chemistry agent driving cloud-lab experiments; [ChemCrow][chemcrow] — GPT-4 + 18 chemistry tools; [BioPlanner][bioplanner] — biology protocol generation (BIOPROT, 9K+ protocols); [BioChatter][biochatter] — privacy-preserving biomedical conversational-AI framework.

## 2. Specialized Scientific Models

- [MatterGen (Microsoft)][mattergen] — diffusion generative model for inorganic-materials design with multi-property conditioning (CIF output).
- [MatterSim (Microsoft)][mattersim] — M3GNet deep-learning atomistic simulator across elements/temperatures/pressures (1M and 5M variants).

## 3. Research Discovery & Analysis Platforms

Literature search, paper analysis, and discovery (assistive, not autonomous conductors).

- [OpenScholar (Ai2/UW)][openscholar] — retrieval-augmented LM over 45M open-access papers; +5% correctness vs GPT-4o, far lower hallucination (Llama-3.1-8B fine-tune) ([paper][openscholar-paper]).
- [FutureHouse Platform][futurehouse] — Crow/Falcon/Owl agents with benchmarked superhuman literature search; built on PaperQA2.
- [Elicit][elicit] — literature-matrix extraction, ~99.4% data-point accuracy in systematic reviews; 200M+ Semantic Scholar corpus.
- [Scite][scite] — Smart Citations classifying supporting/contrasting/mentioning references (1.3B+ citations).
- [Consensus][consensus] — evidence-backed yes/no answers from scholarly consensus.
- [Undermind][undermind] — adaptive "successive search" claiming 10–50× over Google Scholar with completeness estimates.
- [Semantic Scholar][semantic-scholar] — 200M+ paper semantic search, embeddings, and [API][semantic-scholar-api] underpinning many tools here.
- [Liner][liner] — AI research search over 200M+ sources with line-by-line citations and Scholar Mode.
- [SciSpace][scispace] — Copilot reading assistant over 270M+ papers, 100+ languages.
- [Perplexity Academic][perplexity-academic] — academic deep research generating 100+ cited studies in minutes.
- [NotebookLM][notebooklm] — Gemini 3 research assistant with Deep Research, data tables, multimodal sources.
- [Web of Science Research Assistant][wos-research-assistant] — agentic reviews over the WoS Core Collection (institutional).
- [ResearchRabbit][researchrabbit] — free citation-network visualization + recommendations, Zotero integration.
- [Litmaps][litmaps] — interactive citation maps from Microsoft Academic Graph + Semantic Scholar.
- [PaSa][pasa] — RL-trained paper-search agent (AutoScholarQuery, 35K queries).
- [SciSummary][scisummary] / [Scholarcy][scholarcy] — academic summarization (flashcards / key-claim extraction).
- [Ai2 Scholar QA][ai2-scholar-qa] — Allen Institute research Q&A over scientific papers.

## 4. Research Support Frameworks

- [Paper2Agent][paper2agent] — converts a paper + codebase into an interactive **MCP-server agent** (auto-generated, test-refined); integrates with Claude Code. Cross-ref: [ai-security-governance-analysis.md § MCP Ecosystem Security](../sdlc-lcm/ai-security-governance-analysis.md#mcp-ecosystem-security) for MCP-server hardening.
- [PaperQA2][paperqa2] — superhuman scientific-literature RAG (beats PhD/postdoc on LitQA2); powers WikiCrow and ContraCrow ([paper][paperqa2-paper]).

## Mapping to the CC `/deep-research` Harness

Claude Code ships one bundled workflow, [`/deep-research`](../cc-native/agents-skills/CC-dynamic-workflows-analysis.md#bundled-workflow-deep-research): fan-out web searches across angles → fetch + cross-check sources → vote per claim → cited report (unsupported claims dropped). How the deep-research-style agents above relate to that pattern:

| Agent | Overlap with `/deep-research` | Beyond / gap vs the CC workflow | CC-based? |
|---|---|---|---|
| **local-deep-research** | Same fan-out → search → cross-check → cited-report loop | Local/offline LLMs, 20+ specialized sources (PubMed/arXiv/SearXNG), persistence + encryption | No (LangGraph; runs Claude as a model option) |
| **local-deep-researcher** | Same iterative search→summarize→reflect loop | Minimal LangGraph *reference* design; local-only by default; not a full assistant | No (LangGraph reference impl) |
| **dataroom** | Gathers + cross-checks sources into a structured package | Two-stage local-gather / frontier-synthesize split; Jina CLI tools; no CC tie-in | No (Pi + local LLM) |
| **AutoScientists** | Multi-agent fan-out + peer-critique ≈ cross-check/vote | Runs *experiments* (code/compute), not just literature; computational-science domain | **Yes** — built on CC subagents |
| **GPT-Researcher** | Multi-agent web+local research → cited long-form report | Self-hosted LangGraph with explicit planner/executor roles | No |
| **OpenAI Deep Research** | Agentic multi-step browse → cited analyst report | Hosted `o3`-tuned browsing model, RL-trained; API-gated, not local | No |
| **Gemini Deep Research** | Iterative plan → search → synthesize cited report | Gemini-3-Pro hosted, server-side background runs | No |
| **STORM / Co-STORM** | Multi-perspective fan-out → cited synthesis | Perspective-simulation step; tuned for Wikipedia-style articles | No |
| **FutureHouse / PaperQA2** | Retrieval + cross-check, citation-grounded | Scientific-literature RAG (not open web); benchmarked superhuman retrieval | No |

**Takeaway**: CC's `/deep-research` is a general open-web harness; the third-party agents specialize it — local/private (local-deep-research), scientific-corpus (PaperQA2/FutureHouse), or autonomous experimentation (AutoScientists, the one actually built on CC). AutoScientists is the clearest reference design for extending CC's harness toward long-running scientific work.

## Cross-References

- [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) — agent frameworks, orchestration, memory infrastructure
- [evaluation-data-resources-landscape.md](../sdlc-lcm/evaluation-data-resources-landscape.md) — evaluation frameworks, benchmarks, datasets
- [rxiv-agentic-papers.md](../research/rxiv-agentic-papers.md) — agentic-AI research papers (auto-generated pipeline)
- [CC-dynamic-workflows-analysis.md § Bundled Workflow: /deep-research](../cc-native/agents-skills/CC-dynamic-workflows-analysis.md#bundled-workflow-deep-research) — CC's first-party deep-research harness these agents map to

## Sources

| Source | Content |
|---|---|
| [DeepResearch (Alibaba-NLP)][deepresearch-alibaba] | Long-horizon information-seeking agent |
| [AI-Researcher (HKUDS)][ai-researcher] · [paper][ai-researcher-paper] | Literature→manuscript pipeline + Scientist-Bench |
| [AI Scientist v2 (Sakana AI)][ai-scientist-v2] · [paper][ai-scientist-v2-paper] | Agentic tree-search paper generation |
| [GPT-Researcher][gpt-researcher] | LangGraph multi-agent deep-research |
| [STORM / Co-STORM (Stanford)][storm] | Multi-perspective cited-article curation |
| [Agent Laboratory][agent-laboratory] | Human-in-the-loop research assistant |
| [MLR-Copilot][mlr-copilot] · [paper][mlr-copilot-paper] | Three-phase ML-research automation |
| [SciSciGPT][sciscigpt] | "Science of science" agent (capability-maturity model) |
| [autoresearch (Karpathy)][autoresearch] | Minimalist overnight ML research |
| [Kosmos (Edison Scientific)][kosmos] | Autonomous scientist (proprietary) |
| [Denario (AstroPilot-AI)][denario] | AG2 + LangGraph LaTeX-producing pipeline |
| [CMBAgent][cmbagent] | AG2 planning-and-control multi-agent system |
| [OpenAI Deep Research][openai-deep-research] | Agentic ChatGPT / `o3-deep-research` API |
| [Gemini Deep Research][gemini-deep-research] | Gemini 3 Pro long-horizon agent (Interactions API) |
| [AutoScientists (mims-harvard)][autoscientists] | Computational-science experiments via CC subagents |
| [local-deep-research (LearningCircuit)][local-deep-research] | LLM-agnostic deep-research assistant |
| [local-deep-researcher (langchain-ai)][local-deep-researcher] | Minimal LangGraph reference impl |
| [dataroom (hanxiao / Jina)][dataroom] | Local-gather / frontier-synthesize harness |
| [Perplexity Computer][perplexity-computer] · [paper][perplexity-computer-paper] | Autonomy/efficiency/scope study vs. Search |
| [Coscientist (CMU, Nature)][coscientist] | GPT-4 chemistry agent (cloud lab) |
| [ChemCrow][chemcrow] | GPT-4 + 18 chemistry tools |
| [BioPlanner][bioplanner] | Biology protocol generation (BIOPROT) |
| [BioChatter][biochatter] | Privacy-preserving biomedical conversational AI |
| [MatterGen (Microsoft)][mattergen] | Diffusion generative model for materials |
| [MatterSim (Microsoft)][mattersim] | Deep-learning atomistic simulator |
| [OpenScholar (Ai2/UW)][openscholar] · [paper][openscholar-paper] | Retrieval-augmented LM over open-access papers |
| [FutureHouse Platform][futurehouse] | Crow/Falcon/Owl literature-search agents |
| [Elicit][elicit] | Literature-matrix extraction |
| [Scite][scite] | Smart Citations classification |
| [Consensus][consensus] | Evidence-backed answers from scholarly consensus |
| [Undermind][undermind] | Adaptive "successive search" |
| [Semantic Scholar][semantic-scholar] · [API][semantic-scholar-api] | 200M+ paper semantic search + API |
| [Liner][liner] | AI research search with line-by-line citations |
| [SciSpace][scispace] | Copilot reading assistant over 270M+ papers |
| [Perplexity Academic][perplexity-academic] | Academic deep research |
| [NotebookLM][notebooklm] | Gemini research assistant with Deep Research |
| [Web of Science Research Assistant][wos-research-assistant] | Agentic reviews over WoS Core Collection |
| [ResearchRabbit][researchrabbit] | Citation-network visualization |
| [Litmaps][litmaps] | Interactive citation maps |
| [PaSa][pasa] | RL-trained paper-search agent |
| [SciSummary][scisummary] · [Scholarcy][scholarcy] | Academic summarization |
| [Ai2 Scholar QA][ai2-scholar-qa] | Allen Institute research Q&A |
| [Paper2Agent][paper2agent] | Paper+codebase → MCP-server agent |
| [PaperQA2][paperqa2] · [paper][paperqa2-paper] | Superhuman scientific-literature RAG |

[deepresearch-alibaba]: https://github.com/Alibaba-NLP/DeepResearch/
[ai-researcher]: https://github.com/HKUDS/AI-Researcher
[ai-researcher-paper]: https://arxiv.org/abs/2505.18705
[ai-scientist-v2]: https://github.com/SakanaAI/AI-Scientist-v2
[ai-scientist-v2-paper]: https://arxiv.org/abs/2504.08066
[gpt-researcher]: https://github.com/assafelovic/gpt-researcher
[storm]: https://github.com/stanford-oval/storm
[agent-laboratory]: https://github.com/SamuelSchmidgall/AgentLaboratory
[mlr-copilot]: https://github.com/du-nlp-lab/MLR-Copilot
[mlr-copilot-paper]: https://arxiv.org/abs/2408.14033
[sciscigpt]: https://arxiv.org/abs/2504.05559
[autoresearch]: https://github.com/karpathy/autoresearch
[kosmos]: https://edisonscientific.com/
[denario]: https://github.com/AstroPilot-AI/Denario
[cmbagent]: https://github.com/CMBAgents/cmbagent
[openai-deep-research]: https://openai.com/index/introducing-deep-research/
[gemini-deep-research]: https://blog.google/technology/developers/deep-research-agent-gemini-api/
[autoscientists]: https://github.com/mims-harvard/AutoScientists
[local-deep-research]: https://github.com/LearningCircuit/local-deep-research
[local-deep-researcher]: https://github.com/langchain-ai/local-deep-researcher
[dataroom]: https://github.com/hanxiao/dataroom
[perplexity-computer]: https://research.perplexity.ai/articles/how-ai-agents-reshape-knowledge-work
[perplexity-computer-paper]: https://arxiv.org/abs/2606.07489
[coscientist]: https://www.nature.com/articles/s41586-023-06792-0
[chemcrow]: https://arxiv.org/abs/2304.05376
[bioplanner]: https://arxiv.org/abs/2310.10632
[biochatter]: https://biochatter.org/
[mattergen]: https://github.com/microsoft/mattergen
[mattersim]: https://github.com/microsoft/mattersim
[openscholar]: https://github.com/AkariAsai/OpenScholar
[openscholar-paper]: https://arxiv.org/abs/2411.14199
[futurehouse]: https://www.futurehouse.org/research-announcements/launching-futurehouse-platform-ai-agents
[elicit]: https://elicit.com/
[scite]: https://scite.ai/
[consensus]: https://consensus.app/
[undermind]: https://www.undermind.ai/
[semantic-scholar]: https://www.semanticscholar.org/
[semantic-scholar-api]: https://api.semanticscholar.org/
[liner]: https://app.liner.com/
[scispace]: https://scispace.com/
[perplexity-academic]: https://www.perplexity.ai/academic
[notebooklm]: https://notebooklm.google/
[wos-research-assistant]: https://clarivate.com/academia-government/scientific-and-academic-research/research-discovery-and-referencing/web-of-science/web-of-science-research-assistant/
[researchrabbit]: https://researchrabbitapp.com/
[litmaps]: https://www.litmaps.com/
[pasa]: https://arxiv.org/abs/2501.10120
[scisummary]: https://scisummary.com/
[scholarcy]: https://www.scholarcy.com/article-summarizer
[ai2-scholar-qa]: https://qa.allen.ai/chat
[paper2agent]: https://arxiv.org/abs/2509.06917
[paperqa2]: https://github.com/Future-House/paper-qa
[paperqa2-paper]: https://arxiv.org/abs/2312.07559
