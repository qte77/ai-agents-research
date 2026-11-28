---
title: Amp Analysis
source: https://ampcode.com/
purpose: Analysis of Amp (Sourcegraph spinoff) as a terminal-first agentic coding tool with pay-as-you-go model pricing.
created: 2026-06-16
updated: 2026-11-28
validated_links_on: 2026-06-16
status: trial
---

**Details:** **GA**: May 27, 2026 (rebuilt Amp available to everyone; free tier since Oct 15, 2025) | **Vendor**: Amp Frontier Corporation (spun out of Sourcegraph, Dec 2, 2025) | **License**: Proprietary (closed source) | No-markup pricing for individuals: older claim, no longer stated on the pricing page (unverified)

## What It Is

Amp is a **multi-model agentic coding tool**, CLI-first and now also on web, desktop
and mobile with cloud "orbs" ([home][amp-home], checked 2026-11-26); the site
describes it as a "Coding agent and dev environment built for the frontier". Originally developed
at Sourcegraph as a successor to Cody, it spun out as an independent company
(Amp Frontier Corporation) on December 2, 2025, and the rebuilt Amp became available
to everyone on May 27, 2026 ([news][amp-news]).

The tool runs in the terminal (CLI package `@sourcegraph/amp`), syncs threads
across web and mobile, and exposes editor plugins for Neovim ([amp.nvim][amp-nvim])
and an examples-and-guides repository. It is **not open source**; no source code
or license terms are published. The CLI is distributed as an npm package under the
`@sourcegraph` scope.

**Key distinction vs OSS peers** (Aider, OpenCode, Kilo Code): Amp passed
through model costs with zero markup for individuals (older claim, no longer on the pricing page; unverified), making it cheaper than
fixed-subscription tools for low-to-moderate usage, but it is fully proprietary
and cloud-dependent for credit management.

## How It Works

### Architecture and modes

Amp runs as a CLI agent (`amp`) that orchestrates LLM calls, file edits, shell
commands, and web search in persistent "threads" that sync across devices. Since July 9, 2026
("The Dial") four modes select models: **low**, **medium**, **high** and **ultra**; the
earlier smart, deep, rush and large modes are deprecated ([news][amp-news], checked 2026-11-26).

| Mode | Model (checked 2026-11-26) |
|---|---|
| **ultra** | Claude Fable 5.1 (since 2026-09-01) |
| **medium** | Claude Opus 5.5 (since 2026-09-28) |
| **low**, **high** | not checked |

Historical (deprecated modes): deep and rush start 87% faster and finish 32% faster
(June 5, 2026, [news][amp-news]); smart was Claude Opus 4.8, deep GPT-5.5, rush a
fast GPT-5.5 variant (as of 2026-06-16).

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

The [pricing page][amp-pricing] (checked 2026-11-26) lists Hobby (free, with free
self-hosted orbs and runners and pay-as-you-go Amp-hosted orbs), Individual at $20/mo
(shown with the Megawatt and Gigawatt plans), Teams (no extra charge, pooled credits) and
Enterprise (custom). Students and teachers get Megawatt for $10/mo. The [news][amp-news]
records monthly subscriptions (2026-07-18) and free use with your own compute and model
keys or subscriptions (2026-09-13).

The older terms below are no longer stated on the pricing page and are unverified:
zero markup for individuals, a $5 minimum credit purchase, credit expiry after one year
of inactivity, an Enterprise 50% premium and a one-time $1,000 activation purchase.
Execute mode (`-x`) was described as consuming credits (unverified).

