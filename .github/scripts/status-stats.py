#!/usr/bin/env python3
"""Generate statistical analysis of Claude platform outages from JSONL archive.

Reads the outage archive and produces a markdown report with frequency,
duration, severity, component, and time-of-day analysis.

Usage:
    python status-stats.py --archive data/outages.jsonl > data/outage-stats.md

All calculations use stdlib only (no pandas/numpy).
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


def load_archive(path: Path) -> list[dict]:
    """Load all records from the JSONL archive."""
    records: list[dict] = []
    if not path.exists():
        print(f"ERROR: Archive not found: {path}", file=sys.stderr)
        sys.exit(2)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def parse_dt(s: str) -> datetime | None:
    """Parse an ISO 8601 datetime string."""
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def median(values: list[int | float]) -> float:
    """Compute median of a sorted list."""
    if not values:
        return 0.0
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return float(s[n // 2])
    return (s[n // 2 - 1] + s[n // 2]) / 2.0


def mean(values: list[int | float]) -> float:
    """Compute mean of a list."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def format_duration(minutes: float) -> str:
    """Format minutes as human-readable duration."""
    if minutes < 60:
        return f"{minutes:.0f}m"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.1f}h"
    days = hours / 24
    return f"{days:.1f}d"


def generate_report(records: list[dict]) -> str:
    """Generate a markdown statistical report from outage records."""
    lines: list[str] = []
    lines.append("# Claude Platform Outage Statistics")
    lines.append("")
    lines.append(f"*Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} "
                 f"| {len(records)} incidents in archive*")
    lines.append("")

    if not records:
        lines.append("No incidents recorded yet.")
        return "\n".join(lines)

    # Parse dates
    resolved = []
    all_starts: list[datetime] = []
    durations: list[int] = []
    for r in records:
        start = parse_dt(r.get("started_at", ""))
        if start:
            all_starts.append(start)
        dur = r.get("duration_minutes")
        if dur is not None and isinstance(dur, (int, float)):
            durations.append(int(dur))
            resolved.append(r)

    # --- Summary ---
    lines.append("## Summary")
    lines.append("")
    unresolved = sum(1 for r in records if r.get("status") != "resolved")
    lines.append(f"- **Total incidents**: {len(records)}")
    lines.append(f"- **Resolved**: {len(resolved)}")
    lines.append(f"- **Unresolved/ongoing**: {unresolved}")
    if all_starts:
        earliest = min(all_starts)
        latest = max(all_starts)
        lines.append(f"- **Date range**: {earliest.strftime('%Y-%m-%d')} to {latest.strftime('%Y-%m-%d')}")
        span_days = max(1, (latest - earliest).days)
        lines.append(f"- **Span**: {span_days} days")
        lines.append(f"- **Rate**: {len(records) / (span_days / 7):.1f} incidents/week")
    lines.append("")

    # --- Duration Analysis ---
    if durations:
        lines.append("## Resolution Time")
        lines.append("")
        lines.append(f"| Metric | Value |")
        lines.append(f"|--------|-------|")
        lines.append(f"| Min | {format_duration(min(durations))} |")
        lines.append(f"| Max | {format_duration(max(durations))} |")
        lines.append(f"| Median | {format_duration(median(durations))} |")
        lines.append(f"| Mean | {format_duration(mean(durations))} |")
        lines.append(f"| Total downtime | {format_duration(sum(durations))} |")
        lines.append("")

    # --- Severity Distribution ---
    impact_counts = Counter(r.get("impact", "unknown") for r in records)
    lines.append("## Severity Distribution")
    lines.append("")
    lines.append("| Impact | Count | % |")
    lines.append("|--------|-------|---|")
    for impact, count in impact_counts.most_common():
        pct = count / len(records) * 100
        lines.append(f"| {impact} | {count} | {pct:.0f}% |")
    lines.append("")

    # --- MTTR by Severity ---
    if durations:
        severity_durations: dict[str, list[int]] = defaultdict(list)
        for r in resolved:
            dur = r.get("duration_minutes")
            if dur is not None:
                severity_durations[r.get("impact", "unknown")].append(int(dur))

        lines.append("## MTTR by Severity")
        lines.append("")
        lines.append("| Impact | MTTR (mean) | MTTR (median) | Count |")
        lines.append("|--------|-------------|---------------|-------|")
        for impact in sorted(severity_durations.keys()):
            durs = severity_durations[impact]
            lines.append(
                f"| {impact} | {format_duration(mean(durs))} "
                f"| {format_duration(median(durs))} | {len(durs)} |"
            )
        lines.append("")

    # --- Component Heatmap ---
    comp_counts: Counter[str] = Counter()
    comp_durations: dict[str, list[int]] = defaultdict(list)
    for r in records:
        dur = r.get("duration_minutes")
        for comp in r.get("affected_components", []):
            comp_counts[comp] += 1
            if dur is not None:
                comp_durations[comp].append(int(dur))

    if comp_counts:
        lines.append("## Component Frequency")
        lines.append("")
        lines.append("| Component | Incidents | Total Downtime | Avg Duration |")
        lines.append("|-----------|-----------|----------------|--------------|")
        for comp, count in comp_counts.most_common():
            durs = comp_durations.get(comp, [])
            total = format_duration(sum(durs)) if durs else "—"
            avg = format_duration(mean(durs)) if durs else "—"
            lines.append(f"| {comp} | {count} | {total} | {avg} |")
        lines.append("")

    # --- Time-of-Day Distribution ---
    if all_starts:
        hour_counts = Counter(dt.hour for dt in all_starts)
        lines.append("## Time-of-Day Distribution (UTC)")
        lines.append("")
        lines.append("| Hour | Incidents | Bar |")
        lines.append("|------|-----------|-----|")
        max_count = max(hour_counts.values()) if hour_counts else 1
        for hour in range(24):
            count = hour_counts.get(hour, 0)
            bar = "#" * int(count / max_count * 20) if count > 0 else ""
            lines.append(f"| {hour:02d}:00 | {count} | {bar} |")
        lines.append("")

    # --- Day-of-Week Distribution ---
    if all_starts:
        dow_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow_counts = Counter(dt.weekday() for dt in all_starts)
        lines.append("## Day-of-Week Distribution")
        lines.append("")
        lines.append("| Day | Incidents | Bar |")
        lines.append("|-----|-----------|-----|")
        max_dow = max(dow_counts.values()) if dow_counts else 1
        for day_idx, day_name in enumerate(dow_names):
            count = dow_counts.get(day_idx, 0)
            bar = "#" * int(count / max_dow * 20) if count > 0 else ""
            lines.append(f"| {day_name} | {count} | {bar} |")
        lines.append("")

    # --- Monthly Trend ---
    if all_starts:
        month_counts: Counter[str] = Counter()
        for dt in all_starts:
            month_counts[dt.strftime("%Y-%m")] += 1

        lines.append("## Monthly Trend")
        lines.append("")
        lines.append("| Month | Incidents | Bar |")
        lines.append("|-------|-----------|-----|")
        max_month = max(month_counts.values()) if month_counts else 1
        for month in sorted(month_counts.keys()):
            count = month_counts[month]
            bar = "#" * int(count / max_month * 20) if count > 0 else ""
            lines.append(f"| {month} | {count} | {bar} |")
        lines.append("")

    # --- Uptime Estimate ---
    if all_starts and durations:
        span_minutes = max(1, (max(all_starts) - min(all_starts)).total_seconds() / 60)
        total_down = sum(durations)
        uptime_pct = (1 - total_down / span_minutes) * 100
        lines.append("## Uptime Estimate")
        lines.append("")
        lines.append(f"- **Overall uptime**: {uptime_pct:.3f}%")
        lines.append(f"- **Total downtime**: {format_duration(total_down)}")
        lines.append(f"- **Measurement period**: {format_duration(span_minutes)}")
        lines.append("")

        # Per-component uptime
        if comp_durations:
            lines.append("| Component | Uptime % | Downtime |")
            lines.append("|-----------|----------|----------|")
            for comp, durs in sorted(comp_durations.items(), key=lambda x: -sum(x[1])):
                comp_down = sum(durs)
                comp_up = (1 - comp_down / span_minutes) * 100
                lines.append(f"| {comp} | {comp_up:.3f}% | {format_duration(comp_down)} |")
            lines.append("")

    return "\n".join(lines)


def main() -> None:
    """Entry point for the status stats generator."""
    parser = argparse.ArgumentParser(
        description="Generate outage statistics from JSONL archive."
    )
    parser.add_argument(
        "--archive", type=Path, default=Path("data/outages.jsonl"),
        help="Path to the JSONL archive file (default: data/outages.jsonl)",
    )
    args = parser.parse_args()

    records = load_archive(args.archive)
    report = generate_report(records)
    print(report)


if __name__ == "__main__":
    main()
