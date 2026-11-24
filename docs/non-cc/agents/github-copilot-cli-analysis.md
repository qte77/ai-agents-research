---
title: GitHub Copilot CLI Analysis
source: https://github.com/github/copilot-cli
purpose: Analysis of GitHub Copilot CLI as a terminal coding agent sharing the agentic harness of the Copilot coding agent, distinct from its cloud surface, plus the Copilot SDK that embeds the same engine.
platform_scope: [cli, cloud]
created: 2026-06-11
updated: 2026-11-20
validated_links_on: 2026-10-24
status: assess
---

**Details:** Proprietary ([custom license][copilot-cli-license], no derivatives) | **GA**: 2026-02-25 | **Version**: v1.0.61 (2026-06-09) | requires active Copilot subscription

## What It Is

GitHub Copilot CLI is a **terminal-native coding agent** — "the power of GitHub
Copilot, in your terminal." Run `copilot` in a repo and it plans, edits files,
runs commands, reviews changes, and remembers across sessions. It is "powered by
the **same agentic harness** as GitHub's Copilot coding agent," so the two share
behavior but are **different surfaces**: this is the interactive local terminal
agent; the [Copilot coding agent][copilot-agent] is the autonomous cloud product
that opens PRs from assigned issues (covered in
[github-copilot-cloud-agent-analysis.md](github-copilot-cloud-agent-analysis.md) and under
[CI automation](../../cc-native/ci-remote/CC-github-actions-analysis.md#issue-lifecycle-automation-landscape)).

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
| Model Context Protocol (MCP) servers | GitHub MCP server preconfigured; add via `/mcp add` → `mcp-config.json` |
| Custom agents | Markdown profiles at `~/.copilot/agents`, `.github/agents`, `.github-private/agents` |
| Instructions | `.github/copilot-instructions.md`, `.github/instructions/**/*.instructions.md`, `AGENTS.md`, `CLAUDE.md` (also `.claude/CLAUDE.md`), `GEMINI.md`, plus `$HOME/.copilot/` and `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` ([custom instructions][copilot-cli-instructions]) |
| Settings | `settings.json` in `~/.copilot` (override path via `COPILOT_HOME`) |
| LSP | `~/.copilot/lsp-config.json` (user) or `.github/lsp.json` (repo) |

**Updated 2026-10-24:** the CLI now reads `AGENTS.md`, `CLAUDE.md` and `GEMINI.md` alongside
`copilot-instructions.md` ([custom instructions][copilot-cli-instructions]), so the earlier
portability gap against the AGENTS.md convergence
([multi-agent-onboarding-outlook.md](../../sdlc-lcm/multi-agent-onboarding-outlook.md)) is closed.

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
**Copilot Requests** permission set through `GH_TOKEN` / `GITHUB_TOKEN`. Usage is
billed in GitHub AI Credits — `/usage` shows "The amount of GitHub AI Credits used in the current
session" ([using the CLI][copilot-cli-use]); "premium requests" no longer appear on the CLI or
billing pages checked 2026-10-24; a [legacy request-based billing page][copilot-legacy-requests] still lists one premium request per CLI prompt (checked 2026-11-15).

### Install and invoke

`curl -fsSL https://gh.io/copilot-install | bash` · `brew install copilot-cli` ·
`winget install GitHub.Copilot` · `npm install -g @github/copilot`. Then run
`copilot` (Linux/macOS/Windows).

## Copilot SDK (embed the CLI's agent engine)

The [Copilot SDK repository][copilot-sdk] (MIT, "Multi-platform SDK for integrating GitHub Copilot
Agent into apps and services"; created 2026-01-14, formerly under the `github` organisation, now
`microsoft/copilot-sdk`) exposes "the same engine behind Copilot CLI" as a library. It sits in this
doc because it is the programmable form of the harness described above (re-read 2026-11-20 at the
README and `gh api`).

- **Rename in progress.** The README banner says the GitHub Copilot SDK "is becoming Microsoft
  Copilot SDK", the interface to the Microsoft Copilot harness, with package names that may still
  say GitHub during the transition; the harness naming is tracked in
  [microsoft-365-copilot-analysis.md](microsoft-365-copilot-analysis.md#three-things-called-harness).
- **Languages:** Python, TypeScript, Go, .NET, Java and Rust. The runtime is a native component
  driven over JSON-RPC, loaded in-process by default, with spawned-process and standalone-server
  modes for isolation; the README says in-process hosting gives no crash isolation or sandbox.
- **Auth and licence:** a GitHub Copilot subscription is required, including the free tier, unless
  you bring your own key (BYOK) from a supported model provider, where no GitHub authentication is
  needed. BYOK is key-based only; the README says Entra ID, managed identities and third-party
  identity providers are not supported there. Usage counts against the same allowance as the CLI.
  Non-BYOK auth paths: a signed-in CLI user, an OAuth GitHub App token, or
  `COPILOT_GITHUB_TOKEN` / `GH_TOKEN` / `GITHUB_TOKEN`.
- **Tools by default:** the CLI's first-party tools are exposed, similar to `--allow-all`; the
  application's permission handler decides each call, so an embedding app owns the approval policy.
- **Status (2026-11-20):** latest stable release v2.0.1 (2026-11-18); v2.0.2 pre-releases on
  2026-11-19; repository pushed 2026-11-19. The README states "The Microsoft Copilot SDK is
  generally available and follows semantic versioning" ([README][copilot-sdk]).
- **Licence scope:** the repository is MIT, but the README does not say whether the MIT licence
  also covers the native runtime the SDK loads (it describes a separate runtime component), so
  whether the CLI engine itself is open for reuse is unclear. Check the runtime package's own
  licence before relying on it.
- Skill Recorder's GitHub description cites a "Copilot SDK"; see
  [skill-recorder-analysis.md](skill-recorder-analysis.md).

## Adoption Decision

| Dimension | Assessment |
|---|---|
| **Use case** | Terminal coding agent; peer to Codex CLI / Gemini CLI / Claude Code (Gemini CLI: [status 2026-11-18](../coding-agents/gemini-cli-analysis.md), no longer served for free, AI Pro, AI Ultra users) |
| **Model flexibility** | Multi-provider via `/model` (default Claude Sonnet 4.5) |
| **Extensibility** | MCP (GitHub server default), custom agents, plugins, LSP |
| **Permission model** | Preview-every-action → plan/autopilot → `--yolo`; local/cloud sandbox |
| **Maturity** | GA 2026-02-25, actively released (v1.0.61) |
| **License** | **Proprietary** (CLI) — no modification, no standalone redistribution; the SDK repository is MIT, runtime licence unclear ([SDK section](#copilot-sdk-embed-the-clis-agent-engine)) |
| **Cost** | Copilot Pro / Pro+ / Business / Enterprise; usage billed in GitHub AI Credits. The SDK also works on the Copilot free tier (limited usage) per its README, or with your own model key |

**Strengths**: Same agentic harness as the Copilot coding agent — consistent
behavior across CLI and cloud. Reuses existing GitHub auth, billing, and MCP
server (lowest onboarding friction for orgs already on Copilot). Strong
permission/sandbox model. Multi-provider model choice.

**Risks**: **Proprietary CLI license** — cannot fork or self-host the CLI (unlike
Aider/Kilo/OpenCode); embedding goes through the MIT-licensed SDK, whose runtime licence is unclear. Subscription + AI-credit allowance.
Business/Enterprise use requires admin enablement. PAT auth keys
off `GH_TOKEN`/`GITHUB_TOKEN` — watch for env-var shadowing in CI.

## Action Items

- **Evaluate** as the terminal agent for teams already holding Copilot
  Business/Enterprise — no new vendor, reuses GitHub identity and billing.
- **Disambiguate** in any agent comparison: CLI (local, interactive) vs coding
  agent (cloud, issue→PR) — same harness, different surface.
- **Reuse an existing `AGENTS.md`** in multi-agent repos — the CLI reads it, so a separate
  `copilot-instructions.md` is optional ([multi-agent-onboarding-outlook.md](../../sdlc-lcm/multi-agent-onboarding-outlook.md)).
- **Flag the license** when comparing against OSS peers — adoption is reversible
  only at the subscription level, not the code level.

## Goal Loop

Checked 2026-10-22 against the vendor's own docs; compared across agents in
[goal-loops-landscape.md](../coding-agents/goal-loops-landscape.md).

The CLI lists `/goal [OBJECTIVE]` in the same row as `/autopilot [OBJECTIVE]`; "Without an objective,
autopilot infers intent from context", and `--max-ai-credits N` caps spend
([command reference][goal-copilot-cmds]). The page doesn't say who judges completion. An `agentStop`
hook "can block and force continuation"; "After 8 consecutive block continuations, the CLI overrides
the hook and ends the turn anyway" ([hooks][goal-copilot-hooks]).

## Cross-References

- [github-copilot-cloud-agent-analysis.md](github-copilot-cloud-agent-analysis.md) — the cloud agent, automations, MCP config, instructions and code review
- [CC-github-actions-analysis.md](../../cc-native/ci-remote/CC-github-actions-analysis.md#issue-lifecycle-automation-landscape) — the Copilot **coding agent** (cloud) it shares a harness with
- [multi-agent-onboarding-outlook.md](../../sdlc-lcm/multi-agent-onboarding-outlook.md) — the AGENTS.md/GEMINI.md convergence + per-agent config-file comparison
- [CC-community-tooling-landscape.md](../../cc-community/CC-community-tooling-landscape.md) — multi-agent tooling (CC Switch, CodeBurn) that targets Copilot; `~/.copilot` session data

## Sources

| Source | Content |
|---|---|
| [github/copilot-cli repo][copilot-cli-repo] | Install, models, MCP, permission model, license |
| [Copilot CLI docs][copilot-cli-docs] | Agents, slash commands, config files, sandboxing, auth |
| [Copilot CLI overview][copilot-cli-overview] | Capabilities, autopilot, LSP, quota |
| [GA changelog 2026-02-25][copilot-cli-ga] | GA date, eligible plans, headline features |
| [Copilot CLI custom instructions][copilot-cli-instructions] | Instruction files incl. AGENTS.md / CLAUDE.md / GEMINI.md (checked 2026-10-24) |
| [Using Copilot CLI][copilot-cli-use] | AI Credits in `/usage` (checked 2026-10-24) |
| [microsoft/copilot-sdk][copilot-sdk] | README, MIT licence, languages, auth and BYOK, rename notice, releases (2026-11-20) |

[copilot-cli-repo]: https://github.com/github/copilot-cli
[copilot-sdk]: https://github.com/microsoft/copilot-sdk
[copilot-cli-license]: https://github.com/github/copilot-cli/blob/main/LICENSE.md
[copilot-cli-docs]: https://docs.github.com/en/copilot/how-tos/copilot-cli
[copilot-cli-overview]: https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview
[copilot-cli-ga]: https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/
[copilot-agent]: https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent
[copilot-cli-instructions]: https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-custom-instructions
[copilot-cli-use]: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli
[goal-copilot-cmds]: https://docs.github.com/en/copilot/reference/cli-command-reference
[goal-copilot-hooks]: https://docs.github.com/en/copilot/reference/hooks-configuration
[copilot-legacy-requests]: https://docs.github.com/en/copilot/reference/copilot-billing/request-based-billing-legacy/copilot-requests
