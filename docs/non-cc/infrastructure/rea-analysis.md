---
title: REA — Reverse Engineer Anything
source: https://github.com/morluto/rea
purpose: Assess REA, an MCP server and CLI giving coding agents reverse-engineering tools for native binaries, JS/Electron apps, .NET assemblies, and websites.
platform_scope: [claude-code, codex, cursor, gemini-cli]
created: 2026-10-11
updated: 2026-10-11
validated_links: 2026-10-11
status: assess
---

## What It Is

[REA][repo] ("Reverse Engineer Anything") connects a coding agent to reverse-engineering tooling
through one MCP server, distributed as the npm package `rea-agents`. The README's own framing:
"See a feature you like. Understand how it works, down to the binary level." An agent (or a human
from the terminal, via the same tool surface) can inspect a target without its source — a native
binary, a JavaScript/Electron app, a .NET assembly, a website, an Android APK, firmware, and more —
and REA returns findings with their evidence, which the agent then uses to explain the behavior or
reimplement it.

`npx rea-agents setup` registers REA's MCP server and matching workflow instructions. Quoting the
README verbatim: "Setup supports Claude Code, Codex, Cursor, Gemini CLI, Grok Build and other
agents" — Claude Code is one of several first-class named targets, not the product's differentiator.
Deep native-binary analysis (pseudocode, assembly, symbols) can drive an existing Hopper, Ghidra, or
IDA installation; static JavaScript/Electron and .NET analysis need no native engine at all. The
analysis-target table in the README lists over a dozen formats beyond native binaries and JS/.NET,
including WASM artifacts, EVM bytecode, HAR network captures, Android APKs/devices, JEB projects,
firmware, and raw process-behavior capture — each with its own requirements and a dedicated guide.
Analysis runs locally; the README states results "include the evidence and limitations behind each
conclusion."

## License, stars, dates

MIT (confirmed by reading the `LICENSE` file directly: "Copyright (c) 2026 morluto"). 101,489 stars,
22,286 forks, 170 open issues, 314 watchers (all `gh api repos/morluto/rea`, 2026-10-11). Created
2026-04-14; last pushed 2026-10-11 (same day) — under six months old. The README's own star-history
section reports crossing 90,000 stars as a milestone, and the repo carries a Trendshift badge. A star
count this large for a six-month-old repo is unusual; this is reported as an observed GitHub metric,
not evidence of production adoption, which this review did not independently assess. The README
also includes a disclaimer stating REA has "not issued or endorsed any cryptocurrency or token" and
that tokens using the REA name are unaffiliated.

The repo's own GitHub topics (`gh api repos/morluto/rea`) include `dsh-plugin` and `cordis` alongside
the expected `mcp`/`reverse-engineering`/`ctf` tags — Cordis is the dependency-injection framework
[DeepSeek Harness][dsh] is built on, so REA appears designed to also install as a DeepSeek Harness
(`dsh`) plugin, in addition to its MCP-server path for Claude Code/Codex/Cursor/Gemini CLI/Grok Build.
This review did not independently verify the `dsh-plugin` integration beyond the topic tag.

## Why a new doc, not an extension

Per this corpus's "extend, don't create" convention, three existing landscapes were checked as
possible homes before writing a standalone doc:

- [CC-reverse-engineering-landscape.md](../../cc-community/CC-reverse-engineering-landscape.md) — its
  own purpose line scopes it to tools that "reverse engineer Claude Code internals — system prompts,
  binary analysis, env vars, API interception." That is reverse-engineering of Claude Code itself;
  REA is the opposite direction — an agent (Claude Code or otherwise) reverse-engineering *other*
  software. No topical overlap.
- [CC-code-tooling-landscape.md](../../cc-community/CC-code-tooling-landscape.md) — scoped to
  "code-understanding tools that integrate with Claude Code" (knowledge graphs, semantic LSP,
  structural search, repo packers) for an agent's *own* repository, and CC-exclusive by its own
  framing. REA targets black-box binaries/apps the agent does not own the source of, and is explicitly
  multi-agent (Claude Code, Codex, Cursor, Gemini CLI, Grok Build). Wrong subject and wrong scope.
- [agent-code-analysis-landscape.md](../../sdlc-lcm/agent-code-analysis-landscape.md) — scoped to
  static/dynamic analysis *of agent-produced code* for security (SCA/DCA), not reverse engineering of
  arbitrary third-party binaries or apps. Different subject (security scanning vs. feature-level
  reverse engineering).

None of the three fits REA's actual subject, so this doc is new, following the existing
single-product pattern in this directory (e.g. [corsair-analysis.md](corsair-analysis.md),
[goclaw-analysis.md](goclaw-analysis.md)).

## Adoption Decision

**Assess.** REA is MIT-licensed, multi-agent (not CC-exclusive), and ships a genuinely broad analysis
surface (native binaries via Hopper/Ghidra/IDA, static JS/Electron/.NET with no native engine
required, Android, firmware, and more) with per-target documentation. The scale of its star count and
its very recent creation date (2026-04-14) both argue for caution: this review did not independently
verify any of the showcased case studies (DX-Ball, Notion, TH04) or run REA against a target, and the
"90,000 GitHub stars" milestone is a platform metric, not an adoption or correctness signal. Revisit
once independent usage reports or security review of the MCP surface (a tool that drives
reverse-engineering binaries and can launch native analysis engines) are available.

## Sources

| Source | Content |
|---|---|
| [morluto/rea][repo] (README) | Product description, target-analysis table, agent support list, FAQ, disclaimer, star-history (accessed 2026-10-11) |
| [morluto/rea][repo] (repo metadata) | Stars/forks/issues/watchers, license, created/pushed dates (accessed 2026-10-11 via GitHub API) |
| `LICENSE` file, decoded via GitHub API, 2026-10-11 | MIT license text, copyright "morluto" |

[repo]: https://github.com/morluto/rea
[dsh]: ../coding-agents/deepseek-harness-analysis.md
