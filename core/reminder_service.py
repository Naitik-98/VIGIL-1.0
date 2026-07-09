from __future__ import annotations

from datetime import date
from typing import Iterable

from models.maintenance_task import MaintenanceTask


class ReminderService:
    def __init__(self, due_soon_days: int = 3) -> None:
        self.due_soon_days = due_soon_days

    def get_due_items(self, tasks: Iterable[MaintenanceTask]) -> list[MaintenanceTask]:
        reference_date = date.today()
        due_items = [
            task
            for task in tasks
            if task.is_overdue(reference_date) or task.is_due_soon(reference_date, self.due_soon_days)
        ]
        return sorted(due_items, key=self._sort_key)

    def get_overdue_items(self, tasks: Iterable[MaintenanceTask]) -> list[MaintenanceTask]:
        reference_date = date.today()
        overdue_items = [task for task in tasks if task.is_overdue(reference_date)]
        return sorted(overdue_items, key=self._sort_key)

    def _sort_key(self, task: MaintenanceTask) -> tuple[int, int, str]:
        remaining = task.days_remaining(date.today())
        urgency_rank = 0 if remaining < 0 else 1
        return urgency_rank, remaining, task.name.lower()
