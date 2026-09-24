---
title: Agent Plugins — Cross-Vendor Portable Plugin Standard
purpose: Assess the Agent Plugins open standard for packaging Agent Skills and MCP servers across AI agent clients
source: https://agent-plugins.org
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

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

## Unverifiable / Hedged

- No confirmed client implementations (Claude Code or otherwise) were found
  on the site; TSC membership is not evidence of a shipped integration.
- Adoption, download, or real-world usage figures are not published anywhere
  on the site or in the spec repo.

## Sources

| Source | Content |
|---|---|
| [agent-plugins.org][site] | Standard description, problem statement, governance (first-party) |
| [agent-plugins-spec repo][repo] | Spec source, README |
| [LICENSE.md][license] | Dual CC BY 4.0 / Apache-2.0 licensing statement |
| GitHub API repo metadata, 2026-09-24 | Stars(1,325)/forks(74)/issues(18), dates, license detection |

[site]: https://agent-plugins.org
[repo]: https://github.com/agentplugins/agent-plugins-spec
[license]: https://github.com/agentplugins/agent-plugins-spec/blob/main/LICENSE.md
