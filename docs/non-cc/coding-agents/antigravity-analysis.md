---
title: Google Antigravity Analysis
source: https://antigravity.google/
purpose: Analysis of Google Antigravity as an agent-first IDE and agentic development platform announced at Google I/O 2026.
created: 2026-06-16
updated: 2026-11-26
validated_links_on: 2026-11-18
status: assess
---

## What It Is

Google Antigravity is an agentic development platform comprising a desktop IDE, CLI (`agy`), and SDK, with no published licence for the CLI (observed 2026-11-18). Announced at [Google I/O 2026][io-2026-blog], it positions itself as an "agent-first" environment built for multi-agent orchestration rather than single-turn AI code completion. It launched in public preview on 2025-11-18 (version 1.11.2, unverified). Per [Wikipedia][wiki] (third-party, checked 2026-11-26) the stable releases are Antigravity 2.0 at 2.31.0 (2026-11-09) and the IDE at 2.6.0 (2026-10-26); the install docs reference desktop v2.30.0+.

Antigravity is described as a heavily modified fork of Visual Studio Code, though some sources debate whether it derives from Windsurf. It replaces Google's open-source [Gemini CLI][gemini-cli-fossforce], which was sunset for non-enterprise users on 2026-06-18.

## How It Works

The platform centres on two views inside the desktop app:

- **Editor View** — standard IDE layout with an integrated agent sidebar
- **Manager View** — orchestrates multiple agents in parallel across workspaces; up to 5 parallel agents on the free tier (access date: 2026-06-16, per [Stackpick pricing][stackpick])

Key capabilities (sourced from [Google Codelabs][codelabs-getting-started] and [I/O blog][io-2026-blog], 2026-06-16):

- **Multi-agent orchestration** — dynamic subagents for parallelised workflows, scheduled background tasks
- **Artifact system** — agents emit verifiable deliverables (implementation plans, task lists, browser recordings) before executing; human review gate before action
- **Browser Subagent** — spins up a real Chrome instance, clicks UI elements, takes screenshots, and self-debugs visual failures
- **MCP integration** — local and remote Model Context Protocol (MCP) servers ground agents in external data systems
- **Skills system** — contextual knowledge packages loaded on demand via markdown + optional Python/Bash scripts
- **Model support** — primarily Gemini 3.1 Pro and Gemini 3.5 Flash; also supports Claude Sonnet 4.6, Claude Opus 4.6, and GPT-OSS-120B (per [Wikipedia][wiki], 2026-06-16; unverified). Wikipedia (2026-11-26) now lists Claude Opus and Sonnet 4.6 and 5.5, with 5.5 for paid Pro and Ultra subscribers and 4.6 slated for removal on 2026-11-02; the Gemini model names are unverified

The CLI (`agy`) provides a lightweight terminal interface for instant agent creation. The SDK exposes the same agent harness programmatically. An enterprise tier ("Antigravity in Gemini Enterprise Agent Platform") integrates with Google Cloud.

Platform support: 64-bit Windows 10+, macOS Monterey 12+, 64-bit Linux with glibc 2.28+.

## Antigravity CLI (`agy`): first-party docs, checked 2026-11-18

Facts below are from Antigravity's own docs unless marked. Gemini CLI's status and tier
reconciliation: [gemini-cli-analysis.md](gemini-cli-analysis.md).

| Aspect | Documented | Source |
|---|---|---|
| Replaces Gemini CLI | Announced 2026-05-19; written in Go; shares architecture with the 2.0 desktop app; keeps skills, hooks, subagents, extensions (now plugins) | [maintainer post][gcli-discussion] |
| Licence | Not stated in the docs read. The public repo [google-antigravity/antigravity-cli][agy-repo] holds README, CHANGELOG and examples; API reports no licence and no source (2026-11-18). Our inference: treat as proprietary until Google states a licence | [install docs][agy-install] (no licence text on the page), repo |
| Install | Quickstart: `curl` install script (macOS/Linux) or PowerShell script (Windows); binary `agy`, verify with `agy --version` | [getting started][agy-start] |
| Auth | Personal Google account via browser OAuth (keyring-cached; paste-code flow over SSH); Gemini API key (needs `"modelProvider": "gemini"` in the CLI `settings.json`; `GEMINI_API_KEY` alone has no effect); Application Default Credentials; Google Cloud project for Enterprise. Workspace accounts are not covered by Antigravity plans | [install docs][agy-install] |
| Resume | `/resume` picker, `agy -c` (latest conversation in the workspace), `agy --conversation <id>`; per-workspace cache under `~/.gemini/antigravity-cli/` | [resume][agy-resume] |
| Sandbox | OS-level terminal sandbox (Linux namespaces, macOS Seatbelt, Windows AppContainer); CLI default `enableTerminalSandbox` is off, `--sandbox` or `--mode=auto` turns it on; default permission mode is request-review | [sandbox][agy-sandbox] |
| Headless | `agy -p`; `--output-format text/json/stream-json`, `--json-schema`, `-c`/`--conversation`; unauthenticated headless runs exit with an error, so sign in once interactively or use an API key | [headless][agy-headless] |
| Migration | Context files `GEMINI.md`/`AGENTS.md` keep working; workspace skills move to `.agents/skills/`; MCP config moves to `mcp_config.json`; `agy plugin import gemini` converts extensions | [migration][agy-migration] |

