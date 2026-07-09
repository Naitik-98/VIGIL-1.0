from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from utils import format_date, parse_date


@dataclass(slots=True)
class MaintenanceTask:
    task_id: str
    component: str
    maintenance_type: str
    last_service_date: date
    next_service_date: date
    cost: float
    status: str = "Healthy"
    notes: str = ""

    def days_remaining(self, as_of: date | None = None) -> int:
        reference_date = as_of or date.today()
        return (self.next_service_date - reference_date).days

    def is_overdue(self, as_of: date | None = None) -> bool:
        return self.days_remaining(as_of) < 0

    def is_due_soon(self, as_of: date | None = None, reminder_days: int = 7) -> bool:
        remaining = self.days_remaining(as_of)
        return 0 <= remaining <= reminder_days

    def refresh_status(self, as_of: date | None = None, reminder_days: int = 7) -> str:
        if self.is_overdue(as_of):
            self.status = "Overdue"
        elif self.is_due_soon(as_of, reminder_days):
            self.status = "Due Soon"
        else:
            self.status = "Healthy"
        return self.status

    def extend_next_service_date(self, interval_days: int) -> None:
        self.next_service_date = self.last_service_date + timedelta(days=interval_days)
        self.refresh_status()

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "component": self.component,
            "maintenance_type": self.maintenance_type,
            "last_service_date": format_date(self.last_service_date),
            "next_service_date": format_date(self.next_service_date),
            "cost": round(float(self.cost), 2),
            "status": self.status,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MaintenanceTask":
        if not isinstance(payload, dict):
            raise TypeError("Task payload must be a dictionary.")

        task = cls(
            task_id=str(payload["task_id"]).strip(),
            component=str(payload["component"]).strip(),
            maintenance_type=str(payload["maintenance_type"]).strip(),
            last_service_date=parse_date(payload["last_service_date"]),
            next_service_date=parse_date(payload["next_service_date"]),
            cost=float(payload["cost"]),
            status=str(payload.get("status", "Healthy")).strip() or "Healthy",
            notes=str(payload.get("notes", "")).strip(),
        )
        return task
