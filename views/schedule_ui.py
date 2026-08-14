# views/schedule_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from models.schedule import Schedule


class ScheduleUI:

    def __init__(self, parent, manager, holiday_manager):

        self.parent = parent

        self.manager = manager

        self.holiday_manager = holiday_manager

        self.selected_id = None

        # COLORS

        self.PRIMARY = "#1f4e79"
        self.SECONDARY = "#2e75b6"
        self.SUCCESS = "#2e8b57"
        self.DANGER = "#c0392b"

        self.BACKGROUND = "#eef2f7"

        self.WHITE = "#ffffff"
        self.TEXT = "#2c3e50"

        self.create_ui()

        self.load_data()

    # ==========================
    # CREATE UI
    # ==========================

    def create_ui(self):

        self.frame = tk.Frame(self.parent, bg=self.BACKGROUND)

        self.frame.pack(fill="both", expand=True)

        # ======================
        # HEADER
        # ======================

        header = tk.Frame(self.frame, bg=self.PRIMARY, height=60)

        header.pack(fill="x")

        title = tk.Label(
            header,
            text="⚖ Court Hearing Schedule System",
            font=("Segoe UI", 20, "bold"),
            bg=self.PRIMARY,
            fg="white",
        )

        title.pack(pady=12)

        # ======================
        # FORM CARD
        # ======================

        form_card = tk.Frame(self.frame, bg=self.WHITE, bd=1, relief="solid")

        form_card.pack(padx=25, pady=15, fill="x")

        form_header = tk.Label(
            form_card,
            text="📋 Hearing Information",
            font=("Segoe UI", 13, "bold"),
            bg=self.SECONDARY,
            fg="white",
            anchor="w",
            padx=15,
        )

        form_header.pack(fill="x")

        form = tk.Frame(form_card, bg=self.WHITE)

        form.pack(pady=15)

        left = tk.Frame(form, bg=self.WHITE)

        left.grid(row=0, column=0, padx=30)

        self.case_entry = self.create_entry(left, "📄 NLRC Case No:", 0)

        self.complainant_entry = self.create_entry(left, "👤 Complainant:", 1)

        self.respondent_entry = self.create_entry(left, "👤 Respondent:", 2)
        # RIGHT SIDE

        right = tk.Frame(form, bg=self.WHITE)

        right.grid(row=0, column=1, padx=30)

        tk.Label(
            right,
            text="📅 Date:",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=5, pady=8)

        self.date_entry = DateEntry(
            right, width=22, date_pattern="yyyy-mm-dd", font=("Segoe UI", 10)
        )

        self.date_entry.grid(row=0, column=1, padx=5, pady=8)

        self.date_entry.bind("<<DateEntrySelected>>", self.check_selected_date)

        self.holiday_label = tk.Label(
            right, text="", bg=self.WHITE, fg=self.DANGER, font=("Segoe UI", 9, "bold")
        )

        self.holiday_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.time_entry = self.create_entry(right, "⏰ Time:", 1)

        tk.Label(
            right,
            text="⚖ Proceeding:",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold"),
        ).grid(row=2, column=0, sticky="w", padx=5, pady=8)

        self.proceeding = ttk.Combobox(
            right,
            width=28,
            state="readonly",
            values=[
                "1st Mandatory Conference",
                "2nd Mandatory Conference",
                "Settlement",
                "Reply",
                "Execution Conference",
                "P/P",
                "Position Paper",
            ],
        )

        self.proceeding.grid(row=2, column=1, padx=5, pady=8)

        # ======================
        # BUTTONS
        # ======================

        buttons = tk.Frame(self.frame, bg=self.BACKGROUND)

        buttons.pack(pady=10)

        button_style = {
            "font": ("Segoe UI", 10, "bold"),
            "fg": "white",
            "relief": "flat",
            "width": 15,
            "cursor": "hand2",
        }

        tk.Button(
            buttons,
            text="➕ Add Schedule",
            bg=self.SUCCESS,
            command=self.add,
            **button_style,
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            buttons,
            text="✏ Update",
            bg=self.SECONDARY,
            command=self.update,
            **button_style,
        ).grid(row=0, column=1, padx=8)

        tk.Button(
            buttons,
            text="🗑 Delete",
            bg=self.DANGER,
            command=self.delete,
            **button_style,
        ).grid(row=0, column=2, padx=8)

        tk.Button(
            buttons, text="↻ Clear", bg="#7f8c8d", command=self.clear, **button_style
        ).grid(row=0, column=3, padx=8)
        # ======================
        # TABLE CARD
        # ======================

        table_card = tk.Frame(self.frame, bg=self.WHITE, bd=1, relief="solid")

        table_card.pack(fill="both", expand=True, padx=25, pady=10)

        table_header = tk.Label(
            table_card,
            text="📅 Scheduled Hearings",
            font=("Segoe UI", 13, "bold"),
            bg=self.SECONDARY,
            fg="white",
            anchor="w",
            padx=15,
        )

        table_header.pack(fill="x")

        table_frame = tk.Frame(table_card, bg=self.WHITE)

        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = (
            "id",
            "case",
            "complainant",
            "respondent",
            "date",
            "time",
            "proceeding",
        )

        style = ttk.Style()

        style.configure("Treeview", font=("Segoe UI", 10), rowheight=32)

        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        style.map("Treeview", background=[("selected", self.SECONDARY)])

        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        headings = {
            "id": "ID",
            "case": "Case No",
            "complainant": "Complainant",
            "respondent": "Respondent",
            "date": "Date",
            "time": "Time",
            "proceeding": "Proceeding",
        }

        widths = {
            "id": 50,
            "case": 120,
            "complainant": 150,
            "respondent": 150,
            "date": 100,
            "time": 90,
            "proceeding": 180,
        }

        for col in columns:

            self.table.heading(col, text=headings[col])

            self.table.column(col, width=widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")

        self.table.pack(fill="both", expand=True)

        self.table.bind("<ButtonRelease-1>", self.select_row)

    # ==========================
    # ENTRY HELPER
    # ==========================

    def create_entry(self, parent, text, row):

        tk.Label(
            parent,
            text=text,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold"),
        ).grid(row=row, column=0, sticky="w", padx=5, pady=8)

        entry = tk.Entry(parent, width=32, font=("Segoe UI", 10), relief="solid", bd=1)

        entry.grid(row=row, column=1, padx=5, pady=8)

        return entry

    # ==========================
    # LOAD DATA
    # ==========================

    def load_data(self):

        for item in self.table.get_children():

            self.table.delete(item)

        for s in self.manager.schedules:

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
                ),
            )

    # ==========================
    # ADD
    # ==========================

    def add(self):

        schedule = Schedule(
            self.manager.generate_id(),
            self.case_entry.get(),
            self.complainant_entry.get(),
            self.respondent_entry.get(),
            self.date_entry.get(),
            self.time_entry.get(),
            self.proceeding.get(),
        )

        self.manager.add(schedule)

        self.load_data()

        self.clear()

    # ==========================
    # UPDATE
    # ==========================

    def update(self):

        if self.selected_id is None:

            messagebox.showwarning("Warning", "Select a record first")

            return

        schedule = Schedule(
            self.selected_id,
            self.case_entry.get(),
            self.complainant_entry.get(),
            self.respondent_entry.get(),
            self.date_entry.get(),
            self.time_entry.get(),
            self.proceeding.get(),
        )

        self.manager.update(self.selected_id, schedule)

        self.load_data()

        self.clear()

    # ==========================
    # DELETE
    # ==========================

    def delete(self):

        if self.selected_id is None:

            return

        confirm = messagebox.askyesno("Delete", "Delete selected schedule?")

        if confirm:

            self.manager.delete(self.selected_id)

            self.load_data()

            self.clear()

    # ==========================
    # SELECT ROW
    # ==========================

    def select_row(self, event=None):

        selected = self.table.focus()

        if not selected:

            return

        values = self.table.item(selected)["values"]

        self.selected_id = values[0]

        self.case_entry.delete(0, tk.END)

        self.case_entry.insert(0, values[1])

        self.complainant_entry.delete(0, tk.END)

        self.complainant_entry.insert(0, values[2])

        self.respondent_entry.delete(0, tk.END)

        self.respondent_entry.insert(0, values[3])

        self.date_entry.set_date(values[4])

        self.time_entry.delete(0, tk.END)

        self.time_entry.insert(0, values[5])

        self.proceeding.set(values[6])

        self.check_selected_date()

    # ==========================
    # CHECK HOLIDAY
    # ==========================

    def check_selected_date(self, event=None):

        selected_date = self.date_entry.get()

        if self.holiday_manager.is_holiday(selected_date):

            holiday = self.holiday_manager.get_holiday_name(selected_date)

            self.holiday_label.config(text=f"⚠ Holiday: {holiday}")

        else:

            self.holiday_label.config(text="")

    # ==========================
    # CLEAR
    # ==========================

    def clear(self):

        self.selected_id = None

        self.case_entry.delete(0, tk.END)

        self.complainant_entry.delete(0, tk.END)

        self.respondent_entry.delete(0, tk.END)

        self.time_entry.delete(0, tk.END)

        self.proceeding.set("")

        self.holiday_label.config(text="")
