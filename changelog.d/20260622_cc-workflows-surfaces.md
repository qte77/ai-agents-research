### Added

- `docs/cc-native/agents-skills/CC-dynamic-workflows-analysis.md`: new **Across surfaces** section — dynamic workflows and their primitives across interactive / headless `claude -p` / Agent SDK, with first-party-verified headless nuances: background agents are **awaited** (10-min default cap from **v2.1.182**, `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`), `--bare` skips skills/hooks/MCP/memory (slated to become the `-p` default), and user-invoked skills/custom commands work in `-p` since **v2.1.181**. Answers "are workflows usable in the SDK / `-p` / interactive?" (yes, all three).
