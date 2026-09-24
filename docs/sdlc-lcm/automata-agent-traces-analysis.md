---
title: Automata from Agent Traces — FSM Reconstruction for Failure & Next-Step Prediction
purpose: Reconstructing a compact finite-state machine from LLM-agent trace corpora to predict failures and next steps, and to audit agent behavior independent of the underlying model.
source: https://arxiv.org/abs/2608.23670
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

An arXiv paper, "Automata from Agent Traces: Failure and Next-Step Prediction"
(arXiv:2608.23670v1, submitted 2026-08-24, cs.AI / cs.CL / cs.LG; authors Seonglae Cho,
Franklin Cardenoso Fernandez, Umar Mohammed, Zekun Wu, Kleyton Da Costa, Ilham
Wicaksono, Adriano Koshiyama), addressing the opacity of LLM-agent behavior by building
**a single, compact finite-state machine (FSM)** that serves as a structural substrate
recovered from a corpus of agent execution traces, rather than treating each trace as an
opaque sequence to be modeled statistically end to end.

## Method & Results

The FSM is fit per task family on a corpus of traces, then evaluated against a held-out
portion of the trace data. Reported results across twelve datasets (paper-claimed):

- FSMs with **7–43 states** replay held-out trace data at **≥0.997 fitness**.
- **Held-out AUROC up to 0.94** for failure detection — the FSM's structure alone
  predicts whether a run is heading toward failure.
- Superior next-step prediction compared to the baselines the paper compares against.

The headline interpretive claim: "behavioral topology appears shaped more by the
deployment harness than by the LLM" — i.e. the recovered automaton reflects how the
agent scaffold constrains and sequences actions more than which model is plugged into
it. That framing is what makes the method **model-agnostic**: the same FSM-extraction
approach is proposed as a safety-auditing and runtime-monitoring tool independent of
which LLM backs a given agent deployment.

## Corpus Relevance

This is a structural, harness-level companion to
[agent-silent-failure-taxonomy-analysis.md](agent-silent-failure-taxonomy-analysis.md)'s
production case study of silent failures in an LLM agent runtime: where that doc derives
a taxonomy of failure *classes* from an 8-week longitudinal study, this paper proposes a
mechanism — FSM fitness and AUROC — that could in principle *detect* a run drifting
toward one of those classes before it completes, from trace structure alone rather than
from output inspection.

## Sources

| Source | Content |
|---|---|
| [arXiv:2608.23670 abstract][paper-abs] | Title, authors, abstract, submission date, subject categories |

[paper-abs]: https://arxiv.org/abs/2608.23670
