---
title: Claude Code Skills Adoption - Implementation Summary
description: Implementation summary of adopting Claude Code Skills for modular agent capabilities, including format analysis and ecosystem context.
category: analysis
version: 2.0.0
status: completed
created: 2026-01-11
updated: 2026-04-11
validated_links: 2026-04-11
---

**Date**: 2026-01-11
**Status**: Completed

## Summary

Claude Code Skills provide a modular capability pattern for projects using CC.
Skills follow the [Agent Skills open standard][agentskills-spec] (originated by
Anthropic, now adopted by 30+ agent products) and are extended by Claude Code
with additional frontmatter fields.

Autonomous development loop adoption is documented separately (see the Ralph loop references in [CC-ralph-enhancement-research.md](CC-ralph-enhancement-research.md)).

## Example Skills (Initial Adoption Pattern)

The table below shows a representative set of skills covering the main capability areas. Naming follows the lowercase-hyphenated convention required by the Agent Skills spec. Your project skills will differ.

| Skill (example name) | Location | Purpose |
| ----- | -------- | ------- |
| `backend-design` | `.claude/skills/backend-design/SKILL.md` | Backend architecture planning |
| `code-implementation` | `.claude/skills/code-implementation/SKILL.md` | Language-specific code implementation |
| `code-review` | `.claude/skills/code-review/SKILL.md` | Code quality review |
| `requirements-generation` | `.claude/skills/requirements-generation/SKILL.md` | Requirements document conversion |

A project can grow to many more skills over time. Run
`ls .claude/skills/` for the current list in your project.

**Key Features**:

- Progressive disclosure architecture (name+description → full body → resources)
- Third-person descriptions with explicit triggers for auto-discovery
- References to project instructions and contributing guide for compliance
- Under 500 lines per SKILL.md

## Skill Context Budgets

