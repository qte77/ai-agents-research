### Changed

- `.github/workflows/issue-triage.yaml`: pinned gha-issue-triage v0.6.0 and turned on
  `decide-shadow`. Triage comments here now carry a fixed-format decision-model section
  (value, probability and band from Clef). Labels still come only from the existing triage.
- Plan 0012: P1 struck (v0.6.0 released, six consumer repos bumped); labels from the decision
  model are deferred until the shadow mode has data from real issues.
