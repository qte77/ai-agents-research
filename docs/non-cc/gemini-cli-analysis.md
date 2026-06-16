---
title: Gemini CLI Analysis
source: https://github.com/google-gemini/gemini-cli
purpose: Analysis of Gemini CLI as Google's open-source terminal AI agent, now deprecated for non-enterprise users.
platform_scope: [cli]
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
---

**Status**: Hold

## What It Is

Gemini CLI was Google's **open-source terminal AI agent**, launched on June 25,
2025 under the Apache 2.0 license. Built in TypeScript, it brought Gemini 2.5 Pro
(1M token context window) directly into the command line, competing with
[GitHub Copilot CLI][copilot-cli-analysis] and Anthropic's Claude Code.

**Critical status change (as of 2026-06-16):** On May 19, 2026, Google announced
that Gemini CLI would stop serving requests for free-tier users, Google AI Pro
subscribers, and Google AI Ultra subscribers on **June 18, 2026** — one day after
this analysis was written. Only Gemini Code Assist Standard and Enterprise
subscribers retain access. Non-enterprise users are directed to migrate to
[Antigravity CLI][antigravity-discussion], Google's closed-source replacement.
This renders the project effectively an archive for the vast majority of its
100,000+ GitHub-star community.

The Apache 2.0 repository remains public and maintained for enterprise customers,
but without Google's backend serving requests, it is not independently operable by
community users.

## How It Works

### Architecture and model access

Gemini CLI is a TypeScript application (98.1% of codebase per GitHub language
breakdown, accessed 2026-06-16). It connects to Google's Gemini models via three
authentication pathways:

| Auth method | User tier | Free quota |
|---|---|---|
| Google OAuth (personal account) | Free / Pro / Ultra | 60 req/min, 1,000 req/day |
| Gemini API key (Google AI Studio) | Free / paid | 1,000 req/day (free tier) |
| Vertex AI credentials | Enterprise | Usage-based billing |

All three pathways accessed Gemini 2.5 Pro with a 1M token context window.
[Pricing and quota data from Google's official blog post, accessed 2026-06-16.][blog]

### Built-in tools

Gemini CLI exposed three built-in tool categories to the agent loop:

- **File system operations** — read, write, and edit files in the working
  directory
- **Shell commands** — execute arbitrary shell commands within a trusted-folder
  policy
- **Web fetch and Google Search grounding** — fetch URLs and ground responses
  with real-time Search results

Extensibility was provided via [Model Context Protocol (MCP)][gemini-cli-repo]
server support, configured in `~/.gemini/settings.json`.

### Context and memory

Project-specific behavior was customizable via `GEMINI.md` files (analogous to
`CLAUDE.md` in Claude Code), loaded at session start to inject system-level
instructions. Conversation checkpointing and token caching were also supported.

### Headless / scripting mode

Non-interactive use was first-class:

- `-p <prompt>` — single-shot text response
- `--output-format json` — structured JSON output
- `--output-format stream-json` — newline-delimited streaming JSON

This made Gemini CLI viable for CI pipelines and scripted automation.

### Release cadence

Active development produced three release channels (data from GitHub releases
page, accessed 2026-06-16):

| Channel | Cadence | Example |
|---|---|---|
| Stable | Weekly (Tuesdays 20:00 UTC) | v0.46.0 (2026-06-10) |
| Preview | Weekly (Tuesdays 23:59 UTC) | v0.47.0-preview.0 |
| Nightly | Daily (00:00 UTC) | v0.48.0-nightly.20260613.g9e5599c32 |

Latest stable at time of writing: **v0.46.0** (2026-06-10).

## Adoption Decision

**Hold** — the free-tier and prosumer access model that made Gemini CLI
compelling ends June 18, 2026. Evaluation should be redirected to Antigravity CLI
for Google-ecosystem teams, or to Claude Code / GitHub Copilot CLI for
non-Google-locked alternatives.

Key factors:

| Factor | Assessment |
|---|---|
| License | Apache 2.0 (open source, but backend-dependent) |
| Free tier | Ends June 18, 2026 for non-enterprise |
| Enterprise path | Gemini Code Assist Standard/Enterprise only |
| Replacement | Antigravity CLI (closed-source, Go) |
| Community | 100,000+ stars, 6,000+ merged PRs — now effectively archived |
| Headless | Yes — `-p`, `--output-format json/stream-json` flags |
| MCP support | Yes — `~/.gemini/settings.json` |

The Apache 2.0 license technically permits forks, but without Google's model
backend the CLI is inoperable as-is. Community forks rewiring to an alternative
Gemini-compatible backend are possible but not currently documented.

**Compare:** [GitHub Copilot CLI][copilot-cli-analysis] (proprietary, active,
subscription-gated) offers a similar terminal agent model with continued access
guarantees for paying users.

## Action Items

- Track whether the community produces a fork with an alternative backend (e.g.,
  wired to a self-hosted or third-party Gemini-compatible endpoint)
- Evaluate Antigravity CLI when first-party documentation matures; note it is
  currently closed-source
- For Google-ecosystem organizations with Gemini Code Assist Enterprise licenses,
  Gemini CLI v0.46.0 remains the current stable version through the enterprise
  support window

## Sources

| Source | Content |
|---|---|
| [google-gemini/gemini-cli (GitHub)][gemini-cli-repo] | Repository, README, release history, star/fork counts — accessed 2026-06-16 |
| [Google blog: Introducing Gemini CLI][blog] | Launch announcement (2025-06-25): license, model, free quota, preview status |
| [Gemini Code Assist FAQs][gcfa-faqs] | Official June 18, 2026 shutdown announcement; affected tiers; Antigravity migration |
| [GitHub Discussion #27274: Transitioning to Antigravity CLI][antigravity-discussion] | Official Google deprecation notice; Antigravity CLI feature summary |
| [TechTimes: Google Accepted 6,000 Gemini CLI Contributions][techtimes] | Third-party reporting on access restriction announcement (2026-05-23) |

[gemini-cli-repo]: https://github.com/google-gemini/gemini-cli
[blog]: https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/
[gcfa-faqs]: https://developers.google.com/gemini-code-assist/resources/faqs
[antigravity-discussion]: https://github.com/google-gemini/gemini-cli/discussions/27274
[techtimes]: https://www.techtimes.com/articles/317056/20260523/google-accepted-6000-gemini-cli-contributions-then-closed-tool-enterprise-only.htm
[copilot-cli-analysis]: github-copilot-cli-analysis.md
