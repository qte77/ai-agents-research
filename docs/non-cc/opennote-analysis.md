---
title: "Opennote: AI Tutor Embedded in Note-Taking"
source: https://www.ycombinator.com/launches/Nwd-opennote-interactive-learning-for-students
purpose: Track Opennote as an AI-native edtech product with open agent SDKs and a Llama-backed tutoring pipeline
created: 2026-06-20
updated: 2026-06-20
validated_links: 2026-06-20
platform_scope: [web, google-drive, notion, api-sdk]
---

**Status**: Assess

## What It Is

Opennote is an AI-powered learning platform that embeds a tutor directly in a
note-taking workspace — "the AI tutor that lives in your notes." It is a Y
Combinator Summer 2025 company (≈$850K pre-seed led by Afore Capital) targeting
higher-education learners who want to turn written notes into interactive,
AI-guided study. Under the hood it runs on Meta's open-source **Llama** models.
See the [YC launch page][yc-launch].

It is included here as an **AI-native application** rather than a coding agent.
The corpus-relevant hook is its open surface: the closed-core SaaS is paired with
an open-source GitHub org ([opennote-dev][gh-org]) publishing **MIT-licensed**
Python and TypeScript API SDKs plus document utilities (`speedyf`) — i.e. it
exposes an agent/RAG integration surface, not just an end-user app.

## Capabilities

Per the [YC launch][yc-launch] and [BetaKit coverage][betakit]:

- **Feynman** — generates narrated, animated video lessons from a student's notes
  via a custom AI pipeline.
- **Turing** — a coding sidekick that analyzes scripts, suggests fixes, and
  generates inline practice problems.
- Real-time Socratic feedback while writing; visual-aid generation (graphs,
  diagrams, images); collaborative whiteboards; a community sharing feed.
- Google Drive and Notion import for existing course materials.
- Open **Python + TypeScript API SDKs** (MIT) via [opennote-dev][gh-org].

## Adoption Decision

**Assess.** Early-stage edtech (YC S25, pre-seed) with a differentiated
AI-in-notes angle and reported traction ("55,000+ students" — vendor figure,
unaudited). Worth tracking as an example of a Llama-backed tutoring agent with an
open integration surface; too early for Trial/Adopt without retention data or a
stable feature set. The primary domain is edtech/tutoring; adjacency to the
corpus is via its open SDKs and document-agent pipeline rather than developer
tooling.

Pricing (per [BetaKit][betakit]; the first-party pricing page did not load at
access time, 2026-06-20): freemium free tier; Premium ~$15/mo (unlimited chats,
video generation); enterprise quote-based; 20% student discount. Treat exact
figures as secondary-sourced.

## Sources

| Source | Content |
|---|---|
| [YC launch — Opennote][yc-launch] | First-party launch: founders, product description, feature list, user-count claim, launch promo |
| [opennote-dev (GitHub org)][gh-org] | Open-source MIT Python/TypeScript SDKs + `speedyf` document utilities |
| [BetaKit — Opennote raises $850K][betakit] | Secondary — funding round, pricing tiers, Llama model usage |

[yc-launch]: https://www.ycombinator.com/launches/Nwd-opennote-interactive-learning-for-students
[gh-org]: https://github.com/opennote-dev
[betakit]: https://betakit.com/opennote-raises-850000-usd-secures-y-combinator-spot-for-edtech-platform/
