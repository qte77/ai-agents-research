---
title: Ripwire — Deterministic Repo-Context CLI for Coding Agents
source: https://github.com/redhat-et/ripwire
purpose: Analysis of Ripwire, a Red Hat Emerging Technologies CLI (with optional MCP server) that produces deterministic, disclosed-confidence code-context maps for coding agents.
platform_scope: [claude-code, cursor, windsurf, gemini-cli]
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

Ripwire ([redhat-et/ripwire][repo]) is a zero-dependency C++23 CLI — with an
optional MCP server — described in the repo as "the ripgrep of AI context."
The CLI is the primary interface; MCP is opt-in for agents that prefer a
tool-call surface over shelling out. It targets a specific inefficiency in
agent-based coding: every cold context orientation otherwise means
re-reading repository structure from scratch. Ripwire instead produces
ranked call graphs, blast-radius/impact analysis, and code-quality
assessments up front. It ships from `redhat-et`, Red Hat's emerging
technologies organization.

## Key Features (per README, self-reported)

- **Speed/footprint claims**: repository indexing in milliseconds, warm
  queries in "~197ms," and full runs completing in "0.25–0.45 seconds" using
  "6.6–16.5 MB" of memory. These are the vendor's own numbers; no
  independent benchmark reproduction was found.
- **Signature-only output mode**: the README states this produces "74.7%
  fewer bytes than bodies," aimed at agent context budgets rather than
  human-terminal readability (XML wire format).
- **Code intelligence**: ranked, deterministic call graphs; impact analysis
  disclosing blast radius and affected test suites; six independent
  "quality evidence families" (structural complexity, naming, idioms, git
  churn, colocation, state effects).
- **Language support**: parsing via vendored Tree-sitter grammars, described
  in the README as covering 24+ languages (C++, Rust, Python, Go,
  JavaScript/TypeScript, Java, C#, Swift, Kotlin, Dart, and others) plus
  Markdown/YAML/TOML/JSON.
- **"Honesty contract"**: the README states every truncation is disclosed,
  confidence scores accompany rankings, and ambiguous calls are labelled
  rather than hidden — "every guess labelled, every loss published."

## Core Commands

Representative usage from the README: `--for="task description"` (ranked
symbol map with complexity/churn inline), `--callers=SYMBOL`,
`--impact=SYMBOL` (change amplification and affected code), `--test-gate`
(which tests must run before commit), and `--quality-delta` (what changed in
code quality metrics between two states).

## Architecture

A single self-contained binary with no runtime dependencies: no server, no
daemon, offline-capable. Tree-sitter core and its grammars are vendored so
network-off builds are supported. Build requirements are CMake 3.24+ and a
C++23 compiler (clang 16+, gcc 13+, or MSVC).

## Research Grounding

The repo publishes a lineage document that the README says folds in "49
repositories and 71 papers," spanning McCabe's 1976 cyclomatic-complexity
work through 2026 publications on retrieval for agents — a self-reported
count, not independently verified here.

## License and Maturity

Apache-2.0 (per `gh api repos/redhat-et/ripwire`). Created 2026-07-29 —
roughly two months old at the time of writing — latest release `v0.6.2`
(published 2026-09-21), most recent push 2026-09-24: 2,334 stars, 151 forks,
52 open issues (all via `gh api`, accessed 2026-09-24).

## Corpus Relevance

Ripwire is multi-platform by design (Claude Code, Cursor, Windsurf, Gemini,
and other MCP-capable clients per the README), with Claude Code as one
integration target among several — hence `non-cc/` placement rather than
`cc-community/`. It sits in the same "deterministic repo-context for coding
agents" space as FastContext (see [Cross-References](#cross-references)),
but as a standalone CLI/MCP tool rather than a subagent pattern.

## Cross-References

- [fastcontext-analysis.md][fastcontext] — a dedicated repo-exploration
  subagent aimed at the same token-cost problem (cold-context orientation),
  via a different mechanism (a subagent role vs. a standalone deterministic
  CLI/MCP tool).

## Sources

| Source | Content |
|---|---|
| [redhat-et/ripwire repo][repo] | README — architecture, commands, performance claims, language support, lineage document, license |
| GitHub API `repos/redhat-et/ripwire`, accessed 2026-09-24 | Stars, forks, open issues, license, created/pushed timestamps, latest release tag |

[repo]: https://github.com/redhat-et/ripwire
[fastcontext]: fastcontext-analysis.md
