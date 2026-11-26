---
title: "Opennote: AI Tutor Embedded in Note-Taking"
source: https://www.ycombinator.com/launches/Nwd-opennote-interactive-learning-for-students
purpose: Track Opennote as an AI-native edtech product with open agent SDKs and a Llama-backed tutoring pipeline
created: 2026-06-20
updated: 2026-11-26
validated_links_on: 2026-06-20
status: assess
---

**Details:**. Also runs on or integrates with: `web`, `google-drive`, `notion`, `api-sdk`.

> **Status note (checked 2026-11-26):** [opennote.com][opennote-site] says Opennote was acquired by Reducto (announced 2026-05-06) and that the app has been sunset and is no longer available. The product description, pricing and adoption text below describe the product as it stood on 2026-06-20, before this check, and are kept for the record. The `opennote-dev` SDK repos remain public and MIT-licensed on GitHub; whether they are still maintained is unverified.

## What It Is

Opennote is an AI-powered learning platform that embeds a tutor directly in a
note-taking workspace — "the AI tutor that lives in your notes." It is a Y
Combinator Summer 2025 company (≈$850K pre-seed led by Afore Capital, per [BetaKit][betakit]) targeting
higher-education learners who want to turn written notes into interactive,
AI-guided study. Under the hood it ran on Meta's open-source **Llama** models (per [BetaKit][betakit]).
See the [YC launch page][yc-launch].

It is included here as an **AI-native application** rather than a coding agent.
The corpus-relevant hook is its open surface: the closed-core SaaS is paired with
an open-source GitHub org ([opennote-dev][gh-org]) publishing **MIT-licensed**
Python and TypeScript API SDKs plus document utilities (`speedyf`) — i.e. it
exposes an agent/Retrieval-Augmented Generation (RAG) integration surface, not just an end-user app.

## Capabilities

Per the [YC launch][yc-launch] and [BetaKit coverage][betakit] (the YC page supports only Feynman, real-time Socratic feedback with visual explanations, friend and journal sharing, and the "over 55,000 students" claim; the Turing, whiteboard and Google Drive/Notion import items below are unverified against both sources):

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

Pricing (per [BetaKit][betakit], as of 2026-06-20; the first-party pricing page now shows only the acquisition notice): free tier; Premium ~$15/mo (unlimited chats,
video generation); enterprise quote-based. A "20% student discount" in the earlier version of this analysis is not in the BetaKit article (unverified). Treat exact
figures as secondary-sourced and historical.

## Sources

| Source | Content |
|---|---|
| [YC launch — Opennote][yc-launch] | First-party launch: founders, product description, feature list, user-count claim, launch promo |
| [opennote.com][opennote-site] | First-party acquisition and sunset notice (2026-05-06; checked 2026-11-26) |
| [opennote-dev (GitHub org)][gh-org] | Open-source MIT Python/TypeScript SDKs + `speedyf` document utilities |
| [BetaKit — Opennote raises $850K][betakit] | Secondary — funding round, pricing tiers, Llama model usage |

[opennote-site]: https://opennote.com
[yc-launch]: https://www.ycombinator.com/launches/Nwd-opennote-interactive-learning-for-students
[gh-org]: https://github.com/opennote-dev
[betakit]: https://betakit.com/opennote-raises-850000-usd-secures-y-combinator-spot-for-edtech-platform/
