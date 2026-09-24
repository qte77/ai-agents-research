---
title: "book-to-skill: Books and Documents as Agent Skills"
source: https://github.com/virgiliojr94/book-to-skill
purpose: Analysis of book-to-skill — converts technical books and documents into on-demand Claude Code (and other-harness) Skills, avoiding both PDF search and full-context dumping.
category: analysis
platform_scope: [claude-code, github-copilot-cli]
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Trial

## What It Is

[book-to-skill][repo] converts a technical book, document folder, or collection of sources — PDF,
EPUB, DOCX, HTML, RTF, MOBI, Markdown, reStructuredText, AsciiDoc — into a structured skill the
agent loads on demand, rather than a static summary or a document dump into context. Framing:
*"You buy a great technical book. You read it once. Three months later you can't remember chapter
7 existed."* PDF search returns pages, not answers; asking the agent about the book either
hallucinates or gets a "no content" refusal; hand-written notes go unread. book-to-skill's answer
is a skill the agent consults selectively, chapter by chapter, across Claude Code, GitHub Copilot
CLI, Amp, Hermes Agent, and OpenClaw.

Basics (first-party, 2026-09-24): [virgiliojr94/book-to-skill][repo]; MIT; 32,193 stars, 3,349
forks; Python; repo created 2026-05-01, last push 2026-09-22 (active).

## How It Works

Two-stage pipeline:

1. **Extraction** — a modular Python extractor converts the source document to clean text plus
   metadata. Format-specific parsers: `pdftotext` (poppler, instant, prose-oriented) or `docling`
   (technical mode, ~1.5s/page, preserves tables and code as markdown) for PDFs; `ebooklib` for
   EPUB; `python-docx` for DOCX; stdlib fallbacks where possible. A `--check` flag diagnoses which
   optional extractors are installed.
2. **Generation** — produces a skill billed by the project as following an "Agent Skills" open
   standard: a core `SKILL.md` (frameworks, chapter index), per-chapter files loaded only when
   queried, plus a glossary, patterns, and a cheatsheet.

Install: `npx skills add virgiliojr94/book-to-skill`, or a manual clone into `~/.claude/skills/`,
`~/.copilot/skills/`, or the host's skills directory — one installation registers across every
supported agent.

### Measured Token Cost (first-party, `docs/performance.md`)

The repo's own benchmark methodology (`tiktoken` cl100k_base token counts, reproducible via
`tools/discovery_tax.py`) reports **24×–51× fewer tokens than dumping the full book into context**
to answer one targeted question:

| Book (chapter size) | Context-dump tokens | book-to-skill tokens | Reduction |
|---|---:|---:|:---:|
| Think Python 2 (small) | 119,264 | ~5,000 | 24× |
| Working Backwards (medium) | 175,253 | ~5,000 | 35× |
| AI Engineering (large) | 256,287 | ~5,000 | 51× |

The doc itself frames this as a self-measured, reproducible number, not an independently verified
one — the 24–51× context-dump comparison is "the strongest claim: that cost recurs on every
conversation turn," versus a smaller 2.4×–15.6× advantage over a manual discovery-loop
(search, open, re-search) baseline.

## Adoption Considerations

**Strengths**: rapid adoption (32.2K stars from a 2026-05-01 repo creation date) with active
maintenance (pushed 2026-09-22); a reproducible, first-party benchmark methodology rather than a
bare marketing number; cross-platform skill discovery (one install registers on multiple
harnesses); MIT-licensed (`LICENSE.md`), though the README itself notes this covers the tool, not
the books you feed it — "follow the license or terms of the source document."

**Risks**: extraction quality depends on which optional per-format tool is installed (`pdftotext`
vs. `docling` vs. Calibre for MOBI) — the `--check` flag exists precisely because this varies by
machine; chapter auto-detection has documented gaps (e.g. books that head chapters with section
titles rather than "Chapter N" don't auto-segment); the token-reduction numbers are self-measured
on the project's own chosen book set, not an independent benchmark.

Cross-ref: [CC-community-skills-landscape.md](CC-community-skills-landscape.md) — the Agent Skills
ecosystem this tool targets.

## Sources

| Source | Content |
|---|---|
| [virgiliojr94/book-to-skill][repo] | Repository README, license, stars, install (2026-09-24) |
| [book-to-skill performance docs][perf] | First-party token-cost methodology and per-book measurements |

[repo]: https://github.com/virgiliojr94/book-to-skill
[perf]: https://github.com/virgiliojr94/book-to-skill/blob/master/docs/performance.md
