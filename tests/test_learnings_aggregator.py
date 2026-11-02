"""Tests for learnings-aggregator change detection.

The script filename is hyphenated (not a valid module name), so it is loaded via
importlib rather than imported. Run: python3 -m unittest discover -s tests
"""
import datetime
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

_SCRIPT = (
    Path(__file__).resolve().parents[1] / ".github" / "scripts" / "learnings-aggregator.py"
)
_spec = importlib.util.spec_from_file_location("learnings_aggregator", _SCRIPT)
learnings_aggregator = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(learnings_aggregator)


def _fixed_date(iso):
    class _Date(datetime.date):
        @classmethod
        def today(cls):
            return datetime.date.fromisoformat(iso)

    return _Date


class ChangeDetectionTests(unittest.TestCase):
    def _run(self, tmp, day, content):
        argv = [
            "learnings-aggregator.py",
            "--target-dir", str(Path(tmp) / "per-repo"),
            "--state-file", str(Path(tmp) / "state.json"),
        ]
        with mock.patch.object(sys, "argv", argv), \
                mock.patch.object(learnings_aggregator, "REPO_FILENAME_MAP", {"some-repo": "some-repo"}), \
                mock.patch.object(learnings_aggregator, "fetch_learnings", return_value=content), \
                mock.patch.object(learnings_aggregator, "date", _fixed_date(day)):
            return learnings_aggregator.main()

    def test_unchanged_upstream_on_a_later_day_is_not_an_update(self):
        # The weekly run must not rewrite mirrors (and open a PR) when only the
        # date moved; the 2026-10-26 run bumped `updated:` in all 7 files. PR #731.
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._run(tmp, "2026-10-19", "## Learned\n\n- a\n"), 1)
            mirror = Path(tmp) / "per-repo" / "some-repo.md"
            first = mirror.read_text(encoding="utf-8")
            state = (Path(tmp) / "state.json").read_text(encoding="utf-8")

            self.assertEqual(self._run(tmp, "2026-10-26", "## Learned\n\n- a\n"), 0)
            self.assertEqual(mirror.read_text(encoding="utf-8"), first)
            self.assertEqual((Path(tmp) / "state.json").read_text(encoding="utf-8"), state)

    def test_changed_upstream_is_an_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._run(tmp, "2026-10-19", "## Learned\n\n- a\n")
            self.assertEqual(self._run(tmp, "2026-10-26", "## Learned\n\n- a\n- b\n"), 1)
            mirror = (Path(tmp) / "per-repo" / "some-repo.md").read_text(encoding="utf-8")
            self.assertIn("- b", mirror)
            self.assertIn("updated: 2026-10-26", mirror)
            self.assertEqual(len(json.loads((Path(tmp) / "state.json").read_text())), 1)


if __name__ == "__main__":
    unittest.main()
