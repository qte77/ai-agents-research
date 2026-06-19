---
title: "Open Knowledge Format (OKF): Agent-Readable Data-Catalog Standard"
source: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
purpose: Assess OKF as an interchange format for agent knowledge bundles in the ai-agents-research context
created: 2026-06-16
updated: 2026-06-16
validated_links: 2026-06-16
---

**Status**: Assess

## What It Is

Open Knowledge Format (OKF) is a vendor-neutral, open specification for
representing metadata, context, and curated knowledge as a directory of
markdown files with YAML frontmatter. It was published at v0.1 on
2026-06-12 by the Google Cloud team via [the knowledge-catalog
repository][repo] (Apache 2.0, 2.2 k stars as of 2026-06-16) and
introduced in [a Google Cloud blog post][blog].

OKF is a **format, not a platform** — it requires no central schema
registry, no proprietary SDK, and no cloud account. Bundles ship as git
repositories, tarballs, or subdirectories.

It formalises the LLM-wiki/markdown-first knowledge pattern (compare
[Karpathy's LLM-wiki approach][karpathy] and the [OpenViking knowledge
store][openviking]) into a portable, interoperable standard that AI agents
and humans can read with the same tooling.

## Parent Repository: Knowledge Catalog Platform

OKF lives in the `okf/` subdirectory of the broader
[GoogleCloudPlatform/knowledge-catalog][repo] repository (Apache 2.0, ~2.3 k
stars). The platform is described as an AI-powered data catalog and metadata
management system whose goal is to provide "semantics and business context to
AI agents" via a dynamic knowledge graph over structured and unstructured data.

The repo is organised into four top-level components:

| Directory | Role |
|---|---|
| `agents/` | AI agent implementations for enrichment and retrieval |
| `okf/` | The OKF interchange-format specification (this doc's subject) |
| `samples/` | Reference knowledge bundles (GA4, Stack Overflow, Bitcoin) |
| `toolbox/` | Supporting utilities and the static HTML graph visualiser |

OKF is therefore the wire format that the platform's agents produce and
consume; the other components provide the runtime, tooling, and examples that
demonstrate it end-to-end.

## How It Works

An OKF **bundle** is a directory tree of `.md` files where **file path =
concept identity**. Each file carries YAML frontmatter:

| Field | Required? | Purpose |
|---|---|---|
| `type` | **Mandatory** | Producer-defined concept kind (e.g. "BigQuery Table", "Playbook") |
| `title` | Recommended | Display name |
| `description` | Recommended | Single-sentence summary |
| `resource` | Recommended | URI of the underlying asset |
| `tags` | Recommended | Cross-cutting categorisation list |
| `timestamp` | Recommended | ISO 8601 last-modified datetime |

Producers may add arbitrary extra fields; consumers must preserve unknown
fields. Two reserved filenames exist: `index.md` (directory listing) and
`log.md` (update history).

**Relationships** are expressed as standard markdown links — bundle-relative
links (starting with `/`) are recommended for stability. Consumers must
handle broken links and missing fields gracefully.

The [knowledge-catalog repo][repo] ships three reference implementations
alongside the spec:

- **Enrichment agent** — walks BigQuery datasets, drafts OKF documents, and
  enriches them with schema citations (Python, 50 % of the repo by language).
- **Static HTML visualiser** — renders an OKF bundle as an interactive graph
  view with no backend required (TypeScript/HTML, ~49 %).
- **Three sample bundles** — GA4 e-commerce, Stack Overflow, and Bitcoin
  datasets.

Design principles (from the spec, accessed 2026-06-16):

1. Minimally opinionated — only `type` is mandatory.
2. Producer/consumer independence — writers and readers are fully decoupled.
3. Just markdown, just files, just YAML — no proprietary tooling needed.

## Adoption Decision

**Assess** — OKF is highly relevant to the agent-knowledge-interchange
problem this repo studies, but it is a v0.1 draft published only days before
this analysis (2026-06-12). Key trade-offs:

### Strengths for agent-research context

- Directly addresses the knowledge-sharing gap between data producers and AI
  agents; the spec explicitly frames agents as first-class consumers.
- Format aligns with the markdown-first / LLM-wiki pattern already tracked
  in [karpathy-llm-kb-analysis.md][karpathy].
- Apache 2.0 license, no vendor lock-in; bundles are git-native and
  filesystem-portable.
- Reference enrichment agent (BigQuery-focused) demonstrates the
  auto-generation workflow that agent pipelines need.

### Limitations / unknowns

- v0.1 Draft — the spec is explicitly a draft; breaking changes are possible
  before a stable release.
- Google Cloud / BigQuery origin — reference implementations are BigQuery-
  centric; generic adoption requires adapting the enrichment agent to other
  data sources.
- Not an agent framework — OKF is a data-sharing format. It does not
  prescribe how agents plan, act, or coordinate; it only specifies the
  knowledge bundle they consume or produce.
- Star count (2.2 k) and commit count (28) suggest early community traction
  but not yet broad ecosystem adoption as of 2026-06-16.

**Recommended next step**: trial OKF as the knowledge-bundle wire format in
an internal agent experiment before committing to it as a standard.

## Action Items

- Watch the [knowledge-catalog repo][repo] for v0.2 / stable release and
  any breaking spec changes.
- Prototype an OKF bundle from a small internal dataset using the reference
  enrichment agent; evaluate whether the format maps cleanly to non-BigQuery
  sources.
- Compare OKF frontmatter schema against existing internal metadata standards
  to assess migration cost.
- Track whether other LLM/agent frameworks (LangChain, LlamaIndex, etc.)
  adopt OKF as an ingestion format — ecosystem convergence is the main
  adoption signal to watch.

## Sources

| Source | Content |
|---|---|
| [Google Cloud Blog — OKF introduction][blog] | OKF purpose, design principles, v0.1 release date (2026-06-12), structure examples, reference implementations |
| [OKF SPEC.md v0.1][spec] | Mandatory/recommended fields, bundle organisation, link conventions, consumer tolerance rules |
| [GoogleCloudPlatform/knowledge-catalog (GitHub)][repo] | Apache 2.0 license, 2.2 k stars, language breakdown, repo description |
| [knowledge-catalog platform][repo] | Parent platform repo — directory structure (`agents/`, `okf/`, `samples/`, `toolbox/`), ~2.3 k stars, platform description verified 2026-06-16 |

[blog]: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/
[spec]: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
[repo]: https://github.com/GoogleCloudPlatform/knowledge-catalog
[karpathy]: karpathy-llm-kb-analysis.md
[openviking]: openviking-analysis.md
