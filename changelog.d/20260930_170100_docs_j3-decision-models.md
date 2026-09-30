<!--
A new scriv changelog fragment.

Uncomment the section that is right (remove the leading dashes) and
describe your change in one or more bullet points, in past tense, like
the entries in CHANGELOG.md. Don't add your own headers, and don't
include an "Unreleased" header — that is added automatically.

Only uncomment categories that actually apply.
-->

### Added

- `docs/non-cc/reference/system-1-decision-models-landscape.md`: new landscape page surveying open-weight and research alternatives to TypeSafe's Jev — Laya, kev, CLM/CLM-8B, GLiNER2.5-Decide, RuVector, the JEV-as-a-Judge paper (CMU, arXiv:2609.26550), plus lighter mentions of probably, JevK5, and SemIf — all rubric-scored against the agent substrate rubric. Indexed in `docs/non-cc/README.md` and `docs/_topics/harness.md` (plan 0009 row J3, #517).
- `docs/cc-community/CC-community-tooling-landscape.md`: `abide` (coldteadotai) — AGENTS.md rule enforcement via a per-edit/turn Jev decision-model question, across Claude Code, Codex, and OpenCode.
- `docs/cc-community/CC-code-tooling-landscape.md`: `jevgrep` (dzhng) — a question-driven code-search CLI that uses Jev to judge file/declaration relevance for a coding agent.

### Changed

- `docs/cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md`: added `jev-ultrafast` (browser-use) to the Alternative MCP Options table — a decision-model-driven browser agent, distinct from browser-use itself.
- `docs/non-cc/protocols/agents-md-cookbook-analysis.md`: cross-linked `abide` from the Coldtea field-study section (same maker).
- `docs/cc-community/CC-codex-plugin-cc-analysis.md`: cross-linked `abide` as the same one-agent-gates-another Stop-hook pattern applied to rule enforcement rather than code review.
- `docs/_topics/plugins.md`, `docs/_topics/code-tooling.md`: extended existing hub rows to name `jev-ultrafast` and `jevgrep`.
