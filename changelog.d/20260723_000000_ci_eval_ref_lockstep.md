### Fixed

- `.github/workflows/rxiv-paper-eval.yaml`: bump `eval_ref` v0.2.2 → v0.4.0, in lockstep with the reusable-workflow pin — the v0.4.0 workflow unconditionally passes `--max-llm-calls`, which the v0.2.2 script rejects (exit 2), leaving the PR-path eval permanently red (bit #390). Upstream skew-guard tracked in qte77/gha-rxiv-paper-eval#80; GitHub Models retirement (2026-07-30) migration tracked in qte77/gha-rxiv-paper-eval#81.
