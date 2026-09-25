---
title: Backlog triage — open PRs, branches and issues (2026-09-23)
status: draft
issue: 438, 433, 417, 410, 254, 347, 348, 309, 382, 232
created: 2026-09-23
updated: 2026-09-23
---

**Status**: Reference (plan)

Read-only audit of every open PR, every non-main branch and every open issue, run 2026-09-23 by two
subagents. The Source map tables below are the **snapshot taken at audit start**; what has happened
since is in Current status and the Remaining work table. In scope: PRs/issues authored by
`qte77`, GitHub Actions bots and Dependabot (all 29 open PRs and all 10 open issues qualified).

## Current status

- **Shipped (2026-09-23):** 23 superseded bot PRs closed, including the 7 community-triage PRs
  (#415–#440), once every row they alone carried was confirmed present in main's `triage/`. Merged
  with owner `--admin` squash: #445 (this plan), #446 (ccsync), #447 (link rot, closes #254), #434
  (actions bump), #442, #444, #424, #418, #443, then #448–#451 and #453 (plan bookkeeping,
  permission-rule fix, ccsync docs, sandbox-runtime repoint). **v0.8.0 released** (#454, tag
  `v0.8.0`, GitHub Release published). #433 closed with evidence; #309 boxes ticked and Phase 1
  layout commented; #347 scope commented; plan 0001 tracked in #452.
- **Shipped (2026-09-24):** #457 (owner-approved lychee excludes, rows 15 + 21b), #458 (reusable
  tag/publish, row 10), #459 (cross-session messaging doc, row 8, closes #438), #460–#478 (row 20:
  18 batch PRs, **123 topics added, 7 dropped**, 33 new docs), #479 (Runtype, owner request).
