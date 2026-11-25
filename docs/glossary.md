---
title: Glossary and concept owners
purpose: Where each recurring term and abbreviation is defined in this corpus, so a doc links its owner instead of defining it again.
created: 2026-11-21
updated: 2026-11-25
validated_links_on: 2026-11-25
status: reference
---

Each row names a term, its expansion if it is an abbreviation, and the one section that owns its
definition. This page holds no definitions: read the owner. When a doc uses a term from this list,
it expands an abbreviation on first use and links the owner section rather than restating it
(owner decision D7, plan 0015). Before defining a new concept, search the corpus for an existing
definition first; if one exists, link it, and if not, add the term here with its new owner.

## Agents and protocols

| Term | Expansion | Owner |
|---|---|---|
| A2A | Agent-to-Agent Protocol | [ag-ui-protocol-landscape.md § A2A][a2a] |
| AG-UI | Agent-User Interaction Protocol | [ag-ui-protocol-landscape.md § AG-UI][ag-ui] |
| MCP | Model Context Protocol | [ag-ui-protocol-landscape.md § MCP as a Protocol Spec][mcp] |
| Prompt, context, harness, loop, graph, flow and spec engineering | — | [agentic-engineering-disciplines-landscape.md § 1][disciplines-1] |
| Agent identity, delegated authorization | — | [agent-identity-auth-landscape.md § 1][identity-1] and [§ 2][identity-2] |

## Memory and retrieval

| Term | Expansion | Owner |
|---|---|---|
| Episodic, semantic, procedural memory | — | [CC-memory-tooling-landscape.md § Memory Taxonomy][memory] |
| RAG | Retrieval-Augmented Generation | [agent-frameworks-infrastructure-landscape.md § RAG patterns at a glance][rag] |
| GraphRAG | Graph-based retrieval-augmented generation | [agent-frameworks-infrastructure-landscape.md § GraphRAG family][graphrag] |
| Hybrid search, RRF | RRF = Reciprocal Rank Fusion | [agent-frameworks-infrastructure-landscape.md § Hybrid search & query transforms][hybrid] |
| Reranker | — | [agent-frameworks-infrastructure-landscape.md § Rerankers][rerankers] |

## Knowledge structures

| Term | Expansion | Owner |
|---|---|---|
| Tag, controlled vocabulary, taxonomy, thesaurus, ontology, knowledge graph | — | [semantic-layers-data-catalog-landscape.md § Choosing a Structure][structure] |
| RDF | Resource Description Framework | [semantic-layers-data-catalog-landscape.md § Formal Ontologies & Semantic Web][formal] |
| OWL | Web Ontology Language | [same section][formal] |
| SKOS | Simple Knowledge Organization System | [same section][formal] |
| RDFS | RDF Schema | [same section][formal] |
| Triple, entailment | — | [same section][formal] (triple: the RDF bullet; entailment: the LeanRDF entry) |
| Lean, Elpi | — | [same section][formal] (the LeanRDF entry) |
| SHACL | Shapes Constraint Language | [same section][formal] |
| SPARQL | The W3C query language for RDF | [same section][formal] |
| JSON-LD | The W3C JSON format for Linked Data | [same section][formal] |
| Property graph | — | [graph-databases-query-languages-landscape.md § Property Graph vs RDF][pg-rdf] |
| Cypher, GQL | GQL = the ISO graph query language (ISO/IEC 39075) | [graph-databases-query-languages-landscape.md § Query Languages][query] |
| Data lake, lakehouse, data warehouse | — | [data-platforms-lakehouse-landscape.md § Data lake vs lakehouse vs data warehouse][lakehouse] |
| MOC, Zettelkasten, PARA, Diátaxis | MOC = Map of Content; PARA = Projects, Areas, Resources, Archives | [knowledge-organisation-methods-landscape.md § Methods at a glance][methods] |

## Evaluation

| Term | Expansion | Owner |
|---|---|---|
| BLEU | Bilingual Evaluation Understudy | [agent-evaluation-metrics-landscape.md § BLEU][bleu] |
| ROUGE | Recall-Oriented Understudy for Gisting Evaluation | [agent-evaluation-metrics-landscape.md § ROUGE][rouge] |
| LLM-as-a-judge | — | [agent-evaluation-metrics-landscape.md § LLM-as-a-Judge Quality Assessment][judge] |
| RLVR | Reinforcement Learning with Verifiable Rewards | [agent-evaluation-metrics-landscape.md § Verifiable rewards (RLVR)][rlvr] |
| RSI | recursive self-improvement | [weco-aide-recursive-self-improvement-analysis.md][rsi] |

## Sources

This page cites only corpus docs; each owner section carries its own sources.

[a2a]: non-cc/protocols/ag-ui-protocol-landscape.md#a2a-agent-to-agent-protocol
[ag-ui]: non-cc/protocols/ag-ui-protocol-landscape.md#ag-ui-agent-user-interaction-protocol
[mcp]: non-cc/protocols/ag-ui-protocol-landscape.md#mcp-as-a-protocol-spec
[identity-1]: sdlc-lcm/agent-identity-auth-landscape.md#1-authenticate-the-agent-agent-as-a-first-class-principal
[identity-2]: sdlc-lcm/agent-identity-auth-landscape.md#2-authorize-the-agent-on-behalf-of-a-human-delegated-scoped-auditable
[disciplines-1]: sdlc-lcm/agentic-engineering-disciplines-landscape.md#1-the--engineering-ladder
[memory]: cc-community/CC-memory-tooling-landscape.md#memory-taxonomy
[rag]: non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#rag-patterns-at-a-glance
[graphrag]: non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#graphrag-family
[hybrid]: non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#hybrid-search--query-transforms
[rerankers]: non-cc/frameworks/agent-frameworks-infrastructure-landscape.md#rerankers
[structure]: non-cc/infrastructure/semantic-layers-data-catalog-landscape.md#choosing-a-structure
[formal]: non-cc/infrastructure/semantic-layers-data-catalog-landscape.md#formal-ontologies--semantic-web
[pg-rdf]: non-cc/infrastructure/graph-databases-query-languages-landscape.md#property-graph-vs-rdf
[query]: non-cc/infrastructure/graph-databases-query-languages-landscape.md#query-languages
[lakehouse]: non-cc/infrastructure/data-platforms-lakehouse-landscape.md#data-lake-vs-lakehouse-vs-data-warehouse
[methods]: non-cc/knowledge-management/knowledge-organisation-methods-landscape.md#methods-at-a-glance
[bleu]: sdlc-lcm/agent-evaluation-metrics-landscape.md#bleu-bilingual-evaluation-understudy
[rouge]: sdlc-lcm/agent-evaluation-metrics-landscape.md#rouge-recall-oriented-understudy-for-gisting-evaluation
[judge]: sdlc-lcm/agent-evaluation-metrics-landscape.md#llm-as-a-judge-quality-assessment
[rlvr]: sdlc-lcm/agent-evaluation-metrics-landscape.md#verifiable-rewards-rlvr
[rsi]: non-cc/reference/weco-aide-recursive-self-improvement-analysis.md
