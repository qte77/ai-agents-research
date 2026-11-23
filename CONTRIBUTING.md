# Contributing to ai-agents-research

Documentation standards and conventions for research analysis documents — for any contributor, human or AI agent.

## Document Structure

Every analysis document (`CC-*-analysis.md`, `CC-*-reference.md`, etc.) follows this structure:

### 1. Frontmatter

```yaml
---
title: Descriptive Title
purpose: One-line purpose statement
created: YYYY-MM-DD
updated: YYYY-MM-DD
validated_links: YYYY-MM-DD
status: assess
---
```

Required keys:

- `title`, `purpose` (one sentence on one line, at most 200 characters, saying what the doc covers; detail goes in the body or on the `**Details:**` line; there is no separate `description:`)
- `created`, `updated` (date of last content edit), `validated_links` (date the URLs were last checked), all ISO `YYYY-MM-DD`
- `status` — the doc's lifecycle token (see §2); the single source of status, read by `make check_status` and the doc graph

Optional keys: `source` (the one primary URL the doc is based on; other sources go in the Sources section), `platform_scope` (see [platform_scope frontmatter](#platform_scope-frontmatter)), `test_run`.

Not in frontmatter (owner decision D5, plan 0015, 2026-11-21):

- `sources:` — sources belong in the Sources section at the end
- `description:` — use `purpose:`
- `release:`, `version:`, `license:`, `authority:` — release status, version and licence go on the `**Details:**` line (§2)
- `category:` — the filename suffix (`-landscape`, `-analysis`, `-reference`, …) already says it

**Frontmatter must be on line 1.** No HTML comments (`<!-- -->`) before the opening `---` — this breaks markdownlint's frontmatter parser and causes false MD041/MD003 errors.

### 2. Frontmatter status

Status lives only in the frontmatter `status:` field (#348). There is no body `**Status**:` badge; `make check_status` runs in strict mode and fails on one.

`status` says where the doc's subject stands for us, not what the vendor calls its release. Values (Technology Radar convention, plus three for docs that recommend nothing):

| Status | Meaning |
|---|---|
| `adopt` | Validated, recommended for use |
| `trial` | Worth pursuing, needs more validation |
| `assess` | Worth exploring, not yet validated |
| `hold` | Not recommended or deprecated |
| `research` | A paper or method; nothing to adopt |
| `reference` | Descriptive: a spec, index, runbook or requirements doc |
| `archived` | Retired; see [Archiving legacy content](#archiving-legacy-content) |

Plans (`docs/plans/`) use `draft`, `approved`, `done` or `superseded`, and only plans use them.

Release status, licence and version go on a `**Details:**` line right after the frontmatter, per surface where they differ (for example "preview on the web, GA in the CLI", which one token can't hold).

`make check_status` and `make check_frontmatter` reject any other token, including the older release and licence tokens (`generally-available`, `beta`, `open-source`, …).

### 3. Body

- **"What It Is"** section — brief description
- Domain-specific sections (implementation, configuration, comparison tables, etc.)
- MD013 (line length) is disabled globally in `.markdownlint.json` — no inline `<!-- markdownlint-disable MD013 -->` needed

### 4. Inline References

Use short reference-style links throughout the body:

```markdown
The [official env vars reference][env-vars] lists 80+ variables.
See the [monitoring docs][monitoring] for OTel configuration.
```

**Not** bare URLs in prose. Bare URLs are acceptable only in tables or code blocks.

### 5. Sources Section (End)

Every doc ends with a `## Sources` table (a `## References` section is accepted as equivalent) linking all references used:

```markdown
## Sources

| Source | Content |
|---|---|
| [CC env vars reference][env-vars] | Official complete list |
| [CC monitoring docs][monitoring] | OTel configuration and metrics |
| CC 2.1.83, Codespaces, 2026-03-27 | Runtime observation (no URL) |
```

Followed by reference-style link definitions:

```markdown
[env-vars]: https://code.claude.com/docs/en/env-vars
[monitoring]: https://code.claude.com/docs/en/monitoring-usage
```

### 6. Cross-References

Link to sibling docs with relative paths:

```markdown
Cross-ref: [CC-model-provider-configuration.md](CC-model-provider-configuration.md)
```

For docs in other subdirectories:

```markdown
Cross-ref: [CC-agent-teams-orchestration.md](../agents-skills/CC-agent-teams-orchestration.md)
```

## Source Citation Rules

- **Every factual claim** must be traceable to a source (URL, observation, or cross-ref)
- **First-party sources** (official docs, changelogs) take priority over third-party
- **Observations** include CC version, environment, and date: `CC 2.1.83, Codespaces, 2026-03-27`
- **Pricing and version-specific data** must note the access date — these change across model generations

## Research Workflow

- **Search before creating** — extend an existing doc on hit; create a new file only if there is zero coverage. Agents: prefer the **Grep**/**Glob**/**Read** tools over shell `grep`/`find`/`cat` for speed and lower token cost
- **Cross-verify counts and capabilities** against the upstream repo (README, source tree, lockfile via `gh api repos/<owner>/<repo>/contents/<path>`) — vendor marketing copy and short GitHub descriptions drift from reality
- **Soften or remove unverified claims** — explicit hedging beats unsourced numbers; "up to N" without a first-party source is not acceptable
- **Cite a version gate** when behavior is version-specific (e.g., `@anthropic-ai/claude-code@2.1.88, 2026-03-31`, `CC v2.1.96+`)
- **Shell tooling**: prefix shell calls with `rtk` (Rust Token Killer) when a shell call is genuinely needed — see `/workspaces/.claude-files/RTK.md`. Shell is a fallback, not the default
- **Dynamic / unparsable sources**: when WebFetch can't render a page (JS-SPA, TLS- or bot-blocked) or parse a document (PDF/Office/image), escalate to the estate tools via `uv run --directory <clone>` (runs in the clone's own venv — no poison): [polyfetch-scrape](https://github.com/qte77/polyfetch-scrape) to **fetch** dynamic/blocked pages (see its `USING.md`), and [doc-pipeline-engine](https://github.com/qte77/doc-pipeline-engine) to **process** documents to text/markdown (offline `local` leg; one-off `uv sync --extra extract`)

## Directory Structure

```text
ai-agents-research/
  README.md                            # Repo overview, contents table, related repos
  CONTRIBUTING.md                      # This file — doc standards
  docs/
    cc-native/                         # Anthropic-native CC features (primary focus)
      README.md                        # Index with doc counts per subdirectory
      agents-skills/README.md          # Agent teams, spawning, skills, Ralph
      sessions/README.md               # Session lifecycle, cost, keepalive, headless
      sandboxing/README.md             # Sandbox internals, Codespaces friction, platforms
      ci-remote/README.md              # GHA, cloud sessions, remote access, web auth
      configuration/README.md          # Hooks, model config, env vars, tools, fast/bash mode
      context-memory/README.md         # Extended context, memory, prompt caching, llms.txt
      plugins-ecosystem/README.md      # Official plugins, connectors, Cowork, packaging
      model-internals/README.md        # Model-level interpretability research
      examples/                        # Working config/script examples
    non-cc/                            # Non-CC agents (JetBrains Air, DeerFlow, etc.)
      <section>/                       # 9 subdirs mirroring non-cc/README.md sections: orchestrators, agents, coding-agents, knowledge-management, reference, context-memory, infrastructure, frameworks, protocols
    cc-community/                      # Community skills, plugins, tooling, CLAUDE.md patterns
    sdlc-lcm/                          # SDLC/lifecycle management specs
    _topics/                           # Cross-subject hub indexes (list in _topics/README.md); pointers only
    learnings/                         # Cross-repo compound learnings hub (CRLA write-back target)
    research/                          # Auto-generated cumulative rxiv agentic-AI paper index
    plans/                             # Plan/design docs (durable plan-mode output; backlog = GitHub Issues)
    archive/                           # Retired/superseded docs (excluded from link-checking)
  changelog.d/                         # scriv changelog fragments (collected on release)
  scripts/                             # Site-info + font-fetch helpers (stdlib-only); cc-multi-account.sh (CLAUDE_CONFIG_DIR profiles)
  ui/                                  # Branded gh-pages site (index.html, doc-graph.html, assets)
  triage/                              # Auto-generated monitor outputs
  .github/                             # CI automation (monitors, scripts, templates)
    state/                             # Per-monitor fingerprint files (committed)
```

### Classification: cc-community vs non-cc

Many tools work with multiple AI agents/editors, not just Claude Code. The
placement decision is based on **research interest**, not exclusivity:

| Directory | Placement criterion | Example |
|---|---|---|
| `cc-community/` | The CC integration surface is the primary research interest — how the tool plugs into CC via hooks, MCP, plugins, slash commands | Serena (an MCP server any MCP client can use, but its CC integration is the analysis focus) |
| `non-cc/` | The tool's architecture or capabilities are the primary research subject — CC is incidental or one of many providers | Hermes Agent (supports Claude via API, but self-improving skill loop is the analysis focus) |

When a tool spans both, place it where the **deeper analysis** lives and
cross-reference from the other directory.

#### platform_scope frontmatter

For tools that support multiple platforms, add a `platform_scope` field to
frontmatter to make cross-platform reach explicit:

```yaml
platform_scope: [claude-code, cursor, windsurf, zed, opencode, antigravity]
```

This prevents misreading a `cc-community` placement as "CC-exclusive."

### Index maintenance

- Every content doc is linked from its folder's README index: the nearest `README.md` above it inside `docs/` (a `non-cc/<section>/` doc is indexed by `non-cc/README.md`), and from at least one other doc or repo-root file. `make check_coverage` enforces both in CI, and also fails on a doc-to-doc link whose `#fragment` matches no heading in the target (rename a heading → fix its inbound anchors)
- Not covered: the README indexes themselves, `docs/` root files (no folder index; still need an inbound link), `cc-native/examples/` (example files) and `docs/archive/`
- Every content doc is also in at least one topic hub ([`docs/_topics/README.md`](docs/_topics/README.md) lists them), one row per doc and section. Exempt (owner decision D6): `docs/` root files, single-product profiles in `non-cc/{coding-agents,agents,orchestrators,reference}/`, single-product `non-cc/frameworks/*-analysis.md`, specs (`*-spec.md`) and runbooks (`*-runbook.md`); landscapes never are by rule. The owner's X2 list (2026-11-22, `_OWNER_EXEMPT` in `doc_coverage.py`) adds `docs/learnings/`, the Claude Code reference indexes, the agent-substrate pair and two single-case analyses. `make check_coverage` fails on duplicate hub rows and when more docs than `MAX_UNHUBBED` (a ratchet in the `Makefile` that only goes down) are in no hub
- When adding a `cc-native/` doc, update **both** the subdirectory README and `cc-native/README.md` (doc count); `cc-community/` follows the same standard
- `docs/archive/` holds retired/superseded docs — excluded from link-checking, not content candidates

## Naming Convention

- Analysis docs: `CC-<topic>-analysis.md`
- Reference docs: `CC-<topic>-reference.md`
- Research docs: `CC-<topic>-research.md`
- Landscape docs: `CC-<topic>-landscape.md`
- Gotchas/friction: `CC-<topic>-gotchas.md`, `CC-<topic>-friction.md`

## Anti-Patterns

- `sources:` in YAML frontmatter — use Sources section instead
- Bare URLs in prose — use reference-style links
- Duplicating content across docs — cross-reference the authoritative doc
- Defining a term another doc already owns — link its owner from [docs/glossary.md](docs/glossary.md); expand an abbreviation on first use or link the glossary (`make check_coverage` fails if a doc never expands it and doesn't link the glossary)
- Missing Sources section — every doc must cite its sources (a `## Sources` table, or an equivalent `## References` section)
- Stale `validated_links` dates — re-check URLs when updating findings

## Auto-generated content

The `triage/` directory contains **auto-generated monitor outputs** (changelog triage, community triage, outage archive). It is populated exclusively by the GitHub Actions monitors in `.github/workflows/` and is **not a source of hand-written analysis**. Do not treat triage files as content candidates for promotion into `docs/` — findings of interest should be re-researched from their first-party sources and written as new analysis docs under the appropriate `docs/` subdirectory. The directory is intentionally excluded from link checking via `lychee.toml`.

The `docs/research/rxiv-agentic-papers.md` index is generated by the `rxiv-paper-eval` pipeline. **Run `rxiv-paper-eval` dispatches one at a time, and merge each triage PR before the next run.** The triage branch is `chore/rxiv-paper-triage-<server>-<year>-W<week>-<date>`, so runs for different weeks no longer collide on a branch name, but every triage PR regenerates the whole index and state file from `main`; two open triage PRs conflict. Rerunning the same week on the same day still reuses the branch. Tracked upstream: [gha-rxiv-paper-eval#71](https://github.com/qte77/gha-rxiv-paper-eval/issues/71).

**Fold-in rule for relevant papers.** Consistent with the paragraph above, a triage report lists leads, never text to promote. Before a triage PR merges, give each paper one outcome: *cited* (already in `docs/`), *routed* (its arXiv ID added as a lead to the source-map entry of the open plan row whose topic it fits, at most four per row, preferring benchmarks, measurements and failure studies over method papers), or *dropped* with a class reason (domain application, training method, model report, past the row's cap, no row topic). Papers that fit a row already shipped go to one follow-up row. The lane that works a row folds its routed papers when the row ships, re-reading each arXiv page and citing that, never the triage summary. The plan's source map holds the routed IDs; the per-paper outcome table is a local triage note, not a repo file.

## Maintenance

| Trigger | Required action |
|---|---|
| Content change | Bump `updated:` |
| Lychee re-run on the file | Bump `validated_links:` |
| Vendor releases new version affecting documented behavior | Re-fetch first-party page, update version gate, bump `updated:` |
| External URL 404 / redirect | Replace with current canonical URL; do not add to `lychee.toml` exclude unless the host is bot-blocking (403/418) |
| Vendor renames a feature | Replace in-place; add a one-line `Note:` only if the old name is widely cited externally |

### Pruning entries (well-known, performance-optimised filter)

Owner rule D8 (plan 0015, approved 2026-11-21). A catalog entry in a landscape stays only if all three hold:

1. **A usable artifact exists**: code, a package, model weights, or a product you can sign up for.
2. **It is alive**: not archived, with a release or commit in the last 12 months.
3. **It is adopted or proven**: a standards body, named independent users, or about 1,000+ GitHub stars; or a
   first-party measured benefit.

A widely adopted tool that has gone stale keeps one dated line (what it is, and its last activity with an
as-of date). An entry that fails moves to a `## Not included` section at the end of the owning landscape,
just before `## Sources`: a table `| Name | Reason | Date | Link |`, the reason short and sourced (for example
"55 stars; last push 2025-09-17 (`gh api` 2026-11-21)"). Remove the name's other mentions in the corpus in the
same PR. A whole doc that fails is archived (below), and only with the owner's approval.

### Archiving legacy content

When a doc is superseded, **archive — do not delete**. Pattern (see commits `#105`, `#120`, `#121`):

1. Set frontmatter `status: archived` and add the archive date
2. Move the file to `docs/archive/<original-subdir>/`
3. Add a banner immediately after frontmatter: `> **Status: archived** on YYYY-MM-DD. Preserved for historical context. See [<replacement>](path) for current analyses.`
4. Rewrite incoming refs to point at the replacement (or remove if dead)

`docs/archive/` is in `lychee.toml` `exclude_path` — archived files do not gate CI.

## Local development

Doc linting is wired into the top-level `Makefile`. All tools install user-locally with zero sudo.

```bash
make setup_all   # install lychee, Node.js (user-local), markdownlint-cli2
make lint        # run lychee + markdownlint-cli2 over the full repo
make autofix     # mechanical markdownlint --fix pass
make test        # unit tests for src/ + .github/scripts/lib/ modules (stdlib unittest)
make graph-data  # doc graph for the site (docs with their topic hubs, one edge per linked pair) into ui/doc-graph.json — no LLM
make census      # rubric evidence matrix from every scored row's subject: tag (8 subjects × 6 properties) — no LLM
make reconcile   # newest plan's remaining-work rows vs live PR/issue state (needs an authenticated gh)
make help        # list all recipes grouped by section
```

Run `make lint` against any PR that touches docs before requesting review. `lychee` reads `lychee.toml`; `markdownlint-cli2` reads `.markdownlint.json`.

**Doc graph:** the Pages deploy rebuilds the doc graph from `docs/` on every push to `main`; `make graph-data` builds the same JSON locally. Details: [architecture.md § Doc Graph and Site](docs/architecture.md#doc-graph-and-site).

## Commit & PR

- **Conventional commits** per `.gitmessage`: `docs:`, `chore:`, `ci:`, `feat:`, `fix:`, …
- **Split commits by topic** within a single PR — content additions, lint cleanup, CI/config changes each get their own commit
- **Branch naming**: `<type>/<short-slug>` (e.g., `docs/otel-and-ag-ui-research`, `ci/cache-lychee-binary`)
- **Merge policy**: squash-merge to main; delete the remote branch on merge. Squash breaks ancestry, so the local branch must be force-deleted (`git branch -D`) afterward
- **Track follow-up work as GitHub issues**, not in-doc TODOs (e.g., `#123` for the `gha-md-lychee` extraction)
- **Working on a tool you write about?** Great, we'd love your input. Just mention in the PR if you work for, or are paid by, the vendor. The most helpful contributions are an issue suggesting coverage, or a PR that adds a row or section to an existing comparison, backed by first-party sources. Please don't retitle or re-index existing docs around a single tool, or set a doc's `status`. We keep those neutral and decide them ourselves. When we adopt your idea, a maintainer writes it up in the repo's own words and verifies it at source, and we credit your PR or issue by link.
- **Signed commits, please.** `main` only accepts signed commits, so a branch with unsigned ones can't be merged. GitHub's guide to [signing commits][gh-signing] shows how.

[gh-signing]: https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits

## Release & Changelog

Releases are **operator-driven** and the CHANGELOG is managed with
[scriv](https://scriv.readthedocs.io/) fragments (the `changelog.d/` workflow
deferred in #217). Version config lives in `pyproject.toml` — `[tool.bumpversion]`
holds the version single-source-of-truth, `[tool.scriv]` configures fragments. The
tooling runs ephemerally (`pip`/`uvx` in the reusable CI workflow, `pipx` in the Makefile recipes); this repo
ships no Python package, so there is no venv or lockfile.

### Per-PR: add a changelog fragment

Instead of editing `CHANGELOG.md` directly, add a fragment:

```bash
make changelog_new        # creates + stages changelog.d/<timestamp>_<branch>.md
```

Edit the generated file — uncomment the relevant category (`Added`, `Changed`,
`Fixed`, …) and write the entry in the same `` `path`: description `` style as
existing CHANGELOG entries. `make changelog_preview` shows the assembled result.

### Cutting a release (maintainer)

1. **Bump** — run the `bump` workflow (Actions → Run workflow → choose
   `major`/`minor`/`patch`). It bumps `current_version`, collects `changelog.d/`
   fragments into a dated `## [X.Y.Z]` CHANGELOG section, and opens a release PR
   whose commit GitHub signs, so it satisfies `main`'s signed-commit rule.
2. **Merge** — squash-merge the release PR once its checks pass. PRs opened by the
   Actions token start no workflows on their own, so a maintainer may need to
   approve the waiting Lint run (and re-run a check that never reports) until the
   App-token setup in qte77/.github#70 is in place.
3. **Tag and publish** — `release` fires on the `pyproject.toml` change, pushes the
   annotated `vX.Y.Z` tag against the merge commit, and publishes the GitHub Release
   with notes from the matching CHANGELOG section, in the same run.

`publish-release` is a manual fallback that publishes a Release for an existing tag
that has none. `bump.yaml`, `release.yaml` and `publish-release.yaml` are thin callers
of the estate's reusable workflows in `qte77/.github`, pinned to a commit SHA with a
date comment; refresh the pin by hand when the reusable workflows change.

> **Transition note:** `## [Unreleased]` content predating this flow is collected
> into the first tagged release (`v0.4.0`); from `v0.5.0` onward, use fragments.
