"""Plans collector - Architectural thinking statistics."""

from pathlib import Path
from typing import Any


def collect_plans(year: int) -> dict[str, Any]:
    """
    Collect plan file statistics from plans directory.

    Args:
        year: The year (not used for filtering, counts all plans)

    Returns:
        Dictionary containing plan statistics
    """
    plans_path = Path.home() / ".claude" / "plans"

    if not plans_path.exists():
        return {
            "status": "not_found",
            "error": f"Directory not found: {plans_path}"
        }

    try:
        plan_files = list(plans_path.glob("*.md"))
        total_plans = len(plan_files)

        # Calculate architectural thinking score
        if total_plans >= 20:
            score = "exceptional"
        elif total_plans >= 10:
            score = "high"
        elif total_plans >= 5:
            score = "moderate"
        elif total_plans > 0:
            score = "developing"
        else:
            score = "none"

        return {
            "status": "ok",
            "total_plans": total_plans,
            "architectural_thinking_score": score
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
