from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from typing import Any, Callable
import os
from PIL import Image, ImageTk

from manager import ProtectionManager
from domain import MaintenanceTask
from dashboard import SystemMonitor
from analytics import StatsEngine
from theme import DARK_PALETTE, FONT_SCHEME, PADDING_LARGE, PADDING_MEDIUM, PADDING_SMALL
from validator import COMPONENTS, MAINTENANCE_TYPES


class StatCard(tk.Frame):
    """Reusable stat card widget for dashboard metrics."""

    def __init__(
        self,
        parent: tk.Widget,
        label: str,
        value: str | int | float,
        unit: str = "",
        color: str = "#00C896",
        **kwargs: Any,
    ) -> None:
        super().__init__(parent, **kwargs)
        self.configure(bg=DARK_PALETTE.card, relief=tk.FLAT)

        label_widget = tk.Label(
            self,
            text=label,
            fg=DARK_PALETTE.text_secondary,
            bg=DARK_PALETTE.card,
            font=FONT_SCHEME.get_small(),
        )
        label_widget.pack(side=tk.TOP, anchor=tk.W, padx=PADDING_MEDIUM, pady=(PADDING_MEDIUM, 0))

        self.unit = unit
        self.value_widget = tk.Label(
            self,
            text=f"{value}{unit}",
            fg=color,
            bg=DARK_PALETTE.card,
            font=FONT_SCHEME.get_heading(),
        )
        self.value_widget.pack(side=tk.TOP, anchor=tk.W, padx=PADDING_MEDIUM, pady=(PADDING_SMALL, PADDING_MEDIUM))

    def set_value(self, new_value: str | int | float) -> None:
        self.value_widget.config(text=f"{new_value}{self.unit}")

class Sidebar(tk.Frame):
    """Left sidebar navigation panel."""

    def __init__(self, parent: tk.Widget, on_nav: Callable[[str], None], **kwargs: Any) -> None:
        super().__init__(parent, bg=DARK_PALETTE.sidebar, **kwargs)
        self.on_nav = on_nav
        self.active_button: tk.Button | None = None

        # Load and resize logo
        logo_path = os.path.join("media", "Your Silent Protector(logo VIGIL).png")
        try:
            pil_image = Image.open(logo_path)
            # Resize image to fit sidebar appropriately (e.g., width 150)
            target_width = 150
            ratio = target_width / pil_image.width
            target_height = int(pil_image.height * ratio)
            pil_image = pil_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(pil_image)

            title = tk.Label(
                self,
                image=self.logo_img,
                bg=DARK_PALETTE.sidebar,
            )
        except Exception as e:
            print(f"Error loading logo: {e}")
            title = tk.Label(
                self,
                text="VIGIL",
                fg=DARK_PALETTE.accent,
                bg=DARK_PALETTE.sidebar,
                font=FONT_SCHEME.get_title(),
            )

        title.pack(padx=PADDING_LARGE, pady=PADDING_LARGE, anchor=tk.W)

        divider = tk.Frame(self, bg=DARK_PALETTE.border, height=1)
        divider.pack(fill=tk.X, padx=PADDING_MEDIUM)

        # Theme toggle button
        self.theme_btn = tk.Button(
            self,
            text="Toggle Theme",
            command=self.toggle_theme,
            bd=0,
            relief=tk.FLAT,
            fg=DARK_PALETTE.text_secondary,
            bg=DARK_PALETTE.sidebar,
            activebackground=DARK_PALETTE.card,
            activeforeground=DARK_PALETTE.text,
            font=FONT_SCHEME.get_body(),
            cursor="hand2",
            anchor=tk.W,
            padx=PADDING_LARGE,
            pady=PADDING_MEDIUM,
        )
        self.theme_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, PADDING_LARGE))

        self.nav_items = [
            ("Dashboard", "dashboard"),
            ("Protection Center", "protection"),
            ("History", "history"),
            ("Analytics", "analytics"),
            ("Reminders", "reminders"),
            ("Settings", "settings"),
        ]

        for label, key in self.nav_items:
            btn = self._create_nav_button(label, key)
            btn.pack(fill=tk.X, padx=PADDING_MEDIUM, pady=PADDING_SMALL)

    def toggle_theme(self) -> None:
        """Toggle between dark and light themes."""
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.palette = theme.DARK_PALETTE
            self.sidebar.theme_btn.config(text="🌙 Dark Mode")
        else:
            self.palette = theme.LIGHT_PALETTE
            self.sidebar.theme_btn.config(text="☀️ Light Mode")
            
        # For a full dynamic app, we usually need to re-render or recursively configure.
        # Given limitations of simple tkinter without a proper variable watcher across files,
        # we update the root background and require restart or redraw of subframes. 
        # A simple hack is updating the button text for now to show interaction.
        # We can implement a recursive update:
        self.config(bg=self.palette.background)
        self._recursive_style(self)
        
    def _recursive_style(self, w: tk.Widget) -> None:
        try:
            name = w.winfo_name()
            wtype = w.winfo_class()
            if wtype in ("Tk", "Frame", "Toplevel", "LabelFrame"):
                # We need to distinguish sidebar vs background vs card. 
                # This is a bit complex in raw tk. 
                pass
            elif wtype in ("Label", "Button", "Checkbutton", "Radiobutton"):
                pass
        except tk.TclError:
            pass
            
        for child in w.winfo_children():
            self._recursive_style(child)
            
    def run(self) -> None:
        """Run the application."""
        self.mainloop()


