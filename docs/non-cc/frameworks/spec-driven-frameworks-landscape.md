---
title: Spec-Driven Frameworks — Landscape
purpose: Comparison of spec-driven development frameworks (Spec-Kit, OpenSpec, BMAD-METHOD, Agent-OS, Kiro, Tessl), the deep-dive behind the synthesis entry in the agentic-engineering disciplines landscape.
created: 2026-06-27
updated: 2026-11-26
validated_links_on: 2026-07-23
status: research
---

## What It Is

By 2026 every major coding tool shipped a **spec-driven development (SDD)** flavor: a machine-readable spec becomes the agent's source of truth, and human review shifts from reviewing code to reviewing the spec. This is the standalone comparison behind the synthesis-level §3 table in [agentic-engineering-disciplines-landscape.md](../../sdlc-lcm/agentic-engineering-disciplines-landscape.md). Stars, licenses and releases via `gh api`, as of 2026-11-19.

## Frameworks

| Framework | Stars | License | Loop | Distinctive |
|---|---|---|---|---|
| [github/spec-kit][spec-kit] | 150.6K (v1.4.2, 2026-11-17) | MIT | Spec → Plan → Tasks → Implement | 30+ agent integrations, 70+ extensions; "intent is the source of truth" (counts as of 2026-06-27, not re-checked) |
| [Fission-AI/OpenSpec][openspec] | 75.2K (v2.1.0, 2026-11-17) | MIT | Proposal → Apply → Archive | change-proposal centric; no Model Context Protocol (MCP)/keys required |
| [bmad-code-org/BMAD-METHOD][bmad] | 55.5K (v6.12.4, 2026-10-14) | MIT per the LICENSE file (the API reports "NOASSERTION"); the file adds a trademark notice on the BMad names | multi-agent planning → context-engineered dev | role agents (Analyst / PM / Architect) author the spec; moved from `bmadcode/` to the `bmad-code-org` org |
| [buildermethods/agent-os][agent-os] | 5.6K (v3.0.0, 2026-01-20; last push 2026-10-07) | MIT | MCP context-injection layer | composes with any SDD framework rather than replacing it |
| [kirodotdev/Kiro][kiro-repo] | 4.5K (no releases; last push 2026-11-05) | Proprietary (AWS Customer Agreement); the GitHub repo has no LICENSE file | requirements/bugfix → design → tasks "waves" | full IDE; specs workflow (variants, Quick Spec, bugfix specs) in [kiro-analysis.md § Spec-Driven Workflow](../coding-agents/kiro-analysis.md) |
| Tessl | [`tesslio/spec-driven-development-tile`][tessl-tile]: 58 | MIT (that repo) | steering tile, "No framework" per its README | see [Tessl status](#tessl-status); the earlier "closed-beta / spec-as-source" description is a dated October 2025 claim ([Fowler][fowler-sdd]), not reproducible today |

## How they differ

- **Spec-Kit / OpenSpec** are the two large OSS frameworks — Spec-Kit is the broadest (multi-agent, extension ecosystem), OpenSpec is leaner (proposal → apply → archive, no keys).
- **BMAD** front-loads multi-agent *planning* (role agents draft the spec) before context-engineered execution.
- **Agent-OS** is a *layer*, not a framework — an MCP context-injection shim that pairs with the others.
- **Kiro** bakes SDD into a full IDE — covered in depth, including its specs workflow, in its own analysis.

## Tessl status

Checked 2026-11-19. The `tesslio` GitHub org holds [`spec-driven-development-tile`][tessl-tile] (58 stars, MIT), whose README describes a "steering tile" for writing specs before coding and states "No framework"; an open-source tile. The org has other repos (for example `cli`, 71 stars, no SPDX license detected by the API), so the old "~41" may have come from one of them; that is a guess, not verified. [tessl.io][tessl] now frames the company around Context, Loops and Factory (footer, checked 2026-11-26: Tessl Platform, Tessl Registry, Pricing, Docs, System Status), with no mention of a spec framework, tiles or beta/GA status. The earlier "~41 stars, closed-beta, spec-as-source" row could not be reproduced from current sources; its private-beta and spec-as-source wording matches an October 2025 survey by Birgitta Böckeler ([Fowler][fowler-sdd], 15 Oct 2025), a dated claim and not current status.

## Where SDD sits

SDD is the *what* (machine-readable spec → plan → tasks → implement); **EDD** (eval-driven development) is the *how-to-verify*. Together they bound a non-deterministic agent — SDD constrains the input, EDD constrains the output. See the disciplines landscape for the full "-engineering" / "-driven-development" stack.

## Cross-References

- [agentic-engineering-disciplines-landscape.md](../../sdlc-lcm/agentic-engineering-disciplines-landscape.md) — the §3 synthesis entry this doc expands; the full disciplines + methodologies stack
- [kiro-analysis.md](../coding-agents/kiro-analysis.md) — Kiro's spec-driven IDE in depth
- [software-factory-landscape.md § Economics, failure and verification evidence](../../sdlc-lcm/software-factory-landscape.md#economics-failure-and-verification-evidence) — measured evidence on what agent-built output costs downstream, which spec gates are meant to reduce

## Not included

Entries removed under the [pruning rule](../../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter) (alive, adopted or proven; checked 2026-11-22).

| Name | Reason | Date | Link |
|---|---|---|---|
| AB Method | (criterion 3) adopted or proven: 192 stars (`gh api` 2026-11-22), alive (last push 2026-11-13), but the README states no measured benefit, names no independent users and cites no standards body (checked 2026-11-22) | 2026-11-22 | <https://github.com/ayoubben18/ab-method> |

## Sources

| Source | Content |
|---|---|
| [github/spec-kit][spec-kit] · [OpenSpec][openspec] · [BMAD-METHOD][bmad] · [agent-os][agent-os] · [Kiro][kiro-repo] | SDD frameworks (stars, licenses, releases via `gh api`, 2026-11-19; BMAD LICENSE file read 2026-11-19) |
| [tesslio/spec-driven-development-tile][tessl-tile] · [tessl.io][tessl] | Tessl repo and site status (2026-11-19) |
| [Martin Fowler — SDD tools][fowler-sdd] | Spec-driven development survey |

[spec-kit]: https://github.com/github/spec-kit
[openspec]: https://github.com/Fission-AI/OpenSpec
[bmad]: https://github.com/bmad-code-org/BMAD-METHOD
[agent-os]: https://github.com/buildermethods/agent-os
[kiro-repo]: https://github.com/kirodotdev/Kiro
[fowler-sdd]: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
[tessl-tile]: https://github.com/tesslio/spec-driven-development-tile
[tessl]: https://tessl.io/
