---
title: Hermes Agent Analysis
source: https://github.com/nousresearch/hermes-agent
purpose: Analysis of Hermes as a self-improving autonomous agent by Nous Research with multi-platform presence and skill creation.
platform_scope: [cli, telegram, discord, slack, whatsapp, signal, email, simplex]
created: 2026-04-09
updated: 2026-11-20
validated_links: 2026-06-28
status: open-source
---

**Details:** Open-source (MIT), active development by [Nous Research][nous] | **Version**: v0.23.3 (2026-11-20)

## What It Is

Hermes is a **self-improving AI agent** by Nous Research that operates
autonomously across multiple platforms. It features a built-in learning loop for
autonomous skill creation, persistent user models, and cross-session conversation
search. Largest agent project in this survey by star count (264,872 stars, `gh api` 2026-11-20).

**Key distinction**: Unlike coding-focused agents (CC, Goose) or research agents
(Feynman), Hermes is a **general-purpose autonomous agent** with multi-platform
presence (7 messaging channels + CLI), self-improving skills, and scheduled task
execution.

## Core Architecture

### Self-Improvement Loop

1. Agent encounters complex task
2. Autonomously generates reusable skill
3. Skill refined during subsequent use
4. Agent-curated memory with periodic reinforcement nudges
5. FTS5 full-text search across past conversations

### Memory Design (Compared with Claude Code)

Documented in the [Hermes memory docs][hermes-mem] (read 2026-11-20; documented behaviour, not tested here).

- **Two small curated files**: `MEMORY.md` (agent notes, 2,200 characters) and `USER.md` (user profile, 1,375 characters) in `~/.hermes/memories/`, entries separated by `§`. A write over the limit errors and the agent must consolidate first; nothing auto-compacts.
- **Frozen snapshot**: loaded into the system prompt at session start (keeps the prompt cache valid); mid-session writes reach disk at once but show in the prompt only next session.
- **Recall by search, not by index**: all sessions go to a local SQLite store with FTS5; `session_search` returns stored messages without LLM summarisation.
- **Background review**: after a turn an agent pass may save memory or create skills, paced by `memory.nudge_interval` / `skills.creation_nudge_interval`. `write_approval` (default off) holds writes for `/memory approve` or `reject` outside the interactive CLI.
- **External providers run alongside**: RetainDB and ByteRover ship as plugins; Honcho, Hindsight, Mem0 and Supermemory are installable.

| Aspect | Hermes | Claude Code ([CC memory][cc-mem-doc]) | [§ 4 engines][fw-mem] (Mem0, Graphiti, Zep, ...) |
|---|---|---|---|
| Always-loaded budget | ~2.2k + ~1.4k characters, hard error when full | First 200 lines or 25 KB of `MEMORY.md` index, rest silently not loaded | Retrieved per query, no fixed resident set |
| Topic detail | None; use session search | Topic files read on demand | Vector / graph / temporal store |
| Past-conversation recall | FTS5 over raw messages | Transcripts exist; only the feature-flagged, source-derived Auto-Dream searches them, no built-in recall tool | Per-engine extraction and retrieval |
| Consolidation | Agent edits within the size cap; background review nudges | Auto-Dream between sessions (feature-flagged, source-derived) | Engine-side (invalidation, merging) |
| Write gate | Optional approval (`write_approval`) | Plain markdown, human-editable | Varies |
| Extension | Pluggable provider alongside built-in | No built-in plug-in point; community tools in [CC memory tooling](../../cc-community/CC-memory-tooling-landscape.md) | These are the providers |

Reading: Hermes and Claude Code share the "small always-loaded notes plus on-demand recall" shape; Hermes bounds the resident set by hard character caps and recalls by full-text search, Claude Code by an index with topic files. Anthropic's layered framing is summarised in [CC memory](../../cc-native/context-memory/CC-memory-system-analysis.md#anthropics-components-of-agent-memory-2026-11-06).

### Multi-Platform Presence (7 channels)

| Channel | Features |
|---------|----------|
| CLI | Primary interface |
| Telegram | Voice memo transcription |
| Discord | Server integration |
| Slack | Workspace integration |
| WhatsApp | Messaging |
| Signal | Encrypted messaging |
| Email | Unified gateway |

Cross-platform conversation continuity — context carries across channels.

