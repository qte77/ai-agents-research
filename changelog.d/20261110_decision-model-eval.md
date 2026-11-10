### Added

- `.github/workflows/decision-model-eval.yaml` + `.github/scripts/eval-decision-models.py` (manual):
  runs decision models (default Cloudflare `clef-flash` and `clef`, through `decide()` from
  qte77/.github pinned to 43ad121) over the G1 gold sets and writes `records.jsonl` + `summary.md`:
  ROC-AUC with a seeded bootstrap interval (papers only), Brier, accuracy, and a `hi` sweep with a
  rule fixed before the run (smallest `hi` whose acted decisions are wrong at most 5% of the time).
  Transient errors are retried; escalated items are counted and left out. Fails when a model answers
  nothing. Scoring in `lib/decision_eval.py`, 17 tests. Plan 0012 row H1.
