---
title: Migrate doc status into frontmatter (drop the body badge)
status: approved
issue: 348
created: 2026-07-05
updated: 2026-07-05
---

**Status**: Reference (plan)

Durable plan for **#348** — moving doc maturity from the body `**Status**:` badge into a
frontmatter `status:` field. **Approved but deferred** (see Priority). This doc carries the full
context map so a fresh session executes without re-gathering. Handoff: [`docs/handoffs/2026-07-05-status-frontmatter-migration.md`](../handoffs/2026-07-05-status-frontmatter-migration.md).

## Priority — read first (it's YAGNI today)

**Nothing reads `status:`** — verified: zero tooling parses the badge or a `status` field (see
Source Map §6). There is no consumer, so this migration is **not urgent**. Recommended order:
**build a consumer first** (a README status column, a maturity dashboard, or graphify faceting),
*then* migrate so the format is validated by real use. The one genuinely-valuable slice — the
frontmatter↔badge **mismatches** — is handled separately (see §Mismatches; 1 fixed in this PR).

## Goal

Every doc that has a body `**Status**:` badge → a clean `status:` token in frontmatter; the
decoration (license/GA/version/vendor/links) relocates into the body; the badge line is deleted.
`docs/plans/README.md:26` already documents `status ∈ draft|approved|done|superseded` for plan docs,
and `CONTRIBUTING.md:214` uses `status: archived` for archives — so frontmatter status has precedent.

## Source map (regenerate/verify with these — don't re-explore)

- **All badges:** `git grep -n '^\*\*Status\*\*:' -- 'docs/**' ':!docs/archive/**'` → **144 docs** (2026-07-05).
- **Frontmatter status already present:** `git grep -n '^status:' -- 'docs/**'` → **21 files** (19 dual + 2 archive).
- **Convention text to rewrite:** `CONTRIBUTING.md` §1 frontmatter block **lines 9-27**, §2 "Status Badge" **lines 29-44**; archiving note **line 214**. `docs/architecture.md` "Frontmatter Conventions" **lines 67-80** (add `status`; also note the pre-existing `description:` vs CONTRIBUTING `purpose:` mismatch — flag, don't silently fix).
- **Tooling verdict (§6):** `git grep 'Status\*\*' -- scripts .github ui Makefile` → **0 hits**. Frontmatter parsers (`.github/scripts/lib/changelog.py:26-47` keys off `purpose:`; `learnings-aggregator.py:69-75` writes title/description/updated/source) **never touch status**. `scripts/pages_build.py`, `render-graph-page.py`, README-index generation, lint — none read status. **Migration is pure text; nothing breaks.**

### Badge value distribution (144 lines)

Clean radar tokens **~52**: `Assess` 33 (doc-level) · `Adopt` 11 · `Trial` 5 · `Hold` 3.
Decorated / non-radar **~88** — the ones needing the split-and-relocate transform:
`Research (informational)` 28 · `Research (…unique tail…)` ~13 · `Research preview (…)` 7 · `Reference (…)` 8 ·
`Trial | GA/License/Vendor…` 8 · `Open-source (<license>), active development` 8 · `Generally available (…)` 3 ·
`Beta (…)` 3 · `Landscape research (…)` 2 · singletons (Stable/Verified/Available/Public Preview/Proprietary/
Source-available/Adopted (…)/Active development/Active upstream bug/Completed/Done…) ~18.

### Status vocabulary (faithful — do NOT re-assess adoption)

`status:` = normalized leading token of the existing badge (kebab-case). Controlled set:
`adopt · trial · assess · hold · research · reference · research-preview · beta · generally-available ·
stable · public-preview · available · verified · proprietary · source-available · open-source ·
active-development · completed · done · archived`. Fold synonyms ("Research (informational)"→`research`,
"Generally available"→`generally-available`).

## Transform (per doc)

1. Extract the leading status phrase (up to the first `|`, `(`, `,`, `.`, `—`, `:` that begins decoration) → normalize to a vocab token → add `status: <token>` to frontmatter after `validated_links`.
2. Relocate the decoration into a body line right after the frontmatter close, only if it carries real info: `**Details:** <remainder>` (preserve license/GA/version/vendor/`[link]` refs verbatim). Drop pure filler (`(informational)`, `(not implementation requirements)`). The ~52 clean docs have no remainder.
3. Delete the `**Status**: …` line + one adjacent blank, leaving `---` → blank → `## Heading`.

## Mismatches (frontmatter `status:` vs body badge) — 3 flagged; on inspection only 1 is a true bug

- **CC-vlm-screen-sharing-landscape.md** — fm `research` vs badge `Assess` → **FIXED in this PR** (badge → `Research (informational)`, matching fm + sibling landscapes).
- **autoagent-analysis.md**, **openviking-analysis.md** — fm `research` vs badge `Open-source (<license>), active development`. NOT a true contradiction: fm = adoption-status `research`; badge = release/license metadata (different axis). Resolves naturally in the migration (keep `status: research`, relocate the badge to `**Details:**`). No change now.

## Special cases

- **19 dual docs** (already `status:`, listed via the §Source-map grep): keep the fm token, drop the badge, relocate decoration.
- **agent-observability-methods-analysis.md:61** — a `**Status**:` inside a body section describing an *upstream project*, NOT the doc's status → **leave**.
- **cocoindex-analysis.md:59** — a duplicate second `**Status**: Assess` → **remove**.
- **docs/archive/** (already `status: archived`, no badge) → leave. Docs with **no badge** (39: READMEs, specs, auto-gen) → out of scope.

## Staging (one PR per subdir; same green-CI → admin-merge flow)

`cc-native/` (largest) · `non-cc/` (most decorated/license badges) · `cc-community/` · `sdlc-lcm/`+`plans/` · then the convention docs (CONTRIBUTING + architecture). The decorated docs concentrate in `non-cc/` + `cc-native/plugins-ecosystem|configuration` — batch those with extra review. **Recommended:** an Agent subagent per subdir applies the transform + self-reviews before each PR (the decoration split is judgment-y); changelog fragment per PR.

## Verification (per PR)

1. `make lint` (markdownlint over edited docs — badge removal + `**Details:**` line must keep MD022/MD041 clean; lychee: relocated `[link]` refs must still resolve; no orphaned reference-style defs) → 0 errors.
2. `make test` → 69/69 (no modules touched).
3. Invariants: `git grep -c '^\*\*Status\*\*:' <subdir>` → 0; every ex-badge doc has `^status:`.
4. `/security-review` → none (docs only).
