### Fixed

- `.github/workflows/rxiv-paper-eval.yaml`: the weekly arXiv eval runs again. GitHub Models was retired on 2026-07-30, so the eval now calls Cloudflare Workers AI (`@cf/meta/llama-3.3-70b-instruct-fp8-fast`) through `qte77/gha-rxiv-paper-eval` v0.5.0 (`api_base` + `llm-api-key`). Dependabot PRs skip the eval, since they get no repo secrets (#527).
