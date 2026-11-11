### Added

- `docs/non-cc/reference/system-1-decision-models-landscape.md` § Cloudflare Clef: results of the
  first decision-model run on this repo's gold sets (2026-11-10). Clef reached ROC-AUC 0.970 on
  the 100 papers, with a recommended `hi` of 0.75 at 90% coverage; Clef-flash reached 0.958.
  The section notes the limits: in-sample threshold, agent labels, and an issue set whose 3
  negatives are planted fixtures.

### Changed

- Plan 0012: H1's Clef part is shipped (Jev waits on K0). C1 is shipped: live triage checks
  passed in five consumer repos. P1 is shadow-only first, and P2's done-when compares against the
  Llama-70B baseline on the gold set.
- `.github/scripts/eval-decision-models.py`: the summary prints the real negative count, not a
  hardcoded 3.
