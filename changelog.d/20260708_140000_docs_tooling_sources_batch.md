### Added

- `docs/cc-community/CC-codex-plugin-cc-analysis.md`: analysis of OpenAI's official Codex→CC plugin (Apache-2.0) — slash commands, `codex-rescue` subagent, `Stop`-hook review gate, background delegation, session transfer; a rival lab building on CC's own extension surface.
- `docs/plans/2026-07-08-new-sources-batch.md`: durable plan record for the new-sources batch (tracker #374).

### Changed

- `docs/non-cc/repo-to-docs-tools-landscape.md`: added OpenWiki (LangChain, MIT) — an agent-oriented repo→docs generator that appends pointers into `AGENTS.md`/`CLAUDE.md`, distinct from human-facing DeepWiki-style tools.
- `docs/non-cc/agentic-enterprise-os-landscape.md`: added a "company brain" subsection (a synthesis label over agent-memory + KG/ontology + permissioning + write-back; cross-linked to the memory/semantic-layer docs, not a standalone doc).
- `CONTRIBUTING.md`: Research Workflow now points to `polyfetch-scrape` (fetch dynamic/blocked pages) and `doc-pipeline-engine` (process PDF/Office → text) via `uv run --directory`, alongside the existing `rtk` pointer.
