"""Unit tests for lib/status_incidents.py (pure incident-normalization logic)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".github" / "scripts"))

from lib import status_incidents as si  # noqa: E402


class ComputeDurationTests(unittest.TestCase):
    def test_resolved_minutes(self):
        self.assertEqual(si.compute_duration("2026-01-01T00:00:00Z", "2026-01-01T01:30:00Z"), 90)

    def test_unresolved_returns_none(self):
        self.assertIsNone(si.compute_duration("2026-01-01T00:00:00Z", None))
        self.assertIsNone(si.compute_duration("", "2026-01-01T01:00:00Z"))

    def test_unparseable_returns_none(self):
        self.assertIsNone(si.compute_duration("nope", "also-nope"))

    def test_negative_clamped_to_zero(self):
        self.assertEqual(si.compute_duration("2026-01-01T01:00:00Z", "2026-01-01T00:00:00Z"), 0)


class NormalizeIncidentTests(unittest.TestCase):
    def test_maps_fields_and_drops_blank_components(self):
        rec = si.normalize_incident({
            "id": "abc", "name": "Outage", "status": "resolved", "impact": "major",
            "started_at": "2026-01-01T00:00:00Z", "resolved_at": "2026-01-01T00:30:00Z",
            "components": [{"name": "API"}, {"name": ""}, {"foo": "x"}],
            "incident_updates": [{}, {}], "shortlink": "http://s/abc",
        })
        self.assertEqual(rec["duration_minutes"], 30)
        self.assertEqual(rec["affected_components"], ["API"])
        self.assertEqual(rec["updates_count"], 2)
        self.assertEqual(rec["url"], "http://s/abc")
        self.assertIn("collected_at", rec)

    def test_started_at_falls_back_and_url_default(self):
        rec = si.normalize_incident({"id": "x", "created_at": "2026-01-01T00:00:00Z"})
        self.assertEqual(rec["started_at"], "2026-01-01T00:00:00Z")
        self.assertEqual(rec["url"], "https://status.anthropic.com/incidents/x")


class NormalizeWebhookTests(unittest.TestCase):
    def test_none_when_no_incident(self):
        self.assertIsNone(si.normalize_webhook_incident({}))

    def test_normalizes_incident(self):
        self.assertEqual(si.normalize_webhook_incident({"incident": {"id": "w1"}})["id"], "w1")


class RecordChangedTests(unittest.TestCase):
    def test_collected_at_ignored(self):
        self.assertFalse(si.record_changed(
            {"status": "resolved", "collected_at": "t1"},
            {"status": "resolved", "collected_at": "t2"},
        ))

    def test_status_change_detected(self):
        self.assertTrue(si.record_changed({"status": "investigating"}, {"status": "resolved"}))


class UpsertRecordTests(unittest.TestCase):
    def test_new_added(self):
        arc: dict = {}
        self.assertTrue(si.upsert_record(arc, {"id": "a", "status": "x"}))
        self.assertIn("a", arc)

    def test_changed_updated(self):
        arc = {"a": {"id": "a", "status": "x"}}
        self.assertTrue(si.upsert_record(arc, {"id": "a", "status": "y"}))
        self.assertEqual(arc["a"]["status"], "y")

    def test_unchanged_is_noop(self):
        arc = {"a": {"id": "a", "status": "x", "name": "n"}}
        self.assertFalse(si.upsert_record(arc, {"id": "a", "status": "x", "name": "n", "collected_at": "diff"}))


if __name__ == "__main__":
    unittest.main()
