# Topic Hub: Memory

Agent memory across the corpus. Pointers only; see [the hub index](README.md).

| Doc / section | What it covers | Bucket |
|---|---|---|
| [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) | CC's dual memory system: `CLAUDE.md` plus auto memory | cc-native |
| [CC-agentic-harness-patterns-analysis.md § Memory and Context](../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#category-1-memory-and-context-5-patterns) | Harness patterns for memory and context, incl. tiered memory | cc-native |
| [CC-memory-system-analysis.md § Anthropic's Components of Agent Memory](../cc-native/context-memory/CC-memory-system-analysis.md#anthropics-components-of-agent-memory-2026-11-06) | Anthropic's four-layer memory model and its Managed Agents experiments | cc-native |
| [CC-memory-tooling-landscape.md](../cc-community/CC-memory-tooling-landscape.md) | Persistent cross-session memory tools that plug into CC | cc-community |
| [agent-frameworks-infrastructure-landscape.md § 4](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#4-agent-memory-infrastructure) | Agent memory infrastructure catalog. Rubric-scored entries include AgentiCow (copy-on-write vector memory branching), Beads / bd (Dolt-backed distributed task/memory graph), lossless-memory (never-summarize, timestamp-first), HydraDB (object-store-native graph database, S3-backed), WikiTrace (arXiv 2611.14320, evidence-linked memory, code released), GrepMem (arXiv 2611.25123, grep over an append-only history log, code released) and the Weighted Memory Tree (arXiv 2608.20631) and JITMEM (arXiv 2609.27334) curation papers; also Kortix CompanyOS (shared company memory, Elastic License 2.0), the paper-only MemoProAgent/MemoProBench and ReHarness (arXiv 2610.12668), and the unlicensed worked example Hands-On-AI-Engineering `research_assistant_with_memory` | non-cc |
| [hermes-agent-analysis.md § Memory Design](../non-cc/agents/hermes-agent-analysis.md#memory-design-compared-with-claude-code) | Hermes Agent memory compared with Claude Code and the § 4 systems | non-cc |
| [openviking-analysis.md](../non-cc/context-memory/openviking-analysis.md) | Filesystem-based context database with memory extraction | non-cc |
| [mex-analysis.md](../non-cc/context-memory/mex-analysis.md) | Git-shared, human-approved project memory for coding agents | non-cc |
| [helixdb-analysis.md](../non-cc/context-memory/helixdb-analysis.md) | Graph-vector database positioned for agent memory | non-cc |
| [minigraf-analysis.md](../non-cc/context-memory/minigraf-analysis.md) | Embedded bi-temporal Datalog graph database pitched as agent memory; cited third-party agent-memory demo is the maintainer's own project | non-cc |
| [qwenpaw-analysis.md](../non-cc/agents/qwenpaw-analysis.md) | Personal assistant with a three-tier memory design | non-cc |
| [goclaw-analysis.md § 3-Tier Memory](../non-cc/infrastructure/goclaw-analysis.md#3-tier-memory-system) | Three-tier memory system | non-cc |
| [mitosis-cortex-analysis.md](../non-cc/context-memory/mitosis-cortex-analysis.md) | Mitosis Labs Cortex — hosted per-team knowledge-graph memory, rubric-scored | non-cc |
| [CC-memory-tooling-landscape.md § agent-memory](../cc-community/CC-memory-tooling-landscape.md#agent-memory-tigerless-labs) | agent-memory (tigerless-labs) — markdown-native long-term memory shared by Claude Code, Codex, Hermes, rubric-scored | cc-community |
| [hyperspell-analysis.md](../non-cc/context-memory/hyperspell-analysis.md) | Hyperspell (hosted company-data memory platform; marketed as "context" but scored as memory), rubric-scored | non-cc |
| [redis-iris-analysis.md § Agent Memory](../non-cc/context-memory/redis-iris-analysis.md#agent-memory) | Redis Iris's Agent Memory service (two-tier session/long-term store; OSS impl `redis/agent-memory-server`, Apache-2.0), rubric-scored | non-cc |
| [octop-analysis.md](../non-cc/agents/octop-analysis.md) | Octop (TencentCloud): self-hosted multi-user assistant; claimed hierarchical-recall memory, LangGraph SQLite checkpointer | non-cc |
| [CC-memory-tooling-landscape.md § CortexDB](../cc-community/CC-memory-tooling-landscape.md#cortexdb-liliang-cn) | CortexDB: Go agent memory + RDF knowledge graph in one SQLite file, Claude Code plugin + mod | cc-community |
| [CC-memory-tooling-landscape.md § Leviathan](../cc-community/CC-memory-tooling-landscape.md#leviathan-elstongun) | Leviathan: deep memory + full-text index for agents over large datasets | cc-community |
| [CC-memory-tooling-landscape.md § Second-brain vaults](../cc-community/CC-memory-tooling-landscape.md#second-brain-vaults-llm-maintained-markdown) | gbrain and COG: agent-maintained markdown vaults compared (store, harnesses, retrieval, write path) | cc-community |
| [research-agents-landscape.md § 1](../non-cc/knowledge-management/research-agents-landscape.md#1-autonomous-research-agents) | Épi (arXiv 2610.24944) — persistent research agent with hierarchical memory, paper only | non-cc |
| [agent-frameworks-infrastructure-landscape.md § Temporal knowledge-graph memory](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#temporal-knowledge-graph-memory-evidence-and-caveats) | Bi-temporal KG memory (Graphiti/Zep): what the evidence shows, invalidation instead of deletion, caveats on vendor benchmarks | non-cc |

Related hubs: [knowledge-graphs.md](knowledge-graphs.md), [rag.md](rag.md).
