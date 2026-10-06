### Fixed

- `.github/workflows/rxiv-paper-eval.yaml`: the weekly arXiv eval uses an agent-strict relevance prompt (#594). On weeks 22–30 with Llama 3.3 70B, agreement with the earlier labels rose from 46.0% to 83.6% and false accepts fell from 135 to 16; most remaining disagreements were non-agent papers the old labels had accepted.

### Added

- `.github/scripts/lib/relevance_eval.py`: `agent-strict` prompt variant for `llm-model-eval.yaml`, with a unit test that keeps the production workflow's prompt identical to it.
