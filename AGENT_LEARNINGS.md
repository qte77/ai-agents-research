---
title: Agent Learning Documentation
description: Non-obvious patterns that prevent repeated mistakes across sprints
---

## Template

- **Context**: When/where this applies
- **Problem**: What issue this solves
- **Solution**: Implementation approach
- **Example**: Working code
- **References**: Related files

## Learned Patterns

### A merge refused with "Required status check CodeFactor is expected" means the branch is behind

- **Context**: Merging PRs here past the signed-commit rule (owner-approved), several PRs in a row.
- **Problem**: `main` requires CodeFactor on an up-to-date head (`strict_required_status_checks_policy`). After one PR merges the others are behind, and the merge is refused even though CodeFactor was green on the old head. GitHub's `mergeable_state` lags and can still read `clean` or `unknown` right after a merge, so checking it doesn't help.
- **Solution**: compare the PR head against `main` (`gh api repos/<o>/<r>/compare/main...<head>` → `behind_by`). If it's behind, update the branch, wait for CodeFactor on the new head, then merge. Unsigned bot commits (weekly triage PRs) merge the same way; no owner-signed commit is needed. Recurred on #725, #733, #735, #745, #752–#760.

### CodeFactor stuck "in progress", and bot PRs whose Lint shows `action_required`

- **Context**: merging a series of PRs here, including the weekly bot triage PRs.
- **Problem**: (1) the CodeFactor check-run sometimes stays `in_progress` for 10+ minutes and never completes, so the strict required check blocks the merge; (2) Lint on PRs opened by the github-actions bot sits at `action_required` and never runs. Note that CodeFactor reports as a check-run, not a commit status, so a script reading `commits/<sha>/status` sees nothing.
- **Solution**: (1) close and reopen the PR; CodeFactor re-runs and usually passes within a minute. Read it from `commits/<sha>/check-runs`. (2) a maintainer approves the pending workflow runs (Actions tab, or the REST endpoint for approving a workflow run), then waits for the checks. Recurred on #780 (2026-11-11), #863/#869 and #872 (2026-11-17). (3) A Lint job can keep showing `in_progress` (conclusion `success`) after its run has completed, so `gh pr checks` keeps reporting it as pending and exits 8; a wait loop that relies on that exit code never ends. Read the run with `gh run view <id> --json jobs`, and judge the merge on the required checks only (CodeFactor, CodeQL). Seen on #1124 and #1139 (2026-11-27).

### Rotating github.com 503s in the link check mean lychee is unauthenticated

- **Context**: CI `Link check (lychee)` failing on a *different* github.com URL each run (503 or timeout), on links the PR never touched.
- **Problem**: Treated for months as host flakiness (re-run until green). On 2026-10-24 every run failed this way, blocking eight PRs. Root cause: `lint.yaml` ran `make check_links` without a token, so ~2,800 links' github.com requests were unauthenticated and throttled. `link-rot-monitor.yaml` and the shared `lint-md-links.yml` (lychee-action defaults `token` to `github.token`) were already authenticated, which is why they passed.
- **Solution**: Pass `GITHUB_TOKEN: ${{ github.token }}` to any step that runs the lychee binary (`--github-token`, env `GITHUB_TOKEN`). Shipped in #721. Occasional single 5xx can still happen; re-run only when every failure is a 5xx/timeout, never past a 4xx.
- **Related — green runs that did nothing**: the W42 paper triage (2026-10-20) finished green with every relevance call failing on HTTP 401 (expired token), so no PR appeared and nobody noticed. A job whose whole batch fails must exit non-zero (plan 0012 row R12); new monitors guard this (the M365 drift monitor fails on "changed but empty report"). **Second occurrence (2026-11-10):** the paper triage resolved the newest feed file, which was now a header-only stub the feed seeds each Monday; it loaded 0 papers, skipped triage and stayed green, and W45 was never evaluated. The resolver now skips files under 1 KB. When an upstream starts publishing placeholders, "newest file exists" stops meaning "data ready": check the size or row count, not the name.
- **Third occurrence (2026-11-14):** `cc-status-monitor` logged `HTTP Error 403` from `status.anthropic.com` on 12 weekly runs (2026-08-24 → 2026-11-09) and stayed green: the step mapped every exit other than 1 to "no change". Fixed in #837 (read `status.claude.com`, fail on exit > 1). When a script has exit codes for "changed" and "unchanged", every other code must fail the step. Promoted 2026-11-22 to the shared rule in `qte77/claude-code-plugins` `.claude/rules/unattended-execution.md` § Quality gates (qte77/claude-code-plugins#303).
- **References**: #721, #720, plan 0012 rows K0 and R12.

