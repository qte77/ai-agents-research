---
title: Architecture - ai-agents-research
purpose: Document hierarchy, conventions, and downstream consumer relationships for the ai-agents-research repository
created: 2026-03-22
updated: 2026-11-21
validated_links_on: 2026-11-21
status: reference
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
│   │   └── <section>/         # 9 subdirs mirroring non-cc/README.md sections (orchestrators, agents, coding-agents, knowledge-management, reference, context-memory, infrastructure, frameworks, protocols)
│   ├── sdlc-lcm/              # SDLC + product lifecycle management specs
│   ├── _topics/               # Cross-subject hub indexes (memory, knowledge-graphs, rag, code-tooling, visualization, context, skills, plugins, harness, long-running, cost, evals-benchmarks, security, data, agentic-web, management, knowledge-management); pointers only
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
├── scripts/                   # Site-info + font-fetch helpers (stdlib-only); cc-multi-account.sh (CLAUDE_CONFIG_DIR profiles)
├── tests/                     # Unit tests for scripts/ + .github/scripts/lib modules
├── ui/                        # Branded gh-pages site (index.html, doc-graph.html, assets)
├── changelog.d/               # scriv changelog fragments (collected on release)
└── .github/
    ├── workflows/             # content-monitor crons, link-rot, m365-drift + plan-reconcile health monitors, manual model evals, lint, release, Pages
    ├── actions/               # Composite actions (create-triage-pr)
    ├── scripts/               # Monitor scripts, plan-reconcile.py + shared lib/
    └── state/                 # Per-monitor fingerprint files (committed)
