# Topic Hub: Evals and Benchmarks

How agents are measured: eval methods and judges, benchmark catalogues and their validity, building
and maintaining a benchmark, and domain benchmarks. Pointers only; see [the hub index](README.md).

## Eval methods

| Doc / section | What it covers | Bucket |
|---|---|---|
| [agent-evaluation-metrics-landscape.md § Judge Calibration, Trace Evals and Eval Statistics](../sdlc-lcm/agent-evaluation-metrics-landscape.md#judge-calibration-trace-evals-and-eval-statistics) | Judge bias and drift, trace and process grading, error bars, pass@k vs pass^k, Inspect AI | sdlc-lcm |
| [agent-evaluation-metrics-landscape.md § Verifiable rewards (RLVR)](../sdlc-lcm/agent-evaluation-metrics-landscape.md#verifiable-rewards-rlvr) | Where RLVR comes from (Tulu 3), the training papers built on it, and the eval-side lesson that needs no training: grade with a deterministic check where one exists | sdlc-lcm |
| [agent-evaluation-metrics-landscape.md § Update-regression gate](../sdlc-lcm/agent-evaluation-metrics-landscape.md#update-regression-gate) | Adopt a self-edit to an agent's instructions only if replayed cases show no safety regression (Safe Personal RSI) | sdlc-lcm |
| [agent-evaluation-metrics-landscape.md § Code Erosion and Verbosity (SlopCodeBench)](../sdlc-lcm/agent-evaluation-metrics-landscape.md#code-erosion-and-verbosity-slopcodebench) | Multi-checkpoint coding benchmark: strict pass rate plus code-erosion and verbosity metrics | sdlc-lcm |
| [agent-evaluation-metrics-landscape.md § Cost-Performance Efficiency (Pareto)](../sdlc-lcm/agent-evaluation-metrics-landscape.md#cost-performance-efficiency-pareto) | Harness benchmarking by cost against score (Pareto knee); HAL and infrastructure noise | sdlc-lcm |
| [evaluation-data-resources-landscape.md § Why This Catalog Exists: EDD as Methodology](../sdlc-lcm/evaluation-data-resources-landscape.md#why-this-catalog-exists-edd-as-methodology) | Eval-driven development; `/claude-api build-eval` and `/claude-api hillclimb` | sdlc-lcm |
| [evaluation-data-resources-landscape.md § 1. Evaluation & Testing Frameworks](../sdlc-lcm/evaluation-data-resources-landscape.md#1-evaluation--testing-frameworks) | Eval and testing frameworks, LiteLLM `agent_eval` (preview) among them | sdlc-lcm |
| [CC-output-verification-analysis.md § No first-party eval runner → DIY](../cc-native/agents-skills/CC-output-verification-analysis.md#no-first-party-eval-runner--diy) | Claude Code ships no eval runner; what to build instead | cc-native |
| [agentic-legacy-migration-validation-analysis.md](../sdlc-lcm/agentic-legacy-migration-validation-analysis.md) | American Express's agentic test synthesis for validating COBOL-to-Java migrations | sdlc-lcm |
| [agent-silent-failure-taxonomy-analysis.md](../sdlc-lcm/agent-silent-failure-taxonomy-analysis.md) | A five-class taxonomy of silent failures from an 8-week production case study | sdlc-lcm |
| [automata-agent-traces-analysis.md](../sdlc-lcm/automata-agent-traces-analysis.md) | Finite-state machines rebuilt from agent traces to predict failures and audit behaviour | sdlc-lcm |

## Benchmark catalogue and validity

| Doc / section | What it covers | Bucket |
|---|---|---|
| [evaluation-data-resources-landscape.md § 2. Benchmarks](../sdlc-lcm/evaluation-data-resources-landscape.md#2-benchmarks) | Benchmarks by domain; dated status table, validity audits, contamination detection, cyber benchmarks | sdlc-lcm |
| [mas-benchmarking-best-practices.md § 3.2 Trust & Validation](../sdlc-lcm/mas-benchmarking-best-practices.md#32-trust--validation) | Why benchmark scores can mislead: dataset bias and trust issues | sdlc-lcm |

## Building and maintaining a benchmark

| Doc / section | What it covers | Bucket |
|---|---|---|
| [mas-benchmarking-best-practices.md § 3.5 Creating and maintaining a benchmark](../sdlc-lcm/mas-benchmarking-best-practices.md#35-creating-and-maintaining-a-benchmark) | Design, validate, release, maintain; agentic-cax-gauge and Text2WetLab as worked examples | sdlc-lcm |
| [mas-benchmarking-best-practices.md § 3.1 Design Checklist](../sdlc-lcm/mas-benchmarking-best-practices.md#31-design-checklist) | Design criteria, outcome validity first | sdlc-lcm |

## Domain benchmarks

| Doc / section | What it covers | Bucket |
|---|---|---|
| [computer-use-agents-landscape.md § The OSWorld family](../non-cc/agents/computer-use-agents-landscape.md#the-osworld-family) | OSWorld-Verified and OSWorld 2.0 results, vendor scores labelled | non-cc |
| [browser-agents-landscape.md § Browser benchmarks with dates](../non-cc/agents/browser-agents-landscape.md#browser-benchmarks-with-dates) | Web-agent benchmarks with dates; HAL vs a vendor-run aggregator | non-cc |
| [agentic-database-access-landscape.md § Text-to-SQL benchmarks](../non-cc/infrastructure/agentic-database-access-landscape.md#text-to-sql-benchmarks) | BIRD and Spider 2.0 with dates, BIRD-RL | non-cc |
| [programmatic-tool-calling-analysis.md § LLM function-calling benchmarks](../non-cc/protocols/programmatic-tool-calling-analysis.md#llm-function-calling-benchmarks) | Function-calling benchmarks | non-cc |
| [agentic-ai-vulnerability-landscape.md § Benchmarks](../sdlc-lcm/agentic-ai-vulnerability-landscape.md#benchmarks) | Prompt-injection benchmarks | sdlc-lcm |
| [CC-memory-tooling-landscape.md § Benchmarks](../cc-community/CC-memory-tooling-landscape.md#benchmarks) | Memory benchmarks (LongMemEval) | cc-community |
| [CC-skills-adoption-analysis.md § Does Skill Injection Help? (WebDev-Skills-Bench)](../cc-native/agents-skills/CC-skills-adoption-analysis.md#does-skill-injection-help-webdev-skills-bench) | Whether injecting skills helps, per WebDev-Skills-Bench | cc-native |
| [fm-bench-analysis.md](../sdlc-lcm/fm-bench-analysis.md) | FM-Bench: long-horizon management with competing agents | sdlc-lcm |

## Harness and agent comparisons

| Doc / section | What it covers | Bucket |
|---|---|---|
| [weco-aide-recursive-self-improvement-analysis.md § Harness search results](../non-cc/reference/weco-aide-recursive-self-improvement-analysis.md#harness-search-results) | Harness-search methods (HarnessFlow, Harness², AIDE², RRSI, Self-HPO, Meta-Harness): what is searched, reported result | non-cc |
| [CC-agent-teams-orchestration.md § Benchmarking a MAS vs CC-Style Baselines](../cc-native/agents-skills/CC-agent-teams-orchestration.md#benchmarking-a-mas-vs-cc-style-baselines) | Comparing a multi-agent system against Claude Code-style baselines | cc-native |
| [llm-routers-gateways-landscape.md § When to Use What](../non-cc/infrastructure/llm-routers-gateways-landscape.md#when-to-use-what) | LiteLLM `agent_eval` (preview): pass rate, cost and duration per harness | non-cc |

Related hubs: [security.md](security.md), [harness.md](harness.md), [agentic-web.md](agentic-web.md), [data.md](data.md), [cost.md](cost.md).
