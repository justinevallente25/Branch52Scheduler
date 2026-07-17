import tkinter as tk
from tkinter import ttk
from datetime import datetime



class DashboardUI:


    def __init__(
        self,
        parent,
        manager,
        open_schedule
    ):

        self.manager = manager

        self.open_schedule = open_schedule


        self.frame = tk.Frame(
            parent,
            bg="#eef2f7"
        )


        self.frame.pack(
            fill="both",
            expand=True
        )


        self.create_ui()

        self.update_clock()



    def create_ui(self):


        # ==========================
        # HEADER
        # ==========================

        header = tk.Frame(
            self.frame,
            bg="#eef2f7"
        )


        header.pack(
            fill="x",
            padx=30,
            pady=(25,10)
        )



        tk.Label(
            header,
            text="Dashboard",
            bg="#eef2f7",
            fg="#003366",
            font=(
                "Segoe UI",
                24,
                "bold"
            )
        ).pack(
            side="left"
        )



        self.clock_label = tk.Label(
            header,
            text="",
            bg="#eef2f7",
            fg="#555",
            font=(
                "Segoe UI",
                11
            )
        )


        self.clock_label.pack(
            side="right"
        )



        tk.Label(
            self.frame,
            text="Court Proceedings Overview",
            bg="#eef2f7",
            fg="#666",
            font=(
                "Segoe UI",
                11
            )
        ).pack(
            anchor="w",
            padx=30
        )



        # ==========================
        # SUMMARY CARDS
        # ==========================

        cards = tk.Frame(
            self.frame,
            bg="#eef2f7"
        )


        cards.pack(
            fill="x",
            padx=30,
            pady=25
        )



        self.today_value = self.create_card(
            cards,
            "Today's Hearings",
            len(
                self.manager.get_today_cases()
            )
        )



        self.upcoming_value = self.create_card(
            cards,
            "Upcoming Cases",
            len(
                self.manager.get_upcoming_cases()
            )
        )



        self.total_value = self.create_card(
            cards,
            "Total Cases",
            self.manager.get_total_cases()
        )



        # ==========================
        # QUICK ACTION BUTTONS
        # ==========================

        action_frame = tk.Frame(
            self.frame,
            bg="#eef2f7"
        )


        action_frame.pack(
            fill="x",
            padx=30,
            pady=(0,15)
        )



        tk.Button(
            action_frame,
            text="+ New Schedule",
            bg="#003366",
            fg="white",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            width=18,
            command=self.open_schedule
        ).pack(
            side="left",
            padx=5
        )



        tk.Button(
            action_frame,
            text="Refresh",
            bg="#2E8B57",
            fg="white",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            width=18,
            command=self.refresh_dashboard
        ).pack(
            side="left",
            padx=5
        )



        # ==========================
        # TABLE TITLE
        # ==========================


        tk.Label(
            self.frame,
            text="Today's Schedule",
            bg="#eef2f7",
            fg="#003366",
            font=(
                "Segoe UI",
                15,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=30
        )



        self.create_table()



    # ==========================
    # CARD
    # ==========================


    def create_card(
        self,
        parent,
        title,
        value
    ):


        card = tk.Frame(
            parent,
            bg="white",
            width=220,
            height=120,
            relief="solid",
            bd=1
        )


        card.pack(
            side="left",
            padx=10
        )


        card.pack_propagate(
            False
        )



        tk.Label(
            card,
            text=title,
            bg="white",
            fg="#555",
            font=(
                "Segoe UI",
                10,
                "bold"
            )
        ).pack(
            pady=(20,5)
        )



        value_label = tk.Label(
            card,
            text=value,
            bg="white",
            fg="#003366",
            font=(
                "Segoe UI",
                25,
                "bold"
            )
        )


        value_label.pack()



        return value_label



    # ==========================
    # TABLE
    # ==========================


    def create_table(self):


        table_frame = tk.Frame(
            self.frame,
            bg="white"
        )


        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )



        columns = (

            "case_no",
            "complainant",
            "respondent",
            "time",
            "proceeding"

        )



        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )



        headings = {

            "case_no":"Case No",

            "complainant":"Complainant",

            "respondent":"Respondent",

            "time":"Time",

            "proceeding":"Proceeding"

        }



        for column in columns:


            self.table.heading(
                column,
                text=headings[column]
            )


            self.table.column(
                column,
                width=150
            )



        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )


        self.table.configure(
            yscrollcommand=scrollbar.set
        )


        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.table.pack(
            fill="both",
            expand=True
        )


        self.load_today_schedule()



    # ==========================
    # LOAD TODAY
    # ==========================


    def load_today_schedule(self):


        for row in self.table.get_children():

            self.table.delete(row)



        schedules = self.manager.get_today_cases()



        for s in schedules:


            self.table.insert(

                "",

                "end",

                values=(

                    s.case_no,

                    s.complainant,

                    s.respondent,

                    s.time,

                    s.proceeding

                )

            )



    # ==========================
    # REFRESH
    # ==========================


    def refresh_dashboard(self):


        self.today_value.config(
            text=len(
                self.manager.get_today_cases()
            )
        )


        self.upcoming_value.config(
            text=len(
                self.manager.get_upcoming_cases()
            )
        )


        self.total_value.config(
            text=self.manager.get_total_cases()
        )


        self.load_today_schedule()



    # ==========================
    # CLOCK
    # ==========================


    def update_clock(self):


        now = datetime.now()


        self.clock_label.config(
            text=now.strftime(
                "%A, %B %d, %Y | %I:%M:%S %p"
            )
        )


        self.frame.after(
            1000,
            self.update_clock
        )