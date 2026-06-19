---
title: CC Memory System Analysis
source: https://code.claude.com/docs/en/memory
purpose: Analysis of Claude Code's dual memory system (CLAUDE.md + auto memory) for optimizing agent instructions, cross-session learning, and headless CC workflow context management.
created: 2026-03-07
updated: 2026-06-19
validated_links: 2026-06-19
---

**Status**: Generally available (CLAUDE.md); Auto memory enabled by default

## What the Memory System Is

Two complementary mechanisms that carry knowledge across Claude Code sessions ([source][cc-mem]):

1. **CLAUDE.md files**: Human-written persistent instructions (project standards, workflows, architecture)
2. **Auto memory**: Claude-written notes accumulated from corrections and discoveries

Both load at session start. Neither is enforced configuration — they're context. Specificity and conciseness improve adherence ([source][cc-mem]).

### CLAUDE.md vs Auto Memory

| Aspect | CLAUDE.md | Auto Memory |
| ------ | --------- | ----------- |
| Author | Human | Claude |
| Content | Instructions and rules | Learnings and patterns |
| Scope | Project, user, or org | Per working tree (git repo) |
| Loaded | Every session (full file) | Every session (first 200 lines of MEMORY.md) |
| Use for | Coding standards, workflows, architecture | Build commands, debugging insights, preferences |

### CLAUDE.md Scope Hierarchy

| Scope | Location | Shared with |
| ----- | -------- | ----------- |
| Managed policy | `/etc/claude-code/CLAUDE.md` (Linux) | All users in org (cannot be excluded) |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team via source control |
| User | `~/.claude/CLAUDE.md` | Just you (all projects) |
| Local | `./CLAUDE.local.md` | Just you (current project, gitignored) |

More specific locations take precedence. Files in parent directories load at launch; files in subdirectories load on demand when Claude reads files there ([source][cc-mem]).

### `.claude/rules/` System

Topic-specific instruction files with optional path scoping:

```text
.claude/
├── CLAUDE.md
└── rules/
    ├── code-style.md      # Always loaded (no paths frontmatter)
    ├── testing.md          # Always loaded
    └── api-design.md       # Path-scoped (see below)
```

Rules without `paths` frontmatter load unconditionally at launch with the same priority as `.claude/CLAUDE.md`. Path-scoped rules load when Claude reads matching files ([source][cc-mem]).

### Path-Scoped Rules Deep Dive

Path-specific rules use YAML frontmatter with the `paths` field:

```markdown
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All endpoints must include input validation
- Use the standard error response format
```

#### Glob Syntax

| Pattern | Matches |
|---|---|
| `**/*.ts` | All TypeScript files in any directory |
| `src/**/*` | All files under `src/` directory |
| `*.md` | Markdown files in the project root only |
| `src/components/*.tsx` | React components in a specific directory |
| `src/**/*.{ts,tsx}` | Brace expansion for multiple extensions |
| `tests/**/*.test.ts` | Test files in a specific naming convention |

Multiple patterns and brace expansion are supported in a single rule ([source][cc-mem]):

```markdown
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

#### Behavioral Rules

- **Trigger**: Path-scoped rules trigger when Claude **reads** files matching the pattern, not on every tool use ([source][cc-mem])
- **Multiple patterns**: A single rule file can specify multiple glob patterns
- **No paths field**: Rules without `paths` load unconditionally at launch
- **Subdirectory CLAUDE.md**: Files in subdirectories load on-demand when Claude reads files there — not at launch ([source][cc-mem])
- **User-level rules**: Personal rules in `~/.claude/rules/` apply to every project; loaded before project rules (lower priority) ([source][cc-mem])

#### Symlinks for Cross-Project Sharing

`.claude/rules/` supports symlinks for sharing rules across projects ([source][cc-mem]):

```bash
# Link a shared rules directory
ln -s ~/shared-claude-rules .claude/rules/shared

