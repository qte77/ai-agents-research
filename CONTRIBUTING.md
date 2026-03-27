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
- Use `<!-- markdownlint-disable MD013 -->` around wide tables

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
      ci-execution/README.md           # Sandboxing, GHA, cloud, print mode, cost
      configuration/README.md          # Hooks, model config, env vars, fast/bash mode
      context-memory/README.md         # Extended context, memory, caching, llms.txt
      plugins-ecosystem/README.md      # Official plugins, connectors, Cowork, packaging
      examples/                        # Working config/script examples
    non-cc/                            # Non-CC agents (JetBrains Air, DeerFlow, etc.)
    cc-community/                      # Community skills, plugins, tooling, CLAUDE.md patterns
    sdlc-lcm/                          # SDLC/lifecycle management specs
    analysis/                          # Benchmarks, providers, security governance
    landscape/                         # Eval metrics, frameworks, observability
    best-practices/                    # MAS design and security
    research/                          # 263+ papers, cross-framework convergence
  triage/                              # Auto-generated monitor outputs
  .github/                             # CI automation (monitors, scripts, templates)
```

### Index maintenance

- Each `cc-native/` subdirectory has a `README.md` index with a doc table
- When adding a doc, update **both** the subdirectory README and `cc-native/README.md` (doc count)
- `cc-community/` follows the same standard as `cc-native/`
- Other directories (`analysis/`, `landscape/`, `sdlc-lcm/`, `research/`, `best-practices/`) follow their own conventions

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
