---
title: Zed Editor (Agent Panel, ACP host) Analysis
source: https://github.com/zed-industries/zed
purpose: Analysis of the Zed editor as an agent host — its own Zed Agent, external agents such as Claude Agent over the Agent Client Protocol (ACP), and agent CLIs in terminal threads.
platform_scope: [zed, claude-code, codex, opencode, copilot, cursor, pi, gemini-cli]
created: 2026-11-09
updated: 2026-11-09
validated_links: 2026-11-09
status: assess
---

**Details:** GPL-3.0-or-later with Apache-2.0 components; v1.27.0 (2026-11-04); read 2026-11-09.

## What It Is

Zed is a Rust code editor from Zed Industries. Its README calls it "a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter". For this corpus it matters as an **agent host**: it runs its own agent, it runs other vendors' agents (Claude Code's SDK among them) over the [Agent Client Protocol][acp-repo] (ACP), and it runs plain agent CLIs in terminal-backed threads. ACP "standardizes communication between _code editors_ … and _coding agents_" ([ACP README][acp-repo]), and the spec repo started in Zed's org (`zed-industries/agent-client-protocol` now redirects to it, checked 2026-11-09).

**License:** the repo root holds `LICENSE-GPL` and `LICENSE-APACHE`; the README says the source "is licensed primarily under GPL-3.0-or-later, with Apache-2.0 components where marked". That mix is why the GitHub API reports `NOASSERTION`.

## How Agents Run in Zed

The [AI overview][zed-ai-overview] lists three ways to run agentic work:

| Mode | What it is | Who owns model, auth, billing |
|---|---|---|
| **Zed Agent** | Zed's native agent, using models configured in Zed (Zed-hosted, provider API keys, gateways, local) | Zed |
| **External Agents** | "ACP-integrated agents that run through their own process and configuration" | The agent ("Usually owned by the External Agent") |
| **Terminal Threads** | "terminal-backed threads for running an agent CLI or TUI directly in Zed" | The CLI itself |

Several threads of any mode can run at once from the Threads Sidebar, each with a different agent.

### External agents and the ACP Registry

[External agents][zed-external] are installed from the **ACP Registry**, which Zed calls "the primary way to install common External Agents". The curated list names Claude, Codex, OpenCode, Copilot, Cursor and Pi Coding Agent; the same page also documents Gemini CLI and Poolside, and any ACP agent can be added as a custom `agent_servers` entry. Extension-provided agents are deprecated and migrate to their registry equivalents. "Zed does not charge for External Agents."

ACP draws a configuration boundary. Per the [external-agents page][zed-external]:

| Capability | In an External Agent thread |
|---|---|
| Zed Agent profiles | "Do not apply unless the integration says otherwise" |
| Zed Skills | "Do not apply as Zed Skills" |
| Zed MCP servers | "May be forwarded over ACP" |
| Tool permissions | "Zed ACP/tool forwarding permissions may apply; native tool permissions depend on the agent" |

### Claude Code in Zed

There are two routes:

1. **Claude Agent (External Agent).** Installed from the ACP Registry. It "owns its own authentication and billing"; an Anthropic key set for Zed Agent does not configure it. `/login` authenticates "with an API key or with Claude Code where supported", and `CLAUDE.md` "may be read by Claude Agent directly". The adapter is [`agentclientprotocol/claude-agent-acp`][claude-agent-acp] (formerly `zed-industries/claude-code-acp`), described as "Use Claude Agent SDK from any ACP client" (Apache-2.0, v0.101.0, 2026-11-05). So Zed drives the **Claude Agent SDK** through ACP, not the `claude` terminal UI. Which Claude Code features (hooks, slash commands, plan mode) survive that path is not documented on the page and is unverified here.
2. **Terminal Thread.** The `claude` CLI runs unchanged in a terminal that Zed "organizes as a thread" ([terminal threads][zed-terminal]). This keeps the full CLI feature set but gives up ACP's rendered thread and MCP forwarding.

Cross-ref: Claude Code's own IDE protocol (the VS Code and JetBrains extensions) is in [CC-ide-integration-protocol.md](../../cc-native/configuration/CC-ide-integration-protocol.md).

## Agent Client Protocol (ACP)

ACP now lives in its own GitHub org (moved from `zed-industries`), [`agentclientprotocol/agent-client-protocol`][acp-repo] (Apache-2.0). Its README states: "The current stable ACP protocol version is `1`." Wire compatibility is negotiated through `protocolVersion` at `initialize`, separately from the Rust crate and JSON Schema release numbers. Official SDKs exist for Kotlin, Java, Python, Rust and TypeScript.

Other ACP implementations covered in this corpus: [Goose](../agents/goose-analysis.md#acp-agent-client-protocol) (client and server), opencode (its v1.17.7 release added an ACP shell, see [opencode-analysis.md](opencode-analysis.md)), and the ACP notes in [kimi-code-analysis.md](kimi-code-analysis.md) and [windsurf-analysis.md](windsurf-analysis.md).

## Edit Predictions

The default inline-completion provider is Zeta, which the [edit-prediction docs][zed-edit-prediction] describe as "an open source model developed by Zed". Zeta predictions are included with Zed Pro, the Pro trial and the Student plan. GitHub Copilot, Codestral, Mercury Coder and local or OpenAI-compatible endpoints are the alternatives. The license of the Zeta weights was not checked here.

## Adoption Decision

**Assess.** Zed is the most complete ACP host and a working non-terminal way to run Claude Code (via the Agent SDK). Two gaps keep it at assess for a Claude Code-centred workflow: the ACP path's Claude Code feature coverage is undocumented, and Zed's own profiles and skills stop at the ACP boundary, so configuration splits between Zed and each agent.

## Sources

| Source | Content |
|---|---|
| [zed-industries/zed][zed-repo] | README (description, Licensing), root license files, v1.27.0 release (2026-11-04); `gh api` 2026-11-09 |
| [Zed AI overview][zed-ai-overview] | Three agent modes, Threads Sidebar |
| [Zed external agents][zed-external] | ACP Registry, curated agent list, Claude Agent auth/billing, ACP configuration boundary |
| [Zed terminal threads][zed-terminal] | Agent CLIs in terminal-backed threads |
| [Zed edit prediction][zed-edit-prediction] | Zeta default, plan inclusion, alternative providers |
| [agentclientprotocol/claude-agent-acp][claude-agent-acp] | Claude Agent SDK adapter for ACP (Apache-2.0, v0.101.0, 2026-11-05) |
| [agentclientprotocol/agent-client-protocol][acp-repo] | ACP spec repo: stable protocol version 1, versioning rules, SDK list |

Docs pages were read from the `docs/src/ai/` sources in the Zed repo on 2026-11-09; the links point to their published versions.

[zed-repo]: https://github.com/zed-industries/zed
[zed-ai-overview]: https://zed.dev/docs/ai/overview
[zed-external]: https://zed.dev/docs/ai/external-agents
[zed-terminal]: https://zed.dev/docs/ai/terminal-threads
[zed-edit-prediction]: https://zed.dev/docs/ai/edit-prediction
[claude-agent-acp]: https://github.com/agentclientprotocol/claude-agent-acp
[acp-repo]: https://github.com/agentclientprotocol/agent-client-protocol
