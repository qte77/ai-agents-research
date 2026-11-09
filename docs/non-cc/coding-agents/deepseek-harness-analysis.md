---
title: DeepSeek Harness — Plugin-Native Agent Harness
purpose: Assess DeepSeek AI's open-source, Cordis-based "everything-is-a-plugin" agent harness and its very early developer preview
source: https://github.com/deepseek-ai/deepseek-harness
created: 2026-09-24
updated: 2026-11-09
validated_links: 2026-11-09
status: assess
---

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

Complements [agent-plugins-standard-analysis.md](../protocols/agent-plugins-standard-analysis.md)
(this batch) and [agents-md-cookbook-analysis.md](../protocols/agents-md-cookbook-analysis.md)'s
coverage of the wider plugin/config-portability trend: DeepSeek Harness is a
single-vendor "everything-is-a-plugin" runtime (plugins extend `dsh` itself,
discoverable via the `dsh-plugin` GitHub topic), not a cross-vendor packaging
standard like Agent Plugins.

## Super-agent Prototype (dsh-superagent)

[deepseek-ai/dsh-superagent-prototype][superagent] (MIT, "Copyright (c) 2026 DeepSeek Harness Team"; one commit, 2026-10-31; `package.json` 0.1.0, private, needs `dsh` `^0.2.1-alpha.2`) is "a proactive coding agent for one GitHub repository, packaged as a bundle for DeepSeek Harness". Its README opens with a caveat: "Research prototype for reference only, not an official DeepSeek product", with "much of the engineering done by coding agents", and the code "is not identical to our internal version or the implementation described in *Exploring Super-agent Design: Towards a More Autonomous Agent System*". Some designs in that article "are not implemented" here.

- **Trigger and authorization.** It listens to GitHub and, optionally, Feishu. A request from someone allowed becomes a Ticket; the agent "acts only when asked or when a rule the team wrote allows it". The stated principle is "take as little human attention as possible, and give as much value as possible"; a web panel shows what needs a person.
- **Router and workers.** The main Session runs a `dsh-superagent-router` preset with a smaller tool set. Each Ticket gets its own Executor Session, `worker-<ticket id>`, and its own directory, typically a `git worktree` checkout.
- **Execution limits.** Foreground shell commands move to background jobs after 5 seconds; after each turn, background work has at most 30 minutes before jobs are killed and the Ticket is reported waiting.
- **No sandbox.** Executor Sessions "run commands without approval as the operator's OS user", and the command wrappers "establish defaults, not a security boundary. A worker can still execute a program by absolute path." Run it only where the operator account's access is acceptable for an unattended agent.

**Evidence level.** The repo is a runnable reference design with no benchmarks. The latency and supervision figures reported in press coverage of the article could not be traced to a first-party copy of the article and are not repeated here.

Cross-ref: a hosted issue-to-pull-request agent for comparison is in [github-copilot-cloud-agent-analysis.md](../agents/github-copilot-cloud-agent-analysis.md).

## Sources

| Source | Content |
|---|---|
| [deepseek-ai/deepseek-harness repo][repo] | README, architecture, developer-preview status, license (first-party) |
| GitHub API repo metadata, 2026-09-24 | Stars(234,648)/forks(28,223), MIT, dates, issues/PRs disabled |
| [deepseek-ai/dsh-superagent-prototype][superagent] | README, `docs/003-execution.md`, `package.json`, LICENSE, commit list; `gh api` 2026-11-09 |

[repo]: https://github.com/deepseek-ai/deepseek-harness
[cordis]: https://github.com/cordiverse/cordis
[superagent]: https://github.com/deepseek-ai/dsh-superagent-prototype
