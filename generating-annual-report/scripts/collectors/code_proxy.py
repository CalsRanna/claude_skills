"""Code Proxy database collector - PRIMARY data source."""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Any


def collect_code_proxy(year: int) -> dict[str, Any]:
    """
    Collect API request statistics from Code Proxy database.

    This is the PRIMARY data source when available, providing rich API usage metrics.

    Args:
        year: The year to filter data for

    Returns:
        Dictionary containing API request statistics
    """
    db_path = Path.home() / ".code_proxy" / "code_proxy.db"

    if not db_path.exists():
        return {
            "status": "not_found",
            "error": f"Database not found: {db_path}"
        }

    try:
        conn = sqlite3.connect(str(db_path), timeout=10)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Calculate year boundaries (timestamps in milliseconds)
        year_start = int(datetime(year, 1, 1).timestamp() * 1000)
        year_end = int(datetime(year + 1, 1, 1).timestamp() * 1000)

        result = {
            "status": "ok",
            "summary": _get_summary(cursor, year_start, year_end),
            "by_model": _get_by_model(cursor, year_start, year_end),
            "by_hour": _get_by_hour(cursor, year_start, year_end),
            "by_date": _get_by_date(cursor, year_start, year_end),
            "by_endpoint": _get_by_endpoint(cursor, year_start, year_end),
            "response_time_percentiles": _get_response_percentiles(cursor, year_start, year_end),
        }

        conn.close()
        return result

    except sqlite3.Error as e:
        return {
            "status": "error",
            "error": str(e)
        }


def _get_summary(cursor: sqlite3.Cursor, start: int, end: int) -> dict:
    """Get overall summary statistics."""
    cursor.execute("""
        SELECT
            COUNT(*) as total_requests,
            COALESCE(SUM(input_tokens), 0) as total_input_tokens,
            COALESCE(SUM(output_tokens), 0) as total_output_tokens,
            COALESCE(AVG(response_time), 0) as avg_response_time_ms,
            MIN(timestamp) as first_request,
            MAX(timestamp) as last_request
        FROM request_logs
        WHERE timestamp >= ? AND timestamp < ?
    """, (start, end))

    row = cursor.fetchone()

    first_date = None
    last_date = None
    if row['first_request']:
        first_date = datetime.fromtimestamp(row['first_request'] / 1000).strftime('%Y-%m-%d')
    if row['last_request']:
        last_date = datetime.fromtimestamp(row['last_request'] / 1000).strftime('%Y-%m-%d')

    return {
        "total_requests": row['total_requests'],
        "total_input_tokens": row['total_input_tokens'],
        "total_output_tokens": row['total_output_tokens'],
        "total_tokens": row['total_input_tokens'] + row['total_output_tokens'],
        "avg_response_time_ms": round(row['avg_response_time_ms'], 1),
        "date_range": {
            "first": first_date,
            "last": last_date
        }
    }


def _get_by_model(cursor: sqlite3.Cursor, start: int, end: int) -> list[dict]:
    """Get statistics grouped by model."""
    cursor.execute("""
        SELECT
            model,
            COUNT(*) as requests,
            COALESCE(SUM(input_tokens), 0) as input_tokens,
            COALESCE(SUM(output_tokens), 0) as output_tokens,
            COALESCE(AVG(response_time), 0) as avg_response_time_ms
        FROM request_logs
        WHERE timestamp >= ? AND timestamp < ? AND model IS NOT NULL
        GROUP BY model
        ORDER BY requests DESC
    """, (start, end))

    return [
        {
            "model": row['model'],
            "requests": row['requests'],
            "input_tokens": row['input_tokens'],
            "output_tokens": row['output_tokens'],
            "total_tokens": row['input_tokens'] + row['output_tokens'],
            "avg_response_time_ms": round(row['avg_response_time_ms'], 1)
        }
        for row in cursor.fetchall()
    ]


def _get_by_hour(cursor: sqlite3.Cursor, start: int, end: int) -> list[dict]:
    """Get request distribution by hour of day."""
    cursor.execute("""
        SELECT
            CAST(strftime('%H', datetime(timestamp / 1000, 'unixepoch', 'localtime')) AS INTEGER) as hour,
            COUNT(*) as requests
        FROM request_logs
        WHERE timestamp >= ? AND timestamp < ?
        GROUP BY hour
        ORDER BY hour
    """, (start, end))

    return [
        {"hour": row['hour'], "requests": row['requests']}
        for row in cursor.fetchall()
    ]


def _get_by_date(cursor: sqlite3.Cursor, start: int, end: int) -> list[dict]:
    """Get daily request statistics."""
    cursor.execute("""
        SELECT
            date(datetime(timestamp / 1000, 'unixepoch', 'localtime')) as date,
            COUNT(*) as requests,
            COALESCE(SUM(input_tokens + output_tokens), 0) as tokens
        FROM request_logs
        WHERE timestamp >= ? AND timestamp < ?
        GROUP BY date
        ORDER BY date
    """, (start, end))

    return [
        {
            "date": row['date'],
            "requests": row['requests'],
            "tokens": row['tokens']
        }
        for row in cursor.fetchall()
    ]


def _get_by_endpoint(cursor: sqlite3.Cursor, start: int, end: int) -> list[dict]:
    """Get statistics grouped by endpoint."""
    cursor.execute("""
        SELECT
            endpoint_name,
            COUNT(*) as requests,
            COALESCE(SUM(input_tokens + output_tokens), 0) as tokens
        FROM request_logs
        WHERE timestamp >= ? AND timestamp < ?
        GROUP BY endpoint_name
        ORDER BY requests DESC
    """, (start, end))

    return [
        {
            "endpoint": row['endpoint_name'],
            "requests": row['requests'],
            "tokens": row['tokens']
        }
        for row in cursor.fetchall()
    ]


def _get_response_percentiles(cursor: sqlite3.Cursor, start: int, end: int) -> dict:
    """Get response time percentiles."""
    cursor.execute("""
        SELECT response_time
        FROM request_logs
        WHERE timestamp >= ? AND timestamp < ? AND response_time IS NOT NULL
        ORDER BY response_time
    """, (start, end))

    times = [row['response_time'] for row in cursor.fetchall()]

    if not times:
        return {"p50": 0, "p90": 0, "p99": 0}

    def percentile(data: list, p: float) -> int:
        idx = int(len(data) * p)
        return data[min(idx, len(data) - 1)]

    return {
        "p50": percentile(times, 0.50),
        "p90": percentile(times, 0.90),
        "p99": percentile(times, 0.99)
    }
