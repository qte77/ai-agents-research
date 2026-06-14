---
title: Research Agents & Discovery Platforms Landscape
purpose: Catalog of autonomous research agents, scientific-domain models, and literature discovery/analysis platforms for research automation — restored and refreshed from the archived research-agents landscape.
category: landscape
status: research
created: 2026-06-14
updated: 2026-06-14
validated_links: 2026-03-12
---

**Status**: Research (informational)

Survey of agents and platforms for autonomous scientific discovery, literature search, and paper analysis. Restored from `docs/archive/landscape-research-agents.md` (archived 2026-04-23) and trimmed to the durable catalog; project-specific integration notes were dropped. For agent *frameworks* and infrastructure see [agent-frameworks-infrastructure-landscape.md](../non-cc/agent-frameworks-infrastructure-landscape.md); for evaluation tooling see [CC-evaluation-data-resources-landscape.md](CC-evaluation-data-resources-landscape.md).

## 1. Autonomous Research Agents

Agents that conduct multi-step research and generate research outputs.

- [DeepResearch (Alibaba-NLP)](https://github.com/Alibaba-NLP/DeepResearch/) — 30.5B-param long-horizon information-seeking agent (3.3B active/token, 128K ctx); ReAct + "IterResearch Heavy" modes, on-policy RL. On HF/ModelScope/OpenRouter.
- [AI-Researcher (HKUDS)](https://github.com/HKUDS/AI-Researcher) — NeurIPS 2025 Spotlight; end-to-end literature→manuscript pipeline with a Writer Agent and the Scientist-Bench benchmark ([paper](https://arxiv.org/abs/2505.18705)).
- [The AI Scientist v2 (Sakana AI)](https://github.com/SakanaAI/AI-Scientist-v2) — produced the first peer-review-accepted fully-AI-generated workshop paper (Apr 2025); agentic tree-search + VLM feedback, ~$6–15/paper ([paper](https://arxiv.org/abs/2504.08066)).
- [GPT-Researcher](https://github.com/assafelovic/gpt-researcher) — LangGraph multi-agent deep web+local research producing cited long-form reports; STORM-inspired.
- [STORM / Co-STORM (Stanford)](https://github.com/stanford-oval/storm) — multi-perspective knowledge curation generating Wikipedia-style cited articles; 70K+ preview users, FreshWiki/WildSeek datasets.
- [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) — human-in-the-loop end-to-end research assistant (lit review → experiments → report).
- [MLR-Copilot](https://github.com/du-nlp-lab/MLR-Copilot) — three-phase ML-research automation (idea → implementation → execution) ([paper](https://arxiv.org/abs/2408.14033)).
- [SciSciGPT](https://arxiv.org/abs/2504.05559) — open-source "science of science" collaborator proposing an LLM-agent capability-maturity model.
- [autoresearch (Karpathy)](https://github.com/karpathy/autoresearch) — minimalist overnight ML research: agents edit one `train.py`, fixed 5-min GPU runs, single metric (val bits-per-byte), meta-programmed via `program.md`.
- [Kosmos (Edison Scientific)](https://edisonscientific.com/) — autonomous scientist using structured world models; claims ~6 months of PhD-equivalent work per run (proprietary).
- [Denario (AstroPilot-AI)](https://github.com/AstroPilot-AI/Denario) — AG2 + LangGraph multi-agent pipeline producing publication-ready LaTeX; uses CMBAgent as backend.
- [CMBAgent](https://github.com/CMBAgents/cmbagent) — AG2-based autonomous "Planning & Control" multi-agent system; 1st place, NeurIPS 2025 Fair Universe Competition.
- [OpenAI Deep Research](https://openai.com/index/introducing-deep-research/) — agentic ChatGPT capability; API as `o3-deep-research` ($10/$40 per MTok, 200K ctx, MCP connectors), led HLE at launch.
- [Gemini Deep Research](https://blog.google/technology/developers/deep-research-agent-gemini-api/) — Gemini 3 Pro long-horizon agent via the Interactions API (`deep-research-pro-preview-12-2025`); 46.4% HLE, 66.1% DeepSearchQA, background execution + remote MCP.

**Domain-specific science agents**: [Coscientist (CMU, Nature)](https://www.nature.com/articles/s41586-023-06792-0) — GPT-4 chemistry agent driving cloud-lab experiments; [ChemCrow](https://arxiv.org/abs/2304.05376) — GPT-4 + 18 chemistry tools; [BioPlanner](https://arxiv.org/abs/2310.10632) — biology protocol generation (BIOPROT, 9K+ protocols); [BioChatter](https://biochatter.org/) — privacy-preserving biomedical conversational-AI framework.

## 2. Specialized Scientific Models

- [MatterGen (Microsoft)](https://github.com/microsoft/mattergen) — diffusion generative model for inorganic-materials design with multi-property conditioning (CIF output).
- [MatterSim (Microsoft)](https://github.com/microsoft/mattersim) — M3GNet deep-learning atomistic simulator across elements/temperatures/pressures (1M and 5M variants).

## 3. Research Discovery & Analysis Platforms

Literature search, paper analysis, and discovery (assistive, not autonomous conductors).

- [OpenScholar (Ai2/UW)](https://github.com/AkariAsai/OpenScholar) — retrieval-augmented LM over 45M open-access papers; +5% correctness vs GPT-4o, far lower hallucination (Llama-3.1-8B fine-tune) ([paper](https://arxiv.org/abs/2411.14199)).
- [FutureHouse Platform](https://www.futurehouse.org/research-announcements/launching-futurehouse-platform-ai-agents) — Crow/Falcon/Owl agents with benchmarked superhuman literature search; built on PaperQA2.
- [Elicit](https://elicit.com/) — literature-matrix extraction, ~99.4% data-point accuracy in systematic reviews; 200M+ Semantic Scholar corpus.
- [Scite](https://scite.ai/) — Smart Citations classifying supporting/contrasting/mentioning references (1.3B+ citations).
- [Consensus](https://consensus.app/) — evidence-backed yes/no answers from scholarly consensus.
- [Undermind](https://www.undermind.ai/) — adaptive "successive search" claiming 10–50× over Google Scholar with completeness estimates.
- [Semantic Scholar](https://www.semanticscholar.org/) — 200M+ paper semantic search, embeddings, and [API](https://api.semanticscholar.org/) underpinning many tools here.
- [Liner](https://app.liner.com/) — AI research search over 200M+ sources with line-by-line citations and Scholar Mode.
- [SciSpace](https://scispace.com/) — Copilot reading assistant over 270M+ papers, 100+ languages.
- [Perplexity Academic](https://www.perplexity.ai/academic) — academic deep research generating 100+ cited studies in minutes.
- [NotebookLM](https://notebooklm.google/) — Gemini 3 research assistant with Deep Research, data tables, multimodal sources.
- [Web of Science Research Assistant](https://clarivate.com/academia-government/scientific-and-academic-research/research-discovery-and-referencing/web-of-science/web-of-science-research-assistant/) — agentic reviews over the WoS Core Collection (institutional).
- [ResearchRabbit](https://researchrabbitapp.com/) — free citation-network visualization + recommendations, Zotero integration.
- [Litmaps](https://www.litmaps.com/) — interactive citation maps from Microsoft Academic Graph + Semantic Scholar.
- [PaSa](https://arxiv.org/abs/2501.10120) — RL-trained paper-search agent (AutoScholarQuery, 35K queries).
- [SciSummary](https://scisummary.com/) / [Scholarcy](https://www.scholarcy.com/article-summarizer) — academic summarization (flashcards / key-claim extraction).
- [Ai2 Scholar QA](https://qa.allen.ai/chat) — Allen Institute research Q&A over scientific papers.

## 4. Research Support Frameworks

- [Paper2Agent](https://arxiv.org/abs/2509.06917) — converts a paper + codebase into an interactive **MCP-server agent** (auto-generated, test-refined); integrates with Claude Code. Cross-ref: [CC-ai-security-governance-analysis.md § MCP Ecosystem Security](CC-ai-security-governance-analysis.md#mcp-ecosystem-security) for MCP-server hardening.
- [PaperQA2](https://github.com/Future-House/paper-qa) — superhuman scientific-literature RAG (beats PhD/postdoc on LitQA2); powers WikiCrow and ContraCrow ([paper](https://arxiv.org/abs/2312.07559)).

## Cross-References

- [agent-frameworks-infrastructure-landscape.md](../non-cc/agent-frameworks-infrastructure-landscape.md) — agent frameworks, orchestration, memory infrastructure
- [CC-evaluation-data-resources-landscape.md](CC-evaluation-data-resources-landscape.md) — evaluation frameworks, benchmarks, datasets
- [rxiv-agentic-papers.md](../research/rxiv-agentic-papers.md) — agentic-AI research papers (auto-generated pipeline)
