---
title: Devin CLI (Cognition) Analysis
source: https://devin.ai/cli
purpose: Evaluate Devin CLI as an interactive terminal coding agent, distinct from autonomous cloud Devin.
platform_scope: [cli, cloud]
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
---

**Status**: Trial | **GA**: ~April 2026 | **Vendor**: Cognition AI | **License**: Proprietary | requires Devin account (free tier available)

## What It Is

Devin CLI is a **local terminal coding agent** by Cognition AI — "a local
command-line coding agent with deep Devin Cloud integration." It runs directly
in your terminal against local files and environment, offering interactive
development assistance with a seamless escalation path to cloud Devin.

**Critical disambiguation**: Devin CLI ≠ autonomous cloud Devin. The CLI is
for interactive local work ("quick fixes, code exploration"); cloud Devin runs
in a remote VM with Playbooks, Secrets, Knowledge, video recordings, and PR
completion. The `/handoff` command bridges the two: start locally, then
escalate to cloud when the task grows. The cloud surface — including its GitHub
Actions integration — is covered in
[CC-github-actions-analysis.md](../cc-native/ci-remote/CC-github-actions-analysis.md).

**Devin Desktop** (formerly Windsurf/Cascade) is a separate surface: a full
IDE with an agent manager. The CLI is pure terminal; Desktop is GUI-first. The
underlying local agent ("Devin Local") is written in Rust and replaced Cascade
as of July 2026. Devin CLI and Devin Desktop share the same usage quota.

## How It Works

### Installation

Multiple methods (accessed 2026-06-16):

```bash
# macOS / Linux / WSL
curl -fsSL https://cli.devin.ai/install.sh | bash
# Homebrew
brew install --cask devin-cli
# Windows: x86_64 or ARM64 executables, or PowerShell setup script
```

Enterprise plans bundle the CLI with Devin Desktop; admins must enable
installation in team settings. After install, restart the terminal and navigate
to a project directory.

### Invocation and modes

| Invocation | Behavior |
|---|---|
| `devin` | Launch interactive REPL |
| `devin -- <prompt>` | REPL with pre-loaded prompt |
| `devin -p "<prompt>"` | **Single-turn / headless** — runs prompt, prints to stdout, exits |
| `devin -c` / `--continue` | Resume most recent session |
| `devin -r` / `--resume` | Pick from recent sessions interactively |

### Permission modes

Cycle with `Shift+Tab` or pass at startup:

| Mode | Behavior |
|---|---|
| **Normal** (default) | Prompts for writes and shell commands |
| **Accept Edits** | Auto-approves file edits; prompts on shell commands |
| **Bypass** | Auto-approves all tool calls including shell |
| **Autonomous** | Requires `--sandbox`; auto-approves within OS-level isolation |

### Key slash commands

`/handoff` escalates the current task to cloud Devin with full context. Other
commands: `/plan`, `/ask`, `/loop <prompt>` (iterative automation), `/model`,
`/resume`, `/compact`, `/add-dir`, `/workspace`, `/login`, `/update`.

Shell integration (`devin wrap-shell`) lets users invoke Devin from any shell
prompt without a separate `devin` invocation.

### Multi-model support

Supported models include Cognition SWE-1.6, Anthropic Opus 4.8 / Sonnet /
Haiku, OpenAI GPT-5.5 / Codex, Google Gemini, Kimi K2.5, and GLM 5 (per
2026-06-16 search data; model list subject to change). Select via `/model`.

### Limitations vs. cloud Devin

Devin CLI does **not yet** support Knowledge, Playbooks, or Secrets — these
are cloud-only features. Complex, long-running tasks should be handed off via
`/handoff`.

## Adoption Decision

| Dimension | Assessment |
|---|---|
| **Use case** | Interactive local terminal agent; quick fixes, exploration, /handoff for complex tasks |
| **Headless** | Partial — `-p` flag for single-turn scripting; `--permission-mode bypass` for unattended runs |
| **Model flexibility** | Multi-provider (Anthropic, OpenAI, Google, Cognition, Kimi, GLM) |
| **Pricing** | Free tier; Pro $20/mo; Max $200/mo — quota shared with Devin Cloud and Desktop |
| **ACU cost** | ~$2.25/ACU on Pro; 15 min active work ≈ 1 ACU (per third-party analysis, 2026-06) |
| **Maturity** | GA ~April 2026; actively developed; Rust-rewrite "Devin Local" shipped June 2026 |
| **License** | Proprietary — no source, no self-host |
| **Sandboxing** | OS-level sandbox in Autonomous mode; local execution otherwise |

