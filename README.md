# ai-agents-research

> Project overview — start here. Audience: any contributor or AI agent.
>
> Field research and feature analysis for AI coding agents — from sandboxing internals to agent orchestration.

## Why

Understand how Claude Code works under the hood so you can make informed adopt/defer/skip decisions before building production systems with it.

## What

Standalone deep-dive analyses of CC features, each following a consistent format:
**What it is** → **How it works** → **Adoption decision** → **Action items**

## Contents

| Directory | What's there |
|---|---|
| [`docs/cc-native/`](docs/cc-native/) | Anthropic-native features: agents/skills, CI/sandboxing, context/memory, configuration, plugins/ecosystem, model-internals, MCP connectors |
| [`docs/non-cc/`](docs/non-cc/) | Non-CC agents, orchestrators, and infrastructure: JetBrains Air, DeerFlow, Goose, Feynman, Hermes Agent, Rowboat, InsForge, GoClaw, and more |
| [`docs/cc-community/`](docs/cc-community/) | Community skills, plugins, tooling (16 tools), and domain-specific CLAUDE.md patterns |
| [`docs/sdlc-lcm/`](docs/sdlc-lcm/) | SDLC/lifecycle management specs, agentic SDLC patterns, OSS ALM landscape |
| [`docs/archive/`](docs/archive/) | Agents-eval era docs retained for reference (frameworks/infrastructure, evaluation/data resources, further reading, adoption plans) |
| [`docs/learnings/`](docs/learnings/) | Cross-repo compound learnings hub — recurring patterns from live development across the qte77 ecosystem |
| [`triage/`](triage/) | Auto-generated monitor outputs: outage archive, changelog triage, community triage, rxiv paper triage |
| [`.github/`](.github/) | Monitor workflows, scripts, composite actions, state files |

## How it stays current

Four cron-driven monitors open triage PRs against this repo whenever upstream content changes:

| Monitor | Source | Schedule | Output |
|---|---|---|---|
| CC status | Anthropic status page | Mon 09:00 UTC | `triage/status-monitor/` |
| CC changelog + native sources | CC release notes + GitHub issues/discussions + Anthropic blog | Mon 09:00 UTC | `triage/cc-changelog/` |
| Community | claudelog, awesome-* repos, Reddit, X | Mon 10:00 UTC | `triage/community/` |
| ArXiv paper eval | `qte77/gha-rxiv-feed-action` CSV → LLM relevance filter | Tue 09:00 UTC | `triage/rxiv/` |

Each monitor fingerprints its output and skips PR creation when content hasn't changed since the last emission. See [`docs/architecture.md`](docs/architecture.md) for the full pipeline.

## Local development

`Makefile` installs all tooling user-locally with zero sudo (`~/.local/bin`):

```bash
make setup_all   # lychee + Node.js + markdownlint-cli2 + actionlint
make lint        # link check (lychee) + markdown (markdownlint-cli2) + action (actionlint)
make autofix     # mechanical markdownlint --fix pass
make help        # all recipes grouped by section
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for document standards and [`CHANGELOG.md`](CHANGELOG.md) for release history.

## Related Repos

Research from this repository feeds into these downstream implementation repos:

| Repo | Purpose | Consumes |
|---|---|---|
| [cc-recursive-team-mode](https://github.com/qte77/cc-recursive-team-mode) | CLAUDECODE guard clearing, recursive CC subprocess spawning | CC spawning patterns, session artifact research |
| [coding-agent-eval](https://github.com/qte77/coding-agent-eval) | Hands-off coding agent comparison harness | Agent feature matrices, invocation methods |
| [multi-tasking-quality-benchmark](https://github.com/qte77/multi-tasking-quality-benchmark) | WakaTime activity vs code quality correlation | Quality metric methodology |

## Origin

These analyses were originally produced as part of [Agents-eval](https://github.com/qte77/Agents-eval) to inform adoption decisions for a multi-agent evaluation framework built on Claude Code.

## License

[Apache-2.0](LICENSE)
