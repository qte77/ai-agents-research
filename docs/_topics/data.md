# Topic Hub: Data

Agents and data platforms: database access and text-to-SQL, lakehouses and warehouses, semantic
layers, catalogs and ontologies, graph and vector stores. Pointers only; see [the hub index](README.md).

## Databases and SQL

| Doc / section | What it covers | Bucket |
|---|---|---|
| [agentic-database-access-landscape.md § Database MCP servers](../non-cc/infrastructure/agentic-database-access-landscape.md#database-mcp-servers) | Database MCP servers with licences and read-only modes | non-cc |
| [agentic-database-access-landscape.md § Text-to-SQL benchmarks](../non-cc/infrastructure/agentic-database-access-landscape.md#text-to-sql-benchmarks) | BIRD and Spider 2.0 with dates, BIRD-RL | non-cc |
| [agentic-database-access-landscape.md § Write safety](../non-cc/infrastructure/agentic-database-access-landscape.md#write-safety) | Read-only roles, branching, incident evidence | non-cc |
| [agentic-database-access-landscape.md § Data quality and lineage](../non-cc/infrastructure/agentic-database-access-landscape.md#data-quality-and-lineage) | Data quality and lineage, pointing at the semantic-layers landscape | non-cc |
| [insforge-analysis.md](../non-cc/infrastructure/insforge-analysis.md) | InsForge: backend platform with semantic infrastructure for coding agents | non-cc |

## Lakehouses and warehouses

| Doc / section | What it covers | Bucket |
|---|---|---|
| [data-platforms-lakehouse-landscape.md § Data lake vs lakehouse vs data warehouse](../non-cc/infrastructure/data-platforms-lakehouse-landscape.md#data-lake-vs-lakehouse-vs-data-warehouse) | The three architectures compared (Databricks' view plus Delta and Hudi self-descriptions; our rows labelled) | non-cc |
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
| [databricks-genie-analysis.md § Genie Ontology](../non-cc/agents/databricks-genie-analysis.md#genie-ontology) | Genie Ontology (Public Preview), vendor benchmark caveated | non-cc |
| [open-knowledge-format-analysis.md](../non-cc/knowledge-management/open-knowledge-format-analysis.md) | Open Knowledge Format: agent-readable data-catalog spec (v0.2) | non-cc |

Ontology generation and the agent-native ontology tools are indexed in [knowledge-graphs.md](knowledge-graphs.md).

## Enterprise data APIs

| Doc / section | What it covers | Bucket |
|---|---|---|
| [agentic-enterprise-os-landscape.md § Enterprise data APIs for agents](../non-cc/frameworks/agentic-enterprise-os-landscape.md#enterprise-data-apis-for-agents) | Auth, plan, unattended access, terms and MCP servers for 16 enterprise data vendors | non-cc |

## Graphs and vectors

Graph databases, graph query languages, graph MCP servers and ontology tools are indexed in
[knowledge-graphs.md](knowledge-graphs.md); temporal knowledge-graph memory in [memory.md](memory.md);
vector databases and GraphRAG-vs-vector evidence in [rag.md](rag.md).

Related hubs: [knowledge-graphs.md](knowledge-graphs.md), [rag.md](rag.md), [memory.md](memory.md), [security.md](security.md), [evals-benchmarks.md](evals-benchmarks.md).
