---
title: CC Plans as Skill and Rule Templates
description: Analysis of Claude Code plan files — anatomy, plan mode mechanics, and patterns for extracting reusable skills and rules from recurring plans.
category: analysis
status: research
created: 2026-03-13
updated: 2026-04-05
validated_links: 2026-04-05
---

**Status**: Research (informational)

## Summary

Claude Code's plan mode produces structured plan files that serve as reviewable implementation proposals. This document analyzes plan file anatomy, plan mode mechanics, and three reuse patterns: plans as skill input, plans as skill templates, and plan-to-rule extraction.

**Research gap**: No existing CC documentation covers plan file structure, plan mode lifecycle, or systematic plan reuse. This analysis is based on observation of real plan files and community examples.

## Plan File Anatomy

Plan files follow a consistent structure observed across real-world examples:

| Section | Purpose | Required |
|---------|---------|----------|
| **Context** | Problem statement, current state, why the change is needed | Yes |
| **Phases / Changes** | Ordered implementation steps, grouped by concern | Yes |
| **Files table** | Files to create/edit/delete with annotations | Common |
| **Verification** | How to confirm correctness (tests, commands, manual checks) | Common |
| **Commit message** | Conventional commit suggestion | Optional |

**Key characteristics**:

- **No frontmatter** — plan files are plain markdown, not SKILL.md-formatted
- **Inline literal code** — concrete code snippets, not pseudocode
- **Scope scales with task** — simple bug fixes produce 20-line plans; restructuring produces 200+ lines
- **Self-contained** — each plan includes enough context to implement without re-reading the conversation

### Example Structure

```markdown
# Plan: <descriptive title>

## Context
<problem statement and current state>

## Approach
<high-level strategy>

## Changes

### Phase 1: <concern>
- File: `path/to/file.py` (edit)
  - Change X to Y
  - Add function Z

### Phase 2: <concern>
...

## Files

| File | Action |
|------|--------|
| `src/module.py` | Edit |
| `tests/test_module.py` | New |

## Verification
1. `make test` passes
2. `make validate` passes

## Commit
feat(module): add feature X
```

## Plan Mode Mechanics

### Lifecycle

1. **EnterPlanMode** — CC switches to read-only exploration (no edits allowed)
2. **Research phase** — reads files, searches codebase, gathers context
3. **Plan file written** — structured plan saved (typically to conversation context, sometimes to `.claude/plans/`)
4. **ExitPlanMode** — returns to normal mode
5. **User approval** — user reviews plan, approves/rejects/modifies
6. **Implementation** — CC executes the approved plan

### Agent Teams Plan Approval (v2.1.x)

In agent teams, teammates can produce plans that require approval from the coordinator or user before execution. This enables review gates for multi-agent workflows.

### Plan Storage

- Plans created via `/plan` or plan mode appear in conversation context
- Persistent plans can be saved to `.claude/plans/` for cross-session reference
- Plans are not automatically indexed or discoverable — they require manual organization

## Reuse Patterns

### Pattern 1: Plan as Skill Input

A skill consumes a plan file as a reviewable artifact, adding a review or validation layer.

**Example**: gstack's `/plan-ceo-review` and `/plan-eng-review` skills accept a plan and evaluate it from a specific perspective (founder/business review vs. engineering review). The plan itself is the input; the skill adds judgment.

**When to use**: When plans need approval gates from different stakeholder perspectives before implementation.

```text
User creates plan → /plan-ceo-review (business viability check)
                   → /plan-eng-review (technical feasibility check)
                   → Approved → Implementation
```

### Pattern 2: Plan as Skill Template

A skill ships a companion plan template with `{{PLACEHOLDERS}}` that gets filled in per invocation.

**Example**: The `generating-writeup` skill includes template files (IMRaD structure, technical doc structure) that define the skeleton of the output. When invoked, the skill fills in project-specific content while maintaining the template structure.

**When to use**: When a repeatable workflow always follows the same structural pattern but with different content per project/task.

```text
Skill SKILL.md defines:
  - Trigger conditions
  - Template reference: templates/research-paper-plan.md

Template contains:
  ## Context
  {{PROJECT_DESCRIPTION}}

  ## Phases
  ### 1. Literature Review
  - Search for: {{SEARCH_TERMS}}
  ...
```

### Pattern 3: Plan to Rule Extraction

Recurring plan patterns (verification steps, cross-reference checks, changelog updates) can be promoted to `.claude/rules/` as persistent constraints that apply automatically.

**Process** (manual — no tooling exists):

