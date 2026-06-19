"""Pure incident-normalization logic for status-collector.py.

Transforms raw Statuspage incidents into archive records and decides upserts.
Kept import-clean (no HTTP / argparse / sys.exit) so it is unit-testable; the
status-collector.py entry script does the IO and wires these together.
"""
from __future__ import annotations

from datetime import datetime, timezone

from .monitor_utils import parse_iso

STATUSPAGE_BASE = "https://status.anthropic.com"


def compute_duration(started_at: str, resolved_at: str | None) -> int | None:
    """Incident duration in minutes; None if unresolved or unparseable."""
    if not resolved_at or not started_at:
        return None
    start, end = parse_iso(started_at), parse_iso(resolved_at)
    if start is None or end is None:
        return None
    return max(0, int((end - start).total_seconds() / 60))


def normalize_incident(raw: dict) -> dict:
    """Normalize a Statuspage incident into an archive record."""
    started_at = raw.get("started_at") or raw.get("created_at", "")
    resolved_at = raw.get("resolved_at")
    components = [c["name"] for c in raw.get("components", []) if c.get("name")]
    return {
        "id": raw["id"],
        "name": raw.get("name", ""),
        "status": raw.get("status", ""),
        "impact": raw.get("impact", ""),
        "started_at": started_at,
        "resolved_at": resolved_at or "",
        "duration_minutes": compute_duration(started_at, resolved_at),
        "affected_components": components,
        "updates_count": len(raw.get("incident_updates", [])),
        "url": raw.get("shortlink", f"{STATUSPAGE_BASE}/incidents/{raw['id']}"),
        "collected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def normalize_webhook_incident(payload: dict) -> dict | None:
    """Extract + normalize the incident from a webhook payload (None if absent)."""
    incident = payload.get("incident")
    return normalize_incident(incident) if incident else None


def record_changed(old: dict, new: dict) -> bool:
    """True if a record meaningfully changed (ignoring the collected_at stamp)."""
    return any(
        old.get(key) != new.get(key)
        for key in ("status", "resolved_at", "duration_minutes", "updates_count",
                    "affected_components", "impact", "name")
    )


def upsert_record(archive: dict[str, dict], record: dict) -> bool:
    """Insert or update ``record`` in ``archive`` by id; True if it changed."""
    existing = archive.get(record["id"])
    if not existing or record_changed(existing, record):
        archive[record["id"]] = record
        return True
    return False