Skills are both a capability pattern and a context-management mechanism.
The four budget mechanics below apply to any project that ships multiple
skills and shape how many can remain effective in a single session.
Mechanics described here reflect current Claude Code; see
[Skills Evolution](#skills-evolution-v210v2169) below for version-tagged
values in historical releases.

### Three-level progressive disclosure

SKILL.md uses a three-level loading model, confirmed across the
[Agent Skills overview][skills-overview] and Anthropic's
[Complete Guide to Building Skills for Claude][skills-pdf] (p. 5):

| Level | When loaded | Approximate cost | Content |
| ----- | ----------- | ---------------- | ------- |
| 1 — YAML frontmatter (`name`, `description`) | Always, at session start | ~100 tokens per skill | Discovery metadata used to decide when to invoke the skill |
| 2 — SKILL.md body | When the skill is invoked | Under 5,000 tokens (target) | Full instructions; recommended cap of 500 lines per [`code.claude.com/docs/en/skills`][cc-skills] and [authoring best practices][skills-best-practices] |
| 3 — Bundled files (`references/`, `scripts/`, examples) | On demand via Read or Bash | Effectively unlimited until read | Reference docs, utility scripts, templates — zero context cost until accessed |

### Shared auto-compaction budget

When Claude Code summarizes the conversation to free context, recently
invoked skills are re-attached after the summary rather than lost. Per
the Skill content lifecycle section of [`code.claude.com/docs/en/skills`][cc-skills]:
"Claude Code re-attaches the most recent invocation of each skill after
the summary, keeping the first 5,000 tokens of each. Re-attached skills
share a combined budget of 25,000 tokens. Claude Code fills this budget
starting from the most recently invoked skill, so older skills can be
dropped entirely after compaction."

Two numbers matter for sizing: **5,000 tokens per skill** (the preserved
window of each re-attached invocation) and **25,000 tokens shared**
(combined ceiling across all re-attached skills). Tight SKILL.md bodies
mean more recently-used skills fit inside this ceiling after compaction.

### Description budget (always loaded)

Skill descriptions are always in context so Claude knows which skills
exist. They share a budget that, per the Troubleshooting section of
[`code.claude.com/docs/en/skills`][cc-skills], "scales dynamically at 1%
of the context window, with a fallback of 8,000 characters." Additional
mechanics from the same source:

- **Per-skill cap: 250 characters.** Entries longer than this are
  truncated in the skill listing regardless of the shared budget.
- **Override via `SLASH_COMMAND_TOOL_CHAR_BUDGET`** environment variable
  to raise the shared ceiling.
- **Front-load trigger keywords** in the description so truncation does
  not hide the match terms Claude needs for auto-discovery.
- **`disable-model-invocation: true` exempts a skill from the budget.**
  Per the invocation-control table in the same page, such a skill's
  description is "not in context" — the skill loads only on explicit
  user invocation via `/name`.

### Skills as the replacement for procedural CLAUDE.md content

The framing statement from [`code.claude.com/docs/en/skills`][cc-skills]:
"Create a skill when you keep pasting the same playbook, checklist, or
multi-step procedure into chat, or when a section of CLAUDE.md has grown
into a procedure rather than a fact. Unlike CLAUDE.md content, a skill's
body loads only when it's used, so long reference material costs almost
nothing until you need it."

This is why skills exist as a context-management mechanism and not merely
as reusable workflows: every CLAUDE.md token is always loaded, while a
skill body is only loaded when invoked. Procedural content that rarely
fires but is expensive to inline is the canonical migration candidate.
Memory-side constraints on CLAUDE.md itself (sizing, discovery,
`claudeMdExcludes`) are covered in
[CC-memory-system-analysis.md](../context-memory/CC-memory-system-analysis.md).

## Skills Evolution (v2.1.0–v2.1.69)

The skills system has evolved significantly since initial adoption:

### Hot-Reload and Lifecycle (v2.1.0+)

- **Automatic hot-reload** from `~/.claude/skills` and `.claude/skills` (v2.1.0)
- **`/reload-plugins`** command for manual hot-reload of skills (v2.1.69)
- **Merged slash commands and skills** — unified system (v2.1.3)
- **`/skills/` directory visible by default** (v2.1.0)
- **Skill suggestion prioritization** in autocomplete (v2.1.0)
- **Skill progress display** during execution (v2.1.0)
- **Skills context visualization** — see what context skills inject (v2.1.0)
- **Skill character budget scales with context** — 2% of context window (v2.1.32)

### New Frontmatter Fields (v2.1.0+)

| Field | Version | Description |
| ----- | ------- | ----------- |
| `context: fork` | v2.1.0 | Run skill in isolated subagent context |
| `agent` | v2.1.0 | Subagent type when `context: fork` (e.g. `Explore`) |
| `hooks` | v2.1.0 | Agent frontmatter hooks (PreToolUse, PostToolUse, Stop) |
| `skills` | v2.0.43 | Auto-load skills for subagents |

### Variable Substitutions

| Variable | Version | Description |
| -------- | ------- | ----------- |
| `$ARGUMENTS`, `$0`, `$1` | v2.1.3 | Shorthand command arguments |
| `${CLAUDE_SKILL_DIR}` | v2.1.69 | Path to the skill's directory |
| `${CLAUDE_SESSION_ID}` | v2.1.13 | Current session identifier |
| `` !`shell command` `` | v2.1.0 | Dynamic context injection |

### Discovery and Loading Improvements

- **Nested `.claude/skills` discovery** (v2.1.6)
- **Skills in `--add-dir` auto-load** (v2.1.32)
- **Duplicate skill detection** via filesystem inode checks (v2.1.3)
- **Skill `allowed-tools` application fixes** (v2.0.76)
- **`auto:N` MCP tool search threshold** via context % (v2.1.13)

## Skills Auto-Discovery

Skills are auto-discovered by Claude Code based on task context. Example triggers (using the example skill names from above):

- Requesting backend design → `backend-design` activates
- Asking to implement code → `code-implementation` activates
- Requesting code review → `code-review` activates
- Converting a requirements document → `requirements-generation` activates

## Design Decision: Skills vs Agents

Both systems can coexist in a project:

- `.claude/agents/` — Subagent definitions for specific roles
- `.claude/skills/` — Claude Code Skills for modular capabilities
- **Rationale**: Skills complement Agents with progressive disclosure and
  auto-discovery. Agents define subagent roles for Task tool invocations; Skills
  define modular capabilities triggered by task context.

## SKILL.md Format: Open Standard vs Claude Code Extensions

The SKILL.md format has two layers:

### 1. Agent Skills Open Standard (agentskills.io)

Cross-platform specification adopted by Claude Code, GitHub Copilot, Cursor,
Gemini CLI, OpenAI Codex, Roo Code, and others.

| Field | Required | Description |
| ----- | -------- | ----------- |
| `name` | Yes | Lowercase + hyphens, max 64 chars, must match directory |
| `description` | Yes | Max 1024 chars; what it does and when to use |
| `license` | No | SPDX identifier |
| `compatibility` | No | Environment requirements, max 500 chars |
| `metadata` | No | Arbitrary key-value map |
| `allowed-tools` | No | Space-delimited pre-approved tools (experimental) |

### 2. Claude Code Extensions (top-level frontmatter)

CC extends the standard with additional fields documented at
[code.claude.com/docs/en/skills][cc-skills]:

| Field | Description |
| ----- | ----------- |
| `argument-hint` | Shown during autocomplete, e.g. `[issue-number]` |
| `disable-model-invocation` | `true` = only user can invoke via `/` |
| `user-invocable` | `false` = hidden from `/` menu |
| `model` | Model override when skill is active |
| `context` | `fork` = run in isolated subagent context |
| `agent` | Subagent type when `context: fork` (e.g. `Explore`) |
| `hooks` | Skill lifecycle hooks |

CC-specific features not in the open standard (see [Skills Evolution](#skills-evolution-v210v2169) for version details):

- `$ARGUMENTS`, `$0`, `$1` string substitutions (v2.1.3)
- `` !`shell command` `` dynamic context injection (v2.1.0)
- `${CLAUDE_SKILL_DIR}` (v2.1.69), `${CLAUDE_SESSION_ID}` (v2.1.13) variables
- `context: fork`, `agent`, `hooks`, `skills` frontmatter fields (v2.0.43–v2.1.0)

### VSCode Validation Warning (Known Bug)

The Claude Code VSCode extension validates SKILL.md frontmatter against a
**stale snapshot** of the agentskills.io schema. It only recognizes:
`argument-hint`, `compatibility`, `description`, `disable-model-invocation`,
`license`, `metadata`, `name`, `user-invocable`.

Fields like `allowed-tools`, `model`, `context`, `agent` trigger false-positive
warnings. This is a [known upstream bug][cc-schema-bug] (issues #23329, #25380,
\#25795 — all closed as duplicates of a tracked fix).

**Workaround**: Nest CC-specific fields under `metadata:` to avoid the warning.
This is valid per the agentskills.io spec (metadata is a free-form map) but means
CC may not interpret them as first-class directives. Monitor the upstream fix;
when shipped, move these fields to top-level.

## Ecosystem Context

The Agent Skills standard has achieved broad cross-industry adoption:

| Source | Type | Relationship |
| ------ | ---- | ------------ |
| [agentskills.io][agentskills-spec] | Open specification | Base standard; originated by Anthropic |
| [code.claude.com/docs/en/skills][cc-skills] | CC documentation | Extends standard with CC-specific fields |
| [skills.sh][skills-sh] | Marketplace/registry | Distribution layer; `npx skills add owner/repo` |
| [Microsoft Agent Framework][ms-skills] | SDK integration | Implements spec via `FileAgentSkillsProvider`; adds code-defined skills |
| [HashiCorp Agent Skills][hashi-skills] | Domain skill library | Terraform/Packer skills in SKILL.md format |
| [anthropics/skills][gh-skills] | Reference skills | Official Anthropic skill examples |

**Key distinction** (from HashiCorp): "MCP is the 'pipe' connecting data to AI;
Agent Skills are the 'textbooks' of knowledge." These are complementary, not
competing patterns.

## Settings Configuration

Update `.claude/settings.json` to adopt Skills:

- Add Skills tool permission
- Enable skill script execution paths

## References

[agentskills-spec]: https://agentskills.io/specification
[cc-skills]: https://code.claude.com/docs/en/skills
[skills-overview]: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
[skills-best-practices]: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
[skills-pdf]: https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf
[gh-skills]: https://github.com/anthropics/skills/tree/main/skills
[skills-sh]: https://skills.sh/
[ms-skills]: https://learn.microsoft.com/en-us/agent-framework/agents/skills
[hashi-skills]: https://www.hashicorp.com/en/blog/introducing-hashicorp-agent-skills
[cc-schema-bug]: https://github.com/anthropics/claude-code/issues/25795
