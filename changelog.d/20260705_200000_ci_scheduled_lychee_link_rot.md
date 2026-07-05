### Added

- `.github/workflows/link-rot-monitor.yaml` + a `make check_links_report` target: a weekly scheduled lychee link-check that opens/updates a single `link-rot` tracking issue on broken links and auto-closes it when links are healthy again — catches external link rot proactively (between docs PRs) instead of ambushing the next one. Keeps the custom `lint.yaml` PR gate (per the #141 decision) and reuses the same `lychee.toml`, so excludes/accepts stay single-sourced. Sets `GITHUB_TOKEN` on the lychee step to cut github.com rate-limit false negatives.
