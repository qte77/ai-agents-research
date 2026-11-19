---
title: Graph Databases & Query Languages — Agent Landscape
source: https://opencypher.org/
purpose: A thin, dated table of the graph query languages (Cypher/openCypher, ISO GQL, SPARQL, Gremlin, Datalog), the graph databases most relevant to agents, text-to-query evidence, and vendor and vendor-labs graph MCP servers, linking the per-tool analyses in this corpus. Facts as of 2026-11-19.
created: 2026-11-19
updated: 2026-11-19
validated_links: 2026-11-19
status: assess
---

## Why This Doc

An agent that reads or writes a graph needs two things: a database it can reach and a query language it
(or a generator in front of it) can write correctly. This page is the index for both. It is deliberately
thin: per-tool depth lives in the analyses linked below, and knowledge-graph construction, GraphRAG
evidence and ontologies are out of scope here. Companion pages: [Agentic Database Access][adb] (the SQL
side: MCP servers, text-to-SQL, write safety) and [Semantic Layers & Data Catalogs][sem] (RDF, OWL and
SPARQL as a standards stack).

Evidence labels: **documented** (first-party docs or README), **shipped** (a release or repo state
observed), **vendor claim** / **authors' claim** (a number from the project's own abstract or README,
not independently reproduced).

## Query Languages

| Language | Owner / standard | Status on 2026-11-19 | Evidence |
|---|---|---|---|
| Cypher / [openCypher][opencypher] | Cypher was developed by Neo4j, which holds the trademarks; openCypher is the open specification effort | The openCypher site says the language is evolving toward ISO GQL and adds GQL features incrementally, aiming at conformance over time | documented |
| [GQL][gqlsite] (ISO/IEC 39075) | ISO/IEC JTC 1 SC 32 WG 3 | Published in April 2024. A news entry dated 2024-04-17 on the GQL standards site announces it as officially published and sold through the ISO web store; the openCypher site gives 2024-04-11. BigQuery's data agents can run GQL (see [Data Platforms][dp]). The exact day and any later corrigendum are **unverified** (iso.org returned HTTP 403) | documented (published); day unverified |
| [SPARQL][sparql11] | W3C | SPARQL 1.1 Query is a W3C Recommendation dated 2013-03-21. A [SPARQL 1.2 Query][sparql12] document is a W3C Working Draft dated 2026-11-16 on the Recommendation track | documented |
| Gremlin ([Apache TinkerPop][tinkerpop]) | Apache Software Foundation | The project site shows TinkerPop 3.8.2, released 2026-09-01; the repo's tag list also shows core tags `4.0.0-beta.1` to `4.0.0-beta.3` (and Go-driver `gremlin-go/v4.0.0-beta.*` tags), so 4.0 is in beta | documented (site); shipped (tags) |
| Datalog | A family of recursive logic query languages, not one standard (no governing body checked here) | Used by embedded stores such as Minigraf; see [Minigraf][minigraf] | documented (per that analysis) |

What this means for agents: Cypher/openCypher is supported by most databases listed below (Neo4j,
Memgraph, FalkorDB, Kuzu, Neptune), GQL is the ISO direction it is
converging on, SPARQL belongs to the RDF world, and Gremlin is a traversal language embedded in host
languages.

## Graph Databases Relevant to Agents

Stars, push date and latest release come from `gh api` on 2026-11-19. The License column is the text of
the repository's LICENSE file for Neo4j, Memgraph and FalkorDB; for the other rows it is GitHub's
licence metadata (Minigraf: `Cargo.toml` plus its licence files, per its analysis). Not marketing copy.

