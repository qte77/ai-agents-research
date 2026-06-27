### Added

- `docs/cc-native/agents-skills/CC-output-verification-analysis.md`: a first-party guide to verifying Claude Code's own agentic outputs — per-mechanism matrix (workflow / team / subagent / plan / memory), hooks as the deterministic backbone (with the non-uniform `exit 2` semantics), `--json-schema` structured-output validation + the `error_max_structured_output_retries` fail signal, the CLAUDE.md-as-user-message memory gotcha, and the DIY (no first-party eval runner) pattern. Closes #320.
