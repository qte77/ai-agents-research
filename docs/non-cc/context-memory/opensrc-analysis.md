---
title: opensrc Analysis
source: https://github.com/vercel-labs/opensrc
purpose: Analysis of vercel-labs/opensrc — a CLI that fetches package source code (not just types) to deepen AI coding-agent context.
created: 2026-06-27
updated: 2026-11-26
validated_links_on: 2026-06-27
status: assess
---

## What It Is

opensrc (vercel-labs) fetches package **source code** (not just type definitions) to give AI coding agents deeper implementation context — solving the problem of agents seeing type signatures without understanding internal behavior. It is an agent-agnostic CLI (it fetches sources into a global on-disk cache), originally npm-focused and now multi-registry (npm, PyPI, crates.io, GitHub, GitLab, Bitbucket), which is why it lives here rather than in the cc-community tooling docs.

**Repo**: [vercel-labs/opensrc](https://github.com/vercel-labs/opensrc) | **Stars**: 3.0K (3,042, checked 2026-11-26) | **License**: Apache-2.0

## How It Works

Per the CLI README (checked 2026-11-26; v0.7.3, a native Rust binary):

1. Resolves a package to its git repository URL via registry APIs (npm, PyPI, crates.io; plus GitHub, GitLab and Bitbucket repos directly)
2. Detects the installed version from lockfiles (npm only; lockfile filenames not listed in the README, unverified) or uses the latest
3. Shallow-clones the repository at the matching version tag
4. Caches it globally at `~/.opensrc/repos/<host>/<owner>/<repo>/<version>/` (override with `OPENSRC_HOME`), with metadata in `~/.opensrc/sources.json`

The current README documents no project-local `opensrc/` directory and no `.gitignore`, `tsconfig.json` or `AGENTS.md` changes (whether older npx-based versions did is unverified).

## CLI Usage

```bash
npm install -g opensrc
rg parse $(opensrc path zod)            # fetch on cache miss, print cached path
opensrc path zod@3.22.0                 # exact version
opensrc path pypi:requests              # PyPI package
opensrc path vercel/next.js             # GitHub repo
opensrc list [--json]                   # show cached sources
opensrc remove zod                      # clean up
```

Other commands: `opensrc fetch <pkgs>` and `opensrc clean [--packages|--repos|--npm|--pypi|--crates]`.

## Output Structure

```text
~/.opensrc/
├── sources.json        # metadata index
└── repos/<host>/<owner>/<repo>/<version>/   # checked-out source
```

## Key Differentiator

Complements the context-management stack from a different angle: source-fetchers **deepen** context with actual implementations, where other tools reduce, deduplicate, or multiply it.

## Cross-References

- [agent-frameworks-infrastructure-landscape.md](../frameworks/agent-frameworks-infrastructure-landscape.md) — agent context/memory infrastructure
- [CC-community-tooling-landscape.md](../../cc-community/CC-community-tooling-landscape.md) — the CC dev-tooling stack (RTK and others) opensrc complements

## Sources

| Source | Content |
|---|---|
| [vercel-labs/opensrc](https://github.com/vercel-labs/opensrc) | Fetches package source code for agent context (repo; GitHub About text still says npm); CLI README at `packages/opensrc/README.md` |
