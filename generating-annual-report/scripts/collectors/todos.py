"""Todos collector - Task completion statistics."""

import json
from pathlib import Path
from typing import Any


def collect_todos(year: int) -> dict[str, Any]:
    """
    Collect task statistics from todos directory.

    Args:
        year: The year (not used for filtering, counts all todos)

    Returns:
        Dictionary containing task completion statistics
    """
    todos_path = Path.home() / ".claude" / "todos"

    if not todos_path.exists():
        return {
            "status": "not_found",
            "error": f"Directory not found: {todos_path}"
        }

    try:
        total_files = 0
        total_tasks = 0
        status_counts = {
            "completed": 0,
            "in_progress": 0,
            "pending": 0
        }
        files_all_completed = 0

        for json_file in todos_path.glob("*.json"):
            total_files += 1

            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    todos = json.load(f)

                if not isinstance(todos, list):
                    continue

                file_completed = True
                for todo in todos:
                    if not isinstance(todo, dict):
                        continue

                    total_tasks += 1
                    status = todo.get('status', 'pending')

                    if status in status_counts:
                        status_counts[status] += 1
                    else:
                        status_counts['pending'] += 1

                    if status != 'completed':
                        file_completed = False

                if file_completed and len(todos) > 0:
                    files_all_completed += 1

            except (json.JSONDecodeError, IOError):
                continue

        completion_rate = 0
        if total_tasks > 0:
            completion_rate = round(status_counts['completed'] / total_tasks * 100, 1)

        return {
            "status": "ok",
            "total_files": total_files,
            "total_tasks": total_tasks,
            "by_status": status_counts,
            "completion_rate": completion_rate,
            "files_with_all_completed": files_all_completed,
            "avg_tasks_per_session": round(total_tasks / total_files, 1) if total_files > 0 else 0
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
