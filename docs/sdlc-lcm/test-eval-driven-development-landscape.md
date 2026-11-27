---
title: Test- and Eval-Driven Development Landscape (TDD, BDD, PBT, EDD, Tripwires)
purpose: Compares the write-the-check-first practices (TDD, BDD, property-based testing, EDD) and the tripwire tests and evals that guard them, with first-party sources and how coding agents use each.
status: assess
created: 2026-11-27
updated: 2026-11-27
validated_links_on: 2026-11-27
---

**Details:** read from first-party pages on 2026-11-27. Vendor and company statements are labelled as their own claims.
Volatile facts carry `(read 2026-11-27)`. Abbreviations are expanded in [../glossary.md](../glossary.md).

Four practices share one loop: state what correct looks like as a runnable check, watch it fail, then make the
code (or the prompt, tools and harness) pass it. They differ in who writes the check, what a pass means and whether
the check can be repeated exactly. This doc compares them, goes deep on eval-driven development (EDD), and then covers
**tripwires**: checks whose job is to fail when something drifts, including when the test suite itself has gone soft.

Existing coverage is linked, not repeated: the discipline ladder (TDD to BDD to EDD to spec-driven development) is in
[agentic-engineering-disciplines-landscape.md](agentic-engineering-disciplines-landscape.md); eval tools, datasets and
the EDD-as-methodology framing are in
[evaluation-data-resources-landscape.md](evaluation-data-resources-landscape.md#why-this-catalog-exists-edd-as-methodology);
metrics are in [agent-evaluation-metrics-landscape.md](agent-evaluation-metrics-landscape.md); spec-driven
frameworks are in [spec-driven-frameworks-landscape.md][sdd]; guardrail tripwires are in
[openai-agents-sdk-analysis.md § Guardrails][oai-guard].

## What It Is

| Variant | The loop in one line | What changes versus the others |
|---|---|---|
| **TDD** (test-driven development) | Write a failing unit test, make it pass with the least code, refactor, repeat | The baseline. A developer writes the test; the answer is exact and repeatable |
| **BDD** (behaviour-driven development) | Write the behaviour as a business-readable scenario, automate it, then build to it | The check doubles as a shared specification for non-programmers |
| **PBT** (property-based testing) | State a rule that must hold for every input; a library generates the inputs and reports the simplest failing example it finds | The author writes the property, not the examples; inputs are machine-chosen |
| **EDD** (eval-driven development) | Write the eval (dataset plus grader) for the behaviour first, run a baseline, change the agent, compare experiments | Outputs are non-deterministic and several answers can be right, so a score replaces a boolean |

- **TDD.** Martin Fowler's page, updated 2023-12-11, gives the steps as write a test, write the code until it passes,
  refactor, after an initial list of test cases ([Fowler][fowler-tdd]). It credits Kent Beck with developing it in the
  late 1990s as part of Extreme Programming and names neglecting the refactor step as the commonest way to get it
  wrong. Fowler's second benefit is design pressure: writing the test first forces the interface to be thought
  through before the implementation.
- **BDD.** Dan North's origin essay started from renaming tests: methods named as sentences (a "should" template),
  so a failing test names the intended behaviour, and acceptance criteria made executable ([North][north-bdd]).
  Cucumber's Gherkin reference defines the executable-specification format: a Feature holds Scenarios made of
  Given (context), When (action) and Then (outcome) steps in plain language ([Gherkin][gherkin]). Wikipedia states
  that BDD is often mistaken for a refinement of TDD; its purpose is shared understanding ([Wikipedia BDD][w-bdd],
  secondary).
- **PBT.** Hypothesis, the Python library, describes the practice as writing tests that should pass for all inputs in
  a described range, letting the library pick inputs including edge cases the author did not think of; on failure
  it reports the simplest failing example it can find ([Hypothesis docs][hyp-docs], [Hypothesis site][hyp-site]).
  The origin paper (QuickCheck, Claessen and Hughes, 2000) was not readable in this pass (see Not included).
- **EDD.** Covered in depth below.

## Comparison

| Practice | The check | Written by | Pass criterion | Deterministic? | Typical tooling | First-party source |
|---|---|---|---|---|---|---|
| TDD | Unit test with exact expected value | Developer | Assertion holds | Yes | xUnit-family frameworks (pytest, JUnit) | [Fowler][fowler-tdd] |
| BDD | Gherkin scenario bound to step code | Developer plus business and test roles | Every step passes | Yes (the step code is ordinary tests) | Cucumber | [Gherkin][gherkin], [North][north-bdd] |
| PBT | Property over generated inputs | Developer | Property holds for every generated input | How a failure is replayed was not read (the docs list a "Replaying failed tests" page) | Hypothesis (Python); other languages have their own libraries | [Hypothesis docs][hyp-docs] |
| EDD | Dataset of inputs, optional reference outputs, plus code and LLM-judge graders | Product, domain experts and engineers, often seeded from real runs | Score at or above a threshold, with no regression on previously passing examples | No: model output varies run to run | LangSmith, DeepEval, Inspect, Harbor and similar ([catalog][eval-cat]) | [Paper][arxiv-abs], [LangChain][lc-edd], [Airbnb][airbnb-edd] |

Reading the table: the first three produce a boolean you can trust to repeat; EDD produces a distribution, so the pass
criterion, the grader's own reliability and the dataset's coverage all become things to maintain. The practices stack
rather than compete: an agent harness still needs TDD-style tests for its deterministic code, and EDD for the model
behaviour on top.

## EDD in Depth

### The paper's process model

Xia, Lu, Zhu and others, [Evaluation-Driven Development and Operations of LLM Agents][arxiv-abs] (arXiv 2411.13768;
first submitted 2024-11-21, revised through v3 on 2025-11-17, marked "submission under review" (read 2026-11-27)).
Its framing: evaluation should be a continuous, governing function across the lifecycle, not a terminal checkpoint,
and the authors call the approach EDDOps (evaluation-driven development and operations). The abstract page shows v3
under that title; the full text was read from the v2 HTML ([v2 HTML][arxiv-html]), whose title is "Evaluation-Driven
Development of LLM Agents", so details below are v2 and may differ in v3.

- **Evidence base.** A multivocal literature review (MLR, academic plus industry sources) of 134 academic and 27
  grey-literature sources. In the academic set, 93.28% (125/134) of evaluations happen before deployment, while
  post-deployment (2.24%) and continuous (4.48%) evaluation are rare (v2, authors' own count).
- **How it relates to TDD and BDD.** The paper says its approach builds on their iterative feedback (TDD) and shared
  requirements (BDD) but extends past their pre-deployment, deterministic focus to non-deterministic behaviour and
  post-deployment evolution.
- **Process model, four steps.** (1) define an evaluation plan (goals, governance and risk-based priorities);
  (2) develop evaluation test cases, choosing benchmarks and frameworks; (3) conduct offline (development-time) and
  online (runtime) evaluations; (4) analyse and improve, where results drive both runtime adaptation and offline
  redevelopment.
- **Reference architecture.** Three layers, namely a supply-chain layer, an agent layer and an operation layer; the
  operation layer holds the evaluation component and AgentOps (agent operations) infrastructure for logging and
  observability. The paper's case study is an Australian tax-assistant agent, evaluated with DeepEval, pre-deployment
  and offline only, with a pilot of online tracing in a simulated environment (the authors' own report).

### LangChain's practice (vendor blog, 2026-11-09)

[What is eval-driven development?][lc-edd] (Divya Santhanam, LangChain) calls EDD the agent analogue of TDD and
reduces it to three steps (all statements are the vendor's own, written around its LangSmith product):

1. **Define what good looks like**, one behaviour at a time, as a short spec: when it should happen, what the agent
   does, what it must not do, and which existing behaviours must keep working. The spec must be scoreable as pass or
   fail.
2. **Write the eval before building.** Build a dataset (real runs are the preferred source), write an evaluator (code
   when the check is deterministic, LLM-as-judge when not), and run a baseline experiment. Examples for the missing
   feature fail at baseline; the rest record what already works.
3. **Make the change and compare experiments.** Look past the average to per-example regressions, read traces to see
   why something failed, and turn production failures into new dataset examples.

The post's "Common mistakes" section lists five, among them checking only the average score and adding evals not tied to a specific failure or change.
For agents that act in an environment, it says to check the state left behind, not just the answer, using
the Harbor harness (an open-source framework, per the post; not checked further here).

### Airbnb's practice (company engineering blog)

[Eval-driven development: Lessons from evaluating GenAI at scale][airbnb-edd] (Airbnb Engineering, five named authors)
calls EDD the generative-AI analogue of TDD and says the habit starts from looking at real outputs. Its recommendations,
stated as the company's own and explicitly "not intended to be prescriptive":

- Five principles: define goals and gates up front, let observed errors define metrics, keep the evaluator set small
  (3 to 5 calibrated LLM judges preferred over 20 to 30 noisy ones), appoint a human decision-maker, collaborate
  with product partners continuously.
- Three layered methods: programmatic checks first, LLM-as-judge second, human evaluation to calibrate the stack.
- Calibrate a judge against a golden set of 50 to 100 labelled examples that includes bad examples, targeting
  agreement in the high 80s to 90s per cent.
- For agents, evaluate the trajectory (traces, tool calls, subagent order), not only the final answer.
- Mirror evals in production: its walkthrough samples 5% of live de-identified traffic daily and feeds new failure
  modes back as new evals.

### Offline versus online, and regression sets

| Aspect | Offline evals | Online evals |
|---|---|---|
| When | Before release, in development and continuous integration (CI) | On live traffic after release |
| Inputs | Curated dataset, golden outputs | Sampled real traces |
| Role | Compare versions, block regressions | Find cases the dataset never had, feed the dataset |
| Sources | [Paper][arxiv-abs], [LangChain][lc-edd] (CI plus production) | [Paper][arxiv-abs], [Airbnb][airbnb-edd] (5% sampling) |

A **regression set** is the part of the dataset that records behaviour that already works, so a change that fixes one
case but breaks another shows up per example (LangChain's VPN how-to versus ticket example is its own illustration).
Both vendors tie the dataset's growth to observed failures, which is the EDD counterpart of "add a test for every bug".

Contrast worth keeping: Hamel Husain's cautionary essay, cited in the
[existing EDD section](evaluation-data-resources-landscape.md#why-this-catalog-exists-edd-as-methodology), argues for
finding real failure modes before encoding evals; Airbnb's "look at your data" rule says the same.

## Tripwires

A tripwire here means a check that is designed to fail loudly when something drifts, and so protects the other checks.
No single standard term covers all of the cases below; the names are the sources' own.

| Tripwire | What it detects | Mechanism | Source |
|---|---|---|---|
| **Mutation testing** | A test suite that cannot catch faults | Tool seeds small faults ("mutants") into the code, runs the tests, and counts mutants killed (tests fail) versus survived (tests pass) | [Stryker][stryker], [PIT][pit], [mutmut][mutmut] |
| **RED-first check** | A new test that can never fail | See the TDD step: run the new test, confirm it fails for the expected reason before writing the code | [Wikipedia TDD][w-tdd] (secondary, citing Beck) |
| **Guardrail tripwire** | Unsafe or off-policy agent input, output or tool call at runtime | A guardrail function sets a tripwire flag; the runner raises an exception and halts the run | [OpenAI Agents SDK guardrails][oai-guardrails], KB: [Guardrails][oai-guard] |
| **Eval regression gate** | A change that degrades a behaviour that used to work | Baseline-versus-experiment comparison in CI per example | [LangChain][lc-edd] |
| **Judge calibration** | A drifting LLM judge | Re-score the golden set; Airbnb says to "Recalibrate periodically as failure modes evolve" (treating falling agreement as drift is our synthesis) | [Airbnb][airbnb-edd] |

Details per row:

- **Mutation testing.** Stryker's docs: mutants are inserted automatically, tests are run for each, a failing run kills
  the mutant, a passing run means it survived; the killed percentage measures test effectiveness ([Stryker][stryker]).
  PIT (Java) makes the contrast with line coverage explicit: coverage shows only which code ran, not whether the tests
  could detect a fault in it, and tests without assertions are the extreme case; PIT calls itself fast and
  build-tool-integrated, which is its own claim ([PIT][pit]). mutmut (Python) runs pytest per mutant, can resume
  interrupted runs and applies a mutant to disk for inspection; the docs warn to commit the file first ([mutmut][mutmut]).
  Cost: one test-suite run per mutant, so these are scheduled or scoped runs, not every-commit gates.
- **Never-failing tests.** Wikipedia's TDD page gives the purpose of the RED step as showing that new code is needed,
  that the harness works and that the new test is not flawed and will always pass ([Wikipedia TDD][w-tdd], secondary).
  Mutation testing is the after-the-fact version of the same check. Our synthesis: a test that pattern-matches source
  text can pass forever when the pattern is over-broad, because it also matches comments or look-alike names (one project's case, below).
- **Guardrail tripwires** are a runtime concept, not a test: the OpenAI Agents SDK runs input and output guardrails and
  raises a tripwire exception when triggered; in default parallel mode the agent may already have spent tokens or
  run tools before an input tripwire fires, while blocking mode stops it first ([docs][oai-guardrails]). The same
  idea turned into an eval: feed known-bad inputs and assert the tripwire fires.
- **Canary and sentinel tests** (a fixed known-answer probe that must always pass or always fail) are a common
  practice name, but no first-party definition was read in this pass; not claimed here.

### A practitioner protocol (one project's report)

A practitioner from another project (2026-11-24, unverified beyond that project) reports one check and proposes a
protocol around it; treat both as one team's experience, not a standard.

Reported: a manual mutation probe. Eight hand-picked bugs were injected one at a time in a throwaway worktree, and
the tests caught all eight (the report says the sample was hand-picked and is not a coverage claim). The same report
found a source-text test that could never fail: a case-insensitive pattern also matched a longer look-alike name,
fixed by anchoring the pattern and checking that the test now fails.

Proposed, not reported as practised:

1. Commit the new tests alone first (RED) and require each to fail by assertion, not by a syntax or setup error.
2. Record that commit; implement (GREEN) with the test directory unchanged, checked by a diff of the test paths since
   the RED commit being empty.

The adds over the primary sources are the read-only-tests rule (it would stop an agent from weakening a test to get
green) and the RED-commit record. Whether to enforce it with a hook is a settings decision for the repository owner.

## How Agents Use Them

- **Coding agents as test consumers.** The Ralph loop already uses TDD red-green-refactor markers as its stop
  condition and notes it has no BDD switch: see [CC-ralph-enhancement-research.md](../cc-native/agents-skills/CC-ralph-enhancement-research.md).
  The discipline ladder maps TDD's red-green-refactor to a per-task stop condition and BDD's Given-When-Then to
  task boundaries: [agentic-engineering-disciplines-landscape.md](agentic-engineering-disciplines-landscape.md).
- **Agents writing tests first.** The test-first order protects against an agent writing tests that merely mirror its
  own implementation; the RED-first and read-only rules above are the controls. This is our synthesis, not a measured
  result.
- **Agents writing property tests.** The Hypothesis team published a paper and a Claude Code command in which Claude
  writes and runs Hypothesis tests and found real bugs in numpy, pandas and other packages (their own report, linked
  from the [Hypothesis articles page][hyp-articles], read 2026-11-27; the linked paper itself was not read).
- **Agents as the system under EDD.** [Evaluation-data catalog][eval-cat] lists the graders and datasets;
  `/claude-api build-eval` and `hillclimb` are documented there as EDD loops inside Claude Code. For checks that must
  hold when the verifier is itself probabilistic, see
  [agent-probabilistic-verification-analysis.md](agent-probabilistic-verification-analysis.md).

## Not Included

- **QuickCheck origin paper** (Claessen and Hughes, 2000): the copy found returned binary data and the publisher page
  returned 403; cited only through Hypothesis's own docs.
- **Kent Beck's "Canon TDD"** and the practitioner Medium post "From TDD to EDD": both returned 403 to the browser
  tier; Fowler's page (which summarises Beck) stands in. Wikipedia and GeeksforGeeks were read only as secondary
  sources; GeeksforGeeks is not cited.
- **Mutation testing cost and score thresholds**: no first-party benchmark read; none stated.
- **Seeded random generators as a stand-in for a PBT library** (from the practitioner lead): not verified against
  any library docs, so dropped.
- **Other eval vendors' EDD posts** (Braintrust, DeepEval): already cited in the
  [existing section](evaluation-data-resources-landscape.md#why-this-catalog-exists-edd-as-methodology).

## Sources

| Source | Used for |
|---|---|
| [arXiv 2411.13768 abstract][arxiv-abs] | EDDOps paper: title, dates, abstract (read 2026-11-27) |
| [arXiv 2411.13768v2 HTML][arxiv-html] | Process model, architecture, MLR counts |
| [LangChain: What is EDD?][lc-edd] | Three-step practice (vendor blog) |
| [Airbnb: EDD lessons][airbnb-edd] | Principles, calibration, production sampling (company blog) |
| [Martin Fowler: Test Driven Development][fowler-tdd] | TDD loop and benefits (first-party practitioner page) |
| [Dan North: Introducing BDD][north-bdd] | BDD origin |
| [Cucumber Gherkin reference][gherkin] | Executable-specification format |
| [Wikipedia: TDD][w-tdd], [Wikipedia: BDD][w-bdd] | Secondary context only |
| [Hypothesis docs][hyp-docs], [site][hyp-site], [articles][hyp-articles] | PBT definition, agent-written tests |
| [Stryker][stryker], [PIT][pit], [mutmut][mutmut] | Mutation testing |
| [OpenAI Agents SDK guardrails][oai-guardrails] | Guardrail tripwires |

[sdd]: ../non-cc/frameworks/spec-driven-frameworks-landscape.md
[oai-guard]: ../non-cc/frameworks/openai-agents-sdk-analysis.md#guardrails
[eval-cat]: evaluation-data-resources-landscape.md
[arxiv-abs]: https://arxiv.org/abs/2411.13768
[arxiv-html]: https://arxiv.org/html/2411.13768v2
[lc-edd]: https://www.langchain.com/blog/what-is-eval-driven-development
[airbnb-edd]: https://airbnb.tech/ai-ml/eval-driven-development-lessons-from-evaluating-genai-at-scale/
[fowler-tdd]: https://martinfowler.com/bliki/TestDrivenDevelopment.html
[north-bdd]: https://dannorth.net/blog/introducing-bdd/
[gherkin]: https://cucumber.io/docs/gherkin/reference/
[w-tdd]: https://en.wikipedia.org/wiki/Test-driven_development
[w-bdd]: https://en.wikipedia.org/wiki/Behavior-driven_development
[hyp-docs]: https://hypothesis.readthedocs.io/en/latest/
[hyp-site]: https://hypothesis.works/
[hyp-articles]: https://hypothesis.works/articles/
[stryker]: https://stryker-mutator.io/docs/
[pit]: https://pitest.org/
[mutmut]: https://mutmut.readthedocs.io/en/latest/
[oai-guardrails]: https://openai.github.io/openai-agents-python/guardrails/
