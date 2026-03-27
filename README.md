# ai-agents-research

> Field research and feature analysis for AI coding agents — from sandboxing internals to agent orchestration.

## Why

Understand how Claude Code works under the hood so you can make informed adopt/defer/skip decisions before building production systems with it.

## What

Standalone deep-dive analyses of CC features, each following a consistent format:
**What it is** → **How it works** → **Adoption decision** → **Action items**

## Contents

| Directory | What's there |
|---|---|
| [`docs/cc-native/`](docs/cc-native/) | Anthropic-native features: agents/skills, CI/sandboxing, context/memory, configuration, plugins/ecosystem, MCP connectors |
| [`docs/non-cc/`](docs/non-cc/) | Non-CC agents and orchestrators: JetBrains Air, agent-era/devteam |
| [`docs/cc-community/`](docs/cc-community/) | Community skills, plugins, tooling, and domain-specific CLAUDE.md patterns |
| [`docs/sdlc-lcm/`](docs/sdlc-lcm/) | SDLC/lifecycle management specs, agentic SDLC patterns, OSS ALM landscape |
| [`docs/todo/`](docs/todo/) | Agents-eval era docs (analysis, landscape, best-practices, research) — pending review and reorganization |
| [`docs/learnings/`](docs/learnings/) | Cross-repo compound learnings hub — recurring patterns from live development across the qte77 ecosystem |
| [`triage/`](triage/) | Auto-generated monitor outputs: outage archive, changelog triage, community triage |
| [`.github/`](.github/README.md) | CI automation: monitors, scripts, templates — see [.github/README.md](.github/README.md) |

## How it stays current

Three automated monitors poll external sources on cron and open triage PRs when new content is found. See [`.github/README.md`](.github/README.md) for details.

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

[MIT](LICENSE)
