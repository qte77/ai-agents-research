---
title: Cline — Autonomous Coding Agent (VS Code, CLI, SDK)
source: https://github.com/cline/cline
purpose: Evaluate Cline as an open-source autonomous coding agent for IDE, CLI, and CI/CD use cases.
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
platform_scope: [vscode, jetbrains, cursor, windsurf, cli, sdk]
---

**Status**: Adopt

## What It Is

[Cline][cline-gh] is an open-source autonomous coding agent by Cline Bot Inc., available as a VS Code extension, JetBrains plugin (early access as of 2026-06-16), CLI tool, and embeddable SDK. It operates with a plan-and-act loop: the agent proposes a strategy for human review, then executes edits, shell commands, and browser actions with approval checkpoints at each step. The project has 63.4k GitHub stars and 4.3M+ VS Code installs (VS Marketplace, 2026-06-08) and is released under the [Apache 2.0 license][license].

## How It Works

**Core loop.** Cline runs in two phases: *Plan* (explore the codebase, clarify intent) and *Act* (make changes). Each destructive action — file edit, shell command, browser call — presents a diff or preview for human approval before executing. An auto-approval toggle enables fully autonomous operation for CI/CD pipelines.

**File and shell operations.** The agent reads directory trees, creates and edits files with coordinated multi-file changes, monitors linter and compiler output, and runs bash commands with live stdout reaction. Checkpoint/undo rolls back groups of edits.

**Browser automation.** Built-in browser tool enables the agent to click, type, and screenshot for UI testing and web research without leaving the task session.

**Model providers.** Cline is provider-agnostic with BYOK (bring your own key): Anthropic (Claude Opus/Sonnet/Haiku), OpenAI, Google Gemini, AWS Bedrock, Azure, GCP Vertex, OpenRouter (200+ models), Groq, Cerebras, Vercel AI Gateway, DeepSeek, Ollama, LM Studio, and any OpenAI-compatible endpoint (github.com/cline/cline, 2026-06-16).

**MCP extensibility.** Cline connects to MCP servers to query databases, call external APIs, and manage cloud infrastructure. Custom tools are registerable via the SDK.

**Project rules.** `.clinerules` files encode coding standards and architecture guidance, scoped per project, giving teams a lightweight way to enforce conventions without baking them into prompts.

**Multi-agent and scheduling.** A kanban-style task board (separate repo) orchestrates specialist agents in dependency chains. Cron-based scheduling enables recurring autonomous runs. Messaging integrations (Slack, Telegram, Discord, Linear) route task notifications and approvals.

**Headless / CLI.** `npm i -g cline` installs the CLI. The GitHub README explicitly documents "Run Cline with zero interaction for scripting and automation," making it a first-class headless agent (2026-06-16). Latest CLI release: v3.0.24 (2026-06-11).

**VS Code extension.** Listed as `saoudrizwan.claude-dev` on the VS Marketplace; version 3.89.2 as of 2026-06-08, rated 4/5 from 293 reviews.

**Pricing.** The extension and CLI are free (Apache 2.0). Users pay only for AI inference at cost or via their own API keys — no seat fees or subscriptions. Enterprise plan (custom pricing, contact sales) adds SSO/OIDC, SLA, centralized billing, RBAC, and authentication logging ([cline.bot/pricing][pricing], 2026-06-16).

## Adoption Decision

Cline warrants **Adopt** based on:

- **Production maturity**: 63.4k stars, 4.3M VS Code installs, and active release cadence (v3.89.2 as of June 2026) indicate broad real-world use.
- **Open-source governance**: Apache 2.0 with no vendor lock-in; all model providers are BYOK.
- **First-class headless support**: CLI and CI/CD integration are documented and shipped, not afterthoughts — relevant alongside [GitHub Copilot CLI][copilot-cli-doc].
- **MCP ecosystem**: Native MCP support aligns with the direction of agentic tool extensibility in this research corpus.
- **Low switching cost**: Provider-agnostic design means the agent can run against any model, including self-hosted options via Ollama.

Considerations: JetBrains support is early access. Enterprise features (fine-grained permissions, advanced config management) are listed as "coming soon" (2026-06-16). Inference cost is the user's responsibility under BYOK.

## Action Items

- Benchmark plan-and-act latency against comparable agents on a representative codebase task.
- Evaluate `.clinerules` as a mechanism for encoding project conventions — compare with CLAUDE.md patterns tracked in `cc-community/`.
- Monitor JetBrains plugin GA timeline.
- Assess multi-agent kanban board for orchestration use cases once the separate repo stabilizes.

## Sources

| Source | Content |
|---|---|
| [cline/cline GitHub][cline-gh] | Repo description, license, star count, feature list, provider matrix, headless docs; accessed 2026-06-16 |
| [cline.bot][cline-website] | Product overview, deployment options, 8M+ installs claim; accessed 2026-06-16 |
| [cline.bot/pricing][pricing] | Free/Enterprise plan details, BYOK model, inference-cost-only pricing; accessed 2026-06-16 |
| [VS Marketplace — saoudrizwan.claude-dev][vscode-marketplace] | Version 3.89.2, 4.3M installs, 4/5 rating, last updated 2026-06-08; accessed 2026-06-16 |
| [CLI release v3.0.24][cli-release] | Latest CLI tag, release date 2026-06-11, changelog summary; accessed 2026-06-16 |

[cline-gh]: https://github.com/cline/cline
[cline-website]: https://cline.bot/
[pricing]: https://cline.bot/pricing
[vscode-marketplace]: https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev
[cli-release]: https://github.com/cline/cline/releases/tag/cli-v3.0.24
[license]: https://github.com/cline/cline/blob/main/LICENSE
[copilot-cli-doc]: github-copilot-cli-analysis.md
