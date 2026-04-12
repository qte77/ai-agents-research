---
title: Compass-MCP Analysis
source: https://github.com/richlira/compass-mcp
purpose: Architecture analysis, contribution gaps, and CC-native integration potential for compass-mcp.
created: 2026-03-28
updated: 2026-03-29
validated_links: 2026-03-29
---

## Compass-MCP Analysis

## What It Is

MCP server bridging Claude Chat, Cowork, and Code via shared operational state.
Provides task management and project context persistence in plain markdown files.

- **Stack**: TypeScript, Node.js 20+, `@modelcontextprotocol/sdk` 1.25.2, Zod 4
- **Storage**: `~/compass-data/` (plain markdown, no database)
- **Philosophy**: "Six tools, two file types, zero database"
- **License**: MIT

## Architecture

```text
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

## Contribution Gaps (2026-03-29)

Identified during source analysis for [multi-repo contribution plan][contrib-plan].

### Repo Hygiene (Pressing)

| Gap | Detail |
|-----|--------|
| **No LICENSE file** | README claims MIT but `gh api` reports `license: null` |
| **Version mismatch** | `package.json` = 1.0.0, `index.ts` creates server with 2.0.0 |
| **Node.js version inconsistency** | `package.json` engines >=20, README says "Node.js 18+" |
| **Dead parameter** | `complete_task` accepts `notes` but never writes it to file |
| **No repo description/topics** | GitHub metadata empty — hurts discoverability |

### Functional Gaps (High ROI)

| Gap | Detail |
|-----|--------|
| **No `list_contexts` tool** | Can save/get context by name but can't discover what exists |
| **No `delete_task` tool** | Can add/complete but never remove — basic CRUD gap |
| **No date validation** | `deadline` accepts any string, no format check |
| **Zero tests** | No test files, no test framework, no CI/CD |

### Architectural Gaps (Strategic)

| Gap | Detail |
|-----|--------|
| **Naive fuzzy matching** | `complete_task` uses `includes()` — ambiguous with overlapping titles |
| **No `edit_task` tool** | Can't update title/tags/deadline after creation |
| **No file locking** | Concurrent writes from Chat+Code = last-write-wins data loss |
| **No npm publishing** | Install requires git clone; no `bin` field for global CLI |

### Code Quality Notes

- `insertAfterHeading` is fragile with edge cases around newlines
- No error handling on write failures beyond OS throws
- ~250 lines total — very small codebase, low barrier to contribute

## Sources

| Source | Content |
|---|---|
| [richlira/compass-mcp][repo] | Repository source (3 commits, 2026-03-28) |
| [Multi-repo contribution plan][contrib-plan] | Contribution strategy and prioritization |

[repo]: https://github.com/richlira/compass-mcp
[contrib-plan]: # "(Codespaces-local reference removed — see project kanban for contribution context)"
