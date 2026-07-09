# VIGIL — System Health Suite

**Your PC's Silent Guardian**

A modern, professional desktop application for managing and monitoring PC maintenance tasks, system health tracking, and maintenance analytics.

## Overview

VIGIL is a local-first desktop application built with Python and Tkinter that helps users maintain their PC through preventive maintenance management, live system monitoring, and data-driven analytics.

### Key Features

- **Dashboard**: Live CPU, RAM, disk usage, uptime, and maintenance summary at a glance
- **Protection Center**: Full CRUD operations for maintenance tasks with search and filtering
- **Protection History**: Chronological audit log of all maintenance actions
- **Analytics**: NumPy-based statistical analysis with compliance rates, cost tracking, and trends
- **Reminder Center**: Intelligent prioritization of due and overdue tasks
- **Settings**: Dark mode, reminder intervals, autosave, and data reset

## Requirements

- Python 3.10+
- tkinter (typically included with Python)
- psutil
- numpy

## Installation

```bash
pip install psutil numpy
```

## Project Structure

```
VIGIL/
├── main.py                 # Application entry point
├── gui.py                  # Tkinter UI components and views
├── theme.py                # Color palette and font scheme
├── dashboard.py            # System monitoring (psutil)
├── analytics.py            # NumPy-based statistics engine
├── manager.py              # Core business logic (ProtectionManager)
├── models.py               # Domain model (MaintenanceTask)
├── storage.py              # JSON persistence (JSONStorage)
├── validator.py            # Input validation and rules
├── utils.py                # Shared utilities
├── data/
│   └── maintenance.json    # Local data store
├── core/                   # (Legacy module for reference)
├── models/                 # (Legacy module for reference)
├── storage/                # (Legacy module for reference)
└── README.md               # This file
```

## Architecture

### Layered Design

The application follows a **layered architecture** to maintain clean separation of concerns:

1. **Presentation Layer** (`gui.py`, `theme.py`)
   - Tkinter-based UI
   - Views and widgets
   - Theme and styling

2. **Domain Layer** (`models.py`, `manager.py`)
   - `MaintenanceTask`: Encapsulates task data and status logic
   - `ProtectionManager`: Orchestrates CRUD, search, reminders, statistics

3. **Infrastructure Layer** (`storage.py`, `dashboard.py`, `analytics.py`)
   - `JSONStorage`: File persistence with corruption recovery
   - `SystemMonitor`: psutil integration for live metrics
   - `StatsEngine`: NumPy-based analytics

4. **Cross-Cutting** (`validator.py`, `utils.py`)
   - Input validation
   - Utility functions

### Data Flow

```
User Input (GUI)
	↓
Validator (input rules check)
	↓
Manager (business logic)
	↓
Storage (JSON persistence)
	↓
Analytics (NumPy statistics)
	↓
Display (updated UI)
```

## Usage

### Running the Application

```bash
python main.py
```

### Adding a Task

1. Navigate to **Protection Center**
2. Click **+ Add Task**
3. Fill in component, maintenance type, dates, cost, and notes
4. Submit

### Marking Tasks Complete

Click **Mark Done** in Protection Center or Reminder Center to update last service date and log to history.

### Viewing Statistics

Navigate to **Analytics** to see:
- Compliance rate (% of healthy tasks)
- Cost statistics (average, highest, lowest, total, median)
- Maintenance interval analysis
- Monthly spending trends
- Task distribution by component and type

### Configuring Settings

In **Settings**:
- **Dark Mode**: Toggle dark/light theme
- **Reminder Days**: Days before due date to show as "Due Soon" (default: 7)
- **Autosave**: Automatically save changes to JSON (default: on)
- **Reset Data**: Clear all tasks and history

## Data Model

### MaintenanceTask

```python
@dataclass(slots=True)
class MaintenanceTask:
	task_id: str                    # Unique identifier
	component: str                  # CPU, GPU, RAM, SSD, HDD, Motherboard, Cooling, PSU, OS, Network
	maintenance_type: str           # Dust Cleaning, Driver Update, Antivirus Scan, etc.
	last_service_date: date         # When was it last done?
	next_service_date: date         # When is it due next?
	cost: float                     # Maintenance cost (0+)
	status: str                     # Healthy | Due Soon | Overdue (computed)
	notes: str                      # Additional details
```

### Status Calculation

- **Healthy**: Next service date is more than `reminder_days` in the future
- **Due Soon**: Next service date is within `reminder_days` (default: 7 days)
- **Overdue**: Next service date has passed

## Assignment Demonstrations

The project clearly demonstrates:

✅ **Variables**: Task properties, UI state, configuration settings  
✅ **Operators**: Date arithmetic, comparisons, string formatting  
✅ **Branching**: Status calculation, search filters, view selection  
✅ **Loops**: Task iteration, history display, analytics aggregation  
✅ **Functions**: Validation, formatting, statistics calculation  
✅ **Lists**: Task collections, history records, search results  
✅ **Tuples**: Status states, components, maintenance types  
✅ **Dictionaries**: Task/history serialization, settings, statistics  
✅ **Sets**: Component validation, unique category tracking  
✅ **OOP**: MaintenanceTask class, ProtectionManager class, view hierarchy  
✅ **File Handling**: JSON load/save with error recovery  
✅ **Exception Handling**: ValueError, FileNotFoundError, JSONDecodeError  
✅ **Tkinter**: Full GUI with multiple views and interactive widgets  
✅ **NumPy**: Compliance rate, cost statistics, interval analysis  
✅ **psutil**: CPU, RAM, disk, and uptime monitoring  

## Storage Format

Tasks and history are stored in `data/maintenance.json`:

```json
{
  "tasks": [
	{
	  "task_id": "VT-abc123def456",
	  "component": "CPU",
	  "maintenance_type": "Thermal Paste Replacement",
	  "last_service_date": "2024-01-15",
	  "next_service_date": "2025-01-15",
	  "cost": 50.00,
	  "status": "Healthy",
	  "notes": "Applied new thermal compound"
	}
  ],
  "history": [
	{
	  "record_id": "vt-rec-001",
	  "action": "created",
	  "task_id": "VT-abc123def456",
	  "component": "CPU",
	  "maintenance_type": "Thermal Paste Replacement",
	  "status": "Healthy",
	  "cost": 50.00,
	  "timestamp": "2024-01-15 10:30:45"
	}
  ],
  "settings": {
	"dark_mode": true,
	"reminder_days": 7,
	"autosave": true
  }
}
```

## Error Handling

- **Missing files**: Automatically created with defaults
- **Corrupted JSON**: Backed up to `.corrupted-TIMESTAMP` and recreated
- **Invalid input**: Validated before persistence
- **Type mismatches**: Gracefully coerced or rejected
- **No crashes**: All exceptions caught and logged

## Future Enhancements

- GPU/CPU temperature sensors
- Email/SMS reminders
- Export reports (PDF, CSV)
- Task templates and presets
- Multi-device sync
- Web dashboard
- Mobile companion app

## License

MIT

---

**VIGIL** — Built as a professional-grade desktop application demonstrating clean architecture, comprehensive validation, and user-centric design principles.
