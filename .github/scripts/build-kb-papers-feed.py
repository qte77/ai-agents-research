#!/usr/bin/env python3
"""Export arXiv papers cited in docs/ but missing from the rxiv feed as paperverse JSONL.

Reads arXiv IDs from ``docs/`` (minus the generated rxiv index and ``docs/archive/``), drops the
IDs already in ``triage/rxiv/data/`` or in the output file, fetches the rest from the arXiv API
(batches, 3 s between requests, one connection at a time; see
https://info.arxiv.org/help/api/tou.html) and merges them into the output file.

Usage:
    python build-kb-papers-feed.py [--docs docs] [--feed triage/rxiv/data]
        [--out triage/kb-papers/arxiv-kb.jsonl] [--batch-size 100]

Exit codes:
    0 = output written (IDs the API did not return are listed on stderr)
    2 = fatal error (network or bad response)
"""

import argparse
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib import kb_papers as kb  # noqa: E402

API = "http://export.arxiv.org/api/query"
USER_AGENT = "ai-agents-research-kb-papers"
DELAY_S = 3  # arXiv terms of use: at most one request every three seconds


def fetch(ids: list[str]) -> str:
    query = urllib.parse.urlencode({"id_list": ",".join(ids), "max_results": len(ids)})
    req = urllib.request.Request(f"{API}?{query}", headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310 (fixed http API URL)
        return resp.read().decode("utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--docs", type=Path, default=Path("docs"))
    ap.add_argument("--feed", type=Path, default=Path("triage/rxiv/data"))
    ap.add_argument("--out", type=Path, default=Path("triage/kb-papers/arxiv-kb.jsonl"))
    ap.add_argument("--batch-size", type=int, default=100)
    args = ap.parse_args()

    existing = kb.read_jsonl(args.out)
    cited = kb.collect_cited_ids(args.docs)
    todo = kb.ids_to_fetch(cited, kb.load_ids(args.feed), {r["doi"] for r in existing})
    print(f"cited={len(cited)} to_fetch={len(todo)} already_in_output={len(existing)}")

    new: list[dict] = []
    for i, batch in enumerate(kb.batches(todo, args.batch_size)):
        if i:
            time.sleep(DELAY_S)
        try:
            new += kb.parse_atom(fetch(batch))
        except Exception as exc:  # noqa: BLE001 (any failure aborts; nothing is written)
            print(f"fatal: batch {i} failed: {exc}", file=sys.stderr)
            return 2

    missing = sorted(set(todo) - {r["doi"] for r in new})
    if missing:
        print(f"not returned by the API ({len(missing)}): {' '.join(missing)}", file=sys.stderr)
    kb.write_jsonl(args.out, kb.merge_records(existing, new))
    print(f"fetched={len(new)} total={len(existing) + len(new)} -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
