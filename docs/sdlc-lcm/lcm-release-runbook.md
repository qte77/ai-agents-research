---
title: Release Management Runbook
purpose: Checklist bridging SDLC release phase to LCM phase transitions.
created: 2026-03-24
---

# Release Management Runbook

Checklist for executing the SDLC **Release** phase and triggering LCM phase
transitions when applicable.

## Standard Release Checklist

### Pre-Release (SDLC: Test -> Release gate)

- [ ] All tests pass: `make validate`
- [ ] CHANGELOG.md updated with `## [Unreleased]` entries
- [ ] No critical or high security findings open
- [ ] Documentation reflects current state
- [ ] Dependencies audited (no known CVEs in pinned versions)

### Release Execution

- [ ] Determine version bump (semver): patch / minor / major
- [ ] Update version in `pyproject.toml`
- [ ] Move CHANGELOG entries from `[Unreleased]` to `[x.y.z] - YYYY-MM-DD`
- [ ] Create git tag: `git tag -a vx.y.z -m "Release vx.y.z"`
- [ ] Push tag: `git push origin vx.y.z`
- [ ] Create GitHub release from tag (with release notes from CHANGELOG)

### Post-Release

- [ ] Verify tag and release visible on GitHub
- [ ] Update downstream consumers if needed (submodule refs, dependency pins)
- [ ] Add `## [Unreleased]` section to CHANGELOG.md for next cycle

## LCM Phase Transition Releases

These releases mark lifecycle phase changes, not just version increments.

### Incubation -> Alpha

- [ ] Standard release checklist above
- [ ] Version format: `x.y.z-alpha.1`
- [ ] README updated with alpha status notice
- [ ] Core functionality documented

### Alpha -> Beta

- [ ] Standard release checklist above
- [ ] Version format: `x.y.z-beta.1`
- [ ] Integration tests exist and pass
- [ ] API surface documented
- [ ] Known limitations documented

### Beta -> Active (GA)

- [ ] Standard release checklist above
- [ ] Version format: `x.y.z` (no pre-release suffix)
- [ ] Security review completed
- [ ] Performance acceptable under expected load
- [ ] README reflects production status
- [ ] Support expectations documented

### Active -> Maintenance

- [ ] Announcement: development wind-down notice
- [ ] README updated with maintenance-only status
- [ ] CI/CD simplified (remove feature-related workflows if any)
- [ ] Document allowed change types (security, critical bugs only)

### Maintenance -> Deprecated

- [ ] Deprecation notice with sunset date published
- [ ] README banner: `[DEPRECATED] — use [successor] instead`
- [ ] `deprecated` classifier added to `pyproject.toml` if applicable
- [ ] Migration guide published (if successor exists)
- [ ] Downstream consumers notified

### Deprecated -> Retired

- [ ] Sunset date reached
- [ ] Verify no active dependents (check submodule refs, import references)
- [ ] Archive repo on GitHub
- [ ] Update references in ecosystem docs (ai-agents-research, profile README)
- [ ] Retain docs and release artifacts for reference

## Automation Candidates

For future implementation in `qte77/sdlc-lcm-manager`:

| Step | Automation | Priority |
|------|-----------|----------|
| Version bump | `bumpversion` or `uv version` | High |
| CHANGELOG formatting | `git-cliff` or custom script | Medium |
| Tag + release creation | `gh release create` in gate predicate | High |
| Phase inference | Read `pyproject.toml` version + repo signals | High |
| Downstream notification | GitHub Actions workflow dispatch | Low |
| Deprecation banner | PR auto-generated from phase transition | Low |
