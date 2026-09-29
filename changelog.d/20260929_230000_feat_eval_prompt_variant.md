### Added

- `.github/scripts/lib/relevance_eval.py`, `eval-relevance-models.py`, `.github/workflows/llm-model-eval.yaml`: `prompt_variant` choice input (`default` | `no-borderline-yes`). The new variant drops only the production prompt's "When borderline, prefer YES" sentence, to test whether it drives false accepts (#527). The summary records the variant.
