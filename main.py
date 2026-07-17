import tkinter as tk


from controllers.schedule_manager import ScheduleManager
from controllers.settings_manager import SettingsManager
from controllers.holiday_manager import HolidayManager


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



        # ==========================
        # CONTROLLERS
        # ==========================


        self.manager = ScheduleManager()

        self.settings = SettingsManager()

        self.holiday_manager = HolidayManager()



        # ==========================
        # WINDOW SETTINGS
        # ==========================


        self.root.title(

            self.settings.get(
                "system_name"
            )

        )



        self.root.geometry(
            "1200x700"
        )


        self.center_window()



        self.root.configure(
            bg="#eef2f7"
        )



        # ==========================
        # MAIN FRAME
        # ==========================


        self.main_frame = tk.Frame(

            self.root,

            bg="#eef2f7"

        )


        self.main_frame.pack(

            fill="both",

            expand=True

        )



        self.show_dashboard()





    # ==========================
    # CENTER WINDOW
    # ==========================


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





    # ==========================
    # CLEAR PAGE
    # ==========================


    def clear_page(self):


        for widget in self.main_frame.winfo_children():


            widget.destroy()





    # ==========================
    # DASHBOARD
    # ==========================


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

            self.manager,

            self.show_schedule

        )







    # ==========================
    # SCHEDULE
    # ==========================


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

            self.manager,

            self.holiday_manager

        )







# ==========================
# START APPLICATION
# ==========================


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