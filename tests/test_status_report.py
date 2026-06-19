"""Unit tests for lib/status_report.py (pure markdown-report generation)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import status_report as sr  # noqa: E402

SAMPLE = [
    {"id": "1", "status": "resolved", "impact": "major",
     "started_at": "2026-01-05T03:00:00Z", "resolved_at": "2026-01-05T04:00:00Z",
     "duration_minutes": 60, "affected_components": ["API"]},
    {"id": "2", "status": "resolved", "impact": "minor",
     "started_at": "2026-01-06T10:00:00Z", "resolved_at": "2026-01-06T10:30:00Z",
     "duration_minutes": 30, "affected_components": ["API", "Console"]},
    {"id": "3", "status": "investigating", "impact": "major",
     "started_at": "2026-01-07T12:00:00Z", "duration_minutes": None,
     "affected_components": ["Console"]},
]


class FormatDurationTests(unittest.TestCase):
    def test_minutes_hours_days(self):
        self.assertEqual(sr.format_duration(45), "45m")
        self.assertEqual(sr.format_duration(90), "1.5h")
        self.assertEqual(sr.format_duration(60 * 24 * 2), "2.0d")


class ExtractTimingTests(unittest.TestCase):
    def test_splits_resolved_and_durations(self):
        resolved, starts, durations = sr._extract_timing(SAMPLE)
        self.assertEqual(len(resolved), 2)
        self.assertEqual(sorted(durations), [30, 60])
        self.assertEqual(len(starts), 3)


class RenderBarTableTests(unittest.TestCase):
    def test_exact_output_with_scaled_bar_and_separator(self):
        out = sr._render_bar_table("My Title", "Hour", [("00:00", 2), ("01:00", 0)])
        self.assertEqual(out, [
            "## My Title", "",
            "| Hour | Incidents | Bar |", "|------|-----------|-----|",
            f"| 00:00 | 2 | {'#' * 20} |",
            "| 01:00 | 0 |  |",
            "",
        ])


class GenerateReportTests(unittest.TestCase):
    def test_sections_and_counts(self):
        rep = sr.generate_report(SAMPLE)
        self.assertIn("# Claude Platform Outage Statistics", rep)
        self.assertIn("- **Total incidents**: 3", rep)
        self.assertIn("- **Resolved**: 2", rep)
        self.assertIn("- **Unresolved/ongoing**: 1", rep)
        self.assertIn("| Median | 45m |", rep)  # median([60,30]) = 45
        self.assertIn("## Severity Distribution", rep)
        self.assertIn("## Time-of-Day Distribution (UTC)", rep)
        self.assertIn("## Uptime Estimate", rep)

    def test_empty_archive(self):
        self.assertIn("No incidents recorded yet.", sr.generate_report([]))


if __name__ == "__main__":
    unittest.main()
