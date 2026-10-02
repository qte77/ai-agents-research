# Topic Hub: Context

What enters the context window: repo context, compression, retrieval-for-context, and context-budget
patterns across the corpus. Pointers only; see [the hub index](README.md).

| Doc / section | What it covers | Bucket |
|---|---|---|
| [CC-extended-context-analysis.md § Context Quality Degradation](../cc-native/context-memory/CC-extended-context-analysis.md#context-quality-degradation) | 1M-token window smart-zone/dumb-zone degradation and mitigation | cc-native |
| [CC-memory-system-analysis.md § Context Engineering Workflow (ACE-FCA)](../cc-native/context-memory/CC-memory-system-analysis.md#context-engineering-workflow-ace-fca) | Frequent-compaction methodology, context-quality ranking | cc-native |
| [CC-memory-system-analysis.md § CLAUDE.md Growth and Catastrophic Remembering (arXiv 2608.11095)](../cc-native/context-memory/CC-memory-system-analysis.md#claudemd-growth-and-catastrophic-remembering-arxiv-260811095) | Empirical study of instruction-file bloat; rationale-comment mitigation | cc-native |
| [CC-memory-system-analysis.md § Practitioner Template: context-engineering-intro](../cc-native/context-memory/CC-memory-system-analysis.md#practitioner-template-context-engineering-intro) | PRP (Product Requirements Prompt) starter template for CLAUDE.md-driven development | cc-native |
| [CC-memory-system-analysis.md § Scored on the Agent Substrate Rubric](../cc-native/context-memory/CC-memory-system-analysis.md#scored-on-the-agent-substrate-rubric) | CC's CLAUDE.md/auto memory scored Shared/Distributed/Versionable/Traceable | cc-native |
| [CC-memory-system-analysis.md § A Non-CC Comparison: Topic-Label Gating (TrackPoint)](../cc-native/context-memory/CC-memory-system-analysis.md#a-non-cc-comparison-topic-label-gating-trackpoint) | Vendor pattern compared to CC's MEMORY.md-index/topic-file split; self-reported, unverified | cc-native |
| [CC-agentic-harness-patterns-analysis.md § Category 1: Memory and Context (5 patterns)](../cc-native/agents-skills/CC-agentic-harness-patterns-analysis.md#category-1-memory-and-context-5-patterns) | Harness patterns for scoped context assembly and progressive compaction | cc-native |
| [CC-skills-adoption-analysis.md § Skill Context Budgets](../cc-native/agents-skills/CC-skills-adoption-analysis.md#skill-context-budgets) | Progressive disclosure and context-fork budgets for skills | cc-native |
| [CC-repo-guidance-probe-refine-analysis.md](../cc-native/context-memory/CC-repo-guidance-probe-refine-analysis.md) | Iteratively tuning a repo's AGENTS.md/CLAUDE.md guidance file | cc-native |
| [fastcontext-analysis.md](../non-cc/context-memory/fastcontext-analysis.md) | Dedicated repo-exploration subagent | non-cc |
| [ripwire-analysis.md](../non-cc/context-memory/ripwire-analysis.md) | Deterministic repo-context CLI for coding agents | non-cc |
| [opensrc-analysis.md](../non-cc/context-memory/opensrc-analysis.md) | Fetches dependency source code into agent context | non-cc |
| [redis-iris-analysis.md § Context Retriever](../non-cc/context-memory/redis-iris-analysis.md#context-retriever) | Auto-generated MCP tools over business data, shared read access across agents; first row to score `partial` on context·Shared and context·Distributed (plan 0010) | non-cc |

Related hubs: [memory.md](memory.md), [code-tooling.md](code-tooling.md), [rag.md](rag.md).
