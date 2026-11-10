#!/usr/bin/env python3
"""Run decision models over the G1 gold sets and report calibration (plan 0012 row H1).

Calls `decide()` from a checkout of qte77/.github (`actions/decide/decide.py`) once per gold item
and model, then writes `records.jsonl` and `summary.md`: ROC-AUC with a bootstrap interval and
Brier score (papers only; the issue set has 3 negatives), accuracy at 0.5, and a sweep of the
`hi` threshold with the recommended value per set. Pure scoring lives in lib/decision_eval.py.

Credentials come from the environment, as `decide()` reads them: CF_WORKERS_AI_TOKEN and
LLM_BASE_URL for the `clef` backend, TYPESAFE_API_KEY for `jev`.

Usage:
    python eval-decision-models.py --decide-dir DIR [--models clef:clef-flash,clef:clef]
        [--sets papers,issues] [--limit N] [--out DIR]

Exit codes: 0 = report written; 1 = a model answered no item at all (auth or endpoint failure).
"""
import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.decision_eval import (
    ISSUE_QUESTION,
    PAPER_QUESTION,
    bootstrap_ci,
    brier,
    is_transient,
    issue_state,
    load_gold,
    paper_state,
    recommend_hi,
    roc_auc,
    sweep,
)

GOLD_DIR = Path(__file__).parent / "data" / "gold"
SETS = {
    "papers": (paper_state, PAPER_QUESTION),
    "issues": (issue_state, ISSUE_QUESTION),
}
GRID = [round(0.5 + 0.05 * i, 2) for i in range(10)]  # 0.50 .. 0.95
# Pre-registered rule (fixed before any run): recommend the smallest hi whose acted decisions
# (both tails) are wrong at most this often. Coverage at that hi is reported next to it.
MAX_ERROR_RATE = 0.05
SEED = 20261110
BOOTSTRAP_N = 1000
RETRIES = 3
CALL_TIMEOUT = 60.0


