---
title: DeepSeek Harness — Plugin-Native Agent Harness
purpose: Assess DeepSeek AI's open-source, Cordis-based "everything-is-a-plugin" agent harness and its very early developer preview
source: https://github.com/deepseek-ai/deepseek-harness
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

[DeepSeek Harness][repo] (`dsh`) is DeepSeek AI's open-source agent harness,
built on an "everything-is-a-plugin" architecture and powered by
[Cordis][cordis], a separate framework the README cites as implementing "A
Programming Paradigm for Spatiotemporal Composability" (arXiv:2608.25512 —
that paper was not independently fetched for this entry; cited only as the
README's own citation). It ships a local Web UI, launched with
`npx @deepseek-ai/dsh web` and served at `http://127.0.0.1:3080`, plus a
Desktop client. The project explicitly labels itself a **developer
preview**, warning "THERE WILL BE COMPATIBILITY-BREAKING CHANGES," asks
users to review a `SAFETY.md` notice before running it, and publishes no
version number anywhere in the README — only preview status.

## Repo Stats (2026-09-24)

234,648 stars · 28,223 forks — reached in roughly **six weeks** since the
repo's creation date of 2026-08-13 — MIT license · TypeScript. Both Issues
and Pull Requests are **disabled** on the repo (`has_issues: false`,
`has_pull_requests: false`); GitHub Discussions is the only public feedback
channel, consistent with the "developer preview, iterating rapidly" framing
in the README.

## Corpus Relevance

Complements [agent-plugins-standard-analysis.md](agent-plugins-standard-analysis.md)
(this batch) and [agents-md-cookbook-analysis.md](agents-md-cookbook-analysis.md)'s
coverage of the wider plugin/config-portability trend: DeepSeek Harness is a
single-vendor "everything-is-a-plugin" runtime (plugins extend `dsh` itself,
discoverable via the `dsh-plugin` GitHub topic), not a cross-vendor packaging
standard like Agent Plugins.

## Sources

| Source | Content |
|---|---|
| [deepseek-ai/deepseek-harness repo][repo] | README, architecture, developer-preview status, license (first-party) |
| GitHub API repo metadata, 2026-09-24 | Stars(234,648)/forks(28,223), MIT, dates, issues/PRs disabled |

[repo]: https://github.com/deepseek-ai/deepseek-harness
[cordis]: https://github.com/cordiverse/cordis
