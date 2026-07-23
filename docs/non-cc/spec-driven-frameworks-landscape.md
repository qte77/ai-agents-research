---
title: Spec-Driven Frameworks — Landscape
purpose: Comparison of spec-driven development (SDD) frameworks — GitHub Spec-Kit, OpenSpec, BMAD-METHOD, Agent-OS, Kiro, Tessl, AB Method — the standalone deep-dive behind the synthesis entry in the agentic-engineering disciplines landscape.
category: landscape
created: 2026-06-27
updated: 2026-07-23
validated_links: 2026-07-23
---

**Status**: Research (informational)

## What It Is

By 2026 every major coding tool shipped a **spec-driven development (SDD)** flavor: a machine-readable spec becomes the agent's source of truth, and human review shifts from reviewing code to reviewing the spec. This is the standalone comparison behind the synthesis-level §3 table in [agentic-engineering-disciplines-landscape.md](../sdlc-lcm/agentic-engineering-disciplines-landscape.md). Stars via `gh api`, 2026-06-27.

## Frameworks

| Framework | Stars | License | Loop | Distinctive |
|---|---|---|---|---|
| [github/spec-kit][spec-kit] | 115.9K | MIT | Spec → Plan → Tasks → Implement | 30+ agent integrations, 70+ extensions; "intent is the source of truth" |
| [Fission-AI/OpenSpec][openspec] | 57.1K | MIT | Proposal → Apply → Archive | change-proposal centric; no MCP/keys required |
| [bmadcode/BMAD-METHOD][bmad] | 49.8K | MIT | multi-agent planning → context-engineered dev | role agents (Analyst / PM / Architect) author the spec |
| [buildermethods/agent-os][agent-os] | 5.0K | MIT | MCP context-injection layer | composes with any SDD framework rather than replacing it |
| [kirodotdev/Kiro][kiro-repo] | 3.9K | proprietary | requirements → design → tasks "waves" | full IDE; spec phase is mandatory — see [kiro-analysis.md](kiro-analysis.md) |
| Tessl (`tile`) | ~41 | MIT | "spec-as-source" | the spec, not the code, is the maintained artifact; main framework closed-beta |
| [ayoubben18/ab-method][ab-method] | 180 | MIT | grill → roadmap → tasks → missions (TDD) | fractal structure; opt-in-silent critic agents bracket implementation; dual-runtime CC + Codex (v3.7.1; stars via `gh api`, 2026-07-23) |

## How they differ

- **Spec-Kit / OpenSpec** are the two large OSS frameworks — Spec-Kit is the broadest (multi-agent, extension ecosystem), OpenSpec is leaner (proposal → apply → archive, no keys).
- **BMAD** front-loads multi-agent *planning* (role agents draft the spec) before context-engineered execution.
- **Agent-OS** is a *layer*, not a framework — an MCP context-injection shim that pairs with the others.
- **Kiro** bakes SDD into a full IDE (the spec phase is mandatory) — covered in depth in its own analysis.
- **Tessl** pushes "spec-as-source" furthest (the spec is the maintained artifact, code is regenerated), but the main framework is closed-beta.
- **AB Method** is the lightweight dual-runtime sibling: `npx ab-method` installs into `.claude/` (CC slash commands) *and* `.agents/` (Codex `ab-*` skills). No generated spec docs — "the test is the spec"; plans are grounded in `UBIQUITOUS_LANGUAGE.md`/`CONTEXT.md`, missions are one-line tracker entries, and four critic skills (`critique-plan`, `reconcile-roadmap`, `review-implementation` with three parallel critics, `sync-architecture`) gate each layer. Runtime-adaptive: nests subagents on CC (verified two levels), stays flat on Codex (`spawn_agent` can't nest).

## Where SDD sits

SDD is the *what* (machine-readable spec → plan → tasks → implement); **EDD** (eval-driven development) is the *how-to-verify*. Together they bound a non-deterministic agent — SDD constrains the input, EDD constrains the output. See the disciplines landscape for the full "-engineering" / "-driven-development" stack.

## Cross-References

- [agentic-engineering-disciplines-landscape.md](../sdlc-lcm/agentic-engineering-disciplines-landscape.md) — the §3 synthesis entry this doc expands; the full disciplines + methodologies stack
- [kiro-analysis.md](kiro-analysis.md) — Kiro's spec-driven IDE in depth

## Sources

| Source | Content |
|---|---|
| [github/spec-kit][spec-kit] · [OpenSpec][openspec] · [BMAD-METHOD][bmad] · [agent-os][agent-os] · [Kiro][kiro-repo] | SDD frameworks (stars via `gh api`, 2026-06-27) |
| [ayoubben18/ab-method][ab-method] | Fractal CC+Codex workflow method, v3.7.1, MIT from LICENSE (stars via `gh api`, 2026-07-23) |
| [Martin Fowler — SDD tools][fowler-sdd] | Spec-driven development survey |

[spec-kit]: https://github.com/github/spec-kit
[ab-method]: https://github.com/ayoubben18/ab-method
[openspec]: https://github.com/Fission-AI/OpenSpec
[bmad]: https://github.com/bmadcode/BMAD-METHOD
[agent-os]: https://github.com/buildermethods/agent-os
[kiro-repo]: https://github.com/kirodotdev/Kiro
[fowler-sdd]: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
