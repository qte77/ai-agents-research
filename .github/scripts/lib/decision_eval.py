"""Pure logic for eval-decision-models.py: calibrate decision models on the G1 gold sets.

Plan 0012 row H1. A decision model (Cloudflare Clef, TypeSafe Jev) answers a yes/no question with a
probability; `decide()` in qte77/.github acts when that probability is >= `hi` or <= 1 - `hi` and
sends the middle band to review. This module scores those probabilities against the gold labels
(ROC-AUC with a bootstrap interval, Brier score) and sweeps `hi` to find the smallest threshold
whose acted decisions stay under an error budget. No network here: the entry script calls
`decide()` and hands the probabilities in.
"""
from __future__ import annotations

import json
import random
import re
from collections.abc import Callable, Sequence
from pathlib import Path

from lib.relevance_eval import AGENT_STRICT_PROMPT

# The literal topic the paper gold set was labelled against (data/gold/README.md, Set 1).
# Frozen with the labels: changing it would change the question the labels answer.
GOLD_PAPER_TOPIC = (
    "LLM-based autonomous agents, tool use and function calling, "
    "multi-agent coordination, agentic evaluation and benchmarking, "
    "and LLM reasoning and planning"
)

# Reason: reuse the agent-strict criterion verbatim, minus the chat-model reply-format sentences;
# a decision model answers a typed predicate, not a YES/NO token.
_REPLY_FORMAT = "You are a relevance classifier. Reply with a single token: YES or NO. "
PAPER_QUESTION = {
    "name": "relevant",
    "type": "predicate",
    "instructions": AGENT_STRICT_PROMPT.removeprefix(_REPLY_FORMAT).format(topic=GOLD_PAPER_TOPIC),
}

# The inverse of gha-issue-triage's `irrelevant` predicate, as the issue gold set was labelled
# (data/gold/README.md, Set 2): an in-scope project item for the repository it was filed in.
ISSUE_QUESTION = {
    "name": "relevant",
    "type": "predicate",
    "instructions": (
        "Is this issue relevant to the repository it was filed in? Answer yes for an in-scope "
        "bug report, feature request, documentation or maintenance item for this repository. "
        "Answer no for off-topic, nonsense or test-fixture issues unrelated to the repository's purpose."
    ),
}

_TRANSIENT_RE = re.compile(r"\b(429|5\d\d)\b|timed? ?out", re.IGNORECASE)


def load_gold(items_path: Path, labels_path: Path) -> list[dict]:
    """Join a gold set's items and labels by id: [{id, title, text, context, label}], items order."""
    labels = {}
    for line in labels_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            labels[record["id"]] = bool(record["label"])
    gold = []
    for line in items_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        gold.append(
            {
                "id": item["id"],
                "title": item["title"],
                "text": item["text"],
                "context": item.get("context", ""),
                "label": labels[item["id"]],
            }
        )
    return gold


def paper_state(item: dict) -> str:
    """Title + abstract: the paper labellers' only inputs."""
    return f"Paper title: {item['title']}\n\nAbstract: {item['text']}"


def issue_state(item: dict) -> str:
    """Repo description + issue title + body: the issue labellers' only inputs."""
    return (
        f"Repository description: {item['context']}\n\n"
        f"Issue title: {item['title']}\n\nIssue body: {item['text']}"
    )


def is_transient(error: str | None) -> bool:
    """True for errors worth retrying (rate limit, 5xx, timeout); auth or shape errors are not."""
    return bool(error) and bool(_TRANSIENT_RE.search(error))


def roc_auc(probs: Sequence[float], labels: Sequence[bool]) -> float | None:
    """P(a random positive scores above a random negative), ties counted half; None if one class."""
    pos = [p for p, y in zip(probs, labels, strict=True) if y]
    neg = [p for p, y in zip(probs, labels, strict=True) if not y]
    if not pos or not neg:
        return None
    wins = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def brier(probs: Sequence[float], labels: Sequence[bool]) -> float:
    """Mean squared error of the probabilities against 0/1 outcomes (0 is perfect)."""
    return sum((p - (1.0 if y else 0.0)) ** 2 for p, y in zip(probs, labels, strict=True)) / len(probs)


def bootstrap_ci(
    metric: Callable[[Sequence[float], Sequence[bool]], float | None],
    probs: Sequence[float],
    labels: Sequence[bool],
    n: int = 1000,
    seed: int = 0,
    alpha: float = 0.05,
) -> tuple[float, float] | None:
    """Percentile bootstrap interval for ``metric``; resamples where it is undefined are skipped."""
    # Reason: seeded, reproducible resampling; not used for anything security-related.
    rng = random.Random(seed)  # nosec B311
    size = len(probs)
    values = []
    for _ in range(n):
        idx = [rng.randrange(size) for _ in range(size)]
        value = metric([probs[i] for i in idx], [labels[i] for i in idx])
        if value is not None:
            values.append(value)
    if not values:
        return None
    values.sort()
    low = values[int((alpha / 2) * (len(values) - 1))]
    high = values[int((1 - alpha / 2) * (len(values) - 1))]
    return low, high


def sweep(probs: Sequence[float], labels: Sequence[bool], grid: Sequence[float]) -> list[dict]:
    """For each ``hi``: how many items act (either tail), how many acted wrongly, and coverage."""
    rows = []
    total = len(probs)
    for hi in grid:
        acted = false_accepts = false_rejects = 0
        for p, y in zip(probs, labels, strict=True):
            if p >= hi:
                acted += 1
                false_accepts += not y
            elif p <= 1 - hi:
                acted += 1
                false_rejects += y
        errors = false_accepts + false_rejects
        rows.append(
            {
                "hi": hi,
                "acted": acted,
                "review": total - acted,
                "false_accepts": false_accepts,
                "false_rejects": false_rejects,
                "coverage": acted / total if total else 0.0,
                "error_rate": errors / acted if acted else 0.0,
            }
        )
    return rows


def recommend_hi(rows: list[dict], max_error_rate: float) -> dict | None:
    """The smallest ``hi`` (most coverage) whose acted decisions stay within ``max_error_rate``."""
    for row in sorted(rows, key=lambda r: r["hi"]):
        if row["acted"] and row["error_rate"] <= max_error_rate:
            return row
    return None


def compare_to_baseline(
    current: dict[str, dict],
    baseline: dict[str, dict],
    auc_drop: float = 0.03,
    hi_move: float = 0.05,
) -> list[str]:
    """Drift findings for each ``set/backend:model`` key present in both runs (plan 0013 row A7).

    Flags an ROC-AUC drop above ``auc_drop`` and a recommended ``hi`` that moved by ``hi_move`` or
    more, or that no longer exists. Brier is reported elsewhere but never flagged: it has no agreed
    threshold.
    """
    findings = []
    for key in sorted(current.keys() & baseline.keys()):
        now, base = current[key], baseline[key]
        if now["auc"] is not None and base["auc"] is not None and base["auc"] - now["auc"] > auc_drop:
            findings.append(f"{key}: ROC-AUC fell from {base['auc']:.3f} to {now['auc']:.3f}")
        if base["recommended_hi"] is None:
            continue
        if now["recommended_hi"] is None:
            findings.append(f"{key}: no hi meets the rule now (baseline {base['recommended_hi']:.2f})")
        # Reason: the sweep grid steps by 0.05, so compare with a small tolerance for float error.
        elif abs(now["recommended_hi"] - base["recommended_hi"]) >= hi_move - 1e-9:
            findings.append(
                f"{key}: recommended hi moved from {base['recommended_hi']:.2f} to {now['recommended_hi']:.2f}"
            )
    return findings
