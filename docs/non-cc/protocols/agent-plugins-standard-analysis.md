---
title: Agent Plugins — Cross-Vendor Portable Plugin Standard
purpose: Assess the Agent Plugins open standard for packaging Agent Skills and MCP servers across AI agent clients
source: https://agent-plugins.org
created: 2026-09-24
updated: 2026-09-30
validated_links: 2026-09-30
status: assess
---

## What It Is

[Agent Plugins][site] is an open standard (v1.0.0) for packaging reusable AI
agent components — Agent Skills and MCP servers — into one directory format
that any compatible client can discover and load the same way. A plugin is a
directory containing a `plugin.json` manifest, optional `skills/` and
`mcp.json` files, and extensible client-specific namespaces for anything a
particular client needs beyond the shared shape.

**Problem it targets**: per the site's own framing, "AI agent clients have
developed their own plugin formats, even when plugins contain the same
underlying components," forcing plugin authors to repackage the same skill or
MCP server separately for each client. Agent Plugins standardizes only the
shared component structure; distribution, installation, permissions, UX, and
client-specific capabilities stay under each client's own control.

## Governance

Development happens in the open on [agentplugins/agent-plugins-spec][repo] via
GitHub Discussions and Discord, with a public proposal-and-decision process.
The initial Technical Steering Committee lists Core Maintainers from Amazon,
Cursor, Microsoft, OpenAI, and Vercel — but this is committee membership by
company affiliation, not a claim that any of those companies' own clients
(including Claude Code) have shipped Agent Plugins support. The site does not
publish a separate adopters/implementers list.

## License

