---
title: Semantic Layers & Data Catalogs — Agentic Data Access Landscape
source: https://cube.dev/docs/product/apis-integrations/mcp-server
purpose: The semantic-layer (consistent metrics) and data-catalog (discovery, lineage, governance) substrate that grounds agentic data access — what each tool exposes to an agent (MCP / SDK / NL query), and how it relates to the agent-native context layers (Databricks Genie Ontology, Open Knowledge Format). Reference catalog verified 2026-06-22.
created: 2026-06-22
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Assess

## Why Agents Need This

When an agent answers a data question ("Q2 revenue by region?"), free-form text-to-SQL over raw tables is unreliable — it hallucinates joins, misnames columns, and re-invents metric definitions on every call. Two substrate layers harden this:

- **Semantic / metrics layers** define metrics, dimensions, and joins *once*, so the agent queries governed definitions instead of authoring raw SQL.
- **Data catalogs** provide discovery, lineage, ownership, and permissions, so the agent knows *what exists* and *what it may touch*.

The agent-relevant question for each tool is: **what does it expose to an agent** — a Model Context Protocol (MCP) server, an SDK tool layer, or natural-language query? The agent-native evolution of this substrate is covered under [The Agent-Native Layer](#the-agent-native-layer) below.

## Semantic / Metrics Layers

Define metrics/dimensions once; query consistently across clients.

| Tool | License | Agent surface | Notes |
|---|---|---|---|
| [Cube][cube] | Apache-2.0 (~20k★) | **MCP server** (hosted, OAuth PKCE) + outbound MCP connectors | Most agent-ready of the group; `claude mcp add` documented |
| [dbt MetricFlow / Semantic Layer][metricflow] | Apache-2.0 (~1.6k★) | JDBC/GraphQL API; community MCP wrappers only | Engine behind dbt Cloud's Semantic Layer; part of the Open Semantic Interchange effort |
| [Malloy][malloy] | MIT (Google; ~2.5k★) | None official (one community MCP wrapper) | Semantic *query language* compiling to SQL; VS Code-first |
| AtScale (`atscale.com`, homepage dead 2026-07-23 — 404) | Proprietary | Partner [MQO-MCP][atscale-mqo] (typed query grammar) | MQO validates every reference against a live catalog snapshot to block hallucinated SQL — notable agent-safety pattern (early/reference impl) |

## Catalogs / Metadata / Governance

Discovery, lineage, ownership, and permissions across the data estate.

| Tool | License | Agent surface | Notes |
|---|---|---|---|
| [OpenMetadata][openmetadata] | Apache-2.0 (~14k★) | **Official MCP** (OAuth PKCE, user-scoped perms) | Self-describes as "for humans, AI assistants, and agents" |
| [DataHub][datahub] | Apache-2.0 (~12k★) | **Official MCP** ([acryldata/mcp-server-datahub][datahub-mcp]) | NL search, column-level lineage, usage-grounded SQL generation |
| [Unity Catalog (OSS)][unity-catalog] | Apache-2.0 / LF (~3.4k★) | **SDK** (`unitycatalog-ai`) with Anthropic/LangChain/etc. integrations | UC functions as agent tools; LF project, distinct from Databricks' proprietary UC |
| [Apache Atlas][atlas] | Apache-2.0 (~2.1k★) | None (pre-MCP; REST only) | Hadoop-era lineage backend; no LLM-facing surface |
| [Google Dataplex / Universal Catalog][dataplex] | Proprietary (Google) | Gemini NL querying; underpins the OKF reference impl | Managed GCP governance + metadata |

## Formal Ontologies & Semantic Web

Before LLM-embedded knowledge graphs, the W3C Semantic Web stack formalized machine-readable meaning. These standards predate agents but increasingly **connect to, are excluded by, or enhance** the LLM-native layers below:

- **[RDF][rdf]** — subject–predicate–object triples; the base data model for graph-structured facts.
- **[OWL][owl]** — Web Ontology Language: classes, properties, and logical constraints enabling automated inference (open-world assumption — unstated ≠ false).
- **[SKOS][skos]** — lightweight taxonomy/thesaurus vocabulary (broader/narrower/related) for concept schemes; the pragmatic middle between flat tags and a full OWL ontology.
- **[SPARQL][sparql]** — the query language for RDF graphs (the "SQL of the Semantic Web"); an MCP-wrappable agent surface alongside the catalogs above.

**Open- vs closed-world.** OWL/RDF assume an *open world* (absent ≠ false), which fits the web's incompleteness but makes hard validation awkward; [SHACL][shacl] adds closed-world *shape* constraints for validation. SQL catalogs and most semantic layers above are closed-world — an agent reasoning across both must know which regime applies.

**connect / exclude / enhance** — how formal ontologies relate to the LLM-embedded KGs (Genie Ontology, GraphRAG) and the catalog/semantic layers above:

- **Connect** — an existing OWL/SKOS ontology can seed or constrain an LLM KG's entity/relation types instead of extracting them from scratch; a SPARQL endpoint is a queryable tool surface (MCP-wrappable) next to the catalogs above.
- **Exclude** — for many agent tasks full OWL reasoning is overkill: LLMs approximate semantic relations statistically, and a heavyweight ontology adds authoring/maintenance cost without payoff; the pragmatic stack often stops at SKOS + a catalog.
- **Enhance** — where correctness must be *provable* (compliance, finance, clinical), formal ontologies + SHACL give the deterministic backbone probabilistic LLM KGs lack; the two compose (LLM for recall/extraction, ontology for precision/validation).

This is the formal-semantics counterpart to [The Agent-Native Layer](#the-agent-native-layer) below: Genie Ontology and OKF are the *LLM-native* curation of the same verified business meaning that OWL/SKOS encode *formally*.

## The Agent-Native Layer

The generic layers above solve the *plumbing* — governed APIs an agent can query. But an agent hitting a raw semantic API still re-derives business meaning on every call (and can still get it wrong). Two efforts go further, and are analyzed in depth elsewhere in this repo:

- **[Databricks Genie Ontology](databricks-genie-analysis.md#genie-ontology)** — a persistent, authority-ranked context graph (metric definitions, joins, synonyms, business logic) built from query history + workplace apps, **MCP-exposed** so external agents consume the same verified context instead of re-deriving it per query.
- **[Open Knowledge Format](open-knowledge-format-analysis.md)** — a vendor-neutral, Apache-2.0 spec (Google Cloud, v0.1) for portable "knowledge bundles" (markdown + YAML) with AI agents as first-class consumers — the platform-independent interchange format for that curated context.

Together they mark the shift from "query the catalog at runtime" to "pre-loaded, verified business context the agent can trust."

## Cross-References

- [databricks-genie-analysis.md](databricks-genie-analysis.md) — Genie One agentic data coworker + Genie Ontology (the agent-native semantic graph)
- [open-knowledge-format-analysis.md](open-knowledge-format-analysis.md) — OKF portable knowledge-bundle spec
- [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) — §7 RAG & retrieval infrastructure agents call as tools

## Sources

| Source | Content |
|---|---|
| [Cube MCP server docs][cube] | Hosted MCP server, OAuth PKCE, connectors |
| [dbt MetricFlow][metricflow] | Metrics-layer engine; Open Semantic Interchange |
| [Malloy][malloy] | Semantic query language |
| AtScale · [MQO-MCP][atscale-mqo] | Proprietary semantic layer; typed-query MCP pattern (AtScale homepage dead 2026-07-23) |
| [OpenMetadata][openmetadata] | Catalog with official MCP module |
| [DataHub][datahub] · [MCP server][datahub-mcp] | Catalog with official MCP server |
| [Unity Catalog OSS][unity-catalog] | LF open catalog + `unitycatalog-ai` SDK |
| [Apache Atlas][atlas] | Hadoop-era governance framework |
| [Google Dataplex][dataplex] | GCP governance/metadata + Gemini |
| [RDF][rdf] · [OWL][owl] · [SKOS][skos] · [SPARQL][sparql] · [SHACL][shacl] | W3C Semantic Web standards — formal ontologies, query, validation; open- vs closed-world; connect/exclude/enhance vs LLM KGs |

[cube]: https://cube.dev/docs/product/apis-integrations/mcp-server
[metricflow]: https://github.com/dbt-labs/metricflow
[malloy]: https://github.com/malloydata/malloy
[atscale-mqo]: https://github.com/joeyen-atscale/mqo-mcp
[openmetadata]: https://github.com/open-metadata/OpenMetadata
[datahub]: https://github.com/datahub-project/datahub
[datahub-mcp]: https://github.com/acryldata/mcp-server-datahub
[unity-catalog]: https://github.com/unitycatalog/unitycatalog
[atlas]: https://github.com/apache/atlas
[dataplex]: https://cloud.google.com/dataplex
[rdf]: https://www.w3.org/RDF/
[owl]: https://www.w3.org/OWL/
[skos]: https://www.w3.org/2004/02/skos/
[sparql]: https://www.w3.org/TR/sparql11-overview/
[shacl]: https://www.w3.org/TR/shacl/
