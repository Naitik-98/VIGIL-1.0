from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any, ClassVar

DATE_FORMAT: str = "%Y-%m-%d"
DUE_SOON_BUFFER_DAYS: int = 3


@dataclass(slots=True)
class MaintenanceTask:
    id: str
    name: str
    category: str
    interval_days: int
    last_done: date
    notes: str = ""

    def days_remaining(self, as_of: date | None = None) -> int:
        reference_date = as_of or date.today()
        next_due = self.last_done + timedelta(days=self.interval_days)
        return (next_due - reference_date).days

    def is_overdue(self, as_of: date | None = None) -> bool:
        return self.days_remaining(as_of) < 0

    def is_due_soon(self, as_of: date | None = None, buffer_days: int = DUE_SOON_BUFFER_DAYS) -> bool:
        remaining = self.days_remaining(as_of)
        return 0 <= remaining <= buffer_days

    @property
    def status(self) -> str:
        if self.is_overdue():
            return "Overdue"
        if self.is_due_soon():
            return "Due"
        return "Healthy"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "interval_days": self.interval_days,
            "last_done": self.last_done.strftime(DATE_FORMAT),
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "MaintenanceTask":
        if not isinstance(payload, dict):
            raise TypeError("Task payload must be a dictionary.")

        return cls(
            id=str(payload["id"]).strip(),
            name=str(payload["name"]).strip(),
            category=str(payload["category"]).strip(),
            interval_days=int(payload["interval_days"]),
            last_done=datetime.strptime(str(payload["last_done"]), DATE_FORMAT).date(),
            notes=str(payload.get("notes", "")).strip(),
        )
