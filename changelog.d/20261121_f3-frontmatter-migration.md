### Changed

- Content-doc frontmatter migrated to the CONTRIBUTING §1–§2 schema: release and licence words moved out of `status:` to the `**Details:**` line, `category`/`description`/`sources`/`version`/`authority` removed from frontmatter (sources moved into each doc's Sources section), missing dates and `validated_links` filled; `status:` accepts lifecycle and plan tokens only, and `make check_frontmatter` is now strict; `learnings-aggregator.py` writes the same schema (plan 0015 F3)
