# views/navbar.py

import tkinter as tk


class Navbar:

    def __init__(self, parent, app):

        self.app = app

        self.buttons = {}

        self.frame = tk.Frame(parent, bg="#003366", width=220)

        self.frame.pack(side="left", fill="y")

        self.create_ui()

    # ==========================
    # CREATE UI
    # ==========================

    def create_ui(self):

        self.create_header()

        self.create_button("📊 Dashboard", self.app.show_dashboard, "dashboard")

        self.create_button("📅 Schedule", self.app.show_schedule, "schedule")

    # ==========================
    # HEADER
    # ==========================

    def create_header(self):

        tk.Label(
            self.frame,
            text="⚖\nScheduler",
            bg="#003366",
            fg="white",
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=30)

    # ==========================
    # CREATE BUTTON
    # ==========================

    def create_button(self, text, command, name):

        button = tk.Button(
            self.frame,
            text=text,
            command=lambda: self.select(name, command),
            bg="#005B96",
            fg="white",
            relief="flat",
            font=("Segoe UI", 11),
            anchor="w",
            padx=20,
        )

        button.pack(fill="x", padx=15, pady=5)

        self.buttons[name] = button

    # ==========================
    # SELECT BUTTON
    # ==========================

    def select(self, name, command):

        for key, button in self.buttons.items():

            button.config(bg="#005B96")

        self.buttons[name].config(bg="#007ACC")

        command()
