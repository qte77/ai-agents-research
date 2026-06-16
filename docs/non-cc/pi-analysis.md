---
title: Pi — Minimal Extensible AI Coding Agent CLI
source: https://pi.dev/
purpose: Evaluate Pi as an open-source terminal coding agent harness with multi-provider LLM support and extension-first architecture
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
platform_scope: [claude, openai, google, azure, bedrock, groq, mistral, ollama]
---

**Status**: Trial

## What It Is

[Pi][pi-home] is an open-source, MIT-licensed AI coding agent CLI built around a minimal, transparent
harness. Originally created by Mario Zechner (`@mariozechner`), the project moved to its long-term
home under [Earendil Inc.][pi-home] in May 2026, with npm packages republished under the
`@earendil-works` scope starting at v0.74.0 (accessed 2026-06-16).

Pi is the third named harness integrated by [Omnigent][omnigent-doc], alongside Claude Code and
Codex, confirming its standing as a peer-level coding agent in that ecosystem.

The monorepo ships three packages (as of v0.79.4, 2026-06-15, accessed 2026-06-16):

- **`@earendil-works/pi-coding-agent`** — interactive CLI for coding tasks
- **`@earendil-works/pi-agent-core`** — runtime handling tool-calling and state management
- **`@earendil-works/pi-ai`** — unified multi-provider LLM API

The GitHub repository (`earendil-works/pi`) had approximately 46,000 stars as of 2026-06-16.

## How It Works

Pi operates as a terminal-based agent loop. The core loop is deliberately minimal (described as
approximately 150 lines), leaving capabilities to the extension layer rather than embedding them
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

## Adoption Decision

Pi occupies a well-defined niche: a minimal, transparent, extension-first coding agent for
developers who want to own their toolchain rather than accept a feature-complete but opinionated
harness. With 46k GitHub stars, an MIT license, active release cadence (v0.79.4 on 2026-06-15),
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
| [Pi homepage][pi-home] | Feature overview, installation, pricing (MIT/free), 2026-06-16 |
| [earendil-works/pi GitHub][pi-gh] | Repository, license (MIT), star count (~46k), v0.79.4 release date 2026-06-15, accessed 2026-06-16 |
| [Pi new home announcement][pi-new-home] | Organizational move from @mariozechner to Earendil Inc., v0.74.0 transition, accessed 2026-06-16 |
| [pi-coding-agent PyPI][pi-pypi] | Separate community package by Ashutosh Sharma (MIT, v0.6.0 2026-06-12); distinct from earendil-works/pi |
| [omnigent-analysis.md][omnigent-doc] | Pi named as peer harness alongside Claude Code and Codex in Omnigent meta-harness |
| [DEV.to Pi overview][pi-devto] | Third-party overview of Pi architecture and extensibility |
| [Dan Saattrup Smart blog][pi-blog] | Practitioner writeup on Pi in Neovim workflow, 2026-06-02 |

[pi-home]: https://pi.dev/
[pi-gh]: https://github.com/earendil-works/pi
[pi-new-home]: https://pi.dev/news/2026/5/7/pi-has-a-new-home
[pi-pypi]: https://pypi.org/project/pi-coding-agent/
[omnigent-doc]: omnigent-analysis.md
[pi-devto]: https://dev.to/arshtechpro/pi-the-open-source-ai-coding-agent-you-probably-havent-tried-yet-2h0h
[pi-blog]: https://www.saattrupdan.com/posts/2026-06-02-agentic-coding-v3-pi
