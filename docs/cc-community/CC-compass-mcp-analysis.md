---
title: Compass-MCP Analysis
source: https://github.com/richlira/compass-mcp
purpose: Architecture and status analysis of compass-mcp for CC-native integration potential.
created: 2026-03-28
updated: 2026-03-28
validated_links: 2026-03-28
---

# Compass-MCP Analysis

## What It Is

MCP server bridging Claude Chat, Cowork, and Code via shared operational state.
Provides task management and project context persistence in plain markdown files.

- **Stack**: TypeScript, Node.js 20+, `@modelcontextprotocol/sdk` 1.25.2, Zod 4
- **Storage**: `~/compass-data/` (plain markdown, no database)
- **Philosophy**: "Six tools, two file types, zero database"
- **License**: MIT

## Architecture

```
src/
├── index.ts           # MCP server entry (StdioServerTransport)
├── tools/
│   ├── workspace.ts   # init_workspace (idempotent setup)
│   ├── tasks.ts       # add_task, complete_task, get_tasks
│   └── contexts.ts    # save_context, get_context
└── utils/
    ├── config.ts      # DATA_DIR (env: COMPASS_DATA_DIR)
    ├── dates.ts       # today() helper
    └── files.ts       # readDataFile, writeDataFile, fileExists
```

### Task Format

```markdown
- [ ] Task title | tags: tag1, tag2 | deadline: YYYY-MM-DD | created: YYYY-MM-DD
- [x] Done task | tags: dev | completed: YYYY-MM-DD
```

Fuzzy matching for completion (case-insensitive contains). Pipe-separated metadata.

### Context Format

Individual markdown files in `contexts/{project-slug}.md`.

## Project Status

- **Maturity**: Brand new (3 commits, initial release)
- **Open Issues**: 0
- **Open PRs**: 0
- **Contributors**: 1 (+ Claude co-author)
- **Activity**: Foundation/branding phase

## Alignment with qte77 Ecosystem

| Factor | Assessment |
|--------|------------|
| Cross-surface context persistence | Direct overlap with cc-meta research |
| Plain markdown storage | Compatible with CC's own artifact patterns |
| MCP server architecture | Can integrate with CC hooks and plugins |
| Task management | Parallel to CC's native tasks (but cross-surface) |

## Technical Notes

- Uses Zod v4 (latest) for schema validation
- StdioServerTransport (local only, no HTTP transport yet)
- No build artifacts in repo (needs `npm run build` first)
- Google Calendar integration mentioned in README but not in source code yet
