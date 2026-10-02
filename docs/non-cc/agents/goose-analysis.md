---
title: Goose Analysis
source: https://github.com/aaif-goose/goose
purpose: Analysis of Goose as MCP co-creator, reference implementation, and AAIF founding project — architectural comparison with CC's MCP integration.
created: 2026-04-05
updated: 2026-10-02
validated_links: 2026-09-30
status: assess
---

**Details:** open-source, active, architecturally significant

## What It Is

Goose is an open-source (Apache-2.0) general-purpose AI agent — "for code, workflows, and everything in between" — now stewarded by the **Agentic AI Foundation (AAIF)** at the Linux Foundation, donated by Block (Square). ~50K stars, Rust 65% / TypeScript 28%. Desktop app + CLI + API. LLM-agnostic with multi-model routing.

**Key distinction**: Goose co-developed MCP with Anthropic — Block's internal extension friction led to the collaboration that produced the protocol. Goose is the **reference MCP implementation**, not merely an adopter. It moved from `block/goose` to the **Agentic AI Foundation** in April 2026 — a founding AAIF project alongside MCP and AGENTS.md ([formation][aaif], [move][goose-move]).

## MCP Co-Origin

Before MCP had a name, Block's internal Goose agent had a Python extension system that required custom integration per tool. Block contacted Anthropic about this friction and discovered Anthropic was already building what became MCP. They co-developed the protocol, with Goose as the proving ground ([source][arcade-origin]).

This means Goose's architecture **is** MCP architecture — extensions are MCP servers, tools are MCP tool calls, the agent loop speaks MCP natively. 3,000+ MCP servers available. Goose is also the reference client for MCP Apps (interactive UI rendered in conversation) ([source][mcp-apps]).

## Architecture

```text
User → Interface (desktop/CLI)
         → Agent (interactive loop)
           → Provider (any LLM via configurable backends)
           → Extensions (= MCP servers, built-in + external)
             → Tools (MCP tool calls)
```

### Six-Step Agent Loop

1. **Human request** → agent
2. **Provider chat** → sends request + available tools to LLM
3. **Model extension call** → LLM returns tool call (JSON)
4. **Goose executes** → runs tool, gathers results
5. **Context revision** → summarizes/deletes outdated content for token efficiency
6. **Model response** → final output or loop back to step 2

Errors are sent back to the model as tool responses — the LLM self-corrects rather than breaking execution ([source][arch]).

### ACP (Agent Client Protocol)

Goose implements ACP bidirectionally:

- **As server**: `goose acp` over stdio — enables IDE integration (JetBrains, Zed)
- **As client**: delegates to external ACP agents, passing extensions as MCP servers

This is comparable to CC's WebSocket IDE protocol but uses a different standard ([source][arch]).

## Install, CLI & Configuration

**Install** (see [Goose install docs][install]):

```bash
# Linux/macOS
curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | bash
# macOS (Homebrew)
brew install block-goose-cli
# non-interactive (CI): skip the interactive configure step
curl -fsSL https://github.com/aaif-goose/goose/releases/download/stable/download_cli.sh | CONFIGURE=false bash
```

**CLI**: `goose session` (interactive run), `goose configure` (providers + extensions), `goose update`; `goose acp` exposes the ACP server for IDEs (above).

**Environment variables**: runtime provider keys — `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY` (other providers per the [docs][install]). Install-time: `GOOSE_VERSION` pins a release for reproducible CI and `CONFIGURE=false` skips interactive setup. Beyond keys, configuration (15+ providers, 70+ MCP extensions) lives in `goose configure`.

## Comparison with CC

| Aspect | Claude Code | Goose |
|--------|------------|-------|
| MCP role | Consumer (MCP bridge since v2.1.46) | Co-creator and reference implementation |
| LLM | Anthropic-only (Opus/Sonnet/Haiku) | Any provider (multi-model routing) |
| Extensions | Plugins + MCP servers (separate systems) | Extensions = MCP servers (unified) |
| IDE protocol | WebSocket JSON-RPC 2.0 (proprietary) | ACP (open standard) |
| License | Proprietary | Apache-2.0 |
| Context management | Prompt caching + compaction | Context revision (summarize + delete) |
| MCP Apps | Not supported | Reference client |
| Language | TypeScript (Bun) | Rust + TypeScript |

## Agentic AI Foundation (AAIF): governance and hosted projects

Researched 2026-09-30 for plan 0009's skills/plugins standards row (S5); the plan's prior coverage of
AAIF was only this doc's mention of it as Goose's steward. Per the foundation's own site, AAIF is "the
neutral and open foundation built on transparency, collaboration, and standardization to advance the
public interest in agentic AI innovation" ([AAIF homepage][aaif-home], fetched 2026-09-30) — a Linux
Foundation project, consistent with the [formation announcement][aaif] already cited above.

**Governance**: the [AAIF charter][aaif-charter] (a PDF in the `aaif/foundation` repo, "Amended July 29,
2026") puts a Governing Board in charge. The board approves new projects "in consultation with the
Technical Committee", and "Each Technical Project shall have a TSC, which shall be responsible for the
technical direction" of that project, whose governance "is as set forth in the charter for that
project". The site lists the [Governing Board][aaif-board] (chair from AWS; members from Google,
Microsoft, OpenAI, Cloudflare, Anthropic and others), the [Technical Committee][aaif-tc] (chair from
Anthropic, co-chair from Microsoft; members from Block, OpenAI, Google, Cloudflare and others) and
tiered [membership][aaif-members], where voting rights and board seats depend on the tier. Eight
working groups are named on the [homepage][aaif-home] (Accuracy & Reliability, Agentic Commerce,
Governance/Risk/Regulatory Alignment, Identity & Trust, Observability & Traceability, Security &
Privacy, Workflows & Process Integration, Taxonomy & Landscape). The site does not list the members of
each hosted project's TSC, and publishes no board minutes or decision log (all checked 2026-10-01).

