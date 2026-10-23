---
title: Decision models first across the qte77 GitHub Actions estate
status: approved
created: 2026-10-10
updated: 2026-10-22
---

Tracking issue: #652.

## Current status

**What this arc is:**

- Every qte77 GitHub Action that calls a model asks **decision-shaped** questions through a decision model first: a typed yes/no probability (`noul`), a choice, or a score, with Jev as the default.
- A generative LLM, Cloudflare Workers AI through an OpenAI-compatible `api_base`, is used **only for free text** and as the fallback.
- One shared `decide()` lives in `qte77/.github/actions/decide/`.

**Status:** **approved 2026-10-10** (owner: "proceed" on #651). Already done: on 2026-10-10 `LLM_BASE_URL` was set as a repo **secret** in the 10 repos listed under K0. Phase A lanes L1, L3 (G1 only), L4 and L5 started 2026-10-10. Shipped: D1 (#653), G1 (#654), owner lead Cloudflare Clef + Unsloth decision training in the landscape (#657; on Clef's own card Jev leads on GPQA, MMLU-Pro, BBH, When2Call and BRIGHT, so H1 must test our tasks), W12 (gha-rxiv-feed-action #207, #209, #210; #655). L1's PR qte77/.github#45 awaits the owner's merge; L2 pre-stages its PRs and merges after K0. K0 is pre-staged: `/workspaces/temp/ai-agents-research-triage/set_keys.sh` (see the K0 row). **2026-10-22:** owner leads N9 shipped; new research rows R1–R6 (agent) and owner rows R7–R10 added. Next agent work while D0 is deferred: R1–R5. Research notes: `/workspaces/temp/goal-research-2026-10-22/findings.md`.

**How to run it:**

1. Reconcile: `git log`, `gh pr list`, and the gate rows below. The plan may be stale; check before acting.
2. Run **Phase A** as parallel lanes. Each lane is a subagent in its own worktree, briefed with the lane's file fence (Lanes table). Lanes open PRs but never merge. The main session never edits a lane's files.
3. Worktrees: for ai-agents-research lanes, the Agent tool's `isolation: worktree`. For sibling repos, the main session first runs `git -C /workspaces/qte77/<repo> worktree add <path> -b <branch>` and points the brief at that path; the lane follows that repo's CLAUDE.md/AGENTS.md/CONTRIBUTING.md. Finished worktrees: `git worktree remove -f -f`.
4. The main session reviews each lane's PR **at source** (strongest claims, test run) and merges. For an ai-agents-research lane, it pushes the row strike onto the lane's PR branch before merging (same PR). A sibling-repo row is struck in the ai-agents-research PR that records the merge.
5. Phase B is one owner sitting (K0). Phase C activates (C1 to P2).

**Rules for every lane:**

- **No links or cross-references to qte77/ai-agents-research** in any other repo's issues, PRs or docs (owner rule, 2026-10-10).
- **Strict TDD:** failing tests first.
- Each repo's own validate/lint/test target must be green before pushing.
- Prefix `gh`/`git` with `env -u GH_TOKEN -u GITHUB_TOKEN`.
- **Secrets are never printed;** set them via stdin.
- **Merging:** commits can't be GPG-signed in this sandbox. Use `gh pr merge --squash --admin` only when the signature rule is the sole blocker; never use it past a failing check. In ai-agents-research use `/workspaces/temp/ai-agents-research-triage/merge_retry.sh <PR>`.
- Briefs forbid skills, `.claude/` edits and spawning sub-subagents.

**Owner gates:** K0 (create keys). Everything else defaults as decided below; the owner may override.

**Watch-outs:**

- TypeSafe's Cloudflare WAF returns 403 on some content. That must route to the fallback, never become a verdict.
- Thresholds don't transfer between repos. The feelings gate at 0.70 flagged 3.4% of clean changes vs 23% on a held-out repo, so ship **shadow mode** first.
- The Cloudflare fallback has no calibrated confidence: `confidence=None` always escalates.
- GitHub `CodeFactor` is the required check and races on new pushes. Retry; never bypass.

## Decisions (owner, 2026-10-10)

1. **Shared code** lives in `qte77/.github/actions/decide/` as a composite action plus `decide.py`.
   - Standard library only (`urllib`, `json`).
   - Callers pin a commit SHA; `.github` has no tags.
   - Fable's alternative, a per-repo copy, was declined.
2. **`LLM_BASE_URL` is a secret, not a variable,** so the Cloudflare account id stays out of logs. Workflows switch `vars.LLM_BASE_URL` to `secrets.LLM_BASE_URL`, then the variables are deleted.
3. **Separate keys per use case;** the local dev key is never reused.

   | Key | Repos |
   |---|---|
   | Jev `triage` | gha-issue-triage + 7 consumers |
   | Jev `paper-eval` | ai-agents-research + gha-rxiv-paper-eval |
   | Cloudflare Workers-AI-scoped `triage` | gha-issue-triage + 7 consumers |
   | Cloudflare Workers-AI-scoped `paper-eval` | ai-agents-research + gha-rxiv-paper-eval |

   The owner creates the keys and puts them in one local file outside any repo. The agent sets them and deletes the file. Do NOT use `feelings/.env`. Unverified: whether TypeSafe allows multiple keys.
4. **Recheck relevance with Jev** (H1) on gold sets labelled by the agent (G1). Owner spot-check of ~20 items is optional.
5. **Deferred:** gha-ai-changelog (no consumer found) and gha-repo-index (AI off by default). Leave only a short note on their issues.
6. **Target wire shape:** TypeSafe's `state` + `noul` (also used by Perplexity and Laya). OpenAI `/v1/decisions` (`input` + `predicate`) is mapped later and not built now.
7. **Cloudflare Clef as a decision backend (agent default, 2026-10-11; owner may override).** Cloudflare shipped Clef (27B) and Clef-flash (9B) on Workers AI on 2026-10-01: the same System One shape as Jev, open weights (Apache-2.0), and Clef-flash at $0.038 per 1M input tokens vs Jev's $0.042 (Cloudflare changelog 2026-10-09). The estate's existing `CF_WORKERS_AI_TOKEN` reaches it, so it needs no new vendor key. Default: add a `clef` backend to `decide()` (D2) and let H1 pick the primary backend per use case from the gold sets. Jev stays the default until H1 reports. Unsloth's train-your-own path (Clef head + QLoRA, v0.1.904-beta) is the self-hosted option if the hosted models fall short.

## Code, file and source map

### qte77/.github (local `/workspaces/qte77/.github`)

- 23 files: reusable workflows `.github/workflows/{bump-version,lint-md-links,publish-release,svg-render,tag-release,validate}.yml`, community templates, `lychee.toml`.
- **No Python, no tests, no tags.**
- New for D0:
  - `actions/decide/{action.yml,decide.py,README.md}`;
  - `tests/decide/test_{schema,jev,fallback,failures,gate,cli}.py`;
  - `pyproject.toml` (dev only: pytest, ruff);
  - `.github/workflows/test-decide.yml`. It runs on PRs touching the decide paths: ruff + pytest on 3.11/3.12 with no network, a smoke job that runs `uses: ./actions/decide` and imports `decide()`, and an optional manual live Jev call.

### Interface (D0)

- Call: `decide(state: str, questions: [{name, type: predicate|choice|score, instructions, choices?, levels?}], backend="jev"|"cf") -> {name: {value, probability|confidence|None, source}}`.
- **Jev:** `POST https://api.typesafe.ai/v1/systemone`, body `{model:"jev-1.13.0", state, questions:{name:{type:"noul", instructions}}}`. A `noul` comes back as a float probability. predicate maps to `noul`; Jev also supports `choice` and `score`.
- **Cloudflare Clef (D2):** `POST https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/cloudflare/clef-flash` (or `clef`), Bearer `CF_WORKERS_AI_TOKEN`, body `{model:"clef-flash"|"clef", state, questions}` (1–64 questions, optional `images`); response `{model, answers, usage}`. Context 24,576 tokens for clef-flash. Source: developers.cloudflare.com/workers-ai/models/clef-flash/. The account id is the one inside the `LLM_BASE_URL` secret.
- **Cloudflare LLM fallback:** `POST {LLM_BASE_URL}/chat/completions` with model `@cf/meta/llama-3.3-70b-instruct-fp8-fast`, asking for a constrained JSON answer. `confidence=None`.
- **Gate:**
  - probability ≥ `hi` or ≤ 1−`hi`: act;
  - middle band: review, with LLM text if needed;
  - error, 403, refusal or `None`: escalate. Never a verdict.
  - `hi` is an input with a conservative default.
- **Reference implementation** (read, don't import), `/workspaces/qte77/feelings/eval/`:
  - `jev_gate.py`: `typesafe-sdk==0.7.1`, `client.system_one(state, {name: Noul(instructions=q)}, model="jev-1.13.0")`, `response.nouls[name].noul`, cost $0.042 per 1M input tokens, a WAF 403 handled per item;
  - `concerns.py`: questions as a dict, with a test keeping copies in sync;
  - `metrics.py`: stdlib ROC-AUC, PR-AUC, `brier_score`, `bootstrap_ci`, `sweep`;
  - `jev_check.py`: fail-open, so a missing key or error means "skipped".

### gha-issue-triage (v0.4.0 = `1bf71f215a70a9b19f228e1c190aaf578baa6a59`)

- Call sites:
  - `src/relevance.py:29`: score 1–10 + category choice + irrelevant (yes/no);
  - `src/feasibility.py:51`: feasibility (yes/no) + complexity (low/medium/high) + effort (hours/days/weeks).
- Both go through `src/llm.py:107` (`call_llm`).
- The `reasoning` text appears at `src/comment.py:66,74`; it is the only free-text need.
- `action.yaml` inputs: `api_base`, `llm-api-key`, `MODEL` (default still `openai/gpt-4.1`), `GH_TOKEN`, deprecated `OPENAI_API_BASE`/`AI_TOKEN`.
- `.github/workflows/self-triage.yml` is wired to CF (#114). Its `CF_WORKERS_AI_TOKEN` may be empty: it was set non-interactively.
- Tests: 86, including `tests/test_llm.py`. Related open issue: #80 (pydantic AppSettings).

### gha-rxiv-paper-eval (v0.5.0 = `6097eb9981c76014793eb7e468e1aec00f56e12f`)

- `scripts/eval_papers.py`: `:604` `is_relevant` (YES/NO, `max_tokens=4`) is decision work; `:643` `extract_fields` stays with the LLM; shared caller at `:542`.
- `Settings.api_base` / `llm_api_key`, env `RXIV_EVAL_API_BASE` / `RXIV_EVAL_LLM_API_KEY`.
- Dead self-test: `.github/workflows/eval-papers-dispatch.yaml:74,104` (GitHub Models).
- Open issue #58, "single OpenAIModelSpecClassifier + SDK-backed Anthropic", is the home for the decision backend.

### 7 broken triage consumers

- Repos: `agentic-job-offer-to-application-kit`, `analyze-stock-kpi`, `claude-code-plugins` (v0.3.0 `4a07dd2`); `cc-senses-plugin`, `vlm-toolkit`, `CellPlateVision-Prototype`, `cc-voice-plugin-prototype` (v0.2.4 `cc8f0cf`).
- Each has `.github/workflows/issue-triage.yaml` with `models: read` and no `api_base`. Each now has the `LLM_BASE_URL` secret and nothing else.
- Fix:
  - pin v0.4.0 (or the P1 release);
  - `llm-api-key: ${{ secrets.CF_WORKERS_AI_TOKEN }}`, `api_base: ${{ secrets.LLM_BASE_URL }}`, `MODEL: "@cf/meta/llama-3.3-70b-instruct-fp8-fast"`;
  - drop `models: read`.
- Reference wiring: ai-agents-research `.github/workflows/issue-triage.yaml`.

### ai-agents-research (this repo)

- Paper eval:
  - consumer `.github/workflows/rxiv-paper-eval.yaml` (agent-strict prompt, `max_llm_calls: 100`);
  - harness `.github/workflows/llm-model-eval.yaml` + `.github/scripts/eval-relevance-models.py` + `.github/scripts/lib/relevance_eval.py` (`PROMPT_VARIANTS`, `AGENT_STRICT_PROMPT`, test-locked to the workflow);
  - labelled data `triage/rxiv/data/arxiv-2026-W*.jsonl` (labels = retired gpt-4o-mini verdicts, not ground truth).
- Backfill drivers: `/workspaces/temp/ai-agents-research-triage/{backfill_week.sh,merge_retry.sh}`.

### Other repos

- **qte77/qte77:** `.github/workflows/repo-registry.yml` has a stale `models: read`; README tech-stack line 68 shows a GitHub Models icon. Open #31.
- **Deferred:** gha-ai-changelog `action.yaml:98,127` (local clone lags origin; issue #45). gha-repo-index `scripts/summarize-with-ai.sh:54` (issue #20).
- **W12:** `qte77/gha-rxiv-feed-action` `data/arxiv/2026/12.csv` has the old 6-column header; issue #206. Regenerate it: delete the file, then dispatch `update-rxiv-feed.yaml` with `server=arxiv`, `date_from=2026-03-16`, `date_to=2026-03-22`. `scripts/migrate_csv_schema.py` skips it (renamed column). `src/fetchers/common.py` `write_file` would pad the existing rows with empty abstracts.

### Sources

- [TypeSafe confidence docs](https://docs.typesafe.ai/confidence) (act/confirm/escalate);
- [TypeSafe models and pricing](https://docs.typesafe.ai/models) (jev-1.13.0, $0.042/1M);
- [OpenAI Decisions guide](https://developers.openai.com/api/docs/guides/decisions);
- [Cloudflare Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/).

## Lanes (parallel subagents, each in its own worktree)

| Lane | Rows | Repo / worktree | File fence (only these) |
|---|---|---|---|
| L1 | D0 | qte77/.github | `actions/decide/**`, `tests/decide/**`, `pyproject.toml`, `.github/workflows/test-decide.yml`, `CHANGELOG.md` |
| L2 | C1 | the 7 consumer repos (one worktree each, sequential inside the lane) | `.github/workflows/issue-triage.yaml` only |
| L3 | G1 + H1 | ai-agents-research | `.github/scripts/**`, `.github/workflows/llm-model-eval.yaml`, `tests/**`, `.github/scripts/data/gold/**` (new; `triage/` is bot-only per CONTRIBUTING), `changelog.d/*_gold-sets.md` |
| L4 | D1 | ai-agents-research | `docs/non-cc/reference/system-1-decision-models-landscape.md`, `changelog.d/*_decision-1.md` |
| L5 | W12 | qte77/gha-rxiv-feed-action | `data/arxiv/2026/12.csv` (via its workflow; deletion via PR, never a direct push to main) |

L1, L3 (G1), L4 and L5 run in parallel. L2 opens its PRs in Phase A and merges them after K0. H1 needs the K0 Jev key. P1 and P2 start after L1 merges (they pin its SHA) and after H1, which sets thresholds. E1 runs after P1.

Lane notes:

- **L1:** the Jev request body in the map was read from the SDK wrapper. Verify the raw request shape (docs.typesafe.ai, or how `typesafe-sdk==0.7.1` in the feelings venv builds it) before writing `test_jev.py`. Keep `.github`'s `validate.yml` green.
- **L3 (G1):** papers come from the top-100 ranked pool of `triage/rxiv/data/arxiv-2026-W40.jsonl`; issues from repos with past triage comments (ai-agents-research since 2026-10-04, gha-issue-triage self-triage). The existing `label` fields are gpt-4o-mini verdicts and are never ground truth. The second pass is a separate blind labeller that the main session spawns; disagreements are reconciled with written rationale.

## Remaining work

| Row | Item | Gate | Done when |
|---|---|---|---|
| ~~T0~~ | ~~Tracking issue in ai-agents-research, linked from this plan~~ | agent | Shipped: #652 (PR #651) |
| K0 | Create 4 keys (Jev + CF per use case) into one local file; the agent runs the pre-staged `/workspaces/temp/ai-agents-research-triage/set_keys.sh <file>` (sets `TYPESAFE_API_KEY` + `CF_WORKERS_AI_TOKEN` per the key table via stdin, prints nothing secret), then deletes the file. `LLM_BASE_URL` secret already set (10 repos) | owner | `gh secret list` shows both secrets in every target repo; **2026-10-18: owner set `CF_WORKERS_AI_TOKEN` in the six consumers and re-set it in gha-issue-triage; no TypeSafe keys yet** |
| D0 | `decide` action in qte77/.github, TDD per the map. PR qte77/.github#45 is built (60 tests, CI green) and **deferred by the owner 2026-10-12**; D2, P1, P2 and E1 wait on it | owner (deferred) | `test-decide.yml` green; README documents schema, bands, secrets |
| C1 | 6 consumer PRs (pin + CF inputs + drop `models: read`; `cc-voice-plugin-prototype` redirects to `cc-senses-plugin`), pre-staged 2026-10-11: agentic-job-offer-to-application-kit#447, analyze-stock-kpi#512, cc-senses-plugin#137, claude-code-plugins#245, vlm-toolkit#20, CellPlateVision-Prototype#9; gha-issue-triage self-triage secret switch #115 (**deferred by the owner 2026-10-12**; keep its `LLM_BASE_URL` variable until it merges); the owner merges each consumer PR after K0; switch gha-issue-triage self-triage to `secrets.LLM_BASE_URL` and delete its variable. ai-agents-research's `issue-triage.yaml` + `llm-model-eval.yaml` switched in #659; its variable stays until P2, because `rxiv-paper-eval.yaml` passes `api_base` as a reusable-workflow `with:` input, which cannot read secrets | agent (L2), after K0 | One test issue per consumer gets a triage comment; self-triage run green; **2026-10-18: agentic-job-offer#447 merged, live test #457 passed; self-triage live test gha-issue-triage#116 passed on rerun; five consumer PRs still open** |
| ~~G1~~ | ~~Gold sets: 62 issues + 100 papers (W40 ranked pool), two agent passes~~ | agent (L3) | Shipped: #654, `.github/scripts/data/gold/`. Papers 77/23 (96/100 pass agreement; 4 splits reconciled to NO), issues 59/3 (3 negatives are planted fixtures: weak for false accepts). Owner spot-check optional |
| D2 | `clef` backend in `decide()` (qte77/.github), TDD, mocked like the Jev adapter; README lists both | agent, after D0 merges | Tests green; one manual live call with the repo's `CF_WORKERS_AI_TOKEN` returns a probability |
| H1 | Decision runner in the eval harness: AUC + bootstrap CI, Brier, threshold sweep (port feelings `metrics.py`); compare Jev, Clef, Clef-flash and Llama-70B agent-strict on G1; pick the primary backend per use case | agent (L3), Clef part after D2, Jev part after K0 | Report artifact; recommended `hi` threshold per use case |
| P1 | gha-issue-triage port: all six fields via `decide()`, LLM only for `reasoning` in the middle band; shadow mode (probabilities in the comment, no labels) → labels at the H1 threshold; defaults off GitHub Models | agent (sibling), after D0 + H1 | Release tag; consumers bumped; tests mocked per adapter |
| P2 | gha-rxiv-paper-eval: `is_relevant` → `noul` via `decide()` as #58's first registry entry; fix `eval-papers-dispatch.yaml`; accept `api_base` as a reusable-workflow secret so ai-agents-research can delete its `LLM_BASE_URL` variable | agent (sibling), after D0 + H1 | Release tag; ai-agents-research bumped; Jev ≥ 83.6% agreement with fewer false accepts on G1 |
| ~~D1~~ | ~~Microsoft Decision-1 in the system-1 landscape~~ | agent (L4) | Shipped: #653. Same `state` + `noul`/`choice`/`score` shape as Jev at `<endpoint>/providers/microsoft/v1/systemone` (optional `criteria`, `api-key` header), so a later `decide()` adapter is cheap; not built (YAGNI) |
| E1 | Estate convention doc in qte77/.github: decision first, defaults, secret names, escalation bands | agent, after P1 | Merged; linked from the 4 model-using READMEs |
| ~~N1~~ | ~~Owner leads 2026-10-11 (28 links), folded in four lanes~~ | agent | Shipped: F3 #662 (anatomy skill, herdr refresh, Strata: documents `ANTHROPIC_BASE_URL` for Claude Code), F1 #663 (AnyJev: self-hosted Apache-2.0 Jev-style decider, an H1 candidate next to Jev and Clef; typesafe-computer-use), F4 #664 (moli, uber/ADR, IdeaScientist, harness-cost paper under the cost-performance metric, new rea and minigraf docs), F2 #666 (OpenRig, TrueForge, AECP, MemoType/TriMEM, GraphJin). Held and skipped leads: see Deferred |
| ~~N2~~ | ~~Usage and token optimization~~ | agent | Shipped: #674 (cache-TTL controls and precedence; corrected two stale claims; resume/continue/fork; `-p` result fields + jq; wrap-up allowance; usage-limit best practices) |
| ~~N3~~ | ~~Org Console API key for headless Claude Code + platform admin~~ | agent | Shipped: #673 (extends `CC-web-auth-setup-analysis.md`) |
| ~~N4~~ | ~~Refresh mods, channels, scheduled tasks, slash commands, docs index~~ | agent | Shipped: #675 (`scheduled-tasks` now documents `/loop`; cloud routines are `routines`) |
| ~~N5~~ | ~~Claude Code goals~~ | agent | Shipped: #676 (`docs/cc-native/sessions/CC-goal-analysis.md`) |
| ~~N7~~ | ~~Owner leads 2026-10-15~~ | agent | Shipped: #677 (Maritime, Ora, Lightsage arenas + payments tracker, AA Coding Agent Index), #678 (AA Decision Index, live and launch views; GLiDE, Celeris-1 Decision, d1 and d1-ultra, Mercury Decide). Held: colin.chat. For H1: d1-ultra (Liquid API) and Clef (existing Cloudflare token) need no TypeSafe key |
| ~~N6~~ | ~~Hub and README rows; strike N2–N5 and N7~~ | agent | Shipped: this PR. Falsification workflow (owner, 2026-10-15) checked 70 claims across #674–#678: 13 wrong or overstated, all fixed before merge |
| ~~N8~~ | ~~`/code-review` and ultrareview from first-party docs~~ | agent | Shipped: #683 (tools inventory rows + section, official-plugins three-way table, `/review-pr` example fixed). Falsification: 13 of 14 claims confirmed; the plugin author/version attribution was corrected before merge |
| Q1 | qte77/qte77: drop the stale `models: read` in `repo-registry.yml`, retire the GitHub Models icon in README (#31) | agent, after E1 | PR merged in qte77/qte77; #31 updated |
| ~~W12~~ | ~~Regenerate W12 in gha-rxiv-feed-action (#206), then backfill W12 here~~ | agent (L5) | Shipped: feed #207 (delete), #209 (fix: OR'd topics now grouped before the `submittedDate` range; the date path had bounded only the last category), #210 (2,875 rows, 9 columns); triage #655 (87 relevant) |
| ~~N9~~ | ~~Owner leads 2026-10-19 – 2026-10-22~~ | agent | Shipped: #690 + #694 (`/goal` paired with a task list; goal loops across coding agents; `claude -p` needs a permission mode from v2.1.302), qte77/qte77 #194 + #197 (Phase A with `/goal`, headless permission fix), qte77/qte77 #195 (one plan file per arc), #693 (jev-browser, awesome-jev catalogs), #695 (DevTool Arena / Lightsage refresh, conflict-of-interest note), #696 (agent payment protocols: MPP, L402, UCP, Visa, Mastercard; 32/33 claims survived falsification), #697 (Omi Health medical STT benchmark), #698 (Onyx), #699 (OpenUI), #700 (ADLC artifact loop, prompt-injection caution), #701 (mods refresh + community catalogs). Pricing/positioning posts routed to qte77/agentic-market-research-to-gtm#21 |
| R1 | GEO/AEO for AI search: AI-crawler controls (robots.txt user agents, Cloudflare AI Crawl Control), refresh `CC-llms-txt-analysis.md` (updated 2026-06-22); a new discoverability landscape if nothing fits | agent | PR merged; claims first-party and falsified like #696 |
| R2 | Agent-ready businesses: NLWeb, schema.org for agents, consumer MCP connectors (e.g. Checkatrade's Claude connector), OAuth for agents; refresh the Ora entry | agent | PR merged; extends `evaluation-data-resources-landscape.md` / `agent-identity-auth-landscape.md` where they fit |
| R3 | A2A refresh (corpus pins v1.0.1, 2026-05) and "agent marketing" / agent-facing storefronts | agent | PR merged; `ag-ui-protocol-landscape.md` § A2A current |
| R4 | Vendor docs missing their goal features: `codex-cli-analysis.md`, `cursor-analysis.md`, `antigravity-analysis.md`, `vscode-copilot-chat-analysis.md`, `github-copilot-cli-analysis.md`; `kiro-analysis.md` still says "autopilot" (now `/autonomous on`, v2.31.0) | agent | Each doc points to `goal-loops-landscape.md`; Kiro wording current |
| R5 | Visa Trusted Agent Protocol next to Web Bot Auth in `agent-identity-auth-landscape.md` (only cross-referenced from the payments doc so far) | agent | Section added, RFC 9421 and the sample repo cited |
| R6 | Goal → KR loop gaps in qte77/qte77: KR `eval:` and the `/goal` condition are unlinked; no `/goal` session can close a KR (merge is owner-gated, by design); nothing triggers `goal_rollup.py`; `goals.md` doesn't name the plan `NNN`. **Default:** a doc-only proposal in `docs/goals.md`, no automation yet | agent (sibling), owner merges | PR in qte77/qte77 merged |
| R7 | Marketplace product SEO/ASO (server-rendered pages, schema.org listings, city × service pages, app-store listing) | owner | Owner names the product repo; the plan goes there, linking this repo's research |
| R8 | DevTool Arena change monitor. **Default:** none — re-check by hand per docs refresh (no data licence, conflict of interest, repo rule against copying external data) | owner | Owner keeps the default, or asks for a monthly changelog-hash monitor that only opens an issue |
| R9 | Microsoft 365 agent research: no PR or issue found in this repo (nearest: qte77/__azure-doc-workflows#544) | owner | Owner says where it went, or asks for a research lane |
| R10 | GPG signing for qte77/qte77 failed on 2026-10-22 ("No secret key"; worked earlier the same week) | owner | Codespaces trusted-repos setting checked; a signed commit succeeds |
| ~~R11~~ | ~~`/focus` (focus view) and `viewMode` from the first-party commands reference~~ | agent | Shipped: this PR (row in `CC-tools-inventory.md` § Slash Commands; `viewMode` values/default not yet verified verbatim) |

**Loop (not rows):** weekly bot triage PRs (changelog/community/learnings) await owner review.

**Deferred** (gate: owner; reason):

- gha-ai-changelog and gha-repo-index ports: no consumer found / AI off by default (owner, 2026-10-10). Note only on #45 / #20.
- OpenAI Decisions and Perplexity adapters: beta APIs and no key.
- Laya self-hosting: no use case yet.
- Owner leads 2026-10-22, not folded here: the positioning and founder-mental-model LinkedIn posts (opinion, lead funnels; listed in qte77/agentic-market-research-to-gtm#21); MrJev's `awesome-jev-1` and `jev-browser` (stale forks — upstream cited in #693).
- Owner leads 2026-10-11, held: helix-foundry (4 days old, no agent surface of its own), MIMESIS 2610.09484 (placement unclear), CLIFT 2610.06829 (calibration-adjacent, no fitting section yet), the CAD blog behind lnkd.in/emArvKmz (one self-reported case, no code). Skipped: WeKnora (already covered, 2026-09-30), fastapi/asyncer and openRigProject/openRig (no agent angle; the latter is ham-radio software, unrelated to mvschwarz/openrig), 2610.07907 (no agent angle, its repo 404s), manglekuo.com / tfl.manglekuo.com (personal portfolio). The Unsloth decision notebook and a duplicate 2610.07907 were already handled (#657).
