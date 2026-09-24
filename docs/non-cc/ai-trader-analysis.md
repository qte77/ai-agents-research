---
title: AI-Trader — Agent-Native Trading Signal Platform
purpose: Assess ai4trade.ai's SKILL.md onboarding surface for Claude Code/Codex/Cursor agents competing on live trading signals
source: https://ai4trade.ai/SKILL.md
created: 2026-09-24
updated: 2026-09-24
validated_links: 2026-09-24
---

**Status**: Assess

## What It Is

AI-Trader (ai4trade.ai) is a trading-signal platform where AI coding agents —
the SKILL.md names Claude Code, Codex, and Cursor explicitly — publish
trading signals, follow other agents' signals (copy trading), and compete in
challenges across crypto, US stocks, and Polymarket. Each registered agent
gets $100,000 in simulated capital and earns points for activity: +10 for
publishing a signal, +1 per follower gained through copy trading. A heartbeat
subscription system delivers replies, mentions, and follower events back to
the agent. Authentication uses JWT tokens against a base API at
`https://ai4trade.ai/api`.

## Why This Is a Research-Relevant Artifact

The fetched file is not documentation about the product — it is the root
`SKILL.md` the vendor publishes at its domain root as the agent's own
bootstrap and routing layer: a coding agent reads it directly to authenticate
and discover further specialized skills (copy trading, real-time trades,
competitions, market intelligence). This is an instance of a "root SKILL.md
as onboarding surface" pattern vendors are starting to publish for direct
agent consumption — narrower in scope than AGENTS.md (one product's own API,
not general repo conventions) but the same underlying idea of a file written
for an agent to read first.

## Unverifiable / Hedged

- **No GitHub repository, license, or maintaining-company information** is
  published anywhere in the fetched SKILL.md; `ai4trade.ai` is the only
  public identity found. A GitHub user literally named `ai4trade` exists,
  but nothing in the fetched material ties it to this platform, so it is
  **not** cited as a source here.
- The platform's simulated-capital and competition mechanics are described
  exactly as the vendor's own SKILL.md states them; this entry verifies only
  that the document says this, not that the underlying platform, its
  business entity, or its trading-competition claims are legitimate or
  operate as described. No independent corroboration was available from a
  second first-party source.

## Sources

| Source | Content |
|---|---|
| [ai4trade.ai/SKILL.md][skill] | Platform mechanics, supported agents, API base, points system (first-party, fetched 2026-09-24) |

[skill]: https://ai4trade.ai/SKILL.md
