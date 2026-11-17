### Fixed

- rxiv paper eval: pass the agent-strict prompt as `relevance_prompt_template`, the input gha-rxiv-paper-eval v0.6.1 reads, instead of the deprecated `relevance_prompt` alias that logged a warning on every run (seen on the 2026-11-17 scheduled run).
