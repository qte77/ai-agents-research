---
title: Knowledge Organisation Methods for a Markdown KB
purpose: Short survey of widely used methods for organising a plain-markdown knowledge base (hub pages, backlinks, Zettelkasten, PARA, Diátaxis, llms.txt) and what each means for humans and agents.
status: research
created: 2026-11-21
updated: 2026-11-21
validated_links: 2026-11-21
---

Scope: well-known methods only, each read at its originator's own site on 2026-11-21 (documented).
"Implication" lines are our reading, not the source's claim. The source gist for the LLM-wiki pattern is
analysed in [karpathy-llm-kb-analysis.md](karpathy-llm-kb-analysis.md).

## Methods at a glance

| Method | What it is (per its source) | Implication for an agent-maintained plain-markdown KB |
|---|---|---|
| **Maps of content / hub pages** | A Map of Content (MOC) is a hub note that maps other notes in context and, unlike a folder, is an overlay that does not restrict or move the base notes (paraphrase of the [LYT MOC overview][moc]; page is JS-only, read via WebFetch only, browser-tier re-read failed 2026-11-21, wording unverified verbatim) | Cheapest navigation layer: one hub file per topic lists its docs. Agents can regenerate and lint hubs; stale hub rows are the failure mode |
| **Folders vs tags** | Obsidian's default `tags` property is a list on each note ([properties][ob-prop]); the folder-versus-tag trade-off itself is common practice, unsourced | Keep folders few and stable (moves break inbound links); put cross-cutting views in hub pages |
| **Backlinks** | A backlink is "a link from another note to that note"; Obsidian shows linked and unlinked mentions ([Obsidian backlinks][ob-back]) | Plain relative links already give backlinks via grep or tooling; zero-inbound-link files (orphans) are checkable by script |
| **Zettelkasten** | Atomicity: "one knowledge building block per note"; "connecting and not collecting" is the priority; structure notes are "a Zettel about other Zettels" ([zettelkasten.de][zk]) | Favours small single-topic docs with explicit links that say why; the structure note is the same idea as a hub page |
| **PARA** | Projects, Areas, Resources, Archives; "organize by actionability" ([Forte Labs][para]) | Fits personal task-driven notes. A research corpus is organised by topic, not by current project, so only the Archive idea transfers |
| **Diátaxis** | Documentation is split into four forms: tutorials, how-to guides, reference and explanation; the needs they serve (learning, doing, information, understanding) are our paraphrase of the site ([diataxis.fr][dx]) | Useful as a check that a doc has one job. Analysis docs here are mostly explanation plus reference |
| **Obsidian vault** | A folder of markdown files; properties are YAML at the top of the file; default list properties `tags`, `aliases`, `cssclasses`; graph view draws notes as nodes and links as lines ([properties][ob-prop], [graph][ob-graph]) | A vault is just files, so agents and humans can share it. Properties are frontmatter, so no lock-in |
| **Logseq** | Describes itself as an "open-source platform for knowledge management and collaboration" supporting Markdown and Org-mode (AGPL-3.0 per the repo's licence metadata); a database version is in beta, with "data loss is possible" warned ([README][logseq]) | Block-based and moving to a DB graph, so less natural for plain-file agent edits than a vault |
| **llms.txt** | Not repeated; see [CC-llms-txt-analysis.md](../../cc-native/context-memory/CC-llms-txt-analysis.md) | Same file |

## Frontmatter schemas compared

| Schema | Format | Mandatory | Notes |
|---|---|---|---|
| Open Knowledge Format | YAML frontmatter | `type` only | Provenance fields (`sources`, `generated`, `verified`) in v0.2; see [open-knowledge-format-analysis.md](open-knowledge-format-analysis.md) |
| Obsidian properties ([properties][ob-prop]) | YAML | none | Typed per property name vault-wide (text, list, number, checkbox, date, date and time, tags) |
| Jekyll | YAML between `---` lines | none (an empty block still triggers processing) | Predefined `layout`, `permalink`, `published`; custom keys allowed ([Jekyll][jekyll]) |
| Hugo | YAML (`---`), TOML (`+++`) or JSON | none | Common fields `date`, `draft`, `title`, `weight`; custom data under `params` ([Hugo][hugo]) |

The four share one shape: a small YAML header, free extra keys, tolerant readers.

## What this means for a corpus like this one (our synthesis)

- The corpus already is the plain-markdown pattern: folders by section, hub pages under `docs/_topics/`, YAML frontmatter, reference links. No new tooling is needed to adopt these methods.
- Keep one job per doc (Diátaxis check), link with reasons (Zettelkasten), and treat hubs as the MOC layer.
- Cheap agent-side checks beat new platforms. Orphan detection is our suggestion; hub-row coverage and frontmatter key presence are tracked in plan 0015 (X2, F1).
- Obsidian is a viewer over the same files, optional.

## Sources

| Source | Content |
|---|---|
| [LYT MOCs overview][moc] | MOC definition, folder contrast (page names no author) |
| [Obsidian backlinks][ob-back] | Backlink and unlinked-mention definitions |
| [Obsidian properties][ob-prop] | YAML storage, types, default properties |
| [Obsidian graph view][ob-graph] | Nodes, links, filters, groups |
| [zettelkasten.de introduction][zk] | Atomicity, linking, structure notes |
| [Forte Labs PARA][para] | Four categories, actionability |
| [Diátaxis][dx] | Four documentation needs |
| [Jekyll front matter][jekyll] | Format and predefined variables |
| [Hugo front matter][hugo] | Formats and common fields |
| [Logseq README][logseq] | Positioning, formats, DB-version beta warning; AGPL-3.0 via `gh api`, 2026-11-21 |

[moc]: https://notes.linkingyourthinking.com/Cards/MOCs+Overview
[ob-back]: https://obsidian.md/help/plugins/backlinks
[ob-prop]: https://obsidian.md/help/properties
[ob-graph]: https://obsidian.md/help/plugins/graph
[zk]: https://zettelkasten.de/introduction/
[para]: https://fortelabs.com/blog/para/
[dx]: https://diataxis.fr/start-here/
[jekyll]: https://jekyllrb.com/docs/front-matter/
[hugo]: https://gohugo.io/content-management/front-matter/
[logseq]: https://github.com/logseq/logseq#readme
