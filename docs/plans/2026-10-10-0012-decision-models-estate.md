---
title: Decision models first across the qte77 GitHub Actions estate
status: draft
created: 2026-10-10
updated: 2026-10-10
---

## Handoff (start here)

**What this arc is:**

- Every qte77 GitHub Action that calls a model asks **decision-shaped** questions through a decision model first: a typed yes/no probability (`noul`), a choice, or a score, with Jev as the default.
- A generative LLM, Cloudflare Workers AI through an OpenAI-compatible `api_base`, is used **only for free text** and as the fallback.
- One shared `decide()` lives in `qte77/.github/actions/decide/`.

**Status:** draft. **The owner approves it first** ("proceed" → set `status: approved`); no lanes start before then. Nothing here is built yet. One thing is already done: on 2026-10-10 `LLM_BASE_URL` was set as a repo **secret** in the 10 repos listed under K0.

**How to run it:**

1. Reconcile: `git log`, `gh pr list`, and the gate rows below. The plan may be stale; check before acting.
2. Run **Phase A** as parallel lanes. Each lane is a subagent with `isolation: worktree`, briefed with the lane's file fence (Lanes table). The main session never edits a lane's files.
3. Sibling repos are edited **in their own repo**: the subagent's working directory is that repo's clone under `/workspaces/qte77/<repo>`, and it follows that repo's CLAUDE.md/AGENTS.md/CONTRIBUTING.md. The worktree requirement applies there too: `git -C <repo> worktree add`.
4. The main session reviews each lane's PR **at source** (strongest claims, test run), merges, and strikes the row **in the same PR or right after**.
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
- **Cloudflare fallback:** `POST {LLM_BASE_URL}/chat/completions` with model `@cf/meta/llama-3.3-70b-instruct-fp8-fast`, asking for a constrained JSON answer. `confidence=None`.
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
| L3 | G1 + H1 | ai-agents-research | `.github/scripts/**`, `.github/workflows/llm-model-eval.yaml`, `tests/**`, `triage/gold/**` (new) |
| L4 | D1 | ai-agents-research | `docs/non-cc/reference/system-1-decision-models-landscape.md`, one changelog fragment |
| L5 | W12 | qte77/gha-rxiv-feed-action | `data/arxiv/2026/12.csv` (via its workflow) |

L1–L5 run in parallel. P1 and P2 start after L1 merges (they pin its SHA) and after H1, which sets thresholds. E1 runs after P1.

## Remaining work

| Row | Item | Gate | Done when |
|---|---|---|---|
| T0 | Tracking issue in ai-agents-research; link it in this plan's frontmatter | agent | Issue exists, linked both ways |
| K0 | Create 4 keys (Jev + CF per use case) into one local file; agent sets `TYPESAFE_API_KEY` + `CF_WORKERS_AI_TOKEN` in each repo, then deletes the file. `LLM_BASE_URL` secret already set (10 repos) | owner | `gh secret list` shows both secrets in every target repo |
| D0 | `decide` action in qte77/.github, TDD per the map | agent (L1) | `test-decide.yml` green; README documents schema, bands, secrets |
| C1 | 7 consumer PRs (pin + CF inputs + drop `models: read`); switch gha-issue-triage self-triage and ai-agents-research to `secrets.LLM_BASE_URL`, delete the variables | agent (L2), after K0 | One test issue per consumer gets a triage comment; self-triage run green |
| G1 | Gold sets: ~60 issues (from past triage comments) + 100 papers (W40 ranked pool), agent-labelled from title/body/abstract, with an independent second pass on disagreements | agent (L3) | `triage/gold/*.jsonl` committed with label rationale; owner spot-check optional |
| H1 | Jev runner in the eval harness: AUC + bootstrap CI, Brier, threshold sweep (port feelings `metrics.py`); compare Jev vs Llama-70B agent-strict on G1 | agent (L3), after K0 | Report artifact; recommended `hi` threshold per use case |
| P1 | gha-issue-triage port: all six fields via `decide()`, LLM only for `reasoning` in the middle band; shadow mode (probabilities in the comment, no labels) → labels at the H1 threshold; defaults off GitHub Models | agent (sibling), after D0 + H1 | Release tag; consumers bumped; tests mocked per adapter |
| P2 | gha-rxiv-paper-eval: `is_relevant` → `noul` via `decide()` as #58's first registry entry; fix `eval-papers-dispatch.yaml` | agent (sibling), after D0 + H1 | Release tag; ai-agents-research bumped; Jev ≥ 83.6% agreement with fewer false accepts on G1 |
| D1 | Microsoft Decision-1 in the system-1 landscape (Azure catalog: GA, Qwen3.5-9B base; licence/pricing from first-party pages) | agent (L4) | Section merged; owner may veto |
| E1 | Estate convention doc in qte77/.github: decision first, defaults, secret names, escalation bands | agent, after P1 | Merged; linked from the 4 model-using READMEs |
| W12 | Regenerate W12 in gha-rxiv-feed-action (#206), then backfill W12 here | agent (L5) | `12.csv` has 9 columns with abstracts; W12 triage PR merged |

**Loop (not rows):** weekly bot triage PRs (changelog/community/learnings) await owner review.

**Deferred:**

- gha-ai-changelog and gha-repo-index ports (note on #45 / #20);
- OpenAI Decisions and Perplexity adapters (beta, no key);
- Laya self-hosting.