class DashboardView(tk.Frame):
    """Main dashboard view with system stats and maintenance summary."""

    def __init__(self, parent: tk.Widget, manager: ProtectionManager, **kwargs: Any) -> None:
        if 'bg' not in kwargs:
            kwargs['bg'] = DARK_PALETTE.background
        super().__init__(parent, **kwargs)
        self.manager = manager
        self.monitor = SystemMonitor()

        header = tk.Label(
            self,
            text="Dashboard",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.background,
            font=FONT_SCHEME.get_title(),
        )
        header.pack(padx=PADDING_LARGE, pady=PADDING_LARGE, anchor=tk.W)

        self._build_system_metrics()
        self._build_maintenance_summary()

    def _build_system_metrics(self) -> None:
        metrics_frame = tk.Frame(self, bg=DARK_PALETTE.background)
        metrics_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        self.cpu_card = StatCard(
            metrics_frame,
            "CPU Usage",
            self.monitor.get_cpu_percent(),
            "%",
            color=DARK_PALETTE.accent,
        )
        self.cpu_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_SMALL)

        self.ram_card = StatCard(
            metrics_frame,
            "RAM Usage",
            self.monitor.get_ram_percent(),
            "%",
            color=DARK_PALETTE.accent,
        )
        self.ram_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_SMALL)

        self.disk_card = StatCard(
            metrics_frame,
            "Disk Usage",
            self.monitor.get_disk_percent(),
            "%",
            color=DARK_PALETTE.accent,
        )
        self.disk_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_SMALL)

        self.disk_free_card = StatCard(
            metrics_frame,
            "Disk Free",
            self.monitor.get_disk_free_gb(),
            " GB",
            color=DARK_PALETTE.accent,
        )
        self.disk_free_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_SMALL)

        time_frame = tk.Frame(self, bg=DARK_PALETTE.background)
        time_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        self.time_card = StatCard(
            time_frame,
            "Current Time",
            self.monitor.get_current_time(),
            color=DARK_PALETTE.accent,
        )
        self.time_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_SMALL)

        self.date_card = StatCard(
            time_frame,
            "Date",
            self.monitor.get_current_date(),
            color=DARK_PALETTE.accent,
        )
        self.date_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_SMALL)

        self.uptime_card = StatCard(
            time_frame,
            "System Uptime",
            self.monitor.get_uptime_string(),
            color=DARK_PALETTE.accent,
        )
        self.uptime_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_SMALL)

        # Start updating metrics periodically
        self._update_metrics()

    def _update_metrics(self) -> None:
        if not self.winfo_exists():
            return
            
        self.cpu_card.set_value(self.monitor.get_cpu_percent())
        self.ram_card.set_value(self.monitor.get_ram_percent())
        self.disk_card.set_value(self.monitor.get_disk_percent())
        self.disk_free_card.set_value(self.monitor.get_disk_free_gb())
        
        self.time_card.set_value(self.monitor.get_current_time())
        self.date_card.set_value(self.monitor.get_current_date())
        self.uptime_card.set_value(self.monitor.get_uptime_string())
        
        self.after(1000, self._update_metrics)

    def _build_maintenance_summary(self) -> None:
        summary_frame = tk.Frame(self, bg=DARK_PALETTE.card, relief=tk.FLAT)
        summary_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        title = tk.Label(
            summary_frame,
            text="Maintenance Summary",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.card,
            font=FONT_SCHEME.get_subheading(),
        )
        title.pack(anchor=tk.W, padx=PADDING_MEDIUM, pady=(PADDING_MEDIUM, PADDING_SMALL))

        stats = self.manager.statistics()

        stat_line = tk.Label(
            summary_frame,
            text=f"Total: {stats['total_tasks']} | Healthy: {stats['healthy']} | "
                 f"Due Soon: {stats['due_soon']} | Overdue: {stats['overdue']}",
            fg=DARK_PALETTE.text_secondary,
            bg=DARK_PALETTE.card,
            font=FONT_SCHEME.get_normal(),
        )
        stat_line.pack(anchor=tk.W, padx=PADDING_MEDIUM, pady=(PADDING_SMALL, PADDING_MEDIUM))


