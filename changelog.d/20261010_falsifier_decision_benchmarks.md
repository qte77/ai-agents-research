### Fixed

- `docs/non-cc/infrastructure/jev-analysis.md` (and the two docs that repeat it): the qte77/feelings pre-CI gate numbers now come from the post-P5 run (feelings#45): 76% caught, 2 of 59 clean flagged (3.4%), 23% held-out false flags, about 67x faster and 51x cheaper than Claude; the earlier figures predated the removal of a new-file cue.
- `docs/non-cc/reference/system-1-decision-models-landscape.md`: pplx-decider's "61.56 vs 57.9" is reconciled — it is Decision Index edition 0.2.1, reproduced from the published area weights; edition 0.3's `balanced_skill` blends in private tests and is not comparable. The Panahi leaderboard note now flags the unexplained "tied at #1" and the "42% less" claim (52% at published prices).