| Database | Model / query language | License (repo LICENSE) | Stars · last push · latest release | Notes (evidence) |
|---|---|---|---|---|
| [Neo4j][neo4j] | Property graph; Cypher | GPL-3.0 text in `LICENSE.txt`; commercial editions are separate and not examined here | 17,459 · 2026-11-06 · the repo's latest GitHub *release* is a 2017 alpha, so use tags (newest `2026.10.2`) | Cypher was developed by Neo4j (per openCypher). Agent-memory project in the corpus: [Neo4j Agent Memory][fw] |
| [Memgraph][memgraph] | In-memory property graph; Cypher-compatible | `LICENSE` says files are variously Business Source License 1.1 or Memgraph Enterprise License | 4,665 · 2026-11-19 · v3.14.0 (2026-10-21) | BUSL-1.1 is not OSI-approved per [SPDX][spdx-busl] (`isOsiApproved: false`). Self-described for GraphRAG and agent memory (vendor claim) |
| [FalkorDB][falkordb] | Property graph on GraphBLAS sparse matrices; openCypher | Server Side Public License v1 (`LICENSE`) | 10,506 · 2026-11-19 · v6.0.4 (2026-11-05) | SSPL-1.0 is not OSI-approved per [SPDX][spdx-sspl] (`isOsiApproved: false`). Positions itself as a knowledge-graph store for GraphRAG (vendor claim) |
| [Kuzu][kuzu] | Embedded property graph; Cypher | MIT | 4,022 · **archived** · v0.11.3 (2025-10-10) | Repo archived by its owner (GitHub flag; last push 2025-10-10). The corpus's [LatticeDB][latticedb] analysis uses it as the comparison point. Treat as unmaintained unless a maintained fork is verified |
| [Apache AGE][age] | PostgreSQL extension (query language not re-checked in this pass) | Apache-2.0 | 4,954 · 2026-11-04 · `PG18/v1.8.0-rc0` (2026-07-09) | The releases page lists per-Postgres-version release candidates; adds graph queries to an existing Postgres |
| [NebulaGraph][nebula] | Distributed property graph | Apache-2.0 | 12,473 · 2026-09-08 · latest release 2024-05-17 | High star count, but the releases page shows no release since 2024-05; pushes continue |
| Amazon Neptune | Managed service; openCypher and Gremlin (Neptune Database), openCypher (Neptune Analytics), per the AWS MCP server README | Managed service, no repo | n/a | See the MCP table. SPARQL support is **not verified here** |
| [HelixDB][helixdb] | Graph + vector; DSL query builders; source builds also document an openCypher profile (reads and CRUD, `POST /v2/cypher`) per its README | Apache-2.0 | 6,303 · 2026-11-19 · v3.7.0 (2026-11-11) | Corpus analysis: [HelixDB][helixdb-doc] (see it for the query model) |
| [LatticeDB][latticedb-gh] | Embedded graph + vector, single writer | MIT | 757 · 2026-11-18 | Corpus analysis: [LatticeDB][latticedb] |
| [Minigraf][minigraf-gh] | Embedded bi-temporal graph; Datalog | `MIT OR Apache-2.0` (`Cargo.toml`; see [Minigraf][minigraf]) | 229 · 2026-11-19 | Corpus analysis: [Minigraf][minigraf] |

TigerGraph was not verified first-party in this pass (no public source repository found by search) and is
left out rather than described from memory.

## Text-to-Query for Agents

Evidence is thin and mostly the authors' own claims.

| Item | What it is | Result (as dated) | Evidence |
|---|---|---|---|
| [Text2Cypher (arXiv 2412.10064)][t2c] | Neo4j-authored paper that merges and cleans public Text2Cypher datasets into 44,387 instances and fine-tunes models on them | Submitted 2024-12-13. Fine-tuning improved Google-BLEU and exact-match over baselines; the abstract says general LLMs often return incomplete or incorrect Cypher | authors' claim (abstract only) |
| [SPARQL-LLM (arXiv 2512.14277)][sparqlllm] | Open-source system that turns natural-language questions into SPARQL over bioinformatics knowledge graphs | v1 2025-12-16, revised 2026-09-23. Abstract claims up to 59% higher F1 and up to 27x faster than the second-best challenge system, at most $0.01 per question | authors' claim |
| [SPARQL-LLM at TEXT2SPARQL 2026 (arXiv 2610.13648)][sparqlllm26] | Challenge paper by the same five authors | Submitted 2026-10-09. Abstract: ranks first overall among eight competing approaches; up to 59% higher accuracy than the second-best | authors' claim |

The organisers' own TEXT2SPARQL results pages were unreachable during this pass, so no challenge ranking
is asserted beyond the authors' abstracts, and these numbers are not comparable across languages.

## Graph MCP Servers

