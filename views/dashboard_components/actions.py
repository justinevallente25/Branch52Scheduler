import tkinter as tk


class DashboardActions:

    def __init__(self, parent, open_schedule, refresh_dashboard, colors):

        self.parent = parent

        self.open_schedule = open_schedule

        self.refresh_dashboard = refresh_dashboard

        self.BACKGROUND = colors["BACKGROUND"]
        self.SUCCESS = colors["SUCCESS"]
        self.SECONDARY = colors["SECONDARY"]

    # ==========================
    # CREATE ACTION BUTTONS
    # ==========================

    def create(self):

        actions = tk.Frame(self.parent, bg=self.BACKGROUND)

        actions.pack(anchor="w", padx=30, pady=5)

        tk.Button(
            actions,
            text="➕ New Schedule",
            width=18,
            bg=self.SUCCESS,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            command=self.open_schedule,
        ).pack(side="left", padx=5)

        tk.Button(
            actions,
            text="↻ Refresh",
            width=18,
            bg=self.SECONDARY,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            command=self.refresh_dashboard,
        ).pack(side="left", padx=5)

        return actions
