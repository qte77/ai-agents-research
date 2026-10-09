---
title: System-1 Decision Models Landscape
purpose: Survey open-weight, research, independent, and major-vendor alternatives to TypeSafe's Jev — fast, typed-output classifiers (choice/score/noul answers, calibrated probabilities, one forward pass, no free text) used for agent routing, guardrails, and verification — scored against the agent substrate rubric where the model's deployment path makes that possible.
created: 2026-09-30
updated: 2026-10-09
validated_links: 2026-10-09
status: assess
---

## What It Is

TypeSafe's Jev popularized the **system-one decision model**: instead of a full LLM call that
generates prose an application then parses back into a branch, a system-one model answers a
*typed* question — yes/no (`noul`), multiple-choice (`choice`), or a rating (`score`) — over a
short state (a ticket, a diff, a page) in a single forward pass, returning a calibrated
probability and nothing else. There is no free text, so there is nothing to hallucinate, and the
call is far cheaper and faster than a reasoning-model round trip. Jev itself is TypeSafe's hosted
model ([docs.typesafe.ai][typesafe]); its API, pricing and a measured pre-CI review-gate pilot
are analyzed in [jev-analysis.md](../infrastructure/jev-analysis.md).

September 2026 saw a wave of open-weight, research, and independent projects that reproduce or
build on Jev's interface (the entries below), tracked as [issue #517][issue-517] / plan row J3.
Classifier-style guardrails already covered in this corpus — Llama Guard, ShieldGemma,
Bespoke-MiniCheck — are cross-referenced rather than repeated; see
[agent-frameworks-infrastructure-landscape.md §8 Output Validation][frameworks-8].

Every score below follows the [agent substrate rubric][rubric]; licenses are confirmed against
each repository's own `LICENSE` file, not GitHub's license-detection metadata alone.

