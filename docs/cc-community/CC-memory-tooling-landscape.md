---
title: CC Memory Tooling Landscape
purpose: Persistent cross-session memory tools that integrate with Claude Code — ByteRover, Claude-Mem, MemPalace, MemSearch.
category: landscape
status: research
created: 2026-06-14
updated: 2026-06-16
validated_links: 2026-06-14
---

**Status**: Research (informational)

Persistent-memory tools for Claude Code. Split out of [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) (which keeps the cross-tool comparison table). For non-CC memory *infrastructure* (Mem0, Zep/Graphiti, Cognee, LangMem, A-MEM), see [agent-frameworks-infrastructure-landscape.md § Agent Memory Infrastructure](../non-cc/agent-frameworks-infrastructure-landscape.md#4-agent-memory-infrastructure). CC's native memory: [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md).

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

**Repo**: [thedotmack/claude-mem][claude-mem] | **Stars**: 45.2K | **License**: AGPL-3.0 | **Version**: 6.5.0

Persistent memory compression system for Claude Code. Automatically captures everything Claude does during coding sessions, compresses it with AI, and injects relevant context back into future sessions for continuity.

### Architecture

| Component | Purpose |
|-----------|---------|
| **Lifecycle Hooks** (5) | SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd |
| **Worker Service** | Express API on port 37777, managed by Bun runtime, includes web viewer UI |
| **SQLite Storage** | Sessions, observations, summaries with FTS5 full-text search |
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
- Web viewer UI at localhost:37777
- Notification integrations (Telegram, Discord, Slack)

### Live Observer Architecture

A dedicated observer AI watches each session in real-time, generating searchable observations with before-and-after context — capturing causality and decision chains, not just snapshots. Observations are auto-categorized by type (decisions, bugfixes, features, discoveries) and queryable by file path or semantic concept (e.g., "decisions about token refresh").

### RAD Protocol (Coming Soon)

**Real-Time Agent Data** — an open protocol standardizing how AI agents capture and retrieve working memory. Positioned as a counterpart to RAG (Retrieval Augmented Generation). Hook-based architecture for temporal awareness.

### Adoption Considerations

**Strengths**: Largest community memory solution (45.2K stars), progressive disclosure saves tokens, hybrid search (FTS5 + vector), multi-platform (CC + Gemini CLI), web UI for browsing history, [dedicated docs site][claude-mem-docs].

**Risks**: AGPL-3.0 (copyleft — commercial use requires compliance). Ragtime subdirectory under separate PolyForm Noncommercial License. Heavy dependencies (Bun + uv + Chroma). Overlaps with CC's built-in memory system and ByteRover.

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

## Cross-References

- [CC-community-tooling-landscape.md](CC-community-tooling-landscape.md) — full cross-tool comparison + the rest of the CC tooling landscape
- [agent-frameworks-infrastructure-landscape.md](../non-cc/agent-frameworks-infrastructure-landscape.md) — non-CC memory infrastructure (Mem0, Zep, Cognee, LangMem)

[byterover]: https://github.com/campfirein/byterover-cli
[byterover-paper]: https://arxiv.org/abs/2604.01599
[claude-mem]: https://github.com/thedotmack/claude-mem
[claude-mem-docs]: https://docs.claude-mem.ai/introduction
[mempalace]: https://github.com/MemPalace/mempalace
[longmemeval]: https://github.com/xiaowu0162/LongMemEval
[memsearch]: https://github.com/zilliztech/memsearch
[memsearch-docs]: https://zilliztech.github.io/memsearch/platforms/claude-code/
