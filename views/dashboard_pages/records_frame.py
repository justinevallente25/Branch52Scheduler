# views/dashboard_pages/records_frame.py

from views.dashboard_pages.case_list_frame import CaseListFrame


class RecordsFrame(CaseListFrame):

    def __init__(self, parent, manager, back_command=None):

        schedules = manager.get_calendar_records()

        super().__init__(
            parent, "🗂 Completed / Not Attended Records", schedules, back_command
        )
