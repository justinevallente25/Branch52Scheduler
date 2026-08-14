# views/dashboard_pages/case_list_frame.py

import tkinter as tk
from tkinter import ttk


class CaseListFrame:

    def __init__(self, parent, title, schedules, back_command=None, manager=None):

        self.parent = parent

        self.title = title

        self.schedules = schedules

        self.back_command = back_command

        self.manager = manager

        self.selected_id = None

        self.frame = tk.Frame(self.parent, bg="#eef2f7")

        self.create_ui()

    # ==========================
    # CREATE UI
    # ==========================

    def create_ui(self):

        header = tk.Frame(self.frame, bg="#1f4e79", height=60)

        header.pack(fill="x")

        tk.Label(
            header,
            text=self.title,
            font=("Segoe UI", 18, "bold"),
            bg="#1f4e79",
            fg="white",
        ).pack(side="left", padx=20, pady=15)

        if self.back_command:

            tk.Button(
                header,
                text="← Back",
                width=12,
                bg="#2e75b6",
                fg="white",
                relief="flat",
                command=self.back_command,
            ).pack(side="right", padx=20)

        action_frame = tk.Frame(self.frame, bg="#eef2f7")

        action_frame.pack(fill="x", padx=30, pady=(15, 5))

        tk.Button(
            action_frame,
            text="✅ Mark Completed",
            bg="#2e8b57",
            fg="white",
            width=18,
            relief="flat",
            command=lambda: self.change_status("Completed"),
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="❌ Mark Not Attended",
            bg="#c0392b",
            fg="white",
            width=18,
            relief="flat",
            command=lambda: self.change_status("Not Attended"),
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="⏳ Mark Pending",
            bg="#f39c12",
            fg="white",
            width=18,
            relief="flat",
            command=lambda: self.change_status("Pending"),
        ).pack(side="left", padx=5)

        table_frame = tk.Frame(self.frame, bg="white")

        table_frame.pack(fill="both", expand=True, padx=30, pady=20)

        columns = (
            "id",
            "case",
            "complainant",
            "respondent",
            "date",
            "time",
            "proceeding",
            "status",
        )

        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        headings = {
            "id": "ID",
            "case": "Case No",
            "complainant": "Complainant",
            "respondent": "Respondent",
            "date": "Date",
            "time": "Time",
            "proceeding": "Proceeding",
            "status": "Status",
        }

        for col in columns:

            self.table.heading(col, text=headings[col])

            self.table.column(col, width=120)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")

        self.table.pack(fill="both", expand=True)

        self.table.bind("<ButtonRelease-1>", self.select_row)

        self.load_data()

    # ==========================
    # SELECT ROW
    # ==========================

    def select_row(self, event):

        row = self.table.focus()

        if row:

            values = self.table.item(row)["values"]

            self.selected_id = values[0]

    # ==========================
    # CHANGE STATUS
    # ==========================

    def change_status(self, status):

        if not self.selected_id:

            return

        if self.manager:

            self.manager.update_status(self.selected_id, status)

        self.refresh()

    # ==========================
    # REFRESH
    # ==========================

    def refresh(self):

        if self.manager:

            self.schedules = self.schedules

        self.load_data()

    # ==========================
    # LOAD DATA
    # ==========================

    def load_data(self):

        for row in self.table.get_children():

            self.table.delete(row)

        for s in reversed(self.schedules):

            self.table.insert(
                "",
                "end",
                values=(
                    s.id,
                    s.case_no,
                    s.complainant,
                    s.respondent,
                    s.date,
                    s.time,
                    s.proceeding,
                    s.status,
                ),
            )

    # ==========================
    # SHOW
    # ==========================

    def show(self):

        self.frame.pack(fill="both", expand=True)

    # ==========================
    # HIDE
    # ==========================

    def hide(self):

        self.frame.pack_forget()
