---
title: System-1 Decision Models Landscape
purpose: Survey open-weight, research, independent, and major-vendor alternatives to TypeSafe's Jev — fast, typed-output classifiers (choice/score/noul answers, calibrated probabilities, one forward pass, no free text) used for agent routing, guardrails, and verification — scored against the agent substrate rubric where the model's deployment path makes that possible.
created: 2026-09-30
updated: 2026-10-15
validated_links: 2026-10-15
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
  several candidate models. Still no system-1 decision model checked in this corpus, vendor or
  independent, *ships a worked example* of selecting which model should answer a request. The
  nearest matches already in this doc are narrower still: Laya's `Router` class picks among Laya's
  *own* three checkpoints (not other LLMs), and RuVector's decision layer classifies support
  tickets into a fixed department label set (77.3–84.0% accuracy) rather than routing between
  models. A third vendor, Microsoft, now *names* the exact pattern, without a worked example
  either: its own Learn how-to for Decision-1 (below) lists "Model, tool, or agent selection: Choose the
  component that should handle a request" as a common use case, and its Command Line launch blog
  suggests, under "Consider trying out the following" (not a worked example), "Model routing:
  Evaluate an incoming request and select the best model for the task based on quality, cost, and
  latency requirements." The gap narrows again — a third vendor naming model-selection by name —
  but stays open for a worked example.

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
  caught 76% of flawed changes at a 3.4% false-positive rate (2 of 59) on the repos it was tuned
  on, but a fixed threshold wrongly flagged 23% of clean changes on a held-out codebase.
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
- [typesafe-computer-use][tcu-home] (shipped) — a macOS (Windows "experimental") computer-use
  agent, nicknamed "jev" by its own README, that drives the real mouse and keyboard toward a
  plain-English goal. Per its own design principle, "the classifier picks, code decides facts,
  and the writer only writes free text": each step feeds OCR of the frontmost window, the
  accessibility tree, and code-computed facts (date deltas, the focused field, repeated-label
  rows, actions already tried) to the real, hosted TypeSafe Jev model, which answers three
  `Choice` questions — action kind, item, site — before a separate writer model (Anthropic by
  default, swappable to any OpenAI-compatible endpoint) produces free text for a field or the
  final answer and "never picks an action." Its own cost/latency table — "measured on the same
  screenshot and goal, one decision each," a single maintainer's single-task measurement (the
  repo's sole `LICENSE` copyright holder is its author, Aaron Levin) rather than an independently
  reproduced benchmark — reports $0.0002 vs. $0.032 per decision against "Claude Opus 5, bare
  screenshot" (155x cheaper) and 0.13–0.38s vs. 5.2s model latency (14x–40x faster). README's own
  hedge: "Beta. This is under heavy development. Expect rough edges... It drives your real mouse
  and keyboard, so start with a dry run."
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
- [JevSpawn (arXiv:2610.00437)][jevspawn-paper] (documented — a research paper, code released) —
  relaxes this section's own premise that the action vocabulary is "a fixed action/tool
  vocabulary": per its abstract, Jev-style models "offer fast probabilistic predictions over
  finite fields, but require those fields to be specified in advance," so JevSpawn instead infers
  a per-branch, compositional finite action space from natural-language task context rather than
  taking a developer-predefined one. See § Paper: JevSpawn below for the method, benchmarks, and
  its relationship to Jev (which it extends conceptually, not a dependency it runs on by default).
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
  action to take rather than gating one already formed (jev-ultrafast, typesafe-computer-use,
  GLiNER2.5-Decide, Perplexity's own browser-agent cookbook, OpenAI's announced-only "next
  action") — a related but
  distinct decision shape from Adrian's and Perplexity's action-gate pattern. Microsoft's catalog
  page for Decision-1 (below) names the approve/deny pattern too — "Agent guardrails: Evaluate
  proposed agent actions or tool calls before an integrating application permits execution" — but,
  like OpenAI's announced-only mention, ships no worked example to match Perplexity's cookbook; the
  Jev-family-proper gap is still unchanged.

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
- [Cloudflare Clef][clef-blog] (self-reported, narrows but doesn't close this gap) — the launch
  blog's own 10-benchmark table reports nDCG@10 on two retrieval-ranking benchmarks: ToolRet (Clef
  69.19, Clef-flash 66.43, vs. Jev 65.28) and BRIGHT (Clef 45.91, Clef-flash 39.26, vs. Jev 47.52,
  a Jev win) — the first Jev-style model in this doc measured on a ranking metric. A benchmark
  score is not a worked example of sorting a retrieved candidate list in an application, so this
  narrows the gap on evidence, not on use; see § Cloudflare Clef below.
- **Gap, narrowed but not closed**: re-checked 2026-10-11 — neither Jev's docs nor Fastino's
  announcement names query-document reranking, and Clef's own nDCG@10 numbers above are a
  benchmark score, not a worked example; no model in this landscape ships a worked example of
  sorting retrieved candidates by probability. Microsoft names a related capability for
  Decision-1 (below) without a worked example either: the catalog's "Search and document
  relevance: Judge whether search results or documents are relevant to a supplied question or
  task" and the Learn how-to's "Ranking and prioritization: Order incidents, leads, search
  results, or review queues by an application-defined scale." **Failure mode**: not measured by
  any system-1 model here beyond Clef's own nDCG@10 figures above; see the Rerankers entries
  above for cross-encoder latency/calibration trade-offs instead.

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
coding." (That OpenAI, Perplexity, Microsoft, and Cloudflare now *ship* their own Jev-style decision
APIs is this corpus's own conclusion from the first-party docs below, not Panahi's claim.
Cloudflare's Clef and Clef-flash launched 2026-10-01, a week *before* this post, and
Microsoft-Decision-1 launched 2026-10-09, one day *after* it; neither is named among the 24 models
on Panahi's board — but that board is unpublished (below), so this corpus cannot tell whether Clef
was scored and simply didn't place, or wasn't entered at all — see § Cloudflare Clef and
§ Microsoft-Decision-1 below.) Quoted verbatim: "pplx-decider
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
the "board" the author says he ranked 24 models on. Checked 2026-10-09 (7 comments then; 40 on 2026-10-10, of which the 9 visible without
sign-in were read): the post's comments
contain no link to one either — one commenter asks for per-model cost/time stats and examples,
another asks whether severe misses cluster by task, and neither gets a reply in the thread; a
Hugging Face Spaces query scoped to the author
(`huggingface.co/api/spaces?author=MaziyarPanahi`, no search filter) returns his full list of 12
Spaces, none naming Jev, decisions, triage, or clinical; the first page of his Hugging Face
profile (huggingface.co/MaziyarPanahi, 2,817 models / 53 datasets / 20 collections — a subset, not
the full profile) surfaces no matching Space, dataset, or model either; his GitHub profile
(github.com/MaziyarPanahi, first page of 43 repositories) lists none; and two web searches for the
leaderboard and for "pplx-decider" with "669" found no independent page describing it. A 2026-10-10 sweep of his Hugging Face models and datasets by last
modified found two related uploads (the `ModernJEV-Decide-Preview` model and the
`AgentToolDecisions-180K` dataset), both about agent tool-routing, not clinical decisions, and
neither mentions 669 decisions or the models above. Two parts of the post do not check out on
their own terms: GPT-6 Luna's 637 is "tied at #1" with pplx-decider's 643, which the post calls
"the top score", and the tie rule is not given; and "costs 42% less per decision" than Jev does
not follow from the published per-token prices (pplx-decider [$0.02 per 1M input
tokens][pplx-pricing], Jev $0.042 per 1M per [docs.typesafe.ai/models][typesafe-models]), which
give 52% less at equal token counts. Because one miss zeroes every decision in a patient message,
"643 of 669 right" is a clustered score, not per-item accuracy. Treat every number quoted above as
the author's self-report, not an independently reproduced result.

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

