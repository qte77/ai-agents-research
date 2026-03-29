---
paths:
  - "docs/**/*.md"
---

# Frontmatter Convention for docs/

Every markdown file in `docs/` MUST have YAML frontmatter. Exception: `README.md` files are exempt (they serve as directory indexes, not analysis docs).

## Required Fields

```yaml
---
title: Descriptive Title
purpose: One-line purpose statement
created: YYYY-MM-DD
updated: YYYY-MM-DD
validated_links: YYYY-MM-DD
---
```

- `title` — descriptive, matches the `# H1` heading
- `purpose` — one line, used for relevance matching
- `created` — date of first commit
- `updated` — date of last content edit (bump on every edit)
- `validated_links` — date when URLs were last verified working

## Optional Fields

- `source` — primary URL the doc is based on
- `category` — `technical`, `requirements`, `implementation`, `landscape`
- `status` — only if not using the inline Status badge

## Rules

- No `sources:` key in frontmatter — sources go in the Sources section at end of file
- Status badge goes immediately after frontmatter: `**Status**: Adopt|Trial|Assess|Hold`
- Use `<!-- markdownlint-disable MD013 -->` at file top only (not inline around tables)
- Sources section uses reference-style links (`[key]: url` at bottom)

See `CONTRIBUTING.md` for full conventions.
