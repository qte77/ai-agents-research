---
title: User Story - ai-agents-research
description: User stories for systematic coding agent research, comparison, and feature triage
category: requirements
created: 2026-03-22
updated: 2026-09-30
version: 1.0.0
---

## User Story: ai-agents-research

## Problem Statement

The coding agent landscape evolves rapidly with frequent feature releases, new entrants, and changing capabilities. There is no systematic process to research, compare, and triage new agent features, leading to outdated assumptions and missed opportunities in downstream evaluation repos.

## Target Users

AI researchers tracking coding agent capabilities and informing evaluation harness development.

## Value Proposition

Maintain a living knowledge base of coding agent capabilities, CC internals, and community patterns — enabling data-driven decisions about what to evaluate, adopt, or defer in downstream repos.

## User Stories

- As a researcher, I want to research a new coding agent and add an analysis doc so that the team has a structured reference for each agent's capabilities.
- As a researcher, I want to triage CC changelog entries for new features so that I can identify evaluation-relevant changes quickly.
- As a researcher, I want to update the feature comparison matrix so that cross-agent capability differences are visible at a glance.
- As a researcher, I want to document CC session artifacts and orchestration patterns so that downstream repos (cc-recursive-team-mode, coding-harness-eval) have accurate reference material.
- As a researcher, I want weekly ArXiv preprints filtered by an AI-agent relevance prompt so that I see only papers worth promoting to `docs/` without manually scanning the firehose.
- As a researcher, I want tools for agent memory, context, skills, plugins and harnesses scored on one rubric (shared, distributed, reproducible, adaptable, versionable, traceable) so that I can see which properties the field already delivers and which are still open.
- As a reader, I want to browse by subject (memory, knowledge graphs, RAG, code tooling, visualization, context, skills, plugins, harness, long-running tasks) across the CC-relationship buckets so that I find every related doc without knowing which bucket it lives in.

## Success Criteria

1. New agent analysis doc follows frontmatter conventions and lands in the correct subdirectory (`docs/cc-native/<subdir>/` or `docs/non-cc/<section>/`), and gets a row in the matching `docs/_topics/` hub when it covers a hub subject.
2. CC changelog triage identifies evaluation-relevant features within 7 days of release.
3. Feature comparison matrix covers all agents tracked by coding-harness-eval.
4. Session artifact documentation is accurate enough for cc-recursive-team-mode to implement parsers without additional research.

## Constraints

- Markdown corpus; code is limited to stdlib tooling that validates the docs and builds the doc graph (`.github/scripts/`, `scripts/`, tested with `make test`)
- Follows existing doc hierarchy (cc-native/, non-cc/, community/, triage/)
- Analysis format: What it is → How it works → Adoption decision → Action items
- Four automated monitors maintain currency via GitHub Actions (CC status, CC changelog + native sources, community, ArXiv paper eval)

## Out of Scope

- Automated triage without human review
- Product code (this is a research-only repo; tooling serves the corpus only)
- Agent benchmarking (that's coding-harness-eval's job)
