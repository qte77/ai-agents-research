---
title: GitHub Copilot CLI Analysis
source: https://github.com/github/copilot-cli
purpose: Analysis of GitHub Copilot CLI as a terminal coding agent sharing the agentic harness of the Copilot coding agent, distinct from its cloud surface.
platform_scope: [cli, cloud]
created: 2026-06-11
updated: 2026-06-11
validated_links: 2026-06-11
---

**Status**: Proprietary ([custom license][copilot-cli-license], no derivatives) | **GA**: 2026-02-25 | **Version**: v1.0.61 (2026-06-09) | requires active Copilot subscription

## What It Is

GitHub Copilot CLI is a **terminal-native coding agent** — "the power of GitHub
Copilot, in your terminal." Run `copilot` in a repo and it plans, edits files,
runs commands, reviews changes, and remembers across sessions. It is "powered by
the **same agentic harness** as GitHub's Copilot coding agent," so the two share
behavior but are **different surfaces**: this is the interactive local terminal
agent; the [Copilot coding agent][copilot-agent] is the autonomous cloud product
that opens PRs from assigned issues (covered separately under
[CI automation](../cc-native/ci-remote/CC-github-actions-analysis.md#issue-lifecycle-automation-landscape)).

**Key distinction vs OSS peers** (Aider, Kilo Code, OpenCode): Copilot CLI is
**proprietary** and gated on a Copilot subscription, but reuses an org's existing
GitHub identity, billing, and the GitHub MCP server out of the box — the adoption
cost is access control, not a new vendor.

## How It Works

### Agentic harness and models

Default model is **Claude Sonnet 4.5**; `/model` switches across providers
(Anthropic, OpenAI, Google) — e.g. Claude Sonnet 4, GPT-5. The harness plans,
executes multi-step workflows, and can **delegate to subagent processes**.

### Built-in agents

Six specialized agents cover distinct workflows: **Explore** (codebase analysis
without growing primary context), **Task** (run tests/builds), **General
purpose** (full toolset), **Code review** (low-false-positive change assessment),
**Research** (deep cross-source investigation), **Rubber duck** (feedback).
Select via `/agent` or `--agent=<name>`.

### Extensibility (MCP, custom agents, instructions)

| Surface | Location |
|---|---|
| MCP servers | GitHub MCP server preconfigured; add via `/mcp add` → `mcp-config.json` |
| Custom agents | Markdown profiles at `~/.copilot/agents`, `.github/agents`, `.github-private/agents` |
| Instructions | `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md` |
| Settings | `settings.json` in `~/.copilot` (override path via `COPILOT_HOME`) |
| LSP | `~/.copilot/lsp-config.json` (user) or `.github/lsp.json` (repo) |

Note the instruction file is `copilot-instructions.md`, **not `AGENTS.md`** — a
portability gap vs the AGENTS.md convergence ([CC-skills-adoption-analysis.md](../cc-native/agents-skills/CC-skills-adoption-analysis.md)).

### Permissions, sandboxing, autonomy

Default model is **preview-every-action**: approve once, approve session-wide, or
reject with alternate instructions. Escalating autonomy via plan mode and
autopilot mode (cycle with Shift+Tab), `--allow-all` / `--yolo` to bypass
prompts, and `/sandbox enable` for local or cloud sandboxing. `--cloud` delegates
the run to the cloud coding-agent backend.

### Sessions, memory, auth

`/resume` (or `--resume` / `--continue`) restores sessions with automatic context
compression and **cross-session repository memory**; `/usage`, `/context`,
`/compact` manage the window. Auth via `/login` or a fine-grained PAT with the
**Copilot Requests** permission set through `GH_TOKEN` / `GITHUB_TOKEN`. Each
prompt consumes one premium request against the monthly quota.

### Install and invoke

`curl -fsSL https://gh.io/copilot-install | bash` · `brew install copilot-cli` ·
`winget install GitHub.Copilot` · `npm install -g @github/copilot`. Then run
`copilot` (Linux/macOS/Windows).

## Adoption Decision

| Dimension | Assessment |
|---|---|
| **Use case** | Terminal coding agent; peer to Codex CLI / Gemini CLI / Claude Code |
| **Model flexibility** | Multi-provider via `/model` (default Claude Sonnet 4.5) |
| **Extensibility** | MCP (GitHub server default), custom agents, plugins, LSP |
| **Permission model** | Preview-every-action → plan/autopilot → `--yolo`; local/cloud sandbox |
| **Maturity** | GA 2026-02-25, actively released (v1.0.61) |
| **License** | **Proprietary** — no modification, no standalone redistribution |
| **Cost** | Copilot Pro / Pro+ / Business / Enterprise; 1 premium request per prompt |

**Strengths**: Same agentic harness as the Copilot coding agent — consistent
behavior across CLI and cloud. Reuses existing GitHub auth, billing, and MCP
server (lowest onboarding friction for orgs already on Copilot). Strong
permission/sandbox model. Multi-provider model choice.

**Risks**: **Proprietary license** — cannot fork, embed, or self-host (unlike
Aider/Kilo/OpenCode). Subscription + per-prompt premium-request quota.
Business/Enterprise use requires admin enablement. `copilot-instructions.md`
instead of `AGENTS.md` adds a config surface in multi-agent shops. PAT auth keys
off `GH_TOKEN`/`GITHUB_TOKEN` — watch for env-var shadowing in CI.

## Action Items

- **Evaluate** as the terminal agent for teams already holding Copilot
  Business/Enterprise — no new vendor, reuses GitHub identity and billing.
- **Disambiguate** in any agent comparison: CLI (local, interactive) vs coding
  agent (cloud, issue→PR) — same harness, different surface.
- **Factor the config gap** (`copilot-instructions.md` ≠ `AGENTS.md`) into
  multi-agent onboarding ([multi-agent-onboarding-outlook.md](../sdlc-lcm/multi-agent-onboarding-outlook.md)).
- **Flag the license** when comparing against OSS peers — adoption is reversible
  only at the subscription level, not the code level.

## Cross-References

- [CC-github-actions-analysis.md](../cc-native/ci-remote/CC-github-actions-analysis.md#issue-lifecycle-automation-landscape) — the Copilot **coding agent** (cloud) it shares a harness with
- [CC-skills-adoption-analysis.md](../cc-native/agents-skills/CC-skills-adoption-analysis.md) — AGENTS.md convergence vs `copilot-instructions.md`
- [multi-agent-onboarding-outlook.md](../sdlc-lcm/multi-agent-onboarding-outlook.md) — per-agent config-file comparison
- [CC-community-tooling-landscape.md](../cc-community/CC-community-tooling-landscape.md) — multi-agent tooling (CC Switch, CodeBurn) that targets Copilot; `~/.copilot` session data

## Sources

| Source | Content |
|---|---|
| [github/copilot-cli repo][copilot-cli-repo] | Install, models, MCP, permission model, license |
| [Copilot CLI docs][copilot-cli-docs] | Agents, slash commands, config files, sandboxing, auth |
| [Copilot CLI overview][copilot-cli-overview] | Capabilities, autopilot, LSP, quota |
| [GA changelog 2026-02-25][copilot-cli-ga] | GA date, eligible plans, headline features |

[copilot-cli-repo]: https://github.com/github/copilot-cli
[copilot-cli-license]: https://github.com/github/copilot-cli/blob/main/LICENSE.md
[copilot-cli-docs]: https://docs.github.com/en/copilot/how-tos/copilot-cli
[copilot-cli-overview]: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview
[copilot-cli-ga]: https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/
[copilot-agent]: https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent
