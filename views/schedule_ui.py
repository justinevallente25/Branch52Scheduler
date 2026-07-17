import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from models.schedule import Schedule



class ScheduleUI:


    def __init__(
        self,
        parent,
        manager
    ):

        self.manager = manager

        self.selected_id = None


        self.PRIMARY = "#1f4e79"
        self.SECONDARY = "#2e75b6"
        self.SUCCESS = "#2e8b57"
        self.DANGER = "#c0392b"
        self.BACKGROUND = "#eef2f7"


        self.frame = tk.Frame(
            parent,
            bg=self.BACKGROUND
        )

        self.frame.pack(
            fill="both",
            expand=True
        )


        self.setup_style()

        self.build_ui()

        self.refresh()



    # ================= STYLE =================


    def setup_style(self):

        style = ttk.Style()

        style.theme_use(
            "clam"
        )


        style.configure(
            "Treeview",
            rowheight=38,
            font=(
                "Segoe UI",
                10
            ),
            background="white",
            fieldbackground="white"
        )


        style.configure(
            "Treeview.Heading",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            background=self.PRIMARY,
            foreground="white"
        )


        style.map(
            "Treeview",
            background=[
                (
                    "selected",
                    self.SECONDARY
                )
            ],
            foreground=[
                (
                    "selected",
                    "white"
                )
            ]
        )


        style.configure(
            "Action.TButton",
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            padding=8
        )



    # ================= UI =================


    def build_ui(self):


        # HEADER

        header = tk.Frame(
            self.frame,
            bg=self.PRIMARY,
            height=70
        )


        header.pack(
            fill="x"
        )


        title = tk.Label(
            header,
            text="📅 Court Proceedings Scheduler",
            bg=self.PRIMARY,
            fg="white",
            font=(
                "Segoe UI",
                22,
                "bold"
            )
        )


        title.pack(
            padx=20,
            pady=15,
            anchor="w"
        )



        # FORM CARD


        form = tk.Frame(
            self.frame,
            bg="white",
            padx=30,
            pady=20,
            relief="solid",
            bd=1
        )


        form.pack(
            fill="x",
            padx=20,
            pady=15
        )


        for i in range(6):

            form.grid_rowconfigure(
                i,
                minsize=42
            )



        def create_label(text,row):

            tk.Label(
                form,
                text=text,
                bg="white",
                fg="#444",
                font=(
                    "Segoe UI",
                    10,
                    "bold"
                )
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=5
            )



        def create_entry():

            return tk.Entry(
                form,
                width=60,
                font=(
                    "Segoe UI",
                    11
                ),
                relief="flat",
                bd=5,
                highlightthickness=1,
                highlightbackground="#cccccc"
            )



        create_label(
            "NLRC Case No",
            0
        )


        self.case_no = create_entry()

        self.case_no.grid(
            row=0,
            column=1
        )



        create_label(
            "Complainant",
            1
        )


        self.complainant = create_entry()

        self.complainant.grid(
            row=1,
            column=1
        )



        create_label(
            "Respondent",
            2
        )


        self.respondent = create_entry()

        self.respondent.grid(
            row=2,
            column=1
        )



        create_label(
            "Hearing Date",
            3
        )


        self.date = DateEntry(
            form,
            width=18,
            date_pattern="yyyy-mm-dd",
            font=(
                "Segoe UI",
                11
            )
        )


        self.date.grid(
            row=3,
            column=1,
            sticky="w"
        )
                # TIME


        create_label(
            "Time",
            4
        )


        time_frame = tk.Frame(
            form,
            bg="white"
        )


        time_frame.grid(
            row=4,
            column=1,
            sticky="w"
        )



        self.hour = ttk.Combobox(
            time_frame,
            values=[
                f"{x:02}"
                for x in range(1,13)
            ],
            width=5,
            state="readonly"
        )


        self.hour.set(
            "09"
        )


        self.hour.pack(
            side="left"
        )



        tk.Label(
            time_frame,
            text=":",
            bg="white",
            font=(
                "Segoe UI",
                11,
                "bold"
            )
        ).pack(
            side="left"
        )



        self.minute = ttk.Combobox(
            time_frame,
            values=[
                f"{x:02}"
                for x in range(60)
            ],
            width=5,
            state="readonly"
        )


        self.minute.set(
            "30"
        )


        self.minute.pack(
            side="left"
        )



        self.ampm = ttk.Combobox(
            time_frame,
            values=[
                "AM",
                "PM"
            ],
            width=5,
            state="readonly"
        )


        self.ampm.set(
            "AM"
        )


        self.ampm.pack(
            side="left",
            padx=5
        )



        create_label(
            "Proceeding",
            5
        )


        self.proceeding = ttk.Combobox(
            form,
            values=[
                "1st Mandatory Conference",
                "2nd Mandatory Conference",
                "Settlement",
                "Reply",
                "Execution Conference",
                "Position Paper"
            ],
            width=42,
            state="readonly"
        )


        self.proceeding.set(
            "Settlement"
        )


        self.proceeding.grid(
            row=5,
            column=1
        )



        # BUTTON AREA


        action_frame = tk.Frame(
            self.frame,
            bg=self.BACKGROUND
        )


        action_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )



        buttons = [

    (
        "➕ ADD",
        self.add
    ),

    (
        "✏ UPDATE",
        self.update
    ),

    (
        "🗑 DELETE",
        self.delete
    ),

    (
        "↻ RESET",
        self.clear
    ),

    (
        "🔄 REFRESH",
        self.refresh
    )

]



        for text,cmd in buttons:


            ttk.Button(
                action_frame,
                text=text,
                style="Action.TButton",
                command=cmd
            ).pack(
                side="left",
                padx=5
            )



        search_frame = tk.Frame(
            action_frame,
            bg=self.BACKGROUND
        )


        search_frame.pack(
            side="right"
        )



        self.search_box = tk.Entry(
            search_frame,
            width=25,
            font=(
                "Segoe UI",
                11
            )
        )


        self.search_box.pack(
            side="left",
            padx=5
        )



        ttk.Button(
            search_frame,
            text="🔍 SEARCH",
            style="Action.TButton",
            command=self.search
        ).pack(
            side="left"
        )



        # TABLE


        table_frame = tk.Frame(
            self.frame,
            bg="white",
            relief="solid",
            bd=1
        )


        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )



        self.tree = ttk.Treeview(

            table_frame,

            columns=(

                "id",
                "case",
                "date",
                "party",
                "time",
                "type"

            ),

            show="headings"

        )



        headings = {

            "id":"",
            "case":"CASE NO",
            "date":"DATE",
            "party":"PARTIES",
            "time":"TIME",
            "type":"PROCEEDING"

        }



        for col in self.tree["columns"]:

            self.tree.heading(
                col,
                text=headings[col]
            )



        self.tree.column(
            "id",
            width=0,
            stretch=False
        )


        self.tree.column(
            "case",
            width=150
        )


        self.tree.column(
            "date",
            width=130
        )


        self.tree.column(
            "party",
            width=350
        )


        self.tree.column(
            "time",
            width=120
        )


        self.tree.column(
            "type",
            width=220
        )



        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )


        self.tree.configure(
            yscrollcommand=scrollbar.set
        )


        scrollbar.pack(
            side="right",
            fill="y"
        )


        self.tree.pack(
            fill="both",
            expand=True
        )



        self.tree.tag_configure(
            "odd",
            background="#f5f8fc"
        )


        self.tree.tag_configure(
            "even",
            background="white"
        )



        self.tree.bind(
            "<ButtonRelease-1>",
            self.select
        )



    # ================= CRUD =================


    def add(self):

        if not self.validate():
            return


        schedule = Schedule(

            self.manager.generate_id(),

            self.case_no.get(),

            self.complainant.get(),

            self.respondent.get(),

            self.date.get(),

            self.get_time(),

            self.proceeding.get()

        )


        self.manager.add(
            schedule
        )


        self.refresh()

        self.clear()



    def update(self):

        if not self.selected_id:

            messagebox.showwarning(
                "Warning",
                "Select record first"
            )

            return



        schedule = Schedule(

            self.selected_id,

            self.case_no.get(),

            self.complainant.get(),

            self.respondent.get(),

            self.date.get(),

            self.get_time(),

            self.proceeding.get()

        )


        self.manager.update(
            self.selected_id,
            schedule
        )


        self.refresh()

        self.clear()



    def delete(self):

        if not self.selected_id:
            return


        if messagebox.askyesno(
            "Delete",
            "Delete selected schedule?"
        ):

            self.manager.delete(
                self.selected_id
            )

            self.refresh()

            self.clear()



    # ================= FUNCTIONS =================


    def validate(self):

        if not self.case_no.get().strip():

            messagebox.showwarning(
                "Required",
                "Case number required"
            )

            return False


        if not self.complainant.get().strip():

            messagebox.showwarning(
                "Required",
                "Complainant required"
            )

            return False


        if not self.respondent.get().strip():

            messagebox.showwarning(
                "Required",
                "Respondent required"
            )

            return False


        return True



    def get_time(self):

        return (
            f"{self.hour.get()}:"
            f"{self.minute.get()} "
            f"{self.ampm.get()}"
        )



    def refresh(self):

        self.tree.delete(
            *self.tree.get_children()
        )


        for index,s in enumerate(
            self.manager.schedules
        ):

            self.tree.insert(

                "",

                "end",

                values=(

                    s.id,
                    s.case_no,
                    s.date,
                    s.get_parties(),
                    s.time,
                    s.proceeding

                ),

                tags=(

                    "even"
                    if index % 2 == 0
                    else "odd"

                )

            )



    def select(self,event):

        item = self.tree.focus()


        if not item:
            return


        values = self.tree.item(
            item,
            "values"
        )


        self.selected_id = int(
            values[0]
        )


        self.case_no.delete(
            0,
            tk.END
        )

        self.case_no.insert(
            0,
            values[1]
        )



        parties = values[3].split(
            " vs "
        )


        if len(parties) == 2:

            self.complainant.delete(
                0,
                tk.END
            )

            self.complainant.insert(
                0,
                parties[0]
            )


            self.respondent.delete(
                0,
                tk.END
            )

            self.respondent.insert(
                0,
                parties[1]
            )


        self.proceeding.set(
            values[5]
        )



    def search(self):

        results = self.manager.search(
            self.search_box.get()
        )


        self.tree.delete(
            *self.tree.get_children()
        )


        for s in results:

            self.tree.insert(

                "",

                "end",

                values=(

                    s.id,
                    s.case_no,
                    s.date,
                    s.get_parties(),
                    s.time,
                    s.proceeding

                )

            )



    def clear(self):

        self.case_no.delete(
            0,
            tk.END
        )


        self.complainant.delete(
            0,
            tk.END
        )


        self.respondent.delete(
            0,
            tk.END
        )


        self.selected_id = None
        
    def refresh(self):

        self.tree.delete(
            *self.tree.get_children()
        )


        for index,s in enumerate(
            self.manager.schedules
        ):

            tag = (
                "even"
                if index % 2 == 0
                else "odd"
            )


            self.tree.insert(

                "",

                "end",

                values=(

                    s.id,
                    s.case_no,
                    s.date,
                    s.get_parties(),
                    s.time,
                    s.proceeding

                ),

                tags=(tag,)

            )