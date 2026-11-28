---
title: Pi — Minimal Extensible AI Coding Agent CLI
source: https://pi.dev/
purpose: Evaluate Pi as an open-source terminal coding agent harness with multi-provider LLM support and extension-first architecture
created: 2026-06-16
updated: 2026-11-28
validated_links_on: 2026-09-24
status: trial
---

**Details:**. Also runs on or integrates with: `claude`, `openai`, `google`, `azure`, `bedrock`, `groq`, `mistral`, `ollama`.

## What It Is

[Pi][pi-home] is an open-source, MIT-licensed AI coding agent CLI built around a minimal, transparent
harness. Originally created by Mario Zechner (`@mariozechner`), the project moved to its long-term
home under [Earendil Inc.][pi-home] in May 2026, with npm packages republished under the
`@earendil-works` scope starting at v0.74.0 (accessed 2026-06-16).

Pi is the third named harness integrated by [Omnigent][omnigent-doc], alongside Claude Code and
Codex, confirming its standing as a peer-level coding agent in that ecosystem.

The monorepo's `packages/` directory now lists 12 directories (agent, ai, chord, codemode, coding-agent, durable, env, evals, mcp, schema, telemetry, tui; checked 2026-11-26; directory names are not confirmed to equal npm package names); latest release v1.6.1, 2026-11-25, via `gh api`. Three core packages, as of v0.79.4 (2026-06-15):

- **`@earendil-works/pi-coding-agent`** — interactive CLI for coding tasks
- **`@earendil-works/pi-agent-core`** — runtime handling tool-calling and state management
- **`@earendil-works/pi-ai`** — unified multi-provider LLM API

The GitHub repository (`earendil-works/pi`) has approximately 124,000 stars and 16,000 forks as of 2026-11-26 (about 46,000 stars on 2026-06-16).

## How It Works

Pi operates as a terminal-based agent loop. The core loop is deliberately minimal (described as
approximately 150 lines; unverified, pi.dev says only that the system prompt is minimal), leaving capabilities to the extension layer rather than embedding them
in the core.

**Operational modes** (per [pi.dev][pi-home], accessed 2026-06-16):

- Interactive TUI
- Print/JSON output (for scripting)
- RPC protocol
- SDK embedding

**Multi-provider LLM support**: 15+ providers including Anthropic, OpenAI, Google, Azure, Bedrock,
Mistral, Groq, Cerebras, xAI, Hugging Face, Ollama, and OpenRouter. Users can switch models
mid-session.

**Extensibility primitives**: Extensions (TypeScript modules) add tools, slash commands, event
handlers, and custom UI. Skills loaded from `~/.pi/agent/skills/` provide specialized
instructions. Features like sub-agent delegation, permission gates, and planning are built as
extensions rather than built-ins.

**Session model**: Tree-structured history with branching; sessions can be exported to HTML or
shared via GitHub Gist.

**Context engineering**: Supports project-specific `AGENTS.md` and `SYSTEM.md` for instructions,
with auto-compaction for context management.

**Installation** (accessed 2026-06-16):

