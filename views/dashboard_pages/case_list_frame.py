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
        self.cards = []

        self.frame = tk.Frame(
            self.parent,
            bg="#eef2f7",
        )

        self.create_ui()

    # ==========================
    # CREATE UI
    # ==========================

    def create_ui(self):

        # ==========================
        # HEADER
        # ==========================

        header = tk.Frame(
            self.frame,
            bg="#1f4e79",
            height=68,
        )

        header.pack(
            fill="x",
        )

        header.pack_propagate(False)

        title_frame = tk.Frame(
            header,
            bg="#1f4e79",
        )

        title_frame.pack(
            side="left",
            padx=25,
            pady=9,
        )

        tk.Label(
            title_frame,
            text=self.title,
            font=("Segoe UI", 18, "bold"),
            bg="#1f4e79",
            fg="white",
        ).pack(
            anchor="w",
        )

        tk.Label(
            title_frame,
            text="Case Schedule Management",
            font=("Segoe UI", 8),
            bg="#1f4e79",
            fg="#d9e8f5",
        ).pack(
            anchor="w",
        )

        if self.back_command:

            tk.Button(
                header,
                text="← Back",
                width=12,
                bg="#2e75b6",
                fg="white",
                activebackground="#3b82c4",
                activeforeground="white",
                relief="flat",
                bd=0,
                font=("Segoe UI", 9, "bold"),
                cursor="hand2",
                command=self.back_command,
            ).pack(
                side="right",
                padx=20,
                pady=18,
            )

        # ==========================
        # MAIN AREA
        # ==========================

        main_frame = tk.Frame(
            self.frame,
            bg="#eef2f7",
        )

        main_frame.pack(
            fill="both",
            expand=True,
        )

        # ==========================
        # ACTION BAR
        # ==========================

        self.action_frame = tk.Frame(
            main_frame,
            bg="#eef2f7",
        )

        self.action_frame.pack(
            fill="x",
            padx=30,
            pady=(18, 8),
        )

        tk.Label(
            self.action_frame,
            text="Case Actions",
            font=("Segoe UI", 11, "bold"),
            bg="#eef2f7",
            fg="#1f4e79",
        ).pack(
            side="left",
            padx=(0, 12),
        )

        tk.Button(
            self.action_frame,
            text="✓  Mark Completed",
            bg="#2e8b57",
            fg="white",
            activebackground="#379f67",
            activeforeground="white",
            width=18,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            command=lambda: self.change_status("Completed"),
        ).pack(
            side="left",
            padx=3,
        )

        tk.Button(
            self.action_frame,
            text="✕  Mark Not Attended",
            bg="#c0392b",
            fg="white",
            activebackground="#d94a3b",
            activeforeground="white",
            width=19,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            command=lambda: self.change_status("Not Attended"),
        ).pack(
            side="left",
            padx=3,
        )

        tk.Button(
            self.action_frame,
            text="◷  Mark Pending",
            bg="#f39c12",
            fg="white",
            activebackground="#f7a72c",
            activeforeground="white",
            width=17,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            command=lambda: self.change_status("Pending"),
        ).pack(
            side="left",
            padx=3,
        )

        self.count_label = tk.Label(
            self.action_frame,
            text="",
            font=("Segoe UI", 9),
            bg="#eef2f7",
            fg="#7f8c8d",
        )

        self.count_label.pack(
            side="right",
            padx=5,
        )

        # ==========================
        # EXTRA ACTION FRAME
        # ==========================

        self.extra_action_frame = tk.Frame(
            main_frame,
            bg="#eef2f7",
        )

        # ==========================
        # CARD AREA
        # ==========================

        card_area = tk.Frame(
            main_frame,
            bg="#eef2f7",
        )

        card_area.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(5, 25),
        )

        # ==========================
        # CANVAS
        # ==========================

        self.canvas = tk.Canvas(
            card_area,
            bg="#eef2f7",
            highlightthickness=0,
            bd=0,
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )

        # ==========================
        # SCROLLBAR
        # ==========================

        scrollbar = ttk.Scrollbar(
            card_area,
            orient="vertical",
            command=self.canvas.yview,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set,
        )

        # ==========================
        # CARD CONTAINER
        # ==========================

        self.cards_frame = tk.Frame(
            self.canvas,
            bg="#eef2f7",
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.cards_frame,
            anchor="nw",
        )

        self.cards_frame.bind(
            "<Configure>",
            self.update_scrollregion,
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_cards_frame,
        )

        self.canvas.bind(
            "<Enter>",
            self.bind_mouse_wheel,
        )

        self.canvas.bind(
            "<Leave>",
            self.unbind_mouse_wheel,
        )

        self.load_data()

    # ==========================
    # MOUSE WHEEL
    # ==========================

    def bind_mouse_wheel(self, event):

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_wheel,
        )

    def unbind_mouse_wheel(self, event):

        self.canvas.unbind_all(
            "<MouseWheel>",
        )

    def mouse_wheel(self, event):

        try:

            self.canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units",
            )

        except tk.TclError:

            pass

    # ==========================
    # UPDATE SCROLL REGION
    # ==========================

    def update_scrollregion(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
        )

    # ==========================
    # RESIZE CARD FRAME
    # ==========================

    def resize_cards_frame(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width,
        )

    # ==========================
    # LOAD DATA
    # ==========================

    def load_data(self):

        for widget in self.cards_frame.winfo_children():

            widget.destroy()

        self.cards = []

        self.selected_id = None

        schedules = list(reversed(self.schedules))

        self.count_label.config(
            text=f"{len(schedules)} case(s)",
        )

        if not schedules:

            self.show_empty()

            self.update_scrollregion()

            return

        for schedule in schedules:

            self.create_case_card(
                schedule,
            )

        self.update_scrollregion()

    # ==========================
    # GET STATUS STYLE
    # ==========================

    def get_status_style(self, schedule):

        status = str(
            getattr(schedule, "status", "")
        ).strip()

        status_lower = status.lower()

        if status_lower == "completed":

            return (
                "#2e8b57",
                "#e8f6ee",
                "#2e8b57",
                "✓  COMPLETED",
            )

        if status_lower == "not attended":

            return (
                "#c0392b",
                "#fdecea",
                "#c0392b",
                "✕  NOT ATTENDED",
            )

        if status_lower == "pending":

            return (
                "#f39c12",
                "#fff4df",
                "#d68910",
                "◷  PENDING",
            )

        return (
            "#2e75b6",
            "#edf4fb",
            "#2e75b6",
            status.upper() if status else "NO STATUS",
        )

    # ==========================
    # CREATE CASE CARD
    # ==========================

    def create_case_card(self, schedule):

        (
            status_strip,
            status_bg,
            status_fg,
            status_text,
        ) = self.get_status_style(schedule)

        # ==========================
        # CARD SHADOW
        # ==========================

        shadow = tk.Frame(
            self.cards_frame,
            bg="#d5dce3",
        )

        shadow.pack(
            fill="x",
            padx=2,
            pady=(0, 14),
        )

        # ==========================
        # CARD
        # ==========================

        card = tk.Frame(
            shadow,
            bg="white",
            highlightthickness=1,
            highlightbackground="#dce3e9",
        )

        card.pack(
            fill="x",
            padx=(0, 3),
            pady=(0, 3),
        )

        card_data = {
            "id": schedule.id,
            "card": card,
            "shadow": shadow,
        }

        self.cards.append(
            card_data,
        )

        # ==========================
        # STATUS STRIP
        # ==========================

        status_bar = tk.Frame(
            card,
            bg=status_strip,
            width=6,
        )

        status_bar.pack(
            side="left",
            fill="y",
        )

        # ==========================
        # CONTENT
        # ==========================

        content = tk.Frame(
            card,
            bg="white",
        )

        content.pack(
            side="left",
            fill="both",
            expand=True,
        )

        # ==========================
        # TOP SECTION
        # ==========================

        top = tk.Frame(
            content,
            bg="white",
        )

        top.pack(
            fill="x",
            padx=20,
            pady=(17, 10),
        )

        case_frame = tk.Frame(
            top,
            bg="white",
        )

        case_frame.pack(
            side="left",
            fill="x",
            expand=True,
        )

        tk.Label(
            case_frame,
            text="CASE NO.",
            font=("Segoe UI", 8, "bold"),
            bg="white",
            fg="#7f8c8d",
        ).pack(
            anchor="w",
        )

        tk.Label(
            case_frame,
            text=(
                str(schedule.case_no)
                if schedule.case_no
                else "No Case Number"
            ),
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#1f4e79",
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        status_label = tk.Label(
            top,
            text=status_text,
            font=("Segoe UI", 8, "bold"),
            bg=status_bg,
            fg=status_fg,
            padx=12,
            pady=6,
        )

        status_label.pack(
            side="right",
        )

        # ==========================
        # DIVIDER
        # ==========================

        tk.Frame(
            content,
            bg="#e9edf1",
            height=1,
        ).pack(
            fill="x",
            padx=20,
        )

        # ==========================
        # PARTIES
        # ==========================

        parties = tk.Frame(
            content,
            bg="white",
        )

        parties.pack(
            fill="x",
            padx=20,
            pady=15,
        )

        complainant_frame = tk.Frame(
            parties,
            bg="white",
        )

        complainant_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 15),
        )

        tk.Label(
            complainant_frame,
            text="COMPLAINANT",
            font=("Segoe UI", 8, "bold"),
            bg="white",
            fg="#7f8c8d",
        ).pack(
            anchor="w",
        )

        complainant_label = tk.Label(
            complainant_frame,
            text=(
                schedule.complainant
                if schedule.complainant
                else "—"
            ),
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            anchor="w",
            justify="left",
            wraplength=450,
        )

        complainant_label.pack(
            anchor="w",
            fill="x",
            pady=(4, 0),
        )

        respondent_frame = tk.Frame(
            parties,
            bg="white",
        )

        respondent_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(15, 0),
        )

        tk.Label(
            respondent_frame,
            text="RESPONDENT",
            font=("Segoe UI", 8, "bold"),
            bg="white",
            fg="#7f8c8d",
        ).pack(
            anchor="w",
        )

        respondent_label = tk.Label(
            respondent_frame,
            text=(
                schedule.respondent
                if schedule.respondent
                else "—"
            ),
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2c3e50",
            anchor="w",
            justify="left",
            wraplength=450,
        )

        respondent_label.pack(
            anchor="w",
            fill="x",
            pady=(4, 0),
        )

        # ==========================
        # INFORMATION BAR
        # ==========================

        info_frame = tk.Frame(
            content,
            bg="#f7f9fb",
        )

        info_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 15),
        )

        # ==========================
        # DATE
        # ==========================

        date_frame = tk.Frame(
            info_frame,
            bg="#f7f9fb",
        )

        date_frame.pack(
            side="left",
            padx=15,
            pady=12,
        )

        tk.Label(
            date_frame,
            text="DATE",
            font=("Segoe UI", 7, "bold"),
            bg="#f7f9fb",
            fg="#7f8c8d",
        ).pack(
            anchor="w",
        )

        tk.Label(
            date_frame,
            text=str(schedule.date),
            font=("Segoe UI", 9, "bold"),
            bg="#f7f9fb",
            fg="#2c3e50",
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        # ==========================
        # TIME
        # ==========================

        time_frame = tk.Frame(
            info_frame,
            bg="#f7f9fb",
        )

        time_frame.pack(
            side="left",
            padx=25,
            pady=12,
        )

        tk.Label(
            time_frame,
            text="TIME",
            font=("Segoe UI", 7, "bold"),
            bg="#f7f9fb",
            fg="#7f8c8d",
        ).pack(
            anchor="w",
        )

        tk.Label(
            time_frame,
            text=str(schedule.time),
            font=("Segoe UI", 9, "bold"),
            bg="#f7f9fb",
            fg="#2c3e50",
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        # ==========================
        # PROCEEDING
        # ==========================

        proceeding_frame = tk.Frame(
            info_frame,
            bg="#f7f9fb",
        )

        proceeding_frame.pack(
            side="left",
            fill="x",
            expand=True,
            padx=25,
            pady=12,
        )

        tk.Label(
            proceeding_frame,
            text="PROCEEDING",
            font=("Segoe UI", 7, "bold"),
            bg="#f7f9fb",
            fg="#7f8c8d",
        ).pack(
            anchor="w",
        )

        proceeding_label = tk.Label(
            proceeding_frame,
            text=str(schedule.proceeding),
            font=("Segoe UI", 9, "bold"),
            bg="#f7f9fb",
            fg="#2c3e50",
            anchor="w",
            justify="left",
            wraplength=500,
        )

        proceeding_label.pack(
            anchor="w",
            fill="x",
            pady=(2, 0),
        )

        # ==========================
        # CLICK EVENTS
        # ==========================

        self.bind_all_children(
            card,
            schedule.id,
        )

    # ==========================
    # BIND CHILDREN
    # ==========================

    def bind_all_children(self, widget, schedule_id):

        widget.bind(
            "<Button-1>",
            lambda event, sid=schedule_id: self.select_card(sid),
        )

        for child in widget.winfo_children():

            self.bind_all_children(
                child,
                schedule_id,
            )

    # ==========================
    # SELECT CARD
    # ==========================

    def select_card(self, schedule_id):

        self.selected_id = schedule_id

        for item in self.cards:

            card = item["card"]

            if item["id"] == schedule_id:

                card.configure(
                    highlightthickness=2,
                    highlightbackground="#2e75b6",
                )

            else:

                card.configure(
                    highlightthickness=1,
                    highlightbackground="#dce3e9",
                )

    # ==========================
    # SHOW EMPTY
    # ==========================

    def show_empty(self):

        empty_card = tk.Frame(
            self.cards_frame,
            bg="white",
            highlightthickness=1,
            highlightbackground="#dce3e9",
        )

        empty_card.pack(
            fill="x",
            padx=2,
            pady=25,
        )

        tk.Label(
            empty_card,
            text="No Cases Found",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#1f4e79",
        ).pack(
            pady=(35, 5),
        )

        tk.Label(
            empty_card,
            text="There are currently no schedules in this list.",
            font=("Segoe UI", 9),
            bg="white",
            fg="#7f8c8d",
        ).pack(
            pady=(0, 35),
        )

    # ==========================
    # CHANGE STATUS
    # ==========================

    def change_status(self, status):

        if not self.selected_id:

            return

        if self.manager:

            self.manager.update_status(
                self.selected_id,
                status,
            )

        self.refresh()

    # ==========================
    # REFRESH
    # ==========================

    def refresh(self):

        self.load_data()

    # ==========================
    # SHOW
    # ==========================

    def show(self):

        self.frame.pack(
            fill="both",
            expand=True,
        )

    # ==========================
    # HIDE
    # ==========================

    def hide(self):

        self.frame.pack_forget()