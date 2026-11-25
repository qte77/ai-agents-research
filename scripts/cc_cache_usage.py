#!/usr/bin/env python3
"""Prompt-cache usage of one Claude Code session, read from its transcript (stdlib only).

Usage: python3 scripts/cc_cache_usage.py <session.jsonl> [gap_min=60] [ttl_min=auto: 5 or 60]

Transcripts live under ~/.claude/projects/<project>/<session-id>.jsonl. The report counts each
main-thread API response once (streamed chunks repeat a message id; subagent turns are sidechains
with their own cache), sums the usage fields, lists turns after idle gaps longer than gap_min with
their cache write and read, checks a simple hit/miss prediction (miss when the gap since the
previous response exceeds ttl_min) against the actual outcome (miss when a turn writes more than it
reads), and lists the compaction markers. Token counts only; multiply by your model's prices.
"""
import json
import sys
from datetime import datetime


def _ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def _usage(rec):
    u = rec.get("usage")
    return u if isinstance(u, dict) else {}


def summarize(lines, gap_min=60, ttl_min=None):
    """Summarize transcript lines (JSON strings) into token totals, gaps, predictions, compactions.

    ttl_min=None picks the cache lifetime from the write buckets: 5 minutes when most writes are
    5-minute writes, else 60.
    """
    s = dict(responses=0, read=0, write=0, write_1h=0, write_5m=0, uncached=0, output=0, ttl_min=ttl_min,
             gaps=[], gap_write=0, predicted={"hit": 0, "miss": 0}, prediction_correct=0, compactions=[])
    recs, by_id = [], {}
    for line in lines:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if not isinstance(d, dict) or d.get("isSidechain"):
            continue  # Reason: subagent turns and markers are sidechains with their own cache.
        if d.get("subtype") == "compact_boundary":
            cm = d.get("compactMetadata") if isinstance(d.get("compactMetadata"), dict) else {}
            s["compactions"].append({"time": d.get("timestamp"), "trigger": cm.get("trigger"),
                                     "pre": cm.get("preTokens", 0), "post": cm.get("postTokens", 0)})
            continue
        m = d.get("message")
        if d.get("type") != "assistant" or not isinstance(m, dict):
            continue
        mid = m.get("id")
        if mid is not None and mid in by_id:
            by_id[mid]["usage"] = m.get("usage")  # streamed chunks: the last one carries final output
            continue
        rec = {"time": d.get("timestamp"), "usage": m.get("usage")}
        recs.append(rec)
        if mid is not None:
            by_id[mid] = rec

    for rec in recs:
        u = _usage(rec)
        cc = u.get("cache_creation") if isinstance(u.get("cache_creation"), dict) else {}
        rec["read"], rec["write"] = u.get("cache_read_input_tokens") or 0, u.get("cache_creation_input_tokens") or 0
        s["responses"] += 1
        s["read"] += rec["read"]
        s["write"] += rec["write"]
        s["write_1h"] += cc.get("ephemeral_1h_input_tokens") or 0
        s["write_5m"] += cc.get("ephemeral_5m_input_tokens") or 0
        s["uncached"] += u.get("input_tokens") or 0
        s["output"] += u.get("output_tokens") or 0
    if s["ttl_min"] is None:
        s["ttl_min"] = 5 if s["write_5m"] > s["write_1h"] else 60

    prev = None
    for rec in recs:
        try:
            now = _ts(rec["time"])
        except (TypeError, ValueError, AttributeError):
            continue  # no usable timestamp: counted above, left out of the gap logic
        if prev is not None:
            gap = (now - prev).total_seconds() / 60
            # Reason: gaps run between responses, so they slightly understate the time since the
            # previous request started, which is where the cache lifetime counts from.
            predicted = "miss" if gap > s["ttl_min"] else "hit"
            actual = "miss" if rec["write"] > rec["read"] else "hit"
            s["predicted"][predicted] += 1
            s["prediction_correct"] += predicted == actual
            if gap > gap_min:
                s["gaps"].append({"time": rec["time"], "gap_min": round(gap), "write": rec["write"], "read": rec["read"]})
                s["gap_write"] += rec["write"]
        prev = now
    return s


def report(s):
    """Render a summary as plain text."""
    inp = s["read"] + s["write"] + s["uncached"] or 1
    n = sum(s["predicted"].values()) or 1
    out = [f"main-thread responses: {s['responses']}",
           f"input: cache read {s['read']:,} ({s['read'] / inp:.1%}), cache write {s['write']:,} "
           f"({s['write'] / inp:.1%}; 1h {s['write_1h']:,}, 5m {s['write_5m']:,}), uncached {s['uncached']:,}",
           f"output: {s['output']:,}",
           f"prediction (miss after a gap past the {s['ttl_min']:g}-minute lifetime; actual miss = writes > reads): "
           f"{s['prediction_correct']}/{n} turns right",
           "turns after an idle gap (time UTC, gap min, cache write, cache read):"]
    out += [f"  {g['time'][:16]}  {g['gap_min']:6}  {g['write']:>9,}  {g['read']:>9,}" for g in s["gaps"]]
    out.append(f"cache writes after gaps: {s['gap_write']:,} of {s['write']:,} "
               f"({s['gap_write'] / (s['write'] or 1):.0%})")
    out.append("compactions (time UTC, trigger, tokens before -> after):")
    out += [f"  {c['time'][:16]}  {c['trigger']}  {c['pre']:,} -> {c['post']:,}" for c in s["compactions"]]
    return "\n".join(out)


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    try:
        gap = float(argv[2]) if len(argv) > 2 else 60
        ttl = float(argv[3]) if len(argv) > 3 else None
    except ValueError:
        sys.exit("gap_min and ttl_min must be numbers")
    with open(argv[1], encoding="utf-8") as f:
        print(report(summarize(f, gap, ttl)))


if __name__ == "__main__":
    main(sys.argv)
