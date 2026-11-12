### Added

- `docs/sdlc-lcm/ai-security-governance-analysis.md` § Defensive Tooling: Stroq (local
  tool-call-gating + secret-leak tracing for coding-agent sessions), Tracekit (tamper-evident
  signed audit log for tool calls, mapped to EU AI Act / ISO 42001 / NIST AI RMF / OWASP), and
  devvm (per-project Lima VM sandbox for coding-agent hooks and local MCP servers).
- `docs/sdlc-lcm/agent-code-analysis-landscape.md` §3: Grim Prompter (agent-driven,
  file-and-line-cited threat modeling) and OpenQodex (scanner-then-agent-review pre-push
  pipeline).
- `docs/sdlc-lcm/agent-evaluation-metrics-landscape.md` § Evaluation Platform Integration: Waza
  (Microsoft's Go CLI for authoring and grading agent-skill eval scenarios).
- `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` §1/§3: ToolCallJudge
  (Pydantic AI Harness's tool-call-approval gate), Harness² (Google Research's recursive
  harness-optimization loop) and OpenHuman (a Rust agent harness self-benchmarked against
  Hermes).
- `docs/cc-community/CC-code-tooling-landscape.md`: Floorplan, a Claude Code/Codex plugin that
  draws an interactive map of a codebase, with a Health check and a Recent-work view.
- `docs/cc-community/CC-community-plugins-landscape.md`: new Notable Plugin Profiles for
  Impeccable (cross-agent design-vocabulary/slop-detector plugin) and Elephant-Goldfish Model
  (Google's drafter/fresh-context-reviewer spec-review plugin).
- `docs/cc-community/CC-community-tooling-landscape.md`: cogit, a Claude Code plugin that
  records the intent behind agent-written code as git-linked "thought commits."
- `docs/non-cc/agents/skill-recorder-analysis.md` (new doc): Microsoft Skill Recorder, which
  turns a recorded or imported screen session into a reusable Skill or Automation via the
  GitHub Copilot CLI, for Scout/Copilot Cowork/Copilot Studio.
- `docs/_topics/harness.md` and `docs/_topics/skills.md`: hub rows for the Harness²/OpenHuman/
  ToolCallJudge and Skill-Recorder/Waza additions above.

### Changed

- `docs/cc-community/CC-community-plugins-landscape.md` § claude-seo: refreshed the stale
  2026-04-15 snapshot (23 skills/17 subagents/3 extensions, 2026-04-23 counts) to the repo's
  current README and `gh api` figures (26 skills/19 subagents/9 extensions, 28,262★).
