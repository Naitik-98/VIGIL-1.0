from __future__ import annotations

import json
from collections import Counter
from datetime import date
from statistics import mean
from typing import Any
from uuid import uuid4

from domain import MaintenanceTask
from persistence import JSONStorage
from utils import current_timestamp
from validator import (
    COMPONENTS,
    MAINTENANCE_TYPES,
    STATUS_STATES,
    validate_component,
    validate_cost,
    validate_date,
    validate_maintenance_type,
    validate_required_text,
    validate_status,
    validate_task_id,
)


class ProtectionManager:
    def __init__(self, storage: JSONStorage | None = None, reminder_days: int = 7, autosave: bool = True) -> None:
        self.storage = storage or JSONStorage()
        self.reminder_days = reminder_days
        self.autosave = autosave
        self.tasks: dict[str, MaintenanceTask] = {}
        self.history: list[dict[str, Any]] = []
        self.settings: dict[str, Any] = {
            "dark_mode": True,
            "reminder_days": reminder_days,
            "autosave": autosave,
        }
        self.load()

    def load(self) -> None:
        try:
            payload = self.storage.load_payload()
        except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError):
            payload = self.storage.default_payload()

        loaded_tasks: dict[str, MaintenanceTask] = {}
        for raw_task in payload.get("tasks", []):
            try:
                task = MaintenanceTask.from_dict(raw_task)
                task.refresh_status(reminder_days=self.reminder_days)
                loaded_tasks[task.task_id] = task
            except (KeyError, TypeError, ValueError):
                continue

        self.tasks = loaded_tasks
        self.history = [record for record in payload.get("history", []) if isinstance(record, dict)]
        self._apply_settings(payload.get("settings", {}))
        self._persist_if_needed()

    def save(self) -> None:
        self.storage.save_payload(self._build_payload())

    def add_task(self, task: MaintenanceTask) -> MaintenanceTask:
        normalized = self._normalize_task(task)
        self._validate_task(normalized)
        if normalized.task_id in self.tasks:
            raise ValueError(f"Task ID '{normalized.task_id}' already exists.")

        normalized.refresh_status(reminder_days=self.reminder_days)
        self.tasks[normalized.task_id] = normalized
        self._append_history("created", normalized)
        self._persist_if_needed()
        return normalized

    def update_task(self, task_id: str, **changes: Any) -> MaintenanceTask:
        existing = self._get_task(task_id)
        candidate = MaintenanceTask(
            task_id=existing.task_id,
            component=changes.get("component", existing.component),
            maintenance_type=changes.get("maintenance_type", existing.maintenance_type),
            last_service_date=self._coerce_date(changes.get("last_service_date", existing.last_service_date), "Last service date"),
            next_service_date=self._coerce_date(changes.get("next_service_date", existing.next_service_date), "Next service date"),
            cost=self._coerce_cost(changes.get("cost", existing.cost)),
            status=str(changes.get("status", existing.status)).strip() or existing.status,
            notes=str(changes.get("notes", existing.notes)).strip(),
        )
        self._validate_task(candidate)
        candidate.refresh_status(reminder_days=self.reminder_days)
        self.tasks[task_id] = candidate
        self._append_history("updated", candidate)
        self._persist_if_needed()
        return candidate

    def delete_task(self, task_id: str) -> None:
        task = self._get_task(task_id)
        del self.tasks[task_id]
        self._append_history("deleted", task)
        self._persist_if_needed()

    def search_task(
        self,
        query: str = "",
        *,
        component: str | None = None,
        maintenance_type: str | None = None,
        status: str | None = None,
        due_soon_only: bool = False,
        overdue_only: bool = False,
    ) -> list[MaintenanceTask]:
        needle = query.strip().lower()
        results: list[MaintenanceTask] = []
        active_statuses = {status} if status else set(STATUS_STATES)

        for task in self.tasks.values():
            if needle:
                searchable = (
                    task.task_id.lower(),
                    task.component.lower(),
                    task.maintenance_type.lower(),
                    task.notes.lower(),
                    task.status.lower(),
                )
                if not any(needle in field for field in searchable):
                    continue
            if component and task.component != component:
                continue
            if maintenance_type and task.maintenance_type != maintenance_type:
                continue
            if task.status not in active_statuses:
                continue
            if overdue_only and not task.is_overdue():
                continue
            if due_soon_only and not task.is_due_soon(reminder_days=self.reminder_days):
                continue
            results.append(task)

        return sorted(results, key=lambda item: (item.days_remaining(), item.component.lower(), item.maintenance_type.lower()))

    def statistics(self) -> dict[str, Any]:
        tasks = list(self.tasks.values())
        costs = [task.cost for task in tasks]
        intervals = [max((task.next_service_date - task.last_service_date).days, 0) for task in tasks]
        monthly_spending = self._monthly_spending(tasks)

        return {
            "total_tasks": len(tasks),
            "healthy": sum(1 for task in tasks if task.status == "Healthy"),
            "due_soon": sum(1 for task in tasks if task.status == "Due Soon"),
            "overdue": sum(1 for task in tasks if task.status == "Overdue"),
            "average_cost": round(mean(costs), 2) if costs else 0.0,
            "highest_cost": max(costs) if costs else 0.0,
            "lowest_cost": min(costs) if costs else 0.0,
            "average_interval": round(mean(intervals), 2) if intervals else 0.0,
            "tasks_by_component": dict(Counter(task.component for task in tasks)),
            "tasks_by_maintenance_type": dict(Counter(task.maintenance_type for task in tasks)),
            "monthly_maintenance_spending": monthly_spending,
        }

    def days_remaining(self, task_id: str) -> int:
        return self._get_task(task_id).days_remaining()

    def is_overdue(self, task_id: str) -> bool:
        return self._get_task(task_id).is_overdue()

    def get_due_soon_tasks(self) -> list[MaintenanceTask]:
        return [task for task in self.tasks.values() if task.is_due_soon(reminder_days=self.reminder_days)]

    def get_overdue_tasks(self) -> list[MaintenanceTask]:
        return [task for task in self.tasks.values() if task.is_overdue()]

    def get_all_tasks(self) -> list[MaintenanceTask]:
        return list(self.tasks.values())

    def get_history(self) -> list[dict[str, Any]]:
        return list(self.history)

    def reset_data(self) -> None:
        self.tasks.clear()
        self.history.clear()
        self._persist_if_needed()

    def _normalize_task(self, task: MaintenanceTask) -> MaintenanceTask:
        if not isinstance(task, MaintenanceTask):
            raise TypeError("Task must be a MaintenanceTask instance.")

        return MaintenanceTask(
            task_id=validate_task_id(task.task_id),
            component=task.component,
            maintenance_type=task.maintenance_type,
            last_service_date=task.last_service_date,
            next_service_date=task.next_service_date,
            cost=task.cost,
            status=task.status,
            notes=task.notes,
        )

    def _validate_task(self, task: MaintenanceTask) -> None:
        validate_required_text(task.task_id, "Task ID")
        task.component = validate_component(task.component, COMPONENTS)
        task.maintenance_type = validate_maintenance_type(task.maintenance_type, MAINTENANCE_TYPES)
        task.last_service_date = self._coerce_date(task.last_service_date, "Last service date")
        task.next_service_date = self._coerce_date(task.next_service_date, "Next service date")
        task.cost = self._coerce_cost(task.cost)
        task.status = validate_status(task.status, STATUS_STATES)
        task.notes = str(task.notes).strip()

        if task.next_service_date < task.last_service_date:
            raise ValueError("Next service date cannot be earlier than last service date.")

    def _coerce_date(self, value: object, field_name: str) -> date:
        return validate_date(value, field_name)

    def _coerce_cost(self, value: object) -> float:
        return validate_cost(value)

    def _append_history(self, action: str, task: MaintenanceTask) -> None:
        record = {
            "record_id": str(uuid4()),
            "action": action,
            "task_id": task.task_id,
            "component": task.component,
            "maintenance_type": task.maintenance_type,
            "status": task.status,
            "cost": task.cost,
            "timestamp": current_timestamp(),
        }
        self.history.append(record)

    def _build_payload(self) -> dict[str, Any]:
        return {
            "tasks": [task.to_dict() for task in self.tasks.values()],
            "history": list(self.history),
            "settings": dict(self.settings),
        }

    def _apply_settings(self, settings: dict[str, Any]) -> None:
        if not isinstance(settings, dict):
            return
        self.settings.update(settings)
        self.reminder_days = int(self.settings.get("reminder_days", self.reminder_days))
        self.autosave = bool(self.settings.get("autosave", self.autosave))

    def _persist_if_needed(self) -> None:
        if self.autosave:
            self.save()

    def _get_task(self, task_id: str) -> MaintenanceTask:
        task_id = validate_task_id(task_id)
        try:
            return self.tasks[task_id]
        except KeyError as exc:
            raise KeyError(f"Task '{task_id}' was not found.") from exc

    def _monthly_spending(self, tasks: list[MaintenanceTask]) -> dict[str, float]:
        spending: dict[str, float] = {}
        for task in tasks:
            month_key = task.last_service_date.strftime("%Y-%m")
            spending[month_key] = round(spending.get(month_key, 0.0) + float(task.cost), 2)
        return dict(sorted(spending.items()))
