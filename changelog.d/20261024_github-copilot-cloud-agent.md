### Added

- `docs/non-cc/agents/github-copilot-cloud-agent-analysis.md`: Copilot on github.com — cloud agent,
  automations (launched 2026-06-02; schedule/issue/PR triggers; not in public repos), MCP config
  (GitHub + Playwright MCP on by default, `COPILOT_MCP_` secrets, no OAuth remotes, tools only),
  repository instructions incl. `AGENTS.md`/`CLAUDE.md`/`GEMINI.md`, automatic code review (ruleset
  rule, AI credits + Actions minutes, external-licence setting) and responsible-use mitigations;
  github/github-mcp-server (MIT, v2.0.3). 19/19 claims confirmed by an independent falsifier.

### Changed

- `docs/non-cc/agents/github-copilot-cli-analysis.md`: the CLI now reads `AGENTS.md`/`CLAUDE.md`/
  `GEMINI.md` (the "not AGENTS.md" gap is closed) and is billed in GitHub AI Credits, not premium requests.
- `docs/sdlc-lcm/multi-agent-onboarding-outlook.md`: Copilot row notes AGENTS.md/CLAUDE.md/GEMINI.md.
- `docs/cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md`: Playwright MCP licence/release,
  on by default in Copilot cloud agent, README security and CLI+skills notes.
- `docs/non-cc/README.md`: index row for the new doc.
