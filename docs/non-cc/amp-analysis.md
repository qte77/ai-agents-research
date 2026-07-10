---
title: Amp Analysis
source: https://ampcode.com/
purpose: Analysis of Amp (Sourcegraph spinoff) as a terminal-first agentic coding tool with pay-as-you-go model pricing.
created: 2026-06-16
updated: 2026-07-10
validated_links: 2026-06-16
---

**Status**: Trial | **GA**: May 7, 2026 (public launch; free tier since Oct 15, 2025) | **Vendor**: Amp Frontier Corporation (spun out of Sourcegraph, Dec 2, 2025) | **License**: Proprietary (closed source) | No markup on provider API prices for individuals

## What It Is

Amp is a **terminal-first, multi-model agentic coding tool** — "the frontier
coding agent built for leading models, and what comes next." Originally developed
at Sourcegraph as a successor to Cody, it spun out as an independent company
(Amp Frontier Corporation) on December 2, 2025, and publicly launched to everyone
on May 7, 2026.

The tool runs in the terminal (CLI package `@sourcegraph/amp`), syncs threads
across web and mobile, and exposes editor plugins for Neovim ([amp.nvim][amp-nvim])
and an examples-and-guides repository. It is **not open source**; no source code
or license terms are published. The CLI is distributed as an npm package under the
`@sourcegraph` scope.

**Key distinction vs OSS peers** (Aider, OpenCode, Kilo Code): Amp passes
through model costs with zero markup for individuals, making it cheaper than
fixed-subscription tools for low-to-moderate usage, but it is fully proprietary
and cloud-dependent for credit management.

## How It Works

### Architecture and modes

Amp runs as a CLI agent (`amp`) that orchestrates LLM calls, file edits, shell
commands, and web search in persistent "threads" that sync across devices. Three
operating modes select models automatically:

| Mode | Model (as of 2026-06-16) | Use case |
|---|---|---|
| **smart** | Claude Opus 4.8 | Maximum capability, self-verification |
| **deep** | GPT-5.5 | Complex multi-step reasoning |
| **rush** | GPT-5.5 (fast variant) | Quick, interactive tasks |

87% faster Deep/Rush startup and 32% faster completions were shipped June 5,
2026 (accessed 2026-06-16 from ampcode.com/news).

### CLI and headless operation

Install globally: `pnpm add -g @sourcegraph/amp` (or npm / yarn). Core invocation
patterns:

- **Interactive**: `amp` — starts a threaded session in the terminal
- **Execute mode (headless)**: `amp -x "<prompt>"` — single-shot, non-interactive;
  consumes paid credits; suitable for CI/CD scripts and pipelines
- **JSON streaming**: `--stream-json` — structured output for programmatic integration
- **Usage inspection**: `amp usage` — view credit consumption

Amp is designed to "run anywhere — from your terminal, IDE, CI/CD pipelines,
Docker container or anywhere with a terminal" (ampcode.com/manual, accessed
2026-06-16).

### Extensibility

- **AGENTS.md** guidance files for codebase-specific instructions (same
  convention as Claude Code)
- **Plugins** via TypeScript SDK for extending tool definitions
- **MCP servers** for external integrations
- **Subagent spawning** for parallel work
- **Python and TypeScript SDKs** for embedding Amp capabilities

### Pricing model

Amp charges actual provider API costs with **zero markup for individuals**. If a
thread consumes $2 in Anthropic API calls and $0.50 in OpenAI calls, the user is
billed exactly $2.50. Minimum credit purchase is **$5**; unused credits expire
after one year of account inactivity. Interactive CLI sessions are free;
execute-mode (`-x`) consumes credits.

**Enterprise**: 50% premium over standard rates; activation requires a one-time
**$1,000 USD purchase** that converts to equivalent credits and upgrades workspace
access. Enterprise workspaces include per-user quotas and managed settings.

A legacy **Frontier Access** tier ($10/day, launched Jan 8, 2026) provided early
access to smart/deep modes; the current pricing model replaced it at the May 2026
public launch.

