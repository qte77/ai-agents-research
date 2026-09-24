### Added

- `docs/cc-native/sessions/CC-session-cost-analysis.md`: new "Shared plan usage across Claude products" section — the one usage limit shared by claude.ai/Claude Code/Claude Desktop, the five-hour reset shown at Settings > Usage, sign-in-based metering (Enterprise seat pool vs API-key pay-per-token), the owner-observed per-product usage split undocumented in the help center, and a "Local tools vs plan usage" subsection on why `/stats` and CodeBurn's transcript-based commands undercount total plan usage (with `codeburn quota` as the live-data exception).

### Changed

- `docs/cc-community/CC-usage-tooling-landscape.md`: corrected CodeBurn's stale "Menubar v0.9.0 (2026-04-25)" / "Node.js 20+" notes to the current `v0.9.25` (2026-09-21, GitHub Releases + npm registry) and `>=22.13.0` engine requirement; added the confirmed `codeburn doctor` subcommand and `export --billing` flag; added one-line local-transcripts-only blind-spot notes to both CodeBurn and ccusage, cross-linked to the new section above.
