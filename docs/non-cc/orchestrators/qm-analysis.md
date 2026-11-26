---
title: QM — Y Combinator's Multiplayer Agent Harness
source: https://github.com/yc-software/qm
purpose: Evaluate QM's multi-scope (personal + shared) agent harness for team/startup use, and its multi-provider core with Pi as the agent loop (other harness drivers unverified)
created: 2026-09-24
updated: 2026-11-26
validated_links_on: 2026-09-24
status: assess
---

## What It Is

[QM][qm-gh] is "a multiplayer agent harness for work. In Slack and on the web," published under
the GitHub organization `yc-software` — whose org profile name is literally **"Y Combinator"**
(confirmed via `gh api orgs/yc-software`, accessed 2026-09-24), so the YC affiliation is
first-party, not inferred from the repo name alone.

Where most agent harnesses model a single personal assistant, QM is architected for a whole
company: each person and each shared "room" (channel/project) gets its own scoped memory, files,
keychain view, permissions, crons, web apps, and durable sandbox (per the [README][qm-gh],
accessed 2026-09-24). The README says QM runs models from many providers, so a deployment isn't tied to any single vendor, and names Pi as the agent loop inside core; that Pi, OpenCode, Codex and Claude Code all drive the same core is unverified (the README only says QM's security approach follows local coding agents like OpenCode, Codex and Claude Code) — see
[`pi-analysis.md`](../coding-agents/pi-analysis.md), [`opencode-analysis.md`](../coding-agents/opencode-analysis.md),
[`codex-cli-analysis.md`](../coding-agents/codex-cli-analysis.md) for those individually.

**Repository facts** (`gh api repos/yc-software/qm`, checked 2026-11-26): 15,794 stars, 1,960
forks, **MIT** license, created 2026-07-29, latest tagged release `v0.1.18` (published
2026-11-11) — about four months old with unusually fast star growth for its age, consistent with a
high-visibility YC-backed launch.

## How It Works

**Personal and shared scopes.** People customize the agent as their own, while still
collaborating with it in Slack channels and projects; the same identity and configuration carries
between Slack and the web app.

**Admin governance.** Org-level configuration controls security/sharing posture and which
harnesses and models are available org-wide.

**Web apps and shared skills.** Users can "spin up custom internal apps and publish them to the
right people"; skills are scope-owned and shareable by grant, with admin-gated promotion to the
whole org and skill packs importable from git repositories.

**Background work.** Crons, watches, and inbound webhooks run automation while nobody is actively
in a session.

**Architecture** (per the README's own diagram, accessed 2026-09-24): a headless TypeScript/Node
core (Fastify HTTP) holds the API, identity/policy layer, scheduler, and the agent loop itself;
PostgreSQL is the persistence layer for sessions, memory, and the work queue; each scope (person or
room) gets its own isolated, durable sandbox for `execute` and other tool calls; the web/admin UI
and Slack integration are separate services/plugins that talk to the core over its HTTP API. For
durability across restarts, `DATABASE_URL` must be set (the README says core requires Postgres); that `SESSION_STORE=postgres` is also needed, and that sessions otherwise live only in process memory, is unverified.

**Deployment.** QM is self-hosted, not via the source repo but via `qm init`, which materializes a
deployment directory from the published `@yc-software/qm` npm package into an empty
organization-owned repo. Per the repo's [`docs/getting-started.md`][qm-deploy-docs] (accessed
2026-09-24): the operator chooses **AWS, Render or Fly.io** at init time (`--target aws|render|fly`; Render also needs `--repo` and `--branch`; the page says the installed package carries Fly and AWS templates) (provider choice is fixed
thereafter — switching providers means a fresh init), and `qm init` also generates a
`deployment.md` and a `.codex/skills/deploy-qm/` skill meant to be handed to an agent, which
confirms the billing account before mutating anything, wires email-gated onboarding, and returns
the live operational URLs. The README links Agent 37 as a fully hosted option (`www.agent37.com/qm`); who operates it is unverified.

## Adoption Decision

**Assess.** QM's per-scope isolation model (personal workspace + shared room, each with its own
sandbox/permissions/memory) is a genuinely different shape than the single-user assistants and
single-team-channel bots more commonly covered in this corpus, and its multi-provider core (the claim that the same
runtime drives Pi, OpenCode, Codex, or Claude Code is unverified) is a concrete multi-harness design worth
comparing against [`agent-frameworks-infrastructure-landscape.md`](../frameworks/agent-frameworks-infrastructure-landscape.md).
Star growth is exceptional for a repo about four months old, though that on its own is not evidence of
production maturity — no independent case studies were found as of 2026-09-24, and the project is
self-hosted with no first-party managed-hosting offering (the README links Agent 37 as a hosted option; its operator is unverified).

## Action Items

- Verify whether QM's Claude Code driver mode has any first-party documentation of its own (the README sentence that all four harnesses drive the same core is unverified) before treating it as equivalent in depth to a native
  CC integration.
- Track `v0.1.x` → `v1.0` for API stability signals.
- Do not present the Agent 37 hosted offering as QM-operated without independently
  verifying who runs it.

## Sources

| Source | Content |
|---|---|
| [yc-software/qm README][qm-gh] | Product description, scopes/features, architecture diagram |
| [`docs/getting-started.md`][qm-deploy-docs] | `qm init` deployment mechanics, AWS/Render/Fly.io provider choice, accessed 2026-09-24 |
| `gh api orgs/yc-software` | Org display name "Y Combinator" — confirms first-party YC affiliation, accessed 2026-09-24 |
| `gh api repos/yc-software/qm` | Stars (15,794), forks (1,960), license (MIT), created (2026-07-29), checked 2026-11-26 |
| `gh api repos/yc-software/qm/releases/latest` | Latest tag `v0.1.18`, published 2026-11-11, checked 2026-11-26 |

[qm-gh]: https://github.com/yc-software/qm
[qm-deploy-docs]: https://github.com/yc-software/qm/blob/main/docs/getting-started.md