Whether an act/abstain decision can be trusted is a calibration question; for the Brier-score metric and why stated confidence and committed action can diverge, see [agent-evaluation-metrics-landscape.md § Verbalized Confidence Calibration](../../sdlc-lcm/agent-evaluation-metrics-landscape.md#verbalized-confidence-calibration-brier).

## Use cases

Where this corpus finds a system-1 decision model actually wired into an agent loop, by use
case — each bullet sourced to the tool's own README, docs, or paper where noted `(documented)`
or `(shipped)`, or to an existing, already-verified corpus analysis of one. Jev's own docs
(re-fetched 2026-10-09) stay mostly generic about downstream use — except for confidence-gated
action (§6 below), which [docs.typesafe.ai/confidence][typesafe-confidence] documents directly.
Fastino's [GLiNER2.5-Decide announcement][gliner-blog] independently names several of these use
cases under its own bolded labels, quoted verbatim per use case.

### 1. Model routing

**Decision shape**: a discrete choice among destinations/models, with a probability and
confidence per choice.

- [GLiNER2.5-Decide][gliner-blog] (documented) — its own "Model routing" bullet: "Route requests
  by destination, complexity, or escalation level and return the selected route with
  probabilities and confidence scores."
- [OpenAI Decisions API][openai-decisions-guide] (documented) — its own guide names the use case:
  "Use those answers to classify content, route requests, and prioritize work in your
  application." Its own worked example, "Route a customer complaint," asks one `choice` question
  ("Which department should handle this complaint?") over four options
  (`billing`/`technical`/`shipping`/`other`) — routing to a department, the same shape already
  noted below for RuVector, not a worked example of choosing between LLMs.
- [Perplexity Decisions API][pplx-ticket-triage] (documented) — its own ticket-triage cookbook
  feeds three questions (a `noul`, a seven-option `choice`, and a `score`) per support ticket into
  threshold logic that sorts tickets into `escalate`/`review`/`queue`/`auto_reply`/`close`; only
  `escalate` tickets are then handed to a *second*, more capable system (the Agent API) for an
  investigation plan — escalation-based routing to one fixed downstream system, the same pattern
  already described above for the Panhwar cascade, not a choice among several candidate models.
- [RouteLLM][routellm-home] and [Not Diamond][notdiamond-home] (shipped) — classifier-trained
  per-query routers, already cataloged in
  [llm-routers-gateways-landscape.md § Open / Self-Hostable Gateways][llm-routers-open] and
  [§ Hosted Aggregators][llm-routers-hosted]; cross-referenced here, not duplicated. Neither uses
  a `noul`/`choice`/`score` API.
- Practitioner report (self-reported, not independently verified) — Muhammad Waseem Panhwar's
  LinkedIn post of 2026-10-08 (plain text, LinkedIn blocks link checkers:
  `linkedin.com/posts/panhwerwaseem_i-just-put-a-web-crawler-inside-claude-share-7513930132773068801-9uVv`)
  describes Jev as the cheap first stage of a cascade: "crawler → jev asks 8 questions → grok 4.7
  reads only what changed → claude writes the fix → i approve". A nightly crawl of 1,860 pages
  (docs, changelogs and pricing of 37 tools) gets 8 typed questions per page ("did it change, yes
  or no. does it touch my setup, pick one. how urgent, score 1 to 10"); the author reports
  "14,880 decisions, done in 11.2 seconds for $0.29", with "1,791 pages ... dropped by code, no
  model call at all. 55 go to grok 4.7. 11 reach claude. 3 come to me". This is routing by
  escalation rather than by model choice: Jev's answers decide whether a costlier model sees the
  page at all, and a human still approves "anything that touches my keys or my money" (§6).
- **Gap, narrowed but not closed**: re-checked 2026-10-09 — `docs.typesafe.ai`'s home, `/api`, and
  `/models` pages name no use case that selects *between other LLMs*; the only "routing" sentence
  found is in `/models` § Language support ("pay close attention to Confidence when routing"
  non-English content), a caution about Jev's own accuracy, not model selection. The corpus
  entries above for Laya, kev, CLM, and RuVector likewise describe no router-to-other-LLMs use.
  Two major vendors now name "routing" as a use case for their own Jev-style APIs — OpenAI's guide
  and Perplexity's cookbook, both above — but both worked examples route to a fixed internal label
  set (a department, or an escalate/review/queue/auto_reply/close bucket), not to a choice among
  several candidate models. No system-1 decision model checked in this corpus, vendor or
  independent, documents selecting *which model* should answer a request. The nearest matches
  already in this doc are narrower still: Laya's `Router` class picks among Laya's *own* three
  checkpoints (not other LLMs), and RuVector's decision layer classifies support tickets into a
  fixed department label set (77.3–84.0% accuracy) rather than routing between models.

### 2. Guardrails (block / grant)

**Decision shape**: a binary accept/reject (`noul`), or a hazard-category `choice`.

- [GLiNER2.5-Decide][gliner-blog] (documented) — its own "Guardrails" bullet: "Evaluate safety,
  harm type, and escalation together, extracting harmful spans verbatim. Apply constraints when
  combinations of answers would be contradictory."
- Established safety classifiers and policy engines (shipped) — Llama Guard, ShieldGemma,
  Guardrails AI, NeMo Guardrails, LLM Guard; see
  [agent-frameworks-infrastructure-landscape.md § Guardrails / policy][guardrails-policy].
- [abide][abide-home] (shipped) — asks Jev one typed question per AGENTS.md rule on every edit
  or turn and has the agent repair the break in the same turn.
- Jev's own pre-CI pilot (observed) — [jev-analysis.md § Measured: Pre-CI Code-Change Gate][jev-pilot]:
  caught 78% of flawed changes at a 1.7% false-positive rate on the repos it was tuned on, but a
  fixed threshold wrongly flagged 23–30% of clean changes on a held-out codebase.
- **Failure mode**: fail open, not closed. Abide's own README documents no fallback behavior for
  an outage or missing key (re-checked 2026-10-09; the fail-open risk is this corpus's own
  analysis in [CC-community-tooling-landscape.md § abide][abide-home], not an abide-stated
  guarantee); Jev's own design guidance is to [run it non-blocking][jev-wrong]
  (jev-analysis.md § Build for When It's Wrong).

### 3. Tool-call gating

**Decision shape**: a `choice` among a fixed action/tool vocabulary (what GLiNER2.5-Decide and
jev-ultrafast document), distinct from an allow/deny verdict on an already-formed call (what
Adrian documents).

- [jev-ultrafast][jevultrafast-home] (shipped) — each step asks Jev to pick an operation
  (`CLICK`, `TYPE_TEXT`, `SELECT`, `SCROLL_UP`, `SCROLL_DOWN`, `WAIT`, `DONE`, `BLOCKED`) and a
  target, replacing per-step LLM reasoning with one typed decision. Its own hedge: "three repeats
  of one task on one browser profile, not a general reliability benchmark."
- [GLiNER2.5-Decide][gliner-blog] (documented) — its own "Tool calling" and "Browser and computer
  use" bullets: "Select from a permitted set of tools and capture arguments from the request as
  structured records" and "Evaluate the current state to select the next action. Represent the
  action, target, and parameters as a structured record."
- [Secure Agentics Adrian][adrian-home] (shipped, not Jev-family — a bundled local Gemma
  classifier, not a `noul`/`choice`/`score` API) — the clearest first-party match for gating a
  *proposed* call rather than picking one: per its README, "every tool call is classified in real
  time, with risky actions blocked or held for your approval."
- [Perplexity Decisions API][pplx-action-gate] (documented) — Perplexity, not a Jev-family clone,
  is the first entry in this corpus to document this gap's exact pattern for *any* Jev-style
  (`noul`/`choice`/`score`) model: an agent proposes a function call (its example is
  `schedule_payment`), `pplx-decider-v1.1-27b` scores three `noul` questions about it (policy
  compliance, record match, reversibility), and application code applies ordered thresholds to
  allow, ask a human, or block. Per the cookbook: "Only your code allows, asks about, or blocks
  anything." It hedges its own thresholds as "starting points, not validated production values."
- [Perplexity Decisions API][pplx-browser-agent] (documented) — its own browser-agent cookbook
  documents the *pick-next-action* shape instead (alongside jev-ultrafast and GLiNER2.5-Decide
  above): six questions (`noul`/`choice`/`score`) per step choose click/dismiss/scroll/stop; "the
  model never clicks anything," and ordered thresholds in application code turn probabilities into
  the action. Its own measurement: "Our runs took 16 to 22 seconds, most of it page loads and the
  1.5 second pause per decision" over a 5-step run.
- OpenAI's DevDay 2026 recap (announced, not documented in its own technical guide) — only the
  recap names a fourth use case: "get back answers they can use to classify content, route
  requests, or choose an agent's next action." No worked example of choosing a next action appears
  in the Decisions API guide itself, so treat this as an announced, not yet documented, use case.
- **Gap, now partly filled**: this Gap originally found no *Jev-family* model's own docs (Jev
  itself, plus its open-weight/independent clones: Laya, kev, CLM, RuVector, GLiNER2.5-Decide,
  JevK5, SemIf) describing a classic approve/deny gate on an already-formed tool call. As of
  2026-10-09, Perplexity's action-gate cookbook above is the first first-party documentation of
  that exact pattern for a Jev-style (`noul`/`choice`/`score`) model — but it's Perplexity's own
  cookbook, not a Jev-family model's docs, so the gap for the Jev-family proper is unchanged.
  Every other entry in this section, Jev-family and vendor alike, still mostly picks *which*
  action to take rather than gating one already formed (jev-ultrafast, GLiNER2.5-Decide,
  Perplexity's own browser-agent cookbook, OpenAI's announced-only "next action") — a related but
  distinct decision shape from Adrian's and Perplexity's action-gate pattern.

### 4. Reranking (by query, by probability)

**Decision shape**: sort candidates by a returned score or probability.

- Dedicated cross-encoder rerankers (shipped) — Cohere Rerank, bge-reranker-v2-m3, Qwen3-Reranker,
  mxbai-rerank, FlashRank, rerankers, Voyage/ZeroEntropy/Contextual/Jina; see
  [agent-frameworks-infrastructure-landscape.md § Rerankers][rerankers]. None use the typed
  `noul`/`choice`/`score` interface this page tracks.
- [jevgrep][jevgrep-home] (shipped) — the closest system-1-family match: its README states it
  uses Jev "to judge relevance across folders, files, and declarations," ranking results by that
  judgment rather than running a dedicated cross-encoder.
- [GLiNER2.5-Decide][gliner-blog] (documented) — its "Context pruning" bullet is the nearest
  related capability, but is not reranking: "Decide which information in the context is relevant
  and return the exact character spans associated with that decision" marks relevance within one
  context rather than sorting a candidate list.
- **Gap**: re-checked 2026-10-09 — neither Jev's docs nor Fastino's announcement names
  query-document reranking; no model in this landscape documents sorting retrieved candidates by
  probability as a worked use case. **Failure mode**: not measured by any system-1 model here;
  see the Rerankers entries above for cross-encoder latency/calibration trade-offs instead.

### 5. LLM output evals and scores (judge)

**Decision shape**: a `score`/`choice` probability over a rubric, or an accept/escalate verdict on
another model's output.

- [GLiNER2.5-Decide][gliner-blog] (documented) — its own "LLM-as-a-judge" bullet: "Express rubric
  criteria as categorical or ordinal questions and return selected values with probability
  distributions and confidence scores."
- [JEV-as-a-Judge (arXiv:2609.26550)][jaaj] (documented — a research paper, no released code or
  dataset) — a decision-only judge that "comes within three points of GPT-6 wherever a verdict
  can be read off the text, at 0.36% of its fee."
- [Perplexity Decisions API][pplx-answer-gate] (documented, hedged by the source itself) — its own
  citation-accuracy cookbook scores whether cited passages support each sentence of another
  model's generated answer, using one `checkable` `noul` question plus a `supports_N`/
  `contradicts_N` `noul` pair per cited passage; fixed probability cutoffs then label each
  sentence `supported`/`weak`/`contradicted`/`unsupported`/`uncited`/`not_checkable`.
  The page itself never uses the term "LLM-as-a-judge," and states plainly: "Each probability is
  the model's estimate of how well the snippets you sent support the sentence" and this "is not
  proof that the sentence is true" — a grounding check on another model's output, not a rubric
  verdict on its quality.
- Free-text LLM-as-a-judge metrics (documented) — G-Eval, TRUE, and others; see
  [agent-evaluation-metrics-landscape.md § LLM-as-a-Judge Quality Assessment][judge-metrics].
  These score generated prose, not a typed decision.
- **Failure mode**: per the paper's own abstract (re-checked 2026-10-09), the approach "falls
  behind where the verdict must be derived, as in math, code, and logic," and "Confidence routing
  weakens on style-adversarial pairs and reference-free prose."

### 6. Confidence gate (act / confirm / human-in-the-loop escalation)

**Decision shape**: a confidence/probability threshold splits the outcome into act, confirm, or
escalate-to-human.

- Jev itself (documented) — [docs.typesafe.ai/confidence][typesafe-confidence] (re-fetched
  2026-10-09) names this pattern directly as "Three paths for using confidence in your code":
  **High confidence** — "Act automatically. The model has a clear read and you can proceed
  without human involvement." **Medium confidence** — "you might ask the user to confirm, flag
  for review, or gather more information before acting." **Low confidence** — "Do not act. Route
  to a human, request clarification, or fall back to a different system." A worked code example
  calls `route_to_human(user_message)` below a 0.5 threshold.
- [kev][kev] (shipped) — its own README reports a per-size Brier-score table ("Brier: New
  Sources") against held-out data, the calibration evidence a confidence gate needs; see
  [agent-evaluation-metrics-landscape.md § Verbalized Confidence Calibration (Brier)][brier] for
  what the score means and why it can diverge from the act/abstain decision itself ("Calibrated
  Enough to Know, Not Calibrated to Act" — Aggarwal, arXiv:2608.27167).
- [Secure Agentics Adrian][adrian-home] (shipped) — classifies every tool call and, per
  [agentic-ai-vulnerability-landscape.md § Secure Agentics Adrian][adrian-home], can intervene
  in-flight (alert, hold for human review, or block) — a three-way act/confirm/escalate gate.
- [JEV-as-a-Judge][jaaj] (documented) — accepts when confident, escalates to a reasoning judge
  when unsure: "0.9 points more accurate than GPT-6 on 1,610 held-out pairs at 41% of its fee."
- **Failure mode**: treat an uncertain or blocked signal as its own outcome, never as a verdict —
  see [jev-analysis.md § Build for When It's Wrong][jev-wrong].

## October 2026: major vendors ship Jev-style decision models

Trigger: a 2026-10-08 LinkedIn post by Maziyar Panahi (self-reported, not independently
verified — plain text, LinkedIn blocks link checkers:
`linkedin.com/posts/maziyarpanahi_someone-just-open-sourced-a-better-jev-share-7513969858003439616-8dc6`),
headlined "Someone just open-sourced a better Jev," reported that OpenAI's GPT-6 Luna (via its
Decisions API) and Perplexity's pplx-decider v1.1 topped his leaderboard of 24 "Jev-style" models
scored on 669 clinical decisions across "triage, clinical notes, eligibility criteria and ICD-10
coding." (That OpenAI and Perplexity now *ship* their own Jev-style decision APIs is this corpus's
own conclusion from the first-party docs below, not Panahi's claim.) Quoted verbatim: "pplx-decider
v1.1 (Perplexity): 643 of 669 right
(96.1%), the top score. All 669 decisions cost 1.7 cents through an API, less than any other model
on the board, and under Apache-2.0 a hospital can run it on its own servers." The same post:
"GPT-6 Luna (OpenAI), through its new Decisions API: 637 of 669, tied at #1, and the only top model
with zero severe misses"; "Mistral Large 4: 617 of 669, also zero severe misses, and the best
triage score on the board (238 of 240)"; and "Jev 1.13, at 345 ms a decision." Mistral Large 4
appears on the post only as a scored entrant on the leaderboard, not as a vendor shipping its own
Jev-style decision API — this corpus found no first-party Mistral page describing one, so it gets
no section here.

**The leaderboard does not appear to be publicly published.** The post itself links only to the
`perplexity-ai/pplx-decider-v1.1-27b` model card, not to a scoreboard page, and names no host for
the "board" the author says he ranked 24 models on. Checked 2026-10-09: the post's own 7 comments
contain no link to one either — one commenter asks for per-model cost/time stats and examples,
another asks whether severe misses cluster by task, and neither gets a reply in the thread; a
Hugging Face Spaces query scoped to the author
(`huggingface.co/api/spaces?author=MaziyarPanahi`, no search filter) returns his full list of 12
Spaces, none naming Jev, decisions, triage, or clinical; the first page of his Hugging Face
profile (huggingface.co/MaziyarPanahi, 2,817 models / 53 datasets / 20 collections — a subset, not
the full profile) surfaces no matching Space, dataset, or model either; his GitHub profile
(github.com/MaziyarPanahi, first page of 43 repositories) lists none; and two web searches for the
leaderboard and for "pplx-decider" with "669" found no independent page describing it. Treat every
number quoted above as the author's self-report, not an independently reproduced result.

### OpenAI Decisions API (GPT-6 Luna)

**First-party**: [Decisions API guide][openai-decisions-guide] · [API reference —
`decisions.create`][openai-decisions-ref] · [DevDay 2026 recap][openai-devday] · [API
changelog][openai-changelog]

A dedicated `POST /v1/decisions` endpoint (documented) that "evaluates text, images, or both and
returns typed answers... about 10x faster than the Responses API" — OpenAI's own equivalent of
Jev's typed-decision interface, built on a single supported model, `gpt-6-luna`. A request sets
`model`, `input` (a text string, or messages mixing text and inline base64 images — **not**
`evidence`), and `questions` (each with a `type` of `predicate`, `choice`, or `score`, a unique
`name`, `instructions`, and, for `choice`/`score`, a `choices`/ordered-`levels` list); the response
returns one `answers[]` entry per question — a `probability` for `predicate`; a `choice` plus
`probabilities` and `confidence` for `choice`; a probability-weighted `score` plus `confidence`
for `score` — plus `usage.input_tokens` (verified against the worked request/response example on
the API reference page, 2026-10-09). A fourth outcome, `refusal`, is handled explicitly in the
guide's own SDK code samples (not shown on the reference page itself).

**Status — three first-party pages, three different words, within 72 hours**: the
[Decisions API guide][openai-decisions-guide] (checked 2026-10-09) states: "The Decisions API is
in public beta, and we expect to GA in the coming weeks." The [API changelog][openai-changelog]'s
Oct 6, 2026 entry agrees on the stage: "Released the Decisions API in beta with `gpt-6-luna`." The
[DevDay 2026 recap][openai-devday] (dated Oct 6–7, 2026 — the page carries both timestamps) uses
different wording for the same release: "Available in limited preview today with a broad release
planned in the coming days."

**Stated use cases (documented, guide)**: "Use those answers to classify content, route requests,
and prioritize work in your application." The guide's own worked example, "Route a customer
complaint," asks one `choice` question over four department options
(`billing`/`technical`/`shipping`/`other`) — see § Use cases → Model routing above for why this
does not close that section's gap. Its "Score against a rubric" section documents the `score`
type generically; its own worked example scores package-damage and ticket-urgency levels, not
another model's generated output, so this corpus does not count it toward the judge use case
either.

**Stated use case (announced, DevDay recap only)**: "get back answers they can use to classify
content, route requests, or choose an agent's next action." This phrase appears only in the DevDay
recap, not in the technical guide, and no worked example of it is shown in either page — see
§ Use cases → Tool-call gating above.

**Pricing (documented)**: "input costs $0.10 per 1M tokens. You pay only for input tokens: there
are no cache-read, cache-write, or output-token charges" (guide, checked 2026-10-09). Regional
processing premiums and long-context multipliers can apply; the Decisions API supports Zero Data
Retention and HIPAA use for eligible customers, with data residency in the US and EEA/Switzerland.

**Leaderboard placement (self-reported, not independently verified)**: see § October 2026 above —
Panahi's post reports GPT-6 Luna, through the Decisions API, scoring "637 of 669... tied at #1,
and the only top model with zero severe misses" on the unpublished 669-decision clinical
benchmark.

No rubric row: under this corpus's gap-driven scoring policy, a new row is added only when it
could change an open cell in the rubric's evidence census. This entry doesn't, so none is added
here.

### Perplexity pplx-decider

**First-party**: [Hugging Face model card (v1.1)][pplx-decider-hf] · [HF API model
metadata][pplx-decider-api] · [Decisions API quickstart][pplx-quickstart] · [Decisions API
pricing][pplx-pricing] · [API changelog][pplx-changelog] · [Decision Index Space][decision-index-space]

Perplexity ships `pplx-decider` two ways: as an Apache-2.0, open-weight checkpoint on Hugging Face
you can self-host, and as a hosted model behind Perplexity's own "Decisions API" — the same model
family under one name, reachable at `POST https://api.perplexity.ai/v1/decisions`. The hosted API
uses Jev's own type vocabulary verbatim: `noul`, `choice`, `score` (OpenAI's API, above, renames
the binary type `predicate` instead) — the closest naming match to Jev of any hosted entry in this
landscape (the open-weight card's own Markdown only shows `choice` in a usage snippet; its text
doesn't use the word `noul`). The hosted request shape, per the [quickstart][pplx-quickstart]
(checked 2026-10-09): `model`,
`state` (text, JSON, or images — up to 262,144 input tokens, 1–128 questions per request), and
`questions`, each a `noul` (yes/no), `choice` (1–255 named options), or `score` (2–10 ordered
levels). The open-weight card describes the same architecture from the other side: a
`Qwen/Qwen3.8-27B` base fine-tuned into the "native decision-checkpoint layout" — the stock
`Qwen3_5Model` backbone plus a separate `readout.safetensors` file, a BF16 `[255, 5120]` decision
head rather than a full-vocabulary `lm_head` — 26B parameters in BF16; `DecisionModel.predict`
applies a saved calibration temperature and returns probabilities over the candidate answers
(verified against the model card and the HF API's `siblings` file list, 2026-10-09).

**Pricing (documented) — a price cut, not a conflict**: the [pricing page][pplx-pricing] (checked
2026-10-09) lists both `pplx-decider-v1.1-27b` and `pplx-decider-v1-27b` at $0.02 per 1M input
tokens, free output, no per-request fee. The [changelog][pplx-changelog] explains why both read
the same: the "New: Decisions API" entry originally priced `pplx-decider-v1-27b` at "$0.04 per
million tokens," and the later "pplx-decider-v1.1-27b replaces v1" entry states "Input now costs
$0.02 per million tokens, down from $0.04," with "requests that still use the older v1 name" kept
working "at the same $0.02 rate." Neither changelog entry uses the words beta, preview, or GA, so
this corpus found no first-party release-stage label for Perplexity's Decisions API (contrast
OpenAI's explicit "public beta," above).

**Benchmark (documented; the card's figures don't fully match the board it cites)**: the v1.1 card
reports its own "Decision Index" score — 61.56 overall against Jev's 57.9 (v1 scored 56.4), "now
outperforms Jev by more than 3.5 points." Per category, v1.1 trails Jev on Knowledge (48.18 vs.
51.4) and leads on Language (69.45 vs. 62.0), Retrieval (61.26 vs. 55.4), Tools (78.88 vs. 75.1,
though v1 scored higher at 79.3), and Arts (44.66 vs. 37.7); the card states the overall figure
uses the suite's own weighting, not a plain average. The card links the
[Decision Index Space][decision-index-space] (`multimodalart/jev-decision-index`, 550 likes as of
2026-10-09, over 100 linked model repos), which describes itself as "Unofficial and
community-maintained; not affiliated with TypeSafe AI" — a public, community-run leaderboard
combining "20% public benchmarks" (37 benchmarks across five chance-corrected areas), "50% private
tests of the same skills," and "30% private tasks from new domains," with the private components
never published. Both models do have live entries on the board's own data file (checked
2026-10-09): Jev's `public_skill`/`frozen_scores.balanced_skill` of 57.96 is a near-exact match for
the card's "57.9," and the per-category `skill` values for both Jev and pplx-decider-v1.1 match
the card exactly on Retrieval and Tools (55.4/55.42 and 75.1/75.09 for Jev; 61.26/61.26 and
78.88/78.88 for v1.1) but run 1.4–3.8 points off the card on Knowledge, Language, and Arts for
*both* models. The board's own headline score for v1.1 (`scores.balanced_skill` 62.75,
`frozen_scores.balanced_skill`/`public_skill` 62.25) does not match the card's "61.56" either. The
entry is real and the two sources agree closely on two of five categories, but this corpus could
not fully reconcile the remaining numbers from the data available — treat "61.56 vs. 57.9" as the
card's own stated comparison, not a figure independently confirmed against the board's current
state.

**Access — resolving the card's own wording (documented + observed, corrects the card)**: the
card's usage section states a reader needs "authenticated Hugging Face access to this private
repository." This is inconsistent with the repository's live state: the Hugging Face API
([`huggingface.co/api/models/perplexity-ai/pplx-decider-v1.1-27b`][pplx-decider-api], checked
2026-10-09) reports `"gated": false`, `"private": false`, 1,072 downloads, and lists all 11
safetensors shards, `LICENSE`/`NOTICE`, and the full training source tree as downloadable
`siblings`. A web search also surfaced an OpenRouter listing page for the same checkpoint
(`openrouter.ai/perplexity/pplx-decider-v1.1-27b`) — unverified here, since a direct fetch of that
URL 404'd on 2026-10-09; not relied on for this claim. The card's "private repository" sentence
reads as stale
wording from an earlier internal release, not the current access state; the weights are public
and downloadable without authentication. Separately, the model page's "isn't deployed by any
Inference Provider" banner is Hugging Face's own standard widget placeholder for any model without
a configured serving partner — platform UI text, not a Perplexity statement; it does not appear
anywhere in the card's own raw Markdown.

**Documented use cases (hosted API cookbooks)**: Perplexity's own cookbook pages apply
`pplx-decider` to patterns already tracked by this doc's § Use cases — ticket triage (routing,
above), gating an agent's proposed function call before it runs (tool-call gating, above),
driving a browser step by step (tool-call gating, above), and scoring whether cited passages
support a generated sentence (judge, above) — each cross-referenced from its matching use case
rather than repeated here.

**Leaderboard placement (self-reported, not independently verified)**: see § October 2026 above —
Panahi's post reports: "pplx-decider v1.1 (Perplexity): 643 of 669 right (96.1%), the top score.
All 669 decisions cost 1.7 cents through an API, less than any other model on the board, and under
Apache-2.0 a hospital can run it on its own servers."

No rubric row: under this corpus's gap-driven scoring policy, a new row is added only when it
could change an open cell in the rubric's evidence census. This entry doesn't, so none is added
here.

## Laya (NandhaKishorM)

**Repo**: [NandhaKishorM/laya][laya] | **License**: Apache-2.0 (confirmed against `LICENSE`) |
**Stars**: 28,928 / 2,524 forks, pushed 2026-09-29 (`gh api`, 2026-09-30)

A non-autoregressive System-1 decision engine: typed `choice`/`score`/`noul` decisions over any
text (email, ticket, JSON) in one forward pass — 33 ms for one question, 7.2 ms/question batched,
measured on a T4. Three pinned Hugging Face checkpoints, picked per request by a `Router`: `laya`
(ModernBERT-large, 421M, English), `laya-multilingual` (mmBERT-base, 322M, 100+ languages),
`laya-typed-decisions` (ModernBERT-large, 421M, tuned for typed-decision workflows). Self-hosted
only — no hosted API. `laya.serve` exposes `/v1/systemone` on the same wire protocol as Jev's
hosted API, with a schema-identical answer payload, so an existing Jev client (the README names
the Haskell client `hs-jev`) only needs its `baseUrl` repointed.

The README's own caveat, worth stating plainly: **"Jev figures are third-party published, never
measured here (no TypeSafe API access)."** Every Laya number in its own comparison table comes
from `Router().predict(...)` actually running; every Jev number is someone else's publication, not
a controlled A/B.

`subject: harness`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no [README][laya] (self-hosted, single-process serving; no documented multi-writer store) | no data [README][laya] (a self-hosted HTTP server; no cluster/sync deployment documented) | yes [README][laya] (three Hugging Face checkpoints, unpinned by default (`LAYA_REVISION` and per-checkpoint SHA-256 maps allow pinning), deterministic forward pass, no LLM generation step) | yes [README][laya] (a `Router` swaps checkpoints per request; a JS/TS SDK and third-party projects like `stuntd` train new heads on the frozen encoder) | yes [HF org][laya-hf] (checkpoints are commit-addressable Hugging Face repos; `laya` and `laya-multilingual` carry no Hub tags as of 2026-09-30, and the README's quickstart loads `main` by default — `LAYA_REVISION` and per-checkpoint SHA-256 maps allow pinning) | partial [README][laya] (returns calibrated probabilities and usage counts per call, but its own Jev comparisons are explicitly unmeasured, not an audit trail) |

`scored 2026-09-30`

## kev (jaredpalmer)

**Repo**: [jaredpalmer/kev][kev] | **License**: Apache-2.0 (confirmed against `LICENSE`) |
**Stars**: 7,997 / 505 forks, pushed 2026-09-29 (`gh api`, 2026-09-30)

A family of decision models on Qwen3.5/Qwen3.8 (0.8B, 4B, 9B, 27B) you can run pretrained or
train yourself. Its API matches TypeSafe's System One, so the TypeSafe Python SDK works against a
local Kev server unchanged (`base_url` repoint only). Unlike Laya, kev **ran Jev itself** on its
own development sets (a `Jev | Hosted | 0.857 / –` row in its comparison table — the README
states Jev was only run on the development sets, never the held-out test sets) — but
hedges the comparison in its own words: **"We don't know what Jev was trained on, so this isn't a
controlled comparison of the two architectures."** On "new sources" (data Kev never trained on),
Kev-27B lands within a point of Jev (0.851 vs 0.857) and Kev-4B/9B within four points. Release
weights ship with SHA-256 checksums and a frozen eval-suite dataset on Hugging Face
(`jaredpalmer/kev-suites`); a `kev-finetune` coding-agent skill runs an end-to-end fine-tune on
Modal from your own labelled examples (about $1/run on an H100 for Kev-4B).

`subject: harness`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no [README][kev] (self-hosted single server; no documented multi-writer semantics) | no data [README][kev] (self-hosted HTTP server; scale-to-zero deploy is one endpoint, not a cluster) | yes [README][kev] (SHA-256-checksummed release weights, a frozen eval-suite dataset, and model cards with the full training recipe per size) | yes [README][kev] (`kev-finetune` skill fine-tunes any released checkpoint on your own data, fits a new temperature, and deploys) | yes [HF org][kev-hf] (Hub tags keep earlier checkpoint versions; GitHub releases carry checksummed weights) | partial [README][kev] (returns calibrated probabilities per typed question and reports Brier scores against held-out sets; no per-answer citation mechanism) |

`scored 2026-09-30`

## CLM / CLM-8B (Contrastive-LM)

**Repo**: [Contrastive-LM/CLM][clm] | **License**: Apache-2.0, code and weights (confirmed against
`LICENSE`; weights on [Hugging Face][clm-hf]) | **Stars**: 2,565 / 223 forks, pushed 2026-09-24
(`gh api`, 2026-09-30)

A "Contrastive Language Model" — a System-1 model trained with a contrastive objective that
connects states and actions, served behind a TypeSafe-compatible API. CLM-8B runs its encoder as
a stock `Qwen/Qwen3-8B` pooling server (via `vllm serve`) and downloads a separate, small (~75 MB)
"reference head" on first run; states and actions are embedded independently and cached, which is
what the README credits for its serving speed. Per the README, the head is pre-trained on 60M
Nemotron Q&A pairs, mid-trained on 30M synthetic hard negatives, and post-trained on 1M agentic
trajectories. Self-reported: on par with Jev across computer-use, gaming, and tool-calling tasks
at up to 9× lower latency, and — with lightweight fine-tuning — a new verifier SOTA on
Terminal-Bench 2.1 (87.6%) and DeepSWE (81.6%). **Correction to the plan's lead**: a social post
credited Stanford and NVIDIA for this work; neither institution appears in the README, its
citation block (seven individual co-author names, no affiliations given), or the license file — that
credit is unconfirmed and is dropped here rather than repeated.

`subject: harness`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no [README][clm] (self-hosted encoder + head server; no multi-writer store) | no data [README][clm] (two local server processes — a pooling encoder and the CLM API — not a documented multi-node deployment) | partial [README][clm] (the 8B checkpoint and code are Apache-2.0 and versioned on Hugging Face, but the 60M/30M/1M training corpora are described, not released, so the training pipeline itself can't be rebuilt) | yes [README][clm] (a documented fine-tuning path onto agentic coding verifiers reaches a new reported SOTA) | yes [HF][clm-hf] (weights are a versioned Hugging Face repo) | partial [README][clm] (usage/latency are reported per call; benchmark numbers are the project's own, not independently replicated) |

`scored 2026-09-30`

## GLiNER2.5-Decide (Fastino Labs)

**First-party**: [Fastino's own announcement][gliner-blog] · [HF model card][gliner-hf] |
**License**: Apache 2.0 (per the announcement and model card)

A 340M-parameter open-weight, encoder-based decision model with a constrained decoder for jointly
answering a set of typed, schema-defined questions in one pass — aimed at the high-frequency
judgment calls inside an agent pipeline (routing, triage, tool selection, guardrails). It runs on
CPU (Fastino reports p50 167.3 ms at batch size 1/64 tokens on a 48-vCPU Intel Xeon Platinum
8581C) and is deployable air-gapped. Fastino's own "Fast Decisions" internal benchmark reports
GLiNER2.5-Decide leading with a 60.1% average across 17 datasets, ahead of JevK5 (57.5%), SemIf
(56.4%), GLiFormer (49.0%), and Laya (46.6%) — with Fastino's **own** caveat quoted verbatim:
**"This is an internal benchmark, not JevBench, and JevK5 is an open reproduction rather than
TypeSafe's Jev."** No training-data statement is given in either source.

`subject: harness`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no [blog][gliner-blog] (a self-hosted or single-endpoint model; no shared-store semantics described) | partial [blog][gliner-blog] (a hosted inference API at `agent.fastino.ai` exists alongside self-hosting; no cluster/sync protocol documented for the open weights themselves) | no data [blog][gliner-blog] (no training-data source is stated in the announcement or model card) | yes [blog][gliner-blog] (an encoder architecture explicitly framed as easy to fine-tune for new schemas) | yes [HF][gliner-hf] (a versioned Hugging Face model repo) | partial [blog][gliner-blog] (returns probabilities, confidence, and constraint-feasibility metadata per answer; the vendor's own benchmark is not third-party audited) |

`scored 2026-09-30`

## RuVector (ruvnet)

**Repo**: [ruvnet/RuVector][ruvector] | **License**: MIT (confirmed against `LICENSE`) |
**Stars**: 4,528 / 607 forks, created 2025-11-19, pushed 2026-09-30 (`gh api`, 2026-09-30)

RuVector predates this batch — it is a Rust-native vector-DB and agent-memory substrate ("Git for
Agent Memory" territory alongside the same author's [AgentiCow][agenticow], already cross-linked
from [agent-frameworks-infrastructure-landscape.md][agenticow-xref]) that added a Jev-compatible
decision layer. That layer, `@ruvector/typesafe`, is a **separate package** — installing the root
`ruvector` package does not enable it. It turns text into typed `choice`/`score`/`noul` decisions
using local embeddings and native decision heads (with a WASM fallback) and can serve a
Jev-compatible HTTP API. **Correction to the plan's lead**: the vs-Jev figures are not only "from
an ad" — they are in RuVector's own README: on a documented 150-ticket test split, its local ONNX
decision engine reports 4–10 ms p95 latency at 77.3–84.0% department accuracy, against a Jev
replay reference at 231 ms p95 and 85.3% accuracy. The README states its own limits plainly:
these are "workload-specific measurements, not a universal speed or quality guarantee," and "the
default hash embedder is a test double... not calibrated for production decisions."

`subject: harness`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| partial [README][ruvector] ("optional shared memory" is named as a feature of the broader RuVector substrate; the decision layer itself is single-process) | no [README][ruvector] (an embedded, local-first store; no cluster/remote deployment for the decision layer) | partial [README][ruvector] (local ONNX inference is deterministic, but the default embedder is explicitly a test double, and the production embedding model is left to the integrator) | yes [README][ruvector] (supports labeled examples, evaluation, and a Jev-compatible HTTP server as an alternate serving mode) | no data [README][ruvector] (no snapshot/rollback documented specifically for the decision layer, as distinct from the memory store's own lifecycle controls) | partial [README][ruvector] (reports confidence and abstention per decision; the vs-Jev numbers are self-reported on one documented split, not independently verified) |

`scored 2026-09-30`

## Domain example: BioDecision-4B

[`lighteternal/biodecision-tev1-4b`][biodecision] (and a `-lora-v1.1` variant) on Hugging Face: a
Qwen3.5-4B model with a LoRA fine-tune using the Tev1 recipe (credited to Together AI on the model
card) and Jev's typed decision format, returning calibrated per-answer probabilities for
biomedical multiple-choice/yes-no/score questions in one pass. **Correction to the plan's lead**:
the model card does not claim to be "the first open System-1 model for biomedicine" — that framing
is dropped. The card's own license is research-only use, and it states explicitly it is **not
validated for patient care**. One line only, per this batch's scope — no rubric.

## Tools built on Jev

Five projects call Jev (or an alternative decision model) as one step in a larger tool. Three have
their own home elsewhere in this corpus and this section only points to them; probably and pg-jev
have none yet, so their full entries live here.

- **abide** (coldteadotai) — asks Jev one question per AGENTS.md rule on every coding-agent edit or
  turn and has the agent repair a break. See
  [CC-community-tooling-landscape.md § abide][abide-home].
- **jev-ultrafast** (browser-use) — a browser agent whose action-selection loop is a Jev decision
  per step instead of an LLM generating an action. See
  [CC-web-scraping-plugins-analysis.md § Alternative MCP Options][jevultrafast-home].
- **jevgrep** (dzhng) — a code-search CLI that uses Jev to judge file/declaration relevance to a
  natural-language question. See [CC-code-tooling-landscape.md § jevgrep][jevgrep-home].
- **pg-jev** (realZachi) — **Repo**: [realZachi/pg-jev][pg-jev] | **License**: PostgreSQL License
  (confirmed against `LICENSE`; GitHub's license detector reports `NOASSERTION` — the file matches
  the [OSI's PostgreSQL License template][osi-pgl] with its `$ORGANISATION` placeholder generalized
  to "the copyright holders" rather than a bespoke or missing license, and the README's own badge
  reads "license-PostgreSQL") | **Stars**: 976, created 2026-09-17, pushed
  2026-10-03, one release `v0.2.1` (2026-10-03) (`gh api`, 2026-10-06). A PostgreSQL extension
  (`CREATE EXTENSION jev CASCADE`) that exposes `jev()`/`jev_prob()`/`jev_choice()`/`jev_score()` as
  ordinary SQL functions, so a plain-language condition composes with `WHERE`, `JOIN`, `GROUP BY`
  and `ORDER BY`. Per its README: it batches 20 rows into one shared Jev `state` with one typed
  question per row (batches of 40/80 rows measured 92–98%/77–94% correct against ground truth,
  vs. 100% at 20), caches answers per row/question for the backend session, and needs PostgreSQL
  14–17 with `plpython3u` and superuser — so it does not run on Supabase, Neon, or RDS. Ships an
  agent skill (`npx skills add realZachi/pg-jev`) that the README names as installable by "Claude
  Code, Codex, Cursor or any other skill-aware agent." This page is pg-jev's home in the corpus, not
  a placeholder. No rubric row: it is a SQL wrapper around Jev's existing decision-model API, not a
  new decision-model architecture, so it cannot bear on any open rubric cell (gap-driven scoring,
  plan 0011 row O1).

- **probably** (southpolesteve) — **Repo**: [southpolesteve/probably][probably] | **License**: MIT
  (confirmed against `LICENSE`) | **Stars**: 12, pushed 2026-09-19 (`gh api`, 2026-09-30). An
  experimental toy programming language whose `if value feels "description"` branches ask Jev
  directly for a yes/no judgment, with a `match` construct for 2–8 semantic labels and a `chaos`
  block that samples judgment probabilities. The interpreter is real (it executes the program;
  it does not ask an LLM to interpret it), and runs (`--save`/`--replay`) record the input and
  every model output so a run replays offline, with no model call and no credentials, rejecting
  any mismatched or incomplete recording. [jev-analysis.md](../infrastructure/jev-analysis.md)
  already cross-references this page for probably (see its Cross-References section) — this page
  is probably's home in the corpus, not a placeholder.

  `subject: harness`

  | Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
  |---|---|---|---|---|---|
  | n/a [README][probably] (a single-user CLI/language, not a multi-agent store) | n/a [README][probably] (a local interpreter; no deployment target) | partial [README][probably] (`--replay` deterministically reproduces a prior run from its saved effect tape, but a live run's model outputs are not themselves pinned/reproducible) | no data [README][probably] (no plugin/backend extension point beyond the two built-in provider adapters) | no [README][probably] (recordings are individual JSON files, not a versioned store) | yes [README][probably] (a saved run's every judgment, generated text, and random draw is inspectable in its recording) |

  `scored 2026-09-30`

## Also found: JevK5 and SemIf

Two more independent, open-weight Jev alternatives turned up first-party sources during this
batch (neither was in the original lead list); light treatment only, per this batch's scope.

- **JevK5** — **Repo**: [allebee/jevk5][jevk5] | **License**: Apache-2.0 (confirmed against
  `LICENSE`; weights and code) | **Stars**: 126, pushed 2026-09-28 (`gh api`, 2026-09-30). An
  independent open-weight alternative (Qwen3.5-4B/9B plus a distilled LoRA, merged), explicitly
  "not affiliated with TypeSafe AI." On the third-party [JevBench v1.4][jevbench] leaderboard it
  ranks second of 76 systems and first among open entrants (62.04 vs. Jev 1.13.0's 63.29).
  (`ngrok-adhoc/jevk5` is a same-day fork of this repo, not a second independent project.)
- **SemIf** (formerly OpenJev) — **Repo**: [TheoLeeCJ/SemIf-OpenJev][semif] | **License**: MIT
  (confirmed against `LICENSE`) | **Stars**: 4,602, pushed 2026-09-23 (`gh api`, 2026-09-30). An
  independent research project that reproduces Jev's **interface pattern** (typed decisions read
  directly as option-logit probabilities, no generation) with open models — explicitly "not
  affiliated with or endorsed by TypeSafe" and not a reproduction of Jev's own model or training.
  Multiple community backends (CUDA, Apple Silicon MLX/MPS, CPU via llama.cpp). The project
  spells its name **SemIf** (its repository and Fastino's announcement agree).

## Paper: JEV-as-a-Judge (CMU)

**Paper**: [arXiv:2609.26550][jaaj] — "JEV-as-a-Judge: Accept When Confident, Escalate When
Unsure" (Yubo Li, Yidi Miao, Ramayya Krishnan, Rema Padman; Carnegie Mellon University, per the
paper's own affiliation block and `@andrew.cmu.edu` author emails). Submitted 22 Sep 2026 (v1),
current version v3, 29 Sep 2026.

Per the abstract (quoted): a decision-only judge (JEV) "returns label probabilities instead of
text," and its confidence decides whether to accept its verdict or escalate to a reasoning judge.
Against sixteen generative and reward-model judges, with blinded human adjudication, it "comes
within three points of GPT-6 wherever a verdict can be read off the text, at 0.36% of its fee and
a 0.15-second median latency, and falls behind where the verdict must be derived, as in math,
code, and logic." With a threshold frozen in advance, the accept/escalate cascade is "0.9 points
more accurate than GPT-6 on 1,610 held-out pairs at 41% of its fee," and in a pre-specified live
test on two new workloads "matches GPT-6's accuracy exactly." Confidence-based routing weakens on
style-adversarial pairs and reference-free prose.

`subject: harness`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| n/a [abs][jaaj] (a research method, not shipped multi-user software) | n/a [abs][jaaj] (no deployment artifact to run across machines) | no data [abs][jaaj] (no code or dataset release is linked from the abstract page) | n/a [abs][jaaj] (a method description, not an extensible system) | yes [abs][jaaj] (arXiv revisions v1 → v3, 22–29 Sep 2026) | partial [abs][jaaj] (the confidence-gated escalation is itself a routing rationale for every verdict, but no persistent audit log or citation mechanism is described) |

`scored 2026-09-30`

## Sources

| Source | Content |
|---|---|
| Maziyar Panahi, LinkedIn post, 2026-10-08 (plain text, no link: `linkedin.com/posts/maziyarpanahi_someone-just-open-sourced-a-better-jev-share-7513969858003439616-8dc6`) | Trigger for this section; self-reported 24-model/669-decision clinical leaderboard, fetched verbatim via polyfetch 2026-10-09; post and its 7 comments checked for a leaderboard link (none found) |
| Hugging Face Spaces API, `?author=MaziyarPanahi` | Author's full Space list (12), checked 2026-10-09 for a leaderboard match (none found) |
| [OpenAI Decisions API guide][openai-decisions-guide] | Request/response shape, status ("public beta"), pricing, use cases; fetched 2026-10-09 |
| [OpenAI Decisions API reference — `decisions.create`][openai-decisions-ref] | Worked request/response example (`model`/`input`/`questions`, `answers`/`usage`); fetched 2026-10-09 |
| [OpenAI DevDay 2026 recap][openai-devday] | "Limited preview" status wording (differs from the guide/changelog) and the "agent's next action" use case; published 2026-10-07, fetched 2026-10-09 |
| [OpenAI API changelog][openai-changelog] | Oct 6, 2026 "Released the Decisions API in beta" entry |
| [pplx-decider-v1.1-27b (Hugging Face)][pplx-decider-hf] | Model card: architecture, Decision Index scores, access wording |
| [pplx-decider-v1.1-27b (HF API)][pplx-decider-api] | `gated`/`private`/`siblings` metadata resolving the card's "private repository" wording, checked 2026-10-09 |
| [Perplexity Decisions API quickstart][pplx-quickstart] | Hosted request shape (`state`/`questions`/`noul`/`choice`/`score`), limits; fetched 2026-10-09 |
| [Perplexity Decisions API pricing][pplx-pricing] | Current $0.02/1M input-token rate for both model names; fetched 2026-10-09 |
| [Perplexity API changelog][pplx-changelog] | v1 → v1.1 price-cut history ($0.04 → $0.02); fetched 2026-10-09 |
| [Jev Decision Index (Hugging Face Space)][decision-index-space] | Confirms the benchmark is community-run ("not affiliated with TypeSafe AI"); its own `data/index.json` has live entries for both Jev and pplx-decider-v1.1, partially but not fully reconciling the model card's cited numbers; checked 2026-10-09 |
| [Perplexity Decisions API — ticket-triage cookbook][pplx-ticket-triage] | Routing worked example (escalate/review/queue/auto_reply/close) |
| [Perplexity Decisions API — action-gate cookbook][pplx-action-gate] | Approve/deny gate on a proposed `schedule_payment` call |
| [Perplexity Decisions API — browser-agent cookbook][pplx-browser-agent] | Next-action selection (click/dismiss/scroll/stop) with measured per-step latency |
| [Perplexity Decisions API — answer-gate (citation-accuracy) cookbook][pplx-answer-gate] | Citation/grounding verification of another model's generated sentences |
| [Laya][laya] | README, LICENSE (fetched via GitHub contents API, 2026-09-30) |
| [Laya (Hugging Face org)][laya-hf] | Checkpoint versioning |
| [kev][kev] | README, LICENSE (fetched via GitHub contents API, 2026-09-30) |
| [kev (Hugging Face org)][kev-hf] | Weights collection, frozen eval suites |
| [CLM][clm] | README, LICENSE (fetched via GitHub contents API, 2026-09-30) |
| [CLM-8B (Hugging Face)][clm-hf] | Weights, license |
| [GLiNER2.5-Decide announcement][gliner-blog] | Fastino's own blog post: architecture, benchmark, hosting |
| [GLiNER2.5-Decide (Hugging Face)][gliner-hf] | Model card |
| [RuVector][ruvector] | README, LICENSE (fetched via GitHub contents API, 2026-09-30) |
| [BioDecision-4B][biodecision] | Hugging Face model card |
| [probably][probably] | README, LICENSE (fetched via GitHub contents API, 2026-09-30) |
| [pg-jev][pg-jev] | README, LICENSE, releases (fetched via GitHub contents/API, 2026-10-06) |
| [OSI PostgreSQL License template][osi-pgl] | Compared verbatim against pg-jev's `LICENSE` file, 2026-10-06 |
| [JevK5][jevk5] | README, LICENSE (fetched via GitHub contents API, 2026-09-30) |
| [JevBench v1.4][jevbench] | Third-party leaderboard cited by JevK5's own README |
| [SemIf-OpenJev][semif] | README, LICENSE (fetched via GitHub contents API, 2026-09-30) |
| [JEV-as-a-Judge (arXiv:2609.26550)][jaaj] | Abstract page (verbatim, fetched 2026-09-30) |
| [agent-frameworks-infrastructure-landscape.md §8][frameworks-8] | Existing classifier/output-validation coverage, cross-referenced not repeated |
| [Plan 0009][plan] | Lead list (J3 / issue #517) and rubric scope for this batch |
| [Issue #517][issue-517] | Batch scope, proposed placements, owner corrections |
| [GLiNER2.5-Decide announcement][gliner-blog] | Use-case bullets ("Model routing," "Tool calling," "Browser and computer use," "Guardrails," "LLM-as-a-judge") re-fetched verbatim, 2026-10-09 |
| [docs.typesafe.ai][typesafe] (home, `/api`, `/models`) | Re-checked 2026-10-09 for a model-selection routing claim; none found |
| [docs.typesafe.ai/confidence][typesafe-confidence] | Re-fetched verbatim 2026-10-09: the "Three paths for using confidence in your code" act/confirm/escalate pattern |
| [Secure Agentics Adrian README][adrian-gh] | Tool-call classification and block/hold-for-approval behavior, re-fetched verbatim via `gh api`, 2026-10-09 |
| [agentic-ai-vulnerability-landscape.md § Secure Agentics Adrian][adrian-home] | Existing corpus analysis of Adrian's act/confirm/escalate intervention modes, cross-referenced not repeated |
| [agent-evaluation-metrics-landscape.md § LLM-as-a-Judge Quality Assessment][judge-metrics] | Free-text judge metrics, cross-referenced not repeated |
| [agent-frameworks-infrastructure-landscape.md § Guardrails / policy][guardrails-policy] | Safety-classifier/guardrail tools, cross-referenced not repeated |
| [agent-frameworks-infrastructure-landscape.md § Rerankers][rerankers] | Dedicated cross-encoder rerankers, cross-referenced not repeated |
| [llm-routers-gateways-landscape.md][llm-routers-open] | RouteLLM / Not Diamond classifier-trained routers, cross-referenced not repeated |

[rubric]: ../../sdlc-lcm/agent-substrate-rubric.md
[plan]: ../../plans/2026-09-27-0009-focus-shared-memory-context.md
[typesafe]: https://docs.typesafe.ai/
[issue-517]: https://github.com/qte77/ai-agents-research/issues/517
[frameworks-8]: ../frameworks/agent-frameworks-infrastructure-landscape.md#8-output-validation-guardrails--verification
[laya]: https://github.com/NandhaKishorM/laya
[laya-hf]: https://huggingface.co/convaiinnovations/laya
[kev]: https://github.com/jaredpalmer/kev
[kev-hf]: https://huggingface.co/collections/jaredpalmer/kev-6aad9d0ea49f2589665e07cd
[clm]: https://github.com/Contrastive-LM/CLM
[clm-hf]: https://huggingface.co/Contrastive-LM/CLM-v0.1-8B
[gliner-blog]: https://fastino.ai/blog/gliner-2-5-decide-open-weight-decision-model
[gliner-hf]: https://huggingface.co/fastino/GLiNER2.5-Decide
[ruvector]: https://github.com/ruvnet/RuVector
[agenticow]: https://github.com/ruvnet/agenticow
[agenticow-xref]: ../frameworks/agent-frameworks-infrastructure-landscape.md
[biodecision]: https://huggingface.co/lighteternal/biodecision-tev1-4b
[abide-home]: ../../cc-community/CC-community-tooling-landscape.md#abide-coldteadotai
[jevultrafast-home]: ../../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md#alternative-mcp-options-brief
[jevgrep-home]: ../../cc-community/CC-code-tooling-landscape.md#jevgrep-dzhng
[probably]: https://github.com/southpolesteve/probably
[pg-jev]: https://github.com/realZachi/pg-jev
[osi-pgl]: https://opensource.org/license/postgresql
[jevk5]: https://github.com/allebee/jevk5
[jevbench]: https://github.com/fstandhartinger/jevbench
[semif]: https://github.com/TheoLeeCJ/SemIf-OpenJev
[jaaj]: https://arxiv.org/abs/2609.26550
[typesafe-confidence]: https://docs.typesafe.ai/confidence
[jev-pilot]: ../infrastructure/jev-analysis.md#measured-pre-ci-code-change-gate
[jev-wrong]: ../infrastructure/jev-analysis.md#build-for-when-its-wrong
[guardrails-policy]: ../frameworks/agent-frameworks-infrastructure-landscape.md#guardrails--policy
[rerankers]: ../frameworks/agent-frameworks-infrastructure-landscape.md#rerankers
[llm-routers-open]: ../infrastructure/llm-routers-gateways-landscape.md#open--self-hostable-gateways
[llm-routers-hosted]: ../infrastructure/llm-routers-gateways-landscape.md#hosted-aggregators
[routellm-home]: https://github.com/lm-sys/RouteLLM
[notdiamond-home]: https://www.notdiamond.ai/
[judge-metrics]: ../../sdlc-lcm/agent-evaluation-metrics-landscape.md#llm-as-a-judge-quality-assessment
[brier]: ../../sdlc-lcm/agent-evaluation-metrics-landscape.md#verbalized-confidence-calibration-brier
[adrian-home]: ../../sdlc-lcm/agentic-ai-vulnerability-landscape.md#secure-agentics-adrian--open-source-runtime-agent-monitor
[openai-decisions-guide]: https://developers.openai.com/api/docs/guides/decisions
[openai-decisions-ref]: https://developers.openai.com/api/reference/resources/decisions/methods/create
[openai-devday]: https://openai.com/index/devday-2026-recap/
[openai-changelog]: https://developers.openai.com/api/docs/changelog
[pplx-decider-hf]: https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b
[pplx-decider-api]: https://huggingface.co/api/models/perplexity-ai/pplx-decider-v1.1-27b
[pplx-quickstart]: https://docs.perplexity.ai/docs/decisions/quickstart
[pplx-pricing]: https://docs.perplexity.ai/docs/getting-started/pricing
[pplx-changelog]: https://docs.perplexity.ai/docs/resources/changelog
[decision-index-space]: https://huggingface.co/spaces/multimodalart/jev-decision-index
[pplx-ticket-triage]: https://docs.perplexity.ai/docs/cookbook/examples/decisions-api-ticket-triage/README
[pplx-action-gate]: https://docs.perplexity.ai/docs/cookbook/examples/decisions-api-action-gate/README
[pplx-browser-agent]: https://docs.perplexity.ai/docs/cookbook/examples/decisions-api-browser-agent/README
[pplx-answer-gate]: https://docs.perplexity.ai/docs/cookbook/examples/decisions-api-answer-gate/README
[adrian-gh]: https://github.com/secureagentics/Adrian
