---
title: "Databricks Genie One: Agentic Data Coworker (Genie Ontology + Genie Agents)"
source: https://www.databricks.com/blog/introducing-genie-one-genie-ontology-and-genie-agents
purpose: Assess Databricks Genie One and its Genie Ontology semantic layer as an enterprise data-agent platform
created: 2026-06-20
updated: 2026-11-19
validated_links: 2026-11-19
status: trial
platform_scope: [databricks, slack, microsoft-teams, ios, android, mcp]
---

## What It Is

Genie One is Databricks' agentic data "coworker," announced at the Data + AI
Summit on 2026-06-16. It extends the earlier Genie conversational-analytics
product from "ask a question, get a chart" into an agent that can schedule and
monitor reports, draft documents, run custom skills, and take MCP-based actions
across structured and unstructured data — pitched at business teams (marketing,
finance, sales, operations) rather than data engineers. It answers through
native Slack, Microsoft Teams, iOS, and Android surfaces and enforces Unity
Catalog access controls on every response. See the [introduction blog][genie-blog]
and the [launch press release][genie-press].

Genie One ships as **three layers**: the **Genie One** coworker, the **Genie
Ontology** semantic-context graph that grounds it, and **Genie Agents** —
reusable, shareable autonomous workflows. The suite is a **proprietary, managed
Databricks platform feature**; only the lakehouse foundations it sits on (Apache
Spark, Delta Lake, Apache Iceberg) are open source, and MCP is an open-protocol
integration point rather than an open-source release.

Disambiguation: the community project `databrickslabs/ontobricks` (an
R2RML/GraphQL knowledge-graph layer over Databricks tables) is unrelated to
Genie Ontology.

## Genie Ontology

Genie Ontology is a self-improving enterprise context graph that grounds the
coworker. Per the [blog][genie-blog], it automatically extracts and ranks
business knowledge — metric definitions, business terms, JOIN relationships, SQL
business logic, and synonyms — from Databricks-native assets plus connected
workplace applications via Lakeflow Connect. Distinguishing properties:

- **Authority scoring** — a PageRank-like model weights definitions by author
  authority, usage frequency, certification status, and freshness; Unity Catalog
  Semantics definitions carry the highest weight.
- **Persistent, not per-query** — it maintains a cumulative, authority-ranked
  knowledge store, replacing the per-query RAG re-derivation that ad-hoc
  text-to-SQL agents repeat on every request.
- **MCP-exposed** — the governed context is served as an MCP server, so external
  agents (Claude, Copilot, custom agents) can consume the same enterprise context.

### Status and changes since launch (checked 2026-11-19)

Per the first-party [Genie Ontology docs page][genie-ont-docs] (shows "Last updated on Nov 16, 2026" under its title) and the
[AI/BI release notes][genie-rn] (documented):

- **Rollout** (one sequence) — 2026-06-04: first release-notes entry,
  "Genie Ontology (Public Preview)", describing an automatically built map of
  the business. 2026-06-15/16: launch announcement (press release; blog dated
  2026-06-16). 2026-07-02: "ontology snippets" entry, Public Preview, sign-up
  via the account team. 2026-08-06: ontology "enabled by default" (Public
  Preview). 2026-08-13: snippets available to all customers without requesting
  access. 2026-10-22: snippets also extracted from queries that external tools
  such as dbt run on Databricks. The docs page carries no GA announcement as of
  this date.
- **Two knowledge classes** — *modeled knowledge* (metric views, domains,
  Pages, certification, curated Genie Agents) takes precedence over *learned
  knowledge* (snippets Genie extracts from dashboards, SQL queries, metric views
  and Genie Agents). Learned snippets cannot be edited directly: to change what
  Genie learns, change the source asset or model the concept.
- **Provenance of machine-written context** — a snippet shows its description,
  source asset, author, domains and lineage, and responses carry citations
  (documented). Snippets inherit Unity Catalog permissions, except snippets
  from external knowledge sources (Beta, e.g. Power BI definitions), which "are
  available to all users in your account". The page lists one limitation: no
  customer-managed keys. Whether a reviewable change history of newly learned
  snippets exists is not stated on the page (unverified).
