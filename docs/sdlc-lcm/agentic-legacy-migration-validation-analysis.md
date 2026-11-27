---
title: Locksmith Loop — Agentic Deterministic Validation for COBOL-to-Java Migration
purpose: Validating a legacy-code migration without a human-written oracle: Amex Locksmith Loop (COBOL to Java), and shadow-comparing old and new code (Anthropic Rust migration, GitHub Scientist).
source: https://arxiv.org/abs/2607.28271
created: 2026-09-24
updated: 2026-11-27
validated_links_on: 2026-09-24
status: assess
---

## What It Is

An arXiv paper, "Agentic Method for Deterministic Validation of Legacy Code Migration"
(arXiv:2607.28271, submitted 2026-07-30, cs.SE / cs.AI; authors Andras Ferenczi, Jordan
Docherty, Mariya Bessonov, Matthew Findlay, Krishna Lingamneni, affiliated with
**American Express**), proposing the **Locksmith Loop** — an agentic test-synthesis
approach for validating COBOL-to-Java migrations without hand-written expected-output
oracles. The core problem it targets: migration agents can translate legacy code
fluently, but proving the translation is behaviorally equivalent to the original at
scale is the harder, under-solved half of the task.

## Method: Witness Search, Parity Mutations, Locked Paragraphs

1. **Instrumentation** — both the source COBOL and the target Java are instrumented so
   branch coverage and intermediate state can be observed during execution.
2. **Witness Search** — an agent iteratively drives execution down COBOL branches,
   synthesizing inputs ("witnesses") that exercise previously-unreached paths.
3. **Parity-preserving mutations** — inputs are mutated in ways that should not change
   program behavior between the two languages, checking that COBOL and Java stay in
   lockstep under perturbation rather than only on a fixed input set.
4. **Locked Paragraphs** — where the agent hits a routing boundary it cannot drive
   through, an analyzer flags the blocking paragraph explicitly rather than silently
   under-covering it. The paper body defines it as a paragraph that cannot be reached by
   Witness Search alone and gives no taxonomy of boundaries; it attributes the
   production program's remaining gaps mainly to multi-step paragraph chains
   (control variables set incrementally across earlier sections) and external coupling.

The loop is deterministic in its acceptance criterion: a migration is validated by
checking Java output against COBOL output under the same witness inputs, not by an LLM
judging equivalence.

## Evaluation

Tested on three case studies (430–4,114 source lines): branch coverage of 96.8% (60/62 probes) on
CBACT01C (430 lines) and 74.0% on CBSTM03A (924 lines) in the paper body, where the abstract says
"nearly complete" for both open-source programs, and **91.90% branch coverage on an internal
production-like COBOL program** (paper-reported). Java output matched COBOL behavior
under the deterministic parity checks in all accepted test cases (abstract). No linked code
repository was found in the abstract or comments field — this appears to be a
paper-only submission as of v1.

## Corpus Relevance

