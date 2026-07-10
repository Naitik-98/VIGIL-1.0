# VIGIL — System Health Suite

**Your PC's Silent Guardian**

A modern, professional desktop application for managing and monitoring PC maintenance tasks, system health tracking, and maintenance analytics.

---

##  Quick Start & Installation

### Requirements
- Python 3.10+
- tkinter (typically included with Python)
- psutil (for system metrics)
- 
umpy (for analytics)

### Installation
`ash
pip install psutil numpy
`

### Launch the Application
`ash
python main.py
`

---

##  Architecture & File Structure

VIGIL uses a clean layered architecture separating presentation (GUI), domain (business logic), and infrastructure (storage, metrics).

`	ext
VIGIL/
├── main.py                 # Application entry point
├── gui.py                  # Tkinter UI components and views
├── theme.py                # Color palette and font scheme
├── dashboard.py            # System monitoring (psutil)
├── analytics.py            # NumPy-based statistics engine
├── manager.py              # Core business logic (ProtectionManager)
├── models.py               # Domain model (MaintenanceTask)
├── persistence.py          # JSON persistence implementation
├── validator.py            # Input validation and rules
├── utils.py                # Shared utilities
└── data/
    └── maintenance.json    # Local data store (auto-created)
`

---

##  Data Management & Privacy

- **Storage Format:** All tasks and history are stored locally in plain text JSON at data/maintenance.json.
- **Autosave:** Automatically enabled by default. Every action instantly saves.
- **Error Recovery:** If maintenance.json gets corrupted, VIGIL detects it on startup, backs up the corrupted file to .corrupted-TIMESTAMP, and restores defaults to prevent application crashes.
- **Privacy:** 100% offline. No cloud sync, telemetry, or internet required.

---

##  Usage Guide

### Managing Maintenance Tasks
- **Add:** Go to **Protection Center** -> **+ Add Task**. Fill in the details.
- **Mark Complete:** Click **Mark Done** in the Protection Center or Reminder Center. It will update the last service date and log the action to the History.
- **History:** Check the **Protection History** tab for a chronological audit log of all creations, updates, and completions.

### Analytics & Insights
- **Compliance Rate:** See what percentage of your tasks are healthy.
- **Cost Tracking:** View total, average, and highest maintenance costs.
- **Reminders:** The **Reminders Center** intelligently sorts tasks by urgency (Overdue first, then Due Soon). By default, "Due Soon" is 7 days before the deadline (adjustable in Settings).

---

# VIGIL Development Roadmap

## VIGIL (Midterm Release)

**Status:** MVP
**Goal:** Meet all course requirements with a polished, professional desktop application.

---

## Phase 1 â€” Planning & Design

* [x] Finalize project scope
* [x] Create folder structure
* [x] Design application architecture
* [x] Design dark UI theme
* [x] Create logo (VIGIL)
* [x] Choose typography and color palette
* [x] Draw application wireframes
* [x] Create class diagram
* [x] Create flowchart

---

## Phase 2 â€” Core Backend

### Models

* [x] Create `MaintenanceTask` class
* [x] Create `ProtectionManager` class

### Validation

* [x] Empty input validation
* [x] Duplicate ID validation
* [x] Cost validation
* [x] Date validation
* [x] Component validation
* [x] Maintenance type validation

### File Handling

* [x] Create JSON storage
* [x] Auto-create JSON file
* [x] Save records
* [x] Load records
* [x] Handle corrupted JSON
* [x] Handle missing files

---

## Phase 3 â€” CRUD System

* [x] Add Protection Task
* [x] View Protection Tasks
* [x] Search Task
* [ ] Update Task
* [ ] Delete Task
* [x] Filter Tasks

---

## Phase 4 â€” Dashboard

Live Information

* [x] CPU Usage (%)
* [x] RAM Usage (%)
* [x] Disk Usage (%)
* [x] Free Disk Space
* [x] Current Date
* [x] Current Time
* [x] System Uptime

Protection Summary

* [x] Total Tasks
* [x] Healthy
* [x] Due Soon
* [x] Overdue

---

## Phase 5 â€” Analytics

Using NumPy

* [x] Average Maintenance Cost
* [x] Total Maintenance Cost
* [x] Highest Cost
* [x] Lowest Cost
* [ ] Tasks per Component
* [ ] Tasks per Maintenance Type
* [ ] Monthly Spending
* [x] Average Maintenance Interval

---

## Phase 6 â€” Reminder System

