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

- **Context**: Claude Code with bubblewrap sandbox on Linux/WSL2/Codespaces.
- **Problem**: 0-byte char-special files leak into project root (`.bashrc`, `.mcp.json`, `HEAD`, `config`, etc.) — poison `git status`, break `git log HEAD`, block `EnterWorktree`.
- **Solution**: Use the rooted-pattern `.gitignore` block (already in repo). See friction doc for dead-ends to avoid.
- **References**: [docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md](docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md) (canonical), [anthropics/claude-code#17727](https://github.com/anthropics/claude-code/issues/17727).
