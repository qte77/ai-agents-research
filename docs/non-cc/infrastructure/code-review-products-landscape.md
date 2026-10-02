---
title: AI PR-Review Products — Tool Landscape
purpose: Catalog of standalone SaaS PR-review products (multi-platform GitHub/GitLab review bots), distinct from Claude Code-integrated review tooling.
category: landscape
created: 2026-06-27
updated: 2026-10-02
validated_links: 2026-09-30
status: research
---

## What It Is

Standalone **SaaS PR-review products**: hosted bots that review pull requests with
whole-codebase context. They install as GitHub/GitLab/Bitbucket/Azure apps and
comment on PRs directly; most also expose IDE or agent hooks. They are
multi-platform, **not** Claude Code-specific — any CC integration is incidental,
which is why they live here rather than in the cc-community tooling docs.

For CC-*integrated* code-review tooling — Qodo's `open-aware` MCP server +
cross-repo review, and the Code-Review-Graph AST/blast-radius MCP tool — see
[CC-code-tooling-landscape.md](../../cc-community/CC-code-tooling-landscape.md).

## Products

- [CodeRabbit](https://www.coderabbit.ai/) — GitHub/GitLab/Azure/Bitbucket app + IDE (VS Code/Cursor/Windsurf) + CLI; bills itself "the most installed AI app on GitHub" (SaaS).
- [Greptile](https://www.greptile.com/) — a swarm of agents builds a codebase graph index, then reviews PRs in parallel; GitHub/GitLab, API, **MCP**, and a Claude Code plugin; SaaS or self-hosted in AWS.
- [Ellipsis](https://www.ellipsis.dev/) — GitHub-app code review plus automated bug fixes, Q&A, and changelogs (SaaS; free for public repos).
- [Sourcery](https://sourcery.ai/) — review focused on security and AI-generated-code defects; GitHub/GitLab, VS Code/JetBrains, fixes via coding agents (SaaS).
- [Qodo Merge / PR-Agent](https://github.com/qodo-ai/pr-agent) — the original open-source PR reviewer (MIT) behind Qodo; `/review` `/improve` `/describe` `/ask` via CLI, GitHub Action, Docker, or webhooks; GitHub/GitLab/Bitbucket/Azure/Gitea.
- [Graphite Diamond](https://graphite.com/) — AI reviewer bundled with Graphite's PR-stacking workflow; GitHub app, tuned for low false positives (SaaS).
- [Cursor Bugbot](https://cursor.com/bugbot) — Cursor's PR-review agent; comments on GitHub PRs and pushes fixes into the Cursor editor or a Background Agent; usage-based billing (SaaS).
- [Cubic](https://www.cubic.dev/) — YC-backed AI review plus whole-codebase bug scanning; GitHub app + IDE, one-click fixes, custom rules (SaaS).
- [Bito](https://bito.ai/) — codebase-aware AI Code Review Agent for GitHub/GitLab/Bitbucket (SaaS).
- [Korbit](https://www.korbit.ai/) — AI review across GitHub/GitLab/Bitbucket with bug explanations and auto-generated PR descriptions (SaaS).

These overlap heavily; the differentiators are codebase-context depth (Greptile's graph
index), OSS vs SaaS (open-code-review, below, is Apache-2.0; PR-Agent is MIT-licensed —
both are open-source options), and agent/MCP reach (Greptile, CodeRabbit, Sourcery). The
structural/AST counterpart (Code-Review-Graph) and cross-repo review (Qodo) are
CC-integrated tooling — see Cross-References.

### Hybrid deterministic + LLM review

Unlike the pure-LLM products above, [open-code-review][open-code-review] (Alibaba;
Apache-2.0, 42,772★, `gh api` 2026-09-30) reads Git diffs and combines a **deterministic
pipeline** — file selection, "smart file bundling" that fans large changesets out to
isolated sub-agents, and fine-grained rule matching by file type — with an **LLM agent**
for the judgment calls, via any OpenAI- or Anthropic-compatible model. It runs as a
self-hosted CLI, Docker image, or GitHub Action, or in a delegation mode where an existing
coding agent (Claude Code, Codex, Cursor, Kimi Code, OpenCode, QCA Forward) performs the
review; a session viewer records and replays past runs. Scored 2026-09-30 against the
[agent substrate rubric][rubric]:

`subject: harness`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no data ([README][open-code-review] — one CLI/Action invocation per review; no documented multi-user concurrent-write model) | partial ([README][open-code-review] — sub-agents run concurrently per bundle within one review, and it deploys as a GitHub Action, but no multi-node cluster is documented) | partial ([README][open-code-review] — file selection and rule matching are deterministic, but the LLM-agent review pass uses a configurable, unpinned OpenAI/Anthropic-compatible backend) | yes ([README][open-code-review] — pluggable LLM providers, GitHub/GitLab/GitFlic CI/Gerrit integrations, and six coding-agent delegation modes) | no data ([README][open-code-review] — rule configs are file-based, but no git-versioned snapshot/diff/rollback workflow is documented) | partial ([README][open-code-review] — a session viewer records and replays reviews with comment marking/filtering, but comments don't cite sources beyond the diff itself) |

`scored 2026-09-30`

## Cross-References

- [CC-code-tooling-landscape.md](../../cc-community/CC-code-tooling-landscape.md) — CC-integrated code-review tooling: Qodo (`open-aware` MCP + cross-repo review) and Code-Review-Graph (AST blast-radius MCP)
- [CC-official-plugins-landscape.md](../../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) — the first-party `/code-review` plugin
- [jev-analysis.md](jev-analysis.md) — a cheap classifier-model gate rather than an LLM-review bot; comparable in that both are automatable pre-merge checks, but Jev answers narrow typed questions instead of writing review comments

## Sources

Each product links to its first-party page inline in the list above. Moved here from
[CC-code-tooling-landscape.md](../../cc-community/CC-code-tooling-landscape.md) on
2026-06-27 (tracked in [#326](https://github.com/qte77/ai-agents-research/issues/326)),
where the roundup was flagged as out-of-scope for a `cc-community` doc.

| Source | Content |
|---|---|
| [open-code-review README][open-code-review] | Hybrid deterministic + LLM-agent architecture, deployment modes, license and star count verified 2026-09-30 |
| [Agent substrate rubric][rubric] | Six-property scoring rubric applied above |

[open-code-review]: https://github.com/alibaba/open-code-review
[rubric]: ../../sdlc-lcm/agent-substrate-rubric.md
