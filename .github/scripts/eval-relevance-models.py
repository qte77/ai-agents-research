#!/usr/bin/env python3
"""One-off model-comparison eval for the paper relevance filter.

GitHub Models was retired 2026-07-30, killing the weekly rxiv-paper-eval
pipeline's LLM backend (reusable action qte77/gha-rxiv-paper-eval v0.4.0).
This script reproduces that pipeline's relevance-classification behaviour
against three Cloudflare Workers AI models and scores each against the
retired model's OWN verdicts (accepted-paper sets in
triage/rxiv/data/arxiv-2026-W<week>.jsonl) — those are labels, not ground
truth. See lib/relevance_eval.py for the pure prompt/parsing/metrics logic
this reuses.

Intended to run only via workflow_dispatch
(.github/workflows/llm-model-eval.yaml); reads the Cloudflare Workers AI
token from the environment (repo secret CF_WORKERS_AI_TOKEN, only present in
Actions).

Usage:
    python eval-relevance-models.py --preflight
    python eval-relevance-models.py --weeks 30 --dry-run
    python eval-relevance-models.py --out llm-model-eval-output

Exit codes:
    0 = eval / dry-run / preflight completed successfully
    1 = preflight call failed (non-auth error)
    2 = preflight: required env var missing
    3 = preflight: token lacks inference permission (401/403)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor_utils import load_jsonl  # noqa: E402
from lib.relevance_eval import (  # noqa: E402
    build_labelled_set,
    build_messages,
    compute_metrics,
    parse_verdict,
)

DEFAULT_MODELS = (
    "@cf/meta/llama-3.1-8b-instruct-fp8,"
    "@cf/qwen/qwen3-30b-a3b-fp8,"
    "@cf/google/gemma-4-26b-a4b-it"
)
DEFAULT_WEEKS = "22,23,24,25,30"
DEFAULT_CONFIGS = "strict:4,relaxed:64"

# Kept in lockstep with rxiv-paper-eval.yaml's `vars.RXIV_TOPIC || '<this>'`
# fallback (only used when the RXIV_TOPIC repo var is unset/empty).
FALLBACK_TOPIC = (
    "LLM-based autonomous agents, tool use and function calling, "
    "multi-agent coordination, agentic evaluation and benchmarking, "
    "and LLM reasoning and planning"
)

FEED_YEAR = "2026"
FEED_URL_TMPL = "https://raw.githubusercontent.com/qte77/gha-rxiv-feed-action/main/data/arxiv/{year}/{week}.csv"
TRIAGE_DATA_DIR = Path(__file__).resolve().parents[2] / "triage" / "rxiv" / "data"

RETRYABLE_CODES = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 3
CALL_TIMEOUT = 60
CAP = 50


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for the eval driver."""
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--models", default=DEFAULT_MODELS, help="Comma-separated Workers AI model ids.")
    p.add_argument("--weeks", default=DEFAULT_WEEKS, help="Comma-separated ISO weeks (arxiv 2026 feed).")
    p.add_argument("--configs", default=DEFAULT_CONFIGS, help="Comma-separated name:max_tokens configs.")
    p.add_argument("--out", default="output", help="Output directory for results.jsonl + summary.md.")
    p.add_argument("--preflight", action="store_true", help="One tiny call to check token permissions, then exit.")
    p.add_argument("--dry-run", action="store_true", help="Build + print per-week dataset counts only; no API calls.")
    return p.parse_args()


def _parse_configs(spec: str) -> list[tuple[str, int]]:
    """Parse ``name:max_tokens,name:max_tokens`` into ``[(name, max_tokens)]``."""
    configs = []
    for part in spec.split(","):
        name, _, tokens = part.partition(":")
        configs.append((name.strip(), int(tokens.strip())))
    return configs


def _base_url() -> str:
    base = os.environ.get("LLM_BASE_URL", "").rstrip("/")
    if not base:
        raise SystemExit("LLM_BASE_URL is not set")
    return base


def _endpoint() -> str:
    return f"{_base_url()}/chat/completions"


def _host() -> str:
    """Host:port only (via netloc) — never log the full base URL, which
    embeds the Cloudflare account id."""
    return urllib.parse.urlparse(_base_url()).netloc or "?"


def _load_accepted_ids(week: str) -> set[str]:
    """Accepted arxiv ids for a week, from the committed triage JSONL."""
    path = TRIAGE_DATA_DIR / f"arxiv-{FEED_YEAR}-W{week}.jsonl"
    return {rec["doi"] for rec in load_jsonl(path) if rec.get("doi")}


