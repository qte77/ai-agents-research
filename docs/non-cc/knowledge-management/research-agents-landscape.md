---
title: Research Agents & Discovery Platforms Landscape
purpose: Catalog of autonomous research agents, scientific-domain models and literature platforms for research automation, mapped to Claude Code's bundled /deep-research harness.
status: research
created: 2026-06-14
updated: 2026-11-26
validated_links_on: 2026-11-18
---

Survey of agents and platforms for autonomous scientific discovery, literature search, and paper analysis. Restored from `docs/archive/landscape-research-agents.md` (archived 2026-04-23) and trimmed to the durable catalog; project-specific integration notes were dropped. For agent *frameworks* and infrastructure see [agent-frameworks-infrastructure-landscape.md](../frameworks/agent-frameworks-infrastructure-landscape.md); for evaluation tooling see [evaluation-data-resources-landscape.md](../../sdlc-lcm/evaluation-data-resources-landscape.md).

## 1. Autonomous Research Agents

Agents that conduct multi-step research and generate research outputs.

- [DeepResearch (Alibaba-NLP)][deepresearch-alibaba] — 30.5B-param long-horizon information-seeking agent (3.3B active/token, 128K ctx); ReAct + "IterResearch Heavy" modes, on-policy RL. On HF/ModelScope/OpenRouter.
- [AI-Researcher (HKUDS)][ai-researcher] — NeurIPS 2025 Spotlight end-to-end literature→manuscript pipeline with a Writer Agent and the Scientist-Bench benchmark ([paper][ai-researcher-paper]); 5.9k stars, last push 2026-11-23 (`gh api` 2026-11-26).
- [The AI Scientist v2 (Sakana AI)][ai-scientist-v2] — produced the first peer-review-accepted fully-AI-generated workshop paper (Apr 2025); agentic tree-search + VLM feedback, ~$6–15/paper ([paper][ai-scientist-v2-paper]).
- [GPT-Researcher][gpt-researcher] — LangGraph multi-agent deep web+local research producing cited long-form reports; STORM-inspired.
- [STORM / Co-STORM (Stanford)][storm] — multi-perspective knowledge curation generating Wikipedia-style cited articles; 70K+ preview users, FreshWiki/WildSeek datasets; stale: 31.9k stars, last push 2025-09-30 (`gh api` 2026-11-22).
- [Agent Laboratory][agent-laboratory] — human-in-the-loop end-to-end research assistant (lit review → experiments → report); stale: 5.9k stars, last push 2025-08-20 (`gh api` 2026-11-22).
- [SciSciGPT][sciscigpt] — open-source "science of science" collaborator proposing an LLM-agent capability-maturity model.
- [autoresearch (Karpathy)][autoresearch] — minimalist overnight ML research: agents edit one `train.py`, fixed 5-min GPU runs, single metric (val bits-per-byte), meta-programmed via `program.md`.
- [Kosmos (Edison Scientific)][kosmos] — autonomous scientist using structured world models; claims ~6 months of PhD-equivalent work per run (proprietary).
- [Denario (AstroPilot-AI)][denario] — AG2 + LangGraph multi-agent pipeline producing publication-ready LaTeX; uses CMBAgent as backend.
- [CMBAgent][cmbagent] — AG2-based autonomous "Planning & Control" multi-agent system; 1st place, NeurIPS 2025 Fair Universe Competition.
- [OpenAI Deep Research][openai-deep-research] — agentic ChatGPT capability; API as `o3-deep-research` ($10/$40 per MTok, 200K ctx, MCP connectors; model shut down 2026-07-23 per OpenAI's model page, which points to its web research guide), led HLE at launch.
- [Gemini Deep Research][gemini-deep-research] — Gemini 3 Pro long-horizon agent via the Interactions API (current docs list agent IDs `deep-research-preview-04-2026` and `deep-research-max-preview-04-2026`; the earlier ID `deep-research-pro-preview-12-2025` is no longer listed); 46.4% HLE, 66.1% DeepSearchQA (launch-blog figures, Gemini 3 Pro era), background execution (`background=True` required) + remote Model Context Protocol (MCP) as a preview via the `mcp_server` tool type.
- [AutoScientists (mims-harvard)][autoscientists] — decentralized team of AI agents for long-running computational-science experiments, self-organizing around promising hypotheses; **packaged as Claude Code subagents** coordinating via a local ClawInstitute server (no central planner). BioML-Bench 74.4% mean leaderboard percentile (801★, Python; no licence metadata on GitHub, checked 2026-11-26) — the most direct CC-harness tie-in here.
- [IdeaScientist][ideascientist] — treats research ideation itself as an agentic task, split across three RL-trained roles (gap-finding, innovation, report-writing) that find limitations in related work, borrow solution ideas from analogous problems in other fields, and turn them into full research proposals; built on the **Svalbard Idea Vault**, a 2.77M-item corpus of decomposed research ideas used for retrieval/training/eval against a literature-cutoff date. On a Qwen3.6-27B backbone, the authors report besting the strongest open-source autoresearch baseline by 14.0% (mainly novelty) and outperforming "Claude Code SDK with Claude-4.8-Opus and Codex SDK with GPT-5.4" by up to 5.9% — both self-reported. arXiv:2610.04074, submitted 2026-10-02. The abstract page links no code, but the authors' repo [jiarui-liu/IdeaScientist](https://github.com/jiarui-liu/IdeaScientist) (366 stars, `gh api` 2026-11-26) ships the agent and links the Svalbard Idea Vault dataset on Hugging Face.
- [Hyperresearch (jordan-gibbs)][hyperresearch] — Claude Code skill (`/hyperresearch <query>`) running a tier-adaptive 16-step research pipeline: 250+ sources per `premier`-scale run, adversarial citation verification, syndication-independence auditing, and a persistent cross-session vault; the README now says its hosted version, Hyperresearch Deep, is #1 on the DRACO deep-research benchmark at 77.7 (10 tasks), a self-reported claim (an earlier README claim about the DeepResearch-Bench RACE leaderboard is no longer there). MIT, 5.1k★ (checked 2026-11-26).
- [OpenScience (Synthetic Sciences)][openscience] — open-source AI research workbench: plan → literature search → write/run code → run experiments → write up findings, with hundreds of bundled scientific skills (biology/chemistry/physics/ML/data engineering), ChEMBL/UniProt/PubMed/arXiv connectors, and desktop/browser/CLI interfaces; repo ships a `CLAUDE.md` and credits Claude Scientific Writer (K-Dense) among its skill sources. Apache-2.0, 4.4k★ (checked 2026-11-26).
- [Claude Science (Anthropic)][claude-science] — first-party desktop workbench, the same shape as OpenScience above: Claude runs Python/R/shell in a sandbox and saves "versioned artifacts with a full provenance record", with a reviewer that checks claims against the execution record. Beta. Full analysis: [CC-claude-science-analysis.md](../../cc-native/plugins-ecosystem/CC-claude-science-analysis.md).
- [ScientistTwo (Google Cloud AI Research)][scientisttwo] — autonomous end-to-end research system across six agent groups (Idea Generator → Evaluator → Analyzer → Writer → Peer-Review → Meta-Review); paper reports besting human baselines on 80.4% of 107 evaluated research problems (avg. +25.2% relative improvement) across 86 generated papers in eight AI domains, with 91.9%/72.1% acceptance under its ScholarPeer/Stanford-Agentic-Reviewer simulated reviewers ([paper][scientisttwo-paper]).
- [A Society of AI Scientists][society-ai-scientists] — Ahmad, Anderson, Qu et al. (alphaXiv lists MIT and Stanford among affiliations), first posted 2026-11-18 (v2 on 2026-11-19), CC BY 4.0, 46 authors per the alphaXiv BibTeX. Not to be confused with [A Society of Researchers](https://arxiv.org/abs/2610.10468) (arXiv 2610.10468, indexed in [rxiv-agentic-papers.md](../../research/rxiv-agentic-papers.md)). An exploratory twelve-week study of 936 autonomous agents from 35 human-operated labs working on a shared agent-only preprint server and messaging workspace. Authors' claims, none re-checked here: 936 studies with code and data, 9,500 messages across 229 agent-made chat rooms, agents publicly retracting their own mistaken claims, an agent-run "Journal of Agent Research", and agent-run reproducibility audits matching reported results. In blinded comparisons with recent human preprints, agent studies rated higher on experimental rigor and measured claims, human preprints higher on novelty and significance. The authors say they release the full archive (manuscripts, code, data, reviews, chat). **Provenance caveat:** only the alphaXiv page was readable; it shows no arXiv ID and an arXiv API search for the title returned nothing on 2026-11-20, so no arXiv URL is cited and the paper counts as a preprint on alphaXiv's host, not yet on arXiv. The study is a multi-agent social setting, unlike the single-pipeline systems above.
- [local-deep-research (LearningCircuit)][local-deep-research] — LLM-agnostic deep-research assistant: local (Ollama/LM Studio/llama.cpp) + cloud (Claude, OpenAI, Gemini, OpenRouter), LangGraph agent strategies, 20+ search sources (arXiv/PubMed/SearXNG/…), cited reports; 95.7% SimpleQA. MIT, 9.7k★, v2.0.4 (2026-11-24) (checked 2026-11-26) — a close OSS parallel to CC's [`/deep-research`](../../cc-native/agents-skills/CC-dynamic-workflows-analysis.md#bundled-workflow-deep-research).
- [local-deep-researcher (langchain-ai)][local-deep-researcher] — **distinct from the above** despite the near-identical name: LangChain's minimal LangGraph *reference* implementation of the search→summarize→reflect loop (Ollama/LMStudio, local-only by default) — the canonical starting pattern, not a full assistant. MIT, ~9.4k★ (checked 2026-11-26).
- [Épi: Towards a Persistent, Self-Improving Agent for Autonomous Research][epi] — Huang, Xu, Luo, Liu, Li, Wang, Song, Ramos, Xie, Isayev, Liang, Dziri, Sun, Gao, Liu, Sra, Zhang, Pentland & Chen (19 authors; arXiv:2610.24944, submitted 2026-10; affiliations not listed on the abstract page). An autonomous research agent that "sustains investigations across model sessions and evolves its methods through accumulated experience," combining **hierarchical memory**, persistent research history, branching, and independent review by a fixed verifier — the abstract gives no structural detail on the memory hierarchy itself. Evaluated on mathematical/research problems (numerical bounds, constructions, a computer-assisted proof) and, via its coding variant Épi-turbo, on FrontierOR operations-research tasks. Self-reported: 120 record-setting results (20 numerical-bound records across 12 families, 100 construction records across 8 families), an n-queens-constant interval ~84× narrower than prior work, a quartic Feigenbaum-attractor-dimension interval >3.6M× narrower, exact dual certificates ruling out a sharp Cohn-Elkies bound in dimensions 10–11, a computer-assisted proof of Tuza's conjecture for a restricted split-graph case, and Épi-turbo achieving "a 5.4% higher total benchmark score than Codex" on 30 FrontierOR tasks at 64% of its model cost (same underlying model/reasoning effort) (paper claims; methodology not independently verified; the agent's code is not released, but its results, constructions and certificates are in [BakeLab/Epi-results](https://github.com/BakeLab/Epi-results), checked with `gh api` 2026-11-22).
- [Perplexity Computer][perplexity-computer] — Perplexity's general-purpose autonomous agent orchestrator (launched Feb 2026, MCP tool/connector calls; follows 2025's Comet browser agent). HBS+Perplexity production-data study ([paper][perplexity-computer-paper], Feb 27–May 27, 2026; 10,000 matched query pairs drawn from a pool of 100,000 dual-product users, multiple pairs per user permitted) finds 26min of autonomous machine work per session vs. 33s for Search, 55% lower per-query dissatisfaction (1.3% vs. 2.9%), -87%/-94% time/cost vs. Search+human workflows (79–92%/87–96% across 18 occupational domains), and +38% knowledge-domain scope per query (2.40 vs. 1.74 domains).

**Domain-specific science agents**: [Coscientist (CMU, Nature)][coscientist] — GPT-4 chemistry agent driving cloud-lab experiments; [ChemCrow][chemcrow] — GPT-4 + 18 chemistry tools; [BioPlanner][bioplanner] — biology protocol generation (BIOPROT, 9K+ protocols); [BioChatter][biochatter] — privacy-preserving biomedical conversational-AI framework.

## 2. Specialized Scientific Models

- [MatterGen (Microsoft)][mattergen] — diffusion generative model for inorganic-materials design with multi-property conditioning (CIF output).
- [MatterSim (Microsoft)][mattersim] — M3GNet deep-learning atomistic simulator across elements/temperatures/pressures (1M and 5M variants).
- [Polaron][polaron] — "The intelligence layer for materials science": three models over microstructure images — Segmentation ("Identify and quantify the features that matter in microscopy data"), Reconstruction ("From 2D images to 3D volumes") and Design (explore "microstructural design scenarios"). Commercial; Imperial College spinout per [Imperial][polaron-imperial]. Use case: materials characterisation from microscopy, where MatterGen/MatterSim work from atomic structure.

## 3. Research Discovery & Analysis Platforms

Literature search, paper analysis, and discovery (assistive, not autonomous conductors).

- [OpenScholar (Ai2/UW)][openscholar] — retrieval-augmented LM over 45M open-access papers; +5% correctness vs GPT-4o, far lower hallucination (Llama-3.1-8B fine-tune) ([paper][openscholar-paper]); stale: 1.7k stars, last push 2025-08-13 (`gh api` 2026-11-22).
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

- [Paper2Agent][paper2agent] — converts a paper + codebase into an interactive **MCP-server agent** (auto-generated, test-refined); integrates with Claude Code. Cross-ref: [ai-security-governance-analysis.md § MCP Ecosystem Security](../../sdlc-lcm/ai-security-governance-analysis.md#mcp-ecosystem-security) for MCP-server hardening.
- [PaperQA2][paperqa2] — superhuman scientific-literature Retrieval-Augmented Generation (RAG) (beats PhD/postdoc on LitQA2); powers WikiCrow and ContraCrow ([paper][paperqa2-paper]).

## 5. Research Communities

Not tools: groups that coordinate work on a research use case.

- [AIDDA Institute][aidda] — "Institute for AI Driven Discovery of Algorithms": "Coordinating research, knowledge sharing, and networking around AI-driven algorithm discovery" through speaker events and working groups. Its site names AlphaEvolve, CodeEvolve, OpenEvolve and ShinkaEvolve; committee members include developers of CodeEvolve and OpenEvolve. Use case: AI-driven discovery of algorithms (an institute, not a tool).

## Mapping to the CC `/deep-research` Harness

Claude Code ships one bundled workflow, [`/deep-research`](../../cc-native/agents-skills/CC-dynamic-workflows-analysis.md#bundled-workflow-deep-research): fan-out web searches across angles → fetch + cross-check sources → vote per claim → cited report (unsupported claims dropped). How the deep-research-style agents above relate to that pattern:

| Agent | Overlap with `/deep-research` | Beyond / gap vs the CC workflow | CC-based? |
|---|---|---|---|
| **Hyperresearch** | Same fan-out → search → cross-check/cite-verify → cited-report loop, packaged as the CC skill itself | Tier-adaptive 16-step pipeline, 250+ sources/run, adversarial citation audit + syndication-independence check, persistent cross-session vault | **Yes** — is a CC skill (`/hyperresearch`) |
| **local-deep-research** | Same fan-out → search → cross-check → cited-report loop | Local/offline LLMs, 20+ specialized sources (PubMed/arXiv/SearXNG), persistence + encryption | No (LangGraph; runs Claude as a model option) |
| **local-deep-researcher** | Same iterative search→summarize→reflect loop | Minimal LangGraph *reference* design; local-only by default; not a full assistant | No (LangGraph reference impl) |
| **AutoScientists** | Multi-agent fan-out + peer-critique ≈ cross-check/vote | Runs *experiments* (code/compute), not just literature; computational-science domain | **Yes** — built on CC subagents |
| **GPT-Researcher** | Multi-agent web+local research → cited long-form report | Self-hosted LangGraph with explicit planner/executor roles | No |
| **OpenAI Deep Research** | Agentic multi-step browse → cited analyst report | Hosted `o3`-tuned browsing model, RL-trained; API model `o3-deep-research` shut down 2026-07-23; not local | No |
| **Gemini Deep Research** | Iterative plan → search → synthesize cited report | Gemini-3-Pro hosted, server-side background runs | No |
| **STORM / Co-STORM** | Multi-perspective fan-out → cited synthesis | Perspective-simulation step; tuned for Wikipedia-style articles | No |
| **FutureHouse / PaperQA2** | Retrieval + cross-check, citation-grounded | Scientific-literature RAG (not open web); benchmarked superhuman retrieval | No |

**Takeaway**: CC's `/deep-research` is a general open-web harness; the third-party agents specialize it — local/private (local-deep-research), scientific-corpus (PaperQA2/FutureHouse), or autonomous experimentation (AutoScientists). Two of these are actually built on CC: **Hyperresearch** packages a tier-adaptive, citation-audited deep-research pipeline directly as a CC skill — the closest like-for-like extension of the bundled harness — while **AutoScientists** extends the pattern into long-running computational-science experiments via CC subagents.

**Field evidence on agent search behaviour.** [Agentic Search in the Wild][agentic-search-wild] (Ning, Coelho et al., CMU and Lisbon; arXiv 2601.17617, accepted at SIGIR 2026) analyses 14.44M search requests in 3.97M sessions that external agent clients sent to the DeepResearchGym search API (June–December 2025). Nearly half (47.77%) of sessions are a single query. In fact-seeking ("Declarative") sessions, repeated queries rise to 42.68% by step 9, a candidate stall signal. A new metric, CTAR, finds that 54.35% of newly introduced query terms already appear in earlier retrieved evidence. The authors flag that the logs carry no success labels and no client-side prompts or memory, so these are behaviour patterns, not quality results. For a `/deep-research`-style loop they point at repetition-aware stopping and carrying evidence across steps. The anonymized logs are on [Hugging Face][agentic-search-logs] (CC-BY-4.0).

## Cross-References

- [agent-frameworks-infrastructure-landscape.md](../frameworks/agent-frameworks-infrastructure-landscape.md) — agent frameworks, orchestration, memory infrastructure
- [evaluation-data-resources-landscape.md](../../sdlc-lcm/evaluation-data-resources-landscape.md) — evaluation frameworks, benchmarks, datasets
- [rxiv-agentic-papers.md](../../research/rxiv-agentic-papers.md) — agentic-AI research papers (auto-generated pipeline)
- [CC-dynamic-workflows-analysis.md § Bundled Workflow: /deep-research](../../cc-native/agents-skills/CC-dynamic-workflows-analysis.md#bundled-workflow-deep-research) — CC's first-party deep-research harness these agents map to

## Not included

Entries removed under the [pruning rule](../../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (alive, adopted or proven; checked 2026-11-22), kept here so they are not re-added.

| Name | Reason | Date | Link |
|---|---|---|---|
| CEDAR (Sakana AI) | Paper only: no code or project link in the arXiv HTML or PDF (read 2026-11-22), and no CEDAR repo in Sakana AI's GitHub org; code appears only as appendix listings, so no released artifact (criterion 1). | 2026-11-22 | <https://arxiv.org/abs/2608.06871> |
| RankEvolve | Paper only: the HTML version says components "will be released" with a codebase but links none (read 2026-11-22), so no usable artifact (criterion 1). | 2026-11-22 | <https://arxiv.org/abs/2609.39551> |
| dataroom (hanxiao / Jina) | 194 stars (`gh api` 2026-11-22); its README's numbers measure the local model's inference tuning (draft acceptance, memory use), not a research benefit, and it names no independent users (criterion 3). | 2026-11-22 | <https://github.com/hanxiao/dataroom> |
| MLR-Copilot | 72 stars; last push 2025-03-30, outside 12 months (`gh api` 2026-11-22); no named independent users (criteria 2, 3). | 2026-11-22 | <https://github.com/du-nlp-lab/MLR-Copilot> |
| Open Coscientist (Jataware) | 70 stars; last push 2026-02-25; source-available (MIT + Commons Clause), community port of Google's AI co-scientist with no benchmark or named independent users (`gh api` 2026-11-22; criterion 3). Google's own description: <https://research.google/blog/accelerating-scientific-breakthroughs-with-an-ai-co-scientist/>. | 2026-11-22 | <https://github.com/jataware/open-coscientist> |

## Sources

| Source | Content |
|---|---|
| [DeepResearch (Alibaba-NLP)][deepresearch-alibaba] | Long-horizon information-seeking agent |
| [Agentic Search in the Wild (arXiv 2601.17617)][agentic-search-wild] · [logs][agentic-search-logs] | SIGIR 2026 log study of agent search sessions; CC-BY-4.0 dataset |
| [AI-Researcher (HKUDS)][ai-researcher] · [paper][ai-researcher-paper] | Literature→manuscript pipeline + Scientist-Bench |
| [AI Scientist v2 (Sakana AI)][ai-scientist-v2] · [paper][ai-scientist-v2-paper] | Agentic tree-search paper generation |
| [GPT-Researcher][gpt-researcher] | LangGraph multi-agent deep-research |
| [STORM / Co-STORM (Stanford)][storm] | Multi-perspective cited-article curation |
| [Agent Laboratory][agent-laboratory] | Human-in-the-loop research assistant |
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
| [A Society of AI Scientists][society-ai-scientists] | alphaXiv abstract page read 2026-11-20 (authors, abstract claims; no arXiv ID found) |
| [IdeaScientist][ideascientist] | RL-trained gap-finding/innovation/report-writing agent roles for research ideation |
| [Hyperresearch (jordan-gibbs)][hyperresearch] | CC skill: 16-step cited-report deep-research pipeline |
| [OpenScience (Synthetic Sciences)][openscience] | Open-source AI research workbench |
| [ScientistTwo (Google Cloud AI Research)][scientisttwo] · [paper][scientisttwo-paper] | Autonomous end-to-end research + self-peer-review system |
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
| [Claude Science (Anthropic)][claude-science] | First-party AI workbench for scientists |
| [Polaron][polaron] · [Imperial news][polaron-imperial] | Microstructure segmentation, 2D→3D reconstruction, design; Imperial spinout |
| [AIDDA Institute][aidda] | AI-driven algorithm discovery community |

[deepresearch-alibaba]: https://github.com/Alibaba-NLP/DeepResearch/
[ai-researcher]: https://github.com/HKUDS/AI-Researcher
[ai-researcher-paper]: https://arxiv.org/abs/2505.18705
[ai-scientist-v2]: https://github.com/SakanaAI/AI-Scientist-v2
[ai-scientist-v2-paper]: https://arxiv.org/abs/2504.08066
[gpt-researcher]: https://github.com/assafelovic/gpt-researcher
[storm]: https://github.com/stanford-oval/storm
[agent-laboratory]: https://github.com/SamuelSchmidgall/AgentLaboratory
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
[epi]: https://arxiv.org/abs/2610.24944
[ideascientist]: https://arxiv.org/abs/2610.04074
[society-ai-scientists]: https://www.alphaxiv.org/abs/2611.society-ai-scientists
[hyperresearch]: https://github.com/jordan-gibbs/hyperresearch
[openscience]: https://github.com/synthetic-sciences/openscience
[scientisttwo]: https://scientist-two.github.io
[scientisttwo-paper]: https://arxiv.org/abs/2609.19644
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
[claude-science]: https://claude.com/docs/claude-science/overview
[polaron]: https://polaron.ai/
[polaron-imperial]: https://www.imperial.ac.uk/news/250657/ai-spinout-polaron-accelerate-design-advanced/
[aidda]: https://algorithmdiscovery.org/
[agentic-search-wild]: https://arxiv.org/abs/2601.17617
[agentic-search-logs]: https://huggingface.co/datasets/cx-cmu/deepresearchgym-agentic-search-logs
