---
title: Agent-Consumable Design Formats — Tool Landscape
purpose: Catalog of agent-consumable design-system formats and tooling (the DESIGN.md corpus + Google Labs format spec/CLI; the upstream Figma/W3C token chain) — multi-agent, not Claude Code-specific.
category: landscape
created: 2026-06-27
updated: 2026-06-27
validated_links: 2026-06-27
---

**Status**: Research (informational)

## What It Is

A small but coherent category: **design systems encoded for coding agents** — a
visual identity (colors, typography, spacing, components) captured as
LLM-consumable Markdown/tokens so any coding agent can apply it consistently.
These are **agent-agnostic** (Google Stitch, Cursor, Copilot, Claude Code, …), not
CC-specific, which is why they live here rather than in the cc-community tooling
docs. Two complementary pieces — a hand-authored **corpus** (awesome-design-md) and
a **format spec + CLI** (Google Labs `design.md`) — plus the upstream Figma → W3C
token chain that feeds them.

For Claude Code's own design surface, see the first-party
[Figma MCP plugin](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md#figma-mcp).

## awesome-design-md (VoltAgent)

**Repo**: [VoltAgent/awesome-design-md][awesome-design-md] | **Stars**: 93.8K | **License**: MIT

Curated collection of **58 DESIGN.md files** capturing design systems from popular websites in LLM-consumable Markdown. Each file includes color palettes, typography rules, component styles, layout principles, responsive behavior, and an explicit **Agent Prompt Guide** section. Format designed for Google Stitch and general-purpose coding agents.

### DESIGN.md Format (9 Sections)

1. Visual Theme & Atmosphere — mood, density, design philosophy
2. Color Palette & Roles — semantic names with hex codes (40+ per file)
3. Typography Rules — font families, 16-role hierarchy with px/weight/line-height
4. Component Stylings — buttons (5 variants), cards, inputs, navigation
5. Layout Principles — spacing scale (8px base), grid widths, border-radius (7 levels)
6. Depth & Elevation — 5-level system with exact CSS shadow values
7. Do's and Don'ts — design guardrails and anti-patterns
8. Responsive Behavior — 5 breakpoints, collapsing strategies, touch targets (44x44px min)
9. Agent Prompt Guide — color reference table, 4 example component prompts, 7 iteration principles

### 58 Design Systems (7 Categories)

AI & ML (12): Claude, Mistral AI, Replicate, xAI, ElevenLabs. Developer Tools (14): Cursor, Linear, PostHog, Sentry, Vercel. Infrastructure (6): Stripe, MongoDB, HashiCorp. Design & Productivity (10): Figma, Notion, Framer, Miro. Fintech (4): Coinbase, Revolut, Wise. Enterprise (7): Airbnb, Apple, IBM, SpaceX, Spotify. Car Brands (5): BMW, Ferrari, Tesla.

### Key Differentiator

A new artifact type: design systems encoded for LLM consumption rather than human developers or design tool plugins. The Agent Prompt Guide section is a novel contribution — ready-to-use component prompts with iteration instructions. Files capture publicly visible CSS values, not proprietary design tokens. 93.8K stars (21.8K in its first 6 days, riding the Google Stitch launch wave).

**Who is VoltAgent**: Open-source [TypeScript AI Agent Framework](https://voltagent.dev) for enterprise multi-agent systems (tool calling, persistent memory, supervisor orchestration, 40+ integrations). The awesome-design-md repo is a community/marketing project.

**Gap**: No public tooling for generating DESIGN.md from arbitrary sites — extraction appears manual/internal.

Cross-ref: [CC-domain-claudemd-showcase.md](../cc-community/CC-domain-claudemd-showcase.md) — CLAUDE.md as domain controller, analogous pattern

## DESIGN.md format spec + CLI (Google Labs)

**Repo**: [google-labs-code/design.md][google-design-md] | **Stars**: 22.1K | **License**: Apache-2.0 (alpha)

Google Labs' canonical **format specification + CLI** for the artifact awesome-design-md collects by hand: a `DESIGN.md` encodes a visual identity for coding agents as YAML front matter (machine-readable design tokens — color, typography, spacing, components) plus prose rationale (the *why* behind each decision), giving agents a persistent, structured design system instead of scattered Figma links. The `@google/design.md` CLI adds the validation/generation tooling the awesome-design-md "Gap" note flags as missing:

- **Lint / validate** — broken token references, contrast violations, structural issues
- **Diff** — compare design versions to catch regressions
- **Export** — tokens → Tailwind, CSS, or W3C Design Token format
- **Structured JSON output** — for programmatic agent consumption

### Key Differentiator

awesome-design-md is a *corpus* of 58 hand-authored DESIGN.md files; Google Labs `design.md` is the *spec + toolchain* that makes the format machine-checkable (lint/diff/export). The two are complementary — the spec defines the contract, the corpus demonstrates it. Format is **alpha**; expect changes.

### Related: design source + token standard

DESIGN.md sits downstream of two adjacent pieces. **Source of truth:** the [Figma Dev Mode MCP server][figma-mcp] (beta) feeds AI coding agents structured design context — components, variables, layout — straight from Figma files (and can write frames/variables back to the canvas), supported in Claude Code, Copilot/VS Code, Cursor, and Windsurf. **Token format:** the [W3C Design Tokens (DTCG) format][dtcg] (`$value`/`$type`; first stable spec Oct 2025) is the interchange standard that Amazon's [Style Dictionary][style-dictionary] (v4+) emits — the same token shape DESIGN.md's CLI exports. The chain: Figma MCP supplies live design context to the agent → DTCG/Style Dictionary standardizes the tokens → DESIGN.md packages them as agent-readable Markdown.

## Cross-References

- [CC-community-tooling-landscape.md](../cc-community/CC-community-tooling-landscape.md) — the CC dev-tooling landscape this cluster moved out of
- [CC-official-plugins-landscape.md](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md#figma-mcp) — Claude Code's first-party Figma MCP plugin (design-to-code)

## Sources

| Source | Content |
|---|---|
| [VoltAgent/awesome-design-md][awesome-design-md] | 58 DESIGN.md files for agent-consumable UI generation (93.8K stars, MIT) |
| [google-labs-code/design.md][google-design-md] | Canonical DESIGN.md format spec + `@google/design.md` CLI (lint/diff/export to Tailwind/CSS/W3C tokens); 22.1K stars, Apache-2.0, alpha |
| [Figma Dev Mode MCP server][figma-mcp] | Feeds Figma design context to coding agents (Claude Code/Copilot/Cursor/Windsurf); beta |
| [W3C Design Tokens (DTCG)][dtcg] · [Style Dictionary][style-dictionary] | Design-token interchange standard (first stable spec Oct 2025) + Amazon's token transformer (v4 DTCG support) |

Moved here from [CC-community-tooling-landscape.md](../cc-community/CC-community-tooling-landscape.md) on 2026-06-27 (tracked in [#329](https://github.com/qte77/ai-agents-research/issues/329)) — agent-consumable design formats are multi-agent, not CC-specific.

[awesome-design-md]: https://github.com/VoltAgent/awesome-design-md
[google-design-md]: https://github.com/google-labs-code/design.md
[figma-mcp]: https://www.figma.com/blog/introducing-figma-mcp-server/
[dtcg]: https://www.w3.org/community/design-tokens/
[style-dictionary]: https://styledictionary.com/
