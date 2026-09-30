---
title: Semantic Layers & Data Catalogs — Agentic Data Access Landscape
source: https://cube.dev/docs/product/apis-integrations/mcp-server
purpose: The semantic-layer (consistent metrics) and data-catalog (discovery, lineage, governance) substrate that grounds agentic data access — what each tool exposes to an agent (MCP / SDK / NL query), and how it relates to the agent-native context layers (Databricks Genie Ontology, Open Knowledge Format). Reference catalog verified 2026-06-22.
created: 2026-06-22
updated: 2026-09-30
validated_links: 2026-09-30
status: assess
---

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

**A concrete "connect" instance: Vault-LD.** [Vault-LD][vault-ld] (Apache-2.0, 235★ verified 2026-09-24) is a 2026 third-party spec — not a W3C standard — that turns a Markdown note vault into linked data: YAML-LD frontmatter plus a shared `@context` file map note metadata to RDF triples, with reference Python converters (`vault_to_rdf.py` / `rdf_to_vault.py`) giving a lossless roundtrip between Markdown and RDF. It is a file-based, no-database instance of the connect pattern above — an ontology-backed `@context` a human edits as prose and a machine reads as a graph.

### Agent-native ontology tools (2026 MCP wave)

Five 2026 tools expose an ontology as an MCP surface for coding agents — the same "connect the agent to governed meaning" goal as Genie Ontology and OKF above, but scoped to a single ontology store rather than a whole platform. Scored 2026-09-30 against the [agent substrate rubric][rubric].

**[Ontology Atlas][ontology-atlas]** (MIT, 139★, pushed 2026-09-28) keeps a project's ontology as an `atlas/` folder of Markdown (`project`/`domain`/`capability`/`element`/`document` frontmatter types) that a desktop app, CLI, and MCP server read directly from disk — "local-first... no Atlas backend, account, or telemetry." Multiple coding agents (Claude Code, Codex, Cursor, Antigravity) connect via one MCP button each, and every proposed change to the ontology arrives as a Markdown diff a human reviews in Git before it lands, with unknowns surfaced as unknown rather than papered over. An `.ontology-atlas/llm-audit.jsonl` log records every model/provider transfer.

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| partial [README][ontology-atlas] ("MCP — one button per agent," no documented write-concurrency model) | partial [README][ontology-atlas] ("local-first... no Atlas backend"; cross-machine sync is via git push/pull only) | no data [README][ontology-atlas] (ontology content is human/agent-curated, not a deterministic extraction pipeline) | yes [README][ontology-atlas] ("Extensions are files a git diff shows you"; one-button MCP support across 4 agent clients) | yes [README][ontology-atlas] ("Your disk is the database; Git is the history"; History screen shows exact diffs) | yes [README][ontology-atlas] (wiki pages cite sources; code-evidence paths on every node; llm-audit.jsonl) |

`scored 2026-09-30`

**[open-ontologies][open-ontologies]** (MIT, 544★, pushed 2026-09-29) is a Rust MCP server (Oxigraph 0.5 for RDF/SPARQL 1.1) built around one loop — `plan` a change to a production OWL/SHACL ontology, `apply` it, watch for `drift`, `certify` what the engine derived, `rollback` if wrong — and it backs every claim with a Lean-4-checked certificate: "two tab-separated files… An auditor, months later… [runs] the same command, on the archived files. That auditor does not need an instance of this software." The free engine is explicitly single-user: "The engine does not give you a place for the evidence" — a shared, multi-reviewer store is upsold to the proprietary hosted `tesseractsemantics.com`, not shipped in the OSS binary. `rmcp` serves MCP over streamable HTTP, so one running server can, in principle, take connections from more than one client over a network.

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| partial [README][open-ontologies] (HTTP-transport MCP server can serve multiple clients, but the README states the OSS engine has no shared evidence store — that's the paid "for teams" tier) | partial [README][open-ontologies] ("`rmcp` for MCP over streamable HTTP" — a remote-reachable single node, not a documented multi-node deployment) | yes [README][open-ontologies] (Lean 4 v4.33.1 proof checker, pinned Oxigraph 0.5/Rust 1.85+, a `docs/determinism.md` page, "lost zero conclusions out of 2,583 differences") | yes [README][open-ontologies] (plugin marketplace; `--features embeddings,plugins,sql` build flags; alignment/crosswalk module) | yes [README][open-ontologies] (explicit plan/apply/drift/rollback loop over the ontology's own state) | yes [README][open-ontologies] (proof certificates re-checkable "months later… with no installation"; SQLite lineage store) |

