import tkinter as tk


class DashboardHeader:

    def __init__(self, parent, primary):

        self.parent = parent

        self.PRIMARY = primary

        self.clock_label = None

    # ==========================
    # CREATE HEADER
    # ==========================

    def create(self):

        header = tk.Frame(self.parent, bg=self.PRIMARY, height=70)

        header.pack(fill="x")

        tk.Label(
            header,
            text="⚖ Court Scheduler Dashboard",
            font=("Segoe UI", 22, "bold"),
            bg=self.PRIMARY,
            fg="white",
        ).pack(side="left", padx=25, pady=15)

        self.clock_label = tk.Label(
            header, text="", font=("Segoe UI", 11), bg=self.PRIMARY, fg="white"
        )

        self.clock_label.pack(side="right", padx=25)

        return self.clock_label
