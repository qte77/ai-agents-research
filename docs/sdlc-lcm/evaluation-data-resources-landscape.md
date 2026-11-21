---
title: Evaluation & Data Resources Landscape
purpose: Catalog of agent/LLM evaluation frameworks, agentic benchmarks, and evaluation datasets — the tools, benchmarks, and data behind the metrics defined in the evaluation-metrics landscape.
status: research
created: 2026-06-14
updated: 2026-11-21
validated_links: 2026-11-18
---

Catalog of the **tools, benchmarks, and datasets** for evaluating agents and LLMs — the companion to [agent-evaluation-metrics-landscape.md](agent-evaluation-metrics-landscape.md), which defines the *metrics* themselves. Folded in from `docs/archive/landscape-evaluation-data-resources.md` (archived 2026-04-23) and distilled; project-specific boilerplate dropped. Tool/benchmark facts are a **February–March 2026 snapshot** — verify before relying. Web-scraping, browser-automation, and enterprise-infrastructure sections from the source are out of scope here (see [CC-web-scraping-plugins-analysis.md](../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md) for scraping).

## Why This Catalog Exists: EDD as Methodology

The tools below serve **eval-driven development (EDD)** — evals authored *before* the agent capability they measure, then used as the iteration oracle. The term has **no single coiner** (see the provenance-uncertain framing in [agentic-engineering-disciplines-landscape.md §2](agentic-engineering-disciplines-landscape.md)); it is used in parallel by first parties and tool vendors: Anthropic's [Demystifying evals for AI agents][anthropic-evals] (2026-01-09) names the practice directly — "build evals to define planned capabilities before agents can fulfill them, then iterate", "owning and iterating on evaluations should be as routine as maintaining unit tests" — and frames eval-task definition as a stress-test of whether requirements are concrete enough to build. OpenAI's [evaluation best-practices guidance][openai-evals] recommends "adopting eval-driven development … evaluating early and often" and draws the BDD analogy (specify behavior before implementing). Vendors [Braintrust][braintrust-edd] and [DeepEval][deepeval-edd] each market the exact term ("define success early and build toward it … use the eval scores as your oracle"). Counterweight: [Hamel Husain's practitioner essay][husain-evals] cautions against blind eval-first — discover real failure modes, *then* encode them as evals. This section names the methodology; the disciplines landscape holds the full "-driven-development" stack.

### Operationalizing EDD: `/claude-api build-eval` and `/claude-api hillclimb`

claude.dev — Anthropic's own developer blog, though the post itself never states the publisher by name;
it links `anthropics/skills` and an Anthropic engineering post, which is the only signal tying it to
Anthropic (same hedge this corpus already applies to claude.dev in
[CC-mods-function-hooks-analysis.md][mods-claudedev]) — published "Automating eval design and
hillclimbing with Claude" (Lance Martin, 2026-09-28), which gives the `claude-api` skill two commands
that operationalize the EDD loop above inside Claude Code itself ([source][claude-api-hillclimb]):

- **`/claude-api build-eval`**: "Claude interviews you, builds the eval inside your codebase, and pauses
  for approval at specific points." It samples inputs in order (production transcripts, bug
  reports/tickets, 5–10 hand-written cases, then codebase-synthesized cases), proposes the cheapest
  grader that fits (programmatic or LLM-as-judge), runs a baseline with a confidence interval, and checks
  grader consistency (does the verdict change on a repeat run of the same output) and noise (timeouts,
  API errors), warning if the baseline is already ~95%+.
- **`/claude-api hillclimb`**: iterates against a built eval. Claude "splits the evaluation set at random
  into test and train," then each round "reads the previous round's train transcripts and proposes one
  change as a patch" to an editable surface the user picks (system prompt, skills, tool descriptions,
  model/effort, harness code). If train improves but test is flat, Claude suspects overfitting and
  reverts; a regression also reverts; only a patch that improves both is kept. The workflow "leaves your
  code at the version that did best on the test set."

