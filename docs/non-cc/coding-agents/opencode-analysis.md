---
title: opencode Analysis
source: https://github.com/sst/opencode
purpose: Analysis of opencode as a provider-agnostic, open-source terminal coding agent with TUI, desktop, and headless modes.
created: 2026-06-16
updated: 2026-11-28
validated_links_on: 2026-11-09
status: trial
---

**Details:** **License**: MIT | **Latest release**: v1.19.6 (2026-11-17) | **Stars**: ~229 k (anomalyco/opencode, checked 2026-11-26). Also runs on or integrates with: `terminal`, `desktop`, `ide`, `web`, `headless`.

## What It Is

opencode is an **open-source, provider-agnostic AI coding agent** built for the
terminal. It combines a rich TUI (Terminal User Interface) with a headless
`opencode run` mode, a desktop application (macOS/Windows/Linux; no longer labelled beta on first-party pages as of 2026-11-26), and IDE
extensions — all driven by the same engine and `opencode.json` configuration.

The project originated inside [SST][sst] (the Serverless Stack infra framework
team) and is now maintained by Anomaly under the
[`anomalyco/opencode`][gh-repo] GitHub organisation (the `sst/opencode`
canonical URL still resolves). It reached ~229 k GitHub stars by 2026-11-26,
making it one of the fastest-growing open-source coding-agent projects.

**Key distinction vs proprietary peers** (GitHub Copilot CLI, Cursor): opencode
is fully MIT-licensed, self-hostable, and brings your own API key — there is no
required subscription and no vendor lock-in on the inference layer. Compare
with [GitHub Copilot CLI][gh-copilot-cli], which requires an active Copilot
subscription and routes all inference through GitHub.

## How It Works

### Dual-agent system

| Agent | Purpose | Default permissions |
|---|---|---|
| **build** | Full development loop — edit files, run bash | Full write + execute |
| **plan** | Read-only analysis of unfamiliar codebases | Edits disabled; bash requires approval |

Switch between agents with Tab. A **general subagent** (`@general`) handles
complex multi-step searches and delegates sub-tasks while keeping the primary
context clean.

### Provider support

opencode integrates 200+ LLM providers (per opencode.ai, checked 2026-11-26) via the AI SDK and [Models.dev][models-dev],
including Anthropic, OpenAI, Google Vertex AI, Azure OpenAI, AWS Bedrock, GitHub
Copilot, GitLab Duo, DeepSeek, Groq, xAI, Ollama, LM Studio, OpenRouter, and
OpenAI-compatible custom endpoints. Credentials are stored in
`~/.local/share/opencode/auth.json` and can also be supplied via environment
variables. Model selection uses `/connect` then `/models` or the `--model` flag
(format: `provider/model-id`).

Two managed tiers sit on top of bring-your-own-key:

- **OpenCode Zen** — curated, team-vetted model list for newcomers.
- **OpenCode Go** — low-cost subscription for popular open coding models.
  (Not required; BYOK works without either tier, per [opencode.ai/docs/providers][providers-doc].)

### MCP (Model Context Protocol) support

opencode supports both local (subprocess) and remote (HTTP/OAuth) MCP servers,
configured under the `mcp` key in `opencode.json`. Remote configurations can
also be distributed via a repo's `.well-known/opencode` endpoint so teams share
a consistent MCP baseline. Token budget guidance is explicit in the docs:
high-token MCP servers (e.g. the GitHub MCP server) can exhaust context limits
and should be enabled selectively ([MCP servers doc][mcp-doc]).

### Headless / non-interactive mode

`opencode run "<prompt>"` executes a prompt without launching the TUI, making
it scriptable in CI or automation pipelines. Supporting commands:

| Command | Purpose |
|---|---|
| `opencode run` | Non-interactive single-prompt execution |
| `opencode serve` | Start a headless server for API access |
| `opencode web` | Headless server with web-browser UI |
| `opencode attach` | Attach TUI to an already-running backend |

Output format is selectable via `--format json` for structured consumption.

### Configuration and extensibility

Configuration merges from multiple layers (project `opencode.json`, global
`~/.config/opencode/opencode.json`, env var `OPENCODE_CONFIG`, remote
`.well-known/opencode`). Key knobs: `model`, `small_model`, `tools`
(enable/disable write/bash per agent), `permission` (approval granularity),
`snapshot` (file-change tracking, on by default), `mcp`, `keybinds`, and
`autoupdate`.

Project context is seeded via an `AGENTS.md` file (created on
`opencode init`) that describes repo structure and coding conventions —
aligned with the emerging cross-editor AGENTS.md standard.

### Notable UX features

