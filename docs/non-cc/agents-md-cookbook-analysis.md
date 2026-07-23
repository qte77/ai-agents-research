---
title: agents-md-cookbook — Tool-Agnostic AGENTS.md Template Kit
purpose: Assess a tested AGENTS.md template/linter/migrator kit and its claim of cross-tool AGENTS.md support
source: https://github.com/Taiizor/agents-md-cookbook
platform_scope: [cursor, openai-codex, github-copilot, windsurf, cline, zed, amp, google-jules, opencode, roocode, claude-code]
created: 2026-07-23
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Assess

## What It Is

A tested, tool-agnostic [AGENTS.md][agents-standard] kit: 15 stack-specific
AGENTS.md templates, a CI linter (`agents-md-lint`), and a migrator
(`agents-md-migrate`) that converts an existing `CLAUDE.md`/`.cursorrules`/
`GEMINI.md`/Copilot/Windsurf/Cline/Aider config into a single AGENTS.md.
MIT-licensed, single-maintainer ([Taiizor][repo]), v1.0.0 (tagged
2026-06-14, aliased `v1` for its GitHub Action), last pushed 2026-07-21.
7 stars, 7 watchers, 0 forks, 0 open issues.

## Contents and Verification

- **15 templates** (`templates/`, confirmed by directory listing): typescript-node,
  python, go, rust, java-spring, dotnet-csharp, nextjs, react-vite, django,
  fastapi, rails, monorepo, data-ml, react-native, minimal.
- **`packages/*`** npm monorepo (Node >=18, Bun+TS): `agents-md-lint` (scores/lints
  AGENTS.md, fails CI on regressions) and `agents-md-migrate` (converts other
  agents' configs into AGENTS.md). Plus a first-party GitHub Action and a docs
  handbook (`anatomy.md`, `best-practices.md`, `nesting-monorepos.md`,
  `common-mistakes.md`); CI dogfoods its own linter on its own templates.
- **Template justification**: README cites three studies converging on a
  100-150 line, command-first AGENTS.md — GitHub's review of 2,500+ repos,
  ETH Zurich's AGENTbench ([arXiv:2602.11988][agentbench], Feb 2026), and
  Augment Code's golden-PR (AuggieBench) eval — the project's own framing,
  not independently re-verified here.
- **Compatibility matrix** (`COMPATIBILITY.md`, summarized in README): Cursor,
  OpenAI Codex, GitHub Copilot (coding agent), Windsurf/Cascade, Cline, Zed,
  Amp, Google Jules, and opencode/RooCode are marked **NATIVE** AGENTS.md
  readers. **Claude Code is marked ADAPTER** (needs a symlink or `@AGENTS.md`
  import) — confirming this doc's `non-cc/` placement over `cc-community/`.
- License and version were independently re-verified against the LICENSE
  file and `package.json` (root + `packages/linter`) via the GitHub API.

## Corpus Relevance

No prior coverage — `git grep` across `docs/` for `agents-md-cookbook`,
`Taiizor`, `agents-md-lint`, `agents-md-migrate` returns zero hits. The only
tangential mention of AGENTS.md itself is
[opencode-analysis.md](opencode-analysis.md) (~L93-95, 138, 147), which
covers it only as opencode's own context-seeding file — not this cookbook.

This kit is a concrete tooling instance of the convergence trend traced in
[multi-agent-onboarding-outlook.md](../sdlc-lcm/multi-agent-onboarding-outlook.md)
("AGENTS.md Convergence" section): that doc covers the config-format
fragmentation problem across agents; this one is a templates+linter+migrator
answer to it.

## Unverifiable / Hedged

- README's claim of "60,000+ repositories" and "24+ tools" reading AGENTS.md
  natively, and stewardship by the "Linux Foundation's Agentic AI
  Foundation," is the project's own framing of the external standard — not
  independently verified here.
- `agents-md-migrate`'s exact version and npm download counts for either
  package were not independently checked.

## Sources

| Source | Content |
|---|---|
| [agents-md-cookbook repo][repo] | README, templates/, packages/, action.yml, docs handbook (first-party) |
| [LICENSE][license] | MIT text, verified via decode against `Copyright (c) 2026 Taiizor` |
| [package.json][pkg] | Root + `packages/linter` version 1.0.0, `node >=18`, Bun+TS scripts |
| [COMPATIBILITY.md][compat] | Native-vs-adapter classification (Claude Code = ADAPTER) |
| GitHub API repo metadata, 2026-07-23 | Stars(7)/watchers(7)/forks(0)/issues(0), dates, v1.0.0 = v1 tag alias |

[agents-standard]: https://agents.md
[repo]: https://github.com/Taiizor/agents-md-cookbook
[license]: https://github.com/Taiizor/agents-md-cookbook/blob/main/LICENSE
[pkg]: https://github.com/Taiizor/agents-md-cookbook/blob/main/package.json
[compat]: https://github.com/Taiizor/agents-md-cookbook/blob/main/COMPATIBILITY.md
[agentbench]: https://arxiv.org/abs/2602.11988
