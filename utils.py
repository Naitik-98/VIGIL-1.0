from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

DATE_FORMAT: str = "%Y-%m-%d"
DISPLAY_DATE_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"


def normalize_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def generate_task_id(prefix: str = "VT") -> str:
    return f"{prefix}-{uuid4().hex[:12].upper()}"


def parse_date(value: object) -> date:
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise ValueError("Date must be provided as a date or YYYY-MM-DD string.")

    text = value.strip()
    if not text:
        raise ValueError("Date cannot be empty.")
    return datetime.strptime(text, DATE_FORMAT).date()


def format_date(value: date | str) -> str:
    if isinstance(value, date):
        return value.strftime(DATE_FORMAT)
    return parse_date(value).strftime(DATE_FORMAT)


def current_date() -> date:
    return date.today()


def current_timestamp() -> str:
    return datetime.now().strftime(DISPLAY_DATE_TIME_FORMAT)


def build_path(*parts: str) -> Path:
    return Path(*parts)
