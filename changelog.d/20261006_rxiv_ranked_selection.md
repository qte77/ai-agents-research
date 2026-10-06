### Changed

- `.github/workflows/rxiv-paper-eval.yaml`: each week's papers are ranked by topic-keyword overlap and the top 100 go to the LLM (`max_llm_calls`), instead of the first 50 rows in feed order (`max_papers`). The dispatch input is now `max_llm_calls` (default 100).
