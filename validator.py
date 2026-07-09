from __future__ import annotations

from datetime import date
from typing import Iterable

from utils import parse_date, normalize_text

COMPONENTS: tuple[str, ...] = (
    "CPU",
    "GPU",
    "RAM",
    "SSD",
    "HDD",
    "Motherboard",
    "Cooling",
    "PSU",
    "Operating System",
    "Network",
)

MAINTENANCE_TYPES: tuple[str, ...] = (
    "Dust Cleaning",
    "Thermal Paste Replacement",
    "Driver Update",
    "Windows Update",
    "SSD Health Check",
    "Antivirus Scan",
    "Backup",
    "Fan Cleaning",
    "BIOS Update",
    "General Inspection",
)

STATUS_STATES: tuple[str, ...] = ("Healthy", "Due Soon", "Overdue")
COMPONENT_SET: set[str] = set(COMPONENTS)
MAINTENANCE_TYPE_SET: set[str] = set(MAINTENANCE_TYPES)
STATUS_SET: set[str] = set(STATUS_STATES)


def validate_required_text(value: object, field_name: str) -> str:
    text = normalize_text(value)
    if not text:
        raise ValueError(f"{field_name} cannot be empty.")
    return text


def validate_component(component: object, allowed: Iterable[str] | None = None) -> str:
    text = validate_required_text(component, "Component")
    options = set(allowed or COMPONENT_SET)
    if text not in options:
        raise ValueError("Invalid component.")
    return text


def validate_maintenance_type(maintenance_type: object, allowed: Iterable[str] | None = None) -> str:
    text = validate_required_text(maintenance_type, "Maintenance type")
    options = set(allowed or MAINTENANCE_TYPE_SET)
    if text not in options:
        raise ValueError("Invalid maintenance type.")
    return text


def validate_status(status: object, allowed: Iterable[str] | None = None) -> str:
    text = validate_required_text(status, "Status")
    options = set(allowed or STATUS_SET)
    if text not in options:
        raise ValueError("Invalid status.")
    return text


def validate_cost(cost: object) -> float:
    if isinstance(cost, bool):
        raise ValueError("Cost must be a numeric value.")
    try:
        amount = float(cost)
    except (TypeError, ValueError) as exc:
        raise ValueError("Cost must be a numeric value.") from exc
    if amount < 0:
        raise ValueError("Cost cannot be negative.")
    return round(amount, 2)


def validate_date(value: object, field_name: str) -> date:
    try:
        return parse_date(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a valid date in YYYY-MM-DD format.") from exc


def validate_task_id(task_id: object) -> str:
    return validate_required_text(task_id, "Task ID")
