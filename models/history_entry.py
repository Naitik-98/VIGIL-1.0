from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

DATE_FORMAT: str = "%Y-%m-%d"


@dataclass(slots=True)
class HistoryEntry:
    id: str
    task_id: str
    completed_on: date
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "task_id": self.task_id,
            "completed_on": self.completed_on.strftime(DATE_FORMAT),
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "HistoryEntry":
        if not isinstance(payload, dict):
            raise TypeError("History payload must be a dictionary.")

        return cls(
            id=str(payload["id"]).strip(),
            task_id=str(payload["task_id"]).strip(),
            completed_on=datetime.strptime(str(payload["completed_on"]), DATE_FORMAT).date(),
            note=str(payload.get("note", "")).strip(),
        )
