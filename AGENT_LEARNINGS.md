---
title: Agent Learning Documentation
description: Non-obvious patterns that prevent repeated mistakes across sprints
---

## Template

- **Context**: When/where this applies
- **Problem**: What issue this solves
- **Solution**: Implementation approach
- **Example**: Working code
- **References**: Related files

## Learned Patterns

### Phantom files in repo root from bwrap sandbox

- **Context**: Linux/WSL2/Codespace with Claude Code's bubblewrap sandbox enabled (default). Reproduces on Fedora 43, Arch, Ubuntu 24.04, WSL2.
- **Problem**: Project root accumulates 0-byte char-special files (`.bashrc`, `.gitconfig`, `.gitmodules`, `.mcp.json`, `HEAD`, `config`, etc.) that poison `git status`, break `git log HEAD`, block `EnterWorktree`, and surface as `Permission denied` warnings during `git fetch`.
- **Solution**: Recognize the symptom early via the file morphology table in the friction doc. Apply the rooted-pattern `.gitignore` block (already in this repo). Do NOT try to fix via `permissions.deny` (the deny list is hardcoded in runtime function `Rx4`, not user-configurable). Do NOT pre-create the file with `touch` (bwrap mounts `/dev/null` over real content; cleanup is best-effort and skipped when concurrent sandboxes are active).
- **References**: [docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md](docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md) — canonical analysis with full issue map, version timeline, and dead-end mitigations. Upstream: [anthropics/claude-code#17727](https://github.com/anthropics/claude-code/issues/17727), [sandbox-runtime#139](https://github.com/anthropic-experimental/sandbox-runtime/issues/139).