def _fetch_feed_csv(week: str) -> str:
    url = FEED_URL_TMPL.format(year=FEED_YEAR, week=week.zfill(2))
    req = urllib.request.Request(url, headers={"User-Agent": "rxiv-model-eval/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # nosec B310  # noqa: S310
        return resp.read().decode("utf-8")


def build_week_dataset(week: str) -> tuple[list[dict], list[str]]:
    """Fetch + label one week's dataset.

    Returns ``(labelled_rows, accepted_ids_outside_the_first_cap_rows)`` —
    the second element should normally be empty; a non-empty result means an
    accepted paper from that week's triage data fell outside the evaluated
    window and its label can't be reproduced.
    """
    csv_text = _fetch_feed_csv(week)
    accepted = _load_accepted_ids(week)
    labelled = build_labelled_set(csv_text, accepted, cap=CAP)
    in_window_ids = {r["id"] for r in labelled}
    return labelled, sorted(accepted - in_window_ids)


def _build_datasets(weeks: list[str]) -> dict[str, list[dict]]:
    """Build + print per-week dataset counts for every requested week."""
    datasets: dict[str, list[dict]] = {}
    for week in weeks:
        labelled, out_of_window = build_week_dataset(week)
        yes_count = sum(1 for r in labelled if r["label"] == "YES")
        print(
            f"W{week}: rows_used={len(labelled)} yes_labels={yes_count} "
            f"accepted_outside_window={out_of_window}",
            file=sys.stderr,
        )
        datasets[week] = labelled
    return datasets


def _post_raw(model: str, messages: list[dict], max_tokens: int) -> bytes:
    """Single POST to the chat-completions endpoint; returns the raw body.

    Raises ``HTTPError``/``URLError``/``TimeoutError`` on failure — callers
    decide retry policy.
    """
    payload = json.dumps({
        "model": model,
        "temperature": 0,
        "max_tokens": max_tokens,
        "messages": messages,
    }).encode("utf-8")
    token = os.environ.get("CF_WORKERS_AI_TOKEN", "")
    req = urllib.request.Request(
        _endpoint(),
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=CALL_TIMEOUT) as resp:  # nosec B310  # noqa: S310
        return resp.read()


def _call_model(model: str, messages: list[dict], max_tokens: int) -> tuple[dict, float]:
    """One POST; returns ``(parsed_json_body, latency_seconds)``."""
    start = time.monotonic()
    body = json.loads(_post_raw(model, messages, max_tokens))
    return body, time.monotonic() - start


def _call_with_retry(model: str, messages: list[dict], max_tokens: int) -> tuple[dict | None, float, str | None]:
    """Call with retry on 429/5xx and transient network errors.

    Returns ``(body, latency, error)`` — ``error`` is None on success. A
    non-retryable HTTP error (e.g. a model rejecting the ``system`` role) is
    recorded and returned immediately rather than raised, so one model's
    failure doesn't abort the run for the others.
    """
    last_err: str | None = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            body, latency = _call_model(model, messages, max_tokens)
            return body, latency, None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            last_err = f"HTTP {exc.code}: {detail[:200]}"
            if exc.code not in RETRYABLE_CODES:
                return None, 0.0, last_err
        except (urllib.error.URLError, TimeoutError) as exc:
            reason = getattr(exc, "reason", exc)
            last_err = f"network error: {reason}"
        if attempt + 1 < MAX_ATTEMPTS:
            time.sleep(2**attempt)
    return None, 0.0, last_err


def _record_call(
    model: str, config_name: str, row: dict, max_tokens: int, strip_think: bool, topic: str
) -> dict:
    """Run one relevance call and return its full result record."""
    messages = build_messages(topic, row["title"], row["category"], row["abstract"])
    body, latency, err = _call_with_retry(model, messages, max_tokens)
    base = {
        "model": model, "config": config_name, "id": row["id"], "label": row["label"],
        # None (not 0.0) on error, so a failed call is excluded from the
        # mean/p95 latency stats instead of dragging them toward zero.
        "latency": None if err is not None else round(latency, 3),
    }
    if err is not None:
        return {
            **base, "pred": "UNPARSEABLE", "raw": "", "error": err,
            "finish_reason": None, "usage": None, "reasoning_content": None,
        }
    choice = (body.get("choices") or [{}])[0]
    message = choice.get("message") or {}
    raw = message.get("content") or ""
    return {
        **base,
        "pred": parse_verdict(raw, strip_think=strip_think),
        "raw": raw[:200], "error": None,
        "finish_reason": choice.get("finish_reason"),
        "usage": body.get("usage"),
        "reasoning_content": message.get("reasoning_content"),
    }


def _run_model_config(
    model: str, config_name: str, max_tokens: int, weeks: list[str],
    datasets: dict[str, list[dict]], topic: str, out_f,
) -> list[dict]:
    """Run every row for one model x config across all weeks; stream to ``out_f``."""
    # Reason: only the literal "strict" config reproduces production's raw
    # parsing untouched; every other config name (not just "relaxed") gets
    # think-block stripping. A --configs override with a third name inherits
    # this on purpose -- "strict" is the one config that must stay literal.
    strip_think = config_name != "strict"
    records = []
    for week in weeks:
        for row in datasets[week]:
            rec = _record_call(model, config_name, row, max_tokens, strip_think, topic)
            rec["week"] = week
            out_f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            out_f.flush()
            records.append(rec)
    return records


def _write_summary(out_dir: Path, metrics_table: list[dict]) -> None:
    lines = [
        "# Relevance-filter model comparison",
        "",
        "Labels are the retired GitHub Models gpt-4o-mini verdicts, not ground truth.",
        "",
        "Agreement % denominator is total calls per model x config "
        "(an unparseable call counts against agreement, not excluded from it).",
        "",
        "| Model | Config | n | Agreement % | False-accept | False-reject | "
        "Unparseable | Mean latency (s) | P95 latency (s) |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for row in metrics_table:
        m = row["metrics"]
        lines.append(
            f"| {row['model']} | {row['config']} | {m['n']} | {m['agreement_pct']} | "
            f"{m['false_accept']} | {m['false_reject']} | {m['unparseable']} | "
            f"{m['mean_latency_s']} | {m['p95_latency_s']} |"
        )
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n")


def _run_full_eval(
    models: list[str], configs: list[tuple[str, int]], weeks: list[str],
    datasets: dict[str, list[dict]], topic: str, out_dir: Path,
) -> None:
    metrics_table: list[dict] = []
    with (out_dir / "results.jsonl").open("w") as f:
        for model in models:
            for config_name, max_tokens in configs:
                records = _run_model_config(model, config_name, max_tokens, weeks, datasets, topic, f)
                metrics = compute_metrics(records)
                metrics_table.append({"model": model, "config": config_name, "metrics": metrics})
                print(f"{model} / {config_name}: {metrics}", file=sys.stderr)
    _write_summary(out_dir, metrics_table)


def run_preflight(model: str) -> int:
    """One tiny inference call; print HTTP status + truncated body.

    Exit codes: 2 = required env var missing, 3 = 401/403 (token lacks
    inference permission), 1 = any other failure, 0 = success.
    """
    missing = [n for n in ("CF_WORKERS_AI_TOKEN", "LLM_BASE_URL") if not os.environ.get(n)]
    if missing:
        print(f"FAIL: missing required env var(s): {', '.join(missing)}", file=sys.stderr)
        return 2

    print(f"Preflight: POST /chat/completions on {_host()} model={model}", file=sys.stderr)
    messages = [{"role": "user", "content": "Reply with a single token: YES or NO. YES"}]
    try:
        body_bytes = _post_raw(model, messages, max_tokens=1)
        status = 200
    except urllib.error.HTTPError as exc:
        status = exc.code
        body_bytes = exc.read() if exc.fp else b""
    except (urllib.error.URLError, TimeoutError) as exc:
        reason = getattr(exc, "reason", exc)
        print(f"FAIL: network error reaching {_host()}: {reason}", file=sys.stderr)
        return 1

    body_text = body_bytes.decode("utf-8", errors="replace")
    print(f"Preflight status: {status}", file=sys.stderr)
    print(f"Preflight body (first 300 chars): {body_text[:300]}", file=sys.stderr)

    if status in (401, 403):
        print(
            "FAIL: token lacks inference permission — create a token via the "
            "dashboard's 'Create a Workers AI API Token' template "
            "(Workers AI Read + Edit).",
            file=sys.stderr,
        )
        return 3
    if status >= 400:
        print(f"FAIL: preflight call failed with HTTP {status}", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    """Parse args and dispatch to preflight / dry-run / full eval."""
    args = parse_args()
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    weeks = [w.strip() for w in args.weeks.split(",") if w.strip()]
    configs = _parse_configs(args.configs)
    topic = os.environ.get("RXIV_TOPIC") or FALLBACK_TOPIC

    if args.preflight:
        return run_preflight(models[0])

    datasets = _build_datasets(weeks)
    if args.dry_run:
        return 0

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    _run_full_eval(models, configs, weeks, datasets, topic, out_dir)
    print(f"Done. Wrote {out_dir / 'results.jsonl'} and {out_dir / 'summary.md'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
