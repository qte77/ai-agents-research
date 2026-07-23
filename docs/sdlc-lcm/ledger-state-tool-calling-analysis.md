---
title: LedgerAgent — Structured State for Policy-Adherent Tool-Calling Agents
purpose: Ledger-state tracking and pre-execution policy gating for tool-calling agents
source: https://arxiv.org/abs/2606.20529
created: 2026-07-23
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Assess

## What It Is

LedgerAgent is an inference-time method for building policy-adherent,
tool-calling customer-service agents. Instead of requiring the agent to
reconstruct task state by re-reading raw conversation and tool-call history
each turn, it maintains a separate structured **ledger** — observed facts,
identifiers, constraints, and conditions pulled from successful tool
returns — and re-renders that ledger into the prompt every turn. A
deterministic **policy gate** then checks any environment-changing tool call
against the ledger's state-dependent policy constraints *before* execution,
blocking calls that are syntactically valid but policy-violating.

## Problem Framing

Standard prompt-based tool-calling agents can ground a decision in stale,
missing, or incorrect state even when the correct facts were retrieved
earlier in the same conversation — the model has to re-derive state from
free-text history on every turn, and that reconstruction is where policy
violations creep in. LedgerAgent's premise is that separating **state
storage** (the ledger) from **state use** (the policy gate check) removes
that reconstruction step as a failure mode.

## Mechanism

- **Ledger**: a structured record, updated from tool-call results, that
  persists facts/identifiers/constraints/conditions across turns and is
  injected into the prompt rather than left implicit in conversation history.
- **Policy gate**: a check that runs before any state-changing tool call
  executes, validating the call against the current ledger contents and
  blocking violations deterministically rather than relying on the model to
  self-police policy compliance.

## Results

The method was evaluated across four customer-service domains using a mixed
panel of open-weight and closed-weight models, reporting an improved average
pass rate over a standard prompt-based tool-calling baseline. The paper states
the largest reported gains show up under stricter multi-trial consistency
metrics (repeated-trial/pass^k-style scoring) rather than single-shot pass
rate — i.e., the ledger + policy gate combination appears to buy more
consistency across repeated trials than a one-shot accuracy bump.

The specific four domains, the exact model list, and numeric pass-rate deltas
are not stated in the abstract/summary and are not asserted here; confirming
them would require pulling tables from the full paper body rather than the
abstract.

## Corpus Relevance

No hand-authored doc in this corpus currently covers ledger-based state
tracking or pre-execution policy gating for tool-calling agents specifically
— the only prior mention is the auto-generated
`docs/research/rxiv-agentic-papers.md` index stub, which per
[CONTRIBUTING.md](../../CONTRIBUTING.md#auto-generated-content) does not count
as coverage. The closest topically-adjacent `docs/sdlc-lcm/` docs (agentic
SDLC patterns, goal/attribution tracking, MAS design principles, agent
evaluation metrics) address different concerns and are not cross-referenced
here.

## Sources

| Source | Content |
|---|---|
| [LedgerAgent (arXiv:2606.20529)][ledgeragent] | Abstract/summary — ledger + policy-gate mechanism, evaluation setup, CC BY 4.0 license |

[ledgeragent]: https://arxiv.org/abs/2606.20529
