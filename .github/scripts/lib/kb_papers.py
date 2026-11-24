"""Pure helpers for the KB papers export (plan 0016 N37).

arXiv IDs cited by hand in ``docs/`` but absent from the rxiv feed are resolved through the
arXiv API and written in the same row schema as ``triage/rxiv/data/*.jsonl``. Network calls
live in ``build-kb-papers-feed.py``; everything here is deterministic and stdlib only.
"""
import datetime
import json
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

# Reason: the version suffix (v2) and .pdf extension sit after the ID and must not join it.
ID_RE = re.compile(r"arxiv\.org/(?:abs|html|pdf)/(\d{4})\.(\d{4,5})(?!\d)", re.IGNORECASE)
# Excluded: the generated rxiv index (its IDs are the feed) and archived docs.
EXCLUDED = ("research/rxiv-agentic-papers.md", "archive")

ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
ENTRY_ID_RE = re.compile(r"arxiv\.org/abs/(?P<id>\d{4}\.\d{4,5})(?:v(?P<v>\d+))?$")
FIELDS = ("date", "iso_week", "doi", "version", "category", "title", "authors", "abstract", "extracted")


def extract_ids(text: str) -> set[str]:
    """Return the bare arXiv IDs cited as abs/html/pdf URLs in ``text``."""
    ids = set()
    for yymm, num in ID_RE.findall(text):
        # Reason: 4-digit serials for 0704-1412, 5-digit from 1501; other shapes would
        # make the API answer a whole batch with one error entry.
        if (704 <= int(yymm) <= 1412 and len(num) == 4) or (int(yymm) >= 1501 and len(num) == 5):
            ids.add(f"{yymm}.{num}")
    return ids


def collect_cited_ids(docs_dir: Path) -> set[str]:
    """Union of cited IDs over every markdown file under ``docs_dir``, minus the exclusions."""
    ids: set[str] = set()
    for path in sorted(docs_dir.rglob("*.md")):
        rel = path.relative_to(docs_dir).as_posix()
        if any(rel == e or rel.startswith(e + "/") for e in EXCLUDED):
            continue
        ids |= extract_ids(path.read_text(encoding="utf-8"))
    return ids


def _bare(doi: str) -> str:
    return re.sub(r"v\d+$", "", doi)


def read_jsonl(path: Path) -> list[dict]:
    """Rows of a JSONL file; a missing file is an empty list."""
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_ids(data_dir: Path) -> set[str]:
    """Bare arXiv IDs (field ``doi``, version dropped) of every ``*.jsonl`` under ``data_dir``."""
    ids: set[str] = set()
    for path in sorted(data_dir.glob("*.jsonl")):
        ids |= {_bare(r["doi"]) for r in read_jsonl(path) if r.get("doi")}
    return ids


def iso_week(date: str) -> str:
    """ISO week number as an unpadded string, as in the rxiv rows ("1", "16")."""
    return str(datetime.date.fromisoformat(date).isocalendar()[1])


def _text(el) -> str:
    # Reason: the API wraps titles and abstracts across lines; collapse to single spaces.
    return " ".join((el.text or "").split()) if el is not None else ""


def parse_atom(xml: str) -> list[dict]:
    """Records for each paper entry of an arXiv API Atom response; error entries are dropped."""
    records = []
    for entry in ET.fromstring(xml).iter(ATOM + "entry"):
        m = ENTRY_ID_RE.search(_text(entry.find(ATOM + "id")))
        if not m:  # Reason: unknown IDs come back as an "Error" entry under /api/errors
            continue
        date = _text(entry.find(ATOM + "published"))[:10]
        cat = entry.find(ARXIV + "primary_category")
        authors = [_text(a.find(ATOM + "name")) for a in entry.findall(ATOM + "author")]
        records.append({
            "date": date,
            "iso_week": iso_week(date),
            "doi": m["id"],
            "version": m["v"] or "1",
            "category": cat.get("term", "") if cat is not None else "",
            "title": _text(entry.find(ATOM + "title")),
            "authors": ", ".join(authors),
            "abstract": _text(entry.find(ATOM + "summary")),
            "extracted": {},
        })
    return records


def ids_to_fetch(cited: set[str], feed: set[str], fetched: set[str]) -> list[str]:
    """Sorted cited IDs that are neither in the rxiv feed nor already in the output file."""
    return sorted(cited - feed - fetched)


def batches(items: list[str], size: int) -> list[list[str]]:
    return [items[i:i + size] for i in range(0, len(items), size)]


def merge_records(existing: list[dict], new: list[dict]) -> list[dict]:
    """Union by ``doi`` (new wins), sorted by ``doi`` so a re-run is a no-op diff."""
    by_doi = {r["doi"]: r for r in existing}
    by_doi.update({r["doi"]: r for r in new})
    return [by_doi[k] for k in sorted(by_doi)]


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")
    os.replace(tmp, path)  # Reason: atomic, so an interrupted run never leaves a truncated file
