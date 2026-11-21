---
title: CC Memory Tooling Landscape
purpose: Persistent cross-session memory tools that integrate with Claude Code — ByteRover, Claude-Mem, MemPalace, MemSearch, Roampal Core, plus cross-agent/procedural-memory tools (agent-memory, ai-memory, claude-reflect, Core, CortexDB, deja-vu, engrim, Leviathan, Operator Memory), plus second-brain vault tools (gbrain, COG-second-brain, open-second-brain, agent-second-brain, claude-second-brain).
status: research
created: 2026-06-14
updated: 2026-11-17
validated_links: 2026-10-06
---

Persistent-memory tools for Claude Code. Split out of [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) (which keeps the cross-tool comparison table). For non-CC memory *infrastructure* (Mem0, Zep/Graphiti, Cognee, LangMem, A-MEM), see [agent-frameworks-infrastructure-landscape.md § Agent Memory Infrastructure](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#4-agent-memory-infrastructure). CC's native memory: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md).

## Memory Taxonomy

Agent memory is conventionally split into four modules ([CoALA][coala], arXiv:2309.02427):

- **Working** — active in-context state for the current decision cycle; transient.
- **Episodic** — records of past interactions/experiences, retrievable across sessions.
- **Semantic** — persistent facts about the world, the user, and the domain.
- **Procedural** — encoded behavior: implicit in model weights, explicit in system prompt / agent code.

[LangMem][langmem] maps its API most directly to the semantic/episodic/procedural split ([conceptual guide][langmem-concepts]); the others use their own scheme (OS-style tiers, memory blocks, temporal graphs) that only *approximately* aligns. The table normalizes the non-CC frameworks onto the CoALA axes — full descriptions live in [agent-frameworks-infrastructure-landscape.md §4][non-cc-mem] (not duplicated here):

| Framework | Working | Episodic | Semantic | Procedural | Primary backend |
|---|:-:|:-:|:-:|:-:|---|
| [Mem0][mem0] | ~ | ✓ | ✓ | — | Vector (+ optional graph) |
| [Cognee][cognee] | ~ | ✓ | ✓ | — | Relational + vector + graph |
| [Letta / MemGPT][letta] | ✓ | ✓ | ✓ | — | In-context blocks + external store |
| [Zep / Graphiti][graphiti] | — | ✓ | ✓ | — | Temporal graph + vector + BM25 |
| [A-MEM][a-mem] | — | ✓ | ✓ | — | Vector (ChromaDB) |
| [LangMem][langmem] | — | ✓ | ✓ | ✓ | KV / DB-backed store |
| [MemoryOS][memoryos] | ✓ | ✓ | ✓ | — | File-based (+ ChromaDB) |

Legend: ✓ explicit layer · ~ partial/implicit · — not a documented layer. Mappings are approximate — each project names its tiers differently; only LangMem ships an explicit *procedural* layer.

**Design lens — memory should change future behavior.** Beyond *what is stored*, the test for any of these layers is whether a stored item actually alters a later decision. André Lindenberg frames memory as a first-class component judged by behavior change — a "skillbook" that updates after tasks, failures, and feedback, not a passive transcript (Lindenberg, *Memory should change future behavior*, LinkedIn, 2026). It reframes episodic/procedural memory as the loop that lets an agent compound rather than merely recall — the same write-back-and-reuse intent behind this repo's CRLA/`docs/learnings/` flow.

## agent-memory (tigerless-labs)

**Repo**: [tigerless-labs/agent-memory][agent-memory] | **Stars**: 1,692 | **License**: MIT | **Version**: 0.1.0 (README badge; no tagged GitHub release as of 2026-09-30, `gh api` — install from a checkout, no PyPI package yet)

Long-term memory runtime pitched as "the two lines" of prior memory architecture in one store: a retrieval engine (ranking, links-as-graph) indexing a plain markdown filesystem the agent can still `ls`/`grep` directly. Markdown files are the single source of truth; the SQLite/FTS5 index beside them is a deletable cache.

### Architecture

- **Three read tracks**: deterministic `MEMORY.md` injection at session start; BM25 recall over FTS5 (optional vector plugin fused by RRF); the plain directory tree as a last resort
- **Path-then-level retrieval**: `mem recall` returns an L0 index (abstract, path, anchor, score); the agent opens a hit at `outline`, `abstract`, or `full` depth, or `mem trace <name>` for the cited raw messages
- **Validity-interval versioning**: each memory carries `valid_from`/optional `invalid_at`; `mem correct`, `mem supersede`, and `mem merge` don't destroy history — replaced/deleted files stay in the store for `recall --as-of <date>` and `trace`
- **Schema-driven types**: one schema file per memory type under `schemas/`; `config.toml` holds every tunable and refuses an unknown knob at load
- **Sleep-time Manage layer with authority tiers**: an unattended pass may add/update; deletion only ever arrives as a proposal a human confirms
- **No LLM client in the library**: zero API keys required for core read/write; judgment is borrowed from the host agent's own CLI, so every write stays visible in that agent's transcript

### CC Integration

Claude Code and Codex CLI (and "anything else that can run a shell command") share one store via `mem`/`mem-mcp`/`mem-hook` binaries built with `uv sync --all-packages`. The README's own benchmark claims **"one store, three hosts"**: all 9 ordered writer/reader pairs across Claude Code, Codex CLI, and Hermes passed — what one host's shell writes, another's `mem recall` finds, specifics intact (self-reported, `docs/experiments.md` and `experiments/` ship with the source for independent replay).

### Adoption Considerations

**Strengths**: cross-agent sharing that ships its own replayable experiment ledger rather than only a headline number; `rm -rf .index/ && mem rebuild` losing zero knowledge is "enforced by a test, not promised in a doc" (per the README); validity-interval versioning (`--as-of`, supersede-not-overwrite) is more thorough than most peers in this doc; no LLM/API-key dependency for core operation.

**Risks**: pre-1.0 (v0.1.0), no PyPI package — install from a git checkout; its own self-reported LongMemEval-S comparison (52.9% pooled accuracy vs. 35.8% for a "MemCore W2" baseline and 5.8% with no memory, 120 episodes, Haiku 4.5 host, Sonnet 5 judge) is explicitly flagged by the README itself as **not comparable to published LongMemEval scores** — the haystack is bounded to 12 sessions per episode, so treat it as a write-strategy study, not a benchmark result. Overlaps with CC's built-in memory and every other cross-agent tool in this doc — pick one.

### Rubric

Scored 2026-09-30, evidence from the [README][agent-memory] unless noted.

`subject: memory`

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| yes | no | yes | yes | yes | yes |

- **Shared — yes**: "one store, three hosts" — all 9 writer/reader pairs across Claude Code, Codex CLI, and Hermes pass.
- **Distributed — no**: a local directory (`~/agent-memory-store` by default); no multi-machine sync or remote service is documented, only multi-agent access to one local store.
- **Reproducible — yes**: "files are the truth; every index is a rebuildable cache" — `rm -rf .index/ && mem rebuild` is asserted to lose zero knowledge, "enforced by a test."
- **Adaptable — yes**: one schema file per memory type under `schemas/`, plus a fully tunable `config.toml` that refuses unknown keys.
- **Versionable — yes**: `valid_from`/`invalid_at` validity intervals; `correct`/`supersede`/`merge`/`delete` preserve prior state for `recall --as-of` and `trace` rather than overwriting it.
- **Traceable — yes**: `mem trace <name>` returns cited raw messages; an append-only `archive/provenance/` keeps distillation evidence "forever."

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## ai-memory (akitaonrails)

**Repo**: [akitaonrails/ai-memory][ai-memory] | **Stars**: 16,057 (2026-11-17; was 8.2K at last review) | **License**: MIT | **Version**: v3.4.7 (2026-11-15; was 2.4.0 at last review)

Rust-based cross-agent long-term memory: "Quit Claude Code mid-task, start OpenAI Codex in the same directory, continue without re-explaining the architecture" ([README][ai-memory]). A git-backed Markdown wiki is the source of truth (`wiki/` pages, `raw/` sanitized transcript segments), with a derived SQLite index (FTS5 + local embeddings) for retrieval — the same "plain-text is durable, index is disposable" pattern MemSearch uses below.

### Architecture

- Lifecycle hooks capture observations silently during a session; session-end consolidation writes readable wiki pages
- Next session gets a bounded briefing plus full-text/entity search over prior sessions
- Typed, claim-once handoff protocol between agents — the next agent to open the directory gets a structured handoff, not a raw transcript dump
- Zero-LLM default: full-text search, entity matching, and handoffs work without any API calls; local embedding models are optional

### CC Integration

Registers via MCP. Claude Code is one of "twenty-plus harnesses" sharing the store — Codex, Cursor, Gemini CLI, OpenCode, Grok, Devin, Kimi, Kiro, and more, per the README.

### Adoption Considerations

**Strengths**: Markdown-native (grep-searchable, no binary lock-in), no API key required for core functionality, multi-user/multi-machine with per-user handoffs isolated, access-weighted retention (frequently-used memory decays slower than cold notes).

**Risks**: Overlaps with CC's built-in memory and the other cross-agent tools in this doc — pick one if the need is CC-only. README install instructions are Arch/AUR-centric (`ai-memory-bin` prebuilt, or `ai-memory` built from source); check platform support before adopting elsewhere.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## ByteRover CLI (campfirein)

**Repo**: [campfirein/byterover-cli][byterover] | **Stars**: 4.1K | **License**: Elastic License 2.0 | **Paper**: [arXiv:2604.01599][byterover-paper]

Portable memory layer for autonomous coding agents. Persistent hierarchical context trees (Domain→Topic→Subtopic→Entry) with cloud sync and sub-100ms retrieval without vector databases.

### Architecture

- **Context Tree**: LLM-curated hierarchical knowledge storage in human-readable markdown
- **Adaptive Knowledge Lifecycle**: Importance scoring + recency decay
- **5-tier progressive retrieval**: Escalates to LLM reasoning only for novel queries
- **MCP integration**: `brv mcp` starts an MCP server for CC to access memory natively

### CC Integration

ByteRover integrates with Claude Code via MCP protocol. Run `brv mcp` to expose the memory layer as an MCP server, giving CC access to persistent cross-session knowledge, semantic search, and context tree operations.

### Adoption Considerations

**Strengths**: Research-backed ([arXiv:2604.01599][byterover-paper] — SOTA on LoCoMo benchmark), 20+ LLM provider support, cloud sync with SOC 2 Type II, active development (48 releases, 2,391 commits).

**Risks**: Elastic License 2.0 (not OSS — requires commercial agreement for production). Cloud dependency for sync features. Overlaps with CC's built-in memory system (`~/.claude/memory/`). Standalone daemon CLI — install alongside CC via MCP, not embeddable in plugins.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## Claude-Mem (thedotmack / Alex Newman)

**Repo**: [thedotmack/claude-mem][claude-mem] | **Stars**: 115.2K (`gh api`, 2026-11-09) | **License**: Apache-2.0 | **Version**: v15.13.0 (2026-11-09)

Persistent memory compression system, started for Claude Code and now cross-agent. A second "observer" agent turns the session's tool activity into observations and summaries, and the next session starts with a short index that pulls in details only when needed. The README says it "Works with Claude Code, Codex, Cursor, OpenCode and 11 more agents", and that Copilot CLI, Goose, Roo Code and Warp can search the memory but their sessions aren't recorded. Placement stays here because the hook, plugin and MCP surface is the analysis focus (see [CONTRIBUTING § Classification](../../CONTRIBUTING.md#classification-cc-community-vs-non-cc)).

### Architecture

| Component | Purpose |
|-----------|---------|
| **Lifecycle Hooks** (9 on Claude Code) | Setup, SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PostToolUseFailure, Stop, SubagentStop, SessionEnd; one adapter per agent in `src/cli/adapters/` |
| **Worker Service** | Local HTTP worker managed by Bun; per-user default port `37700 + (uid % 100)` (`CLAUDE_MEM_WORKER_PORT` overrides), memory viewer at `/viewer` ([configuration][claude-mem-config]) |
| **SQLite Storage** | `~/.claude-mem/claude-mem.db`: sessions, observations, summaries with FTS5 full-text search; cloud sync is opt-in |
| **Chroma Vector DB** | Hybrid semantic/keyword search |
| **MCP Tools** | 3-layer progressive disclosure workflow |

### MCP Search Pattern (Token-Efficient)

| Tool | Purpose | Cost |
|------|---------|------|
| `search` | Compact index retrieval with IDs | ~50–100 tokens/result |
| `timeline` | Chronological context around observations | moderate |
| `get_observations` | Full detail for filtered IDs | ~500–1,000 tokens/result |

Progressive disclosure: start with index → assess via timeline → fetch full detail only for relevant matches. Estimated **10x token savings** over naive retrieval.

### Installation

```bash
npx claude-mem install                          # CLI install
/plugin marketplace add thedotmack/claude-mem   # marketplace install
```

**Note**: npm global install provides only the SDK library; proper plugin registration requires `npx claude-mem install`.

### Key Features

- AI-compressed semantic summaries of session activity
- Automatic context injection into new sessions
- `<private>` tags for content exclusion
- Citation system referencing past observations by ID
- Web viewer UI at `/viewer` on the worker port
- Observer model: the hosted "claude-mem observer" (30-day trial at a checkout page), your own OpenRouter or Gemini key, or your Anthropic plan
- Real-time observation feeds to Telegram, Discord and Slack, now described only in the OpenClaw installer path

### Live Observer Architecture

A dedicated observer AI watches each session in real-time, generating searchable observations with before-and-after context — capturing causality and decision chains, not just snapshots. Observations are auto-categorized by type (decisions, bugfixes, features, discoveries) and queryable by file path or semantic concept (e.g., "decisions about token refresh").

### RAD Protocol (announced earlier, not in the current README)

**Real-Time Agent Data** — an open protocol for how AI agents capture and retrieve working memory, announced as a counterpart to RAG. The README no longer mentions it (checked 2026-11-09); whether it was dropped or moved is unverified.

### Adoption Considerations

**Strengths**: 115.2K stars (2026-11-09), progressive disclosure saves tokens, hybrid search (FTS5 + vector), cross-agent adapters, web UI for browsing history, [dedicated docs site][claude-mem-docs].

**Risks**: Heavy dependencies (Bun + uv + Chroma). Overlaps with CC's built-in memory system and ByteRover. The README states "Anonymous usage analytics are on by default" (`npx claude-mem telemetry disable` turns them off). The hosted observer and cloud sync are paid or opt-in services next to the Apache-2.0 core.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## claude-reflect (BayramAnnakov)

**Repo**: [BayramAnnakov/claude-reflect][claude-reflect] | **Stars**: 1.7K | **License**: MIT | **Version**: 3.2.0

Self-learning Claude Code plugin that "captures corrections and discovers workflow patterns — turning them into permanent memory and reusable skills" ([README][claude-reflect]). Distinct from the session-recall tools in this doc: it targets the taxonomy's *procedural* layer (behavior correction), not episodic/semantic recall.

### Architecture

- **Capture (automatic)**: hooks detect corrections via hybrid regex + AI-powered semantic matching, queuing them with confidence scores
- **Review (manual)**: `/reflect` presents queued learnings for approval/edit/skip before syncing
- **Skill discovery**: `/reflect-skills` analyzes session history to find repeating task patterns that could become reusable commands/skills
- Semantic deduplication consolidates similar entries; can backfill from historical sessions predating install

### CC Integration

Installs via the Claude Code plugin marketplace; hooks auto-configure on install. Syncs learnings to `CLAUDE.md` (global and project-level), `AGENTS.md`, and skill files under `.claude/commands/`.

### Adoption Considerations

**Strengths**: Targets the taxonomy's procedural layer specifically — few other tools in this doc do; human-in-the-loop review before anything is written; can recover pre-install learnings from session history; MIT.

**Risks**: Regex + semantic correction detection can mis-fire on ambiguous phrasing (mitigated, not eliminated, by the manual `/reflect` review step). Writes directly into `CLAUDE.md`/`AGENTS.md`, which needs periodic pruning like any growing instructions file.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## CortexDB (liliang-cn)

**Repo**: [liliang-cn/cortexdb][cortexdb] | **Stars**: 479 | **License**: MIT | **Version**: Go module v2, `gh api` 2026-11-12

Pure-Go AI memory and knowledge graph in one SQLite file — "no service to run, works without an embedding model" ([README][cortexdb]). Combines vector search (HNSW/IVF/flat/binary), FTS5 full-text, RAG knowledge, scoped agent memory, and an RDF 1.2 knowledge graph (SPARQL 1.1/1.2, OWL 2 RL inference, SHACL validation, read-only Cypher) plus a Palantir-style governed-action ontology, behind 100+ tools exposed in-process or over MCP.

### Architecture

- **Vectors + graph + FTS in one file**: HNSW/IVF/flat/binary vector indexes, FTS5 full-text, hybrid and graph retrieval; an `EmbeddedConfig` mode opens 100k 768-d vectors in 0.28s with a 193MB heap for small devices
- **RDF knowledge graph**: SPARQL 1.1/1.2, RDFS + OWL 2 RL inference, SHACL Core + SHACL-SPARQL — the README states it passes the W3C SPARQL, RDF 1.2 and SHACL test suites (RDFS/OWL 2 RL covered by the repo's own tests)
- **Versioned history**: every entity/relation/triple/schema change is kept with `as_of` queries on SPARQL, find, expand and Cypher, plus a live 3D graph viewer (`serve_graph_3d`) with an Entity page showing why a value is in effect and what it replaced
- **`import_agent_memory`**: pulls in what Claude Code, Codex and DeepSeek Harness already remember — memory notes, `CLAUDE.md`/`AGENTS.md`, Codex memories, optionally past sessions distilled into memories

### CC Integration

| Surface | Mechanism |
|---|---|
| Plugin | `/plugin marketplace add liliang-cn/cortexdb`, `/plugin install cortexdb@cortexdb` — gives Claude Code one global brain at `~/.cortexdb/cortexdb.db`, `/remember`/`/recall`, and an auto-recall hook |
| Mod (early access) | `cortexdb-live`: Haiku plans each recall before the brain is searched (so a bare "ok" searches nothing), a status line names the active brain/node-count/recall latency, and 90 seconds of session idle triggers Haiku to distil new durable memories — run on Claude Code's own model access, no separate API key |

### Adoption Considerations

**Strengths**: single-file, zero-dependency Go binary (no vector DB or server required, unless sharing one brain over the optional `cortexdb-grpc`); the RDF/SPARQL/SHACL layer is a standards-conformant knowledge graph rather than a marketing label; distinguishes verified facts from guesses and marks superseded memories rather than deleting them.

**Risks**: young project (created 2025-08-07) relative to its star count; the Claude Code mod is explicitly "early access"; overlaps with CC's built-in memory and every other cross-agent tool in this doc — pick one. The social post that queued this entry cited "80+ MCP tools" — the current README states "100+ tools," so the count has grown since whatever version prompted the post.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## Core (RedPlanetHQ)

**Repo**: [RedPlanetHQ/core][core] | **Stars**: 2K | **License**: AGPL-3.0 | **Version**: 0.7.20

Self-hosted "Personal AI OS" — broader in scope than the other tools in this doc: it indexes email, meetings, GitHub, Linear, Slack, and conversation history into a persistent memory layer, then acts on it via voice, chat, and messaging (WhatsApp/Slack/Telegram) interfaces, not just as a coding-agent sidecar.

### CC Integration

"CORE spins up Claude Code or Codex sessions with the full task context, runs them on your machine or in Docker/Railway, and opens a PR when done. Sessions keep running when your laptop is closed" ([README][core]). It can point at an existing Claude Pro or Codex subscription instead of a separate API key (a "subscription proxy," per the docs).

### Adoption Considerations

**Strengths**: 50+ MCP app connectors (GitHub, Linear, Jira, Slack, Gmail, and others) feed the same memory the coding sessions draw on; self-reported **88.24%** average accuracy on the [LoCoMo benchmark][core-benchmark] across single-hop, multi-hop, open-domain, and temporal reasoning; CASA Tier 2 certified, TLS 1.3 in transit, AES-256 at rest.

**Risks**: AGPL-3.0 — copyleft, not permissive. Self-hosting requires Docker 20.10+/Compose 2.20+ and 4 vCPU/8 GB RAM, a heavier footprint than any other tool in this doc. Coding-agent delegation is one feature among many (task automation, messaging, browser/terminal access) — evaluate it as a full OS, not a drop-in memory layer, if CC memory is the only need.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## deja-vu (vshulcz)

**Repo**: [vshulcz/deja-vu][deja-vu] | **Stars**: 935 | **License**: MIT | **Version**: 0.21.1

Local memory index built from session history already on disk — "one memory shared by Claude Code, Codex, Cursor, Copilot CLI, OpenClaw and 29 more coding agents... including months of sessions from before you installed it" ([README][deja-vu]). A single Go binary; no LLM or embeddings required for core retrieval (optional semantic recall via local Ollama or OpenAI endpoints).

### Architecture

- Local inverted index in `~/.cache/deja`, parsing each agent's existing JSONL/SQLite session stores directly — retroactive, no re-indexing needed for prior history
- MCP server for tool integration; Claude Code gets automatic session-start recall, captured before compaction discards it
- Keys and tokens are stripped as the index is built (documented in its [security model][deja-vu-security])

### Adoption Considerations

**Strengths**: Retroactive indexing parses each agent's *existing* on-disk session stores directly, so months of pre-install history become searchable immediately — no separate backfill step (claude-reflect above can also recover pre-install learnings, but only by re-scanning sessions through its own capture pipeline); no LLM or embedding dependency for core full-text search; self-reported **88.1% hit@1 on LongMemEval-S** and **70.5% retrieval hit@1 on LoCoMo**, both reproducible in-repo against the public datasets (see [Benchmarks](#benchmarks) below); millisecond lookups.

**Risks**: Overlaps with CC's built-in memory and every other tool in this doc — pick one. Depends on each agent's own on-disk session format; a harness that changes its log layout could break parsing until deja-vu updates. Pre-1.0 (v0.21.1).

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## engrim (timgordontg)

**Repo**: [timgordontg/engrim][engrim] | **Stars**: 283 | **License**: MIT | **Version**: 1.4.11

Local-first SQLite episodic-memory store aimed at the "200,000-token context window trap": rather than replaying raw transcripts, it distills project memory into "4,000 characters of high-precision, curated episodic working memory" in a single file (`~/.engrim/memory.db`, WAL mode, restrictive POSIX permissions) ([README][engrim]).

### Architecture

- Hybrid retrieval: BM25 full-text search (FTS5) + vector embeddings via `model2vec`
- Native adapters for seven environments: Claude Code (SessionStart/Stop hooks), Codex CLI (command hooks), Cursor and Windsurf (MCP), GitHub Copilot CLI, OpenCode (plugin + MCP), and Google Antigravity
- Tracks `origin_agent` provenance per entry, so a team can see which agent/environment contributed a given decision

### Adoption Considerations

**Strengths**: Only tool in this doc with a Google Antigravity adapter (alongside Claude Code, Cursor, Codex CLI, Copilot CLI, OpenCode, and Windsurf — seven environments total); per-entry `origin_agent` provenance lets a team see which agent contributed a given decision; tiny on-disk footprint (single SQLite file); MIT, with an optional commercial variant for teams rather than a required upsell.

**Risks**: Overlaps with CC's built-in memory, ai-memory, and deja-vu above — three cross-agent stores in this doc alone; pick one. Smaller community than its cross-agent peers here (283 stars vs. ai-memory's 8.2K (16,057 on 2026-11-17) and deja-vu's 935). No third-party or public benchmark number, unlike ByteRover/MemPalace/deja-vu.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## Leviathan (elstongun)

**Repo**: [elstongun/leviathan][leviathan] | **Stars**: 881 | **License**: Apache-2.0 | **Version**: Rust 1.88+ (README badge), `gh api` 2026-11-12

Single static Rust binary that turns records (JSONL, JSON, CSV/TSV, SQLite, or any database CLI's output) into a ranked full-text (FTS5 + BM25) index, so an agent gets "the few records that answer the question" instead of grepping raw history ([README][leviathan]). A separate, opt-in **memory** mode lives in its own SQLite file: the agent `remember`s one claim at a time keyed so a later write replaces rather than contradicts the old value, and `recall` returns only what fits a token budget.

### Benchmarks (self-reported, synthetic maintenance-log dataset, `docs/BENCHMARKS.md` and `docs/MEMORY.md`)

| At 1M records (678 MB) | Leviathan | best grep strategy |
|---|---:|---:|
| Median tokens per question | 436 | 107,122 (245×) |
| Relevant record in top 5 | 99.0% | 96.0% (within a 30K-char cap) |

| After 300 sessions | Leviathan memory | MEMORY.md, whole file |
|---|---:|---:|
| Tokens at session start | 736 | 33,313 |
| Stale value in context | 0% | 73.8% |

Both tables are the project's own methodology on one synthetic dataset — "nothing in Leviathan is specific to it," per the README — not an independent benchmark; treat the multiples as directional.

### CC Integration

CLI + skill (`skills/leviathan` and `skills/leviathan-memory`, copied into `~/.claude/skills/`, costs 0 tokens until used) or an optional MCP server (`leviathan mcp`, five read-only stdio tools). `leviathan wrap claude --memory --hooks --rules --apply` configures tools, a session-start briefing and an always-on rule specifically for Claude Code; `leviathan wrap` also targets Codex, Cursor, Gemini CLI, Windsurf and the rest of the 24 agents the README lists. `leviathan memory import ~/.claude/projects/<project>/memory/MEMORY.md` migrates an existing CC memory file in.

### Adoption Considerations

**Strengths**: no runtime dependencies (one SQLite-backed binary); works over arbitrary tabular exports, not just code or chat logs, so it doubles as a support-ticket/log search tool; the memory mode is separate from the search index, so adopting one doesn't require the other; Apache-2.0.

**Risks**: young (created 2026-10-05); the 245× and token-saving figures are self-reported on one synthetic dataset; overlaps with CC's built-in memory and every other cross-agent tool in this doc if the memory mode is adopted — pick one.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## MemPalace (milla-jovovich)

**Repo**: [milla-jovovich/mempalace][mempalace] | **Stars**: 33.6K | **License**: MIT | **Version**: 3.0.0

Local-first AI memory system storing conversation histories verbatim using a spatial "palace" metaphor. Achieved 96.6% R@5 on [LongMemEval benchmark][longmemeval] — the highest published result — without cloud dependencies.

### Palace Architecture

| Layer | Metaphor | Purpose |
|-------|----------|---------|
| **Wings** | Projects or people | Top-level partitioning |
| **Rooms** | Topic categories | Within-wing organization |
| **Halls** | Memory types | Cross-wing shared categories (facts, events, discoveries) |
| **Closets** | Summaries | Pointers to original content |
| **Drawers** | Verbatim files | Raw original data |
| **Tunnels** | Cross-references | Links between rooms across wings |

34% retrieval improvement over unstructured search from this hierarchical organization.

### Memory Stack

| Layer | Content | Size | Timing |
|-------|---------|------|--------|
| L0 | Identity/system prompt | ~50 tokens | Always loaded |
| L1 | Critical facts | ~120 tokens (AAAK) | Always loaded |
| L2 | Room recall (recent sessions) | On demand | When topic emerges |
| L3 | Deep semantic search | On demand | When explicitly queried |

### CC Integration

```bash
claude plugin marketplace add milla-jovovich/mempalace   # marketplace install
claude mcp add mempalace -- python -m mempalace.mcp_server  # MCP install
```

19 MCP tools for search and memory operations. Also supports ChatGPT, Cursor, Gemini, and local models (Ollama, Mistral).

### Adoption Considerations

**Strengths**: Highest published LongMemEval score (96.6% raw mode, reproducible via `/benchmarks`). Free and fully local. ChromaDB + SQLite knowledge graph. Specialist agent support with per-agent memory wings.

**Risks**: AAAK compression is lossy and regresses to 84.2% ([README candid note][mempalace]). Overlaps with CC's built-in memory, ByteRover, and Claude-Mem. ChromaDB dependency adds install complexity.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

---

## MemSearch (zilliztech)

**Repo**: [zilliztech/memsearch][memsearch] | **Stars**: 2K | **Forks**: 184 | **License**: MIT | **Version**: v0.4.8 (2026-06-15)

Persistent, cross-session semantic memory for AI coding agents from the Milvus/Zilliz team. Stores conversation history as human-readable Markdown and indexes it with Milvus for hybrid vector + BM25 search. Unlike MCP-based memory tools, it ships as a **native Claude Code plugin** — "4 shell hooks + 1 skill + 1 watch process, no MCP, no sidecar service" ([CC plugin docs][memsearch-docs]).

### Architecture

- **Markdown is the source of truth** (`.memsearch/memory/*.md`); the Milvus index is a derived "shadow" cache, rebuildable at any time
- **3-layer progressive retrieval**: search → expand → transcript
- **Hybrid search**: dense vector embeddings + BM25 sparse + RRF reranking
- **Local-first embeddings**: ONNX bge-m3 int8 by default (CPU, no API key); pluggable to OpenAI, Google, Voyage, Ollama
- **SHA-256 dedup** avoids re-indexing unchanged content; a live file watcher auto-indexes edits
- **Backend options**: Milvus Lite (embedded default), self-hosted Milvus, or Zilliz Cloud (free tier)

### CC Integration

```bash
/plugin marketplace add zilliztech/memsearch
/plugin install memsearch
```

The memory-recall skill runs in a `context: fork` subagent, so intermediate search results never pollute the main context — and because there is no MCP server, no tool definitions consume context tokens permanently. The same Markdown store is shared across Claude Code, OpenCode, Codex CLI, and OpenClaw.

### Adoption Considerations

**Strengths**: Zero permanent context overhead (no MCP tool defs); human-readable Markdown that survives index loss; local embeddings need no API key; one memory store across multiple agent CLIs.

**Risks**: Overlaps with CC's built-in memory, Claude-Mem, MemPalace, and ByteRover — pick one. Milvus/Zilliz dependency for the index. Pre-1.0 (v0.4.8), active release cadence. Distinct from Zilliz's separate `claude-context` code-search MCP — do not conflate the two.

Cross-ref: [CC-remote-access-landscape.md](../cc-native/ci-remote/CC-remote-access-landscape.md) — memsearch as a mobile/remote supporting tool

---

## Operator Memory (aerovato)

**Repo**: [aerovato/operator-memory][operator-memory] | **Stars**: 359 | **License**: BSD-3-Clause |
**Version**: Operator Helper `helper@v1.8.0` (repo release tags, `gh api`, 2026-10-06)

Cross-agent "self-improving context engine for coding agents" (repo description field, verbatim) built
on canonical Markdown documents rather than vector/embedding recall. The README states every session
runs the same loop: *"1. **Consult** — the agent starts from your Brain: instructions, codebase index,
specs, guides. 2. **Build** — the agent does normal development work, informed by that knowledge.
3. **Update** — the agent records what changed: new specs, decisions, standards, lessons."* A listed
feature: *"Zero Infrastructure — No background agents, no embeddings, no vector database, no model
configuration."*

### Architecture

- **Three storage tiers**: `.operator/` (private, machine-local project knowledge), `.operator-shared/`
  (project knowledge committed with the repo), `~/.operator/user/` (personal rules/knowledge reused
  across projects)
- Canonical files are updated in place by the agent itself as part of ordinary work; retrieval at
  session start is a Claude Code **hook** (`packages/claude-code/hooks/hooks.json`, described in its
  own metadata as "Operator Memory preamble injection" — checked via the GitHub contents API,
  2026-10-06), not a background service or MCP server. `docs/architecture.md` states session start is
  "a small, deterministic orientation... Nothing is ranked, guessed, or retrieved by similarity" — the
  *retrieval* path is deterministic; the *content* of the Brain is still authored by whichever agent/
  model is running the session, with "no model configuration" pinned anywhere
- Installed via the `@aerovato/operator-helper` npm package (global install), then a per-harness
  `operator-helper install <harness>` step; slash commands `/operator:user-init` (once) and
  `/operator:project-init` (per project) scaffold the three tiers

### CC Integration

The README's own harness table lists three support tiers. Claude Code (CLI + Desktop) is one of five
marked **Fully Supported** (🟢), alongside Codex (CLI + Desktop), OpenCode V2, Pi, and DeepSeek Harness;
OpenCode V1 is **Supported, Legacy** (🟡) and Kiro is **Supported** (🟡, not "fully") — seven harnesses
across three tiers, not seven at the same tier. Six of the eight `packages/` directories carry
independent GitHub release tags (`codex@`, `deepseek@`, `helper@`, `opencode@`, `opencode-v2@`, `pi@` —
36 tags total, `gh api`, 2026-10-06); `claude-code` and `core` have directories but no tags of their
own, and Kiro — the lowest support tier — has no `packages/` directory at all (`gh api` contents
listing, 2026-10-06).

### Adoption Considerations

**Strengths**: BSD-3-Clause (permissive); Markdown-native and git-trackable, so the knowledge store is
diffable/reviewable like code; "Zero Infrastructure" — no embeddings, vector DB, or model config to
stand up; six of eight harness packages carry independent release tags, suggesting active, scoped
maintenance; the private/shared/personal tiers map onto a team's actual read/write boundaries without
extra config.

**Risks**: small community relative to peers in this doc (359 stars vs. deja-vu's 935 or ai-memory's
8.2K, 16,057 on 2026-11-17); only 5 of 7 listed harnesses are "Fully Supported" — OpenCode V1 and Kiro carry a lower support
tier per the README's own table; no pinned-model or deterministic-rebuild claim is documented for the
Update step itself — only the retrieval/orientation path is stated to be deterministic, not the Brain's
content generation (the agent authoring the Markdown each session is whichever model the harness is
running, unpinned). Overlaps with CC's built-in memory and every other cross-agent tool in this
doc — pick one.

**No rubric row.** The one open cell in the agent-substrate matrix is **context·Reproducible**
([agent-substrate-reference-architecture.md][sub-arch]). Operator Memory's Brain content is authored by
the session's own (unpinned) agent/model — no checksum, pinned version, or rebuild-from-source command
is documented for that write step — the same shape as CLAUDE.md/AGENTS.md, which the reference
architecture already holds at `no data` on Reproducible. A more generous reading could call the
*retrieval* path `partial` (deterministic orientation, no ranking or embeddings, per
`docs/architecture.md`), since Reproducible's trap example is specifically "LLM extraction with no
fixed model/version"; Operator Memory has no extraction step at all for reads. Under the gap-driven scoring policy this reading is noted, not scored — as assessed here, it does not move the open cell, so no
row is added.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) —
CC's native memory for comparison.

---

## Roampal Core (roampal-ai)

**Repo**: [roampal-ai/roampal-core][roampal-core] | **PyPI**: [`roampal`][roampal-pypi] | **Stars**: 47 | **Forks**: 7 | **License**: Apache-2.0 | **Version**: 0.5.7 (2026-05-12)

Outcome-based persistent-memory MCP server for Claude Code and OpenCode. Auto-injects contextual memories into coding-assistant sessions and continuously promotes advice that led to good outcomes while demoting advice that didn't, based on per-exchange scoring — a design distinct from the static-recall model of the other tools in this doc.

### Architecture

- **Five memory collections** with distinct lifetimes: `working` (24h), `history` (30 days), `patterns` (persistent), `memory_bank` (permanent identity/preferences), `books` (reference docs)
- **FastAPI HTTP server** on port 27182 wraps a `UnifiedMemorySystem` backed by ChromaDB, using "TagCascade retrieval" (tags-first + CE rerank); auto-starts on first use with self-healing
- **Bias-avoiding scoring**: in Claude Code the main LLM scores its own exchanges via a `score_memories` tool invoked through hooks; in OpenCode an independent sidecar makes a separate API call to score silently, avoiding self-assessment bias
- **MCP tools**: `search_memory`, `add_to_memory_bank`, `update_memory`, `delete_memory`, `score_memories` (Claude Code only), `record_response`

### CC Integration

```bash
pip install roampal && roampal init   # auto-detects and configures Claude Code / OpenCode
```

One of exactly two first-class clients alongside OpenCode (the README also states "Cursor compatible," though repo topics list only `claude-code` and `opencode` — the support tier for Cursor is unclear). Stated requirements: Python 3.10+, ~800MB RAM, ~500MB disk, x86-64 with AVX2, no GPU (ONNX Runtime for CPU-only embedding inference).

### Adoption Considerations

**Strengths**: Outcome-based scoring loop (promotes memories tied to good outcomes, demotes ones tied to bad ones) rather than static recall. Fully OSS (Apache-2.0). CPU-only embeddings, no GPU or API key required. Single `pip install` auto-configures detected clients. Active recent release (v0.5.7, 2026-05-12; release notes cite 720 passing tests, including new coverage for stale-timestamp pruning and atomic-write contracts).

**Risks**: No independent or third-party benchmark for the core "good advice promoted / bad advice demoted improves outcomes" claim — unlike ByteRover (LoCoMo) and MemPalace (LongMemEval) above, roampal-core reports no benchmark number. Small community relative to siblings in this doc (47 stars, 7 forks). ChromaDB dependency. Overlaps with CC's built-in memory, ByteRover, Claude-Mem, MemPalace, and MemSearch — pick one.

Cross-ref: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CC's native memory for comparison

## Second-brain vaults (LLM-maintained markdown)

A second family of tools treats memory as a personal or team *knowledge base* the agent writes and curates, not a session log: pages live as markdown, usually in an Obsidian-style vault, and the agent reads them back at the start of a task. These are variants of the pattern analysed in [karpathy-llm-kb-analysis.md](../non-cc/knowledge-management/karpathy-llm-kb-analysis.md) (raw sources, an LLM-owned wiki, a schema file), which is not re-explained here; three of them (gbrain, open-second-brain, claude-second-brain) add vector or semantic retrieval, which the original pattern set out to replace. The five below differ mainly in who writes pages and what indexes them. Three of the five run on many harnesses besides Claude Code; they sit here, next to ai-memory and deja-vu, because this doc is the corpus home for cross-agent memory tools.

Metadata as of 2026-11-17 (`gh api`, READMEs read the same day). All five are MIT-licensed.

| Tool | Store | Harnesses (as documented) | Retrieval | Write path | Stars / last push |
|---|---|---|---|---|---|
| [gbrain][gbrain] | Database (PGlite or Postgres) indexing markdown folders; an Obsidian vault works as a source | Claude Code and Codex via `gbrain setup`; MCP for OpenClaw, Hermes, opencode, Cursor, ChatGPT, Claude Desktop and others | Keyword by default; semantic search once an embedding key is added; optional graph and synthesis layer | Agent writes via MCP and hooks; `gbrain sync` re-reads source folders; an optional overnight "dream" cycle | 33,218 / 2026-11-17 |
| [COG-second-brain][cog] | Obsidian vault of plain `.md` files, optional git | Claude Code, Antigravity, Cursor, Kiro, Gemini CLI; Codex and others via `AGENTS.md` | None documented; the agent reads the files | User-invoked skills (braindump, daily-brief, weekly-checkin, knowledge-consolidation) | 1,499 / 2026-10-23 |
| [open-second-brain][osb] | Obsidian vault, agent-written files under `Brain/`, rebuildable SQLite index | Plugins for Claude Code, Codex, Hermes, opencode, Grok Build; MCP config for Cursor, kiro, Copilot CLI, Gemini CLI, ZCode; ChatGPT desktop via the Codex config; OpenClaw; Aider and Pi via CLI | Keyword; optional semantic lane (embedding provider plus `sqlite-vec`) | Agent via MCP, lifecycle hooks and the `o2b` CLI; a deterministic `dream` pass promotes repeated signals into rules | 602 / 2026-11-17 |
| [agent-second-brain][asb] | Obsidian vault on a VPS, plain markdown | Claude Code only (the bot drives one long-lived session in tmux) | Agent searches the vault; the bundled `autograph` skill adds typed cards, decay tiers and indexes | Telegram voice, text and files; a nightly 21:00 pass writes vault cards | 499 / 2026-08-05 |
| [claude-second-brain][csb] | Git repo that is also an Obsidian vault | Claude Code (skills) | qmd local hybrid search (vector + BM25) | `/brain-ingest` on files dropped into `raw-sources/` | 172 / 2026-04-20 |

Evidence levels: **documented** = stated in the project's README or docs; **shipped in code** = checked against repo contents; **vendor claim** = the author's own assertion, not independently reproduced.

**gbrain** ([garrytan/gbrain][gbrain], latest release v0.60.734.0, 2026-11-17; the README says new releases come out many times a day and a slower `stable` channel is the default install)

- Repo created 2026-04-05; README presents it as a "brain" read by every connected agent, with `gbrain setup claude-code` registering MCP, hooks and a brain-first block in the agent's instruction file (documented).
- Self-hostable and keyless to start; hosted gbrain.io is an optional paid service (documented).
- Author's own deployment is stated as 155,795 pages, 24,589 people and 66 autonomous cron jobs (vendor claim, unverifiable).
- The README embeds an install prompt meant to be pasted into a coding agent, pointing at a remote instruction file. It was not followed or fetched here.

**COG-second-brain** ([huytieu/COG-second-brain][cog], v3.16.0, 2026-10-23)

- Credits gbrain's compiled-truth and tiered people-profile ideas as inspiration (documented).
- Agent surfaces: full Claude Code and Antigravity surfaces, thinner Kiro and Gemini CLI ones, `AGENTS.md` fallback (documented).
- Internal inconsistency, confirmed 2026-11-17: the repo description says "35 AI skills", the README's agent matrix says Claude Code has 33 native skills and its diagram says 43, and `.claude/skills/` and `skills/` each contain 43 entries via the contents API (shipped in code). Agent definitions: 10 in `.claude/agents/`, while the README's tree comment says 6 (the 6 workers; the 4 verifiers are listed separately).
- The README's "120+ braindumps, 95%+ source accuracy" results are the author's own (vendor claim).

**open-second-brain** ([itechmeat/open-second-brain][osb], v1.98.0, 2026-11-03)

- One of the two broadest harness lists here (about 14 clients, comparable to gbrain's), with per-client install guides and `o2b install --check` / `o2b doctor` verification (documented).
- Learning loop: agent feedback becomes inbox signals, the dream pass renders rules into `Brain/active.md`, read at next session start; the README says "no model runs inside that algorithm", while its how-it-works doc names one model-delegated rollup step (documented).
- Safety features: snapshots with `o2b brain rollback` (the README says "Brain mutations take a snapshot first"; its how-it-works doc names dream runs and imports), and a hash-chained write log (documented, not described as opt-in); staged review of agent writes and a permissions file (documented as off or absent by default).

**agent-second-brain** ([smixs/agent-second-brain][asb], v3.0.3, 2026-06-20)

- Voice-first: Deepgram transcribes audio; text goes to Claude; the vault stays on the server (documented).
- Memory model borrows forgetting-curve decay across five tiers via the separate `autograph` project (documented; not evaluated here).
- The README's rationale for driving one interactive session is its claim that headless `claude -p` runs bill separately from the subscription since 2026-06-15. Anthropic's [API-credits article][api-credits-max] (undated page, read 2026-11-17) conflicts with that for plan logins: `claude -p` and Agent SDK usage signed in with a plan "still draw from your plan's usage limits", and the Agent SDK credit announced in June "isn't available". For what scripted runs bill, see [CC-web-auth-setup-analysis.md § What a Scripted Run Bills](../cc-native/ci-remote/CC-web-auth-setup-analysis.md#what-a-scripted-run-bills).
- The README's quick start pipes a remote `bootstrap.sh` into bash; it was not run here.

**claude-second-brain** ([jessepinkman9900/claude-second-brain][csb], v1.1.0, 2026-04-20)

- Closest to the Karpathy pattern: raw sources, an LLM-owned `wiki/` with five page types, and `CLAUDE.md` as the schema file the README calls the "idea file" (documented).
- Scaffolds with an `npx` command per the README; qmd needs a one-time download of roughly 2 GB of models (documented).
- Roadmap items (scheduled refresh, auto-ingest on push) are unchecked, so not shipped per the README.

Adoption note: page quality depends on the agent following the schema or skills, and none of the five READMEs read cites an independent third-party benchmark; the scale and accuracy numbers above are the authors' own.

## Benchmarks

Two long-term-memory benchmarks recur in this space. **Most per-framework numbers are vendor self-reported** — each project's own run on the public dataset, with its own LLM/harness — not produced or audited by the benchmark authors, and not directly comparable across rows. Treat as directional.

### LongMemEval ([repo][longmemeval], arXiv:2410.10813)

500 questions over multi-session chat histories testing five abilities: information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention. Two settings: ~115k tokens (S) and ~1.5M tokens / 500 sessions (M). The paper reports a ~30% accuracy drop for commercial assistants on long histories and names no framework scores.

| Framework | Reported result | Source |
|---|---|---|
| MemPalace | 96.6% R@5 (raw mode) | vendor README — see [MemPalace](#mempalace-milla-jovovich) above |
| deja-vu | 88.1% hit@1 (LongMemEval-S, 470Q cleaned set) | vendor README — see [deja-vu](#deja-vu-vshulcz) above |
| Mem0 | ~94% accuracy, ~6.8k mean tokens | mem0.ai/research (vendor, 2026) |

### LOCOMO ([Meta][locomo], arXiv:2402.17753)

Long conversational memory — QA (single/multi-hop, temporal, open-domain), event summarization, multimodal dialogue over conversations averaging ~300 turns / ~9k tokens across up to 35 sessions. Humans substantially outperform all evaluated systems.

| Framework | Reported result (self-reported) | Source |
|---|---|---|
| Mem0 | ~92.5 overall; ~7k tokens vs 25k+ full-context; "~90% lower token cost" | [Mem0 paper][mem0-paper] |
| MemoryOS | +49.11% F1, +46.18% BLEU-1 over baselines | vendor README ([MemoryOS][memoryos]) |
| Core | 88.24% avg accuracy (single/multi-hop, open-domain, temporal) | vendor README — see [Core](#core-redplanethq) above |
| deja-vu | 70.5% retrieval hit@1 | vendor README — see [deja-vu](#deja-vu-vshulcz) above |

Caveat: LOCOMO's authors (Meta) did not evaluate these frameworks; cite as "X-reported on LOCOMO," not "LOCOMO result."

## Cross-References

- [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) — full cross-tool comparison + the rest of the CC tooling landscape
- [agent-frameworks-infrastructure-landscape.md](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md) — non-CC memory infrastructure (Mem0, Zep, Cognee, LangMem)

## Sources

| Source | Content |
|---|---|
| [agent-memory][agent-memory] | Long-term memory runtime for Claude Code/Codex/Hermes (README, `gh api`, 2026-09-30) |
| [ai-memory][ai-memory] | Cross-agent long-term memory (Rust) |
| [gbrain][gbrain] · [COG-second-brain][cog] · [open-second-brain][osb] · [agent-second-brain][asb] · [claude-second-brain][csb] | Second-brain vault tools (READMEs, `gh api`, 2026-11-17) |
| [Anthropic: monthly API credits][api-credits-max] | What `claude -p` and Agent SDK runs bill on a plan login (support article, undated page, read 2026-11-17) |
| [Byterover][byterover] · [paper][byterover-paper] | Agent memory layer (CLI) |
| [claude-mem][claude-mem] · [docs][claude-mem-docs] · [configuration][claude-mem-config] | Cross-agent memory plugin (README, releases, `gh api`, 2026-11-09) |
| [claude-reflect][claude-reflect] | Correction/preference memory plugin for Claude Code |
| [Core][core] · [benchmark repo][core-benchmark] | Self-hosted personal AI OS with CC/Codex delegation |
| [CortexDB][cortexdb] | Go agent memory + RDF knowledge graph in one SQLite file (README, `gh api`, 2026-11-12) |
| [deja-vu][deja-vu] · [security model][deja-vu-security] | Cross-agent session-history memory index |
| [engrim][engrim] | Cross-agent episodic memory store (SQLite) |
| [Leviathan][leviathan] | Deep memory + full-text index for agents over large datasets (README, `gh api`, 2026-11-12) |
| [MemPalace][mempalace] | Agent memory tool |
| [memsearch][memsearch] · [CC docs][memsearch-docs] | Zilliz memory search (CC integration) |
| [roampal-core][roampal-core] · [PyPI][roampal-pypi] | Outcome-based memory MCP server (CC integration) |
| [operator-memory][operator-memory] | Self-improving context engine / cross-agent memory (README, `gh api` tags, 2026-10-06) |
| [LangMem][langmem] · [concepts][langmem-concepts] | LangChain long-term memory |
| [Mem0][mem0] · [paper][mem0-paper] | Memory layer for agents |
| [Cognee][cognee] | Memory / knowledge-graph framework |
| [Letta][letta] | Stateful agents (MemGPT lineage) |
| [Zep Graphiti][graphiti] | Temporal knowledge-graph memory |
| [A-MEM][a-mem] | Agentic memory system |
| [MemoryOS][memoryos] | Hierarchical memory OS |
| [CoALA][coala] | Cognitive-architectures framework (paper) |
| André Lindenberg — *Memory should change future behavior* (LinkedIn, 2026) | Design principle: memory judged by behavior change, not storage (LinkedIn — not link-checked) |
| [LongMemEval][longmemeval] | Long-term-memory benchmark |
| [LOCOMO][locomo] | Long-conversation memory benchmark |

[agent-memory]: https://github.com/tigerless-labs/agent-memory
[ai-memory]: https://github.com/akitaonrails/ai-memory
[byterover]: https://github.com/campfirein/byterover-cli
[byterover-paper]: https://arxiv.org/abs/2604.01599
[claude-mem]: https://github.com/thedotmack/claude-mem
[claude-mem-config]: https://github.com/thedotmack/claude-mem/blob/main/docs/public/configuration.mdx
[claude-mem-docs]: https://docs.claude-mem.ai/introduction
[claude-reflect]: https://github.com/BayramAnnakov/claude-reflect
[gbrain]: https://github.com/garrytan/gbrain
[api-credits-max]: https://support.claude.com/en/articles/17154008-monthly-api-credits-for-max-users
[cog]: https://github.com/huytieu/COG-second-brain
[osb]: https://github.com/itechmeat/open-second-brain
[asb]: https://github.com/smixs/agent-second-brain
[csb]: https://github.com/jessepinkman9900/claude-second-brain
[core]: https://github.com/RedPlanetHQ/core
[core-benchmark]: https://github.com/RedPlanetHQ/core-benchmark
[cortexdb]: https://github.com/liliang-cn/cortexdb
[deja-vu]: https://github.com/vshulcz/deja-vu
[deja-vu-security]: https://github.com/vshulcz/deja-vu/blob/main/docs/SECURITY-MODEL.md
[engrim]: https://github.com/timgordontg/engrim
[leviathan]: https://github.com/elstongun/leviathan
[mempalace]: https://github.com/MemPalace/mempalace
[longmemeval]: https://github.com/xiaowu0162/LongMemEval
[memsearch]: https://github.com/zilliztech/memsearch
[memsearch-docs]: https://zilliztech.github.io/memsearch/platforms/claude-code/
[roampal-core]: https://github.com/roampal-ai/roampal-core
[roampal-pypi]: https://pypi.org/project/roampal/
[operator-memory]: https://github.com/aerovato/operator-memory
[sub-arch]: ../sdlc-lcm/agent-substrate-reference-architecture.md#what-stays-open
[coala]: https://arxiv.org/abs/2309.02427
[langmem]: https://github.com/langchain-ai/langmem
[langmem-concepts]: https://langchain-ai.github.io/langmem/concepts/conceptual_guide/
[non-cc-mem]: ../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#4-agent-memory-infrastructure
[mem0]: https://github.com/mem0ai/mem0
[mem0-paper]: https://arxiv.org/abs/2504.19413
[cognee]: https://github.com/topoteretes/cognee
[letta]: https://github.com/letta-ai/letta
[graphiti]: https://github.com/getzep/graphiti
[a-mem]: https://github.com/agiresearch/A-mem
[memoryos]: https://github.com/BAI-LAB/MemoryOS
[locomo]: https://arxiv.org/abs/2402.17753