# Link an individual file
ln -s ~/company-standards/security.md .claude/rules/security.md
```

Circular symlinks are detected and handled gracefully ([source][cc-mem]).

### Monorepo Management

#### `claudeMdExcludes`

Skip irrelevant CLAUDE.md files in monorepos via `.claude/settings.local.json` ([source][cc-mem]):

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

- Patterns matched against **absolute file paths** using glob syntax
- Configurable at any settings layer (user, project, local, managed policy)
- Arrays merge across layers
- **Managed policy CLAUDE.md cannot be excluded** — ensures org-wide instructions always apply ([source][cc-mem])

#### Organization-Wide Managed CLAUDE.md

Centrally managed file that applies to all users on a machine ([source][cc-mem]):

| OS | Path |
|---|---|
| macOS | `/Library/Application Support/ClaudeCode/CLAUDE.md` |
| Linux / WSL | `/etc/claude-code/CLAUDE.md` |
| Windows | `C:\Program Files\ClaudeCode\CLAUDE.md` |

Deploy via MDM, Group Policy, Ansible, or similar. Cannot be excluded by individual `claudeMdExcludes` settings.

The `claudeMd` key in `managed-settings.json` can carry CLAUDE.md content inline instead of deploying a separate file (honored in managed/policy settings only) ([source][cc-mem]).

#### Additional Directories

Load CLAUDE.md from directories outside the main working directory ([source][cc-mem]):

```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Overly broad globs (e.g., `**/*`) | Fires on every file read, defeating scoping purpose | Scope to specific directories or extensions |
| CLAUDE.md > 200 lines | Reduced adherence; more tokens consumed | Split into `.claude/rules/` files or use `@` imports |
| Conflicting instructions across files | Claude picks one arbitrarily | Periodic review; use `/memory` to audit loaded files |
| Deep `@` import chains | Increases token cost | Audit total imported size; keep chain under 400 total lines |
| Duplicate auto memory vs manual learnings | Stale or contradicting patterns | Periodic deduplication review |

### Instruction Adherence Patterns

CC injects CLAUDE.md content wrapped in a `<system-reminder>` tag — [observed via API interception][cc-reverse-eng] and documented in the Agiflow prompt-augmentation analysis. The `<system-reminder>` framing signals to the model that the content is optionally relevant rather than unconditionally binding. As the file grows, instruction adherence degrades: instructions buried deeper in a large file are less reliably followed than those at the top.

This answers the open question "Why Claude ignores explicit MUST directives" flagged in [CC-community-skills-landscape.md][cc-skills-landscape] (claude-code-best-practice entry).

#### Conditional XML Blocks

The recommended fix is to scope domain-specific rules with [conditional XML blocks][hlyr-claude-md] rather than shrinking the file:

```markdown
<important if="you are writing or modifying tests">
- Every test must have an Arrange-Act-Assert comment block
- Mocks are forbidden for the system under test
</important>
```

The condition narrows when the block fires. This improves adherence without reducing total instruction coverage.

**Foundational vs conditional split**:

| Rule type | Treatment | Examples |
|---|---|---|
| Foundational | Unconditional (always in scope) | Project identity, tech stack, directory structure |
| Conditional | Wrapped in `<important if="…">` | Testing procedures, deployment steps, domain rules |

**Condition specificity principle**: conditions must be narrow enough to fire only when relevant. Anti-pattern: `"you are writing code"` (fires on nearly every task, defeating the purpose). Good: `"you are writing or modifying tests"` or `"you are modifying a CI workflow file"`.

HumanLayer ships an `improve-claude-md` skill that automates this restructuring ([source][hlyr-claude-md]):

```bash
npx skills add humanlayer/skills --skill improve-claude-md
```

Cross-ref: [CC-reverse-engineering-landscape.md][cc-reverse-eng] — Agiflow section documents the five injection mechanisms including the `<system-reminder>` wrapping of CLAUDE.md; [CC-community-skills-landscape.md][cc-skills-landscape] — claude-code-best-practice open research questions.

### Auto Memory Architecture

```text
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index (first 200 lines loaded at session start)
├── debugging.md       # Topic file (loaded on demand)
├── api-conventions.md # Topic file (loaded on demand)
└── ...
```