Dual-licensed per [`LICENSE.md`][license] (decoded via the GitHub API today,
which GitHub's own detector reports only as `other`/`NOASSERTION`): spec
text, documentation, examples, and diagrams are under CC BY 4.0, while
schemas, source code, and scripts are under Apache License 2.0.

## Repo Stats (2026-09-24)

1,325 stars · 74 forks · 18 open issues · created 2026-04-03 · last push
2026-08-19 · no primary language (specification-only repo).

## Corpus Relevance

No prior coverage — `git grep` across `docs/` for `agent-plugins`,
`agentplugins`, and `agent-plugins.org` returns zero hits before this doc.
This is a structural parallel to the fragmentation problem
[agents-md-cookbook-analysis.md](agents-md-cookbook-analysis.md) documents at
the instructions-file layer (AGENTS.md vs. CLAUDE.md vs. `.cursorrules`):
Agent Plugins targets the same "one vendor, one format" problem one layer
down, at packaged Skills/MCP servers rather than prose config files.

## Concrete implementation: Mitosis Memory (`mitosis-agent-plugin`)

Found 2026-09-30, updating the "no confirmed client implementations" note below. [Mitosis
Labs][mitosis-plugin] (org [`OperatingSystem-1`][mitosis-org], analyzed for its Cortex memory product
in [mitosis-cortex-analysis.md][mitosis-cortex]) ships `mitosis-agent-plugin` (MIT, 0★, pushed
2026-09-20) as a real Agent Plugins 1.0.0 package: "The plugin ships two manifests so the same
directory loads in clients that implement either format" — `plugin.json`/`mcp.json` at the Agent
Plugins 1.0.0 paths (read by VS Code, GitHub Copilot, Kiro, and Cursor) alongside client-specific
namespaces for Cursor, Grok Build, and Claude Code (`.claude-plugin/`). It bundles a remote MCP server
(`https://mitosislabs.ai/api/mcp`, OAuth 2.0 + PKCE, dynamically registered per client — "there is no
API key to paste") with seven skills (`mitosis-memory-skills`, MIT, 1★, pushed 2026-08-17:
`memory-connect`, `memory-manifest`, `memory-ask`, `memory-recall`, `memory-remember`,
`memory-ingest`, `memory-status`) that each "prefer the MCP tool when present and fall back to the
`mi` CLI... when it is not" — the same skill runs whether or not the plugin's MCP server is loaded.
The repo runs a CI check (`node scripts/validate.mjs`) that "validates both manifests against their
published JSON Schemas and parses the YAML frontmatter of every `SKILL.md`" — this is the Agent
Plugins side of the reproducibility question the standard's own repo leaves open (its spec is
versioned; a given implementer's manifest validity is not, absent a check like this one).

This is TSC-adjacent evidence, not a TSC-member client shipping support: none of Amazon, Cursor,
Microsoft, OpenAI, or Vercel is the author here. It's a third-party vendor building a memory plugin
*to* the open standard, across four clients from one source tree — exactly the "one vendor, one
format" problem this standard targets, now with one worked example.

| Shared | Distributed | Reproducible | Adaptable | Versionable | Traceable |
|---|---|---|---|---|---|
| yes [README][mitosis-plugin] (multiple clients — VS Code, Cursor, Grok Build, Claude Code — read the same manifests and the same remote MCP server) | partial [README][mitosis-plugin] (remote MCP server is centrally hosted and reachable from any client; the plugin package itself is copied per-install, not synced) | partial [README][mitosis-plugin] (CI validates manifest schemas and SKILL.md frontmatter on every push — deterministic *packaging* — but the memory content the MCP server serves depends on Mitosis's own ingest pipeline, scored `no` in [mitosis-cortex-analysis.md][mitosis-cortex]) | yes [README][mitosis-plugin] (two manifests cover four client formats from one source tree; skills fall back from MCP tool to CLI transparently) | yes [README][mitosis-plugin] (MIT-licensed source in git; skills also published standalone at [`mitosis-memory-skills`][mitosis-skills]) | partial [README][mitosis-plugin] (`cortex_ask` "returns a cited block," but the plugin/skill layer itself has no install- or invocation-level audit trail) |

`scored 2026-09-30`

## Unverifiable / Hedged

- No confirmed client implementations (Claude Code or otherwise) were found
  on the site; TSC membership is not evidence of a shipped integration.
- Adoption, download, or real-world usage figures are not published anywhere
  on the site or in the spec repo.
- **Update 2026-09-30**: the "no confirmed client implementations" statement
  above is about the *standard's own site*, which still lists no
  adopters/implementers page. A third-party implementation now exists (see
  above) — the standard has real-world usage the site itself doesn't surface.
- **Update 2026-09-30 (OpenAI)**: OpenAI, a TSC member, now documents the
  standard as its packaging format: new ChatGPT/Codex plugins should declare the
  Agent Plugins `$schema` in a root `plugin.json`, with `.codex-plugin/plugin.json` kept
  as a compatibility fallback. That is documented support, not yet observed adoption:
  none of OpenAI's own example plugins declares the schema. See
  [openai-apps-plugins-analysis.md](openai-apps-plugins-analysis.md#manifest).

## Sources

| Source | Content |
|---|---|
| [agent-plugins.org][site] | Standard description, problem statement, governance (first-party) |
| [agent-plugins-spec repo][repo] | Spec source, README |
| [LICENSE.md][license] | Dual CC BY 4.0 / Apache-2.0 licensing statement |
| GitHub API repo metadata, 2026-09-24 | Stars(1,325)/forks(74)/issues(18), dates, license detection |
| [mitosis-agent-plugin README][mitosis-plugin] | Concrete Agent Plugins 1.0.0 implementation, MCP server, skills, CI validation (fetched via GitHub contents API, 2026-09-30) |
| [mitosis-memory-skills README][mitosis-skills] | Standalone skills publication, MIT license (fetched via GitHub contents API, 2026-09-30) |
| [mitosis-cortex-analysis.md][mitosis-cortex] | The memory product this plugin connects to; Reproducible scoring cross-ref |

[site]: https://agent-plugins.org
[repo]: https://github.com/agentplugins/agent-plugins-spec
[license]: https://github.com/agentplugins/agent-plugins-spec/blob/main/LICENSE.md
[mitosis-plugin]: https://github.com/OperatingSystem-1/mitosis-agent-plugin
[mitosis-skills]: https://github.com/OperatingSystem-1/mitosis-memory-skills
[mitosis-org]: https://github.com/OperatingSystem-1
[mitosis-cortex]: ../context-memory/mitosis-cortex-analysis.md
