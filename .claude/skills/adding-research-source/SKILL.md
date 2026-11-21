---
name: adding-research-source
description: Add or enrich research in the ai-agents-research corpus. Add a source — research a tool / paper / protocol / agent first-party and place it as an analysis doc (placement, conventions, lint, one PR per topic) — when the user drops a URL/tool/paper to "add as a source". Enrich a topic — gap survey, up to three worktree lanes on separate files, two falsification passes, lead adds hub and index rows — when the user asks to deepen, extend or prune coverage of a topic or hub. For >~4 sources at once, use the batch workflow.
compatibility: ai-agents-research repo; needs make, git, gh, and uv (for polyfetch-scrape / doc-pipeline-engine escalation on dynamic/PDF sources). Designed for Claude Code.
metadata:
  author: qte77
  version: "0.2"
allowed-tools: Agent Bash Read Grep Glob Write Edit WebFetch
---

# adding-research-source

Two modes: **add a source** (below) and **[enrich a topic](#mode-enrich-a-topic)** (a hub or area
that needs depth, a pruning sweep, or several related gaps). To re-verify facts already in the corpus,
use the `refresh-docs` workflow (`.claude/workflows/refresh-docs.js`) instead.

## Mode: add a source

Add a source the way it's done consistently here: **research first-party → place correctly → write to
convention → lint → ship one PR per topic.** Judgment lives in *placement* and *sourcing*; the rest is
mechanical. Reference [CONTRIBUTING.md](../../../CONTRIBUTING.md) — don't duplicate its rules.

### Procedure (per source)

1. **Research first-party.** Dispatch an **Explore subagent** with the brief below (read-only). Never
   trust marketing — verify license/counts/version against the upstream README/LICENSE/releases
   (`gh api repos/<o>/<r>`). Dynamic/blocked pages → **polyfetch-scrape**; PDF/Office → **doc-pipeline-engine**
   (both via `uv run --directory`; see CONTRIBUTING Research Workflow).
2. **Place it** (decision tree):
   - Anthropic-native CC feature/internals → `docs/cc-native/<subdir>/CC-<topic>-analysis.md`
   - CC-**exclusive** community plugin/tool (CC is THE surface) → `docs/cc-community/CC-<topic>-analysis.md`
   - Cross-vendor tool/protocol/infra (CC = one of many) → `docs/non-cc/<section>/<topic>-analysis.md|-landscape.md`,
     where `<section>` is the subdir matching its `docs/non-cc/README.md` section (orchestrators, agents,
     coding-agents, knowledge-management, reference, context-memory, infrastructure, frameworks, protocols);
     add the index row under that section
   - Security / governance / identity / lifecycle → `docs/sdlc-lcm/<topic>-landscape.md`
   - Whatever the bucket: add a row to every matching hub listed in `docs/_topics/README.md`
     (pointer + one line, no content; one row per doc and section). Only CONTRIBUTING's hub
     exemptions may skip this, and `make check_coverage` holds the unhubbed count to its ratchet
   - **Extend, don't create** when a landscape already covers the area (dup-check with `git grep`);
     synthesis labels (e.g. "company brain") → extend, never standalone. Spans both dirs → deeper
     analysis in one, cross-ref from the other.
   - **Define nothing twice**: before defining a term, check [`docs/glossary.md`](../../../docs/glossary.md)
     and `git grep` for an existing definition; link the owner section instead of restating it.
3. **Write** per CONTRIBUTING: frontmatter (`title/purpose/created/updated/validated_links/status`; no
   body status badge), body sections, a **Sources table with reference-style links**, cross-refs. Hedge unverified
   claims; flag weak/secondary sources explicitly. State each claim at the level its evidence shows,
   *documented* / *announced* / *shipped* / *observed*, and never let a headline sentence claim more than
   the caveat below it.
4. **Index + changelog:** add the subdir README row (+ `cc-native/README` count for cc-native docs);
   add a `changelog.d/<ts>_<slug>.md` fragment.
5. **Lint:** `make lint` (markdown, status, coverage, frontmatter, actions, then links last). A URL
   you added that fails: recheck it locally and replace a dead one with its current canonical URL.
   Don't add `lychee.toml` excludes yourself; ask the owner.