- `<project>` derived from git repo — all worktrees and subdirectories within the same repo share one auto memory directory. Outside a git repo, the project root is used instead ([source][cc-mem])
- **MEMORY.md**: First 200 lines (or 25 KB, whichever comes first) loaded at session start. Content beyond that threshold is not loaded. Claude keeps it concise by moving detailed notes into topic files ([source][cc-mem])
- **Topic files** (e.g., `debugging.md`, `patterns.md`): Not loaded at startup. Claude reads them on demand using file tools when needed ([source][cc-mem])
- Machine-local; not shared across machines or cloud environments
- Claude reads/writes during session; "Writing memory" / "Recalled memory" indicators shown
- **Subagent support**: Subagents can maintain their own auto memory ([source][cc-sub])
- **Agent memory frontmatter**: Agent definitions in `.claude/agents/` support persistent memory via frontmatter configuration (v2.1.33) — scoped to that agent's execution, distinct from subagent auto-memory

#### Configuration

```json
{
  "autoMemoryEnabled": false
}
```

Or: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` env var. Toggle via `/memory` command in session ([source][cc-mem]).

**Requires Claude Code v2.1.59+** for auto memory. **Custom location**: set `autoMemoryDirectory` in `settings.json` (absolute or `~/`-prefixed path; honored only after the workspace-trust dialog) to relocate the memory directory from the default `~/.claude/projects/<project>/memory/` ([source][cc-mem]).

#### Auditing

Auto memory files are plain markdown — edit or delete at any time. Run `/memory` to browse loaded files, toggle auto memory, and open the memory folder ([source][cc-mem]).

### Key Behaviors

- **Import syntax**: `@path/to/file` expands imports in CLAUDE.md. Both relative and absolute paths supported; relative paths resolve relative to the containing file. Max 5 hops recursion ([source][cc-mem])
- **Size target**: Under 200 lines per CLAUDE.md for best adherence ([source][cc-mem])
- **`/init`**: Auto-generates starting CLAUDE.md from codebase analysis. If CLAUDE.md exists, suggests improvements rather than overwriting; `CLAUDE_CODE_NEW_INIT=1` enables an interactive multi-phase flow that also sets up skills/hooks and proposes changes before writing ([source][cc-mem])
- **`/memory`**: Lists all loaded instruction files; toggles auto memory; opens memory folder ([source][cc-mem])
- **Compaction survival**: CLAUDE.md fully survives `/compact` (re-read from disk). Instructions given only in conversation are lost after compaction ([source][cc-mem])
- **Sensitive instruction preservation**: As of v2.1.139, the compaction prompt explicitly asks the model to preserve sensitive user instructions carried in the conversation. This reduces the risk of security-relevant directives (e.g., credential handling rules, output filtering instructions) being dropped during mid-session compaction.
- **`InstructionsLoaded` hook**: Log exactly which instruction files load, when, and why — useful for debugging path-specific rules ([source][cc-mem])
- **First-time trust**: CC shows approval dialog for external `@` imports on first encounter in a project ([source][cc-mem])
- **AGENTS.md**: CC reads `CLAUDE.md`, not `AGENTS.md` — import (`@AGENTS.md`) or symlink it so both agents share one instruction source; `/init` folds an existing `AGENTS.md` (and `.cursorrules` / `.windsurfrules`) into the generated CLAUDE.md ([source][cc-mem])

## Auto-Dream — Background Memory Consolidation (Feature-Flagged)

Auto-Dream is a background memory consolidation engine that runs as a forked subagent between sessions. Where auto memory writes notes on-demand during active sessions, Auto-Dream performs a scheduled reflective pass — consolidating, deduplicating, and pruning accumulated memories. Analogous to REM sleep consolidating short-term memories into long-term storage.

**Provenance**: Sourced from `@anthropic-ai/claude-code@2.1.88` npm sourcemap exposure (2026-03-31). System prompt extracted by [Piebald-AI][piebald-dream]. Not officially documented by Anthropic. Feature-flagged via `isAutoDreamEnabled()`.

### Three Memory Layers

| Layer | Author | Trigger | Mechanism |
|-------|--------|---------|-----------|
| CLAUDE.md | Human | Manual edit | Loaded at session start |
| Auto memory | Claude (active) | On-demand during session | Writes to `MEMORY.md` + topic files |
| **Auto-Dream** | Claude (background) | Scheduled between sessions | Forked subagent consolidates existing memory |

### Four Phases

1. **Orient** — `ls` memory directory, read `MEMORY.md`, skim existing topic files to understand current state and avoid duplication
2. **Gather Signal** — search recent session transcripts (JSONL) and daily logs via narrow grep for user corrections, key decisions, contradicted facts
3. **Consolidate** — merge new signal into existing topic files, convert relative dates to absolute, delete contradicted facts, deduplicate
4. **Prune & Index** — trim `MEMORY.md` to ~25 KB / ~200 lines, enforce one-line entries (<150 chars), remove stale pointers, resolve cross-file contradictions

### Triggering Gates (ordered by cost)

All gates must pass before a dream runs:

| Gate | Threshold | Purpose |
|------|-----------|---------|
| Time | 24 h since last dream | Prevent over-dreaming |
| Sessions | >=5 recent transcripts | Ensure enough new signal |
| Lock | No concurrent consolidation | Prevent race conditions |
| Cooldown | 10-min scan throttle | Batch rapid session bursts |

### Constraints

- **Read-only bash** — dream subagent can inspect files but not modify the project
- **Disabled when**: Kairos mode active, remote mode, or auto memory turned off
- **Telemetry**: `tengu_auto_dream_fired`, `tengu_auto_dream_completed`, `tengu_auto_dream_failed`
- **User control**: abortable via background-tasks dialog; lock rolls back on failure
- **Surfaced**: around v2.1.83 under the `/memory` interface

Cross-ref: [CC-community-reimplementations-landscape.md](../../cc-community/CC-community-reimplementations-landscape.md) — CLAURST documents Auto-Dream's three-gate trigger and four-phase architecture

## Usage Considerations

| Aspect | Notes | Optimization Opportunity |
| ------ | ----- | ------------------------ |
| Autonomous loop context | Each iteration starts fresh; reads CLAUDE.md + auto memory | Working as designed — see [Context Quality Degradation][cc-extended-ctx-degradation] for headless invocation patterns |
| Cloud sessions | Auto memory is machine-local | Cloud sessions rely on committed CLAUDE.md only (see CC-cloud-sessions-analysis.md) |
| `includeGitInstructions` | `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1` removes built-in git workflow instructions from context (v2.1.69) | Saves context tokens in headless/autonomous loops that don't need commit/PR guidance |

For CLAUDE.md size, import chains, path-scoped rules, auto memory deduplication, `claudeMdExcludes`, and managed policy details, see the expanded sections above.

### Decision Rule

**CLAUDE.md and rules files are a project's primary instruction mechanism. Focus optimization on: (1) path-scoping rules to reduce context noise, (2) keeping the CLAUDE.md import chain under 400 total lines, (3) deduplicating auto memory vs manually maintained learnings files.**

### Potential Optimizations

1. **Path-scope role or subsystem boundaries** (see [glob syntax table](#glob-syntax) above):

   ```markdown
   ---
   paths:
     - "src/agents/**/*.py"
   ---
   # Agent Implementation Rules
   - Follow established agent patterns for this codebase
   ```

2. **Deduplicate auto memory vs learnings files**: Run periodic review to ensure auto memory doesn't accumulate stale patterns that contradict updated entries in a manually maintained learnings document.

3. **Use `InstructionsLoaded` hook** to audit which rules actually fire during typical workflows — prune rules that never trigger.

**Recommendation**: No structural changes needed for a project already using CLAUDE.md + rules + auto memory. Minor wins from path-scoping and deduplication reviews.

## Context Engineering Workflow (ACE-FCA)

The ACE-FCA (Advanced Context Engineering — Frequent Compaction Architecture) methodology was introduced by [Dex at hlyr.dev][hlyr-ace] (2025-08-29) as a structured approach to preventing context degradation in long agentic sessions. This repo's [.claude/rules/context-management.md](../../../.claude/rules/context-management.md) encodes this framework — the 40–60% utilization target and the context-quality ranking originate from the hlyr.dev source.

### Three-Phase Workflow with Human-Review Gates

```text
Research → [human review] → Planning → [human review] → Implementation
```

Each phase produces a **durable markdown artifact** before the next phase begins:

| Phase | Artifact | Content |
|---|---|---|
| Research | `research.md` | Sources, findings, open questions |
| Planning | `plan.md` | Approach rationale, step sequence, tradeoffs |
| Implementation | `implement.md` | Completed steps, current state, blockers |

Human review gates are ordered by downstream leverage: reviewing research first catches misframing before it propagates into planning and code. A wrong plan costs more to fix than a wrong research note.

### Frequent Intentional Compaction

Rather than letting context fill to exhaustion, ACE-FCA calls for distilling progress into a structured artifact at each phase boundary — or earlier when a compaction trigger is hit. The artifact schema:

- **End goal**: what the session is trying to accomplish
- **Approach rationale**: why this path was chosen
- **Completed steps**: what has been done and verified
- **Current failures**: what isn't working and what was tried
- **File and dependency map**: which files are involved and how they relate

### Generic Subagents for Discovery Isolation

Noisy discovery operations (file searches, grep sweeps, large JSON tool results) run inside generic subagents that return structured summaries only. This prevents search artifacts from polluting the parent window. Cross-ref: [Progressive Context Compaction in CC-agentic-harness-patterns-analysis.md][cc-harness-patterns]; [skills compaction budget in CC-skills-adoption-analysis.md][cc-skills-adoption]; [fresh-context-per-iteration in CC-ralph-enhancement-research.md][cc-ralph]; [1M-window compaction-avoidance in CC-extended-context-analysis.md][cc-extended-ctx].

### Context-Quality Ranking

When information is imperfect, the quality hierarchy determines what to drop ([source][hlyr-ace]):

| Rank | Information type | Effect |
|---|---|---|
| Worst | Incorrect information | Cascading errors (garbage in, garbage out) |
| Middle | Missing information | Model guesses, sometimes wrong |
| Least bad | Excessive noise | Dilutes signal; truth still present |

Better to have less correct information than more information with errors.

## References

- [CC Memory docs][cc-mem]
- [CC Skills docs][cc-skills]
- [CC Settings docs][cc-settings]
- [CC Subagent memory][cc-sub]
- [Getting Claude to Actually Read Your CLAUDE.md][hlyr-claude-md] — hlyr.dev, Dex, 2026-03-17
- [Advanced Context Engineering for Coding Agents][hlyr-ace] — hlyr.dev, Dex, 2025-08-29

[cc-mem]: https://code.claude.com/docs/en/memory
[cc-skills]: https://code.claude.com/docs/en/skills
[cc-settings]: https://code.claude.com/docs/en/settings
[cc-sub]: https://code.claude.com/docs/en/sub-agents#enable-persistent-memory
[piebald-dream]: https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/system-prompts/agent-prompt-dream-memory-consolidation.md
[hlyr-claude-md]: https://www.hlyr.dev/blog/stop-claude-from-ignoring-your-claude-md
[hlyr-ace]: https://www.hlyr.dev/blog/advanced-context-engineering
[cc-reverse-eng]: ../../cc-community/CC-reverse-engineering-landscape.md
[cc-skills-landscape]: ../../cc-community/CC-community-skills-landscape.md
[cc-harness-patterns]: ../agents-skills/CC-agentic-harness-patterns-analysis.md
[cc-skills-adoption]: ../agents-skills/CC-skills-adoption-analysis.md
[cc-ralph]: ../agents-skills/CC-ralph-enhancement-research.md
[cc-extended-ctx]: CC-extended-context-analysis.md
[cc-extended-ctx-degradation]: CC-extended-context-analysis.md#context-quality-degradation
