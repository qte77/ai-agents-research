# Contributing to ai-agents-research

Documentation standards and conventions for research analysis documents.

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
---
```

- `validated_links` — date when URLs in the doc were last checked
- `updated` — date of last content edit
- **No `sources:` key in frontmatter** — sources belong in the Sources section at the end

Optional fields: `source` (primary URL the doc is based on), `category`, `test_run`.

**Frontmatter must be on line 1.** No HTML comments (`<!-- -->`) before the opening `---` — this breaks markdownlint's frontmatter parser and causes false MD041/MD003 errors.

### 2. Status Badge

Immediately after frontmatter:

```markdown
**Status**: Adopt
```

Values (Technology Radar convention):

| Status | Meaning |
|---|---|
| **Adopt** | Validated, recommended for use |
| **Trial** | Worth pursuing, needs more validation |
| **Assess** | Worth exploring, not yet validated |
| **Hold** | Not recommended or deprecated |

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

Every doc ends with a `## Sources` table linking all references used:

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
      examples/                        # Working config/script examples
    non-cc/                            # Non-CC agents (JetBrains Air, DeerFlow, etc.)
    cc-community/                      # Community skills, plugins, tooling, CLAUDE.md patterns
    sdlc-lcm/                          # SDLC/lifecycle management specs
    todo/                              # Agents-eval era docs pending review (analysis, landscape, best-practices, research)
  triage/                              # Auto-generated monitor outputs
  .github/                             # CI automation (monitors, scripts, templates)
```

### Classification: cc-community vs non-cc

Many tools work with multiple AI agents/editors, not just Claude Code. The
placement decision is based on **research interest**, not exclusivity:

| Directory | Placement criterion | Example |
|---|---|---|
| `cc-community/` | The CC integration surface is the primary research interest — how the tool plugs into CC via hooks, MCP, plugins, slash commands | Graphify (5 platforms, but CC hook/MCP integration is the analysis focus) |
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

- Each `cc-native/` subdirectory has a `README.md` index with a doc table
- When adding a doc, update **both** the subdirectory README and `cc-native/README.md` (doc count)
- `cc-community/` follows the same standard as `cc-native/`
- `docs/todo/` contains Agents-eval era docs pending review — not yet standardized
- Other directories (`sdlc-lcm/`, `non-cc/`) follow their own conventions

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
- Missing Sources section — every doc must cite its sources
- Stale `validated_links` dates — re-check URLs when updating findings

## Auto-generated content

The `triage/` directory contains **auto-generated monitor outputs** (changelog triage, community triage, outage archive). It is populated exclusively by the GitHub Actions monitors in `.github/workflows/` and is **not a source of hand-written analysis**. Do not treat triage files as content candidates for promotion into `docs/` — findings of interest should be re-researched from their first-party sources and written as new analysis docs under the appropriate `docs/` subdirectory. The directory is intentionally excluded from link checking via `lychee.toml`.

## Local development

Doc linting is wired into the top-level `Makefile`. All tools install user-locally with zero sudo.

```bash
make setup_all   # install lychee, Node.js (user-local), markdownlint-cli2
make lint        # run lychee + markdownlint-cli2 over the full repo
make autofix     # mechanical markdownlint --fix pass
make help        # list all recipes grouped by section
```

Run `make lint` against any PR that touches docs before requesting review. `lychee` reads `lychee.toml`; `markdownlint-cli2` reads `.markdownlint.json`.
