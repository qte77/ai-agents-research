---
title: Locksmith Loop — Agentic Deterministic Validation for COBOL-to-Java Migration
purpose: American Express's agentic test-synthesis method for validating COBOL-to-Java legacy code migrations without a human-written oracle.
source: https://arxiv.org/abs/2607.28271
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

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
   under-covering it. The abstract names the concept but does not enumerate which kinds
   of boundaries qualify — that detail would need a read of the full paper body.

The loop is deterministic in its acceptance criterion: a migration is validated by
checking Java output against COBOL output under the same witness inputs, not by an LLM
judging equivalence.

## Evaluation

Tested on three case studies (430–4,114 source lines): near-complete branch coverage on
two open-source COBOL programs, and **91.90% branch coverage on an internal
production-like COBOL program** (paper-reported). Java output matched COBOL behavior
under the deterministic validation checks for the covered branches. No linked code
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

## Sources

| Source | Content |
|---|---|
| [arXiv:2607.28271 abstract][paper-abs] | Title, authors (American Express), abstract, submission date |
| [arXiv:2607.28271 HTML][paper-html] | Author affiliation confirmation (American Express, aexp.com) |

[paper-abs]: https://arxiv.org/abs/2607.28271
[paper-html]: https://arxiv.org/html/2607.28271v1
