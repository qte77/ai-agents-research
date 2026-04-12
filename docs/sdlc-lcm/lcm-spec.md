---
title: Product Lifecycle Management (LCM) Specification
purpose: Product/project lifecycle phases for RAPID-managed products in the qte77 ecosystem.
created: 2026-03-24
authority: This document is the specification. Implementation lives in qte77/sdlc-lcm-manager.
---

## Product Lifecycle Management (LCM) Specification

Lifecycle phases for products and projects managed through RAPID. Applies at the
product/project level (cross-repo), not per-feature.

## Phase Definitions

### 1. Incubation

| Attribute | Value |
|-----------|-------|
| **Version convention** | `0.x.y` (pre-release) |
| **Support level** | Best-effort, no SLA |
| **Allowed changes** | Any (breaking changes expected) |
| **Entry criteria** | BRD approved, initial repo created |
| **Exit criteria** | Core functionality works, first users onboarded |
| **ISO 42001** | A.6.1 (specification), A.6.2 (data assessment) |

### 2. Alpha

| Attribute | Value |
|-----------|-------|
| **Version convention** | `x.y.z-alpha.N` |
| **Support level** | Internal feedback only |
| **Allowed changes** | Breaking changes with notice, rapid iteration |
| **Entry criteria** | Core features functional, basic tests exist |
| **Exit criteria** | Feature-complete for MVP scope, integration tests pass |
| **ISO 42001** | A.6.3 (design), A.6.4 (build) |

### 3. Beta

| Attribute | Value |
|-----------|-------|
| **Version convention** | `x.y.z-beta.N` |
| **Support level** | Bug reports accepted, fixes on best-effort |
| **Allowed changes** | Non-breaking preferred, breaking with migration guide |
| **Entry criteria** | Feature-complete, integration tests pass, docs exist |
| **Exit criteria** | No critical bugs, performance acceptable, security review done |
| **ISO 42001** | A.6.5 (verification and validation) |

### 4. Active

| Attribute | Value |
|-----------|-------|
| **Version convention** | `x.y.z` (semver, no pre-release suffix) |
| **Support level** | Full support, defined response times |
| **Allowed changes** | Semver-compliant (patch: fixes, minor: features, major: breaking) |
| **Entry criteria** | Beta exit criteria met, release runbook executed |
| **Exit criteria** | Superseded by successor OR usage drops below threshold |
| **ISO 42001** | A.6.6 (deployment), A.6.7 (operation and monitoring) |

### 5. Maintenance

| Attribute | Value |
|-----------|-------|
| **Version convention** | `x.y.z` (patch increments only) |
| **Support level** | Security patches and critical bugs only |
| **Allowed changes** | Security fixes, critical bug fixes, dependency updates |
| **Entry criteria** | Decision to wind down active development |
| **Exit criteria** | Deprecation notice published, migration path documented |
| **ISO 42001** | A.6.7 (monitoring), A.7.3 (transparency) |

### 6. Deprecated

| Attribute | Value |
|-----------|-------|
| **Version convention** | No new versions |
| **Support level** | No support, security advisories only |
| **Allowed changes** | None (read-only) |
| **Entry criteria** | Deprecation notice published with sunset date |
| **Exit criteria** | Sunset date reached, no active dependents |
| **ISO 42001** | A.7.3 (transparency) |

### 7. Retired

| Attribute | Value |
|-----------|-------|
| **Version convention** | Archived |
| **Support level** | None |
| **Allowed changes** | None (archived) |
| **Entry criteria** | Sunset date passed, dependents migrated |
| **Exit criteria** | N/A (terminal state) |
| **ISO 42001** | A.6.7 (decommissioning) |
| **Actions** | Archive repo, update downstream references, retain docs |

## Phase Transition Rules

```text
incubation --> alpha --> beta --> active --> maintenance --> deprecated --> retired
                                   ^            |
                                   +-- (reactivate, rare, re-enter via beta gate)
```

- **Forward only** in normal flow
- **Skip allowed**: incubation -> beta (small utilities with clear scope)
- **No skipping** active -> retired (must go through deprecation notice period)

## State Inference

| Signal | Inferred Phase |
|--------|---------------|
| `version: 0.x.y` in pyproject.toml | Incubation |
| Version contains `-alpha` | Alpha |
| Version contains `-beta` | Beta |
| Stable semver, active commits in last 30 days | Active |
| Stable semver, only dependency/security commits | Maintenance |
| `[DEPRECATED]` in README or `deprecated` classifier | Deprecated |
| Repo archived on GitHub | Retired |

Optional explicit override in `pyproject.toml`:

```toml
[tool.lcm]
phase = "active"
```

## Risk Register (ISO 23894)

| Risk | Phase | Likelihood | Impact | Treatment |
|------|-------|------------|--------|-----------|
| Inadequate specification | Incubation | HIGH | HIGH | PRD review gates in RAPID |
| Undetected defects | Beta | MEDIUM | HIGH | Security review + `make validate` |
| Dependency vulnerabilities | Active, Maintenance | HIGH | MEDIUM | Dependabot + `exclude-newer` awareness |
| Knowledge loss | Maintenance | MEDIUM | HIGH | AGENT_LEARNINGS.md, architecture docs |
| Continued use after deprecation | Deprecated | LOW | MEDIUM | Deprecation notices, migration guides |
| Orphaned dependencies | Retired | LOW | LOW | Audit downstream refs before archiving |
