# views/dashboard_pages/overdue_frame.py

from views.dashboard_pages.case_list_frame import CaseListFrame


class OverdueFrame(CaseListFrame):

    def __init__(self, parent, manager, back_command=None):

        schedules = manager.get_overdue_cases()

        super().__init__(
            parent, "⚠ Overdue Hearing Cases", schedules, back_command, manager
        )
