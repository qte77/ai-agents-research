### Fixed

- `.github/workflows/issue-triage.yaml`: issue triage runs again. GitHub Models was retired on 2026-07-30, so the action now calls Cloudflare Workers AI (`@cf/meta/llama-3.3-70b-instruct-fp8-fast`) through `qte77/gha-issue-triage` v0.4.0 (`api_base` + `llm-api-key`). `permissions: models: read` is no longer needed (#527).