A **Frontier** offer ($10/day limit for any mode, free; announced Jan 8, 2026 as "The
Frontier Is Now Free") preceded the current model; when it ended is not stated in the news.

## Adoption Decision

| Dimension | Assessment |
|---|---|
| **Use case** | Terminal agent + CI/CD headless mode; peer to Claude Code, Copilot CLI, Codex CLI |
| **Model flexibility** | Multi-provider (Anthropic + OpenAI); mode-based auto-selection |
| **Extensibility** | Model Context Protocol (MCP), TypeScript plugins, AGENTS.md, Python/TypeScript SDKs |
| **Headless** | Yes — `amp -x` + `--stream-json` for scripted/CI use |
| **Maturity** | Public availability May 27, 2026; active weekly releases |
| **License** | **Proprietary** — no source, no self-hosting |
| **Cost** | Tiered plans (Hobby free, Individual $20/mo, Teams, Enterprise custom; checked 2026-11-26); older zero-markup, $1k activation and $5 minimum terms unverified |
| **Vendor** | Amp Frontier Corporation (independent since Dec 2025, ex-Sourcegraph) |

**Strengths**: Free use with your own model keys or subscriptions (per the news, 2026-09-13) suits teams
that already pay for Anthropic/OpenAI API access. AGENTS.md compatibility aligns
with Claude Code conventions — lower config friction in mixed shops. Headless
execute mode and JSON streaming make it scriptable for CI. Multi-model routing
avoids single-provider lock-in at the tool level.

**Risks**: Fully proprietary with no self-hosting option — all credit management
is cloud-dependent. Spinoff trajectory (Sourcegraph → Amp Frontier Corporation,
Dec 2025) is recent; organizational stability unproven at enterprise scale. The
editor extension was discontinued on 2026-02-19 ([news][amp-news]); the Neovim plugin
remains. Enterprise pricing is custom and not published.

## Action Items

- **Pilot** execute mode (`amp -x`) in a CI workflow where pricing
  vs a fixed-subscription agent (Copilot CLI, Claude Code) is the key variable.
- **Validate** AGENTS.md portability: test whether codebase instruction files
  authored for Claude Code transfer without modification.
- **Monitor** editor integration: the editor extension was discontinued
  (2026-02-19); track the changelog for IDE connections.
- **Reassess** at 6 months post-GA (Nov 2026, now due) on organizational stability and
  whether enterprise pricing has stabilized.

## Cross-References

- [github-copilot-cli-analysis.md](../agents/github-copilot-cli-analysis.md) — proprietary peer with fixed subscription model; useful cost comparison baseline
- [CC-agentic-harness-patterns-analysis.md § Cross-Harness Matrix](../../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#cross-harness-matrix-checked-2026-11-15) — sandbox, permissions, hooks, skills, subagents and MCP side by side with the other harnesses

## Sources

| Source | Content |
|---|---|
| [ampcode.com home][amp-home] | Product description, model list, feature overview (accessed 2026-06-16) |
| [ampcode.com pricing][amp-pricing] | Plan tiers (checked 2026-11-26); older zero-markup, $1k activation and $5 minimum terms not on the page |
| [ampcode.com news][amp-news] | Spinoff date (Dec 2, 2025), public availability (May 27, 2026), changelog (accessed 2026-06-16) |
| [ampcode.com manual (CLI guide)][amp-manual-cli] | Install commands, execute mode, headless usage, CI/CD patterns (accessed 2026-06-16) |
| [amp-examples-and-guides repo][amp-examples] | Supplemental guides, 58 stars (checked 2026-11-26), JavaScript/Shell; confirms CLI-first design (accessed 2026-06-16) |
| [amp.nvim repo][amp-nvim] | Neovim plugin; only confirmed editor integration at time of writing (accessed 2026-06-16) |
| [Product Hunt listing][amp-ph] | Confirms Sourcegraph authorship; community reception (accessed 2026-06-16) |
| [Sourcegraph Wikipedia][sg-wiki] | Organizational background; Cody → Amp transition (accessed 2026-06-16) |

[amp-home]: https://ampcode.com/
[amp-pricing]: https://ampcode.com/pricing
[amp-news]: https://ampcode.com/news
[amp-manual-cli]: https://github.com/sourcegraph/amp-examples-and-guides/blob/main/guides/cli/README.md
[amp-examples]: https://github.com/ampcode/amp-examples-and-guides
[amp-nvim]: https://github.com/ampcode/amp.nvim
[amp-ph]: https://www.producthunt.com/products/amp-free
[sg-wiki]: https://en.wikipedia.org/wiki/Sourcegraph