```bash
curl -fsSL https://pi.dev/install.sh | sh
# or
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

## Fork: omp (oh-my-pi)

[`can1357/oh-my-pi`][omp-gh] ("omp") is a fork of Pi built by Stencil Labs (Can Bölük), described
in its own README as "the most capable agent surface that ships... complete out of the box, open
all the way down" (accessed 2026-09-24). It keeps Pi's core vision but adds substantial production
tooling on top: **60+ LLM providers, 31 built-in tools, 14 LSP operations, and 28 DAP (debugger)
operations**, plus "~80k lines of Rust core" — the README's own figure, confirming the project has
grown well beyond a thin TypeScript wrapper around Pi. IDE-adjacent features include LSP-driven
renames that propagate through re-exports and barrel files, a real debugger backend (`lldb`,
`dlv`, `debugpy`), subagent fan-out with typed schema validation, persistent Python/Bun execution
kernels, memory/skills persisted across sessions, and live session sharing (`omp join` or a
browser link with a QR code).

**Repository facts** (`gh api repos/can1357/oh-my-pi`, checked 2026-11-26): 39,946 stars, 4,640
forks, **MIT** license, latest tagged release `v19.2.1` (published 2026-11-25) — substantial
traction for a fork (Pi itself has ~124k stars, per the Sources above), and the omp repository's
push history shows continuous daily activity.

**Installation** (accessed 2026-09-24):

```bash
curl -fsSL https://omp.sh/install | sh          # macOS/Linux
bun install -g @oh-my-pi/pi-coding-agent        # via Bun (recommended by the README)
brew install can1357/tap/omp                    # Homebrew
irm https://omp.sh/install.ps1 | iex             # Windows PowerShell
```

**Homepage vs. repo framing.** The [omp.sh][omp-site] landing page separately markets an "omp²"
positioning — a "native Rust core" with Windows-native support requiring no WSL (unverified) — which is
consistent with, but more forward-leaning than, the GitHub README's own "~80k lines of Rust core"
figure and its plain PowerShell/Windows install path. This doc describes the GitHub-repo-documented
`v19.2.1` release; the omp.sh page's headline reads "omp², soon!", so omp² is presented as upcoming, not as a shipped version.

See the [Cross-Harness Matrix](../../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#cross-harness-matrix-checked-2026-11-15) for sandbox, permissions, hooks, skills, subagents and Model Context Protocol (MCP) side by side with the other harnesses.

## Adoption Decision

Pi occupies a well-defined niche: a minimal, transparent, extension-first coding agent for
developers who want to own their toolchain rather than accept a feature-complete but opinionated
harness. With 124k GitHub stars (checked 2026-11-26), an MIT license, active release cadence (v1.6.1 on 2026-11-25),
and first-class integration in [Omnigent][omnigent-doc], it has demonstrated community traction.

**For adoption in this project's context**: Pi is worth **Trial** status. Its multi-provider
flexibility (including Anthropic/Claude) and headless CLI modes make it a viable harness
alternative to Claude Code for scripted or multi-model workflows. The extension architecture
parallels CC's hooks/skills model but is more composable. The Omnigent integration path is the
clearest on-ramp for teams already evaluating that meta-harness.

Key unknowns: enterprise support status, sandboxing story, and security posture are not stated on
the first-party site (not stated, as of 2026-06-16).

## Action Items

- Evaluate Pi's extension/skill model against CC hooks: assess parity for the agentic patterns
  documented in this repo
- Track `earendil-works/pi` CHANGELOG for sub-agent and permission-gate extensions reaching
  stability
- Verify Omnigent's `--harness pi` flag behavior once Omnigent exits alpha (see
  [omnigent-analysis.md][omnigent-doc])

## Sources

| Source | Content |
|---|---|
| [Pi homepage][pi-home] | Feature overview, installation, license (MIT), 2026-06-16 |
| [earendil-works/pi GitHub][pi-gh] | Repository, license (MIT), star count (~124k), v1.6.1 release date 2026-11-25, checked 2026-11-26 |
| [Pi new home announcement][pi-new-home] | Organizational move from @mariozechner to Earendil Inc., v0.74.0 transition, accessed 2026-06-16 |
| [pi-coding-agent PyPI][pi-pypi] | Separate community package by Ashutosh Sharma (MIT, v0.6.0 2026-06-12); distinct from earendil-works/pi |
| [omnigent-analysis.md][omnigent-doc] | Pi named as peer harness alongside Claude Code and Codex in Omnigent meta-harness |
| [DEV.to Pi overview][pi-devto] | Third-party overview of Pi architecture and extensibility |
| [Dan Saattrup Smart blog][pi-blog] | Practitioner writeup on Pi in Neovim workflow, 2026-06-02 |
| [can1357/oh-my-pi README][omp-gh] | omp fork description, provider/tool/LSP/DAP counts, Rust-core line count, install commands, accessed 2026-09-24 |
| [omp.sh][omp-site] | Homepage "omp²" framing (Rust core, no-WSL Windows support) |
| `gh api repos/can1357/oh-my-pi` | Stars (39,946), forks (4,640), license (MIT), checked 2026-11-26 |
| `gh api repos/can1357/oh-my-pi/releases/latest` | Latest tag `v19.2.1`, published 2026-11-25 |

[pi-home]: https://pi.dev/
[pi-gh]: https://github.com/earendil-works/pi
[pi-new-home]: https://pi.dev/news/2026/5/7/pi-has-a-new-home
[pi-pypi]: https://pypi.org/project/pi-coding-agent/
[omnigent-doc]: ../orchestrators/omnigent-analysis.md
[pi-devto]: https://dev.to/arshtechpro/pi-the-open-source-ai-coding-agent-you-probably-havent-tried-yet-2h0h
[pi-blog]: https://www.saattrupdan.com/posts/2026-06-02-agentic-coding-v3-pi
[omp-gh]: https://github.com/can1357/oh-my-pi
[omp-site]: https://omp.sh
