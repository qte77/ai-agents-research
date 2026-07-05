# ai-agents-research

> Field research and feature analysis for AI coding agents — sandboxing, orchestration, plugins, community tooling, SDLC patterns.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Changelog](https://img.shields.io/badge/changelog-Keep_a_Changelog-blue.svg)](CHANGELOG.md)
[![Lint](https://github.com/qte77/ai-agents-research/actions/workflows/lint.yaml/badge.svg)](https://github.com/qte77/ai-agents-research/actions/workflows/lint.yaml)

## What

A continuously-updated research catalog for making **adopt / defer / skip** decisions about AI
coding agents and their ecosystems before building production systems on them. Every analysis
follows one structure: **What it is → How it works → Adoption decision → Action items**.

- **Claude Code (Anthropic-native)** — agents/skills, CI/sandboxing, context/memory, configuration, plugins, MCP connectors
- **Non-CC agents & infrastructure** — JetBrains Air, DeerFlow, Goose, Codex, Devin, frameworks, orchestrators
- **Community ecosystem** — skills, plugins, tooling, domain-specific CLAUDE.md patterns
- **SDLC / lifecycle management** — agentic SDLC patterns, OSS ALM landscape
- **Cross-repo learnings** and an auto-generated cumulative index of agentic-AI papers
- **Self-currency** — four cron monitors open triage PRs when upstream sources change

Full directory map and the monitor pipeline live in [`docs/architecture.md`](docs/architecture.md); the research goals and user stories are in [`docs/UserStory.md`](docs/UserStory.md); browse the analyses under [`docs/`](docs/).

## How

Doc tooling installs user-locally (zero sudo, into `~/.local/bin`) and runs through the `Makefile`:

```bash
make setup_all   # lychee + Node.js + markdownlint-cli2 + actionlint + shellcheck
make lint        # links (lychee) + markdown (markdownlint-cli2) + actions (actionlint)
make test        # stdlib unit tests for scripts/ + .github/scripts/lib/ modules
make help        # all recipes, grouped by section
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for document standards and [`CHANGELOG.md`](CHANGELOG.md) for history.

## Why

Make informed decisions about coding agents before committing production systems to them. The
catalog tracks Claude Code, JetBrains Air, DeerFlow, Goose, Codex, Devin and others — plus the
surrounding plugins, observability, SDLC patterns, and cross-repo learnings distilled from live
development across the qte77 ecosystem.

## Refs

- [An Open Agentic Coding Harness](https://qte77.github.io/open-agentic-coding-harness/) — the write-up this catalog feeds
- [cc-recursive-team-mode](https://github.com/qte77/cc-recursive-team-mode) — recursive CC subprocess spawning, session-artifact research
- [coding-agent-eval](https://github.com/qte77/coding-agent-eval) — hands-off coding-agent comparison harness
- [multi-tasking-quality-benchmark](https://github.com/qte77/multi-tasking-quality-benchmark) — WakaTime activity vs code-quality correlation
- [Agents-eval](https://github.com/qte77/Agents-eval) — origin: these analyses began here, to inform a multi-agent evaluation framework

## License

[Apache-2.0](LICENSE)
