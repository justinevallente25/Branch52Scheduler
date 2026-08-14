# views/dashboard_components/status_menu.py

import tkinter as tk


class DashboardStatusMenu:

    def __init__(self, parent, manager, refresh_dashboard):

        self.parent = parent

        self.manager = manager

        self.refresh_dashboard = refresh_dashboard

        self.table = None

        self.selected_id = None

    # ==========================
    # SET TABLE
    # ==========================

    def set_table(self, table):

        self.table = table

    # ==========================
    # RIGHT CLICK MENU
    # ==========================

    def show(self, event):

        row = self.table.identify_row(event.y)

        if not row:

            return

        self.table.selection_set(row)

        values = self.table.item(row)["values"]

        self.selected_id = values[0]

        menu = tk.Menu(self.parent, tearoff=0)

        menu.add_command(
            label="✅ Mark Completed", command=lambda: self.change_status("Completed")
        )

        menu.add_command(
            label="❌ Mark Not Attended",
            command=lambda: self.change_status("Not Attended"),
        )

        menu.add_command(
            label="⏳ Mark Pending", command=lambda: self.change_status("Pending")
        )

        menu.post(event.x_root, event.y_root)

    # ==========================
    # CHANGE STATUS
    # ==========================

    def change_status(self, status):

        self.manager.update_status(self.selected_id, status)

        self.refresh_dashboard()

    # ==========================
    # CHANGE STATUS BY ID
    # ==========================

    def change_status_by_id(self, schedule_id, status):

        self.manager.update_status(schedule_id, status)

        self.refresh_dashboard()