`scored 2026-09-30`

**[EvoOntology][evoontology]** (ruc-datalab; MIT, 539★, pushed 2026-09-29; [arXiv:2609.15779][evoontology-paper]) is a self-evolving Ontology Layer for data agents, installed as a Claude Code or Codex plugin. A builder constructs a typed semantic graph (Terms/Mappings/Constraints/**Evidence** node families) grounded against the workload; an evolution agent proposes bounded updates and only "publishes a Candidate when paired evaluation shows a reproducible improvement over its Parent," else retains the Parent — a named `ontology_v0` → `ontology_vN+1` lifecycle. The repo layout labels its own store "Deterministic core." Reported gains (BIRD, DDR-Bench, InsightBench, four-backbone subset) are the authors' own benchmark, so treat as self-reported pending independent replication.

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| no data [README][evoontology] (single Claude Code/Codex session per ontology; no multi-agent concurrent-write semantics documented) | no [README][evoontology] (SQLite-backed local store; "read-only task replay" is local, not a network/cluster deployment) | yes [README][evoontology] (`evoontology/` labelled "Deterministic core"; gated Candidate-vs-Parent evaluation on fixed data/agent/decoding settings) | yes [README][evoontology] ("Continuous Self-Evolution" adapts Content/Schema/Tool layers without a rewrite; Claude Code + Codex plugins) | yes [README][evoontology] (named `ontology_v0`/`ontology_vN+1` versions; reject retains the prior Parent) | yes [README][evoontology] (dedicated Evidence node family; proposals verified against raw sources before commit) |

`scored 2026-09-30`

**[AWS context-ontology-accelerator][coa]** (Apache-2.0, 885★, pushed 2026-09-29) is a full semantic-context platform following a **Scan → Model → Serve** pipeline: ingest sources, induce an OWL 2 ontology (Bedrock Claude for concept extraction, Bedrock Cohere Embed v4 for grounding-ontology similarity, HermiT/ELK + OntoQA + OoPS! for three-tier validation), then serve it to agents via a Virtual Knowledge Graph (Ontop) over SPARQL and an MCP server. Access is namespace-isolated with RBAC: per-namespace roles (owner, maintainer, data-steward, data-analyst) plus cross-namespace `platform-admin`/`platform-viewer` roles — the clearest **Shared** evidence in this ontology set. It deploys as AWS CDK-provisioned microservices (control-plane, data-layer, ontology-engine, metric-service, vkg, mcp-server, context-manager), not a single local process. The repo is published as a **read-only mirror**: "We are not accepting pull requests at this time."

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| yes [README][coa] (namespace-isolated RBAC: owner/maintainer/data-steward/data-analyst plus cross-namespace platform-admin/platform-viewer roles) | yes [README][coa] (AWS CDK per-service stacks — control-plane, data-layer, ontology-engine, metric-service, vkg, mcp-server, context-manager — each independently deployed) | partial [ontology-engine README][coa-engine] (HermiT/ELK reasoners and OntoQA/OoPS! validation are deterministic; concept-extraction LLM "Amazon Bedrock Claude" has no pinned model ID) | yes [README][coa] (pluggable induction strategies; Athena federation connectors incl. a reference connector and Databricks) | no data [ontology-engine README][coa-engine] (a `proposals.py` review workflow gates changes, but no documented snapshot/diff/rollback of ontology state) | yes [ontology-engine README][coa-engine] (grounds against named foundational ontologies — Schema.org, Dublin Core, PROV-O, FOAF, FIBO — via three-tier formal validation reports) |

`scored 2026-09-30`

**[Utopia][utopia]** (DeepLethe; Apache-2.0, 7,972★, `gh api` 2026-09-30) is a single-binary (Rust + Postgres) "enterprise world model" that builds a **bitemporal knowledge graph** bottom-up from ingested documents rather than a hand-authored top-down ontology — its own README asks readers not to call it "an open-source take on Palantir," framing itself instead as "a different route to enterprise intelligence, built bottom up from knowledge governance to trustworthy decisions and simulation." A new knowledge base starts from one of five bundled vocabulary packs (schema.org, W3C Org, PROV-O, FOAF, IOF Core); a phrase is promoted to a relation only once it recurs across at least two documents, and every fact carries two clocks — `valid_from`/`valid_to` for when it held in the world, `recorded_at`/`invalidated_at` for when the system learned it — because corrections never overwrite, they supersede: "the change of mind is information" (verbatim from the project's own [`docs/decisions/README.md`][utopia-decisions] conventions). That `docs/decisions/` folder records real failures behind the design: decision [0012][utopia-0012] found 102 of 130 checkable facts written backwards under a naive domain/range check (schema.org's `employee(organization→person)` inverted to "Elon Musk employee Microsoft"), verdict "an empty predicate is honest silence; a reversed edge is a confident error." An MCP server exposes each knowledge base's read tools (facts-as-of-a-date, graph paths, "what changed last week") to Claude Desktop, Cursor and other clients with fine-grained permissions; anything an agent wants to record goes to a human review queue first.

Design lens — Lindenberg's *The Change of Mind Is Information* treats Utopia's bitemporal ledger as evidence that a four-week-old open-source project can already do "the knowledge half" of an ontology platform priced in the seven figures, provided it takes correction as seriously as its own decision records show — a reversed or superseded fact is never silently fixed in place, it is superseded and kept (Lindenberg, *The Change of Mind Is Information*, LinkedIn, 2026-09-05; `linkedin.com/pulse/change-mind-information-andré-lindenberg-uvcue`). That reframes **Versionable**/**Traceable** as properties a bottom-up ontology earns through its correction history, not just its schema.

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| partial [README][utopia] (an MCP server "for every knowledge base" lets multiple agent clients — Claude Desktop, Cursor, Workbuddy — connect with fine-grained permissions, but writes funnel through one human review queue; no multi-writer concurrency documented) | no [README][utopia] ("One Rust binary and one Postgres... nothing else to run" — single-node deployment, no cluster/replica documented) | partial [README][utopia] · [decisions/README.md][utopia-decisions] (a term must recur in ≥2 documents before promotion to a relation — a deterministic gate — but the underlying LLM extraction itself is not pinned/seeded) | yes [README][utopia] (five swappable vocabulary packs at knowledge-base creation; ontology axioms are user-editable) | yes [decisions/README.md][utopia-decisions] ("a correction inserts a new row that supersedes the old one, because the change of mind is information"; every fact carries `valid_from`/`valid_to` + `recorded_at`/`invalidated_at`) | yes [README][utopia] · [decision 0012][utopia-0012] (Turtle/JSON-LD export with intervals; `docs/decisions/` records real extraction failures with verdicts, e.g. "102 of 130 checkable facts were written backwards") |

`scored 2026-09-30`

These five give the [agent substrate rubric][rubric] its first ontology-doc evidence for **Shared** and **Distributed**, both previously unscored here: `open-ontologies` and `Ontology Atlas` are `partial` on both, `AWS context-ontology-accelerator` is `yes` on both, `EvoOntology` stays `no data`/`no` — a single-session plugin with no shared-store or multi-machine claim — and `Utopia` is `partial`/`no` (one shared knowledge base behind an MCP server, gated through a single human review queue; single-binary deployment, no cluster documented).

**Semantica's decision-graph audit trail** is a candidate for this same "ontology as MCP surface" pattern; its full profile (decision-as-graph-node, PROV-O lineage, bi-temporal facts, point-in-time snapshots) lives elsewhere in this corpus and is not restated here: [agent-frameworks-infrastructure-landscape.md § Agent-native graph & hybrid RAG platforms][semantica-frameworks]. Two facts add to that profile. Timing matters here: [EU AI Act Article 12][ai-act-12] requires high-risk systems to "technically allow for the automatic recording of events... over their lifetime," and the currently amended Act sets that deadline at 2027-12-02 for Annex III systems (2028-08-02 for Annex I) — later than the original date Lindenberg's issue cites, which this entry could not independently re-verify against a primary pre-amendment source. Semantica's own [CHANGELOG][semantica-changelog] is harder evidence than the audit-trail pitch itself: v0.6.7 (2026-08-28) fixed `get_causal_chain()` silently returning an empty chain whenever a causal edge used the analyzer's present-tense vocabulary (`causes`/`influences`/`precedes`) rather than the canonical uppercase form — "silent, and in the dangerous direction for a compliance trace," in the project's own words — fixed a `SHACLGenerator` that produced shapes matching no data so `pySHACL` reported `conforms: True` on plainly violating input, and fixed every RDF export path except JSON-LD silently dropping an entity's source document, page, extractor and reviewer.

Design lens — Lindenberg's *Audit the Auditor* treats a CHANGELOG, not a README pitch, as the real evidence a decision-audit-trail tool is used in earnest: "an audit trail does not fail by crashing; it fails by giving a reassuring answer" (Lindenberg, *Audit the Auditor*, LinkedIn, 2026-08-29; `linkedin.com/pulse/audit-auditor-andré-lindenberg-odvfe`).

## The Agent-Native Layer

The generic layers above solve the *plumbing* — governed APIs an agent can query. But an agent hitting a raw semantic API still re-derives business meaning on every call (and can still get it wrong). Two efforts go further, and are analyzed in depth elsewhere in this repo:

- **[Databricks Genie Ontology](../agents/databricks-genie-analysis.md#genie-ontology)** — a persistent, authority-ranked context graph (metric definitions, joins, synonyms, business logic) built from query history + workplace apps, **MCP-exposed** so external agents consume the same verified context instead of re-deriving it per query.
- **[Open Knowledge Format](../knowledge-management/open-knowledge-format-analysis.md)** — a vendor-neutral, Apache-2.0 spec (Google Cloud, v0.1) for portable "knowledge bundles" (markdown + YAML) with AI agents as first-class consumers — the platform-independent interchange format for that curated context.

Together they mark the shift from "query the catalog at runtime" to "pre-loaded, verified business context the agent can trust."

A complementary research direction formalizes *why* this grounding improves reliability: **[Symbolic Separation][symbolic-separation]** (Davletiyarov, Khan & Bartolini, arXiv:2609.17107, submitted 2026-09-15) lets a deep agent reason freely in natural language but restricts it to *act* on data only through an ontology-constrained Virtual Knowledge Graph with deterministic pre-execution validation — turning a multi-step question into one validated graph traversal instead of LLM-inferred joins. Instantiated as the "Neurosymbolic Deep Analyst" and evaluated on 49.9 TB of supercomputer telemetry against a rigid workflow and a non-symbolic ablation, it raised end-to-end task success from 43% to 86%, eliminated silent data-integrity errors no syntactic check catches, and cut token cost 2.4x — evidence for the agent-native layer's premise from the opposite direction: an *unconstrained* agent over raw telemetry fails multi-step composition, a *symbolically separated* one succeeds.

## Cross-References

- [databricks-genie-analysis.md](../agents/databricks-genie-analysis.md) — Genie One agentic data coworker + Genie Ontology (the agent-native semantic graph)
- [open-knowledge-format-analysis.md](../knowledge-management/open-knowledge-format-analysis.md) — OKF portable knowledge-bundle spec
- [agent-frameworks-infrastructure-landscape.md](../frameworks/agent-frameworks-infrastructure-landscape.md) — §7 RAG & retrieval infrastructure agents call as tools

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
| [Vault-LD][vault-ld] | Markdown-vault-as-linked-data spec; YAML-LD frontmatter + shared `@context`, roundtrip RDF converters |
| [Symbolic Separation (arXiv:2609.17107)][symbolic-separation] | Ontology-constrained Virtual Knowledge Graph + deterministic pre-execution validation for deep agents over operational telemetry |
| [Ontology Atlas README][ontology-atlas] | MCP-native, git-versioned Markdown ontology; MIT license and star count verified 2026-09-30 |
| [open-ontologies README][open-ontologies] | Rust MCP server, Lean-4-certified ontology plan/apply/rollback; MIT license and star count verified 2026-09-30 |
| [EvoOntology README][evoontology] · [arXiv:2609.15779][evoontology-paper] | Self-evolving ontology layer for data agents; MIT license and star count verified 2026-09-30 |
| [AWS context-ontology-accelerator README][coa] · [ontology-engine README][coa-engine] | Namespace-RBAC, AWS CDK-deployed semantic context platform; Apache-2.0 license and star count verified 2026-09-30 |
| [Utopia README][utopia] · [decisions/README.md][utopia-decisions] · [decision 0012][utopia-0012] | Bottom-up bitemporal ontology platform; Apache-2.0 license and star count verified 2026-09-30 (`gh api`) |
| [Semantica CHANGELOG][semantica-changelog] | v0.6.7 (2026-08-28) fixes verified against the changelog text: empty causal chain, SHACL false-conforms, dropped RDF provenance metadata |
| [EU AI Act Article 12 explainer][ai-act-12] | Record-keeping requirement text and the amended Annex III deadline (2027-12-02) |
| André Lindenberg — *The Change of Mind Is Information* (LinkedIn, 2026-09-05; `linkedin.com/pulse/change-mind-information-andré-lindenberg-uvcue`) | Design lens: bitemporal correction as the cheap starting point for an agent-facing ontology (LinkedIn — not link-checked) |
| André Lindenberg — *Audit the Auditor* (LinkedIn, 2026-08-29; `linkedin.com/pulse/audit-auditor-andré-lindenberg-odvfe`) | Design lens: a tool's CHANGELOG, not its pitch, is the real evidence for an audit-trail claim (LinkedIn — not link-checked) |
| [Agent substrate rubric][rubric] | Six-property scoring rubric applied to the five ontology tools above |

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
[vault-ld]: https://github.com/The-Knowledge-Graph-Guys/vault-ld
[symbolic-separation]: https://arxiv.org/abs/2609.17107
[ontology-atlas]: https://github.com/wlsdks/ontology-atlas
[open-ontologies]: https://github.com/fabio-rovai/open-ontologies
[evoontology]: https://github.com/ruc-datalab/EvoOntology
[evoontology-paper]: https://arxiv.org/abs/2609.15779
[coa]: https://github.com/aws/context-ontology-accelerator
[coa-engine]: https://github.com/aws/context-ontology-accelerator/tree/main/packages/ontology-engine
[utopia]: https://github.com/deeplethe/utopia
[utopia-decisions]: https://github.com/deeplethe/utopia/blob/dev/docs/decisions/README.md
[utopia-0012]: https://github.com/deeplethe/utopia/blob/dev/docs/decisions/0012-the-ontology-is-a-contract-not-a-suggestion.md
[semantica-frameworks]: ../frameworks/agent-frameworks-infrastructure-landscape.md#agent-native-graph--hybrid-rag-platforms
[semantica-changelog]: https://github.com/semantica-agi/semantica/blob/main/CHANGELOG.md
[ai-act-12]: https://artificialintelligenceact.eu/article/12/
[rubric]: ../../sdlc-lcm/agent-substrate-rubric.md
