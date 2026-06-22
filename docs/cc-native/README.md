# CC-Native Features

Deep-dive analyses of Anthropic-native Claude Code features and internals.

## Subdirectories

| Directory | Coverage | Docs |
|-----------|----------|------|
| [agents-skills/](agents-skills/) | Agent teams, recursive spawning, skills adoption, Ralph, dynamic workflows | 8 |
| [sessions/](sessions/) | Session lifecycle, cost analysis, keepalive, headless mode, error messages | 7 |
| [sandboxing/](sandboxing/) | Filesystem/network sandbox, Codespaces friction, platform comparison, permission bypass | 5 |
| [ci-remote/](ci-remote/) | GitHub Actions, cloud sessions, remote access/control, web auth, version pinning, monitoring | 8 |
| [configuration/](configuration/) | Hooks, model/provider config, fast/bash mode, loop/cron, env vars, tools, binary + IDE/stream-json internals, models reference, changelog, visuals | 14 |
| [context-memory/](context-memory/) | Extended context, memory system, llms.txt, prompt caching | 4 |
| [plugins-ecosystem/](plugins-ecosystem/) | Official plugins, connectors, Cowork, packaging, web scraping | 10 |
| [model-internals/](model-internals/) | Emotion vectors, interpretability, safety classifiers, alignment steering, first-party research index | 2 |

## Reference

| Document | Coverage |
|----------|----------|
| [CC-first-party-docs-index.md](CC-first-party-docs-index.md) | Canonical Anthropic URLs for CC, Agent SDK, API, hooks, and best practices |
