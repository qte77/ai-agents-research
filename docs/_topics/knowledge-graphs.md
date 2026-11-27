# Topic Hub: Knowledge Graphs

Knowledge graphs, graph databases, ontologies and code graphs across the corpus. Pointers only;
see [the hub index](README.md).

| Doc / section | What it covers | Bucket |
|---|---|---|
| [architecture.md § Doc Graph and Site](../architecture.md#doc-graph-and-site) | This repo's own doc graph (links between docs, rebuilt on deploy) | repo |
| [CC-code-tooling-landscape.md § Graphify](../cc-community/CC-code-tooling-landscape.md#graphify-safishamsi) | Graphify: knowledge-graph builder with CC hook/MCP integration | cc-community |
| [CC-code-tooling-landscape.md § Code-Review-Graph](../cc-community/CC-code-tooling-landscape.md#code-review-graph-tirth8205) | Code graph for PR review | cc-community |
| [CC-code-tooling-landscape.md § codebase-memory-mcp](../cc-community/CC-code-tooling-landscape.md#codebase-memory-mcp-deusdata) | Embedded typed code graph over MCP | cc-community |
| [CC-community-skills-landscape.md § pid-to-knowledge-graph](../cc-community/CC-community-skills-landscape.md#scottduncanaipid-to-knowledge-graph) | Claude skill that builds a process knowledge graph (JSON + DuckDB) from P&ID (piping and instrumentation diagram) PDFs; early watch entry | cc-community |
| [helixdb-analysis.md](../non-cc/context-memory/helixdb-analysis.md) | Rust graph-vector database | non-cc |
| [latticedb-analysis.md](../non-cc/context-memory/latticedb-analysis.md) | Embedded graph + vector + full-text database | non-cc |
| [minigraf-analysis.md](../non-cc/context-memory/minigraf-analysis.md) | Embedded bi-temporal Datalog graph database (Rust/Python/WASM/mobile) | non-cc |
| [semantic-layers-data-catalog-landscape.md § Choosing a Structure](../non-cc/infrastructure/semantic-layers-data-catalog-landscape.md#choosing-a-structure) | Tag list, controlled vocabulary, taxonomy, SKOS thesaurus, OWL ontology and knowledge graph compared: what each is, upkeep, when a KB needs it | non-cc |
| [graph-databases-query-languages-landscape.md § Property Graph vs RDF](../non-cc/infrastructure/graph-databases-query-languages-landscape.md#property-graph-vs-rdf) | The two graph data models and their query languages (Cypher/GQL vs SPARQL) | non-cc |
| [graph-databases-query-languages-landscape.md § Higher-order and layered relationships](../non-cc/infrastructure/graph-databases-query-languages-landscape.md#higher-order-and-layered-relationships) | How each graph model stores n-ary facts (hypergraph, property graph, RDF patterns, triple terms, named graphs, TypeDB), multilayer graphs, time as a layer, hypergraph and multilayer libraries | non-cc |
| [graph-databases-query-languages-landscape.md](../non-cc/infrastructure/graph-databases-query-languages-landscape.md) | Graph query languages, graph databases for agents, text-to-Cypher/SPARQL evidence, graph MCP servers; links the per-tool docs | non-cc |
| [rowboat-analysis.md](../non-cc/agents/rowboat-analysis.md) | AI coworker that builds knowledge graphs from communications | non-cc |
| [databricks-genie-analysis.md § Genie Ontology](../non-cc/agents/databricks-genie-analysis.md#genie-ontology) | Enterprise semantic graph behind Genie | non-cc |
| [open-knowledge-format-analysis.md](../non-cc/knowledge-management/open-knowledge-format-analysis.md) | OKF: agent-readable knowledge-bundle standard; v0.2 adds provenance, trust tiers and lifecycle fields | non-cc |
| [semantic-layers-data-catalog-landscape.md § Formal Ontologies](../non-cc/infrastructure/semantic-layers-data-catalog-landscape.md#formal-ontologies--semantic-web) | Formal ontologies and the semantic web (RDF, OWL, SKOS, SPARQL, SHACL, JSON-LD) | non-cc |
| [semantic-layers-data-catalog-landscape.md § Agent-native ontology tools](../non-cc/infrastructure/semantic-layers-data-catalog-landscape.md#agent-native-ontology-tools-2026-mcp-wave) | Ontology Atlas, open-ontologies, EvoOntology, AWS context-ontology-accelerator, Utopia — MCP-exposed ontology stores, rubric-scored; plus NVIDIA Auto Ontology (relational, SQL-only, unscored) | non-cc |
| [CC-code-tooling-landscape.md § AxiomCode Graph](../cc-community/CC-code-tooling-landscape.md#axiomcode-graph-axiomcodeai) | AxiomCode Graph: compiler-accurate (type-resolved, not tree-sitter-guessed) code knowledge graph, FSL license | cc-community |
| [CC-code-tooling-landscape.md § Graphicle](../cc-community/CC-code-tooling-landscape.md#graphicle-graphicle-ai) | Graphicle: Rust port of Graphify's code graph plus an agent-memory layer, benchmarked against Graphify | cc-community |
| [agent-frameworks-infrastructure-landscape.md § Agent-native graph & hybrid RAG platforms](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#agent-native-graph--hybrid-rag-platforms) | Graph-native context platforms for agents (TrustGraph, Carrel and others) | non-cc |
| [agent-frameworks-infrastructure-landscape.md § GraphRAG vs vector RAG and KG construction evidence](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#graphrag-vs-vector-rag-and-kg-construction-evidence) | GraphRAG vs vector RAG evidence, KG construction quality, provenance of LLM-written edges; hypergraph vs graph evidence (authors' claims) | non-cc |
| [semantic-layers-data-catalog-landscape.md § Ontology generation and ontology-constrained extraction](../non-cc/infrastructure/semantic-layers-data-catalog-landscape.md#ontology-generation-and-ontology-constrained-extraction) | LLM-generated ontologies and extraction constrained by an ontology (Text2KGBench and others) | non-cc |

Related hubs: [memory.md](memory.md), [rag.md](rag.md), [visualization.md](visualization.md), [data.md](data.md).
