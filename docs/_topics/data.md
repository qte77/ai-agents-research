# Topic Hub: Data

Agents and data platforms: database access and text-to-SQL, lakehouses and warehouses, semantic
layers, catalogs and ontologies, graph and vector stores. Pointers only; see [the hub index](README.md).

## Databases and SQL

| Doc / section | What it covers | Bucket |
|---|---|---|
| [agentic-database-access-landscape.md § Database MCP servers](../non-cc/infrastructure/agentic-database-access-landscape.md#database-mcp-servers) | Database MCP servers with licences and read-only modes | non-cc |
| [agentic-database-access-landscape.md § Text-to-SQL benchmarks](../non-cc/infrastructure/agentic-database-access-landscape.md#text-to-sql-benchmarks) | BIRD and Spider 2.0 with dates, BIRD-RL, DualSQL | non-cc |
| [agentic-database-access-landscape.md § Write safety](../non-cc/infrastructure/agentic-database-access-landscape.md#write-safety) | Read-only roles, branching, incident evidence | non-cc |
| [agentic-database-access-landscape.md § Data quality and lineage](../non-cc/infrastructure/agentic-database-access-landscape.md#data-quality-and-lineage) | Data quality and lineage, pointing at the semantic-layers landscape | non-cc |

## Lakehouses and warehouses

| Doc / section | What it covers | Bucket |
|---|---|---|
| [data-platforms-lakehouse-landscape.md § Open table formats](../non-cc/infrastructure/data-platforms-lakehouse-landscape.md#open-table-formats) | Iceberg, Delta, Hudi, DuckLake with versions and licences | non-cc |
| [data-platforms-lakehouse-landscape.md § Catalog-level and storage-level branching](../non-cc/infrastructure/data-platforms-lakehouse-landscape.md#catalog-level-and-storage-level-branching) | Nessie and lakeFS branching (lakeFS under BSL 1.1) | non-cc |
| [data-platforms-lakehouse-landscape.md § Warehouse-native agents](../non-cc/infrastructure/data-platforms-lakehouse-landscape.md#warehouse-native-agents) | Snowflake Cortex Agents, BigQuery conversational analytics, Genie, Fabric data agent | non-cc |
| [data-platforms-lakehouse-landscape.md § Local engines as agent scratch space](../non-cc/infrastructure/data-platforms-lakehouse-landscape.md#local-engines-as-agent-scratch-space) | DuckDB, chDB, Polars as agent scratch space | non-cc |
| [data-platforms-lakehouse-landscape.md § Cost and permission controls](../non-cc/infrastructure/data-platforms-lakehouse-landscape.md#cost-and-permission-controls) | Cost and permission controls for agents on data platforms | non-cc |

## Semantic layers, catalogs and ontologies

| Doc / section | What it covers | Bucket |
|---|---|---|
| [semantic-layers-data-catalog-landscape.md § Choosing a Structure](../non-cc/infrastructure/semantic-layers-data-catalog-landscape.md#choosing-a-structure) | From tags to taxonomy, SKOS, OWL and knowledge graphs: which structure a KB needs | non-cc |
| [semantic-layers-data-catalog-landscape.md § Semantic / Metrics Layers](../non-cc/infrastructure/semantic-layers-data-catalog-landscape.md#semantic--metrics-layers) | Semantic and metrics layers that keep metrics consistent | non-cc |
| [semantic-layers-data-catalog-landscape.md § Catalogs / Metadata / Governance](../non-cc/infrastructure/semantic-layers-data-catalog-landscape.md#catalogs--metadata--governance) | Data catalogs, metadata, lineage, governance | non-cc |
| [semantic-layers-data-catalog-landscape.md § Ontology generation and ontology-constrained extraction](../non-cc/infrastructure/semantic-layers-data-catalog-landscape.md#ontology-generation-and-ontology-constrained-extraction) | Generating ontologies and extracting against one | non-cc |
| [databricks-genie-analysis.md § Genie Ontology](../non-cc/agents/databricks-genie-analysis.md#genie-ontology) | Genie Ontology (Public Preview), vendor benchmark caveated | non-cc |
| [open-knowledge-format-analysis.md](../non-cc/knowledge-management/open-knowledge-format-analysis.md) | Open Knowledge Format: agent-readable data-catalog spec (v0.2) | non-cc |

## Graphs and vectors

| Doc / section | What it covers | Bucket |
|---|---|---|
| [graph-databases-query-languages-landscape.md § Query Languages](../non-cc/infrastructure/graph-databases-query-languages-landscape.md#query-languages) | Graph query languages and their standard status | non-cc |
| [graph-databases-query-languages-landscape.md § Graph Databases Relevant to Agents](../non-cc/infrastructure/graph-databases-query-languages-landscape.md#graph-databases-relevant-to-agents) | Graph databases with licences and repo state | non-cc |
| [graph-databases-query-languages-landscape.md § Text-to-Query for Agents](../non-cc/infrastructure/graph-databases-query-languages-landscape.md#text-to-query-for-agents) | Text-to-graph-query evidence (authors' claims) | non-cc |
| [graph-databases-query-languages-landscape.md § Graph MCP Servers](../non-cc/infrastructure/graph-databases-query-languages-landscape.md#graph-mcp-servers) | Graph MCP servers and their read-only behaviour | non-cc |
| [agent-frameworks-infrastructure-landscape.md § Temporal knowledge-graph memory: evidence and caveats](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#temporal-knowledge-graph-memory-evidence-and-caveats) | Graphiti/Zep temporal KG memory, vendor and author claims labelled | non-cc |
| [agent-frameworks-infrastructure-landscape.md § GraphRAG vs vector RAG and KG construction evidence](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#graphrag-vs-vector-rag-and-kg-construction-evidence) | GraphRAG vs vector RAG, KG construction and hypergraph evidence | non-cc |
| [agent-frameworks-infrastructure-landscape.md § Vector databases](../non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#vector-databases) | Vector databases | non-cc |

Related hubs: [knowledge-graphs.md](knowledge-graphs.md), [rag.md](rag.md), [memory.md](memory.md), [security.md](security.md), [evals-benchmarks.md](evals-benchmarks.md).
