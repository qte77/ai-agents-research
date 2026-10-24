---
title: Onyx Analysis
purpose: Analysis of Onyx (onyx-dot-app), an open-core, self-hostable knowledge/context layer that indexes company apps for chat, agents and MCP clients — and its claim to beat agent-side MCP search on cost and latency.
created: 2026-10-22
updated: 2026-10-22
validated_links: 2026-10-22
status: assess
---

**Details:** **Repo**: [onyx-dot-app/onyx][onyx-repo] | **License**: MIT ("MIT Expat") except
everything under `ee` directories, which is under the Onyx Enterprise License ([LICENSE][onyx-license];
GitHub's detector reports `NOASSERTION` because of the split) | **Stars**: 32,842, created 2023-04-27 |
**Latest release**: `v4.9.2`, 2026-10-15 (`gh api`, 2026-10-22). The LICENSE copyright line is
"DanswerAI, Inc.", the company behind the earlier Danswer project; the README itself doesn't mention
the old name.

## What It Is

Onyx describes itself as "the knowledge/context layer for your team and AI agents": it "connects to
your application to index and surface knowledge from 50+ applications while protecting your data
sovereignty through flexible self-hosted deployments" ([README][onyx-readme]). It ingests content
together with metadata and permissions, so answers respect who may see what, and serves that index
through several surfaces.

## Features (per the README)

- **Agentic RAG** on a hybrid (vector + keyword) index, **Deep Research** reports, and **Custom
  Agents** with their own knowledge subsets, instructions and actions.
- **Web search** (Serper, Google PSE, Brave, SearXNG and others; its own crawler plus Firecrawl/Exa),
  **External Actions & MCP**, a **Secure Sandbox** for code, **Artifacts** and **Voice Mode**.
- **LLM providers**: "all major LLM providers, both self-hosted (like Ollama, LiteLLM, vLLM, etc.) and
  proprietary (like Anthropic, OpenAI, Gemini, etc.)".
- **Access surfaces**: web and desktop app, Slack and Discord bots, a Chrome extension, an embeddable
  widget, and an **MCP server** — "Point Claude Code, Open Code, Codex, or any MCP client at Onyx. Your
  AI agents get company context with the same access controls as the person running them."
- **Deployment**: Docker, Kubernetes, Helm/Terraform; "air-gappable, self-hosted". Two modes:
  Standard (vector + keyword index, connector workers, model inference servers, Redis, MinIO) and Lite
  ("under 1GB memory", a chat UI that "is not capable of indexing documents"). A hosted Onyx Cloud
  exists as well.
- **Editions**: Community Edition under MIT covers "all of the core features for RAG, AI Chat, Agents,
  and Actions"; Enterprise Edition adds SSO (OIDC/SAML), SCIM, RBAC, analytics, query history, custom
  code hooks and whitelabeling.

## Why it matters for agents

Onyx is a direct answer to a design choice every agent builder faces: let the agent search live
systems through many MCP servers, or give it one pre-built, permission-aware index. Its README argues
for the index — "Instead of an agent coordinating and iteratively searching dozens of MCP and burning
many thousands of tokens, Onyx fetches the context across its internal representation instantly" —
and claims "a more reliable, low latency, and low cost context" than "MCP based searches and
index-free approaches". **No figures back this in the README**; treat it as the vendor's position, not
a measured result. The org also publishes [EnterpriseRAG-Bench][onyx-erb] ("Dataset and benchmark for
RAG on company internal documents"), not reviewed here.

Because Onyx is both an MCP *server* (feeding context to Claude Code, Codex and others) and an MCP
*client* (for actions), it can sit underneath a coding agent as its company-knowledge source without
replacing the agent.

## Watch-outs

- **Open core.** Features under `ee/` are not MIT; check which ones a deployment needs before
  treating it as fully open source.
- **Install script.** The README's quick start pipes a remote script into the shell
  (`curl -fsSL https://onyx.app/install_onyx.sh | bash`); read it before running it.
- **Cost/latency claim unverified.** See above.

## Cross-References

- [agentic-enterprise-os-landscape.md](../frameworks/agentic-enterprise-os-landscape.md) — Glean and
  other enterprise "company brain" platforms; Onyx is the self-hostable, open-core alternative.
- [rag topic hub](../../_topics/rag.md) — other retrieval and indexing work in the corpus.

## Sources

| Source | Content |
|---|---|
| [onyx-dot-app/onyx README][onyx-readme] | Positioning, features, access surfaces, deployment modes, editions, MCP claim |
| [Onyx LICENSE][onyx-license] | MIT outside `ee/`, Onyx Enterprise License inside; DanswerAI, Inc. copyright |
| [Onyx releases][onyx-releases] | `v4.9.2`, 2026-10-15 |
| [EnterpriseRAG-Bench][onyx-erb] | The org's RAG benchmark repo (description only) |
| `gh api repos/onyx-dot-app/onyx`, 2026-10-22 | Stars, creation date, license detection |

[onyx-repo]: https://github.com/onyx-dot-app/onyx
[onyx-readme]: https://github.com/onyx-dot-app/onyx#readme
[onyx-license]: https://github.com/onyx-dot-app/onyx/blob/main/LICENSE
[onyx-releases]: https://github.com/onyx-dot-app/onyx/releases
[onyx-erb]: https://github.com/onyx-dot-app/EnterpriseRAG-Bench
