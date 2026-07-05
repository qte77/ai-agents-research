### Added

- `docs/plans/2026-07-05-status-frontmatter-migration.md` + `docs/handoffs/2026-07-05-status-frontmatter-migration.md`: durable plan + onboarding handoff for #348 (migrate doc `status` into YAML frontmatter, drop the body badge), with a complete source map (grep commands, counts, file:line lists, vocabulary, transform rule) so a future session executes without re-mapping. Migration itself is deferred (YAGNI — nothing reads `status:` yet). Introduces `docs/handoffs/` for cross-session handoff notes.

### Fixed

- `docs/cc-community/CC-vlm-screen-sharing-landscape.md`: resolved a frontmatter↔badge contradiction (`status: research` but badge `Assess`) — aligned the badge to `Research (informational)`, matching the frontmatter and sibling landscape docs.
