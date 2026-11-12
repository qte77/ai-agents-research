### Added

- `.github/workflows/decision-model-eval.yaml`, `.github/scripts/eval-decision-models.py`, `.github/scripts/lib/decision_eval.py`: monthly drift check for the decision models. The gold-set eval runs on the 1st of each month with Clef, Clef-flash and Jev 1.13.0, writes `metrics.json`, compares with the committed `.github/scripts/data/gold/baseline.json` (ROC-AUC drop above 0.03, recommended `hi` moving by 0.05 or more) and opens, updates or closes one `decision-drift` issue (plan 0013 row A7, part 1).
