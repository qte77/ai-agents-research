---
title: Data Platforms and Lakehouses for Agents — Table Formats, Branching, Warehouse-Native Agents, Scratch Engines, Cost Controls
purpose: "What the data-lake and lakehouse layer offers an agent: open table formats, catalogs, warehouse-native agents, local analytical engines, and cost and permission controls. As of 2026-11-18."
created: 2026-11-18
updated: 2026-11-26
validated_links_on: 2026-11-18
status: assess
---

## Why This Doc

Agent work on analytical data differs from agent work on an application database
([agentic-database-access-landscape.md](agentic-database-access-landscape.md) covers database MCP servers,
text-to-SQL and write safety). Analytical stores are large, scan-priced and shared, so the questions are:
which storage layer gives an agent cheap isolation (snapshots, branches, clones), which vendors ship an agent
inside the warehouse, where an agent can compute without touching shared state, and which documented controls
cap spend and access. Catalogs, metrics and lineage are in
[semantic-layers-data-catalog-landscape.md](semantic-layers-data-catalog-landscape.md). Versions, licenses and
star counts are from each project's repo (`gh api`) on 2026-11-21; vendor feature statements are from the
vendor's docs read on 2026-11-18 (the definitions below on 2026-11-21) and are documented behavior, not tested
here.

## Data lake vs lakehouse vs data warehouse

Rows 1 to 3 summarize Databricks' [blog post][dbx-lakehouse] (a vendor that sells the lakehouse, so the framing
is its own; documented, read 2026-11-21). The last two rows are our mapping, not the vendor's.

| | Data warehouse | Data lake | Lakehouse |
|---|---|---|---|
| What it is | Long used for decision support and BI; the post says warehouses handled unstructured data poorly or expensively | Low-cost storage for raw data in any format | Warehouse and lake capabilities combined, with ACID transactions, schema enforcement and governance, on cloud object storage |
| Transactions and quality | Not discussed beyond the point above | Per the post, lakes "do not support transactions" and "do not enforce data quality" | ACID transactions via a metadata layer |
| Open table format (ours) | Usually closed or vendor-specific | Not applicable (raw files) | [Iceberg][iceberg], [Delta Lake][delta], [Hudi][hudi] below |
| Where an agent queries it (ours) | Warehouse-native agents (below) or database MCP servers ([database-access doc](agentic-database-access-landscape.md)) | Through an engine that reads the files | Any engine that speaks the table format, through a catalog (below) |

Delta describes a lakehouse layer over existing data lakes with ACID transactions and time travel ([Delta
docs][delta-docs], read 2026-11-21). Hudi calls itself an open lakehouse platform with efficient upserts and
deletes, incremental processing, a transaction timeline and copy-on-write or merge-on-read tables ([Hudi
overview][hudi-docs], 2026-11-21). No performance comparison between the formats is made or cited here.

## Open table formats

| Format | License | Latest release (2026-11-21) | Snapshot / branch feature (documented) |
|---|---|---|---|
| [Apache Iceberg][iceberg] | Apache-2.0 | 1.12.0 (2026-09-30) | Snapshots for time travel; [branches and tags][iceberg-branching] are named references with their own retention policies |
| [Delta Lake][delta] | Apache-2.0 | v4.4.1 (2026-10-05) | Time travel and `RESTORE`; [shallow clone][delta-clone] copies a table at a version with its own history, referencing source files |
| [Apache Hudi][hudi] | Apache-2.0 | 1.2.1 (2026-09-24) | Not researched for branching here |
| [DuckLake][ducklake] | MIT | Site read 2026-11-18, not re-read: docs site (`/docs/stable`) labels 1.1 stable, requiring DuckDB 2.0.0 or later; the homepage calls 1.0 production-ready (GitHub shows no tagged release) | SQL database as catalog (PostgreSQL, MySQL, SQLite or DuckDB), Parquet data; snapshots and time travel; the page does not mention branching |

Iceberg's own docs name audit branches and experimental branches "for testing and validating new jobs" as use
cases ([branching page][iceberg-branching]). Delta's shallow clone is writable without touching the source
as long as source files are not modified, but a `vacuum` on the source can break clone reads
([Delta docs][delta-clone]). Our reading: both are table-level isolation and neither isolates other tables.

## Catalog-level and storage-level branching

