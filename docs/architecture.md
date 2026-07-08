---
title: Architecture - ai-agents-research
description: Document hierarchy, conventions, and downstream consumer relationships for the ai-agents-research repository
category: technical
created: 2026-03-22
updated: 2026-06-22
---

## Architecture: ai-agents-research

## Overview

This is a research-only repository — no code, only structured markdown documents. The "architecture" is the document hierarchy, naming conventions, and the four automated monitors that keep it current.

## Document Hierarchy

```text
ai-agents-research/
├── docs/
│   ├── cc-native/             # Anthropic-native CC features
│   │   ├── agents-skills/     # Agent spawning, skills, orchestration patterns
│   │   ├── ci-remote/         # GHA, cloud sessions, remote access, web auth
│   │   ├── configuration/     # Hooks, fast mode, model/provider config, CLI ref
│   │   ├── context-memory/    # Extended context, memory system, llms.txt
│   │   ├── examples/          # Worked examples and reference workflows
│   │   ├── model-internals/   # Model-level interpretability research
│   │   ├── plugins-ecosystem/ # Official plugins, community plugins, cowork API
│   │   ├── sandboxing/        # Sandbox internals (bwrap, platforms, permissions)
│   │   └── sessions/          # Session lifecycle, artifacts, schemas
│   ├── cc-community/          # Community skills, tooling, CLAUDE.md patterns
│   ├── non-cc/                # Non-CC coding agents (JetBrains Air, DeerFlow, Goose, ...)
│   ├── sdlc-lcm/              # SDLC + product lifecycle management specs
│   ├── learnings/             # Cross-repo compound learnings hub (CRLA write-back target)
│   │   └── per-repo/          # Per-repo pattern distillations
│   ├── research/              # Auto-generated cumulative agentic-AI paper index (rxiv eval)
│   ├── plans/                 # Plan/design docs (durable plan-mode output; backlog = GitHub Issues)
│   └── archive/               # Retired Agents-eval era docs
├── triage/                    # Auto-generated monitor outputs (at repo root)
│   ├── cc-changelog/          # CC changelog + native-sources triage
│   ├── community/             # Community-sources triage
│   ├── status-monitor/        # CC status page incident archive + stats
│   └── rxiv/                  # ArXiv paper eval triage (filtered by RXIV_TOPIC)
├── scripts/                   # Graph-page render + font-fetch helpers (stdlib-only)
├── tests/                     # Unit tests for scripts/ + .github/scripts/lib modules
├── ui/                        # Branded gh-pages site (index.html, graph.html, assets)
├── changelog.d/               # scriv changelog fragments (collected on release)
└── .github/
    ├── workflows/             # 4 content-monitor crons + link-rot monitor + lint workflow
    ├── actions/               # Composite actions (create-triage-pr)
    ├── scripts/               # Monitor scripts + shared lib/monitor_utils.py
    └── state/                 # Per-monitor fingerprint files (committed)
```

## Planning & Roadmap