6. **Ship:** branch `<type>/<slug>`; **commit by topic** (doc, then index/meta); PR; merge once CI is
   green. Owner rule for the link check: a failure counts as green only if `main` already has it or
   it passes when rechecked locally, and that check happens before the merge → prune the branch.

### Research-subagent brief (dispatch verbatim; one per source or tight cluster)

> Read-only. Use WebFetch + `git grep`/Read. Do NOT edit files or invoke skills. For `<URL(s)>`:
> canonical name; what it is (1–2 lines); **license from the LICENSE file, not marketing**;
> version/stars/date; 5–7 concrete first-party facts; one line on why it matters for an AI-agents / CC
> corpus. Then **coverage check**: `git grep -il '<name>'` in `docs/` — already covered? closest doc?
> Recommend placement (subdir + new-vs-extend) per the tree above. Calibrate grep on a term you know
> exists. **Flag anything you can't source first-party.** Put text in quotation marks only if it
> appears verbatim at the source. End with a **strongest claims** list: every superlative, "confirmed",
> "only" or bolded claim, each with its one piece of evidence. Return prose + compact blocks, no raw dumps.

### Batch mode (>~4 sources at once)

Run the workflow `scripts/batch-sources.workflow.js` (Workflow tool) — parallel first-party research +
**adversarial verify** across all URLs → structured findings (facts + placement + dup-flags). Then
write/ship each per steps 3–6. Needs explicit user opt-in (workflows spawn many agents).

## Mode: enrich a topic

For a hub in [`docs/_topics/README.md`](../../../docs/_topics/README.md), an area with several gaps, or
a pruning sweep under CONTRIBUTING
[§ Pruning entries](../../../CONTRIBUTING.md#pruning-entries-well-known-performance-optimised-filter).
The lead (you) plans, verifies and integrates; lanes write.

1. **Gap survey (read-only).** One Explore subagent surveys the hub and the docs it lists: what
   exists, what's missing, duplicate definitions, stale facts, entries failing the pruning rule. It
   returns a summary, not file dumps. Re-check every gap and absence claim yourself with `git grep`
   before acting on it.
2. **Plan the lanes.** At most three. Each lane owns separate files (no two lanes edit the same file)
   and gets a task list with a default for every decision. Collect shared evidence (for example
   `gh api` star counts and push dates) once and hand it to the lanes.
3. **Run the lanes.** Each lane is a subagent in its own git worktree, outside the main checkout.
   Brief = [references/lane-brief.md](references/lane-brief.md) with its placeholders filled in, plus
   the task list. Lanes commit and stop; they never touch hubs, indexes, the glossary or plans.
4. **Two falsification passes.** Run [references/falsifier-briefs.md](references/falsifier-briefs.md):
   pass 1 re-checks every claim at source; fix what it finds; then pass 2 checks the diffs for
   scope creep, lost facts, inconsistent rules, duplicate definitions and orphans. Verify each
   finding before applying it.
5. **Integrate.** Add the hub rows, README index rows and glossary rows the lanes proposed, then run
   `make lint` and `make test`. Ship one PR per lane or topic, with each plan row struck in the PR
   that ships it.

## Guardrails (why this exists)

- **Verify first-party** — this discipline caught real errors: stale KV min-token numbers, license/count
  drift, AP2/Humanity URL rot. A subagent's "fact" is advisory until re-checked.
- **Review the strongest claims first.** Subagents overclaim: in plan 0009, a docs page became a
  "confirmed shipped implementation", four sources became a "structural property", a paraphrase was
  put in quotation marks, and a synthesis presented dead workflows as live. Open the source for each
  superlative before merging; for a claim about a live system, check that it is still live.
- **Absence claims need a site-wide check.** "No repo", "no charter" or "no license" checked
  against one page is not evidence: plan 0009 got Flue's repo and AAIF's charter wrong this way, and
  a falsifier and its verifier repeated the AAIF error. Before writing "no X", check the site's
  navigation, its GitHub org and the linked repos.
- **One PR per topic**; don't mix content additions with reformatting.
- **Don't over-place** — the cc-vs-non-cc line is judgment. When genuinely unsure, ask the user rather
  than guess (placement calls get challenged: *opus-in-non-cc*, *firecrawl-in-cc-native*, *agents-cli-within-cc*).
- **Never trust marketing counts/license** — read LICENSE + live README/releases.
