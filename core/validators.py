from __future__ import annotations

from datetime import date, datetime
from typing import Iterable

DATE_FORMAT: str = "%Y-%m-%d"
DEFAULT_CATEGORIES: tuple[str, ...] = (
    "Security",
    "Performance",
    "Backup",
    "Storage",
    "System",
    "Network",
)


def is_valid_task_name(name: str) -> bool:
    return isinstance(name, str) and bool(name.strip())


def is_valid_interval(interval_days: object) -> bool:
    return isinstance(interval_days, int) and interval_days > 0


def is_valid_date(value: object) -> bool:
    if isinstance(value, date):
        return True
    if not isinstance(value, str) or not value.strip():
        return False

    try:
        datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        return False
    return True


def parse_date(value: object) -> date:
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        raise ValueError("Date must be provided as a date or YYYY-MM-DD string.")
    return datetime.strptime(value.strip(), DATE_FORMAT).date()


def is_valid_category(category: str, allowed_categories: Iterable[str] | None = None) -> bool:
    allowed = tuple(allowed_categories or DEFAULT_CATEGORIES)
    return isinstance(category, str) and category.strip() in allowed