> **Update (2026-06-27):** The channel roster has grown well past these seven
> since the early v0.8.0 baseline. The current [integrations index][hermes-int] (Hermes
> at v0.17.0 "The Reach Release", 2026-06-19; latest release now v0.23.3) lists 27+ messaging platforms —
> among them [SimpleX][simplex], Matrix, Mattermost, ntfy, and Microsoft Teams.
> [SimpleX][simplex] is the most privacy-preserving channel of the set: a
> decentralized messenger with **no user identifiers of any kind** and
> double-ratchet end-to-end encryption (AGPLv3), which Hermes reaches via SimpleX's
> bot/WebSocket client library. (The integrations index lists SimpleX; the release
> notes do not attribute it to a specific version.)

### Terminal Backends (6)

| Backend | Use Case |
|---------|----------|
| Local | Default execution |
| Docker | Containerized isolation |
| SSH | Remote server execution |
| Daytona | Cloud workspace (hibernation) |
| Singularity | HPC containers |
| Modal | Serverless (cost-optimized hibernation) |

### LLM Provider Support

[Nous Portal][nous], OpenRouter (200+ models), z.ai/GLM, Kimi/Moonshot, MiniMax,
OpenAI, custom endpoints. Model switching via `hermes model` command.

### Task Automation

Built-in cron scheduler with delivery to any platform. Subagent spawning for
parallel workstreams in isolated contexts.

## Always-on Teammate Agents

Hermes shares a category with products that give each agent its own computer and most of: memory, routines and chat access (not every row states all three). Rows are identified first-party; all are fast-moving (checked 2026-11-20). Related coworker-style agents elsewhere in the corpus: [Rowboat](rowboat-analysis.md), [Odysseus](odysseus-analysis.md), [Databricks Genie](databricks-genie-analysis.md).

