---
title: AG-UI / A2UI / OpenGenerativeUI Landscape
purpose: Disambiguates the agent-interoperability "Protocol Triangle" — frontend (AG-UI / A2UI / OpenGenerativeUI), agent↔agent (A2A), model↔tools (MCP) — plus the AGNTCY infrastructure stack. Tracks 2026 ecosystem adoption and clarifies which vendors have and have not joined.
created: 2026-04-24
updated: 2026-06-22
validated_links: 2026-06-22
---

**Status**: Research (informational)

## Summary

Three frequently-confused names occupy the agent↔user frontend layer in 2026: **AG-UI** is a transport protocol, **A2UI** is a declarative UI-payload spec, and **OpenGenerativeUI** is a CopilotKit reference framework. AG-UI carries A2UI (and other generative-UI specs) as payload. OpenGenerativeUI demonstrates the stack end-to-end but is not itself a protocol. Major framework vendors (Google ADK, Microsoft Agent Framework, AWS AgentCore, Oracle Agent Spec, PydanticAI) have adopted AG-UI; **Salesforce Agentforce 360 has not** — its protocol strategy centers on MCP via MuleSoft.

## The Protocol Triangle (CopilotKit framing)

| Layer | Protocol | Purpose |
|---|---|---|
| Model ↔ Tools | **MCP** (Model Context Protocol) | Context and tool exposure |
| Agent ↔ Agent | **A2A** | Cross-agent coordination |
| User/App ↔ Agent | **AG-UI** | Bi-directional event stream |
| UI payload format | **A2UI** (and others) | Declarative widget descriptions carried inside AG-UI events |

Source: [CopilotKit — AG-UI vs A2UI][ag-vs-a2]

## A2A (Agent-to-Agent Protocol)

The **agent ↔ agent** leg. Open protocol for interoperability between *opaque* agentic apps — agents on different frameworks discover each other, delegate tasks, and exchange results without exposing internal logic. Originally **Google**, donated to the **Linux Foundation** (2025; TSC spans AWS, Cisco, Google, IBM, Microsoft, Salesforce, SAP, ServiceNow). Spec at [a2a-protocol.org][a2a]; current **v1.0.1** (2026-05; v1.0.0 in 2026-03 broke from the v0.x line).

Core primitives ([spec][a2a-spec]):

- **Agent Card** — JSON discovery doc at `/.well-known/agent-card.json` (renamed from `agent.json` in v0.3.0): name, service URL, capabilities (streaming, push), auth schemes (Bearer / OAuth2 / mTLS / OIDC), skills; digitally signable.
- **Task** — stateful unit of work with a lifecycle (`submitted → working → input-required / auth-required → completed / failed / canceled / rejected`).
- **Message / Artifact / Part** — conversational turns, generated outputs, and the content container (text, bytes, URLs, structured JSON).
- **Transport** — JSON-RPC 2.0 over HTTP(S); SSE for streaming; gRPC for high-throughput. v1.0.0 modernized auth to OAuth 2.0 (PKCE / device code).

Complementary to MCP, not competing: "encapsulating an agent as a simple [tool] is fundamentally limiting" ([spec][a2a-spec]) — MCP is agent↔tools, A2A is agent↔agent.

## AGNTCY ("Internet of Agents")

An open-source **infrastructure stack beneath** the semantic protocols — discovery, identity, messaging, observability — rather than a task-semantics protocol itself. Initiated by **Cisco (Outshift)** in 2026-03, donated to the **Linux Foundation** by 2026-07 (75+ orgs). Components ([agntcy.org][agntcy]):

| Component | Role | Status |
|---|---|---|
| **OASF** (Open Agentic Schema Framework) | Agent-description schema (OCSF-inspired); carries A2A agent cards + MCP server descriptions | v1.0.0 (2026-02) |
| **Agent Directory** | Federated, synchronized agent registry | active |
| **SLIM** (Secure Low-latency Interactive Messaging) | Transport (gRPC/HTTP2 + MLS E2E encryption); carries A2A/MCP as payload | IETF draft |
| **Identity** | Agent/MCP identity via W3C Verifiable Credentials + DIDs | v0.0.x |
| **ACP** (Agent Connect Protocol) | REST interface to invoke remote agents | **archived 2026-04** |

Positioned as complementary infra *below* the semantic protocols (SLIM transports A2A/MCP; OASF and the Directory index both). Overlap with A2A's coordination role exists at different stack layers; independent overlap analysis is limited (vendor framing). Note: "AGP" (Agent Gateway Protocol) is informal naming — **SLIM** is the actual transport component.

