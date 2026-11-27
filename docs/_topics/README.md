# Topic Hubs

Cross-subject indexes. The corpus is split by relationship to Claude Code (`cc-native/`,
`cc-community/`, `non-cc/`, `sdlc-lcm/`), so one subject can span several buckets. Each hub lists
the docs and sections for its subject across all buckets. Hubs hold pointers only; the content
lives in the linked docs. For where a term is defined, see the [glossary](../glossary.md).

| Hub | Subject |
|---|---|
| [memory.md](memory.md) | Agent memory: CC's own memory system, CC memory plugins, memory infrastructure |
| [knowledge-graphs.md](knowledge-graphs.md) | Knowledge graphs, graph databases, ontologies, code graphs |
| [rag.md](rag.md) | Retrieval, embeddings, vector stores, indexing pipelines, RAG alternatives |
| [code-tooling.md](code-tooling.md) | Code search, repo context, code analysis, repo-to-docs, PR review |
| [visualization.md](visualization.md) | Inline visuals, agent-run visualizers, trace viewers, graph rendering |
| [context.md](context.md) | What enters the context window: repo context, compression, retrieval-for-context |
| [skills.md](skills.md) | Packaged agent capabilities (SKILL.md and equivalents), distribution and optimization |
| [plugins.md](plugins.md) | Extension packaging: plugins, MCP servers, marketplaces |
| [harness.md](harness.md) | The loop around the model: orchestration, tools, sandboxes, self-improving harnesses |
| [long-running.md](long-running.md) | Hands-off, offloaded, multi-hour or scheduled agent work: durability, resume, remote execution |
| [cost.md](cost.md) | Token usage and spend: cost drivers, levers that lower them, measurement tools |
| [evals-benchmarks.md](evals-benchmarks.md) | Eval methods and judges, benchmark catalogues and validity, building a benchmark, domain benchmarks |
| [security.md](security.md) | Threat models, prompt injection, guardrails and permissions, sandboxes, offensive-security agents |
| [data.md](data.md) | Database access and text-to-SQL, lakehouses, semantic layers and catalogs, graph and vector stores |
| [agentic-web.md](agentic-web.md) | Browser and computer-use agents, fetching and scraping, agent identity, access and payments |
| [management.md](management.md) | Agent management: fleet policy, registries, cost attribution, identity, licences, lifecycle |
| [knowledge-management.md](knowledge-management.md) | Wikis, LLM-maintained knowledge bases, knowledge-organisation methods, frontmatter schemas, enterprise knowledge layers |
| [model-internals.md](model-internals.md) | Interpretability and hidden-state research: what activations reveal, monitoring and detection uses |
| [dev-platforms.md](dev-platforms.md) | Code forges, CI/CD and runners, dev environments, repository rules and enterprise features |

To score the tools behind these hubs, use the [agent substrate rubric](../sdlc-lcm/agent-substrate-rubric.md) (shared, distributed, reproducible, adaptable, versionable, traceable).
The scored rows are read together in the [agent substrate reference architecture](../sdlc-lcm/agent-substrate-reference-architecture.md) (evidence matrix per subject and property, layers, open cells).
