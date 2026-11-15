### Fixed

- `CC-extended-context-analysis.md`: drop the long-context premium above 200K tokens, which no longer exists — current models bill the full 1M window at standard per-token rates (Haiku 5.5 has its own over-100K tier). Adds which models default to 1M, plan gating per the model-config docs (Opus 4.6 at 1M included on Max/Ultra/Team/Enterprise; Sonnet 4.6 at 1M needs usage credits), and removes the dead long-context rate-limit link (plan 0014 K1).
