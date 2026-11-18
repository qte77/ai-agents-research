---
title: "Agent Evaluation Metrics Landscape"
purpose: Survey of agent evaluation metrics and methodologies — task completion, reasoning quality, tool use, safety.
created: 2025-10-05
updated: 2026-11-18
validated_links: 2026-11-18
status: assess
---

<!-- markdownlint-disable MD024 no-duplicate-heading -->

Comprehensive catalog of evaluation metrics for AI agent systems, with
definitions, use cases, and primary research references for each metric.

**Related Document:** [Evaluation & Data Resources Landscape](evaluation-data-resources-landscape.md) - Tools, platforms, datasets, and benchmarks for implementing these metrics

## Core Evaluation Metrics

### Text Generation Quality

*See also: [Traditional Metrics Libraries](evaluation-data-resources-landscape.md)*

#### BLEU (Bilingual Evaluation Understudy)

- **Definition**: N-gram precision metric measuring overlap between
  generated and reference text
- **Use Case**: Evaluate generated review similarity to reference reviews
- **Strengths**: Fast computation, established baseline
- **Limitations**: Ignores semantic meaning, favors exact matches
- **Reference**: [BLEU: a Method for Automatic Evaluation of Machine Translation](https://aclanthology.org/P02-1040/)

#### ROUGE (Recall-Oriented Understudy for Gisting Evaluation)

- **Definition**: Recall-based metric measuring content overlap using
  n-grams and longest common subsequences
- **Use Case**: Assess coverage of key paper concepts in generated reviews
- **Strengths**: Captures content coverage, multiple variants (ROUGE-1,
  ROUGE-2, ROUGE-L)
- **Limitations**: Surface-level matching, no semantic understanding
- **Reference**: [ROUGE: A Package for Automatic Evaluation of Summaries](https://aclanthology.org/W04-1013/)

#### BERTScore

- **Definition**: Contextual embedding-based similarity using pre-trained
  BERT models
- **Use Case**: Measure semantic similarity beyond lexical matching
- **Strengths**: Captures semantic meaning, correlates with human judgment
- **Limitations**: Computationally expensive, model-dependent
- **Reference**: [BERTScore: Evaluating Text Generation with BERT](https://arxiv.org/abs/1904.09675)

#### Semantic Similarity (Cosine)

- **Definition**: Vector similarity between sentence embeddings using
  cosine distance
- **Use Case**: Compare semantic content of generated vs reference reviews
- **Strengths**: Fast, captures semantic relationships
- **Limitations**: Single similarity score, no aspect-specific assessment
- **Reference**: [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084)

### LLM-as-a-Judge Quality Assessment

*See also: evaluation frameworks and benchmarks in [evaluation-data-resources-landscape.md](evaluation-data-resources-landscape.md)*

#### Answer Relevancy

- **Definition**: LLM assessment of how well generated content addresses
  the input query/paper
- **Use Case**: Evaluate if generated reviews address key paper aspects
- **Strengths**: Contextual understanding, query-specific evaluation
- **Limitations**: LLM bias, requires careful prompt engineering
- **Reference**: [G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment](https://arxiv.org/abs/2303.16634)

#### Faithfulness

- **Definition**: Degree to which generated content remains factually
  consistent with source material
- **Use Case**: Ensure generated reviews don't hallucinate paper content
- **Strengths**: Detects factual inconsistencies, source-grounded
- **Limitations**: Requires clear source-target relationships
- **Reference**: [TRUE: Re-evaluating Factual Consistency Evaluation](https://arxiv.org/abs/2204.04991)

#### Hallucination Detection

- **Definition**: Identification of generated content not supported by
  source documents
- **Use Case**: Detect fabricated claims about paper methodology/results
- **Strengths**: Critical for academic accuracy, prevents misinformation
- **Limitations**: Difficult to define ground truth, context-dependent
- **Reference**: [Survey of Hallucination in Natural Language Generation](https://arxiv.org/abs/2202.03629)
- **Vendor statement**: Anthropic's help center calls this "hallucinating" information, "a byproduct of some of the current limitations of frontier Generative AI models", names outdated training data and quotes that "look authoritative or sound convincing, but are not grounded in fact" as examples, and tells users to review Claude's cited sources rather than rely on Claude "as a singular source of truth" ([Anthropic Help Center, read 2026-10-26](https://support.claude.com/en/articles/8525154-claude-is-providing-incorrect-or-misleading-responses-what-s-going-on)). A user-facing FAQ with no rates or mechanisms — useful only as the vendor's own acknowledgement.

#### Context Relevance

- **Definition**: Assessment of how well retrieved/provided context relates
  to the query
- **Use Case**: Evaluate if paper sections support generated review claims
- **Strengths**: RAG-specific, improves retrieval quality
- **Limitations**: Requires clear context-query relationships
- **Reference**: [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- **Landscape Reference**: [RAG evaluation tools (RAGAs, TruLens)](evaluation-data-resources-landscape.md)

### Judge Calibration, Trace Evals and Eval Statistics

Methods for trusting a score, as opposed to the metric definitions above. Pairs with the benchmark-side
[lifecycle in mas-benchmarking-best-practices.md § 3.5](mas-benchmarking-best-practices.md#35-creating-and-maintaining-a-benchmark),
which this section does not repeat.

#### Judge calibration

- **Agreement with humans**: [Zheng et al. (MT-Bench)][mtbench] report that strong LLM judges such as GPT-4 reach over 80% agreement with human preferences, "the same level of agreement between humans" (paper result, 2023-era judges). The body reports 85% GPT-4-to-human against 81% human-to-human in the no-tie setup. Re-measure on your own task: agreement on chat preferences says little about grading agent outputs.
- **Known biases**: the same paper names position bias (favouring an answer slot), verbosity bias (favouring longer answers) and self-enhancement bias (in its tests GPT-4 gave itself a 10% higher win rate and Claude-v1 25%, while GPT-3.5 did not favour itself), plus limited reasoning when the judge grades maths or logic. Its verbosity test, a "repetitive list" attack, is failed by all judges tried, GPT-4 least. Its mitigations: call the judge twice with the answer order swapped and count a win only if it holds in both orders (position bias), and give a chain-of-thought or reference answer for maths (with GPT-4 as judge, failure 14/20 default, 6/20 with CoT, 3/20 with a reference, on 10 maths questions each judged in both orders). Each is a check to run on your judge, not a property to assume.
- **Pairwise vs pointwise**: the paper treats both. Pairwise comparison discriminates subtle differences but the number of pairs grows quadratically; single-answer (pointwise) grading avoids that but, in the paper's words, absolute scores "are likely to fluctuate more than relative pairwise results if the judge model changes". Our reading (inference, not a paper result): pointwise for tracking one system over time with a pinned judge, pairwise for ranking a few candidates.
- **Prompt sensitivity**: [Prompt Lottery][promptlottery] (v1 2026-10-27, revised 2026-11-05) finds that meaning-preserving rephrasings of the judge prompt change verdicts and in some settings reverse model rankings; in a 10-annotator study judges lost 6 to 9 times more agreement under rephrasing than humans did. The authors recommend aggregating over several prompt variants instead of a single judge prompt (paper result, authors' own setup).
- **Drift**: [Chen, Zaharia and Zou][llmdrift] show that the "same" hosted model can change behaviour within months (GPT-4 prime-number accuracy with a step-by-step prompt, 84% in March 2023 and 51% in June, on 1,000 numbers; paper result). A judge behind a hosted alias drifts the same way, so pin the judge version where the API allows it, keep a frozen human-labelled sample, and re-score it whenever the judge changes. Judge-side manipulation is covered under [LLM Evaluator Vulnerability](#llm-evaluator-vulnerability); judge-agreement scoring under [Evaluator Alignment](#evaluator-alignment).

#### Trajectory, trace and outcome-vs-process grading

- **Outcome grading** checks the end state (a test passes, a database matches a goal state, as in [τ-bench][taubench]); it is hard to game by prose but blind to how the agent got there. **Process grading** scores intermediate steps; for training reward models, [Lightman et al.][prm] found process supervision beat outcome supervision on MATH (paper result, maths reasoning, not agent traces).
- **Trace evals**: [TRAIL][trail] provides 148 human-annotated agent traces with a taxonomy of error types; the best long-context model it tried (Gemini 2.5 Pro) scored 11% as a combined score (paper result, mid-2025 models). Judging a long trace is a hard task in its own right, so treat trace judges as needing the same calibration as any other.
- **Agent-as-a-Judge**: [Zhuge et al.][agentjudge] use an agentic system to grade agentic systems with intermediate feedback, on DevAI (55 tasks, 365 hierarchical requirements). The abstract says it "dramatically outperforms" LLM-as-a-Judge; in the body its alignment with the human consensus is about 90%, against roughly 60–71% for LLM-as-a-Judge and 85–89% for individual human judges (paper result, one benchmark, authors' own).
- **Auditing trace detectors**: [Adeniji et al.][tracedetect] (2026-10-21) check three trace-level detectors on six models doing 30 GSM8K problems each with a sometimes-corrupted calculator. Their main failure: a model silently used a different value than the tool returned without re-calling it, so the verification detector logged no re-check; human review matched automated labels on 67/67 final-correctness and 19/19 fault-impact calls but only 67/81 on verification. One model's score moved from 21/30 to 27/30 as step and token limits changed (paper result, small and synthetic).
- **Cached traces to cut eval cost**: [Johnson and Helm][cachedtraces] (2026-11-04) summarise reference systems' traces with an LLM, embed them, and predict a new system's score from where it lands; given one executed task, mean absolute error on SWE-bench Verified fell from 0.13 to 0.08 and on Terminal-Bench 2.0 from 0.14 to 0.12 (paper result, authors' method and benchmarks, abstract-level numbers).
- Vendor trace judges (TruLens Agent GPA, Arize Phoenix, LangChain AgentEvals) are listed under [Observability Tool Integration](#observability-tool-integration) and in the [frameworks table](evaluation-data-resources-landscape.md).

#### Eval statistics

- **Error bars**: [Miller][errorbars] treats an eval as an experiment on questions drawn from a super-population: standard errors of the mean, clustered standard errors when questions come in related groups, resampling answers to cut variance, paired differences (not two unpaired summaries) when comparing models, and power analysis before running. Report an interval with every headline score, and an interval on the paired difference when claiming one system beats another.
- **pass@k vs pass^k**: with n trials per task and c successes, the [τ-bench paper][taubench] defines pass^k as the chance that all k i.i.d. trials succeed, averaged over tasks, and pass@k (from [Codex][codex], at least one of k succeeds) as its optimistic counterpart; both have unbiased estimators from n and c. Use pass@k when one good attempt is enough (a human picks the best), pass^k when every run must work (unattended agents). τ-bench's own result for GPT-4o with function calling: about 61% pass^1 in retail and 35% in airline, with pass^8 below 25% in retail (paper result, 2024 model).
- **Run-to-run variance**: report the number of runs and the spread, not one run. Resampling within a task is one of Miller's variance-reduction levers.

#### Harness: Inspect AI

[Inspect AI][inspect] is the UK AI Security Institute and Meridian Labs framework; its docs describe composable datasets, agents, tools and scorers, 200-plus pre-built evals, a web log viewer and sandboxed execution (Docker, Kubernetes and others), including running external agents such as Claude Code. Statistics-relevant features per its [options reference][inspect-opts]: `--epochs` repeats each sample, and built-in epoch reducers include `mean`, `median`, `mode`, `max`, `at_least_{n}`, `pass_at_{k}` and `pass_k_{k}`; built-in scorers such as `exact()` report mean and stderr, and `model_graded_qa()` is its LLM-judge scorer (calibrate it as above). MIT licence; v0.3.290 released 2026-11-14, about 3.3k GitHub stars (checked 2026-11-15). Peers in the [frameworks table](evaluation-data-resources-landscape.md): HELM and the lm-evaluation-harness (via Every Eval Ever).

### Agent Performance Metrics

*See also: [evaluation frameworks & benchmarks](evaluation-data-resources-landscape.md) and [observability platforms](../non-cc/protocols/agent-observability-methods-analysis.md)*

#### Tool Selection Accuracy

- **Definition**: Percentage of correct tool choices for given tasks
- **Use Case**: Assess agent ability to select appropriate research tools
- **Measurement**: `correct_selections / total_selections`
- **Strengths**: Directly measures decision-making quality
- **Limitations**: Requires clear correct/incorrect labels
- **Reference**: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- **Recent Advance**: [When Tools Get in the Way](https://arxiv.org/abs/2609.14157) (Paturi, Kenzhebayev, Sethi, Raina et al., Sep 2026) finds that merely making an *irrelevant* tool available — not misusing it — drops accuracy from 98.2% to 63.5% across six LLMs and 500 query pairs spanning 10 domains; the drop persists even when the tool is rarely called, so it isn't explained by tool misuse alone. A one-sentence scope-aware system instruction recovers most of the lost accuracy.

#### Retrieval-Invoked Actual-Use Effect (RAE)

- **Definition**: Same-task outcome difference between matched skill-enabled and skill-disabled agent runs, computed only over tasks where the agent actually retrieved a skill ("Skill Following")
- **Use Case**: Distinguish genuine skill-following benefit from aggregate-metric illusions in retrieval-enabled agents
- **Calculation**: outcome difference between matched skill-retrieved-and-used vs. skill-disabled runs, conditioned on tasks with an actual retrieval event
- **Strengths**: Exposes cases where a positive aggregate metric coexists with a negative per-retrieval impact
- **Limitations**: Requires matched task pairs and retrieval-event detection; evaluated on coding/math tasks (e.g. MBPP+) across 17 LLMs
- **Reference**: [Skill Following: Evaluating Actual Skill Use in Retrieval-Enabled LLM Agents](https://arxiv.org/abs/2609.00549) (Cho & Park, Sep 2026; accepted to EMNLP 2026 Findings)
- **Finding**: Several models post positive aggregate MBPP+ scores under retrieval while showing *negative* RAE — aggregate metrics can mask retrieval actively harming the tasks where a skill was actually invoked

#### Response Time

- **Definition**: End-to-end processing time from input to output
- **Use Case**: Evaluate system performance for real-time applications
- **Measurement**: Wall clock time in seconds/milliseconds
- **Strengths**: Simple, directly impacts user experience
- **Limitations**: Hardware-dependent, varies with load
- **Reference**: [The Computer Systems Performance Handbook](https://dl.acm.org/doi/book/10.5555/280288) (standard performance measurement)

#### Token Usage Efficiency

- **Definition**: Ratio of useful output tokens to total consumed tokens
- **Use Case**: Optimize LLM API costs and computational efficiency
- **Calculation**: `output_tokens / (input_tokens + output_tokens)`
- **Strengths**: Cost optimization, resource management
- **Limitations**: Doesn't account for output quality
- **Reference**: [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) (RLHF efficiency considerations)

#### Path Convergence

- **Definition**: Ratio of minimum required steps to actual steps taken
- **Use Case**: Measure agent execution efficiency in completing evaluation tasks
- **Calculation**: `minimum_steps / actual_steps`
- **Strengths**: Quantifies workflow efficiency, identifies optimization opportunities
- **Limitations**: Requires determination of optimal path
- **Reference**: [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854)
- **Landscape Reference**: [Arize Phoenix - Path Metrics](../non-cc/protocols/agent-observability-methods-analysis.md)

#### Tool Call Accuracy

- **Definition**: Percentage of successful tool calls compared to attempted calls
- **Use Case**: Evaluate agent reliability in tool selection and parameter extraction
- **Calculation**: `successful_tool_calls / total_tool_calls`
- **Strengths**: Direct measure of agent competency with tools
- **Limitations**: Requires clear success/failure definitions
- **Reference**: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- **Landscape Reference**: [Arize Phoenix - LLM-as-a-Judge Templates](../non-cc/protocols/agent-observability-methods-analysis.md)
- **Recent Advance**: [Tool-Calling LLM Agents Under Realistic MCP Faults: Scale Does Not Purchase Fault Tolerance](https://arxiv.org/abs/2610.32555) (Iannillo, Owotogbe, Natella, Avallone, Kudryavtseva, Kumara; accepted NeurIPS 2026, Oct 2026) introduces MCP-Injector, fault-injection middleware for the MCP tool-call path, calibrated against 57,240 issue/PR threads mined from 1,774 open-source MCP repositories. Across a 1,350-cell experiment (two gpt-oss model sizes × three agent stacks × three fault conditions), permanent-heavy faults drop task-completion quality from 8.08 to 3.23 out of 10 (~60%), and the larger 120B model does not tolerate faults better than the 20B model (completion rate 91.1% vs. 95.6%, difference not statistically clear) — the authors' conclusion is that agent-framework error handling, not model scale, drives tool-call reliability. Code and data: [gitlab.com/uniluxembourg/snt/sedan/papers/mcp-injector](https://gitlab.com/uniluxembourg/snt/sedan/papers/mcp-injector) (archived at [Zenodo](https://doi.org/10.5281/zenodo.23573765)).

#### Behavioral Fingerprint Profile

- **Definition**: Diagnostic assessment revealing agent behavioral characteristics beyond performance metrics
- **Use Case**: Agent identity evaluation, consistency tracking, alignment validation
- **Components**: Personality clustering (ISTJ/ESTJ patterns), semantic robustness, sycophancy detection
- **Strengths**: Captures behavioral patterns, reveals alignment choices
- **Limitations**: Requires diagnostic prompt suite, model-dependent patterns
- **Reference**: Behavioral Fingerprinting of LLMs (Agents4Science 2025)
- **Application**: Inform Tier 3 Graph Analysis for agent identity persistence and behavioral consistency tracking across interactions

#### Cost-Performance Efficiency (Pareto)

- **Definition**: Average USD cost per task paired with average success rate (0-1) across a benchmark suite
- **Use Case**: Framework selection on the efficiency frontier — choose the framework achieving acceptable success at lowest cost
- **Calculation**: Plot (avg_cost_per_task, avg_success_rate) per framework; Pareto-optimal frameworks are those where no other framework dominates on both dimensions simultaneously
- **Strengths**: Makes cost/quality trade-off explicit; avoids optimizing only for accuracy at unbounded cost
- **Limitations**: Cost varies with model/provider pricing; task distribution must be representative
- **Reference**: [2602.22953] General Agent Evaluation / Exgentic (IBM Research, Feb 2026)
- **Example**: SmolAgents + Claude Opus 4.5 = 0.66 success at $4.39/task vs OpenAI MCP + Claude Opus 4.5 = 0.73 success at $8.54/task — 2× cost for 11% success gain
- **Application**: Use during framework selection for PeerRead batch evaluation to identify the cost-performance knee point
- **Recent Advance**: ["What Does a Harness Buy? Tokens, Mostly"](https://arxiv.org/abs/2610.04433) (Liu & Han, Oct 2026; code and data: [github.com/YangzeLiu/what-does-a-harness-buy](https://github.com/YangzeLiu/what-does-a-harness-buy), MIT, confirmed live 2026-10-11) holds the model fixed and varies the harness instead — five models across Claude Code, mini-SWE-agent, and OpenCode on SWE-bench Verified. On the full 447-task pool, Claude Code and mini-SWE-agent score within ~5 points of each other; OpenCode is the only harness whose effect clearly exceeds run-to-run noise, trailing by up to 9 points. But cost per task differs by up to 3x across harnesses at the same model/tasks/prices — the gap comes mainly from the fixed system-prompt-plus-tool-schema preamble sent at the first call, scaled by step count. The paper's own framing: "What is rarely measured is how much the harness itself moves the score when the model is held fixed" — reinforcing this metric's core point that harness/framework choice is predominantly a **cost** lever, not a capability one. Also argues 45-task benchmark pools detect a 13-point gap only about half the time, so small claimed harness-score deltas may not be statistically resolvable at common benchmark sizes (self-reported findings; not independently re-run here).
- **Harness-benchmarking method** (added 2026-11-18): to attribute a score difference to the harness, vary one thing and hold the rest fixed, then report variance. Each source below measured something different:
  - *Hold fixed: model, tools, prompts, budget and the task set.* [What Does a Harness Buy?][what-harness-buy] (above) fixes the model and varies the harness. [HarnessFlow][harnessflow-eval] fixes the executor model and the refinement budget across methods; its protocol is summarized in [weco-aide-recursive-self-improvement-analysis.md § Harness search results](../non-cc/reference/weco-aide-recursive-self-improvement-analysis.md#harness-search-results). [When Agents Fail: Model or Harness][model-harness-fit] runs four harnesses against four models (111 settings, 52,168 trajectories) and finds rankings shift across models and benchmarks, so a harness ranking measured on one model does not transfer; it proposes Valid Completion Rate, Model-Harness Fit and Token Load as measures. A harness comparison on a single model is a statement about that pairing.
  - *Hold fixed: the environment, not only the harness.* Anthropic's [infrastructure-noise post][infra-noise] (2026-02-05) measured a 6-point Terminal-Bench 2.0 gap between the least- and most-resourced container setups in its own runs, with scores flat between 1x and about 3x resources and rising above that, and advises treating resource configuration as a controlled variable and being skeptical of leaderboard gaps under 3 points. SWE-bench moved by only 1.54 points when RAM was scaled to 5x. Report the resource multiplier, not just the harness.
  - *Score the harness, not only the task.* [Trial by Trace (TraceTrial-Bench)][tracetrial] scores seven harness-reliability components on 95 tasks (4 harnesses, 9 models, 3,420 runs) and reports that 31.1% of runs succeeded on the task while failing at least one harness criterion. [Doc2Harness][doc2harness] instead tests whether a model can *build* a harness, replaying it against a scripted mock model so the model under test is removed from the measurement (19 models, 328 test cases; top score 53.05%, lowest 27.44%; no code link on the abstract page).
  - *Inspect logs, not just scores, and fix the evaluation harness.* The [Holistic Agent Leaderboard][hal] (arXiv 2510.11977, Oct 2025) ran 21,730 rollouts across 9 models and 9 benchmarks with one standardized evaluation harness, and used LLM-assisted log review to find agent behaviors that scores alone hid (for example an agent searching for the benchmark itself).
  - *A controlled ablation is the cleanest form.* [A Strong Harness Narrows the Model Gap][legal-xml] (Oct 2026, one domain: U.S. legislative-to-XML conversion, three Claude models, 153 bills) crosses three harness setups with three models: the weakest model in the full pipeline scored 0.948 against 0.806 for the strongest model alone. Single-domain, self-reported, no code link.
  - *Variance.* Pool size matters: [What Does a Harness Buy?][what-harness-buy] argues 45-task pools detect a 13-point gap only about half the time (a claim carried over from the entry above, not re-read this pass). Run several seeds or repeats, show spread, and record seeds and sampling settings; the HarnessFlow protocol note linked above shows what a paper leaves unstated. All figures are self-reported and were not re-run here.
- **Landscape Reference**: [Artificial Analysis Coding Agent Index](https://artificialanalysis.ai/agents/coding-agents) (v2.0, "October 2026 – current" per its own [methodology page](https://artificialanalysis.ai/methodology/coding-agents-benchmarking), confirmed 2026-11-12) is a live, continuously-updated cross-vendor implementation of this same performance/cost/execution-time triad. v2.0 is, in the page's own words, "the equal-weight average of FrontierCode v1.1, Terminal-Bench 4.0 and SWE-Atlas-QnA-AA." Relative to the v1.5 methodology previously cited here, v2.0 replaced the DeepSWE v1.1 component with **FrontierCode v1.1** — Cognition's benchmark, described as "changes to real open-source repositories, graded on whether a maintainer would merge them" — and renamed **SWE-Atlas-QnA** (Scale AI's benchmark) to **SWE-Atlas-QnA-AA**, graded in v2.0 with a different Artificial Analysis-chosen judge and reworded rubric criteria (v1.5 already used an AA-chosen judge); **Terminal-Bench** carries over at the v4.0 edition AA scores against (the live site has since moved to v4.1 as of 2026-11-12 — see that benchmark's own first-party details, including a Stanford-affiliation discrepancy between its two first-party sources, in [evaluation-data-resources-landscape.md § 2. Benchmarks](evaluation-data-resources-landscape.md#2-benchmarks)). The methodology page states "Each public row is an agent variant, not a model" — i.e. the index compares agent+model configurations, not models in isolation. The same operator's [Endpoint Accuracy Index](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) (v1.0, not re-checked this pass) weights a Berkeley Function Calling Leaderboard subset for tool-use accuracy — a second first-party agentic benchmark with its own methodology page. Both self-reported by the operator (an independent benchmarking company, per its own site), not independently re-run here. (Scope note: Artificial Analysis's separate **Decision Index** is out of scope for this entry — tracked instead against [system-1-decision-models-landscape.md](../non-cc/reference/system-1-decision-models-landscape.md).)
  **API scope** (checked 2026-11-12): the [data API docs](https://artificialanalysis.ai/data-api/docs) document model-level endpoints and none for agents, so the Coding Agent Index above is available on the website only. Separately, the docs mark the model-level `artificial_analysis_coding_index` and `artificial_analysis_agentic_index` fields as always null — "Artificial Analysis no longer publishes a Coding Index or an Agentic Index" — those are older model-level sub-indexes, not the agent-level Coding Agent Index.
  **Terms-of-use note**: Artificial Analysis's [Terms of Use](https://artificialanalysis.ai/terms-of-use) limit the site to "personal, noncommercial use" (§2.1), bar copying/reproducing/republishing site content (§2.2(d): "no part of the Site may be copied, reproduced, distributed, republished, downloaded") and bar automated scraping or data mining (§3.3(b), the second item labelled (vi): "to generate automated searches, requests, or queries to (or to strip, scrape, or mine data from) the Site"). This corpus accordingly describes the index's methodology narratively, by link, and does not scrape, reproduce, or cite its scores, costs, or rankings.

### Multi-Agent Coordination Metrics

*See also: [Graph Analysis & Network Tools](evaluation-data-resources-landscape.md) and [Agent Frameworks](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md)*

#### Step Efficiency

- **Definition**: Ratio of productive work steps to total execution steps
- **Use Case**: Identify coordination overhead in multi-agent workflows
- **Calculation**: `productive_steps / total_steps`
- **Strengths**: Measures workflow optimization effectiveness
- **Limitations**: Requires classification of step types
- **Reference**: Multi-agent coordination in distributed systems
- **Landscape Reference**: [Arize Phoenix - Path Metrics](../non-cc/protocols/agent-observability-methods-analysis.md)

#### Centrality Measures

- **Definition**: Graph theory metrics measuring agent importance in
  coordination networks
- **Variants**: Betweenness, closeness, degree centrality
- **Use Case**: Identify coordination bottlenecks and key agents
- **Strengths**: Quantifies structural importance
- **Limitations**: Requires graph construction from interaction logs
- **Reference**: [Networks: An Introduction](https://oxford.universitypressscholarship.com/view/10.1093/acprof:oso/9780199206650.001.0001/acprof-9780199206650)
  (Newman, 2010)
- **Landscape Reference**: [Graph Analysis & Network Tools](evaluation-data-resources-landscape.md)

#### Communication Overhead

- **Definition**: Ratio of coordination messages to productive work messages
- **Use Case**: Optimize agent communication efficiency
- **Calculation**: `coordination_messages / total_messages`
- **Strengths**: Measures coordination cost
- **Limitations**: Requires message classification
- **Reference**: Coulouris et al., "Distributed Systems: Concepts and Design"
  (5th Edition, 2012)

#### Task Distribution Balance

- **Definition**: Measure of workload evenness across agents using
  statistical variance
- **Use Case**: Ensure fair load balancing in multi-agent systems
- **Calculation**: `1 - std_dev(agent_tasks) / mean(agent_tasks)`
- **Strengths**: Quantifies load balancing effectiveness
- **Limitations**: Doesn't account for task complexity differences
- **Reference**: Multi-agent coordination in distributed systems (coordination metrics)
- **Landscape Reference**: [Agent Frameworks](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md)

### Production Framework Metrics

Metrics derived from production evaluation frameworks and competition benchmarks

#### Plan Adherence

- **Definition**: Degree to which agent follows its own generated execution plan
- **Use Case**: Detect agents that generate good plans but deviate during execution
- **Calculation**: `planned_steps_executed / total_planned_steps`
- **Strengths**: Separates planning quality from execution discipline
- **Limitations**: Requires plan extraction and step matching
- **Reference**: DeepEval PlanAdherenceMetric
- **Landscape Reference**: [DeepEval Framework](evaluation-data-resources-landscape.md)

#### Argument Correctness

- **Definition**: Accuracy of arguments passed to tool calls beyond tool selection
- **Use Case**: Detect subtle tool misuse where correct tool is called with wrong parameters
- **Calculation**: `correct_arguments / total_tool_calls`
- **Strengths**: Catches parameter-level errors missed by tool selection metrics
- **Limitations**: Requires ground truth for argument values
- **Reference**: DeepEval ArgumentCorrectnessMetric

#### Handoff Quality

- **Definition**: Effectiveness of context transfer between agents in multi-agent systems
- **Use Case**: Evaluate multi-agent coordination efficiency
- **Calculation**: `successful_handoffs / total_handoffs` with context preservation score
- **Strengths**: Quantifies multi-agent coordination effectiveness
- **Limitations**: Requires handoff event detection and context comparison
- **Reference**: Arize Phoenix Multi-Agent Evaluation
- **Landscape Reference**: [Arize Phoenix](../non-cc/protocols/agent-observability-methods-analysis.md)

#### Semantic Outcome

- **Definition**: Meaningful task completion beyond surface-level metrics
- **Use Case**: Evaluate if agent achieved the underlying intent, not just literal task
- **Measurement**: LLM-as-Judge assessment of outcome meaningfulness
- **Strengths**: Captures intent fulfillment vs. task completion
- **Limitations**: Requires clear outcome definitions
- **Reference**: LangSmith Multi-turn Evals

#### Evaluator Alignment

- **Definition**: Consistency between different evaluation methods on same outputs
- **Use Case**: Validate evaluation reliability and detect metric drift
- **Calculation**: Correlation coefficient between evaluator scores
- **Strengths**: Ensures evaluation trustworthiness
- **Limitations**: Requires multiple evaluation methods
- **Reference**: Self-Improving LLM Evals (Arize), TEAM-PHI (Agents4Science 2025)
- **Recent Advance**: TEAM-PHI demonstrates multi-LLM evaluator consensus through majority voting matches supervised evaluation without costly expert annotations
- **Recent Advance**: [DUET: Co-Evolving Solver and Grader Agents](https://arxiv.org/abs/2610.04087) (Gao, Pal, Henley, Radhakrishna, Soares; Oct 2026) frames the grader as something to optimize jointly with the solver rather than hold fixed: each round selects training tasks, runs the solver, scores outcomes with the grader, then revises both agents with a tool-using update module. The authors report gains for both agents across four agent benchmarks, outperforming baselines that optimize only the solver against a fixed grader — first-party evidence that evaluator alignment degrades as the agent it scores keeps changing, and that re-optimizing the evaluator alongside it is one fix. No code repository was found on the abstract page (checked 2026-11-12).

#### Fix Rate

- **Definition**: Percentage of issues successfully resolved in long-horizon tasks
- **Use Case**: Measure partial progress in complex multi-step tasks
- **Calculation**: `issues_fixed / total_issues_attempted`
- **Strengths**: Rewards incremental progress, not just full completion
- **Limitations**: Requires issue tracking and resolution verification
- **Reference**: SWE-EVO Benchmark (arXiv:2512.18470)

#### Rubric Alignment

- **Definition**: Degree to which agent output matches structured evaluation criteria
- **Use Case**: Self-grading against predefined quality rubrics
- **Calculation**: Weighted rubric criterion scores
- **Strengths**: Enables reproducible quality assessment
- **Limitations**: Requires rubric design and criterion weighting
- **Reference**: Rubric Rewards for AI Co-Scientists (arXiv:2512.23707)

#### Latent Failure Detection (SIMMER)

- **Definition**: State-machine execution of LLM-generated plans against a symbolic world model to detect failures that pass surface execution but silently undermine the goal
- **Use Case**: Evaluate LLM planning agents (household/kitchen domain) for silent or irreversible plan failures beyond simple task-completion checks
- **Components**: Three failure classes — Immediate Failures (precondition violations, observable at execution time), Latent Failures (all preconditions satisfied but consequences manifest later), Irreversible Failures (a latent-failure subset where no subsequent action can restore a valid world state)
- **Calculation**: `error_free_plans / total_plans`; `plans_with_latent_failures / total_plans`; `irreversible_failures / latent_failures`
- **Strengths**: Distinguishes silent/delayed failures from immediate ones; world model spans 77 actions, 262 objects, ~46,800 possible interactions grounded in real cooking scripts
- **Limitations**: Single domain (kitchen/household); benchmark code/data not yet released (conditional on acceptance) as of 2026-07-23
- **Reference**: SIMMER Benchmark (arXiv:2606.14574)
- **Finding**: Even frontier models achieve at most 17% error-free plans; up to 56% of plans contain latent failures, most leading to irreversible consequences
- **Mitigation**: Counterfactual foresight simulation (predicting state changes and self-checking for hazards before committing each action) reduces latent failures by up to 72% and irreversible cases by up to 75%

#### Elicitation Rate

- **Definition**: Percentage of evaluation runs achieving threshold score (≥7/10)
- **Use Case**: Measure behavioral consistency across multiple runs
- **Calculation**: `runs_above_threshold / total_runs`
- **Strengths**: Simple, threshold-based behavioral assessment
- **Limitations**: Requires multiple runs and score threshold definition
- **Reference**: Bloom Framework (Anthropic)
- **Landscape Reference**: [Bloom](../archive/further_reading.md#practitioner-resources)

#### Session Continuity

- **Definition**: Quality of state preservation across agent sessions or context windows
- **Use Case**: Evaluate long-running agent performance with context handoffs
- **Measurement**: State reconstruction accuracy after session boundary
- **Strengths**: Critical for production agents with context limits
- **Limitations**: Requires session boundary detection and state comparison
- **Reference**: Anthropic Effective Harnesses Pattern

#### Scope Adherence

- **Definition**: Alignment between planned work scope and actual executed work
- **Use Case**: Detect scope creep or premature completion in agents
- **Calculation**: `overlap(planned_scope, actual_scope) / planned_scope`
- **Strengths**: Identifies planning-execution gaps
- **Limitations**: Requires scope definition and extraction
- **Reference**: Anthropic Effective Harnesses Pattern

#### Verification Coverage

- **Definition**: Completeness of agent self-testing and validation
- **Use Case**: Measure how thoroughly agent verifies its own work
- **Calculation**: `verified_outputs / total_outputs`
- **Strengths**: Quantifies agent reliability and self-correction
- **Limitations**: Requires verification action detection
- **Reference**: Anthropic Effective Harnesses Pattern

### Observability-Based Metrics

*See also: [Observability & Monitoring Platforms](../non-cc/protocols/agent-observability-methods-analysis.md)*

#### Trace Coverage

- **Definition**: Percentage of agent execution paths captured in observability traces
- **Use Case**: Ensure comprehensive monitoring of agent behavior
- **Calculation**: `traced_execution_paths / total_execution_paths`
- **Strengths**: Validates observability completeness
- **Limitations**: Requires trace path definition
- **Reference**: [OpenTelemetry Specification](https://opentelemetry.io/docs/specs/)
- **Landscape Reference**: [AgentNeo - Observability Platform](../non-cc/protocols/agent-observability-methods-analysis.md)
- **Landscape Reference**: [Tracely](https://github.com/jwuthri-cloud/Tracely-ai) (MIT, 1,156★ on 2026-10-23; republished under `jwuthri-cloud` on 2026-10-11 — the original `Jwuthri/Tracely-ai` returns 404) — trace-native CI/CD for agents: production traces are auto-clustered into failures, frozen into hermetic regression cases with recorded fixtures, and replayed in CI at $0 to block the PR, without hand-authored eval datasets

#### Error Recovery Rate

- **Definition**: Percentage of errors that agents successfully recover from
- **Use Case**: Measure system resilience and self-correction capability
- **Calculation**: `recovered_errors / total_errors`
- **Strengths**: Quantifies system robustness
- **Limitations**: Requires error classification and recovery detection
- **Reference**: [Fault tolerance in distributed systems](https://dl.acm.org/doi/10.1145/98163.98167)
- **Landscape Reference**: [Browser Use - Self-Correcting Architecture](evaluation-data-resources-landscape.md)

#### Memory Utilization Efficiency

- **Definition**: Ratio of relevant retrieved memory to total memory accessed
- **Use Case**: Optimize agent memory systems and context management
- **Calculation**: `relevant_memory_retrieved / total_memory_accessed`
- **Strengths**: Measures memory system effectiveness
- **Limitations**: Requires relevance assessment
- **Reference**: [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)
- **Landscape Reference**: [Letta - Advanced Memory Architecture](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md)
- **Recent Advance**: The MSCE (Memory-Skill Co-Evolution) framework — [From Memory to Skills](https://arxiv.org/abs/2607.16621) (Tang, Zhang, Zhuang et al., Jul 2026) — converts prior agent experience into callable skills carrying evidence links, applicability boundaries, and reliability estimates, using "reflection-weighted value backfilling" to turn sparse terminal feedback into evidence-calibrated signals for memory/skill evolution; reports strong cross-domain transfer and lifelong-evolution capability
- **Landscape Reference**: [MemTensor/MemOS](https://github.com/MemTensor/MemOS) (Apache-2.0, 11.6k★) — a self-evolving memory OS (own papers: arXiv:2507.03724, arXiv:2505.22101) with an L1-trace/L2-policy/L3-world-model skill-evolution tier, reporting 35.24% token savings from structured memory reuse

#### Streaming Memory Fidelity (StreamMemBench)

- **Definition**: Two-stage streaming evaluation of agent memory systems — Task 1 measures whether an agent correctly uses observed streaming evidence; Task 2 (follow-up) measures whether feedback from Task 1 is incorporated into later assistance responses
- **Use Case**: Diagnose whether memory systems adapt longitudinally to feedback, not just ingest streaming evidence in the moment
- **Components**: Four normalized (0-1) diagnostic metrics — Fidelity, Initial evidence use, Feedback incorporation, Followup reuse
- **Strengths**: Separates one-shot evidence use from longitudinal feedback adaptation; benchmarked across 8 systems (2 RAG baselines + 6 memory systems: mem0, memos, evermemos, memskill, memoryos, a_mem)
- **Limitations**: No published leaderboard — results require running the repo's own evaluation scripts; dataset-scale figures are repo-README-sourced and not independently re-verified
- **Reference**: StreamMemBench (arXiv:2606.14571)
- **Finding**: Current memory systems frequently fail to use observed evidence and don't reliably convert user feedback into improved follow-up behavior

### Security & Safety Metrics

*See also: [AI Model Testing & Validation Platforms](evaluation-data-resources-landscape.md)*

#### Hallucination Rate

- **Definition**: Percentage of generated content not supported by source material
- **Use Case**: Ensure factual accuracy in academic review generation
- **Calculation**: `hallucinated_statements / total_statements`
- **Strengths**: Critical for academic integrity
- **Limitations**: Requires ground truth verification
- **Reference**: [Survey of Hallucination in Natural Language Generation](https://arxiv.org/abs/2202.03629)
- **Landscape Reference**: [Patronus AI - Hallucination Detection](evaluation-data-resources-landscape.md)

#### Bias Detection Score

- **Definition**: Quantified measurement of bias in agent outputs across demographic groups
- **Use Case**: Ensure fair evaluation across diverse academic content
- **Calculation**: Statistical variance in performance across protected attributes
- **Strengths**: Promotes fair and equitable agent behavior
- **Limitations**: Requires demographic data and bias definitions
- **Reference**: [Bias in AI Systems](https://arxiv.org/abs/1909.01326)
- **Landscape Reference**: [Patronus AI - Bias Assessment](evaluation-data-resources-landscape.md)

#### Prompt Injection Resistance

- **Definition**: Ability to maintain intended behavior despite malicious input attempts
- **Use Case**: Prevent manipulation of academic evaluation processes
- **Measurement**: Success rate against standardized injection attacks
- **Strengths**: Essential for production security
- **Limitations**: Requires comprehensive attack vectors
- **Reference**: [Prompt injection attacks against large language models](https://arxiv.org/abs/2302.12173)
- **Landscape Reference**: [Giskard - Security Testing](evaluation-data-resources-landscape.md)
- **Taxonomy**: [Prompt injection: attacks and defenses](agentic-ai-vulnerability-landscape.md#prompt-injection-attacks-and-defenses)

#### LLM Evaluator Vulnerability

- **Definition**: Susceptibility of LLM-based evaluators to manipulation strategies
- **Use Case**: Validate robustness of LLM-as-Judge evaluation tier
- **Attack Vectors**: TooGoodGains (exaggerating metrics), BaselineSelect (cherry-picking), StatTheater (statistical facades), CoherencePolish (presentation quality), ProofGap (hiding oversights)
- **Observed Rate**: 67-82% acceptance rates for manipulated content
- **Critical Issue**: Concern-acceptance conflict where reviewers flag issues yet assign acceptance scores
- **Strengths**: Identifies critical LLM judge vulnerabilities
- **Limitations**: Requires adversarial testing framework
- **Reference**: BadScientist (Agents4Science 2025)
- **Mitigation**: Implement adversarial robustness validation and meta-evaluation to detect manipulation

#### Verbalized Confidence Calibration (Brier)

- **Definition**: How well a model's stated confidence ("I am 80% confident…") matches how often it is right, scored with the Brier score (mean squared error between stated probability and outcome; lower is better)
- **Use Case**: Decide when an agent's answer can be acted on without review, and when it should abstain or escalate
- **Calculation**: `mean((confidence - correct)^2)` over questions, `correct` ∈ {0, 1}; elicited by prompting, so no logit access is needed
- **Reference values**: [ConfidenceBench (arXiv:2607.20526)](https://arxiv.org/abs/2607.20526), 15 frontier LLMs on 200 private questions: best 0.103 (Claude Opus 4.6, Gemini 3.1 Pro Preview), calibrated-random baseline 0.1875, Gemini 3.1 Flash-Lite 0.367, "indicating severe miscalibration"; "the most accurate model is not the best-calibrated". The 200 questions are private and the abstract page links no code, so the scores cannot be re-run independently
- **Training for it**: [ConfTuner (arXiv:2508.18847, NeurIPS 2025)](https://arxiv.org/abs/2508.18847) fine-tunes with a "tokenized Brier score", proved a proper scoring rule, needing no ground-truth confidence labels; reports gains in calibration, self-correction and model cascades ([code](https://github.com/liushiliushi/ConfTuner))
- **Limitations**: calibrated belief does not mean calibrated action. [Aggarwal (arXiv:2608.27167)](https://arxiv.org/abs/2608.27167): across 12 frontier models, commitment on a provably unpredictable question "rises from 6.5% to 54.0% as evidence is escalated", and a fully fabricated evidence panel lifts it "from 24.5% to 36.8%", statistically indistinguishable from genuine data (37.6%), while stated probabilities "barely move". The act/don't-act gate is trainable (a 3B model fine-tuned on 540 synthetic cases) but fails under rigid response formats ([code + data](https://github.com/Pranav-1100/confidence-calibration-evaluation)). Measure the decision, not only the stated probability. For typed act/abstain decisions from small classifiers, see [system-1-decision-models-landscape.md](../non-cc/reference/system-1-decision-models-landscape.md).

## Implementation Frameworks

### Evaluation Platform Integration

*For comprehensive implementation guidance, see [Agent Evaluation & Benchmarking](evaluation-data-resources-landscape.md)*

- **AutoGenBench**: Docker-isolated evaluation with benchmark performance metrics
- **Swarms Agent Evaluation**: Continuous monitoring with real-time performance tracking  
- **DeepEval**: 30+ LLM-as-a-judge metrics with pytest integration
- **Braintrust Agent Evaluation**: Architecture-specific assessment with custom scorers
- **Google ADK Evaluation**: Trajectory analysis with multi-turn conversation testing
- **[Waza](https://github.com/microsoft/waza)** (Microsoft, Go CLI, MIT): authors repository/CLI/MCP eval scenarios for agent workflows, skills and custom agents, runs graded trials and inspects the evidence behind each grade; a published-binary release line (`v0.40.1` as of `gh api` 2026-11-12) plus CI-regression-gate guides, and an azd extension with its own separately versioned release line. The README is explicit that several features (a logical execution-attempt embedding API, a checkpoint-embedding preview, public submission commands) are documented but not yet in an installed binary — check `waza --version` against the feature/platform matrix before relying on a specific capability.

### Observability Tool Integration

*For detailed technical analysis, see [Observability & Monitoring Platforms](../non-cc/protocols/agent-observability-methods-analysis.md)*

- **Pydantic Logfire**: First-party PydanticAI instrumentation via `logfire.instrument_pydantic_ai()` with OTel-based tracing
- **Comet Opik**: OpenTelemetry-compatible spans with local deployment
- **Arize Phoenix**: Path convergence metrics with LLM-as-a-judge templates
- **Langfuse**: Comprehensive prompt management with evaluation integration
- **AgentNeo**: Decorator-based tracing with SQLite storage
- **TruLens**: RAG Triad metrics plus seven agent evaluators (logical consistency, execution efficiency, plan adherence, plan quality, tool selection, tool calling, tool quality) over OpenTelemetry traces, and an `MCP` span type for tool calls. Its README reports that the Agent GPA judge caught 267 of 281 human-annotated errors on TRAIL/GAIA, against 55% for a baseline trace judge ([arXiv:2510.08847][agent-gpa]; vendor result). MIT, v2.16.0 (2026-10-19). Created by TruEra; [trulens.org][trulens-org] says Snowflake has maintained it since the acquisition ([README][trulens])

### Graph Analysis Integration

*For network analysis capabilities, see [Graph Analysis & Network Tools](evaluation-data-resources-landscape.md)*

- **NetworkX**: Centrality measures and coordination pattern analysis
- **LangGraph**: Stateful agent workflow orchestration with conditional logic
- **PyTorch Geometric**: Graph neural networks for agent behavior modeling
- **NetworKit**: High-performance graph analysis with parallel processing

## Additional Resources

[Framework implementations and practical guidance on using these metrics](evaluation-data-resources-landscape.md)

## Sources

Metric definitions are sourced from the research papers and tool docs cited inline throughout; the implementing frameworks, benchmarks, and datasets are catalogued in [evaluation-data-resources-landscape.md](evaluation-data-resources-landscape.md).

| Source | Content |
|---|---|
| [MT-Bench][mtbench] | LLM-judge agreement with humans; position, verbosity and self-enhancement bias; pairwise vs single-answer grading |
| [LLM drift][llmdrift] | Behaviour change of hosted models over months |
| [TRAIL][trail] / [Agent-as-a-Judge][agentjudge] | Trace-level error taxonomy and agentic judges |
| [Prompt Lottery][promptlottery] / [trace detector audit][tracedetect] / [cached traces][cachedtraces] | Judge-prompt sensitivity, trace-detector audit, trace-based score prediction (abstract pages, read 2026-11-18) |
| [Adding Error Bars][errorbars] | Statistics for eval reporting |
| [τ-bench][taubench] / [Codex][codex] | pass^k and pass@k |
| [Inspect AI][inspect] | Harness docs and repo |
| [What Does a Harness Buy?][what-harness-buy] / [HarnessFlow][harnessflow-eval] / [When Agents Fail][model-harness-fit] | Fixed-model harness comparison, five-run protocol, model-harness interaction measures (abstract pages, read 2026-11-18) |
| [Trial by Trace][tracetrial] / [Doc2Harness][doc2harness] / [Strong Harness][legal-xml] | Harness-reliability benchmark, harness-building benchmark, single-domain controlled ablation (abstract pages, read 2026-11-18) |
| [Infrastructure noise][infra-noise] / [HAL][hal] | Container-resource effect on agentic coding scores; standardized evaluation harness and log review (read 2026-11-18) |

[trulens]: https://github.com/truera/trulens
[trulens-org]: https://www.trulens.org/
[agent-gpa]: https://arxiv.org/abs/2510.08847
[mtbench]: https://arxiv.org/abs/2306.05685
[llmdrift]: https://arxiv.org/abs/2307.09009
[taubench]: https://arxiv.org/abs/2406.12045
[codex]: https://arxiv.org/abs/2107.03374
[prm]: https://arxiv.org/abs/2305.20050
[trail]: https://arxiv.org/abs/2505.08638
[agentjudge]: https://arxiv.org/abs/2410.10934
[errorbars]: https://arxiv.org/abs/2411.00640
[inspect]: https://inspect.aisi.org.uk/
[inspect-opts]: https://inspect.aisi.org.uk/options.html
[what-harness-buy]: https://arxiv.org/abs/2610.04433
[harnessflow-eval]: https://arxiv.org/abs/2611.06254
[model-harness-fit]: https://arxiv.org/abs/2610.32483
[tracetrial]: https://arxiv.org/abs/2610.32285
[doc2harness]: https://arxiv.org/abs/2610.20344
[legal-xml]: https://arxiv.org/abs/2610.19999
[infra-noise]: https://www.anthropic.com/engineering/infrastructure-noise
[hal]: https://arxiv.org/abs/2510.11977
[promptlottery]: https://arxiv.org/abs/2610.38076
[tracedetect]: https://arxiv.org/abs/2610.30491
[cachedtraces]: https://arxiv.org/abs/2611.06803
