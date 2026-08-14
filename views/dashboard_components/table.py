# views/dashboard_components/table.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime


class DashboardTable:

    def __init__(self, parent, manager, status_menu, colors):

        self.parent = parent

        self.manager = manager

        self.status_menu = status_menu

        self.WHITE = colors["WHITE"]
        self.SECONDARY = colors["SECONDARY"]

        self.table = None

    # ==========================
    # CREATE TABLE
    # ==========================

    def create(self):

        table_card = tk.Frame(self.parent, bg=self.WHITE, bd=1, relief="solid")

        table_card.pack(fill="both", expand=True, padx=30, pady=15)

        tk.Label(
            table_card,
            text="📅 Hearing Schedule Monitor",
            bg=self.SECONDARY,
            fg="white",
            font=("Segoe UI", 13, "bold"),
            anchor="w",
            padx=15,
        ).pack(fill="x")

        self.create_table(table_card)

        return self.table

    # ==========================
    # TABLE CREATION
    # ==========================

    def create_table(self, parent):

        table_frame = tk.Frame(parent, bg=self.WHITE)

        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

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

        style = ttk.Style()

        style.configure("Treeview", rowheight=32, font=("Segoe UI", 10))

        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

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

        self.table.tag_configure("completed", background="#d5f5e3")

        self.table.tag_configure("overdue", background="#fadbd8")

        self.table.tag_configure("today", background="#fcf3cf")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")

        self.table.pack(fill="both", expand=True)

        self.table.bind("<Button-3>", self.status_menu.show)

        self.load_schedule()

    # ==========================
    # LOAD SCHEDULE TABLE
    # ==========================

    def load_schedule(self):

        for row in self.table.get_children():

            self.table.delete(row)

        for s in reversed(self.manager.schedules):

            tag = ""

            if s.status == "Completed":

                tag = "completed"

            elif s.status == "Not Attended":

                tag = "overdue"

            else:

                today = datetime.now().strftime("%Y-%m-%d")

                if s.date < today:

                    tag = "overdue"

                elif s.date == today:

                    tag = "today"

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
                tags=(tag,),
            )
