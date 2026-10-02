---
title: Jev (TypeSafe AI) — System-One Decision Model
purpose: What Jev is (question types, pricing, limits) and the qte77/feelings measured pilot using it as a pre-CI code-review gate.
created: 2026-09-30
updated: 2026-10-02
validated_links: 2026-09-30
status: trial
---

## What It Is

Jev is TypeSafe AI's "System One" model: instead of generating text, it answers a typed
question against a `state` input and returns a machine-consumable result with a
probability, eliminating text parsing ([docs.typesafe.ai][typesafe-home]). It supports
three question types, verified at [docs.typesafe.ai/api][typesafe-api] on 2026-09-30:

| Type | Purpose | Returns |
|---|---|---|
| `noul` | "Is this statement true?" | `noul`, a 0–1 probability (no `confidence` field) |
| `choice` | Pick one option from a list | `choice` (highest-probability option), `probabilities` (every option, sums to 1), `confidence` |
| `score` | Score the state on a rubric | `score` (probability-weighted, can land between levels), `legend`, `probabilities`, `confidence` |

TypeSafe's own fit guidance: Jev works best for atomic questions, composed in code —
well-scoped, single-factor evaluations. For a complex decision, decompose it into several
atomic questions and combine the results in application logic, rather than asking Jev to
weigh multiple factors in one call.

## Pricing and Limits

Verified at [docs.typesafe.ai/models][typesafe-models] on 2026-09-30 — re-check before
relying on these; TypeSafe states its own limits "can change without notice":

- Model: `jev-1.13.0`; the `jev-latest` and `jev-preview` aliases both currently point to it.
- Input tokens cost $0.042 per million ($42 per billion); output tokens are free.
- 64k tokens per request (the `state` plus every question combined); 32k tokens for the
  `state` plus the single longest question.
- Rate limits: 100k tokens/second and 40 requests/second, but "Rate limits are adjusting
  dynamically. We are serving a very large volume of demand, and the limits above can change
  without notice while we do."

## Measured: Pre-CI Code-Change Gate

[qte77/feelings][feelings-fork], a fork of [BoundaryML/feelings][feelings-upstream] (its
BAML `.fill<T>()` side is covered in [§8 of the frameworks landscape][frameworks-8]),
tested Jev as a cheap pre-CI review gate. The numbers below are read from the fork's own
`site/data/results.json` and `ytdlp.json`, not the page's summary prose — both files and
the [results page][feelings-results] are first-party for the *pilot's own measurements*,
not for Jev itself.

- **184 labelled changes, four public qte77 repos** (59 clean, 125 flawed), scored with
  four `noul` questions per change (scope creep, unused abstraction, duplicated code,
  weakened tests). Per-question ROC-AUC ranged 0.89–0.99.
- **At the shipped 0.70 threshold:** caught 78% of the flawed changes and wrongly flagged
  1 of the 59 clean ones (1.7%), in a p95 of about 0.3 s (278 ms) and about $0.0001 per
  check (per-call cost $0.0001165).
- **Against Claude on the same changes and questions:** Haiku 4.5 averaged 0.90 ROC-AUC
  and wrongly flagged 12% (11.9%); Sonnet 5 averaged 0.96; Opus 5.5 averaged 0.97 and
  caught 98%. Jev ran about 70x faster than the fastest Claude tested (Opus, 19.1 s p95)
  and about 80x cheaper than the cheapest (Haiku, $0.0092/check).
- **BAML vs. the plain Python SDK:** identical requests; the two setups' per-question AUC
  never differed by more than 0.0165 ("within 0.02").
- **Held-out codebase (yt-dlp, 120 changes):** the ranking mostly held (per-question AUC
  0.82–0.99), but the fixed 0.70 threshold did not transfer — it wrongly flagged 23–30% of
  clean changes (vs. 1.7% on the repos it was tuned on). Each codebase needs its own setting.
- **Lesson — ask about what is *in the input*.** "Does this change add ... that is used
  only once?" needs whole-codebase knowledge Jev doesn't have. Rewording it to "...that
  nothing else in the diff uses?" — answerable from the diff alone — cut that question's
  false-positive rate from 6.7% to 0% on the same 60-fixture set and raised its AUC from
  0.921 to 0.939 ([pilot plan][feelings-plan]).

## When It Fits, and When It Doesn't