**Benchmark (documented; reconciled 2026-10-10)**: the v1.1 card reports its own "Decision Index"
score — 61.56 overall against Jev's 57.9 (v1 scored 56.4), "now outperforms Jev by more than 3.5
points." Per category, v1.1 trails Jev on Knowledge (48.18 vs. 51.4) and leads on Language (69.45
vs. 62.0), Retrieval (61.26 vs. 55.4), Tools (78.88 vs. 75.1, though v1 scored higher at 79.3), and
Arts (44.66 vs. 37.7). The card links the [Decision Index Space][decision-index-space]
(`multimodalart/jev-decision-index`), which describes itself as "Unofficial and
community-maintained; not affiliated with TypeSafe AI". The card's figures are the board's
**edition 0.2.1** numbers: applying that edition's published area weights
([`data/methodology-v0.2.1.json`][decision-index-methodology]: knowledge 0.2585, language 0.2585,
retrieval 0.2002, tools 0.1828, arts 0.10) to the card's own category scores gives 61.557 for v1.1
and 57.903 for Jev, and Jev's and v1's category scores match
[`data/index-v0.2.1.json`][decision-index-v021] (generated 2026-09-28) to two decimals; v1.1 has no
entry in that edition. The board moved to edition 0.3 on 2026-10-06, a day after the card's
release commit. Its current [`data/index.json`][decision-index-current] reports two different
overall numbers: `public_skill` (v1.1 62.25, Jev 57.96), the public-benchmark figure comparable
to the card, and `balanced_skill` (v1.1 62.75), which also blends in the private tests ("50% private
tests of the same skills," "30% private tasks from new domains") and is not comparable to the
card. The card and the board are consistent; the gap between 61.56 and 62.25 comes from category
scores moving between editions. Checked against the Space at commit `f4ecd9f7`, 2026-10-10.

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

### Microsoft-Decision-1 (Microsoft Foundry)

**First-party**: [Microsoft Tech Community launch blog][msft-decision1-blog] · [Microsoft Foundry
model catalog][msft-decision1-catalog] · [Microsoft Command Line blog][msft-decision1-cmdline] ·
[Microsoft Learn how-to][msft-decision1-learn]

Released 2026-10-09 — one day after Panahi's leaderboard post above, so it is not among the 24
models that post scored, and gets no leaderboard-placement paragraph here. Per the
[Foundry catalog][msft-decision1-catalog] (checked 2026-10-10): "Microsoft-Decision-1 is a
decision-scoring model: given a situation and a question with a fixed set of answer options, it
returns a calibrated probability for each option instead of generated text." It uses Jev's own
type vocabulary verbatim — `noul`, `choice`, `score` — per the [Learn how-to][msft-decision1-learn]'s
own table: a `noul` question returns "a probability from 0 through 1"; a `choice` question returns
"one selected option and the probability for each option"; a `score` question returns "a value on
an ordered scale and the probability for each level," where "the returned score is the
probability-weighted average of the level indexes." The wire shape (verified against the how-to's
worked `curl` example and the launch blog's Python sample, both identical): `POST
<foundry-resource-endpoint>/providers/microsoft/v1/systemone`, body `{"model": <deployment-name>,
"state": <text-or-JSON>, "questions": {<name>: {"type": "noul"|"choice"|"score", "instructions":
…, "criteria": …}}}`, response `{"answers": {<name>: {"type": …, …}}}` — the path literally ends
`/v1/systemone`, the same path Laya's self-hosted server exposes (above). Catalog capabilities
include "Explicit abstention: Supports options such as 'cannot tell' when the supplied evidence is
insufficient" and a 32,768-token context window ("Single-pass scoring... over inputs of up to 32K
tokens").

**Status — three first-party statements, two different stages, the OpenAI pattern again**:
Microsoft's own
[Tech Community launch blog][msft-decision1-blog] (2026-10-09, byline Saumil-Shrivastava) states:
"Now available in public preview, Microsoft-Decision-1 is a decision model built on Qwen3.5-9B..."
The [Foundry catalog page][msft-decision1-catalog] for the same model disagrees, in both its
rendered badge and its own embedded page state: "Lifecycle Generally available (GA)" (rendered UI)
and `"lifecycle","Generally Available"` (the page's own JSON). The catalog's License tab, however,
still points at Azure's generic preview terms: `licenseDescription`: "Use of this Azure Direct
Model is subject to supplemental Terms of Use for Microsoft Azure"
(`azure.microsoft.com/.../support/legal/preview-supplemental-terms/`) — not resolved here, quoted
as found on both pages.

**Base model and license (documented)**: "It is built on Alibaba's open-weight Qwen3.5-9B and
post-trained by Microsoft" (catalog) — confirmed independently by the
[Command Line blog][msft-decision1-cmdline]'s own words: "we post trained Qwen3.5-9B for fast,
single-pass decision scoring and will soon rebase it on other models, including Microsoft AI (MAI)
and OpenAI." Training data: "publicly available datasets subject to Microsoft's Open Data process,
plus synthetic data created by the team" (catalog), whose own `trainingDataDate` field reads
"October 2026" — the same month as the launch, quoted as given rather than interpreted. Like
OpenAI's Decisions API above — and unlike Perplexity's open-weight `pplx-decider` checkpoint —
Microsoft-Decision-1 has no released weights to check a `LICENSE` file against: none of the four
first-party pages above links or names a repository, and a Hugging Face API query scoped to the
`microsoft` org (`?author=microsoft&search=decision`) returns an empty list (checked 2026-10-10) —
hosted-only. The catalog's own license field reads `"license","custom"`; no open-source license
applies.

**Pricing (documented, two first-party pages agree, checked 2026-10-10)**: both the
[Tech Community blog][msft-decision1-blog]'s pricing table and the
[Command Line blog][msft-decision1-cmdline] state input costs "$0.042" per "1M" tokens with output
free ("Output tokens are free"), for both US and EU Datazone deployments (GlobalStandard's price
isn't shown on either page) — identical to Jev's own $0.042 per 1M per
[docs.typesafe.ai/models][typesafe-models], already cited above.

**Benchmark (self-reported, Microsoft's own numbers — including chart data the post's own prose
never states)**: the [Command Line blog][msft-decision1-cmdline]'s prose states Microsoft-Decision-1
"achieved the highest accuracy in our 36-benchmark comparison, spanning nearly 150,000 questions
across benchmarks kept blind from training," and was "the fastest measured: 2.5 times quicker than
H2O-Lightning-4B v1.1, the runner-up, and 35 times quicker than GPT-6 Sol" (P50). The post's own
interactive charts — rendered client-side from data embedded in the page, not shown in the prose;
decoded from the page's own embedded iframe payloads, 2026-10-10 — give the per-model numbers
behind that claim. Average accuracy over the 36 benchmarks: Microsoft-Decision-1 83.5%, Jev 1.13.0
82.3%, Quyet-1.0-Large 81.9% ("#1 on JevBench"), Surogate Rune 26B-A4B 79.7%, GPT-6 Luna Decisions
79.4%, deck-31B 77.8%, H2O-Lightning-4B 77.2%, Strands-Decider 2B 54.8% (footnoted "AWS · 23 of 36
benchmarks" — a partial run, not comparable). P50/P95 latency in ms: Microsoft-Decision-1 85/125,
H2O-Lightning-4B v1.1 210/—, Jev 1.13.0 240/—, GPT-6 Luna Decisions 300/—, Quyet-1.0-Large 380/—,
Surogate Rune 26B-A4B 380/—, deck-31B 400/—, GPT-6 Sol 3010/— (a latency reference only, not
ranked for accuracy). So the prose's "runner-up" is a *latency* ranking (H2O-Lightning-4B, at 210
ms); on accuracy, Jev is the closest competitor, 1.2 points behind. A fourth chart — calibration
score over the same 36 benchmarks — is the one number the prose never states, and it does not
favor Microsoft-Decision-1: Jev 1.13.0 ranks first at 93.7, Quyet-1.0-Large second at 93.1,
Microsoft-Decision-1 third at 92.2, ahead only of Surogate Rune (91.8), H2O-Lightning-4B (91.8),
GPT-6 Luna Decisions (89.9), and deck-31B (83.5). The post's own "Appendix: Models benchmarked"
names six of the seven comparison models by source link — all but Jev (Quyet-1.0-Large, Surogate
Rune 26B-A4B, GPT-6 Luna Decisions, deck-31B, H2O-Lightning-4B, Strands-Decider 2B) — even though
an editor's note on the same post states "This post was updated from the original to add
benchmarks for Jev on accuracy and calibration," and Jev's numbers do appear in the charts; the
appendix does not list Jev. Safety (documented): "We tested Microsoft-Decision-1 on
5,250 requests across 11 benchmarks, covering harmful content, jailbreak attempts, and prompt
injection, and found that the model successfully refused harmful behavior while retaining a high
degree of utility." Robustness (documented): "Microsoft-Decision-1 changes its decision on 1.3% of
perturbations on average with zero flips when option descriptions are paraphrased or when options
are reversed or shuffled," across eight paraphrase/reorder perturbations of the same request.

**Internal case study — two Microsoft posts, two different numbers for what reads as the same
study**: the [Tech Community blog][msft-decision1-blog] states "Xbox Research used
Microsoft-Decision-1 to categorize more than 10,000 pieces of open-ended feedback into
researcher-defined themes, reporting quality competitive with GPT-5 while running 80–100 times
faster." The [Command Line blog][msft-decision1-cmdline], describing what otherwise reads as the
same study (same "more than 10,000" feedback items, same "sort... into a fixed set of themes
established by researchers"), names a different comparator and multiplier: "competitive on quality
with GPT-6 Sol while running over 14 times faster and 200 times less expensive." Command Line's
own chart data (decoded, 2026-10-10) gives a per-game breakdown against GPT-6 Sol across three
datasets — Racing Title (753 reviews), First-Person Shooter (341 reviews), Studio Livestream (1,030
posts): mean ms per item 159/188/143 for Microsoft-Decision-1 vs. 2,800/2,600/2,600 for GPT-6 Sol
(14–18x faster), and $0.009/$0.005/$0.013 vs. $1.83/$1.03/$2.92 per run (roughly 212–223x cheaper)
— consistent with Command Line's own "14 times faster... 200 times less expensive," but neither
source gives a number reconciling with Tech Community's separately-stated 80–100x/GPT-5 figure;
the two posts simply name different comparator models for what appears to be one study. Neither
multiplier is independently verified here.

**Documented use cases, cross-referenced to the sections above**: the catalog lists capabilities
quoted verbatim: "AI and agent evaluation: Grades AI responses and proposed agent actions against
supplied criteria or rubrics" and "Groundedness evaluation: Assesses responses against evidence
provided in the input" (§5 Judge, above); "Agent guardrails: Evaluate proposed agent actions or
tool calls before an integrating application permits execution" (§3 Tool-call gating, above —
named, no worked example, the same gap this doc tracks for the Jev family); "Safety and guardrail
checks: Supports content-safety flagging and application-defined thresholds" (§2 Guardrails,
above); "Search and document relevance: Judge whether search results or documents are relevant to
a supplied question or task" (§4 Reranking, above — named, not a worked sort-by-probability
example); "Confidence-based automation: Automate high-confidence outcomes and escalate
low-confidence or ambiguous outcomes for additional review" (§6 Confidence gate, above). The
[Learn how-to][msft-decision1-learn]'s own "Common use cases" list separately names "Model, tool,
or agent selection: Choose the component that should handle a request" (§1 Model routing, above);
the [Command Line blog][msft-decision1-cmdline] states a more specific version of the same idea,
but only as a suggestion ("Consider trying out the following"), not a worked example: "Model
routing: Evaluate an incoming request and select the best model for the task based on quality,
cost, and latency requirements."

No rubric row: under this corpus's gap-driven scoring policy, a new row is added only when it
could change an open cell in the rubric's evidence census. Microsoft-Decision-1 is hosted-only,
like OpenAI's and Perplexity's own APIs above, so this entry doesn't change that census; none is
added here.

### Cloudflare Clef (Workers AI)

**First-party**: [10-01 changelog][clef-changelog-1001] · [10-09 changelog][clef-changelog-1009] ·
[launch blog][clef-blog] · [Clef model page][clef-model-page] · [Clef-flash model
page][clef-flash-model-page] · [Workers AI pricing][workers-ai-pricing] · [HF model card —
Clef][clef-hf] · [HF model card — Clef-flash][clef-flash-hf]

Launched 2026-10-01 — a week before Panahi's leaderboard post above, and not among its 24 models
(see § October 2026 above). Cloudflare ships Clef two ways on its own infrastructure: as two
hosted Workers AI models, `@cf/cloudflare/clef` (27B) and `@cf/cloudflare/clef-flash` (9B), and as
open weights on Hugging Face. Per the launch blog, Clef "follows the System One API" — Jev's own
`noul`/`choice`/`score` question vocabulary verbatim — so "you can switch an existing Jev
integration to Clef by changing the endpoint and model." The Workers AI binding call is
`env.AI.run("@cf/cloudflare/clef", { model, state, questions })`; the REST equivalent is `POST
https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/cloudflare/clef` with a
bearer token. Both take the same body: `model` (`"clef"` or `"clef-flash"`), `state` (text or
structured data), `questions` (1–64 entries, each `noul`/`choice`/`score`), and an optional
`images` array (up to four PNG/JPEG/WebP images, billed as input tokens) — confirmed against both
model pages, 2026-10-11.

**Base model and license (documented)**: both HF cards (checked 2026-10-11) state "Released under
the Apache-2.0 license." Clef post-trains `Qwen/Qwen3.8-27B` (including its vision encoder) with a
small "joint schema head" transformer that scores every option of every question in one forward
pass; Clef-flash post-trains `Qwen/Qwen3.5-9B` the same way. Clef's 27B base is the same checkpoint
family as Perplexity's `pplx-decider-v1.1-27b` above — both cards independently name
`Qwen/Qwen3.8-27B` — two vendors converging on the same base model.

**Context, and a mid-month change (documented)**: at launch (10-01), both models carried a 64K
hosted context window — the launch blog states "our model has a 64k context window (compared to
Jev's 32k)." Jev's own docs give two numbers for the same model, though: "64k tokens per request;
32k tokens for `state` plus the longest question" ([docs.typesafe.ai/models][typesafe-models],
re-checked 2026-10-11) — the blog's comparison uses Jev's narrower, single-question figure, not
its per-request total. On 10-09, Cloudflare cut Clef-flash's *hosted* context to 24,576 tokens to
help fund the price cut below — "only 0.24% of requests exceed 24K input tokens" — while Clef
keeps its 65,536-token hosted window; Clef-flash's self-hosted Hugging Face weights are unchanged
and "support up to 256K tokens" per the 10-09 changelog (which states no corresponding self-hosted
figure for Clef). Both model pages (checked 2026-10-11) confirm the current hosted figures: Clef
65,536 tokens, Clef-flash 24,576 tokens.

**Pricing (documented, checked 2026-10-11; the pricing page is marked "Last updated Oct 9,
2026")**: `clef` $0.240, `clef-flash` $0.038, `clef-omni` (below) $0.150 — all per 1M input tokens,
with no output-token charge ("Clef models do not charge for output tokens," per the Clef-flash
model page). The 10-09 changelog states Clef-flash "now costs $0.038 per million input tokens,
down from $0.090, which makes it cheaper than Jev" — true against Jev's own $0.042/1M figure
already cited above for Microsoft-Decision-1, though the changelog itself never states Jev's
price. Clef's own $0.240 is roughly 5.7× Jev's rate; Cloudflare does not state what Clef cost
before 10-09, only that Clef-flash's price changed.

**Benchmarks (self-reported, mixed — not a clean sweep)**: the launch blog's own 10-benchmark
table has Clef and Clef-flash ahead of Jev on most rows shown (e.g. BFCL case-exact 98.47/98.76
vs. 95.75; BANKING77 macro-F1 94.20/90.93 vs. 79.74; home-appliance case-exact 82.95/97.73 vs.
52.27), but Jev leads two of the ten: When2Call accuracy (80.97 vs. 72.37/65.58) and BRIGHT
nDCG@10 (47.52 vs. 45.91/39.26 — see § Use cases → Reranking above). The model page's own summary:
"across 10 decision benchmarks, a Clef model scores highest on 7" — this corpus did not recount
that tally itself (the "other open decision models" in the comparison aren't named in the public
table). The HF cards run a wider comparison the blog's table omits — Cloudflare's own "Decision
Index" reproduction — and there Jev clearly leads on general-reasoning rows: GPQA Diamond 78.3 vs.
Clef's 48.0, MMLU-Pro 82.7 vs. 65.9, BBH 92.9 vs. 73.7. The blog separately claims Clef "is
currently the leader when evaluated against the Jev Decision Index," but both HF cards label this
same table "our internal run" (one card: "our internal run of the Decision Index 0.2.1 suite") —
a self-run reproduction, not a submission to the public [Decision Index Space][decision-index-space]
already cited above for Perplexity. A partial, non-exhaustive search of that Space's current
`index.json` (roughly 40% of its 1.6M-character file sampled across its length, 2026-10-11) found
no `clef` entry, consistent with "internal run," but the file was not checked exhaustively. A
*different*, independently-run benchmark — Artificial Analysis's unrelated "Decision Index," below
— does score Clef, Clef-Flash, and Clef-Omni directly: all three land in the bottom half of its
eleven decision models, with Clef itself below Jev (48.61 vs. 57.50). See § Artificial Analysis
Decision Index below; this is not a reproduction or rebuttal of the "internal run" claim above, a
different benchmark on different eval sets.

On Typesafe's own four workflow evals, the blog reports Clef/Clef-flash beating Jev on three of
four: invoice processing (64.7/57.1 vs. 61.8), customer service (76.3/77.0 vs. 76.0), and security
incidents (62.9/61.7 vs. 61.7) — but trailing on agent trace observability (68.5/69.8 vs. 71.6).
Jev's own measured median latency on Cloudflare's bench, 524.1 ms, is a third first-party figure
for Jev's speed in this doc, alongside Panahi's 345 ms and Microsoft's 240 ms P50 above — three
vendors' own measurements, not reconciled here. Clef and Clef-flash measured 209.3 ms and 38.8 ms
median respectively against that same 524.1 ms Jev figure (Cloudflare's own "2.5x" and "13x
faster" claims); the same table places two other decision models already in this corpus ahead of
Clef-flash on raw median latency — Laya at 5.8 ms and Kev-9B at 51.4 ms — with the blog conceding
Clef beats "the decision models on latency except for Laya."

**clef-omni (documented, launched 2026-10-09)**: a third model, `@cf/cloudflare/clef-omni`, adds
audio (WAV/MP3) and video (MP4/WebM) input to Clef's text/image inputs, passed as base64 data URLs
in `audio`, `videos`, and `images` fields; "a video's soundtrack is aligned with its frames, so the
model can reason over what is seen and heard at the same time." It runs a 30B-parameter
mixture-of-experts backbone with 3B active parameters — no base-model name is given on either
first-party page. Confirmed public on Hugging Face
(`huggingface.co/api/models/Cloudflare/clef-omni`, checked 2026-10-11: `license: apache-2.0`,
`pipeline_tag: image-text-to-text`, full safetensors shards listed) — hosted *and* self-hostable,
unlike OpenAI's and Microsoft's APIs above. Measured latency: "text takes about 20 ms, image or
audio under 100 ms, and a 21-second video with sound about 300 ms." It leads the Clef family on
BANKING77 (94.8 macro-F1), CLINC150+OOS (97.7 macro-F1), and Amazon ESCI (57.8 macro-F1); priced at
$0.150 per 1M input tokens with a 64K-token hosted context window.

**Serving speedup via SGLang (documented, 2026-10-09)**: the same changelog reports Clef "now
returns decisions up to 2x faster" on Workers AI with unchanged model weights, crediting part of
the gain to moving serving to SGLang: "Clef support is coming to SGLang in version 0.5.22,"
linking a pull request this corpus confirmed merged (`sgl-project/sglang#42721`, checked via `gh
api`, 2026-10-11) — its own title, "[Model] Support Clef and Clef-Flash decision models on
/v1/systemone," serves Clef over the same wire path Laya's and Microsoft Foundry's servers already
expose in this doc (see § Train your own below for a fourth). Cloudflare's "0.5.22" version claim
was not separately checked against an SGLang release. Measured median-latency gains: 1.7× at ~800
tokens, 2.0× at ~3,400 tokens, 1.7× at ~16,000 tokens.

**RL fine-tuning design-partner service (announced)**: alongside the 10-01 launch, Cloudflare is
"offering a service to help customers fine-tune Clef to suit their workloads with our hands-on FDE
team," with a later self-serve platform planned; interested customers can sign up as design
partners via an interest-form link on the blog (not reproduced here).

No rubric row: under this corpus's gap-driven scoring policy, a new row is added only when it
could change an open cell in the rubric's evidence census. Like OpenAI's, Perplexity's, and
Microsoft's own entries above, this one doesn't, so none is added here.

### GLiDE (Fastino Labs)

**First-party**: [Fastino launch blog][fastino-glide-blog] · [Fastino decision-models
comparison][fastino-decision-models-explained] — cross-ref [GLiNER2.5-Decide above][gliner-blog]

Published 2026-09-30 (the launch post's own `<time datetime="2026-09-30">` tag; its page template's
separate, unrelated Framer build timestamp reads 2026-10-15, which this corpus does not read as a
second publish or edit date). Billed as "the first thinking decision model," GLiDE ("Generalized
Lightweight Decision Engine," per the blog's own expansion) is adaptive rather than single-pass:
per the post, it "first produces a fast probability distribution, then allocates additional
reasoning when the leading result is uncertain" — reasoning that happens *inside* GLiDE's own call
("thinking tokens count against the same window"), unlike AnyJev's `Tacit.adaptive` or
JEV-as-a-Judge above, both of which escalate to a *separate* model or judge from outside rather than
reasoning within the decision call itself. Fastino's own 2026-10-14 roundup, "Decision Models
Explained," lists GLiNER2.5-Decide and GLiDE as two separate rows in its own "Top decision models in
2026" table — GLiNER2.5-Decide: "Compact English classifier for supplied labels, routing, tagging,
and operational decisions" (Apache 2.0 weights); GLiDE: "Additional reasoning when the initial
decision is uncertain, while returning structured answers" (Hosted API) — with no sentence anywhere
in either post stating a lineage between the two; this corpus treats them as separate products, not
a version of one another. The API "conforms to the System One model schema" at
`https://api.fastino.ai/v1/systemone`, model id `fastino/glide`, with a 40,000-token context window
("GLiDE's context window spans 40k tokens"); oversized requests are rejected. Unlike GLiNER2.5-Decide,
the launch post gives no license and no Hugging Face link — checked against the Fastino Hugging
Face org page (2026-10-15): none of its 16 listed models is named GLiDE, so this corpus treats it as
hosted-API-only. Pricing is not stated on the post itself (it points to Fastino's own docs).

**Benchmark (self-reported, on the *community* Decision Index, not the Artificial Analysis one
below)**: "GLiDE achieves a score of 64.81, leading Jev's published score of 57.91 by 6.90 skill
points" on "Decision Index 0.2.1" — the same `multimodalart/jev-decision-index` community
benchmark already cited above for Perplexity's pplx-decider — run with the Space's own scorer but
not submitted to it: "GLiDE has not been added to the public leaderboard, where submissions to
version 0.2.1 are currently paused." Per-area: "Tools and Automation: 83.5 vs 75.1, a lead of 8.4
skill points" and "Knowledge and Reasoning: 62.9 vs 51.4, a lead of 11.5 skill points"; overall, "it
outperforms Jev across all five evaluation areas and on 31 of 38 benchmarks." Jev is the only other
model named in the post's comparisons. See § Artificial Analysis Decision Index below for GLiDE's
score on an unrelated, independently-run benchmark that gives a materially different result.

No rubric row: under this corpus's gap-driven scoring policy, a new row is added only when it could
change an open cell in the rubric's evidence census. Like the other October 2026 vendor entries
above, this one doesn't, so none is added here.

### Celeris-1 Decision (Celeris Labs)

**First-party**: [launch post][celeris-decision-blog] · [API docs][celeris-decisions-docs] ·
[pricing][celeris-pricing]

Celeris (LinkedIn company name "Celeris Labs") describes itself as "Building the world's fastest
language models, powered by diffusion" — its flagship Celeris-1 is a diffusion LLM, not an
autoregressive one; Celeris-1 Decision, launched 2026-10-08, is the diffusion-based decision model
built on that base, described in the launch post as "a diffusion language model built for typed
decisions" that answers "questions about text or images with probabilities" (API docs). It can
return a free-text one-sentence explanation alongside the typed answer, togglable via an
`x_celeris: {explain: true}` request flag that is not part of Jev's own vocabulary — the launch
post's own description is "It returns a reason with each response," and separately notes
explanations are available "on request," so this corpus does not read that as every call producing
one automatically, and found no first-party claim that this is unique among hosted decision models.
The API is System-One-shaped at `POST https://inference.celeris.ai/celeris-1-decision/v1/systemone`
— the docs state it "follows the systemone convention, so existing clients can point to the Celeris
base URL" — plus an OpenAI-Decisions-API-shaped `POST /v1/decisions` on the same model; images are
supported via `x_celeris.images`. On license and weights, the launch post is explicit: "There are
no open weights and no fine-tuning in this release." No context-window figure or self-hosting
option is stated anywhere in Celeris's own docs or launch post (checked 2026-10-15).

**Benchmark (self-reported, Celeris's own "decision-benching harness")**: the launch post's own
table, run with one scorer across providers, has Celeris-1 Decision leading Perplexity's
pplx-decider-v1.1-27b, Inception's Mercury Decide, Jev 1.13.0, and OpenAI's gpt-6-luna on both
accuracy and Brier score across the full jev-bench (22 datasets, 3,210 items: 0.800 accuracy / 0.272
Brier, vs. Jev's 0.731 / 0.380) and a narrower "typed-decisions" split (0.765 / 0.079, vs. Jev's
0.736 / 0.149), with the post's own words: it "wins 17 of the 22 datasets." Measured median
latency (one question, from AWS us-east-1, a region neither Celeris nor Jev serves — the post notes
every figure therefore includes a cross-region network path): 67 ms, against Perplexity 122 ms,
Mercury Decide 147 ms, Jev 135 ms, and gpt-6-luna 110 ms. Pricing: $0.04 per 1M input tokens
(confirmed on the separate pricing page), output and explanations both free.

No rubric row: under this corpus's gap-driven scoring policy, a new row is added only when it could
change an open cell in the rubric's evidence census. Like the other October 2026 vendor entries
above, this one doesn't, so none is added here.

### d1 (Liquid AI)

**First-party**: [hosted-API launch blog][liquid-d1-blog] · [open-weight launch
blog][liquid-d1-open-blog] · [Hugging Face model card — d1-3b][liquid-d1-hf]

Liquid AI shipped d1 in two stages. The hosted API (2026-10-05 blog) is "our first decision model,"
answering `noul`/`choice`/`score` questions (`noul`: "a yes/no question, answered with a
probability between 0 and 1") "in one forward pass" and "without generating any tokens," at `POST
https://api.liquid.ai/decisions/v1/systemone` — the page states no explicit System-One-compatibility
claim, but the path and `state`/`questions` body shape match this doc's vocabulary. Text decisions
take "200 to 300 ms." Pricing: $0.04 per 1M input tokens, images billed at "1.5 tokens per
32×32-pixel patch." The blog's only comparison to this doc's base model is one unquantified
sentence: "last week's experimental release" made d1 "the first model to rival Jev on text
decisions."

The open-weight release (2026-10-07 blog) ships two self-hostable checkpoints on Hugging Face:
`LiquidAI/d1-3b` (3.12B parameters, a SigLIP2 NaFlex vision encoder of about 400M, 32,768-token
context, built on `LFM2.5-VL-3B`) and the audio-capable `LiquidAI/d1-omni-600M` (600M, an "early
research release," no benchmarks reported for it on the blog). Both are called "Open-weight":
"Download, fine-tune, and deploy without restrictions" — but the d1-3b model card's own license
field reads `lfm1.0`, a custom Liquid license tagged `other` on Hugging Face's own API metadata
(not a recognized standard identifier; `gated: false`, checked 2026-10-15); treat "without
restrictions" as the vendor's own characterization, not a statement about license terms. Measured latency, d1-3b,
one question: 8 ms (NVIDIA RTX 4090), 9 ms (AMD MI325X), 30 ms (Apple M5 Pro), 16–50 ms across three
Jetson boards.

**Benchmark (documented, model card, on the *community* Decision Index, not the Artificial
Analysis one below)**: d1-3b scores 48.57 overall on "Decision Index 0.2.1" (the same community
benchmark cited above for Perplexity and GLiDE) — sub-scores Knowledge 23.8, Language 56.4,
Retrieval 52.8, Tools 74.5, Arts 36.3 — well below both Jev's 57.9 and GLiDE's self-reported 64.81
on that same community index. d1-omni-600M scores 15.95 on the same index.

No rubric row: under this corpus's gap-driven scoring policy, a new row is added only when it could
change an open cell in the rubric's evidence census. As with Perplexity's own open-weight
pplx-decider above, shipping open weights doesn't by itself trigger a row for an entry in this
October 2026 vendor grouping; this one doesn't change an open cell either, so none is added here.

### Mercury Decide (Inception Labs)

**First-party**: [API docs][inception-decide-docs] · [pricing][inception-pricing]

Inception Labs — maker of the Mercury diffusion-LLM family — ships Mercury Decide as a hosted
decision endpoint with no dedicated launch blog post of its own on `inceptionlabs.ai/blog` (checked
2026-10-15: the site's homepage links the model only via an "Introducing Mercury Decide" banner
pointing to its OpenRouter listing, not to a first-party post); the model's first-party home is
instead a docs page, `docs.inceptionlabs.ai/capabilities/decisions`, whose own homepage card
describes it: "Classify, route, and score with typed decisions and probabilities." Per that docs
page, Mercury Decide answers at `POST /v1/decisions` — OpenAI's endpoint naming, not Jev's
`/v1/systemone` path — taking a `state` plus a map of named `noul`/`choice`/`score` questions
(Jev's own type names, unlike OpenAI's `predicate`) and returning per-type answers (`noul`: a 0–1
probability; `choice`: the top option plus `probabilities` and `confidence`; `score`: a
probability-weighted average level, `legend`, `probabilities`, `confidence`). It does not support
streaming or tool calling. Pricing, confirmed on two first-party pages: "$0.02 per million input
tokens (50% off the regular $0.04 price)," output free (reported in `usage` but not charged). No
context-window figure, parameter count, license, or benchmark number appears on either first-party
page (checked 2026-10-15) — both leave a blank or a dash where one would go.

No rubric row: under this corpus's gap-driven scoring policy, a new row is added only when it could
change an open cell in the rubric's evidence census. Like the other October 2026 vendor entries
above, this one doesn't, so none is added here.

## Artificial Analysis Decision Index (third-party benchmark, launched 2026-10-13)

[Artificial Analysis][aa-decision-index-article] — a vendor-neutral AI-model-benchmarking firm, not
a decision-model vendor itself — launched its own "Decision Index" on 2026-10-13, independently
scoring decision models (and, separately, ordinary LLMs prompted to answer the same typed
questions) on four evals it already runs. **This is not the same benchmark as the community
"Decision Index" cited several times above** (the Hugging Face Space
`multimodalart/jev-decision-index`, editions 0.2.1/0.3, used by Perplexity's pplx-decider card,
Fastino's GLiDE post, and Liquid AI's d1 card): that one is run by an unaffiliated third party on
its own curated eval mix; Artificial Analysis's is run by a separate commercial benchmarking firm on
its own four named evals, launched a week after the community index's edition 0.3 (2026-10-06,
above).
The near-identical name is coincidental — this corpus never adds the two together or treats one as
validating the other.

**Composition (documented, methodology page, checked 2026-10-15)**: "a weighted average of" four
evals, 25% each — **AA-Omniscience-Decision** (500 private questions, five options each including
"I don't know"; accuracy 12.5% + non-hallucination rate 12.5%, where non-hallucination rate is
100 × (1 − the share of wrong-not-"I-don't-know" answers among all incorrect ones)); **HLE-MultiChoice**
(513 of Humanity's Last Exam's 2,500 questions, text-only multiple-choice, reasoning);
**When2Call** (3,423 of NVIDIA's 3,652 tool-calling tasks, ambiguous ones removed, tool-calling
accuracy); **WildGuardTest** (835 of Ai2's 1,725 rows, kept only where all three annotators agreed,
safety classification, average F1). Call format, quoted verbatim: "Decision models choose from a
fixed set of options, with a probability for each, in one call" — ordinary LLMs instead answer
"with a structured output that names the option it chose, so it gives no probability for each
option." The page labels
this "Version 1.0," described only as "October 2026 to current"; it states no rule for when a v1.1
might follow.

**Scores (documented — both the 2026-10-13 launch article and the live leaderboard's own embedded
data, fetched via polyfetch 2026-10-15; the two agree within normal rounding, e.g. Jev 57.50 live
vs. "58" at launch, so this corpus treats them as the same index at two points in time, not a
methodology change)**. All 11 decision models the index currently scores, sorted by index score,
cost and latency from the live data (`$` = cost per **million tasks**, derived from the page's own
per-task cost field; `ms` = median time per task):

| Decision model | Host (per AA) | Index | Omniscience acc. | Non-hallucination | HLE-MultiChoice | When2Call | WildGuardTest | $/1M tasks | ms |
|---|---|---|---|---|---|---|---|---|---|
| Jev 1.13 | TypeSafe | 57.50 | 34.6 | 35.2 | 20.9 | 80.7 | 93.6 | $42 | 127 |
| GLiDE | Fastino | 53.91 | 36.4 | 16.4 | 10.5 | 83.7 | 95.1 | $119 | 217 |
| Microsoft-Decision-1 | OpenRouter | 53.76 | 28.2 | 39.8 | 10.9 | 81.9 | 88.2 | $31 | 207 |
| Decider v1.1 27B (pplx-decider) | Perplexity | 53.06 | 39.8 | 13.3 | 15.4 | 76.5 | 93.8 | $17 | 170 |
| Mercury Decide | Inception | 52.72 | 35.0 | 32.0 | 10.1 | 79.3 | 88.0 | $30 | 500 |
| Celeris-1 Decision | Celeris | 52.29 | 37.8 | 0.0 | 13.3 | 83.7 | 93.3 | $32 | 63 |
| d1 | Liquid AI | 50.29 | 41.0 | 1.7 | 11.5 | 77.4 | 90.9 | $30 | 299 |
| Clef | Cloudflare | 48.61 | 39.0 | 4.3 | 11.1 | 71.0 | 90.7 | $199 | 309 |
| GPT-6 Luna (Decisions) | OpenAI | 48.49 | 40.6 | 10.1 | 11.7 | 74.1 | 82.8 | $79 | 168 |
| Clef-Flash | Cloudflare | 45.81 | 32.6 | 2.7 | 10.3 | 64.4 | 90.9 | $32 | 298 |
| Clef-Omni | Cloudflare | 44.26 | 36.0 | 1.6 | 9.0 | 62.1 | 87.2 | $123 | 172 |

Every row is a *new* run by Artificial Analysis itself, not a number carried over from the model's
own section above; see those sections (§ OpenAI Decisions API, § Perplexity pplx-decider,
§ Microsoft-Decision-1, § Cloudflare Clef, and the four new entries above) for each model's own
pricing/license/API details, not repeated here. Note the host column: Artificial Analysis runs
Microsoft-Decision-1 through **OpenRouter**, not Microsoft Foundry directly — the only one of the
eleven not benchmarked against its own first-party endpoint.

**Per-eval leaders among decision models (computed from the table above)**: reasoning
(HLE-MultiChoice) — Jev 1.13; knowledge accuracy (AA-Omniscience-Decision) — d1; non-hallucination
rate — Microsoft-Decision-1 (39.8), then Jev (35.2), then Mercury Decide (32.0); tool calling
(When2Call) — Celeris-1 Decision and GLiDE, tied (83.7); classification (WildGuardTest) — GLiDE
(95.1). Cost spans $17 (Decider v1.1 27B) to $199 per million tasks (Clef); latency spans 63 ms
(Celeris-1 Decision) to 500 ms (Mercury Decide).

**LLM baselines (not decision models — prompted to answer the same questions as structured JSON)**:
of the 15 language-model configurations the index separately tracks (26 models in all, decision
models plus LLMs), the launch article names two explicitly: **Claude Haiku 5.5 (Low)** scores 61 at
launch (60.59 live), 3 points above Jev, at $184/1M tasks and 1.4 s; **GPT-6 Luna (Low)** scores 55
at launch (55.18 live), below Jev, at $131/1M tasks and 1.5 s. The live leaderboard's own data shows
most of the other 13 LLM configurations it tracks (across Claude Haiku/Opus and GPT-6/6.1 effort
levels) also scoring above Jev's 57.50 — so "beats Jev" is not rare among LLM baselines on this
index, only among the eleven decision models. Both of the article's two named baselines cost
roughly 3–4x Jev's $42 and run an order of magnitude slower (Jev: 127 ms) — the same speed/cost
trade-off this doc's § Use cases and vendor sections already document for Jev-style models vs. full
LLM calls, now measured by a third party on a shared eval set instead of each vendor's own
benchmark.

**Calibration (documented, article, re-checked verbatim 2026-10-15)**: under the heading "Decision
models are overconfident," the article states "across almost all probability levels, accuracy
falls below that probability for all decision models," but "most decision models are relatively
well-calibrated on When2Call (tool calling) and WildGuardTest" (classification). Separately:
"Calibration for language models coming soon" — not yet published. The calibration
chart's own legend lists nine entries: Jev 1.13, GLiDE, Microsoft-Decision-1, Decider v1.1 27B,
Mercury Decide, Celeris-1 Decision, d1, Clef, and GPT-6 Luna (Decisions) — Clef-Flash and Clef-Omni
are scored in the main table above but not broken out on the calibration chart.

**Coverage — which corpus models this index does and doesn't include (checked 2026-10-15)**: of the
independent/open-weight projects covered earlier in this doc, none appear on the Artificial
Analysis Decision Index — Laya, kev, CLM, RuVector, GLiNER2.5-Decide, JevK5, SemIf, and AnyJev are
all absent, alongside BioDecision-4B and the Jev-family tooling (abide, jev-ultrafast, jevgrep,
typesafe-computer-use, pg-jev, probably). The eleven scored are exactly: TypeSafe's Jev, three
major-vendor Jev-style APIs already in this doc (OpenAI's GPT-6 Luna Decisions, Microsoft-Decision-1,
and Perplexity's pplx-decider, branded here "Decider v1.1 27B"), Cloudflare's three Clef variants,
and the four vendor models new to this doc above (GLiDE, Celeris-1 Decision, d1, Mercury Decide). A
future Artificial Analysis run could add any of the absent names; this corpus found no
request-to-add mechanism that would change this list retroactively.

**A contrast worth flagging, not resolved here**: GLiDE's own launch post (above) reports a 64.81
score on the *community* Decision Index, 6.90 points above Jev's 57.91 on that same board. On this
*separate* Artificial Analysis index, GLiDE scores 53.91 — below Jev's 57.50, the opposite ranking.
The two benchmarks share no eval sets, so neither figure contradicts the other on its own terms;
this corpus states both, dated and sourced, rather than reconciling them into one number.

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

## Train your own: Unsloth decision-model training

**First-party**: [release v0.1.904-beta][unsloth-release-0.1.904] · [training
guide][unsloth-decision-guide] · [example notebook][unsloth-decision-notebook] · [local serving
docs][unsloth-decision-laya-serving] · [dataset: LocalLLaMA/typed-decisions][typed-decisions-dataset]

Not a new decision-model architecture but a **training path**: Unsloth's v0.1.904-beta release
(2026-10-07, titled "Train your own Decision model") adds two classes, `FastDecisionModel` and
`DecisionTrainer`, that turn an ordinary base LLM into a Jev-style typed-decision model. Per the
guide's own framing: "A small head, the same design as Cloudflare's Clef [above], looks at the
LLM's output over each question and option" — the same joint-schema-head pattern Cloudflare's own
Clef cards describe (§ Cloudflare Clef above), built generically over whichever base the user
fine-tunes rather than Cloudflare's fixed Qwen3.8-27B/Qwen3.5-9B pair. Supported bases per the
guide: Qwen3.5 (0.8B/2B/4B), Qwen3.8, Llama 3.2 3B, and Gemma 4 E4B ("other LLMs that Unsloth can
fine-tune should work the same way").

**Method (documented, notebook + release)**: the example notebook
([`Qwen3_5_(4B)-Decision.ipynb`][unsloth-decision-notebook]) loads `unsloth/Qwen3.5-4B`
4-bit-quantized (`load_in_4bit = True`) with LoRA adapters (`r = 16`, `lora_alpha = 16`) — the
release notes label this combination "QLoRA" ("Train any text or vision LLM as a Jev-style
decision model using QLoRA"), though the notebook's own text never uses that word, only "LoRA
adapters" and "4 bit quantization." `DecisionTrainer(model=model, processing_class=tokenizer,
train_dataset=train_items, eval_dataset=eval_items, args=TrainingArguments(...))` trains the new
decision head and LoRA weights together on `LocalLLaMA/typed-decisions`
(`state`/`questions`/`gold` rows); a quick run (`max_steps = 60`) is swapped for a full run
(`num_train_epochs = 2`, `max_steps` removed) for production fine-tunes.
`FastDecisionModel.predict(model, tokenizer, state, questions)` takes the same
`state`/`questions`/`criteria` shape as Clef and Jev (`noul` takes no criteria; `choice` takes a
dict of option names to descriptions; `score` takes an ordered list of levels) and returns an
`answer` plus a `probabilities` dict per question. `FastDecisionModel.calibrate(model, tokenizer,
eval_items)` fits a temperature so that, per the notebook, "an answer given with 90% confidence is
right about 90% of the time," reporting an `ece` (calibration error) score.

**Reported numbers — two different runs, kept separate**: the notebook's own quick run reports
"about 30% accuracy" before training, "75% to 78%" on the test split after 60 steps, and "80% to
84% held-out accuracy and an `ece` of 0.02 to 0.06"; a full 70-step/2-epoch run reaches 78% test
accuracy in 25 minutes on an A100. The separate training guide reports a different, larger
3,000-row test (2,000 `typed-decisions` rows plus 500 each from BANKING77 and CLINC150) across
five base models: Qwen3.5-0.8B (36%→73% on typed-decisions, 78% held-out, 4GB VRAM, 42 min),
Qwen3.5-2B (33%→78%, 81% held-out, 8GB, 40 min), Llama 3.2 3B (79% held-out, 4.1GB, 30 min), Gemma
4 E4B (77% held-out, 14.4GB, 49 min), and a fine-tuned Laya checkpoint (77% held-out, 2.5GB, 10
min) — plus a separate quick-try figure for Qwen3.5-4B, "76% in 10 minutes on an L4" at `max_steps
= 60`. Treat the notebook's and the guide's numbers as different runs on different data, not one
result restated.

**Dataset (documented)**: [`LocalLLaMA/typed-decisions`][typed-decisions-dataset] is
Apache-2.0-licensed and tagged `Synthetic` (no prose on the card states its generation method). It
has 5 configs — `agent_trace_observability`, `customer_service`, `invoice_processing`,
`security_incidents`, and the combined `all` — with each of the four workflow configs split 300
train / 100 test rows (confirmed per-config via the Hugging Face Datasets Server API, 2026-10-11);
`all` combines them into 1,200 train / 400 test rows (1.6k total), matching the card's own "all
(1.6k rows)" label.

**Serving the trained model (documented)**: `UNSLOTH_SYSTEMONE_MODEL=/path/to/merged/model
unsloth studio -H 0.0.0.0 -p 8888` serves a fine-tuned model behind the same local
TypeSafe-compatible endpoint Unsloth already exposes for Laya (above): `POST
http://localhost:8888/v1/systemone`, `model` resolving to `laya`/`default`/`jev-latest` (or a
specific checkpoint name such as `laya-multilingual`), and the `typesafe-sdk` Python client
pointed at it via `TYPESAFE_BASE_URL=http://localhost:8888` — the fourth distinct
`/v1/systemone`-path server in this doc, after Laya's own server, Microsoft Foundry's hosted one,
and the sglang PR serving Cloudflare's Clef (§ Cloudflare Clef above). The docs flag one migration
caveat verbatim: "`confidence` uses a different formula [from Jev's], so a threshold tuned on Jev
won't transfer; threshold on `probabilities` instead." A link inside the notebook's own closing
cell — "read our guide" at the path `docs/models/decision-model-training` — 404s (checked
2026-10-11: "The URL `models/decision-model-training` does not exist"); the guide cited above
(`/docs/basics/train-your-own-decision-model-with-unsloth`) is the page that actually exists.

**License (observed, three different licenses in one project)**: the `unslothai/unsloth`
repository's root `LICENSE` is Apache-2.0 (confirmed by fetching its content via `gh api`,
2026-10-11); the Decision API server lives under `studio/`, whose own `studio/LICENSE.AGPL-3.0`
file is the GNU AGPLv3 (confirmed the same way) — so the training library and the local serving
app it ships carry different copyleft terms. The example notebook carries a third, separate
license: its own first markdown cell states "This notebook is licensed [LGPL-3.0]."

No rubric row: this is a training path layered on an existing serving app (Laya's own server,
scored above) and existing base models, not a new decision-model architecture of its own — the
same reasoning this doc already applies to pg-jev and probably.

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

Six projects call Jev (or an alternative decision model) as one step in a larger tool. Four have
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
- **typesafe-computer-use** (awlevin) — a macOS computer-use agent whose per-step
  action-selection loop asks the real, hosted TypeSafe Jev model three `Choice` questions (action
  kind, item, site). See § Use cases → Tool-call gating above.
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

## AnyJev (nokia-applied-research)

**Repo**: [nokia-applied-research/AnyJev][anyjev] | **License**: Apache-2.0 (confirmed against
`LICENSE`) | **Stars**: 1,183 / 144 forks, created 2026-09-21, pushed 2026-10-07 (`gh api`,
2026-10-11)

Turns any open causal LM into a Jev-style decision model two ways. Per the README's own author
block, nine co-authors span Nokia (Sunnyvale, CA), Tencent Hunyuan, and the Hong Kong Polytechnic
University; a companion arXiv technical report — [arXiv:2610.00831][anyjev-paper], "AnyJev
Technical Report," submitted 30 Sep 2026 (v1), same nine authors — is cited from the README's own
citation block, confirmed here only for its title, authors, and submission date (this corpus's
fetch of the abstract page could not reproduce its text verbatim, so no figures or quotes from the
paper are repeated here; the README's own numbers, below, are the first-party source for this
entry). **Training-free** (`Decider`, level `L0`): reads a typed decision from any
HF-transformers/vLLM/SGLang/llama.cpp backend's own next-token distribution, with no training and
no labels,
debiasing option-order and label-prior effects by averaging over cyclic rotations of the option
list, with a rotation-budget stopping rule calibrated against its own full-cycle answer rather than
against held-out labels. **Self-distilled** (`Tacit`): five Hugging Face checkpoints (1.7B–9B, on
Qwen3/Qwen3.5 bases; `Tacit-9B` confirmed public and ungated via the Hugging Face API, 2026-10-11)
trained by self-distillation to answer in one forward pass what the model reaches by reasoning,
with `adaptive=True` escalating a capped share of low-confidence decisions back to chain-of-thought.
Per the README, verbatim: "Not affiliated with TypeSafe AI or Jev."

**API shape vs. System One (documented, from the README's own code samples)**: the two entry
points differ. `Decider.decide(state, [Question.choice(...), ...])` takes one `state` plus a
**list** of named `Question` objects, with answers returned keyed by name — the same
multiple-question-per-call shape as the `state`+`questions` vocabulary this doc tracks for
Jev/Clef/Microsoft-Decision-1/Perplexity's hosted API above, just expressed as Python objects
rather than one JSON body. `Tacit.decide(state, question, options)` and the HTTP gateway's `POST
/v1/decide` instead take one `state` plus a single `question` and `options` list per call
(`{"state", "question", "options"}`), with multiple items batched via `decide_batch([...])` or
`{"items": [...]}` rather than one multi-question request — a narrower, per-item shape for the
self-distilled path. Per the README, the gateway "listens on 127.0.0.1 and has no authentication
of its own." The README is not internally consistent on its own type vocabulary: the
`Tacit`/gateway code sample uses `kind` values `choice` (default), `yes_no`, and `score`, while the
project's own roadmap line reads "`choice`, `noul` and `score` from one prefill" — `yes_no` and
`noul` naming the same binary type in two places of the same document; both are reported here, not
resolved (the same kind of same-document inconsistency this doc already notes for OpenAI's
`predicate`, above).

**Numbers (self-reported — the README's own words: "Every number in this README is read from
committed JSON," not independently reproduced here)**: on Qwen3-8B/BANKING77 20-way (300 test
items), going from raw logits to L0: order-flip rate 0.230 → 0.073, accuracy 0.747 → 0.803,
calibration error (ECE) 0.240 → 0.184, share auto-decidable at ≤5% error 7.7% → 46.3%. The rotation
budget reads ~7.2 of 18 rotations at a "certified" 1% disagreement vs. the full cycle, for 2.2x more
decisions/sec on vLLM and 2.3x–2.7x on transformers, "with accuracy unchanged." Tacit accuracy on
the third-party [JevBench][jevbench] public set (231 items) and the `bev-decision` test split
(46,320 items), one-forward-pass vs. adaptive (escalated share in parentheses): Tacit-9B 0.823 /
0.887 (15.2%) and 0.727 / 0.755 (18.1%); Tacit-4B 0.723 / 0.758 (14.3%) and 0.663 / 0.704 (17.8%);
Tacit-8B 0.736 and 0.663 (adaptive not yet run); Tacit-2B 0.671 and 0.626 (adaptive not yet run);
Tacit-1.7B 0.619 and 0.598 (adaptive not yet run) — the README's own roadmap marks escalation
results for Tacit-8B/2B/1.7B "come next."

No rubric row: under this corpus's gap-driven scoring policy, a new row is added only when it could
change an open cell in the rubric's evidence census. This entry doesn't, so none is added here.

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

## Paper: JevSpawn (Fudan, SJTU, Shanghai Innovation Institute)

**Paper**: [arXiv:2610.00437][jevspawn-paper] — "JevSpawn: Adaptive Agentic Inference through
Compositional Action Spaces" (Haoyang Su, Weiran Huang). The paper's own affiliation block lists
three institutions — Fudan University, Shanghai Jiao Tong University, and Shanghai Innovation
Institute (the last listed twice) — without a per-author mapping recoverable from the rendered
page. Submitted 30 Sep 2026; v1 is the only version as of 2026-10-10. Code released at
[github.com/Hoyant-Su/JevSpawn][jevspawn-repo].

**Relation to Jev — established from the paper's own text, not assumed**: JevSpawn extends the
Jev-style finite-field interface rather than running on Jev by default. Its abstract states
(quoted verbatim): "Jev-style models offer fast probabilistic predictions over finite fields, but
require those fields to be specified in advance. This requirement limits autonomous task solving,
where the available actions must be derived from natural language instructions and adapted
through interaction." Its own experimental setup states "JevSpawn and the seven agent baselines
use Qwen3.8-27B as the pretrained policy" — Qwen, not Jev, is the default scorer. The paper
separately measures a "TypeSafe Jev variant," defined in its own appendix as one that "uses API
model jev-1.13.0 for finite scoring and Qwen for declarations and text generation" — the real Jev
API substituted for JevSpawn's own scoring step, benchmarked head-to-head against the default and
seven other agent baselines, not merely named. The repository's README repeats this as one of
three reported configurations: "**TypeSafe Jev** — JevSpawn with API-based finite scoring,"
with a public entry point at `src/jev_spawn/api.py` (`gh api`, 2026-10-10).

**What it is (documented)**: a compositional policy that infers a per-branch finite action space
— named fields with permitted values, plus a renderer turning a complete field assignment into an
executable action — from natural-language task context, instead of taking a developer-predefined
vocabulary. A bounded beam of candidate field assignments is scored by joint probability using
shared-prefix batched evaluation; each candidate runs in its own copy of the environment,
observations update branch history, the top-ranked branch is kept, its declaration can be
revised, and earlier branches stay available for backtracking. No additional training is used.

**Benchmarks (documented — eight tasks, five suites; figures from the paper's own Table 1/Table
2, which the repository README republishes unchanged)**: PPNL, Maze and Grid report success
rates (0–1); LightsOut, RushHour, Sokoban, 2048 and Nullify report benchmark rewards/scores,
against seven agent baselines (LATS, LLMCompiler, AgentPrune, HiAgent, FoldAgent, DyFlow,
LatentMAS). Selected results, JevSpawn (default, Qwen-scored) vs. the strongest *other* baseline
per column:

- Maze 0.960 (tied with the TypeSafe Jev variant) vs. FoldAgent 0.520.
- Grid 0.950 vs. FoldAgent 0.730.
- 2048 score 305.120 vs. LLMCompiler 5.000.
- Nullify reward 0.210 vs. HiAgent/FoldAgent 0.090 (tied).
- Latency: 40.91 s on Maze and 40.58 s on Grid, against the fastest other baseline on each column
  (AgentPrune 47.91 s on Maze; FoldAgent 61.44 s on Grid).
- **Not a universal win, by the paper's own numbers**: AgentPrune scores highest on PPNL (0.956
  vs. JevSpawn's 0.950), RushHour (0.453 vs. 0.390) and Sokoban (0.790 vs. 0.150); LLMCompiler
  (13.61 s) and HiAgent (16.25 s) both beat JevSpawn's own 21.88 s latency on PPNL.

**Jev-as-scorer, measured (documented)**: swapping the real Jev API in for JevSpawn's own Qwen
scorer gives mixed, roughly comparable task quality across the eight columns — the TypeSafe Jev
variant scores higher on PPNL (0.955 vs. 0.950), LightsOut (0.660 vs. 0.610) and Sokoban (0.250
vs. 0.150), ties on Maze (0.960 each), and trails on Grid (0.930 vs. 0.950), RushHour (0.290 vs.
0.390), 2048 (296.000 vs. 305.120) and Nullify (0.170 vs. 0.210) — but costs more latency on every
one of the eight tasks: per the paper's own text, "The TypeSafe Jev variant takes 1.4 to 2.1 times
as long as Qwen scoring across all eight tasks, including API communication."

**Code and license (documented + observed)**: the abstract states "Code is available at
`https://github.com/Hoyant-Su/JevSpawn`," confirmed public (`gh api`, 2026-10-10: 5 stars, 1 fork,
Python, pushed 2026-10-02). No `LICENSE` file exists in the repository root, and its README states
no license terms (checked 2026-10-10) — treat the code as unlicensed, not open-source, until the
author adds one. A GitHub search for "JevSpawn" (`gh api search/repositories`, 2026-10-10) returns
only this repository and the same author's `JevSpawn_web_demo` companion demo — no unrelated or
competing project shares the name.

No rubric row: under this corpus's gap-driven scoring policy, a new row is added only when it
could change an open cell in the rubric's evidence census. This entry doesn't, so none is added
here.

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
| Decision Index data at Space commit `f4ecd9f7`: [methodology v0.2.1][decision-index-methodology] · [index v0.2.1][decision-index-v021] · [current index][decision-index-current] | Area weights and edition 0.2.1 scores that reproduce the card's 61.56 / 57.9; edition 0.3 `public_skill` vs `balanced_skill` (checked 2026-10-10) |
| [Perplexity Decisions API — ticket-triage cookbook][pplx-ticket-triage] | Routing worked example (escalate/review/queue/auto_reply/close) |
| [Perplexity Decisions API — action-gate cookbook][pplx-action-gate] | Approve/deny gate on a proposed `schedule_payment` call |
| [Perplexity Decisions API — browser-agent cookbook][pplx-browser-agent] | Next-action selection (click/dismiss/scroll/stop) with measured per-step latency |
| [Perplexity Decisions API — answer-gate (citation-accuracy) cookbook][pplx-answer-gate] | Citation/grounding verification of another model's generated sentences |
| [Microsoft Tech Community launch blog][msft-decision1-blog] | Author (Saumil-Shrivastava), "public preview" status wording, pricing table, Xbox Research case study (GPT-5 comparator, 80–100x); fetched via polyfetch 2026-10-10 |
| [Microsoft Foundry model catalog — Microsoft-Decision-1][msft-decision1-catalog] | "Lifecycle Generally available (GA)" (rendered + embedded JSON), base model, `licenseDescription`, capabilities/use-case bullets, 32,768-token context, `trainingDataDate`; fetched via polyfetch 2026-10-10 |
| [Microsoft Command Line blog — Decision-1 launch][msft-decision1-cmdline] | Base model, pricing, benchmark prose + embedded chart data (accuracy/latency/calibration over 36 benchmarks, decoded from base64 iframe payloads), appendix model list, editor's note, Xbox Research case study (GPT-6 Sol comparator, 14–18x/212–223x per-game breakdown), safety/robustness testing; fetched via polyfetch 2026-10-10 |
| [Microsoft Learn how-to — Microsoft-Decision-1][msft-decision1-learn] | Wire shape (`POST …/providers/microsoft/v1/systemone`), question-type table (`noul`/`choice`/`score`), deployment types, use cases, limitations; fetched via WebFetch 2026-10-10 |
| [Cloudflare changelog — Clef launch (10-01)][clef-changelog-1001] | Model sizes, System One API, licence, HF repos, latency/benchmark tables, RL fine-tuning service; fetched 2026-10-11 |
| [Cloudflare changelog — Clef-omni (10-09)][clef-changelog-1009] | clef-omni launch (audio/video), Clef-flash price cut and hosted context-window change, Clef SGLang speedup; fetched 2026-10-11 |
| [Cloudflare blog — Clef launch][clef-blog] | Full launch narrative: base models, context-window comparison to Jev, latency/benchmark/workflow-eval tables, RL design-partner service; fetched 2026-10-11 |
| [Workers AI model page — Clef][clef-model-page] | Hosted context window (65,536 tokens), API call shape (binding + REST), body keys, pricing; fetched 2026-10-11 |
| [Workers AI model page — Clef-flash][clef-flash-model-page] | Hosted context window (24,576 tokens), pricing, API parameters; fetched 2026-10-11 |
| [Workers AI pricing page][workers-ai-pricing] | Current per-model input-token prices for clef/clef-flash/clef-omni, page marked "Last updated Oct 9, 2026"; fetched 2026-10-11 |
| [Hugging Face model card — Cloudflare/clef][clef-hf] | License, base model (`Qwen/Qwen3.8-27B`), architecture, Decision Index comparison table including general-reasoning rows; fetched 2026-10-11 |
| [Hugging Face model card — Cloudflare/clef-flash][clef-flash-hf] | License, base model (`Qwen/Qwen3.5-9B`), architecture, Decision Index comparison table; fetched 2026-10-11 |
| Hugging Face API, `models/Cloudflare/clef-omni` | Confirms clef-omni is public (`license: apache-2.0`), lists weight files; checked 2026-10-11 |
| Hugging Face Space data, `multimodalart/jev-decision-index/data/index.json` | Partial (~40%) search for a `clef` entry — none found, consistent with the HF cards' own "internal run" label; checked 2026-10-11 |
| `sgl-project/sglang` PR #42721 | Confirms Cloudflare's SGLang-support PR is real and merged, and its own title names the `/v1/systemone` path; checked via `gh api`, 2026-10-11 |
| [Unsloth decision-model example notebook][unsloth-decision-notebook] | `FastDecisionModel`/`DecisionTrainer` usage, 4-bit+LoRA setup, `calibrate()`/`predict()` shapes, reported accuracy/ECE numbers, LGPL-3.0 notebook license, dead guide link; fetched 2026-10-11 |
| [Unsloth guide — train your own decision model][unsloth-decision-guide] | "Same design as Cloudflare's Clef" framing, supported base models, 3,000-row accuracy table, training hardware/time, `UNSLOTH_SYSTEMONE_MODEL` serving; fetched 2026-10-11 |
| [Unsloth docs — Laya/Jev-API local serving][unsloth-decision-laya-serving] | `/v1/systemone` local endpoint, model-name aliases, `typesafe-sdk` config via `TYPESAFE_BASE_URL`; fetched 2026-10-11 |
| [Unsloth release v0.1.904-beta][unsloth-release-0.1.904] | "Train your own Decision model" release notes, QLoRA wording, `FastDecisionModel` PR title; published 2026-10-07, fetched 2026-10-11 |
| [LocalLLaMA/typed-decisions dataset][typed-decisions-dataset] | License (Apache-2.0), row counts (1.6k total), `Synthetic` tag; fetched 2026-10-11 |
| Hugging Face Datasets Server API, `typed-decisions` `/info` | Per-config train/test row counts for all 5 configs (300/100 each workflow config); checked 2026-10-11 |
| `unslothai/unsloth` repo `LICENSE` and `studio/LICENSE.AGPL-3.0` | Confirmed Apache-2.0 (root) and AGPL-3.0 (`studio/`, where the Decision API server lives) via `gh api` content fetch, 2026-10-11 |
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
| [AnyJev][anyjev] | README, LICENSE (fetched via GitHub contents API, 2026-10-11); `gh api` repo metadata (stars/forks/dates); Hugging Face API check on `morriszjm/Tacit-9B` (public, ungated, Apache-2.0), 2026-10-11 |
| [AnyJev Technical Report (arXiv:2610.00831)][anyjev-paper] | Abstract page: title, authors, submission date (30 Sep 2026, v1) verified; abstract text not reproducible verbatim from this fetch, so not quoted or cited for figures; fetched 2026-10-11 |
| [JEV-as-a-Judge (arXiv:2609.26550)][jaaj] | Abstract page (verbatim, fetched 2026-09-30) |
| [JevSpawn (arXiv:2610.00437)][jevspawn-paper] | Abstract (arXiv Atom API, verbatim) and HTML full text (jev-1.13.0/Qwen3.8-27B setup, Table 1/2 figures, code-availability sentence); fetched 2026-10-10 |
| [JevSpawn (GitHub)][jevspawn-repo] | README (same Table 1/2, "TypeSafe Jev — API-based finite scoring" wording, entry point `src/jev_spawn/api.py`), root contents (no `LICENSE`); fetched via `gh api`, 2026-10-10 |
| GitHub code search, `q=JevSpawn` | Absence-of-collision check: 2 results, both Hoyant-Su's own repos; checked 2026-10-10 |
| [agent-frameworks-infrastructure-landscape.md §8][frameworks-8] | Existing classifier/output-validation coverage, cross-referenced not repeated |
| [Plan 0009][plan] | Lead list (J3 / issue #517) and rubric scope for this batch |
| [Issue #517][issue-517] | Batch scope, proposed placements, owner corrections |
| [GLiNER2.5-Decide announcement][gliner-blog] | Use-case bullets ("Model routing," "Tool calling," "Browser and computer use," "Guardrails," "LLM-as-a-judge") re-fetched verbatim, 2026-10-09 |
| [docs.typesafe.ai][typesafe] (home, `/api`, `/models`) | Re-checked 2026-10-09 for a model-selection routing claim; none found |
| [docs.typesafe.ai/confidence][typesafe-confidence] | Re-fetched verbatim 2026-10-09: the "Three paths for using confidence in your code" act/confirm/escalate pattern |
| [Secure Agentics Adrian README][adrian-gh] | Tool-call classification and block/hold-for-approval behavior, re-fetched verbatim via `gh api`, 2026-10-09 |
| [agentic-ai-vulnerability-landscape.md § Secure Agentics Adrian][adrian-home] | Existing corpus analysis of Adrian's act/confirm/escalate intervention modes, cross-referenced not repeated |
| [typesafe-computer-use][tcu-home] | README, LICENSE (fetched via GitHub contents API, 2026-10-11); `gh api` repo metadata (stars/forks/dates); architecture description and cost/latency table |
| [agent-evaluation-metrics-landscape.md § LLM-as-a-Judge Quality Assessment][judge-metrics] | Free-text judge metrics, cross-referenced not repeated |
| [agent-frameworks-infrastructure-landscape.md § Guardrails / policy][guardrails-policy] | Safety-classifier/guardrail tools, cross-referenced not repeated |
| [agent-frameworks-infrastructure-landscape.md § Rerankers][rerankers] | Dedicated cross-encoder rerankers, cross-referenced not repeated |
| [llm-routers-gateways-landscape.md][llm-routers-open] | RouteLLM / Not Diamond classifier-trained routers, cross-referenced not repeated |
| [Fastino launch blog — GLiDE][fastino-glide-blog] | What GLiDE is, API shape, context window, license/HF-link absence, community Decision Index 0.2.1 comparison to Jev (overall, per-area, 31-of-38 tally), exact publish-date `<time>` tag vs. unrelated Framer build timestamp; fetched via WebFetch + polyfetch 2026-10-15 |
| [Fastino blog — "Decision Models Explained"][fastino-decision-models-explained] | "Top decision models in 2026" comparison table listing GLiNER2.5-Decide and GLiDE as separate rows with no stated lineage; fetched via polyfetch 2026-10-15 (WebFetch returned no body text for this page) |
| Hugging Face, `fastino` org model listing | Confirms GLiDE has no public weights (16 listed models, none named GLiDE); checked 2026-10-15 |
| [Celeris-1 Decision launch post][celeris-decision-blog] | What it is, diffusion architecture, explanation feature, jev-bench/typed-decisions accuracy+Brier table vs. Perplexity/Mercury Decide/Jev/gpt-6-luna, latency table; fetched via WebFetch 2026-10-15 |
| [Celeris API docs — Decisions][celeris-decisions-docs] | API shape (`/v1/systemone` + `/v1/decisions`), `x_celeris` explain/image extensions, no license/context-window/self-hosting stated; fetched via WebFetch 2026-10-15 |
| [Celeris pricing page][celeris-pricing] | $0.04/1M input tokens, free output; fetched via WebFetch 2026-10-15 |
| [Liquid AI blog — d1 hosted API][liquid-d1-blog] | Hosted `d1` launch: question types, API shape, pricing, "first model to rival Jev" sentence; fetched via WebFetch 2026-10-15 |
| [Liquid AI blog — open d1][liquid-d1-open-blog] | d1-3b/d1-omni-600M release: modalities, "without restrictions" wording, per-device latency table; fetched via WebFetch 2026-10-15 |
| [Hugging Face model card — LiquidAI/d1-3b][liquid-d1-hf] | License tag (`lfm1.0`, HF-API `other`), parameters, architecture, Decision Index 0.2.1 sub-scores; fetched via WebFetch 2026-10-15 |
| [Inception Labs docs — Decisions (Mercury Decide)][inception-decide-docs] | API shape (`/v1/decisions`, `noul`/`choice`/`score`), homepage card description, no streaming/tool-calling; fetched via WebFetch 2026-10-15 |
| [Inception Labs docs — Models & Pricing][inception-pricing] | $0.02/1M input (50% off $0.04), free output, no context-window figure; fetched via WebFetch 2026-10-15 |
| Inception Labs blog index + homepage | Confirms no dedicated Mercury Decide blog post; the only homepage link is an OpenRouter banner; checked 2026-10-15 |
| [Artificial Analysis — Decision Index launch article][aa-decision-index-article] | Launch date, composition (four 25%-weighted evals), call-format quote, launch-time scores, per-eval leaders, cost/speed ranges, calibration summary, model/baseline counts; fetched via WebFetch 2026-10-15 |
| [Artificial Analysis — Decision Index methodology][aa-decision-index-methodology] | Eval weights and dataset filtering detail, non-hallucination-rate formula, versioning ("Version 1.0... October 2026 to current"); fetched via WebFetch 2026-10-15 |
| [Artificial Analysis — Decision Index live leaderboard][aa-decision-index-leaderboard] | Full per-model scores (11 decision models + 15 LLM configurations), cost-per-task, latency, calibration-chart legend, extracted from the page's own embedded JSON data; fetched via polyfetch 2026-10-15 |

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
[tcu-home]: https://github.com/awlevin/typesafe-computer-use
[probably]: https://github.com/southpolesteve/probably
[pg-jev]: https://github.com/realZachi/pg-jev
[osi-pgl]: https://opensource.org/license/postgresql
[jevk5]: https://github.com/allebee/jevk5
[jevbench]: https://github.com/fstandhartinger/jevbench
[semif]: https://github.com/TheoLeeCJ/SemIf-OpenJev
[anyjev]: https://github.com/nokia-applied-research/AnyJev
[anyjev-paper]: https://arxiv.org/abs/2610.00831
[jaaj]: https://arxiv.org/abs/2609.26550
[jevspawn-paper]: https://arxiv.org/abs/2610.00437
[jevspawn-repo]: https://github.com/Hoyant-Su/JevSpawn
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
[typesafe-models]: https://docs.typesafe.ai/models
[pplx-pricing]: https://docs.perplexity.ai/docs/getting-started/pricing
[pplx-changelog]: https://docs.perplexity.ai/docs/resources/changelog
[decision-index-methodology]: https://huggingface.co/spaces/multimodalart/jev-decision-index/resolve/f4ecd9f76093e73560d25fc5a9bd316f17326790/data/methodology-v0.2.1.json
[decision-index-v021]: https://huggingface.co/spaces/multimodalart/jev-decision-index/resolve/f4ecd9f76093e73560d25fc5a9bd316f17326790/data/index-v0.2.1.json
[decision-index-current]: https://huggingface.co/spaces/multimodalart/jev-decision-index/resolve/f4ecd9f76093e73560d25fc5a9bd316f17326790/data/index.json
[decision-index-space]: https://huggingface.co/spaces/multimodalart/jev-decision-index
[pplx-ticket-triage]: https://docs.perplexity.ai/docs/cookbook/examples/decisions-api-ticket-triage/README
[pplx-action-gate]: https://docs.perplexity.ai/docs/cookbook/examples/decisions-api-action-gate/README
[pplx-browser-agent]: https://docs.perplexity.ai/docs/cookbook/examples/decisions-api-browser-agent/README
[pplx-answer-gate]: https://docs.perplexity.ai/docs/cookbook/examples/decisions-api-answer-gate/README
[adrian-gh]: https://github.com/secureagentics/Adrian
[msft-decision1-blog]: https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/introducing-microsoft-decision-1-in-microsoft-foundry-for-decision-and-classific/4562742
[msft-decision1-catalog]: https://ai.azure.com/catalog/models/Microsoft-Decision-1
[msft-decision1-cmdline]: https://commandline.microsoft.com/microsoft-decision-1-model-foundry/
[msft-decision1-learn]: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision
[clef-changelog-1001]: https://developers.cloudflare.com/changelog/post/2026-10-01-clef-workers-ai/
[clef-changelog-1009]: https://developers.cloudflare.com/changelog/post/2026-10-09-clef-omni-workers-ai/
[clef-blog]: https://blog.cloudflare.com/clef-decision-models/
[clef-model-page]: https://developers.cloudflare.com/workers-ai/models/clef/
[clef-flash-model-page]: https://developers.cloudflare.com/workers-ai/models/clef-flash/
[workers-ai-pricing]: https://developers.cloudflare.com/workers-ai/platform/pricing/
[clef-hf]: https://huggingface.co/Cloudflare/clef
[clef-flash-hf]: https://huggingface.co/Cloudflare/clef-flash
[unsloth-decision-notebook]: https://github.com/unslothai/notebooks/blob/main/nb/Qwen3_5_(4B)-Decision.ipynb
[unsloth-decision-guide]: https://unsloth.ai/docs/basics/train-your-own-decision-model-with-unsloth
[unsloth-decision-laya-serving]: https://unsloth.ai/docs/models/decision-laya.md
[unsloth-release-0.1.904]: https://github.com/unslothai/unsloth/releases/tag/v0.1.904-beta
[typed-decisions-dataset]: https://huggingface.co/datasets/LocalLLaMA/typed-decisions
[fastino-glide-blog]: https://fastino.ai/blog/introducing-glide-the-first-thinking-decision-model
[fastino-decision-models-explained]: https://fastino.ai/blog/decision-models-explained
[celeris-decision-blog]: https://celeris.ai/celeris-1-decision
[celeris-decisions-docs]: https://docs.celeris.ai/decisions
[celeris-pricing]: https://docs.celeris.ai/pricing
[liquid-d1-blog]: https://www.liquid.ai/blog/d1-decision-model
[liquid-d1-open-blog]: https://www.liquid.ai/blog/d1-open
[liquid-d1-hf]: https://huggingface.co/LiquidAI/d1-3B
[inception-decide-docs]: https://docs.inceptionlabs.ai/capabilities/decisions
[inception-pricing]: https://docs.inceptionlabs.ai/get-started/models
[aa-decision-index-article]: https://artificialanalysis.ai/articles/artificial-analysis-decision-index
[aa-decision-index-methodology]: https://artificialanalysis.ai/methodology/decision-index
[aa-decision-index-leaderboard]: https://artificialanalysis.ai/evaluations/artificial-analysis-decision-index