**Self-reported result**: Anthropic ran this on its own `claude-api` skill, starting from a 66.1% eval
score and reaching 87.9% (Figure 9 in the post) through intermediate checkpoints reported in the text as
74%, 77%, 80%, and ~88%.

## 1. Evaluation & Testing Frameworks

Observability-first platforms with strong eval features — **LangWatch, Evidently AI, Braintrust** — have full entries in [agent-observability-methods-analysis.md](../non-cc/protocols/agent-observability-methods-analysis.md); not duplicated here.

| Tool | Link | Focus | Notable |
|---|---|---|---|
| RAGAs | [github](https://github.com/vibrantlabsai/ragas) | Retrieval-Augmented Generation (RAG) eval: context precision/recall, faithfulness | — |
| TruLens | [github](https://github.com/truera/trulens) | RAG Triad + agent feedback functions | — |
| DeepEval | [github](https://github.com/confident-ai/deepeval) | Pytest-like LLM testing, 30+ metrics | 30+ research-backed metrics |
| Confident AI | [site](https://www.confident-ai.com/) | Enterprise eval platform (DeepEval cloud) | 30+ judge metrics, HIPAA/SOC2 |
| Giskard | [site](https://www.giskard.ai/) | AI red-teaming / vulnerability detection | — |
| Patronus AI | [site](https://www.patronus.ai/) | Hallucination detection, custom evaluators | +18% vs OpenAI LLM-judges |
| Deepchecks | [docs](https://docs.deepchecks.com/) | OSS validation (tabular/NLP/CV) | — |
| Inspect AI | [repo](https://github.com/UKGovernmentBEIS/inspect_ai) | UK AISI / Meridian Labs eval framework: datasets, agents, scorers, sandboxes; epochs with `pass_at_k` / `pass_k` reducers (see [methods](agent-evaluation-metrics-landscape.md#harness-inspect-ai)) | 200+ pre-built evals (docs); MIT |
| LiteLLM `agent_eval` | [blog](https://docs.litellm.ai/blog/agent-evaluations) | Compares harness-and-model targets (tool loop, Claude Code, Codex) on your own typed tasks; pass rate, cost, duration. Preview: not in published PyPI releases as of the 2026-11-16 post (see [routers landscape](../non-cc/infrastructure/llm-routers-gateways-landscape.md)) | MIT core (per that landscape) |
| HELM (Stanford) | [github](https://github.com/stanford-crfm/helm) | Holistic LLM evaluation | 16 scenarios, 7 metrics |
| MLflow LLM Evaluate | [docs](https://mlflow.org/docs/latest/genai/eval-monitor/index.html) | Eval with experiment tracking | — |
| AgentBench | [github](https://github.com/THUDM/AgentBench) | LLM-as-Agent across 8 environments | 8 environments |
| AutoGenBench | [github](https://github.com/microsoft/autogen/blob/0.2/samples/tools/autogenbench) | AutoGen agent eval, Docker isolation | — |
| LangChain AgentEvals | [github](https://github.com/langchain-ai/agentevals) | Trajectory / decision-sequence eval (LLM judge) | — |
| LangChain OpenEvals | [github](https://github.com/langchain-ai/openevals) | Prebuilt LLM-judge evaluators | — |
| Google ADK Evaluation | [docs](https://google.github.io/adk-docs/evaluate) | Tool-trajectory + Recall-Oriented Understudy for Gisting Evaluation (ROUGE) response scoring | — |
| Azure AI Evaluation SDK | [docs](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/agent-evaluate-sdk) | Programmatic Azure Foundry agent eval | Likert 1–5 |
| Strands Agents Evaluation | [docs](https://strandsagents.com/docs/user-guide/evals-sdk/quickstart/) | Multi-dimensional agent eval | — |
| Maxim AI | [site](https://www.getmaxim.ai/) | Simulation + eval + observability | — |
| Yupp.ai | [site](https://yupp.ai/) | Crowd-sourced model comparison | Bradley-Terry/VIBE, 500+ models |
| Every Eval Ever | [github](https://github.com/evaleval/every_eval_ever) | Community schema unifying Inspect AI/HELM/lm-evaluation-harness eval outputs into one JSON format | arXiv:2606.14516; backed by Hugging Face, U. Edinburgh, EleutherAI; MIT (code/dataset), paper CC BY 4.0 |

## 2. Benchmarks

**General & real-world agent**: [METR HCAST](https://evaluations.metr.org/) (pre-release autonomy; time-horizon, reward-hacking rate), [CLEAR](https://arxiv.org/abs/2511.14136) (Cost/Latency/Efficacy/Assurance/Reliability, ρ=0.83 production correlation vs 0.41 for accuracy-only, expert study N=15; abstract, v1 2025-11-18), [τ-bench](https://sierra.ai/blog/benchmarking-ai-agents) & [τ²-bench](https://arxiv.org/abs/2506.07982) (simulated-user tool use), [AgentQuest](https://arxiv.org/abs/2404.06411), [AgentBoard](https://arxiv.org/abs/2401.13178), [TheAgentCompany](https://arxiv.org/abs/2412.14161), [Exgentic](https://www.exgentic.ai/) (IBM unified protocol; open general-agent leaderboard; [General Agent Evaluation](https://arxiv.org/abs/2602.22953), 2026-02-26, v2 2026-05-11, is the paper behind it; its abstract does not state the "top 0.73 success @ $8.54/task" figure quoted in [agent-evaluation-metrics-landscape.md](agent-evaluation-metrics-landscape.md), so treat that figure as paper-body-reported and unverified here — the site's `results.csv` lists per-benchmark scores with no date column, e.g. 0.88 on TauBench-Telecom for Smolagent + gemini-3-pro), [E-Commerce Bench](https://github.com/QwenLM/E-CommerceBench) (Qwen; 18 LLM agents each run up to four simulated online stores for 365 days on real market data — negotiation, pricing, inventory, fraud detection; 6,886 products/576 suppliers; Apache-2.0; [arXiv:2608.30730](https://arxiv.org/abs/2608.30730)), [LifeVal](https://arxiv.org/abs/2611.06687) (Yang, Proehl, Bharadwaj, Fan, Cole, Kim, Brown, Thacker, Glaese, Patwardhan; Nov 2026 — 148 personalized agentic consumer-task categories, derived from a >3,800-respondent willingness-to-pay survey cross-checked against two national time-use studies; each task is written from real conversation histories/reference files by an expertise-gated creator and passed through 3+ rounds of human QC; no code link on the abstract page), [MiniCorp](https://arxiv.org/abs/2610.05912) (Zeng, Dai, Li, Shin, Zhang, Lu, He, Wang, Chang; Oct 2026 — an office simulator where agents collectively run an e-commerce company: external market mechanics plus an internal world where agent decisions feed back into market outcomes, with checkpointing for replay under counterfactual decisions; no code link on the abstract page).

**Reward hacking (coding agents)**: [EvilGenie](https://arxiv.org/abs/2511.21654) (LiveCodeBench tasks where agents can hardcode tests or edit test files; detection via held-out tests, LLM judges and test-file edits; covers Claude Code, Codex, Gemini CLI). Context: [ai-security-governance-analysis.md § Reward Hacking](ai-security-governance-analysis.md#reward-hacking-and-evaluation-awareness-research).

**LLM**: [LiveBench](https://livebench.ai/) (self-described contamination-free, with a LiveBench 2.0 edition per its page title; the earlier "18 tasks, top models <70%" figure is undated and was not re-sourced on 2026-11-18).

**Web agent** (dated browser benchmarks: [browser-agents-landscape.md](../non-cc/agents/browser-agents-landscape.md#browser-benchmarks-with-dates)): [WebArena](https://arxiv.org/abs/2307.13854), [BrowseComp](https://www.evidentlyai.com/blog/ai-agent-benchmarks) (1,266 multi-hop questions), [BrowserGym](https://arxiv.org/abs/2412.05467), [OSWorld][osworld-paper] (desktop; the 2024 paper reports humans above 72.36% against 12.24% for the best model then, as of 2024-04-11; OSWorld 2.0 reports 20.6% best binary completion in the paper, as of v2 2026-07-13, and a higher site-file figure — see Benchmark status and validity below), [AppWorld](https://www.evidentlyai.com/blog/ai-agent-benchmarks).

**Code / SWE**: [SWE-EVO](https://arxiv.org/abs/2512.18470) (long-horizon multi-file evolution: 48 tasks from seven Python projects; its abstract (v6, 2026-05-22) reports GPT-5.4 + OpenHands at "only 25%" against 72.80% for GPT-5.2 on SWE-bench Verified; the earlier "21% vs 65%" pair is not in that abstract), [SciCode](https://arxiv.org/abs/2407.13168), [LoopArena](https://github.com/AMAP-ML/LoopArena) (models as runtime *Controllers* directing a fixed coding-agent *Worker* through long-running loops, vs. end-to-end outcome-only scoring; best observed Strict Success Rate 36.25% on full tasks per the abstract (v2, 2026-10-13), Apache-2.0; [arXiv:2608.28281](https://arxiv.org/abs/2608.28281)).

**Harness-level vs model-level coding-agent comparators** (checked 2026-11-12): [SWE-bench / SWE-bench Verified][swe-bench] is harness-level — leaderboard entries are submitted per agent run; the official [SWE-bench/experiments][swe-bench-experiments] record names each submission folder `<date>_<model>`; its own examples (e.g. `20240402_sweagent_gpt4`) fold a scaffold label into that token, which is this entry's evidence for calling the comparator harness-level (the site itself does not state an "agent+model" field structure). Maintained by the SWE-bench project (its README lists contacts with Princeton and Stanford email domains), MIT licence (`SWE-bench/SWE-bench`, confirmed via `gh api`). The original SWE-bench draws "2,294 task instances" from Pull Requests and Issues across 12 Python repos; **SWE-bench Verified** is "a human-validated subset of 500 SWE-bench instances," created "in collaboration with OpenAI." Submissions go through [sb-cli][sb-cli], "a command-line tool for interacting with the SWE-bench API." [Terminal-Bench][terminal-bench] is harness-level — its leaderboard lists Rank/Model/**Agent**/Resolution Rate/Cost/Tokens per row; Apache-2.0 code at [harbor-framework/terminal-bench][tbench-repo] (confirmed via `gh api`). Its README calls it "a continuous benchmark" with "tagged releases" published "on the Harbor Hub," and says it "is hosted by Harbor and Laude Institute" — the live leaderboard page's own footer additionally credits Stanford ("Hosted by Stanford / Harbor / Laude Institute"), a discrepancy between the two first-party sources, stated here as each source states it. The live board is now on Terminal-Bench 4.1 (checked 2026-11-12), one minor version ahead of the Terminal-Bench 4.0 edition (re-read 2026-11-18: header still 4.1) [Artificial Analysis's Coding Agent Index](agent-evaluation-metrics-landscape.md#cost-performance-efficiency-pareto) scores against. [Scale SWE-bench Pro][scale-swe-pro] leans model-level: Scale AI's [paper][scale-swe-pro-paper] frames the evaluation as running "under a unified scaffold," but the public leaderboard's own legend tags only asterisked rows "Run with mini-swe-agent harness," while its narrative separately says frontier models ran under "the SWE-Agent scaffold" — not one disclosed harness across every row. The board separates results run with "a capped cost limit and turn limit of 50" (now linked off to a page named `..._deprecated`) from current results run with "an uncapped cost and ... a turn limit of 250," without stating the two groups are directly comparable — that comparability caveat does not appear on either page checked. The code repo, [scaleapi/SWE-bench_Pro-os][scale-swe-pro-repo], is MIT (confirmed via `gh api`); the paired Hugging Face dataset's licence is not stated on the paper page and was not separately checked. By contrast, [Epoch AI's SWE-bench Verified page][epoch-swebv] is not scaffold-free (correcting an initial assumption that it was): it runs its own default tool-calling scaffold — "a simple loop where models can take an individual action (e.g. reasoning and tool call)" — plus named third-party scaffolds including Claude Code and Codex, over "484 samples that are validated on [Epoch's] infrastructure" out of the 500-instance Verified set, and Epoch states site-wide that its data is under CC BY 4.0 ("All data is freely available under CC BY 4.0", [epoch.ai/llms.txt][epoch-llms]; benchmark questions and answers stay "the property of their respective creators", [data hub][epoch-data]).

**Benchmark upkeep**: [Benchmarks as Software][tb-maintenance] (Buchanan et al., Stanford and Cornell, arXiv 2611.08417) audited Terminal-Bench 2.0, found "issues in roughly 30% of the benchmark", and released the repairs as [Terminal-Bench 2.1][tb21] (Apache-2.0); accuracy rose by over 10 points and ranks moved by up to three, with Claude Code + Opus 4.6 gaining the most. The live board tracked below is a later version.

**Benchmark status and validity** (checked 2026-11-18). A companion table keyed by benchmark rather than extra columns on the prose lists above, which are too wide for them. Cells state what the cited source says unless marked "our reading"; "Not stated" means the source says nothing on that point. Every score carries the date of the version it was read from, and live leaderboards that render client-side were not read.

| Benchmark | Reported best score (source) | Contamination | Successor or repair | As-of and source |
| --- | --- | --- | --- | --- |
| OSWorld | 12.24% best model vs humans above 72.36% (2024 paper); on OSWorld 2.0 the site's results file (reported updatedAt 2026-11-14) lists Claude Opus 5 at 44.33% binary on the full set as the best official end-to-end row | Not stated | [OSWorld-Verified][osworld-site] (announced 2025-07-28, fixed examples); [OSWorld 2.0][osworld2] (108 long-horizon workflows). Our reading: Verified and 2.0 differ in task design, so they are not one trend. Dated score table, vendor claims and open models: [computer-use-agents-landscape.md](../non-cc/agents/computer-use-agents-landscape.md#the-osworld-family) | 2024-04-11 paper; 2.0 results file read 2026-11-19 |
| SWE-bench Verified | 72.80% for GPT-5.2, quoted in the SWE-EVO abstract (a third-party paper's figure, not the leaderboard) | Not stated in the sources read | Dataset-quality assessor [ExLabel / SWE-TQ][exlabel]; other comparators: SWE-EVO (above), [SWE-bench Pro][scale-swe-pro] | SWE-EVO v6 2026-05-22 |
| Terminal-Bench | Not stated | Not stated | 2.0 → [2.1][tb21] after an audit found issues in roughly 30% of the benchmark (the 2.1 repo records 26 modified tasks); leaderboard header reads 4.1 | Paper 2026-11-05; leaderboard header read 2026-11-18 |
| LiveCodeBench | Not stated | Time-windowed problems; see [mas-benchmarking-best-practices.md § 3.1](mas-benchmarking-best-practices.md) | Rolling new problems | arXiv v2 2024-06-06 |
| CyberGym | See [mas-benchmarking-best-practices.md](mas-benchmarking-best-practices.md) (CyberGym entry) | Not stated | Vendor claim of 88.45% (MDASH) is separate and unaudited; see [agentic-ai-vulnerability-landscape.md](agentic-ai-vulnerability-landscape.md) | Abstract revised 2026-03-24 |
| Cybench | Not stated | Not stated | None in the sources read | v4 2025-04-12 |

**Validity audits.** Findings from benchmark audits, each read on its arXiv page. The checklist method itself (ABC, [arXiv 2507.02825][abc]) is already summarised in [mas-benchmarking-best-practices.md](mas-benchmarking-best-practices.md); not repeated here.

| Audit | What it checked | Finding (as stated in the abstract) | Date |
| --- | --- | --- | --- |
| [ABC][abc] | Task setup and reward design in agentic benchmarks | Flaws can mis-estimate performance by "up to 100% in relative terms"; applied to CVE-Bench it cut overestimation by 33% | v5 2025-08-07 |
| [Benchmarks as Software][tb-maintenance] | Terminal-Bench 2.0 | Problems in roughly 30% of the benchmark; repairs raised accuracy by over 10 points; ranks moved by up to three (Spearman 0.958) | 2026-11-05 |
| [ExLabel][exlabel] (Jiang et al.) | Task clarity and test coverage in SWE-bench-style datasets | An LLM assistant with an evolving experience bank reports the best F1 across all settings on its eight-language SWE-TQ benchmark, against the best baseline; a model trained on filtered data resolves 66.2% of SWE-bench Verified | 2026-10-29 |
| [TRACE][trace] (Gaonkar) | Verifier brittleness | Renaming tools or reformatting output mostly left rewards near unchanged; misleading tool names lowered them; identical reruns flipped 15-36% of outcomes | 2026-10-08 |
| [Agents Are Systems][agent-systems] (Wiedmann et al.) | Configuration effects on four scientific tasks | About 54% of outcome variance came from repeating the same configuration; task information had the largest effect | 2026-10-01 |

**Saturation-resistant design.** [SqueezeBench][squeeze] (Manrique, Xia, Szeider, 2026-10-09) avoids saturation by scoring bounds on integer functions: a submission must beat a recorded bound and carry a Lean-checked proof, then replaces the record. Ten extremal-combinatorics problems; agents produced 82 accepted record-improving submissions in the baseline round and 60 more with newer models.

**Contamination detection and mitigation.** The corpus holds the principle ([mas-benchmarking-best-practices.md § 3.1](mas-benchmarking-best-practices.md): dynamic benchmarks and a private test subset); this adds sources. [A survey of benchmark data contamination][contam-survey] (Xu et al., 2024-06-06) reviews the problem; its abstract emphasises mitigation and alternative evaluation rather than detection methods, so it is not cited here for any detection technique. Methods below are read at their arXiv abstract pages (2026-11-18); all are paper-reported results, none independently reproduced here, and none of the abstracts states a limit.

- **Time-based avoidance:** [LiveCodeBench][lcb] (2024) avoids rather than detects contamination; see [mas-benchmarking-best-practices.md § 3.1](mas-benchmarking-best-practices.md).
- **Membership inference, Min-K% Prob:** [Shi et al.][mink] (2023-10-25) test whether a black-box model saw a given text, using the WIKIMIA benchmark of pre- and post-training data; the method needs no corpus knowledge or reference model and reports a 7.4% gain on WIKIMIA over prior methods (paper date).
- **Guided prompting:** [Golchin and Surdeanu][timetravel] (2023-08-16) prompt the model to complete a partial benchmark instance, then score partitions with ROUGE-L, BLEURT or a GPT-4 classifier; they report 92% to 100% accuracy against human experts on seven datasets and flag GPT-4 as contaminated on AG News, WNLI and XSum (paper date).
- **Performance-based, ConStat:** [Dekoninck et al.][constat] (2024-05-25) define contamination as inflated performance that does not carry over to rephrased, synthetic or related benchmarks, and test it statistically against reference models; the abstract gives no effect sizes or thresholds.
- **Not covered:** n-gram or substring overlap checks, which several benchmark papers use, were not read at a first-party abstract and are not claimed here.

**Safety and cyber benchmarks.** Safety and prompt-injection benchmarks stay in the **Safety & security** line above. Cyber-capability additions: [Cybench][cybench] (40 professional-level capture-the-flag tasks from 4 competitions, subtask breakdown; submitted 2024-08-15), [CyberGym][cybergym] (1,507 real vulnerabilities in 188 projects; abstract revised 2026-03-24; headline results are in [mas-benchmarking-best-practices.md](mas-benchmarking-best-practices.md)), and [WMDP][wmdp] (3,668 multiple-choice questions on hazardous knowledge in biosecurity, cybersecurity and chemical security, paired with the RMU unlearning method; 2024-03-05). Vendor-reported scores: [agentic-ai-vulnerability-landscape.md](agentic-ai-vulnerability-landscape.md) covers only CyberGym (MDASH); [ai-security-governance-analysis.md](ai-security-governance-analysis.md) uses Cybench as an evaluation task. WMDP has no vendor-score coverage in the corpus.

**Model Context Protocol (MCP) agents**: [MCPHallu][mcphallu] (PKU and others, arXiv 2611.07689; [code][mcphallu-code], Apache-2.0) — 358 tasks on 36 real MCP servers testing reasoning, execution and memory hallucinations; "Unreachable Goal is the hardest subtype for 12 of the 14 models". Claude Opus 4.6 scored highest (0.728; paper-reported, not in the abstract (average 0.642 across 14 models), unverified here; paper 2026-11-05), but the tasks were generated with Claude Sonnet 4.6.

**Tool use & info-seeking**: [ToolLLM](https://arxiv.org/abs/2307.16789), [StableToolBench](https://github.com/THUNLP-MT/StableToolBench), [InfoDeepSeek](https://arxiv.org/abs/2505.15872).

**Scientific**: [CORE-Bench](https://arxiv.org/abs/2409.11363) (reproducibility), [BadScientist](https://openreview.net/forum?id=7MPstNz66e) (LLM-reviewer manipulation; 67–82% acceptance via 5 strategies; paper-reported, undated here).

**Memory**: [LongMemEval](https://github.com/xiaowu0162/LongMemEval) (long-history temporal reasoning).

**Multi-agent**: [MultiAgentBench](https://arxiv.org/abs/2503.01935).

**Safety & security**: [SALAD-Bench](https://arxiv.org/abs/2402.05044), [Agent-SafetyBench](https://arxiv.org/abs/2412.14470), [AgentHarm](https://arxiv.org/abs/2410.09024), [WASP](https://arxiv.org/abs/2504.18575) (prompt-injection resilience; see the [prompt-injection taxonomy](agentic-ai-vulnerability-landscape.md#prompt-injection-attacks-and-defenses)).

**Multimodal/general**: [GAIA2](https://openreview.net/forum?id=9gw03JpKK4) (async environments; the earlier "~42% best pass@1" is undated and was not re-sourced).

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

**Leaderboards**: SciArena, Berkeley Function-Calling, Chatbot Arena, GAIA, [WebDev Arena][webdev-arena] (hosted on Arena.ai, "formerly LMArena" per Arena.ai's own about page; rows are mostly model-named, with some tagging a harness, e.g. "GPT-5.6 Sol (xHigh, Codex Harness)"), MiniWoB++.

**Agent-readiness scoring (websites/APIs)**: a new category (two vendors when first added; a third below) — `git grep` for `ora.ai`,
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

*Third vendor: Cloudflare (added 2026-11-14).* [isitagentready.com][cf-agent-ready], announced 2026-04-17, scores a site on "four dimensions": Discoverability (robots.txt, sitemap, Link headers), Content (Markdown for Agents), Bot Access Control (Content Signals, AI bot rules, Web Bot Auth) and Capabilities (Agent Skills, API Catalog, OAuth discovery, MCP Server Card, WebMCP). It also checks x402, UCP and ACP, "but these do not currently count towards the score", and exposes the scan as an MCP `scan_site` tool. The owner's own [agent-readiness-kit][ark] calls both Ora and isitagentready.com as scan sources, so it aggregates this category rather than adding an independent fourth score. A neighbouring but different category measures what AI answer engines *say* about a brand rather than whether a site is agent-callable; see [ai-crawlers-discoverability-landscape.md § GEO and AEO](../non-cc/infrastructure/ai-crawlers-discoverability-landscape.md#geo-and-aeo-what-is-canonical).

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
  "Every NLWeb instance also acts as an MCP server (and soon A2A)" (A2A = Agent-to-Agent Protocol). Microsoft announced it on
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

Each framework, benchmark, and dataset links to its first-party page (repo / Hugging Face / arXiv) inline in the tables above. Agent-readiness-scoring sources (checked 2026-10-15; DevTool Arena and Lightsage re-checked 2026-10-22; Cloudflare checked 2026-11-14):

[omi-bench]: https://omi.health/benchmark
[omi-home]: https://omi.health/
[omi-repo]: https://github.com/Omi-Health/medical-STT-eval
[ora]: https://ora.ai
[cf-agent-ready]: https://blog.cloudflare.com/agent-readiness/
[ark]: https://github.com/qte77/agent-readiness-kit
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

Harness-comparison sources (checked 2026-11-12):

[swe-bench]: https://www.swebench.com/
[swe-bench-experiments]: https://github.com/SWE-bench/experiments
[sb-cli]: https://swebench.com/sb-cli/
[terminal-bench]: https://www.tbench.ai/leaderboard
[tbench-repo]: https://github.com/harbor-framework/terminal-bench
[scale-swe-pro]: https://labs.scale.com/leaderboard/swe_bench_pro_public
[scale-swe-pro-paper]: https://labs.scale.com/papers/swe_bench_pro
[scale-swe-pro-repo]: https://github.com/scaleapi/SWE-bench_Pro-os
[epoch-swebv]: https://epoch.ai/benchmarks/swe-bench-verified
[epoch-llms]: https://epoch.ai/llms.txt
[epoch-data]: https://epoch.ai/data/benchmarking
[webdev-arena]: https://arena.ai/leaderboard/webdev

EDD-methodology sources:

[anthropic-evals]: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
[openai-evals]: https://developers.openai.com/api/docs/guides/evaluation-best-practices
[braintrust-edd]: https://www.braintrust.dev/articles/eval-driven-development
[deepeval-edd]: https://deepeval.com/blog/eval-driven-development
[husain-evals]: https://hamel.dev/blog/posts/evals
[claude-api-hillclimb]: https://claude.dev/blog/automating-eval-design-and-hillclimbing/
[mods-claudedev]: ../cc-native/plugins-ecosystem/CC-mods-function-hooks-analysis.md#the-other-built-in-mods-and-a-sample-set
[tb-maintenance]: https://arxiv.org/abs/2611.08417
[tb21]: https://github.com/harbor-framework/terminal-bench-2-1
[mcphallu]: https://arxiv.org/abs/2611.07689
[mcphallu-code]: https://github.com/J1zz/mcp_hallu
[osworld-paper]: https://arxiv.org/abs/2404.07972
[osworld-site]: http://osworld-v1.xlang.ai/
[osworld2]: https://arxiv.org/abs/2606.29537
[exlabel]: https://arxiv.org/abs/2610.39417
[trace]: https://arxiv.org/abs/2610.11678
[agent-systems]: https://arxiv.org/abs/2610.01618
[squeeze]: https://arxiv.org/abs/2610.13461
[abc]: https://arxiv.org/abs/2507.02825
[contam-survey]: https://arxiv.org/abs/2406.04244
[lcb]: https://arxiv.org/abs/2403.07974
[cybench]: https://arxiv.org/abs/2408.08926
[cybergym]: https://arxiv.org/abs/2506.02548
[wmdp]: https://arxiv.org/abs/2403.03218
[mink]: https://arxiv.org/abs/2310.16789
[timetravel]: https://arxiv.org/abs/2308.08493
[constat]: https://arxiv.org/abs/2405.16281
