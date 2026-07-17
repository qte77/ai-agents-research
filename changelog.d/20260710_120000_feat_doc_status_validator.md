### Added

- `.github/scripts/lib/doc_status.py` + `.github/scripts/check-doc-status.py`: a stdlib doc-status validator (#348 consumer). Lenient mode (wired into `make lint` via `make check_status`, and a new `status` CI job) checks that any frontmatter `status:` token is in the controlled vocabulary; `--strict` additionally forbids residual body `**Status**:` badges (the doc-level badge in the preamble — an in-section `**Status**:` line describing an upstream project is left alone). Unit tests in `tests/test_doc_status.py`.
- `.github/workflows/lint.yaml`: added a `tests` job (`make test`) so unit tests gate PRs, and a `status` job (`make check_status`); extended the path triggers to `.github/scripts/**`, `scripts/**`, and `tests/**`.