### Research subagents overclaim — review the strongest claims at source

- **Context**: Merging docs written by research or synthesis subagents (worktree lanes, Fable synthesis).
- **Problem**: In plan 0009 (2026-09-30), five claims were stronger than their evidence, and none was flagged by the lane:
  - a docs page became a "confirmed shipped implementation" (K5), although the same page said no example used it;
  - four agreeing sources became a "structural property" (K6);
  - a paraphrase was put in quotation marks, and a backend relationship was inferred (K7, which then spread into the Feynman cross-link and the plan);
  - a composed rubric row read as all `yes` (Y);
  - dead workflows were presented as live (Y, from a stale corpus doc).
- **Solution**: Briefs require claims at their evidence level (documented / announced / shipped / observed), verbatim-only quotes, and a closing "strongest claims" list. The reviewer opens the source for each item on that list before merging, and checks that live-system claims are still live. All three are in the [`adding-research-source` skill](.claude/skills/adding-research-source/SKILL.md). The shared [claim-verification rule](https://github.com/qte77/claude-code-plugins/blob/main/.claude/rules/claim-verification.md) names the underlying failure modes: hedge decay, assertion from partial evidence, stale aggregate views.
- **Follow-up (2026-10-01)**: a claim-falsifier pass (643 claims, 43 confirmed findings, fixed in #572) showed that checkers err too:
  - a corpus-mismatch finding counted only the docs it was given and missed a row elsewhere (a verifier agreed);
  - two absence claims were wrong because only one page was checked: Flue "has no repo" (K6), and AAIF "publishes no charter" (written in #545, then repeated by the falsifier's correction and its verifier).
  Review a correction like any other claim: check absence site-wide and corpus counts against the full corpus. Fixed in #573; the skill guardrail now says so.
- **Follow-up (2026-11-26)**: the plan 0016 N61 refresh (1,049 proposed corrections across 204 docs) showed two more gaps.
  - A verifier's per-doc verdict is not a filter. Docs marked "holds" carried caveats, and docs marked "does not hold" had a sound core correction. Each claim needs its own outcome (apply, apply as amended, mark `(unverified)`, or drop), recorded in a worklist.
  - Applying verified corrections still introduced errors. A second fact-check pass on each lane's diff found 1–6 per lane: a stale verbatim quote, qualifiers with no source, a true fact deleted, a tense stronger than the source, and lane notes ("per the pack", "not re-read by me") written into published docs. The workflow's own proposals were also wrong a few times, for example a star count and a permission count.
  - Lane briefs now forbid process voice in docs and require repeated numbers to agree across files. Every lane diff gets the second pass before merge.
- **References**: PRs #559, #561, #568, #571–#573; #1100–#1107 and this PR (N61).

### Pruning lanes misjudge "no code" and "no adoption" from the wrong page or repo

- **Context**: Plan 0015 P2 pruning sweep (2026-11-21/22), one worktree lane per landscape, two fact-check passes.
- **Problem**: Fact-check pass 1 reversed lane moves in at least six cases: three because the code was named only in the paper's HTML or appendix, not on the abstract page (Adaptive Skill Granularity, VIPER-MCP's artifact package, UltraQuant's kernel upstreamed into vLLM); one because the lane judged a republished 848-star copy instead of the live 1,122-star original (Tracely); one because a reproducible first-party benchmark was read as "self-run" (agent-audit); one because a reason inferred an unread page's content (Cuttlesoft).
- **Solution**: The lane and falsifier briefs (`.claude/skills/adding-research-source/references/`) now require searching the HTML or PDF for code, checking every copy of a repo, and stating only what was read. Keep both fact-check passes; the second pass must also cover text the lead adds after pass 1.
- **References**: plan 0015 row P2 (batches 13–17), #1013, #1016, #1020, #1022.

### Continued sessions: reconcile git HEAD vs the conversation summary before executing tracked work

- **Context**: A long/continued session whose summary predates recent merges.
- **Problem**: The session built a full plan to "execute the #354 graph rebuild" when it was already done (PR #379, 637 nodes, #354 closed) — wasted effort and nearly re-ran a completed rebuild.
- **Solution**: Before executing any tracked/deferred work in a continued session, reconcile the *actual* state — `git log`, the tracking issue's open/closed state, and key artifacts (e.g. a generated file's node or row count) — against what the summary claims. On mismatch, surface it; don't act on the stale model.
- **References**: plan 0006 (#354), PR #379.
- **Recurrence (2026-11-09)**: plan 0012 kept the gate D0 (qte77/.github#45) and five consumer PRs (C1) as "blocked" for two weeks after the owner merged all six on 2026-10-24. Every session copied the state forward from its summary and only listed this repo's open PRs, so PRs in other repos were never re-read. Also stale: a closed foreign PR still listed as pending, and a signing problem that had since been fixed.
- **Solution (now tooled)**: `make reconcile` (`.github/scripts/plan-reconcile.py`) reads the newest plan's remaining-work table, looks up every cited PR/issue (any repo) through `gh`, and flags rows whose text disagrees with live state. Run it before reporting anything as open or blocked; fix a stale row in the PR that discovers it. Write a reference that doesn't decide its row in backticks so the check skips it. #766, #768; also runs weekly in CI (`plan-reconcile-monitor.yaml`, `plan-drift` issue).
- **Blind spot (2026-11-10)**: a row that names a repo but no PR/issue number can't be checked. D2 ("`clef` backend in qte77/.github") was reported as next work on 2026-11-09, though qte77/.github#47 had merged on 2026-10-26. The check now prints such rows as "verify by hand": look at that repo's merged PRs before calling one open, and write the PR number into the row when it ships.

### Phantom files in repo root from bwrap sandbox

- **Context**: Claude Code with bubblewrap sandbox on Linux/WSL2/Codespaces.
- **Problem**: 0-byte char-special files leak into project root (`.bashrc`, `.mcp.json`, `HEAD`, `config`, etc.) — poison `git status`, break `git log HEAD`, block `EnterWorktree`.
- **Solution**: Use the rooted-pattern `.gitignore` block (already in repo). See friction doc for dead-ends to avoid.
- **References**: [docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md](docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md) (canonical), [anthropics/claude-code#17727](https://github.com/anthropics/claude-code/issues/17727).

### bwrap bind-mount blocks `git unlink` on project-root config files

- **Context**: Claude Code with bubblewrap sandbox on Linux/WSL2/Codespaces, running `git switch` / `git restore` / `gh pr merge`.
- **Problem**: Git operations fail with `error: unable to unlink old '<file>': Device or resource busy` on project-root config files (varies by project: `CHANGELOG.md`, `README.md`, `pyproject.toml`, `Makefile`, `.claude/settings.json`). Server-side merges succeed but local FF fails; working tree desyncs from HEAD.
- **Solution**: `git update-ref` + `git reset HEAD` to move branch pointer without checkout; `git restore` for unlocked files; Claude Code Edit/Write tool for busy ones (overwrites via `O_TRUNC`, bypasses `unlink(2)`).
- **References**: [docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md](docs/cc-native/sandboxing/CC-sandbox-bwrap-host-quirks.md) (canonical, Friction 3), [anthropics/claude-code#17727](https://github.com/anthropics/claude-code/issues/17727).

### Subagent reference sweeps can return false negatives — verify before deleting

- **Context**: Before deleting or moving docs, dispatching a subagent (Explore / general-purpose) to grep the repo for inbound references.
- **Problem**: A subagent sweep confidently reported "no live-doc references" to files queued for deletion. In fact ~28 inbound links existed (a metrics doc deferred to the archive landscapes at ~22 lines; the observability doc linked one too). Acting on the sweep alone would have shipped broken links — and because `lychee.toml` excludes `docs/archive/`, links *into* the archive were never CI-checked, so the breakage would have surfaced only after deletion made them dangle elsewhere.
- **Solution**: Treat subagent ref-sweeps as advisory, not authoritative. Cross-check the result against references you have already read directly; calibrate the sweep by naming known hits and confirming it finds them. Repoint inbound refs to their new homes, then run `make check_links` (lychee) — it is the backstop that catches anything the sweep missed before the change merges.
- **References**: [lychee.toml](lychee.toml) (excludes `docs/archive/` — repoint archive-bound links to live homes before deleting), [PR #237](https://github.com/qte77/ai-agents-research/pull/237).
- **Promoted (2026-06-21)**: recurred 3×+ — including false-negative "create-new" calls on docs that already existed (`databricks-genie-analysis.md`, `opennote-analysis.md`) and a missed whole section (the Agent-HUD block in `ag-ui-protocol-landscape.md`). Constraint added to the read-discipline rule ("Verify subagent findings before acting"), now the shared [read-discipline rule](https://github.com/qte77/claude-code-plugins/blob/main/.claude/rules/read-discipline.md) (plan 0001).
