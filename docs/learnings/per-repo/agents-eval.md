---
title: Agents-eval Learnings
description: Project-specific patterns from qte77/Agents-eval — PydanticAI, Streamlit, BERTScore, evaluation pipeline, MAS orchestration.
created: 2026-03-27
updated: 2026-03-27
source: https://github.com/qte77/Agents-eval
---

## Agents-eval Learnings

Project-specific patterns from [qte77/Agents-eval](https://github.com/qte77/Agents-eval). Cross-repo patterns are in [../cross-repo-digest.md](../cross-repo-digest.md).

This file is a write-back target for Ralph's `compound_writeback()`. Entries below are seeded from `AGENT_LEARNINGS.md` and will be appended by Ralph as new patterns are discovered.

---

## PydanticAI & LLM Providers

### OpenAI-Compatible Provider Strict Tool Definitions

- **Context**: PydanticAI with OpenAI-compatible providers (Cerebras, Groq)
- **Problem**: PydanticAI's per-tool `strict` inference causes HTTP 422 with mixed values.
- **Solution**: Disable via `OpenAIModelProfile(openai_supports_strict_tool_definition=False)`.
- **References**: `src/app/llms/models.py`

### Auto Provider Model Resolution via PROVIDER_REGISTRY

- **Context**: `LLMJudgeEngine` with `tier2_provider=auto`
- **Problem**: Auto-resolved provider inherits `tier2_model` default (`gpt-4o-mini`) which doesn't exist on the resolved provider.
- **Solution**: After auto-resolution, consult `PROVIDER_REGISTRY[provider].default_model` when `chat_model=None`.
- **References**: `src/app/judge/llm_evaluation_managers.py`, `src/app/data_models/app_models.py`

### Cerebras Structured Output Non-Compliance

- **Context**: PydanticAI agents with Cerebras `gpt-oss-120b` and structured output schemas
- **Problem**: Three failure modes: score fields as text, wrong output type for general queries, tool arg/output confusion.
- **Solution**: `BeforeValidator` coercions on result models; `enable_review_tools` default `False`; explicit tool docstrings.
- **References**: `src/app/data_models/peerread_models.py`, `src/app/app.py:343`, `src/app/agents/agent_system.py`

---

## Streamlit

### Background Execution Strategy

- **Context**: Long tasks (LLM calls, pipelines) without blocking Streamlit UI
- **Problem**: Tab navigation aborts execution; `threading.Thread` session state writes not thread-safe.
- **Solution**: Prefer `st.fragment` for isolated re-runs; fall back to `threading.Thread` + synchronized writes when execution must survive full re-renders.
- **References**: `src/gui/pages/run_app.py`

---

## BERTScore / Metrics

### Class-Level Lazy Loading with Failure Caching

- **Context**: `TraditionalMetricsEngine` initializing BERTScorer (HuggingFace model download)
- **Problem**: Per-instance lazy loading retries init on every new engine instance. Hypothesis tests (many instances) exceed deadline.
- **Solution**: Class-level `_bertscore_instance` and `_bertscore_init_failed` flags; first failure cached — no retries.
- **References**: `src/app/judge/traditional_metrics.py`, `tests/evals/test_traditional_metrics.py`

---

## Data Models

### Pydantic `validation_alias` for External Data Mapping

- **Context**: Pydantic models with different external key names (PeerRead `IMPACT` -> `impact`)
- **Problem**: `alias` breaks constructor signature; `model_validator(mode="before")` couples to external format.
- **Solution**: Use `validation_alias` (only affects `model_validate()`) + `ConfigDict(populate_by_name=True)`.
- **References**: `src/app/data_models/peerread_models.py`

---

## Testing

### Test Filesystem Isolation (`tmp_path`)

- **Context**: Tests that mock network calls but call real write paths
- **Problem**: Mocking `download_file` prevents network access but unmocked methods still write to real project directories.
- **Solution**: Always redirect `cache_dir` to `tmp_path` in tests that trigger file writes, even when download is mocked.
- **References**: `tests/data_utils/test_datasets_peerread.py:601`

### Stale Test Fixtures Cause Cross-File Pollution

- **Context**: Full `make test` suite with tests that error due to stale fixtures (patching removed imports)
- **Problem**: Failed fixture setup leaks shared singletons into subsequent test files; test passes alone but fails in suite.
- **Solution**: Delete stale tests promptly. Use `pytest --lf` + bisection to identify the polluter.
- **References**: `tests/gui/test_settings.py` (deleted)

---

## Claude Code / Agent Teams

### Agent Teams Parallel Orchestration

- **Context**: Claude Code agent teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`)
- **Problem**: Need reusable pattern for parallel agent orchestration.
- **Solution**: Independent reviewers with shared task list + dependency-blocked aggregation task.
- **Key Finding**: Parallel reduces latency but token cost scales linearly (N teammates = N instances).
- **References**: `docs/reviews/evaluation-pipeline-parallel-review-2026-02-11.md`

### Claude Code Headless Invocation for Benchmarking

- **Context**: Running CC from Python for MAS vs CC baseline comparison
- **Problem**: `cc_otel` used wrong abstraction — CC tracing is infrastructure (env vars), not application code.
- **Solution**: `claude -p "prompt" --output-format json` via `subprocess.run()`. Collect artifacts from `~/.claude/teams/` + `~/.claude/tasks/`, parse via `CCTraceAdapter`.
- **References**: `scripts/collect-cc-traces/run-cc.sh`, ADR-008

---

## SSRF / Security

### SSRF Allowlist Must Match Actual HTTP Call Sites

- **Context**: SSRF URL validation with domain allowlisting
- **Problem**: Allowlist built from conceptual dependencies rather than actual `validate_url()` call sites.
- **Solution**: Grep for `validate_url(` calls, trace each URL back to its domain. Only list domains that flow through the validation function.
- **References**: `src/app/utils/url_validation.py`, `src/app/data_utils/datasets_peerread.py:300`

---

## Process / Workflow

### PRD Files List Completeness Check

- **Context**: Writing sprint PRD features with acceptance criteria and files lists
- **Problem**: Files referenced in AC or tech requirements missing from Files list; implementers miss changes.
- **Solution**: After writing each feature, verify every file referenced in AC appears in Files with correct annotation.
- **References**: Sprint 6 Features 2, 7

### Review-to-PRD Traceability

- **Context**: Planning a sprint after a security review produced findings tagged for future sprints
- **Problem**: Review findings fall through the cracks between sprints.
- **Solution**: Next PRD must account for every finding: feature, Out of Scope with attribution, or dismissed with rationale.
- **References**: Sprint 5 `docs/reviews/sprint5-code-review.md` -> Sprint 6 Features 10-13

### CVE Version Check Before PRD Story

- **Context**: Writing a CVE remediation story from a security review finding
- **Problem**: Writing the story without checking `pyproject.toml` — CVE already mitigated by current pin.
- **Solution**: Check current dependency version first. If patched, note in PRD and skip.
- **References**: Sprint 6 Feature 10 (scikit-learn CVE dismissed after version check)

### Measurable Acceptance Criteria for Meta-Tasks

- **Context**: PRD meta-tasks (reviews, audits, assessments)
- **Problem**: "Review completed" is not verifiable.
- **Solution**: Three gates: (1) Coverage — every scope item has findings or explicit "no issues", (2) Severity — zero critical unfixed, (3) Artifact — document exists with required structure.
- **References**: Sprint 5 Features 10-11