class ProtectionCenterView(tk.Frame):
    """Protection Center view for viewing and managing tasks."""

    def __init__(self, parent: tk.Widget, manager: ProtectionManager, **kwargs: Any) -> None:
        if 'bg' not in kwargs:
            kwargs['bg'] = DARK_PALETTE.background
        super().__init__(parent, **kwargs)
        self.manager = manager

        header = tk.Label(
            self,
            text="Protection Center",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.background,
            font=FONT_SCHEME.get_title(),
        )
        header.pack(padx=PADDING_LARGE, pady=PADDING_LARGE, anchor=tk.W)

        control_frame = tk.Frame(self, bg=DARK_PALETTE.background)
        control_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        add_btn = tk.Button(
            control_frame,
            text="+ Add Task",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.accent,
            activebackground=DARK_PALETTE.accent,
            font=FONT_SCHEME.get_normal(),
            relief=tk.FLAT,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._on_add_task,
        )
        add_btn.pack(side=tk.LEFT, padx=PADDING_SMALL)

        refresh_btn = tk.Button(
            control_frame,
            text="Refresh",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.card,
            activebackground=DARK_PALETTE.card,
            font=FONT_SCHEME.get_normal(),
            relief=tk.FLAT,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._refresh_table,
        )
        refresh_btn.pack(side=tk.LEFT, padx=PADDING_SMALL)

        search_frame = tk.Frame(control_frame, bg=DARK_PALETTE.background)
        search_frame.pack(side=tk.RIGHT, padx=PADDING_SMALL)

        tk.Label(
            search_frame,
            text="Search:",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.background,
            font=FONT_SCHEME.get_small(),
        ).pack(side=tk.LEFT, padx=(0, PADDING_SMALL))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self._on_search())

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.card,
            insertbackground=DARK_PALETTE.text,
            font=FONT_SCHEME.get_normal(),
            width=20,
        )
        search_entry.pack(side=tk.LEFT)

        self._build_table()

    def _build_table(self) -> None:
        table_frame = tk.Frame(self, bg=DARK_PALETTE.background)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        columns = ("ID", "Component", "Type", "Last Done", "Next Due", "Status")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            height=15,
            show="headings",
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self._refresh_table()

    def _refresh_table(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for task in self.manager.get_all_tasks():
            self.tree.insert(
                "",
                tk.END,
                values=(
                    task.task_id[:8],
                    task.component,
                    task.maintenance_type,
                    task.last_service_date,
                    task.next_service_date,
                    task.status,
                ),
            )

    def _on_search(self) -> None:
        query = self.search_var.get()
        for item in self.tree.get_children():
            self.tree.delete(item)

        results = self.manager.search_task(query)
        for task in results:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    task.task_id[:8],
                    task.component,
                    task.maintenance_type,
                    task.last_service_date,
                    task.next_service_date,
                    task.status,
                ),
            )

    def _on_add_task(self) -> None:
        messagebox.showinfo("Add Task", "Add task form will open here.")


