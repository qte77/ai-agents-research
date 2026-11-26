---
title: Devin CLI (Cognition) Analysis
source: https://devin.ai/cli
purpose: Evaluate Devin CLI as an interactive terminal coding agent, distinct from autonomous cloud Devin.
created: 2026-06-16
updated: 2026-11-26
validated_links_on: 2026-06-16
status: trial
---

**Details:** **GA**: ~April 2026 (unverified; third-party only) | **Vendor**: Cognition AI | **License**: Proprietary | requires Devin account (free tier available). Also runs on or integrates with: `cli`, `cloud`.

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
[CC-github-actions-analysis.md](../../cc-native/ci-remote/CC-github-actions-analysis.md).

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
| **Smart** | A fast model judges what is safe to run (`--permission-mode smart`, `/smart`) |
| **Bypass** | Auto-approves all tool calls including shell (aliases `/yolo`, `/dangerous`) |
| **Autonomous** | Requires `--sandbox` (`devin --sandbox --permission-mode autonomous`); auto-approves within OS-level isolation |

### Key slash commands

`/handoff` escalates the current task to cloud Devin with full context. Other
commands: `/plan`, `/ask`, `/loop <prompt>` (iterative automation), `/model`,
`/resume`, `/compact`, `/add-dir`, `/workspace`, `/login`, `/update`.

Shell integration (`devin wrap-shell`) lets users invoke Devin from any shell
prompt without a separate `devin` invocation (unverified; not in the commands reference or on the landing page).
Other flags: `--cloud` starts a cloud session and `-r <session-id>` resumes one.

### Multi-model support

The [landing page](https://devin.ai/cli) (checked 2026-11-26) lists Anthropic Claude Fable 5.1,
Opus 5 and Sonnet 5; OpenAI GPT-5.6 Sol, GPT-5.6 Luna and GPT-6 Astra; Google
Gemini 3.7 Flash; Cognition SWE-2, Fusion and Adaptive; and open-weight Kimi,
GLM-5.3 and DeepSeek V4 Pro/Flash (model list subject to change). Select via `/model`.

### Limitations vs. cloud Devin

Devin CLI does **not yet** support Knowledge, Playbooks, or Secrets — these
are cloud-only features. Complex, long-running tasks should be handed off via
`/handoff`.

### Open-source alternative to cloud Devin: OpenComputer

[diggerhq/opencomputer][opencomputer] describes itself as "an open-source, faster Devin alternative" (the vendor's own tagline, not an independent comparison). Per its README, you mention `@Computer` in a Slack thread, a gateway starts a Claude Code, Codex or OpenCode session per thread in rootless Podman, and the result lands as a pull request; the stack is self-hostable (a VM plus Cloudflare Workers and Durable Objects) or runs on the vendor's cloud. Apache-2.0 per the `LICENSE` file; created 2025-12-09, 1,810 stars, latest release v0.6.0.50 (2026-11-09) (`gh api` 2026-11-26). Its headline "3.3x faster than Devin" (56s vs 185s to open four PRs) is the vendor's own benchmark on its own blog, not independently verified. Adoption not yet shown: no named independent users were found in the README. Nothing was installed or run.

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
Cloud sessions means heavy Desktop use reduces CLI budget. The landing page FAQ says AGENTS.md rules, MCP servers and
Claude Code plugins load as-is; CLAUDE.md pick-up is not stated.

**Verdict — Trial**: The `/handoff` bridge and multi-model support make Devin
CLI worth piloting for teams already evaluating Devin Cloud. Holds the same
position as [GitHub Copilot CLI][copilot-cli-doc] in the terminal-agent tier —
evaluate against your existing subscriptions before adding a new vendor.

## Action Items

- **Pilot** `devin -p "<prompt>"` in CI scripts to assess headless reliability
  before committing to the platform.
- **Evaluate** the `/handoff` workflow for tasks that outgrow the local CLI —
  confirm cloud Devin ACU consumption stays within plan quota.
- **Confirm CLAUDE.md pick-up** experimentally; AGENTS.md is stated first-party
  (landing page FAQ, checked 2026-11-26), CLAUDE.md is not.
- **Monitor** Knowledge/Playbooks/Secrets support landing in CLI — these are
  roadmap items and would close the local/cloud feature gap.
- **Disambiguate** in team docs: Devin CLI (local/interactive) vs Devin Cloud
  (VM/autonomous/GHA) vs Devin Desktop (IDE) — three surfaces, one billing pool.

## Cross-References

- [CC-github-actions-analysis.md](../../cc-native/ci-remote/CC-github-actions-analysis.md) — autonomous cloud Devin via GitHub Actions (the `/handoff` destination)
- [github-copilot-cli-analysis.md](../agents/github-copilot-cli-analysis.md) — peer terminal agent; compare permission models and headless support
- [multi-agent-onboarding-outlook.md](../../sdlc-lcm/multi-agent-onboarding-outlook.md) — per-agent config-file and onboarding comparison

## Sources

| Source | Content |
|---|---|
| [Devin CLI landing page][devin-cli-page] | Product overview, installation, multi-model list, Rust implementation |
| [Devin CLI docs index][devin-cli-docs] | Quickstart, installation methods, local vs cloud distinction, /handoff |
| [Devin CLI commands reference][devin-cli-cmds] | Full command list, permission modes, slash commands, headless `-p` flag |
| [Devin billing self-serve][devin-billing] | Plan tiers (Free $0, Pro $20, Max $200, Teams $80) and on-demand credits; no ACU mapping |
| [Windsurf → Devin Desktop blog][devin-desktop-blog] | Rust rewrite (Devin Local), Cascade sunset July 2026, Desktop vs CLI distinction |
| [OpenComputer repository][opencomputer] | Open-source Devin-style Slack agent: README, Apache-2.0 `LICENSE`, `gh api` record and release (read 2026-11-23); vendor claims |
| [TerminalTrove / web search][search-result] | ~April 9 2026 CLI launch date, ACU cost estimate ($2.25/ACU, 15 min ≈ 1 ACU); third-party — treat as approximate |

[devin-cli-page]: https://devin.ai/cli
[devin-cli-docs]: https://docs.devin.ai/cli/index.md
[devin-cli-cmds]: https://docs.devin.ai/cli/essential-commands.md
[devin-billing]: https://docs.devin.ai/admin/billing/self-serve.md
[devin-desktop-blog]: https://devin.ai/blog/windsurf-is-now-devin-desktop/
[copilot-cli-doc]: ../agents/github-copilot-cli-analysis.md
[search-result]: https://terminaltrove.com/ai-coding-agents/devin-for-terminal/
[opencomputer]: https://github.com/diggerhq/opencomputer