## Adoption Decision

| Dimension | Assessment |
|---|---|
| **Use case** | Terminal agent + CI/CD headless mode; peer to Claude Code, Copilot CLI, Codex CLI |
| **Model flexibility** | Multi-provider (Anthropic + OpenAI); mode-based auto-selection |
| **Extensibility** | MCP, TypeScript plugins, AGENTS.md, Python/TypeScript SDKs |
| **Headless** | Yes — `amp -x` + `--stream-json` for scripted/CI use |
| **Maturity** | Public GA May 7, 2026; active weekly releases |
| **License** | **Proprietary** — no source, no self-hosting |
| **Cost** | Zero-markup individual pricing; $1k enterprise activation; $5 min credit |
| **Vendor** | Amp Frontier Corporation (independent since Dec 2025, ex-Sourcegraph) |

**Strengths**: Zero-markup model pricing is compelling for cost-conscious teams
that already pay for Anthropic/OpenAI API access. AGENTS.md compatibility aligns
with Claude Code conventions — lower config friction in mixed shops. Headless
execute mode and JSON streaming make it scriptable for CI. Multi-model routing
avoids single-provider lock-in at the tool level.

**Risks**: Fully proprietary with no self-hosting option — all credit management
is cloud-dependent. Spinoff trajectory (Sourcegraph → Amp Frontier Corporation,
Dec 2025) is recent; organizational stability unproven at enterprise scale. No
editor extension for VS Code or JetBrains at time of writing (only Neovim plugin
confirmed). Enterprise $1k activation is a meaningful commitment for a young
product.

## Action Items

- **Pilot** execute mode (`amp -x`) in a CI workflow where zero-markup pricing
  vs a fixed-subscription agent (Copilot CLI, Claude Code) is the key variable.
- **Validate** AGENTS.md portability: test whether codebase instruction files
  authored for Claude Code transfer without modification.
- **Monitor** editor integration: VS Code / JetBrains support has not shipped as
  of 2026-06-16 — track the changelog.
- **Reassess** at 6 months post-GA (Nov 2026) on organizational stability and
  whether enterprise pricing has stabilized.

## Cross-References

- [github-copilot-cli-analysis.md](github-copilot-cli-analysis.md) — proprietary peer with fixed subscription model; useful cost comparison baseline

## Sources

| Source | Content |
|---|---|
| [ampcode.com home][amp-home] | Product description, model list, feature overview (accessed 2026-06-16) |
| [ampcode.com pricing][amp-pricing] | Credit model, zero markup, enterprise $1k activation, $5 minimum (accessed 2026-06-16) |
| [ampcode.com news][amp-news] | Spinoff date (Dec 2, 2025), public launch (May 7, 2026), changelog (accessed 2026-06-16) |
| [ampcode.com manual (CLI guide)][amp-manual-cli] | Install commands, execute mode, headless usage, CI/CD patterns (accessed 2026-06-16) |
| [amp-examples-and-guides repo][amp-examples] | Supplemental guides, 47 stars, JavaScript/Shell; confirms CLI-first design (accessed 2026-06-16) |
| [amp.nvim repo][amp-nvim] | Neovim plugin; only confirmed editor integration at time of writing (accessed 2026-06-16) |
| [Product Hunt listing][amp-ph] | Confirms Sourcegraph authorship; community reception (accessed 2026-06-16) |
| [Sourcegraph Wikipedia][sg-wiki] | Organizational background; Cody → Amp transition (accessed 2026-06-16) |

[amp-home]: https://ampcode.com/
[amp-pricing]: https://ampcode.com/manual
[amp-news]: https://ampcode.com/news
[amp-manual-cli]: https://github.com/sourcegraph/amp-examples-and-guides/blob/main/guides/cli/README.md
[amp-examples]: https://github.com/sourcegraph/amp-examples-and-guides
[amp-nvim]: https://github.com/sourcegraph/amp.nvim
[amp-ph]: https://www.producthunt.com/products/amp-free
[sg-wiki]: https://en.wikipedia.org/wiki/Sourcegraph
