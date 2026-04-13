---
title: Plugin Safety Matrix and Pre-PR Checklist
purpose: Which cc-plugins-utils plugins are safe per upstream repo, and universal checks to avoid .claude/ leakage
created: 2026-03-30
updated: 2026-03-30
---

# Plugin Safety Matrix and Pre-PR Checklist

## Plugin Safety Matrix

Source: [cc-plugins-utils][plugins] inventory across all branches (main + feat/go-dev + feat/rust-dev).

| Plugin | compass-mcp | SimpleAgents | opencode | Leakage Risk | Notes |
|---|:---:|:---:|:---:|---|---|
| commit-helper | Y | Y | Y | None | Conventional commits + PR generation |
| codebase-tools | Y | Y | Y | None | Pre-implementation research |
| backend-design | Y | Y | Y | None | Architectural decisions |
| cc-meta | Y | Y | Y | None | Context compaction + multi-phase planning |
| docs-generator | Y | Y | Y | Low | RFC/design docs; has SessionStart hook |
| docs-governance | — | Y | — | None | AGENTS.md / CONTRIBUTING.md sync |
| rust-dev (feat) | — | Y | — | None | Rust TDD + clippy + fmt |
| mas-design | — | Y | — | None | Multi-agent patterns |
| python-dev | — | Y | — | **Med** | Deploys `settings.local.json` — strip before PR |
| gha-dev | — | Y | — | **Low** | Deploys `settings.local.json` — strip before PR |
| go-dev (feat) | — | Y | — | Low | Go bindings TDD |
| workspace-setup | **X** | **X** | **X** | **CRITICAL** | Deploys `.claude/` infrastructure — NEVER upstream |
| workspace-sandbox | **X** | **X** | **X** | **CRITICAL** | Deploys `.claude/` sandbox config — NEVER upstream |
| embedded-dev | — | — | — | Med | Not relevant to sprint |
| market-research | — | — | — | Low | GTM focused, not relevant |
| website-audit | — | — | — | None | Not relevant |
| ralph | — | — | — | None | Product planning, not relevant |

**Legend**: Y = use, — = not relevant, **X** = never commit upstream

## Pre-PR Checklist (Universal)

Run before every `git push` to an upstream fork:

```bash
# 1. No .claude/ or .opencode/ paths in staged changes
git diff --cached --name-only | grep -E '\.claude/|\.opencode/' && echo "FAIL: AI config staged" || echo "OK"

# 2. No untracked AI dirs about to be added
git ls-files --others --exclude-standard | grep -E '\.claude|\.opencode' && echo "FAIL: untracked AI files" || echo "OK"

# 3. No settings.local.json staged (from python-dev, gha-dev, etc.)
git diff --cached --name-only | grep 'settings.local.json' && echo "FAIL: local settings staged" || echo "OK"

# 4. Verify diff stat — eyeball for unexpected files
git diff --cached --stat
```

Final check: review the PR diff in GitHub UI before requesting review.

## Per-Repo .gitignore Status

| Repo | `.claude/` excluded | `.opencode/` excluded | Action |
|---|---|---|---|
| compass-mcp | **No** | N/A | Consider hygiene PR to add `.claude/` to .gitignore |
| SimpleAgents | **No** | N/A | Consider hygiene PR to add `.claude/` to .gitignore |
| opencode | Unknown | **No** | Verify before first PR |

These repos do NOT exclude Claude Code config directories from version control. Extra vigilance required.

## Sources

| Source | Content |
|---|---|
| [cc-plugins-utils][plugins] | Plugin inventory, all branches, 2026-03-30 |
| [style-cheatsheets.md](style-cheatsheets.md) | Per-repo .gitignore observations |

[plugins]: https://github.com/qte77/claude-code-plugins
