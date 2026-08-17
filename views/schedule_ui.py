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
        self.WARNING = "#f39c12"

        self.BACKGROUND = "#eef2f7"

        self.WHITE = "#ffffff"
        self.TEXT = "#2c3e50"

        self.create_ui()

        self.load_data()

    # ==========================
    # CREATE UI
    # ==========================

    def create_ui(self):

        self.frame = tk.Frame(
            self.parent,
            bg=self.BACKGROUND
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        # ======================
        # HEADER
        # ======================

        header = tk.Frame(
            self.frame,
            bg=self.PRIMARY,
            height=60
        )

        header.pack(
            fill="x"
        )

        title = tk.Label(
            header,
            text="⚖ Court Hearing Schedule System",
            font=("Segoe UI", 20, "bold"),
            bg=self.PRIMARY,
            fg="white"
        )

        title.pack(
            pady=12
        )

        # ======================
        # FORM CARD
        # ======================

        form_card = tk.Frame(
            self.frame,
            bg=self.WHITE,
            bd=1,
            relief="solid"
        )

        form_card.pack(
            padx=25,
            pady=15,
            fill="x"
        )

        form_header = tk.Label(
            form_card,
            text="📋 Hearing Information",
            font=("Segoe UI", 13, "bold"),
            bg=self.SECONDARY,
            fg="white",
            anchor="w",
            padx=15
        )

        form_header.pack(
            fill="x"
        )

        form = tk.Frame(
            form_card,
            bg=self.WHITE
        )

        form.pack(
            fill="x",
            padx=20,
            pady=15
        )

        form.grid_columnconfigure(
            0,
            weight=1
        )

        form.grid_columnconfigure(
            1,
            weight=1
        )

        # ======================
        # LEFT SIDE
        # ======================

        left = tk.Frame(
            form,
            bg=self.WHITE
        )

        left.grid(
            row=0,
            column=0,
            padx=20,
            sticky="nsew"
        )

        self.case_entry = self.create_entry(
            left,
            "📄 NLRC Case No:",
            0
        )

        self.complainant_entry = self.create_text_entry(
            left,
            "👤 Complainant:",
            1
        )

        self.respondent_entry = self.create_text_entry(
            left,
            "👤 Respondent:",
            2
        )

        # ======================
        # RIGHT SIDE
        # ======================

        right = tk.Frame(
            form,
            bg=self.WHITE
        )

        right.grid(
            row=0,
            column=1,
            padx=20,
            sticky="nsew"
        )

        tk.Label(
            right,
            text="📅 Date:",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

        self.date_entry = DateEntry(
            right,
            width=22,
            date_pattern="yyyy-mm-dd",
            font=("Segoe UI", 10)
        )

        self.date_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=8,
            sticky="w"
        )

        self.date_entry.bind(
            "<<DateEntrySelected>>",
            self.check_selected_date
        )

        self.time_entry = self.create_entry(
            right,
            "⏰ Time:",
            1
        )

        tk.Label(
            right,
            text="⚖ Proceeding:",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=5,
            pady=8
        )

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
                "Rejoinder",
                "Mandatory Conference(Zoom)"
            ]
        )

        self.proceeding.grid(
            row=2,
            column=1,
            padx=5,
            pady=8,
            sticky="w"
        )

        self.holiday_label = tk.Label(
            right,
            text="",
            bg=self.WHITE,
            fg=self.DANGER,
            font=("Segoe UI", 9, "bold"),
            wraplength=300,
            justify="left"
        )

        self.holiday_label.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="w",
            padx=5,
            pady=5
        )

        # ======================
        # BUTTONS
        # ======================

        buttons = tk.Frame(
            self.frame,
            bg=self.BACKGROUND
        )

        buttons.pack(
            pady=10
        )

        button_style = {
            "font": ("Segoe UI", 10, "bold"),
            "fg": "white",
            "relief": "flat",
            "width": 15,
            "cursor": "hand2"
        }

        tk.Button(
            buttons,
            text="➕ Add Schedule",
            bg=self.SUCCESS,
            command=self.add,
            **button_style
        ).grid(
            row=0,
            column=0,
            padx=8
        )

        tk.Button(
            buttons,
            text="✏ Update",
            bg=self.SECONDARY,
            command=self.update,
            **button_style
        ).grid(
            row=0,
            column=1,
            padx=8
        )

        tk.Button(
            buttons,
            text="🗑 Delete",
            bg=self.DANGER,
            command=self.delete,
            **button_style
        ).grid(
            row=0,
            column=2,
            padx=8
        )

        tk.Button(
            buttons,
            text="↻ Clear",
            bg="#7f8c8d",
            command=self.clear,
            **button_style
        ).grid(
            row=0,
            column=3,
            padx=8
        )

        # ======================
        # SCHEDULE CARD
        # ======================

        table_card = tk.Frame(
            self.frame,
            bg=self.WHITE,
            bd=1,
            relief="solid"
        )

        table_card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        table_header = tk.Label(
            table_card,
            text="📅 Scheduled Hearings",
            font=("Segoe UI", 13, "bold"),
            bg=self.SECONDARY,
            fg="white",
            anchor="w",
            padx=15
        )

        table_header.pack(
            fill="x"
        )

        # ======================
        # SCROLLABLE CARD AREA
        # ======================

        container = tk.Frame(
            table_card,
            bg=self.WHITE
        )

        container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.canvas = tk.Canvas(
            container,
            bg=self.WHITE,
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.card_frame = tk.Frame(
            self.canvas,
            bg=self.WHITE
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.card_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.card_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_card_frame
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

    # ==========================
    # ENTRY HELPER
    # ==========================

    def create_entry(
        self,
        parent,
        text,
        row
    ):

        tk.Label(
            parent,
            text=text,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=row,
            column=0,
            sticky="nw",
            padx=5,
            pady=8
        )

        entry = tk.Entry(
            parent,
            width=32,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )

        entry.grid(
            row=row,
            column=1,
            padx=5,
            pady=8,
            sticky="w"
        )

        return entry

    # ==========================
    # TEXT ENTRY HELPER
    # ==========================

    def create_text_entry(
        self,
        parent,
        text,
        row
    ):

        tk.Label(
            parent,
            text=text,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=row,
            column=0,
            sticky="nw",
            padx=5,
            pady=8
        )

        entry = tk.Text(
            parent,
            width=32,
            height=3,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            wrap="word"
        )

        entry.grid(
            row=row,
            column=1,
            padx=5,
            pady=8,
            sticky="w"
        )

        return entry

    # ==========================
    # UPDATE SCROLL REGION
    # ==========================

    def update_scroll_region(
        self,
        event=None
    ):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # ==========================
    # RESIZE CARD FRAME
    # ==========================

    def resize_card_frame(
        self,
        event
    ):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    # ==========================
    # MOUSE WHEEL
    # ==========================

    def on_mousewheel(
        self,
        event
    ):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # ==========================
    # LOAD DATA
    # ==========================

    def load_data(self):

        for widget in self.card_frame.winfo_children():

            widget.destroy()

        schedules = list(
            reversed(self.manager.schedules)
        )

        if not schedules:

            tk.Label(
                self.card_frame,
                text="📭 No scheduled hearings.",
                bg=self.WHITE,
                fg="#7f8c8d",
                font=("Segoe UI", 12, "bold")
            ).pack(
                pady=40
            )

            return

        for schedule in schedules:

            self.create_schedule_card(
                schedule
            )

    # ==========================
    # CREATE SCHEDULE CARD
    # ==========================

    def create_schedule_card(
        self,
        schedule
    ):

        card = tk.Frame(
            self.card_frame,
            bg=self.WHITE,
            bd=1,
            relief="solid",
            cursor="hand2"
        )

        card.pack(
            fill="x",
            padx=10,
            pady=6
        )

        # ======================
        # STATUS COLOR
        # ======================

        status_color = self.SECONDARY

        if schedule.status == "Completed":

            status_color = self.SUCCESS

        elif schedule.status == "Not Attended":

            status_color = self.DANGER

        elif schedule.status == "Pending":

            status_color = self.WARNING

        # ======================
        # STATUS BAR
        # ======================

        tk.Frame(
            card,
            bg=status_color,
            width=8
        ).pack(
            side="left",
            fill="y"
        )

        content = tk.Frame(
            card,
            bg=self.WHITE
        )

        content.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=12
        )

        # ======================
        # TOP ROW
        # ======================

        top = tk.Frame(
            content,
            bg=self.WHITE
        )

        top.pack(
            fill="x"
        )

        tk.Label(
            top,
            text=f"#{schedule.id}",
            bg=self.WHITE,
            fg=status_color,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left"
        )

        case_label = tk.Label(
            top,
            text=schedule.case_no or "No Case Number",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            justify="left",
            wraplength=500
        )

        case_label.pack(
            side="left",
            padx=15,
            fill="x",
            expand=True
        )

        time_label = tk.Label(
            top,
            text=schedule.time,
            bg=self.WHITE,
            fg=self.PRIMARY,
            font=("Segoe UI", 11, "bold")
        )

        time_label.pack(
            side="right"
        )

        # ======================
        # COMPLAINANT
        # ======================

        complainant_label = tk.Label(
            content,
            text=schedule.complainant,
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 12, "bold"),
            anchor="w",
            justify="left",
            wraplength=700
        )

        complainant_label.pack(
            fill="x",
            pady=(8, 0)
        )

        # ======================
        # RESPONDENT
        # ======================

        respondent_label = tk.Label(
            content,
            text=f"vs. {schedule.respondent}",
            bg=self.WHITE,
            fg="#7f8c8d",
            font=("Segoe UI", 10),
            anchor="w",
            justify="left",
            wraplength=700
        )

        respondent_label.pack(
            fill="x"
        )

        # ======================
        # BOTTOM INFORMATION
        # ======================

        info = tk.Frame(
            content,
            bg=self.WHITE
        )

        info.pack(
            fill="x",
            pady=(10, 0)
        )

        date_label = tk.Label(
            info,
            text=f"📅 {schedule.date}",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 9)
        )

        date_label.pack(
            side="left",
            padx=(0, 20)
        )

        proceeding_label = tk.Label(
            info,
            text=f"⚖ {schedule.proceeding}",
            bg=self.WHITE,
            fg=self.TEXT,
            font=("Segoe UI", 9),
            anchor="w",
            justify="left",
            wraplength=500
        )

        proceeding_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        status_label = tk.Label(
            info,
            text=schedule.status,
            bg=status_color,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=3
        )

        status_label.pack(
            side="right"
        )

        # ======================
        # CLICK CARD
        # ======================

        self.bind_card_click(
            card,
            schedule
        )

    # ==========================
    # BIND CARD CLICK
    # ==========================

    def bind_card_click(
        self,
        widget,
        schedule
    ):

        widget.bind(
            "<Button-1>",
            lambda event, s=schedule:
            self.select_card(s)
        )

        for child in widget.winfo_children():

            child.bind(
                "<Button-1>",
                lambda event, s=schedule:
                self.select_card(s)
            )

            if child.winfo_children():

                self.bind_card_click(
                    child,
                    schedule
                )

    # ==========================
    # SELECT CARD
    # ==========================

    def select_card(
        self,
        schedule
    ):

        self.selected_id = schedule.id

        self.case_entry.delete(
            0,
            tk.END
        )

        self.case_entry.insert(
            0,
            schedule.case_no
        )

        self.complainant_entry.delete(
            "1.0",
            tk.END
        )

        self.complainant_entry.insert(
            "1.0",
            schedule.complainant
        )

        self.respondent_entry.delete(
            "1.0",
            tk.END
        )

        self.respondent_entry.insert(
            "1.0",
            schedule.respondent
        )

        self.date_entry.set_date(
            schedule.date
        )

        self.time_entry.delete(
            0,
            tk.END
        )

        self.time_entry.insert(
            0,
            schedule.time
        )

        self.proceeding.set(
            schedule.proceeding
        )

        self.check_selected_date()

    # ==========================
    # CHECK HOLIDAY
    # ==========================

    def check_selected_date(
        self,
        event=None
    ):

        selected_date = self.date_entry.get()

        if self.holiday_manager.is_holiday(
            selected_date
        ):

            holiday = self.holiday_manager.get_holiday_name(
                selected_date
            )

            self.holiday_label.config(
                text=f"⚠ Holiday: {holiday}"
            )

        else:

            self.holiday_label.config(
                text=""
            )

    # ==========================
    # ADD
    # ==========================

    def add(self):

        schedule = Schedule(
            self.manager.generate_id(),
            self.case_entry.get(),
            self.complainant_entry.get(
                "1.0",
                tk.END
            ).strip(),
            self.respondent_entry.get(
                "1.0",
                tk.END
            ).strip(),
            self.date_entry.get(),
            self.time_entry.get(),
            self.proceeding.get()
        )

        self.manager.add(
            schedule
        )

        self.load_data()

        self.clear()

    # ==========================
    # UPDATE
    # ==========================

    def update(self):

        if self.selected_id is None:

            messagebox.showwarning(
                "Warning",
                "Select a record first"
            )

            return

        schedule = Schedule(
            self.selected_id,
            self.case_entry.get(),
            self.complainant_entry.get(
                "1.0",
                tk.END
            ).strip(),
            self.respondent_entry.get(
                "1.0",
                tk.END
            ).strip(),
            self.date_entry.get(),
            self.time_entry.get(),
            self.proceeding.get()
        )

        self.manager.update(
            self.selected_id,
            schedule
        )

        self.load_data()

        self.clear()

    # ==========================
    # DELETE
    # ==========================

    def delete(self):

        if self.selected_id is None:

            return

        confirm = messagebox.askyesno(
            "Delete",
            "Delete selected schedule?"
        )

        if confirm:

            self.manager.delete(
                self.selected_id
            )

            self.load_data()

            self.clear()

    # ==========================
    # CLEAR
    # ==========================

    def clear(self):

        self.selected_id = None

        self.case_entry.delete(
            0,
            tk.END
        )

        self.complainant_entry.delete(
            "1.0",
            tk.END
        )

        self.respondent_entry.delete(
            "1.0",
            tk.END
        )

        self.time_entry.delete(
            0,
            tk.END
        )

        self.proceeding.set(
            ""
        )

        self.holiday_label.config(
            text=""
        )