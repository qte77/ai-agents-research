---
title: Learnings Hub
description: Cross-repo pattern aggregation and per-repo knowledge distillations from live development across the qte77 ecosystem.
created: 2026-03-27
updated: 2026-03-27
---

# Learnings Hub

Distilled operational learnings from active development across the qte77 ecosystem. This folder is the write-back target for Ralph's Cross-Repo Compound Learning Aggregator (CRLA).

## Documents

| Document | Content |
|----------|---------|
| [cross-repo-digest.md](cross-repo-digest.md) | ~15 patterns that recur across multiple repos — GitHub API, CC sandbox, CI, release tooling |
| [per-repo/agents-eval.md](per-repo/agents-eval.md) | Agents-eval specific patterns: PydanticAI, Streamlit, BERTScore, evaluation pipeline |
| [per-repo/ralph-template.md](per-repo/ralph-template.md) | Ralph-specific patterns: shell scripting, prd.json, self-evolving loop |
| [per-repo/so101-biolab.md](per-repo/so101-biolab.md) | so101-biolab-automation patterns (placeholder) |
| [per-repo/deepvariant.md](per-repo/deepvariant.md) | DeepVariant ARM64/ML patterns (placeholder) |
| [contribution-sprint/style-cheatsheets.md](contribution-sprint/style-cheatsheets.md) | Per-repo coding style, commit format, PR process for compass-mcp, SimpleAgents, opencode |
| [contribution-sprint/plugin-safety-matrix.md](contribution-sprint/plugin-safety-matrix.md) | Safe plugins per repo + pre-PR .claude/ leakage checklist |

## How This Folder Is Maintained

- **Manually seeded**: `cross-repo-digest.md` — patterns identified during cross-repo exploration
- **Ralph write-back**: `per-repo/*.md` — appended by `compound_writeback()` in `lib/compound.sh` when `COMPOUND_WRITEBACK_ENABLED=true`
- **Read-only inputs**: MEMORY.md, plan files — never written by Ralph

## Consumer

Ralph reads `docs/learnings/` via `COMPOUND_LEARNINGS_PATH` to inject story-relevant context at execution time. See [CRLA plan](../../.claude/plans/ralph-cross-repo-compound-learning-aggregator.md) for architecture details (if available locally).
