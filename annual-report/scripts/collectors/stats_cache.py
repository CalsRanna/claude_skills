"""Stats cache collector - Core usage statistics."""

import json
from pathlib import Path
from typing import Any


def collect_stats_cache(year: int) -> dict[str, Any]:
    """
    Collect statistics from stats-cache.json.

    Args:
        year: The year to filter data for

    Returns:
        Dictionary containing usage statistics
    """
    cache_path = Path.home() / ".claude" / "stats-cache.json"

    if not cache_path.exists():
        return {
            "status": "not_found",
            "error": f"File not found: {cache_path}"
        }

    try:
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Filter data by year
        year_str = str(year)

        daily_activity = [
            d for d in data.get('dailyActivity', [])
            if d.get('date', '').startswith(year_str)
        ]

        daily_model_tokens = [
            d for d in data.get('dailyModelTokens', [])
            if d.get('date', '').startswith(year_str)
        ]

        # Calculate overview stats
        total_messages = sum(d.get('messageCount', 0) for d in daily_activity)
        total_sessions = data.get('totalSessions', 0)
        active_days = len(daily_activity)

        # Hour distribution from hourCounts
        hour_counts = data.get('hourCounts', {})
        hour_distribution = [
            {"hour": int(h), "sessions": c}
            for h, c in sorted(hour_counts.items(), key=lambda x: int(x[0]))
        ]

        # Find peak hour
        peak_hour = None
        if hour_counts:
            peak_hour = max(hour_counts.items(), key=lambda x: x[1])
            peak_hour = {"hour": int(peak_hour[0]), "sessions": peak_hour[1]}

        # Find peak day
        peak_day = None
        if daily_activity:
            max_day = max(daily_activity, key=lambda x: x.get('messageCount', 0))
            peak_day = {
                "date": max_day.get('date'),
                "messages": max_day.get('messageCount', 0)
            }

        # Longest session
        longest_session = data.get('longestSession', {})

        # Model usage
        model_usage = data.get('modelUsage', {})

        return {
            "status": "ok",
            "overview": {
                "total_sessions": total_sessions,
                "total_messages": total_messages,
                "first_session_date": data.get('firstSessionDate'),
                "active_days": active_days,
                "avg_messages_per_day": round(total_messages / active_days, 1) if active_days > 0 else 0,
                "avg_messages_per_session": round(total_messages / total_sessions, 1) if total_sessions > 0 else 0,
            },
            "daily_activity": daily_activity,
            "daily_model_tokens": daily_model_tokens,
            "model_usage": model_usage,
            "hour_distribution": hour_distribution,
            "peak_hour": peak_hour,
            "peak_day": peak_day,
            "longest_session": {
                "messages": longest_session.get('messageCount', 0),
                "timestamp": longest_session.get('timestamp'),
            } if longest_session else None,
        }

    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "error": f"JSON parse error: {e}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
