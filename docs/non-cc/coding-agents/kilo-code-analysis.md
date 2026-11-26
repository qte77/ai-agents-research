---
title: Kilo Code Analysis
source: https://github.com/Kilo-Org/kilocode
purpose: Analysis of Kilo Code as an open-source agentic coding platform covering VS Code, JetBrains, CLI, and Cloud surfaces.
created: 2026-06-16
updated: 2026-11-26
validated_links_on: 2026-06-16
status: trial
---

**Details:** **License**: MIT (repo-confirmed; kilo.ai now also says MIT-licensed source, checked 2026-11-26) | **Version**: v7.8.32 (2026-11-20, checked 2026-11-26) | **Stars**: 28.1k (checked 2026-11-26). Also runs on or integrates with: `vscode`, `jetbrains`, `cli`, `cloud`, `slack`.

## What It Is

Kilo Code is an **open-source agentic engineering platform** — "the all-in-one
agentic engineering platform. Build, ship, and iterate faster with the most
popular open source coding agent." It started as a fork/successor of Roo Code
and ships as:

- A **VS Code extension** (`kilocode.kilo-code`, also on OpenVSX)
- A **JetBrains plugin** (IntelliJ, PyCharm, WebStorm)
- A **CLI** (`npm install -g @kilocode/cli`, or `npx @kilocode/cli`)
- **Cloud Agents** (hosted infrastructure; the KiloClaw name is unverified), plus Kilo Desktop and a mobile app per kilo.ai (checked 2026-11-26)
- A **Slack integration**

The core differentiator is breadth of model access — "500+ models, zero markup" (the earlier
60+ providers figure is unverified) via [Kilo Gateway][kilo-gateway] — combined with MIT-licensed
source availability and no per-seat markup on AI inference.

**Key distinction vs OSS peers**: Unlike [GitHub Copilot CLI][copilot-cli]
(proprietary, subscription-gated), Kilo Code is free to self-host with
bring-your-own-keys (BYOK), local models (Ollama), or free-tier hosted models.
The platform adds optional paid tiers for teams and gateway credits.

## How It Works

### Agent Modes

Five built-in modes (unverified against first-party docs) cover the full development loop:

| Mode | Purpose |
|---|---|
| **Code** | File writing, editing, and code generation from natural language |
| **Architect** | High-level planning and design across the codebase |
| **Debug** | Root-cause analysis and fix suggestions |
| **Ask** | Read-only Q&A over the codebase without file edits |
| **Custom** | User-defined modes for team-specific workflows |

Modes can be switched mid-session without losing context — "switch contexts
without switching tools."

### Model Access

Kilo Gateway provides routing to 500+ models at exact
provider rates with no markup (60+ providers: unverified). As of v7.3.46 (2026-06-15, historical; unverified), the supported
frontier models include GPT-5.5, Claude Opus 4.7, Claude Sonnet 4.6, and
Gemini 3.1 Pro Preview. BYOK and local model (Ollama) paths require no
gateway subscription.

### MCP Integration

The platform ships an MCP Server Marketplace (unverified) for extending agent capabilities.
Model Context Protocol (MCP) servers are configurable via the Automation section of the docs.

### CLI / Headless Mode

The CLI supports an `--auto` flag (unverified) for fully autonomous operation — no user
prompts, suitable for CI/CD pipelines. This makes the CLI path a viable
headless agent runner.

### v7.3.46 Notable Changes (2026-06-15, historical)

- Model-specific reasoning overrides for task subagents (custom subagents can
  carry their own model and variant settings)
- Ability to disable reasoning on custom-provider models post-activation
- Question response routing to the correct worktree
- Prevention of recursive directory deletion during skill removal

## Adoption Decision

**Trial** — Kilo Code is a mature, actively maintained open-source coding
agent (28k+ stars, v7.8.x, frequent releases; checked 2026-11-26) with broad platform coverage and
zero inference markup. The MIT license and BYOK/local-model support eliminate
vendor lock-in. Trial is appropriate rather than Adopt because:

1. The rapid release cadence (multiple patch releases per day) indicates
   active but potentially unstable surface area.
2. The earlier kilo.ai Apache-2.0 vs repo MIT discrepancy is resolved: kilo.ai now says MIT-licensed source (checked 2026-11-26).
3. JetBrains and Cloud/Slack surfaces are newer and less battle-tested than
   the VS Code extension.

For teams already using VS Code and managing their own LLM API keys, the
free-tier + BYOK path is immediately low-risk to trial.

## Action Items

- [ ] Evaluate headless CLI (`--auto`) in a CI/CD pipeline for automated
  code-review or refactoring tasks.
- [ ] Compare Custom modes against team-specific Roo Code profiles to assess
  migration cost if the team currently uses Roo Code.
- [ ] Validate JetBrains plugin stability on target IDEs before rolling out
  to non-VS Code users.

## Sources

| Source | Content |
|---|---|
| [GitHub: Kilo-Org/kilocode][gh-repo] | Repo description, README, star count, license, version (checked 2026-11-26) |
| [kilo.ai][kilo-ai] | Feature overview, platform listing, pricing, model count (2026-06-16) |
| [kilo.ai/pricing][kilo-pricing] | Free, Teams, Enterprise, Kilo Gateway, Kilo Pass tiers (2026-06-16) |
| [GitHub Release v7.8.32][release] | Latest release, 2026-11-20 (the v7.3.46 notes above are historical) |
| [package.json (MIT license)][pkg-json] | License field = MIT, version = 7.3.46 (2026-06-16, historical) |

[gh-repo]: https://github.com/Kilo-Org/kilocode
[kilo-ai]: https://kilo.ai/
[kilo-pricing]: https://kilo.ai/pricing
[kilo-gateway]: https://kilo.ai/docs
[release]: https://github.com/Kilo-Org/kilocode/releases/tag/v7.8.32
[pkg-json]: https://github.com/Kilo-Org/kilocode/blob/main/package.json
[copilot-cli]: ../agents/github-copilot-cli-analysis.md
