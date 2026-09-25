<!--
A new scriv changelog fragment.

Uncomment the section that is right (remove the HTML comment wrapper)
and fill in the content. Comment out (or remove) any remaining
"Uncomment ..." sections.
-->

<!--
### Removed

- A bullet item for the Removed category.

-->
### Changed

- `scripts/restructure_links.py`, `docs/non-cc/.restructure-map.tsv`, `docs/non-cc/orchestrators/`: #309 Phase 1, step 1 of the `docs/non-cc/` faithful-9 subdir restructure. Added a stdlib-only, typed move-and-rewrite tool that repoints every relative markdown link repo-wide when docs move (inline links, reference-style definitions, anchors kept, fenced code blocks left alone), backed by a generated filename-to-subdir mapping file for all 93 `docs/non-cc/` docs. Used it to move the smallest section, Orchestrators (6 docs: `air-`, `deerflow-`, `devteam-`, `omnigent-`, `qm-`, `raven-analysis.md`), into `docs/non-cc/orchestrators/`, updating `docs/non-cc/README.md`'s index and every inbound cross-reference. The remaining 8 sections (Agents, Coding Agents & IDEs, Knowledge Management, Reference & Background, Context & Memory Infrastructure, Infrastructure, Frameworks, Protocols & Interfaces) move in follow-up PRs using the same tool.

<!--
### Deprecated

- A bullet item for the Deprecated category.

-->
<!--
### Added

- A bullet item for the Added category.

-->
<!--
### Fixed

- A bullet item for the Fixed category.

-->
<!--
### Security

- A bullet item for the Security category.

-->
