"""Pure functions for the CF Workers AI relevance-filter model-comparison eval.

One-off eval (.github/scripts/eval-relevance-models.py) comparing three
Cloudflare Workers AI models against the retired GitHub Models gpt-4o-mini
pipeline's own verdicts. Reproduces the retired production script's
prompt/parsing exactly (qte77/gha-rxiv-paper-eval v0.4.0
``scripts/eval_papers.py``):

- ``DEFAULT_RELEVANCE_PROMPT`` — verbatim copy of lines 42-50.
- ``build_messages`` — mirrors the ``is_relevant`` user-prompt format
  (lines 507-511) and the ``ArxivCsvRow.to_paper`` category/title
  normalization (lines 176-190).
- ``build_labelled_set`` — mirrors ``_prefilter`` with no category filter
  (lines 682-690): a plain head cut of the feed CSV, first ``cap`` rows.

No HTTP / os.environ / sys.exit here — the entry script owns those.
"""
from __future__ import annotations

import csv
import io
import re

DEFAULT_RELEVANCE_PROMPT = (
    "You are a relevance classifier. Reply with a single token: YES or NO. "
    "A paper is relevant if it could plausibly inform research on: {topic}. "
    "Methodology papers (computational tools, simulation methods, ML / AI "
    "frameworks, structure-guided design pipelines, scaffold-engineering "
    "techniques) count even when their experimental system differs from the "
    "topic's primary targets, provided the methodology is transferable. "
    "When borderline, prefer YES if methodology is transferable."
)

_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_UNCLOSED_THINK_RE = re.compile(r"<think>", re.IGNORECASE)


def strip_think_blocks(raw: str) -> str:
    """Remove complete ``<think>...</think>`` blocks; strip leading whitespace.

    A closed pair is fully removed. An unclosed ``<think>`` (the model's
    reasoning ran past ``max_tokens`` before it could close the tag) is left
    in place — ``parse_verdict`` treats a still-open think block as no
    answer emitted, not as a NO.
    """
    return _THINK_BLOCK_RE.sub("", raw).lstrip()


def parse_verdict(raw: str | None, *, strip_think: bool = False) -> str:
    """Parse one model response into "YES", "NO", or "UNPARSEABLE".

    Mirrors production's ``raw.strip().upper().startswith("YES")`` exactly
    when ``strip_think`` is False (the "strict" config — measures the
    retired pipeline's literal behaviour, unclosed-think-tag text included).
    When ``strip_think`` is True (the "relaxed" config), closed think blocks
    are removed first; a still-unclosed think block after stripping means
    the model never reached an answer, so it counts as UNPARSEABLE rather
    than a NO. Empty/None input is always UNPARSEABLE — production would
    treat it as a plain NO, but that conflates "no answer" with "answered
    NO", which this eval needs to keep apart.
    """
    if not raw or not raw.strip():
        return "UNPARSEABLE"
    text = strip_think_blocks(raw) if strip_think else raw
    text = text.strip()
    if not text or (strip_think and _UNCLOSED_THINK_RE.search(text)):
        return "UNPARSEABLE"
    return "YES" if text.upper().startswith("YES") else "NO"


def build_messages(topic: str, title: str, category: str, abstract: str) -> list[dict[str, str]]:
    """Build the chat messages exactly as production ``is_relevant`` does."""
    system_prompt = DEFAULT_RELEVANCE_PROMPT.format(topic=topic)
    user_prompt = f"Title: {title}\nCategory: {category}\n\nAbstract: {abstract or '(unavailable)'}"
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def _row_category(row: dict) -> str:
    """Primary category: ``(Categories or Category).split(';')[0]``."""
    raw = row.get("Categories") or row.get("Category") or ""
    return raw.split(";")[0].strip()


def _row_title(row: dict) -> str:
    """Title normalized like ``ArxivCsvRow.to_paper``: strip, then strip a
    wrapping single-quote, then strip again."""
    return (row.get("Title") or "").strip().strip("'").strip()


def _row_id(row: dict) -> str:
    return row.get("ID") or row.get("DOI") or ""


def build_labelled_set(csv_text: str, accepted_ids: set[str], cap: int = 50) -> list[dict]:
    """Build the labelled evaluation set: the first ``cap`` CSV rows, each
    labelled YES/NO by membership in ``accepted_ids`` (the retired
    pipeline's own accepted-paper set for that week — NOT ground truth).

    Mirrors production's ``_prefilter`` with no category filter: a plain
    head cut of the feed, not a random or stratified sample.
    """
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)[:cap]
    labelled = []
    for row in rows:
        paper_id = _row_id(row)
        labelled.append({
            "id": paper_id,
            "title": _row_title(row),
            "category": _row_category(row),
            "abstract": row.get("Abstract") or "",
            "label": "YES" if paper_id in accepted_ids else "NO",
        })
    return labelled


def _percentile(sorted_values: list[float], pct: float) -> float:
    """Return the ``pct`` percentile (0-1) of an already-sorted list by index
    (not ``statistics.quantiles``, which needs n >= 2)."""
    if not sorted_values:
        return 0.0
    idx = min(len(sorted_values) - 1, round(pct * (len(sorted_values) - 1)))
    return sorted_values[idx]


def _agreement_count(records: list[dict]) -> int:
    return sum(1 for r in records if r["pred"] == r["label"])


def _false_accept_count(records: list[dict]) -> int:
    return sum(1 for r in records if r["pred"] == "YES" and r["label"] == "NO")


def _false_reject_count(records: list[dict]) -> int:
    return sum(1 for r in records if r["pred"] == "NO" and r["label"] == "YES")


def _unparseable_count(records: list[dict]) -> int:
    return sum(1 for r in records if r["pred"] == "UNPARSEABLE")


def _latency_stats(records: list[dict]) -> tuple[float, float]:
    """Return ``(mean_latency, p95_latency)`` in seconds."""
    latencies = sorted(r["latency"] for r in records if r.get("latency") is not None)
    mean_latency = sum(latencies) / len(latencies) if latencies else 0.0
    return mean_latency, _percentile(latencies, 0.95)


def compute_metrics(records: list[dict]) -> dict:
    """Compute agreement/false-accept/false-reject/unparseable/latency stats.

    Each record: ``{"pred": "YES"|"NO"|"UNPARSEABLE", "label": "YES"|"NO",
    "latency": float}``. Agreement's denominator is the total call count
    ``n`` — an UNPARSEABLE call counts against agreement rather than being
    excluded, since it produced no usable classification. Invariant:
    ``agree + false_accept + false_reject + unparseable == n``.
    """
    n = len(records)
    mean_latency, p95_latency = _latency_stats(records)
    return {
        "n": n,
        "agreement_pct": round(100 * _agreement_count(records) / n, 1) if n else 0.0,
        "false_accept": _false_accept_count(records),
        "false_reject": _false_reject_count(records),
        "unparseable": _unparseable_count(records),
        "mean_latency_s": round(mean_latency, 3),
        "p95_latency_s": round(p95_latency, 3),
    }
