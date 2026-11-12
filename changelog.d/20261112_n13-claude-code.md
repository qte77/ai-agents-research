### Added

- `docs/sdlc-lcm/software-factory-landscape.md` §(c): Anthropic's own 2026-10-13 engineering post on
  migrating its monorepo off git to an in-house system (Scion) as daily merges rose from ~2,500 to
  30,000+ per day — a vendor-reported internal case alongside the existing Cloudflare Astro case.
- `docs/cc-native/configuration/CC-models-reference.md`: Claude Fable 5.2 / Mythos 5.2 (CC v2.1.321+),
  pricing table rows, and the headline benchmark figures stated directly in Anthropic's 2026-11-09
  announcement.
- `docs/sdlc-lcm/evaluation-data-resources-landscape.md`: the `claude-api` skill's `build-eval` and
  `hillclimb` commands (claude.dev, Lance Martin, 2026-09-28), which operationalize the EDD loop
  already documented there, plus the self-reported 66.1%→87.9% result on Anthropic's own skill.
- `docs/cc-native/configuration/CC-tools-inventory.md`: the account-email-in-outbound-request guardrail
  (CC v2.1.317/v2.1.321 CHANGELOG entries, verbatim) alongside the still-open `claude-code#107757`
  privacy issue it is adjacent to.
- `docs/cc-native/context-memory/CC-memory-system-analysis.md`: the `v2.1.277` CHANGELOG line, quoted
  verbatim, confirming the already-documented AGENTS.md-fallback behavior and its `/config` toggle.
- `docs/cc-native/plugins-ecosystem/CC-cowork-plugins-enterprise-analysis.md`: the Claude for Financial
  Advisors Cowork plugin (2026-09-14, updated 2026-10-27) and the Claude for Nonprofits plugin
  (2026-10-26), distinct from the existing financial-services and Cowork-templates coverage.