| Server | Maintainer | License | Tools and read-only control (documented) | Status |
|---|---|---|---|---|
| [neo4j/mcp][neo4j-mcp] | Neo4j (the Labs README points to it as the official product server) | `LICENSE.txt` plus a `NOTICE.txt` describing mixed terms: GPLv3 for the bundled software, Neo4j's commercial agreements when used with Aura or the commercial products | `get-schema`, `read-cypher`, `write-cypher`, `list-gds-procedures`; `NEO4J_MCP_READ_ONLY=true` disables writes. The README warns a procedure misclassified as read-only could bypass the check | 309 stars, pushed 2026-11-16 |
| [neo4j-contrib/mcp-neo4j][neo4j-labs] | Neo4j Labs (field team, no SLAs per its README) | MIT | `mcp-neo4j-cypher` (schema plus generated Cypher; needs APOC) and `mcp-neo4j-memory` (knowledge-graph memory); `NEO4J_READ_ONLY=true` or `--read-only` | 991 stars, pushed 2026-09-09 |
| [FalkorDB-MCPServer][falkordb-mcp] | FalkorDB | MIT | `query_graph`, `query_graph_readonly`, schema tools; `FALKORDB_DEFAULT_READONLY=true` makes read-only the default, but the caller can override it per query with the `readOnly` parameter, so it is a default, not enforcement | 42 stars, pushed 2026-11-17 |
| [mcp-memgraph in memgraph/ai-toolkit][memgraph-ai] | Memgraph | Apache-2.0 for the repo (GitHub metadata; the MCP package's own licence not checked) | Seven tools on the default server: `run_cypher_query`, `search_schema`, `get_node_schema`, `get_relationship_schema`, `get_enum_schema`, `list_databases`, `use_database`. `MCP_READ_ONLY` defaults to `true` and blocks CREATE, MERGE, DELETE, SET, DROP, REMOVE (README); the README says the smaller `memgraph-experimental` server exposes a different set (not read) | repo 119 stars, pushed 2026-11-17 |
| [Amazon Neptune MCP][neptune-mcp] (`awslabs/mcp`) | AWS Labs | Apache-2.0 (monorepo) | Tools `run_opencypher_query`, `run_gremlin_query`, `get_status`, `get_schema` (server.py). The README says "This server will run any query sent to it" and points to IAM permissions; server.py reads only endpoint and HTTPS settings from the environment, so there is no read-only switch | monorepo 9,932 stars |

Pattern: every server exposes schema plus a query tool. Read-only handling differs: Neo4j and Neo4j Labs
document an opt-in switch, FalkorDB a per-query default the caller can override, Memgraph a default-on
switch (not on the experimental server), and Neptune none (use IAM). The Neo4j README itself says
read-only classification can be bypassed, so a switch is a convenience, not a boundary. For role,
branch and injection controls see [Write safety][adb-ws] in Agentic Database Access.

## Not Verified

- Exact ISO publication day for GQL (iso.org and the ANSI store blocked).
- NebulaGraph's openCypher compatibility, Neptune's SPARQL support, and TigerGraph (no first-party page read).
- TEXT2SPARQL organiser result tables (site unreachable); Neo4j Enterprise licence terms.

## Sources

| Source | Content |
|---|---|
| [openCypher][opencypher] · [GQL standards site][gqlsite] | Cypher/GQL relationship, GQL publication status |
| [SPARQL 1.1 Query][sparql11] · [SPARQL 1.2 Query][sparql12] | W3C status and dates |
| [Apache TinkerPop][tinkerpop] | Gremlin, 3.8.2 release date |
| SPDX [BUSL-1.1][spdx-busl] · [SSPL-1.0][spdx-sspl] | OSI-approval flag (license-list-data JSON, `isOsiApproved`) |
| [neo4j][neo4j] · [memgraph][memgraph] · [FalkorDB][falkordb] · [kuzu][kuzu] · [age][age] · [nebula][nebula] · [helix-db][helixdb] | Repo metadata, LICENSE files, releases via `gh api`, 2026-11-19 |
| [latticedb][latticedb-gh] · [minigraf][minigraf-gh] | Repo metadata via `gh api`, 2026-11-19 |
| [Text2Cypher][t2c] · [SPARQL-LLM][sparqlllm] · [SPARQL-LLM 2026][sparqlllm26] | arXiv abstract pages |
| [neo4j/mcp][neo4j-mcp] · [mcp-neo4j][neo4j-labs] · [FalkorDB-MCPServer][falkordb-mcp] · [ai-toolkit][memgraph-ai] · [Neptune MCP][neptune-mcp] | MCP tools, read-only controls, licences |

[adb]: agentic-database-access-landscape.md
[adb-ws]: agentic-database-access-landscape.md#write-safety
[dp]: data-platforms-lakehouse-landscape.md
[spdx-busl]: https://spdx.org/licenses/BUSL-1.1.html
[spdx-sspl]: https://spdx.org/licenses/SSPL-1.0.html
[sem]: semantic-layers-data-catalog-landscape.md#formal-ontologies--semantic-web
[fw]: ../frameworks/agent-frameworks-infrastructure-landscape.md
[helixdb-doc]: ../context-memory/helixdb-analysis.md
[latticedb]: ../context-memory/latticedb-analysis.md
[minigraf]: ../context-memory/minigraf-analysis.md
[opencypher]: https://opencypher.org/
[gqlsite]: https://www.gqlstandards.org/
[sparql11]: https://www.w3.org/TR/sparql11-query/
[sparql12]: https://www.w3.org/TR/sparql12-query/
[tinkerpop]: https://tinkerpop.apache.org/
[neo4j]: https://github.com/neo4j/neo4j
[memgraph]: https://github.com/memgraph/memgraph
[falkordb]: https://github.com/FalkorDB/FalkorDB
[kuzu]: https://github.com/kuzudb/kuzu
[age]: https://github.com/apache/age
[nebula]: https://github.com/vesoft-inc/nebula
[helixdb]: https://github.com/HelixDB/helix-db
[latticedb-gh]: https://github.com/jeffhajewski/latticedb
[minigraf-gh]: https://github.com/project-minigraf/minigraf
[t2c]: https://arxiv.org/abs/2412.10064
[sparqlllm]: https://arxiv.org/abs/2512.14277
[sparqlllm26]: https://arxiv.org/abs/2610.13648
[neo4j-mcp]: https://github.com/neo4j/mcp
[neo4j-labs]: https://github.com/neo4j-contrib/mcp-neo4j
[falkordb-mcp]: https://github.com/FalkorDB/FalkorDB-MCPServer
[memgraph-ai]: https://github.com/memgraph/ai-toolkit
[neptune-mcp]: https://github.com/awslabs/mcp/tree/main/src/amazon-neptune-mcp-server
