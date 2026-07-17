import tkinter as tk
from tkinter import ttk



class DashboardUI:


    def __init__(
        self,
        parent,
        manager
    ):

        self.manager = manager


        self.frame = tk.Frame(
            parent,
            bg="#eef2f7"
        )


        self.frame.pack(
            fill="both",
            expand=True
        )


        self.create_ui()



    def create_ui(self):


        # HEADER

        tk.Label(
            self.frame,
            text="Dashboard",
            bg="#eef2f7",
            fg="#003366",
            font=(
                "Segoe UI",
                24,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=30,
            pady=(25,10)
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



        # CARDS

        cards = tk.Frame(
            self.frame,
            bg="#eef2f7"
        )


        cards.pack(
            fill="x",
            padx=30,
            pady=25
        )



        self.create_card(
            cards,
            "Today's Hearings",
            len(
                self.manager.get_today_cases()
            )
        )


        self.create_card(
            cards,
            "Upcoming Cases",
            len(
                self.manager.get_upcoming_cases()
            )
        )


        self.create_card(
            cards,
            "Total Cases",
            self.manager.get_total_cases()
        )



        # TABLE TITLE

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



        tk.Label(
            card,
            text=value,
            bg="white",
            fg="#003366",
            font=(
                "Segoe UI",
                25,
                "bold"
            )
        ).pack()



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



        self.table.pack(
            fill="both",
            expand=True
        )



        self.load_today_schedule()



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