---
name: adding-research-source
description: Research a new source (tool / paper / protocol / agent) first-party and add it to the ai-agents-research corpus as an analysis doc — placement, conventions, lint, one-PR-per-topic. Use when the user drops a URL/tool/paper to "add as a source" or asks to extend coverage. For >~4 sources at once, use the batch workflow.
compatibility: ai-agents-research repo; needs make, git, gh, and uv (for polyfetch-scrape / doc-pipeline-engine escalation on dynamic/PDF sources). Designed for Claude Code.
metadata:
  author: qte77
  version: "0.1"
allowed-tools: Agent Bash Read Grep Glob Write Edit WebFetch
---

# adding-research-source

Add a source the way it's done consistently here: **research first-party → place correctly → write to
convention → lint → ship one PR per topic.** Judgment lives in *placement* and *sourcing*; the rest is
mechanical. Reference [CONTRIBUTING.md](../../../CONTRIBUTING.md) — don't duplicate its rules.

## Procedure (per source)

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
   - Whatever the bucket: if the doc is about memory, knowledge graphs, RAG, code tooling or
     visualization, add a row to the matching `docs/_topics/<hub>.md` (pointer + one line, no content)
   - **Extend, don't create** when a landscape already covers the area (dup-check with `git grep`);
     synthesis labels (e.g. "company brain") → extend, never standalone. Spans both dirs → deeper
     analysis in one, cross-ref from the other.
3. **Write** per CONTRIBUTING: frontmatter (`title/purpose/created/updated/validated_links/status`; no
   body status badge), body sections, a **Sources table with reference-style links**, cross-refs. Hedge unverified
   claims; flag weak/secondary sources explicitly. State each claim at the level its evidence shows,
   *documented* / *announced* / *shipped* / *observed*, and never let a headline sentence claim more than
   the caveat below it.
4. **Index + changelog:** add the subdir README row (+ `cc-native/README` count for cc-native docs);
   add a `changelog.d/<ts>_<slug>.md` fragment.
5. **Lint:** `make check_docs` (run it **directly** — `make lint` aborts at the lychee flake before
   markdownlint) then `make check_links`. A URL you added that 404s/bot-blocks → *propose* a
   `lychee.toml` exclude with a note; never admin-merge past a broken link you introduced.
6. **Ship:** branch `<type>/<slug>`; **commit by topic** (doc, then index/meta); PR; green CI → owner
   `gh pr merge --squash --admin` (lychee not required — merge past *pre-existing* rot only) → prune.

## Research-subagent brief (dispatch verbatim; one per source or tight cluster)

> Read-only. Use WebFetch + `git grep`/Read. Do NOT edit files or invoke skills. For `<URL(s)>`:
> canonical name; what it is (1–2 lines); **license from the LICENSE file, not marketing**;
> version/stars/date; 5–7 concrete first-party facts; one line on why it matters for an AI-agents / CC
> corpus. Then **coverage check**: `git grep -il '<name>'` in `docs/` — already covered? closest doc?
> Recommend placement (subdir + new-vs-extend) per the tree above. Calibrate grep on a term you know
> exists. **Flag anything you can't source first-party.** Put text in quotation marks only if it
> appears verbatim at the source. End with a **strongest claims** list: every superlative, "confirmed",
> "only" or bolded claim, each with its one piece of evidence. Return prose + compact blocks, no raw dumps.

## Batch mode (>~4 sources at once)

Run the workflow `scripts/batch-sources.workflow.js` (Workflow tool) — parallel first-party research +
**adversarial verify** across all URLs → structured findings (facts + placement + dup-flags). Then
write/ship each per steps 3–6. Needs explicit user opt-in (workflows spawn many agents).

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
- **"Not found" is not "refuted."** A vendor page searched and found silent on a claim's exact
  wording is `checked-absent` — absence, not refutation. Only mark a claim `refuted` when a vendor
  page states the *opposite* of the claim. Conflating the two overstates how many self-descriptions
  were wrong. (Worked example above: 6 of 11 unverifiable rows were `checked-absent`, only 3 of 85
  rows were flatly `refuted`.)
- **Name the bucket, not just the verdict.** When fact-checking a batch of claims, tag each one
  with both a verdict (`refuted`/`partly`/`unverifiable`/`supported`) and a bucket describing how
  the check went (`checked` / `not-checked` / `checked-absent` / `secondary-only` / `blocked`).
  Report both — a results table that only shows verdicts hides whether "unverifiable" means
  "nobody looked" or "we looked hard and found nothing."
- **Scope-stretch check.** Before accepting a claim as supported, check whether it generalizes
  beyond what the cited evidence literally shows — a narrower scope, a different product, or an
  inference layered on top of a quote. Tag the gap explicitly (e.g. "confirmed for product X; the
  claim's broader 'any product in this family' framing is not") rather than letting a quote-backed
  detail carry an unquoted generalization.
- **A vendor self-description is a claim, not a source.** When the input being checked is an AI
  assistant's own description of a product (or a practitioner how-to that repeats one), that
  description is itself an unverified claim requiring the full first-party challenge pass — never
  treat it as evidence on its own, even when it sounds confident or specific.
- **Timeline claims need the vendor's own per-item roadmap feed.** For a GA/preview/retirement
  date, prefer the vendor's dedicated per-feature feed (e.g.
  `microsoft.com/microsoft-365/RoadmapFeatureRSS/<id>`) over a general roadmap search page or a
  third-party mirror — a mirror or search snippet can disagree with the feed on the exact date, and
  the feed is the thing the vendor actually commits to.
