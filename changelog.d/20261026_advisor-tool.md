### Added

- `docs/cc-native/configuration/CC-advisor-tool-analysis.md`: first-party coverage of Anthropic's
  advisor tool — the `advisor_20260301` API beta (`advisor-tool-2026-03-01` header) that lets an
  executor model consult a stronger advisor mid-request — covering tool parameters, model
  pairing, billing/usage accounting, the Claude Code `/advisor` surface, and an unresolved
  platform-availability conflict between the API and Claude Code docs on Claude Platform on AWS.
- `docs/cc-native/configuration/CC-env-vars-reference.md`: `CLAUDE_CODE_DISABLE_ADVISOR_TOOL` is
  now documented (was binary string-extraction only).
- `docs/cc-native/configuration/CC-tools-inventory.md`: `/advisor` slash command and
  `advisorModel` settings.json key.
- `docs/cc-native/configuration/CC-cli-reference.md`: `--advisor` hidden CLI flag.
- `docs/cc-community/CC-community-reimplementations-landscape.md`: note that the leaked
  `advisor-tool` beta header shipped as `advisor-tool-2026-03-01`.
