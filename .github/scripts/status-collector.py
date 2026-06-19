#!/usr/bin/env python3
"""Collect Claude platform incidents from the Statuspage API into a JSONL archive.

Fetches incidents from the Anthropic Statuspage and upserts them into a local
JSONL archive; can also process webhook payloads from repository_dispatch
events. Pure normalization logic lives in lib/status_incidents.py.

Usage:
    # Fetch from API (weekly cron)
    python status-collector.py --archive triage/status-monitor/outages.jsonl

    # Process webhook payload (repository_dispatch)
    python status-collector.py --archive ... --webhook-payload /tmp/payload.json

Exit codes:
    0 = no new or updated incidents
    1 = archive was updated (workflow should commit)
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor_utils import fatal, load_jsonl
from lib.status_incidents import (
    STATUSPAGE_BASE,
    normalize_incident,
    normalize_webhook_incident,
    upsert_record,
)


def fetch_incidents(base_url: str) -> list[dict]:
    """Fetch all incidents from the Statuspage JSON API."""
    url = f"{base_url}/api/v2/incidents.json"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        fatal(f"ERROR: Failed to fetch incidents: {e}")
    return data.get("incidents", [])


def save_archive(path: Path, archive: dict[str, dict]) -> None:
    """Write archive to JSONL, sorted by started_at."""
    path.parent.mkdir(parents=True, exist_ok=True)
    sorted_records = sorted(archive.values(), key=lambda r: r.get("started_at", ""))
    with open(path, "w") as f:
        for record in sorted_records:
            f.write(json.dumps(record, separators=(",", ":")) + "\n")


def _process_webhook(archive: dict[str, dict], payload_path: Path) -> bool:
    """Upsert one incident from a webhook payload; True if the archive changed."""
    with open(payload_path) as f:
        payload = json.load(f)
    record = normalize_webhook_incident(payload)
    if not record:
        return False
    is_new = record["id"] not in archive
    if upsert_record(archive, record):
        print(f"Webhook: {'new' if is_new else 'updated'} incident {record['id']}: {record['name']}")
        return True
    print(f"Webhook: no changes for incident {record['id']}")
    return False


def _process_api(archive: dict[str, dict], base_url: str) -> bool:
    """Fetch + upsert all API incidents; True if the archive changed."""
    incidents = fetch_incidents(base_url)
    print(f"Fetched {len(incidents)} incidents from API")
    changed = False
    for raw in incidents:
        record = normalize_incident(raw)
        is_new = record["id"] not in archive
        if upsert_record(archive, record):
            changed = True
            print(f"  {'NEW' if is_new else 'UPDATED'}: {record['id']} — {record['name']}")
    return changed


def main() -> None:
    """Entry point for the status collector."""
    parser = argparse.ArgumentParser(
        description="Collect Claude platform incidents into JSONL archive."
    )
    parser.add_argument(
        "--archive", type=Path, default=Path("triage/status-monitor/outages.jsonl"),
        help="Path to the JSONL archive file (default: triage/status-monitor/outages.jsonl)",
    )
    parser.add_argument(
        "--statuspage-base", default=STATUSPAGE_BASE,
        help=f"Statuspage base URL (default: {STATUSPAGE_BASE})",
    )
    parser.add_argument(
        "--webhook-payload", type=Path, default=None,
        help="Path to webhook payload JSON file (for repository_dispatch)",
    )
    args = parser.parse_args()

    archive = {r["id"]: r for r in load_jsonl(args.archive)}
    changed = (
        _process_webhook(archive, args.webhook_payload)
        if args.webhook_payload
        else _process_api(archive, args.statuspage_base)
    )

    if changed:
        save_archive(args.archive, archive)
        print(f"Archive updated: {len(archive)} total incidents in {args.archive}")
        sys.exit(1)
    print(f"No changes. Archive has {len(archive)} incidents.")
    sys.exit(0)


if __name__ == "__main__":
    main()
