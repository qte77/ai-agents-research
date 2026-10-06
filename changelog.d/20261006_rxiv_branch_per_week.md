### Fixed

- `.github/workflows/rxiv-paper-eval.yaml`: the triage branch now includes the week key (`chore/rxiv-paper-triage-<server>-<year>-W<week>-<date>`), so runs for different weeks on the same day no longer collide; `CONTRIBUTING.md` states the remaining rule (one run at a time, merge each triage PR before the next).
