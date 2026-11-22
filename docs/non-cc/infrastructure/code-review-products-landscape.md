---
title: AI PR-Review Products — Tool Landscape
purpose: Catalog of standalone SaaS PR-review products (multi-platform GitHub/GitLab review bots), distinct from Claude Code-integrated review tooling.
created: 2026-06-27
updated: 2026-11-22
validated_links: 2026-10-24
status: research
---

## What It Is

Standalone **SaaS PR-review products**: hosted bots that review pull requests with
whole-codebase context. They install as GitHub/GitLab/Bitbucket/Azure apps and
comment on PRs directly; most also expose IDE or agent hooks. They are
multi-platform, **not** Claude Code-specific — any CC integration is incidental,
which is why they live here rather than in the cc-community tooling docs.

For related code-review tooling — Qodo's cross-repo review, and the Code-Review-Graph AST/blast-radius Model Context Protocol (MCP) tool — see
[CC-code-tooling-landscape.md](../../cc-community/CC-code-tooling-landscape.md).

## Products

- [CodeRabbit](https://www.coderabbit.ai/) — GitHub/GitLab/Azure/Bitbucket app + IDE (VS Code/Cursor/Windsurf) + CLI; bills itself "the most installed AI app on GitHub" (SaaS).
- [Greptile](https://www.greptile.com/) — a swarm of agents builds a codebase graph index, then reviews PRs in parallel; GitHub/GitLab, API, **MCP**, and a Claude Code plugin; SaaS or self-hosted in AWS.
- [Sourcery](https://sourcery.ai/) — review focused on security and AI-generated-code defects; GitHub/GitLab, VS Code/JetBrains, fixes via coding agents (SaaS).
- [Qodo Merge / PR-Agent](https://github.com/The-PR-Agent/pr-agent) — the original open-source PR reviewer (MIT); the repo now lives in the separate `The-PR-Agent` GitHub org and its description says it is not the Qodo free tier (`gh api` 2026-11-22); `/review` `/improve` `/describe` `/ask` via CLI, GitHub Action, Docker, or webhooks; GitHub/GitLab/Bitbucket/Azure/Gitea. Qodo's platform adds **Auto Approval Workflows** (Beta) and **Agent Session Review** (Research Preview), announced 2026-11-18 ([blog][qodo-auto-approval], vendor announcement, not tested here): after a review finishes, a workflow can approve the PR as `qodo-bot` or add a "Qodo approved" label based on criteria such as a severity threshold, blast radius and team rules (the blog lists these as available criteria, not all required); "guards" (repos, paths such as `auth/**`, authors incl. coding-agent logins) are never auto-approved, and approval is re-checked and withdrawn on each new commit. The bot approval counts as one approval, with required reviewers and code owners still applying. Agent Session Review is a `/qodo-agent-session-review` skill in Qodo's Agentic Toolbox that bundles every PR an agent opened in a session, with plan deviations and a reading plan, into one work package. Qodo's CC-integrated pieces: [CC-code-tooling-landscape.md § Qodo](../../cc-community/CC-code-tooling-landscape.md#qodo-qodo-ai).
- [Graphite](https://graphite.com/) — AI reviewer bundled with Graphite's PR-stacking workflow, launched as Diamond ([Series B and Diamond launch post](https://graphite.com/blog/series-b-diamond-launch), 2025-03-17), now unified with Graphite Chat as "Graphite Agent" ([AI reviews docs](https://graphite.com/docs/ai-reviews), read 2026-11-22); GitHub app (SaaS).
- [Cursor Bugbot](https://cursor.com/bugbot) — Cursor's PR-review agent; comments on GitHub PRs and pushes fixes into the Cursor editor or a Background Agent; usage-based billing (SaaS).
- [Cubic](https://www.cubic.dev/) — YC-backed AI review plus whole-codebase bug scanning; GitHub app + IDE, one-click fixes, custom rules (SaaS).
- [Bito](https://bito.ai/) — codebase-aware AI Code Review Agent for GitHub/GitLab/Bitbucket (SaaS).
- [Korbit](https://www.korbit.ai/) — AI review across GitHub/GitLab/Bitbucket with bug explanations and auto-generated PR descriptions (SaaS).
- [GitHub Copilot code review](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/code-review) — built into GitHub, generally available; requested by hand or automatically via a branch-ruleset rule, billed in AI credits plus GitHub Actions minutes, and shares the repository's MCP config with the Copilot cloud agent (read-only tools only). Details: [github-copilot-cloud-agent-analysis.md § Automatic code review](../agents/github-copilot-cloud-agent-analysis.md#automatic-code-review).

These overlap heavily; the differentiators are codebase-context depth (Greptile's graph
index), OSS vs SaaS (open-code-review, below, is Apache-2.0; PR-Agent is MIT-licensed —
both are open-source options), and agent/MCP reach (Greptile, CodeRabbit, Sourcery). The
structural/AST counterpart (Code-Review-Graph) and cross-repo review (Qodo) are
covered in the Claude Code tooling docs — see Cross-References.

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

- [CC-code-tooling-landscape.md](../../cc-community/CC-code-tooling-landscape.md) — code-review tooling in the Claude Code docs: Qodo (cross-repo review) and Code-Review-Graph (AST blast-radius MCP)
- [CC-official-plugins-landscape.md](../../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) — the first-party `/code-review` plugin
- [software-factory-landscape.md § Economics, failure and verification evidence](../../sdlc-lcm/software-factory-landscape.md#economics-failure-and-verification-evidence) — Uber's uReview (vendor claim) and the empirical review-agent merge-rate study (arXiv 2604.03196)
- [jev-analysis.md](jev-analysis.md) — a cheap classifier-model gate rather than an LLM-review bot; comparable in that both are automatable pre-merge checks, but Jev answers narrow typed questions instead of writing review comments

## Not included

Entries removed under the [pruning rule](../../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (alive, adopted or proven; checked 2026-11-22).

| Name | Reason | Date | Link |
|---|---|---|---|
| Ellipsis | Criterion 3: its site names no customers and gives no measured result for review, and its home page now leads with hosted coding agents (read 2026-11-22); no first-party page found for the "free for public repos" claim | 2026-11-22 | <https://www.ellipsis.dev/> |

## Sources

Each product links to its first-party page inline in the list above. Moved here from
[CC-code-tooling-landscape.md](../../cc-community/CC-code-tooling-landscape.md) on
2026-06-27 (tracked in [#326](https://github.com/qte77/ai-agents-research/issues/326)),
where the roundup was flagged as out-of-scope for a `cc-community` doc.

| Source | Content |
|---|---|
| [open-code-review README][open-code-review] | Hybrid deterministic + LLM-agent architecture, deployment modes, license and star count verified 2026-09-30 |
| [Qodo: Auto Approval Workflows and Agent Session Review][qodo-auto-approval] | Vendor announcement, 2026-11-18, read 2026-11-20 (Beta/Research Preview status, guards, approval semantics) |
| [Agent substrate rubric][rubric] | Six-property scoring rubric applied above |

[open-code-review]: https://github.com/alibaba/open-code-review
[rubric]: ../../sdlc-lcm/agent-substrate-rubric.md
[qodo-auto-approval]: https://www.qodo.ai/blog/introducing-auto-approval-workflows-and-agent-session-review