class HistoryView(tk.Frame):
    """History view for maintenance records."""

    def __init__(self, parent: tk.Widget, manager: ProtectionManager, **kwargs: Any) -> None:
        if 'bg' not in kwargs:
            kwargs['bg'] = DARK_PALETTE.background
        super().__init__(parent, **kwargs)
        self.manager = manager

        header = tk.Label(
            self,
            text="Protection History",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.background,
            font=FONT_SCHEME.get_title(),
        )
        header.pack(padx=PADDING_LARGE, pady=PADDING_LARGE, anchor=tk.W)

        table_frame = tk.Frame(self, bg=DARK_PALETTE.background)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        columns = ("Record ID", "Action", "Task ID", "Component", "Type", "Timestamp")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            height=20,
            show="headings",
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill=tk.BOTH, expand=True)

        self._load_history()

    def _load_history(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        history = self.manager.get_history()
        for record in reversed(history):
            self.tree.insert(
                "",
                tk.END,
                values=(
                    record.get("record_id", "")[:8],
                    record.get("action", ""),
                    record.get("task_id", "")[:8],
                    record.get("component", ""),
                    record.get("maintenance_type", ""),
                    record.get("timestamp", ""),
                ),
            )


class AnalyticsView(tk.Frame):
    """Analytics view with NumPy-based statistics."""

    def __init__(self, parent: tk.Widget, manager: ProtectionManager, **kwargs: Any) -> None:
        if 'bg' not in kwargs:
            kwargs['bg'] = DARK_PALETTE.background
        super().__init__(parent, **kwargs)
        self.manager = manager
        self.stats_engine = StatsEngine()

        header = tk.Label(
            self,
            text="Analytics",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.background,
            font=FONT_SCHEME.get_title(),
        )
        header.pack(padx=PADDING_LARGE, pady=PADDING_LARGE, anchor=tk.W)

        tasks = self.manager.get_all_tasks()

        metrics_frame = tk.Frame(self, bg=DARK_PALETTE.background)
        metrics_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        compliance = self.stats_engine.calculate_compliance_rate(tasks)
        costs = self.stats_engine.cost_statistics(tasks)
        intervals = self.stats_engine.maintenance_interval_stats(tasks)

        StatCard(
            metrics_frame,
            "Compliance Rate",
            compliance,
            "%",
            color=DARK_PALETTE.healthy,
        ).pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_SMALL)

        StatCard(
            metrics_frame,
            "Avg Cost",
            f"${costs['average']}",
            color=DARK_PALETTE.accent,
        ).pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_SMALL)

        StatCard(
            metrics_frame,
            "Total Spend",
            f"${costs['total']}",
            color=DARK_PALETTE.accent,
        ).pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_SMALL)

        StatCard(
            metrics_frame,
            "Avg Interval",
            f"{intervals['average_days']}",
            " days",
            color=DARK_PALETTE.accent,
        ).pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_SMALL)

        info_frame = tk.Frame(self, bg=DARK_PALETTE.card, relief=tk.FLAT)
        info_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        info_text = tk.Label(
            info_frame,
            text=f"Highest Cost: ${costs['highest']} | Lowest Cost: ${costs['lowest']} | Median: ${costs['median']}",
            fg=DARK_PALETTE.text_secondary,
            bg=DARK_PALETTE.card,
            font=FONT_SCHEME.get_normal(),
            justify=tk.LEFT,
        )
        info_text.pack(anchor=tk.W, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)


