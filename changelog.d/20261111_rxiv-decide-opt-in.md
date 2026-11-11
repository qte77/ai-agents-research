### Changed

- `.github/workflows/rxiv-paper-eval.yaml`: pinned gha-rxiv-paper-eval v0.6.0 and turned on its
  decision-model path. Relevance asks Clef 27B first, with `hi` 0.75 from the H1 gold-set run.
  Uncertain papers and escalations fall back to the agent-strict chat call. The decision path
  gets the same agent-strict criterion, minus the chat reply-format sentence; a unit test keeps
  the two in sync. The base URL is now passed as the `LLM_BASE_URL` secret, so the
  `LLM_BASE_URL` repo variable is no longer read. A feed week with 0 rows now fails the eval.
