### Added

- `docs/non-cc/agent-frameworks-infrastructure-landscape.md` (§1): expanded the **PydanticAI** entry with its new [capabilities system](https://pydantic.dev/articles/pydantic-ai-capabilities) (Jun 2026) — composable instructions + tools + model-settings bundles with **on-demand / deferred loading** (`defer_loading=True`) for token savings, capability-scoped hooks, and the Pydantic AI Gateway + Logfire companions. First-party source.
- `docs/cc-native/agents-skills/CC-ralph-enhancement-research.md`: new **SantanderAI/ralph** entry under External Pattern Research — Banco Santander AI Lab's multi-CLI Ralph harness (Claude Code / Codex / Gemini / Devin; Apache-2.0, v0.1.0) with live `.ralph/.env` reload, token-exhaustion agent rotation, systemd RAM caps, and project-level distributed skills (`juez` / `maestro`); plus the `ralph-vault-skill` knowledge-vault companion.

### Changed

- `docs/cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md`: cite the companion code repo [VILA-Lab/Dive-into-Claude-Code](https://github.com/VILA-Lab/Dive-into-Claude-Code) for the arXiv 2604.14228 design-space analysis.
- `docs/cc-community/CC-vlm-screen-sharing-landscape.md`: refresh the **PixelRAG** entry (~3.3k★ → ~4.2k★, v0.3.0).
- `docs/cc-community/CC-research-agents-landscape.md`: turn the bare `/deep-research` mention in the local-deep-research entry into an actual cross-ref to the bundled-workflow section (reuses the existing anchor).
- `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md`: cite the Startup CTO Handbook as the traditional engineering-leadership baseline the agentic disciplines diverge from (Cross-References + Sources), linking the qte77 estate mapping note.
