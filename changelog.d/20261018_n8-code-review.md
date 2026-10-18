### Added

- `docs/cc-native/plugins-ecosystem/CC-official-plugins-landscape.md`: a new "`/code-review`
  command and ultrareview" section, next to the existing `code-review@claude-plugins-official`
  plugin entry — the bundled `/code-review` command (any plan, no install, alias `/review` since
  v2.1.223, formerly named `/simplify` before v2.1.147), `ultrareview`/`/code-review ultra`
  (research-preview cloud review: 3 free runs on Pro/Max then typically $5–$25, typically 15–25
  minutes, 500-file/8,000-line defaults, Bedrock/Agent Platform/Foundry/ZDR/HIPAA fall back to a
  local review, CMEK can't run it), and the separate managed GitHub PR "Code Review" service
  (Team/Enterprise, Quick/Standard/Deep). Corrected the plugin entry's usage line: because plugin
  commands are namespaced, the installed plugin runs as `/code-review:code-review`, not bare
  `/code-review` — confirmed via `claude plugin list` and this session's own skill list (CC
  2.1.302) alongside the plugin's README (4-agent confidence-scoring architecture, author Boris
  Cherny, v1.0.0).

### Changed

- `docs/cc-native/configuration/CC-tools-inventory.md`: replaced the stale `/ultrareview` row
  ("Unknown — enhanced review?") and a stale `/review-pr` row (which cited `cli-ref` for a command
  absent from that reference, the live `commands` page, and the full Claude Code CHANGELOG, v0.2.21
  through v2.1.302) with verified `/code-review`, `/review`, `/simplify`, and `/ultrareview` rows,
  plus a detailed subsection covering targets, effort levels, flags, alias/rename version gates,
  and ultrareview's scope, billing, limits, and platform restrictions — verified against the live
  `code-review-local`, `ultrareview`, and `commands` pages (CC 2.1.302).
