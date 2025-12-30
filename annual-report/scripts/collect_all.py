#!/usr/bin/env python3
"""
Annual Report Data Collector

Collects all usage statistics from various data sources and outputs
a unified JSON to stdout for report generation.

Usage:
    python3 collect_all.py [--year YEAR]

Example:
    python3 collect_all.py --year 2025
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Add the script directory to path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from collectors import (
    collect_code_proxy,
    collect_stats_cache,
    collect_history,
    collect_todos,
    collect_file_history,
    collect_plans,
)


def calculate_derived_metrics(data: dict) -> dict:
    """
    Calculate factual derived metrics from collected data.

    NOTE: Persona and traits analysis is intentionally NOT included here.
    These subjective interpretations should be done by Claude based on
    the raw data, allowing for more nuanced and contextual analysis.
    """
    derived = {
        "milestones": []
    }

    code_proxy = data.get('code_proxy', {})
    stats_cache = data.get('stats_cache', {})
    history = data.get('history', {})

    # Milestones - factual events only
    milestones = []
    overview = stats_cache.get('overview', {})

    # First session
    first_date = overview.get('first_session_date') or code_proxy.get('summary', {}).get('date_range', {}).get('first')
    if first_date:
        milestones.append({"type": "first_session", "date": first_date})

    # Longest session
    longest = stats_cache.get('longest_session', {})
    if longest and longest.get('timestamp'):
        milestones.append({
            "type": "longest_session",
            "date": longest.get('timestamp'),
            "messages": longest.get('messages', 0)
        })

    # Peak day
    peak_day = stats_cache.get('peak_day', {})
    if peak_day:
        milestones.append({
            "type": "peak_day",
            "date": peak_day.get('date'),
            "messages": peak_day.get('messages', 0)
        })

    # Most used project
    top_project = history.get('top_project', {})
    if top_project:
        milestones.append({
            "type": "top_project",
            "name": top_project.get('name'),
            "percentage": top_project.get('percentage', 0)
        })

    derived["milestones"] = milestones

    return derived


def collect_all(year: int) -> dict:
    """Collect data from all sources."""
    result = {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "year": year,
            "data_sources": {}
        }
    }

    # Collect from each source (Code Proxy first - highest priority)
    collectors = [
        ("code_proxy", collect_code_proxy),
        ("stats_cache", collect_stats_cache),
        ("history", collect_history),
        ("todos", collect_todos),
        ("file_history", collect_file_history),
        ("plans", collect_plans),
    ]

    for name, collector in collectors:
        try:
            data = collector(year)
            result[name] = data

            # Record data source status
            status = data.get('status', 'unknown')
            source_meta = {"status": status}

            if status == "ok":
                # Add record counts where available
                if 'total_requests' in data.get('summary', {}):
                    source_meta['records'] = data['summary']['total_requests']
                elif 'total_entries' in data:
                    source_meta['entries'] = data['total_entries']
                elif 'total_files' in data:
                    source_meta['files'] = data['total_files']
                elif 'total_plans' in data:
                    source_meta['files'] = data['total_plans']
                elif 'sessions_with_edits' in data:
                    source_meta['sessions'] = data['sessions_with_edits']

            result["meta"]["data_sources"][name] = source_meta

        except Exception as e:
            result[name] = {"status": "error", "error": str(e)}
            result["meta"]["data_sources"][name] = {"status": "error"}

    # Calculate derived metrics
    result["derived"] = calculate_derived_metrics(result)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Collect Claude Code usage statistics for annual report"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=datetime.now().year,
        help="Year to collect data for (default: current year)"
    )

    args = parser.parse_args()

    # Collect all data
    result = collect_all(args.year)

    # Output as JSON to stdout
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
