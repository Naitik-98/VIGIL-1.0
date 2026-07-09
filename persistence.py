from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_STORAGE_NAME: str = "maintenance.json"


class JSONStorage:
    def __init__(self, file_path: str | Path = Path("data") / DEFAULT_STORAGE_NAME) -> None:
        self.file_path = Path(file_path)

    def default_payload(self) -> dict[str, Any]:
        return {
            "tasks": [],
            "history": [],
            "settings": {
                "dark_mode": True,
                "reminder_days": 7,
                "autosave": True,
            },
        }

    def ensure_file(self) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write_payload(self.default_payload())

    def load_payload(self) -> dict[str, Any]:
        self.ensure_file()
        try:
            with self.file_path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except FileNotFoundError:
            payload = self.default_payload()
        except json.JSONDecodeError:
            self._backup_corrupted_file()
            payload = self.default_payload()
            self._write_payload(payload)
            return payload
        except TypeError:
            payload = self.default_payload()

        if not isinstance(payload, dict):
            return self.default_payload()

        merged = self.default_payload()
        merged.update(payload)
        if not isinstance(merged.get("tasks"), list):
            merged["tasks"] = []
        if not isinstance(merged.get("history"), list):
            merged["history"] = []
        if not isinstance(merged.get("settings"), dict):
            merged["settings"] = self.default_payload()["settings"]
        return merged

    def save_payload(self, payload: dict[str, Any]) -> None:
        self.ensure_file()
        self._write_payload(payload)

    def load_tasks(self) -> list[dict[str, Any]]:
        return list(self.load_payload().get("tasks", []))

    def load_history(self) -> list[dict[str, Any]]:
        return list(self.load_payload().get("history", []))

    def load_settings(self) -> dict[str, Any]:
        return dict(self.load_payload().get("settings", {}))

    def save_tasks(self, tasks: list[dict[str, Any]]) -> None:
        payload = self.load_payload()
        payload["tasks"] = list(tasks)
        self.save_payload(payload)

    def save_history(self, history: list[dict[str, Any]]) -> None:
        payload = self.load_payload()
        payload["history"] = list(history)
        self.save_payload(payload)

    def save_settings(self, settings: dict[str, Any]) -> None:
        payload = self.load_payload()
        payload["settings"] = dict(settings)
        self.save_payload(payload)

    def reset(self) -> None:
        self._write_payload(self.default_payload())

    def _write_payload(self, payload: dict[str, Any]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.file_path.with_suffix(self.file_path.suffix + ".tmp")
        with temp_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        temp_path.replace(self.file_path)

    def _backup_corrupted_file(self) -> None:
        if not self.file_path.exists():
            return
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = self.file_path.with_name(f"{self.file_path.stem}.corrupted-{timestamp}{self.file_path.suffix}")
        try:
            backup_path.write_bytes(self.file_path.read_bytes())
        except OSError:
            pass