```

## Planning & Roadmap

- **Backlog / roadmap** — [GitHub Issues](https://github.com/qte77/ai-agents-research/issues) are the single source of truth for planned and deferred work (per #191; the former static `docs/TODO.md` was retired to avoid CHANGELOG/issue duplication).
- **Design docs** — `docs/plans/` holds durable plan/design docs (the saved output of plan-mode work); each links its tracking issue. See [docs/plans/README.md](plans/README.md).
- **Plan vs live state** — `make reconcile` (`.github/scripts/plan-reconcile.py`) checks every PR/issue cited in the newest plan's remaining-work table, in any repo, and flags rows whose text disagrees with GitHub (#768). Run it before reporting what is open or blocked; `plan-reconcile-monitor` also runs it weekly.
- **Landed work** — `CHANGELOG.md` `[Unreleased]` records what has merged.

## Analysis Format Convention

Every research document follows this four-section structure:

1. **What it is** — Brief description of the feature or agent
2. **How it works** — Mechanism, internals, observed behavior
3. **Adoption decision** — the doc's `status` ([CONTRIBUTING.md §2](../CONTRIBUTING.md#2-frontmatter-status): `adopt`, `trial`, `assess` or `hold`) with rationale
4. **Action items** — Concrete next steps for downstream repos

This format ensures each doc is directly actionable, not just descriptive.

## Frontmatter Conventions

All documents carry YAML frontmatter, including the doc's `status:` (there is no body status badge). The rules live in [`schema/frontmatter.schema.json`](schema/frontmatter.schema.json) (JSON Schema, with each key's RDF (Resource Description Framework) term), explained in [CONTRIBUTING.md §1–§2](../CONTRIBUTING.md#1-frontmatter); `make check_frontmatter` and `make check_status` read it.

## Automated Monitors

Four GitHub Actions cron workflows maintain currency by polling external sources and opening triage PRs when new content is found:

| Monitor | Source | Output | Schedule |
|---|---|---|---|
| CC status monitor | Anthropic status page | `triage/status-monitor/` | Monday 09:00 UTC |
| CC changelog + native sources | CC release notes + GH issues/discussions + Anthropic blog | `triage/cc-changelog/` | Monday 09:00 UTC |
| Community monitor | GitHub awesome-lists | `triage/community/` | Monday 10:00 UTC |
| ArXiv paper eval | `qte77/gha-rxiv-feed-action` CSVs → decision-model relevance gate (Clef via `decide()`), chat-LLM fallback for uncertain papers | `triage/rxiv/` | Tuesday 09:00 UTC |

A content source whose fetch fails is listed as skipped, with the reason, in the report, the triage PR and the run summary (#811). A run in which no source returns any entries exits 2 and fails the job instead of opening an empty triage PR (#916).

Each monitor commits its state-fingerprint file in `.github/state/` alongside the triage PR for content-stable dedup across runs. The rxiv eval skips PR creation when the assembled report fingerprint matches the prior emission for the same `(server, year, week)` key. The CC changelog monitor's trigger uses `releases.atom` entry ids as its dedup ledger for feed-covered versions, falling back to the scan-doc version cutoff for any version the feed doesn't cover (a gap, or the feed being unavailable entirely) — `CHANGELOG.md` stays the sole content source either way (#410).

A fifth scheduled workflow — `link-rot-monitor` (Monday 12:00 UTC) — is a **health** monitor rather than a content monitor: it runs lychee weekly and upserts (then auto-closes) a single `link-rot` issue when external links break. See [Lint Gate](#lint-gate).

A sixth — `m365-drift-monitor` (Monday 13:00 UTC, added 2026-10-24, #720) — is also a health monitor: it
re-fetches the Microsoft Learn pages the Microsoft 365 Copilot doc relies on, compares each page's
`ms.date` and checks the doc's stored quote is still present, and upserts a single `m365-drift` issue
on any change or failed fetch (no page text is copied). An entry may also carry a `due` date (YYYY-MM-DD)
for a dated event the doc predicts; once it passes, the entry is reported even if the page is unchanged
(#764). Its state file is refreshed through a triage PR like the content monitors (#705).

A seventh — `plan-reconcile-monitor` (Monday 14:00 UTC) — runs `make reconcile` weekly and upserts (then auto-closes) a single `plan-drift` issue when a row of the newest plan disagrees with the live state of the PRs/issues it cites, so a merged blocker can't stay "blocked" between sessions. It fails the job, rather than filing an issue, when `gh` can't authenticate.

An eighth — `decision-model-eval` (1st of each month, 15:00 UTC; also manual) — is a drift check for the decision models (plan 0013 row A7): it reruns both G1 gold sets with Clef, Clef-flash and Jev 1.13.0, writes `metrics.json`, compares with the committed `.github/scripts/data/gold/baseline.json` (ROC-AUC drop above 0.03, or a recommended `hi` moving by 0.05 or more; Brier shown, not flagged) and upserts (then auto-closes) a single `decision-drift` issue. Manual runs show the same comparison in the run summary without touching the issue. A manual run on 2026-11-12 reproduced the Clef and Clef-flash baseline exactly.

**On-demand refresh (session-driven, not CI):** `.claude/workflows/refresh-docs.js` is a Claude Code Workflow-tool script (companion to the `adding-research-source` skill's `batch-sources` workflow) that re-verifies a given list of docs against their first-party sources — one read-only checker agent per doc plus an adversarial verifier per proposed correction set — and returns a corrections list the session then applies. The link-rot monitor guards URL *liveness*; `refresh-docs` guards claim *currency* (version gates, counts, renamed features). First run: the 2026-07-23 stale-cohort refresh (27 docs with `validated_links: 2026-03-*`).

## Lint Gate

These lint jobs run on every PR touching docs, workflows, or actions:

| Job | Tool | Scope |
|---|---|---|
| Markdown lint | `markdownlint-cli2` | root governance docs (`README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `AGENTS.md`, `AGENT_LEARNINGS.md`, `AGENT_REQUESTS.md`) + `docs/**/*.md` |
| Link check | `lychee` | repo-wide (configured via `lychee.toml`); github.com requests authenticated with the workflow `GITHUB_TOKEN` (#721) |
| Action lint | `actionlint` (+ `shellcheck` on the runner) | `.github/workflows/**`, `.github/actions/**` |
| Doc frontmatter | `make check_frontmatter` (`lib/doc_frontmatter.py`, stdlib) | content docs against `docs/schema/frontmatter.schema.json`; strict |
| Doc coverage | `make check_coverage` (`lib/doc_coverage.py`, stdlib) | every content doc under `docs/` is linked from its folder's README index and from at least one other doc or root file; every `#fragment` in a doc-to-doc link matches a heading (GitHub slug rules) or `<a id>` in its target |

The rxiv triage job additionally runs `markdownlint-cli2` against the assembled would-be PR content (with the action's H1 prepend simulated) and fails the job before opening a triage PR if the output is md-dirty.

## Doc Graph and Site

**Doc graph (plan 0009 row G, option C):** `make graph-data` runs `.github/scripts/build-doc-graph.py`, a stdlib-only builder backed by the unit-tested `lib/doc_graph.py`. `build_graph` holds doc nodes (bucket, status, title, doc type from the filename suffix, platforms) and `link` / `hub` edges with the line numbers and section fragments they occur on; external links make no node or edge. `site_graph` projects it onto `ui/doc-graph.json`: each doc's title, bucket, topic hubs (a hub row counts once per doc, even when it points at a section), hub state and clustering facets (`status`; `doc_type` from the filename suffix: analysis, landscape, reference, spec, runbook or other; `platforms` from `platform_scope`, or `claude-code` for `cc-native/` and `cc-community/` docs without one), and one edge per linked pair. The hub state comes from `doc_coverage.hub_filing`, the function the hub ratchet in `make check_coverage` also counts from, so a doc in no hub is shown as unfiled, exempt by rule (D6) or not hub content (README indexes, plans, research notes and example files) exactly as the check classifies it. The same corpus always gives byte-identical JSON, with no LLM involved. Link validity stays with lychee. The Pages deploy regenerates the JSON from `docs/` on every push to `main`, and the file is never committed, so it cannot drift. It is rendered at `/doc-graph.html` (`ui/doc-graph.html`, using the vendored vis-network): docs as dots coloured by top-level folder, topic hubs as diamonds, the hub index (`docs/_topics/README.md`) as a hollow star; the search box at the top of the side panel dims non-matching docs as you type and Enter zooms to the first match; the top bar shows the build metadata to the right of the theme picker; one checkbox per hub, one each for "Unfiled", "Exempt by rule" and "Not hub content" (each says on hover which rule puts a doc there), and "Select all" filter the graph; a click opens the doc on GitHub in a new tab.

**Build metadata:** every page shows the release version (`pyproject.toml`), last-modified date and commit link. The deploy writes `build.json` with `scripts/build-site-info.py` (pure logic in `pages_build.site_info`), and `ui/build-info.js` renders it.

**Live site:** <https://qte77.github.io/ai-agents-research/> — a branded EyeRest landing page (`index.html`) linking to the doc graph at `/doc-graph.html`.

### Published site (gh-pages)

The site applies the qte77 EyeRest brand (`qte77/qte77/brand/DESIGN.md`: zero-blue, warm umber/parchment), like the sibling repos `analyze-stock-kpi` and `paperverse`. Source lives in `ui/`:

| Path | Role |
|---|---|
| `ui/index.html` | Branded landing page (site root) |
| `ui/doc-graph.html` | Doc graph page; its JSON is built by the deploy |
| `ui/vendor/vis-network.min.js` | Self-hosted vis-network (the doc graph's renderer) — committed so the graph renders offline / without a CDN round-trip |
| `ui/style.css` | EyeRest design tokens + `@font-face` + layout |
| `ui/favicon.svg` | Adapted qte77 logo-mark |
| `ui/assets/fonts/*.woff2` | Self-hosted Inter + JetBrains Mono — committed (refresh with `make graph-fonts`); `@font-face` falls back to system-ui if absent |
| `scripts/pages_build.py` | Pure, unit-tested helpers — `site_info()` and `read_version()` for `build.json`; font helpers feed the fetch script |

**Deploy** is a GitHub Actions workflow (`.github/workflows/gh-pages.yaml`) using the Pages API — like the sibling repos `analyze-stock-kpi` and `paperverse` (no `gh-pages` branch). On every push to `main`, CI assembles `ui/` (with the committed fonts and vendored vis-network), builds the doc-graph JSON and `build.json`, and deploys. The repo's **Settings → Pages → Source** must be set to "GitHub Actions".

The landing page carries a **System / Light / Dark theme picker** (persisted to `localStorage`, no-flash, OS-following by default).

## Downstream Consumers

Research from this repository feeds directly into implementation repos:

| Downstream Repo | Consumes From | Key Docs |
|---|---|---|
| [cc-recursive-team-mode](https://github.com/qte77/cc-recursive-team-mode) | `docs/cc-native/agents-skills/`, `docs/cc-native/session-analysis/` | `CC-recursive-spawning-patterns.md`, session artifact schema docs |
| [coding-harness-eval](https://github.com/qte77/coding-harness-eval) | `docs/cc-native/comparisons/`, `docs/cc-native/features/`, `docs/non-cc/` | Agent feature matrices, invocation method analyses |
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
cc-recursive-team-mode / coding-harness-eval / multi-tasking-quality-benchmark
```

Human review is required at the triage → docs promotion step. Monitors surface content; researchers make adoption decisions.
