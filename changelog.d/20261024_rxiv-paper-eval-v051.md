### Changed

- `.github/workflows/rxiv-paper-eval.yaml`: pinned gha-rxiv-paper-eval v0.5.1, so a weekly run whose
  every relevance call fails (as W42 did on an expired token) now fails the job instead of ending
  green with no triage PR.
