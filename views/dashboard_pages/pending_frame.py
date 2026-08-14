# views/dashboard_pages/pending_frame.py

import tkinter as tk
from tkinter import messagebox

from views.dashboard_pages.case_list_frame import CaseListFrame
from controllers.pdf_manager import PDFManager


class PendingFrame(CaseListFrame):

    def __init__(self, parent, manager, back_command=None):

        self.manager = manager

        self.pdf_manager = PDFManager()

        schedules = manager.get_pending_cases()

        super().__init__(
            parent, "⏳ Pending Hearing Cases", schedules, back_command, manager
        )

        self.create_print_button()

    # ==========================
    # CREATE PRINT BUTTON
    # ==========================

    def create_print_button(self):

        button_frame = tk.Frame(self.frame, bg="#eef2f7")

        button_frame.pack(fill="x", padx=30, pady=5, before=self.table.master)

        tk.Button(
            button_frame,
            text="🖨 Print Selected Pending Cases",
            width=28,
            bg="#1f4e79",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            command=self.print_selected,
        ).pack(side="left")

    # ==========================
    # PRINT SELECTED
    # ==========================

    def print_selected(self):

        selected_rows = self.table.selection()

        if not selected_rows:

            messagebox.showwarning("No Selection", "Please select cases to print.")

            return

        selected_schedules = []

        for row in selected_rows:

            values = self.table.item(row)["values"]

            schedule_id = values[0]

            for s in self.schedules:

                if s.id == schedule_id:

                    selected_schedules.append(s)

        if not selected_schedules:

            return

        filename = self.pdf_manager.generate_today_schedule(selected_schedules)

        messagebox.showinfo(
            "PDF Created", f"Selected pending cases printed.\n\n{filename}"
        )
