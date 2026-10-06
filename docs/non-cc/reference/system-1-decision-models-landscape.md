---
title: System-1 Decision Models Landscape
purpose: Survey open-weight, research, and independent alternatives to TypeSafe's Jev — fast, typed-output classifiers (choice/score/noul answers, calibrated probabilities, one forward pass, no free text) used for agent routing, guardrails, and verification — scored against the agent substrate rubric.
created: 2026-09-30
updated: 2026-10-06
validated_links: 2026-10-06
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