| Product | Origin | Open? | Memory / notes (evidence) |
|---|---|---|---|
| [Grok Bot][grokbot] | xAI ("SpaceX Super Intelligence" per its [launch post][grokbot-news]) | No; included in paid plans | Out of beta; own cloud computer, routines, Slack/Teams; memory: bots "learn how your team works" (vendor page) |
| [Muse][muse] | Meta | No; free tier, paid plans | Announced 2026-09-08; Secure VM with a separate approving "Sentinel" agent; user-editable memory incl. "forget" (vendor post) |
| [Rakazo][rakazo] | elie222 | Apache-2.0, 9,280 stars | Self-hosted "alternative to Grok Bot"; memory, routines, sandboxes (Docker/E2B/Daytona) (README, `gh api` 2026-11-20) |
| [OpenMausBot][openmaus] | milind-soni | Apache-2.0 (`enterprise/` source-available), 26,027 stars | Local-first desktop chat over your `claude`/`codex`/`grok` CLIs; per-bot thread memory; permission broker (README) |
| [Tucano][tucano] | eduwxyz | Apache-2.0, 439 stars | Desktop team of agents over installed harnesses (incl. Hermes, Claude Code); user-approvable memory, MCP gateway with approvals (README) |
| [OpenBot][openbot] | CopilotKit | MIT (memory service separately licensed), 13,018 stars | See [AG-UI landscape](../protocols/ag-ui-protocol-landscape.md#openbot-copilotkit-governed-ai-coworker-template) |
| [Claude Duet][duet] | Anthropic | Hosted; no source release stated; research preview, US waitlist for Pro/Max/Ultra | Own cloud VM with browser; iOS and Android apps and claude.ai; reuses your Claude account memory, skills and connectors; morning brief; approvals before sending or paying (vendor page; [announcement][duet-news], announced 2026-10-21) |
| [dots][dots] | OpenAI | Hosted in ChatGPT; no source release stated; first dot included in Pro and Business Premium | Announced 2026-09-29, beginning to roll out with more users planned; Enterprise users (including Edu and Healthcare) can try the beta; own cloud computer and browser; learns preferences over time (no routines stated); reached via ChatGPT apps, Slack, Teams (vendor post) |
| [Cue][cue] | Manus | Not stated; apps for web, macOS, Windows, iOS and Android | Each agent gets its own email, phone number, wallet and computer, plus routines; chat via Apple Messages and WhatsApp; you control which actions need approval (FAQ); memory and pricing not stated (vendor page) |

Hermes differs by being self-improving (skill creation) and by larger adoption than the open-source rows (264,871 stars, `gh api` 2026-11-20, v0.23.3); the rest compete on governance, approvals and bring-your-own-agent. Newer in the hosted rows: built-in agent identity (Cue: email, phone, wallet) and reuse of the user's existing account (Duet).

## Adoption Decision

| Dimension | Assessment |
|-----------|------------|
| **Use case** | General-purpose autonomous agent with multi-platform presence |
| **Self-improvement** | Autonomous skill creation and refinement |
| **Platforms** | CLI + 6 messaging channels |
| **Compute** | 6 terminal backends (local → serverless) |
| **Maturity** | Active (264,872 stars, v0.23.3; `gh api` 2026-11-20) |
| **License** | MIT |

**Strengths**: Largest community (264,872 stars, 2026-11-20). Self-improving skill loop (compare
[MOSS](moss-self-evolving-agent-analysis.md) and the
[skill-evolution landscape](../frameworks/agent-skill-evolution-research-landscape.md)). Broadest platform coverage (7 channels). 6 compute
backends from local to serverless. MIT licensed. [Skills Hub][skills-hub] for
community skill sharing.

**Risks**: pre-1.0 (v0.23.3 as of 2026-11-20) — stability not guaranteed. General-purpose scope may mean shallow
specialization. Nous Research dependency for portal/models. Overlaps with GoClaw
on multi-channel deployment but different architecture.

## Cross-References

- [goclaw-analysis.md](../infrastructure/goclaw-analysis.md) — also multi-channel agent platform (Go, different architecture)
- [deerflow-analysis.md](../orchestrators/deerflow-analysis.md) — general-purpose agent harness (LangGraph, no messaging channels)
- [CC-community-skills-landscape.md](../../cc-community/CC-community-skills-landscape.md) — CC skill creation (manual vs Hermes autonomous)

## Sources

| Source | Content |
|---|---|
| [Hermes Agent repo][hermes] | Self-improving autonomous agent (264,872 stars, 2026-11-20) |
| [Hermes docs][hermes-docs] | CLI, config, messaging, security, tools, skills, memory |
| [Hermes memory docs][hermes-mem] | File sizes, snapshot injection, FTS5 session search, providers, review nudges |
| [Grok Bot][grokbot] · [Meta Muse][muse] · [Claude Duet][duet] ([announcement][duet-news]) · [OpenAI dots][dots] · [Cue][cue] | Closed always-on agent products (vendor pages, checked 2026-11-20) |
| [Rakazo][rakazo] · [OpenMausBot][openmaus] · [Tucano][tucano] · [OpenBot][openbot] | Open-source teammate-agent projects (READMEs, `gh api` 2026-11-20) |
| [Hermes integrations index][hermes-int] | Full channel roster (27+ platforms incl. SimpleX) |
| [SimpleX Chat repo][simplex] | Privacy-preserving messaging transport (no user identifiers; AGPLv3) — a Hermes channel |

[hermes]: https://github.com/nousresearch/hermes-agent
[hermes-docs]: https://hermes-agent.nousresearch.com/docs/
[hermes-int]: https://hermes-agent.nousresearch.com/docs/integrations/
[simplex]: https://github.com/simplex-chat/simplex-chat
[nous]: https://nousresearch.com
[skills-hub]: https://agentskills.io/home
[hermes-mem]: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
[cc-mem-doc]: ../../cc-native/context-memory/CC-memory-system-analysis.md#auto-memory-architecture
[fw-mem]: ../frameworks/agent-frameworks-infrastructure-landscape.md#4-agent-memory-infrastructure
[grokbot]: https://x.ai/bot
[duet]: https://claude.com/product/claude-duet
[duet-news]: https://claude.com/resources/articles/claude-duet
[dots]: https://openai.com/index/introducing-dots/
[cue]: https://cue.im/
[muse]: https://about.fb.com/news/2026/09/introducing-muse
[grokbot-news]: https://x.ai/news/introducing-grok-bot
[rakazo]: https://github.com/elie222/rakazo
[openmaus]: https://github.com/milind-soni/OpenMausBot
[tucano]: https://github.com/eduwxyz/tucano
[openbot]: https://github.com/CopilotKit/openbot
