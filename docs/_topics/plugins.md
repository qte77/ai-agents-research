# Topic Hub: Plugins

Extension packaging: plugins, MCP servers, marketplaces across the corpus. Pointers only; see
[the hub index](README.md).

| Doc / section | What it covers | Bucket |
|---|---|---|
| [CC-official-plugins-landscape.md](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) | Official CC plugin ecosystem catalog and adoption guidance | cc-native |
| [CC-mods-function-hooks-analysis.md](../cc-native/plugins-ecosystem/CC-mods-function-hooks-analysis.md) | Mods (function hooks): in-process event handlers that redraw or rewrite Claude Code, shipped as plugins; the built-in AGENTS.md and `/diff` mods | cc-native |
| [CC-plugin-packaging-research.md](../cc-native/plugins-ecosystem/CC-plugin-packaging-research.md) | Plugin structure, manifest, packaging vs repo-local config | cc-native |
| [CC-cowork-plugins-enterprise-analysis.md](../cc-native/plugins-ecosystem/CC-cowork-plugins-enterprise-analysis.md) | Cowork plugin architecture and enterprise distribution | cc-native |
| [CC-connectors-overview.md](../cc-native/plugins-ecosystem/CC-connectors-overview.md) | Claude Connectors (Google, Slack, Microsoft 365) | cc-native |
| [CC-connectors-overview.md § Public Connectors Directory](../cc-native/plugins-ecosystem/CC-connectors-overview.md#public-connectors-directory) | The claude.com connectors directory: counts, filters, the Verified and Community labels, ten selected entries (observed 2026-11-25); PandaDoc connector | cc-native |
| [CC-mcp-hardware-standard-analysis.md](../cc-native/plugins-ecosystem/CC-mcp-hardware-standard-analysis.md) | MCP hardware standard research preview | cc-native |
| [CC-web-scraping-plugins-analysis.md](../cc-native/plugins-ecosystem/CC-web-scraping-plugins-analysis.md) | Firecrawl and Playwright MCP plugins; alternative browser-agent tools incl. jev-ultrafast (decision-model-driven action selection) | cc-native |
| [CC-community-plugins-landscape.md](../cc-community/CC-community-plugins-landscape.md) | Community plugin catalogs (awesome-claude-code, awesome-claude-code-plugins) | cc-community |
| [CC-community-tooling-landscape.md § New and unproven: agent plugins](../cc-community/CC-community-tooling-landscape.md#new-and-unproven-agent-plugins-2026-11-23) | Watch entries for three days-old plugins: mobile-agent-testers (agents testing apps on simulators in CI), fast-anything (port a profiled hot function to Rust) and shrink-anything (cut dead code and deps, kept only if your checks pass) | cc-community |
| [CC-plugin-packaging-research.md § 5](../cc-native/plugins-ecosystem/CC-plugin-packaging-research.md#5-version-pinning-for-reproducible-installs) | Version pinning and reproducible installs (manifest `version`; marketplace `ref`/`sha`/`sha256`) | cc-native |
| [agent-plugins-standard-analysis.md § Concrete implementation](../non-cc/protocols/agent-plugins-standard-analysis.md#concrete-implementation-mitosis-memory-mitosis-agent-plugin) | Agent Plugins open standard (v1.0.0); a concrete cross-client implementation (Mitosis) | non-cc |
| [openai-apps-plugins-analysis.md](../non-cc/protocols/openai-apps-plugins-analysis.md) | OpenAI's unified ChatGPT + Codex plugin system vs. CC packaging and the Agent Plugins standard; manifest, marketplace, pinning, review; rubric-scored | non-cc |
| [goose-analysis.md § AAIF](../non-cc/agents/goose-analysis.md#agentic-ai-foundation-aaif-governance-and-hosted-projects) | Agentic AI Foundation governance/hosted-projects; relevance to plugin/MCP standards is indirect (no dedicated AAIF plugin spec) | non-cc |
| [CC-community-skills-landscape.md § cursor/plugins pstack (Lauren Tan)](../cc-community/CC-community-skills-landscape.md#cursorplugins-pstack-lauren-tan) | Cursor's pstack plugin: playbooks installable in Claude Code via a marketplace | cc-community |
| [CC-codex-plugin-cc-analysis.md](../cc-community/CC-codex-plugin-cc-analysis.md) | OpenAI's official Claude Code plugin that delegates work to Codex | cc-community |
| [CC-compass-mcp-analysis.md](../cc-community/CC-compass-mcp-analysis.md) | compass-mcp MCP server: architecture and Claude Code integration | cc-community |
| [CC-netdata-mcp-analysis.md](../cc-community/CC-netdata-mcp-analysis.md) | Netdata's built-in MCP server for incident-time infrastructure queries | cc-community |
| [CC-business-api-integrations.md](../cc-native/plugins-ecosystem/CC-business-api-integrations.md) | Business MCP servers: payments, accounting, CRM, ERP, legal | cc-native |
| [CC-channels-analysis.md](../cc-native/plugins-ecosystem/CC-channels-analysis.md) | Channels: MCP server plugins that push external events into running sessions | cc-native |
| [CC-ide-integration-protocol.md](../cc-native/configuration/CC-ide-integration-protocol.md) | The WebSocket MCP protocol between the CLI and IDE extensions | cc-native |
| [ag-ui-protocol-landscape.md](../non-cc/protocols/ag-ui-protocol-landscape.md) | Protocol triangle: AG-UI and A2UI (frontend), A2A (agent to agent), MCP (model to tools) | non-cc |
| [rea-analysis.md](../non-cc/infrastructure/rea-analysis.md) | REA: MCP server and CLI giving coding agents reverse-engineering tools | non-cc |

Related hubs: [skills.md](skills.md), [harness.md](harness.md).
