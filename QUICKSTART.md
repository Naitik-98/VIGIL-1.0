# VIGIL Quick Start Guide

## Installation & Setup

### Step 1: Verify Python Version

```bash
python --version
# Required: Python 3.10+
```

### Step 2: Install Dependencies (Optional)

For full functionality with live system metrics and NumPy analytics:

```bash
pip install psutil numpy
```

**Note**: VIGIL runs without these libraries using graceful fallbacks.

### Step 3: Launch the Application

```bash
python main.py
```

The GUI will open with a dark theme and sidebar navigation.

---

## First Time Usage

### Dashboard
- View live CPU, RAM, disk, and uptime metrics
- See maintenance summary (Healthy / Due Soon / Overdue counts)

### Protection Center
- Click **+ Add Task** to create your first maintenance item
- Select component (CPU, GPU, RAM, SSD, HDD, etc.)
- Choose maintenance type (Driver Update, Antivirus Scan, Backup, etc.)
- Set last service date and interval (days until next service)
- Enter cost and optional notes
- Submit

### Reminders Center
- View tasks due in the next 7 days
- View overdue tasks (red alert)
- Filter by status

### Analytics
- Compliance rate (% of on-time maintenance)
- Cost statistics and trends
- Task distribution by component

### Settings
- Dark mode (default: on)
- Reminder days (default: 7 days before due)
- Autosave toggle (default: on)

---

## File Structure

```
VIGIL/
├── main.py                      # Entry point
├── gui.py                       # UI & views (1000+ lines)
├── manager.py                   # Business logic
├── models.py                    # Domain model
├── storage.py                   # JSON persistence
├── validator.py                 # Input validation
├── theme.py                     # Colors & fonts
├── dashboard.py                 # System monitoring
├── analytics.py                 # Statistics
├── utils.py                     # Helpers
├── data/
│   └── maintenance.json         # Local data store
├── README.md                    # Full documentation
└── IMPLEMENTATION_SUMMARY.md    # Technical details
```

---

## Common Tasks

### Add a Maintenance Task

1. Open **Protection Center**
2. Click **+ Add Task**
3. Fill in the details
4. Click **Submit**

### Mark a Task Complete

1. Open **Reminder Center** or **Protection Center**
2. Select the task
3. Click **Mark Done**
4. Last service date updates automatically

### View Maintenance History

1. Open **Protection Center History**
2. Scroll through chronological audit log
3. See action type, component, and timestamp

### Export Data

Your data is automatically saved to `data/maintenance.json`. You can:
- Backup the file manually
- Edit it directly (JSON format)
- Copy to another machine

### Reset All Data

1. Open **Settings**
2. Click **Reset All Data**
3. Confirm the warning
4. All tasks and history will be cleared

---

## Tips & Tricks

### Dark Mode Works Great
- Default is dark mode (easier on eyes)
- Toggle in Settings if needed

### Reminder Days Are Customizable
- Default: 7 days
- Set to 14+ for less frequent reminders
- Set to 1-3 for early warnings

### Data Persists Automatically
- Autosave is enabled by default
- Every change saves to `data/maintenance.json`
- Turn off in Settings if you prefer manual saves

### Keyboard Shortcuts
- **Tab**: Move between fields
- **Enter**: Submit forms
- **Esc**: Close dialogs

### Lost Your Data?
- Check `data/maintenance.json`
- If corrupted, VIGIL backs it up to `.corrupted-TIMESTAMP`
- Data resets to defaults; old backup preserved

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'psutil'"
- **Solution**: `pip install psutil` (optional; app still runs with demo data)

### "ModuleNotFoundError: No module named 'numpy'"
- **Solution**: `pip install numpy` (optional; analytics uses pure Python fallbacks)

### GUI doesn't start
- **Check**: Python version is 3.10+
- **Check**: tkinter is available (usually built-in)
- **Try**: `python -m tkinter` to verify tkinter

### Tasks don't save
- **Check**: `data/` directory exists and is writable
- **Check**: Autosave is enabled in Settings
- **Try**: Manually click **Save** after changes

### Can't add components or maintenance types
- Components & types are fixed (10 each)
- See README.md for full list
- Contact developer for custom types

---

## Performance Notes

- Handles 100+ tasks smoothly
- Dashboard refresh: ~1 second (psutil call)
- JSON saves: <100ms typical
- Memory: ~50-100 MB typical

---

## Data Privacy

- **No cloud sync**: All data stays local
- **No telemetry**: No usage tracking
- **No internet required**: Fully offline
- **Encrypted?**: No (JSON is plain text; store `data/` securely)

---

## Next Steps

1. Add your first maintenance task
2. Review the Dashboard
3. Check Analytics for insights
4. Set Reminder Days to suit your workflow
5. Back up `data/maintenance.json` regularly

---

**Need Help?** See `README.md` for full documentation.

---

**VIGIL 1.0** — Your PC's Silent Guardian ✨
