# views/dashboard_pages/upcoming_frame.py

import tkinter as tk
from tkinter import messagebox

from views.dashboard_pages.case_list_frame import CaseListFrame
from controllers.pdf_manager import PDFManager


class UpcomingFrame(CaseListFrame):

    def __init__(self, parent, manager, back_command=None):

        self.manager = manager

        schedules = manager.get_upcoming_cases()

        self.pdf_manager = PDFManager()

        super().__init__(
            parent, "🔔 Upcoming Hearing Schedule", schedules, back_command, manager
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
            text="🖨 Print Upcoming Schedule",
            width=22,
            bg="#1f4e79",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            command=self.print_schedule,
        ).pack(side="left")

    # ==========================
    # PRINT PDF
    # ==========================

    def print_schedule(self):

        schedules = self.manager.get_upcoming_cases()

        if not schedules:

            messagebox.showwarning("No Schedule", "There are no upcoming hearings.")

            return

        filename = self.pdf_manager.generate_today_schedule(schedules)

        messagebox.showinfo(
            "PDF Created", f"Upcoming schedule generated successfully.\n\n{filename}"
        )
