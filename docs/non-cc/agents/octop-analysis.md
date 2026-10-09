---
title: Octop — Self-Hosted Multi-User, Multi-Agent AI Assistant
source: https://github.com/TencentCloud/Octop
purpose: Evaluate Octop's single-process, multi-user agent-orchestration architecture, its memory/context layer, and its outbound ACP delegation to coding agents including Claude Code.
created: 2026-10-09
updated: 2026-10-09
validated_links: 2026-10-09
status: assess
---

## What It Is

[Octop][octop-gh] (TencentCloud) describes itself, verbatim, as "an open-source, self-hosted AI
assistant" that is "not just a tool — it's a digital life form that can operate in parallel" through
a multi-agent architecture. Its own framing of who it serves (verbatim): "Octop is a self-hosted AI
assistant platform for households and small teams." Repository facts (`gh api
repos/TencentCloud/Octop`, accessed 2026-10-09): **8,189 stars, 991 forks, MIT license** (confirmed
from the repo's `LICENSE` file directly, not only the GitHub API's derived license field), created
2026-07-08, Python as primary language. Latest tagged release: `v1.0.2b6`, published 2026-10-04
(`gh api repos/TencentCloud/Octop/releases/latest`).

## How It Works

**Single-process, multi-component bundle.** Per `docs/architecture.md`, Octop ships `octop-harness`
(a LangGraph-based chat runtime), `octop-gateway` (an IM channel pipeline), and a React/TypeScript
dashboard together in one Python wheel. The doc states, verbatim: "The whole stack is one process,"
with "no separate worker, no external queue," and no required external services beyond the user's
chosen LLM provider.

**Multi-user model.** One admin account can serve a household or small team; each user gets their
own set of "experts" (agents), each with its own workspace, model providers, channels, and cron
jobs. Isolation is enforced per database row rather than per process: every request is
JWT-authenticated and resolved to a `User`, and `agents.user_id` is checked against the caller (with
an admin bypass) through a single global agent-manager registry — the architecture doc states this
single registry "keeps admin tooling (`/api/admin/*`) and cross-user diagnostics simple."

**Agent orchestration.** The layering is `OctopServer` → per-user `HarnessAgentManager` → per-agent
`AgentRuntime` (runtime, an `HarnessProcessor` entry point, a channel manager, a cron manager); web
UI, IM, and cron requests all route through one in-process `HarnessProcessor`. **AgentTeams (Beta)**
adds a coordinator layer: per the README (verbatim), "A coordinator schedules multiple experts on
multi-step work" (documented further in `docs/expert-teams.md`). Experts can also be shared within a
deployment through an internal expert library/market.

**Memory and context.** Octop Memory is described as hierarchical recall with full-text search,
traveling with each agent's own workspace; conversation state itself is checkpointed by the harness
runtime through a LangGraph SQLite-backed checkpointer (`CompactSqliteSaver`). The control plane
(users, agents, providers, channels, cron, sessions, audit) runs on SQLite (WAL mode) by default, or
PostgreSQL optionally, in which case agent memory moves to a per-agent PostgreSQL schema on the same
connection by default (or stays SQLite-backed if explicitly configured). A separate maintenance
command, `octop memory slim`, deduplicates and compacts an agent's `memory.sqlite` file; per
`docs/memory-slim.md` (verbatim, translated from the Chinese-language doc), each run's backup "sits
beside the original and is never automatically deleted or overwritten," and online runs explicitly
preserve "history IDs, metadata, parent, writes and business memories" while compacting. Neither doc
describes how hierarchical recall ranks or selects memories at query time — that part of the claim
rests on README prose, not an inspected mechanism.

**Tools, MCP, and agent-to-agent delegation.** Connectors cover OAuth apps and MCP gateways,
including a bundled Tencent suite (Docs, Meeting, News, and others). Octop implements the **Agent
Client Protocol (ACP)** in both directions: inbound (`octop acp`) lets external IDEs drive an Octop
agent; outbound, Octop delegates coding tasks to external coding-agent CLIs — **including Claude
Code** — alongside OpenCode, CodeBuddy, and Codex, gated by permission checks. Additional surfaces:
headless-Chromium browser automation (Octop Browser, via CDP), an in-browser AI-assisted terminal,
live remote-desktop screen/input from the dashboard, a plugin system, and a RAG-backed knowledge base
over user documents. Stated safety controls: tool-approval gates, user-editable shell-command
guardrails, and PII redaction.

**Model providers.** Configured per agent (dashboard or `octop provider` CLI): OpenAI-compatible
APIs, DashScope (Qwen), Ollama, and other presets — model-agnostic rather than tied to one vendor.

**Deployment.** A one-line installer script (macOS/Linux, using `uv` to provision Python 3.12 under
`~/.octop/`), PowerShell/batch installers for Windows, `pip install octop` from PyPI, Docker
(`docker-compose.yml` or a build script), and native desktop apps for Windows/macOS/Linux plus FnOS
NAS packages. First run is `octop init` then `octop run`, serving a local dashboard at
`http://127.0.0.1:8088`; `octop service start` runs it as a system service. The companion repos
`TencentCloud/octop-harness`, `octop-gateway`, `octop-memory`, and `octop-browser` are each split out
as separate projects.

**Claude Code tie-in.** Claude itself is not otherwise discussed in the README; the only first-party
integration found is Claude Code as one of the outbound ACP coding-agent targets Octop can delegate
work to, alongside OpenCode, CodeBuddy, and Codex — Octop is a multi-provider orchestrator in which
CC is one of several backends, not the primary surface.

**Roadmap** (per the README, accessed 2026-10-09): shipped items include the shared expert resource
pool, expert sharing, and the PC desktop client; in progress are AgentTeams (Beta) and a closed-beta
mobile client; planned items include self-evolution, a plugin marketplace, managed agents, and a
cloud-edge continuum.

## Adoption Decision

**Assess.** Octop is a young but fast-growing project (created 2026-07-08; 8,189 stars/991 forks
within three months) with a concrete, documented architecture — ADRs for the single-process model
and database backends, a stated rationale for the shared-registry design — rather than only
marketing claims, a stronger documentation posture than many single-README entries in this corpus.
Its outbound-ACP delegation to Claude Code (alongside OpenCode, CodeBuddy, Codex) is a concrete,
first-party CC-adjacent integration point, and its multi-user, per-row-isolated single-process design
is a distinct architecture from this corpus's other self-hosted-assistant entries
([Odysseus][odysseus], AGPL-3.0, single-user-oriented; [QwenPaw][qwenpaw], Apache-2.0,
channel-breadth-focused): Octop's isolation model and AgentTeams coordinator are the differentiating
facts worth tracking.

Against that: the project is pre-1.0 (`v1.0.2b6`), its multi-user isolation rests on row-level checks
inside one shared process rather than per-user sandboxing, and the one memory-internals doc fetched
(`docs/memory-slim.md`) documents only maintenance mechanics, not how hierarchical recall actually
ranks or retrieves memories. No independent security or scaling review was found. **Assess** — track
it for the self-hosted, multi-user-isolation design pattern; revisit once AgentTeams and the planned
self-evolution roadmap items ship.

## Action Items

- Re-verify the release tag and star/fork counts at the next refresh — both move fast on a young,
  high-growth repo.
- If a future pass inspects `octop-memory` directly, confirm (or correct) the "hierarchical recall
  with full-text search" claim against that repo's own source rather than README prose.
- Watch for the planned self-evolution feature — it would make Octop comparable to
  [MOSS][moss] and [Raven][raven] in this corpus's self-evolving-harness cluster.

## Cross-References

- [agentic-enterprise-os-landscape.md § Tier 2][eos-tier2] — Octop as an open-source
  self-operating workspace, alongside AutoAgent, Odysseus, Goose, multica, and HugAgentOS
- [odysseus-analysis.md][odysseus] — a single-user self-hosted all-in-one AI workspace, contrasted
  with Octop's multi-user row-isolation model
- [qwenpaw-analysis.md][qwenpaw] — a channel-breadth-focused self-hosted personal assistant,
  contrasted with Octop's multi-user/AgentTeams focus

## Sources

| Source | Content |
|---|---|
| [TencentCloud/Octop README][octop-gh] | Tagline, who-it's-for framing, AgentTeams description, feature summary (connectors, ACP, browser/terminal/remote-desktop, plugins, knowledge base), model providers, deployment paths, roadmap — accessed 2026-10-09 |
| `gh api repos/TencentCloud/Octop` | Stars (8,189), forks (991), license (MIT), created (2026-07-08), language (Python) — accessed 2026-10-09 |
| `gh api repos/TencentCloud/Octop/contents/LICENSE` | License text confirmed MIT directly from the LICENSE file — accessed 2026-10-09 |
| `gh api repos/TencentCloud/Octop/releases/latest` | Latest tag `v1.0.2b6`, published 2026-10-04 — accessed 2026-10-09 |
| [`docs/architecture.md`][octop-arch] | Single-process model, layering, multi-user row-level isolation, stated design rationale — accessed 2026-10-09 |
| [`docs/memory-slim.md`][octop-memslim] | Memory maintenance mechanics (backup/compaction), LangGraph SQLite checkpointer — accessed 2026-10-09 |

[octop-gh]: https://github.com/TencentCloud/Octop
[octop-arch]: https://github.com/TencentCloud/Octop/blob/main/docs/architecture.md
[octop-memslim]: https://github.com/TencentCloud/Octop/blob/main/docs/memory-slim.md
[odysseus]: odysseus-analysis.md
[qwenpaw]: qwenpaw-analysis.md
[moss]: moss-self-evolving-agent-analysis.md
[raven]: ../orchestrators/raven-analysis.md
[eos-tier2]: ../frameworks/agentic-enterprise-os-landscape.md#tier-2--open-source-self-operating-workspaces--runtimes
