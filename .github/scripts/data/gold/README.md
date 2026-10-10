# Gold sets for relevance decisions

Two small, independently-labelled gold sets for calibrating the two production relevance
filters this repo depends on: the rxiv paper-eval filter (`qte77/gha-rxiv-paper-eval`, used by
`.github/workflows/rxiv-paper-eval.yaml`) and the issue-triage relevance filter
(`qte77/gha-issue-triage`). Plan 0012 row G1
(`docs/plans/2026-10-10-0012-decision-models-estate.md`).

Each set ships two files so a second, blind labeller can work from the items alone, with no
knowledge of this pass's verdicts:

- `<set>.items.jsonl` — `{id, source, title, text, context}`, **no labels**.
- `<set>.labels.jsonl` — `{id, label: true|false, confidence: "high"|"low", rationale}`.

**Labellers:** agent pass 1 and an independent blind agent pass 2 (both 2026-10-10). Pass 2
saw only the items files and the two criterion sources; its raw verdicts are kept in
`<set>.labels.pass2.jsonl`. `<set>.labels.jsonl` holds the **reconciled** labels (see
[Second pass and reconciliation](#second-pass-and-reconciliation)).

## Set 1 — papers (`papers.items.jsonl` / `papers.labels.jsonl`)

**Question:** is the paper relevant under the **agent-strict** criterion — `AGENT_STRICT_PROMPT`
in [`.github/scripts/lib/relevance_eval.py`](../../lib/relevance_eval.py) (lines 40–50):

> Answer YES only if the paper's main contribution is about: {topic}. That means it builds,
> trains, evaluates or analyses agents or reasoning systems driven by large language models
> (tool use, function calling, multi-agent coordination, planning, agent benchmarks or agent
> safety). Answer NO for general machine-learning methods (optimizers, architectures, sampling,
> clustering, vision or speech models) without an LLM-agent focus, for robotics or control work
> without an LLM agent, and for applications of machine learning in other fields. When unsure,
> answer NO.

`{topic}` is the literal string configured in `rxiv-paper-eval.yaml`: *"LLM-based autonomous
agents, tool use and function calling, multi-agent coordination, agentic evaluation and
benchmarking, and LLM reasoning and planning"*.

**Label basis:** title + abstract only (no full text, no existing verdicts).

### Selection rule (and why it isn't a straight read of the committed data file)

`triage/rxiv/data/arxiv-2026-W40.jsonl` — the file named in the original brief — turned out to
hold **only the papers the production run already accepted** (84 of them): the `rxiv-paper-eval`
workflow persists `extracts.jsonl`, which the upstream script (`gha-rxiv-paper-eval`
`scripts/eval_papers.py`) populates only for papers that passed its own LLM relevance pass. It
carries no rank field and no rejected candidates, so sampling "the top 100" from it is not
possible and it cannot support a false-accept/false-reject calibration (no negatives survive in
it at all).

Instead, the exact top-100 candidate pool was **reconstructed exactly**, not re-ranked by a new
rule:

1. Downloaded the still-live GitHub Actions artifact `rxiv-eval-arxiv-2026-w40` from the run that
   produced this data (run `37946390205`, 2026-10-09), which includes `feed.csv` — the verbatim
   4,284-row weekly feed the production run itself fetched and ranked.
2. Fetched `scripts/eval_papers.py` from `qte77/gha-rxiv-paper-eval` at the exact commit the
   workflow pins (`6097eb9981c76014793eb7e468e1aec00f56e12f`, v0.5.0) and reproduced its
   `_prefilter` → `_keyword_prefilter` pipeline verbatim in a throwaway script (stdlib only, not
   committed): category/cap pre-filter (no-op here: `categories=""`, `max_papers=0`), then rank by
   topic-keyword overlap (`_keyword_score`: count of distinct topic-vocabulary words — stopword- and
   length->3-filtered tokens of the topic string — found in `title + category + abstract`,
   lowercased) and keep the top `max_llm_calls=100`.
3. **Self-check:** all 84 DOIs in the committed `arxiv-2026-W40.jsonl` are a subset of the
   reconstructed top-100 (0 missing) — the reconstruction is exact, not approximate, for this
   week's feed and this topic string.

`papers.items.jsonl` holds exactly those 100 papers, abstracts trimmed to ~1,600 characters,
**in arxiv-ID order** (not rank order, to avoid handing a blind second labeller a relevance cue).

### Counts and class balance

| | count |
|---|---|
| Total | 100 |
| Labelled relevant (YES) | 77 |
| Labelled irrelevant (NO) | 23 |
| High confidence | 61 |
| Low confidence (boundary judgment calls — see rationale per item) | 39 |

**Partial-exposure disclosure:** before the top-100 pool was reconstructed, 21 of its DOIs were
already seen (title + abstract, while inspecting `arxiv-2026-W40.jsonl`'s schema) with the prior
knowledge that all of them were production-accepted — that file holds only accepted papers, so
anything read from it carries that label. All 21 ended up inside the reconstructed 100 and were
then labelled individually like the other 79; one of them (`2609.40048`) was still labelled NO
despite the known prior accept, so this was not pure rubber-stamping, but it is a real,
disclosed deviation from a fully blind pass on exactly those 21 items. The other 63 accepted DOIs
and all 16 rejected ones were not identified until after every one of the 100 had been labelled.

**Observed, for context only (comparison run only after labelling completed):** this pass agrees
with the production agent-strict run (`@cf/meta/llama-3.3-70b-instruct-fp8-fast`) on 89/100 of
this exact pool. 9 disagreements are this pass rejecting a paper production accepted; 2 are the
reverse. Two of the 9 are clean false-accepts rather than boundary calls — `2609.35936`
(a wireless-communication tutorial for embodied multi-agent systems, no LLM anywhere) and
`2610.02255` (a multi-agent time-series-forecasting framework, no LLM anywhere). The remaining
seam is VLM-driven multi-agent systems applied to a vision-centric task (video, images, robot
perception) — the criterion's "driven by large language models" vs. "vision ... models" clauses
pull in opposite directions there. This is where the second pass disagreed (below).

## Set 2 — issues (`issues.items.jsonl` / `issues.labels.jsonl`)

**Question:** is the issue relevant to its repository — the inverse of `gha-issue-triage`'s
`irrelevant` predicate in `src/relevance.py` (`score_relevance`, fetched read-only from
`qte77/gha-issue-triage` at its current `main`): `irrelevant = (score <= 3)` on a 1–10 relevance
score the production LLM assigns against repo context (README.md + CLAUDE.md, first 2,000 chars
each). This pass's label is `relevant = NOT irrelevant`, i.e. "would production score this > 3",
decided from a simplified version of that same scope signal.

**Label basis:** repo description (the one-line GitHub repo description, not the fuller
README/CLAUDE.md context production uses) + issue title + issue body only. Existing triage labels,
`state`, `stateReason` and comments on these issues were never fetched (production's own output
on these exact issues would otherwise leak into the labels).

### Source repos and selection rule

Repos named in the brief that have had issue triage: `ai-agents-research`, `gha-issue-triage`,
`agentic-job-offer-to-application-kit`, `analyze-stock-kpi`, `cc-senses-plugin`,
`claude-code-plugins`, `vlm-toolkit`, `CellPlateVision-Prototype`. (`cc-voice-plugin-prototype`
is the same repo as `cc-senses-plugin` — GitHub redirects the old name — so it does not add a
ninth repo.)

For each repo: `gh issue list --state all --limit 100 --json number,title,body,url,author`
(bot-authored issues, i.e. `github-actions`/`dependabot`, excluded), then the first N by GitHub's
default most-recently-updated ordering: 10 for `ai-agents-research` and
`agentic-job-offer-to-application-kit`; 8 for `gha-issue-triage`, `analyze-stock-kpi`,
`cc-senses-plugin` and `claude-code-plugins`; 6 for `vlm-toolkit`; 1 for
`CellPlateVision-Prototype` (its only issue). That gave 59 items, **all of them relevant** — every
sampled issue was an in-scope project item (bug/feature/docs/chore) for its repo. Most are
owner-authored; a few (`gha-issue-triage#109`, and several in `agentic-job-offer-to-application-kit`
and `claude-code-plugins#199`) are from other contributors but are equally in-scope.

Because a gold set with no negatives can't measure false-accept, all 401 issue titles across the
8 repos (not just the sampled 59) were scanned for anything else irrelevant before accepting that
result. Three were found, all in `gha-issue-triage` itself: `#34` *"Build Hyperspace Drive for
Mars Mission"*, `#33` *"Go To Mars. Don't Make Mistakes."*, `#30` *"Go To Moon. Don't Make
Mistakes."* — each carries an internal `<!-- triage re-validation -->` / `<!-- triage-retry -->`
marker, i.e. they are the project's **own planted test fixtures** for its relevance scorer, not
organic issues. These 3 were added to the pool explicitly (not sampled by the recency rule), for
62 items total. No other irrelevant issue exists in any of the 401 scanned titles — real,
owner-maintained issue trackers are overwhelmingly on-topic by construction, and that skew is
itself the honest finding here.

### Counts and class balance

| | count |
|---|---|
| Total | 62 |
| Labelled relevant (YES) | 59 |
| Labelled irrelevant (NO) | 3 (all planted test fixtures in `gha-issue-triage`) |
| High confidence | 56 |
| Low confidence | 6 (all 6 `vlm-toolkit` issues — that repo has no repo description set, so the primary scope signal this pass was told to use is absent; the label itself is still inferred confidently from the issue content, which is unambiguously VLM-toolkit-internal) |

**Caveat:** with only 3 negatives, all from one repo's deliberate fixtures, this set measures
false rejects (relevant issues scored irrelevant) well but false accepts hardly at all, and any
AUC on it has a very wide interval. It is not a population-representative sample of off-topic
issues. Use the paper set for false-accept behaviour.

## Second pass and reconciliation

| Set | Agreement | Disagreements |
|---|---|---|
| Papers | 96 / 100 | `2609.38078`, `2609.40048`, `2610.02451`, `2610.03099` |
| Issues | 62 / 62 | none |

All four paper disagreements are pass 1 NO (low) vs pass 2 YES (medium), on the seam flagged
above: a VLM-driven agentic or tool-using system whose measured contribution is a vision task
(robot control, video grounding, wildfire reporting, cross-video QA). They were reconciled to
**NO** by the criterion's own tie-break, "When unsure, answer NO": a split between two labellers
is the unsure case. Each keeps `confidence: "low"` and a rationale noting the split. Final paper
counts are unchanged: 77 YES / 23 NO.
