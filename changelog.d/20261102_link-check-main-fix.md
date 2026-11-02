### Fixed

- `docs/cc-community/CC-community-plugins-landscape.md`: unlinked `bacharyehya/talk-to-claude`, whose repo
  now returns 404, so the repo-wide link check passes again.
- `docs/non-cc/context-memory/mitosis-cortex-analysis.md`: `verginglabs.com` now returns 404; the Verging
  Labs citation points to its 2026-10-12 Wayback snapshot instead.
- `lychee.toml`: excluded the one Constellation Research article cited in `kiro-analysis.md`; it returns
  403 to CI runners but loads normally elsewhere.
