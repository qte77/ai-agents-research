#!/usr/bin/env python3
"""Prompt-cache usage of one Claude Code session, read from its transcript (stdlib only).

Usage: python3 scripts/cc_cache_usage.py <session.jsonl> [gap_min=60] [ttl_min=60]

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


def summarize(lines, gap_min=60, ttl_min=60):
    """Summarize transcript lines (JSON strings) into token totals, gaps, predictions, compactions."""
    s = dict(responses=0, read=0, write=0, write_1h=0, write_5m=0, uncached=0, output=0,
             gaps=[], gap_write=0, predicted={"hit": 0, "miss": 0}, prediction_correct=0, compactions=[])
    seen, prev = set(), None
    for line in lines:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("subtype") == "compact_boundary":
            cm = d.get("compactMetadata") or {}
            s["compactions"].append({"time": d.get("timestamp"), "trigger": cm.get("trigger"),
                                     "pre": cm.get("preTokens", 0), "post": cm.get("postTokens", 0)})
            continue
        m = d.get("message")
        if d.get("type") != "assistant" or not isinstance(m, dict) or d.get("isSidechain"):
            continue
        if m.get("id") in seen:
            continue
        seen.add(m.get("id"))
        u = m.get("usage") or {}
        cc = u.get("cache_creation") or {}
        read, write = u.get("cache_read_input_tokens") or 0, u.get("cache_creation_input_tokens") or 0
        s["responses"] += 1
        s["read"] += read
        s["write"] += write
        s["write_1h"] += cc.get("ephemeral_1h_input_tokens") or 0
        s["write_5m"] += cc.get("ephemeral_5m_input_tokens") or 0
        s["uncached"] += u.get("input_tokens") or 0
        s["output"] += u.get("output_tokens") or 0
        now = _ts(d["timestamp"])
        if prev is not None:
            gap = (now - prev).total_seconds() / 60
            # Reason: the cache lifetime runs from the previous request; past it, expect a cold rewrite.
            predicted = "miss" if gap > ttl_min else "hit"
            actual = "miss" if write > read else "hit"
            s["predicted"][predicted] += 1
            s["prediction_correct"] += predicted == actual
            if gap > gap_min:
                s["gaps"].append({"time": d["timestamp"], "gap_min": round(gap), "write": write, "read": read})
                s["gap_write"] += write
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
           f"prediction (miss after a gap past the cache lifetime): {s['prediction_correct']}/{n} turns right",
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
    gap = float(argv[2]) if len(argv) > 2 else 60
    ttl = float(argv[3]) if len(argv) > 3 else 60
    with open(argv[1], encoding="utf-8") as f:
        print(report(summarize(f, gap, ttl)))


if __name__ == "__main__":
    main(sys.argv)
