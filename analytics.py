from __future__ import annotations

from collections import defaultdict, Counter
from datetime import date, datetime, timedelta
from typing import Any

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None  # type: ignore

from domain import MaintenanceTask


class StatsEngine:
    @staticmethod
    def calculate_compliance_rate(tasks: list[MaintenanceTask]) -> float:
        if not tasks:
            return 100.0
        healthy_count = sum(1 for task in tasks if task.status == "Healthy")
        return round((healthy_count / len(tasks)) * 100, 1)

    @staticmethod
    def average_delay_per_component(tasks: list[MaintenanceTask]) -> dict[str, float]:
        by_component: dict[str, list[int]] = defaultdict(list)
        for task in tasks:
            if task.is_overdue():
                days_over = abs(task.days_remaining())
                by_component[task.component].append(days_over)

        result = {}
        for component, delays in by_component.items():
            if delays:
                if NUMPY_AVAILABLE:
                    result[component] = round(float(np.mean(delays)), 2)
                else:
                    result[component] = round(sum(delays) / len(delays), 2)
        return dict(sorted(result.items()))

    @staticmethod
    def tasks_by_component(tasks: list[MaintenanceTask]) -> dict[str, int]:
        counts = Counter(task.component for task in tasks)
        return dict(sorted(counts.items()))

    @staticmethod
    def tasks_by_maintenance_type(tasks: list[MaintenanceTask]) -> dict[str, int]:
        counts = Counter(task.maintenance_type for task in tasks)
        return dict(sorted(counts.items()))

    @staticmethod
    def monthly_spending_trend(tasks: list[MaintenanceTask], months_back: int = 12) -> dict[str, float]:
        spending: dict[str, float] = defaultdict(float)
        cutoff_date = date.today() - timedelta(days=30 * months_back)

        for task in tasks:
            if task.last_service_date >= cutoff_date:
                month_key = task.last_service_date.strftime("%Y-%m")
                spending[month_key] += float(task.cost)

        result = {key: round(value, 2) for key, value in sorted(spending.items())}
        return result

    @staticmethod
    def cost_statistics(tasks: list[MaintenanceTask]) -> dict[str, float]:
        if not tasks:
            return {
                "average": 0.0,
                "highest": 0.0,
                "lowest": 0.0,
                "median": 0.0,
                "total": 0.0,
            }

        costs = [task.cost for task in tasks]
        if NUMPY_AVAILABLE:
            costs_array = np.array(costs)
            return {
                "average": round(float(np.mean(costs_array)), 2),
                "highest": round(float(np.max(costs_array)), 2),
                "lowest": round(float(np.min(costs_array)), 2),
                "median": round(float(np.median(costs_array)), 2),
                "total": round(float(np.sum(costs_array)), 2),
            }
        else:
            sorted_costs = sorted(costs)
            median = (
                sorted_costs[len(sorted_costs) // 2]
                if len(sorted_costs) % 2 != 0
                else (sorted_costs[len(sorted_costs) // 2 - 1] + sorted_costs[len(sorted_costs) // 2]) / 2
            )
            return {
                "average": round(sum(costs) / len(costs), 2),
                "highest": round(max(costs), 2),
                "lowest": round(min(costs), 2),
                "median": round(median, 2),
                "total": round(sum(costs), 2),
            }

    @staticmethod
    def maintenance_interval_stats(tasks: list[MaintenanceTask]) -> dict[str, float]:
        if not tasks:
            return {
                "average_days": 0.0,
                "shortest_days": 0.0,
                "longest_days": 0.0,
            }

        intervals = [max((task.next_service_date - task.last_service_date).days, 0) for task in tasks]
        if NUMPY_AVAILABLE:
            intervals_array = np.array(intervals)
            return {
                "average_days": round(float(np.mean(intervals_array)), 2),
                "shortest_days": round(float(np.min(intervals_array)), 2),
                "longest_days": round(float(np.max(intervals_array)), 2),
            }
        else:
            return {
                "average_days": round(sum(intervals) / len(intervals), 2) if intervals else 0.0,
                "shortest_days": round(float(min(intervals)), 2) if intervals else 0.0,
                "longest_days": round(float(max(intervals)), 2) if intervals else 0.0,
            }