* [x] Due Soon detection
* [x] Overdue detection
* [x] Days Remaining calculation
* [x] Dashboard warning cards

---

## Phase 7 â€” GUI

* [x] Sidebar Navigation
* [x] Dashboard Page
* [x] Protection Center
* [x] Protection History
* [x] Analytics Page
* [x] Settings Page
* [ ] About Page

---

## Phase 8 â€” Settings

* [x] Dark Mode
* [x] Autosave
* [x] Reminder Days
* [x] Reset Application Data

---

## Phase 9 â€” Error Handling

* [x] Invalid Input
* [x] File Errors
* [x] JSON Errors
* [x] Duplicate Records
* [x] Invalid Dates
* [x] Invalid Costs

---

## Phase 10 â€” Polish

* [ ] Better Icons
* [ ] Better Table Styling
* [x] Loading Animation (Theme transition added)
* [x] Success/Error Messages
* [ ] Sample Data
* [ ] Final Testing
* [x] Dynamic Real-Time Stats Loop (New)
* [x] Dynamic Theme UI Animation (New)

---

# Deliverables (Midterm)

* [x] Source Code
* [x] JSON File
* [ ] Screenshots
* [ ] Project Report
* [ ] PPT
* [ ] Viva Preparation

---

# VIGIL 2.1 (Final Release)

**Status:** Professional Edition
**Goal:** Transform VIGIL into a real PC protection and monitoring suite.

---

## Hardware Monitoring

### CPU

* [ ] Temperature
* [ ] Usage
* [ ] Clock Speed
* [ ] Core Count

---

### GPU

* [ ] Temperature
* [ ] Usage
* [ ] VRAM Usage
* [ ] Fan Speed

---

### RAM

* [ ] Used Memory
* [ ] Free Memory
* [ ] Total Memory
* [ ] Memory Speed

---

### Storage

* [ ] SSD Temperature
* [ ] SSD Health
* [ ] SMART Status
* [ ] Read Speed
* [ ] Write Speed

---

### Motherboard

* [ ] BIOS Version
* [ ] Motherboard Model

---

## Live Dashboard

* [ ] Live Graphs
* [ ] Performance Charts
* [ ] Auto Refresh
* [ ] Resource Timeline

---

## Protection Engine

* [ ] Temperature Alerts
* [ ] High CPU Alert
* [ ] High GPU Alert
* [ ] Low Disk Space Alert
* [ ] Missed Maintenance Alert

---

## Maintenance Intelligence

* [ ] Predict next maintenance
* [ ] Automatic reminders
* [ ] Maintenance recommendations
* [ ] Maintenance calendar

---

## Reports

* [ ] Weekly Report
* [ ] Monthly Report
* [ ] PDF Export
* [ ] CSV Export

---

## Backup Center

* [ ] Backup reminders
* [ ] Backup history
* [ ] Restore points log

---

## Driver Center

* [ ] Installed driver list
* [ ] Driver update history
* [ ] Driver reminder

---

## System Information

* [ ] Windows Version
* [ ] CPU Name
* [ ] GPU Name
* [ ] RAM Details
* [ ] Motherboard Details
* [ ] Storage Devices

---

## Advanced Analytics

* [ ] Temperature History
* [ ] Usage Trends
* [ ] Maintenance Cost Trends
* [ ] Hardware Health Score
* [ ] Overall System Score

---

## User Experience

* [ ] Splash Screen
* [ ] Custom App Icon
* [ ] Notification Center
* [ ] Keyboard Shortcuts
* [ ] Search Everything
* [ ] Theme Customization

---

## Future Vision (VIGIL 3.0)

* [ ] Background Windows Service
* [ ] Auto-start with Windows
* [ ] Cloud Sync
* [ ] Multiple PC Profiles
* [ ] Mobile Companion App
* [ ] AI-based maintenance suggestions
* [ ] Plugin system
* [ ] Cross-platform support (Windows/Linux/macOS)

---

## Overall Vision

By the end of **VIGIL 2.1**, the application should feel closer to a lightweight combination of:

* **HWiNFO** (system information)
* **CrystalDiskInfo** (storage health)
* **MSI Afterburner** (performance monitoring)
* **CCleaner Health Check** (maintenance reminders)

while keeping the unique identity of **VIGIL** as a **System Health Suite** focused on preventive care rather than system tuning or overclocking. This gives you a clear progression from a rubric-compliant midterm project to a compelling final-term application.

