### Changed

- `.claude/settings.json`: allow more read-only calls seen often in recent sessions: `~/.local/bin/lychee *` (the user-local install path, which `lychee *` doesn't match), `gh run watch *`, `gh secret list *` (names only, never values), `gh search prs *`, `gh label list *`, and the Cloudflare docs search MCP tool.
