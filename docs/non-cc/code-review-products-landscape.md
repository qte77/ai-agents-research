---
title: AI PR-Review Products — Tool Landscape
purpose: Catalog of standalone SaaS PR-review products (multi-platform GitHub/GitLab review bots), distinct from Claude Code-integrated review tooling.
category: landscape
created: 2026-06-27
updated: 2026-06-27
validated_links: 2026-06-27
---

**Status**: Research (informational)

## What It Is

Standalone **SaaS PR-review products**: hosted bots that review pull requests with
whole-codebase context. They install as GitHub/GitLab/Bitbucket/Azure apps and
comment on PRs directly; most also expose IDE or agent hooks. They are
multi-platform, **not** Claude Code-specific — any CC integration is incidental,
which is why they live here rather than in the cc-community tooling docs.

For CC-*integrated* code-review tooling — Qodo's `open-aware` MCP server +
cross-repo review, and the Code-Review-Graph AST/blast-radius MCP tool — see
[CC-code-tooling-landscape.md](../cc-community/CC-code-tooling-landscape.md).

## Products

- [CodeRabbit](https://www.coderabbit.ai/) — GitHub/GitLab/Azure/Bitbucket app + IDE (VS Code/Cursor/Windsurf) + CLI; bills itself "the most installed AI app on GitHub" (SaaS).
- [Greptile](https://www.greptile.com/) — a swarm of agents builds a codebase graph index, then reviews PRs in parallel; GitHub/GitLab, API, **MCP**, and a Claude Code plugin; SaaS or self-hosted in AWS.
- [Ellipsis](https://www.ellipsis.dev/) — GitHub-app code review plus automated bug fixes, Q&A, and changelogs (SaaS; free for public repos).
- [Sourcery](https://sourcery.ai/) — review focused on security and AI-generated-code defects; GitHub/GitLab, VS Code/JetBrains, fixes via coding agents (SaaS).
- [Qodo Merge / PR-Agent](https://github.com/qodo-ai/pr-agent) — the original open-source PR reviewer (Apache-2.0) behind Qodo; `/review` `/improve` `/describe` `/ask` via CLI, GitHub Action, Docker, or webhooks; GitHub/GitLab/Bitbucket/Azure/Gitea.
- [Graphite Diamond](https://graphite.com/) — AI reviewer bundled with Graphite's PR-stacking workflow; GitHub app, tuned for low false positives (SaaS).
- [Cursor Bugbot](https://cursor.com/bugbot) — Cursor's PR-review agent; comments on GitHub PRs and pushes fixes into the Cursor editor or a Background Agent; usage-based billing (SaaS).
- [Cubic](https://www.cubic.dev/) — YC-backed AI review plus whole-codebase bug scanning; GitHub app + IDE, one-click fixes, custom rules (SaaS).
- [Bito](https://bito.ai/) — codebase-aware AI Code Review Agent for GitHub/GitLab/Bitbucket (SaaS).
- [Korbit](https://www.korbit.ai/) — AI review across GitHub/GitLab/Bitbucket with bug explanations and auto-generated PR descriptions (SaaS).

These overlap heavily; the differentiators are codebase-context depth (Greptile's graph index), OSS vs SaaS (PR-Agent is the lone Apache-2.0 option), and agent/MCP reach (Greptile, CodeRabbit, Sourcery). The structural/AST counterpart (Code-Review-Graph) and cross-repo review (Qodo) are CC-integrated tooling — see Cross-References.

## Cross-References

- [CC-code-tooling-landscape.md](../cc-community/CC-code-tooling-landscape.md) — CC-integrated code-review tooling: Qodo (`open-aware` MCP + cross-repo review) and Code-Review-Graph (AST blast-radius MCP)
- [CC-official-plugins-landscape.md](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) — the first-party `/code-review` plugin

## Sources

Each product links to its first-party page inline in the list above. Moved here from
[CC-code-tooling-landscape.md](../cc-community/CC-code-tooling-landscape.md) on
2026-06-27 (tracked in [#326](https://github.com/qte77/ai-agents-research/issues/326)),
where the roundup was flagged as out-of-scope for a `cc-community` doc.
