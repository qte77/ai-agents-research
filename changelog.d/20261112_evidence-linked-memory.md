### Added

- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §4: WikiTrace
  (arXiv:2611.14320, Lee/Choi/Baek/Hwang, KAIST AI · DeepAuto.ai) — an evidence-linked memory
  that links each lesson to a compilation and the raw trajectory it came from, so an agent can
  check an underspecified, conflicting, or failure-sourced lesson before acting instead of
  trusting it outright. Self-reports the best average score against four prior memory methods,
  an insights-only ablation and no memory across eight evaluation suites, cutting the regression
  rate on tasks solvable without memory
  from 6.5% to 4.5% (paper claims; methodology not independently verified). Code released
  (Apache-2.0, 10★).
- `docs/_topics/memory.md`: hub row for the WikiTrace addition.
