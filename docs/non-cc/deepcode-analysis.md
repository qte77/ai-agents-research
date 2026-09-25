---
title: DeepCode — Open Agentic Coding Harness (HKUDS)
purpose: Assess DeepCode's multi-agent coding harness, including its Paper2Code origin and current broader "Open Agentic Coding" framing
source: https://github.com/HKUDS/DeepCode
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Trial

## What It Is

[DeepCode][repo] is an open-source coding-agent harness from HKUDS (the Data
Intelligence Lab at the University of Hong Kong). The repo's current
self-description — "Open Agentic Coding (Agent Harness & Loop Engineering &
Multi-Agent Orchestration)" — is broader than the tool's original framing as
a paper-to-code generator. Its Paper2Code workflow remains one entry point:
given a research paper, technical document, URL, or reference repository, a
set of specialized agents (research-intent understanding, documentation
parsing, implementation planning, code-reference discovery) collaborate to
generate and verify executable code. Beyond Paper2Code, DeepCode works
directly inside a repository — editing files, running commands, running
tests — through "Loop Engineering": multi-turn, goal-directed loops with
durable sessions that survive restarts and LLM-provider switches (OpenAI,
Anthropic, DeepSeek, and others). It also supports reusable Skills and
Automations, explicit permission controls and sandboxing, MCP server
integration, and CLI, Desktop, Web, and TUI clients sharing one local
service.

The repo's homepage field cites arXiv:2512.07921 (Li et al.) as the
associated paper; that paper itself was not independently fetched for this
entry and is cited here only as the citation the repo names.

## Repo Stats (2026-09-24)

16,632 stars · 2,163 forks · MIT license · Python 3.12+ (with Rust
components for Desktop) · created 2025-05-14 · 16 tagged releases, latest
**v2.2.0** (published 2026-09-06) · last push 2026-09-22.

## Corpus Relevance

Same HKUDS lab as three other tools already tracked in this corpus:
[autoagent-analysis.md](frameworks/autoagent-analysis.md) (AutoAgent),
[openharness-analysis.md](frameworks/openharness-analysis.md) (OpenHarness), and
`docs/cc-native/agents-skills/CC-cli-anything-analysis.md` (CLI-Anything).
`autoagent-analysis.md`'s own "Monitor HKUDS lab output" tracking row does
not yet list DeepCode — out of scope to edit from this doc, noted here for
whoever next maintains that table.

## Sources

| Source | Content |
|---|---|
| [HKUDS/DeepCode repo][repo] | README, architecture description, release history (first-party) |
| GitHub API repo metadata, 2026-09-24 | Stars(16,632)/forks(2,163), MIT, dates, release list |

[repo]: https://github.com/HKUDS/DeepCode