**Hosted projects** ([AAIF projects page][aaif-projects], fetched 2026-09-30 — the homepage itself
names no specific projects): six in total, including Goose; the other five —

- **Model Context Protocol (MCP)** — "a protocol for seamless integration between LLM applications and external data sources"
- **AGENTS.md** — "a simple, open format for guiding coding agents"
- **agentgateway** — "secure, scalable connections between AI agents, models, tools, and APIs across ecosystems"
- **Agent2Agent (A2A)** — agent-to-agent communication and task exchange across platforms
- **Agent Router** — "an open source AI gateway built on Envoy that connects applications to models and MCP tools"

**Relevance to skills/plugins standards**: indirect, not direct. AAIF hosts no dedicated Agent-Skills
or plugin-packaging specification of its own — the [Agent Plugins standard][agent-plugins] (v1.0.0,
packaging Skills + MCP servers) is a separate, unaffiliated effort with its own Technical Steering
Committee (Amazon, Cursor, Microsoft, OpenAI, Vercel), not an AAIF project. AAIF's relevance to this
arc's Skills/Plugins subject runs through the two protocols it *does* host: **MCP** is the transport
plugins wrap (Goose's own "extensions = MCP servers" design, above, is the clearest example), and
**AGENTS.md** is the adjacent open format for the instructions layer plugins and skills sit beside.
Agent Router and agentgateway are infrastructure for routing agent traffic to models/tools, not for
packaging agent capabilities themselves.

`subject: plugins`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| partial [charter][aaif-charter], [board][aaif-board] (foundation-level decisions are shared across member companies on the board and the Technical Committee, but each hosted spec's technical direction sits with its own TSC, whose members the site does not list) | n/a [AAIF homepage][aaif-home] (AAIF is a governance foundation, not a running system — "distributed" as defined by the rubric doesn't apply to an org) | n/a [AAIF projects][aaif-projects] (no software artifact of AAIF's own to rebuild; its hosted projects, e.g. MCP, are scored in their own docs) | partial [charter][aaif-charter] (the board can establish committees and approve new projects without a rewrite; how each spec changes is set by that project's own charter and TSC, not documented on the AAIF site) | partial [charter][aaif-charter] (the charter itself is in git, but as a single PDF commit, so amendments are not diffable; the hosted specs are git-versioned in their own repos; governance decisions are not versioned) | no data [charter][aaif-charter] (the charter requires the chair to submit board minutes for approval, but no minutes or decision log are published on the site or in `aaif/foundation`) |

`scored 2026-09-30`

## Relevance to qte77

- **MCP research**: Goose is the canonical example of ground-up MCP-native design — compare with CC's bolt-on MCP bridge for protocol design insights
- **Plugin architecture**: Goose's "extension = MCP server" unification is what CC's plugin system may converge toward
- **ACP**: emerging protocol for agent-to-agent and agent-to-IDE communication — track alongside CC's WebSocket protocol

## Sources

| Source | Content |
|---|---|
| [aaif-goose/goose][repo] | Repository, architecture docs |
| [Goose Architecture][arch] | Agent loop, extensions, MCP integration |
| [Arcade: Goose shaped MCP][arcade-origin] | MCP co-development history |
| [AAIF announcement][aaif] | Linux Foundation founding with MCP + Goose + AGENTS.md |
| [Goose moves to AAIF][goose-move] | April 2026 relocation from block/goose |
| [MCP Apps blog][mcp-apps] | Goose as reference MCP Apps client |
| [Goose install & CLI docs][install] | Install, CLI commands, provider env vars |
| [AAIF homepage][aaif-home] | Working groups, foundation framing (fetched 2026-09-30) |
| [AAIF charter][aaif-charter], [board][aaif-board], [Technical Committee][aaif-tc], [members][aaif-members] | Governance: board, Technical Committee, per-project TSCs, membership tiers (checked 2026-10-01) |
| [AAIF projects page][aaif-projects] | 6 hosted projects including Goose: MCP, AGENTS.md, agentgateway, A2A, Agent Router (fetched 2026-09-30) |
| [Agent Plugins standard][agent-plugins] | Cross-ref: the skills/plugin-packaging standard AAIF does *not* host |

[repo]: https://github.com/aaif-goose/goose
[arch]: https://goose-docs.ai/
[arcade-origin]: https://www.arcade.dev/blog/goose-the-open-source-agent-that-shaped-mcp
[aaif]: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
[goose-move]: https://goose-docs.ai/blog/2026/04/07/goose-moves-to-aaif/
[mcp-apps]: https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/
[install]: https://goose-docs.ai/docs/getting-started/installation
[aaif-home]: https://aaif.io/
[aaif-projects]: https://aaif.io/projects
[aaif-charter]: https://github.com/aaif/foundation/blob/main/foundation-charter.pdf
[aaif-board]: https://aaif.io/board
[aaif-tc]: https://aaif.io/tc
[aaif-members]: https://aaif.io/members
[agent-plugins]: ../protocols/agent-plugins-standard-analysis.md
