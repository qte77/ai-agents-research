---
title: Backlog triage — open PRs, branches and issues (2026-09-23)
status: draft
issue: 438, 433, 417, 410, 254, 347, 348, 309, 382, 232
created: 2026-09-23
updated: 2026-09-23
---

**Status**: Reference (plan)

Read-only audit of every open PR, every non-main branch and every open issue, run 2026-09-23 by two
subagents. **Nothing has been merged, closed or deleted yet.** In scope: PRs/issues authored by
`qte77`, GitHub Actions bots and Dependabot (all 29 open PRs and all 10 open issues qualified).

## Current status

- **Shipped (2026-09-23):** 16 superseded bot PRs closed; 3 merged local branches deleted; #309
  boxes ticked; PRs opened — #446 (ccsync), #447 (link-rot #417/#254).
- **Found while executing:** the 7 community-triage PRs are **not** fully superseded by #443 (2–6
  items each are missing from it, checked by item key) — held open, row 1b. #433 needs no file in
  this repo — host-root `qte77.github.io/robots.txt` already carries `Content-Signal` (row 6).
- **Next, in order:** remaining agent rows below → pre-stage the owner-review PRs → one owner
  sitting (Phase B).
- **Owner gates:** bot-PR merges (`--admin` is confirm-before-run in global settings), #434
  decision, producthunt lychee exclude, closing #382, deciding #232, #309 scope.
- **Commands:** prefix every `gh`/`git` network call with `env -u GH_TOKEN -u GITHUB_TOKEN`
  (invalid env tokens shadow the stored credential).
- **Watch-outs:**
  - Squash-merges break ancestry → judge "already landed" by content (`git cherry main <branch>`),
    not `git branch --merged`.
  - main requires strict up-to-date branches → merge bot PRs **one at a time**, updating the next
    branch after each.
  - All 29 PRs show `BLOCKED`; the reason was **not verified** (ruleset API not queried).

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
| Dependabot actions bump | #434 | — | — | Lint/lychee + rxiv `eval/evaluate` jobs fail. Lychee flakiness is known; rxiv failure *guessed* to be missing secrets on Dependabot PRs — logs not read (`gh run view 34025441955 --log-failed`) |

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
- **#347 (row 10):** pin `qte77/.github` @ `613b950b4045cc099ca23f8b7344459c3dc22cb3` ✓
  (`bump-version.yml`, `tag-release.yml`, `publish-release.yml` ✓). Caller overrides: tag-release
  `version_regex: '^current_version = "(.*)"'` (`pyproject.toml:14` ✓, since the default regex would
  silently miss); bump-version `collect_scriv: true` + `bump_my_version_pin` (**default** `1.3.0` —
  currently unpinned); publish-release needs none. Side benefit: the shared bump commits through the
  API, so its commits are signed.
- **#348 (row 11):** PR 1 = `docs/cc-native/`, **61 docs** ✓ (configuration 15, agents-skills 9,
  plugins-ecosystem 9, ci-remote 8, sessions 7, context-memory 5, sandboxing 5, model-internals 3). List:
  `git grep -l '^\*\*Status\*\*:' -- docs/cc-native/`. Transform per plan 0003. **Default:** split by
  feature subdir. The plan's two special-case files are in `non-cc/` (PR 2).
- **#309 Phase 1 (row 12):** `docs/non-cc/` has 70 docs + README in 9 README sections; 3 docs are
  unindexed (`agents-md-cookbook-analysis.md`, `moss-self-evolving-agent-analysis.md`,
  `on-device-semantic-search-landscape.md`). Clean merge: Knowledge Mgmt + Context & Memory Infra +
  on-device search → `memory-kg-rag/` (10). **Defaults for the 3 mapping calls:** Infrastructure (9) →
  `reference/`; Agents (7) → coding-agent-shaped ones to `coding-agents/`, the rest to `frameworks/`;
  `visualization/` is too thin (≈1 doc) → fold into `protocols/`. Repoint surface: 60 files outside
  `non-cc/` (493 occurrences) plus ~40 sibling links; lychee is the backstop. **Default:** one PR per
  subdir.

## Remaining work

The only list of open work in this plan. Strike a row in the PR that ships it.

| # | Item | Gate | Done-when |
|---|---|---|---|
| ~~1~~ | ~~Close superseded changelog/learnings/outage bot PRs~~ | agent | Done 2026-09-23: 16 closed (#413–#439 → #442, #416–#441 → #444, #414/#420 → #424), each verified by item key |
| 1b | Community-triage PRs #415, #421, #425, #428, #431, #436, #440 | owner | Decide: merge oldest-first, or close accepting the loss of 2–6 items each that #443 lacks |
| ~~2~~ | ~~Delete 3 merged local branches~~ | agent | Done 2026-09-23 (`git cherry` equivalent before deleting) |
| ~~3~~ | ~~#309: tick Phase 2, Phase 3 and "track #308"~~ | agent | Done 2026-09-23; issue stays open for Phase 1 |
| 4 | Ship `feat/ccsync-and-profile-perms` | owner | PR #446 open (fragment added, shellcheck clean) — merge when CI green |
| 5 | #417: claude.com 404 removed (#447); recheck ampcode.com on next weekly run | agent | Next weekly report has no ampcode.com error, or it's triaged |
| ~~6~~ | ~~#433: Content-Signal / llms.txt~~ | owner | Done 2026-09-23: closed with evidence — host-root robots.txt already carries Content-Signal; no llms.txt for now |
| 7 | #254: vibekanban exclude dropped (#447) — sunsetting already documented (2026-06-20) | owner | PR #447 merged |
| 8 | #438: new cross-session messaging doc (ListAgents, SendMessage, v2.1.224) | agent → owner review | PR open, first-party sourced |
| 9 | #410: feed.xml trigger per the narrowed decision | agent → owner review | Workflow PR open |
| 10 | #347: SHA-pinned reusable release workflows | agent → owner review | PR open |
| 11 | #348: migration PR 1 of ~5 (one subdir) | agent → owner review | PR open, validator passes |
| 12 | #309 Phase 1: `non-cc/` subdivision plan + first move PR | agent → owner review | Plan committed, PR open, lychee green |
| 13 | Merge newest bot PRs #442, #443, #444, #424, #418, one at a time | owner | All five merged; branches deleted |
| 14 | #434: read failed logs, then merge or re-run | owner | Merged or closed with reason |
| 15 | #417: approve producthunt exclude | owner | Exclude added or rejected |
| 16 | Close #382; decide #232; decide #309 scope (keep vs. split) | owner | Each issue closed or updated with decision |

## Unverified

- Why every PR is `BLOCKED` (ruleset not queried).
- Supersession of the community, learnings and outage-archive PRs (inferred, not content-diffed).
- Root cause of #434's rxiv-eval failure.
- Whether ampcode.com's error persists (one data point).
- vibekanban.com under lychee's own TLS check (only WebFetch tried).
- gh-pages branch contents (inferred from the workflow step).
