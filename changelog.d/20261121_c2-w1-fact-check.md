### Fixed

- Abbreviation check: ignores frontmatter, HTML comments, URLs and link targets; counts plurals and hyphen compounds ("MCPs", "MCP-based") as uses; an expansion wrapped across lines counts; only a relative inline or reference-style link to the glossary exempts a doc; fences close only on a matching run, so mixed or nested fences no longer end a block early (plan 0015 C2 fact-check)
- `adding-research-source` skill: `refresh-docs` is named as a workflow, the link-check merge and exclude rules are aligned with CONTRIBUTING, and lanes are told to expand abbreviations (plan 0015 W1 fact-check)