- **Backlog / roadmap** — [GitHub Issues](https://github.com/qte77/ai-agents-research/issues) are the single source of truth for planned and deferred work (per #191; the former static `docs/TODO.md` was retired to avoid CHANGELOG/issue duplication).
- **Design docs** — `docs/plans/` holds durable plan/design docs (the saved output of plan-mode work); each links its tracking issue. See [docs/plans/README.md](plans/README.md).
- **Landed work** — `CHANGELOG.md` `[Unreleased]` records what has merged.

## Analysis Format Convention

Every research document follows this four-section structure:

1. **What it is** — Brief description of the feature or agent
2. **How it works** — Mechanism, internals, observed behavior
3. **Adoption decision** — Adopt / Defer / Skip with rationale
4. **Action items** — Concrete next steps for downstream repos

This format ensures each doc is directly actionable, not just descriptive.

## Frontmatter Conventions

All documents carry YAML frontmatter:

```yaml
---
title: <Descriptive title>
description: <One-line summary>
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Optional fields: `category`, `version`, `tags`, `source`.

## Automated Monitors

Four GitHub Actions cron workflows maintain currency by polling external sources and opening triage PRs when new content is found:

| Monitor | Source | Output | Schedule |
|---|---|---|---|
| CC status monitor | Anthropic status page | `triage/status-monitor/` | Monday 09:00 UTC |
| CC changelog + native sources | CC release notes + GH issues/discussions + Anthropic blog | `triage/cc-changelog/` | Monday 09:00 UTC |
| Community monitor | Community forums, GitHub | `triage/community/` | Monday 10:00 UTC |
| ArXiv paper eval | `qte77/gha-rxiv-feed-action` CSVs → LLM relevance filter | `triage/rxiv/` | Tuesday 09:00 UTC |

Each monitor commits its state-fingerprint file in `.github/state/` alongside the triage PR for content-stable dedup across runs. The rxiv eval skips PR creation when the assembled report fingerprint matches the prior emission for the same `(server, year, week)` key.

A fifth scheduled workflow — `link-rot-monitor` (Monday 12:00 UTC) — is a **health** monitor rather than a content monitor: it runs lychee weekly and upserts (then auto-closes) a single `link-rot` issue when external links break. See [Lint Gate](#lint-gate).

## Lint Gate

Three lint jobs run on every PR touching docs, workflows, or actions:

| Job | Tool | Scope |
|---|---|---|
| Markdown lint | `markdownlint-cli2` | root governance docs (`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, `AGENT_LEARNINGS.md`, `AGENT_REQUESTS.md`) + `docs/**/*.md` |
| Link check | `lychee` | repo-wide (configured via `lychee.toml`) |
| Action lint | `actionlint` (+ `shellcheck` on the runner) | `.github/workflows/**`, `.github/actions/**` |

