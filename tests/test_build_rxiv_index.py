"""Unit tests for the rxiv cumulative index generator."""
import importlib.util
import unittest
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "build-rxiv-index.py"
_spec = importlib.util.spec_from_file_location("build_rxiv_index", SCRIPT_PATH)
assert _spec is not None and _spec.loader is not None
build_rxiv_index = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_rxiv_index)


class RenderTests(unittest.TestCase):
    def test_sparse_records_do_not_emit_multiple_blank_lines(self):
        records = [
            {
                "title": "Sparse Paper",
                "doi": "",
                "extracted": {},
                "server": "arxiv",
                "year": 2026,
                "week": 23,
            },
            {
                "title": "Next Sparse Paper",
                "doi": "",
                "extracted": {},
                "server": "arxiv",
                "year": 2026,
                "week": 23,
            },
        ]

        rendered = build_rxiv_index.render(records, week_count=1)

        self.assertNotIn("\n\n\n", rendered)
        self.assertIn("### Sparse Paper\n\n### Next Sparse Paper", rendered)


if __name__ == "__main__":
    unittest.main()