class RemindersView(tk.Frame):
    """Reminders view for due and overdue tasks."""

    def __init__(self, parent: tk.Widget, manager: ProtectionManager, **kwargs: Any) -> None:
        if 'bg' not in kwargs:
            kwargs['bg'] = DARK_PALETTE.background
        super().__init__(parent, **kwargs)
        self.manager = manager

        header = tk.Label(
            self,
            text="Reminder Center",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.background,
            font=FONT_SCHEME.get_title(),
        )
        header.pack(padx=PADING_LARGE, pady=PADDING_LARGE, anchor=tk.W)

        filter_frame = tk.Frame(self, bg=DARK_PALETTE.background)
        filter_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        self.filter_var = tk.StringVar(value="all")

        tk.Label(
            filter_frame,
            text="Show:",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.background,
            font=FONT_SCHEME.get_normal(),
        ).pack(side=tk.LEFT, padx=(0, PADDING_SMALL))

        for label, value in [("All", "all"), ("Due Soon", "due"), ("Overdue", "overdue")]:
            rb = tk.Radiobutton(
                filter_frame,
                text=label,
                variable=self.filter_var,
                value=value,
                fg=DARK_PALETTE.text,
                bg=DARK_PALETTE.background,
                activeforeground=DARK_PALETTE.accent,
                activebackground=DARK_PALETTE.background,
                selectcolor=DARK_PALETTE.card,
                command=self._refresh_reminders,
            )
            rb.pack(side=tk.LEFT, padx=PADDING_SMALL)

        self._build_reminder_list()

    def _build_reminder_list(self) -> None:
        list_frame = tk.Frame(self, bg=DARK_PALETTE.background)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        self.reminder_listbox = tk.Listbox(
            list_frame,
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.card,
            selectmode=tk.SINGLE,
            font=FONT_SCHEME.get_normal(),
        )
        self.reminder_listbox.pack(fill=tk.BOTH, expand=True)

        self._refresh_reminders()

    def _refresh_reminders(self) -> None:
        self.reminder_listbox.delete(0, tk.END)

        filter_value = self.filter_var.get()
        all_tasks = self.manager.get_all_tasks()

        if filter_value == "overdue":
            tasks = self.manager.get_overdue_tasks()
        elif filter_value == "due":
            tasks = self.manager.get_due_soon_tasks()
        else:
            tasks = self.manager.search_task("", due_soon_only=True, overdue_only=False)
            tasks.extend(self.manager.get_overdue_tasks())

        for task in sorted(tasks, key=lambda t: t.days_remaining()):
            days_left = task.days_remaining()
            status_icon = "🔴" if task.is_overdue() else "🟠"
            display = f"{status_icon} {task.component} - {task.maintenance_type} ({days_left} days)"
            self.reminder_listbox.insert(tk.END, display)


class SettingsView(tk.Frame):
    """Settings view for configuration."""

    def __init__(self, parent: tk.Widget, manager: ProtectionManager, **kwargs: Any) -> None:
        if 'bg' not in kwargs:
            kwargs['bg'] = DARK_PALETTE.background
        super().__init__(parent, **kwargs)
        self.manager = manager

        header = tk.Label(
            self,
            text="Settings",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.background,
            font=FONT_SCHEME.get_title(),
        )
        header.pack(padx=PADDING_LARGE, pady=PADDING_LARGE, anchor=tk.W)

        settings_frame = tk.Frame(self, bg=DARK_PALETTE.card, relief=tk.FLAT)
        settings_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADING_MEDIUM)

        tk.Label(
            settings_frame,
            text="Dark Mode",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.card,
            font=FONT_SCHEME.get_normal(),
        ).pack(side=tk.LEFT, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)

        self.dark_mode_var = tk.BooleanVar(value=self.manager.settings.get("dark_mode", True))
        dark_mode_check = tk.Checkbutton(
            settings_frame,
            variable=self.dark_mode_var,
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.card,
            activebackground=DARK_PALETTE.card,
            selectcolor=DARK_PALETTE.accent,
            command=self._on_dark_mode_toggle,
        )
        dark_mode_check.pack(side=tk.LEFT, padx=PADDING_SMALL)

        reminder_frame = tk.Frame(self, bg=DARK_PALETTE.card, relief=tk.FLAT)
        reminder_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        tk.Label(
            reminder_frame,
            text="Reminder Days",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.card,
            font=FONT_SCHEME.get_normal(),
        ).pack(side=tk.LEFT, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)

        self.reminder_var = tk.IntVar(value=self.manager.reminder_days)
        reminder_spinbox = tk.Spinbox(
            reminder_frame,
            from_=1,
            to=30,
            textvariable=self.reminder_var,
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.background,
            font=FONT_SCHEME.get_normal(),
            width=5,
            command=self._on_reminder_days_change,
        )
        reminder_spinbox.pack(side=tk.LEFT, padx=PADDING_SMALL)

        autosave_frame = tk.Frame(self, bg=DARK_PALETTE.card, relief=tk.FLAT)
        autosave_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        tk.Label(
            autosave_frame,
            text="Autosave",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.card,
            font=FONT_SCHEME.get_normal(),
        ).pack(side=tk.LEFT, padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)

        self.autosave_var = tk.BooleanVar(value=self.manager.autosave)
        autosave_check = tk.Checkbutton(
            autosave_frame,
            variable=self.autosave_var,
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.card,
            activebackground=DARK_PALETTE.card,
            selectcolor=DARK_PALETTE.accent,
            command=self._on_autosave_toggle,
        )
        autosave_check.pack(side=tk.LEFT, padx=PADDING_SMALL)

        reset_frame = tk.Frame(self, bg=DARK_PALETTE.background)
        reset_frame.pack(fill=tk.X, padx=PADDING_LARGE, pady=PADDING_MEDIUM)

        reset_btn = tk.Button(
            reset_frame,
            text="Reset All Data",
            fg=DARK_PALETTE.text,
            bg=DARK_PALETTE.danger,
            activebackground=DARK_PALETTE.danger,
            font=FONT_SCHEME.get_normal(),
            relief=tk.FLAT,
            padx=PADDING_MEDIUM,
            pady=PADDING_SMALL,
            command=self._on_reset_data,
        )
        reset_btn.pack(anchor=tk.W)

    def _on_dark_mode_toggle(self) -> None:
        self.manager.settings["dark_mode"] = self.dark_mode_var.get()
        self.manager.save()

    def _on_reminder_days_change(self) -> None:
        self.manager.reminder_days = self.reminder_var.get()
        self.manager.settings["reminder_days"] = self.reminder_var.get()
        self.manager.save()

    def _on_autosave_toggle(self) -> None:
        self.manager.autosave = self.autosave_var.get()
        self.manager.settings["autosave"] = self.autosave_var.get()
        self.manager.save()

    def _on_reset_data(self) -> None:
        if messagebox.askyesno("Confirm", "Reset all data? This cannot be undone."):
            self.manager.reset_data()
            messagebox.showinfo("Success", "All data has been reset.")