| Tool | License | Version (2026-11-21) | What it adds |
|---|---|---|---|
| [Project Nessie][nessie] | Apache-2.0 | 0.110.1 (2026-11-21) | Version-control-style branches, tags and commits at the catalog, so one commit can span many tables (multi-table transaction); a job writes to a branch and merges when done, per its [guide][nessie-about] |
| [lakeFS][lakefs] | Business Source License 1.1, converting to Apache-2.0 four years after each version's release (LICENSE file; GitHub shows `NOASSERTION`) | v1.88.0 (2026-10-01) | Data version control over object storage per the repo description. The BSL Additional Use Grant has two conditions: (a) the work is unmodified and (b) "Internal Use Only", which bars offering or hosting the work or its functionality to third parties; (b) is the material restriction. The LICENSE names lakeFS 1.87.0 while the latest release is 1.88.0 |

Catalog-level branching is the closest lakehouse analogue to the Postgres branching in the database-access
doc: an agent could write on a branch, a human or check could review, then merge. No source here documents an
agent-specific workflow; that pattern is an inference from the branch semantics.

## Catalogs

[Apache Polaris][polaris] (Apache-2.0, 1.9.0 on 2026-11-14) implements the Iceberg REST catalog API so multiple
engines can share it. [Unity Catalog OSS][uc-oss] (Apache-2.0, v0.7.0 on 2026-10-13 per `gh api`; already covered in the
[catalog landscape](semantic-layers-data-catalog-landscape.md)) is the open-source sibling of Databricks' governance layer. Both are access-control and discovery points; semantic-layer and
lineage coverage is in the [catalog landscape](semantic-layers-data-catalog-landscape.md). Not researched
here: AWS Glue, Hive Metastore, or each catalog's RBAC detail.

## Warehouse-native agents

