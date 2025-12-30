"""Data collectors for annual report generation."""

from .code_proxy import collect_code_proxy
from .stats_cache import collect_stats_cache
from .history import collect_history
from .todos import collect_todos
from .file_history import collect_file_history
from .plans import collect_plans

__all__ = [
    'collect_code_proxy',
    'collect_stats_cache',
    'collect_history',
    'collect_todos',
    'collect_file_history',
    'collect_plans',
]