- **Plan mode** (Tab toggle): disables edits, proposes a step-by-step
  implementation plan before any files are touched.
- **`/undo`**: reverts the last change and restores the prior prompt.
- **Image input**: drag-and-drop images into the terminal to include visual
  references (design mockups, screenshots) in the prompt.
- **`/share`**: publishes a session as a shareable link for async team review.
- **Rune (announced, not shipped):** Anomaly, the company behind opencode, is building [Rune][rune], an MIT-licensed native GPU-rendered Rust UI framework (no releases yet, 2026-11-09). Its plan calls recreating OpenCode Desktop in Rune "the flagship test", and every Rune app can run headless so an agent can render it to PNG, dump the element tree and drive it with scripted input. Whether OpenCode Desktop will move to it is not stated as shipped.

### Install

```bash
curl -fsSL https://opencode.ai/install | bash  # one-liner
brew install opencode                           # Homebrew
npm install -g opencode                         # npm
# also: Scoop, Pacman, Nix, desktop app at opencode.ai/download
```

See the [Cross-Harness Matrix](../../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#cross-harness-matrix-checked-2026-11-15) for sandbox, permissions, hooks, skills, subagents and MCP side by side with the other harnesses.

## Adoption Decision

**Trial** — opencode is real, active, and already at significant scale (~229 k
stars, v1.19.6 in November 2026). The MIT license, 200+ provider support, and full
headless mode make it immediately deployable without a vendor subscription.
Two concerns prevent **Adopt** today:

1. The desktop application was labelled **beta** on opencode.ai in June 2026; the label is gone as of 2026-11-26 ([opencode.ai][home]), but stability for the GUI surface is unvalidated.
2. Managed tiers (Zen, Go) are new commercial offerings with limited public
   track record — BYOK path remains solid but SLA details are not
   disclosed on first-party pages. Go is priced "from $10/month" (opencode.ai, checked 2026-11-26); Zen is not mentioned there (unverified).

For terminal/headless use in CI or local development with BYOK, opencode is
ready to trial. Gate full adoption on desktop GA and production mileage reports.

## Action Items

- [ ] Run `opencode run` in a sample repo to validate headless CI integration.
- [ ] Benchmark context consumption with the GitHub MCP server enabled (MCP
      docs warn this can exhaust limits).
- [ ] Track whether a desktop GA is announced — the beta label is gone but no GA statement was seen.
- [ ] Evaluate OpenCode Zen/Go managed tiers (Go pricing is public; Zen is unverified).
- [ ] Verify AGENTS.md compatibility with CC and Copilot CLI harnesses
      (cross-tool portability).

## Sources

| Source | Content |
|---|---|
| [anomalyco/opencode GitHub repo][gh-repo] | License (MIT), star count (~229 k), v1.19.6 release date, install methods; accessed 2026-06-16 |
| [opencode.ai home][home] | Product overview, desktop status, 200+ providers claim; checked 2026-11-26 |
| [opencode.ai/docs][docs] | TUI features, plan mode, /undo, /share, AGENTS.md, image input; accessed 2026-06-16 |
| [opencode.ai/docs/providers][providers-doc] | Full provider list, Zen/Go tiers, /connect + /models workflow; accessed 2026-06-16 |
| [opencode.ai/docs/config][config-doc] | Configuration layers, MCP key, tool/permission/snapshot options; accessed 2026-06-16 |
| [opencode.ai/docs/mcp-servers][mcp-doc] | Local/remote MCP, OAuth, token budget warning; accessed 2026-06-16 |
| [opencode.ai/docs/cli][cli-doc] | `opencode run`, `serve`, `web`, `attach`, `--format json`; accessed 2026-06-16 |
| [GitHub release v1.19.6][release] | Latest release, 2026-11-17 |
| [GitHub Copilot CLI analysis][gh-copilot-cli] | Proprietary peer comparison |
| [anomalyco/rune][rune] | README, PLAN.md, LICENSE (MIT), no releases; `gh api` 2026-11-09 |

[gh-repo]: https://github.com/sst/opencode
[home]: https://opencode.ai/
[docs]: https://opencode.ai/docs
[providers-doc]: https://opencode.ai/docs/providers
[config-doc]: https://opencode.ai/docs/config
[mcp-doc]: https://opencode.ai/docs/mcp-servers
[cli-doc]: https://opencode.ai/docs/cli
[release]: https://github.com/sst/opencode/releases/tag/v1.19.6
[models-dev]: https://models.dev
[sst]: https://sst.dev
[gh-copilot-cli]: ../agents/github-copilot-cli-analysis.md
[rune]: https://github.com/anomalyco/rune
