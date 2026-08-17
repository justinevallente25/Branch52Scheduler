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
            parent,
            "⏳ Pending Hearing Cases",
            schedules,
            back_command,
            manager,
        )

        self.create_print_button()

    # ==========================
    # CREATE PRINT BUTTON
    # ==========================

    def create_print_button(self):

        self.extra_action_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 5),
        )

        tk.Button(
            self.extra_action_frame,
            text="🖨 Print Selected Pending Case",
            width=28,
            bg="#1f4e79",
            fg="white",
            activebackground="#2e75b6",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.print_selected,
        ).pack(
            side="left",
        )

    # ==========================
    # PRINT SELECTED
    # ==========================

    def print_selected(self):

        if not self.selected_id:

            messagebox.showwarning(
                "No Selection",
                "Please select a case to print.",
            )

            return

        selected_schedules = []

        for s in self.schedules:

            if s.id == self.selected_id:

                selected_schedules.append(s)

                break

        if not selected_schedules:

            return

        filename = self.pdf_manager.generate_today_schedule(
            selected_schedules
        )

        messagebox.showinfo(
            "PDF Created",
            f"Selected pending case printed.\n\n{filename}",
        )

    # ==========================
    # REFRESH
    # ==========================

    def refresh(self):

        self.schedules = self.manager.get_pending_cases()

        self.load_data()