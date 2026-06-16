---
title: Google Antigravity Analysis
source: https://antigravity.google/
purpose: Analysis of Google Antigravity as an agent-first IDE and agentic development platform announced at Google I/O 2026.
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
---

**Status**: Assess

## What It Is

Google Antigravity is a proprietary agentic development platform comprising a desktop IDE, CLI (`agy`), and SDK. Announced at [Google I/O 2026][io-2026-blog], it positions itself as an "agent-first" environment built for multi-agent orchestration rather than single-turn AI code completion. Version 1.11.2 launched in public preview on 2025-11-18; version 2.0.1 shipped 2026-05-19 and is the current preview release (access date: 2026-06-16, per [Wikipedia][wiki]).

Antigravity is described as a heavily modified fork of Visual Studio Code, though some sources debate whether it derives from Windsurf. It replaces Google's open-source [Gemini CLI][gemini-cli-fossforce], which is being sunset on 2026-06-18.

## How It Works

The platform centres on two views inside the desktop app:

- **Editor View** — standard IDE layout with an integrated agent sidebar
- **Manager View** — orchestrates multiple agents in parallel across workspaces; up to 5 parallel agents on the free tier (access date: 2026-06-16, per [Stackpick pricing][stackpick])

Key capabilities (sourced from [Google Codelabs][codelabs-getting-started] and [I/O blog][io-2026-blog], 2026-06-16):

- **Multi-agent orchestration** — dynamic subagents for parallelised workflows, scheduled background tasks
- **Artifact system** — agents emit verifiable deliverables (implementation plans, task lists, browser recordings) before executing; human review gate before action
- **Browser Subagent** — spins up a real Chrome instance, clicks UI elements, takes screenshots, and self-debugs visual failures
- **MCP integration** — local and remote MCP servers ground agents in external data systems
- **Skills system** — contextual knowledge packages loaded on demand via markdown + optional Python/Bash scripts
- **Model support** — primarily Gemini 3.1 Pro and Gemini 3.5 Flash; also supports Claude Sonnet 4.6, Claude Opus 4.6, and GPT-OSS-120B (per [Wikipedia][wiki], 2026-06-16)

The CLI (`agy`) provides a lightweight terminal interface for instant agent creation. The SDK exposes the same agent harness programmatically. An enterprise tier ("Antigravity in Gemini Enterprise Agent Platform") integrates with Google Cloud.

Platform support: 64-bit Windows 10+, macOS Monterey 12+, 64-bit Linux with glibc 2.28+.

## Adoption Decision

**Assess** — Antigravity is in public preview and pricing is not yet finalised. The multi-agent orchestration, artifact-first workflow, and Browser Subagent are meaningfully differentiated from single-agent IDEs. However, several factors warrant caution:

- **Preview status** — v2.0.1 is labelled preview; paid tiers are not finalised (access date: 2026-06-16)
- **Proprietary and closed-source** — replaces the open-source Gemini CLI; no community fork or extension path
- **Vendor lock-in** — deepest value requires Google AI Studio, Firebase, and Gemini ecosystem; cross-provider model support (Claude, GPT-OSS) partially mitigates this
- **Pricing trajectory** — the bait-and-switch from open-source Gemini CLI to proprietary Antigravity, combined with opaque credit structures, signals pricing risk ([FOSS Force][fossforce])

For teams already invested in the Google Cloud/Firebase stack and comfortable with Gemini models, this warrants hands-on evaluation. For teams prioritising open tooling or multi-cloud neutrality, wait for GA and stable pricing.

## Action Items

- [ ] Re-evaluate at GA (expected after preview period; track [antigravity.google][antigravity])
- [ ] Benchmark Browser Subagent against Playwright-based agents for UI verification workflows
- [ ] Assess Antigravity SDK against the existing agent harness if MCP integration is a priority
- [ ] Monitor pricing finalisation — free tier rate limits refresh every ~5 hours; paid tiers under active change (access date: 2026-06-16)
- [ ] Compare with [GitHub Copilot CLI](github-copilot-cli-analysis.md) for terminal-centric agentic workflows

## Sources

| Source | Content |
|---|---|
| [Google I/O 2026 developer highlights][io-2026-blog] | Official announcement, feature list, SDK and CLI details |
| [Google Codelabs — Getting Started with Antigravity][codelabs-getting-started] | Platform architecture, MCP, skills, permissions model |
| [Wikipedia — Google Antigravity][wiki] | Version history, license, platform support, model support |
| [Stackpick — Antigravity Pricing][stackpick] | Free tier details, parallel agent limits, paid tier ranges |
| [FOSS Force — Gemini CLI sunset][fossforce] | Open-source context, Gemini CLI deprecation, proprietary concerns |
| [antigravity.google][antigravity] | Official product page (minimal content; JavaScript-rendered, 2026-06-16) |

[io-2026-blog]: https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights/
[codelabs-getting-started]: https://codelabs.developers.google.com/getting-started-google-antigravity
[wiki]: https://en.wikipedia.org/wiki/Google_Antigravity
[stackpick]: https://stackpick.net/pricing/google-antigravity/
[fossforce]: https://fossforce.com/2026/05/gemini-clis-short-life-and-googles-antigravity-bait-and-switch/
[antigravity]: https://antigravity.google/
[gemini-cli-fossforce]: https://fossforce.com/2026/05/gemini-clis-short-life-and-googles-antigravity-bait-and-switch/