1. Identify a pattern that appears in 3+ plans
2. Extract the constraint (e.g., "always verify cross-references after file moves")
3. Write as a rule file in `.claude/rules/`

**Example extraction**:

```markdown
# Before: recurring plan verification step
## Verification
3. Grep for broken cross-references after renaming

# After: .claude/rules/cross-references.md
# Cross-Reference Integrity
After any file rename or move, verify all markdown links still resolve.
Run: grep -r '](.*old-path' docs/
```

### Pattern 4: Plan to Skill Extraction

Recurring plan structures (restructure + update refs + changelog) can be promoted to skills with SKILL.md frontmatter, transforming one-shot plans into repeatable workflows.

**Process**:

1. Identify a plan structure used 3+ times
2. Extract the common structure, parameterize variable parts
3. Create SKILL.md with trigger conditions and the template

**Example**: A "restructure docs" plan that always involves: move files → update cross-references → update README → update CHANGELOG → verify links. This becomes a `/restructure-docs` skill.

## Adoption Guidance

### When to Extract

- **Rule**: A verification step or constraint appears in 3+ plans → `.claude/rules/`
- **Skill**: A multi-step workflow structure repeats 3+ times → `.claude/skills/`
- **Template**: A plan's file table and phase structure are reusable → companion template

### What to Extract

The most reusable parts of plans are:

1. **Verification checklists** — "run these checks before done" → rules
2. **File table patterns** — "these file types always need these changes together" → skill templates
3. **Phase ordering** — "always do X before Y" → rules or skill workflow

### What NOT to Extract

- One-off plans with project-specific logic
- Plans where the context section is the primary value (the "why" doesn't generalize)
- Plans with fewer than 3 occurrences of the pattern

## UltraPlan — Cloud-Offloaded Planning (Research Preview)

UltraPlan hands a planning task from the local CLI to a [Claude Code on the web][cc-web] session running Opus in plan mode. The plan drafts asynchronously in the cloud while the terminal stays free for other work. A browser-based review surface provides inline comments, emoji reactions, and an outline sidebar — none of which exist in local plan mode ([source][ultraplan]).

### Invocation

| Method | Example | Notes |
|--------|---------|-------|
| Command | `/ultraplan migrate auth from sessions to JWTs` | Shows confirmation dialog |
| Keyword | Include `ultraplan` anywhere in a normal prompt | Shows confirmation dialog |
| Escalate from local plan | Choose *"No, refine with Ultraplan on Claude Code on the web"* from local plan approval dialog | Skips confirmation (selection is implicit) |

### Terminal Status Indicators

| Indicator | Meaning |
|-----------|---------|
| `◇ ultraplan` | Claude is researching and drafting the plan |
| `◇ ultraplan needs your input` | Clarifying question — open session link to respond |
| `◆ ultraplan ready` | Plan ready for browser review |

Run `/tasks` and select the ultraplan entry for session link, agent activity, and a **Stop ultraplan** action.

### Execution After Approval

From the browser, choose one of:

1. **Execute on the web** — Claude implements in the same cloud session; review diff and create PR from the browser
2. **Teleport back to terminal** — plan sent back to the waiting CLI with three sub-options:
   - *Implement here* — inject into current conversation
   - *Start new session* — clear conversation, begin fresh with plan as context (`claude --resume` command printed for return)
   - *Cancel* — save plan to file without executing

### Requirements and Constraints

- Requires [Claude Code on the web][cc-web] account and a GitHub repository
- Disconnects [Remote Control][rc] when active (both occupy the claude.ai/code interface)
- Cloud session runs in the account's default cloud environment

Cross-ref: [CC-cloud-sessions-analysis.md](../ci-remote/CC-cloud-sessions-analysis.md) — cloud execution environment details

## Related Documents

- [CC-skills-adoption-analysis.md](CC-skills-adoption-analysis.md) — skills format and adoption patterns
- [CC-agent-teams-orchestration.md](CC-agent-teams-orchestration.md) — agent teams and task delegation
- [CC-ralph-enhancement-research.md](CC-ralph-enhancement-research.md) — autonomous loop patterns

## References

- [Claude Code Plan Mode](https://code.claude.com/docs/en/plan-mode) — official documentation
- [UltraPlan][ultraplan] — official documentation (research preview)
- ~~[Agent Skills Spec](https://agentskills.org/)~~ — domain offline (archived reference)

[ultraplan]: https://code.claude.com/docs/en/ultraplan
[cc-web]: https://code.claude.com/docs/en/claude-code-on-the-web
[rc]: https://code.claude.com/docs/en/remote-control
