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

### bwrap bind-mount blocks `git unlink` on project-root config files

- **Context**: Claude Code with bubblewrap sandbox on Linux/WSL2/Codespaces, running `git switch` / `git restore` / `gh pr merge`.
- **Problem**: Git operations fail with `error: unable to unlink old '<file>': Device or resource busy` on project-root config files (varies by project: `CHANGELOG.md`, `README.md`, `pyproject.toml`, `Makefile`, `.claude/settings.json`). Server-side merges succeed but local FF fails; working tree desyncs from HEAD.
- **Solution**: `git update-ref` + `git reset HEAD` to move branch pointer without checkout; `git restore` for unlocked files; Claude Code Edit/Write tool for busy ones (overwrites via `O_TRUNC`, bypasses `unlink(2)`).
- **References**: [docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md](docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md) (canonical, Friction 3), [anthropics/claude-code#17727](https://github.com/anthropics/claude-code/issues/17727).

### Subagent reference sweeps can return false negatives — verify before deleting

- **Context**: Before deleting or moving docs, dispatching a subagent (Explore / general-purpose) to grep the repo for inbound references.
- **Problem**: A subagent sweep confidently reported "no live-doc references" to files queued for deletion. In fact ~28 inbound links existed (a metrics doc deferred to the archive landscapes at ~22 lines; the observability doc linked one too). Acting on the sweep alone would have shipped broken links — and because `lychee.toml` excludes `docs/archive/`, links *into* the archive were never CI-checked, so the breakage would have surfaced only after deletion made them dangle elsewhere.
- **Solution**: Treat subagent ref-sweeps as advisory, not authoritative. Cross-check the result against references you have already read directly; calibrate the sweep by naming known hits and confirming it finds them. Repoint inbound refs to their new homes, then run `make check_links` (lychee) — it is the backstop that catches anything the sweep missed before the change merges.
- **References**: [lychee.toml](lychee.toml) (excludes `docs/archive/` — repoint archive-bound links to live homes before deleting), [PR #237](https://github.com/qte77/ai-agents-research/pull/237).
- **Promoted (2026-06-21)**: recurred 3×+ — including false-negative "create-new" calls on docs that already existed (`databricks-genie-analysis.md`, `opennote-analysis.md`) and a missed whole section (the Agent-HUD block in `ag-ui-protocol-landscape.md`). Constraint added to [.claude/rules/read-discipline.md](.claude/rules/read-discipline.md) ("Verify subagent findings before acting").