| Product | What it is (documented) | Permission model (documented) |
|---|---|---|
| [Snowflake Cortex Agents][cortex] | Managed agents that plan, call tools (Cortex Analyst over semantic views, Cortex Search, custom stored-procedure/UDF tools, code execution, web search) and call remote MCP servers | Caller needs the `SNOWFLAKE.CORTEX_USER` or `SNOWFLAKE.CORTEX_AGENT_USER` database role plus privileges on the agent and its tools' objects; if the role cannot use a tool, the run can still continue with the tools it can access. The page states no GA status |
| [Databricks Genie][genie-docs] | See [databricks-genie-analysis.md](../agents/databricks-genie-analysis.md): Genie One and Agents GA on 2026-06-16, Ontology in Public Preview (per that doc) | Unity Catalog governs answers (Genie docs). Pricing conflict, not resolved: the [Genie page][genie-docs] says user usage of Genie One and Agents is free through 2027-01-31, while the analysis doc records pay-as-you-go from 2026-07-06 with about 150 free DBUs per user per month, sourced from community posts |
| [BigQuery conversational analytics][bq-ca] | Data agents bundling up to 100 knowledge sources with instructions and verified queries; runs SQL or [GQL](../../glossary.md#knowledge-structures) | Agent reaches only data the user may query; no write or DML operations; the page gives no release status |
| [Fabric data agent][fabric] | Already analysed in [microsoft-365-copilot-analysis.md](../agents/microsoft-365-copilot-analysis.md) (GA, read-only; that doc notes Fabric's overview files it under the preview Fabric IQ workload). Added here: up to five sources; needs F2 or higher capacity, or Power BI Premium P1 or higher with Fabric enabled | Requesting user's identity; honors Purview DLP and access policies; answers capped at 25 rows and 25 columns |

Our reading: three of four document read-only access (BigQuery and Fabric explicitly bar writes) and all
inherit the caller's permissions; Snowflake Cortex custom tools can run stored procedures, so write exposure
there depends on the tool. The enterprise positioning is in
[agentic-enterprise-os-landscape.md](../frameworks/agentic-enterprise-os-landscape.md).

## Local engines as agent scratch space

An agent can pull a bounded extract into an in-process engine and compute there instead of running exploratory
queries against the warehouse.

| Engine | License | Latest release (2026-11-21) | Note |
|---|---|---|---|
| [DuckDB][duckdb] | MIT | v2.0.1 (2026-11-20) | In-process SQL; DuckLake 1.1 requires 2.0.0 or later. MotherDuck's MCP server is covered in [agentic-database-access-landscape.md](agentic-database-access-landscape.md) |
| [chDB][chdb] | Apache-2.0 | v4.5.1 (2026-11-18) | In-process ClickHouse engine |
| [Polars][polars] | MIT | py-2.2.0 (2026-11-24, checked 2026-11-26) | DataFrame library; not SQL-first |

DuckDB's [security guidance][duckdb-secure] lists settings for running untrusted SQL: `enable_external_access =
false`, allow-lists (`allowed_directories`), disabling auto-install and community extensions,
`lock_configuration`, and caps (`memory_limit`, `threads`, `max_temp_directory_size`). The same page says
these are defense in depth and "not a substitute for proper sandboxing", so isolate the process too. The
local-scratch pattern is the author's inference; no source here benchmarks it for agents.

## Cost and permission controls

| Platform | Control (documented) | Limit stated by the docs |
|---|---|---|
| Snowflake | [Resource monitors][sf-rm]: credit quota with notify, suspend, or suspend-immediately triggers, at account or warehouse scope | Do not cover serverless features and AI services; use budgets for those |
| BigQuery | [Cost controls][bq-cost]: maximum bytes billed (query fails before running), custom daily quotas per project or user, dry run, reservation max slots | Max bytes and custom quotas apply to on-demand pricing; the conversational-analytics page recommends project-, user- and query-level limits and labels agent jobs (`ca-bq-job`, `data-agent-id`) for billing filters |
| Databricks | Genie budgets and cost controls managed by account admins ([Genie docs][genie-docs]) | Detail not researched |
| Fabric | Capacity-based (F2 or higher required); Purview policies constrain data access ([docs][fabric]) | Capacity throttling not researched |

Row- and column-level policies: Fabric's page says RLS and CLS on Power BI semantic models still apply to the
agent. Equivalents for Snowflake, BigQuery and Databricks were not researched for this doc.

## Not verified

- Hudi branching, Unity Catalog and Polaris RBAC details, Glue; Snowflake budget scope (the fetched page did
  not describe budgets); lakeFS hooks and zero-copy claims (docs page did not load).
- Any measured benefit of agent-on-a-branch workflows: no source here reports one.
- Whether Cortex Agents and BigQuery conversational analytics are GA: the cited pages do not say.

## Sources

| Source | Content |
|---|---|
| [Apache Iceberg][iceberg] · [branching page][iceberg-branching] | Version, license, branches and tags |
| [Delta Lake][delta] · [shallow clone docs][delta-clone] | Version, license, clone semantics |
| [Apache Hudi][hudi] · [DuckLake][ducklake] | Versions, licenses, catalog design |
| [Databricks lakehouse blog post][dbx-lakehouse] · [Delta docs][delta-docs] · [Hudi overview][hudi-docs] | Lake, lakehouse and warehouse definitions |
| [Project Nessie][nessie] · [guide][nessie-about] · [lakeFS][lakefs] | Catalog and storage branching, licenses |
| [Apache Polaris][polaris] · [Unity Catalog OSS][uc-oss] | Open catalogs |
| [Cortex Agents][cortex] · [Genie][genie-docs] · [BigQuery conversational analytics][bq-ca] · [Fabric data agent][fabric] | Warehouse-native agents |
| [DuckDB][duckdb] · [securing DuckDB][duckdb-secure] · [chDB][chdb] · [Polars][polars] | Local engines |
| [Snowflake resource monitors][sf-rm] · [BigQuery cost controls][bq-cost] | Cost controls |

[dbx-lakehouse]: https://www.databricks.com/blog/what-is-data-lakehouse
[delta-docs]: https://docs.delta.io/
[hudi-docs]: https://hudi.apache.org/docs/overview
[iceberg]: https://github.com/apache/iceberg
[iceberg-branching]: https://iceberg.apache.org/docs/latest/branching/
[delta]: https://github.com/delta-io/delta
[delta-clone]: https://docs.delta.io/delta-utility/
[hudi]: https://github.com/apache/hudi
[ducklake]: https://ducklake.select/
[nessie]: https://github.com/projectnessie/nessie
[nessie-about]: https://projectnessie.org/guides/about/
[lakefs]: https://github.com/treeverse/lakeFS
[polaris]: https://polaris.apache.org/
[uc-oss]: https://github.com/unitycatalog/unitycatalog
[cortex]: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents
[genie-docs]: https://docs.databricks.com/aws/en/genie/
[bq-ca]: https://docs.cloud.google.com/bigquery/docs/conversational-analytics
[fabric]: https://learn.microsoft.com/en-us/fabric/data-science/concept-data-agent
[duckdb]: https://github.com/duckdb/duckdb
[duckdb-secure]: https://duckdb.org/docs/2.0/operations_manual/securing_duckdb/overview.html
[chdb]: https://github.com/chdb-io/chdb
[polars]: https://github.com/pola-rs/polars
[sf-rm]: https://docs.snowflake.com/en/user-guide/resource-monitors
[bq-cost]: https://docs.cloud.google.com/bigquery/docs/controlling-costs