def load_decide(decide_dir: Path):
    """Import decide.py from a qte77/.github checkout without installing it."""
    path = decide_dir / "decide.py"
    spec = importlib.util.spec_from_file_location("decide", path)
    if spec is None or spec.loader is None:
        sys.exit(f"ERROR: cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.decide


def ask(decide, state: str, question: dict, backend: str, model: str) -> tuple[dict, int]:
    """One decide() call, retried with backoff while the escalate reason looks transient."""
    for attempt in range(1, RETRIES + 1):
        answer = decide(state, [question], backend=backend, model=model, timeout=CALL_TIMEOUT)[question["name"]]
        if answer.get("probability") is not None or not is_transient(answer.get("error")):
            return answer, attempt
        time.sleep(2**attempt)
    return answer, RETRIES


def fmt(value, digits: int = 3) -> str:
    return "n/a" if value is None else f"{value:.{digits}f}"


def summarize(set_name: str, model_key: str, records: list[dict]) -> tuple[list[str], int]:
    """Markdown lines for one set x model, and the number of answered items."""
    answered = [r for r in records if r["probability"] is not None]
    probs = [r["probability"] for r in answered]
    labels = [r["label"] for r in answered]
    lines = [f"### {set_name} — {model_key}", ""]
    negatives = sum(not r["label"] for r in records)
    lines.append(
        f"Items {len(records)} ({negatives} negative), answered {len(answered)}, "
        f"escalated {len(records) - len(answered)}."
    )
    if not answered:
        errors = sorted({r["error"] or "" for r in records})[:3]
        lines += ["", f"No answers. Errors: {errors}", ""]
        return lines, 0
    accuracy = sum((p >= 0.5) == y for p, y in zip(probs, labels, strict=True)) / len(probs)
    lines.append(f"Accuracy at 0.5: {fmt(accuracy)}. Brier: {fmt(brier(probs, labels))}.")
    if set_name == "papers":
        ci = bootstrap_ci(roc_auc, probs, labels, n=BOOTSTRAP_N, seed=SEED)
        ci_text = "n/a" if ci is None else f"{fmt(ci[0])}–{fmt(ci[1])}"
        lines.append(f"ROC-AUC: {fmt(roc_auc(probs, labels))} (95% bootstrap CI {ci_text}).")
    else:
        lines.append("ROC-AUC not reported: 3 negatives, all planted fixtures (see data/gold/README.md).")
    rows = sweep(probs, labels, GRID)
    best = recommend_hi(rows, MAX_ERROR_RATE)
    lines.append(
        "Recommended hi: "
        + ("none meets the rule" if best is None else f"{best['hi']} (coverage {fmt(best['coverage'], 2)})")
        + "."
    )
    lines += [
        "",
        "| hi | acted | review | false accepts | false rejects | coverage | error rate |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['hi']} | {row['acted']} | {row['review']} | {row['false_accepts']} | "
            f"{row['false_rejects']} | {fmt(row['coverage'], 2)} | {fmt(row['error_rate'], 2)} |"
        )
    lines.append("")
    return lines, len(answered)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--decide-dir", type=Path, required=True, help="qte77/.github actions/decide directory")
    parser.add_argument("--models", default="clef:clef-flash,clef:clef", help="backend:model pairs, comma-separated")
    parser.add_argument("--sets", default="papers,issues", help="gold sets, comma-separated")
    parser.add_argument("--limit", type=int, default=0, help="first N items per set (0 = all)")
    parser.add_argument("--out", type=Path, default=Path("decision-eval-output"))
    args = parser.parse_args()

    decide = load_decide(args.decide_dir)
    models = [tuple(pair.split(":", 1)) for pair in args.models.split(",") if pair.strip()]
    sets = [s.strip() for s in args.sets.split(",") if s.strip()]
    unknown = [s for s in sets if s not in SETS]
    if unknown or any(len(m) != 2 for m in models):
        sys.exit(f"ERROR: bad --sets {unknown} or --models {args.models!r}")

    args.out.mkdir(parents=True, exist_ok=True)
    summary = [
        "# Decision-model calibration on the G1 gold sets",
        "",
        f"Rule (fixed before the run): recommend the smallest `hi` in {GRID[0]}–{GRID[-1]} (step 0.05) whose "
        f"acted decisions, both tails, are wrong at most {MAX_ERROR_RATE:.0%} of the time. "
        f"Bootstrap: {BOOTSTRAP_N} resamples, seed {SEED}. Escalated items (no probability after "
        f"{RETRIES} tries) are left out of every metric and counted.",
        "",
    ]
    failed = []
    with (args.out / "records.jsonl").open("w", encoding="utf-8") as out:
        for set_name in sets:
            build_state, question = SETS[set_name]
            gold = load_gold(GOLD_DIR / f"{set_name}.items.jsonl", GOLD_DIR / f"{set_name}.labels.jsonl")
            if args.limit:
                gold = gold[: args.limit]
            for backend, model in models:
                records = []
                for item in gold:
                    started = time.monotonic()
                    answer, attempts = ask(decide, build_state(item), question, backend, model)
                    record = {
                        "set": set_name,
                        "backend": backend,
                        "model": model,
                        "id": item["id"],
                        "label": item["label"],
                        "probability": answer.get("probability"),
                        "band": answer.get("band"),
                        "error": answer.get("error"),
                        "attempts": attempts,
                        "seconds": round(time.monotonic() - started, 2),
                    }
                    records.append(record)
                    out.write(json.dumps(record) + "\n")
                lines, answered = summarize(set_name, f"{backend}:{model}", records)
                summary += lines
                print("\n".join(lines))
                if not answered:
                    failed.append(f"{set_name}/{backend}:{model}")
    (args.out / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    if failed:
        sys.exit(f"ERROR: no answers at all for {', '.join(failed)}")


if __name__ == "__main__":
    main()