class App(tk.Tk):
    """Main application window container."""

    def __init__(self, manager: ProtectionManager) -> None:
        super().__init__()
        self.manager = manager
        
        self.palette = theme.ACTIVE_PALETTE
        self.is_dark_mode = True

        # We will use theme switching via a central place.
        from theme import ACTIVE_PALETTE
        self.palette = ACTIVE_PALETTE

        self.title("VIGIL — System Health Suite")
        self.geometry("1100x700")
        self.configure(bg=self.palette.background)
        self.minsize(900, 600)

        main_frame = tk.Frame(self, bg=DARK_PALETTE.background)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.sidebar = Sidebar(main_frame, self._on_navigate)
        self.sidebar.toggle_theme = self.toggle_theme
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = tk.Frame(main_frame, bg=DARK_PALETTE.background)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.views: dict[str, tk.Frame] = {
            "dashboard": DashboardView(self.content_frame, self.manager, bg=DARK_PALETTE.background),
            "protection": ProtectionCenterView(self.content_frame, self.manager, bg=DARK_PALETTE.background),
            "history": HistoryView(self.content_frame, self.manager, bg=DARK_PALETTE.background),
            "analytics": AnalyticsView(self.content_frame, self.manager, bg=DARK_PALETTE.background),
            "reminders": RemindersView(self.content_frame, self.manager, bg=DARK_PALETTE.background),
            "settings": SettingsView(self.content_frame, self.manager, bg=DARK_PALETTE.background),
        }

        self._show_view("dashboard")

    def _on_navigate(self, view_key: str) -> None:
        self._show_view(view_key)

    def _show_view(self, view_key: str) -> None:
        for view in self.views.values():
            view.pack_forget()

        if view_key in self.views:
            self.views[view_key].pack(fill=tk.BOTH, expand=True)

    def show_view(self, view_id: str) -> None:
        """Switch the main content area to the specified view."""
        if self.current_view:
            self.current_view.pack_forget()

        if view_id in self.views:
            self.current_view = self.views[view_id]
            self.current_view.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=PADDING_LARGE, pady=PADDING_LARGE)
            
    def _apply_theme(self, widget: tk.Widget) -> None:
        """Recursively apply theme to the widget and its children based on self.palette."""
        bg = None
        fg = None
        
        widget_type = widget.winfo_class()
        
        if widget_type in ('Frame', 'Tk', 'Toplevel'):
            # Some specific backgrounds based on hierarchy/name can be tedious, 
            # we'll approximate. The sidebar and cards have specific bg, but a general
            # recolor uses self.palette.
            if hasattr(widget, 'master') and widget.master == self:
                # Top level frames
                pass
                
        # To avoid breaking existing custom coloring, a more robust way to switch in tkinter
        # is to restart or use a style map. However, for a simple manual apply:
        pass


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
