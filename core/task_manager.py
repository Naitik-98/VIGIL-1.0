from __future__ import annotations

import json
from collections import Counter
from datetime import date
from typing import Any
from uuid import uuid4

from core.validators import (
    DEFAULT_CATEGORIES,
    is_valid_category,
    is_valid_interval,
    is_valid_task_name,
    parse_date,
)
from models.history_entry import HistoryEntry
from models.maintenance_task import MaintenanceTask
from storage.json_storage import JSONStorage


class TaskManager:
    def __init__(self, storage: JSONStorage | None = None, due_soon_days: int = 3) -> None:
        self.storage = storage or JSONStorage()
        self.due_soon_days = due_soon_days
        self.tasks: dict[str, MaintenanceTask] = {}
        self.history: list[HistoryEntry] = []
        self.load()

    def load(self) -> None:
        try:
            loaded_tasks = self.storage.load_tasks()
            loaded_history = self.storage.load_history()
        except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError):
            loaded_tasks = []
            loaded_history = []

        self.tasks = {task.id: task for task in loaded_tasks}
        self.history = list(loaded_history)

    def save(self) -> None:
        self.storage.save_tasks(self.tasks.values())
        self.storage.save_history(self.history)

    def add_task(self, task: MaintenanceTask) -> MaintenanceTask:
        normalized = self._normalize_task(task)
        self._validate_task(normalized)
        if normalized.id in self.tasks:
            raise ValueError(f"Task ID '{normalized.id}' already exists.")
        self.tasks[normalized.id] = normalized
        self.save()
        return normalized

    def update_task(self, task_id: str, **changes: Any) -> MaintenanceTask:
        task = self._get_task(task_id)
        last_done_value = changes.get("last_done", task.last_done)
        normalized = MaintenanceTask(
            id=task.id,
            name=str(changes.get("name", task.name)).strip(),
            category=str(changes.get("category", task.category)).strip(),
            interval_days=self._to_int(changes.get("interval_days", task.interval_days)),
            last_done=self._coerce_date(last_done_value),
            notes=str(changes.get("notes", task.notes)).strip(),
        )
        self._validate_task(normalized)
        self.tasks[task_id] = normalized
        self.save()
        return normalized

    def delete_task(self, task_id: str) -> None:
        if task_id not in self.tasks:
            raise KeyError(f"Task '{task_id}' was not found.")
        del self.tasks[task_id]
        self.history = [entry for entry in self.history if entry.task_id != task_id]
        self.save()

    def search_task(self, query: str) -> list[MaintenanceTask]:
        needle = query.strip().lower()
        if not needle:
            return list(self.tasks.values())
        return [
            task
            for task in self.tasks.values()
            if needle in task.name.lower() or needle in task.category.lower() or needle in task.status.lower()
        ]

    def mark_done(self, task_id: str, note: str = "") -> HistoryEntry:
        task = self._get_task(task_id)
        completed_on = date.today()
        task.last_done = completed_on
        history_entry = HistoryEntry(id=str(uuid4()), task_id=task.id, completed_on=completed_on, note=note.strip())
        self.history.append(history_entry)
        self.save()
        return history_entry

    def get_task(self, task_id: str) -> MaintenanceTask:
        return self._get_task(task_id)

    def get_all_tasks(self) -> list[MaintenanceTask]:
        return list(self.tasks.values())

    def get_history(self) -> list[HistoryEntry]:
        return list(self.history)

    def days_remaining(self, task_id: str) -> int:
        return self._get_task(task_id).days_remaining()

    def is_overdue(self, task_id: str) -> bool:
        return self._get_task(task_id).is_overdue()

    def statistics(self) -> dict[str, Any]:
        summary = self.get_summary()
        categories = {task.category for task in self.tasks.values()}
        counts = Counter(task.category for task in self.tasks.values())
        due_soon = [task for task in self.tasks.values() if task.is_due_soon(date.today(), self.due_soon_days)]
        return {
            **summary,
            "categories": tuple(sorted(categories)),
            "category_counts": dict(counts),
            "due_soon_count": len(due_soon),
        }

    def get_summary(self) -> dict[str, int]:
        healthy = due = overdue = 0
        today = date.today()
        for task in self.tasks.values():
            if task.is_overdue(today):
                overdue += 1
            elif task.is_due_soon(today, self.due_soon_days):
                due += 1
            else:
                healthy += 1
        return {
            "total_tasks": len(self.tasks),
            "healthy": healthy,
            "due": due,
            "overdue": overdue,
        }

    def _normalize_task(self, task: MaintenanceTask) -> MaintenanceTask:
        if not isinstance(task, MaintenanceTask):
            raise TypeError("Task must be a MaintenanceTask instance.")
        return MaintenanceTask(
            id=str(task.id).strip(),
            name=str(task.name).strip(),
            category=str(task.category).strip(),
            interval_days=self._to_int(task.interval_days),
            last_done=self._coerce_date(task.last_done),
            notes=str(task.notes).strip(),
        )

    def _validate_task(self, task: MaintenanceTask) -> None:
        if not task.id:
            raise ValueError("Task ID cannot be empty.")
        if not is_valid_task_name(task.name):
            raise ValueError("Task name cannot be empty.")
        if not is_valid_category(task.category, DEFAULT_CATEGORIES):
            raise ValueError("Task category is invalid.")
        if not is_valid_interval(task.interval_days):
            raise ValueError("Interval must be a positive integer.")
        if not isinstance(task.last_done, date):
            raise ValueError("Last done value must be a valid date.")

    def _to_int(self, value: Any) -> int:
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Interval must be a positive integer.") from exc

    def _coerce_date(self, value: Any) -> date:
        try:
            return parse_date(value)
        except ValueError as exc:
            raise ValueError("Last done value must be a valid date.") from exc

    def _get_task(self, task_id: str) -> MaintenanceTask:
        try:
            return self.tasks[task_id]
        except KeyError as exc:
            raise KeyError(f"Task '{task_id}' was not found.") from exc
