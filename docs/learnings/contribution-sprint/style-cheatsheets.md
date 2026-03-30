---
title: Contribution Style Cheatsheets
purpose: Quick-reference coding style and PR conventions for compass-mcp, SimpleAgents, and opencode
created: 2026-03-30
updated: 2026-03-30
---

# Contribution Style Cheatsheets

## Quick Comparison

| Dimension | compass-mcp | SimpleAgents | opencode |
|---|---|---|---|
| Language | TypeScript strict / ESM | Rust-first + Python/Node/Go | TypeScript / Bun |
| Commits | lowercase verb-noun | conventional `feat(mod):` | conventional (PR titles) |
| Default branch | `main` | `main` | **`dev`** |
| CI | none | bindings-ci, docs-quality, benches | test.yml (unit + e2e) |
| Tests | none (MCP Inspector) | `make test-*` per language | `bun turbo test` per-pkg |
| Governance | none | CONTRIBUTING.md + AGENTS.md | CONTRIBUTING.md + AGENTS.md + vouch |
| PR rules | informal | TODO.md update required | issue-first, no AI walls of text |
| License | MIT | Apache-2.0 (dual MIT OR Apache-2.0) | MIT |

---

## compass-mcp ([richlira/compass-mcp][compass])

### Style

- TypeScript **strict mode**, ES2022 target, ESM only (`"type": "module"`)
- `node:` prefix for Node.js builtins (`import fs from 'node:fs/promises'`)
- **camelCase** functions/vars, **PascalCase** interfaces, **SCREAMING_SNAKE** constants
- Zod `.describe()` for parameter docs — no JSDoc
- MCP tools via `server.tool(name, description, zodSchema, asyncHandler)`
- Consistent return: `{ content: [{ type: 'text', text: ... }] }`
- Async/await everywhere; silent-fail error handling (`catch { return '' }`)

### Versions

- Node.js >=20, TypeScript 5.8.3
- MCP SDK 1.25.2, Zod 4.3.6

### PR Process

- No formal guidelines — match existing style
- Lowercase verb-noun commits: `add banner`, `fix parsing`
- Target: `main`
- Build must pass: `npm run build`
- Test with MCP Inspector: `npx @modelcontextprotocol/inspector node build/index.js`

### Anti-Patterns

- No tests exist — propose in issue before adding test framework
- No linter — match style manually
- `.gitignore` does NOT exclude `.claude/` — be extra careful

---

## SimpleAgents ([CraftsMan-Labs/SimpleAgents][simpleagents])

### Style

- **Rust edition 2021**, MSRV 1.75, workspace version 0.2.31
- `cargo fmt --all` + `cargo clippy --all-targets` — CI-enforced + pre-commit hook
- No `unwrap`/`expect` in runtime code (tests only)
- `Option<T>` matching over truthy checks
- Never block async executors with blocking locks
- Python: 3.9+ (maturin/PyO3), `.pyi` stubs required for LSP
- Node: 18+ (napi-rs), `.d.ts` correctness maintained
- Go: 1.21+ (C FFI), exported APIs typed

### PR Process

- Conventional commits: `feat(module):`, `fix(module):`, `docs:`, `refactor:`, `test:`
- Feature branches required
- **TODO.md must be updated in same PR as code changes** — mark `[x]` with evidence
- CI must be green: `bindings-ci.yml`, `docs-quality.yml`, `workflow-benches.yml`
- Docs updated in same PR if behavior changed

### Build & Test

```bash
make test-rust             # Rust tests
make test-python           # Python binding tests
make test-node             # Node binding tests
make test-go-bindings      # Go binding tests
make test-binding-contracts # Cross-language parity
make clippy                # Lint
make fmt                   # Format check
make coverage-rust         # Coverage threshold (default: 100%)
```

### Anti-Patterns

- Do NOT skip TODO.md update
- Do NOT submit without reading CONTRIBUTING.md + AGENTS.md
- `.gitignore` does NOT exclude `.claude/` — verify before push

---

## opencode ([anomalyco/opencode][opencode])

### Style (AGENTS.md — mandatory)

- Bun 1.3.11 (pre-push hook enforced), TypeScript 5.8.2
- Prettier: **no semicolons** (`semi: false`), `printWidth: 120`
- EditorConfig: 2-space indent, spaces, UTF-8, LF
- **Single-word variable names** by default (`pid`, `cfg`, `err`, `opts`)
- No `any` type — precise types required
- No `else` — early returns only
- No unnecessary destructuring — use `obj.a` instead
- No `try/catch` — use `.catch(...)` instead
- Bun APIs over Node APIs (`Bun.file()` etc.)
- `const` only — avoid `let`
- Functional array methods (`flatMap`, `filter`, `map`) over `for` loops
- Drizzle schemas: `snake_case` field names, no string redefinition

### PR Process

- **Default branch is `dev`** — never PR to main
- **Issue-first**: must reference `Fixes #123` or `Closes #123`
- Conventional commit titles: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`
- Optional scope: `feat(app):`, `fix(desktop):`
- PR template required: issue ref, type, description, verification method, screenshots (UI)
- **No AI-generated walls of text** — concise, respect maintainers' time
- Vouch system — new contributors may face additional scrutiny

### Build & Test

```bash
bun install                # Install deps
bun dev                    # Run TUI
bun typecheck              # Type check (not tsc directly)
bun turbo test             # All tests (per-package, NOT from root)
bun --cwd packages/app test:e2e:local  # E2E
bun prettier --write src/**/*.ts       # Format
```

### Anti-Patterns

- Do NOT PR to `main`
- Do NOT submit without an existing issue
- Do NOT write verbose AI-style descriptions
- Do NOT run tests from repo root — always from package dir
- Do NOT use Node.js APIs when Bun equivalents exist
- `.gitignore` status for `.claude/` and `.opencode/` — verify before push

---

## Sources

| Source | Content |
|---|---|
| [compass-mcp][compass] | package.json, tsconfig.json, src/ code patterns |
| [SimpleAgents][simpleagents] | CONTRIBUTING.md, AGENTS.md, Makefile, CI workflows |
| [opencode][opencode] | CONTRIBUTING.md, AGENTS.md, SECURITY.md, package.json, .editorconfig |
| CC plugins analysis, 2026-03-30 | Plugin inventory across all branches |

[compass]: https://github.com/richlira/compass-mcp
[simpleagents]: https://github.com/CraftsMan-Labs/SimpleAgents
[opencode]: https://github.com/anomalyco/opencode
