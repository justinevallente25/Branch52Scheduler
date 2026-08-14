import tkinter as tk

from views.dashboard_components.header import DashboardHeader
from views.dashboard_components.cards import DashboardCards
from views.dashboard_components.actions import DashboardActions
from views.dashboard_components.table import DashboardTable
from views.dashboard_components.status_menu import DashboardStatusMenu
from views.dashboard_components.clock import DashboardClock
from views.dashboard_pages.today_frame import TodayFrame
from views.dashboard_pages.upcoming_frame import UpcomingFrame
from views.dashboard_pages.pending_frame import PendingFrame
from views.dashboard_pages.overdue_frame import OverdueFrame
from views.dashboard_pages.records_frame import RecordsFrame


class DashboardUI:

    def __init__(self, parent, manager, open_schedule, show_dashboard):

        self.manager = manager

        self.open_schedule = open_schedule

        self.show_dashboard = show_dashboard

        # COLORS

        self.PRIMARY = "#1f4e79"
        self.SECONDARY = "#2e75b6"
        self.SUCCESS = "#2e8b57"
        self.DANGER = "#c0392b"
        self.WARNING = "#f39c12"

        self.BACKGROUND = "#eef2f7"
        self.WHITE = "#ffffff"
        self.TEXT = "#2c3e50"

        self.frame = tk.Frame(parent, bg=self.BACKGROUND)

        self.frame.pack(fill="both", expand=True)

        self.colors = {
            "PRIMARY": self.PRIMARY,
            "SECONDARY": self.SECONDARY,
            "SUCCESS": self.SUCCESS,
            "DANGER": self.DANGER,
            "WARNING": self.WARNING,
            "BACKGROUND": self.BACKGROUND,
            "WHITE": self.WHITE,
            "TEXT": self.TEXT,
        }

        self.create_ui()

    # ==========================
    # CREATE UI
    # ==========================

    def create_ui(self):

        self.header = DashboardHeader(self.frame, self.PRIMARY)

        clock_label = self.header.create()

        self.cards = DashboardCards(
            self.frame, self.manager, self.colors, self.open_card_page
        )

        self.cards.create(self.frame)

        self.actions = DashboardActions(
            self.frame, self.open_schedule, self.refresh_dashboard, self.colors
        )

        self.actions.create()

        self.status_menu = DashboardStatusMenu(
            self.frame, self.manager, self.refresh_dashboard
        )

        self.table = DashboardTable(
            self.frame, self.manager, self.status_menu, self.colors
        )

        table = self.table.create()

        self.status_menu.set_table(table)

        self.clock = DashboardClock(self.frame, clock_label)

        self.clock.update()

    # ==========================
    # REFRESH DASHBOARD
    # ==========================

    def refresh_dashboard(self):

        self.cards.refresh()

        self.table.load_schedule()

    # ==========================
    # OPEN CARD PAGE
    # ==========================

    def open_card_page(self, title):

        page = None

        if title == "📅 Today's":

            page = TodayFrame(self.frame, self.manager, self.show_dashboard)

        elif title == "🔔 Upcoming":

            page = UpcomingFrame(self.frame, self.manager, self.show_dashboard)

        elif title == "⏳ Pending":

            page = PendingFrame(self.frame, self.manager, self.show_dashboard)

        elif title == "⚠ Overdue":

            page = OverdueFrame(self.frame, self.manager, self.show_dashboard)

        elif title == "🗂 Records":

            page = RecordsFrame(self.frame, self.manager, self.show_dashboard)

        elif title == "📂 Total Cases":

            from views.dashboard_pages.case_list_frame import CaseListFrame

            page = CaseListFrame(
                self.frame, "📂 All Cases", self.manager.schedules, self.show_dashboard
            )

        if page:

            self.hide_dashboard()

            page.show()

    # ==========================
    # HIDE DASHBOARD
    # ==========================

    def hide_dashboard(self):

        for widget in self.frame.winfo_children():

            widget.pack_forget()
