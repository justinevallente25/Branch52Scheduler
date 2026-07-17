import tkinter as tk
from tkinter import ttk
import threading
import time



class LoadingScreen:


    def __init__(
        self,
        root,
        callback
    ):

        self.root = root
        self.callback = callback


        self.window = tk.Toplevel(
            root
        )


        self.window.title(
            "Loading"
        )


        self.window.geometry(
            "450x250"
        )


        self.window.configure(
            bg="#eef2f7"
        )


        self.window.resizable(
            False,
            False
        )


        self.window.overrideredirect(
            True
        )


        self.center()


        self.create_ui()


        threading.Thread(
            target=self.load,
            daemon=True
        ).start()



    def center(self):

        self.window.update_idletasks()


        x = (
            self.window.winfo_screenwidth()
            -
            450
        ) // 2


        y = (
            self.window.winfo_screenheight()
            -
            250
        ) // 2


        self.window.geometry(
            f"450x250+{x}+{y}"
        )



    def create_ui(self):


        card = tk.Frame(
            self.window,
            bg="white",
            padx=30,
            pady=25,
            relief="solid",
            bd=1
        )


        card.pack(
            expand=True
        )



        tk.Label(
            card,
            text="⚖",
            bg="white",
            fg="#003366",
            font=(
                "Segoe UI",
                30
            )
        ).pack()



        tk.Label(
            card,
            text="Branch 52 Proceedings Scheduler",
            bg="white",
            fg="#003366",
            font=(
                "Segoe UI",
                14,
                "bold"
            )
        ).pack()



        self.status = tk.Label(
            card,
            text="Starting system...",
            bg="white",
            fg="#555",
            font=(
                "Segoe UI",
                10
            )
        )


        self.status.pack(
            pady=10
        )



        self.progress = ttk.Progressbar(
            card,
            length=280,
            mode="determinate"
        )


        self.progress.pack()



    def update_progress(
        self,
        text,
        value
    ):


        self.status.config(
            text=text
        )


        self.progress["value"] = value




    def load(self):


        steps = [

            (
                "Loading schedule manager...",
                30
            ),

            (
                "Checking schedule data...",
                60
            ),

            (
                "Preparing interface...",
                90
            ),

            (
                "System ready",
                100
            )

        ]



        for text,value in steps:


            self.window.after(
                0,
                self.update_progress,
                text,
                value
            )


            time.sleep(
                0.7
            )



        self.window.after(
            500,
            self.finish
        )



    def finish(self):

        self.window.destroy()


        self.callback()