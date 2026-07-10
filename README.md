<div align="center">

#  VIGIL
### *Your PC's Silent Guardian*

**A modern desktop application for PC maintenance management, live system monitoring, and data-driven analytics.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green?style=for-the-badge)
![psutil](https://img.shields.io/badge/Monitoring-psutil-orange?style=for-the-badge)
![NumPy](https://img.shields.io/badge/Analytics-NumPy-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-lightgrey?style=for-the-badge)

</div>


Download for here(https://github.com/Naitik-98/VIGIL/releases/download/v0.0.2/main.exe)
---

## 📖 Overview

VIGIL is a **local-first desktop application** built with Python and Tkinter that helps you maintain your PC through:

-  **Live system monitoring** — Real-time CPU, RAM, and Disk stats (like Task Manager)
-  **Preventive maintenance tracking** — Schedule and manage all your PC maintenance tasks
-  **Data-driven analytics** — NumPy-powered cost and compliance statistics
-  **Smart reminders** — Get alerted when tasks are due or overdue
-  **Beautiful dark/light UI** — Smooth animated theme transitions

---

##  Features

| Feature | Description |
|---|---|
| **Dashboard** | Live CPU, RAM, Disk usage, uptime, date/time — auto-updates every second |
| **Protection Center** | Full CRUD — Add, View, Search, and Filter maintenance tasks |
| **History** | Chronological audit log of all maintenance actions |
| **Analytics** | Compliance rate, cost stats (avg/high/low/total), task distribution |
| **Reminder Center** | Due soon & overdue tasks sorted by urgency |
| **Settings** | Dark mode, reminder days, autosave, data reset |
| **Theme Toggle** | ☀️/🌙 button with animated circular transition |

---

## 🚀 Quick Start

### 1. Requirements

- Python **3.10+**
- `tkinter` *(comes built-in with Python)*

### 2. Install Dependencies

```bash
pip install psutil numpy
```

> **Note:** VIGIL still runs without these — it just uses fallback values. Install both for full live stats and analytics.

### 3. Run the App

```bash
python main.py
```

---

##  Project Structure

```
VIGIL/
├── main.py            # Entry point
├── gui.py             # All UI views and components
├── theme.py           # Color palettes and font scheme
├── dashboard.py       # Live system metrics (psutil)
├── analytics.py       # NumPy statistics engine
├── manager.py         # Core business logic (ProtectionManager)
├── domain.py          # MaintenanceTask data model
├── persistence.py     # JSON file storage
├── validator.py       # Input validation rules
├── utils.py           # Shared utilities
├── data/
│   └── maintenance.json   # Auto-created local data store
├── media/
│   └── *.png              # Logo and assets
└── VIGIL_ROADMAP.md       # Development roadmap & checklist
```

---

##  Architecture

VIGIL follows a clean **layered architecture**:

```
┌─────────────────────────────────┐
│   Presentation Layer            │
│   gui.py · theme.py             │
├─────────────────────────────────┤
│   Domain Layer                  │
│   manager.py · domain.py        │
├─────────────────────────────────┤
│   Infrastructure Layer          │
│   persistence.py · dashboard.py │
│   analytics.py                  │
├─────────────────────────────────┤
│   Cross-Cutting                 │
│   validator.py · utils.py       │
└─────────────────────────────────┘
```

**Data Flow:**
```
User Input → Validator → Manager → Persistence → Analytics → UI
```

---

##  Data Model

Each maintenance task stores:

| Field | Type | Description |
|---|---|---|
| `task_id` | `str` | Auto-generated unique ID |
| `component` | `str` | CPU, GPU, RAM, SSD, HDD, etc. |
| `maintenance_type` | `str` | Dust Cleaning, Driver Update, etc. |
| `last_service_date` | `date` | When it was last done |
| `next_service_date` | `date` | When it is due next |
| `cost` | `float` | Maintenance cost (0+) |
| `status` | `str` | Healthy / Due Soon / Overdue |
| `notes` | `str` | Optional extra details |

**Status Logic:**
- 🟢 **Healthy** — Due date is more than `reminder_days` away
- 🟠 **Due Soon** — Due within `reminder_days` (default: 7 days)
- 🔴 **Overdue** — Due date has already passed

---

##  Storage

All data is saved to `data/maintenance.json` locally:

```json
{
  "tasks": [...],
  "history": [...],
  "settings": {
    "dark_mode": true,
    "reminder_days": 7,
    "autosave": true
  }
}
```

- **Auto-created** if missing
- **Backup & recovery** if corrupted (saved as `.corrupted-TIMESTAMP`)
- **No cloud sync** — your data stays on your machine

---

## 🔧 Usage Tips

- **Add a task:** Protection Center → `+ Add Task`
- **Mark complete:** Select task → `Mark Done` (updates last service date)
- **Toggle theme:** Click ☀️/🌙 button in the top-right corner
- **Change reminder window:** Settings → Reminder Days slider
- **Backup your data:** Copy `data/maintenance.json` to a safe location

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: psutil` | Run `pip install psutil` |
| `ModuleNotFoundError: numpy` | Run `pip install numpy` |
| GUI doesn't open | Run `python -m tkinter` to verify Tkinter works |
| Stats show static values | Ensure `psutil` is installed and restart the app |
| Data not saving | Check that `data/` folder is writable |
| `command not found` error in editor | Run `python main.py` directly in the terminal |

---

##  Roadmap

See **[VIGIL_ROADMAP.md](VIGIL_ROADMAP.md)** for the full development checklist covering VIGIL (MVP) through VIGIL 2.1 (Professional Edition) and the VIGIL 3.0 future vision.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**VIGIL** — Built with ❤️ as a professional-grade desktop application.

*Clean architecture · Comprehensive validation · User-centric design*

</div>
