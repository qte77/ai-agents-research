### Added

- `docs/non-cc/infrastructure/jev-analysis.md`: Jev (TypeSafe AI) "System One" decision model — question types (`noul`/`choice`/`score`), pricing and limits, and the qte77/feelings measured pilot using it as a pre-CI code-review gate (184 labelled changes, 78% catch rate / 1.7% false-positive rate at the shipped 0.70 threshold, roughly 70x faster than the fastest and 80x cheaper than the cheapest Claude model tested, a held-out-codebase threshold-transfer failure, and the reword lesson that cut one question's false positives from 6.7% to 0%), rubric-scored against `sdlc-lcm/agent-substrate-rubric.md`.
- `docs/non-cc/infrastructure/code-review-products-landscape.md`: open-code-review (Alibaba; Apache-2.0), a hybrid deterministic-pipeline + LLM-agent PR reviewer, rubric-scored.
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` § 8: a new "Decision models (typed yes/no, choice, score)" sub-list (Jev, and Laya as the open-weight, schema-compatible alternative), and a `.feels()`/`.fill<T>()` sentence extending the BAML bullet.
- `docs/_topics/code-tooling.md`, `docs/non-cc/README.md`: pointer rows for the new Jev page and the open-code-review addition.

### Changed

- `docs/sdlc-lcm/agentic-sdlc-patterns.md`: repointed the "Gap: no review agent" row to the new Jev analysis page (still Trial, not adopted).
