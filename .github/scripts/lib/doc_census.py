"""Census of agent-substrate rubric rows across the docs corpus (plan 0010 row T1).

Finds every scored rubric row, in either form the corpus uses:

* a table under the six-column header ``| Shared | Distributed | ... | Traceable |``;
* an inline ``**Rubric** (scored YYYY-MM-DD, ...): Shared: <token> (...); ...`` paragraph.

Each row's subject comes from a ``subject: <name>`` tag written next to the score, never
from a guess: an untagged row is reported as unassigned. That keeps the subject in the
artifact itself, so the reference architecture's matrix is regenerable from the corpus.

Pure logic except ``load_corpus``, the only function that touches the filesystem.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

PROPERTIES = ("Shared", "Distributed", "Reproducible", "Adaptable", "Versionable", "Traceable")
SUBJECTS = ("memory", "ontology", "graphs-rag", "context", "skills", "plugins", "harness", "long-running")
# Pages that define or synthesize the rubric, not tools scored on it.
EXCLUDED = frozenset({
    "docs/sdlc-lcm/agent-substrate-rubric.md",
    "docs/sdlc-lcm/agent-substrate-reference-architecture.md",
})
_RANK = {"yes": 4, "partial": 3, "no": 2, "no data": 1, "n/a": 0}

# Optional leading "Tool" column; tables may be indented inside a list item.
_HEADER = re.compile(r"^\s*\|\s*(Tool\s*\|\s*)?" + r"\s*\|\s*".join(PROPERTIES) + r"\s*\|\s*$")
_TOKEN = re.compile(r"^(no data|n/a|partial|yes|no)\b", re.IGNORECASE)
_PROP = re.compile(r"\b(" + "|".join(PROPERTIES) + r"):\s*(no data|n/a|partial|yes|no)\b", re.IGNORECASE)
_SUBJECT = re.compile(r"subject:\s*([a-z][a-z/-]*)")
_SCORED = re.compile(r"scored (\d{4}-\d{2}-\d{2})", re.IGNORECASE)
_HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$")
# A new block: list item, table row or heading. An inline row ends where one starts.
_BLOCK = re.compile(r"^\s*(?:[-*+]\s|\d+[.)]\s|\||#)")


@dataclass(frozen=True)
class Row:
    """One scored rubric row and where it lives."""
    path: str
    line: int
    form: str  # "table" | "inline"
    heading: str
    subject: str | None
    scored: str | None
    scores: dict


def rank(token: str) -> int:
    """Order of evidence strength: yes > partial > no > no data > n/a."""
    return _RANK[token]


def _token(cell: str) -> str:
    m = _TOKEN.match(cell.strip())
    return m.group(1).lower() if m else "no data"


def _section(lines: list[str], i: int) -> tuple[str, int, int]:
    """Heading text and [start, end) line range of the section containing line ``i``."""
    start = next((j for j in range(i, -1, -1) if _HEADING.match(lines[j])), -1)
    end = next((j for j in range(i + 1, len(lines)) if _HEADING.match(lines[j])), len(lines))
    heading = _HEADING.match(lines[start]).group(1) if start >= 0 else ""
    return heading, start + 1, end


def _meta(text: str) -> tuple[str | None, str | None]:
    subject = _SUBJECT.search(text)
    scored = _SCORED.search(text)
    return (subject.group(1) if subject else None), (scored.group(1) if scored else None)


def _nearest(lines: list[str], pattern: re.Pattern, above: range, below: range) -> str | None:
    """First match scanning upward from the table, else downward after it (same section only)."""
    for j in (*above, *below):
        m = pattern.search(lines[j])
        if m:
            return m.group(1)
    return None


def _table_rows(path: str, lines: list[str]) -> list[Row]:
    rows = []
    for i, line in enumerate(lines):
        header = _HEADER.match(line)
        if not header:
            continue
        has_tool = header.group(1) is not None
        heading, start, end = _section(lines, i)
        last = i + 2
        while last < len(lines) and lines[last].lstrip().startswith("|"):
            last += 1
        above, below = range(i - 1, start - 1, -1), range(last, end)
        subject = _nearest(lines, _SUBJECT, above, below)
        scored = _nearest(lines, _SCORED, above, below)
        j = i + 2  # skip the |---| separator
        while j < last:
            cells = lines[j].strip().strip("|").split(" | ")
            name = cells.pop(0).strip() if has_tool else heading
            if len(cells) == len(PROPERTIES):
                scores = {p: _token(c) for p, c in zip(PROPERTIES, cells)}
                rows.append(Row(path, j + 1, "table", name, subject, scored, scores))
            j += 1
    return rows


def _inline_rows(path: str, lines: list[str]) -> list[Row]:
    rows = []
    for i, line in enumerate(lines):
        k = line.find("**Rubric**")
        if k < 0:
            continue
        end = next((j for j in range(i + 1, len(lines))
                    if not lines[j].strip() or _BLOCK.match(lines[j])), len(lines))
        para = " ".join(lines[i:end])[k:]
        scores: dict = {}
        for prop, token in _PROP.findall(para):
            scores.setdefault(prop.capitalize(), token.lower())  # first score per property wins
        if set(scores) != set(PROPERTIES):
            continue
        heading, _, _ = _section(lines, i)
        subject, scored = _meta(para.split("Shared:", 1)[0])
        rows.append(Row(path, i + 1, "inline", heading, subject, scored, scores))
    return rows


def parse_rows(path: str, text: str) -> list[Row]:
    """Every scored rubric row in one doc (none for the rubric's own meta pages)."""
    if path in EXCLUDED:
        return []
    lines = text.split("\n")
    return _table_rows(path, lines) + _inline_rows(path, lines)


def best_per_cell(rows: list[Row]) -> dict:
    """{(subject, property): (best token, row)} over rows that declare a subject."""
    best: dict = {}
    for row in rows:
        if row.subject is None:
            continue
        for prop, token in row.scores.items():
            key = (row.subject, prop)
            if key not in best or rank(token) > rank(best[key][0]):
                best[key] = (token, row)
    return best


def cell_label(entry: tuple | None) -> str:
    """Matrix cell text. A cell is open when no row reaches `partial`."""
    if entry is None:
        return "open (no row)"
    token = entry[0]
    return token if rank(token) >= rank("partial") else f"open (best: {token})"


def census_tsv(rows: list[Row]) -> str:
    """One line per row: path, line, form, subject, scored, heading, six scores."""
    head = ["path", "line", "form", "subject", "scored", "heading", *PROPERTIES]
    body = [[r.path, str(r.line), r.form, r.subject or "unassigned", r.scored or "", r.heading,
             *(r.scores[p] for p in PROPERTIES)] for r in rows]
    return "\n".join("\t".join(cols) for cols in [head, *body]) + "\n"


def matrix_markdown(rows: list[Row]) -> str:
    """The 8 x 6 evidence matrix: best score per subject and property, with its row."""
    best = best_per_cell(rows)
    out = ["| Subject | " + " | ".join(PROPERTIES) + " |", "|---" * (len(PROPERTIES) + 1) + "|"]
    for subject in SUBJECTS:
        cells = []
        for prop in PROPERTIES:
            entry = best.get((subject, prop))
            label = cell_label(entry)
            cells.append(label if entry is None else f"{label} — {entry[1].heading} ({entry[1].path}:{entry[1].line})")
        out.append(f"| {subject} | " + " | ".join(cells) + " |")
    return "\n".join(out) + "\n"


def load_corpus(docs_dir: Path) -> list[Row]:
    """Parse every markdown file under ``docs_dir`` (archive excluded), in path order."""
    rows = []
    for md in sorted(docs_dir.rglob("*.md")):
        rel = md.as_posix()
        if "/archive/" in rel:
            continue
        rows.extend(parse_rows(rel, md.read_text(encoding="utf-8")))
    return rows