Not verified: free-tier quota amounts (the install docs list Free, Pro and Ultra plans without
numbers) and any end date for Code Assist Standard/Enterprise Gemini CLI access.

## Adoption Decision

**Assess** — Antigravity was in public preview at the last first-party check, and pricing finalisation is unverified. The multi-agent orchestration, artifact-first workflow, and Browser Subagent are meaningfully differentiated from single-agent IDEs. However, several factors warrant caution:

- **Preview status** — preview label and paid-tier finalisation unverified against a first-party page; third-party sources list stable 2.x releases (checked 2026-11-26)
- **No published source or licence** (observed 2026-11-18) — replaces the open-source Gemini CLI; extensions continue as plugins (`agy plugin import gemini`)
- **Vendor lock-in** — deepest value requires Google AI Studio, Firebase, and Gemini ecosystem; cross-provider model support (Claude, GPT-OSS) partially mitigates this
- **Pricing trajectory** — what FOSS Force calls a bait-and-switch, from open-source Gemini CLI to proprietary Antigravity, combined with opaque credit structures, signals pricing risk (per [FOSS Force][fossforce])

For teams already invested in the Google Cloud/Firebase stack and comfortable with Gemini models, this warrants hands-on evaluation. For teams prioritising open tooling or multi-cloud neutrality, wait for stable pricing (status unverified).

## Action Items

- [ ] Re-evaluate once GA status is confirmed (track [antigravity.google][antigravity])
- [ ] Benchmark Browser Subagent against Playwright-based agents for UI verification workflows
- [ ] Assess Antigravity SDK against the existing agent harness if MCP integration is a priority
- [ ] Monitor pricing finalisation — free tier rate limits refresh every ~5 hours; paid tiers under active change (access date: 2026-06-16)
- [ ] Compare with [GitHub Copilot CLI](../agents/github-copilot-cli-analysis.md) for terminal-centric agentic workflows

## Goal Loop

Checked 2026-10-22 against the vendor's own docs; compared across agents in
[goal-loops-landscape.md](goal-loops-landscape.md).

Antigravity has `/goal`: "The goal ends only when the agent declares it complete or when you ask the agent to stop", and "there's no
iteration cap"; "Only one goal is active at a time in a conversation" ([goal command][goal-ag-goal]).
With no cap, set your own bound. A `Stop` hook can return `decision: "continue"` to re-enter the
execution loop ([hooks][goal-ag-hooks]).

## Sources

| Source | Content |
|---|---|
| [Google I/O 2026 developer highlights][io-2026-blog] | Official announcement, feature list, SDK and CLI details |
| [Google Codelabs — Getting Started with Antigravity][codelabs-getting-started] | Platform architecture, MCP, skills, permissions model |
| [Wikipedia — Google Antigravity][wiki] | Version history, license, platform support, model support |
| [Stackpick — Antigravity Pricing][stackpick] | Free tier details, parallel agent limits, paid tier ranges |
| [FOSS Force — Gemini CLI sunset][fossforce] | Open-source context, Gemini CLI deprecation, proprietary concerns |
| [GitHub Discussion #27274][gcli-discussion] | Maintainer announcement of the Gemini CLI replacement (2026-05-19) |
| [Antigravity CLI docs][agy-start] | Install, auth, resume, sandbox, headless, migration (2026-11-18) |
| [antigravity.google][antigravity] | Official product page (minimal content; JavaScript-rendered, 2026-06-16) |

[io-2026-blog]: https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights/
[codelabs-getting-started]: https://codelabs.developers.google.com/getting-started-google-antigravity
[wiki]: https://en.wikipedia.org/wiki/Google_Antigravity
[stackpick]: https://stackpick.net/pricing/google-antigravity/
[fossforce]: https://fossforce.com/2026/05/gemini-clis-short-life-and-googles-antigravity-bait-and-switch/
[antigravity]: https://antigravity.google/
[gemini-cli-fossforce]: https://fossforce.com/2026/05/gemini-clis-short-life-and-googles-antigravity-bait-and-switch/
[gcli-discussion]: https://github.com/google-gemini/gemini-cli/discussions/27274
[agy-repo]: https://github.com/google-antigravity/antigravity-cli
[agy-start]: https://antigravity.google/docs/getting-started
[agy-install]: https://antigravity.google/docs/install?tab=cli
[agy-resume]: https://antigravity.google/docs/cli/commands/resume/
[agy-sandbox]: https://antigravity.google/docs/sandbox/
[agy-headless]: https://antigravity.google/docs/cli/headless/
[agy-migration]: https://antigravity.google/docs/cli/gcli-migration/
[goal-ag-goal]: https://antigravity.google/docs/commands/goal/
[goal-ag-hooks]: https://antigravity.google/docs/hooks
