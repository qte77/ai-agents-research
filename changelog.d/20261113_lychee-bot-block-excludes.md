### Changed

- `lychee.toml`: exclude `developer.salesforce.com` and `architect.salesforce.com` (host-level, replacing the single developer.salesforce.com blog URL) and the one path `arena.ai/leaderboard/webdev`. Every URL on them returns 403 to lychee both locally and in CI (a persistent bot-block, unlike runner-IP 403s that pass on a local recheck); one page per host was checked live on 2026-11-13. The Salesforce and harness-comparison docs added on 2026-11-12 had turned the link check red on every run, including `main`.