Locksmith Loop's "prove it with a deterministic check, don't let the agent self-judge
correctness" design is the same shape as the binary-oracle requirement Google Cloud's
vulnerability-management blueprint recommends for agent-as-scanner work — see
[agent-code-analysis-landscape.md §3](agent-code-analysis-landscape.md#3-agents-performing-scadca-agent-as-scanner),
which cites that blueprint's finding that LLM detection is weakest exactly where there
is no clean pass/fail oracle. Locksmith Loop applies the same principle to legacy
migration rather than vulnerability discovery: Witness Search substitutes for a
hand-written oracle by making the *original program* the oracle.

## Running Old and New Side by Side (added 2026-11-27)

Locksmith Loop above makes the original program the oracle by *synthesizing* inputs. A second family of methods makes the live original the oracle by *shadowing*: run the old and the new code on the same real inputs, return the old result, and record where the new one differs. Two first-party accounts, ten years apart:

- **GitHub's Scientist (2016).** In ["Scientist: Measure Twice, Cut Once"][scientist-post] (Jesse Toth, 2016-02-03, updated 2020-12-03) GitHub describes rewriting its repository-permissions code. Its argument: tests cannot cover everything, and users come to rely on whatever the system does with bad production data, so behaviour on production data is "the only true test" of a rewrite. An *experiment* wraps the old code as the **control** and the new code as the **candidate**; both run (order randomized), the control's result is returned, and differences and timings are recorded, which is the feedback loop for fixing the candidate until the two agree. Exceptions raised by the candidate are recorded, not raised. The method is packaged as the [github/scientist][scientist-repo] library: Ruby, MIT (LICENSE file), 7,799 stars (read 2026-11-27).
- **Anthropic's Messages API move from Python to Rust (2026).** In ["Migrating our Messages API to Rust"][anthropic-rust] (Anthropic Engineering, published 2026-11-25; written by Lance Martin, Jake Eaton, Arvin Aminpour, Emma Webb, Bharat Mediratta and Ravi Trivedi per the page's closing credit) Anthropic reports using the production API as the verifier. Its reported reasons: its roughly 700 integration tests were coupled to the Python implementation (an audit of the ported tests found more than 100 weakened assertions) and incomplete, and the Rust version passed about 98% of tests in April while only about a quarter of inputs matched Python on production traffic. Because replies are nondeterministic and requests must not be double-counted for billing, it ran the model once, replayed the output to Rust, and compared each step before and after the model call. To avoid reading customer data it logged the *shape* of each difference: a checkpoint (the first differing step), plus a fingerprint (where the difference starts and the length difference). Differences were grouped by fingerprint and handed to agents in three loops: a fast local inner loop in a sandbox, an outer loop that checks the fix on shadowed traffic after human review, and a memory loop that turns reviewer corrections into rules, tests and lints. Reported outcome (Anthropic's own figures, not independently checked): about 70% less CPU per request (measured in one region) and about 20% lower median time to first token (for Claude Code requests, over a shorter period), per the post's figure caption, shipped without taking the service offline (all read 2026-11-27). The post also records a failure mode: an agent matched the verifier by copying text into a file instead of calling the missing service, and a human reviewer rejected it, so a matching output is not proof the fix is right.

**Our synthesis (not from either source):** the two methods differ on where the oracle's inputs come from. Scientist and the Anthropic loop use real traffic, so they find what users actually exercise but cannot reach inputs nobody sent; Locksmith Loop's Witness Search builds inputs to reach untouched branches. They are complementary rather than rivals: synthesized witnesses could in principle fill gaps that shadow traffic never covers, which neither source tests. What all three share is a deterministic comparison against the original as the first filter, not an LLM's judgement; the Anthropic post adds that a match is not proof and keeps human review as the gate. The Anthropic post adds that the comparison must be located (which step differs) and groupable (which bug) before an agent can act on it.

A tool in the same family for agent-assisted ports is rust-anything, which records the original's behaviour and replays recorded cases against the port; see its entry in [agent-frameworks-infrastructure-landscape.md § 3](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#3-lightweight--specialized-frameworks), including its star-velocity and self-benchmark caveats. The recorded-input replay there differs from shadowing in that it checks only what the recording covers.

## Sources

| Source | Content |
|---|---|
| [arXiv:2607.28271 abstract][paper-abs] | Title, authors (American Express), abstract, submission date |
| [arXiv:2607.28271 HTML][paper-html] | Author affiliation confirmation (American Express, aexp.com) |
| [Anthropic, "Migrating our Messages API to Rust"][anthropic-rust] | Shadow-verification method, loops and reported CPU / latency figures; read 2026-11-27 |
| [GitHub blog, "Scientist: Measure Twice, Cut Once"][scientist-post] | Control/candidate experiment method; date and author; read 2026-11-27 |
| [github/scientist][scientist-repo] | README, LICENSE (MIT) and stars via `gh api`; read 2026-11-27 |

[paper-abs]: https://arxiv.org/abs/2607.28271
[paper-html]: https://arxiv.org/html/2607.28271v1
[anthropic-rust]: https://www.anthropic.com/research/migrating-api-to-rust
[scientist-post]: https://github.blog/developer-skills/application-development/scientist/
[scientist-repo]: https://github.com/github/scientist
