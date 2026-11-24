"""Unit tests for lib/kb_papers.py: KB-cited arXiv IDs -> paperverse JSONL (plan 0016 N37).

No network: the Atom response is a small recorded snippet.
"""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import kb_papers as kb  # noqa: E402

_SCRIPT = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "build-kb-papers-feed.py"
_spec = importlib.util.spec_from_file_location("build_kb_papers_feed", _SCRIPT)
feed = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(feed)

ATOM = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2603.13594v2</id>
    <published>2026-03-13T17:59:01Z</published>
    <title>A  Title
      Over Two Lines</title>
    <summary>  An abstract
      with wrapping.
    </summary>
    <author><name>Ada Lovelace</name></author>
    <author><name>Alan Turing</name></author>
    <arxiv:primary_category term="cs.AI" scheme="http://arxiv.org/schemas/atom"/>
  </entry>
  <entry>
    <id>http://arxiv.org/api/errors#incorrect_id_format_for_9999.99999</id>
    <published>2026-01-01T00:00:00Z</published>
    <title>Error</title>
    <summary>incorrect id format</summary>
    <author><name>arXiv api core</name></author>
  </entry>
</feed>"""


class ExtractIdsTests(unittest.TestCase):
    def test_abs_html_pdf_and_version_suffix(self):
        text = (
            "[a](https://arxiv.org/abs/2603.13594v2) [b](https://arxiv.org/html/2511.16652) "
            "[c](http://arxiv.org/pdf/2401.00001v10.pdf) [d](https://arxiv.org/pdf/2401.00002.pdf)"
        )
        self.assertEqual(
            kb.extract_ids(text), {"2603.13594", "2511.16652", "2401.00001", "2401.00002"}
        )

    def test_ignores_non_arxiv_and_other_paths(self):
        text = "https://example.com/abs/2603.13594 https://arxiv.org/list/cs.AI/2603 arXiv:2603.13594"
        self.assertEqual(kb.extract_ids(text), set())

    def test_four_or_five_digit_serials(self):
        self.assertEqual(
            kb.extract_ids("arxiv.org/abs/2301.1234 arxiv.org/abs/2301.12345"),
            {"1301.1234", "2301.12345"},
        )


class IdShapeTests(unittest.TestCase):
    def test_uppercase_host(self):
        self.assertEqual(kb.extract_ids("https://arXiv.org/abs/2603.13594"), {"2603.13594"})

    def test_trailing_digit_guard(self):
        self.assertEqual(kb.extract_ids("arxiv.org/abs/2301.123456"), set())

    def test_digits_by_yymm(self):
        self.assertEqual(kb.extract_ids("arxiv.org/abs/1412.1234 arxiv.org/abs/0704.0001"),
                         {"1412.1234", "0704.0001"})
        self.assertEqual(kb.extract_ids("arxiv.org/abs/1412.12345 arxiv.org/abs/1501.1234"), set())
        self.assertEqual(kb.extract_ids("arxiv.org/abs/1501.12345"), {"1501.12345"})
        self.assertEqual(kb.extract_ids("arxiv.org/abs/0703.0001"), set())


class MainTests(unittest.TestCase):
    def _run(self, fetch):
        d = tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        root = Path(d.name)
        (root / "docs").mkdir()
        (root / "docs" / "a.md").write_text("arxiv.org/abs/2603.13594 arxiv.org/abs/2603.99999")
        out = root / "out" / "arxiv-kb.jsonl"
        argv = ["--docs", str(root / "docs"), "--feed", str(root / "none"),
                "--out", str(out), "--batch-size", "1"]
        feed.fetch = fetch
        feed.DELAY_S = 0
        return feed.main(argv), out

    def test_missing_id_exits_1_and_still_writes(self):
        code, out = self._run(lambda ids: ATOM if ids == ["2603.13594"] else "<feed xmlns='http://www.w3.org/2005/Atom'/>")
        self.assertEqual(code, 1)
        self.assertEqual([r["doi"] for r in kb.read_jsonl(out)], ["2603.13594"])

    def test_fetch_failure_writes_partial_and_exits_2(self):
        def fetch(ids):
            if ids == ["2603.13594"]:
                return ATOM
            raise OSError("boom")
        code, out = self._run(fetch)
        self.assertEqual(code, 2)
        self.assertEqual([r["doi"] for r in kb.read_jsonl(out)], ["2603.13594"])

    def test_unreturned_id_exits_1(self):
        code, _ = self._run(lambda ids: ATOM)
        self.assertEqual(code, 1)  # 2603.99999 is not in ATOM


class CollectTests(unittest.TestCase):
    def test_excludes_rxiv_index_and_archive(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "docs" / "research").mkdir(parents=True)
            (root / "docs" / "archive").mkdir()
            (root / "docs" / "non-cc").mkdir()
            (root / "docs" / "research" / "rxiv-agentic-papers.md").write_text("arxiv.org/abs/2601.00001")
            (root / "docs" / "archive" / "old.md").write_text("arxiv.org/abs/2601.00002")
            (root / "docs" / "non-cc" / "a.md").write_text("arxiv.org/abs/2601.00003")
            (root / "docs" / "research" / "other.md").write_text("arxiv.org/abs/2601.00004")
            self.assertEqual(kb.collect_cited_ids(root / "docs"), {"2601.00003", "2601.00004"})


class FeedIdsTests(unittest.TestCase):
    def test_reads_doi_and_drops_version(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "arxiv-2026-W11.jsonl").write_text(
                json.dumps({"doi": "2603.13594v2"}) + "\n\n" + json.dumps({"doi": "2603.14248"}) + "\n"
            )
            self.assertEqual(kb.load_ids(p), {"2603.13594", "2603.14248"})

    def test_missing_dir_is_empty(self):
        self.assertEqual(kb.load_ids(Path("/nonexistent-dir-xyz")), set())


class AtomTests(unittest.TestCase):
    def test_parse_entry_fields(self):
        recs = kb.parse_atom(ATOM)
        self.assertEqual(len(recs), 1)  # the API error entry is dropped
        r = recs[0]
        self.assertEqual(r["doi"], "2603.13594")
        self.assertEqual(r["version"], "2")
        self.assertEqual(r["date"], "2026-03-13")
        self.assertEqual(r["category"], "cs.AI")
        self.assertEqual(r["title"], "A Title Over Two Lines")
        self.assertEqual(r["abstract"], "An abstract with wrapping.")
        self.assertEqual(r["authors"], "Ada Lovelace, Alan Turing")

    def test_record_schema_matches_rxiv_rows(self):
        r = kb.parse_atom(ATOM)[0]
        self.assertEqual(
            list(r),
            ["date", "iso_week", "doi", "version", "category", "title", "authors", "abstract", "extracted"],
        )
        self.assertEqual(r["extracted"], {})

    def test_iso_week_unpadded_string(self):
        self.assertEqual(kb.iso_week("2026-04-13"), "16")  # Monday of W16
        self.assertEqual(kb.iso_week("2026-01-02"), "1")
        self.assertEqual(kb.iso_week("2021-01-01"), "53")  # ISO week of the previous year


class MergeTests(unittest.TestCase):
    def test_sorted_by_doi_and_new_wins_on_duplicate(self):
        old = [{"doi": "2602.00002", "title": "old"}, {"doi": "2601.00001", "title": "keep"}]
        new = [{"doi": "2602.00002", "title": "new"}, {"doi": "2601.00000", "title": "add"}]
        merged = kb.merge_records(old, new)
        self.assertEqual([r["doi"] for r in merged], ["2601.00000", "2601.00001", "2602.00002"])
        self.assertEqual(merged[2]["title"], "new")

    def test_ids_to_fetch_skips_feed_and_already_fetched(self):
        cited = {"2601.00001", "2601.00002", "2601.00003"}
        self.assertEqual(kb.ids_to_fetch(cited, {"2601.00001"}, {"2601.00002"}), ["2601.00003"])

    def test_batches(self):
        self.assertEqual(kb.batches(["a", "b", "c"], 2), [["a", "b"], ["c"]])
        self.assertEqual(kb.batches([], 2), [])


class RoundTripTests(unittest.TestCase):
    def test_write_then_read_is_stable(self):
        recs = kb.merge_records([], kb.parse_atom(ATOM))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "arxiv-kb.jsonl"
            kb.write_jsonl(p, recs)
            first = p.read_text()
            kb.write_jsonl(p, kb.merge_records(kb.read_jsonl(p), []))
            self.assertEqual(p.read_text(), first)
            self.assertTrue(first.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
