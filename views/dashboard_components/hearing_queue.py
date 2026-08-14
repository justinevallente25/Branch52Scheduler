# views/dashboard_components/hearing_queue.py

import tkinter as tk
from datetime import datetime


class HearingQueue:

    def __init__(self, parent, manager, colors, refresh_command=None):

        self.parent = parent

        self.manager = manager

        self.refresh_command = refresh_command

        self.PRIMARY = colors["PRIMARY"]
        self.SECONDARY = colors["SECONDARY"]
        self.SUCCESS = colors["SUCCESS"]
        self.DANGER = colors["DANGER"]
        self.WARNING = colors["WARNING"]

        self.BACKGROUND = colors["BACKGROUND"]
        self.WHITE = colors["WHITE"]
        self.TEXT = colors["TEXT"]

        self.frame = None

        self.now_serving_frame = None
        self.next_frame = None
        self.waiting_frame = None

        self.now_serving_case = None
        self.next_case = None
        self.waiting_cases = []

        self.skipped_cases = []

        self.create()

    # ==========================
    # CREATE UI
    # ==========================

    def create(self):

        self.frame = tk.Frame(self.parent, bg=self.BACKGROUND)

        self.frame.pack(fill="x", padx=30, pady=(5, 15))

        tk.Label(
            self.frame,
            text="🎫 Hearing Queue",
            bg=self.BACKGROUND,
            fg=self.TEXT,
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", pady=(0, 8))

        main_frame = tk.Frame(self.frame, bg=self.BACKGROUND)

        main_frame.pack(fill="x")

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        self.now_serving_frame = tk.Frame(
            main_frame,
            bg=self.WHITE,
            bd=1,
            relief="solid",
        )

        self.now_serving_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7),
        )

        self.next_frame = tk.Frame(
            main_frame,
            bg=self.WHITE,
            bd=1,
            relief="solid",
        )

        self.next_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0),
        )

        self.create_waiting_list()

        self.load_queue()

        return self.frame

    # ==========================
    # NOW SERVING
    # ==========================

    def create_now_serving(self, schedule):

        for widget in self.now_serving_frame.winfo_children():

            widget.destroy()

        header = tk.Frame(
            self.now_serving_frame,
            bg=self.SUCCESS,
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="NOW SERVING",
            bg=self.SUCCESS,
            fg="white",
            font=("Segoe UI", 15, "bold"),
        ).pack(pady=10)

        if not schedule:

            tk.Label(
                self.now_serving_frame,
                text="No hearing currently being served",
                bg=self.WHITE,
                fg="#7f8c8d",
                font=("Segoe UI", 12),
            ).pack(pady=35)

            return

        tk.Label(
            self.now_serving_frame,
            text=schedule.case_no or "No Case Number",
            bg=self.WHITE,
            fg=self.PRIMARY,
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(18, 5))

        tk.Label(
            self.now_serving_frame,
            text=schedule.complainant,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 12, "bold"),
            wraplength=350,
        ).pack()

        tk.Label(
            self.now_serving_frame,
            text="vs",
            bg=self.WHITE,
            fg="#7f8c8d",
            font=("Segoe UI", 10),
        ).pack(pady=2)

        tk.Label(
            self.now_serving_frame,
            text=schedule.respondent,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 12, "bold"),
            wraplength=350,
        ).pack()

        tk.Label(
            self.now_serving_frame,
            text=f"{schedule.time}  •  {schedule.proceeding}",
            bg=self.WHITE,
            fg="#7f8c8d",
            font=("Segoe UI", 10),
            wraplength=350,
        ).pack(pady=(8, 12))

        button_frame = tk.Frame(
            self.now_serving_frame,
            bg=self.WHITE,
        )

        button_frame.pack(pady=(0, 10))

        tk.Button(
            button_frame,
            text="✅ Completed",
            width=14,
            bg=self.SUCCESS,
            fg="white",
            relief="flat",
            command=lambda: self.change_status("Completed"),
        ).pack(side="left", padx=3)

        tk.Button(
            button_frame,
            text="❌ Not Attended",
            width=14,
            bg=self.DANGER,
            fg="white",
            relief="flat",
            command=lambda: self.change_status("Not Attended"),
        ).pack(side="left", padx=3)

        tk.Button(
            button_frame,
            text="⏳ Pending",
            width=14,
            bg=self.WARNING,
            fg="white",
            relief="flat",
            command=lambda: self.change_status("Pending"),
        ).pack(side="left", padx=3)

        tk.Button(
            self.now_serving_frame,
            text="⏭️ Skip / Move to Back",
            width=24,
            bg=self.SECONDARY,
            fg="white",
            relief="flat",
            command=self.skip_current,
        ).pack(pady=(0, 18))

    # ==========================
    # NEXT
    # ==========================

    def create_next(self, schedule):

        for widget in self.next_frame.winfo_children():

            widget.destroy()

        header = tk.Frame(
            self.next_frame,
            bg=self.SECONDARY,
        )

        header.pack(fill="x")

        tk.Label(
            header,
            text="NEXT",
            bg=self.SECONDARY,
            fg="white",
            font=("Segoe UI", 15, "bold"),
        ).pack(pady=10)

        if not schedule:

            tk.Label(
                self.next_frame,
                text="No next hearing",
                bg=self.WHITE,
                fg="#7f8c8d",
                font=("Segoe UI", 12),
            ).pack(pady=35)

            return

        tk.Label(
            self.next_frame,
            text=schedule.case_no or "No Case Number",
            bg=self.WHITE,
            fg=self.SECONDARY,
            font=("Segoe UI", 18, "bold"),
        ).pack(pady=(18, 5))

        tk.Label(
            self.next_frame,
            text=schedule.complainant,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 12, "bold"),
            wraplength=350,
        ).pack()

        tk.Label(
            self.next_frame,
            text="vs",
            bg=self.WHITE,
            fg="#7f8c8d",
            font=("Segoe UI", 10),
        ).pack(pady=2)

        tk.Label(
            self.next_frame,
            text=schedule.respondent,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 12, "bold"),
            wraplength=350,
        ).pack()

        tk.Label(
            self.next_frame,
            text=f"{schedule.time}  •  {schedule.proceeding}",
            bg=self.WHITE,
            fg="#7f8c8d",
            font=("Segoe UI", 10),
            wraplength=350,
        ).pack(pady=(8, 12))

    # ==========================
    # WAITING LIST
    # ==========================

    def create_waiting_list(self):

        waiting_card = tk.Frame(
            self.frame,
            bg=self.WHITE,
            bd=1,
            relief="solid",
        )

        waiting_card.pack(fill="x", pady=(10, 0))

        tk.Label(
            waiting_card,
            text="WAITING LIST",
            bg=self.PRIMARY,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            anchor="w",
            padx=15,
        ).pack(fill="x")

        self.waiting_frame = tk.Frame(
            waiting_card,
            bg=self.WHITE,
        )

        self.waiting_frame.pack(fill="x", padx=10, pady=8)

    # ==========================
    # LOAD QUEUE
    # ==========================

    def load_queue(self):

        today = datetime.now().strftime("%Y-%m-%d")

        schedules = []

        for schedule in self.manager.schedules:

            if schedule.date != today:

                continue

            if schedule.status in ["Completed", "Not Attended"]:

                continue

            schedules.append(schedule)

        schedules.sort(key=self.get_time_value)

        active_skipped_cases = []

        for schedule in self.skipped_cases:

            for active_schedule in schedules:

                if active_schedule.id == schedule.id:

                    active_skipped_cases.append(active_schedule)

                    break

        for schedule in active_skipped_cases:

            schedules.remove(schedule)

        schedules.extend(active_skipped_cases)

        self.now_serving_case = None
        self.next_case = None
        self.waiting_cases = []

        if schedules:

            self.now_serving_case = schedules[0]

        if len(schedules) > 1:

            self.next_case = schedules[1]

        if len(schedules) > 2:

            self.waiting_cases = schedules[2:]

        self.create_now_serving(self.now_serving_case)

        self.create_next(self.next_case)

        self.refresh_waiting_list()

    # ==========================
    # TIME VALUE
    # ==========================

    def get_time_value(self, schedule):

        if not schedule.time:

            return datetime.max

        try:

            return datetime.strptime(schedule.time, "%I:%M %p")

        except ValueError:

            return datetime.max

    # ==========================
    # REFRESH WAITING LIST
    # ==========================

    def refresh_waiting_list(self):

        for widget in self.waiting_frame.winfo_children():

            widget.destroy()

        if not self.waiting_cases:

            tk.Label(
                self.waiting_frame,
                text="No other hearings waiting.",
                bg=self.WHITE,
                fg="#7f8c8d",
                font=("Segoe UI", 10),
            ).pack(pady=8)

            return

        for index, schedule in enumerate(self.waiting_cases, start=3):

            row = tk.Frame(
                self.waiting_frame,
                bg=self.WHITE,
            )

            row.pack(fill="x", pady=2)

            tk.Label(
                row,
                text=f"#{index}",
                width=5,
                bg=self.WHITE,
                fg=self.PRIMARY,
                font=("Segoe UI", 10, "bold"),
                anchor="w",
            ).pack(side="left")

            tk.Label(
                row,
                text=schedule.time,
                width=12,
                bg=self.WHITE,
                fg=self.TEXT,
                font=("Segoe UI", 10),
                anchor="w",
            ).pack(side="left")

            tk.Label(
                row,
                text=schedule.case_no or "No Case Number",
                width=20,
                bg=self.WHITE,
                fg=self.TEXT,
                font=("Segoe UI", 10, "bold"),
                anchor="w",
            ).pack(side="left")

            tk.Label(
                row,
                text=schedule.proceeding,
                bg=self.WHITE,
                fg="#7f8c8d",
                font=("Segoe UI", 10),
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

    # ==========================
    # CHANGE STATUS
    # ==========================

    def change_status(self, status):

        if not self.now_serving_case:

            return

        schedule_id = self.now_serving_case.id

        self.manager.update_status(schedule_id, status)

        self.remove_from_skipped(schedule_id)

        self.load_queue()

        if self.refresh_command:

            self.refresh_command()

    # ==========================
    # SKIP CURRENT
    # ==========================

    def skip_current(self):

        if not self.now_serving_case:

            return

        skipped_case = self.now_serving_case

        self.remove_from_skipped(skipped_case.id)

        self.skipped_cases.append(skipped_case)

        self.load_queue()

        if self.refresh_command:

            self.refresh_command()

    # ==========================
    # REMOVE FROM SKIPPED
    # ==========================

    def remove_from_skipped(self, schedule_id):

        self.skipped_cases = [
            schedule
            for schedule in self.skipped_cases
            if schedule.id != schedule_id
        ]

    # ==========================
    # REFRESH
    # ==========================

    def refresh(self):

        self.load_queue()