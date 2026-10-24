### Changed

- `docs/cc-native/agents-skills/CC-skills-adoption-analysis.md`: re-confirmed against the live Agent
  Skills specification that `allowed-tools` is the only tool-related field (Experimental) and that
  the optional package directories are `scripts/`, `references/` and `assets/` — no `evals/`; the
  skill-creator plugin's `evals/evals.json` is a plugin convention. Adds a Claude Code ↔ OpenAI Codex
  CLI SKILL.md / MCP / AGENTS.md parity table. Split out of #704.