It fits routing and yes/no decisions repeated on every line, message, or loop step — the
pilot's four independent per-change checks. It doesn't fit generating text, or a decision
that needs context outside what's in the `state` — the single-use-abstraction lesson above
is the same failure mode TypeSafe's own fit guidance warns about.

## Build for When It's Wrong

Run it non-blocking: an uncertain ("maybe") answer should pass, never reject. TypeSafe's
Cloudflare WAF blocked 4 of the pilot's 60 fixtures (2 source commits, each as its clean
and flawed version) with a repeating 403 on 2026-09-23; the same fixtures passed with 0
errors across 300 requests the next day ([pilot plan][feelings-plan]). Treat a block as its
own outcome — fall back to the slower path, never treat a block as a verdict.

## Rubric

Scored against the [agent substrate rubric][rubric]. Jev is a stateless per-request
classifier API, not a persistent store, so **Shared** and **Versionable** are marked `n/a`.

`subject: harness`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| n/a (stateless per-request API; no shared store for multiple agents to read/write) [docs.typesafe.ai/api][typesafe-api] | partial (hosted multi-tenant service — "serving a very large volume of demand" — but no documented multi-node deployment for a self-run client) [docs.typesafe.ai/models][typesafe-models] | partial (a pinnable versioned model, `jev-1.13.0`, but the default `jev-latest`/`jev-preview` aliases drift, and no decoding-determinism guarantee is documented) [docs.typesafe.ai/models][typesafe-models] | yes (three question types — `noul`/`choice`/`score` — cover yes/no, multi-option and rubric-scored decisions without a schema rewrite) [docs.typesafe.ai/api][typesafe-api] | n/a (no persistent user-owned state to snapshot, diff or roll back; only the model release itself is versioned) [docs.typesafe.ai/models][typesafe-models] | no (returns a probability/confidence, not a citation or audit trail; self-reported confidence is not traceability) [docs.typesafe.ai/api][typesafe-api] |

`scored 2026-09-30`

## Cross-References

- [code-review-products-landscape.md](code-review-products-landscape.md) — SaaS PR-review
  products; alibaba/open-code-review is the nearest hybrid deterministic + LLM comparison
- [agentic-sdlc-patterns.md § 4][sdlc-4] — the "no review agent" gap this pilot fills
- [agent-frameworks-infrastructure-landscape.md § 8][frameworks-8] — BAML's `feelings`
  (`.fill<T>()`) integration with Jev, and Laya as the open-weight alternative
- [system-1-decision-models-landscape.md](../reference/system-1-decision-models-landscape.md) —
  open-weight and research alternatives (Laya, kev, CLM, GLiNER2.5-Decide, RuVector) and tools built on
  Jev (probably, abide, jev-ultrafast, jevgrep)

## Sources

| Source | Content |
|---|---|
| [TypeSafe docs][typesafe-home] | "System One" framing, fit guidance |
| [TypeSafe API reference][typesafe-api] | Question types and returned fields |
| [TypeSafe models page][typesafe-models] | Model IDs, pricing, token limits, rate limits |
| [qte77/feelings results page][feelings-results] | Published pilot results (human-readable) |
| `site/data/results.json`, `site/data/ytdlp.json`, qte77/feelings@main (no URL — read via `gh api repos/qte77/feelings/contents/...`) | Raw pilot numbers cited above |
| [qte77/feelings pilot plan][feelings-plan] | Reword-lesson and WAF-block measurements |
| [BoundaryML/feelings][feelings-upstream] | Upstream repo the pilot forked |
| [Agent substrate rubric][rubric] | Six-property scoring rubric applied above |

[typesafe-home]: https://docs.typesafe.ai/
[typesafe-api]: https://docs.typesafe.ai/api
[typesafe-models]: https://docs.typesafe.ai/models
[feelings-fork]: https://github.com/qte77/feelings
[feelings-upstream]: https://github.com/BoundaryML/feelings
[feelings-results]: https://qte77.github.io/feelings/
[feelings-plan]: https://github.com/qte77/feelings/blob/main/docs/plans/2026-09-23-0001-jev-coding-gate-pilot.md
[sdlc-4]: ../../sdlc-lcm/agentic-sdlc-patterns.md#4-agent-first-developer-toolchain-amplify-partners
[frameworks-8]: ../frameworks/agent-frameworks-infrastructure-landscape.md#8-output-validation-guardrails--verification
[rubric]: ../../sdlc-lcm/agent-substrate-rubric.md
