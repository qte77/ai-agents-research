### Fixed

- `.github/workflows/lint.yaml`: the "Run lychee" step now passes `GITHUB_TOKEN: ${{ github.token }}` so
  lychee authenticates its github.com requests (`--github-token`, env `GITHUB_TOKEN`). Without it, CI link
  checks failed on rotating github.com 503s under throttling. Matches `link-rot-monitor.yaml` and the
  shared `lint-md-links.yml` (lychee-action defaults `token` to `github.token`); the custom workflow from #141 is kept.