The rxiv triage job additionally runs `markdownlint-cli2` against the assembled would-be PR content (with the action's H1 prepend simulated) and fails the job before opening a triage PR if the output is md-dirty.

## Knowledge Graph (graphify)

An optional graphify knowledge graph maps the corpus — concepts, cross-document references, and community structure — for navigation and gap-finding. It is **on-demand only**: no hooks or `CLAUDE.md` mandates run it automatically (that per-tool-call overhead was deliberately removed), so it adds no cost to normal sessions. Build output (`graphify-out/`) is gitignored; the EyeRest-restyled copy is committed to `ui/graph.html` and published to GitHub Pages by the deploy workflow.

**Live site:** <https://qte77.github.io/ai-agents-research/> — a branded EyeRest landing page (`index.html`) linking to the knowledge graph at `/graph.html`. After a rebuild, run `make graph-page`, then commit & push — the gh-pages workflow deploys.

### Published site (gh-pages)

The site applies the qte77 EyeRest brand (`qte77/qte77/brand/DESIGN.md`: zero-blue, warm umber/parchment), like the sibling repos `analyze-stock-kpi` and `paperverse`. Source lives in `ui/`:

| Path | Role |
|---|---|
| `ui/index.html` | Branded landing page (site root) |
| `ui/graph.html` | EyeRest-restyled knowledge graph — committed; produced locally by `make graph-page` |
| `ui/vendor/vis-network.min.js` | Self-hosted vis-network (graphify's renderer) — committed so the graph renders offline / without a CDN round-trip |
| `ui/style.css` | EyeRest design tokens + `@font-face` + layout |
| `ui/favicon.svg` | Adapted qte77 logo-mark |
| `ui/assets/fonts/*.woff2` | Self-hosted Inter + JetBrains Mono — committed (refresh with `make graph-fonts`); `@font-face` falls back to system-ui if absent |
| `scripts/pages_build.py` | Pure, unit-tested helpers — `filter_graph_data()` prunes tooling/code nodes; `restyle_graph()` recolors the export to EyeRest, injects fonts/favicon/title, and repoints vis-network from unpkg to the vendored copy (both run by `make graph-page`); font helpers feed the fetch script |

**Deploy** is a GitHub Actions workflow (`.github/workflows/gh-pages.yaml`) using the Pages API — like the sibling repos `analyze-stock-kpi` and `paperverse` (no `gh-pages` branch). On push to `main` (paths under `ui/`), CI assembles `ui/` (with the committed fonts and vendored vis-network) into the Pages artifact and deploys. The repo's **Settings → Pages → Source** must be set to "GitHub Actions".

The knowledge graph stays **local and interactive** (key-free, via the `/graphify` skill — no LLM in CI): rebuild the graph, run `make graph-page` to render + EyeRest-restyle it into the committed `ui/graph.html`, then commit & push to trigger a deploy. `make graph-page` also **prunes build/tooling nodes** (`scripts/`, `tests/`, `ui/`, `src/`, `.github/scripts/`) so the published graph maps the research corpus, not the machinery — workflows and actions are kept.

The landing page carries a **System / Light / Dark theme picker** (persisted to `localStorage`, no-flash, OS-following by default); the graph page stays dark.

**Build** (semantic extraction needs an LLM):

- Interactive, key-free — the `/graphify` Claude Code skill (uses the session as the extraction model).
- Headless, for CI/scripts — `graphify extract . --backend gemini` (or `claude`, `openai`, …) with the matching API key, then `graphify label .` to name communities. Also exposed as `make graph-build`.

**Navigate** (free, no LLM — operate on `graphify-out/graph.json`):

| Action | Command |
|---|---|
| Query | `make graph-query Q="<question>"` |
| Explain a node | `make graph-explain N="<node>"` |
| Shortest path | `make graph-path A="<node>" B="<node>"` |
| Re-render viz | `make graph-html` |

Install `graphify` with `uv tool install graphifyy` — this puts the `graphify` CLI on `PATH` (interpreter under `~/.local/share/uv/tools/graphifyy/`) and is the key-free path used for a local `/graphify` rebuild. Alternatively it is side-loaded (not on `PATH`); set `GRAPHIFY=/path/to/graphify` to point the recipes at a specific build.

## Downstream Consumers

Research from this repository feeds directly into implementation repos:

| Downstream Repo | Consumes From | Key Docs |
|---|---|---|
| [cc-recursive-team-mode](https://github.com/qte77/cc-recursive-team-mode) | `docs/cc-native/agents-skills/`, `docs/cc-native/session-analysis/` | `CC-recursive-spawning-patterns.md`, session artifact schema docs |
| [coding-agent-eval](https://github.com/qte77/coding-agent-eval) | `docs/cc-native/comparisons/`, `docs/cc-native/features/`, `docs/non-cc/` | Agent feature matrices, invocation method analyses |
| [multi-tasking-quality-benchmark](https://github.com/qte77/multi-tasking-quality-benchmark) | `docs/cc-native/meta/` | Quality metric methodology docs |
| [ralph-loop-cc-tdd-wt-vibe-kanban-template](https://github.com/qte77/ralph-loop-cc-tdd-wt-vibe-kanban-template) | `docs/learnings/` | Cross-repo compound learning aggregation (CRLA) — Ralph reads this as `COMPOUND_LEARNINGS_PATH` |

## Reference Flow

```text
External sources (CC changelog, status page, community)
        ↓ (automated monitors)
triage/  (raw triage outputs, human-reviewed)
        ↓ (researcher promotes findings)
docs/cc-native/ or docs/non-cc/ or docs/cc-community/  (structured analyses)
        ↓ (downstream repos consume)
cc-recursive-team-mode / coding-agent-eval / multi-tasking-quality-benchmark
```

Human review is required at the triage → docs promotion step. Monitors surface content; researchers make adoption decisions.
