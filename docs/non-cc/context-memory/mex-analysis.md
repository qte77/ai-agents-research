---
title: mex Analysis
source: https://github.com/mex-memory/mex
purpose: Analysis of mex, a Git-shared, human-approval-gated project memory and drift-detection CLI for coding agents.
platform_scope: [claude-code, codex, cursor, windsurf, github-copilot, opencode]
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

[mex][repo] (npm package `mex-agent`) is a CLI plus local "Hub" that keeps a team's project memory — architecture, decisions, requirements, handoffs — as canonical Markdown files under `.mex/` in the repository, shared through ordinary Git commits. There is no hosted service or central server: Git is the only sharing layer, and each engineer or agent rebuilds their own local, non-shared SQLite indexes (a Tree-sitter-based Code Graph and a full-text Wiki search index) from that canonical Markdown.

Stars: 1,705 · License: MIT · Language: TypeScript · Latest release: **v0.8.2** (2026-09-13) · 22 contributors · homepage [mexmemory.com][site] (all accessed 2026-09-24). Requires Node.js ≥22.5 with SQLite FTS5 support and a Git repository.

## Key Differentiator: Human Approval Boundary

Per the README's own "Human approval boundaries" table: an agent can search/retrieve Wiki or Code Graph evidence, create a checkout-local Inbox draft (a proposed knowledge addition/correction) or Relay draft (a handoff), and preview a bounded change — but publishing an Inbox proposal, approving/rejecting it, and publishing/closing a Relay all require an explicit human action, bound by signed previews that detect stale or altered plans. This gate is procedural, not a technical lock-out: the README also documents that "ordinary GROW upkeep can still update project knowledge directly" outside the Inbox path, that `mex wiki apply` writes only with an explicit `--apply` flag, and that an "exceptional self-approval flow" exists for a single author. The design is reviewed-by-default, not agent-write-proof.

## Drift Detection

A Wiki claim can be "grounded" to a specific Code Graph node (stored as a node ID plus an identity fingerprint, with newer groundings also carrying a body hash). When the underlying code symbol changes, moves, or disappears, mex flags that grounding for review. The README is explicit that drift is a review signal, not proof the prose is wrong or that a model reasoned correctly from retrieved context — it surfaces a discrepancy for a human to check, rather than auto-correcting or auto-trusting either side.

## Agent Integration

| Integration | Setup behavior | Explicit commands |
|---|---|---|
| Claude Code | Installs/updates project anchor + skills under `.claude/skills/` | `/mex-inbox`, `/mex-relay` |
| Codex | Installs/updates project anchor + skills under `.agents/skills/` | `$mex-inbox`, `$mex-relay` |
| Cursor, Windsurf, GitHub Copilot, OpenCode | Instruction-anchor/template only | No official skill commands in 0.8 |

## What It Explicitly Is Not

Per the README's own "What MEX is not" section: no cloud-hosted Hub or sync, no live notifications/presence/chat, no Git staging or pushes/pulls without explicit review, no authentication/RBAC, no Jira-style task management, no semantic/vector search (Wiki search is full-text; Graph retrieval is lexical/structural), and no published MCP server in the 0.8 line (an MCP workspace exists in-repo but is source-only).

## Privacy

mex does not upload canonical records, the Graph, the Wiki index, drafts, or Hub sessions to any mex-operated service. It ships pseudonymous, opt-out CLI/Hub telemetry (`MEX_TELEMETRY=0` or `DO_NOT_TRACK=1` to disable) built from one random installation UUID; names, repository remotes, argument values, paths, and content are explicitly excluded.

## Adoption Decision

**Assess.** MIT-licensed, actively maintained (22 contributors, a release as recent as 2026-09-13), and its Inbox/Relay review workflow addresses a real risk class — an agent silently "correcting" shared project knowledge — without requiring a hosted service, though the gate is procedural (plan/`--apply`, a self-approval path exists for solo use) rather than an enforced technical restriction. Requires Node ≥22.5 with SQLite FTS5 support; verify that constraint against your CI/dev images before piloting, and note the Code Graph currently covers only TypeScript/TSX, JavaScript/JSX, Python, and Rust.

## Sources

| Source | Content |
|---|---|
| [mex GitHub repo][repo] (README) | Architecture, human-approval model, drift detection, agent integrations, telemetry (accessed 2026-09-24) |
| [mex-memory/mex][repo] (repo metadata + releases) | Stars, license, language, created/pushed dates, v0.8.2 release date (accessed 2026-09-24 via GitHub API) |

[repo]: https://github.com/mex-memory/mex
[site]: https://mexmemory.com
