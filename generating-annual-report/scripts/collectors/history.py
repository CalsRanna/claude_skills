"""History collector - Project distribution and patterns."""

import json
from pathlib import Path
from datetime import datetime
from collections import Counter
from typing import Any


def collect_history(year: int) -> dict[str, Any]:
    """
    Collect project and conversation history from history.jsonl.

    Args:
        year: The year to filter data for

    Returns:
        Dictionary containing project distribution and time patterns
    """
    history_path = Path.home() / ".claude" / "history.jsonl"

    if not history_path.exists():
        return {
            "status": "not_found",
            "error": f"File not found: {history_path}"
        }

    try:
        entries = []
        project_counter = Counter()
        timestamps = []

        with open(history_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Filter by year
                ts = entry.get('timestamp')
                if ts:
                    # Handle both seconds and milliseconds timestamps
                    if ts > 10000000000:  # milliseconds
                        ts = ts / 1000
                    dt = datetime.fromtimestamp(ts)
                    if dt.year != year:
                        continue
                    timestamps.append(dt)

                entries.append(entry)

                # Count projects
                project = entry.get('project')
                if project:
                    project_counter[project] += 1

        total_entries = len(entries)

        # Calculate project distribution
        projects = []
        for path, count in project_counter.most_common():
            projects.append({
                "path": path,
                "name": Path(path).name,
                "count": count,
                "percentage": round(count / total_entries * 100, 1) if total_entries > 0 else 0
            })

        # Time range
        time_range = None
        if timestamps:
            time_range = {
                "first": min(timestamps).isoformat(),
                "last": max(timestamps).isoformat()
            }

        # Top project
        top_project = None
        if projects:
            top_project = {
                "path": projects[0]['path'],
                "name": projects[0]['name'],
                "percentage": projects[0]['percentage']
            }

        return {
            "status": "ok",
            "total_entries": total_entries,
            "unique_projects": len(project_counter),
            "projects": projects[:20],  # Top 20 projects
            "time_range": time_range,
            "top_project": top_project,
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
