---
title: SDLC Phase Specification
purpose: Standardized dev process phases for all repos in the qte77 ecosystem, mapped to governance frameworks.
created: 2026-03-24
authority: This document is the specification. Implementation lives in qte77/sdlc-lcm-manager.
---

# SDLC Phase Specification

Dev lifecycle phases for all repos using Ralph, Polyforge, or manual workflows.

## Phase Definitions

### 1. Plan

| Attribute | Value |
|-----------|-------|
| **Entry criteria** | Business requirement or user story exists |
| **Required artifacts** | PRD.md or UserStory.md with acceptance criteria |
| **Responsible tool** | CABIO (BRD -> PRD -> FRD) |
| **Exit gate** | PRD approved, FRD generated, prd.json initialized |

### 2. Design

| Attribute | Value |
|-----------|-------|
| **Entry criteria** | FRD/PRD approved with clear scope |
| **Required artifacts** | Architecture decision records, data model specs |
| **Responsible tool** | Architect agent (via Ralph or manual) |
| **Exit gate** | Technical spec reviewed, dependencies identified |

### 3. Build

| Attribute | Value |
|-----------|-------|
| **Entry criteria** | Design spec exists, dependencies available |
| **Required artifacts** | Source code, inline documentation |
| **Responsible tool** | Ralph TDD loop |
| **Exit gate** | Code compiles/imports, basic smoke test passes |

### 4. Test

| Attribute | Value |
|-----------|-------|
| **Entry criteria** | Build phase complete, code importable |
| **Required artifacts** | Unit tests, integration tests, security tests |
| **Responsible tool** | `make validate` (lint + type check + test) |
| **Exit gate** | All tests pass, coverage meets threshold, no critical findings |

### 5. Release

| Attribute | Value |
|-----------|-------|
| **Entry criteria** | Test phase passed, CHANGELOG.md updated |
| **Required artifacts** | Version bump, git tag, release notes |
| **Responsible tool** | Release runbook (see [lcm-release-runbook.md](lcm-release-runbook.md)) |
| **Exit gate** | Tag pushed, release created, artifacts published |

### 6. Deploy

| Attribute | Value |
|-----------|-------|
| **Entry criteria** | Release tag exists, deployment target configured |
| **Required artifacts** | Deployment manifest, environment config |
| **Responsible tool** | CI/CD pipeline or manual deployment |
| **Exit gate** | Service healthy, smoke tests pass in target environment |

### 7. Maintain

| Attribute | Value |
|-----------|-------|
| **Entry criteria** | Deployed and operational |
| **Required artifacts** | Monitoring dashboards, incident response plan |
| **Responsible tool** | Ops tooling, Polyforge cross-repo visibility |
| **Exit gate** | Transitions to LCM `deprecated` or `retired` phase |
| **Allowed changes** | Bug fixes, security patches, dependency updates only |

## Phase Transition Rules

```
plan --> design --> build --> test --> release --> deploy --> maintain
                      ^        ^                              |
                      |        |                              v
                      +--------+ (TDD iteration)     LCM phase transition
```

- **Forward only** in normal flow
- **Rework loops**: build <-> test (TDD), design -> build (spec change)
- **No skipping**: every phase must be entered
- **Maintain -> LCM**: transition to product lifecycle (see [lcm-spec.md](lcm-spec.md))

## State Inference

Phase is inferred from repo artifacts, not stored explicitly:

| Signal | Inferred Phase |
|--------|---------------|
| Open PRD/FRD, no implementation branch | Plan |
| Architecture docs updated, no code changes | Design |
| Feature branch active, tests not passing | Build |
| Feature branch active, tests passing, no release | Test |
| Version bumped, tag created, not deployed | Release |
| Deployed to target environment | Deploy |
| Stable, no active development | Maintain |

## Cross-Framework Mapping

| Phase | NIST RMF | ISO 42001 A.6 | MAESTRO Layers |
|-------|----------|---------------|----------------|
| Plan | MAP | A.6.1 | L7 |
| Design | MAP | A.6.2, A.6.3 | L2, L3 |
| Build | MANAGE | A.6.4 | L1, L5 |
| Test | MEASURE | A.6.5 | L1-L7 |
| Release | MANAGE | A.6.6 | L6 |
| Deploy | MANAGE | A.6.6 | L4, L6 |
| Maintain | GOVERN+MEASURE | A.6.7 | L4 |
