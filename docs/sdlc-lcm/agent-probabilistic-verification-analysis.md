---
title: Probabilistic Verification for AI Agent Security Policies
purpose: Analysis of a Datalog-based, distributionally-robust runtime-verification framework that replaces brittle binary policy thresholds with sound probabilistic bounds on agent policy violation.
source: https://arxiv.org/abs/2606.20510
created: 2026-07-23
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Assess

## What It Is

["Efficient and Sound Probabilistic Verification for AI Agents"][paper] (arXiv:2606.20510, v1,
2026-06-18) is a Google DeepMind / Google / UPenn / UW-Madison paper introducing a sound, efficient
runtime-verification framework for AI-agent security policies written in Datalog. Authors: Alaia
Solko-Breslin (Google DeepMind + UPenn), Pramod Kaushik Mudrakarta (Google DeepMind), Mihai
Christodorescu (Google), Somesh Jha (Google + UW-Madison), Krishnamurthy Dj Dvijotham (Google
DeepMind).

The core problem: existing reference monitors binarize probabilistic predicates (e.g. PII
detectors, declassifiers) at a fixed threshold and evaluate them independently, which silently
drops correlation between predicates and produces false-negative verdicts. The paper's motivating
example (Fig. 1) shows a FORGE-style deterministic policy binarizing two correlated 0.45/0.25
message-relevance probabilities to `False` independently, yielding an incorrect "Authorized"
verdict where the correct aggregate is "Unauthorized."

## Method

1. Compile an agent execution trajectory into a Datalog **derivation graph** (fact nodes + rule
   nodes).
2. Embed the graph's Boolean logic into multilinear polynomial constraints over `[0,1]`.
3. Pose the exact worst-case policy-violation probability as an exponentially-sized LP over joint
   probability measures (Eq. 1) — this makes no independence assumption between correlated
   predicates.
4. Relax the LP to a polynomially-sized **semidefinite program (SDP)** that tracks only
   second-order moments, proven to yield a sound upper bound on violation probability (Sec. 4
   theorem).
5. Solve the SDP at runtime with the Splitting Conic Solver ([O'Donoghue et al. 2016][scs]) under
   a 15-second inline-enforcement timeout, falling back to looser bounds on non-convergence.

## Threat Model

Standard security-reference-monitor model (Anderson 1972, Sec. 2.3): an attacker can influence
agent instructions/data — including indirect prompt injection — but cannot bypass or disable the
monitor, modify the policy, or invalidate the paper's own probabilistic tool-failure assumptions.

## Results

Evaluated on three benchmark suites: Intercode-NL2Bash (197 trajectories), ATBench (377
trajectories), and 6 side-channel-vulnerability tasks adapted from Praline (register-allocation
crypto leaks). Baselines: Praline's own SCIP+Z3 engine, a 10,000-sample Monte Carlo sampler
(assumes independence), and a deterministic reference monitor swept across thresholds 0.1-0.9.

At medium security threshold (τ=0.5, Table 2): the SDP verifier hits Utility=1.000/Security=1.000
on both Intercode and ATBench, versus the deterministic monitor's Security=0.702 (Intercode) and
0.950 (ATBench). On the Praline side-channel tasks the SDP matches Praline's own soundness
(Security=1.000) while attaining full utility, at higher average latency than Praline's
purpose-built solver (Table 3).

## License and Availability

The arXiv abs page lists **CC BY 4.0** as the submission license; the PDF's own page-1 footer
separately states "© 2026 Google. All rights reserved." Both are first-party but not reconciled
in the paper itself — stated here as-is rather than resolved. No code or artifact repository link
was found anywhere in the paper; this is a paper-only publication (no GitHub repo).

## Corpus Relevance

This is a **runtime-verification / reference-monitor technique**, distinct from the
threat-taxonomy and vulnerability-scoring material already in this directory:
[mas-security-framework.md](mas-security-framework.md) covers OWASP MAESTRO's 7-layer threat
*taxonomy*, and [agentic-ai-vulnerability-landscape.md](agentic-ai-vulnerability-landscape.md)
covers AIVSS scoring and MITRE ATLAS incident tracking — both catalog threats/incidents rather
than formally bound policy-violation probability at runtime. This doc is a new sub-topic
(Datalog-based reference monitors + distributionally-robust risk bounds), not an extension of
either.

## Sources

| Source | Content |
|---|---|
| [arXiv:2606.20510 abs page][paper] | Paper abstract, license (CC BY 4.0), submission metadata |
| [arXiv:2606.20510 PDF][paper-pdf] | Full method (Sec. 4), threat model (Sec. 2.3), results (Table 2-3) |
| [Splitting Conic Solver][scs] | Runtime SDP solver used for inline enforcement |

[paper]: https://arxiv.org/abs/2606.20510
[paper-pdf]: https://arxiv.org/pdf/2606.20510
[scs]: https://github.com/cvxgrp/scs
