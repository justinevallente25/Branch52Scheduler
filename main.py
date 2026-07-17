import tkinter as tk


from controllers.schedule_manager import ScheduleManager


from views.dashboard_ui import DashboardUI
from views.schedule_ui import ScheduleUI
from views.navbar import Navbar

from views.loading_screen import LoadingScreen





class Application:


    def __init__(
        self,
        root
    ):


        self.root = root



        self.root.title(
            "Court Proceedings Scheduler"
        )



        self.root.geometry(
            "1200x700"
        )


        self.center_window()



        self.root.configure(
            bg="#eef2f7"
        )



        self.manager = ScheduleManager()



        self.main_frame = tk.Frame(
            self.root,
            bg="#eef2f7"
        )


        self.main_frame.pack(
            fill="both",
            expand=True
        )



        self.show_dashboard()





    def center_window(self):


        self.root.update_idletasks()



        width = 1200

        height = 700



        x = (
            self.root.winfo_screenwidth()
            -
            width
        ) // 2



        y = (
            self.root.winfo_screenheight()
            -
            height
        ) // 2



        self.root.geometry(
            f"{width}x{height}+{x}+{y}"
        )





    def clear_page(self):


        for widget in self.main_frame.winfo_children():

            widget.destroy()





    def show_dashboard(self):


        self.clear_page()



        layout = tk.Frame(
            self.main_frame,
            bg="#eef2f7"
        )


        layout.pack(
            fill="both",
            expand=True
        )



        Navbar(
            layout,
            self
        )



        DashboardUI(
            layout,
            self.manager
        )





    def show_schedule(self):


        self.clear_page()



        layout = tk.Frame(
            self.main_frame,
            bg="#eef2f7"
        )


        layout.pack(
            fill="both",
            expand=True
        )



        Navbar(
            layout,
            self
        )



        ScheduleUI(
            layout,
            self.manager
        )







def start_application():


    root = tk.Tk()



    app = Application(
        root
    )



    root.deiconify()



    root.mainloop()







if __name__ == "__main__":



    root = tk.Tk()



    root.withdraw()



    LoadingScreen(
        root,
        start_application
    )



    root.mainloop()