**Strengths**: Low-friction entry (free tier; curl install); `/handoff`
bridges CLI and cloud in a single workflow; multi-provider model choice; `-p`
flag makes scripting viable; shared quota model avoids per-surface billing
complexity. Written in Rust for performance (up to 30% more token-efficient
than legacy Cascade per Cognition blog, 2026-06-02).

**Risks**: Proprietary — no self-host, no fork. Cloud features (Playbooks,
Secrets, Knowledge) unavailable locally, creating a feature gap for teams
that rely on them. ACU pricing is opaque at the free/Pro tier level (not
documented first-party as of 2026-06-16). Quota shared across CLI + Desktop +
Cloud sessions means heavy Desktop use reduces CLI budget. No AGENTS.md
support noted in docs (not confirmed either way).

**Verdict — Trial**: The `/handoff` bridge and multi-model support make Devin
CLI worth piloting for teams already evaluating Devin Cloud. Holds the same
position as [GitHub Copilot CLI][copilot-cli-doc] in the terminal-agent tier —
evaluate against your existing subscriptions before adding a new vendor.

## Action Items

- **Pilot** `devin -p "<prompt>"` in CI scripts to assess headless reliability
  before committing to the platform.
- **Evaluate** the `/handoff` workflow for tasks that outgrow the local CLI —
  confirm cloud Devin ACU consumption stays within plan quota.
- **Confirm AGENTS.md / CLAUDE.md pick-up** experimentally; docs do not
  address cross-agent instruction-file conventions as of 2026-06-16.
- **Monitor** Knowledge/Playbooks/Secrets support landing in CLI — these are
  roadmap items and would close the local/cloud feature gap.
- **Disambiguate** in team docs: Devin CLI (local/interactive) vs Devin Cloud
  (VM/autonomous/GHA) vs Devin Desktop (IDE) — three surfaces, one billing pool.

## Cross-References

- [CC-github-actions-analysis.md](../cc-native/ci-remote/CC-github-actions-analysis.md) — autonomous cloud Devin via GitHub Actions (the `/handoff` destination)
- [github-copilot-cli-analysis.md](github-copilot-cli-analysis.md) — peer terminal agent; compare permission models and headless support
- [multi-agent-onboarding-outlook.md](../sdlc-lcm/multi-agent-onboarding-outlook.md) — per-agent config-file and onboarding comparison

## Sources

| Source | Content |
|---|---|
| [Devin CLI landing page][devin-cli-page] | Product overview, installation, multi-model list, Rust implementation |
| [Devin CLI docs index][devin-cli-docs] | Quickstart, installation methods, local vs cloud distinction, /handoff |
| [Devin CLI commands reference][devin-cli-cmds] | Full command list, permission modes, slash commands, headless `-p` flag |
| [Devin billing self-serve][devin-billing] | Plan tiers (Free/$20/$200), shared quota across CLI+Desktop+Cloud, ACU to credit mapping |
| [Windsurf → Devin Desktop blog][devin-desktop-blog] | Rust rewrite (Devin Local), Cascade sunset July 2026, Desktop vs CLI distinction |
| [TerminalTrove / web search][search-result] | ~April 9 2026 CLI launch date, ACU cost estimate ($2.25/ACU, 15 min ≈ 1 ACU); third-party — treat as approximate |

[devin-cli-page]: https://devin.ai/cli
[devin-cli-docs]: https://docs.devin.ai/cli/index.md
[devin-cli-cmds]: https://docs.devin.ai/cli/essential-commands.md
[devin-billing]: https://docs.devin.ai/admin/billing/self-serve.md
[devin-desktop-blog]: https://devin.ai/blog/windsurf-is-now-devin-desktop/
[copilot-cli-doc]: github-copilot-cli-analysis.md
[search-result]: https://terminaltrove.com/ai-coding-agents/devin-for-terminal/