- **Pricing** — the docs state that "customers do not incur costs for curating
  ontology snippets" "at this time" and that Databricks may change this. The
  [launch blog][genie-blog] says there is no seat-based pricing and "up to $10"
  of free usage per user per month; the release notes extend free Genie One and
  Genie Agents usage through 2027-01-31 (previously 2026-07-31). This replaces
  the earlier community-sourced pricing figures.

Benchmark, restated with its setting: Databricks' internal test used **28**
enterprise data-analysis questions; Genie got 84.5% right on the first attempt
vs 52.4% for the strongest and 25% for the weakest general-purpose coding agent
tested, about 2x faster than the strongest, with competing agents anonymized
([blog][genie-blog], vendor claim, methodology unpublished). 84.5% and 52.4% of
28 are not whole numbers of questions, so the figures are probably averaged
over repeated runs (inference; the blog does not say). If so, one question is
about 3.6 points per run; treat the gap as indicative only.

Unverified: a third-party write-up reports "50+ connected sources" and "up to
200 knowledge snippets per Genie Space" ([talentbricks][talentbricks]); neither
appears in the first-party docs page or blog read on 2026-11-19.

## Genie Agents

Genie Agents are reusable, shareable autonomous workflows assembled from saved
Genie conversations. A user can spin one up from a single prompt; the agent
inherits the conversation's memory (sources, instructions, behavior) and can be
shared with teammates to execute multi-step tasks. They evolved from Genie
Spaces. Per the [press release][genie-press], Genie One and Genie Agents reached
GA on 2026-06-16, while Genie Ontology entered Public Preview (2026-06-15);
Genie App Builder and Genie ZeroOps were announced in Private Preview.

## Adoption Decision

**Trial.** Genie One and Genie Agents are GA with a consumption-based free
allowance, and Genie Ontology is the technically novel layer worth validating
for enterprise data-agent grounding. Trade-offs:

- **Strengths** — persistent, authority-ranked semantic layer over governed
  lakehouse data; Unity Catalog ACL enforcement on answers; MCP exposure means
  the context is reusable by non-Databricks agents.
- **Limits** — proprietary and Databricks/Unity-Catalog-native (no portability
  off the platform); headline accuracy/speed numbers are unaudited internal
  benchmarks; Genie Ontology is still Public Preview (2026-11-19) and its
  curation is free only "at this time". Pricing is usage-based, not per seat;
  see the status section above.

Cross-ref: [omnigent-analysis.md](../orchestrators/omnigent-analysis.md) (Databricks/Neon
meta-harness), [open-knowledge-format-analysis.md](../knowledge-management/open-knowledge-format-analysis.md)
(OKF vs Genie Ontology — open portable format vs proprietary managed graph for
the same data-agent-grounding problem), and [rowboat-analysis.md](rowboat-analysis.md)
(comparable AI-coworker / knowledge-graph pattern).

## Sources

| Source | Content |
|---|---|
| [Genie One introduction blog][genie-blog] | Genie One / Genie Ontology / Genie Agents capabilities, authority-scoring model, internal benchmarks, 2026-06-16 announcement |
| [Genie One launch press release][genie-press] | GA status, preview tiers, availability surfaces (Slack/Teams/iOS/Android) |
| [Genie Ontology docs][genie-ont-docs] | Modeled vs learned knowledge, snippet provenance fields, pricing note, limitations (page dated 2026-11-16, read 2026-11-19) |
| [AI/BI release notes 2026][genie-rn] | Dated ontology rollout entries (07-02, 08-06, 08-13, 10-22), free-usage extension |
| [talentbricks — Genie Ontology][talentbricks] | Third-party — "50+ sources", "200 snippets/Space" (unconfirmed against first-party) |

[genie-blog]: https://www.databricks.com/blog/introducing-genie-one-genie-ontology-and-genie-agents
[genie-press]: https://www.databricks.com/company/newsroom/press-releases/databricks-launches-genie-one-all-new-agentic-coworker-every-team
[talentbricks]: https://www.talentbricks.ai/en/blog/2026-06-16-genie-ontology-databricks
[genie-ont-docs]: https://docs.databricks.com/aws/en/genie/genie-ontology
[genie-rn]: https://docs.databricks.com/aws/en/ai-bi/release-notes/2026
