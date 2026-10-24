---
title: Evaluation & Data Resources Landscape
purpose: Catalog of agent/LLM evaluation frameworks, agentic benchmarks, and evaluation datasets — the tools, benchmarks, and data behind the metrics defined in the evaluation-metrics landscape.
category: landscape
status: research
created: 2026-06-14
updated: 2026-10-24
validated_links: 2026-10-24
---

Catalog of the **tools, benchmarks, and datasets** for evaluating agents and LLMs — the companion to [agent-evaluation-metrics-landscape.md](agent-evaluation-metrics-landscape.md), which defines the *metrics* themselves. Folded in from `docs/archive/landscape-evaluation-data-resources.md` (archived 2026-04-23) and distilled; project-specific boilerplate dropped. Tool/benchmark facts are a **February–March 2026 snapshot** — verify before relying. Web-scraping, browser-automation, and enterprise-infrastructure sections from the source are out of scope here (see [CC-web-scraping-plugins-analysis.md](../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md) for scraping).

## Why This Catalog Exists: EDD as Methodology

The tools below serve **eval-driven development (EDD)** — evals authored *before* the agent capability they measure, then used as the iteration oracle. The term has **no single coiner** (see the provenance-uncertain framing in [agentic-engineering-disciplines-landscape.md §2](agentic-engineering-disciplines-landscape.md)); it is used in parallel by first parties and tool vendors: Anthropic's [Demystifying evals for AI agents][anthropic-evals] (2026-01-09) names the practice directly — "build evals to define planned capabilities before agents can fulfill them, then iterate", "owning and iterating on evaluations should be as routine as maintaining unit tests" — and frames eval-task definition as a stress-test of whether requirements are concrete enough to build. OpenAI's [evaluation best-practices guidance][openai-evals] recommends "adopting eval-driven development … evaluating early and often" and draws the BDD analogy (specify behavior before implementing). Vendors [Braintrust][braintrust-edd] and [DeepEval][deepeval-edd] each market the exact term ("define success early and build toward it … use the eval scores as your oracle"). Counterweight: [Hamel Husain's practitioner essay][husain-evals] cautions against blind eval-first — discover real failure modes, *then* encode them as evals. This section names the methodology; the disciplines landscape holds the full "-driven-development" stack.

## 1. Evaluation & Testing Frameworks

Observability-first platforms with strong eval features — **LangWatch, Evidently AI, Braintrust** — have full entries in [agent-observability-methods-analysis.md](../non-cc/protocols/agent-observability-methods-analysis.md); not duplicated here.

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

**General & real-world agent**: [METR HCAST](https://evaluations.metr.org/) (pre-release autonomy; time-horizon, reward-hacking rate), [CLEAR](https://arxiv.org/abs/2511.14136) (Cost/Latency/Efficacy/Assurance/Reliability, ρ=0.83 production correlation), [τ-bench](https://sierra.ai/blog/benchmarking-ai-agents) & [τ²-bench](https://arxiv.org/abs/2506.07982) (simulated-user tool use), [AgentQuest](https://arxiv.org/abs/2404.06411), [AgentBoard](https://arxiv.org/abs/2401.13178), [TheAgentCompany](https://arxiv.org/abs/2412.14161), [Exgentic](https://www.exgentic.ai/) (IBM unified protocol; first open general-agent leaderboard, top 0.73 success @ $8.54/task), [E-Commerce Bench](https://github.com/QwenLM/E-CommerceBench) (Qwen; 18 LLM agents each run up to four simulated online stores for 365 days on real market data — negotiation, pricing, inventory, fraud detection; 6,886 products/576 suppliers; Apache-2.0; [arXiv:2608.30730](https://arxiv.org/abs/2608.30730)).

**Reward hacking (coding agents)**: [EvilGenie](https://arxiv.org/abs/2511.21654) (LiveCodeBench tasks where agents can hardcode tests or edit test files; detection via held-out tests, LLM judges and test-file edits; covers Claude Code, Codex, Gemini CLI). Context: [ai-security-governance-analysis.md § Reward Hacking](ai-security-governance-analysis.md#reward-hacking-and-evaluation-awareness-research).

**LLM**: [LiveBench](https://livebench.ai/) (contamination-free, monthly; 18 tasks, top models <70%).

**Web agent**: [WebArena](https://arxiv.org/abs/2307.13854), [BrowseComp](https://www.evidentlyai.com/blog/ai-agent-benchmarks) (1,266 multi-hop questions), [BrowserGym](https://arxiv.org/abs/2412.05467), [OSWorld](https://www.evidentlyai.com/blog/ai-agent-benchmarks) (desktop; best agents ~5%), [AppWorld](https://www.evidentlyai.com/blog/ai-agent-benchmarks).

**Code / SWE**: [SWE-EVO](https://arxiv.org/abs/2512.18470) (long-horizon multi-file evolution; 21% resolution vs 65% single-issue), [SciCode](https://arxiv.org/abs/2407.13168), [LoopArena](https://github.com/AMAP-ML/LoopArena) (models as runtime *Controllers* directing a fixed coding-agent *Worker* through long-running loops, vs. end-to-end outcome-only scoring; best observed Strict Success Rate 24.69% on full tasks, Apache-2.0; [arXiv:2608.28281](https://arxiv.org/abs/2608.28281)).

**Tool use & info-seeking**: [ToolLLM](https://arxiv.org/abs/2307.16789), [StableToolBench](https://github.com/THUNLP-MT/StableToolBench), [InfoDeepSeek](https://arxiv.org/abs/2505.15872).

**Scientific**: [CORE-Bench](https://arxiv.org/abs/2409.11363) (reproducibility), [BadScientist](https://openreview.net/forum?id=7MPstNz66e) (LLM-reviewer manipulation; 67–82% acceptance via 5 strategies).

**Memory**: [LongMemEval](https://github.com/xiaowu0162/LongMemEval) (long-history temporal reasoning), [Jenova long-context orchestration](https://www.jenova.ai/en/resources/jenova-ai-long-context-agentic-orchestration-benchmark-february-2026).

**Multi-agent**: [MultiAgentBench](https://arxiv.org/abs/2503.01935).

**Safety & security**: [SALAD-Bench](https://arxiv.org/abs/2402.05044), [Agent-SafetyBench](https://arxiv.org/abs/2412.14470), [AgentHarm](https://arxiv.org/abs/2410.09024), [WASP](https://arxiv.org/abs/2504.18575) (prompt-injection resilience).

**Multimodal/general**: [GAIA2](https://openreview.net/forum?id=9gw03JpKK4) (async environments, ~42% best pass@1).

**Domain: clinical speech-to-text (vendor-run)**: [Omi Health's medical STT benchmark][omi-bench]
scores speech-to-text accuracy and latency on medical speech, batch and realtime. It is not an agent
or clinical-reasoning benchmark, but it is the input layer for voice-driven clinical agents and
scribes. The page states "Omi-run evaluation. Same recordings and scorer for every model" on "1,513
English recordings, 7.2 hours" (edition "2026-10-18.1 (extends 2026-09-26.1)"), with metrics for
medical word error, drug-name errors and dose/unit matches. Omi's own model tops its own tables —
batch medical WER 0.87%, "Lowest among 19 tested APIs", and 1 drug-term error in 442, ahead of Voxtral
Small Transcribe 3 at 1.04% — and Omi sells that model as a hosted API ([home][omi-home]: "Start with 25
free hours"), so this is a vendor scoring itself. The page doesn't say where the 1,513 recordings come
from or whether they are released. The open scorer repo, [Omi-Health/medical-STT-eval][omi-repo] (MIT),
uses a different, public set — 57 PriMock57 consultations, "Reference transcripts derived from PriMock57
under CC BY 4.0" — and its own 42-model leaderboard (updated 2026-04-29) doesn't include Omi's model.
The page's own caveat: "Scores describe the tested configurations, not clinical safety; small
differences do not establish statistical significance." Checked 2026-10-22.

**Leaderboards**: SciArena, Berkeley Function-Calling, Chatbot Arena, GAIA, WebDev Arena, MiniWoB++.

**Agent-readiness scoring (websites/APIs)**: a new, two-vendor category — `git grep` for `ora.ai`,
`lightsage`, and "agent readiness"/"agent experience arena" across `docs/` returns zero hits before
this entry. [Ora][ora] (by era labs) scores how a website or MCP-server endpoint works for AI agents,
pairing a numeric score with a letter grade on its leaderboard (e.g. "96A+", "91A", "77B" — A+/A/B
observed, no C example seen); it self-styles "The standard for agent experience" and ships a CLI
(`npx ax audit <domain>`). Self-reported on its own [research page][ora-research], which runs off a
continuously-updating counter — re-checked twice in one day (2026-10-15) and already different each
time: as last observed, 119,906 sites scanned, an ecosystem-average score of 42/100 (the
score-distribution chart covers a 109,293-site subset of that total), and 5% of sites rated B or
above. Re-checked 2026-10-24: "127,521 sites scanned", "The ecosystem average sits at 43 out of 100",
"6% rank B or above" (chart subset 116,037). Treat the sites-scanned/subset figures as a moving snapshot,
not a fixed count. No pricing or
company
details (team, funding, founding date) appear on the homepage or research page checked; access is
waitlist-gated. [Lightsage][lightsage], "the Agent-Led Growth Platform for software companies," runs a
comparable **[Agent Experience Arena][lightsage-arena]** — self-reported, Lightsage's own methodology,
discovery-data snapshot dated 2026-06-13 — ranking 132 developer tools on a 50/50 blend of a
*discovery score* ("how often coding agents surface a tool when asked to solve tasks in its category")
and a *usability score* (averaged API/CLI/MCP integration results from Lightsage's companion
**[DevTool Arena][lightsage-devtool]**). Neither page states an exact prompt/run count behind the
discovery or usability scores, nor a founder, team, or funding for either vendor (Lightsage's legal
operator is named below) — these are a first,
not-yet-independently-audited example of the category; revisit as a standalone landscape if a third
vendor appears.

*DevTool Arena (re-checked 2026-10-22).* It now lives at devtoolarena.com, and Lightsage's
[terms][lightsage-terms] name the operator: "API-Rex, Inc., doing business as Lightsage" (last updated
October 13, 2026). Its [`llms.txt`][devtoolarena-llms] lists 11 boards across 7 agents: Claude Code and
Codex each have API, CLI and MCP boards; Muse, Gemini, Grok, Cursor and Kilo Code have API boards only.
The Claude Code API board shows 187 companies in 45 categories. Each board's intro names what it
compares (for API: "integration scores, documentation discoverability, tool calls, errors, cost, and
runtime"), but no board carries a date or a published method, and the site states no licence for the
data. A separate [discoverability view][devtoolarena-disc] "ranks developer APIs by whether coding agents
discover and recommend them for controlled benchmark prompts" (46 use cases, 5 prompts each, 19
agent/model columns; undated). Its [changelog][devtoolarena-changelog] is the only dated record: newest
entry October 21, 2026, and it logs scoring fixes (2 June: Nimble's Codex boards corrected "after
documentation/help text was counted as tool errors").

**Conflict of interest.** Lightsage sells to the companies it ranks: "Lightsage helps developer tools and
API companies get discovered, recommended, and used by AI coding agents" ([about][lightsage-about]), with
plans from $100 to $1,000 per month plus custom enterprise ([pricing][lightsage-pricing]), and the free
arena [submission form][devtoolarena-add] asks for "Company and contact details for follow-up." No page
says paying customers are ranked differently — this is an incentive to note, not evidence of
manipulation. Lightsage's name for the goal it sells is
"[Agent-Led Growth][lightsage-alg]" — "a go-to-market strategy for earning discovery, recommendation, and
successful product use through AI agents", split into discoverability, usability and analytics
(vendor framing; the page cites no data and names no author or date). Use the boards as leads to check,
not as evidence, and cite them rather than copying scores.

**Making a business agent-ready (checked 2026-10-24).** Scorers aside, what the platforms themselves
ask for is short:

- **No special markup for AI search.** Google: "There are no additional requirements to appear in AI
  Overviews or AI Mode, nor other special optimizations necessary", and "There's also no special
  schema.org structured data that you need to add" ([AI features][google-ai-features], updated
  2025-12-10). schema.org documents nothing agent-specific; an AI-agent representation proposal
  ([schemaorg#4786][schemaorg-4786]) is still open.
- **Natural-language endpoints over existing data.** [NLWeb][nlweb] (MIT; moved from `microsoft/NLWeb`
  to `nlweb-ai/NLWeb`; 6,259★; no releases or tags; last push 2026-08-11) turns a site's
  schema.org/RSS data into an `ask` endpoint: "It returns responses in JSON using Schema.org", and
  "Every NLWeb instance also acts as an MCP server (and soon A2A)". Microsoft announced it on
  2025-05-19, crediting R.V. Guha ([announcement][nlweb-announce]).
- **A connector agents can call.** Consumer marketplaces now ship MCP connectors: Checkatrade's
  Claude connector — "Find trusted local tradespeople and book fixed-price jobs — without leaving
  Claude" — is "Made by Checkatrade", Anthropic-verified, added July 2026, with tools
  `findTradespeopleV1` and `bookExpressJobV1` ([directory listing][checkatrade-connector]). Directory
  connectors are remote servers using OAuth 2.0 for authenticated services, with read-only/destructive
  hints on every tool; requirements and the MCP authorization model are in
  [agent-identity-auth-landscape.md § 2](agent-identity-auth-landscape.md#2-authorize-the-agent-on-behalf-of-a-human-delegated-scoped-auditable).

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
- [agent-observability-methods-analysis.md](../non-cc/protocols/agent-observability-methods-analysis.md) — tracing/observability platforms (LangWatch, Evidently, Braintrust full entries)
- [research-agents-landscape.md](../non-cc/knowledge-management/research-agents-landscape.md) — research/discovery agents
- [agent-frameworks-infrastructure-landscape.md](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md) — agent frameworks & memory infrastructure

## Sources

Each framework, benchmark, and dataset links to its first-party page (repo / Hugging Face / arXiv) inline in the tables above. Agent-readiness-scoring sources (checked 2026-10-15; DevTool Arena and Lightsage re-checked 2026-10-22):

[omi-bench]: https://omi.health/benchmark
[omi-home]: https://omi.health/
[omi-repo]: https://github.com/Omi-Health/medical-STT-eval
[ora]: https://ora.ai
[google-ai-features]: https://developers.google.com/search/docs/appearance/ai-features
[schemaorg-4786]: https://github.com/schemaorg/schemaorg/issues/4786
[nlweb]: https://github.com/nlweb-ai/NLWeb
[nlweb-announce]: https://news.microsoft.com/source/features/company-news/introducing-nlweb-bringing-conversational-interfaces-directly-to-the-web/
[checkatrade-connector]: https://claude.com/connectors/checkatrade
[ora-research]: https://ora.ai/research
[lightsage]: https://lightsage.com
[lightsage-arena]: https://lightsage.com/agent-experience-arena
[lightsage-devtool]: https://devtoolarena.com/claudecode/api
[lightsage-terms]: https://lightsage.com/terms
[lightsage-about]: https://lightsage.com/about
[lightsage-pricing]: https://lightsage.com/pricing
[lightsage-alg]: https://lightsage.com/resources/what-is-agent-led-growth
[devtoolarena-llms]: https://devtoolarena.com/llms.txt
[devtoolarena-disc]: https://devtoolarena.com/discoverability
[devtoolarena-changelog]: https://devtoolarena.com/changelog
[devtoolarena-add]: https://devtoolarena.com/add.md

EDD-methodology sources:

[anthropic-evals]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
[openai-evals]: https://developers.openai.com/api/docs/guides/evaluation-best-practices
[braintrust-edd]: https://www.braintrust.dev/articles/eval-driven-development
[deepeval-edd]: https://deepeval.com/blog/eval-driven-development
[husain-evals]: https://hamel.dev/blog/posts/evals
