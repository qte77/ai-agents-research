---
title: opensrc Analysis
source: https://github.com/vercel-labs/opensrc
purpose: Analysis of vercel-labs/opensrc — a CLI that fetches npm package source code (not just types) to deepen AI coding-agent context.
created: 2026-06-27
updated: 2026-06-27
validated_links: 2026-06-27
---

**Status**: Assess

## What It Is

opensrc (vercel-labs) fetches npm package **source code** (not just type definitions) to give AI coding agents deeper implementation context — solving the problem of agents seeing type signatures without understanding internal behavior. It is an agent-agnostic CLI (it writes sources to disk and optionally an `AGENTS.md`), TypeScript/npm-ecosystem specific, which is why it lives here rather than in the cc-community tooling docs.

**Repo**: [vercel-labs/opensrc](https://github.com/vercel-labs/opensrc) | **Stars**: 2.6K | **License**: Apache-2.0

## How It Works

1. Queries npm registry for package repository URLs
2. Auto-detects installed versions from lockfiles (package-lock.json, pnpm-lock.yaml, yarn.lock)
3. Clones repositories at matching git tags
4. Stores sources in `opensrc/<package-name>/`
5. Optionally modifies `.gitignore`, `tsconfig.json`, `AGENTS.md`

## CLI Usage

```bash
npx opensrc zod              # fetch version matching lockfile
npx opensrc zod@3.22.0       # exact version
npx opensrc facebook/react   # GitHub repo
npx opensrc list             # show fetched sources
npx opensrc remove zod       # clean up
```

## Output Structure

```text
opensrc/
├── settings.json       # user preferences
├── sources.json        # package index with versions/paths
└── zod/
    └── src/            # actual source code
```

## Key Differentiator

Complements the context-management stack from a different angle: source-fetchers **deepen** context with actual implementations, where other tools reduce, deduplicate, or multiply it. TypeScript/npm-ecosystem specific.

## Cross-References

- [agent-frameworks-infrastructure-landscape.md](agent-frameworks-infrastructure-landscape.md) — agent context/memory infrastructure
- [CC-community-tooling-landscape.md](../cc-community/CC-community-tooling-landscape.md) — the CC dev-tooling stack (RTK, Boucle) opensrc complements

## Sources

| Source | Content |
|---|---|
| [vercel-labs/opensrc](https://github.com/vercel-labs/opensrc) | Fetches npm package source code for agent context (repo) |