- **Shipped (2026-09-24, cont.):** #480 (plan + CONTRIBUTING), #481 (indexes for the 33 new docs + 3
  previously unindexed), **v0.9.0 released** (#482; first run of the reusable tag/publish → #347 closed).
- **Shipped (2026-09-24, owner defaults):** #462 (row 9, closes #410), #484 (coding-harness-eval rename, supersedes #456), #485 (row 22), #486 (shared plan usage + local-tool blind spots); closed #382 and #232; opened qte77/.github#44 (tag reusable workflows) and analyze-stock-kpi#413 (longs/shorts decision).
- **Next, in order:** rows 12 (#309 faithful-9), then 11 (#348, deferred until a status consumer exists).
- **Owner gates:** #462 scope (a/b/c), closing #382, deciding #232, #309 scope, PR #456 (another
  session's `coding-harness-eval` rename).
- **Commands:** prefix every `gh`/`git` network call with `env -u GH_TOKEN -u GITHUB_TOKEN`
  (invalid env tokens shadow the stored credential).
- **Watch-outs:**
  - Squash-merges break ancestry → judge "already landed" by content (`git cherry main <branch>`),
    not `git branch --merged`.
  - main requires strict up-to-date branches → merge PRs **one at a time**: `gh pr update-branch`,
    wait for the required CodeFactor check, then `gh pr merge --squash --admin --delete-branch`
    (the owner's `--admin` gets past required signatures; see Merge gate).

## Source map

### Open PRs (29)

Each monitor keeps a cumulative state file, so the newest PR in a category contains the older ones.

| Category | Newest (merge) | Superseded (close) | State file | Supersession evidence |
|---|---|---|---|---|
| changelog-triage | #442 | #413, #419, #423, #427, #430, #435, #439 | `.github/state/native-monitor-state.json` | **Content-verified**: tokens from #413's triage file present in #442 |
| community-triage | #443 | **not superseded** — #415, #421, #425, #428, #431, #436, #440 | `community-monitor-state.json` | Item-key check 2026-09-23: each older PR has 2–6 table rows missing from #443 |
| learnings-aggregation | #444 | #416, #422, #426, #429, #432, #437, #441 | `learnings-aggregator-state.json` | Same 8 files, one-line updates each; #444 carries the latest values |
| outage-archive | #424 | #414, #420 | `outages.jsonl` / `outage-stats.md` | Item-key check 2026-09-23: every outage `id` in #414/#420 is in #424 |
| rxiv-paper-triage | #418 | — | rxiv-only files | Sole PR in category |
| Dependabot actions bump | #434 | — | — | Lint/lychee + rxiv `eval/evaluate` jobs fail. Logs read later: lychee = corpus-wide rot; rxiv = GitHub Models outage (`HTTP 410 … github_models_retirement_brownout`), not missing secrets (see Merge gate) |

### Branches

| Branch | State | Evidence |
|---|---|---|
| `feat/ccsync-and-profile-perms` | local only, 1 commit ahead (506b91e, `scripts/cc-multi-account.sh` +69), no PR | `ls-remote` empty; missing `changelog.d/` fragment |
| `docs/a11y-tree-and-agent-browser` | local only, content on main | PR #378 merged 2026-07-17; `git cherry` equivalent |
| `feat/doc-status-validator` | local only, content on main | PR #380 merged 2026-07-17; `git cherry` equivalent |
| `tmp/graph-replay` | local only, never pushed | content on main via b168436; `git cherry` equivalent |

### Open issues (10), by cluster

| Cluster | Issue | ROI | Feasibility | Gate | Evidence |
|---|---|---|---|---|---|
| Docs gaps | #438 ListAgents / cross-session messaging | H | M | agent | Only `ListPeers` in `docs/cc-native/agents-skills/CC-agent-teams-orchestration.md`; owner comment 2026-09-08 widens scope to the whole feature (v2.1.224) |
| Docs gaps | #433 robots.txt Content-Signal + llms.txt | M | H | agent | No robots/llms file in repo; `.github/workflows/gh-pages.yaml:44` copies `ui/.` to site root |
| CI/monitors | #417 link-rot report | M | H | agent + owner | claude.com 404 (repoint); ampcode.com HTTP/2 error seen once; producthunt 403 (bot-block → owner-approved exclude) |
| CI/monitors | #410 feed.xml as changelog-monitor trigger | M | H | agent | Decision narrowed in thread; no `feed.xml` refs in workflows/scripts |
| CI/monitors | #254 drop vibekanban.com lychee exclude | L | H | agent | Still at `lychee.toml:89`; site now says Vibe Kanban is sunsetting → stale-fact risk in `CC-office-worker-workflows.md` |
| Release infra | #347 adopt qte77/.github reusable release workflows | M | H | agent | Blocker qte77/.github#33 merged 2026-07-17; `tag-release.yaml` / `publish-release.yaml` / `bump-my-version.yaml` not yet using it |
| Trackers | #348 status → frontmatter migration | M | H | agent | Validator shipped (#380); 158 body badges remain (excl. `docs/archive/`); plan: [2026-07-05-0003-status-frontmatter-migration.md](2026-07-05-0003-status-frontmatter-migration.md) |
| Trackers | #309 project restructure | H | M | agent | Phase 2 done (#361), Phase 3 done (topics 14/14), "track #308" done (#308 closed); Phase 1 (`non-cc/` subdivision, 72 flat entries) not started. The "staged" Phase 1 plan referenced in agent memory was **not found** in `docs/plans/` |
| Close-candidate | #382 semantic-search research | — | — | owner | Downstream azure-doc-workflows#165 closed/completed with the recommended approach |
| Owner decision | #232 paid automation | — | — | owner | Needs API keys + recurring spend if activated |

### Merge gate (verified 2026-09-23)

Ruleset `13630270` on `main`: the only required status check is **CodeFactor**, plus required
signatures, linear history and a `code_quality` rule; 0 approvals. The bot PRs show `BLOCKED` because
their commits are unsigned (#442 head `verified:false, reason:"unsigned"`) → owner `--admin` merge.
The lychee failures on #445–#447 are corpus-wide rot that none of the three PRs touches. #434's two
failures are environmental: the same lychee rot, plus a GitHub Models outage (`HTTP 410 …
github_models_retirement_brownout`).

New rot found in those runs (not yet fixed): `github.com/anthropic-experimental/sandbox-runtime/issues/139`
404 ×4 in `docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md`; pwc.com PDF 403 in
`agentic-sdlc-patterns.md`; beyondtrust.com 403 in `agent-identity-auth-landscape.md` (this one was
already failing on main's 2026-07-23 run).

### Pre-stage briefs (rows 8–12)

Each brief was produced by the triage subagent on 2026-09-23. The spot-checks marked ✓ were re-verified in the main session.

- **#438 (row 8):** first-party source `https://code.claude.com/docs/en/cross-session-messaging` ✓
  (v2.1.224+ macOS/Linux/WSL2, v2.1.234+ native Windows; sub-gates v2.1.225/232/236/239/247/248/251/271
  inline) and `https://code.claude.com/docs/en/whats-new/2026-w32` (ship week). Existing coverage:
  `docs/cc-native/agents-skills/CC-agent-teams-orchestration.md` §"UDS Inbox (Unreleased)" (~L362–395,
  `ListPeers` row) — keep separate from §"Coordinator Mode (Unreleased)". **Default:** new
  `docs/cc-native/agents-skills/CC-cross-session-messaging-analysis.md`, plus a cross-ref in the UDS Inbox
  section correcting its "Unreleased" framing.
- **#410 (row 9):** the feed is `https://github.com/anthropics/claude-code/releases.atom` (entry `id`
  `tag:github.com,2008:Repository/937253475/vX.Y.Z`, per-entry `updated`). Touch
  `.github/workflows/cc-changelog-monitor.yaml:30-35` (add a feed fetch step) and
  `.github/scripts/lib/changelog.py` (parse `id`/`updated` with stdlib `xml.etree`). Use `id` for
  dedup/trigger; CHANGELOG.md stays the only content source.
- **#347 (row 10), narrowed 2026-09-23 to the estate convention:** the estate convention
  (`qte77/qte77/docs/doc-structure.md:86-92`) names only the reusable **`tag-release`** and
  **`publish-release`**, triggered by a human-merged bump PR. It does not name the reusable
  `bump-version.yml`. So: keep this repo's own `bump-my-version.yaml`, which opens the bump PR for
  the owner to merge, and replace only `tag-release.yaml` and `publish-release.yaml` with `uses:`
  calls to `qte77/.github` @ `613b950b4045cc099ca23f8b7344459c3dc22cb3` ✓. Pin with a date comment,
  as `qte77/qte77` does (`# 2026-MM-DD`): the repo has no tags, so Dependabot can't advance this pin
  and it needs a manual refresh. Overrides: tag-release `version_regex: '^current_version = "(.*)"'`
  (`pyproject.toml:14` ✓), because the default regex would silently miss; publish-release needs none.
  Grant `issues: write` in both callers, even though they don't use it: the reusable notify job needs
  it at startup (`qte77/qte77` commit `7bdf439`).
- **#348 (row 11):** PR 1 = `docs/cc-native/`, **61 docs** ✓ (configuration 15, agents-skills 9,
  plugins-ecosystem 9, ci-remote 8, sessions 7, context-memory 5, sandboxing 5, model-internals 3). List:
  `git grep -l '^\*\*Status\*\*:' -- docs/cc-native/`. Transform per plan 0003. **Default:** split by
  feature subdir. The plan's two special-case files are in `non-cc/` (PR 2).
  **Advisor verdict (2026-09-23): keep deferred.** The validator checks `status:`, but nothing renders
  it yet. Build the consumer first (plan 0003 §Priority), so row 11 runs after rows 8–10.
- **#309 Phase 1 (row 12):** `docs/non-cc/` has 70 docs + README in 9 README sections; 3 docs are
  unindexed (`agents-md-cookbook-analysis.md`, `moss-self-evolving-agent-analysis.md`,
  `on-device-semantic-search-landscape.md`). **Default, per the advisor verdict: mirror the README's
  existing 9 sections as 9 subdirs** (the "faithful-9" layout already decided in earlier sessions),
  NOT the issue body's 6. That removes the three mapping calls a 6-way split forces (where
  Infrastructure goes, how to split Agents, a too-thin `visualization/`), and the README is already
  the taxonomy readers use. The 3 unindexed docs join their nearest section. Record 6 → 9 on #309.
  Repoint surface: 60 files outside `non-cc/` (493 occurrences) plus ~40 sibling links; lychee is the
  backstop. **Default:** one PR per subdir.

### Screenshot sources (rows 17–20)

The owner's screenshot dump (`/workspaces/temp/ai-agents-research/`, 1,433 JPGs, 2026-06-24 →
2026-09-21, mostly LinkedIn/X posts) is mined for **leads**: URLs, handles, tool names and
descriptions. **Screenshots are never a source.** Every claim that enters the corpus is verified
against a first-party URL (vendor docs, repo, paper) found from the lead. Working files live
**outside the repo** (they name people from LinkedIn), at `/workspaces/temp/ai-agents-research-triage/`:

- `shots-merged.tsv` — pass 1 tags: 675 in scope / 241 maybe / 504 out / 9 unreadable / 4 untagged.
- `detail/chunk-NNN.jsonl` — pass 2 (in scope + maybe + unreadable + untagged = 929 images):
  `file, scope, urls[], handles[], entities[], description, author, date`, all transcribed as seen;
  truncated URLs are marked `[truncated]`.

Placement follows CONTRIBUTING's classification rules and prefers extending existing docs.
Coverage is checked with `git grep`, calibrated against a known term first; hits only in
`docs/research/rxiv-agentic-papers.md` or `docs/archive/` don't count as coverage.

**Placement results (row 19, 2026-09-23).** 883 in-scope and maybe leads, pre-grouped by GitHub
repo, arXiv ID or first-party domain, became **682 topics**: 292 extend an existing doc, 73 need a new
doc, 43 are already covered, and 274 are out of scope. Priority split: 128 H, 194 M, 355 L. The 80
LinkedIn short links were resolved to their real targets with polyfetch (`lnkd-resolved.tsv`). A
spot-check of 10 high-priority "new doc" placements found no missed coverage. Files:
`placement/merged.json` (all topics) and **`placement/h-priority.tsv` (128 H topics; 125 have a
first-party starting URL)**, both in the working folder above. The 128 H topics by area: non-cc 61,
sdlc-lcm 30, cc-native 21, cc-community 16. The most-extended targets across all topics are:

| Target doc | Topics |
|---|---|
| `docs/non-cc/frameworks/agent-frameworks-infrastructure-landscape.md` | 61 |
| `docs/non-cc/infrastructure/semantic-layers-data-catalog-landscape.md` | 18 |
| `docs/sdlc-lcm/agentic-engineering-disciplines-landscape.md` | 16 |
| `docs/non-cc/infrastructure/web-scraping-extraction-landscape.md` | 15 |
| `docs/non-cc/infrastructure/llm-routers-gateways-landscape.md` | 10 |
| `docs/sdlc-lcm/evaluation-data-resources-landscape.md` | 10 |

**Entry rule for row 20:** a topic enters the corpus only if research finds a first-party URL that
backs the claim. A lead with only LinkedIn/X behind it is dropped, not hedged in. Research in batches
of topics per target doc (one PR per target), starting with the H list. Fetch JS-rendered,
bot-blocked or LinkedIn pages with polyfetch (`uv run --directory /workspaces/qte77/polyfetch-scrape
polyfetch fetch <url> --show-body`) when WebFetch fails.

## Remaining work

The only list of open work in this plan. Strike a row in the PR that ships it.

| # | Item | Gate | Done-when |
|---|---|---|---|
| ~~1~~ | ~~Close superseded changelog/learnings/outage bot PRs~~ | agent | Done 2026-09-23: 16 closed (#413–#439 → #442, #416–#441 → #444, #414/#420 → #424), each verified by item key |
| ~~1b~~ | ~~Community-triage PRs #415, #421, #425, #428, #431, #436, #440~~ | owner | Done 2026-09-23: closed, branches deleted. After #443 and #442 merged, all 6 rows they alone carried are in main's `triage/` |
| ~~2~~ | ~~Delete 3 merged local branches~~ | agent | Done 2026-09-23 (`git cherry` equivalent before deleting) |
| ~~3~~ | ~~#309: tick Phase 2, Phase 3 and "track #308"~~ | agent | Done 2026-09-23; issue stays open for Phase 1 |
| ~~4~~ | ~~Ship `feat/ccsync-and-profile-perms`~~ | owner | Done 2026-09-23: #446 merged |
| ~~5~~ | ~~#417: claude.com 404 removed; recheck ampcode.com~~ | agent | Done 2026-09-23: ampcode.com HTTP/2 error recurred (weekly run + full local run) yet returns 200 via polyfetch → lychee incompatibility, moved to 21b |
| ~~6~~ | ~~#433: Content-Signal / llms.txt~~ | owner | Done 2026-09-23: closed with evidence — host-root robots.txt already carries Content-Signal; no llms.txt for now |
| ~~7~~ | ~~#254: vibekanban exclude dropped~~ | owner | Done 2026-09-23: #447 merged, #254 closed |
| ~~8~~ | ~~#438: cross-session messaging doc~~ | agent → owner review | Done 2026-09-24: #459 merged, #438 closed. Windows gate stated as a conflict (docs v2.1.234 vs CHANGELOG v2.1.239) |
| ~~9~~ | ~~#410: releases.atom trigger~~ | agent | Done 2026-09-24: #462 (option c, owner default): feed-covered versions gated by the id ledger, CHANGELOG cutoff fallback for feed gaps; 84 → 102 tests; main() complexity kept at B (8) for CodeFactor; #410 closed |
| ~~10~~ | ~~#347: reusable `tag-release` + `publish-release`~~ | agent | Done 2026-09-24: #458; verified by the v0.9.0 run (tag + publish via reusable workflows); #347 closed |
| 11 | #348: migration PR 1 of ~5 (one subdir) | agent → owner review | PR open, validator passes |
| ~~12~~ | ~~#309 Phase 1: `non-cc/` subdivision~~ | agent | Done 2026-09-25: #489 (tested move tool + Orchestrators) + #490–#497 (one PR per section); 93 docs in 9 subdirs mirroring the README sections; all relative links rewritten, lychee offline 0 errors every step; tool/map removed after use (recoverable from 7179e0a) |
| 12b | #309 Phase 1 remainder: resolve DeepWiki + CocoIndex duplication (one canonical analysis + landscape pointer); add `docs/_topics/` cross-subject hub indexes | agent | Both dups resolved with inbound links repointed; hub pages exist and are linked from README |
| 23 | Full knowledge-graph rebuild (row 20 added 123 topics + 33 docs; also refreshes the stale `source_file` metadata in `ui/graph.html` after the restructure) | agent | Uniform full rebuild via `/graphify` → `make graph-page` → Pages deploy; node count reported |
| ~~13~~ | ~~Merge newest bot PRs #442, #443, #444, #424, #418~~ | owner | Done 2026-09-23: all five merged, branches deleted |
| ~~14~~ | ~~#434: read failed logs, then merge~~ | owner | Done 2026-09-23: failures were environmental (lychee rot, GitHub Models outage); merged |
| ~~15~~ | ~~#417: approve producthunt exclude~~ | owner | Done 2026-09-24: #457 (exact-URL exclude) |
| 16 | Close #382; decide #232; decide #309 scope (keep vs. split) | owner | Each issue closed or updated with decision |
| ~~17~~ | ~~Screenshot pass 1: tag 1,433 images in / maybe / out~~ | agent | Done 2026-09-23: `shots-merged.tsv` (spot-checked) |
| ~~18~~ | ~~Screenshot pass 2: extract URLs, handles, entities, descriptions~~ | agent | Done 2026-09-23: 921 of 929 records (8 missing), 726 URLs (51 truncated); lnkd.in short links resolved to real targets via polyfetch → `lnkd-resolved.tsv` |
| ~~19~~ | ~~Cluster pass-2 leads into topics; coverage; placement~~ | agent | Done 2026-09-23: 682 topics; results in the Screenshot sources section |
| ~~20~~ | ~~Research the 128 H topics~~ | agent | Done 2026-09-24: #460–#478, 18 disjoint-doc batches; 123 added, 7 dropped (4 without a first-party source, 3 verified but out of batch scope → row 22); 33 new docs; all 70+ cited GitHub repos verified to exist; results at `research/results.json` |
| ~~22~~ | ~~Row-20 follow-ups: 3 verified papers~~ | agent | Done 2026-09-24: #485 (Agent Zero Memory + HarnessEvolve → agent-frameworks §4; Repo-To-Skill → CC-skills-adoption). M-priority topics remain available on owner request |
| ~~21~~ | ~~Repoint `sandbox-runtime` links~~ | agent | Done 2026-09-23: repo moved to `anthropics/sandbox-runtime` (#139 still open); 5 links in 3 sandboxing docs repointed, lychee clean |
| ~~21b~~ | Done 2026-09-24 (#457). Bot-block excludes: `www.pwc.com/m1/en/publications/2026/docs/future-of-solutions-dev-and-delivery-in-the-rise-of-gen-ai.pdf` (`agentic-sdlc-patterns.md`) and `www.beyondtrust.com/resources/glossary/just-in-time-access` (`agent-identity-auth-landscape.md`). Both return 200 via polyfetch (2026-09-23) and 403 only to lychee. Also `ampcode.com` (`amp-analysis.md`): 200 via polyfetch, persistent HTTP/2 protocol error to lychee (same class as the existing `epo.org` exclude). These plus row 15's producthunt 403 are the only failures in a full lychee run (4,440 links, 5 errors) | owner | Exact-URL excludes added to `lychee.toml` (Salesforce precedent), or rejected |

## Unverified

- Whether ampcode.com's error persists (one data point).
- What the ruleset's `code_quality` rule gates.
- gh-pages branch contents (inferred from the workflow step).