## MCP as a Protocol Spec

The **model ↔ tools** leg ([modelcontextprotocol.io][mcp]). Spec revisions are date-stamped `YYYY-MM-DD`; current stable **2025-11-25**. Key additions over **2025-06-18** ([changelog][mcp-changelog]):

- **Tasks** (experimental) — durable requests with polling + deferred result retrieval (mirrors A2A's Task lifecycle at the tool layer).
- **Auth** — OpenID Connect Discovery, OAuth Client ID Metadata Documents, incremental scope consent via `WWW-Authenticate`.
- **Elicitation enhancements** — enum schemas (single/multi-select), URL-mode elicitation; plus **tool calling in sampling** (`tools` / `toolChoice`).
- **Icon metadata** for tools/resources/prompts; **JSON Schema 2020-12** as the default dialect; formalized governance + SDK tiering.

(The prior 2025-06-18 revision introduced elicitation, structured tool output, OAuth Resource-Server classification, and removed JSON-RPC batching.) Cross-ref: [CC-connectors-overview.md](../cc-native/plugins-ecosystem/CC-connectors-overview.md) — CC's MCP connector surface.

## AG-UI (Agent-User Interaction Protocol)

**Repo**: [ag-ui-protocol/ag-ui][ag-ui-repo] | **Docs**: [docs.ag-ui.com][ag-ui-docs] | **Origin**: CopilotKit, incubated via LangGraph + CrewAI partnerships

An open, lightweight, bi-directional protocol between any user-facing application and any agentic backend.

### Wire Format

- Frontend sends **one HTTP POST** carrying the user's prompt or current state
- Backend replies with a **Server-Sent Events (SSE) stream** of typed JSON events
- Optional binary channel for high-throughput scenarios

### Core Event Types

| Event | Purpose |
|---|---|
| `TEXT_MESSAGE_CONTENT` | Streaming token output |
| `TOOL_CALL_START` | Agent invoked an external function/API |
| `STATE_DELTA` | Incremental state diff (table rows, document edits) merged by the UI |
| *Lifecycle / error events* | Timeouts, failures, done signals |

Each event type has a well-defined JSON schema ([source][ag-ui-docs]).

### Capabilities Out of the Box

- Live token streaming
- Tool-call progress updates
- Incremental state diffs (bi-directional read/write or read-only shared state)
- Explicit error and lifecycle events
- Multi-agent handoffs on a single channel

### 2026 Ecosystem Adoption

Confirmed integrations per the [ag-ui README][ag-ui-repo] and [CopilotKit AG-UI page][ag-ui-copilotkit]:

| Vendor / Framework | Source | Notes |
|---|---|---|
| **Google ADK** | [ag-ui README][ag-ui-repo] | Native integration — ADK agents collaborate via AG-UI |
| **Microsoft Agent Framework** | [Microsoft Learn — AG-UI Integration][ms-learn-agui] | Official docs page; CopilotKit supplies UI components |
| **AWS Strands Agents / Bedrock AgentCore** | [ag-ui README][ag-ui-repo] | Dedicated AG-UI endpoint in AgentCore + FAST template pattern (March 2026) |
| **Oracle Agent Spec** | [Oracle blog — Agent Spec + AG-UI][oracle-agui] (March 2026) | Three-way alignment with Oracle + CopilotKit + Google (AG-UI + A2UI) |
| **LangGraph**, **CrewAI** | [ag-ui README][ag-ui-repo] | Origin partnerships |
| **Mastra**, **Pydantic AI**, **Agno**, **LlamaIndex**, **AG2**, **Langroid** | [ag-ui README][ag-ui-repo] | Framework integrations |
| **Community SDKs** | [ag-ui README][ag-ui-repo] | Kotlin, Go, Dart, Java, Rust, Ruby, .NET, Nim, C++ |

Scale signals (as reported by [CopilotKit][ag-ui-copilotkit]): 9K+ GitHub stars, 120K weekly installs combined with CopilotKit, 2M agent↔user interactions/week.

### Non-Adopters (as of 2026-04-24)

- **Salesforce Agentforce 360** — not listed on the [ag-ui README][ag-ui-repo] integrations. Salesforce's own [Agentforce 360 announcements][sf-agentforce] emphasize **MCP via MuleSoft** and the proprietary **MuleSoft Agent Fabric** for cross-platform agent discovery (spanning Agentforce + Amazon Bedrock + Google Vertex AI + Microsoft Copilot Studio). Frontend strategy is "Headless 360" (API/MCP/CLI exposure), not a frontend interaction protocol. See [Salesforce Ben — ISV expansion (Mar 2026)][sf-ben] and [Agentforce 360 for AWS][sf-aws].

## A2UI (Agent-to-UI — Declarative Generative UI)

**Origin**: Google, launched 2026. CopilotKit is a launch partner.

A2UI is **not a transport** — it is a declarative spec describing UI widgets that an agent returns as part of its response. The transport is typically AG-UI, but A2UI is transport-agnostic.

- A2UI widgets can be carried inside AG-UI events (`TEXT_MESSAGE_CONTENT` or dedicated widget events)
- AG-UI natively supports all generative-UI specs — developers can also define custom ones
- CopilotKit claims "full support" for A2UI ([source][ag-vs-a2])

Source: [CopilotKit — Build with Google's new A2UI Spec][a2ui-blog]

## OpenGenerativeUI (CopilotKit Reference Framework)

**Repo**: [CopilotKit/OpenGenerativeUI][ogui-repo] | **Demo**: [opengenerativeui.copilotkit.ai][ogui-site]

Not a protocol — an end-to-end reference implementation:

- **Frontend**: Next.js 16 + React 19 + Tailwind CSS 4; components render as **sandboxed iframes** receiving HTML/SVG from the agent via the `useComponent` hook
- **Agent**: LangChain Deep Agents with skills-based progressive disclosure
- **MCP server**: design-system + skill resources + document-assembler exposed over MCP

Supported clients per the repo: Claude Desktop (stdio), Claude Code / HTTP clients, Cursor, Next.js. Uses MCP for tool exposure and HTTP for client communication — **not AG-UI directly**, though the patterns are compatible.

## Decision Matrix

| Your need | Use |
|---|---|
| Stream agent events to any frontend | **AG-UI** (protocol) |
| Agent emits structured UI widgets | **A2UI** spec over AG-UI |
| End-to-end demo with generative HTML components | **OpenGenerativeUI** (reference) |
| Claude Code observability over agent-user interactions | Use AG-UI-compatible backend + OTel (see [CC-agent-observability-methods-analysis.md § Claude Code (First-Party OTel Integration)](../cc-community/CC-agent-observability-methods-analysis.md#claude-code-first-party-otel-integration)) |

## Agent Control-Surface Naming (2026)

A wave of agent-management products has adopted **cockpit / "command center" / "flight deck" / "HUD"** framing. This is adjacent to — but distinct from — the generative-UI layer above: these are surfaces for *operating* agents, not protocols for agents to *render* UI. First-party-verified examples (June 2026):

| Product | Self-description (first-party) | What it actually is |
|---|---|---|
| Devin Desktop (Cognition) | "Agent Command Center" | Kanban board for local + cloud agents — see [windsurf-analysis.md](windsurf-analysis.md#agent-command-center) |
| [Omnara][omnara] | "the command center for your coding agents… terminal, web, mobile" | Session-sync / notification layer — full analysis: [CC-remote-access-landscape.md](../cc-native/ci-remote/CC-remote-access-landscape.md#omnara) |
| [flightdeckhq/flightdeck][flightdeck] | "observability and control plane for production and coding agents" | Observability dashboard |
| [Ralph TUI][ralph-tui] | "AI Agent Loop Orchestrator" | Task-loop TUI — see [CC-ralph-enhancement-research.md](../cc-native/agents-skills/CC-ralph-enhancement-research.md) |
| [Vibe Kanban][vibe-kanban] | kanban board (sunsetting) | Orchestrator board — see [CC-office-worker-workflows.md](../cc-community/CC-office-worker-workflows.md) |

**The positioning gap.** All of the above are **orchestration-board or observability** surfaces. None is a *live generative-UI* surface — one where the agent streams and renders UI components in real time. That capability is precisely what the AG-UI + A2UI + OpenGenerativeUI stack on this page provides, and **not** what the "command center" products do. So the cockpit/HUD naming space is crowding with board/observability tools, while the live-generative-UI cockpit position remains largely unoccupied under those labels.

**Myth-busting (verified 2026-06-20).** Two widely-repeated "HUD" attributions are **third-party coinages, not first-party framings**: Nous Research's [Hermes][hermes-nous] uses no HUD terminology (it self-describes as a self-improving agent; `hermes-hudui` is an unofficial community monitor), and [Ralph][ralph-tui] self-describes as an "AI Agent Loop Orchestrator" ("heads-up display" appears only as a third-party reviewer's simile).

## Cross-References

- [CC-agent-observability-methods-analysis.md](../cc-community/CC-agent-observability-methods-analysis.md) — OTel observability patterns (AG-UI events can be modeled as OTel spans)
- [CC-connectors-overview.md](../cc-native/plugins-ecosystem/CC-connectors-overview.md) — MCP connector landscape (the model↔tool leg of the Protocol Triangle)

## Sources

| Source | Content |
|---|---|
| [ag-ui-protocol/ag-ui][ag-ui-repo] | Protocol spec, integrations list |
| [docs.ag-ui.com][ag-ui-docs] | Official AG-UI documentation |
| [CopilotKit AG-UI page][ag-ui-copilotkit] | Partner list, adoption metrics |
| [CopilotKit — AG-UI vs A2UI][ag-vs-a2] | Protocol Triangle framing, A2UI relationship |
| [Google A2UI launch (CopilotKit blog)][a2ui-blog] | A2UI spec origin |
| [Oracle Agent Spec + AG-UI (Oracle blog)][oracle-agui] | Three-way alignment announcement |
| [Microsoft Learn — AG-UI Integration][ms-learn-agui] | Microsoft Agent Framework integration |
| [CopilotKit/OpenGenerativeUI][ogui-repo] | Reference framework |
| [Salesforce Agentforce 360][sf-agentforce] | Salesforce protocol strategy (MCP, not AG-UI) |
| [Devin Desktop FAQ][devin-faq] | "Agent Command Center" framing (Kanban for local + cloud agents) |
| [Omnara (YC launch)][omnara] | "command center for AI agents: terminal, web, mobile" |
| [flightdeckhq/flightdeck][flightdeck] | "observability and control plane" for agents |
| [Ralph TUI][ralph-tui] | "AI Agent Loop Orchestrator" — no first-party HUD framing |
| [Nous Research — Hermes Agent][hermes-nous] | Self-improving agent — no HUD / "heads-up display" framing |
| [A2A protocol][a2a] · [spec][a2a-spec] | Agent-to-agent interop (Google → Linux Foundation), v1.0.1 |
| [AGNTCY][agntcy] | "Internet of Agents" infra stack (Cisco → Linux Foundation): OASF, Directory, SLIM, Identity |
| [MCP spec 2025-11-25][mcp] · [changelog][mcp-changelog] | Model↔tools protocol; current spec revision |

[ag-ui-repo]: https://github.com/ag-ui-protocol/ag-ui
[ag-ui-docs]: https://docs.ag-ui.com/
[ag-ui-copilotkit]: https://www.copilotkit.ai/ag-ui
[ag-vs-a2]: https://www.copilotkit.ai/ag-ui-and-a2ui
[a2ui-blog]: https://www.copilotkit.ai/blog/build-with-googles-new-a2ui-spec-agent-user-interfaces-with-a2ui-ag-ui
[oracle-agui]: https://blogs.oracle.com/ai-and-datascience/announcing-agent-spec-for-a2ui-copilotkit-ag-ui
[ms-learn-agui]: https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/
[ogui-repo]: https://github.com/CopilotKit/OpenGenerativeUI
[ogui-site]: https://opengenerativeui.copilotkit.ai/
[sf-agentforce]: https://www.salesforce.com/agentforce/what-is-new/
[sf-ben]: https://www.salesforceben.com/salesforce-opens-agentforce-360-to-isvs-so-partners-can-build-and-distribute-ai-agents/
[sf-aws]: https://www.salesforce.com/news/stories/agentforce-360-for-aws-announcement/
[devin-faq]: https://docs.devin.ai/desktop/devin-desktop-faq
[omnara]: https://www.ycombinator.com/launches/OCT-omnara-the-first-command-center-for-ai-agents-terminal-web-and-mobile
[flightdeck]: https://github.com/flightdeckhq/flightdeck
[ralph-tui]: https://ralph-tui.com/
[hermes-nous]: https://hermes-agent.nousresearch.com/
[vibe-kanban]: https://www.vibekanban.com/
[a2a]: https://a2a-protocol.org/
[a2a-spec]: https://a2a-protocol.org/latest/specification/
[agntcy]: https://agntcy.org/
[mcp]: https://modelcontextprotocol.io/
[mcp-changelog]: https://modelcontextprotocol.io/specification/2025-11-25
