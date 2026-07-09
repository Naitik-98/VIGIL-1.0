from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from models.history_entry import HistoryEntry
from models.maintenance_task import MaintenanceTask


class JSONStorage:
    def __init__(self, data_dir: str | Path = "data") -> None:
        self.data_dir = Path(data_dir)
        self.tasks_file = self.data_dir / "tasks.json"
        self.history_file = self.data_dir / "history.json"

    def ensure_storage(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.tasks_file.exists():
            self._write_json(self.tasks_file, [])
        if not self.history_file.exists():
            self._write_json(self.history_file, [])

    def load_tasks(self) -> list[MaintenanceTask]:
        raw_items = self._read_json(self.tasks_file, default=[])
        tasks: list[MaintenanceTask] = []
        for item in raw_items:
            try:
                tasks.append(MaintenanceTask.from_dict(item))
            except (KeyError, TypeError, ValueError):
                continue
        return tasks

    def save_tasks(self, tasks: Iterable[MaintenanceTask]) -> None:
        self.ensure_storage()
        payload = [task.to_dict() for task in tasks]
        self._write_json(self.tasks_file, payload)

    def load_history(self) -> list[HistoryEntry]:
        raw_items = self._read_json(self.history_file, default=[])
        history: list[HistoryEntry] = []
        for item in raw_items:
            try:
                history.append(HistoryEntry.from_dict(item))
            except (KeyError, TypeError, ValueError):
                continue
        return history

    def save_history(self, history: Iterable[HistoryEntry]) -> None:
        self.ensure_storage()
        payload = [entry.to_dict() for entry in history]
        self._write_json(self.history_file, payload)

    def _read_json(self, path: Path, default: list[dict]) -> list[dict]:
        if not path.exists():
            self.ensure_storage()
            return default

        try:
            with path.open("r", encoding="utf-8") as file_handle:
                payload = json.load(file_handle)
        except FileNotFoundError:
            return default
        except json.JSONDecodeError:
            return default
        except TypeError:
            return default

        if isinstance(payload, list):
            return payload
        return default

    def _write_json(self, path: Path, payload: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(path.suffix + ".tmp")
        with temp_path.open("w", encoding="utf-8") as file_handle:
            json.dump(payload, file_handle, indent=2)
        temp_path.replace(path)
