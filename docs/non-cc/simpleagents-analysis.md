---
title: SimpleAgents Analysis
source: https://github.com/CraftsMan-Labs/SimpleAgents
purpose: Architecture analysis of SimpleAgents — Rust-first LLM agent framework with polyglot bindings and YAML workflow orchestration.
created: 2026-03-29
updated: 2026-03-29
validated_links: 2026-03-29
---

**Status**: Assess

## What It Is

Rust-first framework for building LLM agent applications with a unified provider client (OpenAI, Anthropic, OpenRouter), YAML-driven workflow authoring, and polyglot bindings ([repo][repo]).

- **Stack**: Rust (edition 2021, MSRV 1.75), 13 crates in workspace
- **Version**: 0.2.31 | **License**: Apache-2.0 | **Stars**: 18
- **Bindings**: Python (PyO3), Node.js (N-API), Go (C FFI), WASM (wasm-bindgen)
- **Docs**: VitePress at `docs.simpleagents.craftsmanlabs.net`

## Architecture

| Crate | Role |
|---|---|
| `simple-agent-type` | Canonical request/response types and traits |
| `simple-agents-core` | Unified client orchestration |
| `simple-agents-providers` | Provider adapters (OpenAI, Anthropic, OpenRouter) |
| `simple-agents-router` | Routing: round-robin, latency, cost, fallback, circuit-breaker |
| `simple-agents-cache` | In-memory TTL/eviction cache |
| `simple-agents-healing` | JSON parsing coercion and schema normalization |
| `simple-agents-workflow` | YAML workflow IR, runtime, validation, tracing |
| `simple-agents-workflow-workers` | gRPC worker contract and client pool |
| `simple-agents-cli` | CLI (chat, complete, benchmark, workflow) |
| `simple-agents-ffi` | C ABI surface |
| `simple-agents-napi` | Node.js N-API binding |
| `simple-agents-py` | Python binding (PyO3) |
| `simple-agents-macros` | Procedural macros |

Polyglot workers in `workers/go/`, `workers/python/`, `workers/typescript/`.

## Key Differentiators

- **Rust-first with generated bindings** — single source of truth, not separate implementations per language
- **YAML workflow IR** with validation, tracing, and replay
- **Built-in resilience** — circuit breakers, fallback routing, healing/coercion
- **gRPC worker contract** — polyglot workflow steps (Go, Python, TypeScript workers)
- **WASM binding** — browser-native execution

## Known Gaps

| Issue | Detail |
|---|---|
| [#25][gh-25] | Skills system for coding agents — requested but unbuilt |
| [#24][gh-24] | Parallel DAG execution for guardrails and deep research |
| [#27][gh-27] | Multimodal support (images/video) — currently text-only |
| [#33][gh-33] | Email example shows unrelated content |
| [#30][gh-30] | Runtime error message mislabels provider |
| [#32][gh-32] | Example switching leaks stale chat/error state |
| No GitHub Releases | v0.2.31 in Cargo.toml but 0 tagged releases |
| Bus factor of 1 | ~353 commits from single contributor |

## Positioning

Comparable to LangChain/LlamaIndex (Python-first) and Vercel AI SDK (TypeScript-first), but Rust-first with polyglot bindings. More infrastructure/SDK layer than opinionated agent framework. The "SimpleAgents" name understates scope — it is a comprehensive LLM orchestration toolkit.

## Sources

[repo]: https://github.com/CraftsMan-Labs/SimpleAgents
[gh-25]: https://github.com/CraftsMan-Labs/SimpleAgents/issues/25
[gh-24]: https://github.com/CraftsMan-Labs/SimpleAgents/issues/24
[gh-27]: https://github.com/CraftsMan-Labs/SimpleAgents/issues/27
[gh-33]: https://github.com/CraftsMan-Labs/SimpleAgents/issues/33
[gh-30]: https://github.com/CraftsMan-Labs/SimpleAgents/issues/30
[gh-32]: https://github.com/CraftsMan-Labs/SimpleAgents/issues/32
