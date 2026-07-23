---
title: Evaluation & Data Resources Landscape
purpose: Catalog of agent/LLM evaluation frameworks, agentic benchmarks, and evaluation datasets — the tools, benchmarks, and data behind the metrics defined in the evaluation-metrics landscape.
category: landscape
status: research
created: 2026-06-14
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Research (informational)

Catalog of the **tools, benchmarks, and datasets** for evaluating agents and LLMs — the companion to [agent-evaluation-metrics-landscape.md](agent-evaluation-metrics-landscape.md), which defines the *metrics* themselves. Folded in from `docs/archive/landscape-evaluation-data-resources.md` (archived 2026-04-23) and distilled; project-specific boilerplate dropped. Tool/benchmark facts are a **February–March 2026 snapshot** — verify before relying. Web-scraping, browser-automation, and enterprise-infrastructure sections from the source are out of scope here (see [CC-web-scraping-plugins-analysis.md](../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md) for scraping).

## Why This Catalog Exists: EDD as Methodology

The tools below serve **eval-driven development (EDD)** — evals authored *before* the agent capability they measure, then used as the iteration oracle. The term has **no single coiner** (see the provenance-uncertain framing in [agentic-engineering-disciplines-landscape.md §2](agentic-engineering-disciplines-landscape.md)); it is used in parallel by first parties and tool vendors: Anthropic's [Demystifying evals for AI agents][anthropic-evals] (2026-01-09) names the practice directly — "build evals to define planned capabilities before agents can fulfill them, then iterate", "owning and iterating on evaluations should be as routine as maintaining unit tests" — and frames eval-task definition as a stress-test of whether requirements are concrete enough to build. OpenAI's [evaluation best-practices guidance][openai-evals] recommends "adopting eval-driven development … evaluating early and often" and draws the BDD analogy (specify behavior before implementing). Vendors [Braintrust][braintrust-edd] and [DeepEval][deepeval-edd] each market the exact term ("define success early and build toward it … use the eval scores as your oracle"). Counterweight: [Hamel Husain's practitioner essay][husain-evals] cautions against blind eval-first — discover real failure modes, *then* encode them as evals. This section names the methodology; the disciplines landscape holds the full "-driven-development" stack.

## 1. Evaluation & Testing Frameworks

Observability-first platforms with strong eval features — **LangWatch, Evidently AI, Braintrust** — have full entries in [agent-observability-methods-analysis.md](../non-cc/agent-observability-methods-analysis.md); not duplicated here.

| Tool | Link | Focus | Notable |
|---|---|---|---|
| RAGAs | [github](https://github.com/explodinggradients/ragas) | RAG eval: context precision/recall, faithfulness | — |
| TruLens | [github](https://github.com/truera/trulens) | RAG Triad + agent feedback functions | — |
| DeepEval | [github](https://github.com/confident-ai/deepeval) | Pytest-like LLM testing, 30+ metrics | 30+ research-backed metrics |
| Confident AI | [site](https://www.confident-ai.com/) | Enterprise eval platform (DeepEval cloud) | 30+ judge metrics, HIPAA/SOC2 |
| Giskard | [site](https://www.giskard.ai/) | AI red-teaming / vulnerability detection | — |
| Patronus AI | [site](https://www.patronus.ai/) | Hallucination detection, custom evaluators | +18% vs OpenAI LLM-judges |
| Deepchecks | [docs](https://docs.deepchecks.com/) | OSS validation (tabular/NLP/CV) | — |
| HELM (Stanford) | [github](https://github.com/stanford-crfm/helm) | Holistic LLM evaluation | 16 scenarios, 7 metrics |
| MLflow LLM Evaluate | [docs](https://mlflow.org/docs/latest/genai/eval-monitor/index.html) | Eval with experiment tracking | — |
| AgentBench | [github](https://github.com/THUDM/AgentBench) | LLM-as-Agent across 8 environments | 8 environments |
| AutoGenBench | [github](https://github.com/microsoft/autogen/blob/0.2/samples/tools/autogenbench) | AutoGen agent eval, Docker isolation | — |
| LangChain AgentEvals | [github](https://github.com/langchain-ai/agentevals) | Trajectory / decision-sequence eval (LLM judge) | — |
| LangChain OpenEvals | [github](https://github.com/langchain-ai/openevals) | Prebuilt LLM-judge evaluators | — |
| Google ADK Evaluation | [docs](https://google.github.io/adk-docs/evaluate) | Tool-trajectory + ROUGE response scoring | — |
| Azure AI Evaluation SDK | [docs](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/agent-evaluate-sdk) | Programmatic Azure Foundry agent eval | Likert 1–5 |
| Strands Agents Evaluation | [docs](https://strandsagents.com/docs/user-guide/evals-sdk/quickstart/) | Multi-dimensional agent eval | — |
| Maxim AI | [site](https://www.getmaxim.ai/) | Simulation + eval + observability | — |
| Yupp.ai | [site](https://yupp.ai/) | Crowd-sourced model comparison | Bradley-Terry/VIBE, 500+ models |
| Every Eval Ever | [github](https://github.com/evaleval/every_eval_ever) | Community schema unifying Inspect AI/HELM/lm-evaluation-harness eval outputs into one JSON format | arXiv:2606.14516; backed by Hugging Face, U. Edinburgh, EleutherAI; MIT (code/dataset), paper CC BY 4.0 |

## 2. Benchmarks

**General & real-world agent**: [METR HCAST](https://evaluations.metr.org/) (pre-release autonomy; time-horizon, reward-hacking rate), [CLEAR](https://arxiv.org/abs/2511.14136) (Cost/Latency/Efficacy/Assurance/Reliability, ρ=0.83 production correlation), [τ-bench](https://sierra.ai/blog/benchmarking-ai-agents) & [τ²-bench](https://arxiv.org/abs/2506.07982) (simulated-user tool use), [AgentQuest](https://arxiv.org/abs/2404.06411), [AgentBoard](https://arxiv.org/abs/2401.13178), [TheAgentCompany](https://arxiv.org/abs/2412.14161), [Exgentic](https://www.exgentic.ai/) (IBM unified protocol; first open general-agent leaderboard, top 0.73 success @ $8.54/task).

**LLM**: [LiveBench](https://livebench.ai/) (contamination-free, monthly; 18 tasks, top models <70%).

**Web agent**: [WebArena](https://arxiv.org/abs/2307.13854), [BrowseComp](https://www.evidentlyai.com/blog/ai-agent-benchmarks) (1,266 multi-hop questions), [BrowserGym](https://arxiv.org/abs/2412.05467), [OSWorld](https://www.evidentlyai.com/blog/ai-agent-benchmarks) (desktop; best agents ~5%), [AppWorld](https://www.evidentlyai.com/blog/ai-agent-benchmarks).

**Code / SWE**: [SWE-EVO](https://arxiv.org/abs/2512.18470) (long-horizon multi-file evolution; 21% resolution vs 65% single-issue), [SciCode](https://arxiv.org/abs/2407.13168).

**Tool use & info-seeking**: [ToolLLM](https://arxiv.org/abs/2307.16789), [StableToolBench](https://github.com/THUNLP-MT/StableToolBench), [InfoDeepSeek](https://arxiv.org/abs/2505.15872).

**Scientific**: [CORE-Bench](https://arxiv.org/abs/2409.11363) (reproducibility), [BadScientist](https://openreview.net/forum?id=7MPstNz66e) (LLM-reviewer manipulation; 67–82% acceptance via 5 strategies).

**Memory**: [LongMemEval](https://github.com/xiaowu0162/LongMemEval) (long-history temporal reasoning), [Jenova long-context orchestration](https://www.jenova.ai/en/resources/jenova-ai-long-context-agentic-orchestration-benchmark-february-2026).

**Multi-agent**: [MultiAgentBench](https://arxiv.org/abs/2503.01935).

**Safety & security**: [SALAD-Bench](https://arxiv.org/abs/2402.05044), [Agent-SafetyBench](https://arxiv.org/abs/2412.14470), [AgentHarm](https://arxiv.org/abs/2410.09024), [WASP](https://arxiv.org/abs/2504.18575) (prompt-injection resilience).

**Multimodal/general**: [GAIA2](https://openreview.net/forum?id=9gw03JpKK4) (async environments, ~42% best pass@1).

**Leaderboards**: SciArena, Berkeley Function-Calling, Chatbot Arena, GAIA, WebDev Arena, MiniWoB++.

## 3. Datasets

| Dataset | Link | Content | Size |
|---|---|---|---|
| PeerRead | [github](https://github.com/allenai/PeerRead) | Paper drafts + expert peer reviews + decisions (JSONL) | 14K drafts, 10K+ reviews |
| SWIF2T | [arxiv](https://arxiv.org/abs/2405.20477) | Peer reviews citing scientific-paper weaknesses | 300 reviews |
| BigSurvey | [pdf](https://www.ijcai.org/proceedings/2022/0591.pdf) | Survey papers + referenced abstracts | 7K surveys, 430K abstracts |
| SciXGen | [arxiv](https://arxiv.org/abs/2110.10774) | Context-aware scientific text generation | 205K papers |
| scientific_papers | [hf](https://huggingface.co/datasets/armanc/scientific_papers) | Long structured arXiv/PubMed papers | 300K+ |
| FEVER | [site](https://fever.ai/dataset/fever.html) | Fact extraction & verification | 185.4K |
| LIAR | [zip](https://www.cs.ucsb.edu/~william/data/liar_dataset.zip) | Fake-news detection | 12.8K |
| X-Fact | [github](https://github.com/utahnlp/x-fact/) | Multilingual fact-checking | 31.1K |
| MultiFC | [site](https://www.copenlu.com/publication/2019_emnlp_augenstein/) | Multi-domain evidence-based fact checking | 34.9K |
| Plancraft | [arxiv](https://arxiv.org/abs/2412.21033) | Agent planning (text + multimodal) | — |
| IDAT | [arxiv](https://arxiv.org/abs/2407.08898) | Interactive task-solving agent eval | — |
| PDEBench | [github](https://github.com/pdebench/PDEBench) | SciML on partial differential equations | — |
| MatSci-NLP | [arxiv](https://arxiv.org/abs/2305.08264) | Materials-science NLP eval | — |
| StatLLM | [arxiv](https://arxiv.org/abs/2502.17657) | Statistical analysis + LLM SAS code, human scores | — |
| Trelis Function Calling | [hf](https://huggingface.co/datasets/Trelis/function_calling_v3) | Tool-use / function-invocation | — |
| KnowLM-Tool | [hf](https://huggingface.co/datasets/zjunlp/KnowLM-Tool) | Knowledge-grounded function invocation | — |
| awesome-reasoning | [github](https://github.com/neurallambda/awesome-reasoning) | Curated reasoning-dataset collection | — |

## Cross-References

- [agent-evaluation-metrics-landscape.md](agent-evaluation-metrics-landscape.md) — metric definitions these tools/benchmarks measure
- [agent-observability-methods-analysis.md](../non-cc/agent-observability-methods-analysis.md) — tracing/observability platforms (LangWatch, Evidently, Braintrust full entries)
- [research-agents-landscape.md](../non-cc/research-agents-landscape.md) — research/discovery agents
- [agent-frameworks-infrastructure-landscape.md](../non-cc/agent-frameworks-infrastructure-landscape.md) — agent frameworks & memory infrastructure

## Sources

Each framework, benchmark, and dataset links to its first-party page (repo / Hugging Face / arXiv) inline in the tables above. EDD-methodology sources:

[anthropic-evals]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
[openai-evals]: https://developers.openai.com/api/docs/guides/evaluation-best-practices
[braintrust-edd]: https://www.braintrust.dev/articles/eval-driven-development
[deepeval-edd]: https://deepeval.com/blog/eval-driven-development
[husain-evals]: https://hamel.dev/blog/posts/evals
