---
title: User Story - coding-agents-research
description: User stories for systematic coding agent research, comparison, and feature triage
category: requirements
created: 2026-03-22
updated: 2026-03-22
version: 1.0.0
---

# User Story: coding-agents-research

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
- As a researcher, I want to document CC session artifacts and orchestration patterns so that downstream repos (cc-recursive-team-mode, coding-agent-eval) have accurate reference material.

## Success Criteria

1. New agent analysis doc follows frontmatter conventions and lands in the correct subdirectory (`docs/cc-native/` or `docs/non-cc/`).
2. CC changelog triage identifies evaluation-relevant features within 7 days of release.
3. Feature comparison matrix covers all agents tracked by coding-agent-eval.
4. Session artifact documentation is accurate enough for cc-recursive-team-mode to implement parsers without additional research.

## Constraints

- Markdown-only (no code implementation)
- Follows existing doc hierarchy (cc-native/, non-cc/, community/, triage/)
- Analysis format: What it is → How it works → Adoption decision → Action items
- Three automated monitors maintain currency via GitHub Actions

## Out of Scope

- Automated triage without human review
- CI/CD for documentation validation
- Code implementation (this is a research-only repo)
- Agent benchmarking (that's coding-agent-eval's job)
