---
title: Doc-graph focus, kit colours and encoding; harness subscriptions, M365 APIs, enterprise data APIs, DMS graph
status: approved
issue: "#1071"
created: 2026-11-26
updated: 2026-11-26
---

Tracking issue: #1071 (kept from plan 0016). Successor to
[plan 0016](2026-11-24-0016-graph-ui-sources-paperverse-feed.md): its open rows moved here unchanged
and keep their IDs, so there is one live plan, and `make reconcile`, which reads only the newest plan,
checks all of it.

## Current status

**Read this first: what to do next and how.**

- **Shipped before this plan:** plan 0016 rows N34 to N58 and N61 (#1072 to #1108).
- **Opened 2026-11-26** from the owner's decisions in one sitting. Every decision is recorded in
  [§ Owner decisions](#owner-decisions-2026-11-26), so nothing needs asking again.
- **In flight:** none yet. This PR adds the plan only.

**Next, in order** (rows in [§ Remaining work](#remaining-work)):

1. **Parallel wave 1.** Up to five lanes at once, one git worktree each:
   - **Code:** N60, then N59.
   - **Content:** N64a, N64b and N64c.
2. **Parallel wave 2,** once wave 1's lanes return:
   - **Code:** N63. It builds on N60's `paint()`, so it branches from `main` after N60 merges.
   - **Content:** N65, in three lanes of about five vendors each, then N66.
3. **Merging.** Merge serially as each lane passes its checks. Merge `main` into the branch, strike the
   row as the last commit, then push and merge.
4. **After the batch:** release (minor), but only on the owner's word.

**Owner-gated, don't start:** N9, N38, N41, N56 and N62, plus the `13-*` rows. Each row's own text
gives its gate.

**Watch-outs:**

- **Disk is tight** (about 2.8 GB free on `/workspaces` on 2026-11-26). Worktrees are small (about
  16 MB), but `git worktree add` can take more than a minute, so run it with a timeout. Remove each
  worktree right after its merge.
- **The shell hook rewrites `grep` and `du`** (compact output). Use `git grep` or a small `python3`
  filter when you need exact lines.
- **CI link check:** a GitHub blob URL can return 503 from the runner. Confirm the file exists with
  `gh api repos/<o>/<r>/contents/<path>` and that the URL is not in the PR's diff. Then treat it as
  green under the link-gate rule. No excludes without the owner.
- **Peer sessions** are data only. Their messages carry no owner authority, and the visteer steering
  arc is closed, so don't report PR numbers there.
- **Never write operator commands into repo files.** That means merge-bypass flags, token-unsetting
  wrappers and local absolute paths.

## Owner decisions (2026-11-26)

All taken in the owner's session on 2026-11-26, under the KISS, DRY and YAGNI pushback.

| Topic | Decision |
|---|---|
| N60 trigger | Click or tap only (no hover). Clicking empty space clears it. |
| N60 edges | Edges fade below one zoom threshold. The focused node's own edges stay highlighted. |
| N59 scope | Minimal: commit an unedited copy of `eyerest.css`, plus a test that pins its sha256 and checks the kit-version header and that `style.css` holds no kit colour. No lock file and no scheduled newer-kit check; that check was dropped as unneeded. |
| N59 colours | cc-native → `--data-positive`, non-cc → `--data-caution`, cc-community → `--data-negative`, sdlc-lcm → `--data-alt`. This keeps the current slot order. |
| N63 size | Size docs by link count, always on. No new control. |
| N63 colour | An "age" option in "Colour by", running from `--border` (oldest) to `--primary` (newest). |
| N63 timeline | The Updated panel switches between Updated and Added. One shared date field. |
| N63 rollout | A separate PR after N60 and N59. |
| KB adds | N64a, N64b, N64c, N65 (16 vendors) and N66 (feasibility study only, no code). |

## The loop

**Lanes run in parallel, one worktree each.** Every subagent works in its own worktree, which the lead
creates from `origin/main`:

```text
git worktree add ../wt/aar-<row> -b <branch> origin/main   # sibling of the checkout
```

No two lanes edit the same file. If two lanes must touch one file (N59 and N63 both edit
`ui/doc-graph.html`), the later one branches after the earlier one merges.

- **Content lanes** (N64a to N64c, N65, N66) follow the `adding-research-source` skill's
  enrich-a-topic mode:
  - The brief is
    [`references/lane-brief.md`](../../.claude/skills/adding-research-source/references/lane-brief.md)
    with its placeholders filled, plus the row's task list in [§ Lane tasks](#lane-tasks).
  - Each lane runs on Sonnet and as a general-purpose subagent. The brief forbids skills, spawning
    agents and edits to `.claude/`.
  - After a lane returns, run both passes of
    [`references/falsifier-briefs.md`](../../.claude/skills/adding-research-source/references/falsifier-briefs.md).
    Pass one checks claims at their source; pass two checks diff discipline. Verify each finding
    before applying it.
  - The lead then adds the hub (`docs/_topics/`), index (README) and glossary rows.
- **Code lanes** (N60, N59, N63) are done by the lead or by a Sonnet lane with the same hard limits.
  - Use strict TDD where the change has logic: commit the failing test first. Rendering and wiring
    are tested by the e2e run, not by unit tests.
  - Stdlib only, no new dependency.
  - Review tier 2: one fresh reviewer on a mid-tier model reviews the diff. Fix rounds re-check
    only the delta.
- **Every PR:**
  - Run `make check_docs check_status check_coverage check_frontmatter`, `make test` and
    `make reconcile` before pushing.
  - Add a `changelog.d/<YYYYMMDD>_<row>-<slug>.md` fragment with a scriv heading (`### Added` or
    `### Changed`).
  - Strike the row in the same PR, as the last commit.
  - Pass the link gate: a lychee failure counts as green only if `main` already has it or a local
    recheck passes.
  - Merge serially, pinned to the reviewed head commit.
  - Confirm the PR shows MERGED, then remove the worktree and both branches.
  - Comment progress on #1071.
- **Progress report after each merge:** what shipped, what's next, % done and ETA.

## Source map

### Doc-graph page (N60, N59, N63)

`ui/doc-graph.html` is about 620 lines. Line numbers are as of `main` at `1557a13`.

| Line(s) | What |
|---|---|
| 9 | `<link rel="stylesheet" href="style.css">`. N59 adds `eyerest.css` before it. |
| 11 | `data-theme` set from `localStorage` (`light`, `dark` or `system`) |
| 91–92 | `#colour-by` select (`topic` / `folder`). N63 adds `age`. |
| 100–103 | Updated panel: `#tl-title`, `#tl-window`, `#timeline`. N63 adds the Updated/Added switch. |
| 112 | `vendor/vis-network.min.js` (vis-network 9.1.6, vendored). It supports node `value` + `scaling` and edge `color.opacity`. |
| 130–131 | `FOLDERS`: folder → token list (N59) |
| 136 | `token(name)`: reads a CSS custom property |
| 162–200 | `render(data)`: `colour`, `topicColour` (golden-angle hues), `docColour`, `dim = token("--border")`, the `base` map, node DataSet (hubs are diamonds at 14, docs are dots at 8, the hub index is a star) |
| 284 | `rangeOk(n)` uses `n.updated` (N63 date field) |
| 426–492 | Timeline: `newest` / `oldest`, `refreshTimeline`, `buildTimeline`, the aria labels "docs updated". N63 replaces about six `n.updated` uses. |
| 505–515 | `new vis.Network(...)` options. Edges: `color.color = --border`, `highlight = --primary`. `interaction.hover: true`. |
| 520 | `network.on("zoom", …)` (N60 edge fade) |
| 523–530 | `recolour()`: recomputes `base`, then fires the search input event (N60: call `paint()`) |
| 567 | Detail panel rows "Created" and "Updated" |
| 578–580 | `network.on("click", …)`: opens the detail panel (N60 focus) |
| 583–600 | Search `matches()` and the `input` handler, which dims non-matches with `nodes.update`. N60 folds this into `paint()`. |

Related files:

- **`ui/style.css`:** EyeRest tokens hand-copied at lines 31–90 (`:root`, `[data-theme="dark"]`,
  and the dark media block, including `--cat-rust`, `--cat-olive` and `--cat-clay`). Fonts are at
  lines 7–29; layout tokens follow the colours. N59 removes the colour blocks.
- **`ui/index.html`:** stylesheet link at line 11 (N59).
- **Brand kit:** `qte77/qte77` `brand/ui-kit/eyerest.css` at commit
  `9cbdfa6453f2b8aa323c543afccaf0f1d9bd5945` (#242, kit 0.5.0).
  - Its header says "kit version: 0.5.0 (brand/ui-kit/package.json)" and "DO NOT HAND-EDIT".
  - It defines `--bg`, `--surface`, `--border`, `--text`, `--text-muted`, `--primary`,
    `--primary-on`, `--link` and `--data-positive|caution|negative|alt`, in light and dark and
    under `[data-variant]`.
  - Its dark selectors are `@media (prefers-color-scheme: dark) :root:not([data-theme="light"])`
    and `:root[data-theme="dark"]`.
  - Its `brand/ui-kit/BASELINE.md` item 7 allows an unedited, version-stamped copy.
  - Fetch the file with `gh api 'repos/qte77/qte77/contents/brand/ui-kit/eyerest.css?ref=<sha>' -q .content | base64 -d`.
- **Tests:** stdlib `unittest` in `tests/`, run with `make test`. `tests/test_doc_graph.py` shows the
  pattern (`SiteGraphTests`, `test_deterministic`). N59 adds `tests/test_brand_kit.py`.
- **Data:** `make graph-data` writes `ui/doc-graph.json`, using `.github/scripts/build-doc-graph.py`
  and `.github/scripts/lib/doc_graph.py`. Nodes carry `id, title, bucket, hubs, status, doc_type,
  platforms, created, updated`; edges are linked pairs.
- **Serving:** `make preview` serves `ui/` (default port 8000). `.github/workflows/gh-pages.yaml`
  builds the deployed copy.
- **E2E driver:** polyfetch's patchright Chromium (the `qte77/polyfetch-scrape` clone, run with
  `uv run --directory <clone>`). Browsers go under `PLAYWRIGHT_BROWSERS_PATH=/tmp/ms-playwright`;
  the owner pre-approved the install.

### KB content (N64 to N66)

| Row | File and anchor | Existing text to extend |
|---|---|---|
| N64a | `docs/non-cc/coding-agents/coding-agents-comparison-landscape.md` § Using subscriptions in other harnesses (lines 128–167) | A table with one row per harness: Claude Code, Codex CLI, Gemini CLI, Copilot CLI, OpenCode, Cline and Antigravity, read 2026-11-23, plus a patterns table |
| N64b | `docs/non-cc/agents/microsoft-365-copilot-analysis.md`: Graph row at line 824, tenant sweep at line 1113, Sources at lines 1399 and 1416 (Chat API labelled "Delegated-only, preview, no actions") | A section on building Copilot into your own app (line 764) |
| ~~N64c~~ | ~~`docs/cc-native/context-memory/CC-prompt-caching-behavior.md` § Idle compaction (lines 158–168) and § Second data point (lines 220–232, "Idle compaction did not fire… cause **unverified**")~~ | agent | Shipped 2026-11-26 (this PR): § Idle compaction gains the 2.1.326 and 2.1.332 changelog entries; § Second data point names the four gaps (2.3, 12.6, 14.6, 17.5 h on 2.1.330 and 2.1.331), the 2.3 h gap below the 200K minimum, a later 17.1 h gap on 2.1.332 with no marker (weak evidence), and a stopped host as the better-supported cause (Codespaces 30-minute default idle timeout, 12-hour maximum lifetime; inference); two fact-check passes |
| N65 | `docs/non-cc/frameworks/agentic-enterprise-os-landscape.md` (line 74: the "Data grounding" row, Microsoft Graph vs Salesforce Data 360). Add a new section. | Per-vendor docs to cross-reference: `aws-agent-stack-analysis.md`, `google-cloud-agent-stack-analysis.md`, `databricks-genie-analysis.md`, `salesforce-agentforce-analysis.md` (all in `docs/non-cc/agents/`), and `docs/cc-native/plugins-ecosystem/CC-business-api-integrations.md` (MCP servers) |
| N66 | `docs/non-cc/knowledge-management/repo-to-docs-tools-landscape.md`. Add a new section. | Our builder `.github/scripts/lib/doc_graph.py` parses markdown links in `docs/` only. doc-pipeline-engine (`qte77/doc-pipeline-engine`) converts .docx and .pdf to markdown. |

### First-party sources already read (2026-11-26)

Re-fetch these before writing. Quote only text that is verbatim at the source.

- **Claude Code:**
  - [Remote Control](https://code.claude.com/docs/en/remote-control): "API keys are not supported"; excludes Bedrock, Vertex, Foundry and a non-Anthropic `ANTHROPIC_BASE_URL`.
  - [LLM gateway](https://code.claude.com/docs/en/llm-gateway): a gateway credential replaces the subscription login; setting only `ANTHROPIC_BASE_URL` doesn't.
  - [Legal and compliance](https://code.claude.com/docs/en/legal-and-compliance): third parties may not route requests through plan credentials; the binary must not be modified.
  - [Authentication](https://code.claude.com/docs/en/authentication).
  - [Changelog](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md): idle entries in 2.1.299, 2.1.302, 2.1.314, 2.1.318, 2.1.326 and 2.1.332 ("Fixed idle compaction being skipped for subscribers still well under their weekly limit").
- **GitHub:**
  - [Copilot CLI Entra sign-in changelog (2026-11-17)](https://github.blog/changelog/2026-11-17-github-copilot-cli-adds-microsoft-entra-sign-in-as-a-preview).
  - [Authenticate Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli).
  - [Copilot supports OpenCode (2026-01-16)](https://github.blog/changelog/2026-01-16-github-copilot-now-supports-opencode/).
  - [Third-party coding agents](https://docs.github.com/en/copilot/concepts/agents/about-third-party-coding-agents).
  - [Codespaces timeout](https://docs.github.com/en/codespaces/setting-your-user-preferences/setting-your-timeout-period-for-github-codespaces): "By default this period is 30 minutes"; "a codespace has a maximum lifetime of 12 hours".
- **Microsoft:**
  - [Copilot APIs overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/copilot-apis-overview).
  - [Chat API overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/api/ai-services/chat/overview): text-only; doesn't support tools or long-running tasks.
  - Chat API reference pages under `…/api/ai-services/chat/` (`copilotroot-post-conversations`, `copilotconversation-chat`, `copilotconversation-chatoverstream`). Each has a permissions table; re-check whether application permissions are "Not supported".
  - [M365 Copilot APIs terms of use](https://learn.microsoft.com/en-us/legal/m365-copilot-apis/terms-of-use): 3(b)(5), (6), (12), (13) and (18).
  - [Microsoft APIs terms](https://learn.microsoft.com/en-us/legal/microsoft-apis/terms-of-use).
  - [Copilot Studio billing](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management): footnote 1, no charge only under the licensed user's identity.
- **Unofficial, never presented as supported:** the `copilot-api` (ericc-ch), `coproxy` and
  `copilot-proxy-api` READMEs.

### Session evidence (for N64c; owner's machine, not reproducible by others)

- **Session:** the measured session is the owner's session of 2026-11-22 to 2026-11-26, Claude Code
  2.1.330 to 2.1.332.
- **The four gaps before 2026-11-25:**

  | Gap | Context before it | Rewrite after it |
  |---|---|---|
  | 17.5 h | 352K | 330K |
  | 12.6 h | 330K | 304K |
  | 2.3 h | 135K (under the 200K minimum) | 110K |
  | 14.6 h | not recorded | 435K |

- **On 2.1.332:** a 17.1 h gap at 232K (ending 2026-11-26 15:26 UTC) left no compaction marker. Every
  recorded compaction is `auto` or `manual`. Whether idle compaction writes a marker is not documented.
- **Codespace idle timeout:** not readable without the `codespace` scope.

## Lane tasks

- **N64a, harness subscriptions:** extend § Using subscriptions in other harnesses. Rows and notes to
  add:
  - **Copilot CLI:** add the Microsoft Entra sign-in on an M365 Copilot licence (public preview,
    Frontier customers, usage-based billing, CLI 1.0.113 or later, Windows and macOS).
  - **OpenCode:** GitHub's official Copilot support (Pro, Pro+, Business, Enterprise).
  - **Claude and Codex agents:** both run on a Copilot plan (public preview; Agent SDK and Codex
    SDK; Actions minutes plus AI credits).
  - **Patterns table:** Remote Control is subscription-only; a gateway credential replaces the
    subscription.
  - **Copilot-subscription proxies for Claude Code:** one row, marked unofficial, with the terms
    status "not addressed on the pages read".
  - Don't touch rows for the other harnesses beyond these.
- **N64b, M365 Graph and Copilot APIs:** a short subsection under the build-into-your-own-app
  section (line 764).
  - **Endpoint table:** path, status, permissions and returns.
  - **Chat API limits:** text in and out; files only as OneDrive or SharePoint links; no image
    input, model choice or tools documented; no long-running tasks.
  - **Absences:** no public Cowork, Researcher, Analyst or Managed Runtime API, and no job or poll
    API.
  - **Four ways to use the licence from outside:** Copilot CLI with Entra sign-in; Copilot calling
    out to your tools (an MCP server or API plugin on a declarative or Copilot Studio agent);
    the Chat API from your own app with the user's sign-in; the Work IQ APIs (unverified unless
    re-read).
  - **Terms:** 3(b)(12), (13) and (18).
  - **Fix:** the line 1416 label, cited to the reference page's permissions table.
- **N64c, idle compaction:**
  - Add the 2.1.326 and 2.1.332 entries to § Idle compaction.
  - Rewrite the "did not fire" bullet at line 230:
    - one gap was under the 200K minimum, so it was not due;
    - the 2.1.332 gap shows no marker (caveat: no marker is documented);
    - a stopped host is the better-supported cause, since the Codespaces default idle timeout is
      30 minutes, shorter than the about 54–60 minutes idle compaction waits, and the 12-hour
      maximum lifetime is shorter than the 12.6 to 17.5 hour gaps (inference, marked);
    - the 2.1.332 bug is not excluded, because the changelog doesn't say which versions had it.
  - Update the Sources rows.
- **N65, enterprise data APIs:** a new section, "Enterprise data APIs for agents", in
  `agentic-enterprise-os-landscape.md`.
  - **Table rows:** Microsoft Graph and the Copilot APIs, Google Workspace, Salesforce, Databricks,
    AWS, Google Cloud, Atlassian (Confluence and Jira), Slack, ServiceNow, Snowflake, Box, Notion,
    SAP, Workday, OpenCloud and Nextcloud.
  - **Columns:** auth model (user, app-only or both); licence or plan needed; unattended access;
    the terms' wording on agents or automation; official MCP server (yes or no, with a link).
  - Every cell comes from the vendor's own pages; mark a cell `(unverified)` when it can't be read.
  - **Lanes:** three, split as follows.

    | Lane | Vendors |
    |---|---|
    | 1 | Microsoft, Google, Salesforce, Databricks, AWS |
    | 2 | Google Cloud, Atlassian, Slack, ServiceNow, Snowflake |
    | 3 | Box, Notion, SAP, Workday, OpenCloud, Nextcloud |

    Each lane writes its rows into its own scratch file. The lead assembles the single table, so no
    two lanes edit the doc.
- **N66, doc graph on a DMS (feasibility only):** a new section in `repo-to-docs-tools-landscape.md`.
  For each of SharePoint and OneDrive (Graph drive items, delta query, app-only vs signed-in user,
  licence), Google Drive, Box, Confluence, Nextcloud and OpenCloud (WebDAV), cover:
  - how to list files;
  - how to get each file's links;
  - how to turn .docx and .pdf into markdown links (doc-pipeline-engine);
  - what our `doc_graph.py` would need: an input adapter only;
  - which products already draw document-link graphs.

  End with a recommendation and an effort estimate. No code.

## Remaining work

| Row | Item | Gate | Done when |
|---|---|---|---|
| N60 | Doc graph: clicking or tapping a node keeps it and its linked docs coloured and dims the rest; clicking empty space clears it; edges fade below one zoom threshold. One `paint()` function serves search and focus. Self-hosted only, no third-party request (owner go 2026-11-26) | agent | Merged with the graph e2e green on desktop (1366×768) and phone (390×844) in light, dark and system: tap to focus and clear, search while focused, zoom fade; no console errors, no failed or third-party requests, no horizontal scroll |
| N59 | Brand kit colours: `ui/eyerest.css`, an unedited copy of kit 0.5.0 (qte77/qte77 commit `9cbdfa6`), loaded before `ui/style.css`, whose hand-copied colour blocks are removed; `FOLDERS` uses the kit data colours (mapping in [§ Owner decisions](#owner-decisions-2026-11-26)) (owner go 2026-11-26; scheduled check dropped) | agent | `tests/test_brand_kit.py` (written first) pins the sha256 and checks the header and that `style.css` holds no kit token; `make test` green; graph e2e shows the kit values in both themes, with no regressions |
| N63 | Doc-graph encoding: doc size by link count (`value` + `scaling`); an "age" option in Colour by (`--border` to `--primary` on the chosen date); an Updated/Added switch on the timeline panel, all from one `dateKey` (owner 2026-11-26) | agent | Merged after N60 and N59 with the graph e2e green: sizes follow link count, the switch changes the bars, counts and labels, the age legend shows both ends |
| N64a | Harness subscriptions update in `coding-agents-comparison-landscape.md` ([§ Lane tasks](#lane-tasks)) | agent | Merged after two fact-check passes; every new cell cites a first-party page read in the PR's week |
| N64b | M365 Graph and Copilot APIs subsection in `microsoft-365-copilot-analysis.md`, plus the Chat API permission label fix | agent | As N64a |
| ~~N64c~~ | ~~Idle-compaction cause update in `CC-prompt-caching-behavior.md`~~ | agent | Shipped 2026-11-26 (this PR): § Idle compaction gains the 2.1.326 and 2.1.332 changelog entries; § Second data point names the four gaps (2.3, 12.6, 14.6, 17.5 h on 2.1.330 and 2.1.331), the 2.3 h gap below the 200K minimum, a later 17.1 h gap on 2.1.332 with no marker (weak evidence), and a stopped host as the better-supported cause (Codespaces 30-minute default idle timeout, 12-hour maximum lifetime; inference); two fact-check passes |
| N65 | Enterprise data APIs for agents: one table of 16 vendors in `agentic-enterprise-os-landscape.md` | agent | Merged after two fact-check passes; no cell without a vendor source or an `(unverified)` mark; hub rows added |
| N66 | Feasibility study: the doc graph on SharePoint and other document management systems, in `repo-to-docs-tools-landscape.md` | agent | Merged after two fact-check passes, with a recommendation and an effort estimate; no code |
| N9 | Assess YouTube videos (ai-that-works playlist, Cole Medin channel) as research leads (owner 2026-11-22; #1009) | owner | **ai-that-works part done 2026-11-22** (owner narrowed it to the companion repo's transcripts): all 86 episode dirs triaged from the repo (github.com/ai-that-works/ai-that-works, no licence, so read and cited only), 47 with transcripts; 3 strong, 18 possible and 38 dropped leads, list and reasons in the session triage notes. Shipped, each re-checked at first-party sources with two fact-check passes: #1031 GEPA, #1032 SlopCodeBench, #1033 HumanLayer status, #1034 lethal trifecta. **Concept pass** (owner 2026-11-22: concepts, how-tos and best practices count, not only tools): about 225 ideas triaged, 24 kept, each cited as a single-source practitioner claim with outside corroboration where it exists: #1039 harness patterns, #1040 eval practices, #1041 memory, skills, observability and event-log projections; five LLM-application patterns held for lack of a fitting doc. **Open, owner-gated:** Cole Medin's channel, once the owner picks a transcript route (from this Codespace, yt-dlp and headless browsers hit YouTube's sign-in bot check) |
| N38 | paperverse: make the weekly real-feed sync mergeable, add `triage/kb-papers` as a source, then one catch-up sync (D2) | agent in a paperverse session; owner if the fix needs a setting or an App | The sync PR gets every required check and merges without help; paperverse `main` holds all weekly files and `arxiv-kb.jsonl`; deployed page shows them |
| N41 | Freshness rule for volatile claims (owner question 2026-11-24, lead default): one inline form `(read YYYY-MM-DD)` for counts, stars, versions, prices, GA/beta status, availability and benchmark numbers; `validated_links_on` stays link liveness only; Maintenance table row; no migration of existing notes, no new check | owner | Waits on the owner's answer to the lead default. Done when CONTRIBUTING § Inline References and § Maintenance plus the lane brief state the rule in about six lines; `make lint` green |
| N56 | Compare `scripts/cc_cache_usage.py` with Claude Code `/usage` "Prompt cache (main)" and with a cachemiss run on one session (residual of N55) | owner | The owner pasted the `/usage` section on 2026-11-25 (46 main-thread requests, 99% of input from cache, no misses); still waits on approval to run cachemiss (external code); the three sets of numbers agree or the differences are explained in `CC-prompt-caching-behavior.md`; offer the prediction column to cachemiss only if they agree |
| N62 | Owner calls left by the N61 refresh, each with the doc text already hedged: `status:` for `codebuff-analysis.md` and `opennote-analysis.md` (both shutting down) and `frognano-analysis.md` (code and weights now public); the "cleanroom" label for clawcodex in `CC-community-reimplementations-landscape.md` (its README says "ported from the TypeScript reference"); re-scoring the redis-iris Shared and Distributed rubric cells, which were scored on the old Context Retriever wording | owner | Lead default: keep `status: assess` and the hedged text until the owner decides. Done when the owner has decided each one and the decision is applied |
| 13-A5 | Labels from `decide()` in issue triage at a measured threshold (moved from plan 0012's Deferred list) | data | About 50 issues across the shadowed repos carry the shadow section; then sweep `hi` against the labels the existing triage set and decide |
| 13-A7 | Drift checks for the decision models: (1) a monthly scheduled run of `decision-model-eval.yaml` on the gold sets, flagged against the 2026-11-10/11 baseline (AUC drop above about 0.03, Brier rise, recommended `hi` moving by 0.05 or more); (2) store each weekly paper run's decided / fallback / escalated counts (the artifact summary already prints "Decided via decide()") and flag a sustained fall in the decided share or a rise in escalations; (3) on about 10% of papers also run the chat call and track the disagreement rate. Pin model versions (`jev-1.13.0`, `clef`) and re-run the gold sets before any bump; set thresholds on one half of a gold set and report on the other. **Part (1) shipped 2026-11-12** (`#813`: `decision-model-eval.yaml` monthly on the 1st, `data/gold/baseline.json`, `decision-drift` issue; Brier shown, not flagged). A manual run the same day reproduced the Clef and Clef-flash baseline exactly, so run-to-run noise for Clef is nil on this evidence (Jev not re-run). **Part (2) shipped 2026-11-17** (`#875`): the committed triage reports already store each run's "Decided via decide()" line, so `lib/decide_counts.py` reads them and the monthly `decision-model-eval.yaml` run appends a per-run table to its summary and a note to `drift.md` (the `decision-drift` issue) when each of the last 3 runs' decided share is more than 0.10 below the earlier mean; it needs 6 runs before it can flag. First data point: W45, 88 of 100 decided. Escalations are not printed separately in the summary, so they are counted as fallbacks. Left: (3) the chat-call disagreement sample — ask the owner whether it earns its cost; the split-half thresholds belong to A8 | owner (deferred) | Monthly workflow live with a baseline file; counts stored per run; disagreement sample in the summary. **Part (3) deferred by the owner 2026-11-22** (not built now); parts (1) and (2) ship. Resume only on an owner go |
| 13-A8 | Gold-set refresh against the in-sample caveat: add a second paper week as a held-out set, a human spot-check of about 20 items, and real (not planted) off-topic issues | agent + owner spot-check | Second paper set and an issue set with real negatives in `.github/scripts/data/gold/`; H1 numbers re-reported out of sample |
| 13-O5 | Stale token variables. **Done 2026-11-13 as far as the container allows:** `GH_TOKEN` comes from this codespace's devcontainer mapping of an expired PAT secret; the mapping was already dropped upstream on 2026-07-22, but the codespace was never rebuilt. It is now removed from the machine's environment file and unset for new shells. Running processes keep it until a container rebuild, which is the full fix. `GITHUB_TOKEN` is the Codespaces-issued token and the commit signer uses it, so it stays; network calls to other repos keep needing the per-session workaround | owner | **Deferred by the owner 2026-11-22.** When resumed: Codespace rebuilt (owner) |
| 13-O10 | Cloudflare account details in public repos (owner audit 2026-11-13, checked at source). Shipped: `qte77/ldnmxx-hack#373` and `#374` (the account id is no longer pinned in the repo; `.env.example` carries a placeholder), `qte77/qte77.github.io#62` (a draft link removed). The open decisions (git history, the live Worker hostname, CI secrets) and the step-by-step removal guide sit in the owner's private notes, not in this public plan, so it doesn't point at where the old values still are. An account id itself can't be changed; a new one means a new account | owner | **Deferred by the owner 2026-11-22.** When resumed: Owner closes the private checklist |
