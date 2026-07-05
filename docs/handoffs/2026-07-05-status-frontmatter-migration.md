---
title: Handoff — status → frontmatter migration (#348)
purpose: Onboard a fresh session to execute the deferred status-in-frontmatter migration.
created: 2026-07-05
updated: 2026-07-05
---

**Status**: Reference (handoff)

## TL;DR

Execute **#348**: move each doc's maturity from the body `**Status**:` badge into a frontmatter
`status:` token, relocate any decoration into a body `**Details:**` line, delete the badge. The
**full plan + complete source map** (so you don't re-explore) is
[`docs/plans/2026-07-05-status-frontmatter-migration.md`](../plans/2026-07-05-status-frontmatter-migration.md).
Read it first — it has the exact grep commands, counts, file:line lists, vocabulary, and transform rule.

## Before you touch anything

- **This is not urgent — it's YAGNI.** Nothing reads `status:` today (verified: zero tooling). Confirm
  that's still true (`git grep 'Status\*\*' -- scripts .github ui Makefile` → expect 0). If it's still
  YAGNI, consider building the *consumer* first (README status column / dashboard / graphify facet) and
  migrating after, so the format is validated by real use. If the maintainer wants the convention landed
  regardless, proceed.
- **Scope reality:** 144 docs. ~52 are clean radar tokens (trivial). **~88 pack license/GA/version/vendor
  into the badge** — those need the split-and-relocate transform (judgment-y). Don't underestimate this.

## How to run it (staged — do NOT do one mega-PR)

1. One PR **per `docs/` subdir**, in this order: `cc-native/` → `non-cc/` → `cc-community/` →
   `sdlc-lcm/`+`plans/` → convention docs (CONTRIBUTING §1/§2 + architecture.md).
2. For each subdir, apply the plan's **Transform (per doc)**. The decorated docs concentrate in `non-cc/`
   (tool analyses) and `cc-native/plugins-ecosystem|configuration` — **spawn an Agent subagent per subdir**
   to apply + self-review the split (safer than serial hand-edits at this volume).
3. Per PR: changelog fragment; `make lint` + `make test` green; invariants `git grep -c '^\*\*Status\*\*:'
   <subdir>` → 0 and every ex-badge doc has `^status:`. Admin-merge (signatures) → prune.
4. Do the **convention-doc PR last** (CONTRIBUTING §2 rewrite + architecture.md) so the docs match reality
   only once the corpus is migrated.

## Already done (this session, PR that shipped this handoff)
- Fixed the one **true** frontmatter↔badge mismatch: `CC-vlm-screen-sharing-landscape.md` (badge `Assess` →
  `Research (informational)` to match its `status: research` + sibling landscapes).
- The other 2 flagged "mismatches" (`autoagent`, `openviking`) are **not** bugs — fm `research` (adoption)
  vs a release-metadata badge; they resolve naturally in the migration. No pre-fix needed.

## Gotchas (from the plan's Special cases)
- **Leave** `agent-observability-methods-analysis.md:61` (that `**Status**:` describes an upstream project,
  not the doc). **Remove** the duplicate `cocoindex-analysis.md:59`. **Leave** `docs/archive/**` (already
  `status: archived`). Don't add status to the 39 badge-less docs (READMEs/specs/auto-gen).
- Relocating a badge that contains a `[link]` ref-style link: keep the link def, or lychee/markdownlint
  will flag an orphaned reference.
