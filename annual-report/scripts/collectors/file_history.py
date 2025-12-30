"""File history collector - Edit activity statistics."""

from pathlib import Path
from collections import Counter
from typing import Any


def collect_file_history(year: int) -> dict[str, Any]:
    """
    Collect file editing statistics from file-history directory.

    Args:
        year: The year (not used for filtering, counts all history)

    Returns:
        Dictionary containing file edit statistics
    """
    history_path = Path.home() / ".claude" / "file-history"

    if not history_path.exists():
        return {
            "status": "not_found",
            "error": f"Directory not found: {history_path}"
        }

    try:
        sessions_with_edits = 0
        total_file_versions = 0
        file_counter = Counter()

        # Each subdirectory is a session
        for session_dir in history_path.iterdir():
            if not session_dir.is_dir():
                continue

            sessions_with_edits += 1

            # Count files in each session
            for file_path in session_dir.rglob("*"):
                if file_path.is_file():
                    total_file_versions += 1
                    file_counter[file_path.name] += 1

        # Most edited files
        most_edited = [
            {"file": name, "versions": count}
            for name, count in file_counter.most_common(10)
        ]

        return {
            "status": "ok",
            "sessions_with_edits": sessions_with_edits,
            "total_file_versions": total_file_versions,
            "avg_files_per_session": round(total_file_versions / sessions_with_edits, 1) if sessions_with_edits > 0 else 0,
            "most_edited_files": most_edited
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
