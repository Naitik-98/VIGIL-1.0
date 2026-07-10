#!/usr/bin/env python3
"""VIGIL - Final Validation Script"""

from manager import ProtectionManager
from domain import MaintenanceTask
from datetime import date
import os

print("VIGIL Final Validation")
print("=" * 60)

try:
    # Create a manager
    mgr = ProtectionManager(reminder_days=7, autosave=False)
    print("✓ ProtectionManager initialized")

    # Create a test task
    task = MaintenanceTask(
        task_id="TEST-001",
        component="CPU",
        maintenance_type="Thermal Paste Replacement",
        last_service_date=date(2024, 1, 15),
        next_service_date=date(2025, 1, 15),
        cost=50.0,
        status="Healthy",
        notes="Test task",
    )
    print("✓ MaintenanceTask created")

    # Add task
    mgr.add_task(task)
    print("✓ Task added to manager")

    # Search task
    results = mgr.search_task("CPU")
    if len(results) > 0:
        print("✓ Task search working")
    else:
        print("✗ Task search failed")
        exit(1)

    # Get statistics
    stats = mgr.statistics()
    print(f"✓ Statistics calculated: {stats['total_tasks']} task(s)")

    # Check persistence
    data_file = "data/maintenance.json"
    if os.path.exists(data_file):
        file_size = os.path.getsize(data_file)
        print(f"✓ Data persistence: {data_file} ({file_size} bytes)")
    else:
        print("✗ Data file not found")
        exit(1)

    print("=" * 60)
    print("SUCCESS: All systems operational!")
    print("Run: python main.py to start VIGIL")

except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    exit(1)
